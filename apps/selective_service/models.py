"""
apps/selective_service/models.py

Federal law (50 U.S.C. § 3802) requires ALL male persons
between 18-25 to register, regardless of citizenship status.
This includes undocumented aliens.

Exemptions (tracked in this model):
- Active duty military (they register separately via DoD)
- Certain diplomatic visa holders
- Already served

Registration is auto-triggered by Celery daily task when
a qualifying person turns 18. Can also be manually registered
by REGISTRAR or SUPER_ADMIN roles.

STATUS flow:
  PENDING → ACTIVE (on confirmation)
  ACTIVE → EXEMPT (if exemption granted)
  ACTIVE → DECEASED (on death record)
  ACTIVE → DEREGISTERED (age 26+, legally removed from rolls)
"""

from django.db import models
from django.conf import settings
from apps.persons.models import Person


class SelectiveServiceRegistration(models.Model):

    STATUS_CHOICES = [
        ("PENDING",        "Pending Confirmation"),
        ("ACTIVE",         "Active"),
        ("EXEMPT",         "Exempt"),
        ("DEREGISTERED",   "Deregistered — Age 26+"),
        ("DECEASED",       "Deceased"),
    ]

    EXEMPTION_CHOICES = [
        ("ACTIVE_DUTY",    "Active Duty Military"),
        ("DIPLOMATIC",     "Diplomatic Visa"),
        ("PRIOR_SERVICE",  "Prior Military Service"),
        ("OTHER",          "Other"),
    ]

    METHOD_CHOICES = [
        ("AUTO_SYSTEM",  "Automatic — System (Age 18)"),
        ("MANUAL_STAFF", "Manual — Staff Entry"),
        ("SELF_REPORTED","Self-Reported"),
        ("POSTAL",       "Postal Registration"),
    ]

    # ── Core link ─────────────────────────────────────────────────
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='selective_service'
    )

    # ── Registration details ──────────────────────────────────────
    registration_number = models.CharField(max_length=50, unique=True)
    registration_date   = models.DateField()
    registration_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="AUTO_SYSTEM")
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    # ── Exemption (if applicable) ─────────────────────────────────
    is_exempt           = models.BooleanField(default=False)
    exemption_reason    = models.CharField(max_length=20, choices=EXEMPTION_CHOICES, blank=True, null=True)
    exemption_notes     = models.TextField(blank=True, null=True)

    # ── Deregistration (age 26) ───────────────────────────────────
    deregistered_date   = models.DateField(blank=True, null=True)

    # ── Officer ───────────────────────────────────────────────────
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='selective_service_registrations'
    )

    notes      = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SS-{self.registration_number} — {self.person} ({self.status})"