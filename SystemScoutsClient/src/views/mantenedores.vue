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
      <div class="filtros-left">
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
          
          <div v-if="isDropdownOpen" class="dropdown-menu">
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
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Componentes ya existentes -->
      <MantenedorZonas           v-if="activeTab === 'zonas'"              @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorDistritos       v-if="activeTab === 'distritos'"          @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorGrupos          v-if="activeTab === 'grupos'"             @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorRamas           v-if="activeTab === 'ramas'"              @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorTiposCurso      v-if="activeTab === 'tipos-curso'"        @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorCargos          v-if="activeTab === 'cargos'"             @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorProveedores     v-if="activeTab === 'proveedores'"        @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorAlimentacion    v-if="activeTab === 'alimentacion'"       @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorComunas         v-if="activeTab === 'comunas'"            @show-message="handleMessage" @confirm-action="handleConfirmAction" />

      <!-- Componentes nuevos (antes inline) -->
      <MantenedorProvincias      v-if="activeTab === 'provincias'"         @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorRegiones        v-if="activeTab === 'regiones'"           @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorNiveles         v-if="activeTab === 'niveles'"            @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorEstadoCivil     v-if="activeTab === 'estados-civiles'"    @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorRoles           v-if="activeTab === 'roles'"              @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorConceptosContables v-if="activeTab === 'conceptos-contables'" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      <MantenedorTiposArchivo    v-if="activeTab === 'tipos-archivo'"      @show-message="handleMessage" @confirm-action="handleConfirmAction" />

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
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

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
    BaseButton, AppIcons,
    MantenedorZonas, MantenedorDistritos, MantenedorGrupos, MantenedorRamas, MantenedorTiposCurso,
    MantenedorCargos, MantenedorProveedores, MantenedorAlimentacion, MantenedorComunas,
    MantenedorProvincias, MantenedorRegiones, MantenedorNiveles, MantenedorEstadoCivil,
    MantenedorRoles, MantenedorConceptosContables, MantenedorTiposArchivo
  },
  setup() {
    const activeTab = ref('zonas')
    const isDropdownOpen = ref(false)
    const dropdownContainer = ref(null)
    const error = ref(null)
    const confirmModal = reactive({ visible: false, titulo: '', mensaje: '' })
    const confirmLoading = ref(false)
    const pendingConfirmAction = ref(null)

    const tabs = [
      { id: 'zonas', label: 'Zonas', icon: '🗺️' },
      { id: 'distritos', label: 'Distritos', icon: '📍' },
      { id: 'grupos', label: 'Grupos', icon: '👥' },
      { id: 'ramas', label: 'Ramas', icon: '🏕️' },
      { id: 'tipos-curso', label: 'Tipos de Curso', icon: '📚' },
      { id: 'cargos', label: 'Cargos', icon: '👔' },
      { id: 'proveedores', label: 'Proveedores', icon: '🏷️' },
      { id: 'alimentacion', label: 'Alimentación', icon: '🍽️' },
      { id: 'comunas', label: 'Comunas', icon: '🏘️' },
      { id: 'provincias', label: 'Provincias', icon: '🏞️' },
      { id: 'regiones', label: 'Regiones', icon: '🗾' },
      { id: 'niveles', label: 'Niveles', icon: '📊' },
      { id: 'estados-civiles', label: 'Estado Civil', icon: '💑' },
      { id: 'roles', label: 'Roles', icon: '👤' },
      { id: 'conceptos-contables', label: 'Conceptos Contables', icon: '💰' },
      { id: 'tipos-archivo', label: 'Tipos de Archivo', icon: '📁' }
    ]

    const getSelectedTabInfo = () => tabs.find(t => t.id === activeTab.value) || tabs[0]
    const toggleDropdown = () => { isDropdownOpen.value = !isDropdownOpen.value }
    const selectTab = (id) => { activeTab.value = id; isDropdownOpen.value = false }

    const handleClickOutside = (e) => {
      if (dropdownContainer.value && !dropdownContainer.value.contains(e.target)) {
        isDropdownOpen.value = false
      }
    }

    // Mensajes y confirmaciones de los hijos
    const handleMessage = (msg) => {
      if (msg.type === 'error') error.value = msg.text
      else if (msg.type === 'success') {
        error.value = null
      }
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

    onMounted(() => { document.addEventListener('click', handleClickOutside) })
    onUnmounted(() => { document.removeEventListener('click', handleClickOutside) })

    return {
      activeTab, isDropdownOpen, dropdownContainer, error,
      confirmModal, confirmLoading, tabs,
      getSelectedTabInfo, toggleDropdown, selectTab,
      handleMessage, handleConfirmAction,
      cancelarConfirmacion, confirmarConfirmacion
    }
  }
}
</script>

<style scoped>
/* Container principal - idéntico a CRUDcursos */
.crud-cursos-container {
  padding: 24px;
  background-color: #f9fafb;
  font-family: 'Inter', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: calc(100vh - var(--navbar-height, 64px));
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.filtros-left {
  display: flex;
  gap: 12px;
  flex: 1;
  flex-wrap: wrap;
  align-items: center;
}

/* Error Alert */
.error-alert {
  background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24;
  padding: 15px 20px; margin-bottom: 16px; border-radius: 8px;
  display: flex; justify-content: space-between; align-items: center;
}
.error-alert p { margin: 0; }
.error-alert button { background: none; border: none; color: #721c24; font-size: 1.5rem; cursor: pointer; padding: 0; }

/* Dropdown Selector */
.selector-dropdown {
  position: relative;
  max-width: 400px;
  width: 100%;
}

.mantenedor-dropdown-toggle {
  width: 100%;
  padding: 10px 40px 10px 16px;
  border: 1.5px solid #4b5563;
  border-radius: 6px;
  background: white;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 500;
  height: 40px;
}

.mantenedor-dropdown-toggle:hover {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}

.mantenedor-dropdown-toggle.active {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}

.selected-option {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-weight: 500;
}

.dropdown-icon {
  color: #6b7280;
  transition: transform 0.3s ease;
  font-size: 0.75rem;
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
  border: 1.5px solid #4b5563;
  border-top: none;
  border-radius: 0 0 6px 6px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1001;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.dropdown-item {
  padding: 10px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.15s ease;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
}

.dropdown-item:last-child { border-bottom: none; }
.dropdown-item:hover { background: #f1f5f9; }
.dropdown-item.active { background: #eff6ff; color: #2563eb; font-weight: 600; }

.dropdown-item-icon { font-size: 1rem; width: 24px; text-align: center; }
.dropdown-item-text { color: #374151; font-weight: 500; flex: 1; }
.dropdown-item.active .dropdown-item-text { color: #2563eb; font-weight: 600; }
.dropdown-item:hover .dropdown-item-text { color: #111827; }

/* Main Content */
.main-content {
  flex: 1;
  padding: 0;
  overflow: hidden;
  width: 100%;
  margin: 0;
}

/* Modal de Confirmación */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  transition: color 0.2s ease;
}

.modal-close:hover { color: #111827; }

/* Responsive */
@media (max-width: 768px) {
  .filtros { flex-direction: column; }
  .selector-dropdown { max-width: 100%; }
  .dropdown-menu { max-height: 300px; }
}

@media (max-width: 480px) {
  .crud-cursos-container { padding: 16px; }
}
</style>