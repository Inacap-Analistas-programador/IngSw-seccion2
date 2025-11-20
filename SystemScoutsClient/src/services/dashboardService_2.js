import { request } from './apiClient';

/**
 * Dashboard 2 Service - Conexión API para Dashboard Scout (Dashboard 2)
 * Maneja gestión de cursos, personas, inscripciones, pagos y coordinadores
 */

const dashboard2Service = {
  /**
   * Gestión de Cursos
   * Obtiene información completa de todos los cursos vigentes
   */
  cursos: {
    list: (params) => request(`cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`cursos/${id}/`),
    create: (data) => request('cursos/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`cursos/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`cursos/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`cursos/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Gestión de Personas
   * Obtiene información de todas las personas registradas
   */
  personas: {
    list: (params) => request(`personas${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`personas/${id}/`),
    create: (data) => request('personas/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`personas/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`personas/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`personas/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Gestión de Inscripciones (Personas-Cursos)
   * Obtiene las personas inscritas en cada curso
   */
  personaCursos: {
    list: (params) => request(`persona-cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`persona-cursos/${id}/`),
    create: (data) => request('persona-cursos/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`persona-cursos/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`persona-cursos/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`persona-cursos/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Gestión de Pagos por Persona
   * Obtiene el estado de pagos de personas inscritas
   */
  pagoPersona: {
    list: (params) => request(`pago-persona${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`pago-persona/${id}/`),
    create: (data) => request('pago-persona/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`pago-persona/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`pago-persona/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`pago-persona/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Gestión de Coordinadores de Cursos
   * Obtiene información de coordinadores asignados a cursos
   */
  coordinadores: {
    list: (params) => request(`coordinadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`coordinadores/${id}/`),
    create: (data) => request('coordinadores/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`coordinadores/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`coordinadores/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`coordinadores/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Gestión de Formadores de Cursos
   * Obtiene información de formadores asignados a cursos
   */
  formadores: {
    list: (params) => request(`formadores${params ? `?${new URLSearchParameters(params)}` : ''}`),
    get: (id) => request(`formadores/${id}/`),
    create: (data) => request('formadores/', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => request(`formadores/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => request(`formadores/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => request(`formadores/${id}/`, { method: 'DELETE' }),
  },

  /**
   * Funciones Auxiliares para Estadísticas
   */

  /**
   * Obtener resumen de un curso específico
   * Retorna: inscritos, acreditados, pendientes de pago, etc.
   */
  getCursoResumen: (cursoId) => 
    request(`cursos/${cursoId}/resumen/`),

  /**
   * Obtener estadísticas de un curso
   * Retorna: información compilada de inscripciones, pagos, acreditaciones
   */
  getCursoEstadisticas: (cursoId) => 
    request(`cursos/${cursoId}/estadisticas/`),

  /**
   * Obtener personas inscritas en un curso específico
   */
  getPersonasPorCurso: (cursoId) => 
    request(`cursos/${cursoId}/personas/`),

  /**
   * Obtener pagos de un curso específico
   */
  getPagosPorCurso: (cursoId) => 
    request(`cursos/${cursoId}/pagos/`),

  /**
   * Obtener coordinadores de un curso específico
   */
  getCoordinadoresPorCurso: (cursoId) => 
    request(`cursos/${cursoId}/coordinadores/`),

  /**
   * Obtener formadores de un curso específico
   */
  getFormadoresPorCurso: (cursoId) => 
    request(`cursos/${cursoId}/formadores/`),

  /**
   * Obtener estadísticas globales del dashboard
   * Retorna: totales generales, gráficos, datos compilados
   */
  getEstadisticasGlobales: () => 
    request('estadisticas/dashboard/'),

  /**
   * Obtener resumen de pagos por fecha
   */
  getResumenPagosPorFecha: (params) => 
    request(`estadisticas/pagos-por-fecha${params ? `?${new URLSearchParams(params)}` : ''}`),

  /**
   * Obtener resumen de inscripciones por fecha
   */
  getResumenInscripcionesPorFecha: (params) => 
    request(`estadisticas/inscripciones-por-fecha${params ? `?${new URLSearchParams(params)}` : ''}`),

  /**
   * Buscar personas por criterios
   */
  buscarPersonas: (params) => 
    request(`personas${params ? `?${new URLSearchParams(params)}` : ''}`),

  /**
   * Filtrar cursos por estado
   */
  cursosPorEstado: (estado) => 
    request(`cursos/?estado=${estado}`),

  /**
   * Obtener notificaciones o alertas relacionadas con cursos/pagos
   */
  getAlertas: () => 
    request('alertas/dashboard/'),
};

export default dashboard2Service;
