<template>
  <div class="layout-root">
    <!-- Notificaciones de alertas -->
    <div class="toast-container">
      <div 
        v-for="(alert, index) in visibleAlerts" 
        :key="alert.id" 
        class="alert-toast"
      >
        <div class="alert-toast-icon">⚠️</div>
        <div class="alert-toast-content">
          <div class="alert-toast-title">{{ alert.title }}</div>
          <div class="alert-toast-message">{{ getAlertDescription(alert.type, alert.title) }}</div>
        </div>
        <button class="alert-toast-close" @click="closeAlert(alert.id)">✕</button>
      </div>
    </div>

    <div class="layout-content">
      <main class="main">
        <div class="control-panel">
          <header class="control-header">
            <h1>Centro de Control</h1>
            <p class="control-subtitle">Sistema de Gestión de Cursos Scout</p>
          </header>

          <!-- Navegación por pestañas -->
          <nav class="tabs-nav" v-if="false">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              :class="['tab-btn', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path v-if="tab.id === 'resumen'" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              <span class="tab-label">{{ tab.label }}</span>
            </button>
          </nav>

          <!-- Vista Resumen -->
          <div v-show="activeTab === 'resumen'" class="tab-content">
            <!-- Indicadores críticos tipo semáforo -->
            <div class="semaforo-grid">
              <div :class="['semaforo-card', getSemaforoClass('inscritos')]" @click="goToGestionPersonas">
                <svg class="semaforo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/>
                </svg>
                <div class="semaforo-data">
                  <div class="semaforo-value">{{ kpi.totalInscritos }}</div>
                  <div class="semaforo-label">Pre inscritos totales</div>
                </div>
                <div :class="['semaforo-indicator', getSemaforoClass('inscritos')]"></div>
              </div>

              <div :class="['semaforo-card', getSemaforoClass('cursos')]" @click="showCursosModal = !showCursosModal">
                <svg class="semaforo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
                  <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
                </svg>
                <div class="semaforo-data">
                  <div class="semaforo-value">{{ kpi.totalCursos }}</div>
                  <div class="semaforo-label">Cursos activos</div>
                </div>
                <div :class="['semaforo-indicator', getSemaforoClass('cursos')]"></div>
              </div>

              <div :class="['semaforo-card', getSemaforoClass('alertas')]" @click="showAlerts">
                <svg class="semaforo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                <div class="semaforo-data">
                  <div class="semaforo-value">{{ alerts.length }}</div>
                  <div class="semaforo-label">Alertas activas</div>
                </div>
                <div :class="['semaforo-indicator', getSemaforoClass('alertas')]"></div>
              </div>
            </div>

            <!-- Modal de Cursos Activos -->
            <div v-if="showCursosModal" class="modal-overlay" @click="showCursosModal = false">
              <div class="modal-content" @click.stop>
                <div class="modal-header">
                  <h3>Cursos Activos</h3>
                  <button class="modal-close" @click="showCursosModal = false">✕</button>
                </div>
                <div class="modal-body">
                  <div class="cursos-list">
                    <div 
                      v-for="curso in sortedCursos" 
                      :key="curso.id" 
                      class="curso-item"
                      @click="goToCursoEdit(curso.id)"
                    >
                      <div class="curso-item-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
                          <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
                        </svg>
                      </div>
                      <div class="curso-item-info">
                        <div class="curso-item-title">{{ curso.title }}</div>
                        <div class="curso-item-details">{{ curso.inscritos }}/{{ curso.capacidad }} pre inscritos</div>
                      </div>
                      <div class="curso-item-arrow">→</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Directivos por curso -->
            <div class="data-section">
              <div class="section-header">
                <div>
                  <h2 class="section-title">Formadores por Curso</h2>
                  <p class="section-description">Se requiere 1 formador por cada 10 pre inscritos (mínimo 2 formadores)</p>
                </div>
              </div>
              <div class="directivos-grid">
                <div v-for="curso in sortedCursos" :key="curso.id" class="directivo-card" :class="getDirectivoStatus(curso)">
                  <div class="directivo-header">
                    <div class="directivo-title-group">
                      <svg class="directivo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/>
                      </svg>
                      <h3>{{ curso.title }}</h3>
                    </div>
                    <span :class="['directivo-badge', getDirectivoStatus(curso)]">
                      {{ getDirectivoCount(curso) }}/{{ getDirectivoRequired(curso) }}
                    </span>
                  </div>
                  <div class="directivo-stats">
                    <span class="directivo-stat">
                      <span class="directivo-stat-value">{{ getDirectivoCount(curso) }}</span>
                      <span class="directivo-stat-label">Actuales</span>
                    </span>
                    <span class="directivo-stat-divider">→</span>
                    <span class="directivo-stat">
                      <span class="directivo-stat-value">{{ getDirectivoRequired(curso) }}</span>
                      <span class="directivo-stat-label">Requeridos</span>
                    </span>
                  </div>
                  <div class="directivo-bar">
                    <div 
                      class="directivo-fill" 
                      :class="getDirectivoStatus(curso)"
                      :style="{ width: getDirectivoPercent(curso) + '%' }"
                    ></div>
                  </div>
                  <div class="directivo-message" v-if="getDirectivoStatus(curso) === 'danger'">
                    ⚠️ Faltan {{ getDirectivoRequired(curso) - getDirectivoCount(curso) }} formadores
                  </div>
                  <div class="directivo-message warning" v-else-if="getDirectivoStatus(curso) === 'near'">
                    ⚡ Necesita {{ getDirectivoRequired(curso) - getDirectivoCount(curso) }} formador{{ getDirectivoRequired(curso) - getDirectivoCount(curso) > 1 ? 'es' : '' }} más
                  </div>
                  <div class="directivo-message success" v-else>
                    ✓ Personal completo
                  </div>
                </div>
              </div>
            </div>

            <!-- Cursos con pagos pendientes -->
            <div class="data-section">
              <div class="section-header">
                <div>
                  <h2 class="section-title">Cursos con Pagos Pendientes</h2>
                  <p class="section-description">Resumen de recaudación y montos pendientes por curso</p>
                </div>
              </div>
              <div class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th style="width: auto;">Curso</th>
                      <th class="text-center" style="width: auto;">PreInscritos</th>
                      <th class="text-center" style="width: auto;">Recaudado</th>
                      <th class="text-center" style="width: auto;">Esperado</th>
                      <th class="text-center" style="width: auto;">Pendiente</th>
                      <th class="text-center" style="width: auto;">Progreso</th>
                      <th class="text-center" style="width: auto;">Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="curso in cursosConPagosPendientes" :key="curso.title" :class="'row-' + getPagoStatus(curso)">
                      <td style="width: 25%;">
                        <div class="curso-name-wrapper">
                          <svg class="curso-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
                            <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
                          </svg>
                          <span class="curso-name">{{ curso.title }}</span>
                        </div>
                      </td>
                      <td class="text-center" style="width: auto;">
                        <span class="inscritos-badge">{{ curso.inscritos }}</span>
                      </td>
                      <td class="text-right" style="width: auto;">
                        <span class="amount paid">{{ fmtCurrency(curso.paid) }}</span>
                      </td>
                      <td class="text-right" style="width: auto;">
                        <span class="amount expected">{{ fmtCurrency(curso.expected) }}</span>
                      </td>
                      <td class="text-right" style="width: auto;">
                        <span class="amount pending">{{ fmtCurrency(curso.unpaid) }}</span>
                      </td>
                      <td class="text-center" style="width: auto;">
                        <div class="progress-cell">
                          <div class="mini-progress-bar">
                            <div 
                              class="mini-progress-fill" 
                              :class="getPagoStatus(curso)"
                              :style="{ width: curso.percentPaid + '%' }"
                            ></div>
                          </div>
                          <span class="progress-percent">{{ curso.percentPaid }}%</span>
                        </div>
                      </td>
                      <td class="text-center" style="width: 10%;">
                        <span :class="['status-badge', getPagoStatus(curso)]">
                          {{ getPagoStatusLabel(curso) }}
                        </span>
                      </td>
                    </tr>
                    <tr v-if="cursosConPagosPendientes.length === 0" class="empty-row">
                      <td colspan="7" class="text-center">
                        <div class="empty-state">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                          </svg>
                          <p>¡Excelente! No hay pagos pendientes</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('resumen')
const showCursosModal = ref(false)

const tabs = [
  { id: 'resumen', label: 'Resumen', icon: '📊' }
]

const cursosList = ref([
  { id: 1, title: 'Curso Básico Scout', inscritos: 28, capacidad: 30, valor: 25000, estado: 'Vigente' },
  { id: 2, title: 'Curso de Especialidades', inscritos: 10, capacidad: 20, valor: 35000, estado: 'Vigente' },
  { id: 3, title: 'Formación de Dirigentes', inscritos: 22, capacidad: 25, valor: 40000, estado: 'Vigente' },
  { id: 4, title: 'Capacitación de Liderazgo', inscritos: 15, capacidad: 20, valor: 30000, estado: 'Vigente' }
])

const sortedCursos = computed(() =>
  [...cursosList.value].sort((a, b) => (a.title || '').localeCompare(b.title || '', 'es', { sensitivity: 'base' }))
)

function cursoAlert(curso) {
  if (!curso || !curso.capacidad) return 'ok'
  if (curso.inscritos >= curso.capacidad) return 'full'
  if (curso.inscritos >= curso.capacidad * 0.7) return 'near'
  return 'ok'
}

function chartPercent(curso) {
  const cap = Math.max(0, Number(curso.capacidad) || 0)
  const ins = Math.max(0, Math.min(Number(curso.inscritos) || 0, cap))
  return cap === 0 ? 0 : Math.round((ins / cap) * 100)
}

function getStatusLabel(status) {
  const labels = { ok: 'Normal', near: 'Casi lleno', full: 'Completo' }
  return labels[status] || 'Normal'
}

function getAlertIcon(type) {
  const icons = { full: '🔴', near: '🟡', bajo: '🟢' }
  return icons[type] || '⚠️'
}

function getAlertDescription(type, title) {
  if (type === 'full') return `El curso "${title}" ha alcanzado su capacidad máxima.`
  if (type === 'near') return `El curso "${title}" está cerca de completar su capacidad.`
  if (type === 'bajo') return `El curso "${title}" tiene baja inscripción.`
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
  return 'ok'
}

const pagosSumByCourse = ref({
  1: 450000,  // Curso Básico Scout: 28 * 25000 = 700000, pagado 450000
  2: 280000,  // Curso de Especialidades: 10 * 35000 = 350000, pagado 280000
  3: 520000,  // Formación de Dirigentes: 22 * 40000 = 880000, pagado 520000
  4: 150000   // Capacitación de Liderazgo: 15 * 30000 = 450000, pagado 150000
})
const pagosCountPaidByCourse = ref({})
const directivosByCourse = ref({
  1: 4,  // Curso Básico Scout: tiene 4 de 3 requeridos (OK)
  2: 7,  // Curso de Especialidades: tiene 7 de 2 requeridos (OK)
  3: 0,  // Formación de Dirigentes: tiene 0 de 3 requeridos (CRÍTICO)
  4: 1   // Capacitación de Liderazgo: tiene 1 de 2 requeridos (ADVERTENCIA)
})

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

function getCursoPaid(cursoId) {
  return pagosSumByCourse.value[cursoId] || 0
}

function fmtCurrency(amount) {
  try {
    return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(Number(amount || 0))
  } catch (_) {
    return `$${Number(amount || 0).toLocaleString('es-CL')}`
  }
}

const kpi = computed(() => {
  const totalCursos = sortedCursos.value.length
  const totalInscritos = sortedCursos.value.reduce((sum, c) => sum + (Number(c.inscritos) || 0), 0)
  const ingresosProyectados = sortedCursos.value.reduce((sum, c) => sum + (Number(c.inscritos) || 0) * (Number(c.valor) || 0), 0)
  const ingresosPagados = pagosBars.value.reduce((sum, b) => sum + (Number(b.paid) || 0), 0)
  const ingresosPendientes = Math.max(0, ingresosProyectados - ingresosPagados)
  return { totalCursos, totalInscritos, ingresosProyectados, ingresosPagados, ingresosPendientes }
})

const kpiPaymentPercent = computed(() => {
  if (kpi.value.ingresosProyectados === 0) return 0
  return Math.round((kpi.value.ingresosPagados / kpi.value.ingresosProyectados) * 100)
})

function getBarHeight(value, type, maxValue = null) {
  const allCapacities = sortedCursos.value.map(c => c.capacidad)
  const max = Math.max(...allCapacities, 1)
  if (type === 'capacidad') {
    return (value / max) * 100
  }
  if (type === 'inscritos') {
    const capMax = maxValue || max
    return (value / max) * 100
  }
  return 0
}

function getCursoShortName(title) {
  const words = title.split(' ')
  if (words.length <= 2) return title
  return words.slice(0, 2).join(' ')
}

function getDonutDash() {
  const circumference = 2 * Math.PI * 80
  const percent = kpiPaymentPercent.value
  const dashLength = (percent / 100) * circumference
  return `${dashLength} ${circumference}`
}

const alerts = computed(() => {
  const result = []
  sortedCursos.value.forEach(c => {
    const cap = Number(c.capacidad) || 0
    const ins = Number(c.inscritos) || 0
    if (!cap) return
    const ratio = ins / cap
    if (ratio >= 1) result.push({ id: `${c.id}-full`, title: c.title, type: 'full', label: 'Completo' })
    else if (ratio >= 0.85) result.push({ id: `${c.id}-near`, title: c.title, type: 'near', label: 'Casi lleno' })
    else if (ratio <= 0.25) result.push({ id: `${c.id}-bajo`, title: c.title, type: 'bajo', label: 'Baja inscripción' })
  })
  return result.slice(0, 6)
})

const closedAlerts = ref([])

const visibleAlerts = computed(() => {
  return alerts.value.filter(alert => !closedAlerts.value.includes(alert.id))
})

function closeAlert(alertId) {
  closedAlerts.value.push(alertId)
}

function goToGestionPersonas() {
  router.push('/gestionpersonas')
}

function goToCursoEdit(cursoId) {
  router.push({ path: '/cursos-capacitaciones', query: { edit: cursoId } })
}

function goToGraficos() {
  activeTab.value = 'graficos'
}

function scrollToTable() {
  const table = document.querySelector('.data-section')
  if (table) {
    table.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function showAlerts() {
  closedAlerts.value = []
}

function getDirectivoCount(curso) {
  // Simulado: en producción vendría de la API
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

onMounted(() => {
  async function fetchJSON(url) {
    try {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      return await res.json()
    } catch (err) {
      console.warn('Failed to fetch', url, err)
      return null
    }
  }

  ;(async () => {
    const cursos = await fetchJSON('/api/cursos/cursos/')
    if (Array.isArray(cursos)) {
      cursosList.value = cursos.map(c => ({
        id: c.CURS_ID || c.CUR_ID || c.id || c.ID,
        title: c.CUR_DESCRIPCION || c.CUR_CODIGO || c.CURS_ID || 'Curso',
        inscritos: parseInt(c._inscritos_count || c.INSCRITOS || 0) || 0,
        capacidad: parseInt(c.CUR_COTA_CON_ALMUERZO || c.CUR_COTA_SIN_ALMUERZO || c.CUR_CANT_PARTICIPANTE || c.CAPACIDAD || 0) || 0,
        valor: 0,
        estado: c.CUR_ESTADO || c.ESTADO || 'Vigente'
      }))
    }

    const cuotas = await fetchJSON('/api/cursos/cuotas/')
    if (Array.isArray(cuotas)) {
      const byCourse = {}
      cuotas.forEach(q => {
        const curId = q.CUR_ID || q.curso_id || q.cur_id || null
        if (!curId) return
        const val = Number(q.CUU_VALOR || q.valor || 0)
        const date = q.CUU_FECHA || ''
        const prev = byCourse[curId]
        if (!prev || val > prev.val || (date && prev.date && date > prev.date)) {
          byCourse[curId] = { val, date }
        }
      })
      cursosList.value = cursosList.value.map(c => ({ ...c, valor: byCourse[c.id]?.val || c.valor || 0 }))
    }

    const pagos = await fetchJSON('/api/pagos/pago-persona/')
    if (Array.isArray(pagos)) {
      const sum = {}
      const countPaid = {}
      const asNumber = v => {
        const n = Number((v ?? '').toString().replace(/[^0-9.-]/g, ''))
        return isNaN(n) ? 0 : n
      }
      pagos.forEach(p => {
        const curId = p.CUR_ID || p.CURS_ID || p.curso_id || p.cur_id || null
        if (!curId) return
        const monto = asNumber(p.PAP_VALOR || p.valor || p.MONTO)
        sum[curId] = (sum[curId] || 0) + monto
        countPaid[curId] = (countPaid[curId] || 0) + 1
      })
      pagosSumByCourse.value = sum
      pagosCountPaidByCourse.value = countPaid
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
  background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
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
  background: #fff;
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
  border-bottom: 2px solid #e2e8f0;
}

.control-header h1 {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #2c5282 0%, #1e3a5f 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.control-subtitle {
  color: #64748b;
  font-size: 1rem;
}

.tabs-nav {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 12px;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  color: #64748b;
}

.tab-btn:hover {
  background: #e2e8f0;
}

.tab-btn.active {
  background: linear-gradient(135deg, #2c5282 0%, #1e3a5f 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(44,82,130,0.3);
}

.tab-icon {
  width: 20px;
  height: 20px;
}

.tab-label {
  font-size: 0.95rem;
}

.tab-content {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.semaforo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  max-width: 900px;
}

.semaforo-card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 2px solid #e2e8f0;
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
  background: #22c55e;
}

.semaforo-indicator.near {
  background: #f59e0b;
}

.semaforo-indicator.full {
  background: #ef4444;
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

/* Hide any potential scrollbars just in case of sub-pixel rounding */
.table-container::-webkit-scrollbar {
  height: 0;
}
.table-container {
  scrollbar-width: none; /* Firefox */
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  table-layout: fixed;
}
/* Ensure padding is included within width to avoid overflow */
.data-table, .data-table th, .data-table td {
  box-sizing: border-box;
}

.data-table thead {
  /* Minimal flat header, brand color */
  background: #1e3a5f;
}

.data-table th {
  padding: 0.75rem 0.85rem;
  text-align: left;
  font-weight: 600;
  color: #fff;
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.data-table td {
  padding: 0.75rem 0.85rem;
  border-bottom: 1px solid #e2e8f0;
  color: #475569;
  vertical-align: middle;
  font-size: 0.9rem;
}

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

.progress-bar {
  position: relative;
  width: 100%;
  height: 28px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: width 0.3s ease;
}

.progress-fill.ok {
  background: linear-gradient(90deg, #22c55e, #16a34a);
}

.progress-fill.near {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-fill.full {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.progress-text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #1e293b;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.chart-canvas {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Gráfico de barras verticales */
.bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 300px;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  max-width: 120px;
}

.bar-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 250px;
}

.bar {
  position: relative;
  width: 35px;
  min-height: 20px;
  border-radius: 6px 6px 0 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 6px;
}

.bar:hover {
  filter: brightness(1.1);
  transform: scaleY(1.02);
}

.bar-capacidad {
  background: #3b82f6;
}

.bar-inscritos {
  background: #f59e0b;
}

.bar-value {
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.bar-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  text-align: center;
  max-width: 100%;
  word-wrap: break-word;
}

/* Gráfico de dona */
.donut-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.donut-svg {
  width: 200px;
  height: 200px;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
}

.donut-percent {
  font-size: 2rem;
  font-weight: 800;
  fill: #1e293b;
}

.donut-label {
  font-size: 0.875rem;
  font-weight: 600;
  fill: #64748b;
}

/* Leyenda de gráficos */
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
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

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .tabs-nav {
    flex-wrap: wrap;
  }

  .tab-btn {
    flex: 1 1 45%;
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

  .tab-btn {
    flex: 1 1 100%;
    font-size: 0.875rem;
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
