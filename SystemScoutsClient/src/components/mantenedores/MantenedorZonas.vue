<template>
  <div class="mantenedor-section">
    <div class="mantenedor-header">
      <h2>Gestión de Zonas</h2>
      <!-- El botón de crear ahora se gestiona desde el componente padre -->
      <!-- <button class="btn-primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="18" /> Nueva Zona
      </button> -->
    </div>

    <Teleport to="#search-container">
      <div class="search-box">
        <input 
          type="text" 
          class="search-input-new" 
          v-model="tempSearch" 
          placeholder="Buscar Zona..."
          @keyup.enter="ejecutarBusqueda"
        >
        <button class="search-btn-new" @click="ejecutarBusqueda" title="Buscar">
          <AppIcons name="search" :size="16" />
        </button>
      </div>
    </Teleport>

    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead>
            <tr>
              <th>DESCRIPCIÓN</th>
              <th>UNILATERAL</th>
              <th>ESTADO</th>
              <th class="text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="zona in filteredZonas" :key="zona.id">
              <td data-label="Descripción">{{ zona.descripcion }}</td>
              <td data-label="Unilateral">{{ zona.unilateral ? 'SÍ' : 'NO' }}</td>
              <td data-label="Estado">
                <span class="status-badge" :class="zona.vigente ? 'status-active' : 'status-inactive'">
                  {{ zona.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </td>
              <td class="actions-cell" data-label="Acciones">
                <div class="action-buttons">
                  <button class="action-btn btn-view" @click="verZona(zona)" title="Ver detalle">
                    <AppIcons name="eye" :size="16" />
                  </button>
                  <button class="action-btn btn-edit" @click="editarZona(zona)" title="Editar">
                    <AppIcons name="edit" :size="16" />
                  </button>
                  <button 
                    class="action-btn" 
                    :class="zona.vigente ? 'btn-delete' : 'btn-activate'"
                    @click="zona.vigente ? confirmarAnular(zona) : confirmarActivar(zona)"
                    :title="zona.vigente ? 'Anular' : 'Activar'"
                  >
                    <AppIcons :name="zona.vigente ? 'trash' : 'check'" :size="16" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredZonas.length === 0">
              <td colspan="4" class="no-data">No se encontraron zonas</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>

    <!-- Modal Formulario -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} ZONA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.descripcion"
                @input="form.descripcion = form.descripcion.toUpperCase()"
                placeholder="EJ: ZONA NORTE BIOBÍO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-checkbox">
                <input type="checkbox" v-model="form.unilateral">
                ZONA UNILATERAL
              </label>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal">
                <AppIcons name="close" :size="16" /> Cancelar
              </BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span>
                <span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal Ver Detalle -->
    <div v-if="viewModalVisible" class="modal-overlay" @click="cerrarViewModal">
      <div class="modal-content modal-sm" @click.stop>
        <div class="modal-header">
          <h3>👁 DETALLE ZONA</h3>
          <button class="modal-close" @click="cerrarViewModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ zonaSeleccionada?.descripcion }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">UNILATERAL:</label>
              <div class="view-value">{{ zonaSeleccionada?.unilateral ? 'SÍ' : 'NO' }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ESTADO:</label>
              <div class="view-value">
                <span class="status-badge" :class="zonaSeleccionada?.vigente ? 'status-active' : 'status-inactive'">
                  {{ zonaSeleccionada?.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </div>
            </div>
          </div>
           <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarViewModal">
                <AppIcons name="close" :size="16" /> Cerrar
              </BaseButton>
            </div>
        </div>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="cargando" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>Cargando zonas...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'

// Props para comunicar eventos al padre si es necesario (ej: mostrar toast)
const emit = defineEmits(['show-message', 'confirm-action'])
defineExpose({ abrirModalCrear })

const zonas = ref([])
const search = ref('')
const tempSearch = ref('')
const cargando = ref(false)
const saving = ref(false)

const ejecutarBusqueda = () => {
  search.value = tempSearch.value
}

// Estado Modal Formulario
const modalVisible = ref(false)
const editando = ref(false)
const form = reactive({
  id: null,
  descripcion: '',
  unilateral: false,
  vigente: true
})

// Estado Modal Ver
const viewModalVisible = ref(false)
const zonaSeleccionada = ref(null)

const cargarDatos = async () => {
  cargando.value = true
  try {
    const resp = await mantenedoresService.zona.list()
    console.log('MantenedorZonas: resp raw:', resp)
    // Normalización de datos (adaptado de mantenedores.vue original)
    const rawData = (resp && Array.isArray(resp)) ? resp : (resp?.results || resp?.data || [])
    console.log('MantenedorZonas: rawData:', rawData)
    zonas.value = rawData.map(z => ({
      id: z.zon_id ?? z.ZON_ID ?? z.id,
      descripcion: (z.zon_descripcion ?? z.ZON_DESCRIPCION ?? z.DESCRIPCION ?? z.descripcion ?? '').toString(),
      unilateral: !!(z.zon_unilateral ?? z.ZON_UNILATERAL ?? z.unilateral),
      vigente: !!(z.zon_vigente ?? z.ZON_VIGENTE ?? z.vigente ?? true)
    }))
    console.log('MantenedorZonas: zonas.value mapped:', zonas.value)
  } catch (error) {
    console.error('Error cargando zonas:', error)
    emit('show-message', { type: 'error', text: 'Error al cargar zonas' })
  } finally {
    cargando.value = false
  }
}

const filteredZonas = computed(() => {
  if (!search.value) return zonas.value
  const term = search.value.toLowerCase()
  return zonas.value.filter(z => 
    z.descripcion.toLowerCase().includes(term)
  )
})

function abrirModalCrear() {
  editando.value = false
  Object.assign(form, { id: null, descripcion: '', unilateral: false, vigente: true })
  modalVisible.value = true
}

const editarZona = (zona) => {
  editando.value = true
  Object.assign(form, { 
    id: zona.id, 
    descripcion: zona.descripcion, 
    unilateral: zona.unilateral, 
    vigente: zona.vigente 
  })
  modalVisible.value = true
}

const verZona = (zona) => {
  zonaSeleccionada.value = zona
  viewModalVisible.value = true
}

const cerrarModal = () => {
  modalVisible.value = false
  form.id = null
  editando.value = false
}

const cerrarViewModal = () => {
  viewModalVisible.value = false
  zonaSeleccionada.value = null
}

const guardar = async () => {
  saving.value = true
  try {
    const payload = {
      zon_descripcion: form.descripcion,
      zon_unilateral: form.unilateral,
      zon_vigente: form.vigente
    }
    
    if (editando.value) {
      if (!form.id) throw new Error('ID no válido')
      await mantenedoresService.zona.partialUpdate(form.id, payload)
      emit('show-message', { type: 'success', text: 'Zona actualizada correctamente' })
    } else {
      const resp = await mantenedoresService.zona.create(payload)
      const newZona = resp.data || resp 
      
      // Si es unilateral, crear distrito automáticamente
      if (form.unilateral && newZona) {
          const zonaId = newZona.zon_id ?? newZona.ZON_ID ?? newZona.id
          try {
              await mantenedoresService.distrito.create({
                  dis_descripcion: form.descripcion, // Mismo nombre que la zona
                  zon_id: zonaId,
                  dis_vigente: true
              })
          } catch(e) {
              console.error('Error creando distrito automático:', e)
              emit('show-message', { type: 'error', text: 'Zona creada pero error al crear distrito automático' })
              return // Salir para no mostrar mensaje de éxito doble o confuso
          }
      }

      emit('show-message', { type: 'success', text: 'Zona creada correctamente' })
    }
    cerrarModal()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando zona:', error)
    emit('show-message', { type: 'error', text: 'Error al guardar zona' })
  } finally {
    saving.value = false
  }
}

// Lógica de confirmación delegada al padre o manejada internamente si es simple
// Aquí delegamos la confirmación al componente padre para mantener consistencia con el modal global de confirmación si se desea
// O emitimos el evento para que el padre maneje el modal de confirmación
const confirmarAnular = (zona) => {
  emit('confirm-action', {
    titulo: 'Anular Zona',
    mensaje: `¿Estás seguro de anular la zona "${zona.descripcion}"?`,
    accion: async () => {
        try {
            await mantenedoresService.zona.partialUpdate(zona.id, { zon_vigente: false })
            await cargarDatos()
            emit('show-message', { type: 'success', text: 'Zona anulada correctamente' })
        } catch (e) {
            emit('show-message', { type: 'error', text: 'Error al anular zona' })
        }
    }
  })
}

const confirmarActivar = (zona) => {
   emit('confirm-action', {
    titulo: 'Activar Zona',
    mensaje: `¿Estás seguro de activar la zona "${zona.descripcion}"?`,
    accion: async () => {
        try {
            await mantenedoresService.zona.partialUpdate(zona.id, { zon_vigente: true })
            await cargarDatos()
            emit('show-message', { type: 'success', text: 'Zona activada correctamente' })
        } catch (e) {
            emit('show-message', { type: 'error', text: 'Error al activar zona' })
        }
    }
  })
}


onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
/* Estilos extraídos de mantenedores.vue y adaptados */
.mantenedor-section {
  position: relative;
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  /* Updated padding as requested */
  padding: 16px 0px;
  border-bottom: 2px solid #3949ab;
}

.mantenedor-header h2 {
  color: #1a237e;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

/* Nueva Caja de Búsqueda Integrada */
.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0 4px 0 12px;
  height: 40px;
  width: 100%;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.search-input-new {
  flex: 1;
  border: none !important;
  outline: none !important;
  padding: 8px 0 !important;
  font-size: 0.95rem !important;
  color: #111827 !important;
  background: transparent !important;
}

.search-btn-new {
  background: transparent !important;
  border: none !important;
  color: #6b7280;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: color 0.2s;
  height: 32px;
  width: 32px;
  margin-right: 4px;
}

.search-btn-new:hover {
  color: #1a237e;
}

.search-btn-new :deep(svg) {
  margin-right: 0 !important;
}

.search-button {
  background-color: #1a237e !important;
  height: 40px !important;
}

.search-button :deep(svg) {
  margin-right: 0 !important;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s;
  height: 40px; /* Igualar altura con dropdown y botón */
}

.search-input:focus {
  outline: none;
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.table-container {
  flex: 1;
  overflow: hidden;
  border-radius: 8px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}

.data-table th {
  background-color: #f8f9fa;
  color: #333;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 10;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-active {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-inactive {
  background-color: #ffebee;
  color: #c62828;
}

.actions-cell {
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: background 0.2s;
  color: #555;
}

.action-btn:hover {
  background-color: #f0f0f0;
}

.btn-view:hover { color: #1976d2; background-color: #e3f2fd; }
.btn-edit:hover { color: #f57c00; background-color: #fff3e0; }
.btn-delete:hover { color: #d32f2f; background-color: #ffebee; }
.btn-activate:hover { color: #388e3c; background-color: #e8f5e9; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}

.modal-sm {
  max-width: 360px;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 { margin: 0; color: #1a237e; font-size: 1.2rem; }

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: 70vh;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box; /* Important for padding */
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.view-container {
  text-align: center;
}

.view-group {
  margin-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.view-label {
  font-weight: 600;
  color: #555;
  display: block;
  font-size: 0.85rem;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.view-value {
  color: #111827;
  font-size: 1rem;
  font-weight: 500;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3949ab;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-primary {
  background: #1a237e;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: background 0.2s;
}


.btn-primary:hover {
  background: #283593;
}

/* RESPONSIVE: CARDS VIEW */
@media (max-width: 768px) {
  .mantenedor-header h2 {
    font-size: 1.25rem;
  }
  
  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    max-width: 100%;
  }

  /* Ocultar encabezados de tabla */
  .data-table thead {
    display: none;
  }

  .data-table, .data-table tbody, .data-table tr, .data-table td {
    display: block;
    width: 100%;
  }

  .data-table tr {
    margin-bottom: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }

  .data-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
    padding: 12px 16px;
    border-bottom: 1px solid #f3f4f6;
  }

  .data-table td:last-child {
    border-bottom: none;
    justify-content: center;
    padding-top: 16px;
  }

  /* Etiquetas pseudo-elementos para las columnas */
  .data-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: #6b7280;
    font-size: 0.85rem;
    text-transform: uppercase;
    margin-right: 16px;
    text-align: left;
  }
  
  /* Ajustes específicos para acciones */
  .actions-cell {
    background-color: #f9fafb;
    border-top: 1px solid #e5e7eb;
    border-radius: 0 0 8px 8px;
  }

  /* Reset de altura y scroll para vista móvil */
  .mantenedor-section {
    height: auto;
    overflow: visible;
  }

  .table-container {
    height: auto;
    overflow: visible;
  }
}
</style>
