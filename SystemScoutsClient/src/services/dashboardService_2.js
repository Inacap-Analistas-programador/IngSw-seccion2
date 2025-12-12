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
      request(`cursos/cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`cursos/cursos/${id}/`)
  },

  // ============================
  // PERSONAS
  // ============================
  personas: {
    list: (params) =>
      request(`personas/personas${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`personas/personas/${id}/`)
  },

  // ============================
  // INSCRIPCIONES (persona-cursos)
  // ============================
  personaCursos: {
    list: (params) =>
      request(`personas/cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`personas/cursos/${id}/`)
  },

  // ============================
  // PAGOS (pago-persona)
  // ============================
  pagoPersona: {
    list: (params) =>
      request(`pagos/pago-persona${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`pagos/pago-persona/${id}/`)
  },

  // ============================
  // COORDINADORES
  // ============================
  coordinadores: {
    list: (params) =>
      request(`cursos/coordinadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`cursos/coordinadores/${id}/`)
  },

  // ============================
  // FORMADORES
  // ============================
  formadores: {
    list: (params) =>
      request(`cursos/formadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => request(`cursos/formadores/${id}/`)
  }
}

export default dashboardService_2
