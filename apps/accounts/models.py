from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Build the Custom User Model
# ----------------------------------------------

# Custom User Model with role-based access control
# ----------------------------------------------
class User(AbstractUser):
    
    # Define the different roles that a user can have in the system. This allows us to implement role-based access control, where different users have different permissions and access levels based on their assigned role.
    # ----------------------------------------------
    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Admin"),
        ("REGISTRAR", "Registrar"),
        ("DMV", "DMV"),
        ("LAW_ENFORCEMENT", "Law Enforcement"),
        ("AUDITOR", "Auditor"),
    ]
    
    # Define the role field to store the user's role in the system. This field uses the ROLE_CHOICES defined above to restrict the possible values and ensure that only valid roles can be assigned to users. The field is optional (blank=True, null=True) to allow for flexibility in user creation and management.
    # ----------------------------------------------
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )
    
    # Define a boolean field to indicate whether multi-factor authentication (MFA) is enabled for the user. This allows us to enhance the security of user accounts by requiring an additional form of authentication beyond just a password. The field defaults to False, meaning that MFA is not enabled by default for new users.
    # ----------------------------------------------
    is_mfa_enabled = models.BooleanField(default=False)
    department = models.CharField(max_length = 100, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    
    # define the string representation of the model for better readability in the admin interface and other contexts 
    # ----------------------------------------------
    def __str__(self):
        return f"{self.username} ({self.role})"