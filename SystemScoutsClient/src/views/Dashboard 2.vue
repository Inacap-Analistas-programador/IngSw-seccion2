<template>
  <div class="dashboard-scout">
    <!-- Navbar Superior -->
    <NavBar />

    <!-- Sidebar -->
    <SideBar />

    <!-- Contenido Principal -->
    <main class="main-content">
      <!-- Filtros Principales -->
      <div class="filters-section">
        <BaseSelect
          v-model="filtros.region"
          label="Región"
          :options="regiones"
          placeholder="Seleccione región"
        />
        <BaseSelect
          v-model="filtros.provincia"
          label="Provincia"
          :options="provinciasFiltradas"
          placeholder="Seleccione provincia"
          :disabled="!filtros.region"
        />
        <BaseSelect
          v-model="filtros.comuna"
          label="Comuna"
          :options="comunasFiltradas"
          placeholder="Seleccione comuna"
          :disabled="!filtros.provincia"
        />
        <BaseButton @click="limpiarFiltros" variant="outline">
          Limpiar Filtros
        </BaseButton>
      </div>

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
          title="Pagos Pendientes"
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

      <!-- Tabla de Personas Recientes -->
      <section class="recent-section">
        <h3>Personas Recientemente Registradas</h3>
        <DataTable
          :columns="columnasPersonas"
          :rows="personasRecientes"
          :pageSize="5"
          @view="verPersona"
          @edit="editarPersona"
        />
      </section>

      <!-- Lista de Próximos Cursos -->
      <section class="courses-section">
        <h3>Próximos Cursos</h3>
        <DataCardList :cards="proximosCursos" />
      </section>

      <!-- Modal para Detalles de Persona -->
      <BaseModal v-model="modalPersonaVisible">
        <div v-if="personaSeleccionada">
          <h3>Detalles de Persona</h3>
          <div class="persona-details">
            <p><strong>Nombre:</strong> {{ personaSeleccionada.nombre }}</p>
            <p><strong>RUT:</strong> {{ personaSeleccionada.rut }}</p>
            <p><strong>Email:</strong> {{ personaSeleccionada.email }}</p>
            <p><strong>Teléfono:</strong> {{ personaSeleccionada.telefono }}</p>
            <p><strong>Grupo:</strong> {{ personaSeleccionada.grupo }}</p>
            <p><strong>Rama:</strong> {{ personaSeleccionada.rama }}</p>
          </div>
          <BaseButton @click="modalPersonaVisible = false" variant="primary">
            Cerrar
          </BaseButton>
        </div>
      </BaseModal>
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

// Servicios (ajusta las rutas según tu estructura real)
// import PersonaService from '@/services/PersonaService.js'
// import CursoService from '@/services/CursoService.js'

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
    const filtros = ref({
      region: '',
      provincia: '',
      comuna: ''
    })

    const modalPersonaVisible = ref(false)
    const personaSeleccionada = ref(null)
    const alertas = ref([])

    // Datos de ejemplo (reemplazar con datos reales de tu API)
    const regiones = ref([
      { value: '1', label: 'Región Metropolitana' },
      { value: '2', label: 'Valparaíso' },
      { value: '3', label: 'Biobío' }
    ])

    const provincias = ref([
      { value: '1', label: 'Santiago', region: '1' },
      { value: '2', label: 'Cordillera', region: '1' },
      { value: '3', label: 'Valparaíso', region: '2' },
      { value: '4', label: 'Concepción', region: '3' }
    ])

    const comunas = ref([
      { value: '1', label: 'Santiago', provincia: '1' },
      { value: '2', label: 'Providencia', provincia: '1' },
      { value: '3', label: 'Viña del Mar', provincia: '3' },
      { value: '4', label: 'Concepción', provincia: '4' }
    ])

    const personas = ref([
      { id: 1, nombre: 'Juan Pérez', rut: '12.345.678-9', email: 'juan@email.com', telefono: '+56912345678', grupo: 'Grupo 1', rama: 'Scout', fechaRegistro: '2024-01-15' },
      { id: 2, nombre: 'María González', rut: '23.456.789-0', email: 'maria@email.com', telefono: '+56923456789', grupo: 'Grupo 2', rama: 'Guía', fechaRegistro: '2024-01-14' },
      { id: 3, nombre: 'Carlos López', rut: '34.567.890-1', email: 'carlos@email.com', telefono: '+56934567890', grupo: 'Grupo 1', rama: 'Scout', fechaRegistro: '2024-01-13' }
    ])

    const cursos = ref([
      { id: 1, titulo: 'Curso de Liderazgo', fecha: '2024-02-01', participantes: '15/20', estado: 'activo' },
      { id: 2, titulo: 'Primeros Auxilios', fecha: '2024-02-15', participantes: '18/25', estado: 'activo' },
      { id: 3, titulo: 'Navegación', fecha: '2024-03-01', participantes: '10/15', estado: 'planificado' }
    ])

    // Computed properties para filtros en cascada
    const provinciasFiltradas = computed(() => {
      if (!filtros.value.region) return []
      return provincias.value.filter(p => p.region === filtros.value.region)
    })

    const comunasFiltradas = computed(() => {
      if (!filtros.value.provincia) return []
      return comunas.value.filter(c => c.provincia === filtros.value.provincia)
    })

    // Estadísticas computadas
    const totalPersonas = computed(() => personas.value.length)
    const cursosActivos = computed(() => cursos.value.filter(c => c.estado === 'activo').length)
    const pagosPendientes = computed(() => 5) // Ejemplo estático
    const inscripcionesRecientes = computed(() => 12) // Ejemplo estático

    const personasRecientes = computed(() => {
      return personas.value.slice(0, 5).map(p => ({
        id: p.id,
        nombre: p.nombre,
        rut: p.rut,
        email: p.email,
        grupo: p.grupo,
        fecha: p.fechaRegistro
      }))
    })

    const proximosCursos = computed(() => {
      return cursos.value.slice(0, 3).map(c => ({
        title: c.titulo,
        value: c.participantes,
        description: `Fecha: ${c.fecha}`
      }))
    })

    // Configuración de columnas para DataTable
    const columnasPersonas = [
      { key: 'nombre', label: 'Nombre', sortable: true },
      { key: 'rut', label: 'RUT', sortable: true },
      { key: 'email', label: 'Email', sortable: true },
      { key: 'grupo', label: 'Grupo', sortable: true },
      { key: 'fecha', label: 'Fecha Registro', sortable: true }
    ]

    // Métodos
    const limpiarFiltros = () => {
      filtros.value = {
        region: '',
        provincia: '',
        comuna: ''
      }
    }

    const verPersona = (persona) => {
      personaSeleccionada.value = personas.value.find(p => p.id === persona.id)
      modalPersonaVisible.value = true
    }

    const editarPersona = (persona) => {
      router.push(`/gestionpersonas/editar/${persona.id}`)
    }

    const removerAlerta = (id) => {
      alertas.value = alertas.value.filter(alerta => alerta.id !== id)
    }

    // Simular carga de datos
    onMounted(async () => {
      // Aquí cargarías los datos reales desde tus servicios
      // try {
      //   const datos = await PersonaService.obtenerPersonas();
      //   personas.value = datos;
      // } catch (error) {
      //   alertas.value.push({
      //     id: Date.now(),
      //     type: 'error',
      //     title: 'Error',
      //     message: 'No se pudieron cargar los datos'
      //   });
      // }
    })

    return {
      // Estado
      filtros,
      modalPersonaVisible,
      personaSeleccionada,
      alertas,
      
      // Datos
      regiones,
      provinciasFiltradas,
      comunasFiltradas,
      
      // Computed
      totalPersonas,
      cursosActivos,
      pagosPendientes,
      inscripcionesRecientes,
      personasRecientes,
      proximosCursos,
      
      // Configuración
      columnasPersonas,
      
      // Métodos
      limpiarFiltros,
      verPersona,
      editarPersona,
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

.filters-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: end;
}

.filters-section .base-select {
  min-width: 200px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.recent-section,
.courses-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.recent-section h3,
.courses-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #19548a;
}

.persona-details {
  margin-bottom: 20px;
}

.persona-details p {
  margin: 8px 0;
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters-section .base-select {
    min-width: auto;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>