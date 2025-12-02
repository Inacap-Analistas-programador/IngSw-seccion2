from rest_framework import viewsets
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from ..Serializers import Pago_serializer as MP_S
from ..Models.pago_model import *
from ..Filters.pagos_filter import PagoPersonaFilter

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = MP_S.ProveedorSerializer

class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Pago.objects.all()
    serializer_class = MP_S.ComprobantePagoSerializer

class PagoComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Pago_Comprobante.objects.all()
    serializer_class = MP_S.PagoComprobanteSerializer

class PagoPersonaViewSet(viewsets.ModelViewSet):
    """ViewSet for Pago_Persona with filtering and search enabled.

    - Uses `PagoPersonaFilter` to expose explicit filters (persona_run, curso_id, etc.).
    - Enables search across related persona fields so the frontend can use `search`.
    """
    queryset = Pago_Persona.objects.all()
    serializer_class = MP_S.PagoPersonaSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = PagoPersonaFilter
    # Allow searching by persona name, last name, run and email via `search` query param
    search_fields = [
        'per_id__per_nombres',
        'per_id__per_apelpta',
        'per_id__per_run',
        'per_id__per_mail'
    ]
    ordering_fields = ['pap_fecha_hora', 'pap_valor']

class PrepagoViewSet(viewsets.ModelViewSet):
    queryset = Prepago.objects.all()
    serializer_class = MP_S.PrepagoSerializer
