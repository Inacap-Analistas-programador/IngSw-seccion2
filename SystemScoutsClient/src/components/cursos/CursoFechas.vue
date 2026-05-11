<template>
  <div class="fechas-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Períodos del Curso</h4>
      
      <!-- Tabla de Fechas Existentes -->
      <div class="table-responsive">
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Inicio</th>
              <th>Término</th>
              <th>Tipo</th>
              <th v-if="!modoVer">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="localFechas.length === 0">
              <td :colspan="modoVer ? 3 : 4" class="no-results-small">No hay períodos definidos.</td>
            </tr>
            <tr v-for="(fecha, index) in localFechas" :key="fecha.CUF_ID || ('tmp-' + (fecha.__tmpId || index))">
              <td>{{ formatDateSimple(fecha.CUF_FECHA_INICIO) }}</td>
              <td>{{ formatDateSimple(fecha.CUF_FECHA_TERMINO) }}</td>
              <td>{{ getTipoFechaText(fecha.CUF_TIPO) }}</td>
              <td v-if="!modoVer">
                <div class="acciones-buttons">
                  <BaseButton @click="iniciarEdicion(index)" variant="secondary" size="sm">Modificar</BaseButton>
                  <BaseButton @click="eliminar(index)" variant="danger" size="sm">Eliminar</BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Formulario para Añadir Nueva Fecha -->
      <div class="add-fecha-form" v-if="!modoVer">
        <div class="form-group">
          <label>Fecha Inicio</label>
          <InputBase type="date" v-model="form.CUF_FECHA_INICIO" />
        </div>
        <div class="form-group">
          <label>Fecha Término</label>
          <InputBase type="date" v-model="form.CUF_FECHA_TERMINO" />
        </div>
        <div class="form-group">
          <label>Tipo</label>
          <FilterSelect v-model="form.CUF_TIPO" :options="opcionesTipoFecha" labelKey="text" valueKey="value" />
        </div>
        <BaseButton v-if="editIndex === null" @click="agregar" class="add-button">Añadir Período</BaseButton>
        <BaseButton v-if="editIndex !== null" @click="guardarEdicion" class="add-button" variant="primary">Guardar</BaseButton>
        <BaseButton v-if="editIndex !== null" @click="cancelarEdicion" class="add-button" variant="secondary">Cancelar</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import InputBase from '@/components/InputBase.vue'
import BaseButton from '@/components/BaseButton.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  modoVer: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'show-alert'])

// Local copy for display
const localFechas = computed(() => props.modelValue)

const editIndex = ref(null)

const form = ref({
  CUF_FECHA_INICIO: '',
  CUF_FECHA_TERMINO: '',
  CUF_TIPO: 1,
})

const opcionesTipoFecha = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]

function getTipoFechaText(val) {
  return opcionesTipoFecha.find(o => o.value === Number(val))?.text || 'Desconocido'
}

function formatDateSimple(dateStr) {
  if (!dateStr) return '?'
  // Asegurar formato YYYY-MM-DD para compatibilidad
  const d = new Date(dateStr)
  // Ajuste de zona horaria simple para visualización correcta de fechas ingresadas manualmente
  const userTimezoneOffset = d.getTimezoneOffset() * 60000
  const adjustedDate = new Date(d.getTime() + userTimezoneOffset)
  return adjustedDate.toLocaleDateString('es-CL', { year: 'numeric', month: 'short', day: 'numeric' })
}

function agregar() {
  if (!form.value.CUF_FECHA_INICIO || !form.value.CUF_FECHA_TERMINO) {
    emit('show-alert', { message: 'Debe seleccionar fecha de inicio y término.', type: 'warning' })
    return
  }
  if (new Date(form.value.CUF_FECHA_TERMINO) < new Date(form.value.CUF_FECHA_INICIO)) {
    emit('show-alert', { message: 'La fecha de término no puede ser anterior al inicio.', type: 'warning' })
    return
  }

  // Copia nueva referencia
  const nueva = { ...form.value, __tmpId: Date.now() }
  
  // Update parent
  const newList = [...props.modelValue, nueva]
  emit('update:modelValue', newList)

  // Reset
  form.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
}

function iniciarEdicion(index) {
  editIndex.value = index
  form.value = { ...props.modelValue[index] }
}

function guardarEdicion() {
    if (!form.value.CUF_FECHA_INICIO || !form.value.CUF_FECHA_TERMINO) {
    emit('show-alert', { message: 'Debe seleccionar fecha de inicio y término.', type: 'warning' })
    return
  }
  
  const newList = [...props.modelValue]
  newList[editIndex.value] = { ...form.value }
  
  emit('update:modelValue', newList)
  cancelarEdicion()
}

// function cancelerEdicion removed


function eliminar(index) {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
}

function cancelarEdicion() {
  editIndex.value = null
  form.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
}
</script>

<style scoped>
.fechas-section { margin-top: 1rem; }
.section-divider { margin: 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.section-box h4 { margin-top: 0; color: #444; font-size: 1rem; margin-bottom: 1rem; }
.fechas-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9rem; }
.fechas-table th, .fechas-table td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #eee; }
.fechas-table th { background: #f9fafb; font-weight: 600; color: #555; }
.add-fecha-form { display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 1rem; align-items: end; background: #f8f9fa; padding: 1rem; border-radius: 8px; }
.add-button { height: 42px; }
.form-group { display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.8rem; color: #666; font-weight: 500; }
.no-results-small { text-align: center; color: #999; padding: 1rem; font-style: italic; }
</style>
