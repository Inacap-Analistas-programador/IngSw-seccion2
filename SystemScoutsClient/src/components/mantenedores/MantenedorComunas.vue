<template>
  <div class="mantenedor-section-expanded">
    <div class="mantenedor-header">
      <h2>🏘️ Gestión de Comunas</h2>
      <BaseButton variant="primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="16" /> Nueva Comuna
      </BaseButton>
    </div>

    <!-- Buscador -->
    <div class="search-bar search-bar--compact">
      <input 
        type="text" 
        class="search-input" 
        placeholder="BUSCAR COMUNA..."
        v-model="searchQuery"
        @input="handleSearch"
      >
      <BaseButton class="search-button" variant="primary">
        <AppIcons name="search" :size="16" /> Buscar
      </BaseButton>
    </div>

    <ModernMainScrollbar>
      <div class="table-container-expanded">
        <table class="data-table-expanded">
          <thead>
            <tr>
              <th>DESCRIPCIÓN</th>
              <th>PROVINCIA</th>
              <th>ESTADO</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="4" class="text-center">Cargando...</td>
            </tr>
            <tr v-else-if="filteredItems.length === 0">
              <td colspan="4" class="text-center">No se encontraron registros</td>
            </tr>
            <tr v-else v-for="item in filteredItems" :key="item.id">
              <td>{{ item.descripcion }}</td>
              <td>{{ getProvinciaNombre(item.provincia_id) }}</td>
              <td>
                <span class="status-badge" :class="item.vigente ? 'status-active' : 'status-inactive'">
                  {{ item.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                </span>
              </td>
              <td class="actions">
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
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} COMUNA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="form-group">
              <label class="form-label">PROVINCIA:</label>
              <select class="form-control" v-model="form.provincia_id" required>
                <option :value="null" disabled>SELECCIONE PROVINCIA</option>
                <option v-for="prov in provincias" :key="prov.id" :value="prov.id">
                  {{ prov.descripcion }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.descripcion"
                @input="form.descripcion = form.descripcion.toUpperCase()"
                placeholder="EJ: SANTIAGO"
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

    <!-- Modal Ver -->
    <div v-if="modalActivo === 'ver'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 VISUALIZAR COMUNA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
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
                  {{ elementoSeleccionado?.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                </span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <BaseButton variant="secondary" @click="cerrarModal">Cerrar</BaseButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'

export default {
  name: 'MantenedorComunas',
  components: { BaseButton, AppIcons, ModernMainScrollbar },
  emits: ['show-message', 'confirm-action'],
  setup(props, { emit }) {
    const comunas = ref([])
    const provincias = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const searchQuery = ref('')
    
    // Modal state
    const modalActivo = ref('')
    const editando = ref(false)
    const elementoSeleccionado = ref(null)

    // Form
    const form = reactive({
      id: null,
      descripcion: '',
      provincia_id: null,
      vigente: true
    })

    // Helpers
    const getData = (resp) => {
      if (!resp) return []
      if (Array.isArray(resp)) return resp
      const r = resp
      return r.results || (r.data?.results) || r.data || r.items || []
    }

    const normalize = (arr, mapFn) => (arr || []).map(mapFn)

    // Cargar datos
    const cargarDatos = async () => {
      loading.value = true
      try {
        const [respComunas, respProvincias] = await Promise.all([
          mantenedoresService.comuna.list().catch(e => { console.error('Comunas list error:', e); return [] }),
          mantenedoresService.provincia.list().catch(e => { console.error('Provincias list error:', e); return [] })
        ])

        comunas.value = normalize(getData(respComunas), c => ({
          id: c.com_id ?? c.COM_ID ?? c.id,
          descripcion: (c.com_descripcion ?? c.COM_DESCRIPCION ?? c.DESCRIPCION ?? c.descripcion ?? '').toString(),
          provincia_id: (c.pro_id?.pro_id ?? c.PRO_ID?.PRO_ID ?? c.pro_id ?? c.PRO_ID ?? c.provincia_id ?? null),
          vigente: (c.com_vigente ?? c.COM_VIGENTE ?? c.vigente ?? true) ? true : false
        }))

        provincias.value = normalize(getData(respProvincias), p => ({
          id: p.pro_id ?? p.PRO_ID ?? p.id,
          descripcion: (p.pro_descripcion ?? p.PRO_DESCRIPCION ?? p.DESCRIPCION ?? p.descripcion ?? '').toString(),
          vigente: (p.pro_vigente ?? p.PRO_VIGENTE ?? p.vigente ?? true) ? true : false
        }))

      } catch (error) {
        console.error('Error cargando datos:', error)
        emit('show-message', { type: 'error', text: 'Error al cargar comunas.' })
      } finally {
        loading.value = false
      }
    }

    const getProvinciaNombre = (id) => {
      const p = provincias.value.find(x => x.id === id)
      return p ? p.descripcion : 'NO ENCONTRADA'
    }

    // Filtrado
    const handleSearch = () => {
      // Trigger computed update
    }

    const filteredItems = computed(() => {
      const q = searchQuery.value.toUpperCase()
      if (!q) return comunas.value
      return comunas.value.filter(item => 
        item.descripcion.toUpperCase().includes(q) ||
        getProvinciaNombre(item.provincia_id).toUpperCase().includes(q)
      )
    })

    // Acciones del modal
    const abrirModalCrear = () => {
      modalActivo.value = 'crear'
      editando.value = false
      Object.assign(form, { id: null, descripcion: '', provincia_id: null, vigente: true })
    }

    const verElemento = (item) => {
      elementoSeleccionado.value = item
      modalActivo.value = 'ver'
    }

    const editarElemento = (item) => {
      elementoSeleccionado.value = item
      modalActivo.value = 'editar'
      editando.value = true
      Object.assign(form, {
        id: item.id,
        descripcion: item.descripcion,
        provincia_id: item.provincia_id,
        vigente: item.vigente
      })
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      elementoSeleccionado.value = null
    }

    // Guardar
    const guardar = async () => {
      if (!form.provincia_id) {
        emit('show-message', { type: 'error', text: 'Debe seleccionar una provincia.' })
        return
      }
      
      saving.value = true
      const payload = {
        com_descripcion: form.descripcion,
        pro_id: form.provincia_id,
        com_vigente: !!form.vigente
      }

      try {
        if (editando.value) {
          const id = form.id
          await mantenedoresService.comuna.partialUpdate(id, payload)
          emit('show-message', { type: 'success', text: 'Comuna actualizada correctamente' })
        } else {
          await mantenedoresService.comuna.create(payload)
          emit('show-message', { type: 'success', text: 'Comuna creada correctamente' })
        }
        cerrarModal()
        await cargarDatos()
      } catch (error) {
        console.error('Error al guardar:', error)
        emit('show-message', { type: 'error', text: 'No se pudo guardar la comuna.' })
      } finally {
        saving.value = false
      }
    }

    // Confirmación (Anular/Activar)
    const confirmarAccion = (item, accion) => {
      const titulo = accion === 'anular' ? 'Anular Comuna' : 'Activar Comuna'
      const mensaje = `¿Está seguro que desea ${accion} la comuna "${item.descripcion}"?`
      
      emit('confirm-action', {
        titulo,
        mensaje,
        accion: async () => {
          try {
            const payload = { ...item, com_vigente: accion === 'activar' }
            // API expects database field names typically, or the serializer handles it. 
            // Based on previous code: partialUpdate(id, payload)
            // But here we need to map back to DB fields? 
            // The service seems to handle it or we reuse the payload structure.
            // Let's use the same payload structure as save:
            const updatePayload = { 
              com_vigente: accion === 'activar' 
            }
            
            await mantenedoresService.comuna.partialUpdate(item.id, updatePayload)
            await cargarDatos()
            emit('show-message', { type: 'success', text: `Comuna ${accion === 'activar' ? 'activada' : 'anulada'} correctamente` })
          } catch (error) {
            console.error('Error en acción:', error)
            emit('show-message', { type: 'error', text: `Error al ${accion} la comuna.` })
          }
        }
      })
    }

    onMounted(() => {
      cargarDatos()
    })

    return {
      comunas,
      provincias,
      loading,
      saving,
      searchQuery,
      filteredItems,
      modalActivo,
      editando,
      elementoSeleccionado,
      form,
      handleSearch,
      abrirModalCrear,
      verElemento,
      editarElemento,
      cerrarModal,
      guardar,
      confirmarAccion,
      getProvinciaNombre
    }
  }
}
</script>

<style scoped>
/* Reutilizando estilos de mantenedores.vue */
.mantenedor-section-expanded {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.mantenedor-header h2 {
  font-size: 1.5rem;
  color: #1a237e;
  margin: 0;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 8px;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
}

.table-container-expanded {
  flex: 1;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid #eee;
  background: white;
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
}

.data-table-expanded th {
  background: #f4f6f9;
  color: #5c6bc0;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  padding: 12px 16px;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table-expanded td {
  padding: 14px 16px;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
  font-size: 0.95rem;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-active {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-inactive {
  background: #ffebee;
  color: #c62828;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 6px 12px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #1a237e;
  font-size: 1.25rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #3949ab;
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}

.view-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.view-group {
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.view-label {
  font-size: 0.8rem;
  color: #666;
  text-transform: uppercase;
  margin-bottom: 4px;
  display: block;
}

.view-value {
  font-size: 1.1rem;
  color: #000;
  font-weight: 500;
}

.modal-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
