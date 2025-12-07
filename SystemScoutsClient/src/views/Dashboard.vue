<template>
  <div class="dashboard-container">
    <ModernMainScrollbar>
      <div v-if="loading" class="alert info">Cargando datos...</div>
      <div v-if="loadError" class="alert error">Error cargando datos: {{ loadError }}</div>
      

      <!-- === Gráfico Principal === -->
      <div class="grafico-container">
          <canvas ref="graficoCanvas" width="800" height="400"></canvas>
          <div v-if="tooltip.visible" class="chart-tooltip" :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">{{ tooltip.text }}</div>
      </div>

      <!-- === Tabla de Cursos === -->
      <div class="tabla-container">
        <table class="tabla-cursos">
          <thead>
            <tr>
              <th>Curso</th>
              <th>Monto Estimado</th>
              <th>Monto Recaudado</th>
              <th>Responsable</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="curso in cursos"
              :key="curso.id"
              :class="{
                'curso-ok': curso.porcentaje >= 49 && curso.responsable,
                'curso-error': curso.porcentaje < 49 || !curso.responsable,
              }"
              @click="mostrarDetalles(curso)"
            >
              <td>{{ curso.nombre }}</td>
              <td>{{ formatearMonto(curso.montoEstimado) }}</td>
              <td>{{ formatearMonto(curso.montoRecaudado) }}</td>
              <td>{{ curso.responsable || 'No asignado' }}</td>
              <td>
                <span>{{ curso.porcentaje.toFixed(1) }}%</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </ModernMainScrollbar>

    <!-- === Popup Detalle Curso === -->
    <div v-if="cursoSeleccionado" class="modal-overlay" @click.self="cerrarPopup">
      <div class="modal-content">
        <h2>{{ cursoSeleccionado.nombre }}</h2>
        <p><strong>Lugar:</strong> {{ cursoSeleccionado.lugar || 'No especificado' }}</p>
        <p><strong>Responsable:</strong> {{ cursoSeleccionado.responsable || 'No asignado' }}</p>
        <p><strong>Monto Estimado:</strong> {{ formatearMonto(cursoSeleccionado.montoEstimado) }}</p>
        <p><strong>Monto Recaudado:</strong> {{ formatearMonto(cursoSeleccionado.montoRecaudado) }}</p>
        <p><strong>Porcentaje:</strong> {{ cursoSeleccionado.porcentaje.toFixed(1) }}%</p>
        <button class="boton-cerrar" @click="cerrarPopup">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import ModernMainScrollbar from '../components/ModernMainScrollbar.vue'
import cursosService from '@/services/cursosService.js'
import personasService from '@/services/personasService.js'

const cursos = ref([])
const cursoSeleccionado = ref(null)
const graficoCanvas = ref(null)
const loading = ref(false)
const loadError = ref(null)
const barras = ref([])
const tooltip = ref({ visible: false, text: '', x: 0, y: 0 })

function formatearMonto(monto) {
  return `$${monto.toLocaleString('es-CL')}`
}

async function cargarDatos() {
  try {
    loading.value = true
    loadError.value = null
    // 1. Cargar todos los catálogos en paralelo
    const [cursosResponse, cuotasResponse, coordinadoresResponse, personasResponse] = await Promise.all([
      cursosService.cursos.list({ page_size: 20 }),
      cursosService.cuotas.list(),
      cursosService.coordinadores.list(),
      personasService.personasCompletas.list()
    ]);

    // Debug: mostrar respuestas crudas en consola para verificar forma y status
    console.log('API responses:', { cursosResponse, cuotasResponse, coordinadoresResponse, personasResponse })

    const listaCursos = Array.isArray(cursosResponse) ? cursosResponse : cursosResponse.results || [];
    const todasLasCuotas = Array.isArray(cuotasResponse) ? cuotasResponse : cuotasResponse.results || [];
    const todosLosCoordinadores = Array.isArray(coordinadoresResponse) ? coordinadoresResponse : coordinadoresResponse.results || [];
    const todasLasPersonas = Array.isArray(personasResponse) ? personasResponse : personasResponse.results || [];

    // Normalizar campos que la API puede devolver con nombres distintos (CUR_ID, CUR_DESCRIPCION, CUU_VALOR, etc.)
    const cursosNorm = listaCursos.map(c => ({
      raw: c,
      id: c.id ?? c.CUR_ID ?? null,
      nombre: c.nombre ?? c.CUR_DESCRIPCION ?? c.CUR_CODIGO ?? 'Curso sin nombre',
      lugar: c.lugar ?? c.CUR_LUGAR ?? '',
      estado: Number(c.CUR_ESTADO ?? c.estado ?? c.CUR_ESTADO ?? -1),
    }))

    // Filtrar sólo cursos "vigente" (CUR_ESTADO === 1)
    const cursosVigentes = cursosNorm.filter(c => c.estado === 1)
    if (cursosVigentes.length !== cursosNorm.length) {
      console.log(`Filtrando cursos: ${cursosNorm.length} total, ${cursosVigentes.length} vigentes`)
    }

    const cuotasNorm = todasLasCuotas.map(q => ({
      raw: q,
      curso: q.curso ?? q.CUR_ID ?? (q.CUR_ID && (typeof q.CUR_ID === 'object' ? q.CUR_ID.CUR_ID : q.CUR_ID)) ?? null,
      monto_total: Number(q.monto_total ?? q.CUU_VALOR ?? q.CUU_VALOR ?? 0),
      monto_pagado: Number(q.monto_pagado ?? q.monto_pagado ?? 0),
    }))

    // 2. Procesar los datos en memoria usando campos normalizados
    const datosCompletos = cursosVigentes.map(curso => {
      const courseId = curso.id
      const cuotasDelCurso = cuotasNorm.filter(c => String(c.curso) === String(courseId))
      const montoEstimado = cuotasDelCurso.reduce((s, c) => s + (Number(c.monto_total) || 0), 0)
      const montoRecaudado = cuotasDelCurso.reduce((s, c) => s + (Number(c.monto_pagado) || 0), 0)
      const porcentaje = montoEstimado > 0 ? (montoRecaudado / montoEstimado) * 100 : 0

      const coordinador = todosLosCoordinadores.find(coord => {
        const coordCurso = coord.curso ?? coord.CUR_ID ?? null
        return String(coordCurso) === String(courseId)
      })
      let responsable = null
      if (coordinador) {
        const personaId = coordinador.persona ?? coordinador.PER_ID ?? null
        if (personaId) {
          const persona = todasLasPersonas.find(p => p.PER_ID == personaId || p.id == personaId)
          if (persona) {
            responsable = `${persona.PER_NOMBRES || persona.nombre || ''} ${persona.PER_APELPTA || ''}`.trim()
          }
        }
      }

      return { id: curso.id, nombre: curso.nombre || 'Curso sin nombre', lugar: curso.lugar || '', montoEstimado, montoRecaudado, porcentaje, responsable }
    })

    cursos.value = datosCompletos
    await nextTick()
    dibujarGrafico()
    loading.value = false
  } catch (error) {
    console.error('Error al cargar datos:', error)
    loadError.value = error.message || String(error)
    loading.value = false
  }
}

function dibujarGrafico() {
  const ctx = graficoCanvas.value.getContext('2d')
  ctx.clearRect(0, 0, graficoCanvas.value.width, graficoCanvas.value.height)

  const padding = 70
  const ancho = graficoCanvas.value.width - padding * 2
  const alto = graficoCanvas.value.height - padding * 2
  const n = cursos.value.length
  const maxValor = Math.max(...cursos.value.map((c) => c.montoEstimado), 1000)
  const anchoBarra = ancho / (n * 2)

  // Ejes
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, alto + padding)
  ctx.lineTo(ancho + padding, alto + padding)
  ctx.strokeStyle = '#333'
  ctx.stroke()

  // Eje Y (valores)
  ctx.font = '12px Arial'
  ctx.fillStyle = '#000'
  const pasos = 5
  for (let i = 0; i <= pasos; i++) {
    const y = alto + padding - (i * alto) / pasos
    const valor = Math.round((maxValor / pasos) * i)
    ctx.fillText(`$${valor.toLocaleString('es-CL')}`, 10, y + 4)
    ctx.beginPath()
    ctx.moveTo(padding - 5, y)
    ctx.lineTo(padding, y)
    ctx.stroke()
  }

  // Barras
  const localBarras = []
  cursos.value.forEach((curso, i) => {
    const x = padding + i * anchoBarra * 2 + anchoBarra / 2
    const alturaEstimado = (curso.montoEstimado / maxValor) * alto
    const alturaRecaudado = (curso.montoRecaudado / maxValor) * alto

    // Azul (estimado)
    ctx.fillStyle = 'rgba(0, 102, 255, 0.5)'
    ctx.fillRect(x, alto + padding - alturaEstimado, anchoBarra, alturaEstimado)

    // Verde (recaudado)
    ctx.fillStyle = 'rgba(0, 204, 102, 0.8)'
    ctx.fillRect(x, alto + padding - alturaRecaudado, anchoBarra, alturaRecaudado)

    // Nombres cursos (simplificados para evitar solapamiento)
    ctx.fillStyle = '#000'
    ctx.font = '11px Arial'
    ctx.textAlign = 'center'
    // Decide whether to draw this label based on density
    localBarras.push({ x: x, width: anchoBarra, curso })
  })

  // Store bar positions for tooltip/hit-testing
  barras.value = localBarras

  // No dibujamos etiquetas en el eje X: usamos tooltip para mostrar nombres completos al pasar el ratón.
}

function mostrarDetalles(curso) {
  cursoSeleccionado.value = curso
}

function cerrarPopup() {
  cursoSeleccionado.value = null
}

onMounted(() => {
  cargarDatos()
  // Attach canvas mouse handlers for tooltip
  // Use an interval to wait for the ref to be set if needed
  const attachHandlers = () => {
    const el = graficoCanvas.value
    if (!el) return
    function toCanvasPos(evt) {
      const rect = el.getBoundingClientRect()
      return { x: evt.clientX - rect.left, y: evt.clientY - rect.top }
    }
    function handleMouseMove(evt) {
      const pos = toCanvasPos(evt)
      const found = barras.value.find(b => {
        const left = b.x
        const right = b.x + b.width
        // bars are drawn at x with width anchoBarra; allow some tolerance
        return pos.x >= left - 2 && pos.x <= right + 2 && pos.y <= graficoCanvas.value.height
      })
      if (found) {
        tooltip.value.visible = true
        tooltip.value.text = found.curso.nombre || found.curso.CUR_DESCRIPCION || ''
        tooltip.value.x = evt.clientX
        tooltip.value.y = evt.clientY - 10
      } else {
        tooltip.value.visible = false
      }
    }
    function handleLeave() {
      tooltip.value.visible = false
    }
    el.addEventListener('mousemove', handleMouseMove)
    el.addEventListener('mouseleave', handleLeave)
    // store references so they aren't garbage-collected (not strictly necessary here)
    ;(el)._rs_handlers = { handleMouseMove, handleLeave }
  }
  // Try attach now and again in case canvas not yet rendered
  const tries = [0, 100, 300]
  for (const t of tries) setTimeout(attachHandlers, t)
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f4f6f8;
  font-family: 'Segoe UI', sans-serif;
}

.titulo {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.grafico-container {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  position: relative; /* allow absolute tooltip inside */
}

.tabla-container {
  background-color: #fff;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.tabla-cursos {
  width: 100%;
  border-collapse: collapse;
}

.tabla-cursos th,
.tabla-cursos td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.tabla-cursos th {
  background-color: #f0f0f0;
}

.curso-ok {
  background-color: #d5f5e3;
}

.curso-error {
  background-color: #f8d7da;
}

.curso-ok:hover,
.curso-error:hover {
  background-color: #eafaf1;
  cursor: pointer;
}

/* Popup modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  width: 400px;
  text-align: center;
}

.boton-cerrar {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  margin-top: 15px;
  border-radius: 6px;
  cursor: pointer;
}

.boton-cerrar:hover {
  background-color: #0056b3;
}

.chart-tooltip {
  position: fixed;
  pointer-events: none;
  background: rgba(0,0,0,0.8);
  color: #fff;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 2000;
  transform: translate(-50%, -100%);
  white-space: nowrap;
}
</style>
