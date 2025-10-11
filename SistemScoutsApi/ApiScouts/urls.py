from django.urls import path
from .views import DynamicModelViewSet

urlpatterns = [
    path('<str:model_name>/', DynamicModelViewSet.as_view({'get':'list','post':'create'})),
    path('<str:model_name>/<str:pk>/', DynamicModelViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
]
