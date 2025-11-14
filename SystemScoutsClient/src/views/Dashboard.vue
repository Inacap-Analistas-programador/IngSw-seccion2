<template>
  <div class="dashboard-container">
    <h1 class="titulo">Dashboard de Cursos</h1>

    <!-- === Gráfico Principal === -->
    <div class="grafico-container">
      <canvas ref="graficoCanvas" width="800" height="400"></canvas>
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

const cursos = ref([])
const cursoSeleccionado = ref(null)
const graficoCanvas = ref(null)

function formatearMonto(monto) {
  return `$${monto.toLocaleString('es-CL')}`
}

async function cargarDatos() {
  try {
    const listaCursos = await cursosService.cursos.list()

    const datosCompletos = await Promise.all(
      listaCursos.map(async (curso) => {
        const cuotas = await cursosService.cuotas.list({ curso: curso.id })
        const montoEstimado = cuotas.reduce((s, c) => s + (c.monto_total || 0), 0)
        const montoRecaudado = cuotas.reduce((s, c) => s + (c.monto_pagado || 0), 0)
        const porcentaje = montoEstimado > 0 ? (montoRecaudado / montoEstimado) * 100 : 0

        // Buscar responsable (si existe)
        const coordinadores = await cursosService.coordinadores.list({ curso: curso.id })
        const responsable = coordinadores[0]?.nombre || null

        return {
          id: curso.id,
          nombre: curso.nombre || 'Curso sin nombre',
          lugar: curso.lugar || '',
          montoEstimado,
          montoRecaudado,
          porcentaje,
          responsable,
        }
      })
    )

    cursos.value = datosCompletos
    await nextTick()
    dibujarGrafico()
  } catch (error) {
    console.error('Error al cargar datos:', error)
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

    // Nombres cursos
    ctx.fillStyle = '#000'
    ctx.font = '11px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(curso.nombre, x + anchoBarra / 2, alto + padding + 15)
  })
}

function mostrarDetalles(curso) {
  cursoSeleccionado.value = curso
}

function cerrarPopup() {
  cursoSeleccionado.value = null
}

onMounted(() => {
  cargarDatos()
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
</style>
