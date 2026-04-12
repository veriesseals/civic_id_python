from rest_framework import serializers
from .models import Person

# Serializer for the Person model.
# This serializer converts Person model instances to JSON format and vice versa.
# ---------------------------------------------
class PersonSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be included in the serialization.
    # ---------------------------------------------
    class Meta:
        # Specify the model to be serialized and include all fields.
        # ---------------------------------------------
        model = Person
        fields = "__all__"