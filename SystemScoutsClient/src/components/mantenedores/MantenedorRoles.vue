<template>
  <div class="mantenedor-section">
    <div class="mantenedor-header">
      <h2><AppIcons name="shield" :size="24" /> Gestión de Roles</h2>
      <button class="btn-primary" @click="abrirModalCrear"><AppIcons name="plus" :size="18" /> Nuevo Rol</button>
    </div>
    <div class="search-bar"><input type="text" class="search-input" v-model="search" placeholder="Buscar Rol..."></div>
    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead><tr><th>DESCRIPCIÓN</th><th>TIPO</th><th>ESTADO</th><th class="text-center">ACCIONES</th></tr></thead>
          <tbody>
            <tr v-for="item in filteredItems" :key="item.id">
              <td>{{ item.descripcion }}</td>
              <td>{{ getTipoLabel(item.tipo) }}</td>
              <td><span class="status-badge" :class="item.vigente ? 'status-active' : 'status-inactive'">{{ item.vigente ? 'ACTIVO' : 'INACTIVO' }}</span></td>
              <td class="actions-cell"><div class="action-buttons">
                <button class="action-btn btn-view" @click="verItem(item)"><AppIcons name="eye" :size="16" /></button>
                <button class="action-btn btn-edit" @click="editarItem(item)"><AppIcons name="edit" :size="16" /></button>
                <button class="action-btn" :class="item.vigente ? 'btn-delete' : 'btn-activate'" @click="item.vigente ? confirmarAnular(item) : confirmarActivar(item)"><AppIcons :name="item.vigente ? 'trash' : 'check'" :size="16" /></button>
              </div></td>
            </tr>
            <tr v-if="filteredItems.length === 0"><td colspan="4" class="no-data">No se encontraron roles</td></tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header"><h3>{{ editando ? 'EDITAR' : 'NUEVO' }} ROL</h3><button class="modal-close" @click="cerrarModal">×</button></div>
        <div class="modal-body"><form @submit.prevent="guardar">
          <div class="form-group"><label class="form-label">DESCRIPCIÓN:</label><input type="text" class="form-control" v-model="form.descripcion" @input="form.descripcion = form.descripcion.toUpperCase()" placeholder="EJ: ADMINISTRADOR" required></div>
          <div class="form-group"><label class="form-label">TIPO:</label>
            <select class="form-control" v-model="form.tipo" required>
              <option :value="1">PARTICIPANTE</option><option :value="2">FORMADORES</option><option :value="3">APOYO FORMADORES</option>
              <option :value="4">ORGANIZACIÓN</option><option :value="5">SERVICIO</option><option :value="6">SALUD</option>
            </select>
          </div>
          <div class="form-actions">
            <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
            <BaseButton type="submit" variant="primary" :disabled="saving"><AppIcons name="save" :size="16" /><span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span></BaseButton>
          </div>
        </form></div>
      </div>
    </div>
    <div v-if="viewModalVisible" class="modal-overlay" @click="cerrarViewModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header"><h3>👁 DETALLE ROL</h3><button class="modal-close" @click="cerrarViewModal">×</button></div>
        <div class="modal-body">
          <div class="view-group"><label class="view-label">DESCRIPCIÓN:</label><div class="view-value">{{ itemSeleccionado?.descripcion }}</div></div>
          <div class="view-group"><label class="view-label">TIPO:</label><div class="view-value">{{ getTipoLabel(itemSeleccionado?.tipo) }}</div></div>
          <div class="view-group"><label class="view-label">ESTADO:</label><div class="view-value"><span class="status-badge" :class="itemSeleccionado?.vigente ? 'status-active' : 'status-inactive'">{{ itemSeleccionado?.vigente ? 'ACTIVO' : 'INACTIVO' }}</span></div></div>
          <div class="form-actions"><BaseButton variant="secondary" @click="cerrarViewModal"><AppIcons name="close" :size="16" /> Cerrar</BaseButton></div>
        </div>
      </div>
    </div>
    <div v-if="cargando" class="loading-overlay"><div class="loading-content"><div class="spinner"></div><p>Cargando roles...</p></div></div>
  </div>
</template>
<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
const emit = defineEmits(['show-message', 'confirm-action'])
const items = ref([]); const search = ref(''); const cargando = ref(false); const saving = ref(false)
const modalVisible = ref(false); const editando = ref(false); const viewModalVisible = ref(false); const itemSeleccionado = ref(null)
const form = reactive({ id: null, descripcion: '', tipo: 1, vigente: true })
const tipoLabels = { 1: 'PARTICIPANTE', 2: 'FORMADORES', 3: 'APOYO FORMADORES', 4: 'ORGANIZACIÓN', 5: 'SERVICIO', 6: 'SALUD' }
const getTipoLabel = (t) => tipoLabels[t] || t || ''
const cargarDatos = async () => {
  cargando.value = true
  try {
    const resp = await mantenedoresService.rol.list()
    const raw = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
    items.value = raw.map(r => ({ id: r.rol_id ?? r.ROL_ID ?? r.id, descripcion: (r.rol_descripcion ?? r.ROL_DESCRIPCION ?? r.descripcion ?? '').toString(), tipo: r.rol_tipo ?? r.ROL_TIPO ?? r.tipo ?? '', vigente: !!(r.rol_vigente ?? r.ROL_VIGENTE ?? r.vigente ?? true) }))
  } catch (e) { emit('show-message', { type: 'error', text: 'Error al cargar roles' }) } finally { cargando.value = false }
}
const filteredItems = computed(() => { if (!search.value) return items.value; const t = search.value.toLowerCase(); return items.value.filter(i => i.descripcion.toLowerCase().includes(t)) })
const abrirModalCrear = () => { editando.value = false; Object.assign(form, { id: null, descripcion: '', tipo: 1, vigente: true }); modalVisible.value = true }
const editarItem = (i) => { editando.value = true; Object.assign(form, { id: i.id, descripcion: i.descripcion, tipo: i.tipo, vigente: i.vigente }); modalVisible.value = true }
const verItem = (i) => { itemSeleccionado.value = i; viewModalVisible.value = true }
const cerrarModal = () => { modalVisible.value = false; editando.value = false }
const cerrarViewModal = () => { viewModalVisible.value = false; itemSeleccionado.value = null }
const guardar = async () => {
  saving.value = true
  try {
    const p = { rol_descripcion: form.descripcion, rol_tipo: form.tipo, rol_vigente: form.vigente }
    if (editando.value) { await mantenedoresService.rol.partialUpdate(form.id, p); emit('show-message', { type: 'success', text: 'Rol actualizado' }) }
    else { await mantenedoresService.rol.create(p); emit('show-message', { type: 'success', text: 'Rol creado' }) }
    cerrarModal(); await cargarDatos()
  } catch (e) { emit('show-message', { type: 'error', text: 'Error al guardar rol' }) } finally { saving.value = false }
}
const confirmarAnular = (i) => { emit('confirm-action', { titulo: 'Anular Rol', mensaje: `¿Anular "${i.descripcion}"?`, accion: async () => { try { await mantenedoresService.rol.partialUpdate(i.id, { rol_vigente: false }); await cargarDatos(); emit('show-message', { type: 'success', text: 'Rol anulado' }) } catch (e) { emit('show-message', { type: 'error', text: 'Error' }) } } }) }
const confirmarActivar = (i) => { emit('confirm-action', { titulo: 'Activar Rol', mensaje: `¿Activar "${i.descripcion}"?`, accion: async () => { try { await mantenedoresService.rol.partialUpdate(i.id, { rol_vigente: true }); await cargarDatos(); emit('show-message', { type: 'success', text: 'Rol activado' }) } catch (e) { emit('show-message', { type: 'error', text: 'Error' }) } } }) }
onMounted(() => { cargarDatos() })
</script>
<style scoped>
.mantenedor-section { padding: 0; width: 100%; height: 100%; display: flex; flex-direction: column; background: transparent; }
.mantenedor-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #3949ab; }
.mantenedor-header h2 { color: #1a237e; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; margin: 0; }
.search-bar { margin-bottom: 20px; } .search-input { width: 100%; max-width: 400px; padding: 10px 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
.table-container { flex: 1; overflow: hidden; border: 1px solid #eee; border-radius: 8px; }
.data-table { width: 100%; border-collapse: collapse; } .data-table th, .data-table td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #f0f0f0; } .data-table th { background-color: #f8f9fa; color: #333; font-weight: 600; position: sticky; top: 0; z-index: 10; }
.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; } .status-active { background-color: #e8f5e9; color: #2e7d32; } .status-inactive { background-color: #ffebee; color: #c62828; }
.actions-cell { text-align: center; } .action-buttons { display: flex; justify-content: center; gap: 8px; }
.action-btn { background: none; border: none; cursor: pointer; padding: 6px; border-radius: 4px; transition: background 0.2s; color: #555; } .action-btn:hover { background-color: #f0f0f0; }
.btn-view:hover { color: #1976d2; background-color: #e3f2fd; } .btn-edit:hover { color: #f57c00; background-color: #fff3e0; } .btn-delete:hover { color: #d32f2f; background-color: #ffebee; } .btn-activate:hover { color: #388e3c; background-color: #e8f5e9; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 8px; width: 90%; max-width: 500px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); display: flex; flex-direction: column; }
.modal-header { padding: 15px 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; } .modal-header h3 { margin: 0; color: #1a237e; font-size: 1.2rem; }
.modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #666; } .modal-body { padding: 20px; overflow-y: auto; max-height: 70vh; }
.form-group { margin-bottom: 15px; } .form-label { display: block; margin-bottom: 5px; font-weight: 500; color: #333; } .form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.view-group { margin-bottom: 15px; border-bottom: 1px solid #f9f9f9; padding-bottom: 10px; } .view-label { font-weight: 600; color: #555; display: block; font-size: 0.9rem; margin-bottom: 4px; } .view-value { color: #333; font-size: 1rem; }
.loading-overlay { position: absolute; inset: 0; background: rgba(255,255,255,0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
.spinner { width: 30px; height: 30px; border: 3px solid #f3f3f3; border-top: 3px solid #3949ab; border-radius: 50%; animation: spin 1s linear infinite; } @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.btn-primary { background: #1a237e; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; font-size: 0.95rem; } .btn-primary:hover { background: #283593; }
.no-data { text-align: center; padding: 20px; color: #999; }
</style>
