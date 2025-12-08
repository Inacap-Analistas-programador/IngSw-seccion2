# 🏕️ Sistema de Scouts – Arquitectura MVC con API REST

Este proyecto implementa un **sistema de gestión para Scouts** usando  
**Django** como backend (API REST) y **Vue** como frontend.  
La comunicación se realiza mediante consultas HTTP seguras para realizar operaciones CRUD.

---

## 📚 Documentación

- **[README.md](./README.md)** - Este archivo 

---

## 🚀 Tecnologías principales
* **Python / Django** + **Django REST Framework** – API REST.
* **Vue 3 + Vite** – Cliente web.
* **Arquitectura MVC** – Separación clara entre modelo, vista y controlador.

---

## ⚙️ Requisitos previos
Asegúrate de tener instalados en tu sistema:
* [Python 3.x](https://www.python.org/downloads/)
* [Node.js (LTS)](https://nodejs.org/) (incluye npm)
* [Git](https://git-scm.com/) para clonar el repositorio
* Visual Studio Code (opcional pero recomendado)

---

## 📂 Estructura del proyecto
```
IngSw-seccion2/
│
├─ SystemScoutsApi/       # Backend Django (API REST)
├─ SystemScoutsClient/    # Frontend Vue (Vite)
└─ README.md
```

---

## 🔹 1. Clonar el repositorio (Abrir una nueva terminal)
```bash
git clone https://github.com/Inacap-Analistas-programador/IngSw-seccion2.git
cd IngSw-seccion2/SystemScoutsApi
```

---

## 🔹 2. Backend – Django API REST

### Configuración de la Base de Datos
El proyecto soporta tanto **MySQL** como **SQLite**:
- **MySQL**: Para producción (requiere archivo `.env` con credenciales)
- **SQLite**: Se usa automáticamente como fallback para desarrollo si no hay configuración MySQL

**Crear archivo `.env` (opcional para MySQL):**
```bash
cp SystemScoutsApi/.env.example SystemScoutsApi/.env
# Editar .env con tus credenciales de MySQL
```

Si no configuras MySQL, el sistema usará SQLite automáticamente (`db.sqlite3`).

### Instalación y Ejecución

1. **Crear entorno virtual de Python**
   ```bash
   python -m venv venv
   ```
2. **Activar entorno virtual**
   - Windows (PowerShell):
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar migraciones**
   ```bash
   cd SystemScoutsApi
   python manage.py migrate
   ```
5. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
6. **La API estará disponible en:**
    👉 `http://127.0.0.1:8000/`

---

# Hacer migraciones en el backend: 

1. **Debes estar en esta ruta (cd IngSw-seccion2/SystemScoutsApi):**
```powershell
python manage.py makemigrations
```
2. **Ejecutar migraciones:**
```powershell
python manage.py migrate
```
---

# En caso de tener problemas al migrar los datos, haz estos pasos:

1. **Revertir todas las migraciones de la app:**
```powershell
python manage.py migrate ApiCoreScouts zero
```
3. **Eliminar archivos de migración conflictivos**
```powershell
rm ApiCoreScouts/migrations/0002_*.py
```
4. **Crear migraciones limpias**
```powershell
python manage.py makemigrations ApiCoreScouts
```
5. **Aplicar migraciones**
```powershell
python manage.py migrate
```
# Crear super usuario (si aún no lo haz creado)

---

# Copiar y pegar el siguiente bloque de comandos en la shell de django..
# Esto creará automáticamente un perfil de aministrador con un ID
# (debes estar en esta ruta: cd IngSw-seccion2/SystemScoutsApi) 

######################################################

from ApiCoreScouts.Models.usuario_model import Perfil

perfil_admin, created = Perfil.objects.get_or_create(
    PEL_DESCRIPCION='Administrador',
    defaults={'PEL_VIGENTE': True}
)

print(f"Perfil ID creado: {perfil_admin.PEL_ID}")

######################################################

# Salir de la shell con:
```powershell
exit()
```
# Crear el superusuario con el comando:
```powershell
python manage.py createsuperuser
```
# Introducir datos para crear el super usuario con el perfil "Administrador"
USU USERNAME, Password (x2)

---

# Crear .env para conectar con Base de Datos
debes crear un archivo .env que posea los siguientes datos:
```bash
SECRET_KEY=django-insecure-@mmunrpygm35@p4d**^f34ixb%k6k5zcb^6+@v8hj3%s71
DATABASE=ssb
USER=root
PASSWORD_DB=
HOST=127.0.0.1
PORT=3306
DEBUG_API=True
```
## Crear SECRET_KEY
si no tienes una secret_key o te da problemas, intenta crear una nueva
```bash
<<<<<<< HEAD
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

<<<<<<< HEAD

```
o:
```bash
=======
>>>>>>> 7d2932d2f785da8bc0444f20a0b8b9f0563f914c
=======
>>>>>>> a3e58cb9e8bb4a71df27789f08c3212640f52ee1
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
esto te devolverá una clave, que deberás copiar y pegar en la variable **SECRET_KEY**

---

# 🛢Iniciar Base de Datos🛢
MYSQL debe estar instalado de manera global en tu PC, por lo que debes dirigirte al siguiente link

https://dev.mysql.com/downloads/installer/

debes realizar los siguientes pasos:
1. descargar mysql community que pesa +500mb
2. click donde dice ***No, gracias, solo quiero iniciar la descarga.*** (incluye: MySQL Server + Workbench + utilidades)
3. una vez iniciado el instalador, debes seleccionar mysql workbench y presionar en **ADD**
4. aparecerán dos tablas, el de la izquierda son los productos y el de la derecha son los productos que instalarás
5. debes dejar en la tabla de la derecha los productos que deseas instalar (Solo necesitas MySQL Server y MySQL Workbench, para django es suficiente)
6. luego solo continuas con la instalación de manera normal
7. luego te aparecerá el apartado *Type and Networking*
8. si te dice que el puerto está ocupado, solo cambialo a cualquiera, por ejemplo: Si el instalador dice: 3306 is already in use, cámbialo por 3307 (o el que quieras) *Ese mismo puerto debe quedar en tu archivo .env*
9. ***Accounts and Roles***: debes asignar una contraseña root (luego deberás ingresar esa contraseña en tu archivo .env)
10. Luego continuas con la instalación de manera normal

una vez instalado, comprueba esto antes con **PowerShell Administrador**:

```bash
mysql -u root -p
```

si te devuelve un error, debes escribir en el buscador de windows ***editar las variables de entorno del sistema***, dirigirte a **Variables de entorno... > path y presiona editar**
- copia la ruta de tu mysql, generalmente es esta ruta: C:\Program Files\MySQL\MySQL Server 8.0\bin
- presiona nuevo e ingresa la ruta copiada
- ahora ejecuta el codigo mostrado con anterioridad en PowerShell como administrador

una vez ejecutado, ingresa la contraseña root que habias definido en la instalación de mysql

1. crea una nueva conexión, ingresa: ***nombre***; (cualquiera), ***port***; (el que configuraste en la instalación), en ***Store in Vault...*** debes ingresar la contraseña root que definiste en la instalación
2. crea un nuevo SCHEMA
***El nombre del schema debe coincidir exactamente con el valor que pongas en NAME= dentro de tu archivo .env o settings.py.***

para comprobar que estás conectado, intenta:
- cd SystemScoutsApi
- ejecutar python manage.py makemigrations
si te dice: *No changes detected* entonces estás conectado correctamente
*Si te aparece un error del tipo “Unknown database”, revisa que el nombre del schema sea exactamente igual en Workbench y en tu .env/settings.py*

## Makemigrations y Migrate
para que se creen las tablas de los modelos, debes escribir lo siguiente (debes estar posicionado en **SystemScoutsApi**

```bash
python manage.py makemigrations ApiCoreScouts
```
si te detecta todas las tablas con sus atributos, es hora de migrar
```bash
python manage.py migrate
```
y ya tendrías todas las tablas creadas, ahora puedes empezar a trabajar con la base de datos

**NOTA: no se debe usar *XAMPP*, solo funciona iniciando con *MySQL Workbench* o *MariaDB***

---

## 🔹 3. Frontend – Vue Cliente

1. Desactivar el entorno virtual:
   ```bash
   deactivate 
   ```
2. Entrar en la carpeta del cliente:
   ```bash
   cd ../SystemScoutsClient
   ```
3. Instalar dependencias:
   ```bash
   npm install
   ```
4. Ejecutar servidor de desarrollo:
   ```bash
   npm run dev
   ```
5. **El cliente estará disponible en:**  
   👉 `http://localhost:5173/`

---

## 🔒 Seguridad de la API
La API usa **Django REST Framework** para:
- Proteger endpoints con permisos.
- Controlar los métodos HTTP permitidos.
- Asegurar la comunicación cliente-servidor.

---

## 💡 Recomendaciones de desarrollo
1. Mantén los **entornos virtuales** separados para **Python** y **Node**.  
  Esto evita problemas de compatibilidad en futuros *push*.
2. Antes de cada ``` git push ```, asegúrate de:
```bash
  git pull origin main
```
3. Borra las carpetas pycaché o cualquier archivo cache basura de tu proyecto local para evitar errores **(suceden muy amenudo)**

## Acciones recomendadas:

---

## 🔄 CI/CD - Integración y Despliegue Continuo

El proyecto cuenta con flujos automatizados de CI/CD mediante GitHub Actions que validan la calidad del código en cada push y pull request.

### Workflows Disponibles

#### 1. **Backend CI** (`.github/workflows/backend-ci.yml`)
Ejecuta automáticamente cuando hay cambios en `SystemScoutsApi/`:
- ✅ Instalación de dependencias Python
- ✅ Análisis estático con **flake8** (detecta errores de sintaxis y estilo)
- ✅ Configuración automática de entorno con SQLite
- ✅ Ejecución de migraciones
- ✅ Ejecución de tests unitarios (`python manage.py test`)

#### 2. **Frontend CI** (`.github/workflows/frontend-ci.yml`)
Ejecuta automáticamente cuando hay cambios en `SystemScoutsClient/`:
- ✅ Instalación de dependencias Node.js
- ✅ Análisis de código con **ESLint**
- ✅ Verificación de formato con **Prettier**
- ✅ Build de producción con Vite

#### 3. **Code Quality Check** (`.github/workflows/code-quality.yml`)
Validación completa de calidad de código:
- ✅ Verificación de errores críticos en Python
- ✅ Verificación de estilo y complejidad del código
- ✅ Análisis de seguridad con `npm audit` (frontend)
- ✅ Escaneo de vulnerabilidades con `safety` (backend)

#### 4. **Pull Request Checks** (`.github/workflows/pr-checks.yml`)
Validaciones específicas para Pull Requests:
- ✅ Detección de conflictos de merge
- ✅ Validación de mensajes de commit
- ✅ Detección de archivos grandes (>5MB)
- ✅ Validación de estructura del proyecto
- ✅ Ejecución de tests completos

### Ver Estado de los Workflows

Los workflows se ejecutan automáticamente en cada push o pull request. Puedes ver su estado en:
- Pestaña **Actions** del repositorio en GitHub
- Badge de estado en pull requests
- Notificaciones por email (si están habilitadas)

### Ejecutar Validaciones Localmente

Antes de hacer push, puedes ejecutar las mismas validaciones localmente:

**Backend:**
```bash
cd SystemScoutsApi
# Linting
flake8 . --exclude=venv,migrations --max-line-length=127

# Tests
python manage.py test
```

**Frontend:**
```bash
cd SystemScoutsClient
# Linting
npm run lint

# Formato
npm run format

# Build
npm run build
```

### Buenas Prácticas

- ✅ Ejecuta `npm run lint` y `flake8` antes de hacer commit
- ✅ Asegúrate de que todos los tests pasen antes de crear un PR
- ✅ Revisa los warnings de los workflows aunque no fallen
- ✅ Mantén los commits descriptivos (mínimo 10 caracteres)
- ✅ No incluyas archivos grandes en el repositorio (usa `.gitignore`)


1. Ir a la ruta de tu carpeta raíz del proyecto en una nueva terminal
```bash
  cd IngSw-seccion2
```
(O con click derecho en tu carpeta IngSw-seccion2 > Open in Integrated Terminal)

2. Proceder a ejecutar git pull
```bash
  git pull origin main
```
3. Revisar el estado de los cambios
```bash
  git status
```
4. Agregar los cambios (Agregar todos los cambios)
```bash
  git add .
```
5. Hacer commit de los cambios
```bash
  git commit -m "Descripción de los cambios realizados"
```
6. Subir los cambios
```bash
  git push origin main
```

---

# 🔧 Inicializar Entorno Virtual (Backend Django)

Para trabajar con el backend de Django, es indispensable levantar un entorno virtual.
Esto permite aislar las dependencias del proyecto, evitando conflictos con otras instalaciones de Python.

## 📌 Pasos en la terminal (CMD o PowerShell)

**Crear el entorno virtual**
* Crea una carpeta llamada venv con todos los paquetes de Python exclusivamente para tu proyecto:
```bash
python -m venv venv
```

**Activar el entorno virtual**
* Esto “enciende” el entorno virtual para que cada comando use las dependencias del proyecto:
```bash
venv\Scripts\activate
```

**Instalar las dependencias del proyecto**
* Con el entorno activado, instala todo lo necesario desde el archivo requirements.txt:
```bash
pip install -r requirements.txt
```

Una vez hecho esto, ya puedes ejecutar python manage.py runserver con total tranquilidad.
Si el entorno está activado, verás (venv) al inicio de la línea de tu terminal. Como si tu consola te estuviera guiñando un ojo 😉

---

# 🔐 Crear un Superusuario en Django

Para acceder al panel administrativo de Django y gestionar el sistema, necesitarás un superusuario.

## 📌 Pasos para crear un superusuario

**Asegúrate de estar en la carpeta correcta**
Debes situarte en el mismo directorio donde está el archivo manage.py.
Ejemplo:
```bash
cd IngSw-seccion2/SystemScoutsApi
```

**Crear el superusuario**
Ejecuta el siguiente comando:
```bash
python manage.py createsuperuser
```

**Completar los datos solicitados**
Django te pedirá:

* Nombre de usuario
* Correo electrónico (opcional)
* Contraseña

Y listo. Con eso ya puedes iniciar sesión en:
👉 http://127.0.0.1:8000/admin/

---

# 📡 Endpoints de la API

A continuación se detallan los endpoints disponibles en la API, organizados por módulos funcionales.

## 👥 Módulo de Usuarios
**Base URL:** `/api/usuarios/`

| Endpoint | Descripción |
|----------|-------------|
| `usuarios/` | Gestión de usuarios del sistema |
| `perfiles/` | Administración de perfiles de usuario |
| `aplicaciones/` | Manejo de aplicaciones del sistema |
| `perfil_aplicaciones/` | Relación entre perfiles y aplicaciones |

## 👨‍👩‍👧‍👦 Módulo de Personas
**Base URL:** `/api/personas/`

### Personas
**Endpoint:** `personas/`

**Filtros disponibles:**
| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|----------|
| `nombre` | string | Búsqueda por nombre (insensible a mayúsculas) | `?nombre=juan` |
| `apellido` | string | Búsqueda por apellido (insensible a mayúsculas) | `?apellido=perez` |
| `run` | string | Búsqueda exacta por RUN | `?run=12345678` |
| `dv` | string | Búsqueda exacta por dígito verificador | `?dv=k` |
| `comuna_nombre` | string | Búsqueda por nombre de comuna | `?comuna_nombre=santiago` |
| `comuna_id` | number | Búsqueda por ID de comuna | `?comuna_id=1` |
| `usuario_nombre` | string | Búsqueda por nombre de usuario | `?usuario_nombre=admin` |
| `usuario_id` | number | Búsqueda por ID de usuario | `?usuario_id=1` |
| `vigente` | boolean | Filtro por estado de vigencia | `?vigente=true` |

### Personas Cursos
**Endpoint:** `cursos/`

**Filtros disponibles:**
| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|----------|
| `run` | string | Búsqueda exacta por RUN (sin DV) | `?run=12345678` |
| `dv` | string | Búsqueda exacta por dígito verificador | `?dv=k` |
| `nombre_persona` | string | Búsqueda por nombre de persona | `?nombre_persona=maria` |
| `apellido_persona` | string | Búsqueda por apellido de persona | `?apellido_persona=gonzalez` |
| `curso_codigo` | string | Búsqueda exacta por código de curso | `?curso_codigo=CUR-0778` |
| `rol_nombre` | string | Búsqueda por nombre de rol | `?rol_nombre=participante` |
| `alimentacion_nombre` | string | Búsqueda por tipo de alimentación | `?alimentacion_nombre=vegetariana` |
| `nivel_nombre` | string | Búsqueda por nivel | `?nivel_nombre=basico` |
| `registrado` | boolean | Filtro por registro completado | `?registrado=true` |
| `acreditado` | boolean | Filtro por acreditación | `?acreditado=false` |
| `correo_qr_enviado` | boolean | Filtro por correo QR enviado | `?correo_qr_enviado=true` |

**Endpoints adicionales del módulo:**
| Endpoint | Descripción |
|----------|-------------|
| `grupos/` | Administración de grupos |
| `formadores/` | Manejo de instructores/formadores |
| `niveles/` | Administración de niveles |
| `cursos/` | Cursos asociados a personas |
| `estado-cursos/` | Estados de los cursos |
| `vehiculos/` | Gestión de vehículos |

## 📚 Módulo de Cursos
**Base URL:** `/api/cursos/`

| Endpoint | Descripción |
|----------|-------------|
| `cursos/` | Gestión principal de cursos |
| `cuotas/` | Administración de cuotas de pago |
| `fechas/` | Manejo de fechas del curso |
| `alimentaciones/` | Gestión de servicios de alimentación |
| `coordinadores/` | Administración de coordinadores |
| `secciones/` | Manejo de secciones del curso |
| `formadores/` | Instructores asignados a cursos |

## 📁 Módulo de Archivos
**Base URL:** `/api/archivos/`

| Endpoint | Descripción |
|----------|-------------|
| `archivos/` | Gestión general de archivos |
| `cursos/` | Archivos asociados a cursos |
| `personas/` | Archivos asociados a personas |

## ⚙️ Módulo de Mantenedores
**Base URL:** `/api/mantenedores/`

| Endpoint | Descripción |
|----------|-------------|
| `concepto-contable/` | Conceptos contables |
| `tipo-curso/` | Tipos de cursos disponibles |
| `tipo-archivo/` | Tipos de archivos del sistema |
| `alimentación/` | Opciones de alimentación |
| `rol/` | Roles del sistema |
| `cargo/` | Cargos o puestos |
| `rama/` | Ramas o especialidades |
| `estado-civil/` | Estados civiles |
| `nivel/` | Niveles del sistema |
| `zona/` | Zonas geográficas |
| `distrito/` | Distritos |
| `grupo/` | Grupos del sistema |
| `región/` | Regiones |
| `provincia/` | Provincias |
| `comuna/` | Comunas |

**Endpoints de catálogos ligeros (sin autenticación):**
| Endpoint | Descripción |
|----------|-------------|
| `/api/mantenedores/tipo-curso/min` | Tipos de curso mínimos |
| `/api/mantenedores/roles/min` | Roles mínimos |
| `/api/mantenedores/cargos/min` | Cargos mínimos |
| `/api/mantenedores/ramas/min` | Ramas mínimas |

## 💰 Módulo de Pagos
**Base URL:** `/api/pagos/`

| Endpoint | Descripción |
|----------|-------------|
| `proveedor/` | Gestión de proveedores |
| `comprobante-pago/` | Comprobantes de pago |
| `pago-comprobante/` | Relación pagos-comprobantes |
| `pago-persona/` | Pagos asociados a personas |
| `prepago/` | Sistema de prepagos |

## 📧 Módulo de Correos
**Base URL:** `/api/correos/`

| Endpoint | Descripción |
|----------|-------------|
| `correos/` | Gestión de correos electrónicos |

## 🔐 Autenticación

| Endpoint | Descripción |
|----------|-------------|
| `/login/` | Obtener token JWT (access + refresh) |
| `/refresh/` | Renovar access token usando refresh token |
| `/api/verificar-qr/` | Verificar acreditación por código QR |

**Endpoints de búsqueda ligeros (sin autenticación):**
| Endpoint | Descripción |
|----------|-------------|
| `/api/personas/search` | Búsqueda rápida de personas |
| `/api/personas/min` | Listado mínimo de personas |

---

## 🔍 Uso de Filtros

### Ejemplos de consultas con filtros:

**Buscar personas por nombre y apellido:**
```
GET /api/personas/personas/?nombre=Juan&apellido=Perez
```

**Buscar participantes de un curso específico:**
```
GET /api/personas/individuales/?curso_codigo=CUR-0778&acreditado=true
```

**Buscar personas no vigentes en una comuna:**
```
GET /api/personas/personas/?comuna_nombre=providencia&vigente=false
```

**Buscar participantes por rol y alimentación:**
```
GET /api/personas/individuales/?rol_nombre=formador&alimentacion_nombre=vegetariana
```

---

## 📝 Notas de Uso

- Todos los endpoints soportan operaciones CRUD (GET, POST, PUT, DELETE) según los permisos del usuario
- Las respuestas siguen el formato JSON estándar
- Se requiere autenticación para acceder a la mayoría de los endpoints
- Los códigos de estado HTTP siguen las convenciones REST estándar
- Los filtros pueden combinarse usando múltiples parámetros en la URL
- Los filtros de texto son insensibles a mayúsculas/minúsculas cuando usan `icontains`

---

## 🧪 Testing

El proyecto cuenta con un suite completo de pruebas automatizadas.

### Ejecutar Tests del Backend
```bash
cd SystemScoutsApi
python manage.py test
```

### Ejecutar Tests del Frontend
```bash
cd SystemScoutsClient
npm run test
```

### Cobertura Actual
- ✅ **Backend**: 9 tests de modelos (100% passing)
- ✅ **Frontend**: Tests de componentes y servicios configurados
- ✅ **CI/CD**: Workflows automatizados en GitHub Actions

Para más información, consulta:
- [RUNNING_TESTS.md](./RUNNING_TESTS.md) - Guía rápida de testing
- [TESTING_DOCUMENTATION.md](./TESTING_DOCUMENTATION.md) - Documentación completa
- [MANUAL_QA_CHECKLIST.md](./MANUAL_QA_CHECKLIST.md) - Checklist de pruebas manuales

---

## 📊 Estado del Proyecto

### ✅ Funcionalidades Implementadas
- Sistema de autenticación JWT
- CRUD completo de Usuarios, Personas, Cursos y Pagos
- Gestión de perfiles y permisos
- Verificador QR para acreditaciones
- Exportación de datos (Excel, PDF)
- Sistema de filtros avanzados
- Suite de tests automatizados

### 🚧 En Desarrollo
- Aumento de cobertura de tests
- Tests end-to-end con Playwright
- Mejoras en la documentación de API

---

## 🤝 Contribuir

Al contribuir al proyecto:
1. Asegúrate de que todos los tests pasen
2. Agrega tests para nuevas funcionalidades
3. Mantén la cobertura de código
4. Sigue las convenciones de código existentes
5. Actualiza la documentación según sea necesario

---

## 📧 Soporte

Para problemas o consultas:
- Revisa la documentación en la carpeta del proyecto
- Consulta [SOLUCION_LOGIN.md](./SOLUCION_LOGIN.md) para problemas comunes de autenticación
- Abre un issue en el repositorio de GitHub
