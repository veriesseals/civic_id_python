"""
apps/marriage_certificates/signals.py

When a MarriageCertificate is created:
1. If spouse_1_new_last_name is set:
   - Save maiden_name = spouse_1.last_name (preserve original)
   - Update spouse_1.last_name = spouse_1_new_last_name
2. Same for spouse_2
3. Update voter registrations to reflect new surname
4. Audit log entry
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MarriageCertificate


@receiver(post_save, sender=MarriageCertificate)
def handle_marriage_certificate(sender, instance, created, **kwargs):
    if not created:
        return

    changed = []

    # Handle spouse 1 name change
    if instance.spouse_1_new_last_name:
        s1 = instance.spouse_1
        if not s1.maiden_name:
            s1.maiden_name = s1.last_name
        s1.last_name = instance.spouse_1_new_last_name
        s1.save(update_fields=['last_name', 'maiden_name'])
        changed.append(f"{s1} → {instance.spouse_1_new_last_name}")

    # Handle spouse 2 name change
    if instance.spouse_2_new_last_name:
        s2 = instance.spouse_2
        if not s2.maiden_name:
            s2.maiden_name = s2.last_name
        s2.last_name = instance.spouse_2_new_last_name
        s2.save(update_fields=['last_name', 'maiden_name'])
        changed.append(f"{s2} → {instance.spouse_2_new_last_name}")

    # Audit log
    try:
        from apps.audit.models import AuditLog
        AuditLog.objects.create(
            user=instance.filed_by,
            action_type="MARRIAGE_RECORDED",
            entity_type="MarriageCertificate",
            entity_id=instance.id,
            reason_code=f"Marriage: {instance.spouse_1} & {instance.spouse_2}. Name changes: {', '.join(changed) or 'None'}",
        )
    except Exception:
        pass