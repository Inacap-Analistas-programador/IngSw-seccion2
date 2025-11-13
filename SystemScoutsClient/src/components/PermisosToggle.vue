<template>
  <div class="permisos-toggle">
    <div class="permiso-header">
      <div class="permiso-info">
        <AppIcons :name="iconName" :size="20" class="permiso-icon" />
        <div class="permiso-text">
          <span class="permiso-nombre">{{ label }}</span>
          <span class="permiso-descripcion">{{ description }}</span>
        </div>
      </div>
      <button 
        type="button"
        class="toggle-button" 
        :class="{ 'active': modelValue, 'disabled': disabled }"
        @click="toggle"
        :disabled="disabled"
      >
        <span class="toggle-slider"></span>
      </button>
    </div>
  </div>
</template>

<script>
import AppIcons from '@/components/icons/AppIcons.vue'


export default {
  name: 'PermisosToggle',
  components: {
    AppIcons
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: ''
    },
    iconName: {
      type: String,
      default: 'unlock'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  methods: {
    toggle() {
      if (!this.disabled) {
        this.$emit('update:modelValue', !this.modelValue)
      }
    }
  }
}
</script>

<style scoped>
.permisos-toggle {
  width: 100%;
}

.permiso-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  transition: all 0.2s;
  min-height: 70px;
}

.permiso-header:hover {
  background: #e8f4f8;
  border-color: #3498db;
}

.permiso-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.permiso-icon {
  color: #7f8c8d;
  margin-top: 2px;
  flex-shrink: 0;
}

.permiso-text {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.permiso-nombre {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.permiso-descripcion {
  font-size: 0.875rem;
  color: #7f8c8d;
  line-height: 1.4;
}

/* Toggle Button Styles */
.toggle-button {
  position: relative;
  width: 44px;
  height: 24px;
  background: #95a5a6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.toggle-button:hover:not(.disabled) {
  background: #7f8c8d;
}

.toggle-button.active {
  background: #27ae60;
}

.toggle-button.active:hover:not(.disabled) {
  background: #229954;
}

.toggle-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-button.active .toggle-slider {
  transform: translateX(20px);
}
</style>
