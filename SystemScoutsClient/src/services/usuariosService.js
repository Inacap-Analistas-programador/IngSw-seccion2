import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}/${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(`${base}/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => {
    console.log('[usuariosService] PATCH URL base:', base, 'ID:', id, 'payload:', data)
    return request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) })
  },
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

// Mapeo a las rutas de Django
export const usuarios = makeCrud('usuarios/usuarios')
export const perfiles = makeCrud('usuarios/perfiles') // Ahora maneja django.contrib.auth.Group
export const aplicaciones = makeCrud('usuarios/aplicaciones') // Ahora maneja django.contrib.auth.Permission

export default { usuarios, perfiles, aplicaciones }

