<template>
  <div class="search-box">
    <input 
      type="text" 
      class="search-input-new" 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      @keyup.enter="$emit('search')"
    >
    <button class="search-btn-new" @click="$emit('search')" title="Buscar">
      <AppIcons name="search" :size="16" />
    </button>
  </div>
</template>

<script setup>
import AppIcons from '@/components/icons/AppIcons.vue'

defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Buscar...'
  }
})

defineEmits(['update:modelValue', 'search'])
</script>

<style scoped>
.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0 4px 0 12px;
  height: 40px;
  flex: 1;
  transition: all 0.2s;
  box-sizing: border-box;
}

.search-box:focus-within {
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.search-input-new {
  flex: 1;
  border: none !important;
  outline: none !important;
  padding: 8px 0 !important;
  font-size: 0.95rem !important;
  color: #111827 !important;
  background: transparent !important;
}

.search-btn-new {
  background: transparent !important;
  border: none !important;
  color: #6b7280;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: color 0.2s;
  height: 32px;
  width: 32px;
  margin-right: 4px;
}

.search-btn-new:hover {
  color: #1a237e;
}

.search-btn-new :deep(svg) {
  margin-right: 0 !important;
}

@media (max-width: 768px) {
  .search-box { width: 100%; flex: none; }
}
</style>
