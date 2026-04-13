from django.db import models
from django.conf import settings
from apps.persons.models import Person

# ── VoterRegistration ────────────────────────────────────────────
# Tracks a person's voter registration status, eligibility,
# party affiliation, and any felony-based disqualifications.
# Restoration of rights is also tracked here.
# ────────────────────────────────────────────────────────────────

class VoterRegistration(models.Model):

    PARTY_CHOICES = [
        ("DEMOCRATIC",   "Democratic"),
        ("REPUBLICAN",   "Republican"),
        ("INDEPENDENT",  "Independent"),
        ("GREEN",        "Green"),
        ("LIBERTARIAN",  "Libertarian"),
        ("OTHER",        "Other"),
        ("UNAFFILIATED", "Unaffiliated"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE",      "Active"),
        ("INACTIVE",    "Inactive"),
        ("SUSPENDED",   "Suspended"),
        ("INELIGIBLE",  "Ineligible"),
        ("RESTORED",    "Restored"),
    ]

    INELIGIBILITY_CHOICES = [
        ("FELONY",      "Felony Conviction"),
        ("AGE",         "Under 18"),
        ("NON_CITIZEN", "Non-Citizen"),
        ("OTHER",       "Other"),
    ]

    # ── Core link ────────────────────────────────────────────────
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name="voter_registration"
    )

    # ── Registration details ─────────────────────────────────────
    registration_number = models.CharField(max_length=100, unique=True)
    party_affiliation   = models.CharField(max_length=50, choices=PARTY_CHOICES, default="UNAFFILIATED")
    precinct            = models.CharField(max_length=100, blank=True, null=True)
    county              = models.CharField(max_length=100, blank=True, null=True)
    state               = models.CharField(max_length=50, blank=True, null=True)
    registration_date   = models.DateField()

    # ── Status & eligibility ─────────────────────────────────────
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    ineligibility_reason = models.CharField(max_length=20, choices=INELIGIBILITY_CHOICES, blank=True, null=True)

    # ── Felony restoration tracking ──────────────────────────────
    # When rights are restored (felony resolved), this records when
    # and which officer processed the restoration.
    has_felony_record    = models.BooleanField(default=False)
    felony_resolved      = models.BooleanField(default=False)
    restored_at          = models.DateField(blank=True, null=True)
    restored_by          = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restorations_processed"
    )
    notes = models.TextField(blank=True, null=True)

    # ── Timestamps ───────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person} — {self.registration_number} ({self.status})"


# ── VoterID ──────────────────────────────────────────────────────
# Physical/digital voter ID credential, issued once a registration
# is ACTIVE. Separate from registration so IDs can expire and be
# reissued without losing the registration record.
# ────────────────────────────────────────────────────────────────

class VoterID(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE",    "Active"),
        ("EXPIRED",   "Expired"),
        ("REVOKED",   "Revoked"),
        ("SUSPENDED", "Suspended"),
    ]

    # ── Links ────────────────────────────────────────────────────
    person       = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="voter_ids")
    registration = models.OneToOneField(VoterRegistration, on_delete=models.CASCADE, related_name="voter_id")

    # ── Credential details ───────────────────────────────────────
    voter_id_number = models.CharField(max_length=100, unique=True)
    issue_date      = models.DateField()
    expiration_date = models.DateField()
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    # ── Timestamps ───────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voter ID {self.voter_id_number} — {self.person} ({self.status})"