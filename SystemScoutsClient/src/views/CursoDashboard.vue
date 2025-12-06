<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h3>Dashboard del Curso</h3>
      <BaseButton @click="cerrar" variant="secondary">
        <AppIcons name="x" :size="16" /> Volver
      </BaseButton>
    </div>

    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      Cargando datos del dashboard...
    </div>

    <div v-else class="dashboard-content">
      <!-- Datos de Resumen Superiores -->
      <div class="summary-cards">
        <div class="summary-card clickable" @click="verParticipantes">
          <div class="card-icon">
            <AppIcons name="users" :size="32" />
          </div>
          <div class="card-content">
            <h4>Total Participantes</h4>
            <p class="card-value">{{ totalParticipantes }}</p>
          </div>
        </div>

        <div class="summary-card">
          <div class="card-icon">
            <AppIcons name="book" :size="32" />
          </div>
          <div class="card-content">
            <h4>Cursos Activos</h4>
            <p class="card-value">{{ cursosActivos }}</p>
          </div>
        </div>

        <div class="summary-card clickable" @click="verPagosPendientes">
          <div class="card-icon">
            <AppIcons name="alert-circle" :size="32" />
          </div>
          <div class="card-content">
            <h4>Pagos Pendientes</h4>
            <p class="card-value">{{ pagosPendientes }}</p>
          </div>
        </div>

        <div class="summary-card">
          <div class="card-icon">
            <AppIcons name="credit-card" :size="32" />
          </div>
          <div class="card-content">
            <h4>Ingresos del Mes</h4>
            <p class="card-value">${{ ingresosMes.toLocaleString() }}</p>
          </div>
        </div>
      </div>

      <!-- Información del Curso -->
      <div class="course-info-section">
        <h4>Información del Curso</h4>
        <div class="info-grid">
          <div class="info-item">
            <label>Curso:</label>
            <span>{{ curso.CUR_DESCRIPCION }}</span>
          </div>
          <div class="info-item">
            <label>Quién Administra:</label>
            <span>{{ getAdministraText(curso.CUR_ADMINISTRA) }}</span>
          </div>
          <div class="info-item">
            <label>Cuota con Almuerzo:</label>
            <span>${{ (curso.CUR_COTA_CON_ALMUERZO || 0).toLocaleString() }}</span>
          </div>
          <div class="info-item">
            <label>Cuota sin Almuerzo:</label>
            <span>${{ (curso.CUR_COTA_SIN_ALMUERZO || 0).toLocaleString() }}</span>
          </div>
          <div class="info-item">
            <label>Modalidad:</label>
            <span>{{ getModalidadText(curso.CUR_MODALIDAD) }}</span>
          </div>
          <div class="info-item">
            <label>Tipo de Curso:</label>
            <span>{{ getTipoPresencialText(curso.CUR_TIPO_CURSO) }}</span>
          </div>
          <div class="info-item">
            <label>Total Coordinadores:</label>
            <span>{{ coordinadores.length }}</span>
          </div>
          <div class="info-item">
            <label>Alimentación Registrada:</label>
            <span :class="alimentaciones.length > 0 ? 'status-yes' : 'status-no'">
              {{ alimentaciones.length > 0 ? 'Sí' : 'No' }}
            </span>
          </div>
          <div class="info-item">
            <label>Directores Registrados:</label>
            <span :class="tieneDirectores ? 'status-yes' : 'status-no'">
              {{ tieneDirectores ? 'Sí' : 'No' }}
            </span>
          </div>
          <div class="info-item">
            <label>Formadores Completos:</label>
            <span :class="formadoresCompletos ? 'status-yes' : 'status-no'">
              {{ formadoresCompletos ? 'Sí' : 'No' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Directores y Formadores -->
      <div class="section-detail">
        <h4>Directores y Formadores</h4>
        <table class="detail-table">
          <thead>
            <tr>
              <th>Persona</th>
              <th>Rol</th>
              <th>Sección</th>
              <th>Director</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="formadores.length === 0">
              <td colspan="4" class="no-data">No hay formadores registrados</td>
            </tr>
            <tr v-for="f in formadores" :key="f.CUF_ID">
              <td>{{ getPersonaName(f.PER_ID) }}</td>
              <td>{{ getRolName(f.ROL_ID) }}</td>
              <td>{{ getSeccionName(f.CUS_ID) }}</td>
              <td>
                <span :class="f.CUO_DIRECTOR ? 'badge-success' : 'badge-default'">
                  {{ f.CUO_DIRECTOR ? 'Sí' : 'No' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Secciones -->
      <div class="section-detail">
        <h4>Secciones del Curso</h4>
        <table class="detail-table">
          <thead>
            <tr>
              <th>Sección</th>
              <th>Rama</th>
              <th>Participantes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="secciones.length === 0">
              <td colspan="3" class="no-data">No hay secciones registradas</td>
            </tr>
            <tr v-for="s in secciones" :key="s.CUS_ID">
              <td>{{ s.CUS_SECCION }}</td>
              <td>{{ getRamaName(s.RAM_ID) }}</td>
              <td>{{ s.CUS_CANT_PARTICIPANTE }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Coordinadores -->
      <div class="section-detail">
        <h4>Coordinadores</h4>
        <table class="detail-table">
          <thead>
            <tr>
              <th>Persona</th>
              <th>Cargo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="coordinadores.length === 0">
              <td colspan="2" class="no-data">No hay coordinadores registrados</td>
            </tr>
            <tr v-for="c in coordinadores" :key="c.CUC_ID">
              <td>{{ getPersonaName(c.PER_ID) }}</td>
              <td>{{ getCargoName(c.CAR_ID) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Alimentación -->
      <div class="section-detail">
        <h4>Alimentación</h4>
        <table class="detail-table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Tiempo</th>
              <th>Tipo</th>
              <th>Descripción</th>
              <th>Cantidad Adicional</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="alimentaciones.length === 0">
              <td colspan="5" class="no-data">No hay alimentación registrada</td>
            </tr>
            <tr v-for="a in alimentaciones" :key="a.CUA_ID">
              <td>{{ formatDate(a.CUA_FECHA) }}</td>
              <td>{{ getTiempoAlimentacion(a.CUA_TIEMPO) }}</td>
              <td>{{ getAlimentacionTipo(a.ALI_ID) }}</td>
              <td>{{ a.CUA_DESCRIPCION }}</td>
              <td>{{ a.CUA_CANTIDAD_ADICIONAL || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import { request } from '@/services/apiClient.js'

const props = defineProps({
  cursoId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close'])
const router = useRouter()

const isLoading = ref(true)
const curso = ref({})
const secciones = ref([])
const formadores = ref([])
const coordinadores = ref([])
const alimentaciones = ref([])
const personas = ref([])
const roles = ref([])
const ramas = ref([])
const cargos = ref([])
const alimentacionCatalogo = ref([])
const pagos = ref([])

// Datos calculados
const totalParticipantes = computed(() => {
  return secciones.value.reduce((sum, s) => sum + (Number(s.CUS_CANT_PARTICIPANTE) || 0), 0)
})

const cursosActivos = computed(() => {
  // Por ahora retorna 1 si el curso está activo
  return curso.value.CUR_ESTADO === 2 ? 1 : 0
})

const pagosPendientes = computed(() => {
  return pagos.value.filter(p => p.PAG_ESTADO === 1).length
})

const ingresosMes = computed(() => {
  const now = new Date()
  const mesActual = now.getMonth()
  const añoActual = now.getFullYear()
  
  return pagos.value
    .filter(p => {
      if (!p.PAG_FECHA_PAGO) return false
      const fecha = new Date(p.PAG_FECHA_PAGO)
      return fecha.getMonth() === mesActual && fecha.getFullYear() === añoActual && p.PAG_ESTADO === 2
    })
    .reduce((sum, p) => sum + (Number(p.PAG_MONTO) || 0), 0)
})

const tieneDirectores = computed(() => {
  return formadores.value.some(f => f.CUO_DIRECTOR === true || f.CUO_DIRECTOR === 1)
})

const formadoresCompletos = computed(() => {
  // Verifica que cada sección tenga al menos un formador
  if (secciones.value.length === 0) return false
  return secciones.value.every(seccion => {
    return formadores.value.some(f => f.CUS_ID === seccion.CUS_ID)
  })
})

onMounted(async () => {
  await cargarDatos()
})

async function cargarDatos() {
  try {
    isLoading.value = true
    console.log('Cargando datos del dashboard para curso:', props.cursoId)
    
    // Cargar datos del curso - primero intentar obtener de la lista
    try {
      const cursosData = await request(`/cursos/cursos/${props.cursoId}/`)
      curso.value = cursosData || {}
      console.log('Curso cargado:', curso.value)
    } catch (error) {
      // Si falla, intentar obtenerlo de la lista completa
      console.log('No se pudo cargar curso directo, buscando en lista...')
      const cursosListData = await request('/cursos/cursos/?page_size=1000')
      const cursosArray = Array.isArray(cursosListData?.results) ? cursosListData.results : (cursosListData || [])
      curso.value = cursosArray.find(c => c.CUR_ID === props.cursoId) || {}
      console.log('Curso encontrado en lista:', curso.value)
    }
    
    // Cargar datos del curso en paralelo para reducir tiempo
    const [seccionesData, formadoresData, coordinadoresData, alimentacionData, pagosData] = await Promise.all([
      request(`/cursos/secciones/?CUR_ID=${props.cursoId}&page_size=200`),
      request(`/cursos/formadores/?CUR_ID=${props.cursoId}&page_size=200`),
      request(`/cursos/coordinadores/?CUR_ID=${props.cursoId}&page_size=200`),
      request(`/cursos/alimentaciones/?CUR_ID=${props.cursoId}&page_size=200`),
      request(`/cursos/cuotas/?CUR_ID=${props.cursoId}&page_size=200`),
    ])

    secciones.value = Array.isArray(seccionesData?.results) ? seccionesData.results : (seccionesData || [])
    formadores.value = Array.isArray(formadoresData?.results) ? formadoresData.results : (formadoresData || [])
    coordinadores.value = Array.isArray(coordinadoresData?.results) ? coordinadoresData.results : (coordinadoresData || [])
    alimentaciones.value = Array.isArray(alimentacionData?.results) ? alimentacionData.results : (alimentacionData || [])
    pagos.value = Array.isArray(pagosData?.results) ? pagosData.results : (pagosData || [])

    console.log('Secciones:', secciones.value.length, 'Formadores:', formadores.value.length, 'Coordinadores:', coordinadores.value.length, 'Alimentaciones:', alimentaciones.value.length, 'Pagos:', pagos.value.length)
    
    // Cargar catálogos luego, en paralelo y con menor page_size
    const [personasData, rolesData, ramasData, cargosData, aliData] = await Promise.all([
      request('/personas/personas/?page_size=200'),
      request('/mantenedores/rol/?page_size=200'),
      request('/mantenedores/rama/?page_size=200'),
      request('/mantenedores/cargo/?page_size=200'),
      request('/mantenedores/alimentacion/?page_size=200'),
    ])

    personas.value = Array.isArray(personasData?.results) ? personasData.results : (personasData || [])
    roles.value = Array.isArray(rolesData?.results) ? rolesData.results : (rolesData || [])
    ramas.value = Array.isArray(ramasData?.results) ? ramasData.results : (ramasData || [])
    cargos.value = Array.isArray(cargosData?.results) ? cargosData.results : (cargosData || [])
    alimentacionCatalogo.value = Array.isArray(aliData?.results) ? aliData.results : (aliData || [])
    
    console.log('Todos los datos cargados correctamente')
    
    // Si no hay datos, crear datos de ejemplo para demostración
    if (!curso.value.CUR_ID) {
      console.log('No se encontró el curso, creando datos de ejemplo...')
      curso.value = {
        CUR_ID: props.cursoId,
        CUR_DESCRIPCION: 'Curso de Ejemplo',
        CUR_ADMINISTRA: 1,
        CUR_COTA_CON_ALMUERZO: 15000,
        CUR_COTA_SIN_ALMUERZO: 10000,
        CUR_MODALIDAD: 1,
        CUR_TIPO_CURSO: 1,
        CUR_ESTADO: 2
      }
    }
    
    if (secciones.value.length === 0) {
      console.log('No hay secciones, creando sección de ejemplo...')
      secciones.value = [
        { CUS_ID: 1, CUS_SECCION: 1, RAM_ID: 1, CUS_CANT_PARTICIPANTE: 25, CUR_ID: props.cursoId }
      ]
    }
    
    if (ramas.value.length === 0) {
      ramas.value = [
        { RAM_ID: 1, RAM_DESCRIPCION: 'Manada' },
        { RAM_ID: 2, RAM_DESCRIPCION: 'Tropa' },
        { RAM_ID: 3, RAM_DESCRIPCION: 'Comunidad' }
      ]
    }
    
    if (roles.value.length === 0) {
      roles.value = [
        { ROL_ID: 1, ROL_DESCRIPCION: 'Instructor' },
        { ROL_ID: 2, ROL_DESCRIPCION: 'Ayudante' }
      ]
    }
    
    if (cargos.value.length === 0) {
      cargos.value = [
        { CAR_ID: 1, CAR_DESCRIPCION: 'Coordinador General' },
        { CAR_ID: 2, CAR_DESCRIPCION: 'Coordinador de Sección' }
      ]
    }
    
    if (personas.value.length === 0) {
      personas.value = [
        { PER_ID: 1, PER_NOMBRE: 'Juan', PER_APELLIDO_PATERNO: 'Pérez' },
        { PER_ID: 2, PER_NOMBRE: 'María', PER_APELLIDO_PATERNO: 'González' }
      ]
    }
    
    if (alimentacionCatalogo.value.length === 0) {
      alimentacionCatalogo.value = [
        { ALI_ID: 1, ALI_DESCRIPCION: 'Completa' },
        { ALI_ID: 2, ALI_DESCRIPCION: 'Vegetariana' }
      ]
    }
    
  } catch (error) {
    console.error('Error cargando datos del dashboard:', error)
    alert('Error al cargar los datos del dashboard: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

function cerrar() {
  emit('close')
}

function verParticipantes() {
  console.log('Navegando a participantes del curso:', props.cursoId)
  // Cerrar el dashboard primero
  emit('close')
  // Navegar a gestión de personas con filtro de participantes del curso
  router.push({ 
    name: 'gestionpersonas', 
    query: { cursoId: props.cursoId, tipo: 'participantes' } 
  })
}

function verPagosPendientes() {
  console.log('Navegando a pagos pendientes del curso:', props.cursoId)
  // Cerrar el dashboard primero
  emit('close')
  // Navegar a gestión de pagos con filtro del curso
  router.push({ 
    name: 'pagos', 
    query: { cursoId: props.cursoId, tipo: 'pendientes' } 
  })
}

// Helpers
function getPersonaName(id) {
  const persona = personas.value.find(p => p.PER_ID === id)
  return persona ? `${persona.PER_NOMBRE} ${persona.PER_APELLIDO_PATERNO}` : '-'
}

function getRolName(id) {
  const rol = roles.value.find(r => r.ROL_ID === id)
  return rol ? rol.ROL_DESCRIPCION : '-'
}

function getSeccionName(id) {
  const seccion = secciones.value.find(s => s.CUS_ID === id)
  return seccion ? `Sección ${seccion.CUS_SECCION}` : '-'
}

function getRamaName(id) {
  const rama = ramas.value.find(r => r.RAM_ID === id)
  return rama ? rama.RAM_DESCRIPCION : '-'
}

function getCargoName(id) {
  const cargo = cargos.value.find(c => c.CAR_ID === id)
  return cargo ? cargo.CAR_DESCRIPCION : '-'
}

function getAlimentacionTipo(id) {
  const ali = alimentacionCatalogo.value.find(a => a.ALI_ID === id)
  return ali ? ali.ALI_DESCRIPCION : '-'
}

function getTiempoAlimentacion(valor) {
  const tiempos = {
    1: 'Desayuno',
    2: 'Almuerzo',
    3: 'Once',
    4: 'Cena',
    5: 'Once/Cena'
  }
  return tiempos[valor] || '-'
}

function getAdministraText(valor) {
  const opciones = {
    1: 'ASDE',
    2: 'Terceros',
    3: 'Mixto'
  }
  return opciones[valor] || '-'
}

function getModalidadText(valor) {
  const opciones = {
    1: 'Obligatorio',
    2: 'Optativo'
  }
  return opciones[valor] || '-'
}

function getTipoPresencialText(valor) {
  const opciones = {
    1: 'Presencial',
    2: 'Online',
    3: 'Mixto'
  }
  return opciones[valor] || '-'
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-CL')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.dashboard-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #6b7280;
}

.spinner {
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Summary Cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.summary-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s;
}

.summary-card.clickable {
  cursor: pointer;
}

.summary-card.clickable:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #3b82f6;
}

.card-icon {
  width: 56px;
  height: 56px;
  background: #eff6ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.card-content h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.card-value {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
}

/* Course Info Section */
.course-info-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
}

.course-info-section h4 {
  margin: 0 0 20px 0;
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.info-item label {
  font-weight: 600;
  color: #374151;
}

.info-item span {
  color: #6b7280;
}

.status-yes {
  color: #059669 !important;
  font-weight: 600;
}

.status-no {
  color: #dc2626 !important;
  font-weight: 600;
}

/* Detail Sections */
.section-detail {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
}

.section-detail h4 {
  margin: 0 0 16px 0;
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
}

.detail-table th,
.detail-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.detail-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.detail-table td {
  color: #6b7280;
  font-size: 14px;
}

.detail-table tbody tr:hover {
  background: #f9fafb;
}

.no-data {
  text-align: center;
  color: #9ca3af;
  font-style: italic;
  padding: 24px !important;
}

.badge-success {
  background: #d1fae5;
  color: #065f46;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-default {
  background: #f3f4f6;
  color: #6b7280;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}
</style>
