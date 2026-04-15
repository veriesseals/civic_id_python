"""
apps/civic_tasks/tasks.py

This is the central hub for all scheduled background tasks in CivicID.

How Celery tasks work:
- @shared_task decorator marks a function as a Celery task.
- Tasks can be called immediately (.delay()) or scheduled (beat).
- This file is auto-discovered because we called autodiscover_tasks()
  in civicid/celery.py.

run_daily_civic_checks():
  - Called every day at midnight by Celery Beat.
  - Finds everyone who turns 18 today.
  - Delegates to voter registration and selective service handlers.
  - Returns a summary dict so we can inspect results in Celery logs.
"""

from celery import shared_task
from datetime import date
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.civic_tasks.tasks.run_daily_civic_checks')
def run_daily_civic_checks():
    """
    Master daily task. Runs all age-triggered civic registrations.
    Fired every day at midnight UTC by Celery Beat.
    """
    today = date.today()
    logger.info(f"[CivicTasks] Running daily checks for {today}")

    results = {
        'date': str(today),
        'voter_registrations': 0,
        'selective_service_registrations': 0,
        'errors': [],
    }

    # Find all persons turning 18 today
    from apps.persons.models import Person
    turning_18 = Person.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        date_of_birth__year=today.year - 18,
        date_of_death__isnull=True,   # skip deceased
    )

    logger.info(f"[CivicTasks] Found {turning_18.count()} persons turning 18 today")

    for person in turning_18:
        # Auto voter registration
        try:
            voter_result = auto_register_voter(person)
            if voter_result:
                results['voter_registrations'] += 1
        except Exception as e:
            msg = f"Voter reg failed for Person #{person.id}: {e}"
            logger.error(f"[CivicTasks] {msg}")
            results['errors'].append(msg)

        # Auto selective service registration
        try:
            ss_result = auto_register_selective_service(person)
            if ss_result:
                results['selective_service_registrations'] += 1
        except Exception as e:
            msg = f"Selective Service reg failed for Person #{person.id}: {e}"
            logger.error(f"[CivicTasks] {msg}")
            results['errors'].append(msg)

    logger.info(f"[CivicTasks] Daily check complete: {results}")
    return results


def auto_register_voter(person):
    """
    Automatically registers an eligible person to vote.

    Eligibility for auto-registration:
    - Must be a citizen or verified naturalized citizen
    - Must be exactly 18 (guaranteed by caller)
    - Must not already be registered
    - Must not have a felony disqualification

    Returns True if newly registered, False if skipped.
    """
    from apps.voter_registration.models import VoterRegistration, VoterID
    from apps.voter_registration.serializers import check_eligibility
    from apps.naturalization.models import NaturalizationRecord
    from datetime import timedelta
    import uuid

    # Skip if already registered
    if VoterRegistration.objects.filter(person=person).exists():
        logger.info(f"[AutoVoter] Person #{person.id} already registered — skipping")
        return False

    # Check eligibility
    result = check_eligibility(person)
    if not result['eligible']:
        logger.info(f"[AutoVoter] Person #{person.id} ineligible: {result['reason']}")
        return False

    # Create registration
    reg_number = f"VR-{uuid.uuid4().hex[:8].upper()}"
    reg = VoterRegistration.objects.create(
        person=person,
        registration_number=reg_number,
        party_affiliation='UNAFFILIATED',
        state=person.place_of_birth_state or '',
        registration_date=date.today(),
        status='ACTIVE',
    )

    # Issue Voter ID (4-year expiration)
    voter_id_number = f"VID-{uuid.uuid4().hex[:10].upper()}"
    VoterID.objects.create(
        person=person,
        registration=reg,
        voter_id_number=voter_id_number,
        issue_date=date.today(),
        expiration_date=date.today().replace(year=date.today().year + 4),
        status='ACTIVE',
    )

    logger.info(f"[AutoVoter] Registered Person #{person.id} — {reg_number}")
    return True


def auto_register_selective_service(person):
    """
    Automatically registers an eligible person for Selective Service.

    Federal law (50 U.S.C. § 3802) requires registration for:
    - Male persons
    - Between ages 18-25
    - Citizens, permanent residents, documented and undocumented aliens
    - NOT: active duty military, on valid student visas, or already registered

    Returns True if newly registered, False if skipped.
    """
    from apps.selective_service.models import SelectiveServiceRegistration
    import uuid

    # Federal law applies to male persons only
    if person.gender != 'MALE':
        return False

    # Skip if already registered
    if SelectiveServiceRegistration.objects.filter(person=person).exists():
        logger.info(f"[AutoSS] Person #{person.id} already registered — skipping")
        return False

    # All citizenship statuses are eligible per federal law
    # (citizens, residents, documented AND undocumented aliens)
    ss_number = f"SS-{uuid.uuid4().hex[:10].upper()}"
    SelectiveServiceRegistration.objects.create(
        person=person,
        registration_number=ss_number,
        registration_date=date.today(),
        registration_method='AUTO_SYSTEM',
        status='ACTIVE',
    )

    logger.info(f"[AutoSS] Registered Person #{person.id} for Selective Service — {ss_number}")
    return True