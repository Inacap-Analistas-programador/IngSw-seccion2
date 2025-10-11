from rest_framework import serializers
from . import models

serializers_dict = {}

for model_name in dir(models):
    model = getattr(models, model_name)
    try:
        if issubclass(model, models.models.Model):
            serializers_class = type(f"{model_name}Serializer", (serializers.ModelSerializer,), {
                'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})
            })
            serializers_dict[model_name] = serializers_class
    except TypeError:
        pass