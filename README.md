# 🏕️ Sistema de Scouts – Arquitectura MVC con API REST

Este proyecto implementa un **sistema de gestión para Scouts** usando  
**Django** como backend (API REST) y **Vue** como frontend.  
La comunicación se realiza mediante consultas HTTP seguras para realizar operaciones CRUD.

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
4. **Ejecutar servidor de desarrollo**
asegurate de estar posicionado en manage.py con
   ```bash
      ls
   ```
   si ves el archivo manage.py puedes ejecutar el comando que sigue.
   ```bash
   python manage.py runserver
   ```
   en caso de no estar posicionado, realiza lo siguiente
   ```bash
      cd SystemScoutsApi
   ```
   puedes usar "ls" para verificar tu posición, una vez veas **manage.py** puedes hacer **runserver**
6. **La API estará disponible en:**
    👉 `http://127.0.0.1:8000/`

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
o:

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
**Base URL:** `/api/Personas/`

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
**Base URL:** `/api/Cursos/`

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
**Base URL:** `/api/Archivos/`

| Endpoint | Descripción |
|----------|-------------|
| `archivos/` | Gestión general de archivos |
| `cursos/` | Archivos asociados a cursos |
| `personas/` | Archivos asociados a personas |

## ⚙️ Módulo de Mantenedores
**Base URL:** `/api/Mantenedores/**

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

## 💰 Módulo de Pagos
**Base URL:** `/api/Pagos/`

| Endpoint | Descripción |
|----------|-------------|
| `proveedor/` | Gestión de proveedores |
| `comprobante-pago/` | Comprobantes de pago |
| `pago-comprobante/` | Relación pagos-comprobantes |
| `pago-persona/` | Pagos asociados a personas |
| `prepago/` | Sistema de prepagos |

---

## 🔍 Uso de Filtros

### Ejemplos de consultas con filtros:

**Buscar personas por nombre y apellido:**
```
GET /api/Personas/personas/?nombre=Juan&apellido=Perez
```

**Buscar participantes de un curso específico:**
```
GET /api/Personas/individuales/?curso_codigo=CUR-0778&acreditado=true
```

**Buscar personas no vigentes en una comuna:**
```
GET /api/Personas/personas/?comuna_nombre=providencia&vigente=false
```

**Buscar participantes por rol y alimentación:**
```
GET /api/Personas/individuales/?rol_nombre=formador&alimentacion_nombre=vegetariana
```

---

## 📝 Notas de Uso

- Todos los endpoints soportan operaciones CRUD (GET, POST, PUT, DELETE) según los permisos del usuario
- Las respuestas siguen el formato JSON estándar
- Se requiere autenticación para acceder a la mayoría de los endpoints
- Los códigos de estado HTTP siguen las convenciones REST estándar
- Los filtros pueden combinarse usando múltiples parámetros en la URL
- Los filtros de texto son insensibles a mayúsculas/minúsculas cuando usan `icontains`
