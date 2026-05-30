import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const isProd = process.env.NODE_ENV === 'production'

// https://vite.dev/config/
export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    // Devtools solo en desarrollo
    process.env.VITEST || isProd ? undefined : vueDevTools(),
  ].filter(Boolean),

  server: {
    hmr: { overlay: true },
  },

  build: {
    outDir: 'dist',
    // Advertir si un chunk supera 600KB
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks: {
          // Dependencias externas pesadas separadas del bundle principal
          'vendor-vue': ['vue', 'vue-router', 'pinia'],
          'vendor-leaflet': ['leaflet'],
        }
      }
    }
  },

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },

  esbuild: {
    // Eliminar console.* y debugger en producción para no exponer info interna
    drop: isProd ? ['console', 'debugger'] : [],
  },
})
