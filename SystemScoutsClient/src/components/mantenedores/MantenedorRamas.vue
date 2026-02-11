<template>
  <div class="mantenedor-section-expanded">
    <div class="mantenedor-header">
      <h2>🏕️ Gestión de Ramas</h2>
      <BaseButton variant="primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="16" /> Nueva Rama
      </BaseButton>
    </div>

    <!-- Buscador (Opcional, aunque no tiene filtro específico en el original, siempre es útil) -->
    <div class="search-bar search-bar--compact">
      <input 
        type="text" 
        class="search-input" 
        placeholder="BUSCAR RAMA..."
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
              <th>ESTADO</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="3" class="text-center">Cargando...</td>
            </tr>
            <tr v-else-if="filteredItems.length === 0">
              <td colspan="3" class="text-center">No se encontraron registros</td>
            </tr>
            <tr v-else v-for="rama in filteredItems" :key="rama.id">
              <td>{{ rama.descripcion }}</td>
              <td>
                <span class="status-badge" :class="rama.vigente ? 'status-active' : 'status-inactive'">
                  {{ rama.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                </span>
              </td>
              <td class="actions">
                <BaseButton variant="secondary" class="btn-action" @click="verElemento(rama)">
                  <AppIcons name="eye" :size="16" /> Ver
                </BaseButton>
                <BaseButton variant="secondary" class="btn-action" @click="editarElemento(rama)">
                  <AppIcons name="edit" :size="16" /> Editar
                </BaseButton>
                <BaseButton v-if="rama.vigente" variant="secondary" class="btn-action" @click="confirmarAccion(rama, 'anular')">
                  <AppIcons name="block" :size="16" /> Anular
                </BaseButton>
                <BaseButton v-else variant="primary" class="btn-action" @click="confirmarAccion(rama, 'activar')">
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

    <!-- Modal Ver -->
    <div v-if="modalActivo === 'ver'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 VISUALIZAR RAMA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
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
  name: 'MantenedorRamas',
  components: { BaseButton, AppIcons, ModernMainScrollbar },
  emits: ['show-message', 'confirm-action'], // Eventos para comunicar al padre (si es necesario) o manejar todo aquí.
  // Nota: Para mantener consistencia con MantenedorZonas, usaremos eventos para confirmación si el padre maneja el modal global,
  // pero intentaremos ser autónomos donde sea posible o delegar estandarizadamente.
  // En este refactor, el padre (mantenedores.vue) tiene un modal de confirmación global.
  
  setup(props, { emit }) {
    const items = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const searchQuery = ref('')
    const modalActivo = ref('') // '', 'crear', 'editar', 'ver'
    const editando = ref(false)
    const elementoSeleccionado = ref(null)

    const form = reactive({
      id: null,
      descripcion: '',
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
        const resp = await mantenedoresService.rama.list()
        items.value = normalize(getData(resp), r => ({
          id: r.ram_id ?? r.RAM_ID ?? r.id,
          descripcion: (r.ram_descripcion ?? r.RAM_DESCRIPCION ?? r.DESCRIPCION ?? r.descripcion ?? '').toString(),
          vigente: !!(r.ram_vigente ?? r.RAM_VIGENTE ?? r.vigente)
        }))
      } catch (err) {
        console.error('Error cargando ramas:', err)
        emit('show-message', { type: 'error', text: 'Error al cargar ramas' })
      } finally {
        loading.value = false
      }
    }

    const filteredItems = computed(() => {
      if (!searchQuery.value) return items.value
      const q = searchQuery.value.toLowerCase()
      return items.value.filter(item => 
        item.descripcion.toLowerCase().includes(q)
      )
    })

    const handleSearch = () => {
      // Reactividad automática
    }

    const limpiarFormulario = () => {
      form.id = null
      form.descripcion = ''
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
          ram_descripcion: form.descripcion,
          ram_vigente: !!form.vigente
        }

        if (editando.value) {
          if (!form.id) throw new Error('ID no definido')
          await mantenedoresService.rama.partialUpdate(form.id, payload)
        } else {
          await mantenedoresService.rama.create(payload)
        }
        
        cerrarModal()
        await cargarDatos()
        emit('show-message', { type: 'success', text: editando.value ? 'Rama actualizada' : 'Rama creada' })
      } catch (err) {
        console.error('Error guardando rama:', err)
        emit('show-message', { type: 'error', text: 'Error al guardar rama: ' + err.message })
      } finally {
        saving.value = false
      }
    }

    // Manejo de anular/activar delegando al padre o haciéndolo local.
    // Para simplificar y limpiar el padre, lo haremos localmente si el padre lo permite, 
    // pero el padre tiene un 'confirmModal' global. Vamos a usar el evento 'confirm-action' 
    // para usar el modal del padre, pasándole la función a ejecutar.
    
    const confirmarAccion = (item, accion) => {
      emit('confirm-action', {
        titulo: accion === 'anular' ? 'Confirmar Anulación' : 'Confirmar Activación',
        mensaje: accion === 'anular' ? '¿Está seguro que desea anular esta rama?' : '¿Desea activar nuevamente esta rama?',
        accion: async () => {
          try {
            const payload = { ram_vigente: accion === 'activar' }
            await mantenedoresService.rama.partialUpdate(item.id, payload)
            await cargarDatos()
            emit('show-message', { type: 'success', text: `Rama ${accion === 'activar' ? 'activada' : 'anulada'} correctamente` })
          } catch (err) {
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
      handleSearch
    }
  }
}
</script>

<style scoped>
/* Estilos extraídos y adaptados de mantenedores.vue */
.mantenedor-section-expanded {
  padding: 30px 20px;
  animation: fadeIn 0.5s ease;
  width: 100%;
  margin: 0;
  box-sizing: border-box;
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
  background: #f5f5f5;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.table-container-expanded {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  overflow: hidden;
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
}

.data-table-expanded th,
.data-table-expanded td {
  padding: 14px 20px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table-expanded th {
  background: #f9fafb;
  color: #374151;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-table-expanded tr:hover {
  background-color: #f8f9fa;
}

.status-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
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
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  font-size: 0.85rem;
}

/* Modal styles copied for consistency */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
  animation: slideIn 0.3s ease;
  overflow: hidden;
}

.modal-header {
  background: #3949ab;
  color: white;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.modal-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
 box-sizing: border-box;
}

.form-control:focus {
  border-color: #3949ab;
  outline: none;
  box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

/* View styles */
.view-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.view-group {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 12px;
}

.view-group:last-child {
  border-bottom: none;
}

.view-label {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 4px;
  display: block;
  font-weight: 600;
}

.view-value {
  font-size: 1.1rem;
  color: #111827;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
