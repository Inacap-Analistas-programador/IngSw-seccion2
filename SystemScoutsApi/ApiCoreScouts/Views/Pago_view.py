from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from rest_framework import filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from ..Serializers import Pago_serializer as MP_S
from ..Models.pago_model import *
from ..Filters.pagos_filter import PagoPersonaFilter
from ..Permissions import PerfilPermission

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = MP_S.ProveedorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Pagos'

class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = Comprobante_Pago.objects.all()
    serializer_class = MP_S.ComprobantePagoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Pagos'

class PagoComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Pago_Comprobante.objects.all()
    serializer_class = MP_S.PagoComprobanteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Pagos'

class PagoPersonaViewSet(viewsets.ModelViewSet):
    """ViewSet for Pago_Persona with filtering and search enabled.

    - Uses `PagoPersonaFilter` to expose explicit filters (persona_run, curso_id, etc.).
    - Enables search across related persona fields so the frontend can use `search`.
    """
    queryset = Pago_Persona.objects.all()
    serializer_class = MP_S.PagoPersonaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Pagos'
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

    @action(detail=False, methods=['post'])
    def masivo(self, request):
        try:
            cur_id = request.data.get('CUR_ID')
            monto_total = float(request.data.get('PAP_MONTO', 0))
            fecha = request.data.get('PAP_FECHA_PAGO')
            obs = request.data.get('PAP_OBSERVACION', '')
            tipo = request.data.get('PAP_TIPO', 1)
            
            # The frontend sends 'PER_IDS' multiple times in FormData. 
            # request.data.getlist('PER_IDS') handles this.
            per_ids = request.data.getlist('PER_IDS')
            
            if not per_ids or not cur_id or monto_total <= 0:
                 return Response({'error': 'Datos incompletos'}, status=400)
            
            valor_per = monto_total / len(per_ids)
            pagos = []
            
            # Use atomic transaction
            with transaction.atomic():
                for pid in per_ids:
                    pago = Pago_Persona.objects.create(
                        per_id_id=pid,
                        cur_id_id=cur_id,
                        usu_id_id=request.user.id if request.user and request.user.is_authenticated else 1, # Fallback to 1 if no user? Or error?
                        pap_fecha_hora=fecha,
                        pap_valor=valor_per,
                        pap_estado=1, # Pagado
                        pap_tipo=tipo,
                        pap_observacion=obs
                    )
                    pagos.append(pago.pap_id)
            
            return Response({'message': 'Pagos masivos creados', 'ids': pagos}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'])
    def transferir(self, request):
        pago_id = request.data.get('pago_id')
        nueva_per_id = request.data.get('nueva_persona_id')
        
        if not pago_id or not nueva_per_id:
            return Response({'error': 'Faltan datos'}, status=400)

        try:
            with transaction.atomic():
                original = Pago_Persona.objects.get(pap_id=pago_id)
                
                # Check if already annulled
                if original.pap_estado == 2:
                     return Response({'error': 'El pago ya está anulado'}, status=400)

                # Create new payment
                nuevp = Pago_Persona.objects.create(
                    per_id_id=nueva_per_id,
                    cur_id=original.cur_id,
                    usu_id_id=request.user.id if request.user and request.user.is_authenticated else original.usu_id_id,
                    pap_fecha_hora=original.pap_fecha_hora,
                    pap_valor=original.pap_valor,
                    pap_estado=1, # Activo
                    pap_tipo=original.pap_tipo,
                    pap_observacion=(original.pap_observacion or "") + f" [Transf. origen #{pago_id}]"
                )
                
                # Annull original
                original.pap_estado = 2 # Anulado
                original.pap_observacion = (original.pap_observacion or "") + f" [Transf. a #{nuevp.pap_id}]"
                original.save()
                
            return Response({'status': 'ok', 'nuevo_id': nuevp.pap_id})
        except Pago_Persona.DoesNotExist:
            return Response({'error': 'Pago no encontrado'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PrepagoViewSet(viewsets.ModelViewSet):
    queryset = Prepago.objects.all()
    serializer_class = MP_S.PrepagoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Pagos'

