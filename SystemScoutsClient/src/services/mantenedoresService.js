const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')

async function request(path, options = {}) {
  const normPath = String(path).replace(/^\//, '')
  const url = `${API_BASE}/${normPath}/` // Ensure trailing slash for DRF

  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  return res.status === 204 ? null : res.json()
}

export default {
  async obtenerCargos() {
    return request('mantenedores/cargo')
  },
  async obtenerTiposCurso() {
    return request('mantenedores/tipo_curso')
  },
  async obtenerComunas() {
    return request('mantenedores/comuna')
  },
  async obtenerRoles() {
    return request('mantenedores/rol')
  }
  // Aquí se pueden añadir funciones para otros mantenedores en el futuro
}
