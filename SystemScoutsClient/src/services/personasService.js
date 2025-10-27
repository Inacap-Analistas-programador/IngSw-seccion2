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
}
