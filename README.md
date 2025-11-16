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
├─ SistemScoutsApi/       # Backend Django (API REST)
├─ SistemScoutsClient/    # Frontend Vue (Vite)
└─ README.md
```

---

## 🔹 1. Clonar el repositorio (Abrir una nueva terminal)
```bash
git clone https://github.com/Inacap-Analistas-programador/IngSw-seccion2.git
cd IngSw-seccion2/SistemScoutsApi
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
   ```bash
   python manage.py runserver
   ```
5. **La API estará disponible en:**
    👉 `http://127.0.0.1:8000/`

---

## 🔹 3. Frontend – Vue Cliente

1. Desactivar el entorno virtual:
   ```bash
   deactivate 
   ```
2. Entrar en la carpeta del cliente:
   ```bash
   cd ../SistemScoutsClient
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
para mantener el repositorio sincronizado.


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

| Endpoint | Descripción |
|----------|-------------|
| `personas/` | Gestión completa de personas |
| `grupos/` | Administración de grupos |
| `formadores/` | Manejo de instructores/formadores |
| `individuales/` | Gestión de registros individuales |
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
**Base URL:** `/api/Mantenedores/`

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

## 📝 Notas de Uso

- Todos los endpoints soportan operaciones CRUD (GET, POST, PUT, DELETE) según los permisos del usuario
- Las respuestas siguen el formato JSON estándar
- Se requiere autenticación para acceder a la mayoría de los endpoints
- Los códigos de estado HTTP siguen las convenciones REST estándar