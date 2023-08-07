from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ParkItWebApp.accounts'

    def ready(self):
        result = super().ready()
        import ParkItWebApp.accounts.signals
        return result