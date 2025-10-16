<template>
  <div v-if="visible" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-content">
      <slot></slot>
      <button class="close-btn" @click="closeModal" aria-label="Cerrar">Cerrar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseModal',
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
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
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