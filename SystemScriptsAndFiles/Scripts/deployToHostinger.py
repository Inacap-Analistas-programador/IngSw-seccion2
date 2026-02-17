import os
import sys
import subprocess
import time
import requests
import json

def run_command(command, cwd=None, description=None):
    """Ejecuta un comando en la terminal local y maneja errores."""
    if description:
        print(f"\n🚀 {description}...")
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✅ Éxito: {command}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar: {command}")
        print(f"   Detalle: {e.stderr.strip()}")
        return None

def main():
    print("=" * 60)
    print("🤖  DESPLIEGUE AUTOMATIZADO (SIN INTERACCIÓN)")
    print("=" * 60)
    
    # --- CONFIGURACIÓN ---
    # URL de tu endpoint de despliegue
    DEPLOY_URL = "https://api.guiasyscoutsbiobio.cl/api/deploy/"
    
    # Token de seguridad (Debe coincidir con DEPLOY_SECRET en settings.py/.env)
    # Configúralo aquí o en tus variables de entorno locales
    DEPLOY_TOKEN = os.environ.get('DEPLOY_TOKEN', 'temp-secret-change-me') 
    
    REMOTE_NAME = "origin"
    BRANCH_NAME = "main"
    # ---------------------

    # 1. Verificar estado de git local
    print("\n📦 Verificando estado del repositorio local...")
    status = run_command("git status --porcelain", description="Chequeando cambios pendientes")
    
    if status:
        print("⚠️  Detectados cambios locales.")
        commit_msg = f"Auto-deploy {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        print(f"   Realizando commit automático: '{commit_msg}'")
        run_command("git add .", description="Agregando archivos")
        run_command(f'git commit -m "{commit_msg}"', description="Realizando commit")
        run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}", description="Subiendo cambios a Git")
    else:
        print("✅ Repositorio local limpio. Asegurando sincronización con remoto...")
        run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}", description="Haciendo Push")

    # 2. Invocar Endpoint de Despliegue
    print("\n" + "=" * 60)
    print("📡 EJECUTANDO DESPLIEGUE REMOTO")
    print("=" * 60)
    print(f"URL: {DEPLOY_URL}")
    
    try:
        response = requests.get(DEPLOY_URL, params={'token': DEPLOY_TOKEN}, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ DESPLIEGUE EXITOSO (Respuesta del servidor):")
            print(f"   Estado: {data.get('status')}")
            
            steps = data.get('steps', {})
            print(f"   - Migrate:       {steps.get('migrate')}")
            print(f"   - Collectstatic: {steps.get('collectstatic')}")
            print(f"   - Restart:       {steps.get('restart')}")
            print(f"   - DB Conection:  {steps.get('db_connection')}")
            
            diag = data.get('diagnostics', {})
            print(f"\n🔍 DIAGNÓSTICO DEL SERVIDOR:")
            print(f"   DB_USER (Env):   {diag.get('DB_USER')}")
            print(f"   DB_USER (Set):   {diag.get('DB_USER_IN_SETTINGS')}")
            print(f"   USER (System):   {diag.get('USER_ENV')}")
            print(f"   .env file:       {'Existe' if diag.get('HAS_DOTENV') else 'No existe'}")
            
        elif response.status_code == 403:
            print("\n❌ Error 403: Token denegado. Verifica DEPLOY_SECRET en el servidor.")
        else:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
