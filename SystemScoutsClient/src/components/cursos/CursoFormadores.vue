<template>
  <div class="formadores-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Equipo Formadores</h4>
      
      <div class="table-responsive">
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Persona</th>
              <th>Rol</th>
              <th>Sección</th>
              <th>Director</th>
              <th v-if="!modoVer">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="localList.length === 0">
              <td :colspan="modoVer ? 4 : 5" class="no-results-small">Sin formadores</td>
            </tr>
            <tr v-for="(item, index) in localList" :key="item.CUF_ID || ('tmp-' + (item.__tmpId || index))">
              <td>{{ getPersonaName(item.PER_ID) }}</td>
              <td>{{ getRolName(item.ROL_ID) }}</td>
              <td>{{ getSeccionName(item.CUS_ID) }}</td>
              <td>{{ item.CUO_DIRECTOR ? 'Sí' : 'No' }}</td>
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

      <!-- Formulario -->
      <div class="add-fecha-form add-formadores-form" v-if="!modoVer">
        <div class="form-group">
          <label>Persona</label>
          <FilterSelect v-model="form.PER_ID" :options="personasOptions" labelKey="text" valueKey="value" />
        </div>
        <div class="form-group">
          <label>Rol</label>
          <FilterSelect v-model="form.ROL_ID" :options="rolesOptions" labelKey="text" valueKey="value" />
        </div>
        <div class="form-group">
          <label>Sección</label>
          <FilterSelect v-model="form.CUS_ID" :options="seccionesOptions" labelKey="text" valueKey="value" />
        </div>
        <div class="form-group">
          <label>Director</label>
          <div style="height: 38px; display: flex; align-items: center;">
             <input type="checkbox" v-model="form.CUO_DIRECTOR" style="width:20px; height:20px;"/>
          </div>
        </div>
        <BaseButton v-if="editIndex === null" @click="agregar" class="add-button">Añadir Formador</BaseButton>
        <BaseButton v-if="editIndex !== null" @click="guardarEdicion" class="add-button" variant="primary">Guardar</BaseButton>
        <BaseButton v-if="editIndex !== null" @click="cancelarEdicion" class="add-button" variant="secondary">Cancelar</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  modoVer: { type: Boolean, default: false },
  personasOptions: { type: Array, default: () => [] },
  rolesOptions: { type: Array, default: () => [] },
  seccionesOptions: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:modelValue', 'show-alert'])

const localList = computed(() => props.modelValue)
const editIndex = ref(null)
const form = ref({
  PER_ID: null,
  ROL_ID: null,
  CUS_ID: null,
  CUO_DIRECTOR: false
})

function getPersonaName(id) {
  const p = props.personasOptions.find(o => o.value === id)
  return p ? p.text : 'Desconocido'
}

function getRolName(id) {
  const r = props.rolesOptions.find(o => o.value === id)
  return r ? r.text : '-'
}

function getSeccionName(id) {
  // Manejo de ID temporal o real
  if (!id) return '-'
  const s = props.seccionesOptions.find(o => o.value === id)
  return s ? s.text : '-'
}

function agregar() {
  if (!form.value.PER_ID || !form.value.ROL_ID) {
    emit('show-alert', { message: 'Completa persona y rol.', type: 'warning' })
    return
  }
  
  const nueva = { 
    ...form.value, 
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
  if (!form.value.PER_ID || !form.value.ROL_ID) {
    emit('show-alert', { message: 'Completa persona y rol.', type: 'warning' })
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
  form.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
}
</script>

<style scoped>
.formadores-section { margin-top: 1rem; }
.section-divider { margin: 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.section-box h4 { margin-top: 0; color: #444; font-size: 1rem; margin-bottom: 1rem; }
.fechas-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9rem; }
.fechas-table th, .fechas-table td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #eee; }
.fechas-table th { background: #f9fafb; font-weight: 600; color: #555; }
.add-fecha-form { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr auto; gap: 1rem; align-items: end; background: #f8f9fa; padding: 1rem; border-radius: 8px; }
.add-button { height: 42px; }
.form-group { display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.8rem; color: #666; font-weight: 500; }
.no-results-small { text-align: center; color: #999; padding: 1rem; font-style: italic; }
</style>
