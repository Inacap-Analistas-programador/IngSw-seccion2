<template>
  <div class="layout-root">
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
      <main class="main">
        <div class="control-panel">



          <div class="tab-content">
            <div class="dashboard-grid">
              <div class="left-panel">
                <div class="table-container large">
                  <table class="data-table large">
                    <thead>
                      <tr>
                        <th :title="headerLabel('Curso')">{{ headerLabel('Curso') }}</th>
                        <th :title="headerLabel('Rama')">{{ headerLabel('Rama') }}</th>
                        <th class="text-center" :title="headerLabel('Formadores')">{{ headerLabel('Formadores') }}</th>
                        <th class="text-center" :title="headerLabel('Coordinadores')">{{ headerLabel('Coordinadores') }}</th>
                        <th class="text-center" :title="headerLabel('Directores')">{{ headerLabel('Directores') }}</th>
                        <th class="text-center" :title="headerLabel('Requeridos')">{{ headerLabel('Requeridos') }}</th>
                        <th class="text-center" :title="headerLabel('Inscritos')">{{ headerLabel('Inscritos') }}</th>
                        <th class="text-center" :title="headerLabel('EstadoCurso')">{{ headerLabel('EstadoCurso') }}</th>
                        <!-- Vigencia moved into the row details modal on click -->
                        <th class="text-right" :title="headerLabel('Capacidad')">{{ headerLabel('Capacidad') }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="curso in sortedCursos" :key="curso.id" :class="['row-' + getDirectivoStatus(curso), 'clickable']" @click="openCursoDetails(curso)">
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
                        <td class="text-center">{{ curso.inscritos ?? '-' }}</td>
                        <td class="text-center"><span :class="['status-badge', getDirectivoStatus(curso)]">{{ getDirectivoStatus(curso) === 'ok' ? 'OK' : (getDirectivoStatus(curso) === 'near' ? 'Casi' : 'Faltan') }}</span></td>
                        <td class="text-right">{{ curso.capacidad ?? '-' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="right-panel">
                <div class="chart-card">
                  <h3 class="chart-title">Recaudación: Esperado vs Recaudado</h3>
                  <div class="chart-wrapper">
    <svg viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet" class="column-chart">
      <g>
        <g v-for="(v, idx) in chartTicks" :key="v">
          <line :x1="chartPadding.left" :x2="(svgWidth - chartPadding.right)" :y1="(chartPadding.top + (chartInnerHeight - ((v - chartMin) / (chartMax - chartMin || 1) * chartInnerHeight)))" :y2="(chartPadding.top + (chartInnerHeight - ((v - chartMin) / (chartMax - chartMin || 1) * chartInnerHeight)))" stroke="#e2e8f0" />
          <text :x="(chartPadding.left - 20)" :y="(chartPadding.top + (chartInnerHeight - ((v - chartMin) / (chartMax - chartMin || 1) * chartInnerHeight)) + 4)" font-size="12" fill="#64748b">{{ fmtCurrency(v) }}</text>
        </g>
      </g>
      <g>
        <g v-for="(d, i) in chartData" :key="d.id">
          <rect :x="barXExpected(i)" :y="barYFromValue(d.expected)" :width="barWidth" :height="barHeight(d.expected)" fill="#93c5fd" rx="4" />
          <rect :x="barXPaid(i)" :y="barYFromValue(d.paid)" :width="barWidth" :height="barHeight(d.paid)" fill="#1e40af" rx="4" />
          <text :x="barLabelX(i)" :y="(chartPadding.top + chartInnerHeight + 18)" font-size="12" text-anchor="middle" fill="#334155">{{ d.title }}</text>
        </g>
      </g>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
    <div v-if="showSelectedCurso" class="modal-overlay" @click.self="closeCursoDetails">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedCurso?.title || 'Detalle del curso' }}</h3>
          <button class="modal-close" @click="closeCursoDetails">×</button>
        </div>
        <div class="modal-body">
          <table style="width:100%; border-collapse: collapse;">
            <tbody>
              <tr>
                <td style="padding:8px; font-weight:700">Esperado</td>
                <td style="padding:8px">{{ fmtCurrency((pagosMap[selectedCurso?.id] && pagosMap[selectedCurso?.id].expected) || 0) }}</td>
              </tr>
              <tr>
                <td style="padding:8px; font-weight:700">Alimentación</td>
                <td style="padding:8px">{{ selectedCurso?.alimentacion ? 'Sí' : 'No' }}</td>
              </tr>
              <tr>
                <td style="padding:8px; font-weight:700">Activo</td>
                <td style="padding:8px">{{ selectedCurso ? (isCursoActive(selectedCurso) ? 'Sí' : 'No') : '-' }}</td>
              </tr>
              <tr>
                <td style="padding:8px; font-weight:700">Vigencia</td>
                <td style="padding:8px">{{ (selectedCurso?.vigencia ?? selectedCurso?.estado) || (selectedCurso ? computeCourseState(selectedCurso) : '-') }}</td>
              </tr>
              <tr>
                <td style="padding:8px; font-weight:700">Formadores</td>
                <td style="padding:8px">{{ getDirectivoCount(selectedCurso) }} / {{ getDirectivoRequired(selectedCurso) }}
                  <span :class="['status-badge', getDirectivoStatus(selectedCurso)]" style="margin-left:12px">{{ getDirectivoStatus(selectedCurso) === 'ok' ? 'OK' : (getDirectivoStatus(selectedCurso) === 'near' ? 'Casi' : 'Faltan') }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppIcons from '@/components/icons/AppIcons.vue'
import { cursos as cursosApi, cuotas as cuotasApi } from '@/services/cursosService.js'
import { personas as personasApi } from '@/services/personasService.js'

const router = useRouter()
const showCursosModal = ref(false)

const cursosList = ref([])
const totalPersonas = ref(0)
// selected curso for detail popup
const selectedCurso = ref(null)
const showSelectedCurso = ref(false)

const sortedCursos = computed(() =>
  [...cursosList.value].sort((a, b) => (a.title || '').localeCompare(b.title || '', 'es', { sensitivity: 'base' }))
)



function getAlertIcon(type) {
  const icons = { full: '🔴', near: '🟡', bajo: '🟢', 'formadores-low': '🚨' }
  return icons[type] || '⚠️'
}

// Header label map (no abbreviations — show full names)
const headerMap = {
  'Curso': 'Curso',
  'Rama': 'Rama',
  'Formadores': 'Formadores',
  'Coordinadores': 'Coordinadores',
  'Directores': 'Directores',
  'Requeridos': 'Requeridos',
  'Estado': 'Estado',
  'Vigencia': 'Vigencia',
  'Capacidad': 'Capacidad',
  'Esperado': 'Esperado',
  'Alimentación': 'Alimentación',
  'Activo': 'Activo',
  // special key for second Estado column (course state)
  'EstadoCurso': 'Estado'
}

function headerLabel(key) {
  return headerMap[key] || key
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

// Pagos no enlazados aún: dejamos montos en 0 hasta habilitar API de pagos
const pagosSumByCourse = ref({})
const pagosCountPaidByCourse = ref({})
const directivosByCourse = ref({
  1: 4,  // Curso Básico Scout: tiene 4 de 3 requeridos (OK)
  2: 7,  // Curso de Especialidades: tiene 7 de 2 requeridos (OK)
  3: 0,  // Formación de Dirigentes: tiene 0 de 3 requeridos (CRÍTICO)
  4: 1   // Capacitación de Liderazgo: tiene 1 de 2 requeridos (ADVERTENCIA)
})
// Additional role counts (if available from API later)
const coordinadoresByCourse = ref({})
const directoresByCourse = ref({})

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

const chartMin = 0
const chartMax = computed(() => {
  const maxFromData = chartData.value.length ? Math.max(...chartData.value.map(d => Math.max(d.expected || 0, d.paid || 0))) : 0
  return Math.max(500000, maxFromData)
})

// Dynamic Y ticks (0 .. chartMax) split into 5 steps
const chartTicks = computed(() => {
  const max = chartMax.value || 1
  const steps = 5
  const rawStep = Math.ceil(max / steps / 1000) * 1000
  const ticks = []
  for (let i = 0; i <= steps; i++) ticks.push(i * rawStep)
  // ensure last tick is at least max
  if (ticks[ticks.length - 1] < max) ticks[ticks.length - 1] = Math.ceil(max / 1000) * 1000
  return ticks
})

// SVG/chart layout parameters (for larger drawing area and dynamic bar sizing)
const svgWidth = 800
const svgHeight = 600
const chartPadding = { left: 80, right: 80, top: 60, bottom: 60 }
const chartInnerWidth = computed(() => svgWidth - chartPadding.left - chartPadding.right)
const chartInnerHeight = computed(() => svgHeight - chartPadding.top - chartPadding.bottom)
const barGroupWidth = computed(() => Math.max(1, chartInnerWidth.value / Math.max(1, chartData.value.length)))
// spacing between expected and paid bars inside a group
const barGap = 8
// make bars narrower to avoid overlap: compute available space per group and split between two bars
const barWidth = computed(() => {
  const available = Math.max(0, barGroupWidth.value - barGap)
  // each bar gets roughly half of the available space; cap to keep them readable
  return Math.max(12, Math.min(80, Math.floor(available / 2)))
})

function barHeight(value) {
  const h = chartInnerHeight.value // use computed inner height
  if (!value || value <= chartMin) return 0
  const max = chartMax.value || 500000
  return Math.round(((value - chartMin) / (max - chartMin)) * h)
}

// Helper X/Y functions for SVG positioning
function barXExpected(i) {
  const groupStart = chartPadding.left + i * barGroupWidth.value
  const totalBarsWidth = barWidth.value * 2 + barGap
  return Math.round(groupStart + (barGroupWidth.value - totalBarsWidth) / 2)
}

function barXPaid(i) {
  return Math.round(barXExpected(i) + barWidth.value + barGap)
}

function barYFromValue(value) {
  // Y position within SVG (top-based)
  return Math.round(chartPadding.top + (chartInnerHeight.value - barHeight(value)))
}

function barLabelX(i) {
  const totalBarsWidth = barWidth.value * 2 + barGap
  return Math.round(barXExpected(i) + totalBarsWidth / 2)
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
  sortedCursos.value.forEach(c => {
    const cap = Number(c.capacidad) || 0
    const ins = Number(c.inscritos) || 0
    if (cap) {
      const ratio = ins / cap
      if (ratio >= 1) result.push({ id: `${c.id}-full`, title: c.title, type: 'full', label: 'Completo' })
      else if (ratio >= 0.85) result.push({ id: `${c.id}-near`, title: c.title, type: 'near', label: 'Casi lleno' })
      else if (ratio <= 0.25) result.push({ id: `${c.id}-bajo`, title: c.title, type: 'bajo', label: 'Baja inscripción' })
    }

    // Formadores alerts: notify only when formadores are insufficient (<4)
    const formCount = getDirectivoCount(c)
    if (formCount < 4) {
      result.push({ id: `${c.id}-formadores-low`, title: c.title, type: 'formadores-low', label: 'Formadores insuficientes' })
    }
  })
  return result.slice(0, 6)
})

// Track closed alerts so we don't attempt to mutate a computed property
const closedAlerts = ref([])

const visibleAlerts = computed(() => alerts.value.filter(alert => !closedAlerts.value.includes(alert.id)))

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

function openCursoDetails(curso) {
  selectedCurso.value = curso
  showSelectedCurso.value = true
}

function closeCursoDetails() {
  selectedCurso.value = null
  showSelectedCurso.value = false
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

onMounted(() => {
  ;(async () => {
    try {
      // Fetch cursos data
      const response = await cursosApi.list()
      const cursosData = Array.isArray(response) ? response : (response.results || response.data || [])
      console.log('Cursos data:', cursosData)

      // Map cursos data
      cursosList.value = cursosData.map(c => ({
        id: c.id ?? c.CUS_ID ?? c.pk ?? null,
        title: c.title || c.nombre || c.CUS_NOMBRE || c.name || '',
        inscritos: Number(c.inscritos ?? c.inscritos_total ?? c.inscripciones ?? 0),
        capacidad: Number(c.capacidad ?? c.CUS_CAPACIDAD ?? c.capacity ?? 0),
        valor: Number(c.valor ?? c.valor_cuota ?? c.price ?? 0)
      }))

      // Fetch personas data
      const personas = await personasApi.list()
      const personasData = Array.isArray(personas) ? personas : (personas.results || personas.data || [])
      console.log('Personas data:', personasData)

      // Map roles data
      const roles = { coordinadores: {}, directores: {}, formadores: {} }
      personasData.forEach(p => {
        if (p.curso_id && p.rol) {
          const rol = p.rol.toLowerCase()
          if (rol.includes('coordinador')) {
            roles.coordinadores[p.curso_id] = (roles.coordinadores[p.curso_id] || 0) + 1
          } else if (rol.includes('director')) {
            roles.directores[p.curso_id] = (roles.directores[p.curso_id] || 0) + 1
          } else if (rol.includes('formador')) {
            roles.formadores[p.curso_id] = (roles.formadores[p.curso_id] || 0) + 1
          }
        }
      })

      // Update role counts
      coordinadoresByCourse.value = roles.coordinadores
      directoresByCourse.value = roles.directores
      directivosByCourse.value = roles.formadores

      // Fetch cuotas data
      const cuotasResponse = await cuotasApi.list()
      const cuotasData = Array.isArray(cuotasResponse) ? cuotasResponse : (cuotasResponse.results || cuotasResponse.data || [])
      console.log('Cuotas data:', cuotasData)

      // Map pagos data
      const pagos = { sums: {}, counts: {} }
      cuotasData.forEach(q => {
        const cursoId = q.curso_id || q.CUS_ID || q.curso || q.id
        if (cursoId && q.pagado) {
          pagos.sums[cursoId] = (pagos.sums[cursoId] || 0) + Number(q.valor || q.monto || 0)
          pagos.counts[cursoId] = (pagos.counts[cursoId] || 0) + 1
        }
      })

      // Update pagos data
      pagosSumByCourse.value = pagos.sums
      pagosCountPaidByCourse.value = pagos.counts

      // Update total personas
      totalPersonas.value = personasData.length

      console.log('Dashboard data loaded successfully')
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    }
  })()
})
</script>

<style scoped>
.layout-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #2c5cdd 0%, #2563eb 50%, #3b82f6 100%);
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
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}

.control-subtitle {
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;

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
  overflow-x: hidden; /* avoid horizontal scrollbar */
  max-width: 100%;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.table-container::-webkit-scrollbar {
  height: 0;
}
.table-container {
  scrollbar-width: none;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  table-layout: auto;
}

.data-table, .data-table th, .data-table td {
  box-sizing: border-box;
}

.data-table thead {
  background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
}

.data-table thead th {
  white-space: normal;
  word-break: break-word;
  hyphens: auto;
}

.data-table th {
  padding: 0.45rem 0.6rem;
  text-align: left;
  font-weight: 600;
  color: #fff;
  font-size: 0.66rem;
  
  text-transform: none;
  letter-spacing: 0.01em;
  white-space: normal; 
  line-height: 1.1;
  vertical-align: bottom; 
  background: transparent;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.data-table th.text-center { text-align: center; }
.data-table th.text-right { text-align: right; }

.data-table thead th {
  hyphens: auto;
  overflow-wrap: break-word;
}

.data-table td {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  border-right: 1px solid #e2e8f0;
  color: #334155;
  vertical-align: middle;
  font-size: 0.8125rem;
  line-height: 1.4;
}

.data-table th:last-child,
.data-table td:last-child {
  border-right: none;
}


.dashboard-grid {
  display: grid;
  
  grid-template-columns: 1fr;
  gap: 1.5rem;
  align-items: start;
  margin-top: 1rem;
}

.left-panel .data-table.large th,
.left-panel .data-table.large td {
  padding: 0.75rem 0.6rem;
}

.table-container.large {
  max-height: 720px;
  overflow: auto;
  
  max-width: 1100px;
  margin: 0 auto;
}

.right-panel .chart-card {
  background: var(--ds-surface);
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  height: 100%;
  min-height: 420px; 
  display: flex;
  flex-direction: column;
  max-width: 820px;
  margin: 0 auto; 
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--ds-text);
  margin-bottom: 1rem;
  text-align: center;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
}

.column-chart { 
  width: 100%; 
  height: 100%;
  min-height: 520px;
}



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

.data-table tbody tr.row-ok { border-left-color: #16a34a; }
.data-table tbody tr.row-near { border-left-color: #f59e0b; }
.data-table tbody tr.row-full { border-left-color: #ef4444; }

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.curso-name-wrapper {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  min-width: 0;
}

.vigencia-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}
.vigencia-value {
  font-size: 0.95rem;
  color: #1e293b;
  font-weight: 700;
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
  font-size: 0.875rem;
  overflow: hidden;
  text-overflow: ellipsis;
  
  white-space: nowrap;
  line-height: 1.4;
  padding: 0.125rem 0;
}


@media (max-width: 900px) {
  .curso-name {
    white-space: normal;
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
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
  justify-content: center; 
  width: 100%;
}

.mini-progress-bar {
  width: 80px;
  height: 6px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
  flex-shrink: 0;
  margin: 0 auto; 
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
  text-align: center; 
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
  padding: 0.2rem 0.5rem;
  border-radius: 999px;
  font-size: 0.675rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  white-space: nowrap;
  background: transparent;
  border: 1px solid currentColor;
  line-height: 1.1;
  min-width: 60px;
  text-align: center;
}

.status-badge.ok {
  color: #15803d; 
  border-color: #86efac; 
}

.status-badge.near {
  color: #b45309; 
  border-color: #fde68a; 
}

.status-badge.full {
  color: #b91c1c; 
  border-color: #fecaca;
}

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

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background-image: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
  color: #fff;
  padding: 8px 12px;
  border-radius: 10px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(30, 60, 114, 0.12);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(30, 60, 114, 0.14); }


.data-table th { font-size: 0.72rem; }


.column-chart text { font-family: "Segoe UI", Roboto, system-ui, sans-serif; font-weight: 600; }

</style>

/* Styles adapted from Correos.vue datatable for a cleaner table appearance
   These rules target the existing .table-container .data-table structure
   used by the Dashboard and are intentionally scoped to avoid broad site changes. */
<style scoped>
.table-container.datatable-visual, .table-container {
  overflow-x: auto;
}

.table-container .data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--color-background-soft, #f8fafc);
  border-radius: 10px;
  overflow: hidden;
  font-size: 1.05rem;
  margin-bottom: 0;
}

.table-container .data-table th {
  background: var(--color-background-mute, #f1f5f9);
  color: var(--color-text, #1e293b);
  font-weight: 700;
  padding: 12px 10px;
  border-bottom: 2px solid var(--color-border, #e2e8f0);
  text-align: left;
}

.table-container .data-table td {
  padding: 12px 10px;
  border-bottom: 1px solid var(--color-border, #e2e8f0);
  color: var(--color-text, #334155);
}

.table-container .data-table tr:nth-child(even) {
  background: var(--color-background-soft, #f8fafc);
}

.table-container .data-table tr:last-child td {
  border-bottom: none;
}

/* compact override for existing .data-table styles in dashboard when .large is used */
.table-container.large .data-table th,
.table-container.large .data-table td {
  padding: 0.75rem 0.6rem;
}
</style>
