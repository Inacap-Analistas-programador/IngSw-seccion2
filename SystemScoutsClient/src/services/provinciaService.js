import { request } from './apiClient'

const base = '/mantenedores/provincia/'

export const provinciaApi = {
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
}
