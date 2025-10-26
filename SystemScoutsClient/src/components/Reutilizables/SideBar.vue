<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <img :src="logoSrc" alt="Logo Scouts" class="logo" />
      <h1 class="titulo">SBS</h1>
    </div>

    <nav class="sidebar-nav">
      
      <div v-if="usuario.rol === 'Administradora Regional'">
        <span class="nav-section-title">Navegación Principal</span>
        <router-link to="/" class="nav-item">Panel de Control</router-link>
        <router-link to="/usuarios" class="nav-item">Usuarios y Roles</router-link>
        <router-link to="/cursos" class="nav-item">Cursos y Capacitaciones</router-link>
        <router-link to="/inscripciones" class="nav-item">Inscripciones</router-link>
        <router-link to="/personas" class="nav-item">Gestión de Personas</router-link>
        <router-link to="/pagos" class="nav-item">Pagos</router-link>
        <router-link to="/correos" class="nav-item">Envío de Correos</router-link>
        <router-link to="/reportes" class="nav-item">Reportes</router-link>
        <router-link to="/qr" class="nav-item">Acreditación QR</router-link>
      </div>
      <div v-else>
        <router-link to="/" class="nav-item">🏠 Inicio</router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <hr class="footer-divider" />
      <div class="usuario-menu" @click="toggleMenu">
        <strong>{{ usuario.nombre }}</strong>
        <small>{{ usuario.rol }}</small>
      </div>
      
      <div v-if="menuAbierto" class="dropdown-up">
        <router-link to="/perfil" class="dropdown-item" @click="cerrarMenu">👤 Mi Perfil</router-link>
        <button class="logout" @click="cerrarSesion">🚪 Cerrar sesión</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import logoSrc from '@/assets/Logo_Boyscout_Chile.png'
import { useRouter } from 'vue-router'

const usuario = ref({ nombre: 'Cargando...', rol: '---' })
const menuAbierto = ref(false)
const router = useRouter()

function toggleMenu() {
  menuAbierto.value = !menuAbierto.value
}

function cerrarMenu() {
  menuAbierto.value = false
}

function cerrarSesion() {
  alert(`Hasta pronto, ${usuario.value.nombre}`)
  cerrarMenu()
  router.push('/')
}

onMounted(async () => {
  usuario.value = await usuarioService.obtenerUsuarioActual()
})
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background: #1e3a8a;
  color: white;
  width: 250px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow-y: auto;
  font-weight: 400; /* Regular */
}

/* 1. Encabezado */
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #3b5998;
}
.logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  margin-right: 10px;
}
.titulo {
  margin: 0;
  /* Título secundario (18–24 px, Semibold/500) */
  font-size: 1.25rem; /* 20px */
  font-weight: 500; /* Semibold */
  line-height: 1.3; /* Títulos (1.2–1.4) */
}

/* 2. Navegación */
.sidebar-nav {
  flex-grow: 1; 
  padding-top: 15px;
}
.nav-section-title {
  display: block;
  text-transform: uppercase;
  color: #a0bcf0;
  padding: 0 20px 10px 20px;
  /* Texto pequeño (12 px, Regular/400) */
  font-size: 0.75rem; /* 12px */
  font-weight: 400; /* Regular */
  letter-spacing: 0.05em; /* Espaciado */
}
.nav-item {
  display: block;
  color: white;
  text-decoration: none;
  padding: 12px 20px; /* Padding para clic cómodo */
  transition: background 0.2s;
  /* Botones (14–16 px, Medium/500) */
  font-size: 0.9375rem; /* 15px */
  font-weight: 500; /* Medium */
}
.nav-item:hover {
  background: #2563eb;
}
.router-link-exact-active {
  /* Botones (Bold/600) para estado activo */
  font-weight: 600; /* Bold */
  background: #2563eb;
}

/* 3. Footer (Perfil) */
.sidebar-footer {
  position: sticky;
  bottom: 0;
  background: #1e3a8a;
  padding: 15px;
  position: relative;
  /* Texto normal (line-height) */
  line-height: 1.5;
}
.footer-divider {
  border: 0;
  height: 1px;
  background: #3b5998;
  margin-bottom: 15px;
}
.usuario-menu {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
}
.usuario-menu:hover {
  background: #2563eb;
}
.usuario-menu strong {
  /* Texto normal (14-16px, Medium/500) */
  font-size: 0.875rem; /* 14px */
  font-weight: 500; /* Medium */
}
.usuario-menu small {
  /* Texto pequeño (12px, Regular/400) */
  font-size: 0.75rem; /* 12px */
  font-weight: 400; /* Regular */
  color: #a0bcf0; /* Color secundario (branding) */
}

/* Dropdown que aparece hacia arriba */
.dropdown-up {
  position: absolute;
  bottom: 100%;
  left: 15px;
  right: 15px;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  margin-bottom: 10px;
  /* Texto normal (14-16px, Regular/400) */
  font-size: 0.875rem; /* 14px */
  font-weight: 400; /* Regular */
  line-height: 1.5;
  /* Color de texto principal */
  color: #111111;
}
.dropdown-item {
  display: block;
  text-decoration: none;
  padding: 6px 0;
  /* Botones (14-16px, Medium/500) */
  font-weight: 500; /* Medium */
  /* Links (colores del branding) */
  color: #1e3a8a;
}
.logout {
  width: 100%;
  background: none;
  border: none;
  padding: 6px 0;
  text-align: left;
  cursor: pointer;
  /* Botones (14-16px, Bold/600) */
  font-size: 0.875rem; /* 14px */
  font-weight: 600; /* Bold */
  /* Links (colores del branding) */
  color: #dc2626;
}
</style>