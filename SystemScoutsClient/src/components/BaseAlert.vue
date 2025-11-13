<template>
  <transition name="fade">
    <div
      v-if="visible"
      :class="['p-4 rounded-md mb-4 flex items-start gap-3', alertClasses]"
      role="alert"
      aria-live="polite"
    >
      <div class="shrink-0 mt-0.5" aria-hidden>
        <svg v-if="type === 'exito'" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.707a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <svg v-else-if="type === 'error'" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.72-1.36 3.485 0l6.518 11.59c.75 1.334-.213 2.998-1.742 2.998H3.481c-1.53 0-2.492-1.664-1.742-2.998L8.257 3.1zM11 14a1 1 0 10-2 0 1 1 0 002 0zm-1-3a1 1 0 01-1-1V6a1 1 0 112 0v4a1 1 0 01-1 1z" clip-rule="evenodd"/>
        </svg>
        <svg v-else-if="type === 'Advertencia'" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M8.257 3.099c.765-1.36 2.72-1.36 3.485 0l6.518 11.59c.75 1.334-.213 2.998-1.742 2.998H3.481c-1.53 0-2.492-1.664-1.742-2.998L8.257 3.1z"/>
        </svg>
        <svg v-else class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016.918 3H3.082a2 2 0 00-1.079 2.884zM18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
        </svg>
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-start justify-between gap-3">
          <div>
            <div v-if="title" class="font-semibold truncate">{{ title }}</div>
            <div class="text-sm truncate" v-if="!$slots.default">{{ message }}</div>
            <div class="text-sm" v-else><slot /></div>
          </div>

          <button
            v-if="dismissible"
            @click="close"
            class="ml-2 inline-flex items-center justify-center rounded focus:outline-none focus:ring-2 focus:ring-offset-1"
            :aria-label="`Cerrar alerta: ${title || message}`"
          >
            <svg class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "BaseAlert",
  props: {
    type: {
      type: String,
      default: "info",
      validator: v => ["exito", "error", "advertencia", "informacion"].includes(v)
    },
    title: {
      type: String,
      default: ""
    },
    message: {
      type: String,
      default: ""
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    modelValue: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      visible: this.modelValue
    };
  },
  watch: {
    modelValue(val) {
      this.visible = val;
    }
  },
  computed: {
    alertClasses() {
      switch (this.type) {
        case "success":
          return "bg-green-50 text-green-800 border border-green-200";
        case "error":
          return "bg-red-50 text-red-800 border border-red-200";
        case "warning":
          return "bg-yellow-50 text-yellow-800 border border-yellow-200";
        default:
          return "bg-blue-50 text-blue-800 border border-blue-200";
      }
    }
  },
  methods: {
    close() {
      this.visible = false;
      this.$emit("close");
      this.$emit("update:modelValue", false);
    }
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 200ms ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>