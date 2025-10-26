<template>
  <aside class="sidebar">
    <nav class="sidebar-nav">
      
      <div v-if="usuario.rol === 'Administradora Regional'">
        <span class="nav-section-title">NAVEGACIÓN PRINCIPAL</span>
        
        <router-link to="/usuarios" class="nav-item">Usuarios y Roles</router-link>
        <router-link to="/cursos-capacitaciones" class="nav-item">Cursos y Capacitaciones</router-link>
        <router-link to="/inscripciones" class="nav-item">Inscripciones</router-link>
        <router-link to="/gestionpersonas" class="nav-item">Gestión de Personas</router-link>
        <router-link to="/pagos" class="nav-item">Pagos</router-link>
        <router-link to="/correos" class="nav-item">Envío de Correos</router-link>
        <div class="nav-item nav-collapsible" @click="toggleMantenedores">
          <span>Mantenedores</span>
          <span class="caret" :class="{ open: showMantenedores }">▾</span>
        </div>
        <div v-if="showMantenedores" class="submenu">
          <router-link
            v-for="t in mantenedoresTabs"
            :key="t.id"
            class="submenu-item"
            :to="`/mantenedores/${t.id}`"
          >
            {{ t.label }}
          </router-link>
        </div>
        <router-link to="/manual-acreditacion" class="nav-item">Acreditación Manual</router-link>
        <router-link to="/verificador-qr" class="nav-item">Verificador QR</router-link>
      </div>
      <div v-else>
        <router-link to="/dashboard" class="nav-item">Inicio</router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

// Se mantiene el rol para condicionar el menú
const usuario = ref({ nombre: 'Usuario Demo', rol: 'Administradora Regional' })

// Desplegable de Mantenedores
const showMantenedores = ref(false)
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

onMounted(async () => {
  // Aquí puedes cargar los datos del usuario desde tu servicio
  // usuario.value = await usuarioService.obtenerUsuarioActual()
  const route = useRoute()
  // Abrir automáticamente si se navega a /mantenedores
  showMantenedores.value = route.path.startsWith('/mantenedores')
  watch(() => route.path, (p) => {
    showMantenedores.value = p.startsWith('/mantenedores')
  })
})
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background: #1e3a8a;
  color: white;
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
  background: #173274;
  padding: 6px 0 8px 0;
}
.submenu-item {
  display: block;
  color: #e6eeff;
  text-decoration: none;
  padding: 8px 32px;
  font-size: 0.9rem;
}
.submenu-item:hover, .submenu-item.router-link-exact-active {
  background: #2563eb;
  color: #fff;
}

/* Responsive: ocultar sidebar en móviles */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
}
</style>