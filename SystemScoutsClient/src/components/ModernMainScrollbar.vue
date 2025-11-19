<template>
  <div ref="wrapper" class="modern-scrollbar-wrapper">
    <slot />
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const wrapper = ref(null)
const added = ref([])

function addClass() {
  const el = document.querySelector('.main-content')
  if (el) el.classList.add('modern-scrollbar')
  // añadir la clase al wrapper local para estilos en contenedores internos
  if (wrapper.value) wrapper.value.classList.add('modern-scrollbar')

  // Añadir la clase a elementos internos que suelen manejar overflow
  if (wrapper.value) {
    const targets = wrapper.value.querySelectorAll('.table-wrapper, .table-container, .modal-body-wrapper, .modal-body-content, .modal-body-scroll')
    added.value = Array.from(targets)
    added.value.forEach(node => node.classList.add('modern-scrollbar'))
  }
}
function removeClass() {
  const el = document.querySelector('.main-content')
  if (el) el.classList.remove('modern-scrollbar')
  if (wrapper.value) wrapper.value.classList.remove('modern-scrollbar')
  // remover clases añadidas a elementos internos
  if (added.value && added.value.length) {
    added.value.forEach(node => node.classList.remove('modern-scrollbar'))
    added.value = []
  }
}

onMounted(addClass)
onBeforeUnmount(removeClass)
</script>

<style>
/* Estilo más moderno/diferente al original. Aplicable a .main-content y a wrappers internos que reciban la clase modern-scrollbar */
.main-content.modern-scrollbar,
.modern-scrollbar-wrapper.modern-scrollbar,
.modal-body-content.modern-scrollbar,
.modal-body-scroll.modern-scrollbar {
  /* Firefox */
  scrollbar-width: thin; /* delgado */
  /* thumb | track */
  scrollbar-color: rgba(96,165,250,0.9) transparent;
}

/* WebKit (Chrome, Edge Chromium, Safari, Opera) */
.main-content.modern-scrollbar::-webkit-scrollbar,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar,
.modal-body-content.modern-scrollbar::-webkit-scrollbar,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar {
  width: 8px;  /* fino por defecto */
  height: 8px;
}
/* Ampliar ligeramente cuando el usuario interactúa para sensación premium */
.main-content.modern-scrollbar:hover::-webkit-scrollbar,
.modern-scrollbar-wrapper.modern-scrollbar:hover::-webkit-scrollbar,
.modal-body-content.modern-scrollbar:hover::-webkit-scrollbar,
.modal-body-scroll.modern-scrollbar:hover::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}
.main-content.modern-scrollbar::-webkit-scrollbar-track,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar-track,
.modal-body-content.modern-scrollbar::-webkit-scrollbar-track,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar-track {
  background: transparent; /* sin rail pesado, look minimal */
}
.main-content.modern-scrollbar::-webkit-scrollbar-thumb,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar-thumb,
.modal-body-content.modern-scrollbar::-webkit-scrollbar-thumb,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 9999px;
  /* degradado moderno azul → cian */
  background: linear-gradient(180deg, #60a5fa 0%, #22d3ee 100%);
  /* borde transparente para crear separación del track */
  border: 3px solid transparent;
  background-clip: padding-box;
  /* leve glow para resaltar en fondos claros */
  box-shadow: 0 2px 6px rgba(34, 211, 238, 0.35);
}
.main-content.modern-scrollbar::-webkit-scrollbar-thumb:hover,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar-thumb:hover,
.modal-body-content.modern-scrollbar::-webkit-scrollbar-thumb:hover,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6 0%, #06b6d4 100%);
  border-width: 2px; /* parece un poco más grueso al pasar el mouse */
  box-shadow: 0 3px 10px rgba(37, 99, 235, 0.35);
}
.main-content.modern-scrollbar::-webkit-scrollbar-thumb:active,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar-thumb:active,
.modal-body-content.modern-scrollbar::-webkit-scrollbar-thumb:active,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar-thumb:active {
  background: linear-gradient(180deg, #2563eb 0%, #0891b2 100%);
  border-width: 2px;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.45);
}

/* Opcional: esquina (cuando existen ambos scrollbars) */
.main-content.modern-scrollbar::-webkit-scrollbar-corner,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar-corner,
.modal-body-content.modern-scrollbar::-webkit-scrollbar-corner,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar-corner {
  background: transparent;
}

/* Wrapper ocupa el espacio y permite que clases externas (como modal-body-content) controlen overflow */
.modern-scrollbar-wrapper { display: block; width: 100%; height: 100%; }
/* Si el modal aplica esta clase directamente queremos scroll */
.modern-scrollbar-wrapper.modern-scrollbar,
.modal-body-content.modern-scrollbar,
.modal-body-scroll.modern-scrollbar {
  overflow-y: auto;
}
</style>