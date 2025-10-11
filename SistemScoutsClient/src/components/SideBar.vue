<template>
  <aside class="sidebar">
    <ul>
      <li v-for="item in menuItems" :key="item.id">
        <button 
          class="sidebar-link" 
          @click="goToMockup(item.id)"
          :class="{ active: currentMockup === item.id }"
        >
          <span class="icon">{{ item.icon }}</span>
          <span class="label">{{ item.label }}</span>
        </button>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { ref } from "vue";

// Estado local para saber qué mockup está activo
const currentMockup = ref(1);

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
  width: 220px;
  background: #2c3e50;
  padding: 10px 0;
  height: 100vh;
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
  color: #ecf0f1;
  padding: 12px 15px;
  cursor: pointer;
  text-align: left;
}

.sidebar-link:hover {
  background: #34495e;
}

.sidebar-link.active {
  background: #1abc9c;
}

.icon {
  margin-right: 10px;
}
</style>
