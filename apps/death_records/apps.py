"""
apps/death_records/apps.py

ready() is called once Django has fully loaded all apps.
This is the correct place to import signals — importing them
at module level causes circular import errors because the
models haven't been registered yet when the file is first read.
"""

from django.apps import AppConfig


class DeathRecordsConfig(AppConfig):
    name = 'apps.death_records'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import apps.death_records.signals  # noqa: F401