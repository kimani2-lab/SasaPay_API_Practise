from django.apps import AppConfig


class storageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'
    
    def ready(self):
        # import storage.signals  # noqa: F401
        pass
