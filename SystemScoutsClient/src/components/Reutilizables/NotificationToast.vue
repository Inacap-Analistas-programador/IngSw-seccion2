<template>
  <div class="notification-toast" role="status">
    <AppIcons v-if="icon" :name="icon" :size="18" />
    <div class="message">{{ message }}</div>
    <button class="close" @click="$emit('close')">
      <AppIcons name="x" :size="16" />
    </button>
  </div>
</template>

<script>
import AppIcons from '@/components/icons/AppIcons.vue'

export default {
  name: 'NotificationToast',
  components: { AppIcons },
  props: {
    message: { type: String, required: true },
    icon: { type: String, default: '' }
  }
}
</script>

<style scoped>
.notification-toast { position: fixed; bottom: 20px; right: 20px; background: #2c5aa0; color: white; padding: 10px 14px; border-radius: 6px; display:flex; gap:8px; align-items:center }
.notification-toast .close { background: transparent; border: none; color: white; cursor: pointer }
</style>
