<template>
  <div class="crud-cursos container">
    <!-- Encabezado principal de la página -->
    <header class="page-header">
      <h3>Gestión de Cursos</h3>
    </header>

    <section class="card cursos-card">
      <div class="card-body">
        <div class="title-row">
          <h4>Gestión de Cursos</h4>
          <BaseButton class="btn-success" @click="mostrarFormulario = !mostrarFormulario"><AppIcons name="plus" :size="16" /> Nuevo Curso</BaseButton>
        </div>

        <div class="filtros">
          <div class="filtros-left">
            <InputBase v-model="searchQuery" placeholder="Buscar por nombre o código..." @keydown.enter="filtrarCursos" />
          </div>
          <div class="filtros-right">
            <BaseButton class="btn-search" variant="primary" @click="filtrarCursos"><AppIcons name="search" :size="16" /> Buscar</BaseButton>
          </div>
        </div>

        <!-- Tabla de cursos -->
        <table class="courses-table">
          <thead>
            <tr>
              <th>Nombre del Curso</th>
              <th>Código</th>
              <th>Tipo</th>
              <th>Fechas del Curso</th>
              <th>Responsable</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, i) in paginatedCursos" :key="c.CURS_ID">
              <td>{{ c.CUR_DESCRIPCION }}</td>
              <td>{{ c.CUR_CODIGO }}</td>
              <td>{{ getTipoCursoText(c.CUR_TIPO_CURSO) }}</td>
              <td>{{ formatDates(c.fechaInicio, c.fechaTermino) }}</td>
              <td>{{ c.responsableNombre }}</td>
              <td>
                <span :class="['badge', getEstadoInfo(c.CUR_ESTADO).class]">
                  {{ getEstadoInfo(c.CUR_ESTADO).text }}
                </span>
              </td>
              <td class="actions-cell">
                <BaseButton class="btn-info" small @click="gestionarParticipantes(c.CURS_ID)"><AppIcons name="users" :size="14" /> Participantes</BaseButton>
                <BaseButton class="btn-warning" small @click="editarCurso(i)"><AppIcons name="edit" :size="14" /> Editar</BaseButton>
                <BaseButton class="btn-secondary" small @click="togglePreinscripcion(i)">
                  {{ c.habilitado ? 'Deshabilitar' : 'Habilitar' }}
                </BaseButton>
                <BaseButton class="btn-danger" small @click="eliminarCurso(i)"><AppIcons name="trash" :size="14" /> Eliminar</BaseButton>
              </td>
            </tr>
            <tr v-if="paginatedCursos.length === 0">
              <td colspan="7" class="no-results">No se encontraron cursos.</td>
            </tr>
          </tbody>
        </table>

        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1">
          <BaseButton @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Anterior</BaseButton>
          <span>Página {{ currentPage }} de {{ totalPages }}</span>
          <BaseButton @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">Siguiente</BaseButton>
        </div>


        <!-- Formulario de creación/edición -->
        <div class="create-card" v-if="mostrarFormulario">
          <h5>{{ modoEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</h5>
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre del Curso:</label>
              <InputBase type="text" placeholder="Ej: Formación de Dirigentes" v-model="form.nombre" />
            </div>
            <div class="form-group">
              <label>Código:</label>
              <InputBase type="text" placeholder="Ej: FD-001" v-model="form.codigo" />
            </div>
            <div class="form-group">
              <label>Fecha Inicio:</label>
              <InputBase type="date" v-model="form.fechaInicio" />
            </div>
            <div class="form-group">
              <label>Fecha Fin:</label>
              <InputBase type="date" v-model="form.fechaFin" />
            </div>
            <div class="form-group">
              <label>Responsable:</label>
              <BaseSelect v-model="form.responsable" :options="personas" placeholder="Seleccione un responsable" />
            </div>
            <div class="form-group">
              <label>Tipo de Curso:</label>
              <BaseSelect v-model="form.tipoCurso" :options="tiposCurso" placeholder="Seleccione un tipo" />
            </div>
            <div class="form-group">
              <label>Comuna (Lugar):</label>
              <BaseSelect v-model="form.comuna" :options="comunas" placeholder="Seleccione una comuna" />
            </div>
            <div class="form-group">
              <label>Modalidad:</label>
              <BaseSelect v-model="form.modalidad" :options="modalidadOptions" placeholder="Seleccione modalidad" />
            </div>
          </div>

          <div class="form-group">
            <label>Responsable:</label>
            <BaseSelect v-model="form.responsable" :options="personas" placeholder="Selecciona un responsable" />
          </div>

          <div class="hierarchy-section">
            <label>Equipo del Curso (Jerarquías):</label>
            <div class="coordinador-form">
              <BaseSelect v-model="nuevoCoordinador.persona" :options="personas" placeholder="Seleccionar Persona" class="select-persona" />
              <BaseSelect v-model="nuevoCoordinador.cargo" :options="cargos" placeholder="Seleccionar Cargo" class="select-cargo" />
              <BaseButton @click="agregarCoordinador" class="btn-success">Añadir al Equipo</BaseButton>
            </div>
            
            <table class="coordinador-table" v-if="form.coordinadores.length > 0">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Cargo</th>
                  <th>Acción</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(coord, index) in form.coordinadores" :key="index">
                  <td>{{ getPersonaNombre(coord.PER_ID) }}</td>
                  <td>{{ getCargoNombre(coord.CAR_ID) }}</td>
                  <td>
                    <BaseButton @click="eliminarCoordinador(index)" class="btn-danger" small>Eliminar</BaseButton>
                  </td>
                </tr>
              </tbody>
            </table>
            <p v-else class="no-coordinadores">Aún no se han añadido miembros al equipo.</p>
          </div>


          <div class="actions-row">
            <BaseButton class="btn-primary" @click="guardarCurso">
              {{ modoEdicion ? 'Actualizar' : 'Crear Curso' }}
            </BaseButton>
            <BaseButton class="btn-secondary" @click="cancelarFormulario">Cancelar</BaseButton>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import cursosService from '@/services/cursosService.js'
import personasService from '@/services/personasService.js'
import AppIcons from '@/components/icons/AppIcons.vue'

// Lista de cursos y personas
const cursos = reactive([])
const personas = ref([])

// Estado del formulario
const form = reactive({
  nombre: '',
  codigo: '',
  fechaInicio: '',
  fechaFin: '',
  responsable: null,
  tipoCurso: null,
  comuna: null,
  modalidad: null,
  coordinadores: []
})

// Opciones de selects (placeholder)
const tiposCurso = ref([
  { value: 1, label: 'Básico' },
  { value: 2, label: 'Especialidad' },
])
const comunas = ref([
  { value: 1, label: 'Comuna 1' },
  { value: 2, label: 'Comuna 2' },
])
const modalidadOptions = ref([
  { value: 1, label: 'Presencial' },
  { value: 2, label: 'Mixta' },
])
const cargos = ref([
  { value: 1, label: 'Coordinador' },
  { value: 2, label: 'Asistente' },
])

// Jerarquías/coordinadores
const nuevoCoordinador = reactive({ persona: null, cargo: null })
function agregarCoordinador() {
  if (!nuevoCoordinador.persona || !nuevoCoordinador.cargo) return
  form.coordinadores.push({ PER_ID: nuevoCoordinador.persona, CAR_ID: nuevoCoordinador.cargo })
  nuevoCoordinador.persona = null
  nuevoCoordinador.cargo = null
}
function eliminarCoordinador(index) {
  form.coordinadores.splice(index, 1)
}
function getPersonaNombre(id) {
  const p = personas.value.find(x => x.value === id)
  return p?.label || '-'
}
function getCargoNombre(id) {
  const c = cargos.value.find(x => x.value === id)
  return c?.label || '-'
}

// Filtros y paginación
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const cursosFiltrados = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) return cursos
  return cursos.filter(c =>
    (c.CUR_DESCRIPCION || '').toLowerCase().includes(query) ||
    (c.CUR_CODIGO || '').toLowerCase().includes(query)
  )
})
const totalPages = computed(() => Math.max(1, Math.ceil(cursosFiltrados.value.length / pageSize.value)))
const paginatedCursos = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return cursosFiltrados.value.slice(start, start + pageSize.value)
})
function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
}
function filtrarCursos() {
  currentPage.value = 1
}

// Control de visibilidad y modo
const mostrarFormulario = ref(false)
const modoEdicion = ref(false)
const indiceEdicion = ref(-1)

// Guardar curso (crear o actualizar)
async function guardarCurso() {
  if (!form.nombre || !form.codigo || !form.responsable) {
    alert('Por favor completa nombre, código y responsable')
    return
  }
  try {
    if (modoEdicion.value && indiceEdicion.value >= 0) {
      // Actualizar en servidor vía PATCH sólo los campos editados en el formulario.
      const cursoActual = cursos[indiceEdicion.value]
      const patch = {
        CUR_DESCRIPCION: form.nombre,
        CUR_CODIGO: form.codigo,
        ...(form.responsable ? { PER_ID_RESPONSABLE: form.responsable } : {}),
        ...(form.tipoCurso ? { CUR_TIPO_CURSO: form.tipoCurso } : {}),
        ...(form.modalidad ? { CUR_MODALIDAD: form.modalidad } : {}),
        ...(form.comuna ? { COM_ID_LUGAR: form.comuna } : {}),
      }
      await cursosService.actualizar(cursoActual.CURS_ID || cursoActual.id, patch)
      // Refrescar lista
      const data = await cursosService.listar()
      cursos.splice(0, cursos.length, ...((data || []).map(c => ({
        CURS_ID: c.id,
        CUR_DESCRIPCION: c.nombre || c.codigo || 'Curso',
        CUR_CODIGO: c.codigo || '-',
        CUR_TIPO_CURSO: null,
        fechaInicio: null,
        fechaTermino: null,
        responsableNombre: '-',
        CUR_ESTADO: c.estado ?? 1,
        habilitado: (c.estado === 1)
      }))))
      filtrarCursos()
      limpiarFormulario()
    } else {
      // Creación en servidor: el modelo requiere muchos campos obligatorios.
      // Mostramos aviso y evitamos desincronizar UI con backend.
      alert('La creación de cursos en el servidor requiere campos adicionales (usuario, tipo, comuna, modalidad, administración, cuotas, lugar, etc.). Agrega esos campos al formulario para habilitar el POST.')
      // TODO: cuando el formulario incluya todos los campos requeridos, enviar cursosService.crear(payload)
    }
  } catch (e) {
    console.error('Error guardando curso:', e)
    alert('No se pudo guardar el curso. Revisa los datos e inténtalo nuevamente.')
  }
}

// Editar curso existente
function editarCurso(index) {
  const curso = cursos[index]

  // Llenar el formulario con los datos del curso a editar
  form.nombre = curso.CUR_DESCRIPCION || ''
  form.codigo = curso.CUR_CODIGO || ''

  // Formatear la fecha para el input type="date" (YYYY-MM-DD)
  if (curso.CUR_FECHA_SOLICITUD) {
    form.fechaInicio = new Date(curso.CUR_FECHA_SOLICITUD).toISOString().split('T')[0]
  } else {
    form.fechaInicio = ''
  }
  // Asumimos que no hay fecha de fin en el modelo principal, se deja en blanco
  form.fechaFin = ''

  form.responsable = curso.PER_ID_RESPONSABLE || null
  form.coordinadores = [] // Este campo se puede desarrollar más adelante

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
  form.responsable = null
  form.tipoCurso = null
  form.comuna = null
  form.modalidad = null
  form.coordinadores = []
  mostrarFormulario.value = false
  modoEdicion.value = false
  indiceEdicion.value = -1
}

// Eliminar curso
async function eliminarCurso(index) {
  const curso = cursos[index]
  if (!curso) return
  const ok = confirm(`¿Eliminar el curso "${curso.CUR_DESCRIPCION || curso.CUR_CODIGO}"?`)
  if (!ok) return
  try {
    await cursosService.eliminar(curso.CURS_ID || curso.id)
    cursos.splice(index, 1)
    filtrarCursos()
  } catch (e) {
    console.error('Error eliminando curso:', e)
    alert('No se pudo eliminar el curso.')
  }
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

// Cargar cursos desde API al montar
onMounted(async () => {
  try {
    // Cargar cursos
    const data = await cursosService.listar()
    const mapped = (data || []).map(c => ({
      CURS_ID: c.id,
      CUR_DESCRIPCION: c.nombre || c.codigo || 'Curso',
      CUR_CODIGO: c.codigo || '-',
      CUR_TIPO_CURSO: null,
      fechaInicio: null,
      fechaTermino: null,
      responsableNombre: '-',
      CUR_ESTADO: c.estado ?? 1,
      habilitado: (c.estado === 1)
    }))
    cursos.splice(0, cursos.length, ...mapped)

    // Cargar personas para selects
    const pers = await personasService.listarBasic()
    personas.value = (pers || []).map(p => ({ value: p.id, label: p.nombre }))
  } catch (e) {
    console.warn('No se pudieron cargar cursos/personas desde API', e)
  }
})

// Helpers de presentación
function getTipoCursoText(t) {
  const found = tiposCurso.value.find(x => x.value === (Number(t) || t))
  return found?.label || '—'
}
function getEstadoInfo(estado) {
  const st = Number(estado)
  if (st === 1) return { class: 'badge-success', text: 'Vigente' }
  if (st === 0) return { class: 'badge-secondary', text: 'Inactivo' }
  return { class: 'badge-info', text: 'Desconocido' }
}
function gestionarParticipantes(id) {
  console.log('Gestionar participantes para curso', id)
}
</script>

<style scoped>
.crud-cursos {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px; 
  background: var(--color-surface);
  color: var(--color-text);
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: Arial, sans-serif;
  width: 1100px;                
  max-width: calc(100% - 48px);
  height: auto;
  max-height: calc(100vh - 48px);
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(16,24,40,0.08);
  overflow: hidden;            
}

.page-header {
  background-color: var(--color-primary);
  color: #fff;
  padding: 14px 18px;
  border-radius: 6px;
  margin: 0 0 4px 0;
}

.page-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}

.cursos-card {
  border: none;
  box-shadow: none;
}

.title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title-row h4 {
  margin: 0;
  color: var(--color-text);
  font-weight: 500;
}

.courses-table {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  background-color: var(--color-surface);
  min-width: 0; 
  font-size: 14px;
}

.courses-table th, .courses-table td {
  padding: 14px 12px;
  border-bottom: 1px solid var(--color-border);
  text-align: left;
  color: var(--color-text); 
  opacity: 1;
}

.courses-table th {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 2;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.badge-success {
  background:#d1fae5;
  color:#065f46;
}

.badge-warning {
  background:#fff4db;
  color:#8f5b00;
}

.badge-danger {
  background: #fde2e2;
  color: #9b1c1c;
}

.badge-info {
  background: #e0f2fe;
  color: #0c4a6e;
}

.badge-secondary {
  background: #f3f4f6;
  color: #4b5563;
}

.actions-cell {
  display: flex;
  gap: 6px;
}

.actions-cell .btn {
  padding: 4px 8px;
  font-size: 12px;
}

.no-results {
  text-align: center;
  padding: 32px;
  color: #6b7280;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  padding: 10px;
  background-color: var(--color-background-mute);
  border-radius: 8px;
}

.create-card {
  background: var(--color-background-soft); 
  border-radius: 6px;
  padding: 18px 18px 16px 18px;
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 15px;
  line-height: 1.4;
  margin-top: 16px;
}

.create-card h5 {
  margin: 0 0 10px 0;
  color: var(--color-primary);
  font-size: 20px;
  font-weight:700;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 4px;
  font-weight: 600;
  color: var(--color-text);
}

.hierarchy-section {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.hierarchy-section > label {
  display: block;
  margin-bottom: 12px;
  font-weight: 600;
  color: var(--color-text);
  font-size: 1.1em;
}

.coordinador-form {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  margin-bottom: 16px;
}

.coordinador-form .select-persona {
  flex: 2;
}

.coordinador-form .select-cargo {
  flex: 1;
}

.coordinador-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
}

.coordinador-table th, .coordinador-table td {
  padding: 8px 10px;
  border: 1px solid var(--color-border);
  text-align: left;
}

.coordinador-table th {
  background-color: var(--color-background-mute);
}

.no-coordinadores {
  color: #6b7280;
  font-style: italic;
  padding: 10px;
  background-color: var(--color-background-mute);
  border-radius: 4px;
  text-align: center;
}

.loading-indicator {
  text-align: center;
  padding: 40px;
  font-size: 1.2em;
  color: #6b7280;
}

.participantes-modal {
  padding: 10px;
}

.participantes-modal h4 {
  margin-top: 0;
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.inscripcion-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.participantes-table {
  width: 100%;
  border-collapse: collapse;
}

.participantes-table th, .participantes-table td {
  padding: 10px;
  border: 1px solid var(--color-border);
  text-align: left;
}

.participantes-table th {
  background-color: var(--color-background-mute);
}

.hierarchy {
  margin-top: 16px;
}
</style>

