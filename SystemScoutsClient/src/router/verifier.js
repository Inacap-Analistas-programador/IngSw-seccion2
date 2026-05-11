import { createRouter, createWebHistory } from 'vue-router'
// Direct import for small bundle
import VerificadorQR from '@/views/VerificadorQR.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/verificador-qr'
        },
        {
            path: '/verificador-qr',
            name: 'verificadorqr',
            component: VerificadorQR,
            meta: { requiresAuth: false } // Force public access
        },
        // Catch-all redirects back to verifier
        { path: '/:catchAll(.*)', redirect: '/verificador-qr' },
    ],
})

export default router
