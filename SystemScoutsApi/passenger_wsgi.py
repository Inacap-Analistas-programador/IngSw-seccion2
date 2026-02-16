import sys
import os

# Configuración de rutas
BASE_DIR = '/home/volbiobio/api'
VENV_SITE = '/home/volbiobio/virtualenv/api/3.13/lib/python3.13/site-packages'

# Agregar paths
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, VENV_SITE)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

# Importar la aplicación WSGI
from SystemScoutsApi.wsgi import application