<template>
  <div class="dashboard-scout">
    <!-- Contenido Principal SIN SideBar -->
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

      <!-- Gráfico de Montos Pagados por Curso -->
      <section class="chart-section">
        <h3>Montos Recaudados por Curso</h3>
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

// Componentes
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import BaseModal from '@/components/BaseModal.vue'
import DataCard from '@/components/DataCard.vue'
import DataCardList from '@/components/DataCardList.vue'
import DataTable from '@/components/DataTable.vue'

export default {
  name: 'DashboardScout',
  
  components: {
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

    // Datos basados en la estructura de la base de datos Scouts Biobío
    const personas = ref([
      { 
        PER_ID: 1, 
        PER_RUN: 12345678, 
        PER_DV: '9', 
        PER_APELPAT: 'Pérez', 
        PER_APELMAT: 'González', 
        PER_NOMBRES: 'Juan Antonio', 
        PER_EMAIL: 'juan@email.com', 
        PER_FECHA_NAC: '1990-05-15',
        PER_FONO: '+56912345678',
        PER_VIGENTE: true
      },
      { 
        PER_ID: 2, 
        PER_RUN: 23456789, 
        PER_DV: '0', 
        PER_APELPAT: 'González', 
        PER_APELMAT: 'López', 
        PER_NOMBRES: 'María Isabel', 
        PER_EMAIL: 'maria@email.com', 
        PER_FECHA_NAC: '1985-08-20',
        PER_FONO: '+56923456789',
        PER_VIGENTE: true
      }
    ])

    // Datos de cursos según estructura CURSO de la BD
    const cursos = ref([
      { 
        CUR_ID: 1,
        CUR_CODIGO: 'LID-2024',
        CUR_DESCRIPCION: 'Curso de Liderazgo Scout Avanzado',
        CUR_FECHA_HORA: '2024-02-01 09:00:00',
        CUR_LUGAR: 'Sede Regional Biobío',
        CUR_ESTADO: 1, // 1 = Activo, 2 = Finalizado, 3 = Cancelado
        CUR_CUOTA_CON_ALMUERZO: 75000,
        CUR_CUOTA_SIN_ALMUERZO: 50000,
        CUR_MODALIDAD: 1, // 1 = Presencial, 2 = Virtual
        CUR_TIPO_CURSO: 1 // Según TCU_ID en TIPO_CURSO
      },
      { 
        CUR_ID: 2,
        CUR_CODIGO: 'PA-2024',
        CUR_DESCRIPCION: 'Primeros Auxilios para Dirigentes',
        CUR_FECHA_HORA: '2024-02-15 08:30:00',
        CUR_LUGAR: 'Hospital Regional',
        CUR_ESTADO: 1,
        CUR_CUOTA_CON_ALMUERZO: 60000,
        CUR_CUOTA_SIN_ALMUERZO: 40000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 2
      },
      { 
        CUR_ID: 3,
        CUR_CODIGO: 'AMB-2024',
        CUR_DESCRIPCION: 'Educación Ambiental Scout',
        CUR_FECHA_HORA: '2024-03-01 10:00:00',
        CUR_LUGAR: 'Reserva Natural',
        CUR_ESTADO: 2, // Finalizado
        CUR_CUOTA_CON_ALMUERZO: 45000,
        CUR_CUOTA_SIN_ALMUERZO: 30000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 3
      }
    ])

    // Datos de PERSONA_CURSO (inscripciones)
    const personasCurso = ref([
      { PEC_ID: 1, PER_ID: 1, CUR_ID: 1, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 2, PER_ID: 2, CUR_ID: 1, PEC_ACREDITADO: false, PEC_REGISTRO: true },
      { PEC_ID: 3, PER_ID: 1, CUR_ID: 2, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 4, PER_ID: 2, CUR_ID: 3, PEC_ACREDITADO: true, PEC_REGISTRO: true }
    ])

    // Datos de PAGO_PERSONA según estructura de BD
    const pagosPersona = ref([
      { PAP_ID: 1, PER_ID: 1, CUR_ID: 1, PAP_VALOR: 75000, PAP_ESTADO: 1 }, // 1 = Pagado
      { PAP_ID: 2, PER_ID: 2, CUR_ID: 1, PAP_VALOR: 75000, PAP_ESTADO: 2 }, // 2 = Pendiente
      { PAP_ID: 3, PER_ID: 1, CUR_ID: 2, PAP_VALOR: 60000, PAP_ESTADO: 1 },
      { PAP_ID: 4, PER_ID: 2, CUR_ID: 3, PAP_VALOR: 45000, PAP_ESTADO: 1 }
    ])

    // Datos de responsables según estructura CURSO_COORDINADOR, CURSO_FORMADOR
    const cursoCoordinadores = ref([
      { CUC_ID: 1, CUR_ID: 1, PER_ID: 1, CAR_ID: 1, CUC_CARGO: 'Coordinador General' }
    ])

    const cursoFormadores = ref([
      { CUO_ID: 1, CUR_ID: 1, PER_ID: 2, ROL_ID: 1, CUO_DIRECTOR: false }
    ])

    const cursoDirectores = ref([
      { CUO_ID: 2, CUR_ID: 1, PER_ID: 1, ROL_ID: 2, CUO_DIRECTOR: true }
    ])

    const cursoAlimentacion = ref([
      { CUA_ID: 1, CUR_ID: 1, ALI_ID: 1, CUA_DESCRIPCION: 'Almuerzo tipo scout' }
    ])

    // Computed properties basadas en la estructura real de la BD
    const totalPersonas = computed(() => personas.value.filter(p => p.PER_VIGENTE).length)
    
    const cursosActivos = computed(() => 
      cursos.value.filter(c => c.CUR_ESTADO === 1).length
    )
    
    const pagosPendientes = computed(() => 
      pagosPersona.value.filter(p => p.PAP_ESTADO === 2).length
    )
    
    const inscripcionesRecientes = computed(() => 
      personasCurso.value.filter(pc => {
        // Simular inscripciones de los últimos 7 días
        const inscripcionDate = new Date('2024-01-20') // Fecha de ejemplo
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
        return inscripcionDate >= sevenDaysAgo
      }).length
    )

    const cursosVigentes = computed(() => {
      return cursos.value.map(curso => {
        const inscripciones = personasCurso.value.filter(pc => pc.CUR_ID === curso.CUR_ID).length
        const acreditados = personasCurso.value.filter(pc => 
          pc.CUR_ID === curso.CUR_ID && pc.PEC_ACREDITADO
        ).length
        const pagosCurso = pagosPersona.value.filter(p => p.CUR_ID === curso.CUR_ID)
        const montoRecaudado = pagosCurso
          .filter(p => p.PAP_ESTADO === 1)
          .reduce((sum, pago) => sum + pago.PAP_VALOR, 0)
        const pendientesPago = pagosCurso.filter(p => p.PAP_ESTADO === 2).length

        return {
          CUR_ID: curso.CUR_ID,
          CUR_CODIGO: curso.CUR_CODIGO,
          CUR_DESCRIPCION: curso.CUR_DESCRIPCION,
          CUR_FECHA_HORA: curso.CUR_FECHA_HORA.split(' ')[0], // Solo fecha
          CUR_LUGAR: curso.CUR_LUGAR,
          CUR_ESTADO: getEstadoDisplay(curso.CUR_ESTADO),
          inscripciones: inscripciones,
          acreditaciones: acreditados,
          pendientesPago: pendientesPago,
          montoRecaudado: `$${montoRecaudado.toLocaleString('es-CL')}`
        }
      })
    })

    // Simulación de gráfico usando DataCardList
    const montosCursos = computed(() => {
      return cursos.value.map(curso => {
        const pagosCurso = pagosPersona.value.filter(p => p.CUR_ID === curso.CUR_ID && p.PAP_ESTADO === 1)
        const montoRecaudado = pagosCurso.reduce((sum, pago) => sum + pago.PAP_VALOR, 0)
        const inscripciones = personasCurso.value.filter(pc => pc.CUR_ID === curso.CUR_ID).length

        return {
          title: curso.CUR_DESCRIPCION,
          value: `$${montoRecaudado.toLocaleString('es-CL')}`,
          description: `${inscripciones} inscripciones`
        }
      })
    })

    const coordinadores = computed(() => {
      return cursoCoordinadores.value.map(coord => {
        const persona = personas.value.find(p => p.PER_ID === coord.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === coord.CUR_ID)
        return {
          CUC_ID: coord.CUC_ID,
          nombre: persona ? `${persona.PER_NOMBRES} ${persona.PER_APELPAT}` : 'N/A',
          curso: curso ? curso.CUR_DESCRIPCION : 'N/A',
          contacto: persona ? persona.PER_EMAIL : 'N/A',
          cargo: coord.CUC_CARGO,
          estadoDisplay: '● Activo'
        }
      })
    })

    const formadores = computed(() => {
      return cursoFormadores.value.map(form => {
        const persona = personas.value.find(p => p.PER_ID === form.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === form.CUR_ID)
        return {
          CUO_ID: form.CUO_ID,
          nombre: persona ? `${persona.PER_NOMBRES} ${persona.PER_APELPAT}` : 'N/A',
          curso: curso ? curso.CUR_DESCRIPCION : 'N/A',
          contacto: persona ? persona.PER_EMAIL : 'N/A',
          tipo: form.CUO_DIRECTOR ? 'Director' : 'Formador',
          estadoDisplay: '● Activo'
        }
      })
    })

    const directores = computed(() => {
      return cursoDirectores.value.filter(dir => dir.CUO_DIRECTOR).map(dir => {
        const persona = personas.value.find(p => p.PER_ID === dir.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === dir.CUR_ID)
        return {
          CUO_ID: dir.CUO_ID,
          nombre: persona ? `${persona.PER_NOMBRES} ${persona.PER_APELPAT}` : 'N/A',
          curso: curso ? curso.CUR_DESCRIPCION : 'N/A',
          contacto: persona ? persona.PER_EMAIL : 'N/A',
          estadoDisplay: '● Activo'
        }
      })
    })

    const responsablesAlimentacion = computed(() => {
      return cursoAlimentacion.value.map(alim => {
        const curso = cursos.value.find(c => c.CUR_ID === alim.CUR_ID)
        return {
          CUA_ID: alim.CUA_ID,
          nombre: 'Responsable de Alimentación', // En BD real sería una persona
          curso: curso ? curso.CUR_DESCRIPCION : 'N/A',
          contacto: 'alimentacion@scoutsbiobio.cl',
          descripcion: alim.CUA_DESCRIPCION,
          estadoDisplay: '● Activo'
        }
      })
    })

    // Configuración de columnas para las tablas
    const columnasCursos = [
      { key: 'CUR_CODIGO', label: 'Código', sortable: true },
      { key: 'CUR_DESCRIPCION', label: 'Descripción', sortable: true },
      { key: 'CUR_FECHA_HORA', label: 'Fecha', sortable: true },
      { key: 'CUR_LUGAR', label: 'Lugar', sortable: true },
      { key: 'CUR_ESTADO', label: 'Estado', sortable: true },
      { key: 'inscripciones', label: 'Inscripciones', sortable: true },
      { key: 'acreditaciones', label: 'Acreditados', sortable: true },
      { key: 'pendientesPago', label: 'Pendientes Pago', sortable: true },
      { key: 'montoRecaudado', label: 'Monto Recaudado', sortable: true }
    ]

    const columnasCoordinadores = [
      { key: 'nombre', label: 'Coordinador', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'cargo', label: 'Cargo', sortable: true },
      { key: 'contacto', label: 'Contacto', sortable: true },
      { key: 'estadoDisplay', label: 'Estado', sortable: true }
    ]

    const columnasFormadores = [
      { key: 'nombre', label: 'Formador', sortable: true },
      { key: 'curso', label: 'Curso', sortable: true },
      { key: 'tipo', label: 'Tipo', sortable: true },
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
      { key: 'descripcion', label: 'Descripción', sortable: true },
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

    // Métodos auxiliares
    const getEstadoDisplay = (estado) => {
      const estados = {
        1: '● Activo',
        2: '● Finalizado',
        3: '● Cancelado'
      }
      return estados[estado] || '● Desconocido'
    }

    // Métodos
    const verCurso = (curso) => {
      router.push(`/cursos/detalle/${curso.CUR_ID}`)
    }

    const removerAlerta = (id) => {
      alertas.value = alertas.value.filter(alerta => alerta.id !== id)
    }

    // Simular carga de datos desde API
    onMounted(async () => {
      // En producción, aquí se cargarían los datos reales desde los servicios
      // que se conectan a la base de datos MySQL
      try {
        // Ejemplo de llamadas a API:
        // const responsePersonas = await apiService.getPersonas()
        // const responseCursos = await apiService.getCursos()
        // const responsePagos = await apiService.getPagos()
        // personas.value = responsePersonas.data
        // cursos.value = responseCursos.data
        // pagosPersona.value = responsePagos.data
      } catch (error) {
        console.error('Error cargando datos del dashboard:', error)
      }
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
  margin-left: 0;
  padding: 20px;
  min-height: 100vh;
  width: 100%;
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

/* Estilos para estados */
.status-active {
  color: #28a745;
  font-weight: 600;
}

.status-finished {
  color: #6c757d;
  font-weight: 600;
}

.status-cancelled {
  color: #dc3545;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
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