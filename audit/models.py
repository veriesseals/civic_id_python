from django.db import models
from django.conf import settings

# Create your models here.
# ------------------------------------------

class AuditLog(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    action_type = models.CharField(max_length=255)
    
    entity_type = models.CharField(max_length=100)
    
    entity_id = models.PositiveIntegerField()
    
    reason_code = models.CharField(max_length=255, blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.timestamp}"


