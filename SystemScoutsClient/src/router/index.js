import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load views to keep bundle small
const Dashboard = () => import('@/views/Dashboard.vue')
const Mantenedores = () => import('@/views/mantenedores.vue')
const Gestionpersonas = () => import('@/views/Gestionpersonas.vue')
const PagosView = () => import('@/views/PagosView.vue')
const Correos = () => import('@/views/Correos.vue')
const ManualAcreditation = () => import('@/views/ManualAcreditation.vue')
const VerificadorQR = () => import('@/views/VerificadorQR.vue')
const Usuarios = () => import('@/views/Gestionpersonas.vue')
const CursosCapacitaciones = () => import('@/views/CRUDcursos.vue')
const Login = () => import('@/views/Login.vue')
const FormularioPreInscripcion = () => import('@/views/Formulario.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: Login },
    { path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/usuarios', name: 'usuarios', component: Usuarios, meta: { requiresAuth: true } },
  // Mantenedores admite pestaña vía parámetro opcional
  { path: '/mantenedores/:tab?', name: 'mantenedores', component: Mantenedores, props: true, meta: { requiresAuth: true } },
    { path: '/gestionpersonas', name: 'gestionpersonas', component: Gestionpersonas, meta: { requiresAuth: true } },
    { path: '/pagos', name: 'pagos', component: PagosView, meta: { requiresAuth: true } },
  { path: '/manual-acreditacion', name: 'manualacreditacion', component: ManualAcreditation, meta: { requiresAuth: true } },
  { path: '/verificador-qr', name: 'verificadorqr', component: VerificadorQR },
    { path: '/correos', name: 'correos', component: Correos, meta: { requiresAuth: true } },
    { path: '/cursos-capacitaciones', name: 'cursoscapacitaciones', component: CursosCapacitaciones, meta: { requiresAuth: true } },
    { path: '/inscripciones', name: 'formularioPreInscripcion', component: FormularioPreInscripcion },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/pagos' },
  ],
})

// Auth guard: controlado por variable de entorno para modo pruebas visuales
// Usa VITE_DISABLE_AUTH_GUARD=true en .env.development para desactivar el guard en desarrollo
const DISABLE_AUTH_GUARD = String(import.meta.env.VITE_DISABLE_AUTH_GUARD || '').toLowerCase() === 'true'
router.beforeEach((to, from, next) => {
  if (DISABLE_AUTH_GUARD) return next()
  const token = localStorage.getItem('token')
  if (to.meta?.requiresAuth && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && token) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
