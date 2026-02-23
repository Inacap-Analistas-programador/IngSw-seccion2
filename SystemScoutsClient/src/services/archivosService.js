import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

// Archivo main resources
const baseArchivos = makeCrud('archivos')
export const archivos = {
  ...baseArchivos,
  uploadArchivo: (file, tarId = 1) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('tar_id', tarId)
    // Custom action: archivos/archivos/upload/ (due to router.register('archivos', ...) inside api/archivos/)
    return request('archivos/archivos/upload/', { method: 'POST', body: formData })
  }
}
// Sub-resources under archivos router
export const archivoCursos = makeCrud('archivos/cursos')
export const archivoPersonas = makeCrud('archivos/personas')

export default { archivos, archivoCursos, archivoPersonas }
