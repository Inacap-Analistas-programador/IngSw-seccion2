// Composable para gestionar permisos de usuario basados en roles
import { ref, computed, onMounted } from 'vue'
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

export function usePermissions() {
  const currentRole = ref('')

  const getRoleSync = () => {
    try {
      if (typeof document !== 'undefined') {
        const value = `; ${document.cookie}`
        const parts = value.split(`; currentUser=`)
        if (parts.length === 2) {
          const userCookie = parts.pop().split(';').shift()
          const user = JSON.parse(decodeURIComponent(userCookie))
          return user.role || user.rol || ''
        }
      }

      if (typeof localStorage !== 'undefined') {
        const currentUser = localStorage.getItem('currentUser')
        if (currentUser) {
          const user = JSON.parse(currentUser)
          return user.role || user.rol || ''
        }
      }
    } catch (e) {
      console.error('Error al obtener rol del usuario:', e)
    }
    return ''
  }

  // Inicializar síncronamente si es posible
  currentRole.value = getRoleSync()

  // Actualizar asegurando que estemos en el cliente / onMounted
  onMounted(async () => {
    try {
      const user = await authService.getCurrentUser()
      if (user) {
        currentRole.value = user.role || user.rol || ''
      }
    } catch (e) {
      console.error('Error onMounted al obtener rol', e)
    }
  })

  const getUserRole = async () => {
    try {
      const user = await authService.getCurrentUser()
      return user.role || user.rol || ''
    } catch (e) {
      console.error('Error al obtener rol del usuario:', e)
      return ''
    }
  }

  const isAdmin = computed(() => {
    const role = currentRole.value
    if (!role) return false
    return ADMIN_ROLES.some(adminRole =>
      role.toLowerCase().includes(adminRole.toLowerCase())
    )
  })

  const canCreate = computed(() => isAdmin.value)
  const canEdit = computed(() => isAdmin.value)
  const canDelete = computed(() => isAdmin.value)
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
