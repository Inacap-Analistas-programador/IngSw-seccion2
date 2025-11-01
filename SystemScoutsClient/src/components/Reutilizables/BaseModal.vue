<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="closeModal" role="dialog" aria-modal="true">
    <div class="modal-content" role="document">
      <!-- Renderizado condicional: Nuevo con slots o Antiguo -->
      
      <!-- Nuevo: Si se usan los slots de title o footer -->
      <template v-if="$slots.title || $slots.footer">
        <div class="modal-header" v-if="$slots.title">
          <h3 class="modal-title">
            <slot name="title"></slot>
          </h3>
          <button class="close-btn" @click="closeModal" aria-label="Cerrar ventana">×</button>
        </div>
        
        <div class="modal-body-content">
          <slot></slot> <!-- Contenido principal -->
        </div>
        
        <div class="modal-footer" v-if="$slots.footer">
          <slot name="footer"></slot>
        </div>
      </template>

      <!-- Antiguo: Si no se usan los slots, para retrocompatibilidad -->
      <template v-else>
        <button class="close-btn" @click="closeModal" aria-label="Cerrar ventana">×</button>
        <slot></slot> <!-- Renderiza todo junto como antes -->
      </template>

    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

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
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  width: 95%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden; /* Evita que el contenido se desborde */
  animation: modal-in .2s ease-out both;
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
  padding: 24px;
  overflow-y: auto; /* Permite scroll solo en el cuerpo */
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
  background: none;
  border: none;
  font-size: 24px;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.2s ease;
}
.close-btn:hover {
  color: #111827;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
</style>