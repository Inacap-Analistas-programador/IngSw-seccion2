from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from ..Models.persona_model import Persona
from ..Serializers.Persona_serializer import PersonaSearchSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def persona_search(request):
    q = request.query_params.get('q', '').strip()
    limit = int(request.query_params.get('limit', '20'))
    qs = Persona.objects.all()
    if q:
        # Prefer prefix search for performance; fallback to contains if needed
        qs = qs.filter(
            Q(per_rut__istartswith=q) |
            Q(per_nombres__istartswith=q) |
            Q(per_apellidos__istartswith=q)
        )
    qs = qs[:max(1, min(limit, 50))]
    data = PersonaSearchSerializer(qs, many=True).data
    return Response({"results": data, "count": len(data)})
