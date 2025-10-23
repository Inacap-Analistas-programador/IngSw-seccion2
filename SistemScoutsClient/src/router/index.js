import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load views to keep bundle small
const Dashboard = () => import('@/views/Dashboard.vue')
const Mantenedores = () => import('@/views/Mantenedores.vue')
const Gestionpersonas = () => import('@/views/Gestionpersonas.vue')
const PagosView = () => import('@/views/PagosView.vue')
const Correos = () => import('@/views/Correos.vue')
const ManualAcreditation = () => import('@/views/ManualAcreditation.vue')
const VerificadorQR = () => import('@/views/VerificadorQR.vue')
const Usuarios = () => import('@/views/Gestionpersonas.vue')
const CursosCapacitaciones = () => import('@/views/CRUDcursos.vue')
const Login = () => import('@/views/Login.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: Login },
    { path: '/dashboard', name: 'dashboard', component: Dashboard },
    { path: '/usuarios', name: 'usuarios', component: Usuarios },
    { path: '/mantenedores', name: 'mantenedores', component: Mantenedores },
    { path: '/gestionpersonas', name: 'gestionpersonas', component: Gestionpersonas },
    { path: '/pagos', name: 'pagosview', component: PagosView },
  { path: '/manual-acreditacion', name: 'manualacreditacion', component: ManualAcreditation },
  { path: '/verificador-qr', name: 'verificadorqr', component: VerificadorQR },
    { path: '/correos', name: 'correos', component: Correos },
    { path: '/cursos-capacitaciones', name: 'cursoscapacitaciones', component: CursosCapacitaciones },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})

export default router
