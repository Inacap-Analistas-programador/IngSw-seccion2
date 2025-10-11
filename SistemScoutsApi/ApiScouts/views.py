from rest_framework import viewsets
from . import models, serializers

class DynamicModelViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return serializers.serializers_dict[self.kwargs['model_name']]

    def get_queryset(self):
        model = getattr(models, self.kwargs['model_name'])
        return model.objects.all()
