from rest_framework.routers import DefaultRouter
from ..Views.Correos_view import CorreosViewSet

router = DefaultRouter()
router.register(r'correos', CorreosViewSet, basename='correos')
