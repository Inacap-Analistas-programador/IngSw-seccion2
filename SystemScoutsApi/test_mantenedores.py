import sys
import os
import django

sys.path.append(r"d:\IngSw-seccion2\SystemScoutsApi")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SystemScoutsApi.settings")
django.setup()

from ApiCoreScouts.Models.mantenedor_model import Region, Rol
from ApiCoreScouts.Serializers.Mantenedor_serializer import RegionSerializer

r = Region.objects.first()
if r:
    print(RegionSerializer(r).data)
else:
    print("No regiones")

rol = Rol.objects.first()
if rol:
    from ApiCoreScouts.Serializers.Mantenedor_serializer import RolSerializer
    print(RolSerializer(rol).data)
