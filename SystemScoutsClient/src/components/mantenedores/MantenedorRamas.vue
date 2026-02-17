<template>
  <div class="mantenedor-section">
    <div class="mantenedor-header">
      <h2><AppIcons name="git-branch" :size="24" /> Gestión de Ramas</h2>
      <!-- <button class="btn-primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="18" /> Nueva Rama
      </button> -->
    </div>

    <Teleport to="#search-container">
      <div class="search-box">
        <input 
          type="text" 
          class="search-input-new" 
          v-model="tempSearch" 
          placeholder="Buscar Rama..."
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
              <th>ESTADO</th>
              <th class="text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rama in filteredItems" :key="rama.id">
              <td data-label="Descripción">{{ rama.descripcion }}</td>
              <td data-label="Estado">
                <span class="status-badge" :class="rama.vigente ? 'status-active' : 'status-inactive'">
                  {{ rama.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </td>
              <td class="actions-cell" data-label="Acciones">
                <div class="action-buttons">
                  <button class="action-btn btn-view" @click="verElemento(rama)" title="Ver detalle">
                    <AppIcons name="eye" :size="16" />
                  </button>
                  <button class="action-btn btn-edit" @click="editarElemento(rama)" title="Editar">
                    <AppIcons name="edit" :size="16" />
                  </button>
                  <button 
                    class="action-btn" 
                    :class="rama.vigente ? 'btn-delete' : 'btn-activate'"
                    @click="rama.vigente ? confirmarAnular(rama) : confirmarActivar(rama)"
                    :title="rama.vigente ? 'Anular' : 'Activar'"
                  >
                    <AppIcons :name="rama.vigente ? 'trash' : 'check'" :size="16" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredItems.length === 0">
              <td colspan="3" class="no-data">No se encontraron ramas</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>

    <!-- Modal Formulario -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} RAMA</h3>
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
                placeholder="EJ: LOBATOS"
                required
              >
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
          <h3>👁 DETALLE RAMA</h3>
          <button class="modal-close" @click="cerrarViewModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado?.descripcion }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ESTADO:</label>
              <div class="view-value">
                <span class="status-badge" :class="elementoSeleccionado?.vigente ? 'status-active' : 'status-inactive'">
                  {{ elementoSeleccionado?.vigente ? 'ACTIVO' : 'INACTIVO' }}
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
        <p>Cargando ramas...</p>
      </div>
    </div>

    <!-- Notification Toast -->
    <NotificationToast 
      v-if="toast.visible" 
      :message="toast.message" 
      :icon="toast.icon" 
      @close="toast.visible = false" 
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import NotificationToast from '@/components/NotificationToast.vue'

const emit = defineEmits(['confirm-action'])
defineExpose({ abrirModalCrear })


const items = ref([])
const search = ref('')
const tempSearch = ref('')
const cargando = ref(false)
const saving = ref(false)

const ejecutarBusqueda = () => {
  search.value = tempSearch.value
}

// Toast state
const toast = reactive({ visible: false, message: '', icon: '' })
const showToast = (message, icon = 'check') => {
  toast.message = message
  toast.icon = icon
  toast.visible = true
  setTimeout(() => { toast.visible = false }, 3000)
}

// Estado Modal Formulario
const modalVisible = ref(false)
const editando = ref(false)
const form = reactive({
  id: null,
  descripcion: '',
  vigente: true
})

// Estado Modal Ver
const viewModalVisible = ref(false)
const elementoSeleccionado = ref(null)

const cargarDatos = async () => {
  cargando.value = true
  try {
    const resp = await mantenedoresService.rama.list()
    const rawData = (resp && Array.isArray(resp)) ? resp : (resp?.results || resp?.data || [])
    items.value = rawData.map(r => ({
      id: r.ram_id ?? r.RAM_ID ?? r.id,
      descripcion: (r.ram_descripcion ?? r.RAM_DESCRIPCION ?? r.DESCRIPCION ?? r.descripcion ?? '').toString(),
      vigente: !!(r.ram_vigente ?? r.RAM_VIGENTE ?? r.vigente ?? true)
    }))
  } catch (error) {
    console.error('Error cargando ramas:', error)
    showToast('Error al cargar ramas', 'alert-triangle')
  } finally {
    cargando.value = false
  }
}

const filteredItems = computed(() => {
  if (!search.value) return items.value
  const term = search.value.toLowerCase()
  return items.value.filter(r => r.descripcion.toLowerCase().includes(term))
})

function abrirModalCrear() {
  editando.value = false
  Object.assign(form, { id: null, descripcion: '', vigente: true })
  modalVisible.value = true
}

const editarElemento = (item) => {
  editando.value = true
  Object.assign(form, { id: item.id, descripcion: item.descripcion, vigente: item.vigente })
  modalVisible.value = true
}

const verElemento = (item) => {
  elementoSeleccionado.value = item
  viewModalVisible.value = true
}

const cerrarModal = () => {
  modalVisible.value = false
  form.id = null
  editando.value = false
}

const cerrarViewModal = () => {
  viewModalVisible.value = false
  elementoSeleccionado.value = null
}

const guardar = async () => {
  saving.value = true
  try {
    const payload = {
      ram_descripcion: form.descripcion,
      ram_vigente: form.vigente
    }
    if (editando.value) {
      if (!form.id) throw new Error('ID no válido')
      await mantenedoresService.rama.partialUpdate(form.id, payload)
      showToast('Rama actualizada correctamente', 'check')
    } else {
      await mantenedoresService.rama.create(payload)
      showToast('Rama creada correctamente', 'check')
    }
    cerrarModal()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando rama:', error)
    showToast('Error al guardar rama', 'alert-triangle')
  } finally {
    saving.value = false
  }
}

const confirmarAnular = (item) => {
  emit('confirm-action', {
    titulo: 'Anular Rama',
    mensaje: `¿Estás seguro de anular la rama "${item.descripcion}"?`,
    accion: async () => {
      try {
        await mantenedoresService.rama.partialUpdate(item.id, { ram_vigente: false })
        await cargarDatos()
        showToast('Rama anulada correctamente', 'check')
      } catch (e) {
        showToast('Error al anular rama', 'alert-triangle')
      }
    }
  })
}

const confirmarActivar = (item) => {
  emit('confirm-action', {
    titulo: 'Activar Rama',
    mensaje: `¿Estás seguro de activar la rama "${item.descripcion}"?`,
    accion: async () => {
      try {
        await mantenedoresService.rama.partialUpdate(item.id, { ram_vigente: true })
        await cargarDatos()
        showToast('Rama activada correctamente', 'check')
      } catch (e) {
        showToast('Error al activar rama', 'alert-triangle')
      }
    }
  })
}

onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
/* Estilos estandarizados basados en MantenedorZonas */
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
  padding-bottom: 15px;
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

.search-bar {
  margin-bottom: 0;
  width: 100%;
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
  height: 40px;
}

.search-input:focus {
  outline: none;
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.table-container {
  flex: 1;
  overflow: hidden;
  border: 1px solid #eee;
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
  box-sizing: border-box;
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

.modal-sm {
  max-width: 360px;
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

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}

.text-center {
  text-align: center;
}

@media (max-width: 768px) {
  .mantenedor-header h2 { font-size: 1.25rem; }
  .search-bar { flex-direction: column; align-items: stretch; }
  .search-input { max-width: 100%; }
  
  .mantenedor-section { height: auto; overflow: visible; }
  .table-container { height: auto; overflow: visible; }
  .data-table thead { display: none; }
  .data-table, .data-table tbody, .data-table tr, .data-table td { display: block; width: 100%; }
  .data-table tr { margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); background: white; }
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
  .action-buttons { justify-content: space-evenly; width: 100%; }
}
</style>
