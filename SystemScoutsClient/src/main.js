import './assets/main.css'
import './assets/formulario-shared.css'
import 'leaflet/dist/leaflet.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import PageHeader from '@/components/common/PageHeader.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Componentes globales — disponibles en todas las vistas sin importar localmente
app.component('PageHeader', PageHeader)

app.mount('#app')
