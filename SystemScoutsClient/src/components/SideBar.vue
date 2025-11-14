<template>
  <aside class="sidebar">
    <nav class="sidebar-nav">
      
      <!-- Sin sesión iniciada: solo mostrar Formulario -->
      <div v-if="!isLoggedIn">
        <span class="nav-section-title">ACCESO PÚBLICO</span>
        <router-link to="/inscripciones" class="nav-item">Pre-inscripción</router-link>
      </div>
      
      <!-- Con sesión: mostrar menú completo (por defecto admin) -->
      <div v-else>
        <!-- Apartado desplegable: Usuarios y Roles -->
        <div class="nav-item nav-collapsible" @click="toggleUsuarios" :class="{ 'router-link-exact-active': showUsuarios }">
          <span class="nav-collapsible-title">Usuarios y Roles</span>
          <span class="caret" :class="{ open: showUsuarios }">▾</span>
        </div>
        <div v-show="showUsuarios" class="submenu">
          <router-link to="/usuarios" class="submenu-item">Usuarios</router-link>
          <router-link to="/roles" class="submenu-item">Roles</router-link>
        </div>

        <router-link to="/cursos-capacitaciones" class="nav-item">Cursos y Capacitaciones</router-link>
        <router-link to="/inscripciones" class="nav-item">Inscripciones</router-link>
        <router-link to="/gestionpersonas" class="nav-item">Gestión de Personas</router-link>
        <router-link to="/pagos" class="nav-item">Pagos</router-link>
        <router-link to="/correos" class="nav-item">Envío de Correos</router-link>
        <router-link to="/mantenedores" class="nav-item">Mantenedores</router-link>
        <router-link to="/manual-acreditacion" class="nav-item">Acreditación Manual</router-link>
        <router-link to="/verificador-qr" class="nav-item">Verificador QR</router-link>

  <!-- Apartado desplegable: Pantallas 2 -->
        <div class="nav-item nav-collapsible" @click="togglePantallas2" :class="{ 'router-link-exact-active': showPantallas2 }">
          <span class="nav-collapsible-title">Pantallas 2</span>
          <span class="caret" :class="{ open: showPantallas2 }">▾</span>
        </div>
        <div v-show="showPantallas2" class="submenu">
          <router-link to="/dashboard-2" class="submenu-item">Dashboard 2</router-link>
          <router-link to="/inscripciones-2" class="submenu-item">Formulario 2</router-link>
        </div>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import authService from '@/services/authService'

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
  if (!e) return
  if (STORAGE_TOKEN_KEYS.includes(e.key)) {
    // Recalcular por si cambia una u otra clave
    isLoggedIn.value = hasToken()
  }
}

// Desplegable de Mantenedores
const showUsuarios = ref(false)
const showMantenedores = ref(false)
const showPantallas2 = ref(false)
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
  { id: 'roles', label: 'Roles' },
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

onMounted(async () => {
  // No consultamos el backend de auth en modo UI-only; usar usuario por defecto
  
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
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', onStorage)
})
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background: var(--color-primary);
  color: #fff;
  width: 256px; /* ampliar para cubrir la zona derecha y eliminar franja blanca */
  height: calc(100vh - 64px); /* Altura total menos la navbar reducida */
  position: fixed;
  top: 64px; /* Altura ajustada de la navbar */
  left: 0;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  overflow-y: auto;
  font-weight: 400; /* Regular */
  box-sizing: border-box;
  /* Ocultar scrollbar */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE y Edge */
}

/* Ocultar scrollbar en Chrome, Safari y Opera */
.sidebar::-webkit-scrollbar {
  display: none;
}

/* Nota: ancho aumentado para ocupar el espacio a la derecha y eliminar la franja blanca */
/* 2. Navegación */
.sidebar-nav {
  flex-grow: 1;
  padding-top: 20px; /* más separación respecto a la navbar */
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
}
.nav-item {
  display: flex; /* permite alinear iconos y texto */
  align-items: center;
  gap: 12px;
  color: #fff;
  text-decoration: none;
  padding: 12px 18px; /* Padding para clic cómodo */
  transition: background 0.15s ease, padding 0.12s ease;
  /* Botones (14–16 px, Medium/500) */
  font-size: 0.95rem; /* 15.2px */
  font-weight: 600; /* Medium/Bold para mejor legibilidad */
  width: 100%;
  box-sizing: border-box;
  border-left: 4px solid transparent; /* para indicar activo */
  min-height: 44px; /* tamaño mínimo, clickable fácil */
}
.nav-item:hover {
  background: rgba(255,255,255,0.05);
}
.nav-item:hover {
  background: var(--color-primary-hover);
}
.router-link-exact-active {
  /* Botones (Bold/600) para estado activo */
  font-weight: 700; /* Bold */
  background: var(--color-primary-hover);
  border-left-color: var(--color-warning); /* marca visual a la izquierda */
}

/* Desplegable */
.nav-collapsible {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 12px 18px;
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

/* Responsive: ocultar sidebar en móviles */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
}
</style>