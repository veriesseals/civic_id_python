from django.apps import AppConfig
 
class MarriageCertificatesConfig(AppConfig):
    name = 'apps.marriage_certificates'
    default_auto_field = 'django.db.models.BigAutoField'
 
    def ready(self):
        import apps.marriage_certificates.signals  # noqa: F401