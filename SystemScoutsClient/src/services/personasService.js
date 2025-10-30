import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

// The API registers these resources under the 'personas' prefix (see API root).
export const personas = makeCrud('personas/personas')
export const grupos = makeCrud('personas/grupos')
export const formadores = makeCrud('personas/formadores')
export const individuales = makeCrud('personas/individuales')
export const niveles = makeCrud('personas/niveles')
export const personaCursos = makeCrud('personas/cursos') // persona-curso router registered under personas
export const estadoCursos = makeCrud('personas/estado-cursos')
export const vehiculos = makeCrud('personas/vehiculos')

export default { personas, grupos, formadores, individuales, niveles, personaCursos, estadoCursos, vehiculos }
