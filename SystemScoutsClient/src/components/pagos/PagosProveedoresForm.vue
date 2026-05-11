<template>
  <section class="panel panel-box">
    <div class="panel-title">
      <h3>Pagos a Proveedores</h3>
      <p>Registra egresos destinados a proveedores de servicios o productos.</p>
    </div>

    <div class="grid grid-proveedor">
      <div class="col">
        <label>Nombre o Razón Social *</label>
        <InputBase v-model="form.nombre" placeholder="Ej: Imprenta Central" />
      </div>
      <div class="col">
        <label>RUT del Proveedor *</label>
        <InputBase v-model="form.rut" placeholder="Ej: 76.123.456-7" />
      </div>
      <div class="col">
        <label>Concepto de Egreso *</label>
        <BaseSelect v-model="form.COC_ID" :options="conceptosEgresoOptions" placeholder="Seleccione concepto" />
      </div>
      <div class="col half">
        <label>Valor Pagado *</label>
        <div class="with-prefix">
          <span class="prefix">$</span>
          <input type="number" min="0" v-model.number="form.PAP_MONTO" />
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
          placeholder="Nº de factura, detalle del servicio, etc."
        ></textarea>
      </div>
      <div class="col full comprobante-wrapper">
        <label>Comprobante (Opcional)</label>
        <input ref="fileRef" type="file" accept=".pdf,.jpg,.jpeg,.png" @change="onFileChange" />
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
        <span v-if="!loading"> Registrar Egreso</span>
        <span v-else> Registrando...</span>
      </BaseButton>
      <BaseButton variant="secondary" class="btn-standard" @click="limpiar">
        <AppIcons name="x" :size="16" /> Limpiar
      </BaseButton>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import InputBase from '@/components/InputBase.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import pagosService from '@/services/pagosService.js';

const props = defineProps({
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
  nombre: '',
  rut: '',
  COC_ID: null,
  PAP_MONTO: null,
  PAP_FECHA_PAGO: hoyISO(),
  observacion: '',
  file: null
});

const loading = ref(false);
const fileRef = ref(null);

const conceptosEgresoOptions = computed(() => {
  return props.conceptosOptions.filter(c => c.tipo === 'egreso');
});

const puedeRegistrar = computed(() => {
  return form.nombre &&
         form.rut &&
         form.COC_ID &&
         form.PAP_MONTO > 0 &&
         form.PAP_FECHA_PAGO;
});

function onFileChange(e) {
  form.file = e.target.files?.[0] || null;
}

function limpiar() {
  form.nombre = '';
  form.rut = '';
  form.COC_ID = null;
  form.PAP_MONTO = null;
  form.PAP_FECHA_PAGO = hoyISO();
  form.observacion = '';
  form.file = null;
  if (fileRef.value) fileRef.value.value = '';
}

async function registrar() {
  if (!puedeRegistrar.value || loading.value) return;
  loading.value = true;
  try {
    const fd = new FormData();
    fd.append('prv_descripcion', form.nombre + (form.rut ? ` (${form.rut})` : ''));
    fd.append('prv_celular1', ''); 
    fd.append('prv_direccion', '');
    
    if (form.observacion) {
       fd.append('prv_observacion', form.observacion);
    }
    
    await pagosService.proveedor.create(fd);
    emit('success', 'Pago a proveedor registrado correctamente');
    limpiar();
  } catch (e) {
    console.error("Error en registrarPagoProveedor:", e);
    emit('error', 'Error registrando pago a proveedor');
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
.acciones {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}
.center {
  justify-content: center;
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
