from django.contrib import admin
from .models import AuditLog

# Register your models here.
# --------------------------------------------

# Register the AuditLog model with the admin site.
# ----------------------------------------
admin.site.register(AuditLog)
