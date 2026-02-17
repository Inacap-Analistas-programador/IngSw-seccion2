import sys
import os

# Configuracion de rutas - CORREGIDO (sin caracteres extraños)
BASE_DIR = '/home/volbiobio/api'
VENV_SITE = '/home/volbiobio/virtualenv/api/3.12/lib/python3.12/site-packages'

# Agregar paths
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, VENV_SITE)

# Activar el entorno virtual de forma manual
python_home = '/home/volbiobio/virtualenv/api/3.12'
activate_this = os.path.join(python_home, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')

# Cargar la aplicación
from SystemScoutsApi.wsgi import application