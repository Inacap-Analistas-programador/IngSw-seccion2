<template>
  <ModernMainScrollbar>
    <div class="roles-view">
      <header class="page-header">
        <h3>Roles</h3>
        <p class="page-description">Administra los perfiles (roles) del sistema y sus permisos.</p>
      </header>

      <div class="table-header-bar">
        <h3 class="table-title">Lista de Roles</h3>
        <div class="table-actions">
          <BaseButton variant="primary" @click="abrirCrear">
            <AppIcons name="plus" :size="16" /> Nuevo Rol
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
            <tr v-if="cargando">
              <td colspan="3">Cargando roles...</td>
            </tr>
            <tr v-else-if="error">
              <td colspan="3" style="color: var(--color-danger)">{{ error }}</td>
            </tr>
            <tr v-else-if="!roles.length">
              <td colspan="3">No hay roles registrados.</td>
            </tr>
            <tr v-else v-for="rol in roles" :key="rol.id">
              <td>{{ getDescripcion(rol) }}</td>
              <td>
                <span class="badge" :class="rol.PEL_VIGENTE === false ? 'estado-inactivo' : 'badge-activo'">
                  {{ rol.PEL_VIGENTE === false ? 'Inactivo' : 'Activo' }}
                </span>
              </td>
              <td class="row-actions">
                <BaseButton size="sm" variant="secondary" @click="abrirEditar(rol)">
                  <AppIcons name="edit" :size="14" /> Editar
                </BaseButton>
                <BaseButton size="sm" variant="secondary" @click="toggleVigente(rol)">
                  <AppIcons :name="rol.PEL_VIGENTE === false ? 'check' : 'x'" :size="14" />
                  {{ rol.PEL_VIGENTE === false ? 'Activar' : 'Desactivar' }}
                </BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal Crear/Editar -->
      <BaseModal v-model="modalVisible" @close="cerrarModal">
        <template #default>
          <div class="modal-rol">
            <header class="modal-header">
              <h3>{{ editando ? 'Editar Rol' : 'Nuevo Rol' }}</h3>
            </header>
            <form class="rol-form" @submit.prevent="guardar">
              <!-- Sección Datos Básicos -->
              <div class="form-section datos-basicos">
                <div class="section-title">
                  <AppIcons name="user" :size="22" />
                  <span>Información del Rol</span>
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
                  <span>Permisos del Rol</span>
                  <span class="permisos-subtitle">Define los permisos CRUD por módulo</span>
                </div>
                <div v-if="cargandoAplicaciones" class="loading-permisos">
                  <AppIcons name="refresh" :size="32" />
                  <p>Cargando permisos...</p>
                </div>
                <div v-else class="permisos-container">
                  <div v-for="app in aplicaciones" :key="app.APL_ID || app.id" class="aplicacion-section">
                    <div class="aplicacion-header">
                      <div class="aplicacion-title-wrapper">
                        <AppIcons name="clipboard" :size="22" class="aplicacion-icon" />
                        <h4 class="aplicacion-nombre">{{ app.APL_DESCRIPCION || app.descripcion }}</h4>
                      </div>
                      <div class="permisos-quick-actions">
                        <button 
                          type="button" 
                          class="quick-action-btn"
                          @click="toggleTodosPermisos(app.APL_ID || app.id, true)"
                          title="Seleccionar todos"
                        >
                          <AppIcons name="check" :size="14" /> Todos
                        </button>
                        <button 
                          type="button" 
                          class="quick-action-btn clear"
                          @click="toggleTodosPermisos(app.APL_ID || app.id, false)"
                          title="Quitar todos"
                        >
                          <AppIcons name="x" :size="14" /> Ninguno
                        </button>
                      </div>
                    </div>
                    <div class="permisos-grid">
                      <div class="permiso-item" @click="togglePermiso(app.APL_ID || app.id, 'consultar')">
                        <div class="permiso-content">
                          <div class="permiso-icon-wrapper">
                            <AppIcons name="view" :size="24" class="permiso-icon" />
                          </div>
                          <div class="permiso-info">
                            <span class="permiso-label">Consultar</span>
                            <span class="permiso-description">Ver información</span>
                          </div>
                        </div>
                        <BaseSwitch 
                          v-model="form.permisos[app.APL_ID || app.id].consultar"
                        />
                      </div>
                      <div class="permiso-item" @click="togglePermiso(app.APL_ID || app.id, 'ingresar')">
                        <div class="permiso-content">
                          <div class="permiso-icon-wrapper">
                            <AppIcons name="add" :size="24" class="permiso-icon" />
                          </div>
                          <div class="permiso-info">
                            <span class="permiso-label">Crear</span>
                            <span class="permiso-description">Agregar nuevos registros</span>
                          </div>
                        </div>
                        <BaseSwitch 
                          v-model="form.permisos[app.APL_ID || app.id].ingresar"
                        />
                      </div>
                      <div class="permiso-item" @click="togglePermiso(app.APL_ID || app.id, 'modificar')">
                        <div class="permiso-content">
                          <div class="permiso-icon-wrapper">
                            <AppIcons name="modify" :size="24" class="permiso-icon" />
                          </div>
                          <div class="permiso-info">
                            <span class="permiso-label">Modificar</span>
                            <span class="permiso-description">Editar registros existentes</span>
                          </div>
                        </div>
                        <BaseSwitch 
                          v-model="form.permisos[app.APL_ID || app.id].modificar"
                        />
                      </div>
                      <div class="permiso-item" @click="togglePermiso(app.APL_ID || app.id, 'eliminar')">
                        <div class="permiso-content">
                          <div class="permiso-icon-wrapper">
                            <AppIcons name="delete" :size="24" class="permiso-icon" />
                          </div>
                          <div class="permiso-info">
                            <span class="permiso-label">Eliminar</span>
                            <span class="permiso-description">Borrar registros</span>
                          </div>
                        </div>
                        <BaseSwitch 
                          v-model="form.permisos[app.APL_ID || app.id].eliminar"
                        />
                      </div>
                    </div>
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
      return rol.PEL_DESCRIPCION || rol.descripcion || rol.nombre || ''
    },
    
    async cargarAplicaciones() {
      this.cargandoAplicaciones = true
      try {
        const resp = await aplicacionesService.list()
        this.aplicaciones = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
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
        const appId = app.APL_ID || app.id
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
        const resp = await perfilAplicacionesService.list({ PEL_ID: rolId })
        const permisosList = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
        
        const permisos = this.inicializarPermisos()
        permisosList.forEach(p => {
          const appId = p.APL_ID?.APL_ID || p.APL_ID
          if (permisos[appId]) {
            permisos[appId].consultar = p.PEA_CONSULTAR || false
            permisos[appId].ingresar = p.PEA_INGRESAR || false
            permisos[appId].modificar = p.PEA_MODIFICAR || false
            permisos[appId].eliminar = p.PEA_ELIMINAR || false
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
      this.modalVisible = true
    },

    async abrirEditar(rol) {
      this.editando = true
      this.rolSeleccionado = rol
      const rolId = rol.PEL_ID || rol.id
      
      // Cargar permisos existentes
      const permisos = await this.cargarPermisosRol(rolId)
      
      this.form = {
        id: rolId,
        descripcion: this.getDescripcion(rol),
        vigente: rol.PEL_VIGENTE !== false,
        permisos: permisos
      }
      this.modalVisible = true
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

    async guardarPermisos(rolId) {
      // Guardar permisos por cada aplicación
      const promises = []
      
      for (const appId in this.form.permisos) {
        const perms = this.form.permisos[appId]
        
        try {
          // Buscar si ya existe una entrada perfil-aplicación
          const existingResp = await perfilAplicacionesService.list({ 
            PEL_ID: rolId, 
            APL_ID: appId 
          })
          const existingList = Array.isArray(existingResp) ? existingResp : (existingResp.results || existingResp.data || [])
          const existing = existingList[0]

          const permisoData = {
            PEL_ID: rolId,
            APL_ID: appId,
            PEA_CONSULTAR: perms.consultar,
            PEA_INGRESAR: perms.ingresar,
            PEA_MODIFICAR: perms.modificar,
            PEA_ELIMINAR: perms.eliminar
          }

          if (existing) {
            // Actualizar
            promises.push(perfilAplicacionesService.partialUpdate(existing.PEA_ID || existing.id, permisoData))
          } else {
            // Crear
            promises.push(perfilAplicacionesService.create(permisoData))
          }
        } catch (e) {
          console.error(`Error procesando permisos para app ${appId}:`, e)
        }
      }

      await Promise.all(promises)
    },

    async guardar() {
      if (!this.formValido) return
      this.guardando = true
      try {
        let rolId = this.form.id
        
        if (this.editando && rolId != null) {
          await perfilesService.partialUpdate(rolId, this.payloadFromForm())
          await this.guardarPermisos(rolId)
          this.mostrarToast('Rol y permisos actualizados', 'success')
        } else {
          const resp = await perfilesService.create(this.payloadFromForm())
          rolId = resp.PEL_ID || resp.id
          await this.guardarPermisos(rolId)
          this.mostrarToast('Rol y permisos creados', 'success')
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
        const id = rol.PEL_ID || rol.id
        const nuevo = !(rol.PEL_VIGENTE === false)
        await perfilesService.partialUpdate(id, { PEL_VIGENTE: !nuevo, vigente: !nuevo })
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
.roles-view { max-width: 1100px; margin: 0 auto; padding: 1.5rem; }
.page-description { margin: 0; color: #7f8c8d; font-size: 14px; }

.table-header-bar { background: #fff; padding: .85rem 1rem; border-radius: 8px 8px 0 0; box-shadow: 0 2px 8px rgba(0,0,0,.1); display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #e0e0e0; }
.table-title { margin: 0; font-size: 1.05rem; font-weight: 700; color: #1e3a8a; position:relative; padding-left: 12px; }
.table-title::before { content:''; position:absolute; left:0; top:0; width:4px; height:100%; background:#1e3a8a; border-radius:2px; }
.table-wrapper { background: #fff; border-radius: 0 0 8px 8px; box-shadow: 0 2px 8px rgba(0,0,0,.1); overflow:hidden; }

.usuarios-table { width:100%; border-collapse: collapse; }
.usuarios-table thead { background: #3d4f5f; color: #fff; }
.usuarios-table th { padding: .75rem .85rem; text-align:left; font-weight:600; text-transform: uppercase; font-size: .8rem; letter-spacing:.5px; }
.usuarios-table td { padding: .75rem .85rem; border-bottom: 1px solid #e0e0e0; }

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
  gap: 1.5rem;
  padding: 1rem;
}

.aplicacion-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 16px;
  padding: 1.75rem;
  border: 2px solid #e9ecef;
  box-shadow: 0 3px 8px rgba(0,0,0,.05);
  transition: all 0.3s ease;
}

.aplicacion-section:hover {
  border-color: #2563eb;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.2);
  transform: translateY(-3px);
}

.aplicacion-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #dee2e6;
}

.aplicacion-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.aplicacion-icon {
  color: #2563eb;
  flex-shrink: 0;
}

.aplicacion-nombre {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 0.3px;
}

.permisos-quick-actions {
  display: flex;
  gap: 0.5rem;
}

.quick-action-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 0.75rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
}

.quick-action-btn:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
}

.quick-action-btn.clear {
  background: #6b7280;
}

.quick-action-btn.clear:hover {
  background: #4b5563;
}

.permisos-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.permiso-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem 1rem;
  background: #ffffff;
  border-radius: 12px;
  border: 2px solid #e9ecef;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  min-height: 140px;
  text-align: center;
}

.permiso-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.permiso-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  align-items: center;
}

.permiso-label {
  font-size: 1.05rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 0.3px;
}

.permiso-description {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
  line-height: 1.3;
}

.permiso-item::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 4px;
  background: #2563eb;
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.permiso-item:hover::before {
  transform: scaleX(1);
}

.permiso-item:hover {
  background: #eff6ff;
  border-color: #2563eb;
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.2);
}

.permiso-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #f3f4f6;
  border-radius: 14px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.permiso-item:hover .permiso-icon-wrapper {
  background: #dbeafe;
}

.permiso-icon {
  color: #6b7280;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.permiso-item:hover .permiso-icon {
  color: #2563eb;
}

.permiso-item :deep(.p-4) {
  padding: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  max-width: none !important;
}

.permiso-item :deep(.switch-container) {
  pointer-events: none;
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
@media (max-width: 1024px) {
  .permisos-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .permisos-grid {
    grid-template-columns: 1fr;
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
</style>
