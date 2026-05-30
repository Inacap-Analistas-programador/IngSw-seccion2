/**
 * mantenedoresService.js
 * Capa de acceso a datos para todos los mantenedores del sistema.
 *
 * Patrón: makeCrud(path) genera operaciones CRUD estándar.
 * Todos los paths usan el prefijo 'mantenedores/' consistentemente.
 * Los endpoints de pago se ubican en su prefijo correcto 'pagos/'.
 */
import { request } from './apiClient'

/**
 * Genera operaciones CRUD estándar para un endpoint dado.
 * @param {string} base - Path relativo al API_BASE (ej: 'mantenedores/zona')
 */
const makeCrud = (base) => ({
  list: (params) => {
    const qs = params ? `?${new URLSearchParams(params)}` : ''
    return request(`${base}/${qs}`)
  },
  listMin: () => request(`${base}/min/`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

const M = 'mantenedores'

export const conceptoContable = makeCrud(`${M}/concepto-contable`)
export const tipoCursos       = makeCrud(`${M}/tipo-cursos`)
export const tipoArchivos     = makeCrud(`${M}/tipo-archivos`)
export const alimentacion     = makeCrud(`${M}/alimentacion`)
export const rol              = makeCrud(`${M}/rol`)
export const cargo            = makeCrud(`${M}/cargo`)
export const rama             = makeCrud(`${M}/rama`)
export const estadoCivil      = makeCrud(`${M}/estado-civil`)
export const nivel            = makeCrud(`${M}/nivel`)
export const zona             = makeCrud(`${M}/zona`)
export const distrito         = makeCrud(`${M}/distrito`)
export const grupo            = makeCrud(`${M}/grupo`)
export const region           = makeCrud(`${M}/region`)
export const provincia        = makeCrud(`${M}/provincia`)
export const comuna           = makeCrud(`${M}/comuna`)

// Proveedor pertenece al dominio de pagos
export const proveedorPago    = makeCrud('pagos/proveedor')

export default {
  conceptoContable,
  tipoCursos,
  tipoArchivos,
  alimentacion,
  rol,
  cargo,
  rama,
  estadoCivil,
  nivel,
  zona,
  distrito,
  grupo,
  region,
  provincia,
  comuna,
  proveedorPago,
}
