import { request } from './apiClient';

/**
 * Dashboard Service - Conexión API para Dashboard Principal
 * Maneja todos los datos relacionados con cursos y finanzas
 */

const dashboardService = {
  /**
   * Obtener todos los cursos vigentes
   * Utilizado para: gráfico principal, tabla de cursos
   */
  cursos: {
    list: (params) => request(`cursos${params ? `?${new URLSearchParams(params)}` : ''}`)
  },

  /**
   * Obtener todas las cuotas/montos de cursos
   * Utilizado para: calcular montos estimados y recaudados
   */
  cuotas: {
    list: (params) => request(`cuotas${params ? `?${new URLSearchParams(params)}` : ''}`)
  },

  /**
   * Obtener todos los coordinadores de cursos
   * Utilizado para: mostrar responsables en la tabla
   */
  coordinadores: {
    list: (params) => request(`coordinadores${params ? `?${new URLSearchParams(params)}` : ''}`)
  },

  /**
   * Obtener todas las personas
   * Utilizado para: resolver nombres de responsables
   */
  personas: {
    list: (params) => request(`personas${params ? `?${new URLSearchParams(params)}` : ''}`)
  },

  /**
   * Obtener resumen financiero de un curso específico
   */
  getCursoResumen: (cursoId) => 
    request(`cursos/${cursoId}/resumen/`),

  /**
   * Obtener estadísticas financieras globales
   */
  getEstadisticasGlobales: () => 
    request('estadisticas/dashboard/'),

  /**
   * Obtener pagos por rango de fechas
   */
  getPagosPorFecha: (params) => 
    request(`pagos${params ? `?${new URLSearchParams(params)}` : ''}`),
};

export default dashboardService;




