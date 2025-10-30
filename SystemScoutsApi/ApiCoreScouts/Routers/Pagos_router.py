from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..View.Pagos_view import *

router = DefaultRouter()
router.register(r'proveedor', ProveedorViewSet, basename='proveedor')
router.register(r'comprobante-pago', ComprobantePagoViewSet, basename='comprobante-pago')
router.register(r'pago-comprobante', PagoComprobanteViewSet, basename='pago-comprobante')
router.register(r'pago-persona', PagoPersonaViewSet, basename='pago-persona')
router.register(r'prepago', PrepagoViewSet, basename='prepago')

urlpatterns = router.urls