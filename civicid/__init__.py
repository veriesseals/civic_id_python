"""
civicid/__init__.py

Importing the Celery app here ensures it is loaded when Django starts.
Without this, the @shared_task decorator won't work because Celery
won't have been initialized before the tasks are imported.
"""

from .celery import app as celery_app

__all__ = ('celery_app',)