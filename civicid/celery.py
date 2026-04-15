"""
civicid/celery.py

This file bootstraps Celery for the CivicID project.

Why this file exists:
- Django doesn't know about background tasks by default.
- Celery is a separate process that runs alongside Django.
- This file tells Celery where to find Django's settings and
    which apps to scan for tasks (functions decorated with @shared_task).

How it works:
1. We set the DJANGO_SETTINGS_MODULE env variable so Celery
    uses the same settings as the Django web server.
2. We tell Celery to auto-discover tasks in every INSTALLED_APP
    by looking for a tasks.py file in each app directory.
"""

import os
from celery import Celery

# Point Celery at our Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicid.settings')

app = Celery('civicid')

# Read Celery config from Django settings (keys prefixed with CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in every installed app
app.autodiscover_tasks()