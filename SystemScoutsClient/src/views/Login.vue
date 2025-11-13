<template>
  <div class="login-page">
    <div class="login-card" :class="{ shake }">
      <header class="login-header">
        <div class="login-title">
          <AppIcons name="users" :size="22" />
          <h1>Ingreso al Sistema</h1>
        </div>
        <p class="login-subtitle">Autentícate con tu usuario y contraseña</p>
      </header>

      <form class="login-form" @submit.prevent="handleLogin">
        <InputBase
          ref="usernameInputRef"
          v-model="username"
          label="Usuario"
          placeholder="Tu usuario"
          required
          :external-error="usernameError"
        />
        <div class="password-row">
          <InputBase
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            label="Contraseña"
            placeholder="Tu contraseña"
            required
            :external-error="passwordError"
          >
            <template #append>
              <button
                type="button"
                class="append-btn"
                :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                :title="showPassword ? 'Ocultar' : 'Mostrar'"
                @click="showPassword = !showPassword"
              >
                <AppIcons :name="showPassword ? 'eye-off' : 'eye'" :size="18" />
              </button>
            </template>
          </InputBase>
        </div>

        <div class="actions-row">
          <BaseButton :disabled="loading" type="submit" variant="primary" size="lg" block>
            <template v-if="!loading">
              <AppIcons name="check" :size="18" /> Ingresar
            </template>
            <template v-else>
              Procesando...
            </template>
          </BaseButton>
          <!-- Botón de auto-login solo para desarrollo -->
          <button
            v-if="showAutoLogin"
            type="button"
            class="dev-auto-btn"
            @click="autoLogin"
            :disabled="loading"
            title="Autenticar con credenciales de desarrollo"
          >
            Autologin (dev)
          </button>
        </div>
      </form>

      <footer class="login-footer">
        <small>© {{ new Date().getFullYear() }} Guias y Scouts Biobío</small>
      </footer>
      
      <NotificationToast 
        v-if="alerta.mensaje"
        :message="alerta.mensaje" 
        @close="alerta.mensaje = ''"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '@/services/authService.js'
import InputBase from '@/components/InputBase.vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import NotificationToast from '@/components/NotificationToast.vue'

const username = ref('')
const password = ref('')
const usernameError = ref('')
const passwordError = ref('')
const loading = ref(false)
const showPassword = ref(false)
const alerta = ref({ mensaje: '', tipo: '' })
let toastTimer = null
const usernameInputRef = ref(null)
const shake = ref(false)

const router = useRouter()
const route = useRoute()

// Configuración de autologin
const isDev = !!import.meta.env?.DEV
const enableAutoLogin = String(import.meta.env?.VITE_ENABLE_AUTOLOGIN ?? 'true').toLowerCase() === 'true'
const showAutoLogin = isDev && enableAutoLogin
const AUTO_USERNAME = import.meta.env?.VITE_AUTO_USER ?? 'admin'
const AUTO_PASSWORD = import.meta.env?.VITE_AUTO_PASS ?? 'admin'

function showToast(message) {
  if (alerta.value.mensaje !== message) {
    alerta.value = { mensaje: message, tipo: 'error' }
  }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (alerta.value = { mensaje: '', tipo: '' }), 2500)
}

async function focusUsername(selectAll = true) {
  await nextTick()
  const el = usernameInputRef.value?.$el?.querySelector?.('.base-field')
  if (el) {
    el.focus()
    if (selectAll) {
      try { el.select() } catch {}
    }
  }
}

function triggerShake() {
  shake.value = false
  nextTick(() => {
    shake.value = true
    setTimeout(() => (shake.value = false), 500)
  })
}

watch(username, () => { if (usernameError.value) usernameError.value = '' })
watch(password, () => { if (passwordError.value) passwordError.value = '' })

// ===== LOGIN =====
const handleLogin = async () => {
  try {
    loading.value = true
    if (!username.value || !password.value) {
      showToast('Debes completar usuario y contraseña')
      return
    }

    const data = await authService.login(username.value, password.value)

    if (data.access) {
      localStorage.setItem('token', data.access)
      router.push('/dashboard')
      window.location.reload()
    } else {
      showToast('Usuario o contraseña incorrectos')
      triggerShake()
    }
  } catch (err) {
    console.error(err)
    showToast(err.message || 'Error al iniciar sesión')
    triggerShake()
  } finally {
    loading.value = false
  }
}

// Autologin de desarrollo: rellena y reutiliza el mismo flujo
async function autoLogin() {
  if (loading.value) return
  username.value = AUTO_USERNAME
  password.value = AUTO_PASSWORD
  await handleLogin()
}

// ===== FETCH USUARIOS PROTEGIDOS =====
const usuarios = ref([])

async function cargarUsuarios() {
  try {
    const token = localStorage.getItem('accessToken')
    if (!token) return

    const response = await fetch('http://127.0.0.1:8000/api/usuarios/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw new Error('Error al obtener usuarios')

    usuarios.value = await response.json()
    console.log(usuarios.value)
  } catch (err) {
    console.error(err)
    showToast(err.message || 'Error al cargar usuarios')
  }
}

</script>

<style scoped>
.login-page {
  /* alto dinámico con fallback para distintos navegadores */
  height: 100svh; /* small viewport height (mejor en iOS/Android/Windows) */
  min-height: 100dvh; /* fallback */
  display: grid;
  place-items: center; /* centra perfecto */
  background: var(--color-background);
  padding: 0 24px; /* solo horizontal para evitar overflow vertical */
  overflow: hidden; /* evita barra por redondeos/subpíxeles */
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  /* sombra un poco más marcada y suave */
  box-shadow:
    0 12px 24px rgba(16, 24, 40, 0.12),
    0 2px 6px rgba(16, 24, 40, 0.06);
  padding: 20px 18px 16px 18px;
}

.shake {
  animation: shake 0.4s linear;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

.login-header { margin-bottom: 10px; }
.login-title { display:flex; align-items:center; gap:8px; color: var(--color-primary) }
.login-title h1 { font-size: 20px; font-weight: 800; margin: 0 }
.login-subtitle { margin: 4px 0 0 0; color: #475569; font-size: 13px }

.login-form { display:flex; flex-direction: column; gap: 8px; margin-top: 6px }
/* error inline arriba del input */

/* usar grid para alinear el botón con el input sin saltos */
.password-row {
  display: block;
}
.append-btn { border: none; background: transparent; padding: 6px; border-radius: 6px; color: #6b7280; cursor: pointer; }
.append-btn:hover { background: rgba(0,0,0,0.05); color: var(--color-text); }
.actions-row { margin-top: 8px; }

/* Estilo del botón de autologin (solo dev) */
.dev-auto-btn {
  margin-top: 8px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px dashed rgba(99,102,241,0.6);
  background: rgba(99,102,241,0.06);
  color: var(--color-primary);
  font-weight: 600;
  cursor: pointer;
}
.dev-auto-btn:hover { background: rgba(99,102,241,0.12); }
.dev-auto-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.login-footer { margin-top: 12px; text-align: center; color: #667085; }
</style>