from rest_framework import serializers
from .models import IssuedID

# Serializer for the IssuedID model to convert model instances to JSON and vice versa, including all fields
# ------------------------------------
class IssuedIDSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included in the serialization process
    # ------------------------------------
    class Meta:
        # Specify the model to be serialized, which is the IssuedID model
        # ------------------------------------
        model = IssuedID
        fields = "__all__"