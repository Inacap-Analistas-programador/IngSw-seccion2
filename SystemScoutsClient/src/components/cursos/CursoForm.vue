<template>
  <div class="curso-form-container">

    <div class="modal-body-custom">
      <!-- Bloqueo de UI durante guardado -->
      <div v-if="isSaving" class="saving-overlay">
        <div class="spinner"></div>
        <span>Guardando cambios...</span>
      </div>

      <div class="form-grid-modal">
        <!-- ... existing grid content ... -->
        <div class="form-group span-2">
          <label>Descripción del curso</label>
          <InputBase v-model="form.CUR_DESCRIPCION" :disabled="modoVer" />
          <small class="field-hint">Ej: Curso Básico de Primeros Auxilios</small>
        </div>
        <div class="form-group"><label>Código</label><InputBase v-model="form.CUR_CODIGO" :disabled="modoVer" /></div>
        <div class="form-group">
          <label>Tipo de Curso</label>
          <FilterSelect v-model="form.TCU_ID" :options="options.tiposCurso" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona el tipo de curso</small>
        </div>
        <div class="form-group">
          <label>Responsable</label>
          <FilterSelect v-model="form.PER_ID_RESPONSABLE" :options="options.personas" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona a la persona responsable</small>
        </div>
        <div class="form-group">
          <label>Cargo</label>
          <FilterSelect v-model="form.CAR_ID_RESPONSABLE" :options="options.cargos" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona el cargo del responsable</small>
        </div>
        <div class="form-group">
          <label>Fecha de Solicitud</label>
          <InputBase type="date" v-model="form.CUR_FECHA_SOLICITUD" :disabled="modoVer" />
          <small class="field-hint">Formato: AAAA-MM-DD (Ej: 2025-11-12)</small>
        </div>
        <div class="form-group">
          <label>Modalidad</label>
          <FilterSelect v-model="form.CUR_MODALIDAD" :options="options.modalidad" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona la modalidad</small>
        </div>
        <div class="form-group">
          <label>Tipo (Presencial/Online)</label>
          <FilterSelect v-model="form.CUR_TIPO_CURSO" :options="options.tipoPresencial" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona si es presencial u online</small>
        </div>
        <div class="form-group">
          <label>Administra</label>
          <FilterSelect v-model="form.CUR_ADMINISTRA" :options="options.administra" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Indica quién administra el curso</small>
        </div>
        <div class="form-group">
          <label>Comuna (lugar)</label>
          <FilterSelect v-model="form.COM_ID_LUGAR" :options="options.comunas" labelKey="text" valueKey="value" :disabled="modoVer" />
          <small class="field-hint">Selecciona la comuna donde se realiza</small>
        </div>
        <div class="form-group span-2">
          <label>Lugar</label>
          <div class="input-with-action">
            <InputBase v-model="form.CUR_LUGAR" :disabled="modoVer" placeholder="Ej: Sede Central, Sala 3 o una dirección completa" />
            <BaseButton 
              v-if="!modoVer" 
              @click="handleValidarDireccion" 
              variant="secondary" 
              size="sm" 
              class="btn-validate"
              title="Buscar en el mapa"
            >
              <AppIcons name="search" :size="14" /> Validar
            </BaseButton>
          </div>
          <small class="field-hint">Ej: Sede Central, Sala 3</small>
        </div>
        
        <!-- Mapa Interactivo -->
        <div class="form-group span-2" :style="modoVer ? 'pointer-events: none; opacity: 0.8;' : ''">
          <label>Ubicación (haz clic en el mapa o arrastra el marcador)</label>
          <MapEmbed
            ref="mapRef"
            :lat="form.CUR_COORD_LATITUD"
            :lng="form.CUR_COORD_LONGITUD"
            @update:lat="form.CUR_COORD_LATITUD = $event"
            @update:lng="form.CUR_COORD_LONGITUD = $event"
            @update:address="handleAddressUpdate"
          />
        </div>
        <div class="form-group"><label>Latitud</label><InputBase v-model="form.CUR_COORD_LATITUD" placeholder="Lat" :disabled="modoVer" /><small class="field-hint">Ej: -36.827 (Concepción)</small></div>
        <div class="form-group"><label>Longitud</label><InputBase v-model="form.CUR_COORD_LONGITUD" placeholder="Lng" :disabled="modoVer" /><small class="field-hint">Ej: -73.050 (Concepción)</small></div>

        <div class="form-group span-2"><label>Observaciones</label><textarea v-model="form.CUR_OBSERVACION" rows="3" :disabled="modoVer" class="base-textarea"></textarea><small class="field-hint">Notas internas, ej: traer proyector</small></div>
      </div>

      <!-- Sección de Gestión de Fechas -->
      <CursoFechas 
        v-if="esEdicion" 
        :modelValue="lists.fechas"
        @update:modelValue="$emit('update:lists', { ...lists, fechas: $event })"
        :modoVer="modoVer" 
        @show-alert="$emit('show-alert', $event)"
      />

      <!-- Sección de Gestión de Secciones -->
      <CursoSecciones 
        v-if="esEdicion" 
        :modelValue="lists.secciones"
        @update:modelValue="$emit('update:lists', { ...lists, secciones: $event })"
        :modoVer="modoVer" 
        :ramasOptions="options.ramas"
        @show-alert="$emit('show-alert', $event)"
      />

      <!-- Sección Equipo Formadores -->
      <CursoFormadores 
        v-if="esEdicion" 
        :modelValue="lists.formadores"
        @update:modelValue="$emit('update:lists', { ...lists, formadores: $event })"
        :modoVer="modoVer" 
        :personasOptions="options.personas"
        :rolesOptions="options.roles"
        :seccionesOptions="options.secciones"
        @show-alert="$emit('show-alert', $event)"
      />

      <CursoAlimentacion 
        v-if="esEdicion" 
        :modelValue="lists.alimentaciones"
        @update:modelValue="$emit('update:lists', { ...lists, alimentaciones: $event })"
        :modoVer="modoVer" 
        :alimentacionOptions="options.alimentacion"
        @show-alert="$emit('show-alert', $event)"
      />

      <!-- Sección Cuotas del Curso -->
      <CursoCuotas 
        v-if="esEdicion" 
        :modelValue="lists.cuotas"
        @update:modelValue="$emit('update:lists', { ...lists, cuotas: $event })"
        :modoVer="modoVer" 
        @show-alert="$emit('show-alert', $event)"
      />

      <!-- Acciones del Formulario al final -->
      <div class="form-actions" v-if="!modoVer">
        <BaseButton @click="$emit('cancel')" variant="secondary" :disabled="isSaving">
          <AppIcons name="close" :size="16" /> Cancelar
        </BaseButton>
        <BaseButton @click="$emit('save')" variant="primary" :disabled="isSaving">
          <AppIcons :name="isSaving ? 'clock' : 'save'" :size="16" />
          <span v-if="!isSaving">{{ isTrulyNew ? 'GUARDAR' : 'ACTUALIZAR' }}</span>
          <span v-else>Procesando...</span>
        </BaseButton>
      </div>
      <div class="form-actions" v-else>
        <BaseButton @click="$emit('cancel')" variant="secondary">
          <AppIcons name="close" :size="16" /> Cerrar
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InputBase from '@/components/InputBase.vue'
import BaseButton from '@/components/BaseButton.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import MapEmbed from '@/components/MapEmbed.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

// Import Sub-components
import CursoFechas from './CursoFechas.vue'
import CursoSecciones from './CursoSecciones.vue'
import CursoFormadores from './CursoFormadores.vue'
import CursoAlimentacion from './CursoAlimentacion.vue'
import CursoCuotas from './CursoCuotas.vue'

const props = defineProps({
  form: Object,
  lists: Object,
  options: Object,
  modoVer: Boolean,
  isTrulyNew: Boolean,
  esEdicion: Boolean,
  isSaving: Boolean
})

const emit = defineEmits(['save', 'cancel', 'show-alert', 'update:lists'])

const mapRef = ref(null)

const handleAddressUpdate = (newAddress) => {
  if (newAddress && !props.modoVer) {
    props.form.CUR_LUGAR = newAddress
  }
}

const handleValidarDireccion = async () => {
  if (!props.form.CUR_LUGAR || props.form.CUR_LUGAR.length < 3) {
    emit('show-alert', { message: 'Ingresa una dirección más específica para buscar.', type: 'warning' })
    return
  }
  
  if (mapRef.value) {
    const result = await mapRef.value.buscarDireccion(props.form.CUR_LUGAR)
    if (result) {
      emit('show-alert', { message: 'Dirección encontrada y ubicada en el mapa.', type: 'success' })
    } else {
      emit('show-alert', { message: 'No se pudo encontrar la dirección exacta. Intenta con más detalles.', type: 'error' })
    }
  }
}
</script>

<style scoped>
/* Copied from CRUDcursos.vue but scoped */
.curso-form-container {
  padding: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.modal-body-custom {
  max-height: 75vh;
}

.form-grid-modal {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

@media (max-width: 600px) {
  .form-grid-modal {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .form-group.span-2 {
    grid-column: auto;
  }
}

.saving-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-weight: 500;
  color: #2563eb;
  backdrop-filter: blur(2px);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.input-with-action {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-validate {
  height: 40px;
  padding: 0 16px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.input-with-action .base-input-container {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 0.875rem;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-group :deep(input), 
.form-group :deep(select), 
.form-group :deep(textarea),
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.875rem;
  background: #ffffff;
  transition: all 0.2s ease;
  color: #0f172a;
}

.form-group :deep(input:focus), .form-group :deep(select:focus), .form-group :deep(textarea:focus),
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}

.field-hint {
  margin-top: 4px;
  color: #6b7280;
  font-size: 12px;
}

.base-textarea {
  resize: vertical;
  min-height: 80px;
}

.section-divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 24px 0;
}
</style>
