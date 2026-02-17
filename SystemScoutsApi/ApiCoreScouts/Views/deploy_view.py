from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
import os
import sys

@csrf_exempt
def deploy_view(request):
    """
    Endpoint para ejecutar tareas de despliegue en servidores sin SSH.
    Requiere un token de seguridad en el parámetro GET 'token'.
    """
    token = request.GET.get('token')
    
    # Verificar token de seguridad
    if not token or token != getattr(settings, 'DEPLOY_SECRET', None):
        return JsonResponse({'error': 'Unauthorized', 'message': 'Token inválido o no configurado'}, status=403)

    results = {
        'status': 'started',
        'steps': {}
    }
    
    base_dir = settings.BASE_DIR

    # 1. Instalar Dependencias (Usando installPythonPackages.py)
    try:
        # Localizar el script relativo a BASE_DIR
        # BASE_DIR = .../SystemScoutsApi
        # Script = .../SystemScriptsAndFiles/Scripts/installPythonPackages.py
        script_path = base_dir.parent / 'SystemScriptsAndFiles' / 'Scripts' / 'installPythonPackages.py'
        
        if script_path.exists():
            install_out = subprocess.check_output(
                [sys.executable, str(script_path)],
                stderr=subprocess.STDOUT,
                cwd=base_dir.parent, # Ejecutar desde la raíz del repo
                timeout=300 # Mayor tiempo para instalación
            )
            results['steps']['dependencies'] = '✅ Installed: ' + str(install_out.decode('utf-8')[-50:])
        else:
             results['steps']['dependencies'] = f'⚠️ Script not found at {script_path}'

    except subprocess.CalledProcessError as e:
        results['steps']['dependencies'] = '❌ Error installing packages'
        results['error_dependencies'] = e.output.decode('utf-8')
    except Exception as e:
        results['steps']['dependencies'] = f'❌ Error: {str(e)}'

    # 2. Ejecutar Migraciones
    try:
        # Usamos sys.executable para asegurar que usamos el mismo entorno Python
        migrate_out = subprocess.check_output(
            [sys.executable, 'manage.py', 'migrate'], 
            stderr=subprocess.STDOUT,
            cwd=base_dir,
            timeout=60 # Timeout de seguridad
        )
        results['steps']['migrate'] = '✅ ' + migrate_out.decode('utf-8').split('\n')[-2] # Última línea relevante
    except subprocess.CalledProcessError as e:
        results['steps']['migrate'] = '❌ Error'
        results['error'] = e.output.decode('utf-8')
        return JsonResponse(results, status=500)
    except Exception as e:
        results['steps']['migrate'] = f'❌ Error: {str(e)}'
        return JsonResponse(results, status=500)

    # 2. Recopilar Archivos Estáticos
    try:
        static_out = subprocess.check_output(
            [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
            stderr=subprocess.STDOUT,
            cwd=base_dir,
            timeout=60
        )
        results['steps']['collectstatic'] = '✅ Static files collected'
    except subprocess.CalledProcessError as e:
         results['steps']['collectstatic'] = f"⚠️ Warning: {e.output.decode('utf-8')[:100]}..."

    # 3. Reiniciar Aplicación (Touch passenger_wsgi.py)
    try:
        restart_file = base_dir / 'passenger_wsgi.py'
        if not restart_file.exists():
            restart_file = base_dir.parent / 'passenger_wsgi.py'
        
        if restart_file.exists():
            os.utime(str(restart_file), None)
            results['steps']['restart'] = '✅ App Restarted'
        else:
            results['steps']['restart'] = '⚠️ passenger_wsgi.py not found'
            
    except Exception as e:
        results['steps']['restart'] = f'❌ Error: {str(e)}'

    # 4. Diagnóstico de Variables de Entorno y BD
    import os
    env_vars = {
        'DB_USER': os.environ.get('DB_USER', 'NOT_SET'),
        'DB_USER_IN_SETTINGS': getattr(settings, 'DATABASES', {}).get('default', {}).get('USER'),
        'USER_ENV': os.environ.get('USER', 'NOT_SET'),
        'HAS_DOTENV': os.path.exists(os.path.join(base_dir, '.env')),
        'CWD': os.getcwd(),
    }
    results['diagnostics'] = env_vars
    
    # Probar conexión real DB
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        results['steps']['db_connection'] = "✅ Conexión Exitosa"
    except Exception as e:
        results['steps']['db_connection'] = f"❌ Fallo Conexión: {str(e)}"

    results['status'] = 'completed'
    return JsonResponse(results)
