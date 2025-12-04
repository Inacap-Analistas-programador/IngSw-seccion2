import os
import django
from django.test import RequestFactory as rf
from rest_framework import status
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Views.Health_view import CheckView as cv

def test_health_check():
    factory = rf()
    request = factory.get('/api/health/')
    view = cv.as_view()
    response = view(request)
    
    print(f"Codigo de estado: {response.status_code}")
    print(f"Contenido: {response.data}")

if __name__ == "__main__":
    test_health_check()
