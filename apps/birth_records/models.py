from django.db import models
from django.conf import settings
from persons.models import Person

# Create your models here.
# ------------------------------------------

# Model to represent a birth record, linked to a Person
class BirthRecord(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    ]
    
    # One-to-one relationship with Person model
    # ----------------------------------------------
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="birth_record")
    # Unique certificate number for each birth record
    # ----------------------------------------------
    certificate_number = models.CharField(max_length=100, unique=True)
    # Details about the birth
    # ----------------------------------------------
    hospital_name = models.CharField(max_length=255)
    # Date and time of birth
    # ----------------------------------------------
    registrar_office = models.CharField(max_length=255)
    # Date when the birth record was registered
    # ----------------------------------------------
    registration_date = models.DateField()
    
    # Verification details
    # ----------------------------------------------
    verified_by = models.ForeignKey(
        # Link to the user model who verified the birth record
        # ----------------------------------------------
        settings.AUTH_USER_MODEL,
        # If the user who verified the record is deleted, set this field to null
        # ----------------------------------------------
        on_delete=models.SET_NULL,
        # Allow this field to be null and blank since it may not be set until verification occurs
        # ----------------------------------------------
        null=True,
        # Allow this field to be blank in forms
        # ----------------------------------------------
        blank=True
        
    )
    
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default="PENDING"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.certificate_number
    


