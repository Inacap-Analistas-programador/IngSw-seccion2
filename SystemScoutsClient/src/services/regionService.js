import { request } from './apiClient'

const base = '/mantenedores/region/'

export const regionApi = {
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
}
