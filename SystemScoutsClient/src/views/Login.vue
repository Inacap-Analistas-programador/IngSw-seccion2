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
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const usernameError = ref('')
const passwordError = ref('')
const loading = ref(false)
const showPassword = ref(false)
const alerta = ref({ mensaje: '', tipo: '' })
let toastTimer = null
const usernameInputRef = ref(null)
const shake = ref(false)

function showToast(message) {
  // Evita duplicados y reinicia el timer si llega el mismo mensaje
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
  // nextTick para reiniciar la animación si ya estaba activa
  nextTick(() => {
    shake.value = true
    setTimeout(() => (shake.value = false), 500)
  })
}

// Limpiar errores de campo al escribir
watch(username, () => { if (usernameError.value) usernameError.value = '' })
watch(password, () => { if (passwordError.value) passwordError.value = '' })

const router = useRouter()
const route = useRoute()

// el ojo ahora vive dentro del input, no necesitamos sincronizar alturas

const handleLogin = async () => {
  try {
    errorMessage.value = ''
    usernameError.value = ''
    passwordError.value = ''
    loading.value = true

    // Validación básica antes de llamar al backend
    if (!username.value || !password.value) {
      if (!username.value) usernameError.value = 'Ingresa tu usuario'
      if (!password.value) passwordError.value = 'Ingresa tu contraseña'
      const msg = !username.value && !password.value
        ? 'Debes ingresar usuario y contraseña'
        : 'Completa los campos requeridos'
      showToast(msg)
        focusUsername()
      return
    }
    const data = await authService.login(username.value, password.value)
    if (data && data.token) {
      const redirectTo = route.query.redirect || '/dashboard'
      router.push(redirectTo)
    } else {
      const msg = 'Usuario y contraseña están equivocados'
      errorMessage.value = msg
      usernameError.value = ''
      passwordError.value = msg
      showToast(msg)
      password.value = ''
      focusUsername()
      triggerShake()
    }
  } catch (err) {
    console.error(err)
    if (err?.message?.includes('Failed to fetch')) {
      const msg = 'No se pudo conectar con el servidor. Inténtalo nuevamente.'
      errorMessage.value = msg
      usernameError.value = ''
      passwordError.value = msg
      showToast(msg)
        focusUsername(false)
    } else if (String(err?.message || '').startsWith('401')) {
      const msg = 'Usuario y contraseña están equivocados'
      errorMessage.value = msg
      usernameError.value = ''
      passwordError.value = msg
      showToast(msg)
      password.value = ''
        focusUsername()
        triggerShake()
    } else {
      const msg = 'Ocurrió un error al iniciar sesión'
      errorMessage.value = msg
      usernameError.value = ''
      passwordError.value = msg
      showToast(msg)
        focusUsername(false)
    }
  } finally {
    loading.value = false
  }
};

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

.login-footer { margin-top: 12px; text-align: center; color: #667085; }
</style>