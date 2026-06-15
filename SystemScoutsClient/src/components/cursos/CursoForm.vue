<template>
  <div class="persona-form">
    <header class="form-header">
      <div class="header-content">
        <h2>{{ modoVer ? 'Ver Curso' : (isTrulyNew ? 'Nuevo Curso' : 'Editar Curso') }}</h2>
        <p class="subtitle" v-if="form.CUR_DESCRIPCION">
          {{ form.CUR_CODIGO }} - {{ form.CUR_DESCRIPCION }}
        </p>
      </div>
      <div class="header-actions">
        <BaseButton variant="secondary" @click="$emit('cancel')" :disabled="isSaving">
          <AppIcons name="x" :size="18" />
          {{ modoVer ? 'Cerrar' : 'Cancelar' }}
        </BaseButton>
        <BaseButton v-if="!modoVer" variant="primary" @click="validarYGuardar" :disabled="isSaving">
          <AppIcons :name="isSaving ? 'refresh' : 'save'" :size="18" :class="{ 'spin': isSaving }" />
          {{ isSaving ? 'Guardando...' : (isTrulyNew ? 'Guardar' : 'Actualizar') }}
        </BaseButton>
      </div>
    </header>

    <div class="form-tabs">
      <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">Información</button>
      <button :class="{ active: activeTab === 'fechas' }" @click="activeTab = 'fechas'">Fechas y Cuotas</button>
      <button :class="{ active: activeTab === 'logistica' }" @click="activeTab = 'logistica'">Logística y Equipo</button>
    </div>

    <div class="form-scroll-area relative-area">
      <!-- Bloqueo de UI durante guardado -->
      <div v-if="isSaving" class="saving-overlay">
        <div class="spinner"></div>
        <span>Guardando cambios...</span>
      </div>

      <!-- TAB: INFO -->
      <div v-show="activeTab === 'info'" class="tab-content">
        <div class="form-grid">
          <!-- Información General -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="book-open" :size="18" /> Información General</h3>
            <div class="field">
              <label>Descripción del curso *</label>
              <InputBase v-model="form.CUR_DESCRIPCION" :readonly="modoVer" required />
              <small class="field-hint">Ej: Curso Básico de Primeros Auxilios</small>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Código *</label>
                <InputBase v-model="form.CUR_CODIGO" :readonly="modoVer" required />
              </div>
              <div class="field">
                <label>Tipo de Curso *</label>
                <FilterSelect v-model="form.TCU_ID" :options="options.tiposCurso" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Modalidad *</label>
                <FilterSelect v-model="form.CUR_MODALIDAD" :options="options.modalidad" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
              <div class="field">
                <label>Tipo (Presencial/Online) *</label>
                <FilterSelect v-model="form.CUR_TIPO_CURSO" :options="options.tipoPresencial" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
            </div>
          </section>

          <!-- Responsabilidad -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="users" :size="18" /> Responsabilidad y Adm.</h3>
            <div class="fields-row">
              <div class="field">
                <label>Responsable</label>
                <div class="input-with-action">
                  <FilterSelect v-model="form.PER_ID_RESPONSABLE" :options="options.personas" label-key="text" value-key="value" :disabled="modoVer" style="flex:1;" />
                  <BaseButton
                    v-if="!modoVer"
                    @click="$emit('crear-persona')"
                    variant="secondary"
                    size="sm"
                    class="btn-validate"
                    title="Crear nueva persona"
                  >
                    <AppIcons name="plus" :size="14" /> Crear
                  </BaseButton>
                </div>
              </div>
              <div class="field">
                <label>Cargo Responsable</label>
                <FilterSelect v-model="form.CAR_ID_RESPONSABLE" :options="options.cargos" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Administra</label>
                <FilterSelect v-model="form.CUR_ADMINISTRA" :options="options.administra" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
              <div class="field">
                <label>Fecha Solicitud</label>
                <InputBase type="date" v-model="form.CUR_FECHA_SOLICITUD" :readonly="modoVer" />
              </div>
            </div>
            <div class="field">
              <label>Observaciones</label>
              <textarea v-model="form.CUR_OBSERVACION" rows="3" :readonly="modoVer" class="premium-textarea"></textarea>
            </div>
          </section>

          <!-- Ubicación -->
          <section class="form-section glass-panel map-section">
            <h3 class="section-title"><AppIcons name="map-pin" :size="18" /> Ubicación</h3>
            <div class="fields-row">
              <div class="field">
                <label>Comuna (lugar) *</label>
                <FilterSelect v-model="form.COM_ID_LUGAR" :options="options.comunas" label-key="text" value-key="value" :disabled="modoVer" />
              </div>
              <div class="field" style="flex: 2;">
                <label>Lugar Específico *</label>
                <div class="input-with-action">
                  <InputBase v-model="form.CUR_LUGAR" :readonly="modoVer" placeholder="Ej: Sede Central" style="flex: 1;" />
                  <BaseButton 
                    v-if="!modoVer" 
                    @click="handleValidarDireccion" 
                    variant="secondary" 
                    size="sm" 
                    class="btn-validate"
                  >
                    <AppIcons name="search" :size="14" /> Validar
                  </BaseButton>
                </div>
              </div>
            </div>

            <!-- Mapa Interactivo -->
            <div class="field map-container" :style="modoVer ? 'pointer-events: none; opacity: 0.8;' : ''">
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
            <div class="fields-row">
              <div class="field">
                <label>Latitud *</label>
                <InputBase v-model="form.CUR_COORD_LATITUD" :readonly="modoVer" />
              </div>
              <div class="field">
                <label>Longitud *</label>
                <InputBase v-model="form.CUR_COORD_LONGITUD" :readonly="modoVer" />
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- TAB: FECHAS Y CUOTAS -->
      <div v-show="activeTab === 'fechas'" class="tab-content">
        <div v-if="!esEdicion" class="no-history">
          <AppIcons name="calendar" :size="48" />
          <p>Guarda el curso primero para gestionar fechas y cuotas.</p>
        </div>
        <div v-else class="tab-sections">
          <CursoFechas 
            :modelValue="lists.fechas"
            @update:modelValue="$emit('update:lists', { ...lists, fechas: $event })"
            :modoVer="modoVer" 
            @show-alert="$emit('show-alert', $event)"
          />
          <CursoCuotas 
            :modelValue="lists.cuotas"
            @update:modelValue="$emit('update:lists', { ...lists, cuotas: $event })"
            :modoVer="modoVer" 
            @show-alert="$emit('show-alert', $event)"
          />
        </div>
      </div>

      <!-- TAB: LOGISTICA Y EQUIPO -->
      <div v-show="activeTab === 'logistica'" class="tab-content">
        <div v-if="!esEdicion" class="no-history">
          <AppIcons name="users" :size="48" />
          <p>Guarda el curso primero para gestionar la logística y el equipo.</p>
        </div>
        <div v-else class="tab-sections">
          <CursoSecciones 
            :modelValue="lists.secciones"
            @update:modelValue="$emit('update:lists', { ...lists, secciones: $event })"
            :modoVer="modoVer" 
            :ramasOptions="options.ramas"
            @show-alert="$emit('show-alert', $event)"
          />
          <CursoFormadores 
            :modelValue="lists.formadores"
            @update:modelValue="$emit('update:lists', { ...lists, formadores: $event })"
            :modoVer="modoVer" 
            :personasOptions="options.personas"
            :rolesOptions="options.roles"
            :seccionesOptions="options.secciones"
            @show-alert="$emit('show-alert', $event)"
          />
          <CursoAlimentacion 
            :modelValue="lists.alimentaciones"
            @update:modelValue="$emit('update:lists', { ...lists, alimentaciones: $event })"
            :modoVer="modoVer" 
            :alimentacionOptions="options.alimentacion"
            @show-alert="$emit('show-alert', $event)"
          />
        </div>
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

const emit = defineEmits(['save', 'cancel', 'show-alert', 'update:lists', 'crear-persona'])

const activeTab = ref('info')
const mapRef = ref(null)

const validarYGuardar = () => {
  if (!props.form.CUR_DESCRIPCION || !props.form.CUR_DESCRIPCION.trim()) {
    activeTab.value = 'info'
    return emit('show-alert', { message: 'La descripción del curso es obligatoria.', type: 'warning' })
  }
  if (!props.form.CUR_CODIGO || !props.form.CUR_CODIGO.trim()) {
    activeTab.value = 'info'
    return emit('show-alert', { message: 'El código del curso es obligatorio.', type: 'warning' })
  }
  if (!props.form.COM_ID_LUGAR) {
    activeTab.value = 'info'
    return emit('show-alert', { message: 'La comuna donde se realiza el curso es obligatoria.', type: 'warning' })
  }
  if (!props.form.CUR_LUGAR || !props.form.CUR_LUGAR.trim()) {
    activeTab.value = 'info'
    return emit('show-alert', { message: 'El lugar específico del curso es obligatorio.', type: 'warning' })
  }
  if (!props.form.CUR_COORD_LATITUD || !props.form.CUR_COORD_LONGITUD) {
    activeTab.value = 'info'
    return emit('show-alert', { message: 'Las coordenadas de latitud y longitud son obligatorias.', type: 'warning' })
  }
  
  emit('save')
}

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
/* Base Form Layout (PersonaForm style) */
.persona-form {
  display: flex;
  flex-direction: column;
  height: 90vh;
  max-height: 850px;
  background: #f8fafc;
  border-radius: 16px;
  overflow: hidden;
}

.form-header {
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 { margin: 0; font-size: 1.5rem; color: #1a237e; }
.header-content .subtitle { margin: 4px 0 0; color: #64748b; font-weight: 500; font-size: 0.95rem; }
.header-actions { display: flex; gap: 12px; }

.form-tabs {
  display: flex;
  background: white;
  padding: 0 24px;
  border-bottom: 1px solid #e2e8f0;
  gap: 24px;
}

.form-tabs button {
  padding: 16px 4px;
  background: none;
  border: none;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.form-tabs button.active {
  color: #1a237e;
  border-bottom-color: #1a237e;
}

.form-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.relative-area {
  position: relative;
}

.tab-content { display: flex; flex-direction: column; gap: 24px; }

.glass-panel {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-section { display: flex; flex-direction: column; gap: 16px; }

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
  font-size: 1.1rem;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 12px;
}

.fields-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 0.85rem; font-weight: 600; color: #64748b; }

.premium-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.875rem;
  background: #ffffff;
  transition: all 0.2s ease;
  color: #0f172a;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  box-sizing: border-box;
}

.premium-textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}

.field-hint {
  margin-top: 4px;
  color: #6b7280;
  font-size: 12px;
}

/* Helpers */
.map-section {
  grid-column: 1 / -1;
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

/* Empty State para Pestañas no editables aún */
.no-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 20px;
  color: #94a3b8;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
  text-align: center;
  gap: 16px;
}

.tab-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Modal Saving UI Overlay */
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
  border-radius: 0 0 16px 16px;
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

@media (max-width: 1024px) {
  .form-grid { grid-template-columns: 1fr; }
  .persona-form { height: 95vh; max-height: none; }
  .fields-row { grid-template-columns: 1fr; }
}
</style>
