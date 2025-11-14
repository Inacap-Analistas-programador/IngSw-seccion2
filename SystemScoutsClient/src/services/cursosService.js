import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}/${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(`${base}/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

// NOTE: Backend mounts course routes under /api/cursos/
// Base paths should NOT have trailing slash; makeCrud adds '/' between base and ID
export const cursos = makeCrud('cursos/cursos')
export const cuotas = makeCrud('cursos/cuotas')
export const fechas = makeCrud('cursos/fechas')
export const alimentaciones = makeCrud('cursos/alimentaciones')
export const coordinadores = makeCrud('cursos/coordinadores')
export const secciones = makeCrud('cursos/secciones')
export const formadores = makeCrud('cursos/formadores')

export default { cursos, cuotas, fechas, alimentaciones, coordinadores, secciones, formadores }
