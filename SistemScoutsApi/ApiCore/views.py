from rest_framework import viewsets
from rest_framework.response import Response
from django.apps import apps
from . import serializers

class DynamicModelViewSet(viewsets.ModelViewSet):
    """Vista dinámica que gestiona cualquier modelo del proyecto."""

    def get_serializer_class(self):
        return serializers.serializers_dict[self.kwargs['model_name']]

    def get_queryset(self):
        model = apps.get_model(self.kwargs['app_name'], self.kwargs['model_name'])
        return model.objects.all()
