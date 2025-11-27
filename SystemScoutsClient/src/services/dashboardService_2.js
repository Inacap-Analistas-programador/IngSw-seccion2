import { request } from './apiClient'

/**
 * Dashboard 2 Service - Compatible con DashboardScout.vue
 * ENTREGADO COMPLETO Y LISTO PARA USAR
 */

const dashboardService_2 = {
  // ============================
  // CURSOS
  // ============================
  cursos: {
    list: (params) =>
      request(`cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`cursos/${id}/`)
  },

  // ============================
  // PERSONAS
  // ============================
  personas: {
    list: (params) =>
      request(`personas${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`personas/${id}/`)
  },

  // ============================
  // INSCRIPCIONES (persona-cursos)
  // ============================
  personaCursos: {
    list: (params) =>
      request(`persona-cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`persona-cursos/${id}/`)
  },

  // ============================
  // PAGOS (pago-persona)
  // ============================
  pagoPersona: {
    list: (params) =>
      request(`pago-persona${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`pago-persona/${id}/`)
  },

  // ============================
  // COORDINADORES
  // ============================
  coordinadores: {
    list: (params) =>
      request(`coordinadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`coordinadores/${id}/`)
  },

  // ============================
  // FORMADORES
  // ============================
  formadores: {
    list: (params) =>
      request(`formadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`formadores/${id}/`)
  }
}

export default dashboardService_2
