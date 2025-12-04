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
  /* Oculta la barra manteniendo el desplazamiento */
  scrollbar-width: none; /* Firefox */
}

.main-content.modern-scrollbar::-webkit-scrollbar,
.modern-scrollbar-wrapper.modern-scrollbar::-webkit-scrollbar,
.modal-body-content.modern-scrollbar::-webkit-scrollbar,
.modal-body-scroll.modern-scrollbar::-webkit-scrollbar {
  display: none; /* WebKit */
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