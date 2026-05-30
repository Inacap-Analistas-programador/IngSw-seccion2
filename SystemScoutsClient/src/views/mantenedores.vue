<template>
  <div class="crud-cursos-container">
    <!-- Error Alert -->
    <div v-if="error" class="error-alert">
      <p>{{ error }}</p>
      <button @click="error = null">×</button>
    </div>

    <!-- Page Header (estilo CRUDcursos) -->
    <div class="page-header">
      <h3>Mantenedores</h3>
      <p>Administra y gestiona las tablas maestras del sistema.</p>
    </div>

    <!-- Filtros / Selector de Mantenedor (estilo CRUDcursos .filtros) -->
    <div class="filtros">
      <div class="selector-dropdown" ref="dropdownContainer">
        <button 
          class="mantenedor-dropdown-toggle"
          :class="{ 'active': isDropdownOpen }"
          @click="toggleDropdown"
        >
          <span class="selected-option">
            {{ getSelectedTabInfo().icon }} {{ getSelectedTabInfo().label }}
          </span>
          <div class="dropdown-icon" :class="{ 'rotate': isDropdownOpen }">▼</div>
        </button>
        
        <ModernMainScrollbar v-if="isDropdownOpen" class="dropdown-menu" style="height: auto;">
          <div 
            v-for="tab in tabs" 
            :key="tab.id"
            class="dropdown-item"
            :class="{ 'active': activeTab === tab.id }"
            @click="selectTab(tab.id)"
          >
            <span class="dropdown-item-icon">{{ tab.icon }}</span>
            <span class="dropdown-item-text">{{ tab.label }}</span>
          </div>
        </ModernMainScrollbar>
      </div>

      <!-- Contenedor Destino para el Buscador (Teleport) -->
      <div id="search-container" class="search-target-container"></div>
      
      <!-- Botón Nuevo Item (Global) -->
      <button v-if="can.ingresar" class="btn-primary-global" type="button" @click="handleCreate">
          <AppIcons name="plus" :size="18" />
          <span class="btn-label-desktop">Nuevo</span>
      </button>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Componentes ya existentes -->
      <template v-if="isParentMounted">
       <MantenedorZonas           v-if="activeTab === 'zonas'"              :can="can" :ref="el => setComponentRef(el, 'zonas')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorDistritos       v-if="activeTab === 'distritos'"          :can="can" :ref="el => setComponentRef(el, 'distritos')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorGrupos          v-if="activeTab === 'grupos'"             :can="can" :ref="el => setComponentRef(el, 'grupos')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorRamas           v-if="activeTab === 'ramas'"              :can="can" :ref="el => setComponentRef(el, 'ramas')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorTiposCurso      v-if="activeTab === 'tipos-curso'"        :can="can" :ref="el => setComponentRef(el, 'tipos-curso')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorCargos          v-if="activeTab === 'cargos'"             :can="can" :ref="el => setComponentRef(el, 'cargos')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorProveedores     v-if="activeTab === 'proveedores'"        :can="can" :ref="el => setComponentRef(el, 'proveedores')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorAlimentacion    v-if="activeTab === 'alimentacion'"       :can="can" :ref="el => setComponentRef(el, 'alimentacion')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorComunas         v-if="activeTab === 'comunas'"            :can="can" :ref="el => setComponentRef(el, 'comunas')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />

        <!-- Componentes nuevos (antes inline) -->
        <MantenedorProvincias      v-if="activeTab === 'provincias'"         :can="can" :ref="el => setComponentRef(el, 'provincias')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorRegiones        v-if="activeTab === 'regiones'"           :can="can" :ref="el => setComponentRef(el, 'regiones')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorNiveles         v-if="activeTab === 'niveles'"            :can="can" :ref="el => setComponentRef(el, 'niveles')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorEstadoCivil     v-if="activeTab === 'estados-civiles'"    :can="can" :ref="el => setComponentRef(el, 'estados-civiles')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorRoles           v-if="activeTab === 'roles'"              :can="can" :ref="el => setComponentRef(el, 'roles')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorConceptosContables v-if="activeTab === 'conceptos-contables'" :can="can" :ref="el => setComponentRef(el, 'conceptos-contables')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
        <MantenedorTiposArchivo    v-if="activeTab === 'tipos-archivo'"      :can="can" :ref="el => setComponentRef(el, 'tipos-archivo')" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      </template>

      <!-- Modal de Confirmación compartido -->
      <div v-if="confirmModal && confirmModal.visible" class="modal-overlay" role="dialog" aria-modal="true">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ confirmModal.titulo }}</h3>
            <button class="modal-close" @click="cancelarConfirmacion">✕</button>
          </div>
          <div class="modal-body" style="padding:16px;">
            <p>{{ confirmModal.mensaje }}</p>
          </div>
          <div class="modal-footer" style="display:flex; gap:8px; justify-content:flex-end; padding:16px;">
            <BaseButton variant="secondary" @click="cancelarConfirmacion">
              <AppIcons name="close" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton variant="primary" @click="confirmarConfirmacion" :disabled="confirmLoading">
              <AppIcons name="check" :size="16" />
              <span v-if="!confirmLoading">Confirmar</span>
              <span v-else>Procesando...</span>
            </BaseButton>
          </div>
        </div>
      </div>
    </div>
    <div>
    <NotificationToast 
      v-if="toast.visible" 
      :message="toast.message" 
      :icon="toast.icon" 
      :type="toast.type"
      @close="toast.visible = false" 
    />
  </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import { usePermissions } from '@/composables/usePermissions'

import authService from '@/services/authService'
import NotificationToast from '@/components/NotificationToast.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'

// Componentes ya existentes
import MantenedorZonas from '@/components/mantenedores/MantenedorZonas.vue'
import MantenedorDistritos from '@/components/mantenedores/MantenedorDistritos.vue'
import MantenedorGrupos from '@/components/mantenedores/MantenedorGrupos.vue'
import MantenedorRamas from '@/components/mantenedores/MantenedorRamas.vue'
import MantenedorTiposCurso from '@/components/mantenedores/MantenedorTiposCurso.vue'
import MantenedorCargos from '@/components/mantenedores/MantenedorCargos.vue'
import MantenedorProveedores from '@/components/mantenedores/MantenedorProveedores.vue'
import MantenedorAlimentacion from '@/components/mantenedores/MantenedorAlimentacion.vue'
import MantenedorComunas from '@/components/mantenedores/MantenedorComunas.vue'

// Componentes nuevos (extraídos del inline)
import MantenedorProvincias from '@/components/mantenedores/MantenedorProvincias.vue'
import MantenedorRegiones from '@/components/mantenedores/MantenedorRegiones.vue'
import MantenedorNiveles from '@/components/mantenedores/MantenedorNiveles.vue'
import MantenedorEstadoCivil from '@/components/mantenedores/MantenedorEstadoCivil.vue'
import MantenedorRoles from '@/components/mantenedores/MantenedorRoles.vue'
import MantenedorConceptosContables from '@/components/mantenedores/MantenedorConceptosContables.vue'
import MantenedorTiposArchivo from '@/components/mantenedores/MantenedorTiposArchivo.vue'

export default {
  name: 'MantenedoresScouts',
  components: {
    BaseButton, AppIcons, NotificationToast, ModernMainScrollbar,
    MantenedorZonas, MantenedorDistritos, MantenedorGrupos, MantenedorRamas, MantenedorTiposCurso,
    MantenedorCargos, MantenedorProveedores, MantenedorAlimentacion, MantenedorComunas,
    MantenedorProvincias, MantenedorRegiones, MantenedorNiveles, MantenedorEstadoCivil,
    MantenedorRoles, MantenedorConceptosContables, MantenedorTiposArchivo
  },
  setup() {
    // Estado reactivo
    const activeTab = ref('')
    const isDropdownOpen = ref(false)
    const dropdownContainer = ref(null)
    const error = ref(null)
    const confirmModal = reactive({ visible: false, titulo: '', mensaje: '' })
    const confirmLoading = ref(false)
    const pendingConfirmAction = ref(null)
    const isParentMounted = ref(false)

    // Permisos dinámicos
    const can = reactive({
      consultar: false,
      ingresar: false,
      modificar: false,
      eliminar: false
    })

    const updateCurrentPermissions = async () => {
      const selected = getSelectedTabInfo()
      if (!selected || !selected.permission) return

      const [con, ing, mod, eli] = await Promise.all([
        authService.hasPermission(selected.permission, 'consultar'),
        authService.hasPermission(selected.permission, 'ingresar'),
        authService.hasPermission(selected.permission, 'modificar'),
        authService.hasPermission(selected.permission, 'eliminar')
      ])

      can.consultar = con
      can.ingresar = ing
      can.modificar = mod
      can.eliminar = eli
    }

    const allTabs = [
      { id: 'zonas', label: 'Zonas', icon: '🗺️', permission: 'Mantenedor - Zona' },
      { id: 'distritos', label: 'Distritos', icon: '📍', permission: 'Mantenedor - Distrito' },
      { id: 'grupos', label: 'Grupos', icon: '👥', permission: 'Mantenedor - Grupo' },
      { id: 'ramas', label: 'Ramas', icon: '🏕️', permission: 'Mantenedor - Rama' },
      { id: 'tipos-curso', label: 'Tipos de Curso', icon: '📚', permission: 'Mantenedor - Tipo Curso' },
      { id: 'cargos', label: 'Cargos', icon: '👔', permission: 'Mantenedor - Cargo' },
      { id: 'proveedores', label: 'Proveedores', icon: '🏷️', permission: 'Mantenedor - Proveedor' },
      { id: 'alimentacion', label: 'Alimentación', icon: '🍽️', permission: 'Mantenedor - Alimentacion' },
      { id: 'regiones', label: 'Regiones', icon: '🗾', permission: 'Mantenedor - Region' },
      { id: 'provincias', label: 'Provincias', icon: '🏞️', permission: 'Mantenedor - Provincia' },
      { id: 'comunas', label: 'Comunas', icon: '🏘️', permission: 'Mantenedor - Comuna' },
      { id: 'niveles', label: 'Niveles', icon: '📊', permission: 'Mantenedor - Nivel' },
      { id: 'estados-civiles', label: 'Estado Civil', icon: '💑', permission: 'Mantenedor - Estado Civil' },
      { id: 'roles', label: 'Roles', icon: '👤', permission: 'Mantenedor - Rol' },
      { id: 'conceptos-contables', label: 'Conceptos Contables', icon: '💰', permission: 'Mantenedor - Concepto Contable' },
      { id: 'tipos-archivo', label: 'Tipos de Archivo', icon: '📁', permission: 'Mantenedor - Tipo Archivo' }
    ]

    const tabs = ref([])

    const filterTabs = async () => {
      const user = await authService.getCurrentUser()
      const isAdmin = user && (user.role.toLowerCase().includes('admin') || user.role.toLowerCase().includes('sistema'))
      
      if (isAdmin) {
        tabs.value = allTabs
      } else {
        const authorizedTabs = []
        for (const tab of allTabs) {
          const hasConsultar = await authService.hasPermission(tab.permission, 'consultar')
          if (hasConsultar) {
            authorizedTabs.push(tab)
          }
        }
        tabs.value = authorizedTabs
      }

      if (tabs.value.length > 0) {
        // Si la pestaña activa no está en las autorizadas, cambiar a la primera disponible
        if (!tabs.value.find(t => t.id === activeTab.value)) {
          activeTab.value = tabs.value[0].id
        }
        await updateCurrentPermissions()
      }
    }

    const getSelectedTabInfo = () => tabs.value.find(t => t.id === activeTab.value) || tabs.value[0] || allTabs[0]
    const toggleDropdown = () => { isDropdownOpen.value = !isDropdownOpen.value }
    const selectTab = async (id) => { 
      activeTab.value = id
      isDropdownOpen.value = false
      await updateCurrentPermissions()
    }

    const handleClickOutside = (e) => {
      if (dropdownContainer.value && !dropdownContainer.value.contains(e.target)) {
        isDropdownOpen.value = false
      }
    }

    // Toast State
    const toast = reactive({ visible: false, message: '', icon: '', type: 'info' })
    const showToast = (message, icon = 'check', type = 'info') => {
      toast.message = message
      toast.icon = icon
      toast.type = type
      toast.visible = true
      setTimeout(() => { toast.visible = false }, 3000)
    }

    // Mensajes y confirmaciones de los hijos
    const handleMessage = (msg) => {
      if (msg.type === 'error') showToast(msg.text, 'alert-triangle', 'error')
      else if (msg.type === 'success') showToast(msg.text, 'check', 'success')
      else showToast(msg.text, 'info', 'info')
    }

    const handleConfirmAction = (conf) => {
      confirmModal.titulo = conf.titulo
      confirmModal.mensaje = conf.mensaje
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
        error.value = 'Error al ejecutar la acción'
      } finally {
        confirmLoading.value = false
        cancelarConfirmacion()
      }
    }

    // Referencia al componente activo para llamar a sus métodos
    const activeComponentRef = ref(null)

    // Función para asignar la ref dinámicamente desde el template
    const setComponentRef = (el, tabId) => {
      if (el) {
        if (activeTab.value === tabId) {
          activeComponentRef.value = el
        }
      } else {
        // Al desmontar, solo limpiar si sigue siendo la pestaña activa
        if (activeTab.value === tabId) {
          activeComponentRef.value = null
        }
      }
    }

    const handleCreate = () => {
        console.log('handleCreate click', activeComponentRef.value)
        if (activeComponentRef.value && typeof activeComponentRef.value.abrirModalCrear === 'function') {
            activeComponentRef.value.abrirModalCrear()
        } else {
            console.warn('El componente activo no tiene expuesto el método abrirModalCrear', activeComponentRef.value)
             // Fallback o mensaje para componentes aún no migrados (opcional)
             showToast('Funcionalidad no disponible para este mantenedor aún', 'alert-circle', 'error')
        }
    }

    onMounted(async () => { 
      document.addEventListener('click', handleClickOutside) 
      isParentMounted.value = true
      await filterTabs()
    })
    onUnmounted(() => { document.removeEventListener('click', handleClickOutside) })

    return {
      activeTab, isDropdownOpen, dropdownContainer, error,
      confirmModal, confirmLoading, tabs,
      getSelectedTabInfo, toggleDropdown, selectTab,
      handleMessage, handleConfirmAction,
      cancelarConfirmacion, confirmarConfirmacion,
      toast, activeComponentRef, handleCreate, setComponentRef,
      isParentMounted, can
    }
  }
}
</script>

<style scoped>
/* Container principal - idéntico a CRUDcursos */
.crud-cursos-container {
  padding: 24px;
  box-sizing: border-box;
  font-family: 'Inter', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* Page Header - idéntico a CRUDcursos */
.page-header {
  margin-bottom: 24px;
}

.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin: 4px 0 0;
}

/* Filtros - mismo layout que CRUDcursos */
.filtros {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
}

.search-target-container {
  flex: 1;
  max-width: 600px;
  order: 2;
}

.selector-dropdown {
  order: 1;
}

.btn-primary-global {
  order: 3;
}

/* Dropdown Selector Styles (Restaurados) */
.selector-dropdown {
  position: relative;
  min-width: 250px;
}

.mantenedor-dropdown-toggle {
  width: 100%;
  padding: 8px 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  height: 40px; /* Igualar altura con el botón nuevo */
}

.mantenedor-dropdown-toggle:hover {
  border-color: #9ca3af;
}

.mantenedor-dropdown-toggle.active {
  border-color: #1a237e;
  box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
}

.dropdown-icon {
  font-size: 0.8rem;
  color: #6b7280;
  transition: transform 0.2s;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-top: 4px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 50;
  max-height: 300px;
  overflow-y: auto;
}

.dropdown-item {
  padding: 10px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
}

.dropdown-item.active {
  background-color: #e8eaf6;
  color: #1a237e;
  font-weight: 500;
}

.dropdown-item-icon {
  font-size: 1.1rem;
}

/* Fix for long text in dropdown */
.selected-option {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  max-width: 100%;
}

/* Responsive: Ajustes específicos para móviles */
@media (max-width: 768px) {
  .filtros { 
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .selector-dropdown { 
    flex: 1; 
    max-width: calc(100% - 54px); /* Ensure space for the button (42px + gap) */
    min-width: 0;
    order: 1;
  }
  
  .btn-primary-global {
    order: 2;
    flex-shrink: 0; /* No encoger el botón */
    width: 42px; /* Ancho fijo cuadrado en móvil */
    padding: 0 !important; /* Sin padding lateral */
    justify-content: center !important;
    gap: 0 !important;
    margin-left: auto; /* Push to right if wrapping happens, though flex should handle it */
  }

  .search-target-container {
    order: 3;
    width: 100%;
    max-width: none;
    margin-top: 4px;
    flex-basis: 100%; /* Force new line */
  }
  
  .mantenedor-dropdown-toggle { width: 100%; }
  
  .btn-label-desktop {
    display: none;
  }
  
  /* Fix icon centering: Override default AppIcons margin */
  .btn-primary-global :deep(svg) {
    margin-right: 0 !important;
  }
}

@media (max-width: 450px) {
  .crud-cursos-container { 
    padding: 16px;
    height: auto !important;
    overflow: visible !important;
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  height: 100%;
  position: relative;
  padding: 16px 0px; /* Requested padding */
}

@media (max-width: 768px) {
  .main-content {
    overflow: visible !important; /* Permitir scroll natural en el body/contenedor padre en móvil */
    height: auto !important;   /* Permitir que crezca con el contenido (tarjetas) */
    display: block; 
  }
}

.btn-primary-global {
  background: #1a237e;
  color: white;
  border: none;
  padding: 0 16px;
  height: 40px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: background 0.2s;
  min-width: 40px; 
}

.btn-primary-global:hover {
  background: #283593;
}

/* Shared Confirmation Modal Styles */
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
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1a237e;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
  padding: 4px;
}

.modal-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
}
</style>