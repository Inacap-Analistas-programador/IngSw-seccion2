/**
 * useSidebarAccess.js
 * Composable que centraliza la lógica de visibilidad del sidebar.
 * Extrae responsabilidades de SideBar.vue — mantiene el componente declarativo.
 */
import { ref, computed } from 'vue'
import authService from '@/services/authService'

const MANTENEDOR_PREFIX = 'Mantenedor - '

/**
 * Comprueba si una aplicación del JWT tiene acceso (pea_consultar).
 */
function appHasAccess(app) {
  return app?.permisos?.pea_consultar === true
}

/**
 * Busca una aplicación por nombre exacto (case-insensitive).
 */
function findApp(apps, name) {
  const needle = name.toLowerCase()
  return apps.find(a =>
    (a.apl_descripcion || a.APL_DESCRIPCION || '').toLowerCase() === needle
  )
}

export function useSidebarAccess() {
  const access = ref({
    usuarios: false,
    perfiles: false,
    cursos: false,
    personas: false,
    pagos: false,
    correos: false,
    mantenedores: false,
    acreditacionManual: false,
    verificadorQR: false,
  })

  const isAdmin = ref(false)

  /**
   * Actualiza el objeto access según el payload del JWT.
   * Puede llamarse al montar el sidebar y al cambiar la sesión.
   */
  async function updateAccess() {
    const user = await authService.getCurrentUser()

    if (!user) {
      Object.keys(access.value).forEach(k => (access.value[k] = false))
      isAdmin.value = false
      return
    }

    isAdmin.value = user.isAdmin

    // Admin: acceso total sin buscar en aplicaciones
    if (user.isAdmin) {
      Object.keys(access.value).forEach(k => (access.value[k] = true))
      return
    }

    const apps = user.payload?.aplicaciones || []
    const check = (name) => {
      const app = findApp(apps, name)
      return appHasAccess(app)
    }

    access.value = {
      usuarios: check('Usuarios'),
      perfiles: check('Perfiles'),
      cursos: check('Cursos'),
      personas: check('Personas'),
      pagos: check('Pagos'),
      correos: check('Correos'),
      // Mantenedores: visible si el usuario tiene acceso a CUALQUIER sub-módulo
      mantenedores: apps.some(a =>
        (a.apl_descripcion || '').startsWith(MANTENEDOR_PREFIX) && appHasAccess(a)
      ),
      acreditacionManual: check('AcreditacionManual'),
      verificadorQR: check('VerificadorQR'),
    }
  }

  return { access, isAdmin, updateAccess }
}
