<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import logoSrc from '@/assets/Logo_Boyscout_Chile.png' // asegúrate de que el archivo exista

// Estado reactivo del menú (para móviles)
const menuActive = ref(false)
// Dropdown "Más"
const moreOpen = ref(false)

// Full list provided by user
const allLinks = [
  { label: 'Panel de Control', to: { name: 'dashboard' } },
  { label: 'Usuarios y Roles', to: { name: 'usuarios' } },
  { label: 'Mantenedores', to: { name: 'mantenedores' } },
  { label: 'Cursos y Capacitaciones', to: { name: 'cursoscapacitaciones' } },
  { label: 'Inscripciones', to: { name: 'formularioPreInscripcion' } },
  { label: 'Gestión de Personas', to: { name: 'gestionpersonas' } },
  { label: 'Pagos', to: { name: 'pagosview' } },
  { label: 'Acreditación', to: { name: 'manualacreditacion' } },
  { label: 'QR', to: { name: 'verificadorqr' } },
  { label: 'Envío de Correos', to: { name: 'correos' } },
  { label: 'Reportes', to: '#' },
]

const VISIBLE_COUNT = 5 // mostrar primeros 5 enlaces, resto en "Más"

const visibleLinks = computed(() => allLinks.slice(0, VISIBLE_COUNT))
const moreLinks = computed(() => allLinks.slice(VISIBLE_COUNT))

// Cuando menú móvil esté abierto, queremos mostrar todos los enlaces en columna
const displayedLinks = computed(() => (menuActive.value ? allLinks : visibleLinks.value))

// Cerrar dropdown con Escape o click fuera
function onKeydown(e) {
  if (e.key === 'Escape') {
    moreOpen.value = false
    menuActive.value = false
  }
}

function onWindowClick(e) {
  const target = e.target
  // si el click no es en el botón ni dentro del dropdown, cerrarlo
  const moreBtn = document.querySelector('.more-button')
  const dropdown = document.querySelector('.more-dropdown')
  if (moreOpen.value && moreBtn && dropdown && !moreBtn.contains(target) && !dropdown.contains(target)) {
    moreOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  window.addEventListener('click', onWindowClick)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  window.removeEventListener('click', onWindowClick)
})

function toggleMore() {
  moreOpen.value = !moreOpen.value
}

function onNavClick() {
  // al clicar un enlace en mobile, cerrar menú
  menuActive.value = false
  moreOpen.value = false
}
</script>

<template>
  <nav class="navbar">
    <!-- Logo y título -->
    <div class="navbar-left">
      <img :src="logoSrc" alt="Logo Scouts" class="logo" />
      <span class="title">SSB</span>
    </div>

    <!-- Enlaces de navegación -->
    <ul :class="['navbar-links', { active: menuActive }]">
      <template v-for="(link, idx) in displayedLinks" :key="link.label">
        <li :class="{ 'has-submenu': link.submenu }">
          <template v-if="link.submenu">
            <button class="nav-button" @click.prevent="link.isOpen = !link.isOpen">
              {{ link.label }} ▾
            </button>
            <ul v-show="link.isOpen" class="submenu">
              <li v-for="subItem in link.submenu" :key="subItem.label">
                <router-link :to="subItem.to" @click.native="onNavClick">{{ subItem.label }}</router-link>
              </li>
            </ul>
          </template>
          <template v-else>
            <router-link v-if="typeof link.to === 'object'" :to="link.to" @click.native="onNavClick">{{ link.label }}</router-link>
            <a v-else :href="link.to" @click="onNavClick">{{ link.label }}</a>
          </template>
        </li>
      </template>

      <!-- Más dropdown (solo cuando no estamos mostrando el menú móvil completo) -->
      <li v-if="!menuActive && moreLinks.length" class="more-cell">
        <button class="more-button" @click.prevent="toggleMore" :aria-expanded="moreOpen.toString()" aria-haspopup="menu">
          Más ▾ <span class="more-count">({{ moreLinks.length }})</span>
        </button>

        <ul v-if="moreOpen" class="more-dropdown" role="menu">
          <li v-for="m in moreLinks" :key="m.label" role="none">
            <router-link v-if="typeof m.to === 'object'" :to="m.to" role="menuitem" @click.native="onNavClick">{{ m.label }}</router-link>
            <a v-else :href="m.to" role="menuitem" @click="onNavClick">{{ m.label }}</a>
          </li>
        </ul>
      </li>
    </ul>

    <!-- Botón para menú móvil -->
    <button 
      class="navbar-menu" 
      @click="menuActive = !menuActive" 
      aria-label="Alternar menú">
      ☰
    </button>
  </nav>
</template>

<style scoped>
/* ====== Barra de navegación ====== */
.navbar {
  background: #2c5aa0; /* Azul institucional Scouts */
  color: white;
  padding: 14px 26px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  font-family: "Segoe UI", Arial, sans-serif;
}

/* ====== Sección izquierda ====== */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 18px;
}

.logo {
  width: 60px;          /* 🔹 Tamaño aumentado del logo */
  height: 60px;         /* 🔹 */
  border-radius: 50%;
  border: 3px solid #ffcc00; /* Amarillo brillante */
  background: white;
  object-fit: cover;
  box-shadow: 0 3px 6px rgba(0,0,0,0.18);
}

.title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 0.6px;
}

/* ====== Enlaces ====== */
.navbar-links {
  display: flex;
  gap: 26px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar-links a, .nav-button {
  font-weight: 600;
  text-decoration: none;
  color: white;
  transition: color 0.3s, border-bottom 0.3s;
  border-bottom: 2px solid transparent;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-size: inherit;
}

.has-submenu {
  position: relative;
}

.submenu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  padding: 8px 0;
  min-width: 180px;
  z-index: 100;
  list-style: none;
}

.submenu a {
  color: #2c5aa0;
  display: block;
  padding: 8px 16px;
  text-decoration: none;
}

.submenu a:hover {
  background: #f0f4f8;
  color: #2c5aa0;
  border-bottom: none;
}

.navbar-links a:hover {
  color: #ffcc00;
  border-bottom: 2px solid #ffcc00;
}

/* ====== Botón móvil ====== */
.navbar-menu {
  display: none;
  background: #ffcc00;
  color: #2c5aa0;
  font-size: 1.6rem;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  margin-left: 14px;
}

/* Más dropdown */
.more-cell { position: relative; }
.more-button {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.more-button .more-count { opacity: 0.8; font-size: 0.9rem; margin-left: 6px }
.more-dropdown {
  position: absolute;
  top: 120%;
  right: 0;
  min-width: 200px;
  background: #fff;
  color: #222;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  padding: 8px 6px;
  z-index: 40;
}
.more-dropdown li { list-style: none; }
.more-dropdown a, .more-dropdown router-link {
  display: block;
  padding: 8px 10px;
  color: #163a59;
  text-decoration: none;
}
.more-dropdown a:hover, .more-dropdown router-link:hover { background: rgba(22,58,89,0.06) }

/* ====== Modo responsive ====== */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 15px 20px;
  }

  .navbar-links {
    flex-direction: column;
    gap: 10px;
    width: 100%;
    display: none;
    margin-top: 12px;
  }

  .navbar-links.active {
    display: flex;
  }

  .navbar-menu {
    display: block;
    align-self: flex-end;
  }
}
</style>
