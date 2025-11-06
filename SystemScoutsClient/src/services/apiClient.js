// Simple API client wrapper around fetch with sensible defaults
// - Reads VITE_API_BASE (e.g., http://localhost:8000/api)
// - Normalizes paths and trailing slashes for DRF
// - Adds Authorization header if a token exists in localStorage

const API_BASE = (import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')
// Raíz del backend (para endpoints fuera de /api como /login/ y /refresh/)
const API_ROOT = API_BASE.replace(/\/?api$/, '')

function getAuthHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('accessToken')
  if (!token) return {}
  // Adjust prefix if your backend expects a different scheme
  return { Authorization: `Bearer ${token}` }
}

// Gestionar refresh de JWT evitando múltiples llamadas concurrentes
let refreshingPromise = null
async function refreshAccessToken() {
  if (refreshingPromise) return refreshingPromise
  const refresh = localStorage.getItem('refreshToken')
  if (!refresh) return false

  refreshingPromise = (async () => {
    try {
      const res = await fetch(`${API_ROOT}/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
      })
      const text = await res.text()
      let data
      try { data = JSON.parse(text) } catch { data = null }
      if (!res.ok || !data?.access) throw new Error('refresh_failed')
      localStorage.setItem('accessToken', data.access)
      localStorage.setItem('token', data.access)
      return true
    } catch (e) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('token')
      return false
    } finally {
      refreshingPromise = null
    }
  })()

  return refreshingPromise
}

export async function request(path, options = {}) {
  const normPath = String(path || '').replace(/^\//, '')
  const needsSlash = !/\?(.*)$/.test(normPath) && !normPath.endsWith('/')
  const url = `${API_BASE}/${normPath}${needsSlash ? '/' : ''}`

  const isGet = !options.method || options.method.toUpperCase() === 'GET'
  const headers = { ...getAuthHeaders(), ...(options.headers || {}) }
  if (!isGet && !('Content-Type' in headers) && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  let res = await fetch(url, { ...options, headers })
  if (!res.ok && res.status === 401) {
    // intentar refresh si el token expiró
    // Usar un clon para leer el cuerpo sin consumir el original
    let bodyText = ''
    try { bodyText = await res.clone().text() } catch {}
    if (/token_not_valid|Token is expired|expired/i.test(bodyText)) {
      const ok = await refreshAccessToken()
      if (ok) {
        const retryHeaders = { ...headers, ...getAuthHeaders() }
        res = await fetch(url, { ...options, headers: retryHeaders })
      }
    }
  }
  if (!res.ok) {
    // Importante: usar un clon para evitar "body stream already read"
    // cuando json() falla y luego se intenta text() sobre el mismo Response
    const errClone = res.clone()
    let detail
    try {
      detail = await errClone.json()
    } catch {
      try { detail = await errClone.text() } catch { detail = '' }
    }
    throw new Error(`${res.status} ${res.statusText}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`)
  }
  if (res.status === 204) return null
  const contentType = res.headers.get('content-type') || ''
  return contentType.includes('application/json') ? res.json() : res.text()
}

export function buildUrl(...parts) {
  return `${API_BASE}/${parts.map(p => String(p).replace(/^\/+|\/+$/g, '')).join('/')}/`
}
