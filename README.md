# 🏕️ Sistema de Scouts – Arquitectura MVC con API REST

Este proyecto implementa un **sistema de gestión para Scouts** usando  
**Django** como backend (API REST) y **Vue** como frontend.  
La comunicación se realiza mediante consultas HTTP seguras para realizar operaciones CRUD.

---

## 🚀 Tecnologías principales
- **Python / Django** + **Django REST Framework** – API REST.
- **Vue 3 + Vite** – Cliente web.
- **Arquitectura MVC** – Separación clara entre modelo, vista y controlador.

---

## ⚙️ Requisitos previos
Asegúrate de tener instalados en tu sistema:
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js (LTS)](https://nodejs.org/) (incluye npm)
- [Git](https://git-scm.com/) para clonar el repositorio
- Visual Studio Code (opcional pero recomendado)

---

## 📂 Estructura del proyecto
```
SistemaScouts/
│
├─ SistemScoutsApi/       # Backend Django (API REST)
├─ SistemScoutsClient/    # Frontend Vue (Vite)
└─ README.md
```

---

## 🔹 1. Clonar el repositorio
```bash
git clone <URL-del-repositorio>
cd SistemaScouts
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

1. Entrar en la carpeta del cliente:
   ```bash
   cd SistemScoutsClient
   ```
2. Instalar dependencias:
   ```bash
   npm install
   ```
3. Ejecutar servidor de desarrollo:
   ```bash
   npm run dev
   ```
   El cliente estará disponible en:  
   👉 `http://localhost:5173/`

---

## 🔒 Seguridad de la API
La API usa **Django REST Framework** para:
- Proteger endpoints con permisos.
- Controlar los métodos HTTP permitidos.
- Asegurar la comunicación cliente-servidor.

---

## 💡 Recomendaciones de desarrollo
- Mantén los **entornos virtuales** separados para **Python** y **Node**.  
  Esto evita problemas de compatibilidad en futuros *push*.
- Antes de cada `git push`, asegúrate de:
  ```bash
  git pull origin main
  ```
  para mantener el repositorio sincronizado.

