<template>
  <tr class="data-row" :class="{ 'selected': isSelected }">
    <td v-if="selectable" class="select-cell">
      <InputBase
        type="checkbox"
        :modelValue="isSelected"
        @update:modelValue="$emit('selectionChange', $event)"
      />
    </td>
    
    <td
      v-for="(value, key) in filteredData"
      :key="key"
      class="data-cell"
      @click="$emit('cellClick', { field: key, value: value, row: rowData })"
    >
      <template v-if="editableFields.includes(key) && isEditing">
        <InputBase
          :type="getInputType(key)"
          :modelValue="editedData[key]"
          @update:modelValue="handleFieldUpdate(key, $event)"
          :placeholder="`Editar ${getFieldLabel(key)}`"
        />
      </template>
      <template v-else>
        {{ formatValue(value, key) }}
      </template>
    </td>
    
    <td v-if="hasActions" class="actions-cell">
      <BaseButton
        v-if="editable && !isEditing"
        size="small"
        variant="outline"
        @click="enableEditing"
      >
        Editar
      </BaseButton>
      
      <BaseButton
        v-if="editable && isEditing"
        size="small"
        variant="success"
        @click="saveChanges"
        :loading="saving"
      >
        Guardar
      </BaseButton>
      
      <BaseButton
        v-if="editable && isEditing"
        size="small"
        variant="secondary"
        @click="cancelEditing"
        :disabled="saving"
      >
        Cancelar
      </BaseButton>
      
      <BaseButton
        v-if="deletable"
        size="small"
        variant="danger"
        @click="$emit('delete', rowData.id)"
        :loading="deleting"
      >
        Eliminar
      </BaseButton>
    </td>
  </tr>
</template>

<script setup>
import { ref, computed } from 'vue'
import InputBase from './InputBase.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  rowData: {
    type: Object,
    required: true
  },
  fields: {
    type: Array,
    default: () => []
  },
  selectable: {
    type: Boolean,
    default: false
  },
  selected: {
    type: Boolean,
    default: false
  },
  editable: {
    type: Boolean,
    default: false
  },
  deletable: {
    type: Boolean,
    default: false
  },
  editableFields: {
    type: Array,
    default: () => []
  },
  fieldLabels: {
    type: Object,
    default: () => ({})
  },
  fieldTypes: {
    type: Object,
    default: () => ({})
  },
  saving: {
    type: Boolean,
    default: false
  },
  deleting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update',
  'delete',
  'selectionChange',
  'cellClick'
])

const isEditing = ref(false)
const editedData = ref({...props.rowData})

// Computed properties
const filteredData = computed(() => {
  if (props.fields.length === 0) {
    return props.rowData
  }
  const filtered = {}
  props.fields.forEach(field => {
    if (props.rowData.hasOwnProperty(field)) {
      filtered[field] = props.rowData[field]
    }
  })
  return filtered
})

const hasActions = computed(() => props.editable || props.deletable)
const isSelected = computed(() => props.selected)

// Methods
const enableEditing = () => {
  editedData.value = {...props.rowData}
  isEditing.value = true
}

const cancelEditing = () => {
  editedData.value = {...props.rowData}
  isEditing.value = false
}

const saveChanges = async () => {
  try {
    await emit('update', {
      id: props.rowData.id,
      data: editedData.value
    })
    isEditing.value = false
  } catch (error) {
    console.error('Error al guardar cambios:', error)
  }
}

const handleFieldUpdate = (field, value) => {
  editedData.value[field] = value
}

const getInputType = (field) => {
  return props.fieldTypes[field] || 'text'
}

const getFieldLabel = (field) => {
  return props.fieldLabels[field] || field
}

const formatValue = (value, field) => {
  if (value === null || value === undefined) return '-'
  
  // Formato para fechas
  if (field.includes('fecha') || field.includes('date')) {
    return new Date(value).toLocaleDateString('es-CL')
  }
  
  // Formato para booleanos
  if (typeof value === 'boolean') {
    return value ? 'Sí' : 'No'
  }
  
  return value
}
</script>

<style scoped>
.data-row {
  transition: background-color 0.2s ease;
}

.data-row:hover {
  background-color: #f8f9fa;
}

.data-row.selected {
  background-color: #e3f2fd;
}

.data-cell {
  padding: 12px 8px;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
}

.select-cell {
  width: 40px;
  text-align: center;
}

.actions-cell {
  width: 200px;
  text-align: center;
  white-space: nowrap;
}

.actions-cell button {
  margin: 0 2px;
}
</style>