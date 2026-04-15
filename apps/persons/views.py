from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Person
from .serializers import PersonSerializer
from apps.audit.models import AuditLog
import json


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        before = PersonSerializer(instance).data
        reason = request.data.get('_edit_reason', '').strip()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        after = PersonSerializer(instance).data
        changed_fields = {
            field: {'from': before.get(field), 'to': after.get(field)}
            for field in after
            if not field.startswith('_') and str(before.get(field)) != str(after.get(field))
        }

        if changed_fields:
            AuditLog.objects.create(
                user=request.user,
                action_type='PERSON_EDIT',
                entity_type='Person',
                entity_id=instance.id,
                reason_code=(
                    f"Edited by {request.user.username}. "
                    f"Reason: {reason or 'Not provided'}. "
                    f"Fields changed: {json.dumps(changed_fields)}"
                ),
            )
        return __import__('rest_framework.response', fromlist=['Response']).Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)