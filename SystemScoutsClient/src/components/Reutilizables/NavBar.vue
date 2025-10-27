<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import logoSrc from '@/assets/Logo_Boyscout_Chile.png'
import authService from '@/services/authService.js'
import logoutDefault from '@/assets/logout_default.svg'
import avatarDefault from '@/assets/avatar_default.svg'

// User state (avatar + name)
const user = ref({ name: 'Usuario', role: 'Invitado', avatarUrl: null })
const router = useRouter()
const route = useRoute()
const logoutSrc = ref('/logout.png')
const avatarSrc = ref(avatarDefault)

// Estado reactivo de autenticación
const isAuthenticated = ref(!!localStorage.getItem('token'))

// Función para actualizar el estado de autenticación
function updateAuthState() {
  const hasToken = !!localStorage.getItem('token')
  isAuthenticated.value = hasToken
  
  if (hasToken) {
    // Cargar info del usuario
    authService.getCurrentUser().then(u => {
      if (u) {
        user.value = { name: u.name || 'Usuario', role: u.role || 'Invitado', avatarUrl: u.avatarUrl || null }
        avatarSrc.value = u.avatarUrl || avatarDefault
      }
    })
  }
}

// Escuchar cambios de ruta para detectar login/logout
watch(() => route.path, () => {
  updateAuthState()
})

onMounted(() => {
  updateAuthState()
  
  // Escuchar eventos de storage (cambios en otras pestañas)
  window.addEventListener('storage', updateAuthState)
})

onUnmounted(() => {
  window.removeEventListener('storage', updateAuthState)
})

function logout() {
  authService.logout()
  router.push('/')
}

function onLogoutImgError() {
  // Fallback to bundled SVG if /public/logout.png is missing
  logoutSrc.value = logoutDefault
}

function onAvatarError() {
  avatarSrc.value = avatarDefault
}
</script>

<template>
  <nav class="navbar">
    <!-- Logo y título -->
    <div class="navbar-left">
      <router-link class="brand" :to="{ name: 'dashboard' }" aria-label="Ir al Dashboard">
        <img :src="logoSrc" alt="Logo Scouts" class="logo" />
        <span class="title">S.S.B</span>
      </router-link>
  <router-link class="dash-link" :to="{ name: 'dashboard' }">Panel de Control</router-link>
    </div>

    <!-- Usuario (avatar + nombre/rol + salir) - Solo visible si autenticado -->
    <Transition name="user-fade">
      <div v-if="isAuthenticated" class="navbar-user">
        <img :src="avatarSrc" @error="onAvatarError" alt="Usuario" class="avatar" />
        <div class="user-meta">
          <div class="user-name">{{ user.name }}</div>
          <div class="user-role">{{ user.role }}</div>
        </div>
        <button class="logout-btn" @click="logout" title="Cerrar sesión" aria-label="Cerrar sesión">
          <img :src="logoutSrc" @error="onLogoutImgError" alt="Cerrar sesión" class="logout-img" />
        </button>
      </div>
    </Transition>

    <!-- Botón de Login cuando no está autenticado -->
    <Transition name="user-fade">
      <div v-if="!isAuthenticated" class="navbar-actions">
        <button class="login-btn" @click="router.push('/')" title="Iniciar sesión" aria-label="Iniciar sesión">
          Iniciar Sesión
        </button>
      </div>
    </Transition>
  </nav>
</template>

<style scoped>
/* ====== Barra de navegación ====== */
.navbar {
  background: var(--color-primary); /* Azul institucional estandarizado */
  color: white;
  padding: 8px 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  font-family: "Segoe UI", Arial, sans-serif;
}

/* ====== Sección izquierda ====== */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 18px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}

.logo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid var(--color-warning); /* Amarillo del tema */
  background: white;
  object-fit: cover;
  box-shadow: 0 3px 6px rgba(0,0,0,0.18);
}

.title {
  font-size: 1.15rem;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 0.6px;
}

.dash-link {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 999px;
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  transition: background .2s, border-color .2s, transform .1s;
}
.dash-link:hover { background: rgba(255,255,255,0.2); border-color: rgba(255,255,255,0.4); }
.dash-link:active { transform: translateY(1px); }

/* ====== Usuario derecha (avatar + nombre/rol + salir) ====== */
.navbar-user {
  display: flex;
  align-items: center;
  gap: 12px;
}
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  background: var(--color-surface);
  border: 2px solid var(--color-warning);
  box-shadow: 0 3px 6px rgba(0,0,0,0.18);
}
.user-meta {
  display: flex;
  flex-direction: column;
  margin-right: 6px;
}
.user-name {
  font-weight: 700;
  line-height: 1.1;
}
.user-role {
  font-size: 0.85rem;
  color: #a0bcf0;
  line-height: 1.1;
}
.logout-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.6);
  background: transparent; /* sin tinte azul */
  cursor: pointer;
  transition: background .2s, transform .1s;
}
.logout-btn:hover { background: rgba(255,255,255,0.2); }
.logout-btn:active { transform: scale(0.96); }

.logout-img {
  width: 20px;
  height: 20px;
  object-fit: contain;
  display: block;
  /* Fuerza el ícono a blanco aunque la imagen original sea azul/oscura */
  filter: brightness(0) invert(1);
}

/* ====== Botón de Login (cuando no está autenticado) ====== */
.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.login-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
  border-radius: 8px;
  border: 2px solid rgba(255,255,255,0.8);
  background: rgba(255,255,255,0.15);
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.login-btn:hover {
  background: rgba(255,255,255,0.25);
  border-color: rgba(255,255,255,1);
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.login-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}

/* ====== Responsive ====== */
@media (max-width: 768px) {
  .user-meta { display: none; }
}

/* ====== Animación de entrada/salida del usuario ====== */
.user-fade-enter-active,
.user-fade-leave-active {
  transition: all 0.3s ease;
}

.user-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.user-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
