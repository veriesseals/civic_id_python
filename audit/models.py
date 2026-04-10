from django.db import models
from django.conf import settings

# Create your models here.
# ------------------------------------------

# AuditLog model to track user actions and changes in the system
# ------------------------------------------
class AuditLog(models.Model):
    # Using settings.AUTH_USER_MODEL to reference the user model, allowing for custom user models
    # ------------------------------------------ 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # action_type can be used to specify the type of action performed (e.g., 'create', 'update', 'delete')
    # ------------------------------------------
    action_type = models.CharField(max_length=255)
    
    # entity_type can be used to specify the type of entity affected by the action (e.g., 'User', 'Profile', 'Post')
    # ------------------------------------------
    entity_type = models.CharField(max_length=100)
    
    # entity_id can be used to specify the ID of the entity affected by the action
    # ------------------------------------------
    entity_id = models.PositiveIntegerField()
    
    # reason_code can be used to specify a reason for the action, if applicable (e.g., 'user_request', 'admin_action')
    # ------------------------------------------
    reason_code = models.CharField(max_length=255, blank=True, null=True)
    
    # timestamp will automatically set the time when the log entry is created
    # ------------------------------------------
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # __str__ method to provide a readable representation of the log entry
    # ------------------------------------------
    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.timestamp}"


