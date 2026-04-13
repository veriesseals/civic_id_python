from django.contrib import admin
from .models import VoterRegistration, VoterID

@admin.register(VoterRegistration)
class VoterRegistrationAdmin(admin.ModelAdmin):
    list_display  = ["registration_number", "person", "status", "party_affiliation", "registration_date", "has_felony_record", "felony_resolved"]
    list_filter   = ["status", "party_affiliation", "has_felony_record", "felony_resolved"]
    search_fields = ["registration_number", "person__first_name", "person__last_name"]

@admin.register(VoterID)
class VoterIDAdmin(admin.ModelAdmin):
    list_display  = ["voter_id_number", "person", "status", "issue_date", "expiration_date"]
    list_filter   = ["status"]
    search_fields = ["voter_id_number", "person__first_name", "person__last_name"]