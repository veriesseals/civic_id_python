from django.db import models
from django.conf import settings
from apps.persons.models import Person


class PersonPhoto(models.Model):

    PURPOSE_CHOICES = [
        ("REGISTRATION",   "Initial Registration"),
        ("UPDATE",         "Routine Update"),
        ("ID_RENEWAL",     "ID Renewal"),
        ("PASSPORT",       "Passport Application"),
        ("COURT_ORDER",    "Court Order"),
        ("OTHER",          "Other"),
    ]

    person     = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="photos")
    photo      = models.ImageField(upload_to='person_photos/history/')
    is_current = models.BooleanField(default=True)
    purpose    = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default="REGISTRATION")
    notes      = models.TextField(blank=True, null=True)

    # Who uploaded it and when
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='photos_uploaded'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo for {self.person} ({'current' if self.is_current else 'archived'})"

    def save(self, *args, **kwargs):
        # When saving a new current photo, demote all previous ones
        if self.is_current and not self.pk:
            PersonPhoto.objects.filter(person=self.person, is_current=True).update(is_current=False)
            # Also update the quick-access field on Person
            super().save(*args, **kwargs)
            self.person.photo = self.photo
            self.person.save(update_fields=['photo'])
        else:
            super().save(*args, **kwargs)