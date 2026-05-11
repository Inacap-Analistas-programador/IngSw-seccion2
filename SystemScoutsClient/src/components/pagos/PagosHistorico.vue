<template>
  <div class="card card-historico">
    <!-- Filtros compactos -->
    <div class="filtros filtros-historico" style="align-items: flex-end;">
      <div style="display: flex; flex-direction: column;">
        <label>Buscar</label>
        <InputBase class="filtro-busqueda filtro-corto" v-model="filters.q" placeholder="NOMBRE / RUT / EMAIL" title="Buscar por Nombre, RUT o Email" />
      </div>
      <div style="display: flex; flex-direction: column;">
        <label>Curso</label>
        <BaseSelect class="filtro-corto" v-model="filters.curso" :options="[{ value: '', label: 'Todos los cursos' }, ...cursoOptions]" title="Filtrar por Curso" />
      </div>
      <div style="display: flex; flex-direction: column;">
        <label>Grupo</label>
        <BaseSelect class="filtro-corto" v-model="filters.grupo" :options="[{ value: '', label: 'Todos los grupos' }, ...grupoOptions]" title="Filtrar por Grupo" />
      </div>
      <div style="display: flex; flex-direction: column;">
        <label>Estado de Pago</label>
        <BaseSelect class="filtro-corto" v-model="filters.estado" :options="[{ value: '', label: 'Todos' }, { value: 'pagado', label: 'Pagado' }, { value: 'pendiente', label: 'Pendiente' }, { value: 'anulado', label: 'Anulado' }]" title="Filtrar por Estado de Pago" />
      </div>
      <BaseButton class="btn-standard" variant="primary" @click="cargarPagos(true)">
        <AppIcons name="search" :size="16" /> Buscar
      </BaseButton>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <BaseButton class="btn-standard" variant="secondary" @click="exportarExcel">
        <AppIcons name="download" :size="16" />
        Exportar
      </BaseButton>
    </div>

    <!-- Estado -->
    <div v-if="loading" class="estado-carga">
      <div class="spinner"></div> Cargando pagos...
    </div>
    <div v-if="error" class="mensaje-error">
      {{ error }}
      <div>
        <BaseButton variant="primary" @click="cargarPagos(true)">Reintentar</BaseButton>
      </div>
    </div>

    <!-- Tabla -->
    <div class="table-container" v-if="!loading && !error">
      <table class="courses-table">
        <thead>
          <tr>
            <th style="width: 32px;">
              <input
                type="checkbox"
                :checked="allChecked"
                @change="toggleSelectAll($event.target.checked)"
              />
            </th>
            <th>Nombre</th>
            <th>RUT</th>
            <th>Curso</th>
            <th>Monto</th>
            <th>Fecha</th>
            <th>Método</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pagos" :key="p.PAP_ID">
            <td>
              <input
                type="checkbox"
                :value="p.PAP_ID"
                v-model="seleccionados"
              />
            </td>
            <td data-label="Nombre" class="texto-largo" :title="p.persona_nombre"><strong>{{ p.persona_nombre }}</strong></td>
            <td data-label="RUT">{{ p.persona_rut }}</td>
            <td data-label="Curso">{{ cursoLabel(p.CUR_ID) }}</td>
            <td data-label="Monto">${{ (p.PAP_MONTO)?.toLocaleString('es-CL') }}</td>
            <td data-label="Fecha">{{ dateCL(p.PAP_FECHA_PAGO) }}</td>
            <td data-label="Método">{{ p.MET_DESCRIPCION || 'Transferencia' }}</td>
            <td data-label="Acciones" class="acciones-buttons">
              <BaseButton class="btn-action"
                size="sm"
                variant="info"
                @click="$emit('ver-detalle', p)"
              >
                <AppIcons name="eye" :size="14" /> Ver
              </BaseButton>
              <BaseButton class="btn-action"
                size="sm"
                variant="secondary"
                @click="$emit('editar', p)"
              >
                <AppIcons name="edit" :size="14" /> Editar
              </BaseButton>
              <BaseButton class="btn-action" 
                size="sm"
                variant="secondary"
                @click="$emit('transferir', p)"
              >
                <AppIcons name="share" :size="14" /> Transferir
              </BaseButton>
              <BaseButton class="btn-action"
                size="sm"
                variant="danger"
                @click="$emit('anular', p)"
              >
                <AppIcons name="trash" :size="14" /> Anular
              </BaseButton>
              <BaseButton class="btn-action"
                v-if="p.PAP_RUTA_COMPROBANTE"
                size="sm"
                variant="info"
                @click="$emit('descargar-comprobante', p)"
              >
                <AppIcons name="download" :size="14" /> Comprobante
              </BaseButton>
            </td>
          </tr>
          <tr v-if="!pagos.length">
            <td colspan="8" class="placeholder">
              {{ hasAnyFilter ? 'No se encontraron pagos con los filtros seleccionados' : 'Ingrese filtros para buscar pagos' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import InputBase from '@/components/InputBase.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import pagosService from '@/services/pagosService.js';
import { format, parseISO } from 'date-fns';

const props = defineProps({
  cursoOptions: { type: Array, default: () => [] },
  grupoOptions: { type: Array, default: () => [] }
});

defineEmits(['ver-detalle', 'editar', 'transferir', 'anular', 'descargar-comprobante']);

const filters = reactive({
  q: '',
  estado: '',
  curso: '',
  grupo: ''
});

const pagos = ref([]);
const loading = ref(false);
const error = ref(null);
const seleccionados = ref([]);

const hasAnyFilter = computed(() => {
  return !!(
    (filters.q && filters.q.trim()) ||
    filters.curso ||
    filters.grupo ||
    filters.estado
  );
});

const allChecked = computed(() => {
  return (
    pagos.value.length > 0 &&
    seleccionados.value.length === pagos.value.length
  );
});

const cursoLabel = (id) => {
  const c = props.cursoOptions.find(x => String(x.value) === String(id));
  return c ? c.label : id;
};

const dateCL = (f) => {
  if (!f) return '-';
  try {
    const date = typeof f === 'string' ? parseISO(f) : f;
    return format(date, 'dd-MM-yyyy');
  } catch {
    return f;
  }
};

const formatRutForSearch = (rut) => {
  if (!rut) return '';
  const rutLimpio = String(rut).replace(/[^0-9]/g, '');
  if (rutLimpio.length < 2) return rutLimpio;
  const cuerpo = rutLimpio.slice(0, -1);
  return cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
};

async function cargarPagos(force = false) {
  if (loading.value && !force) return;
  loading.value = true;
  error.value = null;
  try {
    let searchTerm = (filters.q || '').trim();
    if (/^\d{7,8}$/.test(searchTerm)) {
      searchTerm = formatRutForSearch(searchTerm);
    }

    const estadoMap = { pagado: 1, anulado: 2 };
    const params = {};
    
    if (searchTerm) params.search = searchTerm;
    if (filters.curso) params.cur_id = filters.curso;
    if (filters.grupo) params.grupo_id = filters.grupo;
    if (filters.estado) {
      const mapped = estadoMap[filters.estado];
      if (mapped) params.estado = mapped;
    }

    if (!hasAnyFilter.value && !force) {
      pagos.value = [];
      loading.value = false;
      return;
    }

    const response = await pagosService.pagos.list(params);
    let rawList = response.results || response || [];
    
    pagos.value = rawList.map(p => ({
      ...p,
      PAP_ID: p.pap_id || p.PAP_ID,
      CUR_ID: p.cur_id || p.CUR_ID,
      PAP_MONTO: p.pap_valor || p.PAP_VALOR || p.pap_monto || p.PAP_MONTO,
      PAP_FECHA_PAGO: p.pap_fecha_hora || p.PAP_FECHA_HORA,
      MET_DESCRIPCION: p.met_descripcion || p.MET_DESCRIPCION,
      PAP_RUTA_COMPROBANTE: p.pap_ruta_comprobante || p.PAP_RUTA_COMPROBANTE,
      persona_nombre: p.persona_nombre || (p.persona ? `${p.persona.per_nombres} ${p.persona.per_apelpta}` : ''),
      persona_rut: p.persona_rut || (p.persona ? p.persona.per_run : '')
    }));

  } catch (e) {
    console.error('Error al cargar pagos:', e);
    pagos.value = [];
    error.value = 'No fue posible cargar pagos. Verifica el backend.';
  } finally {
    loading.value = false;
  }
}

function toggleSelectAll(checked) {
  seleccionados.value = checked ? pagos.value.map(p => p.PAP_ID) : [];
}

function exportarExcel() {
  if (pagos.value.length === 0) return;

  const rowsToExport = pagos.value.map(p => ({
    'Rut': p.persona_rut,
    'Nombre': p.persona_nombre?.split(' ')[0] || '',
    'Apellidos': p.persona_nombre?.split(' ').slice(1).join(' ') || '',
    'Correo electrónico': p.persona_email || '',
    'Grupo': p.grupo_nombre || '',
    'Distrito': p.distrito_nombre || '',
    'Zona': p.zona_nombre || '',
    'Curso': cursoLabel(p.CUR_ID),
    'Valor Cuota': p.valor_cuota || 0,
    'Valor Pagado': p.PAP_MONTO || 0,
    'Valor Adeudado': (p.valor_cuota || 0) - (p.PAP_MONTO || 0),
    'Fecha Ultimo Pago': dateCL(p.PAP_FECHA_PAGO)
  }));

  const ws = XLSX.utils.json_to_sheet(rowsToExport);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Pagos");
  XLSX.writeFile(wb, "Pagos_Historico.xlsx");
}

onMounted(() => {
  cargarPagos();
});

defineExpose({ cargarPagos });
</script>

<style scoped>
.card-historico {
  min-height: 360px;
  background: #ffffff;
  border-radius: 14px;
  padding: 22px 28px 32px;
}
.filtros {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.filtros-historico {
  margin-bottom: 10px;
}
.filtro-busqueda {
  width: 200px;
}
.filtro-corto {
  width: 160px;
}
label {
  font-weight: 600;
  color: #111827;
  font-size: 13px;
  margin-bottom: 4px;
}
.toolbar {
  display: flex;
  gap: 10px;
  margin: 4px 0 12px;
}
.estado-carga {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  color: #6b7280;
}
.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.table-container {
  overflow-x: auto;
  margin-top: 10px;
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
  font-weight: 600;
  color: #374151;
}
.btn-action {
  padding: 4px 8px;
  font-size: 12px;
}
.acciones-buttons {
  display: flex;
  gap: 4px;
}
.placeholder {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}
.spin {
  animation: spin 1s linear infinite;
}
</style>
