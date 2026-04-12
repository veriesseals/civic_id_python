from django.db import models

# Create your models here.
# ----------------------------------------------

# define the Person model with fields for first name, middle name, last name, suffix, and citizenship status
# ----------------------------------------------
class Person(models.Model):
    CITIZENSHIP_STATUS_CHOICES = [
        ("CITIZEN", "Citizen"),
        ("PERMANENT_RESIDENT", "Permanent Resident"),
        ("VISA_HOLDER", "Visa Holder"),
        ("OTHER", "Other"),
    ]
    
    # define the fields for the Person model
    # ----------------------------------------------
    first_name = models.CharField(max_length = 100)
    middle_name = models.CharField(max_length = 100, blank = True, null = True)
    last_name = models.CharField(max_length = 20, blank = True, null = True)
    suffix = models.CharField(max_length = 20, blank = True, null = True)
    
    # define the fields for date of birth and place of birth with appropriate data types and constraints
    # ----------------------------------------------
    date_of_birth = models.DateField()
    place_of_birth_city = models.CharField(max_length = 100)
    place_of_birth_state = models.CharField(max_length = 100, blank = True, null = True)
    place_of_birth_country = models.CharField(max_length = 100, default = "USA")
    
    # define the citizenship status field with choices and a default value
    # ----------------------------------------------
    citizenship_status = models.CharField(max_length = 50, choices = CITIZENSHIP_STATUS_CHOICES,
    default = "CITIZEN")
    
    # define the fields for tracking the creation and last update timestamps of each Person record
    # ----------------------------------------------
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # define the string representation of the model for better readability in the admin interface and other contexts
    # ----------------------------------------------
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    