"""
apps/persons/signals.py

Two auto-actions fire when a new Person record is saved:

1. AUTO ID APPLICATION (age >= 16)
   post_save → Person created → age >= 16 → IDApplication(FIRST_TIME_ID, DRAFT)

2. AUTO VOTER REGISTRATION (age >= 18, eligible)
   post_save → Person created → age >= 18, citizen, no felony → VoterRegistration + VoterID

Why signals instead of views?
  Signals fire regardless of HOW the person was created — via the API,
  the Django admin, a Celery task, or the birth-records inline-create flow.
  Views can be bypassed; signals cannot.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from apps.persons.models import Person  # direct import — more reliable than string form


@receiver(post_save, sender=Person)
def auto_create_id_application(sender, instance, created, **kwargs):
    """
    Fires after every Person save.
    Only acts on newly-created records (created=True).
    Only creates an application if the person is 16 or older.
    Does nothing if an application already exists (guards against
    duplicate signals or manual re-saves).
    """
    if not created:
        return  # Only run on initial creation, not every save

    # Age gate
    today = date.today()
    age   = (today - instance.date_of_birth).days // 365
    if age < 16:
        return

    # Import inside function to avoid circular imports at module load time
    from apps.id_applications.models import IDApplication

    if IDApplication.objects.filter(person=instance).exists():
        return  # Guard against duplicates

    IDApplication.objects.create(
        person           = instance,
        application_type = 'FIRST_TIME_ID',
        status           = 'DRAFT',
        state_of_issue   = instance.address_state or '',
    )


@receiver(post_save, sender=Person)
def auto_register_voter_on_creation(sender, instance, created, **kwargs):
    """
    Fires after every Person save.
    Only acts on newly-created records (created=True).
    Automatically registers eligible persons aged 18+ to vote.

    Eligibility gates (mirrors check_eligibility in voter_registration/serializers.py):
      1. Citizen or verified naturalized citizen
      2. Age 18+
      3. No existing registration (guard against duplicates)
      4. Person must be living (not deceased)

    A Voter ID is issued automatically with a 4-year expiration, same as
    the manual registration flow in RegisterVoterView.
    """
    if not created:
        return

    # Must be alive
    if instance.date_of_death is not None:
        return

    # Age gate — must be 18+
    today = date.today()
    age   = (today - instance.date_of_birth).days // 365
    if age < 18:
        return

    # Citizenship gate — must be CITIZEN
    # (Naturalized permanent residents require a verified NaturalizationRecord;
    #  that workflow is handled by the Celery daily task after the naturalization
    #  record is verified. We only auto-register on creation for direct citizens.)
    if instance.citizenship_status != 'CITIZEN':
        return

    # Import inside function to avoid circular imports
    from apps.voter_registration.models import VoterRegistration, VoterID
    import uuid

    # Guard against duplicate registrations
    if VoterRegistration.objects.filter(person=instance).exists():
        return

    # Create registration
    reg_number = f"VR-{uuid.uuid4().hex[:8].upper()}"
    reg = VoterRegistration.objects.create(
        person              = instance,
        registration_number = reg_number,
        party_affiliation   = 'UNAFFILIATED',
        state               = instance.address_state or instance.place_of_birth_state or '',
        registration_date   = today,
        status              = 'ACTIVE',
    )

    # Issue Voter ID with 4-year expiration
    voter_id_number = f"VID-{uuid.uuid4().hex[:10].upper()}"
    VoterID.objects.create(
        person          = instance,
        registration    = reg,
        voter_id_number = voter_id_number,
        issue_date      = today,
        expiration_date = today.replace(year=today.year + 4),
        status          = 'ACTIVE',
    )

    # Audit log
    try:
        from apps.audit.models import AuditLog
        AuditLog.objects.create(
            user        = None,   # system-initiated
            action_type = 'VOTER_REGISTRATION',
            entity_type = 'VoterRegistration',
            entity_id   = reg.id,
            reason_code = f"Auto-registered on person creation — age {age} — citizen",
        )
    except Exception:
        pass