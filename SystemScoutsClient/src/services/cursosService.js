<<<<<<< HEAD
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
=======
const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')

async function request(path, options = {}) {
  const normPath = String(path).replace(/^\//, '')
  const needsSlash = !/\?(.*)$/.test(normPath) && !normPath.endsWith('/')
  const url = `${API_BASE}/${normPath}${needsSlash ? '/' : ''}`

  const isGet = !options.method || options.method.toUpperCase() === 'GET'
  const headers = { ...(options.headers || {}) }
  if (!isGet && !('Content-Type' in headers)) {
    headers['Content-Type'] = 'application/json'
  }

  const res = await fetch(url, {
    headers,
    ...options
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  return res.status === 204 ? null : res.json()
}

export default {
  async obtenerCursos() {
    const data = await request('cursos/curso') // Asumiendo que el endpoint es /api/cursos/curso/
    if (!Array.isArray(data)) return []
    return data
  },

  async agregarCurso(cursoData) {
    return request('cursos/curso', { method: 'POST', body: JSON.stringify(cursoData) })
  },

  async actualizarCurso(id, cursoData) {
    return request(`cursos/curso/${id}`, { method: 'PUT', body: JSON.stringify(cursoData) })
  },

  async eliminarCurso(id) {
    return request(`cursos/curso/${id}`, { method: 'DELETE' })
  },

  // --- Funciones para manejar las fechas del curso ---
  async obtenerFechas() {
    return request('cursos/fechas')
  },

  async guardarFecha(fechaData) {
    if (fechaData.CUF_ID) {
      // Si tiene ID, es una actualización (PUT)
      const { CUF_ID, ...data } = fechaData;
      return request(`cursos/fechas/${CUF_ID}`, { method: 'PUT', body: JSON.stringify(data) });
    } else {
      // Si no tiene ID, es una creación (POST)
      return request('cursos/fechas', { method: 'POST', body: JSON.stringify(fechaData) });
    }
  },

  // --- Funciones para manejar los coordinadores del curso ---
  async obtenerCoordinadores() {
    return request('cursos/coordinador');
  },

  async guardarCoordinador(coordinadorData) {
    return request('cursos/coordinador', { method: 'POST', body: JSON.stringify(coordinadorData) });
  },

  async eliminarCoordinador(id) {
    return request(`cursos/coordinador/${id}`, { method: 'DELETE' });
  },

  // --- Funciones para manejar las inscripciones (Persona_Curso) ---
  async obtenerInscripciones() {
    return request('personas/persona_curso');
  },

  async inscribirPersona(inscripcionData) {
    return request('personas/persona_curso', { method: 'POST', body: JSON.stringify(inscripcionData) });
  },

  async eliminarInscripcion(id) {
    return request(`personas/persona_curso/${id}`, { method: 'DELETE' });
>>>>>>> 0d07fbc23e917a3f08e27709965b056a4245f22b
  }
}
