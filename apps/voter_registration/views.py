from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
import uuid

from .models import VoterRegistration, VoterID
from .serializers import (
    VoterRegistrationSerializer,
    VoterIDSerializer,
    EligibilitySerializer,
    RestorationSerializer,
    check_eligibility,
)
from apps.persons.models import Person
from apps.audit.models import AuditLog


# ── Helper: generate unique registration number ──────────────────
def generate_reg_number():
    return f"VR-{uuid.uuid4().hex[:8].upper()}"

def generate_voter_id_number():
    return f"VID-{uuid.uuid4().hex[:10].upper()}"


# ── VoterRegistration ViewSet (CRUD) ─────────────────────────────
class VoterRegistrationViewSet(viewsets.ModelViewSet):
    queryset           = VoterRegistration.objects.select_related("person", "restored_by").all()
    serializer_class   = VoterRegistrationSerializer
    permission_classes = [IsAuthenticated]


# ── VoterID ViewSet (CRUD) ────────────────────────────────────────
class VoterIDViewSet(viewsets.ModelViewSet):
    queryset           = VoterID.objects.select_related("person", "registration").all()
    serializer_class   = VoterIDSerializer
    permission_classes = [IsAuthenticated]


# ── Eligibility Check View ────────────────────────────────────────
# GET /api/voter/eligibility/?person_id=<id>
# Checks all three gates and returns eligibility result.
# Does NOT register — just checks.
# ────────────────────────────────────────────────────────────────
class EligibilityCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        person_id = request.query_params.get("person_id")
        if not person_id:
            return Response({"error": "person_id query param required."}, status=400)

        person = get_object_or_404(Person, pk=person_id)
        today  = date.today()
        age    = (today - person.date_of_birth).days // 365
        result = check_eligibility(person)

        already_registered = VoterRegistration.objects.filter(person=person).exists()

        return Response({
            "person_id":            person.id,
            "person_name":          f"{person.first_name} {person.last_name or ''}".strip(),
            "citizenship_status":   person.citizenship_status,
            "age":                  age,
            "eligible":             result["eligible"],
            "reason":               result["reason"],
            "ineligibility_reason": result["ineligibility_reason"],
            "already_registered":   already_registered,
        })


# ── Auto-Register View ────────────────────────────────────────────
# POST /api/voter/register/
# Body: { "person_id": 1, "party_affiliation": "UNAFFILIATED",
#         "precinct": "...", "county": "...", "state": "..." }
# Runs eligibility check, creates VoterRegistration + VoterID,
# writes audit log.
# ────────────────────────────────────────────────────────────────
class RegisterVoterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        person_id = request.data.get("person_id")
        if not person_id:
            return Response({"error": "person_id is required."}, status=400)

        person = get_object_or_404(Person, pk=person_id)

        # Check eligibility
        result = check_eligibility(person)
        if not result["eligible"]:
            return Response({
                "error":   result["reason"],
                "ineligibility_reason": result["ineligibility_reason"],
            }, status=400)

        # Already registered?
        if VoterRegistration.objects.filter(person=person).exists():
            return Response({"error": "Person is already registered to vote."}, status=400)

        # Create registration
        reg = VoterRegistration.objects.create(
            person              = person,
            registration_number = generate_reg_number(),
            party_affiliation   = request.data.get("party_affiliation", "UNAFFILIATED"),
            precinct            = request.data.get("precinct", ""),
            county              = request.data.get("county", ""),
            state               = request.data.get("state", ""),
            registration_date   = date.today(),
            status              = "ACTIVE",
        )

        # Issue Voter ID (4-year expiration)
        from datetime import timedelta
        voter_id = VoterID.objects.create(
            person          = person,
            registration    = reg,
            voter_id_number = generate_voter_id_number(),
            issue_date      = date.today(),
            expiration_date = date.today().replace(year=date.today().year + 4),
            status          = "ACTIVE",
        )

        # Audit log
        AuditLog.objects.create(
            user        = request.user,
            action_type = "VOTER_REGISTRATION",
            entity_type = "VoterRegistration",
            entity_id   = reg.id,
            reason_code = f"Registered by {request.user.username}",
        )

        return Response({
            "message":      "Voter successfully registered.",
            "registration": VoterRegistrationSerializer(reg).data,
        }, status=status.HTTP_201_CREATED)


# ── Felony Flag View ──────────────────────────────────────────────
# POST /api/voter/flag-felony/
# Body: { "registration_id": 1, "notes": "..." }
# Marks a voter as ineligible due to felony conviction.
# ────────────────────────────────────────────────────────────────
class FlagFelonyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reg_id = request.data.get("registration_id")
        if not reg_id:
            return Response({"error": "registration_id is required."}, status=400)

        reg = get_object_or_404(VoterRegistration, pk=reg_id)
        reg.status               = "INELIGIBLE"
        reg.ineligibility_reason = "FELONY"
        reg.has_felony_record    = True
        reg.felony_resolved      = False
        reg.notes                = request.data.get("notes", "")
        reg.save()

        # Suspend associated Voter ID
        if hasattr(reg, "voter_id"):
            reg.voter_id.status = "SUSPENDED"
            reg.voter_id.save()

        AuditLog.objects.create(
            user        = request.user,
            action_type = "VOTER_FELONY_FLAG",
            entity_type = "VoterRegistration",
            entity_id   = reg.id,
            reason_code = f"Felony flag applied by {request.user.username}",
        )

        return Response({
            "message":      "Voter flagged as ineligible due to felony conviction.",
            "registration": VoterRegistrationSerializer(reg).data,
        })


# ── Rights Restoration View ───────────────────────────────────────
# POST /api/voter/restore/
# Body: { "registration_id": 1, "notes": "Sentence completed" }
# Restores voting rights after felony is resolved.
# Re-activates registration and Voter ID.
# ────────────────────────────────────────────────────────────────
class RestoreRightsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reg_id = request.data.get("registration_id")
        if not reg_id:
            return Response({"error": "registration_id is required."}, status=400)

        reg = get_object_or_404(VoterRegistration, pk=reg_id)

        if not reg.has_felony_record:
            return Response({"error": "No felony record on file for this registration."}, status=400)

        if reg.felony_resolved:
            return Response({"error": "Rights have already been restored."}, status=400)

        reg.status               = "RESTORED"
        reg.felony_resolved      = True
        reg.ineligibility_reason = None
        reg.restored_at          = date.today()
        reg.restored_by          = request.user
        reg.notes                = request.data.get("notes", "")
        reg.save()

        # Reactivate Voter ID
        if hasattr(reg, "voter_id"):
            reg.voter_id.status = "ACTIVE"
            reg.voter_id.save()

        AuditLog.objects.create(
            user        = request.user,
            action_type = "VOTER_RIGHTS_RESTORED",
            entity_type = "VoterRegistration",
            entity_id   = reg.id,
            reason_code = f"Rights restored by {request.user.username}. {reg.notes}",
        )

        return Response({
            "message":      "Voting rights successfully restored.",
            "registration": VoterRegistrationSerializer(reg).data,
        })