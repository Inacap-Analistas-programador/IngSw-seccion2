<template>
  <div class="gestion-personas">
    <!-- Toasts de notificación -->
    <div class="toast-container">
      <NotificationToast
        v-for="(alerta, index) in alertas"
        :key="alerta.id"
        :message="alerta.message"
        :type="alerta.type"
        :icon="alerta.type === 'success' ? 'check' : 'alert-circle'"
        @close="removerAlerta(alerta.id)"
        :style="{ marginBottom: `${index * 60}px` }"
      />
    </div>

    <PageHeader 
      title="Gestión de Personas" 
      subtitle="Administra los miembros, sus roles, grupos y estados de formación."
    />

    <!-- Filtros -->
    <PersonaFilters 
      v-model:searchQuery="filtros.q"
      v-model:selectedRole="filtros.rol"
      v-model:selectedGroup="filtros.grupo"
      v-model:selectedEnrolledCourse="filtros.curso"
      v-model:selectedRama="filtros.rama"
      :role-options="options.roles"
      :group-options="options.grupos"
      :course-options="options.cursos"
      :rama-options="options.ramas"
      :has-any-filter="hasAnyFilter"
      @search="cargarPersonas"
      @clear="limpiarFiltros"
    />

    <!-- Header estilo Mantenedor (Copiado de CRUDcursos) -->
    <div class="mantenedor-header">
      <div class="header-content">
        <h2>Personas</h2>
        <div class="header-actions-group">
          <BaseButton class="header-icon-btn" variant="primary" v-if="canCreate" @click="handleCreateClick" title="Nueva Persona">
            <AppIcons name="plus" :size="20" />
            <span class="btn-label-desktop">Nuevo</span>
          </BaseButton>
          <BaseButton class="header-icon-btn" variant="secondary" @click="modals.import = true" title="Importar Excel">
            <AppIcons name="upload" :size="20" />
            <span class="btn-label-desktop">Importar</span>
          </BaseButton>
          <BaseButton class="header-icon-btn" variant="secondary" @click="modals.export = true" title="Exportar Datos">
            <AppIcons name="download" :size="20" />
            <span class="btn-label-desktop">Exportar</span>
          </BaseButton>
        </div>
      </div>
    </div>

      <!-- Content Area -->
      
      <!-- Tabla -->
      <div class="table-container-fixed">
        <PersonaTable 
          :personas="filteredPersonas" 
          :hasSearched="state.hasSearched"
          :can-edit="canEdit"
          :can-delete="canDelete"
          @view="(p) => abrirModalPersona(p, true)"
          @edit="(p) => abrirModalPersona(p, false)"
          @deactivate="confirmarAnulacion"
          @reactivate="confirmarReactivacion"
        />
      </div>

    <!-- Modal Formulario (Crear/Editar/Ver) -->
    <BaseModal v-model="modals.form" :title="formTitle" class="modal-xl">
      <PersonaForm 
        v-if="modals.form"
        :initial-data="personaEditada"
        :options="options"
        :history="personaEditada.cursosHistorial"
        :is-edit="!!personaEditada.PER_ID"
        :is-read-only="modoSoloLectura"
        :loading="guardando"
        @save="handleSave"
        @cancel="modals.form = false"
        @region-change="cargarProvincias"
        @provincia-change="cargarComunas"
        @nav-course="navToCourse"
        @show-alert="mostrarAlerta"
      />
    </BaseModal>

    <!-- Otros Modales (Import, Export, RUT) -->
    <PersonaModals 
      v-model:rutModalVisible="modals.rut"
      v-model:importModalVisible="modals.import"
      v-model:exportModalVisible="modals.export"
      :importing="importando"
      :import-preview="importPreview"
      @rut-check="checkRutExistencia"
      @download-template="exportarPlantilla"
      @file-selected="procesarExcel"
      @import-execute="importarPersonas"
      @export-excel="exportarExcel"
      @export-emails="copyEmails"
    />

    <!-- Modal de Confirmación Estilizado (Premium) -->
    <Teleport to="body">
      <div v-if="confirmModal.visible" class="modal-overlay-glass" @mousedown.self="cancelarConfirmacion">
        <div class="modal-content-premium confirmation-modal-box">
          <div class="modal-header-premium">
            <div class="header-title">
              <AppIcons :name="confirmModal.type === 'danger' ? 'alert-triangle' : 'help-circle'" :size="24" />
              <h3>{{ confirmModal.titulo }}</h3>
            </div>
            <button type="button" class="modal-close-btn" @click="cancelarConfirmacion">✕</button>
          </div>
          <div class="modal-body-premium">
            <p class="text-slate-600 text-lg">{{ confirmModal.mensaje }}</p>
          </div>
          <div class="modal-footer-premium">
            <BaseButton variant="secondary" @click="cancelarConfirmacion">
              <AppIcons name="x" :size="18" style="margin-right: 8px;" />
              Cancelar
            </BaseButton>
            <BaseButton 
              :variant="confirmModal.type === 'danger' ? 'danger' : 'primary'" 
              @click="confirmarConfirmacion" 
              :disabled="confirmLoading"
            >
              <AppIcons :name="confirmLoading ? 'refresh' : 'check'" :size="18" :class="{ 'spin': confirmLoading }" style="margin-right: 8px;" />
              {{ confirmLoading ? 'Procesando...' : 'Confirmar' }}
            </BaseButton>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal: Confirmación Rut Existente (Premium Design) -->
    <Teleport to="body">
      <div v-if="modals.confirmExist" class="modal-overlay-glass" @mousedown.self="cancelarEdicionExistente">
        <div class="modal-content-premium rut-modal-box" role="dialog" aria-modal="true">
          <div class="modal-header-premium">
            <div class="header-title">
              <AppIcons name="alert-circle" :size="24" style="color: #eab308;" />
              <h3>RUT Existente</h3>
            </div>
            <button type="button" class="modal-close-btn" @click="cancelarEdicionExistente">✕</button>
          </div>
          <div class="modal-body-premium">
            <p class="mb-4 text-slate-700 font-medium">Este RUT ya se encuentra registrado en el sistema bajo el nombre de <strong>{{ personaExistente?.PER_NOMBRES }} {{ personaExistente?.PER_APELPTA }}</strong>.</p>
            <p class="text-slate-500 text-sm">¿Deseas abrir su perfil para editar sus datos en lugar de crear un nuevo registro?</p>
          </div>
          <div class="modal-footer-premium">
            <BaseButton variant="secondary" @click="cancelarEdicionExistente" class="btn-large">No, Cambiar RUT</BaseButton>
            <BaseButton variant="primary" @click="confirmarEdicionExistente" class="btn-large">
              <AppIcons name="edit" :size="20" style="margin-right: 8px;" />
              Sí, Editar Persona
            </BaseButton>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import PageHeader from '@/components/common/PageHeader.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import PersonaFilters from '@/components/personas/PersonaFilters.vue'
import PersonaTable from '@/components/personas/PersonaTable.vue'
import PersonaForm from '@/components/personas/PersonaForm.vue'
import PersonaModals from '@/components/personas/PersonaModals.vue'

import personasService from '@/services/personasService.js'
import mantenedoresService from '@/services/mantenedoresService.js'
import { usePermissions } from '@/composables/usePermissions'
import { toUpperKeys } from '@/utils/formatters'

export default {
  name: 'GestionPersonas',
  components: { 
    PageHeader, NotificationToast, BaseButton, BaseModal, AppIcons, 
    PersonaFilters, PersonaTable, PersonaForm, PersonaModals 
  },
  setup() {
    const { isAdmin, canCreate, canEdit, canDelete } = usePermissions()
    
    // State
    const loading = ref(false)
    const guardando = ref(false)
    const importando = ref(false)
    const modoSoloLectura = ref(false)
    const personas = ref([])
    const filteredPersonas = ref([])
    const personaEditada = ref({})
    const importPreview = ref([])
    const alertas = ref([])
    
    const filtros = reactive({
      q: '',
      rol: '',
      grupo: '',
      curso: '',
      rama: ''
    })
    
    const options = reactive({
      roles: [],
      grupos: [],
      cursos: [],
      ramas: [],
      regiones: [],
      provincias: [],
      comunas: [],
      estadoCivil: [],
      alimentacion: [],
      niveles: []
    })
    
    const modals = reactive({ form: false, rut: false, import: false, export: false, confirmExist: false })
    const confirmModal = reactive({ visible: false, titulo: '', mensaje: '', type: 'primary' })
    const confirmLoading = ref(false)
    const pendingConfirmAction = ref(null)

    const isMobile = ref(window.innerWidth < 1024)
    const hasAnyFilter = computed(() => {
      const f = filtros
      return !!((f.q && f.q.trim()) || f.rol || f.grupo || f.curso || f.rama)
    })
    const filtrosColapsados = ref(isMobile.value)

    const formTitle = computed(() => {
       if (modoSoloLectura.value) return 'Consulta de Persona'
       return personaEditada.value.PER_ID ? 'Editar Información' : 'Registrar Nueva Persona'
    })

    // Methods Alert
    function mostrarAlerta(message, type = 'success') {
      const id = Date.now()
      alertas.value.push({ id, message, type })
      setTimeout(() => removerAlerta(id), 5000)
    }
    function removerAlerta(id) {
      alertas.value = alertas.value.filter(a => a.id !== id)
    }

    // Methods Data
    const cargarCatalogos = async () => {
      try {
        const [roles, grupos, cursos, ramas, regiones, ec, ali, niv] = await Promise.all([
          personasService.obtenerRoles(),
          personasService.obtenerGrupos(),
          personasService.personaCursos.list(),
          personasService.obtenerRamas(),
          mantenedoresService.region.list(),
          mantenedoresService.estadoCivil.list(),
          mantenedoresService.alimentacion.list(),
          mantenedoresService.nivel.list()
        ])
        
        options.roles = roles
        options.grupos = grupos
        options.cursos = (cursos.results || cursos).map(c => ({ value: c.CUR_ID || c.cur_id, label: c.CUR_NOMBRE || c.descripcion || c.cur_nombre }))
        options.ramas = ramas
        options.regiones = (regiones.results || regiones).map(r => ({ value: r.REG_ID || r.reg_id, label: r.REG_NOMBRE || r.reg_descripcion }))
        options.estadoCivil = (ec.results || ec).map(e => ({ value: e.ESC_ID || e.esc_id, label: e.ESC_DESCRIPCION || e.esc_descripcion }))
        options.alimentacion = (ali.results || ali).map(a => ({ value: a.ALI_ID || a.ali_id, label: a.ALI_NOMBRE || a.ali_descripcion }))
        options.niveles = (niv.results || niv).map(n => ({ value: n.NIV_ID || n.niv_id, label: n.NIV_DESCRIPCION || n.niv_descripcion }))
      } catch (e) {
        console.error('Error cargando catálogos:', e)
      }
    }

    const state = reactive({
      hasSearched: false
    })

    const cargarPersonas = async () => {
      // Si no hay filtros aplicados, vaciamos la lista
      if (!filtros.q && !filtros.rol && !filtros.grupo && !filtros.rama && !filtros.curso) {
        personas.value = []
        filteredPersonas.value = []
        state.hasSearched = false
        return
      }

      loading.value = true
      state.hasSearched = true
      
      try {
        const params = {}
        if (filtros.q) params.q = filtros.q
        
        const resp = await personasService.personas.paraMantenedor(params)
        const rawList = Array.isArray(resp) ? resp : (resp && Array.isArray(resp.results) ? resp.results : [])
        personas.value = rawList.map(toUpperKeys)
        ejecutarFiltrado()
      } catch (e) {
        console.error('Error cargando personas:', e)
        mostrarAlerta('Error al cargar datos. Intenta nuevamente.', 'error')
      } finally {
        loading.value = false
      }
    }

    const ejecutarFiltrado = () => {
      let result = [...personas.value]
      const q = filtros.q.toLowerCase()
      
      if (q) {
        result = result.filter(p => 
          `${p.PER_NOMBRES} ${p.PER_APELPTA} ${p.PER_APELMAT}`.toLowerCase().includes(q) ||
          String(p.PER_RUN).includes(q) ||
          (p.PER_MAIL && p.PER_MAIL.toLowerCase().includes(q))
        )
      }
      
      if (filtros.rol) result = result.filter(p => p.ROL_ID == filtros.rol || p.PER_ROL == filtros.rol)
      if (filtros.grupo) result = result.filter(p => p.GRU_ID == filtros.grupo || p.PER_GRUPO == filtros.grupo)
      if (filtros.rama) result = result.filter(p => p.RAM_ID == filtros.rama || p.PER_RAMA == filtros.rama)
      
      filteredPersonas.value = result
    }

    const toggleFiltros = () => { filtrosColapsados.value = !filtrosColapsados.value }

    const limpiarFiltros = () => {
      filtros.q = ''
      filtros.rol = ''
      filtros.grupo = ''
      filtros.curso = ''
      filtros.rama = ''
      // Limpiamos la búsqueda manualmente
      cargarPersonas()
    }

    const handleCreateClick = () => {
      modoSoloLectura.value = false
      personaEditada.value = {
        PER_VIGENTE: true,
        ramas: [{ NIV_ID: '', RAM_ID_NIVEL: '' }]
      }
      modals.rut = true
    }

    const personaExistente = ref(null)

    const checkRutExistencia = async (rutData) => {
      try {
        // Consultamos al endpoint ultra-rápido de verificación
        const response = await personasService.personas.checkRut(rutData.run)
        
        if (response.exists && response.persona) {
          // Guardamos la referencia para mostrar el nombre
          personaExistente.value = response.persona
          // Cerramos modal de RUT y abrimos el de confirmación
          modals.rut = false
          modals.confirmExist = true // This modal is still used for RUT confirmation
        } else {
          personaEditada.value.PER_RUN = rutData.run
          personaEditada.value.PER_DV = rutData.dv
          modals.rut = false
          modals.form = true
        }
      } catch (e) {
        mostrarAlerta('Error al verificar RUT en el servidor', 'error')
      }
    }

    const confirmarEdicionExistente = () => {
      modals.confirmExist = false
      abrirModalPersona(personaExistente.value, false)
    }

    const cancelarEdicionExistente = () => {
      modals.confirmExist = false
      modals.rut = true // Vuelve al selector de RUT
    }

    const abrirModalPersona = async (persona, soloLectura = false) => {
      loading.value = true
      try {
        const fullPersona = await personasService.personas.get(persona.PER_ID)
        personaEditada.value = toUpperKeys(fullPersona)
        modoSoloLectura.value = soloLectura
        
        const hist = await personasService.obtenerCursosPersona(persona.PER_ID)
        personaEditada.value.cursosHistorial = (hist || []).map(toUpperKeys)
        
        if (personaEditada.value.REG_ID) await cargarProvincias(personaEditada.value.REG_ID)
        if (personaEditada.value.PRO_ID) await cargarComunas(personaEditada.value.PRO_ID)
        
        modals.form = true
      } catch (e) {
        mostrarAlerta('Error al cargar detalle de persona', 'error')
      } finally {
        loading.value = false
      }
    }

    const cargarProvincias = async (regId) => {
      const resp = await mantenedoresService.provincia.list({ reg_id: regId })
      const list = resp.results || resp
      options.provincias = list.map(p => ({ value: p.PRO_ID, label: p.PRO_NOMBRE }))
    }

    const cargarComunas = async (proId) => {
      const resp = await mantenedoresService.comuna.list({ pro_id: proId })
      const list = resp.results || resp
      options.comunas = list.map(c => ({ value: c.COM_ID, label: c.COM_NOMBRE }))
    }

    const handleSave = async (data) => {
      guardando.value = true
      try {
        if (data.PER_ID) {
          await personasService.personas.update(data.PER_ID, data)
          mostrarAlerta('Persona actualizada exitosamente', 'success')
        } else {
          await personasService.personas.create(data)
          mostrarAlerta('Persona registrada exitosamente', 'success')
        }
        await cargarPersonas()
        modals.form = false
      } catch (e) {
        mostrarAlerta('Error al guardar datos. Revisa los campos obligatorios.', 'error')
      } finally {
        guardando.value = false
      }
    }

    const handleConfirmAction = (conf) => {
      confirmModal.titulo = conf.titulo
      confirmModal.mensaje = conf.mensaje
      confirmModal.type = conf.type || 'primary'
      confirmModal.visible = true
      pendingConfirmAction.value = conf.accion
    }

    const cancelarConfirmacion = () => {
      confirmModal.visible = false
      confirmModal.titulo = ''
      confirmModal.mensaje = ''
      pendingConfirmAction.value = null
    }

    const confirmarConfirmacion = async () => {
      if (!pendingConfirmAction.value) return
      confirmLoading.value = true
      try {
        await pendingConfirmAction.value()
      } catch (e) {
        console.error('Error en confirmación:', e)
        mostrarAlerta('Error al ejecutar la acción', 'error')
      } finally {
        confirmLoading.value = false
        cancelarConfirmacion()
      }
    }

    const confirmarAnulacion = (p) => {
      handleConfirmAction({
        titulo: 'Anular Persona',
        mensaje: `¿Estás seguro de que deseas anular a ${p.PER_NOMBRES}? Esto desactivará su acceso al sistema.`,
        type: 'danger',
        accion: async () => {
          await personasService.personas.partialUpdate(p.PER_ID, { per_vigente: false })
          mostrarAlerta('Persona anulada exitosamente', 'success')
          await cargarPersonas()
        }
      })
    }

    const confirmarReactivacion = (p) => {
      handleConfirmAction({
        titulo: 'Reactivar Persona',
        mensaje: `¿Deseas reactivar a ${p.PER_NOMBRES}?`,
        type: 'primary',
        accion: async () => {
          await personasService.personas.partialUpdate(p.PER_ID, { per_vigente: true })
          mostrarAlerta('Persona reactivada exitosamente', 'success')
          await cargarPersonas()
        }
      })
    }

    const exportarExcel = () => { mostrarAlerta('Exportando a Excel...', 'info') }
    const copyEmails = () => { mostrarAlerta('Emails copiados al portapapeles', 'success') }
    const procesarExcel = (file) => { mostrarAlerta('Archivo seleccionado: ' + file.name, 'info') }
    const importarPersonas = () => { mostrarAlerta('Iniciando importación...', 'info') }
    const exportarPlantilla = () => { mostrarAlerta('Descargando plantilla...', 'info') }
    const navToCourse = (id) => { window.location.hash = `#/cursos/${id}` }

    onMounted(() => {
      // Fetch only catalogs on mount, keep table empty until search
      cargarCatalogos()
      window.addEventListener('resize', () => {
        isMobile.value = window.innerWidth < 1024
      })
    })

      return {
      isAdmin, canCreate, canEdit, canDelete,
      loading, guardando, importando, modoSoloLectura,
      filteredPersonas, personaEditada, importPreview, alertas,
      filtros, options, modals, isMobile, filtrosColapsados, hasAnyFilter,
      formTitle, toggleFiltros, ejecutarFiltrado, limpiarFiltros, handleCreateClick,
      checkRutExistencia, abrirModalPersona, cargarProvincias, cargarComunas,
      handleSave, confirmarAnulacion, confirmarReactivacion,
      confirmModal, confirmLoading, cancelarConfirmacion, confirmarConfirmacion,
      exportarExcel, copyEmails, procesarExcel, importarPersonas, exportarPlantilla, navToCourse,
      removerAlerta, mostrarAlerta, state, cargarPersonas,
      personaExistente, confirmarEdicionExistente, cancelarEdicionExistente
    }
  }
}
</script>

<style scoped>
/* Glassmorphism Classes */
.modal-overlay-glass {
  position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 20px;
}
.modal-content-premium {
  background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 24px;
  width: 100%; max-width: 500px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); overflow: hidden;
}
.modal-header-premium {
  padding: 24px; display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
.header-title { display: flex; align-items: center; gap: 12px; color: #1e293b; }
.header-title h3 { margin: 0; font-size: 1.25rem; font-weight: 700; }
.modal-close-btn {
  background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; cursor: pointer; color: #64748b; transition: all 0.2s;
}
.modal-close-btn:hover { background: #e2e8f0; color: #0f172a; transform: rotate(90deg); }
.modal-body-premium { padding: 32px 24px; }
.modal-footer-premium {
  padding: 20px 24px; background: rgba(248, 250, 252, 0.5);
  display: flex; justify-content: flex-end; gap: 12px; border-top: 1px solid #e2e8f0;
}
.btn-large { padding: 12px 24px !important; font-weight: 600 !important; border-radius: 12px !important; }

.gestion-personas {
  padding: 0 24px 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
}

/* Mantenedor Header Sub-layout (Sync with CRUDcursos) */
.mantenedor-header { 
  margin-bottom: 20px; 
  padding: 32px 0px 16px; 
  border-bottom: 2px solid #3949ab; 
}

.header-content { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  width: 100%; 
}

.mantenedor-header h2 { font-size: 1.5rem; color: #1a237e; margin: 0; font-weight: 700; }
.header-actions-group { display: flex; gap: 12px; }

.header-icon-btn {
  height: 40px !important;
  min-width: 40px !important;
  padding: 0 16px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 6px;
  font-weight: 600 !important;
}

.btn-label-desktop {
  margin-left: 8px;
}

/* Loading Indicator (Sync with CursoDashboard/CRUDcursos) */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #6b7280;
  flex: 1;
}

.spinner {
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.table-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  flex: 1;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.glass-panel {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
}

.table-container-fixed {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

/* Modals sizing */
.modal-xl :deep(.modal-content) {
  max-width: 1200px;
  width: 95%;
}

@media (max-width: 768px) {
  .btn-label-desktop { display: none; }
  .header-icon-btn { padding: 0 !important; width: 40px !important; }
}
</style>
