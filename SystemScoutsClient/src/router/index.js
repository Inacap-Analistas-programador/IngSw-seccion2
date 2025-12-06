import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'

// Lazy-load views to keep bundle small
const Dashboard = () => import('@/views/Dashboard.vue')
// Variantes alternativas (pantallas 2)
const Dashboard2 = () => import('@/views/Dashboard2.vue')
const Mantenedores = () => import('@/views/mantenedores.vue')
const Gestionpersonas = () => import('@/views/Gestionpersonas.vue')
const PagosView = () => import('@/views/PagosView.vue')
const Correos = () => import('@/views/Correos.vue')
const ManualAcreditation = () => import('@/views/ManualAcreditation.vue')
const VerificadorQR = () => import('@/views/VerificadorQR.vue')
const UsuariosRoles = () => import('@/views/Usuarios.vue')
const Roles = () => import('@/views/Roles.vue')
const CursosCapacitaciones = () => import('@/views/CRUDcursos.vue')
const Login = () => import('@/views/Login.vue')
const FormularioPreInscripcion = () => import('@/views/Formulario.vue')
const FormularioPreInscripcion2 = () => import('@/views/Formulario2.vue')
const Mantenedores2 = () => import('@/views/mantenedores2.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: Login },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: Dashboard, 
      meta: { requiresAuth: true } 
    },
    { 
      path: '/dashboard-2', 
      name: 'dashboard2', 
      component: Dashboard2, 
      meta: { requiresAuth: true } 
    },
    { 
      path: '/usuarios', 
      name: 'usuarios', 
      component: UsuariosRoles, 
      meta: { requiresAuth: true, module: 'Usuarios' } 
    },
    { 
      path: '/roles', 
      name: 'roles', 
      component: Roles, 
      meta: { requiresAuth: true, module: 'Perfiles' } 
    },
    // Mantenedores admite pestaña vía parámetro opcional
    { 
      path: '/mantenedores/:tab?', 
      name: 'mantenedores', 
      component: Mantenedores, 
      props: true, 
      meta: { requiresAuth: true, module: 'Mantenedores' } 
    },
    { 
      path: '/mantenedores-2', 
      name: 'mantenedores2', 
      component: Mantenedores2, 
      meta: { requiresAuth: true } 
    },
    { 
      path: '/gestionpersonas', 
      name: 'gestionpersonas', 
      component: Gestionpersonas, 
      meta: { requiresAuth: true, module: 'Personas' } 
    },
    { 
      path: '/pagos', 
      name: 'pagos', 
      component: PagosView, 
      meta: { requiresAuth: true, module: 'Pagos' } 
    },
    { 
      path: '/manual-acreditacion', 
      name: 'manualacreditacion', 
      component: ManualAcreditation, 
      meta: { requiresAuth: true, module: 'AcreditacionManual' } 
    },
    { 
      path: '/verificador-qr', 
      name: 'verificadorqr', 
      component: VerificadorQR, 
      meta: { requiresAuth: true, module: 'VerificadorQR' } 
    },
    { 
      path: '/correos', 
      name: 'correos', 
      component: Correos, 
      meta: { requiresAuth: true, module: 'Correos' } 
    },
    { 
      path: '/cursos-capacitaciones', 
      name: 'cursoscapacitaciones', 
      component: CursosCapacitaciones, 
      meta: { requiresAuth: true, module: 'Cursos' } 
    },
    { path: '/inscripciones', name: 'formularioPreInscripcion', component: FormularioPreInscripcion },
    // CORRECCIÓN: Esta ruta debe coincidir exactamente con el enlace en SideBar.vue
    { path: '/inscripciones-2', name: 'formularioPreInscripcion2', component: FormularioPreInscripcion2, meta: { requiresAuth: true } },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/dashboard-2' },
  ],
})

// Auth guard: controlado por variable de entorno para modo pruebas visuales
// Usa VITE_DISABLE_AUTH_GUARD=true en .env.development para desactivar el guard en desarrollo
const DISABLE_AUTH_GUARD = String(import.meta.env.VITE_DISABLE_AUTH_GUARD || '').toLowerCase() === 'true'

router.beforeEach(async (to, from, next) => {
  if (DISABLE_AUTH_GUARD) return next()
  
  let token = localStorage.getItem('token') || localStorage.getItem('accessToken')
  // Normalizar: si sólo existe accessToken, duplica en 'token' para compatibilidad
  if (!localStorage.getItem('token') && token) {
    try { localStorage.setItem('token', token) } catch {}
  }
  
  // Verificar autenticación
  if (to.meta?.requiresAuth && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  // Verificar permisos por módulo
  if (to.meta?.module) {
    const hasAccess = await authService.hasPermission(to.meta.module, 'consultar')
    if (!hasAccess) {
      console.warn(`Acceso denegado a ${to.path}. Módulo requerido: ${to.meta.module}`)
      next({ name: 'dashboard' })
      return
    }
  }
  
  // Verificar roles (Legacy support, if any routes still use it)
  if (to.meta?.roles) {
    const user = await authService.getCurrentUser()
    if (user) {
      const userRole = user.role || ''
      // Si el rol del usuario no está en la lista de permitidos
      if (!to.meta.roles.includes(userRole)) {
        // Redirigir a dashboard o página de acceso denegado
        console.warn(`Acceso denegado a ${to.path}. Rol requerido: ${to.meta.roles.join(', ')}. Rol actual: ${userRole}`)
        next({ name: 'dashboard' })
        return
      }
    } else {
      // No hay usuario, redirigir a login
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  // Verificar rol de administrador si es requerido (Legacy check)
  if (to.meta?.requiresAdmin) {
    const user = await authService.getCurrentUser()
    if (user) {
      const userRole = user.role || ''
      
      if (userRole !== 'Administradora Regional') {
        // Si no es administrador, redirigir al dashboard
        next({ name: 'dashboard' })
        return
      }
    } else {
      // No hay usuario, redirigir a login
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  // Evitar loop si ya está logueado y va a login
  if (to.name === 'login' && token) {
    next({ name: 'dashboard' })
    return
  }
  
  next()
})

export default router