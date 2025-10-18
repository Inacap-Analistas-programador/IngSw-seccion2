const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')

async function request(path, options = {}) {
  // Normalize path and ensure trailing slash for DRF list/detail endpoints
  const normPath = String(path).replace(/^\//, '')
  const needsSlash = !/\?(.*)$/.test(normPath) && !normPath.endsWith('/')
  const url = `${API_BASE}/${normPath}${needsSlash ? '/' : ''}`

  const isGet = !options.method || options.method.toUpperCase() === 'GET'
  const headers = { ...(options.headers || {}) }
  // Avoid forcing Content-Type on GET to prevent CORS preflight
  if (!isGet && !('Content-Type' in headers)) {
    headers['Content-Type'] = 'application/json'
  }

  const res = await fetch(url, {
    headers,
    // Do not include credentials unless needed; helps avoid stricter CORS
    // credentials: 'include',
    ...options
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  return res.status === 204 ? null : res.json()
}

function mapPersonaToPago(p) {
  return {
    id: p.PER_ID,
    nombre: [p.PER_NOMBRES, p.PER_APELPTA, p.PER_APELMAT].filter(Boolean).join(' '),
    rut: p.PER_RUN && p.PER_DV ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
    email: p.PER_MAIL,
    direccion: p.PER_DIRECCION,
    telefono: p.PER_FONO,
    fecha_nac: p.PER_FECHA_NAC,
    otros: p.PER_OTROS || '',
    raw: p
  }
}

export default {
  async obtenerPagos() {
    const data = await request('Persona')
    if (!Array.isArray(data)) return []
    return data.map(mapPersonaToPago)
  },

  async agregarPago(pago) {
    return request('Persona', { method: 'POST', body: JSON.stringify(pago) })
  },

  async createPersona(payload) {
    return request('create-persona/', { method: 'POST', body: JSON.stringify(payload) })
  },

  async eliminarPago(id) {
    return request(`Persona/${id}`, { method: 'DELETE' })
  },

  async anularPago(id) {
    const obj = await request(`Persona/${id}`)
    if (!obj) throw new Error('Objeto no encontrado')
    const updated = { ...obj, PER_VIGENTE: false }
    return request(`Persona/${id}`, { method: 'PUT', body: JSON.stringify(updated) })
  },

  async registrarDevolucion(id, datos) {
    // stub: registra devolucion en el frontend (no implementado en backend)
    console.log('registrarDevolucion:', id, datos)
    return Promise.resolve({ ok: true })
  },

  registrarAuditoria(accion, pago) {
    console.log('auditoria:', accion, pago)
  }
}
