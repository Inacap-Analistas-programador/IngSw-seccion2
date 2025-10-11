<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <slot></slot>
      <button @click="closeModal">Cerrar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseModal',
  data() {
    return {
      visible: false,
    };
  },
  methods: {
    openModal() {
      this.visible = true;
    },
    closeModal() {
      this.visible = false;
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  min-width: 300px;
}
</style>

<template>
  <BaseModal ref="modal" @close="onClose">
    <header class="modal-header">
      <h3>{{ title }}</h3>
      <button @click="onClose">✖</button>
    </header>
    <form @submit.prevent="handleSubmit">
      <!--campos y validaciones aquí-->
    </form>
  </BaseModal>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from './BaseModal.vue'
// lógica de validación aquí
</script>