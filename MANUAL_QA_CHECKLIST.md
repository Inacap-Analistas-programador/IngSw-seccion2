# Manual QA Testing Checklist - Sistema de Scouts

Este documento contiene checklists de verificación manual para el sistema de scouts mientras se implementan pruebas automatizadas completas.

## 🎯 Módulo de Autenticación

### Login
- [ ] Login exitoso con credenciales válidas
- [ ] Login falla con usuario incorrecto
- [ ] Login falla con contraseña incorrecta
- [ ] Token JWT se almacena en localStorage
- [ ] Token se incluye en headers de peticiones subsecuentes
- [ ] Redirección correcta al dashboard después del login
- [ ] Mensaje de error apropiado para credenciales inválidas

### Logout
- [ ] Logout limpia el token de localStorage
- [ ] Logout redirige a la página de login
- [ ] Usuario no puede acceder a rutas protegidas después del logout

### Sesión
- [ ] Sesión expira después del tiempo configurado
- [ ] Refresh token funciona correctamente
- [ ] Usuario es redirigido al login cuando el token expira

## 👥 Módulo de Usuarios

### Listado de Usuarios
- [ ] Tabla muestra todos los usuarios vigentes
- [ ] Paginación funciona correctamente
- [ ] Búsqueda por nombre de usuario funciona
- [ ] Filtro por perfil funciona
- [ ] Filtro por estado (vigente/no vigente) funciona
- [ ] Ordenamiento por columnas funciona

### Crear Usuario
- [ ] Formulario de creación se abre correctamente
- [ ] Todos los campos obligatorios están marcados
- [ ] Validación de username único
- [ ] Validación de formato de email
- [ ] Contraseña se requiere en creación
- [ ] Selección de perfil funciona
- [ ] Usuario se crea exitosamente
- [ ] Mensaje de éxito se muestra
- [ ] Tabla se actualiza con el nuevo usuario

### Editar Usuario
- [ ] Formulario de edición carga datos existentes
- [ ] Todos los campos se pueden modificar
- [ ] Cambio de perfil funciona
- [ ] Cambio de estado vigente/no vigente funciona
- [ ] Validaciones funcionan en edición
- [ ] Cambios se guardan correctamente
- [ ] Mensaje de éxito se muestra
- [ ] Tabla se actualiza con los cambios

### Eliminar Usuario
- [ ] Confirmación de eliminación se solicita
- [ ] Usuario se marca como no vigente (soft delete)
- [ ] Usuario no aparece en listado de vigentes
- [ ] Mensaje de éxito se muestra

## 👤 Módulo de Personas

### Listado de Personas
- [ ] Tabla muestra todas las personas vigentes
- [ ] Paginación funciona correctamente
- [ ] Búsqueda por RUN funciona
- [ ] Búsqueda por nombre funciona
- [ ] Búsqueda por apellido funciona
- [ ] Filtro por grupo funciona
- [ ] Filtro por comuna funciona
- [ ] Exportar a Excel funciona
- [ ] Exportar a PDF funciona

### Crear Persona
- [ ] Formulario de creación se abre correctamente
- [ ] Validación de RUN único
- [ ] Validación de formato de RUN y DV
- [ ] Validación de email
- [ ] Validación de teléfono
- [ ] Selección de comuna funciona (cascada desde región)
- [ ] Selección de estado civil funciona
- [ ] Selección de grupo funciona
- [ ] Campo fecha de nacimiento con datepicker
- [ ] Validación de edad mínima/máxima
- [ ] Foto/imagen se puede subir
- [ ] Persona se crea exitosamente
- [ ] Mensaje de éxito se muestra

### Editar Persona
- [ ] Formulario de edición carga datos existentes
- [ ] Todos los campos se pueden modificar
- [ ] RUN no se puede cambiar (o validación especial)
- [ ] Cambios se guardan correctamente
- [ ] Foto se puede actualizar
- [ ] Mensaje de éxito se muestra

### Eliminar Persona
- [ ] Confirmación de eliminación se solicita
- [ ] Persona se marca como no vigente
- [ ] Relaciones con cursos se mantienen

## 📚 Módulo de Cursos

### Listado de Cursos
- [ ] Tabla muestra todos los cursos
- [ ] Paginación funciona correctamente
- [ ] Búsqueda por código funciona
- [ ] Búsqueda por descripción funciona
- [ ] Filtro por estado funciona (Pendiente/Vigente/Anulado/Finalizado)
- [ ] Filtro por tipo de curso funciona
- [ ] Filtro por modalidad funciona
- [ ] Vista de calendario/timeline funciona (si existe)

### Crear Curso
- [ ] Formulario de creación se abre correctamente
- [ ] Código de curso se genera automáticamente o se valida único
- [ ] Selección de tipo de curso funciona
- [ ] Selección de responsable (persona) funciona
- [ ] Selección de cargo responsable funciona
- [ ] Selección de comuna/lugar funciona
- [ ] Validación de cuotas (con/sin almuerzo)
- [ ] Selección de modalidad funciona
- [ ] Selección de fechas funciona
- [ ] Mapa de ubicación se muestra (si aplica)
- [ ] Coordenadas se pueden seleccionar en mapa
- [ ] Curso se crea exitosamente
- [ ] Mensaje de éxito se muestra

### Editar Curso
- [ ] Formulario de edición carga datos existentes
- [ ] Todos los campos se pueden modificar
- [ ] Cambio de estado funciona correctamente
- [ ] Validaciones funcionan en edición
- [ ] Cambios se guardan correctamente

### Inscripciones a Curso
- [ ] Lista de inscritos se muestra correctamente
- [ ] Agregar persona al curso funciona
- [ ] Validación de cupos máximos
- [ ] Quitar persona del curso funciona
- [ ] Estado de inscripción se actualiza
- [ ] Exportar lista de inscritos funciona

## 💰 Módulo de Pagos

### Listado de Pagos
- [ ] Tabla muestra todos los pagos
- [ ] Paginación funciona correctamente
- [ ] Búsqueda por persona funciona
- [ ] Búsqueda por curso funciona
- [ ] Filtro por tipo (Ingreso/Egreso) funciona
- [ ] Filtro por rango de fechas funciona
- [ ] Totales se calculan correctamente
- [ ] Exportar reporte de pagos funciona

### Registrar Pago
- [ ] Formulario de registro se abre correctamente
- [ ] Selección de persona funciona
- [ ] Selección de curso funciona
- [ ] Validación de monto
- [ ] Tipo de pago se selecciona (Ingreso/Egreso)
- [ ] Comprobante se puede adjuntar
- [ ] Pago se registra exitosamente
- [ ] Mensaje de éxito se muestra

### Ver Comprobante
- [ ] Comprobante se visualiza correctamente
- [ ] Descarga de comprobante funciona
- [ ] Impresión de comprobante funciona

### Proveedores
- [ ] Listado de proveedores se muestra
- [ ] Crear proveedor funciona
- [ ] Editar proveedor funciona
- [ ] Validaciones de campos obligatorios

## 🔐 Módulo de Perfiles y Permisos

### Gestión de Perfiles
- [ ] Listado de perfiles se muestra
- [ ] Crear perfil funciona
- [ ] Editar perfil funciona
- [ ] Asignar aplicaciones a perfil funciona
- [ ] Permisos (Ver/Editar/Eliminar) se configuran correctamente

### Verificación de Permisos
- [ ] Usuario solo ve módulos según su perfil
- [ ] Acciones restringidas no se muestran
- [ ] Intentos de acceso no autorizado son bloqueados
- [ ] Mensajes de error apropiados para falta de permisos

## 📊 Reportes y Exportaciones

### Reportes
- [ ] Reporte de personas vigentes por grupo
- [ ] Reporte de cursos activos
- [ ] Reporte de pagos por curso
- [ ] Reporte de asistencia (si aplica)
- [ ] Gráficos y estadísticas se generan correctamente

### Exportaciones
- [ ] Exportar a Excel funciona en todos los módulos
- [ ] Exportar a PDF funciona en todos los módulos
- [ ] Formato de exportación es correcto
- [ ] Datos exportados son completos y precisos

## 📱 Verificador QR (Si aplica)

### Escaneo
- [ ] Lector QR se activa correctamente
- [ ] Cámara se solicita y activa
- [ ] Código QR se escanea correctamente
- [ ] Información se muestra después del escaneo
- [ ] Registro de asistencia funciona

### Generación
- [ ] QR se genera para personas
- [ ] QR se puede descargar
- [ ] QR se puede imprimir

## 🌐 Funcionalidad General

### Navegación
- [ ] Menú lateral funciona correctamente
- [ ] Navegación entre módulos es fluida
- [ ] Breadcrumbs se actualizan correctamente
- [ ] Botón de volver funciona
- [ ] Links internos funcionan

### Responsive Design
- [ ] Layout responsive en móvil
- [ ] Layout responsive en tablet
- [ ] Layout responsive en desktop
- [ ] Menú móvil funciona
- [ ] Tablas tienen scroll horizontal en móvil

### Performance
- [ ] Carga inicial es rápida (< 3 segundos)
- [ ] Navegación entre páginas es fluida
- [ ] Búsquedas responden rápidamente
- [ ] No hay bloqueos de UI
- [ ] Indicadores de carga se muestran

### Errores y Validaciones
- [ ] Mensajes de error son claros
- [ ] Validaciones de campos son apropiadas
- [ ] Errores de servidor se manejan correctamente
- [ ] Errores de red se manejan correctamente
- [ ] Mensajes de éxito son claros

## 🔧 Configuración y Administración

### Mantenedores
- [ ] Países, regiones, comunas se gestionan
- [ ] Estados civiles se gestionan
- [ ] Grupos se gestionan
- [ ] Cargos se gestionan
- [ ] Tipos de curso se gestionan

## Notas de Testing

### Datos de Prueba Recomendados
- Crear al menos 3 usuarios con diferentes perfiles
- Crear al menos 10 personas para testing de búsqueda y paginación
- Crear al menos 5 cursos en diferentes estados
- Registrar al menos 10 pagos de diferentes tipos

### Browsers a Probar
- [ ] Chrome (última versión)
- [ ] Firefox (última versión)
- [ ] Safari (si aplica)
- [ ] Edge (última versión)
- [ ] Móvil - Chrome Android
- [ ] Móvil - Safari iOS

### Roles a Probar
- [ ] Administrador (todos los permisos)
- [ ] Dirigente (permisos limitados)
- [ ] Padre (permisos muy limitados)
- [ ] Usuario sin permisos

---

## ✅ Criterios de Aprobación

Para considerar una funcionalidad como "probada y aprobada":
1. Todos los items del checklist están marcados
2. No hay bugs críticos o bloqueantes
3. Performance es aceptable
4. Funciona en los browsers principales
5. Responsive design funciona correctamente
6. Mensajes de error/éxito son apropiados

## 📝 Reportar Bugs

Al encontrar un bug, registrar:
- Módulo afectado
- Pasos para reproducir
- Resultado esperado
- Resultado actual
- Screenshots (si aplica)
- Browser y versión
- Severidad (Crítico/Alto/Medio/Bajo)
