import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

export const cursos = makeCrud('cursos')
export const cuotas = makeCrud('cuotas')
export const fechas = makeCrud('fechas')
export const alimentaciones = makeCrud('alimentaciones')
export const coordinadores = makeCrud('coordinadores')
export const secciones = makeCrud('secciones')
export const formadores = makeCrud('formadores')

export default { cursos, cuotas, fechas, alimentaciones, coordinadores, secciones, formadores }
