<template>
  <ModernMainScrollbar>
    <div class="roles-view">
      <PageHeader
        title="Perfiles"
        subtitle="Administra los perfiles del sistema y sus permisos."
      />

      <div class="table-header-bar">
        <h3 class="table-title">Lista de Perfiles</h3>
        <div class="table-actions">
          <BaseButton v-if="can.ingresar" variant="primary" @click="abrirCrear">
            <AppIcons name="plus" :size="16" /> Nuevo Perfil
          </BaseButton>
        </div>
      </div>

      <!-- Indicador de carga -->
      <div v-if="cargando" class="loading-container">
        <div class="spinner"></div>
        <p>Cargando perfiles...</p>
      </div>

      <div v-else class="table-wrapper">
        <table class="usuarios-table">
          <thead>
            <tr>
              <th>Descripción</th>
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
              <td class="actions-cell">
                <BaseButton v-if="can.modificar" size="sm" variant="secondary" @click="abrirEditar(rol)">
                  <AppIcons name="edit" :size="14" /> Editar
                </BaseButton>
                <BaseButton v-if="can.eliminar" size="sm" variant="secondary" @click="toggleVigente(rol)">
                  <AppIcons :name="!isVigente(rol) ? 'check' : 'x'" :size="14" />
                  {{ !isVigente(rol) ? 'Activar' : 'Desactivar' }}
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
                          <th class="text-center">Cambiar Estado / Eliminar</th>
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
                            <BaseButton 
                              type="button"
                              size="sm" 
                              :variant="form.permisos[app.apl_id || app.APL_ID || app.id].consultar ? 'primary' : 'secondary'"
                              @click="form.permisos[app.apl_id || app.APL_ID || app.id].consultar = !form.permisos[app.apl_id || app.APL_ID || app.id].consultar"
                            >
                              <AppIcons :name="form.permisos[app.apl_id || app.APL_ID || app.id].consultar ? 'check' : 'x'" :size="14" />
                            </BaseButton>
                          </td>
                          <td class="text-center">
                            <BaseButton 
                              type="button"
                              size="sm" 
                              :variant="form.permisos[app.apl_id || app.APL_ID || app.id].ingresar ? 'primary' : 'secondary'"
                              @click="form.permisos[app.apl_id || app.APL_ID || app.id].ingresar = !form.permisos[app.apl_id || app.APL_ID || app.id].ingresar"
                            >
                              <AppIcons :name="form.permisos[app.apl_id || app.APL_ID || app.id].ingresar ? 'check' : 'x'" :size="14" />
                            </BaseButton>
                          </td>
                          <td class="text-center">
                            <BaseButton 
                              type="button"
                              size="sm" 
                              :variant="form.permisos[app.apl_id || app.APL_ID || app.id].modificar ? 'primary' : 'secondary'"
                              @click="form.permisos[app.apl_id || app.APL_ID || app.id].modificar = !form.permisos[app.apl_id || app.APL_ID || app.id].modificar"
                            >
                              <AppIcons :name="form.permisos[app.apl_id || app.APL_ID || app.id].modificar ? 'check' : 'x'" :size="14" />
                            </BaseButton>
                          </td>
                          <td class="text-center">
                            <BaseButton 
                              type="button"
                              size="sm" 
                              :variant="form.permisos[app.apl_id || app.APL_ID || app.id].eliminar ? 'danger' : 'secondary'"
                              @click="form.permisos[app.apl_id || app.APL_ID || app.id].eliminar = !form.permisos[app.apl_id || app.APL_ID || app.id].eliminar"
                            >
                              <AppIcons :name="form.permisos[app.apl_id || app.APL_ID || app.id].eliminar ? 'check' : 'x'" :size="14" />
                            </BaseButton>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <!-- ─── Sección Ámbito de Datos ───────────────────────────── -->
              <div class="form-section ambito-section">
                <div class="section-title">
                  <AppIcons name="map-pin" :size="22" />
                  <span>Ámbito de Datos</span>
                  <span class="permisos-subtitle">Restricción geográfica de visibilidad</span>
                </div>

                <!-- Selector de Nivel -->
                <div class="ambito-niveles">
                  <button
                    v-for="n in nivelesAmbito"
                    :key="n.valor"
                    type="button"
                    class="nivel-btn"
                    :class="{ active: form.ambito.nivel === n.valor }"
                    @click="onNivelChange(n.valor)"
                  >
                    <span class="nivel-icon">{{ nivelIcon(n.valor) }}</span>
                    <span class="nivel-label">{{ n.etiqueta }}</span>
                  </button>
                </div>

                <!-- Descripción del nivel seleccionado -->
                <p class="nivel-desc">{{ nivelDescripcion }}</p>

                <!-- Selects anidados -->
                <div class="ambito-selects">
                  <!-- Zona -->
                  <div v-if="form.ambito.nivel <= 3" class="form-group">
                    <label>Zona <span class="required">*</span></label>
                    <select
                      v-model="form.ambito.zona"
                      class="ambito-select"
                      @change="onZonaChange"
                      :disabled="cargandoGeo"
                    >
                      <option :value="null">— Seleccionar zona —</option>
                      <option v-for="z in zonas" :key="z.zon_id" :value="z.zon_id">
                        {{ z.zon_descripcion }}
                      </option>
                    </select>
                  </div>

                  <!-- Distrito -->
                  <div v-if="form.ambito.nivel <= 2" class="form-group">
                    <label>Distrito <span class="required">*</span></label>
                    <select
                      v-model="form.ambito.distrito"
                      class="ambito-select"
                      @change="onDistritoChange"
                      :disabled="cargandoGeo || !form.ambito.zona"
                    >
                      <option :value="null">— Seleccionar distrito —</option>
                      <option v-for="d in distritosFiltrados" :key="d.dis_id" :value="d.dis_id">
                        {{ d.dis_descripcion }}
                      </option>
                    </select>
                    <span v-if="!form.ambito.zona" class="ambito-hint">Selecciona primero una zona</span>
                  </div>

                  <!-- Grupo -->
                  <div v-if="form.ambito.nivel === 1" class="form-group">
                    <label>Grupo <span class="required">*</span></label>
                    <select
                      v-model="form.ambito.grupo"
                      class="ambito-select"
                      :disabled="cargandoGeo || !form.ambito.distrito"
                    >
                      <option :value="null">— Seleccionar grupo —</option>
                      <option v-for="g in gruposFiltrados" :key="g.gru_id" :value="g.gru_id">
                        {{ g.gru_descripcion }}
                      </option>
                    </select>
                    <span v-if="!form.ambito.distrito" class="ambito-hint">Selecciona primero un distrito</span>
                  </div>
                </div>
              </div>
              <!-- ─────────────────────────────────────────────────────────── -->

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
import BaseSwitch from '@/components/BaseSwitch.vue'
import InputBase from '@/components/InputBase.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import { perfiles as perfilesService, aplicaciones as aplicacionesService, perfilesAmbito as perfilesAmbitoService } from '@/services/usuariosService'
import { zona as zonaService, distrito as distritoService, grupo as grupoService } from '@/services/mantenedoresService'
import { usePermissions } from '@/composables/usePermissions'

export default {
  name: 'Roles',
  components: { BaseButton, BaseModal, BaseSwitch, InputBase, NotificationToast, AppIcons, ModernMainScrollbar },
  setup() {
    const { can } = usePermissions('Perfiles')
    return { can }
  },
  data() {
    return {
      roles: [],
      aplicaciones: [],
      nivelesAmbito: [], // [{ valor, etiqueta }]
      // Listas de geo para selects
      zonas: [],
      distritos: [],  // todos los distritos cargados
      grupos: [],     // todos los grupos cargados
      cargandoGeo: false,
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
        permisos: {},
        ambito: { nivel: 4, zona: null, distrito: null, grupo: null }
      },
      toast: { visible: false, message: '', type: 'info' }
    }
  },
  computed: {
    formValido() {
      return !!(this.form.descripcion && this.form.descripcion.trim().length >= 3)
    },
    distritosFiltrados() {
      if (!this.form.ambito.zona) return []
      return this.distritos.filter(d => d.zon_id === this.form.ambito.zona)
    },
    gruposFiltrados() {
      if (!this.form.ambito.distrito) return []
      return this.grupos.filter(g => g.dis_id === this.form.ambito.distrito)
    },
    nivelDescripcion() {
      const niveles = {
        4: 'Sin restricciones. El perfil puede ver toda la información del sistema.',
        3: 'Solo puede ver datos de la zona seleccionada y sus distritos.',
        2: 'Solo puede ver datos del distrito seleccionado dentro de la zona.',
        1: 'Solo puede ver datos del grupo específico dentro del distrito y zona.',
      }
      return niveles[this.form.ambito.nivel] || ''
    },
  },
  async mounted() {
    await Promise.all([
      this.cargar(),
      this.cargarAplicaciones(),
      this.cargarGeo(),
    ])
  },
  methods: {
    getDescripcion(rol) {
      if (!rol) return ''
      return rol.name || rol.pel_descripcion || rol.PEL_DESCRIPCION || rol.descripcion || ''
    },

    isVigente(rol) {
      if (rol.pel_vigente !== undefined) return rol.pel_vigente
      if (rol.PEL_VIGENTE !== undefined) return rol.PEL_VIGENTE
      if (rol.vigente !== undefined) return rol.vigente
      return true
    },

    nivelIcon(nivel) {
      return { 4: '🌐', 3: '🗺️', 2: '📍', 1: '👥' }[nivel] || '❓'
    },

    onNivelChange(nivel) {
      this.form.ambito = { nivel, zona: null, distrito: null, grupo: null }
    },

    onZonaChange() {
      this.form.ambito.distrito = null
      this.form.ambito.grupo    = null
    },

    onDistritoChange() {
      this.form.ambito.grupo = null
    },

    async cargarGeo() {
      this.cargandoGeo = true
      try {
        // Cargar niveles con fallback estático por si el endpoint requiere auth
        const nivelesPromise = perfilesAmbitoService.getNiveles().catch(() => null)
        const [zonasResp, distritosResp, gruposResp] = await Promise.all([
          zonaService.list(),
          distritoService.list(),
          grupoService.list(),
        ])
        this.zonas     = Array.isArray(zonasResp)     ? zonasResp     : (zonasResp?.results     || [])
        this.distritos = Array.isArray(distritosResp) ? distritosResp : (distritosResp?.results || [])
        this.grupos    = Array.isArray(gruposResp)    ? gruposResp    : (gruposResp?.results    || [])

        // Niveles: usar respuesta del API o fallback estático
        const nivelesResp = await nivelesPromise
        this.nivelesAmbito = nivelesResp
          ? (Array.isArray(nivelesResp) ? nivelesResp : (nivelesResp.results || []))
          : [
              { valor: 4, etiqueta: 'Global' },
              { valor: 3, etiqueta: 'Zona' },
              { valor: 2, etiqueta: 'Distrito' },
              { valor: 1, etiqueta: 'Grupo (Restricto)' },
            ]
      } catch (e) {
        console.error('Error cargando geo:', e)
        // Fallback estático de niveles
        this.nivelesAmbito = [
          { valor: 4, etiqueta: 'Global' },
          { valor: 3, etiqueta: 'Zona' },
          { valor: 2, etiqueta: 'Distrito' },
          { valor: 1, etiqueta: 'Grupo (Restricto)' },
        ]
      } finally {
        this.cargandoGeo = false
      }
    },

    async cargarAplicaciones() {
      this.cargandoAplicaciones = true
      try {
        const resp = await aplicacionesService.list()
        const allPerms = Array.isArray(resp) ? resp : (resp.results || resp.data || [])
        
        // Agrupar permisos por modelo (content_type)
        const grouped = {}
        allPerms.forEach(p => {
          // Si el nombre tiene el formato "Módulo | Modelo | Acción", extraemos el módulo
            const parts = p.name.split(' | ')
          let model = parts.length > 1 ? parts[1] : (p.codename.split('_').slice(1).join('_') || p.codename)
          
          // Soporte para permisos de pantalla específicos: view_screen_persona -> persona
          if (model === 'screen' && p.codename.startsWith('view_screen_')) {
            const cparts = p.codename.split('_')
            if (cparts.length > 2) model = cparts.slice(2).join('_')
          }
          
          if (!grouped[model]) {
            grouped[model] = {
              id: model,
              descripcion: model.charAt(0).toUpperCase() + model.slice(1),
              perms: { consultar: null, ingresar: null, modificar: null, eliminar: null }
            }
          }
          if (p.codename.startsWith('view_')) grouped[model].perms.consultar = p.id
          if (p.codename.startsWith('add_')) grouped[model].perms.ingresar = p.id
          if (p.codename.startsWith('change_')) grouped[model].perms.modificar = p.id
          if (p.codename.startsWith('delete_')) grouped[model].perms.eliminar = p.id
        })
        
        this.aplicaciones = Object.values(grouped).filter(g => g.perms.consultar || g.perms.ingresar)
      } catch (e) {
        console.error('Error cargando permisos:', e)
        this.mostrarToast('No se pudieron cargar los permisos', 'warning')
      } finally {
        this.cargandoAplicaciones = false
      }
    },

    inicializarPermisos() {
      const permisos = {}
      this.aplicaciones.forEach(app => {
        permisos[app.id] = {
          consultar: false,
          ingresar: false,
          modificar: false,
          eliminar: false
        }
      })
      return permisos
    },

    async cargarPermisosRol(rol) {
      const permisosIds = rol.permissions || []
      const permisos = this.inicializarPermisos()
      
      this.aplicaciones.forEach(app => {
        const appId = app.id
        if (permisos[appId]) {
          permisos[appId].consultar = permisosIds.includes(app.perms.consultar)
          permisos[appId].ingresar = permisosIds.includes(app.perms.ingresar)
          permisos[appId].modificar = permisosIds.includes(app.perms.modificar)
          permisos[appId].eliminar = permisosIds.includes(app.perms.eliminar)
        }
      })
      return permisos
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
        permisos: this.inicializarPermisos(),
        ambito: { nivel: 4, zona: null, distrito: null, grupo: null }
      }
      this.modalVisible = true
    },

    async abrirEditar(rol) {
      this.editando = true
      this.cargandoAplicaciones = true
      this.modalVisible = true
      
      try {
        // Obtener el perfil completo (Group en Django) porque el listado suele ser resumido
        const fullRol = await perfilesService.get(rol.id)
        this.rolSeleccionado = fullRol
        
        const [permisos, ambitoResp] = await Promise.all([
          this.cargarPermisosRol(fullRol),
          perfilesAmbitoService.getAmbito(rol.id).catch(() => null),
        ])
        
        this.form = {
          id: fullRol.id,
          descripcion: fullRol.name || this.getDescripcion(fullRol),
          vigente: true,
          permisos,
          ambito: ambitoResp
            ? { nivel: ambitoResp.nivel, zona: ambitoResp.zona, distrito: ambitoResp.distrito, grupo: ambitoResp.grupo }
            : { nivel: 4, zona: null, distrito: null, grupo: null },
        }
      } catch (e) {
        console.error('Error al cargar detalle del perfil:', e)
        this.mostrarToast('No se pudieron cargar los detalles del perfil', 'error')
        this.cerrarModal()
      } finally {
        this.cargandoAplicaciones = false
      }
    },

    cerrarModal() {
      this.modalVisible = false
      this.form = { 
        id: null, 
        descripcion: '', 
        vigente: true,
        permisos: {},
        ambito: { nivel: 4, zona: null, distrito: null, grupo: null }
      }
    },

    async guardar() {
      if (!this.formValido) return
      this.guardando = true
      try {
        // Recopilar IDs de permisos seleccionados
        const selectedPerms = []
        this.aplicaciones.forEach(app => {
          const p = this.form.permisos[app.id]
          if (p.consultar && app.perms.consultar) selectedPerms.push(app.perms.consultar)
          if (p.ingresar && app.perms.ingresar) selectedPerms.push(app.perms.ingresar)
          if (p.modificar && app.perms.modificar) selectedPerms.push(app.perms.modificar)
          if (p.eliminar && app.perms.eliminar) selectedPerms.push(app.perms.eliminar)
        })

        const payload = {
          name: this.form.descripcion,
          permissions: selectedPerms
        }
        
        let savedId = this.form.id
        if (this.editando) {
          await perfilesService.update(this.form.id, payload)
          this.mostrarToast('Perfil actualizado', 'success')
        } else {
          const created = await perfilesService.create(payload)
          savedId = created?.id
          this.mostrarToast('Perfil creado', 'success')
        }

        // Guardar el ámbito por separado
        if (savedId) {
          await perfilesAmbitoService.updateAmbito(savedId, this.form.ambito).catch(e =>
            console.warn('No se pudo guardar el ámbito:', e)
          )
        }
        
        this.modalVisible = false
        await this.cargar()
      } catch (e) {
        console.error('Error guardando rol:', e)
        this.mostrarToast('No se pudo guardar el rol', 'error')
      } finally {
        this.guardando = false
      }
    },

    async toggleVigente(rol) {
      try {
        const id = rol.PEL_ID || rol.id
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

/* ── Ámbito de Datos ─────────────────────────────────────────────────── */
.ambito-section {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #bae6fd;
}

.ambito-niveles {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.nivel-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.75rem 1.25rem;
  border: 2px solid #cbd5e1;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 90px;
  font-family: inherit;
}
.nivel-btn:hover {
  border-color: #2563eb;
  background: #eff6ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
}
.nivel-btn.active {
  border-color: #2563eb;
  background: #2563eb;
  color: #fff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  transform: translateY(-2px);
}
.nivel-icon {
  font-size: 1.4rem;
  line-height: 1;
}
.nivel-label {
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nivel-desc {
  font-size: 0.85rem;
  color: #475569;
  background: rgba(255,255,255,0.7);
  border-left: 3px solid #2563eb;
  padding: 0.6rem 0.9rem;
  border-radius: 0 6px 6px 0;
  margin-bottom: 1.25rem;
  min-height: 2rem;
}

.ambito-selects {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.ambito-select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9rem;
  font-family: inherit;
  background: #fff;
  color: #374151;
  transition: border-color 0.2s;
  cursor: pointer;
}
.ambito-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}
.ambito-select:disabled {
  background: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

.ambito-hint {
  font-size: 0.75rem;
  color: #9ca3af;
  font-style: italic;
}
/* ─────────────────────────────────────────────────────────────────────── */

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
  gap: 0.75rem;
  line-height: 1;
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
  margin: 0;
}

.permiso-control {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.permiso-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  transition: color 0.2s;
}

.permiso-label.text-active {
  color: #2563eb;
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

/* Loading Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  gap: 1rem;
  color: #6b7280;
  font-weight: 500;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
