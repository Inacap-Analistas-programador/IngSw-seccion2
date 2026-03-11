<template>
  <section class="panel panel-box">
    <div class="panel-title">
      <h3>Registro Individual de Pagos</h3>
      <p>Busca un participante, selecciona el curso y registra el pago.</p>
    </div>

    <!-- Buscar persona -->
    <div class="row-buscar">
      <div class="buscar-input">
        <InputBase id="buscar-persona-input"
          v-model="buscarPersonaQ"
          placeholder="EJ: 12.345.678-9 O JUAN PÉREZ"
        />
      </div>
    </div>

    <div v-if="buscandoPersonas" class="estado-carga">
      <div class="spinner"></div> Buscando personas...
    </div>

    <div v-if="personasEncontradas.length" class="resultados">
      <div
        v-for="p in personasEncontradas"
        :key="p.id"
        class="resultado"
        @click="seleccionarPersona(p)"
      >
        <div class="resultado-left">
          <strong>{{ p.nombre }}</strong>
          <span class="muted">{{ p.rut }} · {{ p.email }}</span>
        </div>
        <BaseButton size="sm" variant="secondary" class="btn-action">
          Elegir
        </BaseButton>
      </div>
    </div>

    <!-- Form individual -->
    <div class="grid grid-individual">
      <div class="col">
        <label>Nombre</label>
        <InputBase v-model="form.nombre" readonly />
      </div>
      <div class="col">
        <label>RUT</label>
        <InputBase v-model="form.rut" readonly />
      </div>
      <div class="col">
        <label>Email</label>
        <InputBase v-model="form.email" readonly />
      </div>

      <div class="col">
        <label>Tipo de Pago *</label>
        <div class="button-group">
          <BaseButton
            :variant="form.tipoPago === 'ingreso' ? 'primary' : 'secondary'"
            @click="form.tipoPago = 'ingreso'">
            Ingreso
          </BaseButton>
          <BaseButton
            :variant="form.tipoPago === 'egreso' ? 'primary' : 'secondary'"
            @click="form.tipoPago = 'egreso'">
            Egreso
          </BaseButton>
        </div>
      </div>

      <div class="col">
        <label>Concepto *</label>
        <BaseSelect
          v-model="form.COC_ID"
          :options="conceptosOptions"
          placeholder="Seleccione concepto"
        />
      </div>

      <div class="col">
        <label>Curso / Capacitación *</label>
        <BaseSelect
          v-model="form.CUR_ID"
          :options="cursoOptions"
          placeholder="Seleccione curso"
        />
      </div>

      <div class="col half">
        <label>Valor Pagado *</label>
        <div class="with-prefix">
          <span class="prefix">$</span>
          <input
            type="number"
            min="0"
            step="100"
            v-model.number="form.PAP_MONTO"
          />
        </div>
      </div>

      <div class="col half">
        <label>Fecha de Pago *</label>
        <InputBase type="date" v-model="form.PAP_FECHA_PAGO" />
      </div>

      <div class="col span-2">
        <label>Comentario / Observación</label>
        <textarea
          class="comentario-input"
          v-model="form.observacion"
          maxlength="200"
          placeholder="Detalle del pago, referencia de transferencia, etc."
        />
      </div>

      <div class="col full comprobante-wrapper">
        <label>Comprobante de transferencia {{ form.tipoPago === 'egreso' ? '(Opcional)' : '' }}</label>
        <input
          ref="fileRef"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          @change="onFileChange"
        />
      </div>
    </div>

    <div class="acciones center acciones-individual">
      <BaseButton
        variant="success"
        class="btn-standard"
        :disabled="!puedeRegistrar || loading"
        @click="registrar"
      >
        <AppIcons v-if="!loading" name="save" :size="16" />
        <AppIcons v-else name="spinner" :size="16" class="spin" />
        <span v-if="!loading"> Registrar Pago</span>
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
  cursoOptions: { type: Array, default: () => [] },
  conceptosOptions: { type: Array, default: () => [] }
});

const emit = defineEmits(['success', 'error']);

const hoyISO = () => {
  const d = new Date();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
};

const buscarPersonaQ = ref('');
const buscandoPersonas = ref(false);
const personasEncontradas = ref([]);
const loading = ref(false);
const fileRef = ref(null);

const form = reactive({
  personaId: null,
  nombre: '',
  rut: '',
  email: '',
  CUR_ID: '',
  PAP_MONTO: null,
  PAP_FECHA_PAGO: hoyISO(),
  observacion: '',
  tipoPago: 'ingreso',
  COC_ID: null,
  file: null
});

let debounceTimer = null;

watch(buscarPersonaQ, (newQuery) => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => buscarPersonas(newQuery), 300);
});

const puedeRegistrar = computed(() => {
  const isEgreso = form.tipoPago === 'egreso';
  return (
    form.personaId &&
    form.CUR_ID &&
    form.COC_ID &&
    form.tipoPago &&
    form.PAP_MONTO > 0 &&
    form.PAP_FECHA_PAGO &&
    (isEgreso || form.file)
  );
});

async function buscarPersonas(q) {
  const termRaw = (q || '').trim();
  if (!termRaw) {
    personasEncontradas.value = [];
    return;
  }

  const termClean = termRaw.replace(/[\.\-\s]/g, '');
  let params = {};

  if (/^\d+$/.test(termClean)) {
    params = { run: termClean };
  } else if (/^\d{7,8}[0-9kK]$/i.test(termClean)) {
    const rutMatch = termClean.match(/^(\d{7,8})([0-9kK])$/i);
    if (rutMatch) {
      params = { run: rutMatch[1], dv: rutMatch[2].toUpperCase() };
    }
  } else {
    const parts = termRaw.split(/\s+/);
    if (parts.length === 1) params = { nombre: termRaw };
    else params = { nombre: parts[0], apellido: parts.slice(1).join(' ') };
  }

  buscandoPersonas.value = true;
  try {
    const response = await personasService.personas.list(params);
    const results = response.results || response;
    personasEncontradas.value = results.map(p => ({
      id: p.per_id || p.PER_ID || p.id,
      nombre: `${p.per_nombres || p.PER_NOMBRES || ''} ${p.per_apelpta || p.PER_APELPTA || ''}`.trim(),
      rut: (p.per_run || p.PER_RUN) ? `${p.per_run || p.PER_RUN}-${p.per_dv || p.PER_DV || ''}` : '',
      email: p.per_mail || p.PER_MAIL || ''
    }));
  } catch (e) {
    console.error('Error buscando personas:', e);
    personasEncontradas.value = [];
  } finally {
    buscandoPersonas.value = false;
  }
}

function seleccionarPersona(p) {
  form.personaId = p.id;
  form.nombre = p.nombre;
  form.rut = p.rut;
  form.email = p.email;
  personasEncontradas.value = [];
  buscarPersonaQ.value = p.nombre;
}

function onFileChange(e) {
  form.file = e.target.files?.[0] || null;
}

function limpiar() {
  form.personaId = null;
  form.nombre = '';
  form.rut = '';
  form.email = '';
  form.CUR_ID = '';
  form.PAP_MONTO = null;
  form.PAP_FECHA_PAGO = hoyISO();
  form.observacion = '';
  form.tipoPago = 'ingreso';
  form.COC_ID = null;
  form.file = null;
  buscarPersonaQ.value = '';
  personasEncontradas.value = [];
  if (fileRef.value) fileRef.value.value = '';
}

async function registrar() {
  if (loading.value) return;
  loading.value = true;
  try {
    const fd = new FormData();
    fd.append('per_id', form.personaId);
    if (form.CUR_ID) fd.append('cur_id', form.CUR_ID);
    if (form.PAP_MONTO !== null) fd.append('pap_valor', form.PAP_MONTO);
    if (form.COC_ID) fd.append('coc_id', form.COC_ID);
    if (form.PAP_FECHA_PAGO) fd.append('pap_fecha_hora', form.PAP_FECHA_PAGO);
    if (form.observacion) fd.append('pap_observacion', form.observacion);
    if (form.file) fd.append('comprobante', form.file);
    fd.append('pap_tipo', form.tipoPago === 'egreso' ? 2 : 1);
    fd.append('pap_estado', 1);

    try {
      const current = await authService.getCurrentUser();
      const usuId = current?.id || current?.usu_id || current?.payload?.usu_id;
      if (usuId) fd.append('usu_id', usuId);
    } catch (e) {
      console.warn('No se pudo resolver usu_id localmente:', e);
    }

    await pagosService.pagos.create(fd);
    emit('success', 'Pago individual registrado correctamente');
    limpiar();
  } catch (e) {
    console.error('Error registrando pago individual', e);
    emit('error', 'Error registrando pago: ' + (e.message || ''));
  } finally {
    loading.value = false;
  }
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
.row-buscar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.buscar-input {
  flex: 0 0 400px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px 16px;
  margin-top: 8px;
}
.grid-individual {
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 18px;
}
.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.col.full {
  grid-column: 1 / -1;
}
.col.span-2 {
  grid-column: span 2;
}
.col.half {
  grid-column: span 1;
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
.resultados {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 4px;
  max-width: 480px;
  background: #ffffff;
  max-height: 280px;
  overflow-y: auto;
  position: absolute;
  z-index: 10;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.resultado {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
}
.resultado:hover {
  background: #f9fafb;
}
.resultado .muted {
  color: #6b7280;
  font-size: 11px;
}
.estado-carga {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  font-size: 13px;
  margin: 8px 0;
}
.spinner {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  width: 14px;
  height: 14px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.acciones {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}
.center {
  justify-content: center;
}
.button-group {
  display: flex;
  gap: 8px;
}
.spin {
  animation: spin 1s linear infinite;
}

/* Base styles copied from PagosView.vue for local overrides if needed */
.btn-standard {
  min-width: 140px;
}
</style>
