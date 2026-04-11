from rest_framework import serializers
from .models import ImmigrationStatus

# Serializer for the ImmigrationStatus model to convert model instances
# to JSON and vice versa, including all fields
# ---------------------------------------------------------------------------

class ImmigrationStatusSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included
    # in the serialization process
    # --------------------------------------------
    class Meta:
        # Specify the model to be serialized
        # --------------------------------------------
        model = ImmigrationStatus
        # Include all fields from the model in the serialization
        # --------------------------------------------
        fields = "__all__"