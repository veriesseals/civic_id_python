from django.contrib import admin
from .models import VerificationRequest

# Register your models here.
# ----------------------------------------------
# This allows us to view and manage verification requests through the Django admin interface, which can be useful for monitoring and auditing purposes. However, in a production environment, access to this admin interface should be tightly controlled to prevent unauthorized access to sensitive information.
# ----------------------------------------------
admin.site.register(VerificationRequest)

