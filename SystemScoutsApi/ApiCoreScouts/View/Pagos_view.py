from rest_framework import viewsets
from ..Serializers import Pagos_serializers as MP_S
from ..Models.ModuloPagos import *

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
    queryset = Pago_Persona.objects.all()
    serializer_class = MP_S.PagoPersonaSerializer

class PrepagoViewSet(viewsets.ModelViewSet):
    queryset = Prepago.objects.all()
    serializer_class = MP_S.PrepagoSerializer

