<<<<<<< HEAD
<template>
  <div class="manual-acreditation">
    <!-- Título -->
    <div class="acreditation-header">
      <h1>Acreditación Manual</h1>
      <p>Sistema de acreditación para eventos scouts</p>
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
      <h2>Información del Participante</h2>
      
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
            <strong>Curso Actual:</strong> {{ selectedParticipant.currentCourse }}
          </div>
          <div class="info-item">
            <strong>Grupo Scout:</strong> {{ selectedParticipant.scoutGroup }}
          </div>
          <div class="info-item">
            <strong>Rol:</strong> {{ selectedParticipant.role }}
          </div>
        </div>

        <div class="info-section">
          <h3>Estado de Inscripción</h3>
          <div class="info-item">
            <strong>Estado Pago:</strong> 
            <span :class="paymentStatusClass">{{ selectedParticipant.paymentStatus }}</span>
          </div>
          <div class="info-item">
            <strong>Estado Inscripción:</strong> 
            <span :class="inscriptionStatusClass">{{ selectedParticipant.inscriptionStatus }}</span>
          </div>
          <div class="info-item">
            <strong>Curso Anterior:</strong> {{ selectedParticipant.previousCourse }}
          </div>
          <div class="info-item">
            <strong>Acreditación:</strong> 
            <span :class="acreditationStatusClass">{{ selectedParticipant.acreditationStatus }}</span>
          </div>
        </div>
      </div>

      <!-- Botón de acreditar -->
      <div class="acreditation-actions">
        <BaseButton
          @click="acreditarParticipante"
          :disabled="!canAcredit"
          variant="primary"
          size="lg"
          class="btn-acreditar"
        >
          {{ acreditationButtonText }}
        </BaseButton>
      </div>
    </div>

    <!-- Métricas usando DataCard -->
    <div class="metrics-grid">
      <DataCard
        title="Total Acreditados"
        :value="metrics.totalAcreditados"
      />
      <DataCard
        title="Pendientes"
        :value="metrics.pendientes"
      />
      <DataCard
        title="% de Acreditación"
        :value="`${metrics.porcentajeAcreditacion}%`"
      />
      <DataCard
        title="Acreditados Hoy"
        :value="metrics.acreditadosHoy"
      />
    </div>

    <!-- Acreditaciones recientes usando DataTable -->
    <div class="recent-acreditations">
      <h2>Acreditaciones Recientes</h2>
      <DataTable
        :columns="tableColumns"
        :rows="recentAcreditations"
        :paginated="true"
        :page-size="5"
        search-placeholder="Buscar en acreditaciones..."
        empty-message="No hay acreditaciones recientes"
        @row-click="handleRowClick"
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
      metrics: {
        totalAcreditados: 87,
        pendientes: 23,
        porcentajeAcreditacion: 79,
        acreditadosHoy: 15
      },
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
        },
        {
          id: 3,
          time: '14:15',
          name: 'ANA TORRES MUÑOZ',
          rut: '22.333.444-5',
          course: 'Formación de Dirigentes',
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
             this.selectedParticipant.inscriptionStatus === 'Habilitado' &&
             this.selectedParticipant.acreditationStatus === 'Pendiente';
    },
    acreditationButtonText() {
      if (!this.selectedParticipant) return 'ACREDITAR PARTICIPANTE';
      return this.selectedParticipant.acreditationStatus === 'Acreditado' 
        ? 'YA ACREDITADO' 
        : 'ACREDITAR PARTICIPANTE';
    },
    paymentStatusClass() {
      return this.selectedParticipant?.paymentStatus === 'Confirmado' 
        ? 'status-confirmado' 
        : 'status-pendiente';
    },
    inscriptionStatusClass() {
      return this.selectedParticipant?.inscriptionStatus === 'Habilitado' 
        ? 'status-habilitado' 
        : 'status-pendiente';
    },
    acreditationStatusClass() {
      return this.selectedParticipant?.acreditationStatus === 'Acreditado' 
        ? 'status-acreditado' 
        : 'status-pendiente';
    }
  },
  methods: {
    handleSearch() {
      // Simular búsqueda - en producción harías una llamada API
      if (this.searchTerm.trim()) {
        this.selectedParticipant = {
          name: 'JUAN PÉREZ GONZÁLEZ',
          rut: '12.345.678-9',
          currentCourse: 'Formación de Dirigentes',
          scoutGroup: 'GRUPO ARAUCO',
          role: 'DIRIGENTE SCOUT',
          paymentStatus: 'Confirmado',
          inscriptionStatus: 'Habilitado',
          previousCourse: 'Curso Básico (2023)',
          acreditationStatus: 'Pendiente'
        };
      } else {
        this.selectedParticipant = null;
      }
    },
    acreditarParticipante() {
      if (this.canAcredit) {
        // Aquí iría la lógica para acreditar en backend
        this.selectedParticipant.acreditationStatus = 'Acreditado';
        
        // Actualizar métricas
        this.metrics.totalAcreditados++;
        this.metrics.pendientes--;
        this.metrics.acreditadosHoy++;
        this.metrics.porcentajeAcreditacion = Math.round(
          (this.metrics.totalAcreditados / (this.metrics.totalAcreditados + this.metrics.pendientes)) * 100
        );
        
        // Agregar a recientes
        this.recentAcreditations.unshift({
          id: Date.now(),
          time: new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' }),
          name: this.selectedParticipant.name,
          rut: this.selectedParticipant.rut,
          course: this.selectedParticipant.currentCourse,
          status: 'Acreditado'
        });

        // Mostrar alerta de éxito
        this.acreditationSuccess = true;
      }
    },
    handleRowClick(event) {
      console.log('Fila clickeada:', event);
      // Aquí podrías implementar ver detalles del participante
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
  min-width: 140px;
  display: inline-block;
}

.acreditation-actions {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.btn-acreditar {
  font-size: 18px;
  font-weight: bold;
  padding: 16px 32px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.recent-acreditations h2 {
  margin-bottom: 16px;
  color: #2c3e50;
}

.status-confirmado {
  color: #155724;
  font-weight: 600;
}

.status-habilitado {
  color: #155724;
  font-weight: 600;
}

.status-acreditado {
  color: #155724;
  font-weight: 600;
}

.status-pendiente {
  color: #856404;
  font-weight: 600;
}
=======
<template>
  <div class="manual-acreditation">
    <!-- Título -->
    <div class="acreditation-header">
      <h1>Acreditación Manual</h1>
      <p>Sistema de acreditación para eventos scouts</p>
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
      <h2>Información del Participante</h2>
      
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
            <strong>Curso Actual:</strong> {{ selectedParticipant.currentCourse }}
          </div>
          <div class="info-item">
            <strong>Grupo Scout:</strong> {{ selectedParticipant.scoutGroup }}
          </div>
          <div class="info-item">
            <strong>Rol:</strong> {{ selectedParticipant.role }}
          </div>
        </div>

        <div class="info-section">
          <h3>Estado de Inscripción</h3>
          <div class="info-item">
            <strong>Estado Pago:</strong> 
            <span :class="paymentStatusClass">{{ selectedParticipant.paymentStatus }}</span>
          </div>
          <div class="info-item">
            <strong>Estado Inscripción:</strong> 
            <span :class="inscriptionStatusClass">{{ selectedParticipant.inscriptionStatus }}</span>
          </div>
          <div class="info-item">
            <strong>Curso Anterior:</strong> {{ selectedParticipant.previousCourse }}
          </div>
          <div class="info-item">
            <strong>Acreditación:</strong> 
            <span :class="acreditationStatusClass">{{ selectedParticipant.acreditationStatus }}</span>
          </div>
        </div>
      </div>

      <!-- Botón de acreditar -->
      <div class="acreditation-actions">
        <BaseButton
          @click="acreditarParticipante"
          :disabled="!canAcredit"
          variant="primary"
          size="lg"
          class="btn-acreditar"
        >
          {{ acreditationButtonText }}
        </BaseButton>
      </div>
    </div>

    <!-- Métricas usando DataCard -->
    <div class="metrics-grid">
      <DataCard
        title="Total Acreditados"
        :value="metrics.totalAcreditados"
      />
      <DataCard
        title="Pendientes"
        :value="metrics.pendientes"
      />
      <DataCard
        title="% de Acreditación"
        :value="`${metrics.porcentajeAcreditacion}%`"
      />
      <DataCard
        title="Acreditados Hoy"
        :value="metrics.acreditadosHoy"
      />
    </div>

    <!-- Acreditaciones recientes usando DataTable -->
    <div class="recent-acreditations">
      <h2>Acreditaciones Recientes</h2>
      <DataTable
        :columns="tableColumns"
        :rows="recentAcreditations"
        :paginated="true"
        :page-size="5"
        search-placeholder="Buscar en acreditaciones..."
        empty-message="No hay acreditaciones recientes"
        @row-click="handleRowClick"
      />
    </div>
  </div>
</template>

<script>
import DataCard from '@/components/Reutilizables/DataCard.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'

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
      metrics: {
        totalAcreditados: 87,
        pendientes: 23,
        porcentajeAcreditacion: 79,
        acreditadosHoy: 15
      },
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
        },
        {
          id: 3,
          time: '14:15',
          name: 'ANA TORRES MUÑOZ',
          rut: '22.333.444-5',
          course: 'Formación de Dirigentes',
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
             this.selectedParticipant.inscriptionStatus === 'Habilitado' &&
             this.selectedParticipant.acreditationStatus === 'Pendiente';
    },
    acreditationButtonText() {
      if (!this.selectedParticipant) return 'ACREDITAR PARTICIPANTE';
      return this.selectedParticipant.acreditationStatus === 'Acreditado' 
        ? 'YA ACREDITADO' 
        : 'ACREDITAR PARTICIPANTE';
    },
    paymentStatusClass() {
      return this.selectedParticipant?.paymentStatus === 'Confirmado' 
        ? 'status-confirmado' 
        : 'status-pendiente';
    },
    inscriptionStatusClass() {
      return this.selectedParticipant?.inscriptionStatus === 'Habilitado' 
        ? 'status-habilitado' 
        : 'status-pendiente';
    },
    acreditationStatusClass() {
      return this.selectedParticipant?.acreditationStatus === 'Acreditado' 
        ? 'status-acreditado' 
        : 'status-pendiente';
    }
  },
  methods: {
    handleSearch() {
      // Simular búsqueda - en producción harías una llamada API
      if (this.searchTerm.trim()) {
        this.selectedParticipant = {
          name: 'JUAN PÉREZ GONZÁLEZ',
          rut: '12.345.678-9',
          currentCourse: 'Formación de Dirigentes',
          scoutGroup: 'GRUPO ARAUCO',
          role: 'DIRIGENTE SCOUT',
          paymentStatus: 'Confirmado',
          inscriptionStatus: 'Habilitado',
          previousCourse: 'Curso Básico (2023)',
          acreditationStatus: 'Pendiente'
        };
      } else {
        this.selectedParticipant = null;
      }
    },
    acreditarParticipante() {
      if (this.canAcredit) {
        // Aquí iría la lógica para acreditar en backend
        this.selectedParticipant.acreditationStatus = 'Acreditado';
        
        // Actualizar métricas
        this.metrics.totalAcreditados++;
        this.metrics.pendientes--;
        this.metrics.acreditadosHoy++;
        this.metrics.porcentajeAcreditacion = Math.round(
          (this.metrics.totalAcreditados / (this.metrics.totalAcreditados + this.metrics.pendientes)) * 100
        );
        
        // Agregar a recientes
        this.recentAcreditations.unshift({
          id: Date.now(),
          time: new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' }),
          name: this.selectedParticipant.name,
          rut: this.selectedParticipant.rut,
          course: this.selectedParticipant.currentCourse,
          status: 'Acreditado'
        });

        // Mostrar alerta de éxito
        this.acreditationSuccess = true;
      }
    },
    handleRowClick(event) {
      console.log('Fila clickeada:', event);
      // Aquí podrías implementar ver detalles del participante
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
  min-width: 140px;
  display: inline-block;
}

.acreditation-actions {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.btn-acreditar {
  font-size: 18px;
  font-weight: bold;
  padding: 16px 32px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.recent-acreditations h2 {
  margin-bottom: 16px;
  color: #2c3e50;
}

.status-confirmado {
  color: #155724;
  font-weight: 600;
}

.status-habilitado {
  color: #155724;
  font-weight: 600;
}

.status-acreditado {
  color: #155724;
  font-weight: 600;
}

.status-pendiente {
  color: #856404;
  font-weight: 600;
}
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
</style>