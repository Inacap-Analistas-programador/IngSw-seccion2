import { request } from './apiClient'

const base = '/mantenedores/comuna/'

export const comunaApi = {
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
}
