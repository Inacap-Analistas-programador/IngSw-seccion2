from rest_framework import viewsets
from ApiCore.serializers import ModuloPagosSerializers
from .models import (Concepto_Contable, Proveedor, Comprobante_Pago,
                     Pago_Comprobante, Pago_Persona, Prepago)

class ConceptoViewSet(viewsets.ModelViewSet):
    queryset = Concepto_Contable.objects.all()
    serializer_class = ModuloPagosSerializers.ConceptoContableSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ModuloPagosSerializers.ProveedorSerializer

class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Pago.objects.all()
    serializer_class = ModuloPagosSerializers.ComprobantePagoSerializer

class PagoComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Pago_Comprobante.objects.all()
    serializer_class = ModuloPagosSerializers.PagoComprobanteSerializer

class PagoPersonaViewSet(viewsets.ModelViewSet):
    queryset = Pago_Persona.objects.all()
    serializer_class = ModuloPagosSerializers.PagoPersonaSerializer

class PrepagoViewSet(viewsets.ModelViewSet):
    queryset = Prepago.objects.all()
    serializer_class = ModuloPagosSerializers.PrepagoSerializer

