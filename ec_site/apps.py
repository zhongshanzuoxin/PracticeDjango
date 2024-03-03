from django.apps import AppConfig


class EcSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ec_site'

    def ready(self):
        import ec_site.signals
