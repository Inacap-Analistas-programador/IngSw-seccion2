// Auth service: login, current user and logout helpers.
// - login() calls backend /api/auth/login/
// - current user info stored in localStorage
// - token persisted under 'token' key for apiClient to pick up

import { request } from './apiClient'

const STORAGE_KEY = 'currentUser'

async function getCurrentUser() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      return {
        name: parsed.name || parsed.nombre || 'Usuario',
        role: parsed.role || parsed.rol || '',
        avatarUrl: parsed.avatarUrl || parsed.foto || parsed.avatar || null,
      }
    }
  } catch (e) {
    // ignore
  }
  // Default placeholder user
  return {
    name: 'Usuario',
    role: '',
    avatarUrl: null,
  }
}

function setCurrentUser(user) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user || {}))
}

async function login(username, password) {
  const data = await request('auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
  if (data && data.token) {
    localStorage.setItem('token', data.token)
  }
  if (data && data.user) {
    setCurrentUser({
      name: data.user.USU_USERNAME,
      role: '',
      avatarUrl: data.user.USU_RUTA_FOTO || null
    })
  }
  return data
}

function logout() {
  // Clear any stored auth/user information
  localStorage.removeItem(STORAGE_KEY)
  localStorage.removeItem('token')
}

export default { getCurrentUser, setCurrentUser, login, logout }
