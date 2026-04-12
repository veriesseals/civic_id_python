from django.db import models
from django.conf import settings
from apps.persons.models import Person

# Create your models here.
# ----------------------------------------------------

# VerificationRequest tracks every identity lookup
# made by a law enforcement officer
# ----------------------------------------------

class VerificationRequest(models.Model):
    
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("DENIED", "Denied"),
    ]
    
    # The officer who made the request
    # ----------------------------------------------
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="verification_request"
    )
    
    # The person being looked up
    # ----------------------------------------------
    
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        related_name="verification_requests"
    )
    
    # Officer MUST provide a reason — this is the
    # privacy-first design core of the LE API
    # ----------------------------------------------
    
    reason = models.TextField()
    
    # Status of the request
    # ----------------------------------------------
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    
    # Timestamp — immutable record of when lookup occurred
    # ----------------------------------------------
    
    requested_at = models.DateTimeField(auto_now_add=True)
    
    # define the string representation of the model for better readability in the admin interface and other contexts 
    # ----------------------------------------------
    def __str__(self):
        return f"{self.requested_by} looked up {self.person} - {self.requested_at}"
