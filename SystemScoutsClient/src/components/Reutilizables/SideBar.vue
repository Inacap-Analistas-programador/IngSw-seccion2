<template>
  <aside class="sidebar">
    <nav class="sidebar-nav">
      
      <!-- Sin sesión iniciada: solo mostrar Formulario -->
      <div v-if="!isLoggedIn">
        <span class="nav-section-title">ACCESO PÚBLICO</span>
        <router-link to="/inscripciones" class="nav-item">Formulario de Pre-inscripción</router-link>
      </div>
      
      <!-- Con sesión: mostrar menú completo (por defecto admin) -->
      <div v-else>
        <span class="nav-section-title">NAVEGACIÓN PRINCIPAL</span>
        
        <router-link to="/usuarios" class="nav-item">Usuarios y Roles</router-link>
        <router-link to="/cursos-capacitaciones" class="nav-item">Cursos y Capacitaciones</router-link>
        <router-link to="/inscripciones" class="nav-item">Inscripciones</router-link>
        <router-link to="/gestionpersonas" class="nav-item">Gestión de Personas</router-link>
        <router-link to="/pagos" class="nav-item">Pagos</router-link>
        <router-link to="/correos" class="nav-item">Envío de Correos</router-link>
        <router-link to="/mantenedores" class="nav-item">Mantenedores</router-link>
        <router-link to="/manual-acreditacion" class="nav-item">Acreditación Manual</router-link>
        <router-link to="/verificador-qr" class="nav-item" v-if="usuario.rol === 'Administradora Regional'">Verificador QR</router-link>

        <!-- Apartado desplegable: Pantallas 2 -->
        <div class="nav-item nav-collapsible" @click="togglePantallas2">
          <span>Pantallas 2</span>
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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import authService from '@/services/authService'

// Se mantiene el rol para condicionar el menú (por defecto admin para pruebas)
const usuario = ref({ nombre: 'Usuario Demo', rol: 'Administradora Regional' })

// Verificar si hay sesión iniciada (reactivo)
const isLoggedIn = ref(!!localStorage.getItem('token'))

// Desplegable de Mantenedores
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

function toggleMantenedores() {
  showMantenedores.value = !showMantenedores.value
}

function togglePantallas2() {
  showPantallas2.value = !showPantallas2.value
}

onMounted(async () => {
  // Actualizar estado de login
  isLoggedIn.value = !!localStorage.getItem('token')
  
  // Cargar información del usuario actual si está logueado
  if (isLoggedIn.value) {
    const currentUser = await authService.getCurrentUser()
    usuario.value = {
      nombre: currentUser.name,
      rol: currentUser.role
    }
    console.log('Usuario cargado:', usuario.value) // Debug
  }
  
  const route = useRoute()
  // Abrir automáticamente si se navega a /mantenedores
  showMantenedores.value = route.path.startsWith('/mantenedores')
  // Abrir automáticamente Pantallas 2 si coincide la ruta
  showPantallas2.value = route.path.startsWith('/dashboard-2') || route.path.startsWith('/inscripciones-2')
  
  // Watch para actualizar estado al cambiar de ruta
  watch(() => route.path, async (p) => {
    showMantenedores.value = p.startsWith('/mantenedores')
    showPantallas2.value = p.startsWith('/dashboard-2') || p.startsWith('/inscripciones-2')
    
    // Actualizar estado de autenticación al cambiar de ruta
    isLoggedIn.value = !!localStorage.getItem('token')
    
    if (isLoggedIn.value) {
      const currentUser = await authService.getCurrentUser()
      usuario.value = {
        nombre: currentUser.name,
        rol: currentUser.role
      }
      console.log('Usuario actualizado:', usuario.value) // Debug
    }
  })
})
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background: var(--color-primary);
  color: #fff;
  width: 250px;
  height: calc(100vh - 64px); /* Altura total menos la navbar reducida */
  position: fixed;
  top: 64px; /* Altura ajustada de la navbar */
  left: 0;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  overflow-y: auto;
  font-weight: 400; /* Regular */
}
/* 2. Navegación */
.sidebar-nav {
  flex-grow: 1; 
  padding-top: 15px;
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
  display: block;
  color: #fff;
  text-decoration: none;
  padding: 12px 20px; /* Padding para clic cómodo */
  transition: background 0.2s;
  /* Botones (14–16 px, Medium/500) */
  font-size: 0.9375rem; /* 15px */
  font-weight: 500; /* Medium */
}
.nav-item:hover {
  background: var(--color-primary-hover);
}
.router-link-exact-active {
  /* Botones (Bold/600) para estado activo */
  font-weight: 600; /* Bold */
  background: var(--color-primary-hover);
}

/* Desplegable */
.nav-collapsible {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}
.caret { transition: transform 0.2s ease; }
.caret.open { transform: rotate(180deg); }
.submenu {
  background: rgba(0,0,0,0.15);
  padding: 6px 0 8px 0;
}
.submenu-item {
  display: block;
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  padding: 8px 32px;
  font-size: 0.9rem;
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