<template>
  <div class="sidebar-wrapper">
    <div v-if="openMobile" class="sidebar-backdrop" @click="closeMobile"></div>
    <aside id="app-sidebar" :class="['sidebar', { collapsed, 'mobile-open': openMobile }]" @click.self="closeMobile">
      <button v-if="openMobile" class="mobile-close-btn" @click="closeMobile" aria-label="Cerrar menú">×</button>
      <nav class="sidebar-nav">
      
      <!-- Sin sesión iniciada: solo mostrar Formulario -->
      <div v-if="!isLoggedIn">
        <span class="nav-section-title">ACCESO PÚBLICO</span>
        <router-link to="/inscripciones" class="nav-item">Pre-inscripción</router-link>
      </div>
      
      <!-- Con sesión: mostrar menú completo (por defecto admin) -->
      <div v-else>
        <!-- Apartado desplegable: Usuarios y Perfiles -->
        <div class="nav-item nav-collapsible" @click="toggleUsuarios" :class="{ 'router-link-exact-active': showUsuarios }">
          <span class="nav-icon"><AppIcons name="users" :size="20" /></span>
          <span class="nav-collapsible-title">Usuarios y Perfiles</span>
          <span class="caret" :class="{ open: showUsuarios }">▾</span>
        </div>
        <Transition name="submenu-slide">
          <div v-show="showUsuarios" class="submenu">
            <router-link to="/usuarios" class="submenu-item"><span class="submenu-icon"><AppIcons name="user" :size="16" /></span>Usuarios</router-link>
            <router-link to="/roles" class="submenu-item"><span class="submenu-icon"><AppIcons name="lock" :size="16" /></span>Perfiles</router-link>
          </div>
        </Transition>

        <router-link to="/cursos-capacitaciones" class="nav-item">
          <span class="nav-icon"><AppIcons name="book" :size="20" /></span>
          <span class="nav-text">Cursos y Capacitaciones</span>
        </router-link>
        <router-link to="/inscripciones" class="nav-item">
          <span class="nav-icon"><AppIcons name="clipboard" :size="20" /></span>
          <span class="nav-text">Inscripciones</span>
        </router-link>
        <router-link to="/gestionpersonas" class="nav-item">
          <span class="nav-icon"><AppIcons name="users" :size="20" /></span>
          <span class="nav-text">Gestión de Personas</span>
        </router-link>
        <router-link to="/pagos" class="nav-item">
          <span class="nav-icon"><AppIcons name="credit-card" :size="20" /></span>
          <span class="nav-text">Pagos</span>
        </router-link>
        <router-link to="/correos" class="nav-item">
          <span class="nav-icon"><AppIcons name="mail" :size="20" /></span>
          <span class="nav-text">Envío de Correos</span>
        </router-link>
          <!-- Apartado desplegable: Mantenedores (sub-tabs) -->
          <div class="nav-item nav-collapsible" @click="toggleMantenedores" :class="{ 'router-link-exact-active': showMantenedores }">
            <span class="nav-icon"><AppIcons name="settings" :size="20" /></span>
            <span class="nav-collapsible-title">Mantenedores</span>
            <span class="caret" :class="{ open: showMantenedores }">▾</span>
          </div>
          <Transition name="submenu-slide">
            <div v-show="showMantenedores" class="submenu">
              <router-link
                v-for="t in mantenedoresTabs"
                :key="t.id"
                :to="{ path: '/mantenedores', query: { tab: t.id } }"
                class="submenu-item"
              >{{ t.label }}</router-link>
            </div>
          </Transition>
        <router-link to="/manual-acreditacion" class="nav-item">
          <span class="nav-icon"><AppIcons name="user-check" :size="20" /></span>
          <span class="nav-text">Acreditación Manual</span>
        </router-link>
        <router-link to="/verificador-qr" class="nav-item">
          <span class="nav-icon"><AppIcons name="qrcode" :size="20" /></span>
          <span class="nav-text">Verificador QR</span>
        </router-link>

        <!-- Apartado desplegable: Pantallas 2 CORREGIDO -->
        <div class="nav-item nav-collapsible" @click="togglePantallas2" :class="{ 'router-link-exact-active': showPantallas2 }">
          <span class="nav-icon"><AppIcons name="chart-bar" :size="20" /></span>
          <span class="nav-collapsible-title">Pantallas 2</span>
          <span class="caret" :class="{ open: showPantallas2 }">▾</span>
        </div>
        <Transition name="submenu-slide">
          <div v-show="showPantallas2" class="submenu">
            <router-link to="/dashboard-2" class="submenu-item">Dashboard 2</router-link>
            <router-link to="/inscripciones-2" class="submenu-item">Formulario 2</router-link>
          </div>
        </Transition>
      </div>
    </nav>
    
    <!-- Footer eliminado para evitar duplicidad con el botón de la navbar -->
  </aside>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import authService from '../services/authService';
import AppIcons from './icons/AppIcons.vue';

// Se mantiene el rol para condicionar el menú (por defecto admin para pruebas)
// Backend auth fue deshabilitado: mostrar el menú completo en UI-only mode
const usuario = ref({ nombre: 'Usuario Demo', rol: 'Administradora Regional' })

// isLoggedIn: derivado del token en localStorage para reflejar estado real de autenticación
const STORAGE_TOKEN_KEYS = ['token', 'accessToken']
function hasToken() {
  try {
    return STORAGE_TOKEN_KEYS.some((k) => !!localStorage.getItem(k))
  } catch (e) {
    return false
  }
}

const isLoggedIn = ref(hasToken())

// Escuchar cambios en localStorage (otras pestañas o logout/login) para mantener sincronizado
function onStorage(e) {
  // `storage` events include a `key`; custom events may call this handler
  if (!e) return
  if (e.key && STORAGE_TOKEN_KEYS.includes(e.key)) {
    // Recalcular por si cambia una u otra clave
    isLoggedIn.value = hasToken()
  }
}

// Handler para cambios de auth dentro de la MISMA pestaña (evento custom)
function handleAuthChanged() {
  isLoggedIn.value = hasToken()
}

// Desplegable de Mantenedores
const showUsuarios = ref(false)
const showMantenedores = ref(false)
const showPantallas2 = ref(false)

// Sidebar can be either controlled by parent via `collapsed` prop or operate in uncontrolled mode using localStorage
const props = defineProps({
  collapsed: { type: Boolean, default: undefined }
})
const emit = defineEmits(['update:collapsed'])

const internalCollapsed = ref(false)
const openMobile = ref(false)

// computed `collapsed` acts as a proxy: when prop is provided, it becomes controlled; otherwise it uses internal state.
const collapsed = computed({
  get() {
    return typeof props.collapsed !== 'undefined' ? props.collapsed : internalCollapsed.value
  },
  set(v) {
    if (typeof props.collapsed !== 'undefined') {
      emit('update:collapsed', v)
    } else {
      internalCollapsed.value = v
    }
    try { localStorage.setItem('sidebar-collapsed', v ? '1' : '0') } catch (e) { /* ignore */ }
  }
})

const mantenedoresTabs = [
  // Orden solicitado: región, provincia, comuna, zona, distrito, grupo
  { id: 'regiones', label: 'Regiones' },
  { id: 'provincias', label: 'Provincias' },
  { id: 'comunas', label: 'Comunas' },
  { id: 'zonas', label: 'Zonas' },
  { id: 'distritos', label: 'Distritos' },
  { id: 'grupos', label: 'Grupos Scout' },
  // Resto de mantenedores (manteniendo su orden relativo original)
  { id: 'ramas', label: 'Ramas' },
  { id: 'tipos-curso', label: 'Tipos Curso' },
  { id: 'cargos', label: 'Cargos' },
  { id: 'alimentacion', label: 'Alimentación' },
  { id: 'niveles', label: 'Niveles' },
  { id: 'estados-civiles', label: 'Estados Civiles' },
  { id: 'roles', label: 'Perfiles' },
  { id: 'conceptos-contables', label: 'Conceptos Contables' },
  { id: 'tipos-archivo', label: 'Tipos de Archivo' }
]

function toggleUsuarios() {
  showUsuarios.value = !showUsuarios.value
}

function toggleMantenedores() {
  showMantenedores.value = !showMantenedores.value
}

function togglePantallas2() {
  showPantallas2.value = !showPantallas2.value
}

function toggleCollapse() {
  const val = !collapsed.value
  collapsed.value = val
}

function loadCollapsedState() {
  const saved = localStorage.getItem('sidebar-collapsed')
  if (saved !== null && typeof props.collapsed === 'undefined') {
    internalCollapsed.value = saved === '1'
  }
}

onMounted(() => {
  loadCollapsedState()
  
  if (typeof window !== 'undefined') {
    const route = useRoute()
    // Abrir automáticamente si se navega a /mantenedores o /usuarios
    if (route && route.path) {
      showUsuarios.value = route.path.startsWith('/usuarios') || route.path.startsWith('/roles')
      showMantenedores.value = route.path.startsWith('/mantenedores')
      showPantallas2.value = route.path.startsWith('/dashboard-2') || route.path.startsWith('/inscripciones-2')
    }

    // Watch para actualizar estado al cambiar de ruta
    watch(() => route && route.path, async (p) => {
      if (p) {
        showUsuarios.value = p.startsWith('/usuarios') || p.startsWith('/roles')
        showMantenedores.value = p.startsWith('/mantenedores')
        showPantallas2.value = p.startsWith('/dashboard-2') || p.startsWith('/inscripciones-2')
      }
      // No actualizamos estado de autenticación ni consultamos authService en modo UI-only
    })
    
    // Registrar listener de storage para detectar login/logout en otras pestañas
    window.addEventListener('storage', onStorage)
    // También escuchar un evento custom para cambios de auth en la MISMA pestaña
    window.addEventListener('auth-changed', handleAuthChanged)
    // Registrar listener para abrir sidebar en móviles
    window.addEventListener('open-sidebar-mobile', openMobileHandler)
    // Cerrar sidebar con tecla Escape
    window.addEventListener('keydown', escHandler)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', onStorage)
  window.removeEventListener('auth-changed', handleAuthChanged)
  window.removeEventListener('open-sidebar-mobile', openMobileHandler)
  window.removeEventListener('keydown', escHandler)
})

function closeMobile() { openMobile.value = false }

// Scroll lock when mobile sidebar is open
watch(openMobile, (v) => {
  try {
    if (v) {
      document.documentElement.style.overflow = 'hidden'
      document.body.style.overflow = 'hidden'
    } else {
      document.documentElement.style.overflow = ''
      document.body.style.overflow = ''
    }
  } catch (e) { /* ignore */ }
})

// Handler para abrir la sidebar en móvil (referencia para add/remove)
function openMobileHandler() { openMobile.value = true }

// Cerrar sidebar con tecla ESC
function escHandler(e) {
  if (!e) return
  const key = e.key || e.code || ''
  if (key === 'Escape' || key === 'Esc') {
    if (openMobile.value) closeMobile()
  }
}
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: var(--sidebar-width, 250px);
  background: var(--color-primary);
  color: #fff;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  overflow-y: auto;
  font-weight: 400; /* Regular */
  box-sizing: border-box;
  transition: width 0.3s ease;
  padding-top: 0; /* Eliminar padding superior para que el header sea visible */
  /* Ocultar scrollbar */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE y Edge */
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width, 70px);
}

.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--color-primary);
  flex-shrink: 0;
}

.collapse-btn-bottom {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.collapse-btn-bottom:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.collapse-btn-bottom:active {
  transform: translateY(0);
}

.sidebar.collapsed .collapse-btn-bottom {
  padding: 12px 8px;
}

.collapse-text {
  font-size: 14px;
}

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  justify-content: flex-end;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--color-primary);
  flex-shrink: 0;
  min-height: 60px;
}

.sidebar.collapsed .sidebar-header {
  justify-content: center;
}

.collapse-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 42px;
  height: 42px;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.collapse-btn:active {
  transform: scale(0.95);
}

/* Ocultar scrollbar en Chrome, Safari y Opera */
.sidebar::-webkit-scrollbar {
  display: none;
}

/* Nota: ancho aumentado para ocupar el espacio a la derecha y eliminar la franja blanca */
/* 2. Navegación */
.sidebar-nav {
  flex-grow: 1;
  padding-top: 32px;
  padding-bottom: 8px;
}
.nav-section-title {
  display: block;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
  padding: 0 20px 10px 20px;
  /* Texto pequeño (12 px, Regular/400) */
  font-size: 0.75rem; /* 12px */
  font-weight: 400; /* Regular */
  letter-spacing: 0.05em; /* Espaciado */
  transition: opacity 0.2s ease;
}

.sidebar.collapsed .nav-section-title {
  display: none;
}

.nav-item {
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  padding: 12px 18px;
  /* Texto mediano (14px, semibold/600) */
  font-size: 0.875rem; /* 14px */
  font-weight: 600; /* Semibold */
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  gap: 12px;
  white-space: nowrap;
  cursor: pointer;
  border-radius: 8px;
  margin: 2px 8px;
}

.sidebar.collapsed .nav-item,
.sidebar.collapsed .nav-collapsible {
  justify-content: center;
  padding: 12px 8px;
}

.nav-icon {
  font-size: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  transition: transform 0.3s ease;
}

.nav-item:hover .nav-icon,
.nav-collapsible:hover .nav-icon {
  transform: scale(1.1);
}

.nav-icon :deep(svg) {
  margin-right: 0 !important;
}

.nav-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: opacity 0.3s ease;
}

.nav-collapsible-title {
  transition: opacity 0.3s ease;
}

.sidebar.collapsed .nav-text,
.sidebar.collapsed .nav-collapsible-title,
.sidebar.collapsed .caret,
.sidebar.collapsed .nav-section-title {
  opacity: 0;
  width: 0;
  display: none;
}

.sidebar.collapsed .nav-icon {
  margin: 0;
  display: flex !important;
  transform: scale(1);
}

.sidebar.collapsed .collapse-text {
  opacity: 0;
  width: 0;
  display: none;
}

.submenu-icon {
  margin-right: 8px;
  font-size: 16px;
  display: inline-flex;
  align-items: center;
}

.submenu-icon :deep(svg) {
  margin-right: 0 !important;
}

.sidebar.collapsed .submenu {
  display: none;
}

.nav-item:hover {
  background: var(--color-primary-hover);
  transform: translateX(4px);
}

.router-link-exact-active {
  /* Botones (Bold/600) para estado activo */
  font-weight: 700; /* Bold */
  background: var(--color-primary-hover);
  border-left-color: var(--color-warning); /* marca visual a la izquierda */
}

.sidebar.collapsed .nav-item:hover {
  transform: translateX(0) scale(1.05);
}

/* Desplegable */
.nav-collapsible {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 12px 18px;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 2px 8px;
}

.nav-collapsible:hover {
  background: var(--color-primary-hover);
  transform: translateX(4px);
}

.sidebar.collapsed .nav-collapsible:hover {
  transform: translateX(0) scale(1.05);
}
/* Asegurar que el título del colapsable tenga el mismo peso que los nav-item */
.nav-collapsible-title {
  font-weight: 600;
  color: inherit;
}
.nav-collapsible.router-link-exact-active .nav-collapsible-title {
  font-weight: 700;
}
.caret { transition: transform 0.2s ease; }
.caret.open { transform: rotate(180deg); }
.submenu {
  background: rgba(0,0,0,0.08);
  padding: 4px 0 6px 0;
  overflow: hidden;
}

.sidebar.collapsed .submenu {
  display: none;
}

/* Animación de expansión/contracción del submenú */
.submenu-slide-enter-active,
.submenu-slide-leave-active {
  transition: all 0.3s ease;
  transform-origin: top;
}

.submenu-slide-enter-from {
  opacity: 0;
  max-height: 0;
  transform: scaleY(0.8);
}

.submenu-slide-enter-to {
  opacity: 1;
  max-height: 500px;
  transform: scaleY(1);
}

.submenu-slide-leave-from {
  opacity: 1;
  max-height: 500px;
  transform: scaleY(1);
}

.submenu-slide-leave-to {
  opacity: 0;
  max-height: 0;
  transform: scaleY(0.8);
}

.submenu-item {
  display: block;
  color: rgba(255,255,255,0.95);
  text-decoration: none;
  padding: 10px 32px;
  font-size: 0.9rem;
  font-weight: 500;
}
.submenu-item:hover, .submenu-item.router-link-exact-active {
  background: rgba(255,255,255,0.04);
  color: #fff;
}
.submenu-item:hover, .submenu-item.router-link-exact-active {
  background: var(--color-primary-hover);
  color: #fff;
}

/* Por defecto ocultar botón móvil en escritorio */
.mobile-open-btn {
  display: none;
}

/* Responsive: transformar sidebar a panel deslizable en móviles */
@media (max-width: 768px) {
  .sidebar-wrapper { position: relative; }
  .sidebar-backdrop {
    position: fixed;
    inset: var(--navbar-height, 64px) 0 0 0;
    background: rgba(0,0,0,0.45);
    z-index: 1100;
    transition: opacity 180ms ease;
  }
  .sidebar {
    position: fixed;
    top: var(--navbar-height, 64px);
    left: 0;
    height: calc(100vh - var(--navbar-height, 64px));
    width: 88%;
    max-width: 360px;
    transform: translateX(-110%);
    transition: transform 220ms ease, opacity 180ms ease;
    z-index: 1200;
    box-shadow: 0 8px 30px rgba(2,6,23,0.4);
    background: var(--color-primary);
  }
  .sidebar.mobile-open { transform: translateX(0%); }

  .mobile-close-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(255,255,255,0.08);
    color: #fff;
    border: none;
    font-size: 20px;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    z-index: 1210;
    cursor: pointer;
  }
  .mobile-close-btn:hover { background: rgba(255,255,255,0.14); }

  /* Evitar que el menú colapse bajo la X: dar espacio en la parte superior y
     reservar zona a la derecha para el botón de cierre solo en móviles */
  .sidebar {
    padding-top: 56px; /* desplaza el contenido hacia abajo para separar de la X */
  }
  /* Botón para abrir menú en móvil */
  .mobile-open-btn {
    display: none;
  }

  /* Ocultar footer dentro de móviles para ahorrar espacio */
  .sidebar-footer { display: none; }
  /* Reservar espacio a la derecha en el primer item colapsable para que no
     quede pegado a la X (solo en móvil) */
  .nav-collapsible:first-of-type {
    padding-right: 64px;
    margin-top: 6px;
  }
}
</style>