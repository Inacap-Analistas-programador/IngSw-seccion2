import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

db = settings.DATABASES['default']
print(f"ENGINE: {db['ENGINE']}")
print(f"NAME: {db['NAME']}")
print(f"USER: {db['USER']}")
print(f"HOST: {db['HOST']}")
print(f"PORT: {db['PORT']}")
