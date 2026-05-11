<template>
  <div>
    <!-- Modal Ver Detalle -->
    <BaseModal :modelValue="modalVerDetalle" @update:modelValue="$emit('update:modalVerDetalle', $event)" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Detalle del Pago</h3>
            <BaseButton
              variant="secondary"
              size="sm"
              @click="$emit('update:modalVerDetalle', false)"
            >
              <AppIcons name="x" :size="16" /> Cerrar
            </BaseButton>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <input type="text" :value="pagoDetalle.nombre" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>RUT</label>
              <input type="text" :value="pagoDetalle.rut" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Curso</label>
              <input type="text" :value="pagoDetalle.curso" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Grupo</label>
              <input type="text" :value="pagoDetalle.grupo" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Concepto</label>
              <input type="text" :value="pagoDetalle.concepto" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Monto</label>
              <input type="text" :value="pagoDetalle.monto" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Fecha de Pago</label>
              <input type="text" :value="pagoDetalle.fecha" readonly disabled class="detail-input" />
            </div>
            <div class="row">
              <label>Método de Pago</label>
              <input type="text" :value="pagoDetalle.metodo" readonly disabled class="detail-input" />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <textarea 
                class="comentario-input" 
                :value="pagoDetalle.observacion" 
                readonly
                disabled
              ></textarea>
            </div>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Editar -->
    <BaseModal :modelValue="modalEditar" @update:modelValue="$emit('update:modalEditar', $event)" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <div class="header-actions">
              <BaseButton
                class="btn-save"
                variant="primary"
                @click="$emit('guardar-edicion')"
                :disabled="loading"
              >
                <AppIcons :name="loading ? 'clock' : 'save'" :size="16" />
                {{ loading ? 'Guardando...' : 'Guardar' }}
              </BaseButton>
            </div>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <InputBase v-model="pagoEdit.nombre" readonly />
            </div>
            <div class="row">
              <label>RUT</label>
              <InputBase v-model="pagoEdit.rut" readonly />
            </div>
            <div class="row">
              <label>Curso</label>
              <BaseSelect v-model="pagoEdit.curso" :options="cursoOptions" />
            </div>
            <div class="row">
              <label>Monto</label>
              <InputBase type="number" v-model.number="pagoEdit.monto" />
            </div>
            <div class="row">
              <label>Fecha</label>
              <InputBase type="date" v-model="pagoEdit.fecha" />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <InputBase v-model="pagoEdit.observacion" />
            </div>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Confirmar Cambios de Edición -->
    <BaseModal :modelValue="modalConfirmarEdicion" @update:modelValue="$emit('update:modalConfirmarEdicion', $event)" class="pago-modal">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">✏️</div>
          <p style="font-weight: 600; margin-bottom: 12px;">Se modificarán los siguientes campos:</p>
          <div style="text-align: left; background: #f9fafb; padding: 12px; border-radius: 6px; margin-bottom: 16px;">
            <div v-for="(cambio, index) in cambiosDetectados" :key="index" style="margin-bottom: 6px; font-size: 13px;">
              • {{ cambio }}
            </div>
          </div>
          <p style="font-weight: 600;">¿Está seguro de guardar estos cambios?</p>
          <div class="confirm-actions modal-actions">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="$emit('cancelar-edicion')"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="success"
              class="btn-modal"
              @click="$emit('confirmar-edicion')"
            >
              <AppIcons name="check" :size="16" /> Guardar
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Transferir -->
    <BaseModal :modelValue="modalTransferir" @update:modelValue="$emit('update:modalTransferir', $event)" title="Transferir Pago">
      <template #default>
        <div class="modal-transfer">
          <h3>Transferir pago de {{ pagoTransferir?.persona_nombre }}</h3>
          <p class="muted">Busca al participante al que deseas transferir el pago.</p>

          <!-- Buscador de personas para transferencia -->
          <div class="row-buscar">
            <div class="buscar-input">
              <InputBase
                v-model="transferForm.q"
                placeholder="Buscar por RUT o nombre..."
                @keydown.enter.prevent="buscarPersonaParaTransferir"
              />
            </div>
            <BaseButton variant="primary" @click="buscarPersonaParaTransferir">Buscar</BaseButton>
          </div>
          <div v-if="buscandoPersonasTransferir" class="estado-carga">
            <div class="spinner"></div> Buscando...
          </div>
          <div v-if="personasEncontradasTransferir.length" class="resultados">
             <div
              v-for="p in personasEncontradasTransferir"
              :key="p.id"
              class="resultado"
              @click="seleccionarPersonaParaTransferir(p)"
            >
              <div class="resultado-left">
                <strong>{{ p.nombre }}</strong>
                <span class="muted">{{ p.rut }}</span>
              </div>
              <BaseButton size="sm" variant="secondary" class="btn-action">Elegir</BaseButton>
            </div>
          </div>

          <div class="form-fields-grid mt-4">
            <div class="row">
              <label>Nombre nuevo participante</label>
              <InputBase v-model="transferForm.nombre" readonly placeholder="Selecciona una persona" />
            </div>
            <div class="row">
              <label>RUT nuevo participante</label>
              <InputBase v-model="transferForm.rut" readonly />
            </div>
            <div class="row">
              <label>Tipo de devolución</label>
              <select v-model="transferForm.tipo" disabled class="base-select">
                <option value="total">Devolución / Transferencia Total</option>
                <option value="parcial">Devolución / Transferencia Parcial</option>
              </select>
            </div>
            <div class="row" v-if="transferForm.tipo === 'parcial'">
              <label>Monto a transferir</label>
              <input
                type="number"
                min="0"
                disabled
                v-model.number="transferForm.monto_parcial"
                class="base-input"
              />
            </div>
          </div>

          <div class="confirm-actions modal-actions mt-4">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="$emit('update:modalTransferir', false)"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="primary"
              class="btn-modal"
              @click="$emit('confirmar-transferencia', transferForm)"
              :disabled="!transferForm.personaId || loading"
            >
              <AppIcons name="check" :size="16" /> Confirmar
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Anular -->
    <BaseModal :modelValue="modalAnular" @update:modelValue="$emit('update:modalAnular', $event)" title="Confirmar Anulación">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">⚠️</div>
          <p>¿Anular pago de <strong>{{ pagoAnular?.persona_nombre }}</strong>?</p>
          <div class="confirm-actions modal-actions">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="$emit('update:modalAnular', false)"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="danger"
              class="btn-modal"
              @click="$emit('confirmar-anulacion')"
            >
              <AppIcons name="trash" :size="16" /> Anular
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '@/components/BaseModal.vue';
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import InputBase from '@/components/InputBase.vue';
import BaseSelect from '@/components/BaseSelect.vue';
import personasService from '@/services/personasService.js';

const props = defineProps({
  modalVerDetalle: Boolean,
  modalEditar: Boolean,
  modalConfirmarEdicion: Boolean,
  modalTransferir: Boolean,
  modalAnular: Boolean,
  pagoDetalle: { type: Object, default: () => ({}) },
  pagoEdit: { type: Object, default: () => ({}) },
  pagoAnular: { type: Object, default: () => null },
  pagoTransferir: { type: Object, default: () => null },
  cambiosDetectados: { type: Array, default: () => [] },
  cursoOptions: { type: Array, default: () => [] },
  loading: Boolean
});

const emit = defineEmits([
  'update:modalVerDetalle',
  'update:modalEditar',
  'update:modalConfirmarEdicion',
  'update:modalTransferir',
  'update:modalAnular',
  'guardar-edicion',
  'cancelar-edicion',
  'confirmar-edicion',
  'confirmar-transferencia',
  'confirmar-anulacion'
]);

const transferForm = reactive({
  q: '',
  personaId: null,
  nombre: '',
  rut: '',
  email: '',
  tipo: 'total',
  monto_parcial: null
});

const buscandoPersonasTransferir = ref(false);
const personasEncontradasTransferir = ref([]);

async function buscarPersonaParaTransferir() {
  const qRaw = (transferForm.q || '').trim();
  if (!qRaw) {
    personasEncontradasTransferir.value = [];
    return;
  }

  const termClean = qRaw.replace(/[\.\-\s]/g, '');
  let params = {};
  if (/^\d{7,8}[0-9kK]$/i.test(termClean)) {
    const rutMatch = termClean.match(/^(\d{7,8})([0-9kK])$/i);
    if (rutMatch) {
      params = { run: rutMatch[1], dv: rutMatch[2].toUpperCase() };
    }
  } else if (/^\d+$/.test(termClean)) {
    params = { run: termClean };
  } else {
    const parts = qRaw.split(/\s+/);
    if (parts.length === 1) params = { nombre: qRaw };
    else params = { nombre: parts[0], apellido: parts.slice(1).join(' ') };
  }

  buscandoPersonasTransferir.value = true;
  try {
    const response = await personasService.personas.list(params);
    const arr = response.results || response || [];
    personasEncontradasTransferir.value = arr.map(p => ({
      id: p.per_id || p.PER_ID || p.id,
      nombre: `${p.per_nombres || p.PER_NOMBRES || ''} ${p.per_apelpta || p.PER_APELPTA || ''}`.trim(),
      rut: (p.per_run || p.PER_RUN) ? `${p.per_run || p.PER_RUN}-${p.per_dv || p.PER_DV || ''}` : '',
      email: p.per_mail || p.PER_MAIL || ''
    }));
  } catch {
    personasEncontradasTransferir.value = [];
  } finally {
    buscandoPersonasTransferir.value = false;
  }
}

function seleccionarPersonaParaTransferir(p) {
  transferForm.personaId = p.id;
  transferForm.nombre = p.nombre;
  transferForm.rut = p.rut;
  transferForm.email = p.email;
  personasEncontradasTransferir.value = [];
  transferForm.q = p.nombre;
}
</script>

<style scoped>
.modal-edit {
  padding: 10px;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 10px;
}
.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1a237e;
}
.form-fields-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.row.full-width {
  grid-column: span 2;
}
label {
  font-weight: 600;
  color: #374151;
  font-size: 13px;
}
.detail-input {
  background: #f9fafb;
  border: 1px solid #d1d5db;
  padding: 8px 10px;
  border-radius: 6px;
  color: #374151;
  pointer-events: none;
  cursor: not-allowed;
  width: 100%;
}
.comentario-input {
  width: 100%;
  min-height: 80px;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  resize: none;
  background: #f9fafb;
  color: #374151;
  pointer-events: none;
  cursor: not-allowed;
  font-family: inherit;
  font-size: 13px;
}
.confirm-content {
  text-align: center;
  padding: 10px;
}
.confirm-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}
.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}
.modal-actions {
  padding-top: 10px;
}
.btn-modal {
  min-width: 120px;
}
.row-buscar {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.buscar-input {
  flex: 1;
}
.resultados {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 4px;
  background: #ffffff;
  max-height: 200px;
  overflow-y: auto;
  position: absolute;
  width: 100%;
  z-index: 100;
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
.base-select, .base-input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.mt-4 {
  margin-top: 1rem;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
