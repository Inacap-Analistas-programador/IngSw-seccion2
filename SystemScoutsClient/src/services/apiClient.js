// Simple API client wrapper around fetch with sensible defaults
// - Reads VITE_API_BASE (e.g., http://localhost:8000/api)
// - Normalizes paths and trailing slashes for DRF
// - Adds Authorization header if a token exists in localStorage

const API_BASE = (import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')

function getAuthHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('accessToken')
  if (!token) return {}
  // Adjust prefix if your backend expects a different scheme
  return { Authorization: `Bearer ${token}` }
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

  const res = await fetch(url, { ...options, headers })
  if (!res.ok) {
    let detail
    try { detail = await res.json() } catch { detail = await res.text() }
    throw new Error(`${res.status} ${res.statusText}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`)
  }
  if (res.status === 204) return null
  const contentType = res.headers.get('content-type') || ''
  return contentType.includes('application/json') ? res.json() : res.text()
}

export function buildUrl(...parts) {
  return `${API_BASE}/${parts.map(p => String(p).replace(/^\/+|\/+$/g, '')).join('/')}/`
}
