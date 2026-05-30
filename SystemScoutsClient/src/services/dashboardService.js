/**
 * dashboardService.js
 * Servicio unificado para el Dashboard.
 *
 * Fusión de dashboardService.js (legacy) y dashboardService_2.js.
 * `dashboardService_2.js` puede eliminarse de la carpeta una vez
 * actualizado Dashboard.vue para importar desde aquí.
 */
import { request } from './apiClient'

// ─── Transformación de claves ──────────────────────────────────────────────
// Dashboard.vue espera claves en MAYÚSCULAS por herencia del backend antiguo.
// Esta función normaliza la respuesta sin modificar el apiClient ni las vistas.
function toUpperKeys(value) {
  if (Array.isArray(value)) return value.map(toUpperKeys)
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) => [k.toUpperCase(), toUpperKeys(v)])
    )
  }
  return value
}

async function requestUpper(path, params) {
  const qs = params ? `?${new URLSearchParams(params)}` : ''
  const data = await request(`${path}${qs}`)
  // Desenvuelve paginación si es necesario
  if (data?.results) return { ...data, results: toUpperKeys(data.results) }
  return toUpperKeys(data)
}

// ─── API pública ───────────────────────────────────────────────────────────
const dashboardService = {
  cursos: {
    list: (params) => requestUpper('cursos/cursos', params),
    get: (id) => requestUpper(`cursos/cursos/${id}/`),
  },
  personas: {
    list: (params) => requestUpper('personas/personas', params),
    get: (id) => requestUpper(`personas/personas/${id}/`),
  },
  personaCursos: {
    list: (params) => requestUpper('personas/cursos', params),
    get: (id) => requestUpper(`personas/cursos/${id}/`),
  },
  pagoPersona: {
    list: (params) => requestUpper('pagos/pago-persona', params),
    get: (id) => requestUpper(`pagos/pago-persona/${id}/`),
  },
  coordinadores: {
    list: (params) => requestUpper('cursos/coordinadores', params),
    get: (id) => requestUpper(`cursos/coordinadores/${id}/`),
  },
  formadores: {
    list: (params) => requestUpper('cursos/formadores', params),
    get: (id) => requestUpper(`cursos/formadores/${id}/`),
  },
  // Alias compactos para estadísticas (heredados del dashboardService original)
  getCursoResumen: (id) => request(`cursos/${id}/resumen/`),
  getEstadisticasGlobales: () => request('estadisticas/dashboard/'),
}

export default dashboardService
