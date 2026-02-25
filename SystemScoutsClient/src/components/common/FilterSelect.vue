<template>
  <div class="custom-select-container" ref="containerRef">
    <div 
      class="custom-select-trigger" 
      @click="toggleDropdown" 
      :class="{ 'active': isOpen, 'disabled': disabled }"
    >
      <span v-if="!isOpen">{{ displayedLabel }}</span>
      <div class="custom-arrow" :class="{ 'open': isOpen }">▼</div>
    </div>
    <div v-if="isOpen" class="custom-options">
      <div 
        v-for="option in options" 
        :key="option[valueKey]" 
        class="custom-option"
        :class="{ 'selected': modelValue == option[valueKey] }"
        @click="selectOption(option[valueKey])"
      >
        {{ option[labelKey] }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  defaultLabel: {
    type: String,
    default: 'Seleccionar'
  },
  valueKey: {
    type: String,
    default: 'id'
  },
  labelKey: {
    type: String,
    default: 'descripcion'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const modelValue = defineModel()

const isOpen = ref(false)
const containerRef = ref(null)

const hasValue = computed(() => {
  return modelValue.value !== '' && modelValue.value !== null && modelValue.value !== undefined
})

const displayedLabel = computed(() => {
  if (!hasValue.value) return props.defaultLabel
  const found = props.options.find(opt => opt[props.valueKey] == modelValue.value)
  return found ? found[props.labelKey] : props.defaultLabel
})

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
}

const selectOption = (id) => {
  modelValue.value = id
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.custom-select-container {
  position: relative;
  width: 100%;
  max-width: 280px;
  height: 40px;
  font-family: 'Inter', Arial, sans-serif;
  box-sizing: border-box;
}

.custom-select-trigger {
  width: 100%;
  height: 100%;
  padding: 0 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
  box-sizing: border-box;
}

.custom-select-trigger:hover {
  border-color: #9ca3af;
}

.custom-select-trigger.active {
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.custom-select-trigger.disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
  border-color: #e5e7eb;
}

.custom-arrow {
  font-size: 0.8rem;
  color: #6b7280;
  transition: transform 0.2s;
}

.custom-arrow.open {
  transform: rotate(180deg);
}

.custom-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-top: 4px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 50;
  max-height: 300px;
  overflow-y: auto;
}

.custom-option {
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s;
  color: #374151;
  font-size: 0.95rem;
}

.custom-option:hover {
  background-color: #f3f4f6;
}

.custom-option.selected {
  background-color: #e8eaf6;
  color: #1a237e;
  font-weight: 500;
}

@media (max-width: 768px) {
  .custom-select-container { 
    max-width: 100%; 
    width: 100%;
  }
}
</style>