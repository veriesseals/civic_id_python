"""
apps/marriage_certificates/models.py

A marriage links TWO Person records together.
It handles:
  - Linking spouse_1 and spouse_2 (both must exist in the system)
  - Recording the name change (who changed their name to what)
  - Automatically updating the voter registration surname display

Why store both maiden_name and last_name on Person?
  After marriage, Person.last_name = new surname.
  Person.maiden_name = original surname.
  The voter roll shows: "Jane Smith (born Doe)"
  Searches for either "Smith" or "Doe" find the same person.

The signal on save:
  1. Updates Person.last_name to new_last_name if a name change occurred
  2. Stores old name in Person.maiden_name
  3. Updates AuditLog
"""

from django.db import models
from django.conf import settings
from apps.persons.models import Person


class MarriageCertificate(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE",   "Active / Married"),
        ("DIVORCED", "Divorced"),
        ("ANNULLED", "Annulled"),
        ("WIDOWED",  "Widowed"),
    ]

    # ── The two spouses ───────────────────────────────────────────
    spouse_1 = models.ForeignKey(
        Person, on_delete=models.PROTECT,
        related_name='marriages_as_spouse_1'
    )
    spouse_2 = models.ForeignKey(
        Person, on_delete=models.PROTECT,
        related_name='marriages_as_spouse_2'
    )

    # ── Certificate details ───────────────────────────────────────
    certificate_number  = models.CharField(max_length=100, unique=True)
    date_of_marriage    = models.DateField()
    place_of_marriage   = models.CharField(max_length=255)
    officiant_name      = models.CharField(max_length=255, blank=True, null=True)
    officiant_title     = models.CharField(max_length=100, blank=True, null=True)
    witness_1_name      = models.CharField(max_length=255, blank=True, null=True)
    witness_2_name      = models.CharField(max_length=255, blank=True, null=True)

    # ── Name changes ──────────────────────────────────────────────
    # If spouse_1 changes their name, record the new surname here.
    # Leave blank if no name change.
    spouse_1_new_last_name = models.CharField(max_length=100, blank=True, null=True,
        help_text="New surname for spouse 1 after marriage (blank = no change)")
    spouse_2_new_last_name = models.CharField(max_length=100, blank=True, null=True,
        help_text="New surname for spouse 2 after marriage (blank = no change)")

    # ── Status ────────────────────────────────────────────────────
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    # ── Officer who filed ─────────────────────────────────────────
    filed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='marriage_certificates_filed'
    )

    notes      = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.spouse_1} & {self.spouse_2} — {self.date_of_marriage}"