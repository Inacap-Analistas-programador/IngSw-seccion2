<template>
  <section class="glass-section verificador-rut">

    <!-- Encabezado integrado al lenguaje del sistema -->
    <div class="section-header-modern">
      <AppIcons name="shield-check" :size="24" />
      <h2>Verificación de identidad</h2>
    </div>

    <p class="ver-intro">
      Ingresa tu RUT para verificar si tienes un registro previo. Te enviaremos un código al
      correo registrado para confirmar tu identidad y cargar tus datos automáticamente.
    </p>

    <!-- ── PASO 1: Ingresar RUT ─────────────────────────────── -->
    <transition name="desplegar" mode="out-in">
      <div v-if="paso === 1" key="p1">
        <div class="campo">
          <label for="rut-verificador">RUT</label>
          <div class="rut-wrap">
            <AppIcons name="user" :size="16" class="rut-icon-svg" />
            <input
              id="rut-verificador"
              v-model="rutIngresado"
              type="text"
              placeholder="Ej: 12.345.678-9"
              maxlength="12"
              autocomplete="off"
              @input="formatearRut"
              @keyup.enter="solicitarCodigo"
              class="rut-native-input"
              :class="{ 'has-error': errorMsg }"
            />
          </div>
          <span v-if="errorMsg" class="campo-error">
            <AppIcons name="alert-circle" :size="13" /> {{ errorMsg }}
          </span>
        </div>

        <div class="ver-actions">
          <BaseButton type="button" variant="primary" size="lg" :disabled="loading || !rutIngresado.trim()" @click="solicitarCodigo" class="full-width-btn">
            <span v-if="loading" class="btn-spinner"></span>
            <AppIcons v-else name="send" :size="16" />
            {{ loading ? 'Verificando...' : 'Enviar código de verificación' }}
          </BaseButton>
        </div>

        <div class="ver-info-row">
          <AppIcons name="info" :size="14" />
          <span>Si no tienes registro previo, un administrador debe crearlo primero.</span>
        </div>
      </div>

      <!-- ── PASO 2: Ingresar código ──────────────────────────── -->
      <div v-else-if="paso === 2" key="p2">
        <div class="email-badge">
          <AppIcons name="mail" :size="16" />
          <span>Código enviado a <strong>{{ emailMasked }}</strong></span>
        </div>

        <div class="campo">
          <label>Código de 6 dígitos</label>
          <div class="codigo-inputs">
            <input
              v-for="(_, i) in codigoDigitos"
              :key="i"
              :ref="el => digitRefs[i] = el"
              v-model="codigoDigitos[i]"
              type="text"
              inputmode="numeric"
              maxlength="1"
              class="digit-box"
              :class="{ 'filled': codigoDigitos[i] }"
              @input="onDigitInput(i, $event)"
              @keydown="onDigitKeydown(i, $event)"
              @paste.prevent="onPaste($event)"
            />
          </div>
          <span v-if="errorMsg" class="campo-error">
            <AppIcons name="alert-circle" :size="13" /> {{ errorMsg }}
          </span>
        </div>

        <div class="timer-row" :class="{ expired: timerSecs === 0 }">
          <AppIcons :name="timerSecs > 0 ? 'clock' : 'alert-triangle'" :size="14" />
          <span v-if="timerSecs > 0">Código válido por <strong>{{ formatTimer(timerSecs) }}</strong></span>
          <span v-else>El código ha expirado —
            <button type="button" class="link-btn" @click="solicitarCodigo" :disabled="loading">reenviar nuevo código</button>
          </span>
        </div>

        <div class="ver-actions">
          <BaseButton
            type="button"
            variant="primary"
            size="lg"
            :disabled="loading || codigoCompleto.length < 6 || timerSecs === 0"
            @click="confirmarCodigo"
            class="full-width-btn"
          >
            <span v-if="loading" class="btn-spinner"></span>
            <AppIcons v-else name="check-circle" :size="16" />
            {{ loading ? 'Verificando código...' : 'Confirmar código' }}
          </BaseButton>

          <button type="button" class="link-btn back-btn" @click="volverPaso1" :disabled="loading">
            <AppIcons name="chevron-left" :size="14" /> Cambiar RUT
          </button>
        </div>
      </div>

      <!-- ── PASO 3: Verificado OK ────────────────────────────── -->
      <div v-else-if="paso === 3" key="p3" class="success-state">
        <div class="success-check">
          <AppIcons name="check" :size="32" />
        </div>
        <div class="success-text">
          <h3>¡Identidad verificada!</h3>
          <p>Tus datos han sido cargados. Puedes continuar completando tu inscripción.</p>
        </div>
        <div class="persona-card">
          <div class="persona-avatar">
            <AppIcons name="user" :size="22" />
          </div>
          <div class="persona-info">
            <span class="persona-name">{{ personaData?.per_nombres }} {{ personaData?.per_apelpta }}</span>
            <span class="persona-rut">RUT: {{ rutIngresado }}</span>
          </div>
        </div>
        <BaseButton type="button" variant="primary" size="lg" @click="continuar" class="full-width-btn">
          Continuar con la inscripción
          <AppIcons name="chevron-right" :size="16" />
        </BaseButton>
      </div>
    </transition>

  </section>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import BaseButton from '@/components/BaseButton.vue'

const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8000').replace(/\/api\/?$/, '')

const emit = defineEmits(['verified', 'cancel'])

const paso = ref(1)
const rutIngresado = ref('')
const emailMasked = ref('')
const codigoDigitos = ref(['', '', '', '', '', ''])
const digitRefs = ref([])
const loading = ref(false)
const errorMsg = ref('')
const personaData = ref(null)
const timerSecs = ref(600)
let timerInterval = null

const codigoCompleto = computed(() => codigoDigitos.value.join(''))

// ─── Formateo RUT ─────────────────────────────────────────────────────────────
const formatearRut = () => {
  let val = rutIngresado.value.replace(/[^0-9kK]/g, '').toUpperCase()
  if (val.length > 9) val = val.slice(0, 9)
  if (val.length > 1) {
    const cuerpo = val.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    rutIngresado.value = `${cuerpo}-${val.slice(-1)}`
  } else {
    rutIngresado.value = val
  }
}

// ─── Paso 1 ───────────────────────────────────────────────────────────────────
const solicitarCodigo = async () => {
  errorMsg.value = ''
  if (!rutIngresado.value.trim()) return
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/verificar-rut/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rut: rutIngresado.value })
    })
    const data = await res.json()
    if (!res.ok) { errorMsg.value = data.error || 'Error al verificar el RUT.'; return }
    emailMasked.value = data.email_masked
    codigoDigitos.value = ['', '', '', '', '', '']
    paso.value = 2
    iniciarTimer()
    setTimeout(() => digitRefs.value[0]?.focus(), 120)
  } catch {
    errorMsg.value = 'Error de conexión. Intenta nuevamente.'
  } finally {
    loading.value = false
  }
}

// ─── Timer ────────────────────────────────────────────────────────────────────
const iniciarTimer = () => {
  clearInterval(timerInterval)
  timerSecs.value = 600
  timerInterval = setInterval(() => {
    if (timerSecs.value > 0) timerSecs.value--
    else clearInterval(timerInterval)
  }, 1000)
}

const formatTimer = (s) => {
  const m = Math.floor(s / 60).toString().padStart(2, '0')
  const sec = (s % 60).toString().padStart(2, '0')
  return `${m}:${sec}`
}

// ─── Inputs dígitos ───────────────────────────────────────────────────────────
const onDigitInput = (i, e) => {
  const val = e.target.value.replace(/\D/g, '')
  codigoDigitos.value[i] = val.slice(-1)
  if (val && i < 5) digitRefs.value[i + 1]?.focus()
}
const onDigitKeydown = (i, e) => {
  if (e.key === 'Backspace' && !codigoDigitos.value[i] && i > 0) digitRefs.value[i - 1]?.focus()
}
const onPaste = (e) => {
  const pasted = (e.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, 6)
  pasted.split('').forEach((ch, i) => { if (i < 6) codigoDigitos.value[i] = ch })
  digitRefs.value[Math.min(pasted.length, 5)]?.focus()
}

// ─── Paso 2 ───────────────────────────────────────────────────────────────────
const confirmarCodigo = async () => {
  errorMsg.value = ''
  if (codigoCompleto.value.length < 6) return
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/verificar-rut/confirmar/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rut: rutIngresado.value, codigo: codigoCompleto.value })
    })
    const data = await res.json()
    if (!res.ok) {
      errorMsg.value = data.error || 'Código incorrecto.'
      codigoDigitos.value = ['', '', '', '', '', '']
      setTimeout(() => digitRefs.value[0]?.focus(), 50)
      return
    }
    clearInterval(timerInterval)
    personaData.value = data.persona
    paso.value = 3
  } catch {
    errorMsg.value = 'Error de conexión. Intenta nuevamente.'
  } finally {
    loading.value = false
  }
}

const continuar = () => emit('verified', personaData.value)
const volverPaso1 = () => {
  clearInterval(timerInterval)
  errorMsg.value = ''
  codigoDigitos.value = ['', '', '', '', '', '']
  paso.value = 1
}

onBeforeUnmount(() => clearInterval(timerInterval))
</script>

<style scoped>
/* ── Integrado al sistema de diseño del formulario ── */
.verificador-rut {
  max-width: 520px;
}

.ver-intro {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 24px;
}

/* ── Campo RUT nativo ── */
.rut-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.rut-icon-svg {
  position: absolute;
  left: 12px;
  color: #94a3b8;
  pointer-events: none;
}

.rut-native-input {
  width: 100%;
  padding: 10px 14px 10px 38px;
  font-size: 1.15rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  box-sizing: border-box;
}

.rut-native-input.has-error {
  border-color: #ef4444 !important;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12) !important;
}

/* ── Error ── */
.campo-error {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #dc2626;
  font-size: 0.82rem;
  font-weight: 600;
  margin-top: 2px;
}

/* ── Acciones ── */
.ver-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.full-width-btn {
  width: 100%;
  justify-content: center;
}

/* ── Info row ── */
.ver-info-row {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  margin-top: 16px;
  padding: 11px 14px;
  background: rgba(30, 64, 175, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(30, 64, 175, 0.15);
  color: #1e40af;
  font-size: 0.82rem;
  line-height: 1.4;
}

/* ── Email badge ── */
.email-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(22, 163, 74, 0.07);
  border: 1px solid rgba(22, 163, 74, 0.25);
  border-radius: 10px;
  color: #15803d;
  font-size: 0.87rem;
  font-weight: 500;
  margin-bottom: 20px;
}

/* ── Código dígitos ── */
.codigo-inputs {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
}

.digit-box {
  width: 48px !important;
  height: 56px !important;
  padding: 0 !important;
  text-align: center;
  font-size: 1.4rem;
  font-weight: 800;
  border-radius: 10px;
  letter-spacing: 0;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

.digit-box:focus {
  border-color: #1e40af;
  box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.12);
  background: white;
}

.digit-box.filled {
  background: rgba(30, 64, 175, 0.06);
  border-color: rgba(30, 64, 175, 0.4);
  color: #1e40af;
}

/* ── Timer ── */
.timer-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 14px 0 0;
  color: #64748b;
  font-size: 0.84rem;
}

.timer-row.expired {
  color: #dc2626;
}

/* ── Links ── */
.link-btn {
  background: none;
  border: none;
  color: #1e40af;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.link-btn:hover { color: #1e3a8a; }
.link-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.back-btn {
  align-self: center;
  text-align: center;
  margin-top: 4px;
}

/* ── Spinner botón ── */
.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Paso 3: éxito ── */
.success-state {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}

.success-check {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(22, 163, 74, 0.1);
  border: 2px solid rgba(22, 163, 74, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #16a34a;
  animation: pop-in 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes pop-in {
  from { transform: scale(0); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

.success-text h3 {
  margin: 0 0 4px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}

.success-text p {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
}

.persona-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  width: 100%;
  box-sizing: border-box;
}

.persona-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(30, 64, 175, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e40af;
  flex-shrink: 0;
}

.persona-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.persona-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
}

.persona-rut {
  font-size: 0.82rem;
  color: #64748b;
}

/* ── Responsive ── */
@media (max-width: 520px) {
  .codigo-inputs { gap: 5px; }
  .digit-box { width: 42px !important; height: 50px !important; font-size: 1.2rem; }
}
</style>
