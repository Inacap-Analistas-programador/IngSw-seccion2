from django.contrib import admin
from . import models

for model_name in dir(models):
    model = getattr(models, model_name)
    try:
        if isinstance(model, type) and issubclass(model, models.models.Model):
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
    except TypeError:
        pass
