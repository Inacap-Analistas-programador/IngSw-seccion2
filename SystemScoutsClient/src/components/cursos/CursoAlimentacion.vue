<template>
  <div class="alimentacion-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Cuotas y Alimentación</h4>
      
      <!-- Campos de Cuota Global -->
      <div class="cuotas-grid">
        <div class="form-group">
          <label>Cuota con Almuerzo</label>
          <InputBase type="number" :modelValue="cuotaCon" @update:modelValue="$emit('update:cuotaCon', $event)" />
          <small class="field-hint">Monto en CLP, ej: 15000</small>
        </div>
        <div class="form-group">
          <label>Cuota sin Almuerzo</label>
          <InputBase type="number" :modelValue="cuotaSin" @update:modelValue="$emit('update:cuotaSin', $event)" />
          <small class="field-hint">Monto en CLP, ej: 10000</small>
        </div>
        <div class="form-group" v-if="!modoVer">
           <label></label>
        </div>
      </div>
      
      <!-- Tabla Alimentación -->
      <table class="fechas-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Tiempo</th>
            <th>Tipo Alimentación</th>
            <th>Descripción</th>
            <th>Adic.</th>
            <th v-if="!modoVer">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="localList.length === 0">
            <td :colspan="modoVer ? 5 : 6" class="no-results-small">Sin alimentación</td>
          </tr>
          <tr v-for="(item, index) in localList" :key="item.CUA_ID || ('tmp-' + (item.__tmpId || index))">
            <td>{{ formatDateSimple(item.CUA_FECHA) }}</td>
            <td>{{ getTiempoText(item.CUA_TIEMPO) }}</td>
            <td>{{ getAlimentacionText(item.ALI_ID) }}</td>
            <td>{{ item.CUA_DESCRIPCION }}</td>
            <td>{{ item.CUA_CANTIDAD_ADICIONAL }}</td>
            <td v-if="!modoVer">
              <BaseButton @click="iniciarEdicion(index)" variant="secondary" size="sm">Modificar</BaseButton>
              <BaseButton @click="eliminar(index)" variant="danger" size="sm">Eliminar</BaseButton>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Formulario -->
      <div class="add-fecha-form add-alimentacion-form" v-if="!modoVer">
        <div class="form-group">
          <label>Fecha</label>
          <InputBase type="date" v-model="form.CUA_FECHA" />
        </div>
        <div class="form-group">
          <label>Tiempo</label>
          <BaseSelect v-model="form.CUA_TIEMPO" :options="tiempoAlimentacionOptions" optionLabel="text" />
        </div>
        <div class="form-group">
          <label>Tipo</label>
          <BaseSelect v-model="form.ALI_ID" :options="alimentacionOptions" optionLabel="text" />
        </div>
        <div class="form-group">
          <label>Descripción</label>
          <InputBase v-model="form.CUA_DESCRIPCION" />
        </div>
        <div class="form-group">
          <label>Adicional</label>
          <InputBase type="number" v-model="form.CUA_CANTIDAD_ADICIONAL" />
        </div>
        <BaseButton v-if="editIndex === null" @click="agregar" class="add-button">Añadir</BaseButton>
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
import BaseSelect from '@/components/BaseSelect.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] }, // Lista de alimentaciones
  modoVer: { type: Boolean, default: false },
  alimentacionOptions: { type: Array, default: () => [] },
  cuotaCon: { type: [Number, String], default: null },
  cuotaSin: { type: [Number, String], default: null },
})

const emit = defineEmits(['update:modelValue', 'update:cuotaCon', 'update:cuotaSin', 'show-alert'])

const localList = computed(() => props.modelValue)
const editIndex = ref(null)

const tiempoAlimentacionOptions = [
  { value: 1, text: 'Desayuno' },
  { value: 2, text: 'Almuerzo' },
  { value: 3, text: 'Once' },
  { value: 4, text: 'Cena' },
  { value: 5, text: 'Colación' },
]

const form = ref({
  ALI_ID: null,
  CUA_FECHA: '',
  CUA_TIEMPO: null,
  CUA_DESCRIPCION: '',
  CUA_CANTIDAD_ADICIONAL: 0
})

function getTiempoText(val) {
  return tiempoAlimentacionOptions.find(o => o.value === Number(val))?.text || '-'
}

function getAlimentacionText(id) {
  const a = props.alimentacionOptions.find(o => o.value === id)
  return a ? a.text : '-'
}

function formatDateSimple(dateStr) {
  if (!dateStr) return '?'
  const d = new Date(dateStr)
  // Ajuste zona horaria visual
  const userTimezoneOffset = d.getTimezoneOffset() * 60000
  const adjustedDate = new Date(d.getTime() + userTimezoneOffset)
  return adjustedDate.toLocaleDateString('es-CL', { year: 'numeric', month: 'short', day: 'numeric' })
}

function agregar() {
  if (!form.value.CUA_FECHA || !form.value.CUA_TIEMPO || !form.value.ALI_ID) {
    emit('show-alert', { message: 'Debe completar fecha, tiempo y tipo.', type: 'warning' })
    return
  }
  
  const nueva = { 
    ...form.value, 
    CUA_CANTIDAD_ADICIONAL: Number(form.value.CUA_CANTIDAD_ADICIONAL || 0),
    __tmpId: Date.now() 
  }
  
  const newList = [...props.modelValue, nueva]
  emit('update:modelValue', newList)
  resetForm()
}

function iniciarEdicion(index) {
  editIndex.value = index
  form.value = { ...props.modelValue[index] }
}

function guardarEdicion() {
  if (!form.value.CUA_FECHA || !form.value.CUA_TIEMPO || !form.value.ALI_ID) {
    emit('show-alert', { message: 'Debe completar fecha, tiempo y tipo.', type: 'warning' })
    return
  }
  const newList = [...props.modelValue]
  newList[editIndex.value] = { ...form.value, CUA_CANTIDAD_ADICIONAL: Number(form.value.CUA_CANTIDAD_ADICIONAL) }
  emit('update:modelValue', newList)
  resetForm()
}

function eliminar(index) {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
}

function cancelarEdicion() {
  resetForm()
}

function resetForm() {
  editIndex.value = null
  form.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
}
</script>

<style scoped>
.alimentacion-section { margin-top: 1rem; }
.section-divider { margin: 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.section-box h4 { margin-top: 0; color: #444; font-size: 1rem; margin-bottom: 1rem; }
.fechas-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9rem; }
.fechas-table th, .fechas-table td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #eee; }
.fechas-table th { background: #f9fafb; font-weight: 600; color: #555; }
.add-fecha-form { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto; gap: 1rem; align-items: end; background: #f8f9fa; padding: 1rem; border-radius: 8px; }
.add-button { height: 42px; }
.form-group { display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.8rem; color: #666; font-weight: 500; }
.no-results-small { text-align: center; color: #999; padding: 1rem; font-style: italic; }
.cuotas-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
</style>
