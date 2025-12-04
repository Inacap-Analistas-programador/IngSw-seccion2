from rest_framework.views import APIView
from rest_framework.response import Response as r
from rest_framework import status as st
from django.db import connection as cn
from django.db.utils import OperationalError

class CheckView(APIView):
    p_cl = [] # endpoint publico

    def get(self, request):
        try:
            cn.ensure_connection()
            return r({"estado": "saludable", "DB": "conectada"}, status=st.HTTP_200_OK)
        except OperationalError as e:
            return r({"estado": "desaludable", "DB": str(e)}, status=st.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return r({"estado": "desaludable", "error": str(e)}, status=st.HTTP_503_SERVICE_UNAVAILABLE)
