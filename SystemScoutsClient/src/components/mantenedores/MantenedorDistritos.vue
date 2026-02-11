<template>
  <div class="mantenedor-section">
    <div class="mantenedor-header">
      <h2><AppIcons name="map" :size="24" /> Gestión de Distritos</h2>
      <button class="btn-primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="18" /> Nuevo Distrito
      </button>
    </div>

    <div class="search-bar">
      <input 
        type="text" 
        class="search-input" 
        v-model="search" 
        placeholder="Buscar Distrito..."
      >
      <select class="select-filter" v-model="filtroZona">
        <option value="">TODAS LAS ZONAS</option>
        <option v-for="zona in zonas" :key="zona.id" :value="zona.id">
          {{ zona.descripcion }}
        </option>
      </select>
    </div>

    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead>
            <tr>
              <th>DESCRIPCIÓN</th>
              <th>ZONA</th>
              <th>ESTADO</th>
              <th class="text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="distrito in filteredDistritos" :key="distrito.id">
              <td>{{ distrito.descripcion }}</td>
              <td>{{ getZonaNombre(distrito.zona_id) }}</td>
              <td>
                <span class="status-badge" :class="distrito.vigente ? 'status-active' : 'status-inactive'">
                  {{ distrito.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <button class="action-btn btn-view" @click="verDistrito(distrito)" title="Ver detalle">
                    <AppIcons name="eye" :size="16" />
                  </button>
                  <button class="action-btn btn-edit" @click="editarDistrito(distrito)" title="Editar">
                    <AppIcons name="edit" :size="16" />
                  </button>
                  <button 
                    class="action-btn" 
                    :class="distrito.vigente ? 'btn-delete' : 'btn-activate'"
                    @click="distrito.vigente ? confirmarAnular(distrito) : confirmarActivar(distrito)"
                    :title="distrito.vigente ? 'Anular' : 'Activar'"
                  >
                    <AppIcons :name="distrito.vigente ? 'trash' : 'check'" :size="16" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredDistritos.length === 0">
              <td colspan="4" class="no-data">No se encontraron distritos</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>

    <!-- Modal Formulario -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} DISTRITO</h3>
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
                placeholder="EJ: DISTRITO CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">ZONA:</label>
              <select class="form-control" v-model="form.zona_id" required>
                <option :value="null" disabled>SELECCIONE ZONA</option>
                <option v-for="zona in zonas" :key="zona.id" :value="zona.id">
                  {{ zona.descripcion }}
                </option>
              </select>
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
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 DETALLE DISTRITO</h3>
          <button class="modal-close" @click="cerrarViewModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ distritoSeleccionado?.descripcion }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ZONA:</label>
              <div class="view-value">{{ getZonaNombre(distritoSeleccionado?.zona_id) }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ESTADO:</label>
              <div class="view-value">
                <span class="status-badge" :class="distritoSeleccionado?.vigente ? 'status-active' : 'status-inactive'">
                  {{ distritoSeleccionado?.vigente ? 'ACTIVO' : 'INACTIVO' }}
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
        <p>Cargando datos...</p>
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

const emit = defineEmits(['show-message', 'confirm-action'])

const distritos = ref([])
const zonas = ref([])
const search = ref('')
const filtroZona = ref('')
const cargando = ref(false)
const saving = ref(false)

// Estado Modal Formulario
const modalVisible = ref(false)
const editando = ref(false)
const form = reactive({
  id: null,
  descripcion: '',
  zona_id: null,
  vigente: true
})

// Estado Modal Ver
const viewModalVisible = ref(false)
const distritoSeleccionado = ref(null)

const cargarDatos = async () => {
  cargando.value = true
  try {
    const [respDistritos, respZonas] = await Promise.all([
      mantenedoresService.distrito.list().catch(e => { console.error('Distritos:', e); return [] }),
      mantenedoresService.zona.list().catch(e => { console.error('Zonas:', e); return [] })
    ])
    
    // Normalizar Zonas
    const rawZonas = Array.isArray(respZonas) ? respZonas : (respZonas.results || respZonas.data || [])
    zonas.value = rawZonas.map(z => ({
      id: z.zon_id ?? z.ZON_ID ?? z.id,
      descripcion: (z.zon_descripcion ?? z.ZON_DESCRIPCION ?? z.DESCRIPCION ?? z.descripcion ?? '').toString()
    }))

    // Normalizar Distritos
    const rawDistritos = Array.isArray(respDistritos) ? respDistritos : (respDistritos.results || respDistritos.data || [])
    distritos.value = rawDistritos.map(d => ({
      id: d.dis_id ?? d.DIS_ID ?? d.id,
      descripcion: (d.dis_descripcion ?? d.DIS_DESCRIPCION ?? d.DESCRIPCION ?? d.descripcion ?? '').toString(),
      zona_id: (d.zon_id?.zon_id ?? d.ZON_ID?.ZON_ID ?? d.zon_id ?? d.ZON_ID ?? d.zona_id ?? null),
      vigente: !!(d.dis_vigente ?? d.DIS_VIGENTE ?? d.vigente ?? true)
    }))

  } catch (error) {
    console.error('Error cargando datos:', error)
    emit('show-message', { type: 'error', text: 'Error al cargar datos' })
  } finally {
    cargando.value = false
  }
}

const filteredDistritos = computed(() => {
  let filtered = distritos.value
  
  if (search.value) {
    filtered = filtered.filter(d => 
      d.descripcion.toLowerCase().includes(search.value.toLowerCase())
    )
  }
  
  if (filtroZona.value) {
    filtered = filtered.filter(d => d.zona_id === filtroZona.value)
  }
  
  return filtered
})

const getZonaNombre = (zonaId) => {
  const zona = zonas.value.find(z => z.id === zonaId)
  return zona ? zona.descripcion : 'NO ENCONTRADA'
}

const abrirModalCrear = () => {
  editando.value = false
  Object.assign(form, { id: null, descripcion: '', zona_id: null, vigente: true })
  modalVisible.value = true
}

const editarDistrito = (distrito) => {
  editando.value = true
  Object.assign(form, { 
    id: distrito.id, 
    descripcion: distrito.descripcion, 
    zona_id: distrito.zona_id, 
    vigente: distrito.vigente 
  })
  modalVisible.value = true
}

const verDistrito = (distrito) => {
  distritoSeleccionado.value = distrito
  viewModalVisible.value = true
}

const cerrarModal = () => {
  modalVisible.value = false
  form.id = null
  editando.value = false
}

const cerrarViewModal = () => {
  viewModalVisible.value = false
  distritoSeleccionado.value = null
}

const guardar = async () => {
  saving.value = true
  try {
    const payload = {
      dis_descripcion: form.descripcion,
      zon_id: form.zona_id,
      dis_vigente: form.vigente
    }
    
    if (editando.value) {
      if (!form.id) throw new Error('ID no válido')
      await mantenedoresService.distrito.partialUpdate(form.id, payload)
      emit('show-message', { type: 'success', text: 'Distrito actualizado correctamente' })
    } else {
      await mantenedoresService.distrito.create(payload)
      emit('show-message', { type: 'success', text: 'Distrito creado correctamente' })
    }
    cerrarModal()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando distrito:', error)
    emit('show-message', { type: 'error', text: 'Error al guardar distrito' })
  } finally {
    saving.value = false
  }
}

const confirmarAnular = (distrito) => {
  emit('confirm-action', {
    titulo: 'Anular Distrito',
    mensaje: `¿Estás seguro de anular el distrito "${distrito.descripcion}"?`,
    accion: async () => {
        try {
            await mantenedoresService.distrito.partialUpdate(distrito.id, { dis_vigente: false })
            await cargarDatos()
            emit('show-message', { type: 'success', text: 'Distrito anulado correctamente' })
        } catch (e) {
            emit('show-message', { type: 'error', text: 'Error al anular distrito' })
        }
    }
  })
}

const confirmarActivar = (distrito) => {
   emit('confirm-action', {
    titulo: 'Activar Distrito',
    mensaje: `¿Estás seguro de activar el distrito "${distrito.descripcion}"?`,
    accion: async () => {
        try {
            await mantenedoresService.distrito.partialUpdate(distrito.id, { dis_vigente: true })
            await cargarDatos()
            emit('show-message', { type: 'success', text: 'Distrito activado correctamente' })
        } catch (e) {
            emit('show-message', { type: 'error', text: 'Error al activar distrito' })
        }
    }
  })
}

onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
/* Reutilizando estilos base */
.mantenedor-section {
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
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
  margin-bottom: 20px;
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.select-filter {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  min-width: 200px;
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
  text-align: left;
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

.view-group {
  margin-bottom: 15px;
  border-bottom: 1px solid #f9f9f9;
  padding-bottom: 10px;
}

.view-label {
  font-weight: 600;
  color: #555;
  display: block;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.view-value {
  color: #333;
  font-size: 1rem;
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
</style>
