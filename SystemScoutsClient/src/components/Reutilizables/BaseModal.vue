<template>
  <div v-if="visible" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-content" role="document">
      <button class="close-btn" @click="closeModal" aria-label="Cerrar ventana">×</button>
      <slot></slot>
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
  position: relative; /* needed for absolute-positioned close button */
  transform-origin: center center;
  /* entrance animation */
  animation: modal-in .18s ease-out both;
}

/* Keep the modal content bounded to the viewport and enable internal scrolling
   so very tall forms (like user permissions) don't expand the modal to full screen. */
.modal-content {
  width: 95%;
  max-width: 900px;
  max-height: 90vh;
  overflow: auto;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(0,0,0,0.06);
  color: #222;
  border: none;
  border-radius: 8px;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  transition: background .12s ease, transform .12s ease;
}
.close-btn:hover {
  background: rgba(0,0,0,0.12);
  transform: translateY(-1px);
}
.close-btn:focus {
  outline: 2px solid #3498db;
  outline-offset: 2px;
}

/* overlay fade in */
.modal-overlay {
  animation: overlay-in .18s ease-out both;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.96); }
  to   { opacity: 1; transform: scale(1); }
}

@keyframes overlay-in {
  from { background: rgba(0,0,0,0); }
  to   { background: rgba(0,0,0,0.5); }
}
</style>