import { request } from './apiClient'

const base = 'mantenedores/estado-civil'

export const estadoCivilApi = {
  list: (params) => request(`${base}/${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
}
