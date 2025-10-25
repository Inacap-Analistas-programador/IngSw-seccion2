from django.contrib import admin
from .Models import ModuloUsuarios

for model_name in dir(ModuloUsuarios):
    model = getattr(ModuloUsuarios, model_name)
    try:
        if issubclass(model, ModuloUsuarios.models.Model):
            admin.site.register(model)
    except (TypeError, admin.sites.AlreadyRegistered):
        pass
