<template>
  <div class="mantenedor-section">
    <div class="mantenedor-header">
      <h2>Gestión de Comunas</h2>
      <!-- <button class="btn-primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="18" /> Nueva Comuna
      </button> -->
    </div>

    <Teleport to="#search-container">
      <div class="search-group">
        <SearchBar 
          v-model="tempSearch" 
          placeholder="Buscar Comuna..." 
          @search="ejecutarBusqueda" 
        />
        <FilterSelect 
          v-model="filtroProvincia" 
          :options="provinciasActivas" 
          defaultLabel="Todas las Provincias" 
        />
      </div>
    </Teleport>

    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead>
            <tr>
              <th>DESCRIPCIÓN</th>
              <th>PROVINCIA</th>
              <th>ESTADO</th>
              <th class="text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredItems" :key="item.id">
              <td class="text-left" data-label="Descripción">{{ item.descripcion }}</td>
              <td data-label="Provincia">{{ getProvinciaNombre(item.provincia_id) }}</td>
              <td data-label="Estado">
                <span class="status-badge" :class="item.vigente ? 'status-active' : 'status-inactive'">
                  {{ item.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </td>
              <td class="actions-cell" data-label="Acciones">
                <div class="action-buttons">
                  <button class="action-btn btn-view" @click="verElemento(item)" title="Ver detalle">
                    <AppIcons name="eye" :size="16" />
                  </button>
                  <button class="action-btn btn-edit" @click="editarElemento(item)" title="Editar">
                    <AppIcons name="edit" :size="16" />
                  </button>
                  <button 
                    class="action-btn" 
                    :class="item.vigente ? 'btn-delete' : 'btn-activate'"
                    @click="item.vigente ? confirmarAnular(item) : confirmarActivar(item)"
                    :title="item.vigente ? 'Anular' : 'Activar'"
                  >
                    <AppIcons :name="item.vigente ? 'trash' : 'check'" :size="16" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredItems.length === 0">
              <td colspan="4" class="no-data">No se encontraron comunas</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>

    <!-- Modal Formulario -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} COMUNA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="form-group">
              <label class="form-label">PROVINCIA:</label>
              <select class="form-control" v-model="form.provincia_id" required>
                <option :value="null" disabled>SELECCIONE PROVINCIA</option>
                <option v-for="prov in provinciasActivas" :key="prov.id" :value="prov.id">
                  {{ prov.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input type="text" class="form-control" v-model="form.descripcion"
                @input="form.descripcion = form.descripcion.toUpperCase()"
                placeholder="EJ: SANTIAGO" required>
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
          <h3>👁 DETALLE COMUNA</h3>
          <button class="modal-close" @click="cerrarViewModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">PROVINCIA:</label>
              <div class="view-value">{{ getProvinciaNombre(elementoSeleccionado?.provincia_id) }}</div>
            </div>
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
        <p>Cargando comunas...</p>
      </div>
    </div>

    <NotificationToast v-if="toast.visible" :message="toast.message" :icon="toast.icon" @close="toast.visible = false" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import SearchBar from '@/components/common/SearchBar.vue'

const emit = defineEmits(['confirm-action'])
defineExpose({ abrirModalCrear })

const comunas = ref([])
const provincias = ref([])
const items = ref([])
const search = ref('')
const tempSearch = ref('')
const filtroProvincia = ref('')
const isFilterOpen = ref(false)
const filterContainer = ref(null)
const cargando = ref(false)
const saving = ref(false)

const ejecutarBusqueda = () => {
  search.value = tempSearch.value
}

const toast = reactive({ visible: false, message: '', icon: '' })
const showToast = (message, icon = 'check') => {
  toast.message = message; toast.icon = icon; toast.visible = true
  setTimeout(() => { toast.visible = false }, 3000)
}

const modalVisible = ref(false)
const editando = ref(false)
const form = reactive({ id: null, descripcion: '', provincia_id: null, vigente: true })
const viewModalVisible = ref(false)
const itemSeleccionado = ref(null)

const cargarDatos = async () => {
  cargando.value = true
  try {
    const [respComunas, respProvincias] = await Promise.all([
      mantenedoresService.comuna.list().catch(e => { console.error('Comunas list error:', e); return [] }),
      mantenedoresService.provincia.list().catch(e => { console.error('Provincias list error:', e); return [] })
    ])

    const getData = (resp) => {
      if (!resp) return []
      if (Array.isArray(resp)) return resp
      return resp.results || (resp.data?.results) || resp.data || resp.items || []
    }

    comunas.value = getData(respComunas).map(c => {
      // Intento de obtener el ID de provincia de forma robusta
      let provId = null
      if (c.pro_id) {
        provId = typeof c.pro_id === 'object' ? (c.pro_id.pro_id || c.pro_id.id) : c.pro_id
      } else if (c.PRO_ID) {
        provId = typeof c.PRO_ID === 'object' ? (c.PRO_ID.PRO_ID || c.PRO_ID.ID) : c.PRO_ID
      } else if (c.provincia_id) {
        provId = c.provincia_id
      }

      return {
        id: c.com_id ?? c.COM_ID ?? c.id,
        descripcion: (c.com_descripcion ?? c.COM_DESCRIPCION ?? c.DESCRIPCION ?? c.descripcion ?? '').toString(),
        provincia_id: provId,
        vigente: !!(c.com_vigente ?? c.COM_VIGENTE ?? c.vigente ?? true)
      }
    })

    provincias.value = getData(respProvincias).map(p => ({
      id: p.pro_id ?? p.PRO_ID ?? p.id,
      descripcion: (p.pro_descripcion ?? p.PRO_DESCRIPCION ?? p.DESCRIPCION ?? p.descripcion ?? '').toString(),
      vigente: !!(p.pro_vigente ?? p.PRO_VIGENTE ?? p.vigente ?? true)
    }))
  } catch (error) {
    console.error('Error cargando datos:', error)
    showToast('Error al cargar comunas', 'alert-triangle')
  } finally { cargando.value = false }
}

const getProvinciaNombre = (id) => {
  const p = provincias.value.find(x => x.id === id)
  return p ? p.descripcion : 'NO ENCONTRADA'
}

const provinciasActivas = computed(() => provincias.value.filter(p => p.vigente))

const filteredItems = computed(() => {
  let result = comunas.value

  // Filtrar por texto
  if (search.value) {
    const q = search.value.toUpperCase()
    result = result.filter(item =>
      item.descripcion.toUpperCase().includes(q) ||
      getProvinciaNombre(item.provincia_id).toUpperCase().includes(q)
    )
  }

  // Filtrar por provincia
  if (filtroProvincia.value) {
    result = result.filter(item => item.provincia_id === filtroProvincia.value)
  }

  return result
})

function abrirModalCrear() {
  editando.value = false
  Object.assign(form, { id: null, descripcion: '', provincia_id: '', vigente: true })
  modalVisible.value = true
}

const editarElemento = (item) => {
  editando.value = true
  Object.assign(form, { id: item.id, descripcion: item.descripcion, provincia_id: item.provincia_id, vigente: item.vigente })
  modalVisible.value = true
}

const verElemento = (item) => { elementoSeleccionado.value = item; viewModalVisible.value = true }
const cerrarModal = () => { modalVisible.value = false; editando.value = false }
const cerrarViewModal = () => { viewModalVisible.value = false; elementoSeleccionado.value = null }

const guardar = async () => {
  if (!form.provincia_id) { showToast('Debe seleccionar una provincia', 'alert-triangle'); return }
  saving.value = true
  try {
    const payload = { com_descripcion: form.descripcion, pro_id: form.provincia_id, com_vigente: !!form.vigente }
    if (editando.value) {
      await mantenedoresService.comuna.partialUpdate(form.id, payload)
      showToast('Comuna actualizada correctamente', 'check')
    } else {
      await mantenedoresService.comuna.create(payload)
      showToast('Comuna creada correctamente', 'check')
    }
    cerrarModal(); await cargarDatos()
  } catch (error) {
    console.error('Error al guardar:', error)
    showToast('Error al guardar comuna', 'alert-triangle')
  } finally { saving.value = false }
}

const confirmarAnular = (item) => {
  emit('confirm-action', {
    titulo: 'Anular Comuna', mensaje: `¿Estás seguro de anular "${item.descripcion}"?`,
    accion: async () => {
      try { await mantenedoresService.comuna.partialUpdate(item.id, { com_vigente: false }); await cargarDatos(); showToast('Comuna anulada correctamente', 'check') }
      catch (e) { showToast('Error al anular comuna', 'alert-triangle') }
    }
  })
}

const confirmarActivar = (item) => {
  emit('confirm-action', {
    titulo: 'Activar Comuna', mensaje: `¿Estás seguro de activar "${item.descripcion}"?`,
    accion: async () => {
      try { await mantenedoresService.comuna.partialUpdate(item.id, { com_vigente: true }); await cargarDatos(); showToast('Comuna activada correctamente', 'check') }
      catch (e) { showToast('Error al activar comuna', 'alert-triangle') }
    }
  })
}

onMounted(() => { cargarDatos() })
</script>

<style scoped>
.mantenedor-section { position: relative;
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}
.mantenedor-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #3949ab; }
.mantenedor-header h2 { color: #1a237e; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; margin: 0; }
.search-group {
  display: flex;
  gap: 12px;
  align-items: center;
  width: 100%;
}

/* Styles cleaned up - using reusable components */
.search-button {
  background-color: #1a237e !important;
  height: 40px !important;
}
.table-container { flex: 1; overflow: hidden; border: 1px solid #eee; border-radius: 8px; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #f0f0f0; }
.data-table th { background-color: #f8f9fa; color: #333; font-weight: 600; position: sticky; top: 0; z-index: 10; }
.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; }
.status-active { background-color: #e8f5e9; color: #2e7d32; }
.status-inactive { background-color: #ffebee; color: #c62828; }
.actions-cell { text-align: center; }
.action-buttons { display: flex; justify-content: center; gap: 8px; }
.action-btn { 
  background: none; 
  border: none; 
  cursor: pointer; 
  padding: 6px; 
  border-radius: 4px; 
  transition: background 0.2s; 
  color: #555; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}
.action-btn:hover { background-color: #f0f0f0; }
.btn-view:hover { color: #1976d2; background-color: #e3f2fd; }
.btn-edit:hover { color: #f57c00; background-color: #fff3e0; }
.btn-delete:hover { color: #d32f2f; background-color: #ffebee; }
.btn-activate:hover { color: #388e3c; background-color: #e8f5e9; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 8px; width: 90%; max-width: 500px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); display: flex; flex-direction: column; }
.modal-header { padding: 15px 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.modal-header h3 { margin: 0; color: #1a237e; font-size: 1.2rem; }
.modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #666; }
.modal-body { padding: 20px; overflow-y: auto; max-height: 70vh; }
.form-group { margin-bottom: 15px; }
.form-label { display: block; margin-bottom: 5px; font-weight: 500; color: #333; }
.form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.modal-sm { max-width: 360px; }
.view-container { text-align: center; }
.view-group { margin-bottom: 15px; border-bottom: 1px solid #f0f0f0; padding-bottom: 10px; }
.view-label { font-weight: 600; color: #555; display: block; font-size: 0.85rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.view-value { color: #111827; font-size: 1rem; font-weight: 500; }
.loading-overlay { position: absolute; inset: 0; background: rgba(255,255,255,0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
.spinner { width: 30px; height: 30px; border: 3px solid #f3f3f3; border-top: 3px solid #3949ab; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.btn-primary { background: #1a237e; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; font-size: 0.95rem; transition: background 0.2s; }
.btn-primary:hover { background: #283593; }
.text-center { text-align: center; }

@media (max-width: 768px) {
  .mantenedor-header h2 { font-size: 1.25rem; }
  .search-group {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  .search-input { max-width: 100%; }

  .data-table thead { display: none; }
  .data-table, .data-table tbody, .data-table tr, .data-table td { display: block; width: 100%; }
  .data-table tr { margin-bottom: 16px; background: white; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .data-table td { display: flex; justify-content: space-between; align-items: center; text-align: right; padding: 12px 16px; border-bottom: 1px solid #f3f4f6; }
  .data-table td:last-child { border-bottom: none; justify-content: center; padding-top: 16px; }
  .data-table td::before { content: attr(data-label); font-weight: 600; color: #6b7280; font-size: 0.85rem; text-transform: uppercase; margin-right: 16px; text-align: left; }
  
  .actions-cell { background-color: #f9fafb; border-top: 1px solid #e5e7eb; border-radius: 0 0 8px 8px; }
  .mantenedor-section { height: auto; overflow: visible; }
  .table-container { height: auto; overflow: visible; }
}
.text-left { text-align: left !important; }
</style>
