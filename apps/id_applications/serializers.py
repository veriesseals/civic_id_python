from rest_framework import serializers
from .models import IDApplication


# Serializer for the IDApplication model.
# This serializer converts IDApplication model instances to JSON format and vice versa.
# ---------------------------------------------
class IDApplicationSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included in the serialization.
    # ---------------------------------------------
    class Meta:
        # Specify the model to be serialized and include all fields.
        # ---------------------------------------------
        model = IDApplication
        fields = "__all__"