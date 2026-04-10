from django.db import models
from persons.models import Person
from id_applications.models import IDApplication

# Create your models here.
# ----------------------------------------------

class IssuedID(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("REPLACED", "Replaced"),
        ("REVOKED", "Revoked"),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="issued_ids")
    
    application = models.OneToOneField(IDApplication, on_delete=models.CASCADE, related_name="issued_id")
    
    id_number = models.CharField(max_length=100, unique=True)
    
    issue_date = models.DateField()
    
    expiration_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    
    def __str__(self):
        return self.id_number