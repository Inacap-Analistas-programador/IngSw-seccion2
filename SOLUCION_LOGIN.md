# Solución al Error de Login - Columnas Faltantes en USUARIO

## Problema
Error: `django.db.utils.OperationalError: (1054, "Unknown column 'USUARIO.USU_IS_STAFF' in 'SELECT'")`

## Solución Rápida (Opción 1 - Script Python)

### Pasos:
1. Abrir terminal en `IngSw-seccion2/SystemScoutsApi`
2. Activar entorno virtual:
   ```bash
   venv\Scripts\activate
   ```
3. Ejecutar el script:
   ```bash
   python add_usuario_columns.py
   ```
4. El script agregará automáticamente las columnas `USU_IS_STAFF` y `USU_IS_SUPERUSER`

## Solución Manual (Opción 2 - SQL Directo)

### Pasos:
1. Abrir MySQL Workbench o cualquier cliente MySQL
2. Conectarse a la base de datos del proyecto
3. Ejecutar el contenido del archivo `fix_usuario_table.sql`:
   ```sql
   ALTER TABLE USUARIO 
   ADD COLUMN USU_IS_STAFF TINYINT(1) NOT NULL DEFAULT 0;
   
   ALTER TABLE USUARIO 
   ADD COLUMN USU_IS_SUPERUSER TINYINT(1) NOT NULL DEFAULT 0;
   ```

## Resetear Contraseña del Admin (Si es necesario)

Si después de agregar las columnas aún tienes problemas para iniciar sesión:

1. Abrir terminal en `IngSw-seccion2/SystemScoutsApi`
2. Activar entorno virtual:
   ```bash
   venv\Scripts\activate
   ```
3. Abrir shell de Django:
   ```bash
   python manage.py shell
   ```
4. Copiar y pegar en la shell:
   ```python
   from ApiCoreScouts.models.usuario_model import Usuario

   try:
       usuario = Usuario.objects.get(USU_USERNAME='admin')
       print(f"Usuario encontrado: {usuario}")
       # Cambiar contraseña
       usuario.set_password('admin')
       usuario.save()
       print("Contraseña actualizada")
   except Usuario.DoesNotExist:
       print("El usuario no existe")
   ```
5. Presionar Enter dos veces
6. Salir con `exit()`

## Credenciales de Acceso

Después de aplicar la solución, usar:
- **Usuario:** admin
- **Contraseña:** admin

## Iniciar el Sistema

1. **Backend:**
   ```bash
   cd SystemScoutsApi
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Frontend:**
   ```bash
   cd SystemScoutsClient
   npm run dev
   ```

3. Acceder a: http://localhost:5173/

## Notas Técnicas

- Las columnas `USU_IS_STAFF` y `USU_IS_SUPERUSER` son requeridas por Django para el sistema de autenticación
- El modelo `Usuario` extiende `AbstractBaseUser` y `PermissionsMixin` de Django
- Estas columnas permiten distinguir usuarios administradores de usuarios regulares
