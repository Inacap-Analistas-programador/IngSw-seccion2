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
        <BaseButton
          v-if="selectedParticipant"
          @click="acreditarParticipante"
          variant="primary"
          size="md"
        >
          <AppIcons name="check" :size="16" style="margin-right: 8px;" /> Acreditar
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
            <strong>Apodo:</strong> {{ selectedParticipant.nickname || 'No especificado' }}
          </div>
          <div class="info-item">
            <strong>RUT:</strong> {{ selectedParticipant.rut }}
          </div>
          <div class="info-item">
            <strong>Curso:</strong> {{ selectedParticipant.currentCourse }}
          </div>
        </div>

        <div class="info-section">
          <h3>Información Scout</h3>
          <div class="info-item">
            <strong>Rama:</strong> {{ selectedParticipant.branchName || 'No especificada' }}
          </div>
          <div class="info-item">
            <strong>Vehículo:</strong> {{ selectedParticipant.vehicle ? 'Sí' : 'No' }}
          </div>
          <div class="info-item">
            <strong>Alimentación:</strong> {{ selectedParticipant.dietType || 'No especificado' }}
          </div>
        </div>

        <div class="info-section">
          <h3>Estado</h3>
          <div class="info-item">
            <strong>Estado:</strong> 
            <span :class="getStatusClass">
              {{ selectedParticipant.paymentConfirmed ? 'Registrado' : 'Pago Pendiente' }}
            </span>
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
          <AppIcons name="credit-card" :size="18" /> Pagar
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
import DataCard from '@/components/DataCard.vue'
import DataTable from '@/components/DataTable.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import authViewsService from '@/services/auth_viewsService'
// Usamos `auth_viewsService` para conectar con los endpoints de acreditación

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
        { 
          per_id: 1, 
          name: 'Juan Pérez González', 
          nickname: 'Juanito',
          rut: '12.345.678-9', 
          currentCourse: 'Formación Inicial', 
          branchName: 'Lobatos',
          vehicle: true,
          dietType: 'Vegetariano',
          paymentStatus: 'Confirmado', 
          paymentConfirmed: true, 
          accreditationStatus: 'Pendiente' 
        },
        { 
          per_id: 2, 
          name: 'María García Silva', 
          nickname: 'Mary',
          rut: '11.222.333-4', 
          currentCourse: 'Primeros Auxilios', 
          branchName: 'Pioneros',
          vehicle: false,
          dietType: 'Sin restricciones',
          paymentStatus: 'Pendiente', 
          paymentConfirmed: false, 
          accreditationStatus: 'Pendiente' 
        },
        { 
          per_id: 3, 
          name: 'Carlos Rodríguez', 
          nickname: 'Carlitos',
          rut: '10.111.222-3', 
          currentCourse: 'Liderazgo', 
          branchName: 'Rovers',
          vehicle: true,
          dietType: 'Sin gluten',
          paymentStatus: 'Confirmado', 
          paymentConfirmed: true, 
          accreditationStatus: 'Acreditado' 
        }
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

    getStatusClass() {
      return this.selectedParticipant?.paymentConfirmed 
        ? 'status-confirmado' 
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

  async handleSearch() {
      const term = this.searchTerm.trim()
      if (!term) { this.selectedParticipant = null; return }

      // Primero intentar por API remota (si el backend responde)
      try {
        const payload = { rut: term, query: term }
        const res = await authViewsService.acreditacion_manual_search(payload)

        // Normalizar varias formas de respuesta posibles
        let person = null
        if (!res) {
          person = null
        } else if (Array.isArray(res) && res.length) {
          person = res[0]
        } else if (res.persona) {
          person = res.persona
        } else if (res.data && Array.isArray(res.data) && res.data.length) {
          person = res.data[0]
        } else if (typeof res === 'object') {
          person = res
        }

        if (person) {
          // Mapear campos de la API al formato local del componente
          const p = {
            per_id: person.PER_ID || person.per_id || person.id || null,
            name: person.PER_NOMBRES || person.nombre || person.name || person.full_name || person.NOMBRE || '',
            nickname: person.PER_APODO || person.apodo || person.nickname || '',
            rut: person.PER_RUN || person.rut || person.run || '',
            currentCourse: person.curso || person.currentCourse || '',
            branchName: person.rama || person.branchName || '',
            vehicle: person.PER_VEHICULO === 1 || person.vehicle || false,
            dietType: person.PER_ALIMENTACION || person.dietType || person.alimentacion || '',
            paymentConfirmed: person.paymentConfirmed || person.PAGO_CONFIRMADO || person.payment_confirmed || false,
            paymentStatus: person.payment_status || (person.paymentConfirmed ? 'Confirmado' : 'Pendiente'),
            accreditationStatus: person.acreditado || person.accredited || person.accreditationStatus || 'Pendiente'
          }
          this.selectedParticipant = Object.assign({}, p)
          return
        }
      } catch (err) {
        // Si falla la llamada, caemos al fallback local
        console.warn('API de acreditación no disponible, usando datos locales:', err)
      }

      // Fallback: buscar en datos locales (por RUT exacto o por nombre parcial)
      const found = this.participants.find(p => {
        const rut = p.rut && p.rut.toLowerCase && p.rut.toLowerCase()
        const name = p.name && p.name.toLowerCase && p.name.toLowerCase()
        return (rut && rut === term.toLowerCase()) || (name && name.includes(term.toLowerCase()))
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
        if (res && (res.PER_ID || res.per_id || res.id)) {
          // Normalizar respuesta similar a handleSearch
          this.selectedParticipant.acreditationStatus = res.acreditado || res.accreditationStatus || 'Acreditado'
          this.selectedParticipant.paymentConfirmed = res.paymentConfirmed || true
          this.selectedParticipant.paymentStatus = res.payment_status || 'Confirmado'
        } else {
          this.selectedParticipant.acreditationStatus = 'Acreditado'
          this.selectedParticipant.paymentConfirmed = true
          this.selectedParticipant.paymentStatus = 'Confirmado'
        }

        const msg = `${this.selectedParticipant.name} acreditado correctamente`
        this.acreditationSuccessMessage = msg
        this.acreditationSuccess = true
        setTimeout(() => {
          this.acreditationSuccess = false
          this.acreditationSuccessMessage = ''
        }, 3500)
      } catch (err) {
        console.error('Error acreditando participante:', err)
        // Mostrar notificación de error reutilizando paymentSuccessMessage (simple)
        this.paymentSuccessMessage = 'Error al acreditar. Intente nuevamente.'
        this.paymentSuccess = true
        setTimeout(() => { this.paymentSuccess = false; this.paymentSuccessMessage = '' }, 3500)
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
  max-width: 800px;
  margin: 0 auto;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
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
