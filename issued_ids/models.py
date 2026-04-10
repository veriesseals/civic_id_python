from django.db import models
from persons.models import Person
from id_applications.models import IDApplication

# Create your models here.
# ----------------------------------------------

# IssuedID model to represent the issued IDs in the system, linked to a Person and an IDApplication
# ----------------------------------------------
class IssuedID(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("REPLACED", "Replaced"),
        ("REVOKED", "Revoked"),
    ]
    
    # ForeignKey to Person model to link the issued ID to a specific person, with cascade delete and related name for reverse lookup
    # ----------------------------------------------
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="issued_ids")
    
    # OneToOneField to IDApplication model to link the issued ID to a specific application, with cascade delete and related name for reverse lookup
    # ----------------------------------------------
    application = models.OneToOneField(IDApplication, on_delete=models.CASCADE, related_name="issued_id")
    
    # id_number is a unique identifier for the issued ID, with a maximum length of 100 characters
    # ----------------------------------------------
    id_number = models.CharField(max_length=100, unique=True)
    
    # issue_date is the date when the ID was issued, stored as a DateField
    # ----------------------------------------------
    issue_date = models.DateField()
    
    # expiration_date is the date when the ID expires, stored as a DateField
    # ----------------------------------------------
    expiration_date = models.DateField()
    
    # status indicates the current status of the issued ID, with predefined choices and a default value of "ACTIVE"
    # ----------------------------------------------
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    
    # __str__ method to provide a readable representation of the IssuedID instance, returning the id_number
    # ----------------------------------------------
    def __str__(self):
        return self.id_number