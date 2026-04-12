from django.contrib import admin
from .models import BirthRecord

# Register your models here.
# ------------------------------------------

# Register the NaturalizationRecord model with the admin site.
# ----------------------------------------
admin.site.register(BirthRecord)