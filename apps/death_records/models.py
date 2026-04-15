"""
apps/death_records/models.py

The DeathRecord stores the official death certificate details.
When a DeathRecord is saved, a Django signal fires that:
  1. Sets Person.date_of_death
  2. Suspends VoterRegistration (status → INACTIVE)
  3. Suspends associated VoterID (status → SUSPENDED)
  4. Suspends Passport (status → SUSPENDED)
  5. Suspends SelectiveService registration (status → DECEASED)

Why signals instead of doing it in the view?
  Signals enforce the cascade no matter HOW the death record is created —
  via the API, the admin panel, or a Celery task. Views can be bypassed.
  Signals cannot.

Access: REGISTRAR and LAW_ENFORCEMENT roles only.
"""

from django.db import models
from django.conf import settings
from apps.persons.models import Person


class DeathRecord(models.Model):

    CAUSE_CATEGORY_CHOICES = [
        ("NATURAL",    "Natural Causes"),
        ("ACCIDENT",   "Accidental"),
        ("HOMICIDE",   "Homicide"),
        ("SUICIDE",    "Suicide"),
        ("UNDETERMINED", "Undetermined"),
        ("PENDING",    "Pending Investigation"),
    ]

    # ── Core link ─────────────────────────────────────────────────
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='death_record'
    )

    # ── Certificate details ───────────────────────────────────────
    certificate_number = models.CharField(max_length=100, unique=True)
    date_of_death      = models.DateField()
    time_of_death      = models.TimeField(blank=True, null=True)
    place_of_death     = models.CharField(max_length=255)
    cause_of_death     = models.TextField()
    cause_category     = models.CharField(
        max_length=20,
        choices=CAUSE_CATEGORY_CHOICES,
        default="PENDING"
    )
    manner_of_death    = models.TextField(blank=True, null=True)

    # ── Medical / official ────────────────────────────────────────
    attending_physician = models.CharField(max_length=255, blank=True, null=True)
    coroner_name        = models.CharField(max_length=255, blank=True, null=True)
    medical_examiner    = models.CharField(max_length=255, blank=True, null=True)

    # ── Funeral / disposition ─────────────────────────────────────
    funeral_home        = models.CharField(max_length=255, blank=True, null=True)
    burial_location     = models.CharField(max_length=255, blank=True, null=True)

    # ── Officer who filed the record ──────────────────────────────
    filed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='death_records_filed'
    )

    notes      = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Death Record — {self.person} ({self.date_of_death})"