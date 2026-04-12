from django.db import models
from apps.persons.models import Person

# Create your models here.
# ------------------------------------------

# ImmigrationStatus Model
# ------------------------------------------
class ImmigrationStatus(models.Model):
    # Define the choices for immigration status types
    # ------------------------------------------ 
    STATUS_TYPE_CHOICES = [
        ("PERMANENT_RESIDENT", "Permanent Resident"),
        ("VISA_HOLDER", "Visa Holder"),
        ("OTHER_LAWFUL_STATUS", "Other Lawful Status" ),
    ]
    
    # Foreign key to the Person model
    # ------------------------------------------
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="immigration_statuses")

    # Fields for immigration status details
    # ------------------------------------------ 
    status_type = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES)
    
    # Fields for tracking the validity period
    # ------------------------------------------
    status_start_date = models.DateField()
    
    # status_end_date can be null for ongoing statuses
    # ------------------------------------------
    status_end_date = models.DateField(blank=True, null=True)
    
    # Additional fields for tracking the issuing authority and reference number
    # ------------------------------------------
    issuing_authority = models.CharField(max_length=255)
    
    # reference_number is set to "PENDING" by default and must be unique
    # ------------------------------------------
    reference_number = models.CharField(max_length=100, default="PENDING", unique=True)

    # Timestamps for record keeping
    # ------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    
    # updated_at is automatically updated to the current time whenever the record is saved
    # ------------------------------------------
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the ImmigrationStatus model
    # ------------------------------------------
    def __str__(self):
        return f"{self.person} - {self.status_type}"