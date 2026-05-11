<template>
  <Transition name="toast">
    <div class="notification-toast" role="status" :class="type">
      <AppIcons v-if="icon" :name="icon" :size="18" />
      <div class="message">{{ message }}</div>
      <button class="close" @click="$emit('close')">
        <AppIcons name="x" :size="16" />
      </button>
    </div>
  </Transition>
</template>

<script>
import AppIcons from '@/components/icons/AppIcons.vue'

export default {
  name: 'NotificationToast',
  components: { AppIcons },
  props: {
    message: { type: String, required: true },
    type: { type: String, default: 'info' }, // success, error, info
    icon: { type: String, default: '' }
  }
}
</script>

<style scoped>
.notification-toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #2c5aa0; /* Default fallback */
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  gap: 12px;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
  max-width: 350px;
  opacity: 1; /* Force opacity */
}

.notification-toast.info { background-color: #2c5aa0 !important; }
.notification-toast.success { background-color: #2e7d32 !important; }
.notification-toast.error { background-color: #c62828 !important; }

.notification-toast .message {
  font-size: 0.95rem;
  line-height: 1.4;
}

.notification-toast .close {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.notification-toast .close:hover {
  opacity: 1;
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 768px) {
  .notification-toast {
    right: 50%;
    transform: translateX(50%);
    bottom: 80px; /* Above bottom nav layout if exists, or just spaced from bottom */
    width: 90%;
    justify-content: space-between;
  }

  /* Transition overrides for mobile centering */
  .toast-enter-from,
  .toast-leave-to {
    transform: translate(50%, 20px); /* Keep centered X, move down Y */
  }
  

}
</style>
