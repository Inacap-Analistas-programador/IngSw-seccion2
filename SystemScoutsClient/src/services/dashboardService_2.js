import { request } from './apiClient'

/**
 * Dashboard 2 Service - Compatible con DashboardScout.vue
 * ENTREGADO COMPLETO Y LISTO PARA USAR
 */

const toUpperCaseKeys = (obj) => {
  if (Array.isArray(obj)) {
    return obj.map(item => toUpperCaseKeys(item))
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      acc[key.toUpperCase()] = toUpperCaseKeys(obj[key])
      return acc
    }, {})
  }
  return obj
}

const requestUpperCase = async (endpoint) => {
  let response = await request(endpoint)
  // Handle pagination unwrapping if needed, though request usually returns data
  // Use simple heuristic: if it has 'results', map that.
  if (response.results) {
    response.results = toUpperCaseKeys(response.results)
    return response
  }
  return toUpperCaseKeys(response)
}

const dashboardService_2 = {
  // ============================
  // CURSOS
  // ============================
  cursos: {
    list: (params) =>
      requestUpperCase(`cursos/cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`cursos/cursos/${id}/`)
  },

  // ============================
  // PERSONAS
  // ============================
  personas: {
    list: (params) =>
      requestUpperCase(`personas/personas${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`personas/personas/${id}/`)
  },

  // ============================
  // INSCRIPCIONES (persona-cursos)
  // ============================
  personaCursos: {
    list: (params) =>
      requestUpperCase(`personas/cursos${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`personas/cursos/${id}/`)
  },

  // ============================
  // PAGOS (pago-persona)
  // ============================
  pagoPersona: {
    list: (params) =>
      requestUpperCase(`pagos/pago-persona${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`pagos/pago-persona/${id}/`)
  },

  // ============================
  // COORDINADORES
  // ============================
  coordinadores: {
    list: (params) =>
      requestUpperCase(`cursos/coordinadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`cursos/coordinadores/${id}/`)
  },

  // ============================
  // FORMADORES
  // ============================
  formadores: {
    list: (params) =>
      requestUpperCase(`cursos/formadores${params ? `?${new URLSearchParams(params)}` : ''}`),
    get: (id) => requestUpperCase(`cursos/formadores/${id}/`)
  }
}

export default dashboardService_2
