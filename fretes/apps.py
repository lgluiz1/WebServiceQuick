from django.apps import AppConfig


class FretesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fretes'

    def ready(self):
        import fretes.signals  # registra o signal automaticamente