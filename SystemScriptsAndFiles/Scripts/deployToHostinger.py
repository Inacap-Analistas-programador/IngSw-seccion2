import os
import sys
import subprocess
import time

def run_command(command, cwd=None, description=None):
    """Ejecuta un comando en la terminal y maneja errores."""
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
    print("🤖  AUTOMATIZACIÓN DE DESPLIEGUE A HOSTINGER")
    print("=" * 60)
    
    # Configuración
    REMOTE_NAME = "origin"
    BRANCH_NAME = "main"
    
    # 1. Verificar estado de git
    print("\n📦 Verificando estado del repositorio...")
    status = run_command("git status --porcelain", description="Chequeando cambios pendientes")
    
    if status:
        print("⚠️  Tienes cambios sin confirmar. ¿Deseas hacer un commit y push automático?")
        confirm = input("   (S/N): ").strip().lower()
        
        if confirm == 's':
            commit_msg = input("   📝 Mensaje del commit: ")
            if not commit_msg:
                commit_msg = f"Despliegue automático {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            run_command("git add .", description="Agregando archivos")
            run_command(f'git commit -m "{commit_msg}"', description="Realizando commit")
            run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}", description="Subiendo cambios al repositorio remoto")
        else:
            print("🛑 Despliegue cancelado. Confirma tus cambios manualmente primero.")
            return
    else:
        print("✅ Repositorio limpio. Verificando actualizaciones remotas...")
        run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}", description="Asegurando que el remoto esté actualizado")

    # 2. Instrucciones para el servidor
    print("\n" + "=" * 60)
    print("📡 CONECTANDO CON EL SERVIDOR")
    print("=" * 60)
    print("Para completar el despliegue, el script necesita ejecutar comandos vía SSH.")
    print("Asegúrate de tener configurado el acceso SSH sin contraseña o ten la clave lista.\n")
    
    ssh_user = input("👤 Usuario SSH (ej. u123456789): ")
    ssh_host = input("🌐 Host SSH (ej. 123.456.78.90): ")
    ssh_port = input("🔌 Puerto SSH (default 65002 para Hostinger): ") or "65002"
    project_path = input("📂 Ruta del proyecto en servidor (ej. domains/midominio.com/public_html/api): ")
    
    if not all([ssh_user, ssh_host, project_path]):
        print("❌ Faltan datos de conexión. Abortando.")
        return

    # Comandos a ejecutar en el servidor
    # 1. Ir al directorio
    # 2. Activar entorno virtual (asumiendo ruta estándar de Hostinger o preguntando)
    # 3. Git pull
    # 4. Pip install requirements
    # 5. Migrate
    # 6. Collectstatic
    # 7. Reiniciar app (touch passenger_wsgi.py)
    
    venv_path = input("🐍 Ruta del entorno virtual en servidor (Enter para 'venv'): ") or "venv"
    
    remote_commands = [
        f"cd {project_path}",
        f"source {venv_path}/bin/activate" if '/' in venv_path else f"source {venv_path}/bin/activate",
        "git pull origin main",
        "pip install -r requirements.txt",
        "python manage.py migrate",
        "python manage.py collectstatic --noinput",
        "touch passenger_wsgi.py"  # Reinicia la aplicación en Passenger
    ]
    
    combined_command = " && ".join(remote_commands)
    
    ssh_cmd = f'ssh -p {ssh_port} {ssh_user}@{ssh_host} "{combined_command}"'
    
    print("\n🚀 Ejecutando despliegue remoto...")
    print(f"   Comando: {ssh_cmd}")
    
    # Ejecutar SSH
    try:
        process = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   [REMOTO] {output.strip()}")
                
        rc = process.poll()
        
        if rc == 0:
            print("\n✅ DESPLIEGUE FINALIZADO EXITOSAMENTE")
        else:
            print(f"\n❌ Error en el despliegue remoto (Código {rc})")
            print(process.stderr.read())
            
    except Exception as e:
        print(f"\n❌ Error al intentar conectar por SSH: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Operación cancelada por el usuario.")
        sys.exit(0)
