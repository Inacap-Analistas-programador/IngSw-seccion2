<template>
  <div class="manual-acreditation">
    <!-- Título -->
    <div class="acreditation-header">
      <h1>Acreditación Manual</h1>
      <p>Sistema de acreditación para eventos scouts</p>
    </div>

    <!-- Barra de búsqueda -->
    <div class="search-section">
      <div class="search-box">z
        <input 
          v-model="searchTerm"
          type="text" 
          placeholder="Buscar por RUT o nombre completo..."
          class="search-input"
          @input="handleSearch"
          aria-label="Buscar por RUT o nombre completo"
        />
        <BaseButton 
          @click="handleSearch"
          variant="primary"
          size="md"
        >
          <template #default>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="margin-right: 8px;" aria-hidden="true">
              <path d="M14 14L11.1 11.1M12.6667 7.33333C12.6667 10.2789 10.2789 12.6667 7.33333 12.6667C4.38781 12.6667 2 10.2789 2 7.33333C2 4.38781 4.38781 2 7.33333 2C10.2789 2 12.6667 4.38781 12.6667 7.33333Z" 
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Buscar
          </template>
        </BaseButton>
      </div>
    </div>

    <!-- Alertas -->
    <BaseAlert
      v-if="acreditationSuccess"
      type="exito"
      title="Acreditación Exitosa"
      :message="`${selectedParticipant?.name} ha sido acreditado correctamente`"
      @close="acreditationSuccess = false"
    />

    <!-- Información del participante -->
    <div v-if="selectedParticipant" class="participant-info">
      <div class="status-header">
        <!-- Luz indicadora -->
        <div class="status-light" :class="statusLightClass"></div>
        <h2>Información del Participante</h2>
      </div>
      
      <div class="info-grid">
        <div class="info-section">
          <h3>Datos Personales</h3>
          <div class="info-item">
            <strong>Nombre:</strong> {{ selectedParticipant.name }}
          </div>
          <div class="info-item">
            <strong>RUT:</strong> {{ selectedParticipant.rut }}
          </div>
          <div class="info-item">
            <strong>Curso:</strong> {{ selectedParticipant.currentCourse }}
          </div>
        </div>

        <div class="info-section">
          <h3>Estado</h3>
          <div class="info-item">
            <strong>Pago:</strong> 
            <span :class="paymentStatusClass">{{ selectedParticipant.paymentStatus }}</span>
          </div>
          <div class="info-item">
            <strong>Acreditación:</strong> 
            <span :class="acreditationStatusClass">{{ selectedParticipant.acreditationStatus }}</span>
          </div>
          
          <!-- Mensaje de estado -->
          <div v-if="statusMessage" class="status-message" :class="statusMessageClass">
            {{ statusMessage }}
          </div>
        </div>
      </div>

      <!-- Acciones -->
      <div class="action-buttons">
        <!-- Botón principal de acreditar -->
        <BaseButton
          v-if="canAcredit"
          @click="acreditarParticipante"
          variant="primary"
          size="lg"
          class="btn-acreditar"
        >
          ✅ Acreditar Participante
        </BaseButton>

        <!-- Botón de pagar si no ha pagado -->
        <BaseButton
          v-else-if="!selectedParticipant.paymentConfirmed"
          @click="handlePagar"
          variant="secondary"
          size="lg"
          class="btn-pagar"
        >
          💳 Marcar como Pagado
        </BaseButton>

        <!-- Mensaje si ya está acreditado -->
        <div v-else-if="selectedParticipant.acreditationStatus === 'Acreditado'" class="already-acredited">
          <span>✅ Usuario ya acreditado</span>
        </div>

        <!-- QR solo en móvil -->
        <BaseButton
          v-if="isMobile && selectedParticipant.acreditationStatus === 'Acreditado'"
          @click="showQR"
          variant="secondary"
          size="md"
          class="btn-qr"
        >
          📱 Ver QR
        </BaseButton>
      </div>
    </div>

    <!-- Acreditaciones recientes -->
    <div class="recent-acreditations">
      <h2>Acreditaciones Recientes</h2>
      <DataTable
        :columns="tableColumns"
        :rows="recentAcreditations"
        :paginated="true"
        :page-size="5"
        search-placeholder="Buscar en acreditaciones..."
        empty-message="No hay acreditaciones recientes"
      />
    </div>
  </div>
</template>

<script>
import DataCard from './DataCard.vue'
import DataTable from './DataTable.vue'
import BaseButton from './BaseButton.vue'
import BaseAlert from './BaseAlert.vue'

export default {
  name: 'ManualAcreditation',
  components: {
    DataCard,
    DataTable,
    BaseButton,
    BaseAlert
  },
  data() {
    return {
      searchTerm: '',
      selectedParticipant: null,
      acreditationSuccess: false,
      isMobile: window.innerWidth <= 768,
      recentAcreditations: [
        {
          id: 1,
          time: '14:35',
          name: 'MARÍA GONZÁLEZ LÓPEZ',
          rut: '98.765.432-1',
          course: 'Formación de Dirigentes',
          status: 'Acreditado'
        },
        {
          id: 2,
          time: '14:28',
          name: 'CARLOS RAMÍREZ SOTO',
          rut: '11.222.333-4',
          course: 'Curso de Especialidades',
          status: 'Acreditado'
        }
      ],
      tableColumns: [
        { key: 'time', label: 'Hora', sortable: true },
        { key: 'name', label: 'Nombre', sortable: true },
        { key: 'rut', label: 'RUT', sortable: true },
        { key: 'course', label: 'Curso', sortable: true },
        { key: 'status', label: 'Estado', sortable: true }
      ]
    }
  },
  computed: {
    canAcredit() {
      return this.selectedParticipant && 
             this.selectedParticipant.paymentStatus === 'Confirmado' &&
             this.selectedParticipant.acreditationStatus === 'Pendiente';
    },
    
    statusLightClass() {
      if (!this.selectedParticipant) return 'status-light-gray';
      if (this.selectedParticipant.acreditationStatus === 'Acreditado') return 'status-light-green';
      if (this.selectedParticipant.paymentStatus === 'Confirmado') return 'status-light-yellow';
      return 'status-light-red';
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

    paymentStatusClass() {
      return this.selectedParticipant?.paymentStatus === 'Confirmado' 
        ? 'status-confirmado' 
        : 'status-pendiente';
    },
    
    acreditationStatusClass() {
      return this.selectedParticipant?.acreditationStatus === 'Acreditado' 
        ? 'status-acreditado' 
        : 'status-pendiente';
    }
  },
  mounted() {
    // Detectar si es móvil para el QR
    window.addEventListener('resize', this.checkMobile);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },

    handleSearch() {
      if (this.searchTerm.trim()) {
        // Simular búsqueda con diferentes estados
        const randomState = Math.random();
        if (randomState < 0.3) {
          // Usuario sin pago
          this.selectedParticipant = {
            name: 'JUAN PÉREZ GONZÁLEZ',
            rut: '12.345.678-9',
            currentCourse: 'Formación de Dirigentes',
            paymentStatus: 'Pendiente',
            acreditationStatus: 'Pendiente',
            paymentConfirmed: false
          };
        } else if (randomState < 0.6) {
          // Usuario listo para acreditar
          this.selectedParticipant = {
            name: 'MARÍA GONZÁLEZ LÓPEZ',
            rut: '98.765.432-1',
            currentCourse: 'Formación de Dirigentes',
            paymentStatus: 'Confirmado',
            acreditationStatus: 'Pendiente',
            paymentConfirmed: true
          };
        } else {
          // Usuario ya acreditado
          this.selectedParticipant = {
            name: 'CARLOS RAMÍREZ SOTO',
            rut: '11.222.333-4',
            currentCourse: 'Curso de Especialidades',
            paymentStatus: 'Confirmado',
            acreditationStatus: 'Acreditado',
            paymentConfirmed: true
          };
        }
      } else {
        this.selectedParticipant = null;
      }
    },

    acreditarParticipante() {
      if (this.canAcredit) {
        this.selectedParticipant.acreditationStatus = 'Acreditado';
        
        // Agregar a recientes
        this.recentAcreditations.unshift({
          id: Date.now(),
          time: new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' }),
          name: this.selectedParticipant.name,
          rut: this.selectedParticipant.rut,
          course: this.selectedParticipant.currentCourse,
          status: 'Acreditado'
        });

        this.acreditationSuccess = true;
      }
    },

    handlePagar() {
      // Marcar como pagado
      this.selectedParticipant.paymentStatus = 'Confirmado';
      this.selectedParticipant.paymentConfirmed = true;
      
      // Podrías mostrar alerta de éxito aquí
      setTimeout(() => {
        alert(`✅ ${this.selectedParticipant.name} marcado como pagado. Ahora puede ser acreditado.`);
      }, 100);
    },

    showQR() {
      // Aquí iría la lógica para mostrar el QR
      alert(`📱 Mostrando QR de ${this.selectedParticipant.name}`);
    }
  }
}
</script>

<style scoped>
.manual-acreditation {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.acreditation-header {
  text-align: center;
  margin-bottom: 30px;
}

.acreditation-header h1 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.search-section {
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 10px;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  font-size: 16px;
}

.participant-info {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 30px;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.status-light {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.status-light-green {
  background: #27ae60;
  animation: pulse-green 2s infinite;
}

.status-light-yellow {
  background: #f39c12;
}

.status-light-red {
  background: #e74c3c;
}

.status-light-gray {
  background: #95a5a6;
}

@keyframes pulse-green {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 24px;
}

.info-section h3 {
  color: #2c3e50;
  margin-bottom: 16px;
  border-bottom: 2px solid #3498db;
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
  border-top: 1px solid #dee2e6;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.btn-acreditar {
  font-size: 18px;
  font-weight: bold;
  padding: 16px 32px;
}

.btn-pagar {
  font-size: 16px;
  font-weight: bold;
  padding: 14px 28px;
}

.btn-qr {
  font-size: 14px;
  padding: 10px 20px;
}

.already-acredited {
  padding: 15px;
  background: #d4edda;
  color: #155724;
  border-radius: 8px;
  font-weight: bold;
  font-size: 16px;
}

.recent-acreditations h2 {
  margin-bottom: 16px;
  color: #2c3e50;
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

/* Responsive */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .search-box {
    flex-direction: column;
  }
}
</style>