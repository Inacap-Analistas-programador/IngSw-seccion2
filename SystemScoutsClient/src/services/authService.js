// Simple auth service to provide current user info and logout.
// Assumptions:
// - If your backend exposes an endpoint, you can replace getCurrentUser()
//   to call it (e.g., GET /api/me). For now, we read from localStorage
//   and fall back to a default user.

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

function logout() {
  // Clear any stored auth/user information
  localStorage.removeItem(STORAGE_KEY)
  localStorage.removeItem('token')
}

export default { getCurrentUser, setCurrentUser, logout }
