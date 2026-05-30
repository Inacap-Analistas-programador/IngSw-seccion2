/**
 * authService.js
 * Responsabilidades: login, logout, sesión y decodificación de JWT.
 * La verificación de permisos se delega a usePermissions() composable.
 */

const API_URL = (import.meta.env?.VITE_API_BASE || 'http://127.0.0.1:8000').replace(/\/api\/?$/, '')

// ─── Claves de sesión (fuente de verdad única) ─────────────────────────────
const TOKEN_KEY = 'auth_token'
const REFRESH_KEY = 'auth_refresh'

function setSession(access, refresh) {
  localStorage.setItem(TOKEN_KEY, access)
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh)
}

function clearSession() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
  // Limpiar claves legacy para evitar tokens huérfanos
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('token')
}

function getToken() {
  // Leer de clave nueva primero; si no existe, migrar desde clave legacy en caliente
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) return token

  const legacy = localStorage.getItem('accessToken') || localStorage.getItem('token')
  if (legacy) {
    // Migración silenciosa: escribir en la nueva clave
    localStorage.setItem(TOKEN_KEY, legacy)
  }
  return legacy
}

// ─── Decode JWT ────────────────────────────────────────────────────────────
function decodeJwtPayload(token) {
  try {
    const base64Url = token.split('.')[1]
    if (!base64Url) return null
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const padded = base64.padEnd(base64.length + (4 - (base64.length % 4)) % 4, '=')
    return JSON.parse(atob(padded))
  } catch {
    return null
  }
}

// ─── API pública ───────────────────────────────────────────────────────────
export default {
  getToken,

  async login(username, password) {
    const response = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })

    const text = await response.text()
    let data
    try {
      data = JSON.parse(text)
    } catch {
      throw new Error('Respuesta inesperada del servidor')
    }

    if (!response.ok) {
      throw new Error(data.detail || `Error al iniciar sesión (${response.status})`)
    }

    if (data.access) {
      setSession(data.access, data.refresh)
    }

    return data
  },

  logout() {
    clearSession()
  },

  /** Alias de getToken para compatibilidad con apiClient.js */
  getAccessToken() {
    return getToken()
  },

  /**
   * Decodifica el JWT actual y devuelve datos del usuario.
   * Opera completamente en memoria (sin llamadas de red).
   */
  async getCurrentUser() {
    const token = getToken()
    if (!token) return null

    const payload = decodeJwtPayload(token)
    if (!payload) return null

    const id = payload.usu_id || payload.user_id || payload.id || null
    const username = payload.usu_username || payload.username || payload.sub || null
    const name = payload.name || username || 'Usuario'
    const avatarUrl = payload.usu_ruta_foto || payload.USU_RUTA_FOTO || null

    let role = 'Invitado'
    if (payload.perfil?.pel_descripcion) role = payload.perfil.pel_descripcion
    else if (payload.perfil?.PEL_DESCRIPCION) role = payload.perfil.PEL_DESCRIPCION

    // is_admin: solo se confía en el claim is_superuser emitido por Django.
    // NO se usa el nombre del rol para evitar escalada de privilegios por nombre de perfil.
    const isAdmin = payload.is_superuser === true

    return { id, username, name, role, isAdmin, avatarUrl, payload }
  },

  /**
   * Verifica si el usuario tiene un permiso específico para un módulo.
   * Admite el alias 'Mantenedores' para cualquier módulo 'Mantenedor - *'.
   */
  async hasPermission(moduleName, action = 'consultar') {
    try {
      const user = await this.getCurrentUser()
      if (!user) return false

      // Administradores: acceso total
      if (user.isAdmin) return true

      const normalizedModule = String(moduleName).trim().toLowerCase()

      // Dashboard: acceso público para usuarios autenticados
      if (normalizedModule === 'dashboard') return true

      const apps = user.payload?.aplicaciones
      if (!apps?.length) return false

      const permKey = `pea_${String(action).trim().toLowerCase()}`

      // Alias especial: "Mantenedores" = acceso a cualquier sub-módulo Mantenedor
      if (normalizedModule === 'mantenedores') {
        return apps.some(a => {
          const name = a.apl_descripcion || a.APL_DESCRIPCION || ''
          return name.startsWith('Mantenedor - ') &&
            a.permisos?.pea_consultar === true
        })
      }

      const app = apps.find(a => {
        const name = a.apl_descripcion || a.APL_DESCRIPCION || ''
        return name.toLowerCase() === normalizedModule
      })

      if (!app?.permisos) return false

      return app.permisos[permKey] === true || app.permisos[permKey.toUpperCase()] === true
    } catch {
      return false
    }
  }
}