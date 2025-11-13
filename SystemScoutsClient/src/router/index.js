import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load views to keep bundle small
const Dashboard = () => import('@/views/Dashboard.vue')
// Variantes alternativas (pantallas 2)
const Dashboard2 = () => import('@/views/Dashboard 2.vue')
const Mantenedores = () => import('@/views/mantenedores.vue')
const Gestionpersonas = () => import('@/views/Gestionpersonas.vue')
const PagosView = () => import('@/views/PagosView.vue')
const Correos = () => import('@/views/Correos.vue')
const ManualAcreditation = () => import('@/views/ManualAcreditation.vue')
const VerificadorQR = () => import('@/views/VerificadorQR.vue')
const UsuariosRoles = () => import('@/views/UsuariosRoles.vue')
const CursosCapacitaciones = () => import('@/views/CRUDcursos.vue')
const Login = () => import('@/views/Login.vue')
const FormularioPreInscripcion = () => import('@/views/Formulario.vue')
const FormularioPreInscripcion2 = () => import('@/views/Formulario 2.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: Login },
    { path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/dashboard-2', name: 'dashboard2', component: Dashboard2, meta: { requiresAuth: true } },
    { path: '/usuarios', name: 'usuarios', component: UsuariosRoles, meta: { requiresAuth: true } },
  // Mantenedores admite pestaña vía parámetro opcional
  { path: '/mantenedores/:tab?', name: 'mantenedores', component: Mantenedores, props: true, meta: { requiresAuth: true } },
    { path: '/gestionpersonas', name: 'gestionpersonas', component: Gestionpersonas, meta: { requiresAuth: true } },
    { path: '/pagos', name: 'pagos', component: PagosView, meta: { requiresAuth: true } },
  { path: '/manual-acreditacion', name: 'manualacreditacion', component: ManualAcreditation, meta: { requiresAuth: true } },
  { path: '/verificador-qr', name: 'verificadorqr', component: VerificadorQR, meta: { requiresAuth: true, requiresAuth: true } },
    { path: '/correos', name: 'correos', component: Correos, meta: { requiresAuth: true } },
    { path: '/cursos-capacitaciones', name: 'cursoscapacitaciones', component: CursosCapacitaciones, meta: { requiresAuth: true } },
    { path: '/inscripciones', name: 'formularioPreInscripcion', component: FormularioPreInscripcion },
  { path: '/inscripciones-2', name: 'formularioPreInscripcion2', component: FormularioPreInscripcion2 },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/pagos' },
  ],
})

// Auth guard: controlado por variable de entorno para modo pruebas visuales
// Usa VITE_DISABLE_AUTH_GUARD=true en .env.development para desactivar el guard en desarrollo
const DISABLE_AUTH_GUARD = String(import.meta.env.VITE_DISABLE_AUTH_GUARD || '').toLowerCase() === 'true'

router.beforeEach((to, from, next) => {
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
  
  // Verificar rol de administrador si es requerido
  if (to.meta?.requiresAdmin) {
    const currentUserRaw = localStorage.getItem('currentUser')
    if (currentUserRaw) {
      try {
        const currentUser = JSON.parse(currentUserRaw)
        const userRole = currentUser.role || currentUser.rol || ''
        
        if (userRole !== 'Administradora Regional') {
          // Si no es administrador, redirigir al dashboard
          next({ name: 'dashboard' })
          return
        }
      } catch (e) {
        // Error al parsear, redirigir a login
        next({ name: 'login', query: { redirect: to.fullPath } })
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
