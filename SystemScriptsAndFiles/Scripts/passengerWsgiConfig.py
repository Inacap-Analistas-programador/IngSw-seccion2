import sys
import os

# Configuración de rutas
BASE_DIR = '/home/volbiobio/services'
VENV_SITE = '/home/volbiobio/virtualenv/services/3.12/lib/python3.12/site-packages'

# Agregar paths
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, VENV_SITE)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

# Importar la aplicación WSGI
from SystemScoutsApi.wsgi import application