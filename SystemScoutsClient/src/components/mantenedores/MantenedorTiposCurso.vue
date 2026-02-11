<template>
  <div class="mantenedor-section-expanded">
    <div class="mantenedor-header">
      <h2>📚 Gestión de Tipos de Curso</h2>
      <BaseButton variant="primary" @click="abrirModalCrear">
        <AppIcons name="plus" :size="16" /> Nuevo Tipo
      </BaseButton>
    </div>

    <!-- Buscador -->
    <div class="search-bar search-bar--compact">
      <input 
        type="text" 
        class="search-input" 
        placeholder="BUSCAR TIPO DE CURSO..."
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
              <th>TIPO</th>
              <th>CANT. PARTICIPANTES</th>
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
              <td>{{ item.descripcion }}</td>
              <td>{{ getTipoNombre(item.tipo) }}</td>
              <td>{{ item.cant_participante }}</td>
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
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} TIPO DE CURSO</h3>
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
                placeholder="EJ: CURSO BÁSICO"
                required
              >
            </div>
            
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="form.tipo" required>
                <option :value="1">CURSO</option>
                <option :value="2">TALLER</option>
                <option :value="3">CHARLA</option>
                <option :value="4">SEMINARIO</option>
                <option :value="5">VERIFICACIÓN</option>
                <option :value="6">INSTITUCIONAL</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">CANT. PARTICIPANTES:</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="form.cant_participante"
                placeholder="EJ: 30"
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
          <h3>👁 VISUALIZAR TIPO DE CURSO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado?.descripcion }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">TIPO:</label>
              <div class="view-value">{{ getTipoNombre(elementoSeleccionado?.tipo) }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">CANT. PARTICIPANTES:</label>
              <div class="view-value">{{ elementoSeleccionado?.cant_participante }}</div>
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
  name: 'MantenedorTiposCurso',
  components: { BaseButton, AppIcons, ModernMainScrollbar },
  emits: ['show-message', 'confirm-action'],
  
  setup(props, { emit }) {
    const items = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const searchQuery = ref('')
    const modalActivo = ref('')
    const editando = ref(false)
    const elementoSeleccionado = ref(null)

    const form = reactive({
      id: null,
      descripcion: '',
      tipo: 1,
      cant_participante: null,
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
        const resp = await mantenedoresService.tipoCursos.list()
        items.value = normalize(getData(resp), t => ({
          id: t.tcu_id ?? t.TCU_ID ?? t.id,
          descripcion: (t.tcu_descripcion ?? t.TCU_DESCRIPCION ?? t.DESCRIPCION ?? t.descripcion ?? '').toString(),
          tipo: t.tcu_tipo ?? t.TCU_TIPO ?? t.tipo ?? 1,
          cant_participante: t.tcu_cant_participante ?? t.TCU_CANT_PARTICIPANTE ?? t.cant_participante ?? 0,
          vigente: !!(t.tcu_vigente ?? t.TCU_VIGENTE ?? t.vigente)
        }))
      } catch (err) {
        console.error('Error cargando tipos de curso:', err)
        emit('show-message', { type: 'error', text: 'Error al cargar tipos de curso' })
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

    const handleSearch = () => {}

    const limpiarFormulario = () => {
      form.id = null
      form.descripcion = ''
      form.tipo = 1
      form.cant_participante = null
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
      form.tipo = item.tipo
      form.cant_participante = item.cant_participante
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
          tcu_descripcion: form.descripcion,
          tcu_tipo: form.tipo,
          tcu_cant_participante: form.cant_participante,
          tcu_vigente: !!form.vigente
        }

        if (editando.value) {
          if (!form.id) throw new Error('ID no definido')
          await mantenedoresService.tipoCursos.partialUpdate(form.id, payload)
        } else {
          await mantenedoresService.tipoCursos.create(payload)
        }
        
        cerrarModal()
        await cargarDatos()
        emit('show-message', { type: 'success', text: editando.value ? 'Tipo de curso actualizado' : 'Tipo de curso creado' })
      } catch (err) {
        console.error('Error guardando tipo de curso:', err)
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
            const payload = { tcu_vigente: accion === 'activar' }
            await mantenedoresService.tipoCursos.partialUpdate(item.id, payload)
            await cargarDatos()
            emit('show-message', { type: 'success', text: `Registro ${accion === 'activar' ? 'activado' : 'anulado'} correctamente` })
          } catch (err) {
             emit('show-message', { type: 'error', text: 'Error al cambiar estado: ' + err.message })
          }
        }
      })
    }

    const getTipoNombre = (tipo) => {
      const tipos = {
        1: 'CURSO',
        2: 'TALLER',
        3: 'CHARLA',
        4: 'SEMINARIO',
        5: 'VERIFICACIÓN',
        6: 'INSTITUCIONAL'
      }
      return tipos[tipo] || 'DESCONOCIDO'
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
      handleSearch,
      getTipoNombre
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
