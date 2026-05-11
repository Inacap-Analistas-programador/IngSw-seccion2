<template>
  <div class="coordinadores-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Coordinadores del Curso</h4>
      
      <div class="table-responsive">
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Persona</th>
              <th>Cargo</th>
              <th v-if="!modoVer">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="localList.length === 0">
              <td :colspan="modoVer ? 2 : 3" class="no-results-small">Sin coordinadores</td>
            </tr>
            <tr v-for="(item, index) in localList" :key="item.CUC_ID || ('tmp-' + (item.__tmpId || index))">
              <td>{{ getPersonaName(item.PER_ID) }}</td>
              <td>{{ getCargoName(item.CAR_ID) }}</td>
              <td v-if="!modoVer">
                <div class="acciones-buttons">
                  <BaseButton @click="eliminar(index)" variant="danger" size="sm">Eliminar</BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Formulario -->
      <div class="add-fecha-form add-coordinador-form" v-if="!modoVer">
        <div class="form-group">
          <label>Persona</label>
          <FilterSelect v-model="form.PER_ID" :options="personasOptions" labelKey="text" valueKey="value" />
        </div>
        <div class="form-group">
          <label>Cargo</label>
          <FilterSelect v-model="form.CAR_ID" :options="cargosOptions" labelKey="text" valueKey="value" />
        </div>
        <BaseButton @click="agregar" class="add-button">Añadir Coordinador</BaseButton>
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
  cargosOptions: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:modelValue', 'show-alert'])

const localList = computed(() => props.modelValue)

const form = ref({
  PER_ID: null,
  CAR_ID: null
})

function getPersonaName(id) {
  const p = props.personasOptions.find(o => o.value === id)
  return p ? p.text : 'Desconocido'
}

function getCargoName(id) {
  const c = props.cargosOptions.find(o => o.value === id)
  return c ? c.text : '-'
}

function agregar() {
  if (!form.value.PER_ID) {
    emit('show-alert', { message: 'Debe seleccionar una persona.', type: 'warning' })
    return
  }
  
  const nueva = { 
    ...form.value,
    __tmpId: Date.now() 
  }
  
  const newList = [...props.modelValue, nueva]
  emit('update:modelValue', newList)
  
  // Reset form
  form.value = { PER_ID: null, CAR_ID: null }
}

function eliminar(index) {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
}
</script>

<style scoped>
.coordinadores-section { margin-top: 1rem; }
.section-divider { margin: 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.section-box h4 { margin-top: 0; color: #444; font-size: 1rem; margin-bottom: 1rem; }
.fechas-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9rem; }
.fechas-table th, .fechas-table td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #eee; }
.fechas-table th { background: #f9fafb; font-weight: 600; color: #555; }
.add-fecha-form { display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: end; background: #f8f9fa; padding: 1rem; border-radius: 8px; }
.add-button { height: 42px; }
.form-group { display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.8rem; color: #666; font-weight: 500; }
.no-results-small { text-align: center; color: #999; padding: 1rem; font-style: italic; }
</style>
