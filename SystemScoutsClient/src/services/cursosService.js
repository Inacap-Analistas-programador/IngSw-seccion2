import { request } from './apiClient'

// Cursos endpoints per backend: /api/cursos/
// Routers likely include: cursos, cuotas, fechas, secciones, etc.

const BASE = 'cursos/cursos'
const CUOTAS = 'cursos/curso-cuota' // Check exact router name; fallback to 'cursos/cuotas'

function mapCurso(c) {
  return {
    id: c.CUR_ID || c.id,
    codigo: c.CUR_CODIGO || '',
    nombre: c.CUR_DESCRIPCION || '',
    estado: c.CUR_ESTADO,
    // Optional enrichments can be added by joining cuotas, fechas, etc.
    raw: c
  }
}

export default {
  async listar() {
    const data = await request(BASE)
    return Array.isArray(data) ? data.map(mapCurso) : []
  },
  async obtener(id) {
    const c = await request(`${BASE}/${id}`)
    return mapCurso(c)
  },
  async crear(payload) {
    // Espera un payload con nombres de campos del backend (e.g., CUR_CODIGO, CUR_DESCRIPCION, etc.)
    // Nota: La creación de Curso requiere múltiples campos obligatorios en el backend.
    // Asegúrate de enviar todos los requeridos.
    const res = await request(BASE, { method: 'POST', body: JSON.stringify(payload) })
    return mapCurso(res)
  },
  async actualizar(id, patch) {
    // Usa PATCH para actualizar parcialmente campos como CUR_DESCRIPCION, CUR_CODIGO, etc.
    const res = await request(`${BASE}/${id}`, { method: 'PATCH', body: JSON.stringify(patch) })
    return mapCurso(res)
  },
  async eliminar(id) {
    await request(`${BASE}/${id}`, { method: 'DELETE' })
    return true
  },
  async listarCuotas() {
    // Try common paths
    try {
      return await request('cursos/curso_cuota')
    } catch {
      try {
        return await request('cursos/cuotas')
      } catch {
        return []
      }
    }
  }
}
