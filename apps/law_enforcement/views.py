from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import VerificationRequest
from .serializers import VerificationRequestSerializer
from .permissions import IsLawEnforcement
from audit.models import AuditLog

# Create your views here.
# ----------------------------------------------------

# VerificationRequestView — the Law Enforcement lookup endpoint
# This is the centerpiece of CIVIC-ID's privacy design:
# - Requires authentication
# - Requires LAW_ENFORCEMENT role
# - Requires a reason before returning any data
# - Automatically logs every request to the audit trail
# ----------------------------------------------


class VerificationRequestView(generics.CreateAPIView):
    
    # Both permissions must pass — authenticated AND LE role
    # ----------------------------------------------
    permission_classes = [IsAuthenticated, IsLawEnforcement]
    serializer_class = VerificationRequestSerializer
    
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Automatically attach the requesting officer
        # to the record — they cannot spoof this
        # ----------------------------------------------
        verification = serializer.save(
            requested_by=request.user,
            status="COMPLETED"
        )
        
        # Write to audit log automatically on every
        # LE lookup — no manual step required
        # ----------------------------------------------
        AuditLog.objects.create(
            user=request.user,
            action_type="LAW_ENFORCEMENT_LOOKUP",
            entity_type="Person",
            entity_id=verification.person.id,
            reason_code=verification.reason,
        )
        
        # Return the response with minimal person data
        # ----------------------------------------------
        return Response(
            VerificationRequestSerializer(verification).data,
            status=status.HTTP_201_CREATED
        )
        
# VerificationHistoryView — lets LE officers see
# their own past lookups only, not others'
# ----------------------------------------------

class VerificationHistoryView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated, IsLawEnforcement]
    serializer_class = VerificationRequestSerializer
    
    def get_queryset(self):
        
        # Officers can only see their own lookup history
        # ----------------------------------------------
        return VerificationRequest.objects.filter(requested_by=self.request.user).order_by("-requested_at")
        
