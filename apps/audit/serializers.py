from rest_framework import serializers
from .models import AuditLog

# Serializer for the AuditLog model to convert model instances to JSON and vice versa, including all fields
# ------------------------------------
class AuditLogSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included in the serialization process
    # ------------------------------------
    class Meta:
        # Specify the model to be serialized, which is the AuditLog model
        # ------------------------------------
        model = AuditLog
        fields = "__all__"