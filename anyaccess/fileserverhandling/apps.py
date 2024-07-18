from django.apps import AppConfig


class FileserverhandlingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fileserverhandling'

    def ready(self) -> None:
        import fileserverhandling.signals
        return super().ready()