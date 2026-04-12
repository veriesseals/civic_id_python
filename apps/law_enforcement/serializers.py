from rest_framework import serializers
from .models import VerificationRequest
from persons.models import Person

# MinimalPersonSerializer — privacy-first design
# Only exposes the minimum data a law enforcement
# officer needs. No sensitive fields exposed.
# ----------------------------------------------

class MinimalPersonSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Only expose the fields that are necessary for law enforcement to identify a person, while keeping sensitive information hidden. This is a key aspect of our privacy-first design, ensuring that we only share what is absolutely necessary for the task at hand.
        # ----------------------------------------------
        model = Person
        
        # Only include the fields that are essential for law enforcement to identify a person, such as their name, date of birth, and citizenship status. This helps to protect the privacy of individuals while still allowing law enforcement to perform necessary identity verifications.
        # ----------------------------------------------
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "citizenship_status",
        ]
        

# VerificationRequestSerializer — handles the incoming
# request from the officer and the outgoing response
# ----------------------------------------------

class VerificationRequestSerializer(serializers.ModelSerializer):
    
    # Nest the minimal person data in the response
    # ----------------------------------------------
    person_details = MinimalPersonSerializer(
        source = "person",
        read_only = True    
    )
    
    class Meta:
        model = VerificationRequest
        
        # Include the fields that are relevant for both the request and the response. The 'reason' field is required in the request to ensure that officers provide a justification for their lookup, while the 'status' and 'person_details' fields are included in the response to provide feedback on the outcome of the request and the details of the person being looked up.
        # ----------------------------------------------
        fields = [
            "id",
            "requested_by",
            "person",
            "person_details",
            "reason",
            "status",
            "requested_at",
        ]
        
        # These fields are set automatically by the system
        # officers cannot manually set them
        # ----------------------------------------------
        read_only_fields = [
            "id",
            "requested_by",
            "status",
            "requested_at",
            "person_details",
        ]
    