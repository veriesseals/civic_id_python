"""
Changes from original:
- Added gender field (required for Selective Service federal law)
- Added maiden_name (for marriage certificate name tracking)
- Added date_of_death (triggers cascades via Django signal)
- Added photo (current profile photo)
- Added address fields (street, city, state, zip) for SSN/SS records

Why date_of_death on Person instead of a separate model?
  Having it on Person makes it trivial to filter all queries
  system-wide with date_of_death__isnull=True. A separate model
  would require joins everywhere. The DeathRecord app stores the
  full certificate details — Person just holds the date as a flag.
"""

from django.db import models

class Person(models.Model):

    CITIZENSHIP_STATUS_CHOICES = [
        ("CITIZEN",             "Citizen"),
        ("PERMANENT_RESIDENT",  "Permanent Resident"),
        ("VISA_HOLDER",         "Visa Holder"),
        ("UNDOCUMENTED_ALIEN",  "Undocumented Alien"),
        ("OTHER",               "Other"),
    ]

    GENDER_CHOICES = [
        ("MALE",   "Male"),
        ("FEMALE", "Female"),
        ("OTHER",  "Other / Not Specified"),
    ]

    # ── Identity ─────────────────────────────────────────────────
    first_name  = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name   = models.CharField(max_length=100, blank=True, null=True)
    maiden_name = models.CharField(max_length=100, blank=True, null=True,
                                   help_text="Birth surname before any name change")
    suffix      = models.CharField(max_length=20, blank=True, null=True)

    gender      = models.CharField(max_length=20, choices=GENDER_CHOICES,
                                   default="OTHER")

    # ── Birth ─────────────────────────────────────────────────────
    date_of_birth         = models.DateField()
    place_of_birth_city   = models.CharField(max_length=100)
    place_of_birth_state  = models.CharField(max_length=100, blank=True, null=True)
    place_of_birth_country = models.CharField(max_length=100, default="USA")

    # ── Death (populated by DeathRecord signal) ───────────────────
    date_of_death = models.DateField(blank=True, null=True,
                                     help_text="Set by DeathRecord — triggers cascade suspensions")

    # ── Citizenship ───────────────────────────────────────────────
    citizenship_status = models.CharField(
        max_length=50,
        choices=CITIZENSHIP_STATUS_CHOICES,
        default="CITIZEN"
    )

    # ── Address ───────────────────────────────────────────────────
    address_street = models.CharField(max_length=255, blank=True, null=True)
    address_city   = models.CharField(max_length=100, blank=True, null=True)
    address_state  = models.CharField(max_length=50,  blank=True, null=True)
    address_zip    = models.CharField(max_length=20,   blank=True, null=True)

    # ── Profile photo ─────────────────────────────────────────────
    # Current photo only — full history in PersonPhoto model
    photo = models.ImageField(upload_to='person_photos/', blank=True, null=True)

    # ── Timestamps ────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    @property
    def is_deceased(self):
        return self.date_of_death is not None

    @property
    def full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        if self.last_name:
            parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return ' '.join(parts)