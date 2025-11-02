<template>
  <div class="layout-root">
    <!-- Notificaciones de alertas -->
    <div class="toast-container">
      <div 
        v-for="(alert, index) in visibleAlerts" 
        :key="alert.id" 
        class="alert-toast"
      >
        <div class="alert-toast-icon"><AppIcons name="alert-circle" :size="20" /></div>
        <div class="alert-toast-content">
          <div class="alert-toast-title">{{ alert.title }}</div>
          <div class="alert-toast-message">{{ getAlertDescription(alert.type, alert.title) }}</div>
        </div>
        <button class="alert-toast-close" @click="closeAlert(alert.id)"><AppIcons name="x" :size="16" /></button>
      </div>
    </div>

    <div class="layout-content">
      <div class="main">
        <div class="control-panel">
          <div class="dashboard-content">
            <!-- Tabla centrada arriba -->
            <div class="table-section">
              <div class="table-container large">
                <table class="data-table large">
                  <thead>
                    <tr>
                      <th>Curso</th>
                      <th>Rama</th>
                      <th class="text-center">Formadores</th>
                      <th class="text-center">Coordinadores</th>
                      <th class="text-center">Directores</th>
                      <th class="text-center">Requeridos</th>
                      <th class="text-center">Estado</th>
                      <th class="text-right">Capacidad</th>
                      <th class="text-right">Esperado</th>
                      <th class="text-center">Alimentación</th>
                      <th class="text-center">Activo</th>
                      <th class="text-center">Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="curso in sortedCursos" :key="curso.id" :class="'row-' + getDirectivoStatus(curso)">
                      <td>
                        <div class="curso-name-wrapper">
                          <span class="curso-name">{{ curso.title }}</span>
                        </div>
                      </td>
                      <td>{{ curso.rama || (curso.ramas ? (Array.isArray(curso.ramas) ? curso.ramas.join(', ') : String(curso.ramas)) : '—') }}</td>
                      <td class="text-center">{{ getDirectivoCount(curso) }}</td>
                      <td class="text-center">{{ getCoordinadorCount(curso) }}</td>
                      <td class="text-center">{{ getDirectorCount(curso) }}</td>
                      <td class="text-center">{{ getDirectivoRequired(curso) }}</td>
                      <td class="text-center"><span :class="['status-badge', getDirectivoStatus(curso)]">{{ getDirectivoStatus(curso) === 'ok' ? 'OK' : (getDirectivoStatus(curso) === 'near' ? 'Casi' : 'Faltan') }}</span></td>
                      <td class="text-right">{{ curso.capacidad ?? '-' }}</td>
                      <td class="text-right">{{ fmtCurrency((pagosMap[curso.id] && pagosMap[curso.id].expected) || 0) }}</td>
                      <td class="text-center">{{ curso.alimentacion ? 'Sí' : 'No' }}</td>
                      <td class="text-center">{{ isCursoActive(curso) ? 'Activo' : 'Inactivo' }}</td>
                      <td class="text-center">{{ curso.estado || computeCourseState(curso) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Gráfico centrado abajo -->
            <div class="chart-card-full">
              <div class="chart-header">
                <h3>Pagos por Curso</h3>
                <p class="chart-description">Montos estimados vs. recibidos por curso</p>
              </div>
              <div class="column-chart">
                <div class="chart-axis">
                  <div v-for="tick in 5" :key="tick" class="axis-label">
                    {{ formatAxisLabel(chartMax * (5-tick) / 4) }}
                  </div>
                </div>
                <div class="chart-bars">
                  <div v-for="curso in chartData" :key="curso.id" class="bar-group">
                    <div class="bar-wrapper">
                      <div class="bar bar-expected" :style="{ height: barHeight(curso.expected) + 'px' }">
                        <span class="bar-value">{{ fmtCurrency(curso.expected) }}</span>
                      </div>
                      <div class="bar bar-received" :style="{ height: barHeight(curso.paid) + 'px' }">
                        <span class="bar-value">{{ fmtCurrency(curso.paid) }}</span>
                      </div>
                    </div>
                    <span class="bar-label">{{ curso.title }}</span>
                  </div>
                </div>
              </div>
              <div class="chart-legend">
                <div class="legend-item">
                  <span class="legend-color expected"></span>
                  <span>Monto Estimado</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color received"></span>
                  <span>Monto Recibido</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppIcons from '@/components/icons/AppIcons.vue'

const router = useRouter()

// State management
const showCursosModal = ref(false)
const cursosList = ref([])
const totalPersonas = ref(0)
const pagosSumByCourse = ref({})
const pagosCountPaidByCourse = ref({})
const directivosByCourse = ref({})
const coordinadoresByCourse = ref({})
const directoresByCourse = ref({})
const closedAlerts = ref([])

// Computed properties
const sortedCursos = computed(() =>
  [...cursosList.value].sort((a, b) => (a.title || '').localeCompare(b.title || '', 'es', { sensitivity: 'base' }))
)



function getAlertIcon(type) {
  const icons = { full: '🔴', near: '🟡', bajo: '🟢', 'formadores-low': '🚨' }
  return icons[type] || '⚠️'
}

function getAlertDescription(type, title) {
  if (type === 'full') return `El curso "${title}" ha alcanzado su capacidad máxima.`
  if (type === 'near') return `El curso "${title}" está cerca de completar su capacidad.`
  if (type === 'bajo') return `El curso "${title}" tiene baja inscripción.`
  if (type === 'formadores-low') return `El curso "${title}" tiene menos de 4 formadores asignados — se requieren más formadores.`
  return ''
}

function getSemaforoClass(indicator) {
  if (indicator === 'inscritos') {
    const ratio = kpi.value.totalInscritos / (sortedCursos.value.reduce((sum, c) => sum + c.capacidad, 0) || 1)
    if (ratio >= 0.85) return 'ok'
    if (ratio >= 0.5) return 'near'
    return 'full'
  }
  if (indicator === 'pagos') {
    const ratio = kpi.value.ingresosPagados / (kpi.value.ingresosProyectados || 1)
    if (ratio >= 0.8) return 'ok'
    if (ratio >= 0.5) return 'near'
    return 'full'
  }
  if (indicator === 'cursos') return kpi.value.totalCursos >= 3 ? 'ok' : 'near'
  if (indicator === 'alertas') {
    if (alerts.value.length === 0) return 'ok'
    if (alerts.value.length <= 2) return 'near'
    return 'full'
  }
  if (indicator === 'formadores') {
    // Overall semaforo for formadores:
    // - red (full) if any course has fewer than 4 formadores
    // - yellow (near) if any course has 4 or 5 formadores (and none <4)
    // - green (ok) only when all courses have at least 6 formadores
    const counts = sortedCursos.value.map(c => getDirectivoCount(c))
    if (counts.some(n => n < 4)) return 'full'
    if (counts.some(n => n < 6)) return 'near'
    return 'ok'
  }
  return 'ok'
}

// Computed properties for pagos
const pagosBars = computed(() => {
  return sortedCursos.value.map(c => {
    const valor = Number(c.valor || 0)
    const expected = Math.max(0, Math.round((Number(c.inscritos) || 0) * valor))
    const paidFromSum = pagosSumByCourse.value[c.id] || 0
    const paidFromCount = (pagosCountPaidByCourse.value[c.id] || 0) * valor
    const paid = paidFromSum || paidFromCount || 0
    const unpaid = Math.max(0, expected - paid)
    const percentPaid = expected > 0 ? Math.max(0, Math.min(100, Math.round((paid / expected) * 100))) : 0
    return { id: c.id, title: c.title, inscritos: c.inscritos, expected, paid, unpaid, percentPaid }
  })
})

const cursosConPagosPendientes = computed(() => {
  return pagosBars.value.filter(c => c.unpaid > 0).sort((a, b) => b.unpaid - a.unpaid)
})

// Helper map for quick lookup by curso id
const pagosMap = computed(() => {
  const m = {}
  pagosBars.value.forEach(p => { m[p.id] = p })
  return m
})

// Chart data: only cursos with expected amounts
const chartData = computed(() => pagosBars.value.filter(p => p.expected > 0))

const chartMin = 100000
const chartMax = computed(() => {
  const maxFromData = chartData.value.length ? Math.max(...chartData.value.map(d => Math.max(d.expected || 0, d.paid || 0))) : 0
  return Math.max(500000, maxFromData)
})

function barHeight(value) {
  const h = 320 // px chart height
  if (!value || value <= chartMin) return 0
  const max = chartMax.value || 500000
  return Math.round(((value - chartMin) / (max - chartMin)) * h)
}

// Format axis labels for the chart
function formatAxisLabel(value) {
  return value >= 1000000 ? `${(value / 1000000).toFixed(1)}M` : 
         value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value
}

function fmtCurrency(amount) {
  try {
    return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(Number(amount || 0))
  } catch (_) {
    return `$${Number(amount || 0).toLocaleString('es-CL')}`
  }
}

function getCoordinadorCount(curso) {
  return coordinadoresByCourse.value[curso.id] !== undefined ? coordinadoresByCourse.value[curso.id] : 0
}

function getDirectorCount(curso) {
  return directoresByCourse.value[curso.id] !== undefined ? directoresByCourse.value[curso.id] : 0
}

function isCursoActive(curso) {
  // Accept several possible flags used in different backends
  if (curso.activo === true || curso.active === true) return true
  if (typeof curso.estado === 'string') {
    const s = curso.estado.toLowerCase()
    return s.includes('act') || s.includes('activo')
  }
  return false
}

function computeCourseState(curso) {
  // Fallback state based on inscritos vs capacidad
  const cap = Number(curso.capacidad) || 0
  const ins = Number(curso.inscritos) || 0
  if (!cap) return 'Sin capacidad'
  const ratio = ins / cap
  if (ratio >= 1) return 'Completo'
  if (ratio >= 0.85) return 'Casi lleno'
  if (ratio <= 0.25) return 'Baja inscripción'
  return 'Abierto'
}

const kpi = computed(() => {
  const totalCursos = sortedCursos.value.length
  // Por ahora usamos el total de personas como "pre inscritos totales"
  const totalInscritos = Number(totalPersonas.value || 0)
  const ingresosProyectados = sortedCursos.value.reduce((sum, c) => sum + (Number(c.inscritos) || 0) * (Number(c.valor) || 0), 0)
  const ingresosPagados = pagosBars.value.reduce((sum, b) => sum + (Number(b.paid) || 0), 0)
  const ingresosPendientes = Math.max(0, ingresosProyectados - ingresosPagados)
  return { totalCursos, totalInscritos, ingresosProyectados, ingresosPagados, ingresosPendientes }
})









const alerts = computed(() => {
  const result = []

  // Add system error alerts
  if (errorState.value.message) {
    result.push({
      id: 'system-error',
      title: 'Error del Sistema',
      type: 'error',
      label: errorState.value.message
    })
  }

  // Add course-specific alerts
  sortedCursos.value.forEach(c => {
    const cap = Number(c.capacidad) || 0
    const ins = Number(c.inscritos) || 0
    
    if (cap) {
      const ratio = ins / cap
      if (ratio >= 1) {
        result.push({ 
          id: `${c.id}-full`, 
          title: c.title, 
          type: 'full', 
          label: 'Completo' 
        })
      } else if (ratio >= 0.85) {
        result.push({ 
          id: `${c.id}-near`, 
          title: c.title, 
          type: 'near', 
          label: 'Casi lleno' 
        })
      } else if (ratio <= 0.25) {
        result.push({ 
          id: `${c.id}-bajo`, 
          title: c.title, 
          type: 'bajo', 
          label: 'Baja inscripción' 
        })
      }
    }

    // Check for insufficient formadores
    const formCount = getDirectivoCount(c)
    if (formCount < 4) {
      result.push({ 
        id: `${c.id}-formadores-low`, 
        title: c.title, 
        type: 'formadores-low', 
        label: 'Formadores insuficientes' 
      })
    }
  })

  // Add pagos errors if any
  if (errorState.value.pagos) {
    result.push({
      id: 'pagos-error',
      title: 'Error en Pagos',
      type: 'error',
      label: 'Error al cargar los datos de pagos'
    })
  }

  return result.slice(0, 6)
})

// Track active error states
const errorState = ref({
  loading: false,
  cursos: false,
  pagos: false
})

function closeAlert(alertId) {
  if (!closedAlerts.value.includes(alertId)) closedAlerts.value.push(alertId)
}

function goToGestionPersonas() {
  router.push('/gestionpersonas')
}

function goToCursoEdit(cursoId) {
  router.push({ path: '/cursos-capacitaciones', query: { edit: cursoId } })
}



function showAlerts() {
  // Clear the list of closed alerts so all current alerts become visible again
  closedAlerts.value = []
}

function getDirectivoCount(curso) {
  return directivosByCourse.value[curso.id] !== undefined ? directivosByCourse.value[curso.id] : 0
}

function getDirectivoRequired(curso) {
  // Ejemplo: 1 formador por cada 10 inscritos, mínimo 2
  return Math.max(2, Math.ceil(curso.inscritos / 10))
}

function getDirectivoPercent(curso) {
  const current = getDirectivoCount(curso)
  const required = getDirectivoRequired(curso)
  return Math.min(100, (current / required) * 100)
}

function getDirectivoStatus(curso) {
  const current = getDirectivoCount(curso)
  const required = getDirectivoRequired(curso)
  if (current >= required) return 'ok'
  if (current >= required * 0.5) return 'near'
  return 'danger'
}

function getPagoStatus(curso) {
  const percent = curso.expected > 0 ? (curso.paid / curso.expected) * 100 : 0
  if (percent >= 80) return 'ok'
  if (percent >= 50) return 'near'
  return 'full'
}

function getPagoStatusLabel(curso) {
  const status = getPagoStatus(curso)
  if (status === 'ok') return 'Al día'
  if (status === 'near') return 'Pendiente'
  return 'Crítico'
}

onMounted(async () => {
  try {
    // Reset all data structures
    cursosList.value = []
    totalPersonas.value = 0
    pagosSumByCourse.value = {}
    pagosCountPaidByCourse.value = {}
    directivosByCourse.value = {}
    coordinadoresByCourse.value = {}
    directoresByCourse.value = {}

    // Fetch cursos with error handling
    const cursosResp = await fetch('http://127.0.0.1:8000/api/cursos/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })

    if (!cursosResp.ok) {
      throw new Error(`Error obteniendo cursos: ${cursosResp.status}`)
    }

    const cursosData = await cursosResp.json()
    const cursos = Array.isArray(cursosData) ? cursosData : (cursosData.results || [])

    // Process cursos data
    cursosList.value = cursos.map(c => ({
      id: c.CUS_ID,
      title: c.CUS_NOMBRE,
      rama: c.CUS_RAMA,
      inscritos: c.CUS_INSCRITOS || 0,
      capacidad: c.CUS_CAPACIDAD || 0,
      valor: c.CUS_VALOR || 0,
      estado: c.CUS_ESTADO,
      alimentacion: c.CUS_ALIMENTACION,
      directivos: c.CUS_DIRECTIVOS || 0,
      coordinadores: c.CUS_COORDINADORES || 0,
      directores: c.CUS_DIRECTORES || 0
    }))

    // Update counters and role assignments
    totalPersonas.value = cursosList.value.reduce((sum, c) => sum + (c.inscritos || 0), 0)

    cursosList.value.forEach(c => {
      directivosByCourse.value[c.id] = c.directivos
      coordinadoresByCourse.value[c.id] = c.coordinadores
      directoresByCourse.value[c.id] = c.directores
    })

    // Fetch and process pagos
    try {
      const pagosResp = await fetch('http://127.0.0.1:8000/api/cuotas/', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!pagosResp.ok) {
        throw new Error(`Error obteniendo pagos: ${pagosResp.status}`)
      }

      const pagosRaw = await pagosResp.json()
      const pagos = Array.isArray(pagosRaw) ? pagosRaw : (pagosRaw.results || [])

      // Reset pagos data before processing
      pagosSumByCourse.value = {}
      pagosCountPaidByCourse.value = {}

      // Process pagos with validation
      pagos.forEach(p => {
        const cursoId = p.CUO_CURSO
        if (!cursoId) return

        // Initialize counters for this curso if needed
        if (!pagosSumByCourse.value[cursoId]) {
          pagosSumByCourse.value[cursoId] = 0
          pagosCountPaidByCourse.value[cursoId] = 0
        }

        if (p.CUO_PAGADO) {
          const monto = Number(p.CUO_VALOR)
          if (!isNaN(monto) && monto > 0) {
            pagosSumByCourse.value[cursoId] += monto
            pagosCountPaidByCourse.value[cursoId]++
          }
        }
      })
    } catch (error) {
      console.error('Error procesando pagos:', error)
      // Continue with empty pagos data rather than failing completely
    }
  } catch (error) {
    console.error('Error cargando datos del dashboard:', error)
    // Reset all data on error
    cursosList.value = []
    totalPersonas.value = 0
    pagosSumByCourse.value = {}
    pagosCountPaidByCourse.value = {}
    directivosByCourse.value = {}
    coordinadoresByCourse.value = {}
    directoresByCourse.value = {}
  }
})
</script>

<style scoped>
.layout-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: var(--color-primary);
  overflow-x: hidden;
}

.layout-content {
  display: flex;
  flex-direction: row;
  flex: 1;
  width: 100%;
  min-height: 0;
  height: 100vh;
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem 1rem;
  min-height: 0;
  margin-left: 0;
  width: 100%;
}

.control-panel {
  background: var(--color-surface);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  max-width: 1400px;
  width: 100%;
  padding: 2rem;
  margin: 0 auto;
}

.control-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid var(--color-border);
}

.control-header h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.5rem;
}

.control-subtitle {
  color: var(--color-text);
  font-size: 1rem;
}



.semaforo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  max-width: 900px;
}

.semaforo-card {
  background: var(--color-surface);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 2px solid var(--color-border);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.semaforo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.semaforo-card.ok {
  border-color: #22c55e;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
}

.semaforo-card.near {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
}

.semaforo-card.full {
  border-color: #ef4444;
  background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
}

.semaforo-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.semaforo-data {
  flex: 1;
}

.semaforo-value {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
}

.semaforo-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.semaforo-indicator {
  position: absolute;
  top: 0;
  right: 0;
  width: 6px;
  height: 100%;
}

.semaforo-indicator.ok {
  background: var(--color-semaforo-green);
}

.semaforo-indicator.near {
  background: var(--color-semaforo-yellow);
}

.semaforo-indicator.full {
  background: var(--color-semaforo-red);
}

.data-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.section-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  max-width: 100%;
  border-radius: 12px;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--color-background-soft);
  border-radius: 10px;
  overflow: hidden;
  font-size: 1.05rem;
  margin-bottom: 0;
}

.data-table thead {
  background: var(--color-background-mute);
}

.data-table th {
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 700;
  padding: 12px 10px;
  border-bottom: 2px solid var(--color-border);
  text-align: left;
}

.data-table td {
  padding: 12px 10px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.data-table tr:nth-child(even) {
  background: var(--color-background-soft);
}

.data-table tr:last-child td {
  border-bottom: none;
}

/* Dashboard two-column layout */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  align-items: center;
  padding: 1rem;
}

.table-section {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.table-container.large {
  max-height: 400px;
  overflow: auto;
  margin-bottom: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-background-soft);
}

.chart-card-full {
  width: 100%;
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
  background: var(--color-surface);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 18px rgba(40,92,168,0.13);
}

.data-table.large th,
.data-table.large td {
  padding: 0.75rem 0.6rem;
}

/* Chart section styles */
.chart-card-full {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.right-panel .chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
}

.column-chart { width: 100%; height: 100%; }


/* Add breathing room on the right-most column so content never touches the edge */
.data-table th:last-child,
.data-table td:last-child {
  padding-right: 1.25rem;
}

.data-table tbody tr {
  background: #ffffff;
  border-left: 4px solid transparent;
  transition: background-color 0.15s ease;
}
.data-table tbody tr:nth-child(even) {
  background: #fafafa;
}
.data-table tbody tr:hover {
  background: #f1f5f9;
}
/* Status left border indicator */
.data-table tbody tr.row-ok { border-left-color: #16a34a; }
.data-table tbody tr.row-near { border-left-color: #f59e0b; }
.data-table tbody tr.row-full { border-left-color: #ef4444; }

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.badge {
  display: inline-block;
  padding: 4px 16px;
  border-radius: 14px;
  font-size: 1em;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-right: 2px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.badge-success {
  background: var(--color-semaforo-green);
  color: #fff;
  border: 1px solid transparent;
}

.badge-warning {
  background: var(--color-semaforo-yellow);
  color: #fff;
  border: 1px solid transparent;
}

.badge-pending {
  background: var(--color-semaforo-red);
  color: #fff;
  border: 1px solid transparent;
}

/* Column Chart Styles */
.chart-card-full {
  background: var(--color-surface);
  border-radius: 12px;
  padding: 24px;
  margin-top: 2rem;
  border: 1.5px solid var(--color-border);
  box-shadow: 0 4px 18px rgba(40,92,168,0.13);
}

.chart-header {
  margin-bottom: 24px;
}

.chart-header h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px 0;
}

.chart-description {
  color: var(--color-text-light);
  font-size: 0.9rem;
  margin: 0;
}

.column-chart {
  display: flex;
  height: 400px;
  margin: 20px 0;
  padding-bottom: 40px;
}

.chart-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: 12px;
  border-right: 1px solid var(--color-border);
  height: 320px;
  margin-bottom: 40px;
}

.axis-label {
  font-size: 0.8rem;
  color: var(--color-text-light);
  padding: 4px 8px;
  text-align: right;
  min-width: 80px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 40px;
  padding: 0 20px;
  flex: 1;
  overflow-x: auto;
  height: 360px;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
}

.bar-wrapper {
  display: flex;
  gap: 4px;
  height: 320px;
  align-items: flex-end;
  margin-bottom: 12px;
}

.bar {
  width: 40px;
  min-height: 2px;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 0.3s ease;
}

.bar-expected {
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  opacity: 0.3;
}

.bar-received {
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
}

.bar-value {
  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text);
  white-space: nowrap;
  background: var(--color-surface);
  padding: 2px 4px;
  border-radius: 4px;
}

.bar-label {
  font-size: 0.9rem;
  color: var(--color-text);
  text-align: center;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 8px;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-color.expected {
  background: var(--color-primary);
  opacity: 0.3;
}

.legend-color.received {
  background: var(--color-primary);
}

.curso-name-wrapper {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  min-width: 0;
}

.curso-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  flex-shrink: 0;
}

.curso-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9375rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.inscritos-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: transparent;
  color: #1e40af;
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  font-size: 0.8125rem;
  font-weight: 700;
}

.amount {
  font-weight: 600;
  font-size: 0.9375rem;
  white-space: nowrap;
}

.amount.paid {
  color: #15803d;
}

.amount.expected {
  color: #475569;
}

.amount.pending {
  color: #b91c1c;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  justify-content: center; /* center the whole group within the cell */
  width: 100%;
}

.mini-progress-bar {
  width: 80px;
  height: 6px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
  flex-shrink: 0;
  margin: 0 auto; /* help centering when layout changes */
}

.mini-progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.mini-progress-fill.ok {
  background: #22c55e;
}

.mini-progress-fill.near {
  background: #f59e0b;
}

.mini-progress-fill.full {
  background: #ef4444;
}

.progress-percent {
  font-size: 0.8125rem;
  font-weight: 700;
  color: #475569;
  min-width: 38px;
  width: 38px;
  text-align: center; /* ensure the % is visually centered */
}

.empty-row td {
  padding: 3rem 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #94a3b8;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #cbd5e1;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
  color: #64748b;
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
  background: transparent;
  border: 1px solid currentColor;
}

.status-badge.ok {
  color: #15803d; /* green-700 */
  border-color: #86efac; /* green-300 */
}

.status-badge.near {
  color: #b45309; /* amber-700 */
  border-color: #fde68a; /* amber-200 */
}

.status-badge.full {
  color: #b91c1c; /* red-700 */
  border-color: #fecaca; /* red-200 */
}





/* Gráfico de pagos por curso */
.chart-card-full {
  margin-top: 2rem;
}

.payment-bars {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.payment-bar-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.payment-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.payment-bar-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.payment-bar-percent {
  font-size: 1.125rem;
  font-weight: 800;
  color: #22c55e;
}

.payment-bar-track {
  display: flex;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  background: #e2e8f0;
}

.payment-bar-fill {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

.payment-bar-paid {
  background: linear-gradient(90deg, #22c55e, #16a34a);
}

.payment-bar-pending {
  background: linear-gradient(90deg, #f59e0b, #ef4444);
}

.payment-bar-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  padding: 0 0.5rem;
}

.payment-bar-footer {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.payment-amount {
  font-size: 0.875rem;
  color: #64748b;
}

.payment-amount strong {
  color: #1e293b;
  font-weight: 600;
}

/* Toast de alertas */
.toast-container {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
  pointer-events: none;
  display: flex;
  flex-direction: column-reverse;
  gap: 12px;
  align-items: flex-end;
}

.alert-toast {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #1e293b;
  padding: 1rem 1.25rem;
  padding-right: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 320px;
  max-width: 400px;
  pointer-events: auto;
  animation: slideInRight 0.3s ease;
  border-left: 4px solid #d97706;
  position: relative;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.alert-toast-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.alert-toast-content {
  flex: 1;
  min-width: 0;
}

.alert-toast-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.alert-toast-message {
  font-size: 0.8rem;
  color: #475569;
  line-height: 1.4;
}

.alert-toast-close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
  line-height: 1;
}

.alert-toast-close:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.1);
}

.alert-toast-close:active {
  transform: scale(0.95);
}

/* Modal de Cursos */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.cursos-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.curso-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.curso-item:hover {
  background: #fff;
  border-color: #2c5282;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(44, 82, 130, 0.15);
}

.curso-item-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #2c5282 0%, #1e3a5f 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.curso-item-icon svg {
  width: 24px;
  height: 24px;
  stroke: #fff;
}

.curso-item-info {
  flex: 1;
  min-width: 0;
}

.curso-item-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.curso-item-details {
  font-size: 0.875rem;
  color: #64748b;
}

.curso-item-arrow {
  font-size: 1.5rem;
  color: #64748b;
  transition: transform 0.3s ease;
}

.curso-item:hover .curso-item-arrow {
  transform: translateX(4px);
  color: #2c5282;
}

/* Directivos por curso */
.directivos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.directivo-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.directivo-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.directivo-card.ok {
  border-left: 4px solid #22c55e;
}

.directivo-card.near {
  border-left: 4px solid #f59e0b;
}

.directivo-card.danger {
  border-left: 4px solid #ef4444;
}

.directivo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.directivo-title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.directivo-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
  flex-shrink: 0;
}

.directivo-header h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.directivo-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
}

.directivo-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.directivo-stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
}

.directivo-stat-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.directivo-stat-divider {
  font-size: 1.25rem;
  color: #cbd5e1;
  font-weight: 700;
}

.directivo-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 700;
}

.directivo-badge.ok {
  background: #dcfce7;
  color: #166534;
}

.directivo-badge.near {
  background: #fef3c7;
  color: #92400e;
}

.directivo-badge.danger {
  background: #fee2e2;
  color: #991b1b;
}

.directivo-bar {
  height: 12px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.directivo-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.directivo-fill.ok {
  background: linear-gradient(90deg, #22c55e, #16a34a);
}

.directivo-fill.near {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.directivo-fill.danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.directivo-message {
  font-size: 0.875rem;
  color: #991b1b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #fee2e2;
  border-radius: 6px;
}

.directivo-message.warning {
  color: #92400e;
  background: #fef3c7;
}

.directivo-message.success {
  color: #166534;
  background: #dcfce7;
}

@media (max-width: 900px) {
  .control-panel {
    padding: 1.5rem;
  }
  
  .control-header h1 {
    font-size: 1.5rem;
  }

  .semaforo-grid {
    grid-template-columns: 1fr;
  }



  .alert-toast {
    min-width: 280px;
    max-width: 90vw;
  }
}

@media (max-width: 600px) {
  .main {
    padding: 1rem 0.5rem;
  }

  .control-panel {
    padding: 1rem;
    border-radius: 12px;
  }

  .control-header h1 {
    font-size: 1.25rem;
  }



  .table-container {
    font-size: 0.875rem;
  }

  .data-table th,
  .data-table td {
    padding: 0.75rem 0.5rem;
  }
}
</style>

