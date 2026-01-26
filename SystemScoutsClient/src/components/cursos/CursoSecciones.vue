<template>
  <div class="secciones-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Secciones del Curso</h4>
      
      <table class="fechas-table">
        <thead>
          <tr>
            <th>Sección</th>
            <th>Rama</th>
            <th>Participantes</th>
            <th v-if="!modoVer">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="localList.length === 0">
            <td :colspan="modoVer ? 3 : 4" class="no-results-small">No hay secciones definidas.</td>
          </tr>
          <tr v-for="(item, index) in localList" :key="item.CUS_ID || ('tmp-' + (item.__tmpId || index))">
            <td>{{ item.CUS_SECCION }}</td>
            <td>{{ getRamaName(item.RAM_ID) }}</td>
            <td>{{ item.CUS_CANT_PARTICIPANTE }}</td>
            <td v-if="!modoVer">
              <BaseButton @click="iniciarEdicion(index)" variant="secondary" size="sm">Modificar</BaseButton>
              <BaseButton @click="eliminar(index)" variant="danger" size="sm">Eliminar</BaseButton>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Formulario -->
      <div class="add-fecha-form" v-if="!modoVer">
        <div class="form-group">
          <label>Sección #</label>
          <InputBase type="number" v-model="form.CUS_SECCION" placeholder="Ej: 1, 2, 3..." />
        </div>
        <div class="form-group">
          <label>Rama</label>
          <BaseSelect v-model="form.RAM_ID" :options="ramasOptions" optionLabel="text" />
        </div>
        <div class="form-group">
          <label>Participantes</label>
          <InputBase type="number" v-model="form.CUS_CANT_PARTICIPANTE" placeholder="Cantidad" />
        </div>
        <BaseButton v-if="editIndex === null" @click="agregar" class="add-button">Añadir Sección</BaseButton>
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
  modelValue: { type: Array, default: () => [] },
  modoVer: { type: Boolean, default: false },
  ramasOptions: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:modelValue', 'show-alert'])

const localList = computed(() => props.modelValue)
const editIndex = ref(null)
const form = ref({
  CUS_SECCION: '',
  RAM_ID: null,
  CUS_CANT_PARTICIPANTE: ''
})

function getRamaName(id) {
  const r = props.ramasOptions.find(o => o.value === id)
  return r ? r.text : 'No definida'
}

function agregar() {
  if (!form.value.CUS_SECCION || !form.value.RAM_ID || !form.value.CUS_CANT_PARTICIPANTE) {
    emit('show-alert', { message: 'Complete todos los campos de la sección.', type: 'warning' })
    return
  }
  
  const nueva = { 
    ...form.value, 
    CUS_SECCION: Number(form.value.CUS_SECCION),
    RAM_ID: Number(form.value.RAM_ID),
    CUS_CANT_PARTICIPANTE: Number(form.value.CUS_CANT_PARTICIPANTE),
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
   if (!form.value.CUS_SECCION || !form.value.RAM_ID || !form.value.CUS_CANT_PARTICIPANTE) {
    emit('show-alert', { message: 'Complete todos los campos.', type: 'warning' })
    return
  }
  const newList = [...props.modelValue]
  newList[editIndex.value] = { ...form.value }
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
  form.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
}
</script>

<style scoped>
.secciones-section { margin-top: 1rem; }
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
