# SystemScoutsApi/ApiAuth/apps.py
from django.apps import AppConfig

class ApiAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SystemScoutsApi.ApiAuth'
    verbose_name = 'API Auth'
