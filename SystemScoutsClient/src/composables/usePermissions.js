/**
 * usePermissions.js
 * Composable que consulta permisos de un módulo dado para el usuario actual.
 *
 * Optimizaciones vs versión anterior:
 * - Una sola llamada a getCurrentUser() (en vez de 5)
 * - Lookup de permisos en memoria (sincrónico sobre el payload del JWT)
 * - Soporte explícito de isAdmin desde payload JWT
 */
import { ref, onMounted } from 'vue'
import authService from '@/services/authService'

const ACTIONS = ['consultar', 'ingresar', 'modificar', 'eliminar']

/**
 * @param {string} moduleName - Nombre del módulo (Dashboard, Personas, etc.)
 */
export function usePermissions(moduleName) {
  const can = ref(Object.fromEntries(ACTIONS.map(a => [a, false])))
  const isAdmin = ref(false)
  const loading = ref(true)

  const updatePermissions = async () => {
    if (!moduleName) {
      loading.value = false
      return
    }

    loading.value = true
    try {
      const user = await authService.getCurrentUser()
      if (!user) return

      isAdmin.value = user.isAdmin

      // Admins: acceso total sin buscar en aplicaciones
      if (user.isAdmin) {
        ACTIONS.forEach(a => (can.value[a] = true))
        return
      }

      const apps = user.payload?.aplicaciones
      if (!apps?.length) return

      const normalizedModule = moduleName.trim().toLowerCase()

      // Alias especial: cualquier sub-módulo Mantenedor
      let app
      if (normalizedModule === 'mantenedores') {
        app = apps.find(a =>
          (a.apl_descripcion || '').startsWith('Mantenedor - ') &&
          a.permisos?.pea_consultar === true
        )
      } else {
        app = apps.find(a =>
          (a.apl_descripcion || a.APL_DESCRIPCION || '').toLowerCase() === normalizedModule
        )
      }

      if (!app?.permisos) return

      // Mapear cada acción desde el payload (sin N llamadas a hasPermission)
      ACTIONS.forEach(a => {
        const key = `pea_${a}`
        can.value[a] = app.permisos[key] === true || app.permisos[key.toUpperCase()] === true
      })
    } catch (e) {
      console.error(`[usePermissions] Error cargando permisos para "${moduleName}":`, e)
    } finally {
      loading.value = false
    }
  }

  onMounted(updatePermissions)

  return { can, isAdmin, loading, refreshPermissions: updatePermissions }
}
