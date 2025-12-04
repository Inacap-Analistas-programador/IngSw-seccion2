<template>
  <ModernMainScrollbar>
    <div class="roles-view">
      <header class="page-header">
        <h3>Perfiles</h3>
        <p class="page-description">Administra los perfiles del sistema y sus permisos.</p>
      </header>

      <!-- Indicador de carga -->
      <div v-if="cargando" class="loading-container">
        <div class="spinner"></div>
        <p>Cargando perfiles...</p>
      </div>

      <div v-else>
        <div class="table-header-bar">
          <h3 class="table-title">Lista de Perfiles</h3>
          <div class="table-actions">
            <BaseButton variant="primary" @click="abrirCrear">
              <AppIcons name="plus" :size="16" /> Nuevo Perfil
            </BaseButton>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="usuarios-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th style="width:220px">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="error">
                <td colspan="3" style="color: var(--color-danger)">{{ error }}</td>
              </tr>
              <tr v-else-if="!roles.length">
                <td colspan="3">No hay perfiles registrados.</td>
              </tr>
              <tr v-else v-for="rol in roles" :key="rol.id">
                <td>{{ getDescripcion(rol) }}</td>
                <td>
                  <span class="badge" :class="!isVigente(rol) ? 'estado-inactivo' : 'badge-activo'">
                    {{ !isVigente(rol) ? 'Inactivo' : 'Activo' }}
                  </span>
                </td>
                <td class="actions-cell">
                  <BaseButton size="sm" variant="secondary" @click="abrirEditar(rol)">
                    <AppIcons name="edit" :size="14" /> Editar
                  </BaseButton>
                  <BaseButton size="sm" variant="secondary" @click="toggleVigente(rol)">
                    <AppIcons :name="!isVigente(rol) ? 'check' : 'x'" :size="14" />
                    {{ !isVigente(rol) ? 'Activar' : 'Desactivar' }}
                  </BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Modal Crear/Editar -->
      <BaseModal v-model="modalVisible" @close="cerrarModal">
        <template #default>
          <div class="modal-rol">
            <header class="modal-header">
                <h3>{{ editando ? 'Editar Perfil' : 'Nuevo Perfil' }}</h3>
              </header>
            <form class="rol-form" @submit.prevent="guardar">
              <!-- Sección Datos Básicos -->
              <div class="form-section datos-basicos">
                <div class="section-title">
                  <AppIcons name="user" :size="22" />
                  <span>Información del Perfil</span>
                </div>
                <div class="form-row">
                  <div class="form-group flex-1">
                    <label>Descripción <span class="required">*</span></label>
                    <InputBase v-model="form.descripcion" placeholder="Ej: Administrador" />
                  </div>
                  <div class="form-group estado-group">
                    <label>Estado</label>
                    <div class="estado-selector">
                      <span 
                        class="estado-badge" 
                        :class="form.vigente ? 'badge-activo' : 'estado-inactivo'"
                      >
                        {{ form.vigente ? 'Activo' : 'Inactivo' }}
                      </span>
                      <select v-model="form.vigente" class="estado-select">
                        <option :value="true">Activo</option>
                        <option :value="false">Inactivo</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sección Permisos -->
              <div class="form-section permisos-section">
                <div class="section-title">
                  <AppIcons name="lock" :size="22" />
                  <span>Permisos del Perfil</span>
                  <span class="permisos-subtitle">Define los permisos CRUD por módulo</span>
                </div>
                <div v-if="cargandoAplicaciones" class="loading-permisos">
                  <AppIcons name="refresh" :size="32" />
                  <p>Cargando permisos...</p>
                </div>
                <div v-else class="permisos-container">
                  <div class="table-responsive">
                    <table class="permisos-table">
                      <thead>
                        <tr>
                          <th class="col-app">Módulo</th>
                          <th class="text-center">Consultar</th>
                          <th class="text-center">Crear</th>
                          <th class="text-center">Modificar</th>
                          <th class="text-center">Eliminar</th>
                          <th class="text-center">Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="app in aplicaciones" :key="app.apl_id || app.APL_ID || app.id">
                          <td>
                            <div class="app-info">
                              <div class="app-icon-wrapper">
                                <AppIcons name="clipboard" :size="18" />
                              </div>
                              <span class="app-name">{{ app.apl_descripcion || app.APL_DESCRIPCION || app.descripcion }}</span>
                            </div>
                          </td>
                          <td class="text-center">
                            <BaseSwitch 
                              v-model="form.permisos[app.apl_id || app.APL_ID || app.id].consultar"
                            />
                          </td>
                          <td class="text-center">
                            <BaseSwitch 
                              v-model="form.permisos[app.apl_id || app.APL_ID || app.id].ingresar"
                            />
                          </td>
                          <td class="text-center">
                            <BaseSwitch 
                              v-model="form.permisos[app.apl_id || app.APL_ID || app.id].modificar"
                            />
                          </td>
                          <td class="text-center">
                            <BaseSwitch 
                              v-model="form.permisos[app.apl_id || app.APL_ID || app.id].eliminar"
                            />
                          </td>
                          <td class="text-center">
                            <div class="row-actions-compact">
                              <BaseButton size="sm" variant="secondary" title="Permitir Todo" @click="toggleTodosPermisos(app.apl_id || app.APL_ID || app.id, true)">
                                <AppIcons name="check" :size="16" />
                              </BaseButton>
                              <BaseButton size="sm" variant="secondary" title="Denegar Todo" @click="toggleTodosPermisos(app.apl_id || app.APL_ID || app.id, false)">
                                <AppIcons name="x" :size="16" />
                              </BaseButton>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <BaseButton variant="secondary" type="button" @click="cerrarModal">Cancelar</BaseButton>
                <BaseButton variant="primary" type="submit" :disabled="guardando || !formValido">
                  <AppIcons name="check" :size="16" /> {{ guardando ? 'Guardando...' : 'Guardar' }}
                </BaseButton>
              </div>
            </form>
          </div>
        </template>
      </BaseModal>

      <NotificationToast v-if="toast.visible" :message="toast.message" :type="toast.type" @close="toast.visible = false" />
    </div>
  </ModernMainScrollbar>
</template>

<script>
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseCheckBox from '@/components/BaseCheckBox.vue'
import BaseSwitch from '@/components/BaseSwitch.vue'
import InputBase from '@/components/InputBase.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import { perfiles as perfilesService, aplicaciones as aplicacionesService, perfilAplicaciones as perfilAplicacionesService } from '@/services/usuariosService'
import { request } from '@/services/apiClient'

export default {
  name: 'Roles',
  components: { BaseButton, BaseModal, BaseCheckBox, BaseSwitch, InputBase, NotificationToast, AppIcons, ModernMainScrollbar },
  data() {
    return {
      roles: [],
      aplicaciones: [],
      cargando: false,
      cargandoAplicaciones: false,
      guardando: false,
      error: null,
      modalVisible: false,
      editando: false,
      form: { 
        id: null, 
        descripcion: '', 
        vigente: true,
        permisos: {} // { aplicacionId: { consultar, ingresar, modificar, eliminar } }
      },
      toast: { visible: false, message: '', type: 'info' }
    }
  },
  computed: {
    formValido() {
      return !!(this.form.descripcion && this.form.descripcion.trim().length >= 3)
    }
  },
  async mounted() {
    await this.cargar()
    await this.cargarAplicaciones()
  },
  methods: {
    getDescripcion(rol) {
      if (!rol) return ''
      return rol.pel_descripcion || rol.PEL_DESCRIPCION || rol.descripcion || rol.nombre || ''
    },

    isVigente(rol) {
      if (rol.pel_vigente !== undefined) return rol.pel_vigente
      if (rol.PEL_VIGENTE !== undefined) return rol.PEL_VIGENTE
      if (rol.vigente !== undefined) return rol.vigente
      return true
    },
    
    async cargarAplicaciones() {
      this.cargandoAplicaciones = true
      try {
        const resp = await aplicacionesService.list()
        this.aplicaciones = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
        this.syncPermisosConAplicaciones()
      } catch (e) {
        console.error('Error cargando aplicaciones:', e)
        this.mostrarToast('No se pudieron cargar los módulos', 'warning')
        this.aplicaciones = []
      } finally {
        this.cargandoAplicaciones = false
      }
    },

    inicializarPermisos() {
      const permisos = {}
      this.aplicaciones.forEach(app => {
        const appId = app.apl_id || app.APL_ID || app.id
        permisos[appId] = {
          consultar: false,
          ingresar: false,
          modificar: false,
          eliminar: false
        }
      })
      return permisos
    },

    async cargarPermisosRol(rolId) {
      try {
        // Obtener permisos del rol desde perfil-aplicaciones
        const resp = await perfilAplicacionesService.list({ pel_id: rolId })
        const permisosList = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
        
        const permisos = this.inicializarPermisos()
        permisosList.forEach(p => {
          const appId = p.apl_id || p.APL_ID?.APL_ID || p.APL_ID
          if (permisos[appId]) {
            permisos[appId].consultar = p.pea_consultar || p.PEA_CONSULTAR || false
            permisos[appId].ingresar = p.pea_ingresar || p.PEA_INGRESAR || false
            permisos[appId].modificar = p.pea_modificar || p.PEA_MODIFICAR || false
            permisos[appId].eliminar = p.pea_eliminar || p.PEA_ELIMINAR || false
          }
        })
        return permisos
      } catch (e) {
        console.error('Error cargando permisos del rol:', e)
        return this.inicializarPermisos()
      }
    },

    payloadFromForm() {
      return {
        pel_descripcion: this.form.descripcion,
        pel_vigente: this.form.vigente,
        PEL_DESCRIPCION: this.form.descripcion,
        PEL_VIGENTE: this.form.vigente,
        descripcion: this.form.descripcion,
        vigente: this.form.vigente
      }
    },

    async cargar() {
      this.cargando = true
      this.error = null
      try {
        const resp = await perfilesService.list()
        this.roles = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
      } catch (e) {
        console.error('Error cargando roles:', e)
        this.error = e?.message || 'No se pudo cargar la lista de roles'
      } finally {
        this.cargando = false
      }
    },

    async abrirCrear() {
      this.editando = false
      this.form = { 
        id: null, 
        descripcion: '', 
        vigente: true,
        permisos: this.inicializarPermisos()
      }
      this.syncPermisosConAplicaciones()
      this.modalVisible = true
    },

    async abrirEditar(rol) {
      this.editando = true
      this.rolSeleccionado = rol
      const rolId = rol.pel_id || rol.PEL_ID || rol.id
      
      // Cargar permisos existentes
      const permisos = await this.cargarPermisosRol(rolId)
      
      this.form = {
        id: rolId,
        descripcion: this.getDescripcion(rol),
        vigente: this.isVigente(rol),
        permisos: permisos
      }
      this.syncPermisosConAplicaciones()
      this.modalVisible = true
    },

    syncPermisosConAplicaciones() {
      if (!this.form.permisos || typeof this.form.permisos !== 'object') {
        this.form.permisos = {}
      }

      const next = { ...this.form.permisos }
      this.aplicaciones.forEach(app => {
        const appId = app.apl_id || app.APL_ID || app.id
        if (!appId) return
        if (!next[appId]) {
          next[appId] = {
            consultar: false,
            ingresar: false,
            modificar: false,
            eliminar: false
          }
        } else {
          next[appId] = {
            consultar: !!next[appId].consultar,
            ingresar: !!next[appId].ingresar,
            modificar: !!next[appId].modificar,
            eliminar: !!next[appId].eliminar
          }
        }
      })

      this.form.permisos = next
    },

    cerrarModal() {
      this.modalVisible = false
      this.form = { 
        id: null, 
        descripcion: '', 
        vigente: true,
        permisos: {}
      }
    },

    async guardarPermisos(rolId, isNew = false) {
      if (!rolId) {
        console.error("No rolId provided to guardarPermisos");
        return;
      }

      // Preparar payload para envío masivo
      const permisosPayload = [];
      
      for (const appId in this.form.permisos) {
        const perms = this.form.permisos[appId]
        permisosPayload.push({
          apl_id: appId,
          pea_consultar: perms.consultar,
          pea_ingresar: perms.ingresar,
          pea_modificar: perms.modificar,
          pea_eliminar: perms.eliminar
        });
      }

      try {
        // Usar el nuevo endpoint de actualización masiva
        await request(`usuarios/perfiles/${rolId}/update-permissions/`, {
          method: 'POST',
          body: JSON.stringify({ permisos: permisosPayload })
        });
        
      } catch (e) {
        console.error("Error guardando permisos masivos:", e);
        throw e; // Re-lanzar para que el toast de error se muestre
      }
    },

    async guardar() {
      if (!this.formValido) return
      this.guardando = true
      try {
        let rolId = this.form.id
        
          if (this.editando && rolId != null) {
          await perfilesService.partialUpdate(rolId, this.payloadFromForm())
          await this.guardarPermisos(rolId)
          this.mostrarToast('Perfil y permisos actualizados', 'success')
        } else {
          const resp = await perfilesService.create(this.payloadFromForm())
          rolId = resp.pel_id || resp.PEL_ID || resp.id
          await this.guardarPermisos(rolId, true)
          this.mostrarToast('Perfil y permisos creados', 'success')
        }
        
        this.modalVisible = false
        await this.cargar()
      } catch (e) {
        console.error('Error guardando rol:', e)
        this.mostrarToast('No se pudo guardar el rol: ' + (e?.message || e), 'error')
      } finally {
        this.guardando = false
      }
    },

    async toggleVigente(rol) {
      try {
        const id = rol.pel_id || rol.PEL_ID || rol.id
        const actual = this.isVigente(rol)
        const nuevo = !actual
        await perfilesService.partialUpdate(id, { pel_vigente: nuevo, PEL_VIGENTE: nuevo, vigente: nuevo })
        await this.cargar()
      } catch (e) {
        console.error('Error cambiando estado:', e)
        this.mostrarToast('No se pudo cambiar el estado', 'error')
      }
    },

    mostrarToast(message, type = 'info') {
      this.toast = { visible: true, message, type }
      setTimeout(() => { this.toast.visible = false }, 3000)
    },

    togglePermiso(appId, permiso) {
      if (this.form.permisos[appId]) {
        this.form.permisos[appId][permiso] = !this.form.permisos[appId][permiso]
      }
    },

    toggleTodosPermisos(appId, valor) {
      if (this.form.permisos[appId]) {
        this.form.permisos[appId].consultar = valor
        this.form.permisos[appId].ingresar = valor
        this.form.permisos[appId].modificar = valor
        this.form.permisos[appId].eliminar = valor
      }
    }
  }
}
</script>

<style scoped>
/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  gap: 0.75rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.roles-view { max-width: 1100px; margin: 0 auto; padding: 1.5rem; }
.page-description { margin: 0; color: #7f8c8d; font-size: 14px; }

.table-header-bar { background: #fff; padding: .85rem 1rem; border-radius: 8px 8px 0 0; box-shadow: 0 2px 8px rgba(0,0,0,.1); display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #e0e0e0; }
.table-title { margin: 0; font-size: 1.05rem; font-weight: 700; color: #1e3a8a; position:relative; padding-left: 12px; }
.table-title::before { content:''; position:absolute; left:0; top:0; width:4px; height:100%; background:#1e3a8a; border-radius:2px; }
.table-wrapper { background: #fff; border-radius: 0 0 8px 8px; box-shadow: 0 2px 8px rgba(0,0,0,.1); overflow-y: auto; overflow-x: auto; max-height: calc(100vh - var(--navbar-height) - var(--card-top-offset)); }

.usuarios-table { width:100%; border-collapse: collapse; }
.usuarios-table thead { background: #3d4f5f; color: #fff; }
.usuarios-table th { padding: .75rem .85rem; text-align:left; font-weight:600; text-transform: uppercase; font-size: .8rem; letter-spacing:.5px; }
.usuarios-table td { padding: .75rem .85rem; border-bottom: 1px solid #e0e0e0; }

.actions-cell { display:flex; gap: 0.5rem; }

.row-actions { display:flex; gap:.4rem; }

.badge { display:inline-block; padding: 4px 14px; border-radius: 12px; font-size: .85rem; font-weight: 600; letter-spacing:.5px; box-shadow: 0 1px 4px rgba(0,0,0,.08); border:1px solid transparent; }
.badge-activo { background:#27ae60; color:#fff; }
.estado-inactivo { background:#95a5a6; color:#fff; }

/* Modal */
.modal-rol { 
  display: flex; 
  flex-direction: column; 
  max-height: 88vh;
  overflow: hidden;
}

.modal-rol .modal-header { 
  padding: 1.5rem 2rem 1rem 2rem; 
  border-bottom: 2px solid #e0e0e0; 
  flex-shrink: 0;
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
}

.modal-rol .modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #ffffff;
  font-weight: 700;
}

.rol-form { 
  padding: 2rem; 
  display:flex; 
  flex-direction: column; 
  gap: 2rem; 
  flex: 1;
  overflow-y: auto;
  background: #fafbfc;
}

/* Form Sections */
.form-section { 
  background: #ffffff; 
  border-radius: 16px; 
  padding: 2rem; 
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.datos-basicos {
  background: linear-gradient(to right, #ffffff 0%, #f8fafc 100%);
}

.form-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #2563eb;
  position: relative;
}

.permisos-subtitle {
  margin-left: auto;
  font-size: 0.8rem;
  font-weight: 500;
  color: #6b7280;
  font-style: italic;
}

.form-row { 
  display:flex; 
  gap:1rem; 
  align-items:flex-end; 
}

.form-group { 
  display:flex; 
  flex-direction: column; 
  gap:.35rem; 
}

.form-group.flex-1 { flex: 1; }

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.form-group .required { color: #e74c3c; }

.estado-group {
  min-width: 200px;
}

.estado-selector {
  position: relative;
  display: inline-block;
}

.estado-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid transparent;
  pointer-events: none;
  position: relative;
  z-index: 1;
}

.estado-select {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  font-size: 0.85rem;
}

/* Permisos Section */
.permisos-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: visible;
}

.loading-permisos {
  padding: 4rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-permisos p {
  margin: 0;
}

.permisos-container {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.table-responsive {
  overflow-x: auto;
}

.permisos-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.permisos-table th {
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
  letter-spacing: 0.05em;
}

.permisos-table th.text-center {
  text-align: center;
}

.permisos-table td {
  padding: 0.25rem 0.75rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.permisos-table tr:last-child td {
  border-bottom: none;
}

.permisos-table tr:hover {
  background-color: #f8fafc;
}

.app-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.app-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #eff6ff;
  border-radius: 8px;
  color: #3b82f6;
}

.app-name {
  font-weight: 600;
  color: #334155;
  font-size: 0.9rem;
}

.text-center {
  text-align: center;
}

.text-center :deep(.switch-container) {
  justify-content: center;
}

.row-actions-compact {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.action-mini-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-mini-btn.success {
  background: #dcfce7;
  color: #166534;
}

.action-mini-btn.success:hover {
  background: #bbf7d0;
}

.action-mini-btn.danger {
  background: #fee2e2;
  color: #991b1b;
}

.action-mini-btn.danger:hover {
  background: #fecaca;
}



.form-actions { 
  display: flex; 
  gap: 1rem; 
  justify-content: flex-end; 
  padding: 1.25rem 1.5rem;
  background: #ffffff;
  border-top: 2px solid #e0e0e0; 
  flex-shrink: 0;
}

.form-actions :deep(button) {
  min-width: 140px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.form-actions :deep(button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 768px) {
  .permisos-table th, .permisos-table td {
    padding: 0.5rem;
  }
  .app-name {
    font-size: 0.8rem;
  }
  
  .modal-rol {
    max-height: 95vh;
  }

  .aplicacion-section {
    padding: 1.25rem;
  }

  .permisos-container {
    max-height: 400px;
  }

  .rol-form {
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .form-section {
    padding: 1.5rem;
  }

  .permisos-quick-actions {
    flex-direction: column;
  }

  .quick-action-btn {
    width: 100%;
    justify-content: center;
  }

  .permiso-item {
    min-height: 120px;
  }
}
.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
}
.page-header { 
	margin-bottom: 2rem;
	padding-bottom: 1rem;
	border-bottom: 2px solid #e0e0e0;
}

/* Ajuste del botón cerrar del modal para que quede centrado en la esquina */
:deep(.close-btn) {
  top: 1.25rem;
  right: 1.25rem;
  width: 36px;
  height: 36px;
  background: var(--color-secondary) !important;
  color: #ffffff !important;
  border: none;
  backdrop-filter: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.close-btn:hover) {
  background: var(--color-secondary-hover) !important;
  color: #ffffff !important;
  transform: rotate(90deg);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}
</style>
