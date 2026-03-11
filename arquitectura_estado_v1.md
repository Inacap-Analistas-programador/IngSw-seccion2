# Arquitectura y Estado Actual - SystemScouts V1

**Fecha:** 25 de Febrero de 2026
**Tecnología Base:**

- **Backend:** Django 4.x + Django REST Framework + MySQL
- **Frontend:** Vue 3 (Composition API) + Vite
**Estado del Proyecto:** Versión 1.0 (MVP) - Entrega a 5 días

---

## 1. Descripción General de la Arquitectura Actual (V1)

Para asegurar la salida a producción en los próximos 5 días, el proyecto se ha construido bajo un modelo **Altamente Acoplado y Monolítico** en sus respectivas capas (Frontend y Backend).

### Backend (SystemScoutsApi)

Se emplea un monolito basado en una única aplicación de Django llamada `ApiCoreScouts`. Toda la lógica, modelos (`curso_model.py`, `usuario_model.py`, etc.), vistas, serializadores y enrutadores conviven dentro de este único módulo. Se ha priorizado la implementación veloz sobre el "Domain Driven Design" (DDD), utilizando fuertemente los abstracciones genéricas que provee Django REST Framework (`ModelViewSet`).

### Frontend (SystemScoutsClient)

Se ha implementado una arquitectura basada en componentes funcionales (`components/`), organizados conceptualmente por "tipo de archivo" tecnológico en vez de dominio. Estado y llamadas a API se han extraído crudamente a archivos sueltos en un directorio `services/` (por ejemplo, `personasService.js`), lo que reduce la carga cognitiva para montar componentes, propiciando sin embargo, fat client services.

---

## 2. Decisiones Técnicas Tomadas (Priorizando Velocidad)

1. **Backend - Uso exhaustivo de `ModelViewSet` en `Mantenedor_view.py` y demás:**
   *Razón:* Se sacrificó la flexibilidad y el control estricto de endpoints REST personalizados a cambio de generar CRUDs automáticos de cada entidad fundamental.
2. **Backend - Única App `ApiCoreScouts` y único `models.py` estructurado en subcarpetas:**
   *Razón:* Para ahorrar el *scaffolding* inicial y migraciones distribuidas, todos los modelos pertenecen e interactúan como si fuesen globales, simplificando radicalmente las integraciones manuales de Foreign Keys de Django.
3. **Frontend - Ausencia de TypeScript y Estado Global (Pinia):**
   *Razón:* Se usó JavaScript puro (`.js` en lugar de `.ts`) para obviar la verbosidad de las interfaces y decoradores, y se prescindió del estado global `Pinia/Vuex` delegando el guardado y flujo de la información al `localStorage` e integraciones directas con los `services`.
4. **Vistas Monolíticas de Vue (`views/`):**
   *Razón:* Vistas grandes como `Gestionpersonas.vue` concentran casi todo el ciclo de vida, fetching y mutaciones de un dominio completo para no tardar creando stores ni composables interconectados.
5. **Autenticación Basada en Simple JWT nativo y Filtros estáticos:**
   *Razón:* Autenticación "Bearer" simple validada por el backend en las Views clave, acoplando levemente la información de sesión a través del router Vue.

---

## 3. Limitaciones Conocidas (V1) y Deuda Técnica

### Riesgos Arquitectónicos Inmediatos

- **Importes Circulares y Agrupación Masiva (Backend):** Si se agrega otra entidad grande, los `__init__.py` dentro de `Models/` o `Serializers/` explotarán en problemas de resolución.
- **Acoplamiento Fuerte y "Prop Drilling" (Frontend):** Las vistas principales son archivos gigantes que pasan excesivos props hacia los componentes modales o tablas. Las modificaciones a un formulario específico requieren lectura exhaustiva del layout y vista padre.
- **Scripts Nativamente Expuestos (Frontend):** Presencia de `find_method.py` mezclados en las carpetas de `src/views/` representan artefactos colaterales sin relevancia productiva que podrían quedar subidos en el build.

### Base de Datos MySQL (Backend)

- **Problema de Consultas N+1:** El `Mantenedor_view.py` no pre-carga (prefetch_related / select_related) campos foráneos (ej: Comunas y Regiones). En cada listado profundo, por cada objeto serializado Django dispara una query individual. *Para ~1000 usuarios este comportamiento degradará notablemente el servidor*.
- **Migraciones Frágiles:** Tener todas las BD colgadas en las migraciones de `ApiCoreScouts` ocasionará que cualquier refactor inter-tablas tranque completamente la historia de la DB.

---

## 4. Estructura de Carpetas Recomendada para Lanzamiento (V1)

**Frontend (`src/`):**

```text
src/
 ├── assets/        (Contiene .css, logos y avatares puros)
 ├── components/    (Componentes agnósticos como BaseButton)
 ├── views/         (Páginas directas de los dominios)
 ├── services/      (Conector apiClient y llamadas organizadas por módulo)
 ├── composables/   (Funciones utilitarias extraídas como usePermissions)
 ├── router/        (Definición de vistas. Idealmente con Lazy-loading)
```

*Se asume la remoción inmediata de cualquier archivo `.py` ajeno al stack de Vite/Vue de esta carpeta.*

**Backend (`SystemScoutsApi/`):**

```text
SystemScoutsApi/
 ├── manage.py
 ├── passenger_wsgi.py (si es cPanel/Shared hosting temporal)
 ├── SystemScoutsApi/  (settings.py para Deploy, urls, wsgi)
 ├── ApiCoreScouts/
 │   ├── Migrations/
 │   ├── Models/
 │   ├── Views/
 │   ├── Serializers/
 │   ├── Routers/
 │   └── Filters/
```

*V1 se va a producción manteniendo el monolito debido a límites temporales, no es viable refactorizar esto sin frenar el sprint.*

---

## 5. Lista de Optimizaciones Post-Lanzamiento (Path to Scalability V2)

Para cuando la aplicación comience a ganar tracción o reciba requerimientos modulares avanzados.

### Backend & MySQL Database

- [ ] **Desintegrar `ApiCoreScouts` (Domain-Driven Design):** Romper el monolito generando distintas APPS de Django formales (`users`, `cursos`, `mantenedores`, `pagos`).
- [ ] **Resolución del N+1:** Sobrescribir los métodos `get_queryset()` en todos los `ModelViewSets` aplicando sistemáticamente `select_related()` en FK simples, y `prefetch_related()` para relaciones Inversas (Muchos a Muchos).
- [ ] **Capa de Servicio (Service Layer):** Centralizar la lógica de correos, transacciones monetarias y creación intrincada de cursos en transacciones atómicas (`@transaction.atomic`) en vez de Views y pre/post-save hooks desperdigados.
- [ ] **Separación de Entornos (Settings Split):** Sustituir el `settings.py` genérico por un layout de configuraciones `/settings/base.py`, `/settings/local.py`, `/settings/production.py`.

### Frontend

- [ ] **Gestión Predictiva de Estado (Pinia):** Refactorizar integraciones dispersas y variables primitivas reactivas (`ref`) por Stores globales de Pinia (`AuthStore`, `MantenedoresStore`), mitigando hits innecesarios a las APIs.
- [ ] **Feature-Based UI:** Mover `views` genéricas hacia agrupaciones por dominio (`src/features/Cursos/...`, `src/features/Personas/...`).
- [ ] **Code Splitting Inteligente:** Convertir la asignación de componentes masivos en el enrutamiento a `const MiVista = () => import('./views/MiVista.vue')` para aligerar la carga principal.
- [ ] **Migración a TypeScript:** Incorporar gradualmente declaración de interfaces estáticas (ej. Estructura exacta de los Payload JSON de creación de personal) que mitigue errores fatales de run-time.

### Seguridad y Entorno

- [ ] **Ajuste de Politicas CORS estables:** Eliminar CORS globales de desarrollo, permitiendo peticiones estrictamente desde la IP estática e ingress rules del bucket o CDN de Frontend.
- [ ] **Configuraciones de TLS/SSL para Auth:** Reforzar las JWT en tokens transmitidas solo a través de protocolos seguros, y considerar delegar la autenticación de Access/Refresh a `httpOnly` cookies persistentes desde el servidor para mitigar el ataque "Cross Site Scripting (XSS)".
- [ ] **Rate Limiting:** Aplicar estrangulamiento (`Throttling` nativo de DRF) en las endpoints de "Login" o "Busquedas Masivas" para evitar bots o scraping desmedido por exceso de carga.

---

## 6. Checklist de Liberación e Integración (Día -1 a Lanzamiento)

- [ ] Verificar que `DEBUG=False` está fijo en el `.env` o configuraciones en el Backend en el servidor.
- [ ] Chequear la existencia de una lista restringida y autorizada estricta de dominios en `ALLOWED_HOSTS`.
- [ ] Limpiar código comentariado sobrante, variables sin utilidad y alert messages huérfanas en el frontend.
- [ ] Vaciar las caché de `localStorage` remanente o configuraciones sucias para evitar que los testers choquen con payloads viejos (TTL desactualizados).
- [ ] Configurar un Server Web (Gunicorn/Uvicorn bajo Nginx/Apache) real que se trague las peticiones simultáneas, deshaciéndose de `runserver` para productivo.
- [ ] Limpieza de archivos misceláneos intrusos (`.py` en frontend, `.txt` innecesarios, logs volcados crudos).
