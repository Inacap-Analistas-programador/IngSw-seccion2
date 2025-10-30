<template>
  <div class="manual-acreditation">
    <!-- Título -->
    <div class="acreditation-header">
  <h1>Acreditación Manual</h1>
    </div>

    <!-- Barra de búsqueda -->
    <div class="search-section">
      <div class="search-box">
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
            <AppIcons name="search" :size="16" style="margin-right: 8px;" />
            Buscar
          </template>
        </BaseButton>
      </div>
    </div>

    <!-- Alertas -->
    <NotificationToast v-if="acreditationSuccess" :message="acreditationSuccessMessage" @close="acreditationSuccess = false" />
    <NotificationToast v-if="paymentSuccess" :message="paymentSuccessMessage" @close="paymentSuccess = false" />

    <!-- Información del participante -->
    <div v-if="selectedParticipant" class="participant-info">
      <div class="status-header">
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
          <AppIcons name="check" :size="18" /> Acreditar Participante
        </BaseButton>

        <!-- Botón de pagar si no ha pagado -->
        <BaseButton
          v-else-if="!selectedParticipant.paymentConfirmed"
          @click="handlePagar"
          variant="secondary"
          size="lg"
          class="btn-pagar"
        >
          <AppIcons name="credit-card" :size="18" /> Marcar como Pagado
        </BaseButton>

        <!-- Mensaje si ya está acreditado -->
        <div v-else-if="selectedParticipant.acreditationStatus === 'Acreditado'" class="already-acredited">
          <AppIcons name="check" :size="18" /> <span>Usuario ya acreditado</span>
        </div>

        <!-- QR solo en móvil -->
        <BaseButton
          v-if="isMobile && selectedParticipant.acreditationStatus === 'Acreditado'"
          @click="showQR"
          variant="secondary"
          size="md"
          class="btn-qr"
        >
          <AppIcons name="qrcode" :size="16" /> Ver QR
        </BaseButton>
      </div>
    </div>

  </div>
</template>

<script>
import DataCard from '@/components/Reutilizables/DataCard.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
// No usamos servicios remotos: datos locales para visualización sin API

export default {
  name: 'ManualAcreditation',
  components: {
    DataCard,
    DataTable,
    BaseButton,
    BaseAlert,
    NotificationToast,
    AppIcons
  },
  data() {
    return {
      searchTerm: '',
      selectedParticipant: null,
      // Datos de ejemplo locales para mostrar la pantalla sin consumir la API
      participants: [
        { per_id: 1, name: 'Juan Pérez González', rut: '12.345.678-9', currentCourse: 'Formación Inicial', paymentStatus: 'Confirmado', paymentConfirmed: true, accreditationStatus: 'Pendiente' },
        { per_id: 2, name: 'María García Silva', rut: '11.222.333-4', currentCourse: 'Primeros Auxilios', paymentStatus: 'Pendiente', paymentConfirmed: false, accreditationStatus: 'Pendiente' },
        { per_id: 3, name: 'Carlos Rodríguez', rut: '10.111.222-3', currentCourse: 'Liderazgo', paymentStatus: 'Confirmado', paymentConfirmed: true, accreditationStatus: 'Acreditado' }
      ],
      acreditationSuccess: false,
      isMobile: window.innerWidth <= 768,
      paymentSuccess: false,
      paymentSuccessMessage: ''
      ,acreditationSuccessMessage: ''
    }
  },
  computed: {
    canAcredit() {
      return this.selectedParticipant && 
             this.selectedParticipant.paymentStatus === 'Confirmado' &&
             this.selectedParticipant.acreditationStatus === 'Pendiente';
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
      const term = this.searchTerm.trim().toLowerCase()
      if (!term) { this.selectedParticipant = null; return }

      // Buscar en datos locales (por RUT exacto o por nombre parcial)
      const found = this.participants.find(p => {
        return (p.rut && p.rut.toLowerCase() === term) || (p.name && p.name.toLowerCase().includes(term))
      })

      if (!found) {
        this.selectedParticipant = null
        this.acreditationSuccess = false
        this.paymentSuccess = false
      } else {
        // Clonar para edición local
        this.selectedParticipant = Object.assign({}, found)
      }
    },

    acreditarParticipante() {
      if (!this.canAcredit || !this.selectedParticipant) return

      // Simular acreditación local (no API)
      this.selectedParticipant.acreditationStatus = 'Acreditado'
      this.selectedParticipant.paymentConfirmed = true
      this.selectedParticipant.paymentStatus = 'Confirmado'
      const msg = `${this.selectedParticipant.name} acreditado correctamente`
      this.acreditationSuccessMessage = msg
      this.acreditationSuccess = true
      setTimeout(() => {
        this.acreditationSuccess = false
        this.acreditationSuccessMessage = ''
      }, 3500)
    },

    handlePagar() {
      // Marcar como pagado
      this.selectedParticipant.paymentStatus = 'Confirmado';
      this.selectedParticipant.paymentConfirmed = true;

      // Mostrar notificación interna en lugar del alert nativo (evita que aparezca el origen localhost)
      const notification = `✅ ${this.selectedParticipant.name} marcado como pagado. Ahora puede ser acreditado.`;
      console.log(notification);
      // Mostrar BaseAlert controlado por estado
      this.paymentSuccessMessage = notification;
      this.paymentSuccess = true;

      // Auto-dismiss del toast después de 3.5 segundos
      setTimeout(() => {
        this.paymentSuccess = false;
        this.paymentSuccessMessage = '';
      }, 3500);
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
  color: var(--color-primary);
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
  background: var(--color-background-soft);
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

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
