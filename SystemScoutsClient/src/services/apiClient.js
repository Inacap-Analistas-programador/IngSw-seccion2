// Simple API client wrapper around fetch with sensible defaults
// - Reads VITE_API_BASE (e.g., http://localhost:8000/api)
// - Normalizes paths and trailing slashes for DRF
// - Adds Authorization header if a token exists in localStorage

const API_BASE = (import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/$/, '')
// Raíz del backend (para endpoints fuera de /api como /login/ y /refresh/)
const API_ROOT = API_BASE.replace(/\/?api$/, '')

// Helper para obtener cookies (httpOnly no es accesible desde JS, pero las normales sí)
function getCookie(name) {
  if (typeof document === 'undefined') return null
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return null
}

function getAuthHeaders() {
  // Leer de la clave unificada; migrar silenciosamente si existen claves legacy
  let token = localStorage.getItem('auth_token')

  if (!token) {
    token = localStorage.getItem('accessToken') || localStorage.getItem('token')
    if (token) localStorage.setItem('auth_token', token) // migración silenciosa
  }

  if (!token) return {}
  return { Authorization: `Bearer ${token}` }
}

// Redirigir al login cuando el token no se puede renovar.
// Debounced: si múltiples requests fallan simultáneamente, solo redirige una vez.
let _redirectScheduled = false
function _redirectToLogin() {
  if (_redirectScheduled) return
  _redirectScheduled = true
  // Limpiar sesión
  ;['auth_token', 'token', 'accessToken', 'refreshToken'].forEach(k => {
    try { localStorage.removeItem(k) } catch { /* ignore */ }
  })
  setTimeout(() => {
    _redirectScheduled = false
    if (typeof window !== 'undefined' && window.location.pathname !== '/') {
      window.location.href = '/'
    }
  }, 100)
}

// Gestionar refresh de JWT evitando múltiples llamadas concurrentes
let refreshingPromise = null
async function refreshAccessToken() {
  if (refreshingPromise) return refreshingPromise

  // Intentar obtener refresh token de cookie primero, luego localStorage
  let refresh = getCookie('refresh_token') || getCookie('refreshToken')
  if (!refresh && typeof localStorage !== 'undefined') {
    refresh = localStorage.getItem('refreshToken')
  }
  if (!refresh) return false

  refreshingPromise = (async () => {
    try {
      const res = await fetch(`${API_ROOT}/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ refresh })
      })
      const text = await res.text()
      let data
      try { data = JSON.parse(text) } catch { data = null }
      if (!res.ok || !data?.access) throw new Error('refresh_failed')

      // El backend debería setear cookies httpOnly, pero guardamos en localStorage como fallback
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem('accessToken', data.access)
        localStorage.setItem('token', data.access)
      }
      return true
    } catch {
      // Limpiar localStorage si existe (las cookies httpOnly se limpian desde el backend)
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('token')
      }
      return false
    } finally {
      refreshingPromise = null
    }
  })()

  return refreshingPromise
}

export async function request(path, options = {}) {
  const normPath = String(path || '').replace(/^\//, '')
  // If normPath already contains a slash before '?', preserve it.
  // The previous logic `!/\?(.*)$/.test(normPath)` returned false if params existed, 
  // preventing the slash addition even if we wanted it.
  // New logic: If it ends with '/' OR contains '/?', don't add another.
  // But simpler: just trust the input if it has params. 
  // Actually, we want to force slash if it's missing before '?' for DRF.

  // DRF requires: /resource/?params not /resource?params
  // Let's check if we have params and NO slash before them.
  let finalPath = normPath
  if (finalPath.includes('?') && !finalPath.includes('/?')) {
    finalPath = finalPath.replace('?', '/?')
  } else if (!finalPath.includes('?') && !finalPath.endsWith('/')) {
    finalPath = `${finalPath}/`
  }

  const url = `${API_BASE}/${finalPath}`

  const isGet = !options.method || options.method.toUpperCase() === 'GET'
  const headers = { ...getAuthHeaders(), ...(options.headers || {}) }
  if (!isGet && !('Content-Type' in headers) && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  // Usar same-origin para desarrollo con localStorage (funciona sin configurar cookies en backend)
  // Cambiar a 'include' cuando el backend esté configurado para setear cookies
  const fetchOptions = {
    ...options,
    headers,
    credentials: 'same-origin'
  }

  let res = await fetch(url, fetchOptions)

  if (!res.ok && res.status === 401) {
    let bodyText = ''
    try { bodyText = await res.clone().text() } catch { /* ignore */ }

    if (/token_not_valid|Token is expired|expired/i.test(bodyText)) {
      // 1. Intentar refresh
      const ok = await refreshAccessToken()
      if (ok) {
        const retryHeaders = { ...headers, ...getAuthHeaders() }
        res = await fetch(url, { ...fetchOptions, headers: retryHeaders })
      } else {
        // 2. Refresh fallido → limpiar sesión y redirigir al login
        _redirectToLogin()
        throw new Error('401 Sesión expirada. Redirigiendo al login...')
      }
    } else {
      // 401 sin poder refrescar (sin token de refresh, o ruta de login misma)
      _redirectToLogin()
      throw new Error('401 No autorizado')
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
