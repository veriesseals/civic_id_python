"""
apps/death_records/signals.py

Django signals are like event listeners.
post_save fires AFTER a model is saved to the database.

When a DeathRecord is created:
1. Update Person.date_of_death
2. Suspend voter registration + voter ID
3. Suspend passport
4. Suspend selective service (if exists)
5. Write to audit log

This runs automatically no matter how the DeathRecord was created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DeathRecord


@receiver(post_save, sender=DeathRecord)
def handle_death_record(sender, instance, created, **kwargs):
    if not created:
        return  # Only trigger on new records, not updates

    person = instance.person

    # 1. Mark person as deceased
    person.date_of_death = instance.date_of_death
    person.save(update_fields=['date_of_death'])

    # 2. Suspend voter registration
    try:
        reg = person.voter_registration
        reg.status = 'INACTIVE'
        reg.notes  = f"Deceased — Death Record #{instance.certificate_number}"
        reg.save(update_fields=['status', 'notes'])

        # Suspend voter ID
        if hasattr(reg, 'voter_id'):
            reg.voter_id.status = 'SUSPENDED'
            reg.voter_id.save(update_fields=['status'])
    except Exception:
        pass  # Person may not have been registered

    # 3. Suspend passport
    try:
        passport = person.passport
        passport.status = 'SUSPENDED'
        passport.notes  = f"Deceased — Death Record #{instance.certificate_number}"
        passport.save(update_fields=['status', 'notes'])
    except Exception:
        pass

    # 4. Suspend Selective Service
    try:
        ss = person.selective_service
        ss.status = 'DECEASED'
        ss.save(update_fields=['status'])
    except Exception:
        pass

    # 5. Audit log
    try:
        from apps.audit.models import AuditLog
        AuditLog.objects.create(
            user=instance.filed_by,
            action_type="DEATH_RECORD_FILED",
            entity_type="Person",
            entity_id=person.id,
            reason_code=f"Death recorded — {instance.date_of_death} — {instance.cause_category}",
        )
    except Exception:
        pass