<template>
  <section class="panel panel-box">
    <div class="panel-title">
      <h3>Registro Masivo de Pagos</h3>
      <p>Selecciona grupo y curso, participantes y registra pagos masivos.</p>
    </div>

    <div class="grid grid-masivo">
      <div class="col">
        <label>Grupo *</label>
        <BaseSelect
          v-model="form.GRU_ID"
          :options="grupoOptions"
          placeholder="Seleccione grupo"
        />
      </div>
      <div class="col">
        <label>Curso / Capacitación *</label>
        <BaseSelect
          v-model="form.CUR_ID"
          :options="computedCursoOptions"
          placeholder="Seleccione curso"
        />
      </div>
      <div class="col">
        <label>Tipo de Pago *</label>
        <BaseSelect
          v-model="form.tipoPago"
          :options="[{value: 'ingreso', label: 'Ingreso'}, {value: 'egreso', label: 'Egreso'}]"
          placeholder="Seleccione tipo"
        />
      </div>
      <div class="col">
        <label>Concepto *</label>
        <BaseSelect
          v-model="form.COC_ID"
          :options="conceptosOptions"
          placeholder="Seleccione concepto"
        />
      </div>
      <div class="col half">
        <label>Valor Total *</label>
        <div class="with-prefix">
          <span class="prefix">$</span>
          <input
            type="number"
            min="0"
            step="100"
            v-model.number="form.PAP_MONTO"
            placeholder="Ingrese el monto total"
            :disabled="!seleccionados.length"
          />
        </div>
      </div>
      <div class="col half">
        <label>Fecha de Pago *</label>
        <InputBase 
          type="date" 
          v-model="form.PAP_FECHA_PAGO" 
          :disabled="!seleccionados.length"
        />
      </div>
      <div class="col auto full-width">
        <label class="invisible">Cargar</label>
        <BaseButton class="btn-standard"
          variant="primary"
          :disabled="!form.GRU_ID || !form.CUR_ID || cargandoParticipantes"
          @click="cargarParticipantes"
        >
          <AppIcons name="users" :size="16" /> {{ cargandoParticipantes ? 'Cargando...' : 'Cargar' }}
        </BaseButton>
      </div>
    </div>

    <div v-if="participantes.length" class="lista">
      <div class="lista-header">
        <h5>Participantes ({{ participantes.length }})</h5>
        <div class="acciones">
          <BaseButton size="sm" variant="secondary" @click="selectAll">
            Seleccionar todos
          </BaseButton>
          <BaseButton size="sm" variant="secondary" @click="unselectAll">
            Deseleccionar
          </BaseButton>
        </div>
      </div>

      <div class="lista-items">
        <label v-for="u in participantes" :key="u.id" class="item">
          <input type="checkbox" :value="u.id" v-model="seleccionados" />
          <div class="info">
            <strong>{{ u.nombre }}</strong>
            <span class="muted">{{ u.rut }} · {{ u.email }}</span>
          </div>
        </label>
      </div>
    </div>

    <div v-if="seleccionados.length" class="grid grid-masivo">
      <div class="col span-2">
        <label>Comentario / Observación (máx. 200 caracteres)</label>
        <textarea
          class="comentario-input"
          v-model="form.observacion"
          maxlength="200"
          placeholder="Detalle general del pago; se aplicará a todos."
        />
      </div>
      <div class="col span-2 comprobante-wrapper">
        <label>Comprobante de transferencia grupal {{ form.tipoPago === 'egreso' ? '(Opcional)' : '' }}</label>
        <input
          ref="fileRef"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          @change="onFileChange"
        />
      </div>
    </div>

    <div
      class="resumen"
      v-if="seleccionados.length && form.PAP_MONTO"
    >
      <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
      <div>Valor por persona: <strong>${{ valorPorPersona.toLocaleString('es-CL') }}</strong></div>
      <div class="total">
        Total:
        <strong>
          ${{
            (form.PAP_MONTO).toLocaleString('es-CL')
          }}
        </strong>
      </div>
    </div>

    <div class="acciones center acciones-individual" v-if="seleccionados.length">
      <BaseButton
        variant="success"
        class="btn-standard"
        :disabled="!puedeRegistrar || loading"
        @click="registrar"
      >
        <AppIcons v-if="!loading" name="save" :size="16" />
        <AppIcons v-else name="spinner" :size="16" class="spin" />
        <span v-if="!loading"> Registrar Pago ({{ seleccionados.length }})</span>
        <span v-else> Registrando...</span>
      </BaseButton>
      <BaseButton variant="secondary" class="btn-standard" @click="limpiar">
        <AppIcons name="x" :size="16" /> Limpiar
      </BaseButton>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue';
import InputBase from '@/components/InputBase.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import personasService from '@/services/personasService.js';
import pagosService from '@/services/pagosService.js';
import authService from '@/services/authService.js';

const props = defineProps({
  grupoOptions: { type: Array, default: () => [] },
  allCursoOptions: { type: Array, default: () => [] },
  conceptosOptions: { type: Array, default: () => [] }
});

const emit = defineEmits(['success', 'error']);

const hoyISO = () => {
  const d = new Date();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
};

const form = reactive({
  GRU_ID: '',
  CUR_ID: '',
  PAP_MONTO: null,
  PAP_FECHA_PAGO: hoyISO(),
  observacion: '',
  tipoPago: 'ingreso',
  COC_ID: null,
  file: null
});

const participantes = ref([]);
const seleccionados = ref([]);
const cargandoParticipantes = ref(false);
const loading = ref(false);
const filteredCursoOptions = ref([]);
const fileRef = ref(null);

const computedCursoOptions = computed(() => {
  return filteredCursoOptions.value.length > 0 ? filteredCursoOptions.value : props.allCursoOptions;
});

watch(() => form.GRU_ID, (newVal) => {
  if (newVal) {
    cargarCursosPorGrupo(newVal);
    form.CUR_ID = null;
  } else {
    filteredCursoOptions.value = [];
    form.CUR_ID = null;
  }
});

const puedeRegistrar = computed(() => {
  return (
    seleccionados.value.length &&
    form.CUR_ID &&
    form.GRU_ID &&
    form.COC_ID &&
    form.tipoPago &&
    form.PAP_MONTO > 0 &&
    form.PAP_FECHA_PAGO &&
    (form.tipoPago === 'egreso' || form.file)
  );
});

const valorPorPersona = computed(() => {
  if (!form.PAP_MONTO || !seleccionados.value.length) return 0;
  return Math.round(form.PAP_MONTO / seleccionados.value.length);
});

async function cargarCursosPorGrupo(gruId) {
  try {
    const response = await personasService.personaCursos.list({ 
      grupo_id: gruId, 
      page_size: 1000 
    });
    const items = response.results || response;
    
    const cursosMap = new Map();
    items.forEach(item => {
      const curId = item.cur_id || item.CUR_ID;
      const curDesc = item.cur_descripcion || item.CUR_DESCRIPCION;
      if (curId && curDesc) {
        cursosMap.set(curId, curDesc);
      }
    });

    filteredCursoOptions.value = Array.from(cursosMap.entries()).map(([id, label]) => ({
      value: id,
      label: label
    }));
  } catch (e) {
    console.error('Error cargando cursos del grupo:', e);
    filteredCursoOptions.value = [];
  }
}

async function cargarParticipantes() {
  cargandoParticipantes.value = true;
  participantes.value = [];
  try {
    const response = await personasService.personas.list({
      grupo: form.GRU_ID, curso: form.CUR_ID
    });
    const results = response.results || response;
    participantes.value = results.map(p => ({
      id: p.per_id || p.PER_ID || p.id,
      nombre: `${p.per_nombres || p.PER_NOMBRES || ''} ${p.per_apelpta || p.PER_APELPTA || ''}`.trim(),
      rut: (p.per_run || p.PER_RUN) ? `${p.per_run || p.PER_RUN}-${p.per_dv || p.PER_DV || ''}` : '',
      email: p.per_mail || p.PER_MAIL || ''
    }));
    seleccionados.value = [];
  } catch (e) {
    console.error('Error cargando participantes:', e);
    participantes.value = [];
  } finally {
    cargandoParticipantes.value = false;
  }
}

function selectAll() {
  seleccionados.value = participantes.value.map(u => u.id);
}

function unselectAll() {
  seleccionados.value = [];
}

function onFileChange(e) {
  form.file = e.target.files?.[0] || null;
}

function limpiar() {
  form.GRU_ID = '';
  form.CUR_ID = '';
  form.PAP_MONTO = null;
  form.PAP_FECHA_PAGO = hoyISO();
  form.observacion = '';
  form.tipoPago = 'ingreso';
  form.COC_ID = null;
  form.file = null;
  participantes.value = [];
  seleccionados.value = [];
  if (fileRef.value) fileRef.value.value = '';
}

async function registrar() {
  if (loading.value) return;
  loading.value = true;
  try {
    const fd = new FormData();
    fd.append('cur_id', form.CUR_ID);
    fd.append('pap_valor', form.PAP_MONTO);
    fd.append('coc_id', form.COC_ID);
    fd.append('pap_fecha_hora', form.PAP_FECHA_PAGO);
    if (form.observacion) fd.append('pap_observacion', form.observacion);
    fd.append('pap_tipo', form.tipoPago === 'egreso' ? 2 : 1);
    
    try {
      const current = await authService.getCurrentUser();
      const usuId = current?.id || current?.usu_id || current?.payload?.usu_id;
      if (usuId) fd.append('usu_id', usuId);
    } catch {}

    seleccionados.value.forEach(id => fd.append('per_ids', id));
    if (form.file) fd.append('comprobante', form.file);
    fd.append('met_id', 1); // Transferencia
    
    await pagosService.pagos.createMasivo(fd);
    emit('success', 'Pago masivo registrado correctamente');
    limpiar();
  } catch (e) {
    console.error('Error registrando pago masivo', e);
    emit('error', 'Error registrando pago masivo: ' + (e.message || ''));
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* Scoped styles same as individual but for masivo */
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
.panel-title h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 700;
}
.panel-title p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px 16px;
  margin-top: 8px;
}
.grid-masivo {
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 18px;
}
.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.col.full-width {
  grid-column: 1 / -1;
}
.col.span-2 {
  grid-column: span 2;
}
.col.half {
  grid-column: span 1;
}
.col.auto {
  align-self: flex-end;
}
label {
  font-weight: 600;
  color: #111827;
  font-size: 13px;
}
.with-prefix {
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}
.with-prefix .prefix {
  background: #eff6ff;
  padding: 8px 10px;
  font-weight: 700;
  color: #1d4ed8;
  border-right: 1px solid #d1d5db;
}
.with-prefix input {
  border: none;
  padding: 8px 10px;
  flex: 1;
  outline: none;
}
.comentario-input {
  width: 100%;
  min-height: 52px;
  max-height: 80px;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  resize: vertical;
  font-family: inherit;
  font-size: 13px;
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
.lista-header h5 {
  margin: 0;
  font-size: 14px;
  color: #374151;
}
.lista-items {
  max-height: 260px;
  overflow: auto;
  display: flex;
  flex-direction: column;
}
.item {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px 10px;
  border-bottom: 1px solid #f9fafb;
  cursor: pointer;
}
.item:hover {
  background: #f9fafb;
}
.item:last-child {
  border-bottom: none;
}
.item .info {
  display: flex;
  flex-direction: column;
}
.item .info strong {
  font-size: 13px;
}
.item .info .muted {
  color: #6b7280;
  font-size: 11px;
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
  font-size: 13px;
}
.total {
  text-transform: uppercase;
}
.acciones {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}
.acciones-individual {
  margin-top: 20px;
}
.center {
  justify-content: center;
}
.invisible {
  visibility: hidden;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.btn-standard {
  min-width: 140px;
}
</style>
