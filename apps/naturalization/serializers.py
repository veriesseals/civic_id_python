from rest_framework import serializers
from .models import NaturalizationRecord

# Serializer for the NaturalizationRecord model to convert model
# instances to JSON and vice versa, including all fields
# --------------------------------------------

class NaturalizationRecordSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included
    # in the serialization process
    # --------------------------------------------
    class Meta:
        # Specify the model to be serialized
        # --------------------------------------------
        model = NaturalizationRecord
        # Include all fields from the model in the serialization
        # --------------------------------------------
        fields = "__all__"