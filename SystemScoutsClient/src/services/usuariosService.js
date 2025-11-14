import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => {
    console.log('[usuariosService] PATCH URL base:', base, 'ID:', id, 'payload:', data)
    return request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) })
  },
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

export const usuarios = makeCrud('usuarios/usuarios')
export const perfiles = makeCrud('usuarios/perfiles')
export const aplicaciones = makeCrud('usuarios/aplicaciones')
export const perfilAplicaciones = makeCrud('usuarios/perfil-aplicaciones')

export default { usuarios, perfiles, aplicaciones, perfilAplicaciones }
