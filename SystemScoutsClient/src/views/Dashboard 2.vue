<template>
  <div class="dashboard-scout">
    <!-- Contenido Principal -->
    <main class="main-content">
      <!-- Selector de Curso con Semáforo - VERSIÓN ESTANDARIZADA -->
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
              <option value="1">CM-LS-2024 - Curso Medio - Liderazgo Scout</option>
              <option value="2">PA-T-2024 - Primeros Auxilios en Terreno</option>
              <option value="3">EA-S-2024 - Educación Ambiental Scout</option>
              <option value="4">CM-LS-2023 - Curso Medio - Liderazgo Scout (Edición Anterior)</option>
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

      <!-- Tabla de Cursos con Acciones - ESTILOS ESTANDARIZADOS -->
      <section class="courses-section">
        <div class="section-header">
          <h3>Cursos Vigentes</h3>
          <button 
            @click="actualizarDatos" 
            class="refresh-btn"
          >
            🔄 Actualizar
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
                  <button class="btn-action btn-activate" @click="activarCurso(curso)">✅ Activar</button>
                  <button class="btn-action btn-anular" @click="anularCurso(curso)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Tabla de Responsables de Cursos - ESTILOS ESTANDARIZADOS CON ACCIONES -->
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
                    <th v-for="col in columnasCoordinadores" :key="col.key">{{ col.label }}</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="coord in coordinadores" :key="coord.CUC_ID">
                    <td>{{ coord.nombre }}</td>
                    <td>{{ coord.curso }}</td>
                    <td>{{ coord.cargo }}</td>
                    <td>{{ coord.contacto }}</td>
                    <td>{{ coord.estadoDisplay }}</td>
                    <td class="actions">
                      <button class="btn-action btn-view" @click="verResponsable('coordinador', coord)">👁 Ver</button>
                      <button class="btn-action btn-edit" @click="editarResponsable('coordinador', coord)">✏ Editar</button>
                      <button class="btn-action btn-anular" @click="anularResponsable('coordinador', coord)">🚫 Anular</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Formadores -->
            <div v-if="activeTab === 'formadores'" class="table-container-expanded">
              <table class="data-table-expanded">
                <thead>
                  <tr>
                    <th v-for="col in columnasFormadores" :key="col.key">{{ col.label }}</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="form in formadores" :key="form.CUO_ID">
                    <td>{{ form.nombre }}</td>
                    <td>{{ form.curso }}</td>
                    <td>{{ form.tipo }}</td>
                    <td>{{ form.contacto }}</td>
                    <td>{{ form.estadoDisplay }}</td>
                    <td class="actions">
                      <button class="btn-action btn-view" @click="verResponsable('formador', form)">👁 Ver</button>
                      <button class="btn-action btn-edit" @click="editarResponsable('formador', form)">✏ Editar</button>
                      <button class="btn-action btn-anular" @click="anularResponsable('formador', form)">🚫 Anular</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Directores -->
            <div v-if="activeTab === 'directores'" class="table-container-expanded">
              <table class="data-table-expanded">
                <thead>
                  <tr>
                    <th v-for="col in columnasDirectores" :key="col.key">{{ col.label }}</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="dir in directores" :key="dir.CUO_ID">
                    <td>{{ dir.nombre }}</td>
                    <td>{{ dir.curso }}</td>
                    <td>{{ dir.contacto }}</td>
                    <td>{{ dir.estadoDisplay }}</td>
                    <td class="actions">
                      <button class="btn-action btn-view" @click="verResponsable('director', dir)">👁 Ver</button>
                      <button class="btn-action btn-edit" @click="editarResponsable('director', dir)">✏ Editar</button>
                      <button class="btn-action btn-anular" @click="anularResponsable('director', dir)">🚫 Anular</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Alimentación -->
            <div v-if="activeTab === 'alimentacion'" class="table-container-expanded">
              <table class="data-table-expanded">
                <thead>
                  <tr>
                    <th v-for="col in columnasAlimentacion" :key="col.key">{{ col.label }}</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="alim in responsablesAlimentacion" :key="alim.CUA_ID">
                    <td>{{ alim.nombre }}</td>
                    <td>{{ alim.curso }}</td>
                    <td>{{ alim.descripcion }}</td>
                    <td>{{ alim.contacto }}</td>
                    <td>{{ alim.estadoDisplay }}</td>
                    <td class="actions">
                      <button class="btn-action btn-view" @click="verResponsable('alimentacion', alim)">👁 Ver</button>
                      <button class="btn-action btn-edit" @click="editarResponsable('alimentacion', alim)">✏ Editar</button>
                      <button class="btn-action btn-anular" @click="anularResponsable('alimentacion', alim)">🚫 Anular</button>
                    </td>
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
import BaseButton from '@/components/BaseButton.vue'
import DataCard from '@/components/DataCard.vue'

export default {
  name: 'DashboardScout',
  
  components: {
    BaseAlert,
    BaseButton,
    DataCard
  },
  
  setup() {
    const router = useRouter()
    
    // Estado reactivo
    const cursoSeleccionado = ref('todos')
    const alertas = ref([])
    const loading = ref(false)
    const activeTab = ref('coordinadores')

    // Datos de ejemplo basados en los cursos reales de pre-inscripción
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
      },
      { 
        PER_ID: 3, 
        PER_RUN: 34567890, 
        PER_DV: '1', 
        PER_APELPAT: 'Martínez', 
        PER_APELMAT: 'Silva', 
        PER_NOMBRES: 'Carlos Alberto', 
        PER_EMAIL: 'carlos@email.com', 
        PER_FECHA_NAC: '1992-11-30',
        PER_FONO: '+56934567890',
        PER_VIGENTE: true
      },
      { 
        PER_ID: 4, 
        PER_RUN: 45678901, 
        PER_DV: '2', 
        PER_APELPAT: 'Rodríguez', 
        PER_APELMAT: 'Fernández', 
        PER_NOMBRES: 'Ana Carolina', 
        PER_EMAIL: 'ana@email.com', 
        PER_FECHA_NAC: '1993-03-25',
        PER_FONO: '+56945678901',
        PER_VIGENTE: true
      },
      { 
        PER_ID: 5, 
        PER_RUN: 56789012, 
        PER_DV: '3', 
        PER_APELPAT: 'López', 
        PER_APELMAT: 'Morales', 
        PER_NOMBRES: 'Pedro Alejandro', 
        PER_EMAIL: 'pedro@email.com', 
        PER_FECHA_NAC: '1988-07-12',
        PER_FONO: '+56956789012',
        PER_VIGENTE: true
      }
    ])

    // Cursos reales de pre-inscripción con diferentes estados para probar el semáforo
    const cursos = ref([
      { 
        CUR_ID: 1,
        CUR_CODIGO: 'CM-LS-2024',
        CUR_DESCRIPCION: 'Curso Medio - Liderazgo Scout',
        CUR_FECHA_HORA: '2024-03-15 09:00:00',
        CUR_LUGAR: 'Campamento Regional Biobío',
        CUR_ESTADO: 1, // Activo - Semáforo VERDE
        CUR_CUOTA_CON_ALMUERZO: 85000,
        CUR_CUOTA_SIN_ALMUERZO: 60000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 1
      },
      { 
        CUR_ID: 2,
        CUR_CODIGO: 'PA-T-2024',
        CUR_DESCRIPCION: 'Primeros Auxilios en Terreno',
        CUR_FECHA_HORA: '2024-03-22 08:30:00',
        CUR_LUGAR: 'Centro de Formación Scout',
        CUR_ESTADO: 1, // Activo - Semáforo VERDE
        CUR_CUOTA_CON_ALMUERZO: 75000,
        CUR_CUOTA_SIN_ALMUERZO: 50000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 2
      },
      { 
        CUR_ID: 3,
        CUR_CODIGO: 'EA-S-2024',
        CUR_DESCRIPCION: 'Educación Ambiental Scout',
        CUR_FECHA_HORA: '2024-02-10 10:00:00',
        CUR_LUGAR: 'Reserva Natural Nonguén',
        CUR_ESTADO: 2, // Finalizado - Semáforo AMARILLO
        CUR_CUOTA_CON_ALMUERZO: 65000,
        CUR_CUOTA_SIN_ALMUERZO: 45000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 3
      },
      { 
        CUR_ID: 4,
        CUR_CODIGO: 'CM-LS-2023',
        CUR_DESCRIPCION: 'Curso Medio - Liderazgo Scout (Edición Anterior)',
        CUR_FECHA_HORA: '2023-11-05 09:00:00',
        CUR_LUGAR: 'Campamento Regional',
        CUR_ESTADO: 3, // Cancelado - Semáforo ROJO
        CUR_CUOTA_CON_ALMUERZO: 80000,
        CUR_CUOTA_SIN_ALMUERZO: 55000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 1
      }
    ])

    const personasCurso = ref([
      // Curso Medio - Liderazgo Scout (CUR_ID: 1)
      { PEC_ID: 1, PER_ID: 1, CUR_ID: 1, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 2, PER_ID: 2, CUR_ID: 1, PEC_ACREDITADO: false, PEC_REGISTRO: true },
      { PEC_ID: 3, PER_ID: 3, CUR_ID: 1, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      
      // Primeros Auxilios en Terreno (CUR_ID: 2)
      { PEC_ID: 4, PER_ID: 4, CUR_ID: 2, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 5, PER_ID: 5, CUR_ID: 2, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      
      // Educación Ambiental Scout (CUR_ID: 3)
      { PEC_ID: 6, PER_ID: 1, CUR_ID: 3, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 7, PER_ID: 3, CUR_ID: 3, PEC_ACREDITADO: true, PEC_REGISTRO: true },
      { PEC_ID: 8, PER_ID: 5, CUR_ID: 3, PEC_ACREDITADO: true, PEC_REGISTRO: true }
    ])

    const pagosPersona = ref([
      // Curso Medio - Liderazgo Scout
      { PAP_ID: 1, PER_ID: 1, CUR_ID: 1, PAP_VALOR: 85000, PAP_ESTADO: 1 }, // Pagado
      { PAP_ID: 2, PER_ID: 2, CUR_ID: 1, PAP_VALOR: 85000, PAP_ESTADO: 2 }, // Pendiente
      { PAP_ID: 3, PER_ID: 3, CUR_ID: 1, PAP_VALOR: 85000, PAP_ESTADO: 1 }, // Pagado
      
      // Primeros Auxilios en Terreno
      { PAP_ID: 4, PER_ID: 4, CUR_ID: 2, PAP_VALOR: 75000, PAP_ESTADO: 1 }, // Pagado
      { PAP_ID: 5, PER_ID: 5, CUR_ID: 2, PAP_VALOR: 75000, PAP_ESTADO: 1 }, // Pagado
      
      // Educación Ambiental Scout
      { PAP_ID: 6, PER_ID: 1, CUR_ID: 3, PAP_VALOR: 65000, PAP_ESTADO: 1 }, // Pagado
      { PAP_ID: 7, PER_ID: 3, CUR_ID: 3, PAP_VALOR: 65000, PAP_ESTADO: 1 }, // Pagado
      { PAP_ID: 8, PER_ID: 5, CUR_ID: 3, PAP_VALOR: 65000, PAP_ESTADO: 1 }  // Pagado
    ])

    // Datos de responsables según estructura CURSO_COORDINADOR, CURSO_FORMADOR
    const cursoCoordinadores = ref([
      { CUC_ID: 1, CUR_ID: 1, PER_ID: 1, CAR_ID: 1, CUC_CARGO: 'Coordinador General' },
      { CUC_ID: 2, CUR_ID: 2, PER_ID: 2, CAR_ID: 2, CUC_CARGO: 'Coordinador Logística' },
      { CUC_ID: 3, CUR_ID: 3, PER_ID: 3, CAR_ID: 1, CUC_CARGO: 'Coordinador Ambiental' }
    ])

    const cursoFormadores = ref([
      { CUO_ID: 1, CUR_ID: 1, PER_ID: 2, ROL_ID: 1, CUO_DIRECTOR: false },
      { CUO_ID: 2, CUR_ID: 2, PER_ID: 3, ROL_ID: 1, CUO_DIRECTOR: false },
      { CUO_ID: 3, CUR_ID: 3, PER_ID: 4, ROL_ID: 1, CUO_DIRECTOR: false }
    ])

    const cursoDirectores = ref([
      { CUO_ID: 4, CUR_ID: 1, PER_ID: 1, ROL_ID: 2, CUO_DIRECTOR: true },
      { CUO_ID: 5, CUR_ID: 2, PER_ID: 2, ROL_ID: 2, CUO_DIRECTOR: true },
      { CUO_ID: 6, CUR_ID: 3, PER_ID: 3, ROL_ID: 2, CUO_DIRECTOR: true }
    ])

    const cursoAlimentacion = ref([
      { CUA_ID: 1, CUR_ID: 1, ALI_ID: 1, CUA_DESCRIPCION: 'Almuerzo tipo scout' },
      { CUA_ID: 2, CUR_ID: 2, ALI_ID: 2, CUA_DESCRIPCION: 'Desayuno energético' },
      { CUA_ID: 3, CUR_ID: 3, ALI_ID: 3, CUA_DESCRIPCION: 'Comida campamento ecológico' }
    ])

    // Computed properties
    const cursoSeleccionadoInfo = computed(() => {
      if (cursoSeleccionado.value === 'todos') return null
      return cursos.value.find(c => c.CUR_ID == cursoSeleccionado.value)
    })

    const personasInscritas = computed(() => {
      if (cursoSeleccionado.value === 'todos') {
        return personasCurso.value.length
      }
      return personasCurso.value.filter(pc => pc.CUR_ID == cursoSeleccionado.value).length
    })

    const pagosPendientesCurso = computed(() => {
      if (cursoSeleccionado.value === 'todos') {
        return pagosPersona.value.filter(p => p.PAP_ESTADO === 2).length
      }
      return pagosPersona.value.filter(p => 
        p.CUR_ID == cursoSeleccionado.value && p.PAP_ESTADO === 2
      ).length
    })

    const acreditadosCurso = computed(() => {
      if (cursoSeleccionado.value === 'todos') {
        return personasCurso.value.filter(pc => pc.PEC_ACREDITADO).length
      }
      return personasCurso.value.filter(pc => 
        pc.CUR_ID == cursoSeleccionado.value && pc.PEC_ACREDITADO
      ).length
    })

    const inscripcionesRecientes = computed(() => {
      // Simular inscripciones de los últimos 7 días para cursos activos
      return personasCurso.value.filter(pc => {
        const curso = cursos.value.find(c => c.CUR_ID === pc.CUR_ID)
        return curso && curso.CUR_ESTADO === 1
      }).length
    })

    const porcentajeInscritos = computed(() => {
      const total = personasInscritas.value
      return total > 0 ? 100 : 0
    })

    const porcentajeAcreditados = computed(() => {
      const total = personasInscritas.value
      const acreditados = acreditadosCurso.value
      return total > 0 ? (acreditados / total) * 100 : 0
    })

    const pagosPagadosCurso = computed(() => {
      if (cursoSeleccionado.value === 'todos') {
        return pagosPersona.value.filter(p => p.PAP_ESTADO === 1).length
      }
      return pagosPersona.value.filter(p => 
        p.CUR_ID == cursoSeleccionado.value && p.PAP_ESTADO === 1
      ).length
    })

    const cursosFiltrados = computed(() => {
      let cursosData = cursos.value.map(curso => {
        const inscripciones = personasCurso.value.filter(pc => pc.CUR_ID === curso.CUR_ID).length
        const acreditados = personasCurso.value.filter(pc => 
          pc.CUR_ID === curso.CUR_ID && pc.PEC_ACREDITADO
        ).length
        const pagosCurso = pagosPersona.value.filter(p => p.CUR_ID === curso.CUR_ID)
        const pendientesPago = pagosCurso.filter(p => p.PAP_ESTADO === 2).length

        return {
          CUR_ID: curso.CUR_ID,
          CUR_CODIGO: curso.CUR_CODIGO,
          CUR_DESCRIPCION: curso.CUR_DESCRIPCION,
          CUR_FECHA_HORA: curso.CUR_FECHA_HORA.split(' ')[0],
          CUR_LUGAR: curso.CUR_LUGAR,
          CUR_ESTADO: getEstadoDisplay(curso.CUR_ESTADO),
          CUR_ESTADO_NUM: curso.CUR_ESTADO,
          inscripciones: inscripciones,
          acreditaciones: acreditados,
          pendientesPago: pendientesPago
        }
      })

      if (cursoSeleccionado.value !== 'todos') {
        cursosData = cursosData.filter(curso => curso.CUR_ID == cursoSeleccionado.value)
      }

      return cursosData
    })

    // Computed properties para responsables
    const coordinadores = computed(() => {
      return cursoCoordinadores.value.map(coord => {
        const persona = personas.value.find(p => p.PER_ID === coord.PER_ID)
        const curso = cursos.value.find(c => c.CUR_ID === coord.CUR_ID)
        return {
          CUC_ID: coord.CUC_ID,
          nombre: persona ? `${persona.PER_NOMBRES} ${persona.PER_APELPAT}` : 'N/A',
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
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
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
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
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
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
          nombre: 'Responsable de Alimentación',
          curso: curso ? `${curso.CUR_CODIGO} - ${curso.CUR_DESCRIPCION}` : 'N/A',
          contacto: 'alimentacion@scoutsbiobio.cl',
          descripcion: alim.CUA_DESCRIPCION,
          estadoDisplay: '● Activo'
        }
      })
    })

    // Configuración de columnas para cursos
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

    // Configuración de columnas para responsables
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

    const getSemaphoreClass = (cursoId) => {
      if (cursoId === 'todos') return 'semaphore-gray'
      
      const curso = cursos.value.find(c => c.CUR_ID == cursoId)
      if (!curso) return 'semaphore-gray'
      
      switch(curso.CUR_ESTADO) {
        case 1: return 'semaphore-green'
        case 2: return 'semaphore-yellow'
        case 3: return 'semaphore-red'
        default: return 'semaphore-gray'
      }
    }

    // Métodos de acciones para cursos
    const verCurso = (curso) => {
      router.push(`/cursos/detalle/${curso.CUR_ID}`)
    }

    const editarCurso = (curso) => {
      router.push(`/cursos/editar/${curso.CUR_ID}`)
    }

    const activarCurso = (curso) => {
      loading.value = true
      setTimeout(() => {
        const cursoIndex = cursos.value.findIndex(c => c.CUR_ID === curso.CUR_ID)
        if (cursoIndex !== -1) {
          cursos.value[cursoIndex].CUR_ESTADO = 1
        }
        alertas.value.push({
          id: Date.now(),
          type: 'success',
          title: 'Curso Activado',
          message: `El curso ${curso.CUR_CODIGO} ha sido activado correctamente.`
        })
        loading.value = false
      }, 1000)
    }

    const anularCurso = (curso) => {
      if (confirm(`¿Está seguro que desea anular el curso ${curso.CUR_CODIGO}?`)) {
        loading.value = true
        setTimeout(() => {
          const cursoIndex = cursos.value.findIndex(c => c.CUR_ID === curso.CUR_ID)
          if (cursoIndex !== -1) {
            cursos.value[cursoIndex].CUR_ESTADO = 3
          }
          alertas.value.push({
            id: Date.now(),
            type: 'warning',
            title: 'Curso Anulado',
            message: `El curso ${curso.CUR_CODIGO} ha sido anulado.`
          })
          loading.value = false
        }, 1000)
      }
    }

    // Métodos de acciones para responsables
    const verResponsable = (tipo, responsable) => {
      alert(`Ver ${tipo}: ${responsable.nombre}`)
      // Aquí podrías redirigir o abrir un modal
    }

    const editarResponsable = (tipo, responsable) => {
      alert(`Editar ${tipo}: ${responsable.nombre}`)
      // Aquí podrías redirigir o abrir un modal
    }

    const anularResponsable = (tipo, responsable) => {
      if (confirm(`¿Está seguro que desea anular al ${tipo} ${responsable.nombre}?`)) {
        alertas.value.push({
          id: Date.now(),
          type: 'warning',
          title: `${tipo.charAt(0).toUpperCase() + tipo.slice(1)} Anulado`,
          message: `El ${tipo} ${responsable.nombre} ha sido anulado.`
        })
      }
    }

    const actualizarDatos = async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1500))
        alertas.value.push({
          id: Date.now(),
          type: 'info',
          title: 'Datos Actualizados',
          message: 'La información se ha actualizado correctamente.'
        })
      } catch (error) {
        alertas.value.push({
          id: Date.now(),
          type: 'error',
          title: 'Error',
          message: 'No se pudieron actualizar los datos.'
        })
      } finally {
        loading.value = false
      }
    }

    const removerAlerta = (id) => {
      alertas.value = alertas.value.filter(alerta => alerta.id !== id)
    }

    // Watch para cambios en el curso seleccionado
    watch(cursoSeleccionado, (newVal) => {
      console.log('Curso seleccionado:', newVal)
    })

    onMounted(async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('Dashboard cargado correctamente')
      } catch (error) {
        console.error('Error cargando datos del dashboard:', error)
        alertas.value.push({
          id: Date.now(),
          type: 'error',
          title: 'Error de Carga',
          message: 'No se pudieron cargar los datos del dashboard.'
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
      directores,
      responsablesAlimentacion,
      columnasCursos,
      columnasCoordinadores,
      columnasFormadores,
      columnasDirectores,
      columnasAlimentacion,
      verCurso,
      editarCurso,
      activarCurso,
      anularCurso,
      verResponsable,
      editarResponsable,
      anularResponsable,
      actualizarDatos,
      removerAlerta,
      getEstadoDisplay,
      getSemaphoreClass
    }
  }
}
</script>

<style scoped>
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

/* Selector de Curso - ESTILOS ESTANDARIZADOS */
.course-selector-section {
  background: white;
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

/* Estilos para el selector nativo estandarizado */
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
  background-color: #ffffff;
  color: #495057;
  font-size: 16px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.native-select:focus {
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.2);
}

.native-select option {
  color: #495057;
  background-color: #ffffff;
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

/* Stats Grid - ESTILOS ESTANDARIZADOS */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

/* Charts Section - ESTILOS ESTANDARIZADOS */
.charts-section {
  background: white;
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
  background-color: white;
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

/* Courses Section - ESTILOS ESTANDARIZADOS CON BOTONES MEJORADOS */
.courses-section {
  background: white;
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

/* BOTÓN ACTUALIZAR MEJORADO - ESTILOS DE MANTENEDORES */
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

.refresh-btn:hover {
  background: #1e3d73;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
}

/* TABLAS ESTANDARIZADAS - ESTILOS DE MANTENEDORES */
.table-container-expanded {
  background: white;
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

/* BOTONES DE ACCIÓN - ESTILOS DE MANTENEDORES */
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

.btn-activate {
  background: #d4edda;
  color: #155724;
}

.btn-anular {
  background: #f8d7da;
  color: #721c24;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Responsables Section - ESTILOS ESTANDARIZADOS CON TABS MEJORADOS */
.responsibles-section {
  background: white;
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

/* BOTONES DE TABS MEJORADOS - ESTILOS DE MANTENEDORES */
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
  background-color: white;
  color: #2c5aa0;
  border-bottom-color: #ffcc00;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.tab-content {
  padding: 20px;
  background: white;
}

/* Responsive - ESTILOS ESTANDARIZADOS */
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
  
  .native-select-wrapper {
    min-width: auto;
    max-width: none;
  }
  
  .native-select {
    font-size: 14px;
    padding: 10px 14px;
  }
  
  .semaphore-container {
    justify-content: center;
    padding: 16px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .refresh-btn {
    width: 100%;
    margin-top: 8px;
  }
  
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    width: 100%;
    text-align: left;
    padding: 14px 20px;
  }
  
  .chart-bars {
    gap: 20px;
  }
  
  .bar {
    width: 40px;
  }
  
  .actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .btn-action {
    justify-content: center;
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
  --color-surface: #f8f9fa;
  --color-border: #e9ecef;
  --color-text: #495057;
}
</style>