import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// Disable Vue 3 Strict Mode in development to prevent double-execution of setup
if (import.meta.env.MODE === 'development') {
  // This is automatically enabled, but we can document it for reference
  // In Vite + Vue 3, Strict Mode can't be easily disabled; instead we use guards in components
}

app.use(router)

app.mount('#app')
