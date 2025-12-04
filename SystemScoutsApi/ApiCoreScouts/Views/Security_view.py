
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from ..Models.security_model import SL
from rest_framework import serializers

# serializador para los logs, facilito
class SLS(serializers.ModelSerializer):
    un = serializers.CharField(source='us.usu_username', read_only=True)
    
    class Meta:
        model = SL
        fields = '__all__'

# viewset para ver los logs, solo admins
class SLVS(viewsets.ReadOnlyModelViewSet):
    queryset = SL.objects.all()
    serializer_class = SLS
    permission_classes = [permissions.IsAdminUser]

# vista para chequear que todo este ok
class SCV(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, rq):
        # chequeo simple de salud/seguridad
        return Response({
            "st": "ok",
            "msg": "sec mod on",
            "ip": rq.META.get('REMOTE_ADDR')
        })
