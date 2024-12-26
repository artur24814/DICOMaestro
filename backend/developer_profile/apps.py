from django.apps import AppConfig


class DeveloperProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'developer_profile'

    def ready(self):
        import developer_profile.signals
