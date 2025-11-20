<template>
  <div class="dashboard-scout">
    <!-- Bloque de alertas globales -->
    <div v-if="alertas.length > 0" style="margin-bottom: 16px;">
      <BaseAlert
        v-for="alerta in alertas"
        :key="alerta.id"
        :type="alerta.type"
        :title="alerta.title"
        :message="alerta.message"
        :dismissible="true"
        @close="removerAlerta(alerta.id)"
      />
    </div>
    <!-- Contenido Principal -->
    <main class="main-content">
      <!-- Selector de Curso con Semáforo -->
      <section class="course-selector-section">
        <div class="selector-container">
          <div class="native-select-wrapper">
            <label for="curso-select" class="native-select-label">
              Seleccionar Curso
            </label>
            <select 
              id="curso-select"
              v-model="cursoSeleccionado" 
              class="native-select"
            >
              <option value="" disabled>Seleccione un curso</option>
              <option value="todos">Todos los cursos</option>
              <option v-for="curso in cursos" :key="curso.CUR_ID" :value="curso.CUR_ID">
                {{ curso.CUR_CODIGO }} - {{ curso.CUR_DESCRIPCION }}
              </option>
            </select>
          </div>
          
          <div class="semaphore-container">
            <div class="semaphore" :class="getSemaphoreClass(cursoSeleccionado)"></div>
            <span class="semaphore-label">{{ getEstadoDisplay(cursoSeleccionadoInfo?.CUR_ESTADO) }}</span>
          </div>
        </div>
      </section>

      <!-- Tarjetas de Estadísticas -->
      <div class="stats-grid">
        <DataCard
          title="Personas Inscritas"
          :value="personasInscritas"
          description="Total inscritos en el curso"
        />
        
        <DataCard
          title="Pendientes de Pago"
          :value="pagosPendientesCurso"
          description="Pagos pendientes del curso"
        />
        
        <DataCard
          title="Acreditados"
          :value="acreditadosCurso"
          description="Personas acreditadas"
        />
        
        <DataCard
          title="Inscripciones Recientes"
          :value="inscripcionesRecientes"
          description="Últimos 7 días"
        />
      </div>

      <!-- Gráficos -->
      <section class="charts-section">
        <h3>Estadísticas del Curso</h3>
        <div class="charts-grid">
          <div class="chart-card">
            <h4>Inscripciones vs Acreditados</h4>
            <div class="chart-placeholder">
              <div class="chart-bars">
                <div class="bar-container">
                  <div class="bar inscritos" :style="{ height: porcentajeInscritos + '%' }"></div>
                  <span>Inscritos: {{ personasInscritas }}</span>
                </div>
                <div class="bar-container">
                  <div class="bar acreditados" :style="{ height: porcentajeAcreditados + '%' }"></div>
                  <span>Acreditados: {{ acreditadosCurso }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="chart-card">
            <h4>Estado de Pagos</h4>
            <div class="chart-placeholder">
              <div class="payment-status">
                <div class="status-item">
                  <span class="dot paid"></span>
                  <span>Pagados: {{ pagosPagadosCurso }}</span>
                </div>
                <div class="status-item">
                  <span class="dot pending"></span>
                  <span>Pendientes: {{ pagosPendientesCurso }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Tabla de Cursos -->
      <section class="courses-section">
        <div class="section-header">
          <h3>Cursos Vigentes</h3>
          <button 
            @click="actualizarDatos" 
            class="refresh-btn"
            :disabled="loading"
          >
            🔄 {{ loading ? 'Cargando...' : 'Actualizar' }}
          </button>
        </div>
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th v-for="col in columnasCursos" :key="col.key">{{ col.label }}</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cursosFiltrados.length === 0">
                <td :colspan="columnasCursos.length + 1" style="text-align: center; padding: 20px; color: #999;">
                  No hay cursos disponibles
                </td>
              </tr>
              <tr v-for="curso in cursosFiltrados" :key="curso.CUR_ID">
                <td>{{ curso.CUR_CODIGO }}</td>
                <td>{{ curso.CUR_DESCRIPCION }}</td>
                <td>{{ curso.CUR_FECHA_HORA }}</td>
                <td>{{ curso.CUR_LUGAR }}</td>
                <td>{{ curso.CUR_ESTADO }}</td>
                <td>{{ curso.inscripciones }}</td>
                <td>{{ curso.acreditaciones }}</td>
                <td>{{ curso.pendientesPago }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verCurso(curso)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarCurso(curso)">✏ Editar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Tabla de Responsables -->
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
            <!-- Coordinadores -->
            <div v-if="activeTab === 'coordinadores'" class="table-container-expanded">
              <table class="data-table-expanded">
                <thead>
                  <tr>
                    <th>Coordinador</th>
                    <th>Curso</th>
                    <th>Cargo</th>
                    <th>Contacto</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="coordinadores.length === 0">
                    <td colspan="5" style="text-align: center; padding: 20px; color: #999;">
                      No hay coordinadores disponibles
                    </td>
                  </tr>
                  <tr v-for="coord in coordinadores" :key="coord.CUC_ID">
                    <td>{{ coord.nombre }}</td>
                    <td>{{ coord.curso }}</td>
                    <td>{{ coord.cargo }}</td>
                    <td>{{ coord.contacto }}</td>
                    <td>{{ coord.estadoDisplay }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Formadores -->
            <div v-if="activeTab === 'formadores'" class="table-container-expanded">
              <table class="data-table-expanded">
                <thead>
                  <tr>
                    <th>Formador</th>
                    <th>Curso</th>
                    <th>Tipo</th>
                    <th>Contacto</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="formadores.length === 0">
                    <td colspan="5" style="text-align: center; padding: 20px; color: #999;">
                      No hay formadores disponibles
                    </td>
                  </tr>
                  <tr v-for="form in formadores" :key="form.CUO_ID">
                    <td>{{ form.nombre }}</td>
                    <td>{{ form.curso }}</td>
                    <td>{{ form.tipo }}</td>
                    <td>{{ form.contacto }}</td>
                    <td>{{ form.estadoDisplay }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

// Componentes del sistema
import BaseAlert from '@/components/BaseAlert.vue'
import DataCard from '@/components/DataCard.vue'

// Services para conectar con la API
import { cursosService, personasService, pagosService } from '@/services'

export default {
  name: 'DashboardScout',
  
  components: {
    BaseAlert,
    DataCard
  },
  
  setup() {
    const router = useRouter()
    
    // Estado reactivo
    const cursoSeleccionado = ref('todos')
    const alertas = ref([])
    const loading = ref(false)
    const activeTab = ref('coordinadores')

    // Datos reactivos que se cargarán desde la API
    const personas = ref([])
    const cursos = ref([])
    const personasCurso = ref([])
    const pagosPersona = ref([])
    const cursoCoordinadores = ref([])
    const cursoFormadores = ref([])

    // Computed: información del curso seleccionado
    const cursoSeleccionadoInfo = computed(() => {
      if (cursoSeleccionado.value === 'todos' || !cursoSeleccionado.value) return null
      return cursos.value.find(c => c.CUR_ID == cursoSeleccionado.value)
    })

    // Computed: personas inscritas en el curso seleccionado
    const personasInscritas = computed(() => {
      if (cursoSeleccionado.value === 'todos' || !cursoSeleccionado.value) {
        return personasCurso.value.length
      }
      return personasCurso.value.filter(pc => pc.CUR_ID == cursoSeleccionado.value).length
    })

    // Computed: pagos pendientes
    const pagosPendientesCurso = computed(() => {
      const filtered = pagosPersona.value.filter(p => {
        if (cursoSeleccionado.value === 'todos' || !cursoSeleccionado.value) return true
        return p.CUR_ID == cursoSeleccionado.value
      })
      // Buscar estado = 2 o estado = "pendiente"
      return filtered.filter(p => p.PAP_ESTADO === 2 || String(p.PAP_ESTADO).toLowerCase() === 'pendiente').length
    })

    // Computed: acreditados
    const acreditadosCurso = computed(() => {
      if (cursoSeleccionado.value === 'todos' || !cursoSeleccionado.value) {
        return personasCurso.value.filter(pc => pc.PEC_ACREDITADO).length
      }
      return personasCurso.value.filter(pc => 
        pc.CUR_ID == cursoSeleccionado.value && pc.PEC_ACREDITADO
      ).length
    })

    // Computed: inscripciones recientes
    const inscripcionesRecientes = computed(() => {
      return personasCurso.value.filter(pc => {
        const curso = cursos.value.find(c => c.CUR_ID === pc.CUR_ID)
        return curso && curso.CUR_ESTADO === 1
      }).length
    })

    // Computed: porcentajes
    const porcentajeInscritos = computed(() => {
      return personasInscritas.value > 0 ? 100 : 0
    })

    const porcentajeAcreditados = computed(() => {
      const total = personasInscritas.value
      const acreditados = acreditadosCurso.value
      return total > 0 ? (acreditados / total) * 100 : 0
    })

    const pagosPagadosCurso = computed(() => {
      const filtered = pagosPersona.value.filter(p => {
        if (cursoSeleccionado.value === 'todos' || !cursoSeleccionado.value) return true
        return p.CUR_ID == cursoSeleccionado.value
      })
      return filtered.filter(p => p.PAP_ESTADO === 1 || String(p.PAP_ESTADO).toLowerCase() === 'pagado').length
    })

    // Computed: cursos filtrados
    const cursosFiltrados = computed(() => {
      let cursosData = cursos.value.map(curso => {
        const inscripciones = personasCurso.value.filter(pc => pc.CUR_ID === curso.CUR_ID).length
        const acreditados = personasCurso.value.filter(pc => 
          pc.CUR_ID === curso.CUR_ID && pc.PEC_ACREDITADO
        ).length
        const pagosCurso = pagosPersona.value.filter(p => p.CUR_ID === curso.CUR_ID)
        const pendientesPago = pagosCurso.filter(p => p.PAP_ESTADO === 2 || String(p.PAP_ESTADO).toLowerCase() === 'pendiente').length

        return {
          CUR_ID: curso.CUR_ID,
          CUR_CODIGO: curso.CUR_CODIGO || 'N/A',
          CUR_DESCRIPCION: curso.CUR_DESCRIPCION || 'N/A',
          CUR_FECHA_HORA: curso.CUR_FECHA_HORA ? String(curso.CUR_FECHA_HORA).split(' ')[0] : 'N/A',
          CUR_LUGAR: curso.CUR_LUGAR || 'N/A',
          CUR_ESTADO: getEstadoDisplay(curso.CUR_ESTADO),
          CUR_ESTADO_NUM: curso.CUR_ESTADO,
          inscripciones: inscripciones,
          acreditaciones: acreditados,
          pendientesPago: pendientesPago
        }
      })

      if (cursoSeleccionado.value !== 'todos' && cursoSeleccionado.value) {
        cursosData = cursosData.filter(curso => curso.CUR_ID == cursoSeleccionado.value)
      }

      return cursosData
    })

    // Computed: coordinadores
    const coordinadores = computed(() => {
      return cursoCoordinadores.value.map(coord => {
        const persona = personas.value.find(p => p.PER_ID === coord.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === coord.CUR_ID)
        return {
          CUC_ID: coord.CUC_ID,
          nombre: persona ? `${persona.PER_NOMBRES || ''} ${persona.PER_APELPAT || ''}`.trim() : 'N/A',
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
          contacto: persona ? persona.PER_EMAIL || 'N/A' : 'N/A',
          cargo: coord.CUC_CARGO || 'N/A',
          estadoDisplay: '● Activo'
        }
      })
    })

    // Computed: formadores
    const formadores = computed(() => {
      return cursoFormadores.value.map(form => {
        const persona = personas.value.find(p => p.PER_ID === form.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === form.CUR_ID)
        return {
          CUO_ID: form.CUO_ID,
          nombre: persona ? `${persona.PER_NOMBRES || ''} ${persona.PER_APELPAT || ''}`.trim() : 'N/A',
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
          contacto: persona ? persona.PER_EMAIL || 'N/A' : 'N/A',
          tipo: form.CUO_DIRECTOR ? 'Director' : 'Formador',
          estadoDisplay: '● Activo'
        }
      })
    })

    // Configuración de columnas
    const columnasCursos = [
      { key: 'CUR_CODIGO', label: 'Código', sortable: true },
      { key: 'CUR_DESCRIPCION', label: 'Descripción', sortable: true },
      { key: 'CUR_FECHA_HORA', label: 'Fecha', sortable: true },
      { key: 'CUR_LUGAR', label: 'Lugar', sortable: true },
      { key: 'CUR_ESTADO', label: 'Estado', sortable: true },
      { key: 'inscripciones', label: 'Inscripciones', sortable: true },
      { key: 'acreditaciones', label: 'Acreditados', sortable: true },
      { key: 'pendientesPago', label: 'Pendientes Pago', sortable: true }
    ]

    // Tabs
    const tabs = ref([
      { id: 'coordinadores', label: 'Coordinadores' },
      { id: 'formadores', label: 'Formadores' }
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

    const getSemaphoreClass = (cursoId) => {
      if (cursoId === 'todos' || !cursoId) return 'semaphore-gray'
      
      const curso = cursos.value.find(c => c.CUR_ID == cursoId)
      if (!curso) return 'semaphore-gray'
      
      switch(curso.CUR_ESTADO) {
        case 1: return 'semaphore-green'
        case 2: return 'semaphore-yellow'
        case 3: return 'semaphore-red'
        default: return 'semaphore-gray'
      }
    }

    // Métodos de navegación
    const verCurso = (curso) => {
      router.push(`/cursos/detalle/${curso.CUR_ID}`)
    }

    const editarCurso = (curso) => {
      router.push(`/cursos/editar/${curso.CUR_ID}`)
    }

    // Función para cargar datos desde la API
    const cargarDatosDesdeAPI = async () => {
      try {
        console.log('Cargando datos desde API para base de datos SSB...')
        
        // Cargar cursos
        try {
          const cursosData = await cursosService.cursos.list()
          if (cursosData && Array.isArray(cursosData)) {
            cursos.value = cursosData
            console.log(`✓ Cursos cargados desde SSB: ${cursosData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando cursos desde SSB:', e.message)
          throw new Error(`No se pudieron cargar los cursos: ${e.message}`)
        }
        
        // Cargar personas
        try {
          const personasData = await personasService.personas.list()
          if (personasData && Array.isArray(personasData)) {
            personas.value = personasData
            console.log(`✓ Personas cargadas desde SSB: ${personasData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando personas desde SSB:', e.message)
        }
        
        // Cargar inscripciones
        try {
          const personasCursoData = await personasService.personaCursos.list()
          if (personasCursoData && Array.isArray(personasCursoData)) {
            personasCurso.value = personasCursoData
            console.log(`✓ Inscripciones cargadas desde SSB: ${personasCursoData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando inscripciones desde SSB:', e.message)
        }
        
        // Cargar pagos
        try {
          const pagosData = await pagosService.pagoPersona.list()
          if (pagosData && Array.isArray(pagosData)) {
            pagosPersona.value = pagosData
            console.log(`✓ Pagos cargados desde SSB: ${pagosData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando pagos desde SSB:', e.message)
        }
        
        // Cargar coordinadores
        try {
          const coordinadoresData = await cursosService.coordinadores.list()
          if (coordinadoresData && Array.isArray(coordinadoresData)) {
            cursoCoordinadores.value = coordinadoresData
            console.log(`✓ Coordinadores cargados desde SSB: ${coordinadoresData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando coordinadores desde SSB:', e.message)
        }
        
        // Cargar formadores
        try {
          const formadoresData = await cursosService.formadores.list()
          if (formadoresData && Array.isArray(formadoresData)) {
            cursoFormadores.value = formadoresData
            console.log(`✓ Formadores cargados desde SSB: ${formadoresData.length}`)
          }
        } catch (e) {
          console.warn('Error cargando formadores desde SSB:', e.message)
        }
        
        console.log('✓ Carga de datos desde SSB completada')
      } catch (error) {
        console.error('Error general cargando datos desde SSB:', error)
        throw error
      }
    }

    // Actualizar datos
    const actualizarDatos = async () => {
      loading.value = true
      try {
        await cargarDatosDesdeAPI()
        alertas.value.push({
          id: Date.now(),
          type: 'success',
          title: 'Datos Actualizados desde SSB',
          message: 'La información se actualizó correctamente desde la base de datos SSB.'
        })
      } catch (error) {
        console.error('Error actualizando datos desde SSB:', error.message)
        alertas.value.push({
          id: Date.now(),
          type: 'error',
          title: 'Error al Actualizar desde SSB',
          message: `No se pudieron actualizar los datos desde la base de datos SSB: ${error.message}`
        })
      } finally {
        loading.value = false
      }
    }

    const removerAlerta = (id) => {
      alertas.value = alertas.value.filter(alerta => alerta.id !== id)
    }

    // Ciclo de vida
    onMounted(async () => {
      loading.value = true
      try {
        await cargarDatosDesdeAPI()
        console.log('✓ Dashboard cargado correctamente desde SSB')
      } catch (error) {
        console.error('Error cargando dashboard desde SSB:', error)
        alertas.value.push({
          id: Date.now(),
          type: 'warning',
          title: 'Datos No Disponibles desde SSB',
          message: 'No se pudieron cargar los datos desde la base de datos SSB. Verifique la conexión.'
        })
      } finally {
        loading.value = false
      }
    })

    return {
      cursoSeleccionado,
      alertas,
      loading,
      activeTab,
      tabs,
      cursoSeleccionadoInfo,
      personasInscritas,
      pagosPendientesCurso,
      acreditadosCurso,
      inscripcionesRecientes,
      porcentajeInscritos,
      porcentajeAcreditados,
      pagosPagadosCurso,
      cursosFiltrados,
      coordinadores,
      formadores,
      columnasCursos,
      verCurso,
      editarCurso,
      actualizarDatos,
      removerAlerta,
      getEstadoDisplay,
      getSemaphoreClass,
      cursos,
      personas
    }
  }
}
</script>

<style scoped>
/* (Mantener los mismos estilos del archivo original) */
.dashboard-scout {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-content {
  margin-left: 0;
  padding: 20px;
  min-height: 100vh;
  width: 100%;
}

/* Selector de Curso */
.course-selector-section {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.selector-container {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.native-select-wrapper {
  flex: 1;
  min-width: 320px;
  max-width: 500px;
}

.native-select-label {
  display: block;
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.native-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  background-color: var(--color-surface);
  color: #495057;
  font-size: 16px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.native-select:focus {
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.2);
}

.native-select option {
  color: #495057;
  background-color: var(--color-surface);
  padding: 12px;
  font-size: 15px;
  border-bottom: 1px solid #f3f4f6;
}

.native-select option:hover {
  background-color: #2c5aa0 !important;
  color: #ffffff !important;
}

.native-select option:checked {
  background-color: #2c5aa0 !important;
  color: #ffffff !important;
}

/* Asegurar visibilidad en todos los navegadores */
.native-select::-ms-expand {
  display: block;
}

.native-select:-moz-focusring {
  color: transparent;
  text-shadow: 0 0 0 #000;
}

.semaphore-container {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.semaphore {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #ddd;
  transition: all 0.3s ease;
}

.semaphore-green {
  background-color: #28a745;
  border-color: #28a745;
  box-shadow: 0 0 12px rgba(40, 167, 69, 0.4);
}

.semaphore-yellow {
  background-color: #ffc107;
  border-color: #ffc107;
  box-shadow: 0 0 12px rgba(255, 193, 7, 0.4);
}

.semaphore-red {
  background-color: #dc3545;
  border-color: #dc3545;
  box-shadow: 0 0 12px rgba(220, 53, 69, 0.4);
}

.semaphore-gray {
  background-color: #6c757d;
  border-color: #6c757d;
}

.semaphore-label {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

/* Charts Section */
.charts-section {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.charts-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c5aa0;
  font-size: 1.5rem;
  font-weight: 600;
  border-bottom: 3px solid #2c5aa0;
  padding-bottom: 8px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.chart-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.chart-card h4 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c5aa0;
  font-size: 1.1rem;
  font-weight: 600;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-surface);
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: 40px;
  height: 150px;
}

.bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.bar {
  width: 50px;
  border-radius: 6px 6px 0 0;
  transition: height 0.5s ease;
  min-height: 20px;
}

.bar.inscritos {
  background: linear-gradient(135deg, #2c5aa0 0%, #1e3a8a 100%);
}

.bar.acreditados {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

.bar-container span {
  font-size: 14px;
  font-weight: 500;
  color: #495057;
  text-align: center;
}

.payment-status {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.dot.paid {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

.dot.pending {
  background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
}

/* Courses Section */
.courses-section {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #2c5aa0;
  font-size: 1.5rem;
  font-weight: 600;
  border-bottom: 3px solid #2c5aa0;
  padding-bottom: 8px;
}

.refresh-btn {
  background: #2c5aa0;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  background: #1e3d73;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Tablas */
.table-container-expanded {
  background: var(--color-surface);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
  box-sizing: border-box;
}

.data-table-expanded thead {
  background: #f8f9fa;
}

.data-table-expanded th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c5aa0;
  border-bottom: 2px solid #e1e5e9;
}

.data-table-expanded td {
  padding: 14px 12px;
  border-bottom: 1px solid #e1e5e9;
}

.data-table-expanded tr:hover {
  background: #f8f9fa;
}

/* Botones de Acción */
.actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-action {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-view {
  background: #e3f2fd;
  color: #1565c0;
}

.btn-edit {
  background: #fff3cd;
  color: #856404;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Responsables Section */
.responsibles-section {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.responsibles-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c5aa0;
  font-size: 1.5rem;
  font-weight: 600;
  border-bottom: 3px solid #2c5aa0;
  padding-bottom: 8px;
}

.tabs-container {
  border: 1px solid #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.tabs-header {
  display: flex;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #e9ecef;
}

.tab-button {
  padding: 16px 24px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: #6c757d;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  flex: 1;
  text-align: center;
  font-size: 14px;
}

.tab-button:hover {
  background-color: rgba(44, 90, 160, 0.1);
  color: #2c5aa0;
}

.tab-button.active {
  background-color: var(--color-surface);
  color: #2c5aa0;
  border-bottom-color: #ffcc00;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.tab-content {
  padding: 20px;
  background: var(--color-surface);
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .selector-container {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .refresh-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .course-selector-section,
  .charts-section,
  .courses-section,
  .responsibles-section {
    padding: 16px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-bars {
    flex-direction: column;
    align-items: center;
    height: auto;
    gap: 20px;
  }
  
  .bar-container {
    flex-direction: row;
    align-items: center;
    gap: 12px;
  }
  
  .bar {
    width: 60px;
    height: 40px !important;
    border-radius: 6px;
  }
  
  .payment-status {
    gap: 16px;
  }
  
  .status-item {
    justify-content: center;
  }
}

/* Estilos para estados de deshabilitado */
.native-select:disabled {
  background-color: #e9ecef;
  opacity: 0.6;
  cursor: not-allowed;
}

/* Transiciones suaves para todos los elementos */
.course-selector-section,
.charts-section,
.courses-section,
.responsibles-section,
.chart-card,
.tab-button,
.refresh-btn,
.btn-action {
  transition: all 0.3s ease-in-out;
}

/* Efectos de hover para todas las tarjetas */
.course-selector-section:hover,
.charts-section:hover,
.courses-section:hover,
.responsibles-section:hover {
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

/* Colores del sistema estandarizados */
:root {
  --color-primary: #2c5aa0;
  --color-primary-dark: #1e3a8a;
  --color-accent: #ffcc00;
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-danger: #dc3545;
  /* Use global --color-surface from base.css for consistent surface color */
  --color-border: #e9ecef;
  --color-text: #495057;
}
</style>