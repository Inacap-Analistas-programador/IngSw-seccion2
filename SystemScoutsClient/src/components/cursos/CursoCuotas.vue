<template>
  <div class="cuotas-section">
    <hr class="section-divider">
    <div class="section-box">
      <h4>Cuotas del Curso</h4>
      
      <div class="table-responsive">
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Fecha</th>
              <th>Monto</th>
              <th v-if="!modoVer">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="localList.length === 0">
              <td :colspan="modoVer ? 3 : 4" class="no-results-small">Sin cuotas</td>
            </tr>
            <tr v-for="(item, index) in localList" :key="item.CUU_ID || ('tmp-' + (item.__tmpId || index))">
              <td>{{ item.CUU_TIPO === 1 ? 'Con Almuerzo' : 'Sin Almuerzo' }}</td>
              <td>{{ formatDateSimple(item.CUU_FECHA) }}</td>
              <td>${{ item.CUU_VALOR }}</td>
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
      <div class="add-fecha-form add-cuota-form" v-if="!modoVer">
        <div class="form-group">
          <label>Tipo</label>
          <FilterSelect v-model="form.CUU_TIPO" :options="[{value:1,text:'Con Almuerzo'},{value:2,text:'Sin Almuerzo'}]" labelKey="text" valueKey="value" />
        </div>
        <div class="form-group">
          <label>Fecha</label>
          <InputBase type="date" v-model="form.CUU_FECHA" />
        </div>
        <div class="form-group">
          <label>Monto</label>
          <InputBase type="number" v-model="form.CUU_VALOR" placeholder="15000" />
        </div>
        <BaseButton @click="agregar" class="add-button">Añadir Cuota</BaseButton>
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
  modelValue: { type: Array, default: () => [] },
  modoVer: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'show-alert'])

const localList = computed(() => props.modelValue)

const form = ref({
  CUU_TIPO: 1,
  CUU_FECHA: '',
  CUU_VALOR: ''
})

function formatDateSimple(dateStr) {
  if (!dateStr) return '?'
  const d = new Date(dateStr)
  // Ajuste zona horaria visual
  const userTimezoneOffset = d.getTimezoneOffset() * 60000
  const adjustedDate = new Date(d.getTime() + userTimezoneOffset)
  return adjustedDate.toLocaleDateString('es-CL', { year: 'numeric', month: 'short', day: 'numeric' })
}

function agregar() {
  if (!form.value.CUU_FECHA || !form.value.CUU_VALOR) {
    emit('show-alert', { message: 'Debe completar fecha y monto.', type: 'warning' })
    return
  }
  
  const nueva = { 
    ...form.value,
    CUU_TIPO: Number(form.value.CUU_TIPO),
    CUU_VALOR: Number(form.value.CUU_VALOR),
    __tmpId: Date.now() 
  }
  
  const newList = [...props.modelValue, nueva]
  emit('update:modelValue', newList)
  
  // Reset form partial (keep type maybe?)
  form.value.CUU_FECHA = ''
  form.value.CUU_VALOR = ''
}

function eliminar(index) {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
}
</script>

<style scoped>
.cuotas-section { margin-top: 1rem; }
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
