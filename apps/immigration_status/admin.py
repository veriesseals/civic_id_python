from django.contrib import admin
from .models import ImmigrationStatus

# Register your models here.
# --------------------------------------------

# Register the ImmigrationStatus model with the admin site.
# ----------------------------------------
admin.site.register(ImmigrationStatus)
