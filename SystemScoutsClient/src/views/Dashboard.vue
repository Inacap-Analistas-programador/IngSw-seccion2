<template>
  <div class="dashboard-container">
    <h2 class="titulo">Dashboard de Cursos Scouts</h2>

    <!-- === Gráfico Principal === -->
    <div class="grafico-container">
      <canvas id="graficoGeneral"></canvas>
    </div>

    <!-- === Lista de Cursos === -->
    <div class="lista-cursos">
      <h3>Cursos Registrados</h3>
      <table>
        <thead>
          <tr>
            <th>Nombre del Curso</th>
            <th>Encargado</th>
            <th>Recaudado</th>
            <th>Estimado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="curso in cursos"
            :key="curso.id"
            :class="evaluarCurso(curso)"
            @click="abrirPopup(curso)"
          >
            <td>{{ curso.nombre || 'Sin nombre' }}</td>
            <td>{{ curso.encargado || 'No asignado' }}</td>
            <td>${{ curso.monto_recaudado }}</td>
            <td>${{ curso.monto_estimado }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- === Popup Detalle del Curso === -->
    <div v-if="popupVisible" class="popup-overlay" @click.self="cerrarPopup">
      <div class="popup-contenido">
        <h3>Detalles del Curso</h3>
        <p><strong>Nombre:</strong> {{ cursoSeleccionado.nombre }}</p>
        <p><strong>Encargado:</strong> {{ cursoSeleccionado.encargado || 'No asignado' }}</p>
        <p><strong>Monto Estimado:</strong> ${{ cursoSeleccionado.monto_estimado }}</p>
        <p><strong>Monto Recaudado:</strong> ${{ cursoSeleccionado.monto_recaudado }}</p>
        <p><strong>Lugar:</strong> {{ cursoSeleccionado.lugar || 'No especificado' }}</p>
        <p><strong>Estado:</strong> {{ cursoSeleccionado.estado || 'Activo' }}</p>
        <button class="cerrar" @click="cerrarPopup">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const cursos = ref([])
const popupVisible = ref(false)
const cursoSeleccionado = ref({})

let chartInstance = null

async function cargarDatos() {
  try {
    const response = await fetch(`${API_BASE}/api/cursos/`)
    if (!response.ok) throw new Error(`Error HTTP ${response.status}`)
    const data = await response.json()
    cursos.value = data
    actualizarGrafico()
  } catch (err) {
    console.error("Error al cargar cursos:", err)
  }
}

function evaluarCurso(curso) {
  const progreso = curso.monto_estimado > 0
    ? (curso.monto_recaudado / curso.monto_estimado) * 100
    : 0
  const cumple = progreso >= 49 && curso.encargado
  return cumple ? 'curso-ok' : 'curso-alerta'
}

function abrirPopup(curso) {
  cursoSeleccionado.value = curso
  popupVisible.value = true
}

function cerrarPopup() {
  popupVisible.value = false
}

function actualizarGrafico() {
  if (!cursos.value.length) return

  const nombres = cursos.value.map(c => c.nombre)
  const estimado = cursos.value.map(c => c.monto_estimado)
  const recaudado = cursos.value.map(c => c.monto_recaudado)

  const ctx = document.getElementById('graficoGeneral').getContext('2d')

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: nombres,
      datasets: [
        {
          label: 'Monto Estimado',
          data: estimado,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
        },
        {
          label: 'Monto Recaudado',
          data: recaudado,
          backgroundColor: 'rgba(75, 192, 75, 0.8)',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        x: { title: { display: true, text: 'Cursos' } },
        y: {
          title: { display: true, text: 'Monto ($)' },
          beginAtZero: true,
        },
      },
    },
  })
}

onMounted(cargarDatos)
watch(cursos, actualizarGrafico)
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f4f6f8;
  min-height: 100vh;
}

.titulo {
  text-align: center;
  margin-bottom: 20px;
}

.grafico-container {
  width: 100%;
  height: 400px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  padding: 15px;
  margin-bottom: 30px;
}

.lista-cursos {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.lista-cursos table {
  width: 100%;
  border-collapse: collapse;
}

.lista-cursos th, .lista-cursos td {
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.lista-cursos tr:hover {
  cursor: pointer;
  opacity: 0.9;
}

.curso-ok {
  background-color: #e8f5e9; /* verde claro */
}

.curso-alerta {
  background-color: #fdecea; /* rojo claro */
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.popup-contenido {
  background: white;
  border-radius: 10px;
  padding: 25px;
  width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.cerrar {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
