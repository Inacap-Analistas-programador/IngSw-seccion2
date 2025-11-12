// Composable para gestionar permisos de usuario basados en roles
import { computed } from 'vue'
import authService from '@/services/authService'

// Lista de roles con permisos de administración (pueden crear, editar y eliminar)
const ADMIN_ROLES = [
  'Administrador',
  'Administradora',
  'Administrador Regional',
  'Administradora Regional',
  'Admin',
  'admin'
]

// Lista de roles con permisos de solo lectura
const READONLY_ROLES = [
  'Invitado',
  'Usuario',
  'Visitante',
  'Lector'
]

export function usePermissions() {
  // Obtener rol del usuario actual desde authService (soporta cookies y localStorage)
  const getUserRole = async () => {
    try {
      const user = await authService.getCurrentUser()
      return user.role || ''
    } catch (e) {
      console.error('Error al obtener rol del usuario:', e)
      return ''
    }
  }

  // Cache del rol para evitar múltiples llamadas async
  let cachedRole = null
  const getRoleSync = () => {
    if (cachedRole !== null) return cachedRole
    
    // Intentar obtener de forma síncrona para compatibilidad con computed
    try {
      // Intenta desde cookie primero
      if (typeof document !== 'undefined') {
        const value = `; ${document.cookie}`
        const parts = value.split(`; currentUser=`)
        if (parts.length === 2) {
          const userCookie = parts.pop().split(';').shift()
          const user = JSON.parse(decodeURIComponent(userCookie))
          cachedRole = user.role || user.rol || ''
          return cachedRole
        }
      }
      
      // Fallback a localStorage
      if (typeof localStorage !== 'undefined') {
        const currentUser = localStorage.getItem('currentUser')
        if (currentUser) {
          const user = JSON.parse(currentUser)
          cachedRole = user.role || user.rol || ''
          return cachedRole
        }
      }
    } catch (e) {
      console.error('Error al obtener rol del usuario:', e)
    }
    return ''
  }

  // Verificar si el usuario tiene rol de administrador
  const isAdmin = computed(() => {
    const role = getRoleSync()
    return ADMIN_ROLES.some(adminRole => 
      role.toLowerCase().includes(adminRole.toLowerCase())
    )
  })

  // Verificar si el usuario puede crear registros
  const canCreate = computed(() => isAdmin.value)

  // Verificar si el usuario puede editar registros
  const canEdit = computed(() => isAdmin.value)

  // Verificar si el usuario puede eliminar/anular registros
  const canDelete = computed(() => isAdmin.value)

  // Verificar si el usuario solo tiene permisos de lectura
  const isReadOnly = computed(() => !isAdmin.value)

  return {
    isAdmin,
    canCreate,
    canEdit,
    canDelete,
    isReadOnly,
    getUserRole
  }
}
