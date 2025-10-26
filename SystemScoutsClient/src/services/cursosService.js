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
