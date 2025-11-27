from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from decimal import Decimal, InvalidOperation
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
        'PER_ID__PER_NOMBRES',
        'PER_ID__PER_APELPTA',
        'PER_ID__PER_RUN',
        'PER_ID__PER_DV',
        'PER_ID__PER_MAIL'
    ]
    ordering_fields = ['PAP_FECHA_HORA', 'PAP_VALOR']

    @action(detail=False, methods=['post'], url_path='masivo')
    def create_masivo(self, request):
        """Crear pagos masivos: espera FormData o JSON con campos:
        - PER_IDS (varios)
        - PAP_MONTO (valor total)
        - CUR_ID
        - COC_ID (opcional)
        - PAP_FECHA_PAGO (opcional)
        - PAP_TIPO (1 ingreso, 2 egreso)
        """
        per_ids = request.POST.getlist('PER_IDS') or request.data.get('PER_IDS') or []
        if isinstance(per_ids, str):
            # caso cuando viene como coma-separados
            per_ids = [p.strip() for p in per_ids.split(',') if p.strip()]

        monto_total = request.POST.get('PAP_MONTO') or request.data.get('PAP_MONTO')
        if monto_total is None:
            return Response({'detail': 'PAP_MONTO (monto total) es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            monto_total = Decimal(str(monto_total))
        except (InvalidOperation, TypeError):
            return Response({'detail': 'PAP_MONTO inválido'}, status=status.HTTP_400_BAD_REQUEST)

        if not per_ids:
            return Response({'detail': 'Debe enviar PER_IDS (lista de personas)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cur_id = request.POST.get('CUR_ID') or request.data.get('CUR_ID')
            coc_id = request.POST.get('COC_ID') or request.data.get('COC_ID')
            pap_tipo = request.POST.get('PAP_TIPO') or request.data.get('PAP_TIPO') or 1
            pap_fecha = request.POST.get('PAP_FECHA_PAGO') or request.data.get('PAP_FECHA_PAGO')
            pap_tipo = int(pap_tipo)
        except Exception:
            pap_tipo = 1

        # Calcular valor por persona
        try:
            count = len(per_ids)
            valor_por_persona = (monto_total / Decimal(count)).quantize(Decimal('0.000001'))
        except Exception:
            return Response({'detail': 'Error calculando valor por persona'}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        with transaction.atomic():
            for pid in per_ids:
                try:
                    persona = Persona.objects.get(PER_ID=pid)
                except Persona.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response({'detail': f'Persona con id {pid} no existe'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    curso = Curso.objects.get(CUR_ID=cur_id) if cur_id else None
                except Curso.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response({'detail': f'Curso con id {cur_id} no existe'}, status=status.HTTP_400_BAD_REQUEST)

                pago = Pago_Persona(
                    PER_ID=persona,
                    CUR_ID=curso,
                    USU_ID=request.user if hasattr(request, 'user') and request.user and request.user.is_authenticated else None,
                    PAP_FECHA_HORA=timezone.now(),
                    PAP_TIPO=pap_tipo,
                    PAP_VALOR=valor_por_persona,
                    PAP_ESTADO=1,  # Pagado
                )
                if pap_fecha:
                    try:
                        # Dejar que el serializer/DB interprete la fecha, si es necesario
                        pago.PAP_FECHA_HORA = pap_fecha
                    except Exception:
                        pass
                if hasattr(request.FILES, 'get') and request.FILES.get('comprobante'):
                    # actualmente no hay campo para ruta de comprobante en Pago_Persona; si existiera, manejar aquí
                    pass
                pago.save()
                created.append(pago.PAP_ID)

        return Response({'created': created, 'per_persona': str(valor_por_persona)}, status=status.HTTP_201_CREATED)

class PrepagoViewSet(viewsets.ModelViewSet):
    queryset = Prepago.objects.all()
    serializer_class = MP_S.PrepagoSerializer

