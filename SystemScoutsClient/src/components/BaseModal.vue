<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="closeModal" role="dialog" aria-modal="true">
    <div class="modal-content" :class="[`modal-size-${size}`]" role="document">
      <!-- Header opcional -->
      <div class="modal-header" v-if="$slots.title">
        <h3 class="modal-title"><slot name="title"></slot></h3>
        <button class="modal-close-btn" @click="closeModal" aria-label="Cerrar">×</button>
      </div>
      <!-- Cuerpo con scrollbar personalizado -->
      <ModernMainScrollbar class="modal-body-content">
        <slot></slot>
      </ModernMainScrollbar>
      <!-- Footer opcional -->
      <div class="modal-footer" v-if="$slots.footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
// Ya no se importan defineProps/defineEmits (macro implícito con <script setup>) para evitar warnings.
import ModernMainScrollbar from './ModernMainScrollbar.vue'
// Alias para variantes con mayúsculas diferentes en algunos archivos
// const ModernMainScrollBar = ModernMainScrollbar

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  size: { type: String, default: 'xl' } // sm, md, lg, xl
});

const emit = defineEmits(['update:modelValue', 'close']);

const closeModal = () => {
  emit('update:modelValue', false);
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  transition: opacity 0.2s ease;
}
.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  width: 98%;
  /* max-width se define por la clase de tamaño */
  max-width: 1200px; /* Fallback */
  max-height: 92vh;
  overflow: hidden; /* Evita que el contenido se desborde */
  animation: modal-in .2s ease-out both;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  background-color: white;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a237e;
  margin: 0;
  text-transform: uppercase;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  line-height: 1;
  padding: 4px;
  transition: color 0.2s;
}

.modal-close-btn:hover {
  color: #3949ab;
}

.modal-body-content {
  padding: 24px;
  overflow-y: auto; /* Permite desplazamiento vertical del contenido largo */
  flex: 1;
  min-height: 0;
}

.modal-body-scroll {
  overflow-y: auto; /* Retrocompatibilidad con versión antigua */
  flex: 1;
  min-height: 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
}


@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}

/* Mobile adjustments: avoid close button overlapping header/content */
@media (max-width: 600px) {
  .modal-content {
    width: 96%;
    max-width: 540px;
    border-radius: 10px;
  }

  /* Make the close button slightly smaller and closer to the corner on phones */
  .close-btn {
    top: 12px;
    right: 12px;
    width: 36px;
    height: 36px;
    font-size: 20px;
  }

  /* Reserve horizontal space in the header so the title doesn't sit under the X */
  .modal-header {
    padding: 18px 64px 12px 16px; /* top, right (space for X), bottom, left */
  }

  /* Slight inner padding so content doesn't touch edges */
  .modal-body-content {
    padding: 0 14px 16px 14px;
  }
}

/* Tamaños */
.modal-size-sm { max-width: 320px; }
.modal-size-md { max-width: 700px; }
.modal-size-lg { max-width: 900px; }
.modal-size-xl { max-width: 1200px; }
</style>