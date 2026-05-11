<template>
  <div class="page-header">
    <h3>{{ title }}</h3>
    <p v-if="subtitle">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
  font-family: 'Inter', Arial, sans-serif;
}

.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin: 4px 0 0;
}
</style>
