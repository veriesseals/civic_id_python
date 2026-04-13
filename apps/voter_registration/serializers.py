from rest_framework import serializers
from .models import VoterRegistration, VoterID
from apps.persons.models import Person
from apps.naturalization.models import NaturalizationRecord
from datetime import date


# ── Eligibility checker ──────────────────────────────────────────
# Runs all three eligibility gates:
#   1. Citizen or naturalized citizen
#   2. Age 18+
#   3. No active felony disqualification
# Returns a dict with eligible bool + reason if not eligible.
# ────────────────────────────────────────────────────────────────

def check_eligibility(person):
    result = {"eligible": True, "reason": None, "ineligibility_reason": None}

    # Gate 1 — Citizenship
    is_citizen = person.citizenship_status == "CITIZEN"
    is_naturalized = (
        person.citizenship_status == "PERMANENT_RESIDENT" and
        NaturalizationRecord.objects.filter(
            person=person,
            verification_status="VERIFIED"
        ).exists()
    )
    if not (is_citizen or is_naturalized):
        result["eligible"] = False
        result["reason"] = "Person is not a citizen or verified naturalized citizen."
        result["ineligibility_reason"] = "NON_CITIZEN"
        return result

    # Gate 2 — Age
    today = date.today()
    age = (today - person.date_of_birth).days // 365
    if age < 18:
        result["eligible"] = False
        result["reason"] = f"Person is {age} years old. Must be 18 or older."
        result["ineligibility_reason"] = "AGE"
        return result

    # Gate 3 — Active felony disqualification
    existing = VoterRegistration.objects.filter(person=person).first()
    if existing and existing.has_felony_record and not existing.felony_resolved:
        result["eligible"] = False
        result["reason"] = "Active felony conviction on record. Rights not yet restored."
        result["ineligibility_reason"] = "FELONY"
        return result

    return result


# ── VoterID Serializer ───────────────────────────────────────────
class VoterIDSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VoterID
        fields = "__all__"


# ── VoterRegistration Serializer ─────────────────────────────────
class VoterRegistrationSerializer(serializers.ModelSerializer):
    voter_id     = VoterIDSerializer(read_only=True)
    person_name  = serializers.SerializerMethodField()
    age          = serializers.SerializerMethodField()
    eligible     = serializers.SerializerMethodField()

    class Meta:
        model  = VoterRegistration
        fields = "__all__"
        read_only_fields = ["registration_number", "restored_by", "restored_at", "created_at", "updated_at"]

    def get_person_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name or ''}".strip()

    def get_age(self, obj):
        today = date.today()
        return (today - obj.person.date_of_birth).days // 365

    def get_eligible(self, obj):
        return check_eligibility(obj.person)["eligible"]


# ── Eligibility Check Serializer (read-only response) ────────────
class EligibilitySerializer(serializers.Serializer):
    person_id            = serializers.IntegerField()
    eligible             = serializers.BooleanField()
    reason               = serializers.CharField(allow_null=True)
    ineligibility_reason = serializers.CharField(allow_null=True)
    already_registered   = serializers.BooleanField()
    person_name          = serializers.CharField()
    citizenship_status   = serializers.CharField()
    age                  = serializers.IntegerField()


# ── Restoration Serializer ───────────────────────────────────────
class RestorationSerializer(serializers.Serializer):
    registration_id = serializers.IntegerField()
    notes           = serializers.CharField(required=False, allow_blank=True)