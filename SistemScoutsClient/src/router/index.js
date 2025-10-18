import { createRouter, createWebHistory } from 'vue-router'

<<<<<<< HEAD
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
    },
=======
// Lazy-load views to keep bundle small
const Dashboard = () => import('@/views/Dashboard.vue')
const Mantenedores = () => import('@/views/Mantenedores.vue')
const Gestionpersonas = () => import('@/views/Gestionpersonas.vue')
const PagosView = () => import('@/views/PagosView.vue')
const Correos = () => import('@/views/Correos.vue')
const ManualAcreditation = () => import('@/views/ManualAcreditation.vue')
const VerificadorQR = () => import('@/views/VerificadorQR.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'dashboard', component: Dashboard },
    { path: '/mantenedores', name: 'mantenedores', component: Mantenedores },
    { path: '/gestionpersonas', name: 'gestionpersonas', component: Gestionpersonas },
    { path: '/pagos', name: 'pagosview', component: PagosView },
  { path: '/manual-acreditacion', name: 'manualacreditacion', component: ManualAcreditation },
  { path: '/verificador-qr', name: 'verificadorqr', component: VerificadorQR },
    { path: '/correos', name: 'correos', component: Correos },
    // fallback
    { path: '/:catchAll(.*)', redirect: '/' },
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
  ],
})

export default router
