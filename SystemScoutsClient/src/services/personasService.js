<<<<<<< HEAD
import { request } from './apiClient'

// Personas & related endpoints
// Base URLs per backend urls.py: /api/personas/
// Available routers: personas, grupos, individuales, niveles, cursos, estado-cursos, vehiculos
// For initial wiring, we provide a basic list from 'personas' and mappers to UI shape.

const BASE = 'personas/personas'

function formatRut(run, dv) {
  if (!run) return ''
  return dv ? `${run}-${dv}` : String(run)
}

function mapPersonaBasic(p) {
  return {
    id: p.PER_ID,
    nombre: [p.PER_NOMBRES, p.PER_APELPTA, p.PER_APELMAT].filter(Boolean).join(' ').trim(),
    rut: formatRut(p.PER_RUN, p.PER_DV),
    email: p.PER_MAIL || '',
    telefono: p.PER_FONO || '',
    fecha_nac: p.PER_FECHA_NAC || '',
    direccion: p.PER_DIRECCION || '',
    profesion: p.PER_PROFESION || '',
    // Placeholders until we combine with other endpoints
    rol: '',
    rama: '',
    grupo: '',
    estado: 'Vigente',
    vigente: !!p.PER_VIGENTE,
    raw: p
  }
}

export default {
  async listarBasic() {
    const data = await request(BASE)
    return Array.isArray(data) ? data.map(mapPersonaBasic) : []
  },
  async obtener(id) {
    const p = await request(`${BASE}/${id}`)
    return mapPersonaBasic(p)
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
  async obtenerPersonas() {
    const data = await request('personas') 
    if (!Array.isArray(data)) return []
    return data
  },
>>>>>>> 0d07fbc23e917a3f08e27709965b056a4245f22b
}
