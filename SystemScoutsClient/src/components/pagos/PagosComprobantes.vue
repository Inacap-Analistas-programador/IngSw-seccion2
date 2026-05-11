<template>
  <section class="panel panel-box">
    <div class="panel-title">
      <h3>Generación de Comprobantes</h3>
      <p>Filtra los pagos y genera un comprobante en formato PDF.</p>
    </div>

    <!-- Filtros para Comprobantes -->
    <div class="grid grid-comprobantes">
      <div class="col">
        <label>Tipo de Comprobante</label>
        <BaseSelect v-model="form.tipo" :options="[{value: 'ingreso', label: 'Ingreso'}, {value: 'egreso', label: 'Egreso'}]" />
      </div>
      <div class="col">
        <label>Concepto</label>
        <BaseSelect v-model="form.COC_ID" :options="conceptosOptions" placeholder="Todos los conceptos" />
      </div>
      <div class="col">
        <label>Curso</label>
        <BaseSelect v-model="form.CUR_ID" :options="cursoOptions" placeholder="Todos los cursos" />
      </div>
      <div class="col">
        <label>Grupo</label>
        <BaseSelect v-model="form.GRU_ID" :options="grupoOptions" placeholder="Todos los grupos" />
      </div>
      <div class="col">
        <label>Fecha Desde</label>
        <InputBase type="date" v-model="form.fechaDesde" />
      </div>
      <div class="col">
        <label>Fecha Hasta</label>
        <InputBase type="date" v-model="form.fechaHasta" />
      </div>
      <div class="col auto">
        <label class="invisible">Buscar</label>
        <BaseButton class="btn-standard" variant="primary" @click="buscar" :disabled="loading">
          <AppIcons name="search" :size="16" /> {{ loading ? 'Buscando...' : 'Buscar Pagos' }}
        </BaseButton>
      </div>
    </div>

    <!-- Tabla de resultados para comprobantes -->
    <div v-if="buscado" class="lista" style="margin-top: 20px;">
      <div class="lista-header">
        <h5>Pagos Encontrados ({{ pagos.length }})</h5>
        <div class="acciones">
          <BaseButton size="sm" variant="secondary" @click="toggleSelectAll(true)">Seleccionar todos</BaseButton>
          <BaseButton size="sm" variant="secondary" @click="toggleSelectAll(false)">Deseleccionar</BaseButton>
        </div>
      </div>
      <div class="table-container" style="max-height: 300px;">
        <table class="courses-table">
          <thead>
            <tr>
              <th style="width: 32px;"><input type="checkbox" @change="toggleSelectAll($event.target.checked)" /></th>
              <th>Nombre</th>
              <th>Concepto</th>
              <th>Monto</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading"><td colspan="5" class="placeholder">Cargando...</td></tr>
            <tr v-else-if="!pagos.length"><td colspan="5" class="placeholder">No se encontraron pagos con esos filtros.</td></tr>
            <tr v-for="p in pagos" :key="p.PAP_ID">
              <td><input type="checkbox" :value="p.PAP_ID" v-model="seleccionados" /></td>
              <td data-label="Nombre">{{ p.persona_nombre }}</td>
              <td data-label="Concepto">{{ p.concepto_descripcion }}</td>
              <td data-label="Monto">${{ (p.PAP_MONTO || 0).toLocaleString('es-CL') }}</td>
              <td data-label="Fecha">{{ dateCL(p.PAP_FECHA_PAGO) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Acciones para comprobantes -->
    <div v-if="seleccionados.length" class="acciones center" style="margin-top: 20px;">
      <div class="resumen" style="margin-bottom: 10px;">
        <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
        <div class="total">Total: <strong>${{ totalSeleccionado.toLocaleString('es-CL') }}</strong></div>
      </div>
      <BaseButton variant="success" class="btn-standard" @click="generarPDF">
        <AppIcons name="download" :size="16" /> Generar Comprobante PDF
      </BaseButton>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import BaseSelect from '@/components/BaseSelect.vue';
import BaseButton from '@/components/BaseButton.vue';
import InputBase from '@/components/InputBase.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import pagosService from '@/services/pagosService.js';
import { format, parseISO } from 'date-fns';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

const props = defineProps({
  cursoOptions: { type: Array, default: () => [] },
  grupoOptions: { type: Array, default: () => [] },
  conceptosOptions: { type: Array, default: () => [] }
});

const emit = defineEmits(['error', 'success']);

const form = reactive({
  tipo: 'ingreso',
  fechaDesde: '',
  fechaHasta: '',
  CUR_ID: '',
  GRU_ID: '',
  COC_ID: ''
});

const pagos = ref([]);
const loading = ref(false);
const buscado = ref(false);
const seleccionados = ref([]);

const totalSeleccionado = computed(() => {
  return pagos.value
    .filter(p => seleccionados.value.includes(p.PAP_ID))
    .reduce((total, p) => total + (p.PAP_MONTO || 0), 0);
});

async function buscar() {
  loading.value = true;
  buscado.value = true;
  pagos.value = [];
  seleccionados.value = [];

  try {
    const params = {
      tipo: form.tipo,
      fecha_desde: form.fechaDesde || undefined,
      fecha_hasta: form.fechaHasta || undefined,
      CUR_ID: form.CUR_ID || undefined,
      GRU_ID: form.GRU_ID || undefined,
      COC_ID: form.COC_ID || undefined,
    };

    const response = await pagosService.pagos.list(params);
    const results = response.results || response || [];
    
    pagos.value = results.map(p => ({
      ...p,
      PAP_ID: p.pap_id || p.PAP_ID,
      PAP_MONTO: p.pap_valor || p.PAP_VALOR || p.pap_monto || p.PAP_MONTO,
      PAP_FECHA_PAGO: p.pap_fecha_hora || p.PAP_FECHA_HORA,
      persona_nombre: p.persona_nombre || (p.persona ? `${p.persona.per_nombres} ${p.persona.per_apelpta}` : ''),
      concepto_descripcion: p.concepto_descripcion || (props.conceptosOptions.find(c => c.value === (p.coc_id || p.COC_ID))?.label || '')
    }));
  } catch (e) {
    console.error("Error buscando pagos para comprobante:", e);
    emit('error', 'No se pudieron cargar los pagos para el comprobante.');
  } finally {
    loading.value = false;
  }
}

function toggleSelectAll(checked) {
  seleccionados.value = checked ? pagos.value.map(p => p.PAP_ID) : [];
}

const dateCL = (f) => {
  if (!f) return '-';
  try {
    const date = typeof f === 'string' ? parseISO(f) : f;
    return format(date, 'dd-MM-yyyy');
  } catch {
    return f;
  }
};

async function generarPDF() {
  const selectedItems = pagos.value.filter(p => seleccionados.value.includes(p.PAP_ID));
  if (selectedItems.length === 0) return;

  const doc = new jsPDF();
  const tipoComprobante = form.tipo.charAt(0).toUpperCase() + form.tipo.slice(1);

  doc.setFontSize(18);
  doc.text(`Comprobante de ${tipoComprobante}`, 14, 22);
  doc.setFontSize(11);
  doc.setTextColor(100);
  doc.text(`Fecha de generación: ${format(new Date(), 'dd-MM-yyyy')}`, 14, 30);

  doc.setFontSize(12);
  doc.text('Resumen', 14, 45);
  doc.autoTable({
    startY: 50,
    head: [['Concepto', 'Valor']],
    body: [
      ['Monto Total', `$${totalSeleccionado.value.toLocaleString('es-CL')}`],
      ['Cantidad de Transacciones', selectedItems.length],
    ],
    theme: 'striped',
    headStyles: { fillColor: [44, 90, 160] },
  });

  const tableBody = selectedItems.map(p => [
    dateCL(p.PAP_FECHA_PAGO),
    p.persona_nombre,
    p.persona_rut || '',
    p.concepto_descripcion,
    `$${(p.PAP_MONTO || 0).toLocaleString('es-CL')}`
  ]);

  doc.autoTable({
    head: [['Fecha', 'Nombre', 'RUT', 'Concepto', 'Monto']],
    body: tableBody,
    startY: doc.autoTable.previous.finalY + 10,
    headStyles: { fillColor: [44, 90, 160] },
  });

  doc.save(`Comprobante_${tipoComprobante}_${format(new Date(), 'yyyyMMdd')}.pdf`);
  emit('success', 'PDF generado correctamente');
}
</script>

<style scoped>
.panel-box {
  border-radius: 12px;
  padding: 16px 18px 22px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}
.panel-title {
  text-align: center;
  margin-bottom: 10px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px 18px;
}
.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.col.auto {
  align-self: flex-end;
}
label {
  font-weight: 600;
  color: #111827;
  font-size: 13px;
}
.invisible {
  visibility: hidden;
}
.lista {
  margin-top: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
}
.lista-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid #f3f4f6;
}
.table-container {
  overflow-x: auto;
}
.courses-table {
  width: 100%;
  border-collapse: collapse;
}
.courses-table th, .courses-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}
.courses-table th {
  background-color: #f9fafb;
  font-size: 12px;
}
.placeholder {
  text-align: center;
  padding: 20px;
  color: #94a3b8;
}
.resumen {
  margin-top: 10px;
  padding: 10px 14px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  display: flex;
  gap: 16px;
  justify-content: center;
  font-weight: 600;
  color: #1d4ed8;
}
.acciones {
  display: flex;
  gap: 12px;
}
.center {
  justify-content: center;
}
.btn-standard {
  min-width: 140px;
}
</style>
