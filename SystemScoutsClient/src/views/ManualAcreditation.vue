<template>
  <div class="manual-acreditation">
    <!-- Título con PageHeader -->
    <PageHeader 
      title="Acreditación Manual" 
      subtitle="Busca participantes por nombre o RUT para gestionar su acreditación y pagos."
    />

    <!-- Filtros y Búsqueda -->
    <div class="search-section">
      
      <div class="filters-container">
        <!-- Filtro Curso -->
        <FilterSelect
          v-model="filters.curso"
          :options="cursosOpts"
          defaultLabel="Cursos"
          class="filter-item"
        />

        <!-- Barra de Búsqueda Componente -->
        <SearchBar 
          v-model="searchTerm" 
          placeholder="Buscar por RUT o nombre completo..." 
          @search="handleSearch"
          class="search-bar-item"
        />

        <!-- Botones de Acción (En línea) -->
        <div class="header-actions">
           <BaseButton
            :disabled="!canAcredit"
            @click="acreditarParticipante"
            variant="primary"
            class="header-icon-btn"
            title="Acreditar"
          >
            <AppIcons name="check" :size="20" />
          </BaseButton>

          <BaseButton
            :disabled="!canPay"
            @click="handlePagar"
            variant="secondary"
            class="header-icon-btn"
            title="Pagar"
          >
            <AppIcons name="credit-card" :size="20" />
          </BaseButton>
        </div>

      </div>
    </div>

    <!-- Indicador de carga centrado -->
    <div v-if="cargando" class="loading-overlay" role="status" aria-live="polite">
      <div class="loading-content">
        <div class="spinner" aria-hidden="true"></div>
        <div>Buscando...</div>
      </div>
    </div>

    <!-- Alertas (Unificadas) -->
    <NotificationToast 
      v-if="showToast" 
      :message="toastMessage" 
      :type="toastType" 
      :icon="toastIcon" 
      @close="showToast = false" 
    />

    <!-- Información del participante -->
    <div class="participant-info">
      <div class="mantenedor-header">
        <h2>Información del Participante</h2>
      </div>
      
      <div class="info-grid">
          <div class="info-section">
          <h3>Datos Personales</h3>
          <div class="info-item">
            <strong>Nombre:</strong> {{ selectedParticipant?.name || '---' }}
          </div>
          <div class="info-item">
            <strong>Apodo:</strong> {{ selectedParticipant?.nickname || '---' }}
          </div>
          <div class="info-item">
            <strong>RUT:</strong> {{ selectedParticipant?.rut || '---' }}
          </div>
          <div class="info-item">
            <strong>Curso:</strong> {{ selectedParticipant?.currentCourse || '---' }}
          </div>
        </div>

        <div class="info-section">
          <h3>Información Scout</h3>
          <div class="info-item">
            <strong>Rama:</strong> {{ selectedParticipant?.branchName || '---' }}
          </div>
          <div class="info-item">
            <strong>Vehículo:</strong> {{ selectedParticipant?.vehicle ? 'Sí' : 'No' }}
          </div>
          <div class="info-item">
            <strong>Alimentación:</strong> {{ selectedParticipant?.dietType || '---' }}
          </div>
        </div>

        <div class="info-section">
          <h3>Estado</h3>
          <div class="info-item">
            <strong>Estado:</strong> 
            <span :class="getStatusClass">
              {{ selectedParticipant ? (selectedParticipant.paymentConfirmed ? 'Registrado' : 'Pago Pendiente') : '---' }}
            </span>
          </div>
          
          <!-- Mensaje de estado -->
          <div v-if="statusMessage" class="status-message" :class="statusMessageClass">
            {{ statusMessage }}
          </div>
        </div>
      </div>

      <!-- Acciones -->
      <!-- Acciones (Removidas) -->
       <div class="action-buttons" style="display: none;"></div>
    </div>

  </div>
</template>

<script>
import BaseButton from '@/components/BaseButton.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

import PageHeader from '@/components/common/PageHeader.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import authViewsService from '@/services/auth_viewsService'
import { cursos as cursosService } from '@/services/cursosService'

export default {
  name: 'ManualAcreditation',
  components: {
    BaseButton,
    NotificationToast,
    AppIcons,
    PageHeader,
    FilterSelect,
    SearchBar
  },
  data() {
    return {
      searchTerm: '',
      selectedParticipant: null,
      // Datos de ejemplo locales
      participants: [ /* ... mantenemos datos si se usan para demos ... */ ],
      
      // Flags UI
      searchNotFound: false,
      searchErrorMessage: '',
      cargando: false,
      isMobile: window.innerWidth <= 768,

      // Sistema de Notificaciones Unificado
      showToast: false,
      toastMessage: '',
      toastType: 'info', // info, success, error
      toastIcon: '',

      // Filtros
      filters: { curso: null },
      cursosOpts: []
    }
  },
  computed: {
    canAcredit() {
      return this.selectedParticipant && 
             this.selectedParticipant.paymentStatus === 'Confirmado' &&
             this.selectedParticipant.acreditationStatus === 'Pendiente';
    },

    canPay() {
      // Habilitado si hay participante seleccionado y NO ha confirmado pago
      // Ojo: si ya pagó, se deshabilita.
      return this.selectedParticipant && !this.selectedParticipant.paymentConfirmed;
    },
    
    statusMessage() {
      if (!this.selectedParticipant) return '';
      
      if (this.selectedParticipant.acreditationStatus === 'Acreditado') {
        return '✅ Este usuario ya fue acreditado';
      }
      if (this.selectedParticipant.paymentStatus !== 'Confirmado') {
        return '❌ Pendiente de pago - No se puede acreditar';
      }
      return '✅ Listo para acreditar';
    },

    statusMessageClass() {
      if (!this.selectedParticipant) return '';
      
      if (this.selectedParticipant.acreditationStatus === 'Acreditado') {
        return 'status-message-success';
      }
      if (this.selectedParticipant.paymentStatus !== 'Confirmado') {
        return 'status-message-error';
      }
      return 'status-message-info';
    },

    getStatusClass() {
      if (!this.selectedParticipant) return ''
      return this.selectedParticipant?.paymentConfirmed 
        ? 'status-confirmado' 
        : 'status-pendiente';
    }
  },
  mounted() {
    window.addEventListener('resize', this.checkMobile);
    this.loadOptions();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    async loadOptions() {
      try {
        // Usar endpoint especializado que filtra por estado y fecha en el backend
        const res = await cursosService.get_acreditacion()
        
        // La respuesta ya es un array de objetos limpios o se debe normalizar si viene paginado?
        // El endpoint devuelve Response(data) que es list, no paginado por defecto en @action salvo que se aplique.
        // StandardResultsSetPagination se aplica a ModelViewSet. @action por defecto usa la paginación del ViewSet si retorna queryset, pero aquí retorno Response(list).
        // Cuando retorno Response(data), DRF no pagina automáticamente la data raw.
        
        let data = res
        if (res && res.results) data = res.results // Fallback por si acaso
        if (!Array.isArray(data)) data = []

        this.cursosOpts = data.map(c => ({ 
          id: c.cur_id, 
          descripcion: c.cur_descripcion 
        }))

      } catch (e) {
        console.warn('Error cargando opciones de acreditación:', e)
        this.notify('Error al cargar cursos disponibles', 'error', 'alert-circle')
      }
    },

    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },

    notify(msg, type = 'info', icon = '') {
      this.toastMessage = msg
      this.toastType = type
      this.toastIcon = icon
      this.showToast = true
      setTimeout(() => { this.showToast = false }, 4000)
    },

    async handleSearch() {
      // 1. Validar selección de curso
      const cursoId = this.filters.curso
      if (!cursoId) {
        this.notify('Debe seleccionar un curso antes de buscar.', 'error', 'alert-circle')
        this.searchErrorMessage = 'Seleccione un curso.'
        this.searchNotFound = true
        return
      }

      const term = this.searchTerm.trim()
      // Búsqueda manual: no ejecutamos automáticamente, solo al presionar el botón o Enter
      if (!term) { this.selectedParticipant = null; this.searchNotFound = false; this.searchErrorMessage = ''; return }

      // Resetear flags
      this.searchNotFound = false
      this.searchErrorMessage = ''

      // Primero intentar por API remota optimizada
      this.cargando = true
      try {
        // Enviar término y el ID del curso seleccionado
        const res = await authViewsService.acreditacion_manual_search(term, cursoId)

        // Normalizar respuesta: endpoint devuelve una lista filtrada
        let person = null
        if (Array.isArray(res) && res.length) {
          person = res[0] // Tomar el primero si hay coincidencias (el backend limita a 20)
        } else if (res && res.per_id) {
           person = res
        }

        if (person) {
          // El endpoint ya devuelve la estructura que necesitamos, mapeo directo
          // pero aseguramos compatibilidad con el resto del componente
          this.selectedParticipant = {
            per_id: person.per_id,
            name: person.name,
            nickname: person.nickname,
            rut: person.rut,
            dv: person.rut.split('-')[1] || '',
            currentCourse: person.currentCourse,
            branchName: person.branchName,
            vehicle: person.vehicle,
            dietType: person.dietType,
            paymentConfirmed: person.paymentConfirmed,
            paymentStatus: person.paymentStatus,
            acreditationStatus: person.acreditationStatus,
            // Extra info que pueda servir
            per_curso_id: person.per_curso_id
          }
          this.searchNotFound = false
          this.searchErrorMessage = ''
          return
        } else {
          // No encontrado
          this.selectedParticipant = null
          this.searchNotFound = true
          this.notify('No se encontró la persona solicitada.', 'error', 'alert-circle')
          return
        }
      } catch (err) {
        // Si falla la llamada, informar al usuario
        console.warn('API de acreditación no disponible:', err)
        const errorMessage = err.response?.data?.error || 'Error al consultar el servidor. Intente nuevamente.'
        this.notify(errorMessage, 'error', 'alert-circle')
        this.searchErrorMessage = errorMessage
        this.searchNotFound = true
        this.selectedParticipant = null
        return
      } finally {
        this.cargando = false
      }
    },

    async acreditarParticipante() {
      if (!this.selectedParticipant) return

      // Si el pago está pendiente, redirigir a la página de pagos
      if (!this.selectedParticipant.paymentConfirmed) {
        this.$router.push({ name: 'pagos', query: { rut: this.selectedParticipant.rut } })
        return
      }

      // Llamar al endpoint de acreditación del backend
      try {
        const payload = { per_id: this.selectedParticipant.per_id, rut: this.selectedParticipant.rut }
        const res = await authViewsService.acreditacion_manual_acreditar(payload)

        // Si la API devolvió la entidad actualizada, usarla; si no, aplicar cambios locales
        if (res && (res.PER_ID || res.per_id || res.id || res.acreditado)) {
          // Normalizar respuesta similar a handleSearch
          this.selectedParticipant.acreditationStatus = (res.acreditado === true || res.accreditationStatus === 'Acreditado') ? 'Acreditado' : 'Acreditado'
          this.selectedParticipant.paymentConfirmed = true
          this.selectedParticipant.paymentStatus = 'Confirmado'
        } else {
          this.selectedParticipant.acreditationStatus = 'Acreditado'
          this.selectedParticipant.paymentConfirmed = true
          this.selectedParticipant.paymentStatus = 'Confirmado'
        }

        const msg = `${this.selectedParticipant.name} acreditado correctamente`
        this.notify(msg, 'success', 'check')

      } catch (err) {
        console.error('Error acreditando participante:', err)
        this.notify('Error al acreditar. Intente nuevamente.', 'error', 'alert-circle')
      }
    },

    handlePagar() {
      // Redirigir a la página de pagos con el RUT como parámetro
      if (this.selectedParticipant && this.selectedParticipant.rut) {
        this.$router.push({
          name: 'pagos',
          query: { rut: this.selectedParticipant.rut }
        });
      }
    },

    showQR() {
      // Aquí iría la lógica para mostrar el QR
      alert(`📱 Mostrando QR de ${this.selectedParticipant.name}`);
    }
  }
}
</script>

<style scoped>
.search-error {
  color: #b71c1c;
  margin-left: 12px;
  align-self: center;
  font-weight: 600;
}

.manual-acreditation {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 24px;
  font-family: 'Inter', Arial, sans-serif;
  height: 100%;
  overflow-y: auto; /* Enable scrolling */
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .manual-acreditation {
    padding: 16px; /* Reduce padding on mobile */
  }
}

/* removed acreditation-header */


.search-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  align-items: flex-end;
}

.filter-item {
  min-width: 200px;
  max-width: 300px;
}

.search-bar-item {
  flex: 1;
  min-width: 300px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 2px; /* Slight alignment adjustment if needed */
}

.search-actions-row {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
  min-height: 20px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  border-radius: 8px;
  font-size: 16px;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}

.participant-info {
  padding: 32px 0px;
  border-radius: 12px;
  margin-bottom: 30px;
}

/* .status-header replaced by mantenedor-header */
.mantenedor-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 20px; 
  padding-bottom: 16px; 
  border-bottom: 2px solid #3949ab; 
}

.mantenedor-header h2 { 
  color: #1a237e; 
  font-size: 1.5rem; 
  display: flex; 
  align-items: center; 
  gap: 10px; 
  margin: 0; 
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 24px;
}

.info-section h3 {
  color: var(--color-primary);
  margin-bottom: 16px;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 8px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
}

.info-item strong {
  min-width: 100px;
  display: inline-block;
}

.status-message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 6px;
  font-weight: 600;
  text-align: center;
}

.status-message-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-message-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f1b0b7;
}

.status-message-info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.action-buttons {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.header-icon-btn { 
  height: 40px !important; 
  width: 40px !important; 
  padding: 0 !important; 
  display: flex !important; 
  align-items: center !important; 
  justify-content: center !important; 
  border-radius: 6px; 
}

.already-acredited {
  padding: 15px;
  background: #d4edda;
  color: #155724;
  border-radius: 8px;
  font-weight: bold;
  font-size: 16px;
}

.status-confirmado {
  color: #155724;
  font-weight: 600;
}

.status-pendiente {
  color: #856404;
  font-weight: 600;
}

.status-acreditado {
  color: #155724;
  font-weight: 600;
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.35);
  z-index: 1200;
}
.loading-content {
  background: var(--color-surface);
  color: var(--color-text);
  padding: 18px 24px;
  border-radius: 10px;
  display: flex;
  gap: 12px;
  align-items: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.spinner {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid rgba(0,0,0,0.1);
  border-top-color: var(--color-primary);
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .manual-acreditation {
    padding: 16px; 
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .filters-container {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .filter-item, .search-bar-item {
    min-width: 100%;
    max-width: 100%;
  }

  .header-actions {
    justify-content: center; /* Centered buttons on mobile */
    width: 100%;
    margin-top: 8px;
  }
}

.header-icon-btn, .search-button {
  height: 40px !important;
  width: 40px !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 6px;
}
</style>
