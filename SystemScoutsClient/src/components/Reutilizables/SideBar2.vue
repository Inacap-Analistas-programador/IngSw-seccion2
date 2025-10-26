<template>
  <aside :class="['sidebar', { collapsed, 'mobile-open': openMobile }]" @click.self="closeMobile">
    <div class="sidebar-top">
      <button class="collapse-btn" @click="toggleCollapse" :aria-pressed="collapsed">
        {{ collapsed ? '»' : '«' }}
      </button>
    </div>

    <ul>
      <li v-for="item in menuItems" :key="item.id">
        <button 
          class="sidebar-link" 
          @click="() => { goToMockup(item.id); closeMobile(); }"
          :class="{ active: currentMockup === item.id }"
          :title="item.label"
        >
          <span class="icon">{{ item.icon }}</span>
          <span class="label">{{ item.label }}</span>
        </button>
      </li>
    </ul>

    <div class="sidebar-bottom">
      <small class="version">v0.1</small>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

// Estado local para saber qué mockup está activo
const currentMockup = ref(1);

// Collapsed / mobile state
const collapsed = ref(false);
const openMobile = ref(false);

// Lista de ítems de la sidebar
const menuItems = [
  { id: 1, label: "Login", icon: "🔑" },
  { id: 2, label: "Dashboard", icon: "📊" },
  { id: 3, label: "Usuarios", icon: "👥" },
  { id: 4, label: "Cursos", icon: "📚" },
  { id: 5, label: "Inscripción", icon: "📝" },
  { id: 6, label: "Personas", icon: "👤" },
  { id: 7, label: "Habilitación", icon: "✅" },
  { id: 8, label: "Pagos", icon: "💰" },
  { id: 9, label: "Gestión", icon: "⚙️" },
  { id: 10, label: "Correos", icon: "📧" },
  { id: 11, label: "Acreditación", icon: "🎟️" },
];

// Persist collapse state
onMounted(() => {
  const saved = localStorage.getItem('sidebar-collapsed')
  if (saved !== null) collapsed.value = saved === '1'
  // listen for mobile open event
  window.addEventListener('open-sidebar-mobile', openMobileSidebar)
})

onBeforeUnmount(() => {
  window.removeEventListener('open-sidebar-mobile', openMobileSidebar)
})

function toggleCollapse() {
  collapsed.value = !collapsed.value
  localStorage.setItem('sidebar-collapsed', collapsed.value ? '1' : '0')
}

function openMobileSidebar() { openMobile.value = true }
function closeMobile() { openMobile.value = false }

// Función para redirigir a un mockup (ejemplo simple con scroll dentro de la misma página)
function goToMockup(id) {
  currentMockup.value = id;
  const mockup = document.getElementById(`mockup-${id}`);
  if (mockup) {
    mockup.scrollIntoView({ behavior: "smooth" });
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--color-primary);
  color: #fff;
  padding: 20px 12px;
  box-shadow: 2px 0 8px rgba(15, 23, 30, 0.08);
  z-index: 40;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: width 180ms ease, transform 180ms ease;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  width: 100%;
  background: none;
  border: none;
  color: #fff;
  padding: 10px 14px;
  cursor: pointer;
  text-align: left;
  border-radius: 8px;
  transition: background 0.15s, transform 0.08s;
}

.sidebar-link:hover {
  background: var(--color-primary-hover);
}

.sidebar-link.active {
  background: var(--color-primary-hover);
  box-shadow: inset 0 0 0 2px rgba(255,255,255,0.02);
}

.icon {
  margin-right: 10px;
}

/* Responsive: hide fixed sidebar on small screens and allow main to take full width */
@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    transform: translateY(-110%);
    width: 100%;
    height: auto;
    box-shadow: none;
    padding: 8px 6px;
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
  }
  .sidebar.mobile-open { transform: translateY(0%); background: rgba(39,73,99,0.98); }
.sidebar.mobile-open { transform: translateY(0%); background: var(--color-primary); }
  .sidebar-link { display: inline-flex; padding: 8px 10px; }
}

/* Collapsed state */
.sidebar.collapsed { width: var(--sidebar-collapsed-width); }
.sidebar.collapsed .label { display: none; }
.sidebar.collapsed .icon { margin-right: 0; }

.sidebar-top { display:flex; justify-content:flex-end }
.collapse-btn { background: rgba(255,255,255,0.04); border: none; color:#fff; padding:6px 8px; border-radius:6px; cursor:pointer }
.collapse-btn { background: rgba(255,255,255,0.1); border: none; color:#fff; padding:6px 8px; border-radius:6px; cursor:pointer }
.sidebar-bottom { margin-top: auto; text-align:center; opacity:0.8 }
.version { font-size: 0.75rem; color: rgba(255,255,255,0.7) }
</style>
