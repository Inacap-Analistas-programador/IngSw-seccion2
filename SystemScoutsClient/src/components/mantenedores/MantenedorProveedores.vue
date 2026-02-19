<template>
  <div class="mantenedor-section-expanded">
    <div class="mantenedor-header">
      <h2>Gestión de Proveedores</h2>
      <!-- <BaseButton variant="primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="16" /> Nuevo Proveedor
      </BaseButton> -->
    </div>

    <Teleport to="#search-container">
      <div class="search-box">
        <input 
          type="text" 
          class="search-input-new" 
          v-model="tempSearch" 
          placeholder="Buscar Proveedor..."
          @keyup.enter="ejecutarBusqueda"
        >
        <button class="search-btn-new" @click="ejecutarBusqueda" title="Buscar">
          <AppIcons name="search" :size="16" />
        </button>
      </div>
    </Teleport>

    <ModernMainScrollbar>
      <div class="table-container-expanded">
        <table class="data-table-expanded">
          <thead>
            <tr>
              <th>DESCRIPCIÓN</th>
              <th>CONTACTO</th>
              <th>DIRECCIÓN</th>
              <th>ESTADO</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="text-center">Cargando...</td>
            </tr>
            <tr v-else-if="filteredItems.length === 0">
              <td colspan="5" class="text-center">No se encontraron registros</td>
            </tr>
            <tr v-else v-for="item in filteredItems" :key="item.id">
              <td data-label="Descripción">{{ item.descripcion }}</td>
              <td data-label="Contacto">{{ item.celular1 }}<span v-if="item.celular2"> / {{ item.celular2 }}</span></td>
              <td data-label="Dirección">{{ item.direccion }}</td>
              <td data-label="Estado">
                <span class="status-badge" :class="item.vigente ? 'status-active' : 'status-inactive'">
                  {{ item.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                </span>
              </td>
              <td class="actions-cell" data-label="Acciones">
                <BaseButton variant="secondary" class="btn-action" @click="verElemento(item)">
                  <AppIcons name="eye" :size="16" /> Ver
                </BaseButton>
                <BaseButton variant="secondary" class="btn-action" @click="editarElemento(item)">
                  <AppIcons name="edit" :size="16" /> Editar
                </BaseButton>
                <BaseButton v-if="item.vigente" variant="secondary" class="btn-action" @click="confirmarAccion(item, 'anular')">
                  <AppIcons name="block" :size="16" /> Anular
                </BaseButton>
                <BaseButton v-else variant="primary" class="btn-action" @click="confirmarAccion(item, 'activar')">
                  <AppIcons name="check" :size="16" /> Activar
                </BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </ModernMainScrollbar>

    <!-- Modal Crear/Editar -->
    <div v-if="modalActivo === 'crear' || modalActivo === 'editar'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} PROVEEDOR</h3>
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
                placeholder="EJ: SERVICIOS DE TRANSPORTE"
                required
              >
            </div>
            
            <div class="form-row">
              <div class="form-group half">
                <label class="form-label">CELULAR 1:</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="form.celular1"
                  placeholder="+569..."
                >
              </div>
              <div class="form-group half">
                <label class="form-label">CELULAR 2:</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="form.celular2"
                  placeholder="+569..."
                >
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">DIRECCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.direccion"
                @input="form.direccion = form.direccion.toUpperCase()"
                placeholder="CALLE, NÚMERO, COMUNA"
              >
            </div>

            <div class="form-group">
              <label class="form-label">OBSERVACIÓN:</label>
              <textarea 
                class="form-control" 
                v-model="form.observacion"
                rows="3"
                placeholder="OBSERVACIONES ADICIONALES..."
              ></textarea>
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

    <!-- Modal Ver -->
    <div v-if="modalActivo === 'ver'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 VISUALIZAR PROVEEDOR</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado?.descripcion }}</div>
            </div>
            <div class="view-row">
                <div class="view-group half">
                    <label class="view-label">CELULAR 1:</label>
                    <div class="view-value">{{ elementoSeleccionado?.celular1 || '-' }}</div>
                </div>
                <div class="view-group half">
                    <label class="view-label">CELULAR 2:</label>
                    <div class="view-value">{{ elementoSeleccionado?.celular2 || '-' }}</div>
                </div>
            </div>
            <div class="view-group">
              <label class="view-label">DIRECCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado?.direccion || '-' }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">OBSERVACIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado?.observacion || '-' }}</div>
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
            <BaseButton variant="secondary" @click="cerrarModal">
              <AppIcons name="close" :size="16" /> Cerrar
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'

export default {
  name: 'MantenedorProveedores',
  components: { BaseButton, AppIcons, ModernMainScrollbar },
  emits: ['show-message', 'confirm-action'],
  expose: ['abrirModalCrear'], // Options API expose
  
  setup(props, { emit }) {
    const items = ref([])
    const searchQuery = ref('')
    const tempSearch = ref('')
    const loading = ref(false)
    const saving = ref(false)

    const ejecutarBusqueda = () => {
      searchQuery.value = tempSearch.value
    }
    const modalActivo = ref('')
    const editando = ref(false)
    const elementoSeleccionado = ref(null)

    const form = reactive({
      id: null,
      descripcion: '',
      celular1: '',
      celular2: '',
      direccion: '',
      observacion: '',
      vigente: true
    })

    const normalize = (arr, mapFn) => (arr || []).map(mapFn)
    const getData = (resp) => {
      if (!resp) return []
      if (Array.isArray(resp)) return resp
      return resp.results || (resp.data?.results) || resp.data || resp.items || []
    }

    const cargarDatos = async () => {
      loading.value = true
      try {
        const resp = await mantenedoresService.proveedorPago.list()
        items.value = normalize(getData(resp), p => ({
          id: p.prv_id ?? p.PRV_ID ?? p.id,
          descripcion: (p.prv_descripcion ?? p.PRV_DESCRIPCION ?? p.DESCRIPCION ?? p.descripcion ?? '').toString(),
          celular1: p.prv_celular1 ?? p.PRV_CELULAR1 ?? p.celular1 ?? '',
          celular2: p.prv_celular2 ?? p.PRV_CELULAR2 ?? p.celular2 ?? '',
          direccion: p.prv_direccion ?? p.PRV_DIRECCION ?? p.direccion ?? '',
          observacion: p.prv_observacion ?? p.PRV_OBSERVACION ?? p.observacion ?? '',
          vigente: !!(p.prv_vigente ?? p.PRV_VIGENTE ?? p.vigente)
        }))
      } catch (err) {
        console.error('Error cargando proveedores:', err)
        emit('show-message', { type: 'error', text: 'Error al cargar proveedores' })
      } finally {
        loading.value = false
      }
    }

    const filteredItems = computed(() => {
      if (!searchQuery.value) return items.value
      const q = searchQuery.value.toLowerCase()
      return items.value.filter(item => 
        item.descripcion.toLowerCase().includes(q) ||
        item.direccion.toLowerCase().includes(q)
      )
    })

    const handleSearch = () => {}

    const limpiarFormulario = () => {
      form.id = null
      form.descripcion = ''
      form.celular1 = ''
      form.celular2 = ''
      form.direccion = ''
      form.observacion = ''
      form.vigente = true
    }

    const abrirModalCrear = () => {
      limpiarFormulario()
      editando.value = false
      modalActivo.value = 'crear'
    }

    const editarElemento = (item) => {
      limpiarFormulario()
      form.id = item.id
      form.descripcion = item.descripcion
      form.celular1 = item.celular1
      form.celular2 = item.celular2
      form.direccion = item.direccion
      form.observacion = item.observacion
      form.vigente = item.vigente
      editando.value = true
      modalActivo.value = 'editar'
    }

    const verElemento = (item) => {
      elementoSeleccionado.value = item
      modalActivo.value = 'ver'
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      elementoSeleccionado.value = null
    }

    const guardar = async () => {
      saving.value = true
      try {
        const payload = {
          prv_descripcion: form.descripcion,
          prv_celular1: form.celular1 || '',
          prv_celular2: form.celular2 || null,
          prv_direccion: form.direccion || '',
          prv_observacion: form.observacion || null,
          prv_vigente: !!form.vigente
        }

        if (editando.value) {
          if (!form.id) throw new Error('ID no definido')
          await mantenedoresService.proveedorPago.partialUpdate(form.id, payload)
        } else {
          await mantenedoresService.proveedorPago.create(payload)
        }
        
        cerrarModal()
        await cargarDatos()
        emit('show-message', { type: 'success', text: editando.value ? 'Proveedor actualizado' : 'Proveedor creado' })
      } catch (err) {
        console.error('Error guardando proveedor:', err)
        emit('show-message', { type: 'error', text: 'Error al guardar: ' + err.message })
      } finally {
        saving.value = false
      }
    }

    const confirmarAccion = (item, accion) => {
      emit('confirm-action', {
        titulo: accion === 'anular' ? 'Confirmar Anulación' : 'Confirmar Activación',
        mensaje: accion === 'anular' ? '¿Está seguro que desea anular este registro?' : '¿Desea activar nuevamente este registro?',
        accion: async () => {
          try {
            const payload = { prv_vigente: accion === 'activar' }
            await mantenedoresService.proveedorPago.partialUpdate(item.id, payload)
            await cargarDatos()
            emit('show-message', { type: 'success', text: `Registro ${accion === 'activar' ? 'activado' : 'anulado'} correctamente` })
          } catch (err) {
             console.error('Error cambio estado proveedor:', err) 
             emit('show-message', { type: 'error', text: 'Error al cambiar estado: ' + err.message })
          }
        }
      })
    }

    onMounted(() => {
      cargarDatos()
    })

    return {
      items,
      loading,
      saving,
      searchQuery,
      modalActivo,
      editando,
      elementoSeleccionado,
      filteredItems,
      form,
      abrirModalCrear,
      editarElemento,
      verElemento,
      cerrarModal,
      guardar,
      confirmarAccion,
      ejecutarBusqueda,
      tempSearch
    }
  }
}
</script>

<style scoped>
/* Estilos estandarizados basados en MantenedorZonas */
.mantenedor-section-expanded {
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
  margin-bottom: 0px;
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

.search-button {
  background-color: #1a237e !important;
  height: 40px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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

.table-container-expanded {
  flex: 1;
  overflow: hidden;
  border: 1px solid #eee;
  border-radius: 8px;
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
}

.data-table-expanded th, .data-table-expanded td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}

.data-table-expanded th {
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

.actions {
  text-align: center;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  font-size: 0.85rem;
}

.text-center { text-align: center; }

@media (max-width: 768px) {
  .mantenedor-header h2 { font-size: 1.25rem; }
  .search-bar { flex-direction: column; align-items: stretch; }
  .search-input { max-width: 100%; }
  
  .mantenedor-section-expanded { height: auto; overflow: visible; }
  .table-container-expanded { height: auto; overflow: visible; }
  .data-table-expanded thead { display: none; }
  .data-table-expanded, .data-table-expanded tbody, .data-table-expanded tr, .data-table-expanded td { display: block; width: 100%; }
  .data-table-expanded tr { margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); background: white; }
  .data-table-expanded td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
    padding: 12px 16px;
    border-bottom: 1px solid #f3f4f6;
  }

  .data-table-expanded td:last-child {
    border-bottom: none;
    justify-content: center;
    padding-top: 16px;
  }
  
  /* Etiquetas pseudo-elementos para las columnas */
  .data-table-expanded td::before {
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
    display: flex; 
    justify-content: center; 
    gap: 8px; 
    flex-wrap: wrap; 
    padding: 12px !important;
  }
  .btn-action { margin: 2px; }
}

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

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 15px;
}

.form-group.half {
  flex: 1;
  margin-bottom: 0;
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
  display: flex;
  flex-direction: column;
}

.view-row {
  display: flex;
  gap: 16px;
}

.view-group.half {
  flex: 1;
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

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>
