from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from ..Models.persona_model import Persona
from ..Models.mantenedor_model import Tipo_Curso, Rol, Cargo, Rama

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def personas_min(request):
    limit = int(request.query_params.get('limit', '50'))
    q = (request.query_params.get('q') or '').strip()
    qs = Persona.objects.all()
    if q:
        qs = qs.filter(per_nombres__istartswith=q)
    qs = qs.values('per_id', 'per_nombres')[:max(1, min(limit, 200))]
    data = [{'id': int(r['per_id']), 'nombre': r['per_nombres'] or ''} for r in qs]
    return Response({'results': data, 'count': len(data)})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def tipos_curso_min(request):
    limit = int(request.query_params.get('limit', '50'))
    q = (request.query_params.get('q') or '').strip()
    qs = Tipo_Curso.objects.all()
    if q:
        qs = qs.filter(tcu_descripcion__istartswith=q)
    qs = qs.values('tcu_id', 'tcu_descripcion')[:max(1, min(limit, 200))]
    data = [{'id': int(r['tcu_id']), 'nombre': r['tcu_descripcion'] or ''} for r in qs]
    return Response({'results': data, 'count': len(data)})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def roles_min(request):
    limit = int(request.query_params.get('limit', '50'))
    q = (request.query_params.get('q') or '').strip()
    qs = Rol.objects.filter(rol_vigente=True)
    if q:
        qs = qs.filter(rol_descripcion__istartswith=q)
    qs = qs.values('rol_id', 'rol_descripcion')[:max(1, min(limit, 200))]
    data = [{'id': int(r['rol_id']), 'nombre': r['rol_descripcion'] or ''} for r in qs]
    return Response({'results': data, 'count': len(data)})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def cargos_min(request):
    limit = int(request.query_params.get('limit', '50'))
    q = (request.query_params.get('q') or '').strip()
    qs = Cargo.objects.filter(car_vigente=True)
    if q:
        qs = qs.filter(car_descripcion__istartswith=q)
    qs = qs.values('car_id', 'car_descripcion')[:max(1, min(limit, 200))]
    data = [{'id': int(r['car_id']), 'nombre': r['car_descripcion'] or ''} for r in qs]
    return Response({'results': data, 'count': len(data)})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def ramas_min(request):
    limit = int(request.query_params.get('limit', '50'))
    q = (request.query_params.get('q') or '').strip()
    qs = Rama.objects.filter(ram_vigente=True)
    if q:
        qs = qs.filter(ram_descripcion__istartswith=q)
    qs = qs.values('ram_id', 'ram_descripcion')[:max(1, min(limit, 200))]
    data = [{'id': int(r['ram_id']), 'nombre': r['ram_descripcion'] or ''} for r in qs]
    return Response({'results': data, 'count': len(data)})
