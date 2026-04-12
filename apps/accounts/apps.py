from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    label = 'accounts'  # This sets the app label explicitly
    default_auto_field = 'django.db.models.BigAutoField'
