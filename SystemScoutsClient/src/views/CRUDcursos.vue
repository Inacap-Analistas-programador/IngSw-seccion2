<template>
  <div class="crud-cursos container">
    <!-- Encabezado principal de la página -->
    <header class="page-header">
      <h3>CRUD Cursos</h3>
    </header>

    <section class="card cursos-card">
      <div class="card-body">
        <div class="title-row">
          <h4>Gestión de Cursos</h4>
          <button class="btn btn-success" @click="mostrarFormulario = !mostrarFormulario">
            + Nuevo Curso
          </button>
        </div>

        <!-- Tabla de cursos -->
        <table class="courses-table">
          <thead>
            <tr>
              <th>Nombre del Curso</th>
              <th>Código</th>
              <th>Fechas</th>
              <th>Responsable</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, i) in cursos" :key="i">
              <td>{{ c.nombre }}</td>
              <td>{{ c.codigo }}</td>
              <td>{{ c.fechas }}</td>
              <td>{{ c.responsable }}</td>
              <td>
                <span :class="['badge', c.habilitado ? 'badge-success' : 'badge-warning']">
                  {{ c.habilitado ? 'Habilitado' : 'No habilitado' }}
                </span>
              </td>
              <td>
                <button class="btn btn-warning" @click="editarCurso(i)">Editar</button>
                <button class="btn btn-primary" @click="togglePreinscripcion(i)">
                  {{ c.habilitado ? 'Deshabilitar' : 'Habilitar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Formulario de creación/edición -->
        <div class="create-card" v-if="mostrarFormulario">
          <h5>{{ modoEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</h5>
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre del Curso:</label>
              <input type="text" placeholder="Ej: Formación de Dirigentes" v-model="form.nombre" />
            </div>
            <div class="form-group">
              <label>Código:</label>
              <input type="text" placeholder="Ej: FD-001" v-model="form.codigo" />
            </div>
            <div class="form-group">
              <label>Fecha Inicio:</label>
              <input type="date" v-model="form.fechaInicio" />
            </div>
            <div class="form-group">
              <label>Fecha Fin:</label>
              <input type="date" v-model="form.fechaFin" />
            </div>
          </div>

          <div class="hierarchy">
            <label>Jerarquías del Curso:</label>
            <div class="checkboxes">
              <label><input type="checkbox" v-model="form.jerarquias" value="Director" /> Director</label>
              <label><input type="checkbox" v-model="form.jerarquias" value="Salud" /> Salud</label>
              <label><input type="checkbox" v-model="form.jerarquias" value="Administración" /> Administración</label>
              <label><input type="checkbox" v-model="form.jerarquias" value="Apoyo" /> Apoyo</label>
            </div>
          </div>

          <div class="actions-row">
            <button class="btn btn-primary" @click="guardarCurso">
              {{ modoEdicion ? 'Actualizar' : 'Crear Curso' }}
            </button>
            <button class="btn btn-secondary" @click="cancelarFormulario">Cancelar</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

// Lista de cursos
const cursos = reactive([
  { nombre: 'Formación de Dirigentes', codigo: 'FD-001', fechas: '15-17 Oct 2024', responsable: 'Juan Pérez', habilitado: true },
  { nombre: 'Curso de Especialidades', codigo: 'CE-002', fechas: '22-24 Nov 2024', responsable: 'María González', habilitado: false }
])

// Estado del formulario
const form = reactive({ 
  nombre: '', 
  codigo: '', 
  fechaInicio: '', 
  fechaFin: '', 
  jerarquias: [] 
})

// Control de visibilidad y modo
const mostrarFormulario = ref(false)
const modoEdicion = ref(false)
const indiceEdicion = ref(-1)

// Guardar curso (crear o actualizar)
function guardarCurso() {
  if (!form.nombre || !form.codigo) {
    alert('Por favor completa nombre y código')
    return
  }

  const cursoData = {
    nombre: form.nombre,
    codigo: form.codigo,
    fechas: formatDates(form.fechaInicio, form.fechaFin),
    responsable: form.responsable || '-',
    habilitado: false
  }

  if (modoEdicion.value) {
    // Actualizar curso existente
    Object.assign(cursos[indiceEdicion.value], cursoData)
  } else {
    // Crear nuevo curso
    cursos.push(cursoData)
  }

  limpiarFormulario()
}

// Editar curso existente
function editarCurso(index) {
  const curso = cursos[index]
  form.nombre = curso.nombre
  form.codigo = curso.codigo
  // Aquí podrías parsear las fechas si las guardas en formato ISO
  form.fechaInicio = ''
  form.fechaFin = ''
  form.jerarquias = []
  
  modoEdicion.value = true
  indiceEdicion.value = index
  mostrarFormulario.value = true
}

// Toggle de preinscripción
function togglePreinscripcion(index) {
  cursos[index].habilitado = !cursos[index].habilitado
}

// Cancelar y limpiar formulario
function cancelarFormulario() {
  limpiarFormulario()
}

// Limpiar formulario
function limpiarFormulario() {
  form.nombre = ''
  form.codigo = ''
  form.fechaInicio = ''
  form.fechaFin = ''
  form.jerarquias = []
  mostrarFormulario.value = false
  modoEdicion.value = false
  indiceEdicion.value = -1
}

// Formatear fechas
function formatDates(a, b) {
  if (!a && !b) return '-'
  if (a && b) return `${formatDate(a)} - ${formatDate(b)}`
  return formatDate(a || b)
}

function formatDate(d) {
  if (!d) return ''
  const dt = new Date(d)
  return dt.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric' })
}
</script>

<style scoped>
.crud-cursos { padding: 12px; }
.page-header { background: #2f6fbf; color: #fff; padding: 10px 16px; border-radius: 4px; margin-bottom: 16px; }
.page-header h3 { margin: 0; font-weight: 700; }
.cursos-card { border-radius: 6px; border: 1px solid #e6e6e6; box-shadow: 0 1px 0 rgba(0,0,0,0.03); }
.title-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.title-row h4 { margin: 0; }
.btn { padding: 6px 12px; border: none; border-radius: 4px; cursor: pointer; margin-right: 4px; }
.btn-success { background: #28a745; color: #fff; }
.btn-primary { background: #2b6fb0; color: #fff; }
.btn-warning { background: #f0ad4e; color: #fff; }
.btn-secondary { background: #6c757d; color: #fff; }

.courses-table { width: 100%; border-collapse: collapse; margin-bottom: 18px; }
.courses-table th, .courses-table td { padding: 12px 10px; border-bottom: 1px solid #eee; text-align: left; }
.courses-table thead th { background: #fafafa; font-weight: 700; }
.badge { display: inline-block; padding: 6px 10px; border-radius: 12px; font-size: 13px; }
.badge-success { background: #dff0d8; color: #3c763d; }
.badge-warning { background: #fcf8e3; color: #8a6d3b; }

.create-card { background: #f7f7f7; border: 1px solid #e6e6e6; padding: 14px; border-radius: 6px; margin-top: 16px; }
.create-card h5 { color: #2b6fb0; margin-top: 0; margin-bottom: 10px; }
.form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }
.form-group { display: flex; flex-direction: column; }
.form-group input[type="text"], .form-group input[type="date"] { padding: 8px; border-radius: 4px; border: 1px solid #dcdcdc; }
.hierarchy { margin: 8px 0; }
.checkboxes { display: flex; gap: 12px; margin-top: 6px; flex-wrap: wrap; }
.checkboxes label { display: flex; align-items: center; gap: 6px; cursor: pointer; }
.actions-row { margin-top: 10px; display: flex; gap: 10px; }

@media (max-width: 800px) {
  .form-grid { grid-template-columns: 1fr 1fr; }
}
</style>