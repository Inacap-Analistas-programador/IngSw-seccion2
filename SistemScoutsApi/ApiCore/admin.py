from django.contrib import admin
from . import models

for model_name in dir(models):
    model = getattr(models, model_name)
    try:
        if issubclass(model, models.models.Model):
            admin.site.register(model)
    except (TypeError, admin.sites.AlreadyRegistered):
        pass
