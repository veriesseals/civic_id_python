from rest_framework import serializers
from .models import BirthRecord

# Serializer for the BirthRecord model.
# This serializer converts BirthRecord model instances to JSON format and vice versa.
# ---------------------------------------------
class BirthRecordSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included in the serialization.
    # ---------------------------------------------
    class Meta:
        # Specify the model to be serialized and include all fields.
        # ---------------------------------------------
        model = BirthRecord
        fields = "__all__"