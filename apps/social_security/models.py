"""
apps/social_security/models.py

Stores Social Security Number assignments.
Access restricted to: REGISTRAR, SUPER_ADMIN, SSA roles only.

Security notes:
- SSN is stored as plain text in dev (SQLite).
- In production you would use django-encrypted-model-fields or
  store only the last 4 digits with a hash of the full number.
- The API serializer masks the SSN: returns "***-**-1234" by default,
  full number only for SSA role.

OneToOneField on Person ensures one SSN per person (legally correct).
"""

from django.db import models
from django.conf import settings
from apps.persons.models import Person


class SocialSecurityRecord(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE",    "Active"),
        ("SUSPENDED", "Suspended"),
        ("DECEASED",  "Deceased — Benefits Ended"),
        ("REPLACED",  "Replaced / Reissued"),
    ]

    # ── Core link ─────────────────────────────────────────────────
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='social_security'
    )

    # ── SSN ───────────────────────────────────────────────────────
    ssn             = models.CharField(max_length=11, unique=True,
                                       help_text="Format: XXX-XX-XXXX")
    issue_date      = models.DateField()
    issuing_office  = models.CharField(max_length=255, default="Social Security Administration")
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    # ── Officer ───────────────────────────────────────────────────
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ssns_issued'
    )

    notes      = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SSN ***-**-{self.ssn[-4:]} — {self.person}"

    @property
    def masked_ssn(self):
        """Returns XXX-XX-1234 format for display."""
        if len(self.ssn) >= 4:
            return f"***-**-{self.ssn[-4:]}"
        return "***-**-****"