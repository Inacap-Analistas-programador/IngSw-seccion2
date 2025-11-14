<template>
  <div class="base-select">
    <!-- Etiqueta del select -->
    <label v-if="label" :for="id" class="base-select__label">
      {{ label }}
      <span v-if="required" class="base-select__required">*</span>
    </label>
    
    <!-- Elemento select -->
    <select
      :id="id"
      :value="modelValue"
      @change="handleChange"
      :disabled="disabled"
      :class="[
        'base-select__element',
        { 
          'base-select__element--error': error,
          'base-select__element--disabled': disabled
        }
      ]"
    >
      <!-- Opción por defecto -->
      <option v-if="placeholder" value="" disabled>
        {{ placeholder }}
      </option>
      
      <!-- Opciones dinámicas -->
      <option
        v-for="option in options"
        :key="getOptionValue(option)"
        :value="getOptionValue(option)"
        :disabled="getOptionDisabled(option)"
      >
        {{ getOptionLabel(option) }}
      </option>
    </select>
    
    <!-- Mensaje de error -->
    <div v-if="error" class="base-select__error">
      {{ error }}
    </div>
    
    <!-- Texto de ayuda -->
    <div v-if="helpText" class="base-select__help">
      {{ helpText }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseSelect',
  props: {
    // Valor seleccionado (v-model)
    modelValue: {
      type: [String, Number, Boolean, Object],
      default: ''
    },
    // Array de opciones
    options: {
      type: Array,
      required: true,
      default: () => []
    },
    // Texto de la etiqueta
    label: {
      type: String,
      default: ''
    },
    // Placeholder
    placeholder: {
      type: String,
      default: 'Seleccione una opción'
    },
    // ID único para el select
    id: {
      type: String,
      default: () => `select-${Math.random().toString(36).substr(2, 9)}`
    },
    // Si el campo es requerido
    required: {
      type: Boolean,
      default: false
    },
    // Si está deshabilitado
    disabled: {
      type: Boolean,
      default: false
    },
    // Mensaje de error
    error: {
      type: String,
      default: ''
    },
    // Texto de ayuda
    helpText: {
      type: String,
      default: ''
    },
    // Key para el valor de la opción (cuando options es array de objetos)
    optionValue: {
      type: String,
      default: 'value'
    },
    // Key para el label de la opción (cuando options es array de objetos)
    optionLabel: {
      type: String,
      default: 'label'
    },
    // Key para determinar si la opción está deshabilitada
    optionDisabled: {
      type: String,
      default: 'disabled'
    }
  },
  emits: ['update:modelValue', 'change'],
  methods: {
    // Manejar cambio de selección
    handleChange(event) {
      const value = event.target.value;
      this.$emit('update:modelValue', value);
      this.$emit('change', value);
    },
    
    // Obtener valor de la opción
    getOptionValue(option) {
      if (typeof option === 'object') {
        return option[this.optionValue];
      }
      return option;
    },
    
    // Obtener label de la opción
    getOptionLabel(option) {
      if (typeof option === 'object') {
        return option[this.optionLabel];
      }
      return option;
    },
    
    // Determinar si la opción está deshabilitada
    getOptionDisabled(option) {
      if (typeof option === 'object') {
        return option[this.optionDisabled] || false;
      }
      return false;
    }
  }
}
</script>

<style scoped>
.base-select {
  margin-bottom: 0; /* Para alineación uniforme en grilla de filtros */
  text-align: left;
}

.base-select__label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
  font-size: 0.9rem;
}

.base-select__required {
  color: #e74c3c;
}

.base-select__element {
  width: 100%;
  padding: 0.55rem 0.65rem; /* Altura más cercana al InputBase */
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background-color: var(--color-surface);
  color: var(--color-text);
  font-size: 0.85rem;
  transition: background-color .15s ease, border-color .15s ease, box-shadow .15s ease;
  outline: none;
  line-height: 1.2;
}

.base-select__element:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}

.base-select__element--error {
  border-color: #e74c3c;
}

.base-select__element--error:focus {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.base-select__element--disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.base-select__error {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.base-select__help {
  color: #6c757d;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}
</style>