from django.db import models
from django.conf import settings
from persons.models import Person

# Create your models here.
# ------------------------------------------

# Model to store naturalization records
# Each record is linked to a person and contains details about the naturalization process, including verification status and the user who verified it.
# ------------------------------------------

class NaturalizationRecord(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    ]
    
    # Link to the person who is being naturalized
    # If the person is deleted, all their naturalization records will also be deleted (CASCADE)
    # ------------------------------------------
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="naturalization_records")
    
    # Unique certificate number for each naturalization record
    # ------------------------------------------
    certificate_number = models.CharField(max_length=100, unique=True)
    
    # Date when the naturalization process was completed    
    # ------------------------------------------
    naturalization_date = models.DateField()
    
    # Location of the office where the naturalization process took place
    # ------------------------------------------
    office_location = models.CharField(max_length=255)
    
    # User who verified the naturalization record
    # ------------------------------------------
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Status of the verification process for the naturalization record
    # ------------------------------------------
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default="PENDING"
    )
    
    # Timestamp for when the naturalization record was created
    # ------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Timestamp for when the naturalization record was last updated
    # ------------------------------------------
    def __str__(self):
        return self.certificate_number