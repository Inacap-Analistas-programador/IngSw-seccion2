<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="closeModal" role="dialog" aria-modal="true">
    <div class="modal-content" role="document">
      <!-- Header opcional -->
      <div class="modal-header" v-if="$slots.title">
        <h3 class="modal-title"><slot name="title"></slot></h3>
      </div>
      <!-- Botón cerrar siempre visible -->
      <button class="close-btn" @click="closeModal" aria-label="Cerrar ventana">×</button>
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
const ModernMainScrollBar = ModernMainScrollbar

const props = defineProps({
  modelValue: { type: Boolean, default: false }
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
  max-width: 1200px;
  max-height: 92vh;
  overflow: hidden; /* Evita que el contenido se desborde */
  animation: modal-in .2s ease-out both;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.modal-body-content {
  padding: 0;
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

 .close-btn {
  position: absolute;
  top: 1rem;
  right: 3.5rem; /* más separación del borde y scrollbar */
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f8f9fa;
  color: #7f8c8d;
  font-size: 24px;
  font-weight: 300;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  line-height: 1;
  padding: 0;
}

.close-btn:hover {
  background: #e74c3c;
  color: white;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
}

.close-btn:active {
  transform: rotate(90deg) scale(0.95);
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
</style>