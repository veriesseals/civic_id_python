from django.db import models
from django.conf import settings
from apps.persons.models import Person

# Create your models here.
# ------------------------------------------

# IDApplication Model
# ------------------------------------------
class IDApplication(models.Model):
    # Define the choices for application types and statuses
    # ------------------------------------------
    APPLICATION_TYPE_CHOICES = [
        ("FIRST_TIME_ID", "First Time ID"),
        ("RENEWAL", "Renewal"),
        ("REPLACEMENT", "Replacement"),
    ]
    
    # Define the choices for application statuses
    # ------------------------------------------
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("ISSUED", "Issued"),
    ]
    
    # Foreign key to the Person model
    # ------------------------------------------
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="id_applications")
    
    # Fields for application details
    # ------------------------------------------
    application_type = models.CharField(max_length=50, choices=APPLICATION_TYPE_CHOICES)
    
    # status is set to "DRAFT" by default when a new application is created
    # ------------------------------------------
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="DRAFT")
    
    # Timestamps for tracking application submission and review
    # ------------------------------------------
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # reviewed_by is a foreign key to the user who reviewed the application, and can be null if not yet reviewed
    # ------------------------------------------
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # reviewed_at is the timestamp for when the application was reviewed, and can be null if not yet reviewed
    # ------------------------------------------
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    # decision_reason is a text field for providing reasons for approval or rejection, and can be blank or null
    # ------------------------------------------
    decision_reason = models.TextField(blank=True, null=True)
    
    # state_of_issue is a field for tracking the state where the ID will be issued, and can be blank or null
    # ------------------------------------------
    state_of_issue = models.CharField(max_length=50, blank=True, null=True)
    
    # additional_info is a JSON field for storing any additional information related to the application, and can be blank or null
    # ------------------------------------------
    def __str__(self):
        return f"{self.person} - {self.application_type}"
