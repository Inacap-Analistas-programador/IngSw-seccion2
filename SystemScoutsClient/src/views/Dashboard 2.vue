<template>
  <div class="dashboard-scout">
    <!-- Navbar Superior -->
    <NavBar />

    <!-- Sidebar -->
    <SideBar />

    <!-- Contenido Principal -->
    <main class="main-content">
      <!-- Tarjetas de Estadísticas -->
      <div class="stats-grid">
        <DataCard
          title="Personas Registradas"
          :value="totalPersonas"
          description="Total de personas en el sistema"
        />
        
        <DataCard
          title="Cursos Activos"
          :value="cursosActivos"
          description="Cursos en progreso"
        />
        
        <DataCard
          title="Pendientes de Pago"
          :value="pagosPendientes"
          description="Pagos por procesar"
        />
        
        <DataCard
          title="Inscripciones Recientes"
          :value="inscripcionesRecientes"
          description="Últimos 7 días"
        />
      </div>

      <!-- Alertas del Sistema -->
      <BaseAlert
        v-if="alertas.length > 0"
        v-for="alerta in alertas"
        :key="alerta.id"
        :type="alerta.type"
        :title="alerta.title"
        :message="alerta.message"
        :dismissible="true"
        @close="removerAlerta(alerta.id)"
      />

      <!-- Gráfico de Montos Pagados por Curso (simulado con DataCardList) -->
      <section class="chart-section">
        <h3>Montos Pagados por Curso</h3>
        <DataCardList :cards="montosCursos" />
      </section>

      <!-- Tabla de Cursos Vigentes -->
      <section class="courses-section">
        <h3>Cursos Vigentes</h3>
        <DataTable
          :columns="columnasCursos"
          :rows="cursosVigentes"
          :pageSize="5"
          @view="verCurso"
        />
      </section>

      <!-- Tabla de Responsables de Cursos -->
      <section class="responsibles-section">
        <h3>Responsables de Cursos</h3>
        <div class="tabs-container">
          <div class="tabs-header">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              :class="['tab-button', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>
          
          <div class="tab-content">
            <DataTable
              v-if="activeTab === 'coordinadores'"
              :columns="columnasCoordinadores"
              :rows="coordinadores"
              :pageSize="5"
            />
            
            <DataTable
              v-if="activeTab === 'formadores'"
              :columns="columnasFormadores"
              :rows="formadores"
              :pageSize="5"
            />
            
            <DataTable
              v-if="activeTab === 'directores'"
              :columns="columnasDirectores"
              :rows="directores"
              :pageSize="5"
            />
            
            <DataTable
              v-if="activeTab === 'alimentacion'"
              :columns="columnasAlimentacion"
              :rows="responsablesAlimentacion"
              :pageSize="5"
            />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Componentes que realmente tienes
import NavBar from '@/components/Reutilizables/NavBar.vue'
import SideBar from '@/components/Reutilizables/SideBar.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import DataCard from '@/components/Reutilizables/DataCard.vue'
import DataCardList from '@/components/Reutilizables/DataCardList.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'

export default {
  name: 'DashboardScout',
  
  components: {
    NavBar,
    SideBar,
    BaseAlert,
    BaseButton,
    BaseSelect,
    BaseModal,
    DataCard,
    DataCardList,
    DataTable
  },
  
  setup() {
    const router = useRouter()
    
    // Estado reactivo
    const activeTab = ref('coordinadores')
    const alertas = ref([])

    // Datos de ejemplo (reemplazar con datos reales de tu API)
    const personas = ref([
      { id: 1, nombre: 'Juan Pérez', rut: '12.345.678-9', email: 'juan@email.com', telefono: '+56912345678', grupo: 'Grupo 1', rama: 'Scout', fechaRegistro: '2024-01-15' },
      { id: 2, nombre: 'María González', rut: '23.456.789-0', email: 'maria@email.com', telefono: '+56923456789', grupo: 'Grupo 2', rama: 'Guía', fechaRegistro: '2024-01-14' },
      { id: 3, nombre: 'Carlos López', rut: '34.567.890-1', email: 'carlos@email.com', telefono: '+56934567890', grupo: 'Grupo 1', rama: 'Scout', fechaRegistro: '2024-01-13' }
    ])

    const cursos = ref([
      { 
        id: 1, 
        titulo: 'Curso de Liderazgo', 
        fecha: '2024-02-01', 
        participantes: '15/20', 
        estado: 'activo',
        inscripciones: 15,
        acreditaciones: 12,
        pendientesPago: 3,
        montoPagado: 750000
      },
      { 
        id: 2, 
        titulo: 'Primeros Auxilios', 
        fecha: '2024-02-15', 
        participantes: '18/25', 
        estado: 'activo',
        inscripciones: 18,
        acreditaciones: 15,
        pendientesPago: 3,
        montoPagado: 900000
      },
      { 
        id: 3, 
        titulo: 'Educación Ambiental Scout', 
        fecha: '2024-03-01', 
        participantes: '10/15', 
        estado: 'activo',
        inscripciones: 10,
        acreditaciones: 8,
        pendientesPago: 2,
        montoPagado: 500000
      }
    ])

    const responsables = ref([
      // Coordinadores
      { id: 1, tipo: 'coordinador', nombre: 'Ana Silva', curso: 'Curso de Liderazgo', estado: 'activo', contacto: 'ana@email.com' },
      { id: 2, tipo: 'coordinador', nombre: 'Roberto Díaz', curso: 'Primeros Auxilios', estado: 'activo', contacto: 'roberto@email.com' },
      { id: 3, tipo: 'coordinador', nombre: 'Lucía Mendoza', curso: 'Educación Ambiental Scout', estado: 'inactivo', contacto: 'lucia@email.com' },
      
      // Formadores
      { id: 4, tipo: 'formador', nombre: 'Pedro Rojas', curso: 'Curso de Liderazgo', estado: 'activo', contacto: 'pedro@email.com' },
      { id: 5, tipo: 'formador', nombre: 'Carmen Fuentes', curso: 'Primeros Auxilios', estado: 'activo', contacto: 'carmen@email.com' },
      { id: 6, tipo: 'formador', nombre: 'Javier Soto', curso: 'Educación Ambiental Scout', estado: 'activo', contacto: 'javier@email.com' },
      
      // Directores
      { id: 7, tipo: 'director', nombre: 'Marcela Vega', curso: 'Curso de Liderazgo', estado: 'activo', contacto: 'marcela@email.com' },
      { id: 8, tipo: 'director', nombre: 'Fernando Castro', curso: 'Primeros Auxilios', estado: 'inactivo', contacto: 'fernando@email.com' },
      { id: 9, tipo: 'director', nombre: 'Isabel Torres', curso: 'Educación Ambiental Scout', estado: 'activo', contacto: 'isabel@email.com' },
      
      // Responsables de alimentación
      { id: 10, tipo: 'alimentacion', nombre: 'Patricia López', curso: 'Curso de Liderazgo', estado: 'activo', contacto: 'patricia@email.com' },
      { id: 11, tipo: 'alimentacion', nombre: 'Ricardo Mora', curso: 'Primeros Auxilios', estado: 'activo', contacto: 'ricardo@email.com' },
      { id: 12, tipo: 'alimentacion', nombre: 'Sandra Reyes', curso: 'Educación Ambiental Scout', estado: 'inactivo', contacto: 'sandra@email.com' }
    ])

    // Computed properties
    const totalPersonas = computed(() => personas.value.length)
    const cursosActivos = computed(() => cursos.value.filter(c => c.estado === 'activo').length)
    const pagosPendientes = computed(() => {
      return cursos.value.reduce((total, curso) => total + curso.pendientesPago, 0)
    })
    const inscripcionesRecientes = computed(() => 12) // Ejemplo estático

    const cursosVigentes = computed(() => {
      return cursos.value.filter(c => c.estado === 'activo').map(c => ({
        id: c.id,
        titulo: c.titulo,
        fecha: c.fecha,
        participantes: c.participantes,
        inscripciones: c.inscripciones,
        acreditaciones: c.acreditaciones,
        pendientesPago: c.pendientesPago,
        montoPagado: `$${c.montoPagado.toLocaleString('es-CL')}`
      }))
    })

    // Simulación de gráfico usando DataCardList
    const montosCursos = computed(() => {
      return cursos.value.map(c => ({
        title: c.titulo,
        value: `$${c.montoPagado.toLocaleString('es-CL')}`,
        description: `${c.inscripciones} inscripciones`
      }))
    })

    const coordinadores = computed(() => {
      return responsables.value
        .filter(r => r.tipo === 'coordinador')
        .map(r => ({
          id: r.id,
          nombre: r.nombre,
          curso: r.curso,
          estado: r.estado,
          contacto: r.contacto,
          estadoDisplay: r.estado === 'activo' ? '● Activo' : '● Inactivo'
        }))
    })

    const formadores = computed(() => {
      return responsables.value
        .filter(r => r.tipo === 'formador')
        .map(r => ({
          id: r.id,
          nombre: r.nombre,
          curso: r.curso,
          estado: r.estado,
          contacto: r.contacto,
          estadoDisplay: r.estado === 'activo' ? '● Activo' : '● Inactivo'
        }))
    })

    const directores = computed(() => {
      return responsables.value
        .filter(r => r.tipo === 'director')
        .map(r => ({
          id: r.id,
          nombre: r.nombre,
          curso: r.curso,
          estado: r.estado,
          contacto: r.contacto,
          estadoDisplay: r.estado === 'activo' ? '● Activo' : '● Inactivo'
        }))
    })

    const responsablesAlimentacion = computed(() => {
      return responsables.value
        .filter(r => r.tipo === 'alimentacion')
        .map(r => ({
          id: r.id,
          nombre: r.nombre,
          curso: r.curso,
          estado: r.estado,
          contacto: r.contacto,
          estadoDisplay: r.estado === 'activo' ? '● Activo' : '● Inactivo'
        }))
    })

    // Configuración de columnas para las tablas
    const columnasCursos = [
      { key: 'titulo', label: 'Curso', sortable: true },
      { key: 'fecha', label: 'Fecha', sortable: true },
      { key: 'participantes', label: 'Participantes', sortable: true },
      { key: 'inscripciones', label: 'Inscripciones', sortable: true },
      { key: 'acreditaciones', label: 'Acreditaciones', sortable: true },
      { key: 'pendientesPago', label: 'Pendientes de Pago', sortable: true },
      { key: 'montoPagado', label: 'Monto Pagado', sortable: true }
    ]

    const columnasCoordinadores = [
      { key: 'nombre', label: 'Coordinador', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'contacto', label: 'Contacto', sortable: true },
      { key: 'estadoDisplay', label: 'Estado', sortable: true }
    ]

    const columnasFormadores = [
      { key: 'nombre', label: 'Formador', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'contacto', label: 'Contacto', sortable: true },
      { key: 'estadoDisplay', label: 'Estado', sortable: true }
    ]

    const columnasDirectores = [
      { key: 'nombre', label: 'Director', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'contacto', label: 'Contacto', sortable: true },
      { key: 'estadoDisplay', label: 'Estado', sortable: true }
    ]

    const columnasAlimentacion = [
      { key: 'nombre', label: 'Responsable', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'contacto', label: 'Contacto', sortable: true },
      { key: 'estadoDisplay', label: 'Estado', sortable: true }
    ]

    // Tabs para responsables
    const tabs = ref([
      { id: 'coordinadores', label: 'Coordinadores' },
      { id: 'formadores', label: 'Formadores' },
      { id: 'directores', label: 'Directores' },
      { id: 'alimentacion', label: 'Alimentación' }
    ])

    // Métodos
    const verCurso = (curso) => {
      router.push(`/cursos/detalle/${curso.id}`)
    }

    const removerAlerta = (id) => {
      alertas.value = alertas.value.filter(alerta => alerta.id !== id)
    }

    // Simular carga de datos
    onMounted(async () => {
      // Aquí cargarías los datos reales desde tus servicios
    })

    return {
      // Estado
      activeTab,
      alertas,
      
      // Datos
      tabs,
      
      // Computed
      totalPersonas,
      cursosActivos,
      pagosPendientes,
      inscripcionesRecientes,
      cursosVigentes,
      montosCursos,
      coordinadores,
      formadores,
      directores,
      responsablesAlimentacion,
      
      // Configuración
      columnasCursos,
      columnasCoordinadores,
      columnasFormadores,
      columnasDirectores,
      columnasAlimentacion,
      
      // Métodos
      verCurso,
      removerAlerta
    }
  }
}
</script>

<style scoped>
.dashboard-scout {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-content {
  margin-left: 250px; /* Ancho del sidebar */
  padding: 20px;
  min-height: calc(100vh - 64px); /* Altura menos navbar */
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-section,
.courses-section,
.responsibles-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.chart-section h3,
.courses-section h3,
.responsibles-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #19548a;
}

.tabs-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.tabs-header {
  display: flex;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.tab-button {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  color: #666;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background-color: #e9e9e9;
}

.tab-button.active {
  background-color: #19548a;
  color: white;
}

.tab-content {
  padding: 15px;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    width: 100%;
    text-align: left;
  }
}
</style>