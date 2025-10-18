<template>
<<<<<<< HEAD
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <slot></slot>
      <button @click="closeModal">Cerrar</button>
=======
  <div v-if="visible" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-content">
      <slot></slot>
      <button class="close-btn" @click="closeModal" aria-label="Cerrar">Cerrar</button>
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseModal',
<<<<<<< HEAD
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
=======
  props: {
    modelValue: { type: Boolean, default: false }
  },
  computed: {
    visible: {
      get() { return this.modelValue },
      set(v) { this.$emit('update:modelValue', v) }
    }
  },
  methods: {
    closeModal() {
      this.$emit('update:modelValue', false)
      this.$emit('close')
    }
  }
}
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
<<<<<<< HEAD
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
=======
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 1.25rem;
  border-radius: 8px;
  min-width: 320px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.close-btn {
  margin-top: 12px;
  background: #eee;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
