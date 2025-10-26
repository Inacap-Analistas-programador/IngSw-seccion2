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
    { path: '/dashboard', name: 'dashboard', component: Dashboard },
    { path: '/usuarios', name: 'usuarios', component: Usuarios },
  // Mantenedores admite pestaña vía parámetro opcional
  { path: '/mantenedores/:tab?', name: 'mantenedores', component: Mantenedores, props: true },
    { path: '/gestionpersonas', name: 'gestionpersonas', component: Gestionpersonas },
    { path: '/pagos', name: 'pagos', component: PagosView },
  { path: '/manual-acreditacion', name: 'manualacreditacion', component: ManualAcreditation },
  { path: '/verificador-qr', name: 'verificadorqr', component: VerificadorQR },
    { path: '/correos', name: 'correos', component: Correos },
    { path: '/cursos-capacitaciones', name: 'cursoscapacitaciones', component: CursosCapacitaciones },
    { path: '/inscripciones', name: 'formularioPreInscripcion', component: FormularioPreInscripcion },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/pagos' },
  ],
})

export default router
