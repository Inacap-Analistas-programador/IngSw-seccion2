import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

export const conceptoContable = makeCrud('concepto-contable')
export const tipoCursos = makeCrud('tipo-cursos')
export const tipoArchivos = makeCrud('tipo-archivos')
export const alimentacion = makeCrud('alimentacion')
export const rol = makeCrud('rol')
export const cargo = makeCrud('cargo')
export const rama = makeCrud('rama')
export const estadoCivil = makeCrud('estado-civil')
export const nivel = makeCrud('nivel')
export const zona = makeCrud('zona')
export const distrito = makeCrud('distrito')
export const grupo = makeCrud('grupo')
export const region = makeCrud('region')
export const provincia = makeCrud('provincia')
export const comuna = makeCrud('comuna')

export default {
  conceptoContable, tipoCursos, tipoArchivos, alimentacion, rol, cargo, rama,
  estadoCivil, nivel, zona, distrito, grupo, region, provincia, comuna
}
