import { request } from './apiClient'

// Elimina el /api inicial, solo usa /mantenedores/estado-civil/
const base = '/mantenedores/estado-civil/'

export const estadoCivilApi = {
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
}
