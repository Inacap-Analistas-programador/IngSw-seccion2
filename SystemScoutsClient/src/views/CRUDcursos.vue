<template>
  <div class="crud-cursos-container">
    <div class="page-header">
      <h3>Gestión de Cursos</h3>
      <p>Administra, crea y organiza los cursos de formación.</p>
    </div>

    <!-- Filtros y Acciones -->
    <div class="filters-card">
      <div class="filter-grid">
        <InputBase v-model="filtros.searchQuery" placeholder="Buscar por nombre o código..." />
        <BaseSelect v-model="filtros.estado" :options="opcionesEstado" placeholder="Filtrar por estado" optionLabel="text" />
        <BaseSelect v-model="filtros.tipoCurso" :options="tiposCursoOptions" placeholder="Filtrar por tipo" optionLabel="text" />
        <BaseSelect v-model="filtros.responsable" :options="personasOptions" placeholder="Filtrar por responsable" optionLabel="text" />
      </div>
      <BaseButton @click="abrirModalCrear" class="create-button">+ Nuevo Curso</BaseButton>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      Cargando datos...
    </div>

    <!-- Tabla de Cursos -->
    <div v-else class="table-container">
      <table class="courses-table">
        <thead>
          <tr>
            <th>Descripción</th>
            <th>Código</th>
            <th>Tipo</th>
            <th>Fechas</th>
            <th>Responsable</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in cursosPaginados" :key="c.CUR_ID">
            <td>{{ c.CUR_DESCRIPCION || '-' }}</td>
            <td>{{ c.CUR_CODIGO || '-' }}</td>
            <td>{{ getTipoCursoName(c.TCU_ID) }}</td>
            <td>{{ formatDates(c) }}</td>
            <td>{{ getPersonaName(c.PER_ID_RESPONSABLE) }}</td>
            <td><span :class="['badge', getEstadoClass(c.CUR_ESTADO)]">{{ getEstadoText(c.CUR_ESTADO) }}</span></td>
            <td class="actions-cell">
              <BaseButton @click="abrirModalEditar(c)" variant="secondary" size="sm">Editar</BaseButton>
              <BaseButton @click="confirmarEliminacion(c.CUR_ID)" variant="danger" size="sm">Eliminar</BaseButton>
              <BaseButton @click="abrirModalSecciones(c)" variant="tertiary" size="sm">Secciones</BaseButton>
            </td>
          </tr>
          <tr v-if="cursosPaginados.length === 0">
            <td colspan="7" class="no-results">No se encontraron cursos que coincidan con los filtros.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    <div class="pagination">
      <BaseButton :disabled="currentPage === 1" @click="currentPage--">Anterior</BaseButton>
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      <BaseButton :disabled="currentPage === totalPages" @click="currentPage++">Siguiente</BaseButton>
    </div>

    <!-- Modal de Creación/Edición de Curso -->
    <BaseModal v-model="mostrarModal" @close="cerrarModal">
      <template #title>{{ esEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</template>
      <div class="modal-body">
        <div class="form-grid-modal">
          <!-- Campos del formulario -->
          <div class="form-group span-2"><label>Descripción del curso</label><InputBase v-model="form.CUR_DESCRIPCION" /></div>
          <div class="form-group"><label>Código</label><InputBase v-model="form.CUR_CODIGO" /></div>
          <div class="form-group"><label>Tipo de Curso</label><BaseSelect v-model="form.TCU_ID" :options="tiposCursoOptions" optionLabel="text" /></div>
          <div class="form-group"><label>Responsable</label><BaseSelect v-model="form.PER_ID_RESPONSABLE" :options="personasOptions" optionLabel="text" /></div>
          <div class="form-group"><label>Fecha de Solicitud</label><InputBase type="date" v-model="form.CUR_FECHA_SOLICITUD" /></div>
          <div class="form-group"><label>Estado</label><BaseSelect v-model="form.CUR_ESTADO" :options="opcionesEstado" optionLabel="text" /></div>
          <div class="form-group"><label>Cuota con Almuerzo</label><InputBase type="number" v-model="form.CUR_COTA_CON_ALMUERZO" /></div>
          <div class="form-group"><label>Cuota sin Almuerzo</label><InputBase type="number" v-model="form.CUR_COTA_SIN_ALMUERZO" /></div>
          <div class="form-group"><label>Modalidad</label><BaseSelect v-model="form.CUR_MODALIDAD" :options="opcionesModalidad" optionLabel="text" /></div>
          <div class="form-group"><label>Tipo (Presencial/Online)</label><BaseSelect v-model="form.CUR_TIPO_CURSO" :options="opcionesTipoPresencial" optionLabel="text" /></div>
          <div class="form-group span-2"><label>Lugar</label><InputBase v-model="form.CUR_LUGAR" /></div>
          
          <!-- Mapa Interactivo -->
          <div class="form-group span-2">
            <label>Ubicación (haz clic en el mapa para seleccionar)</label>
            <MapEmbed 
              :lat="form.CUR_COORD_LATITUD" 
              :lng="form.CUR_COORD_LONGITUD"
              @update:lat="form.CUR_COORD_LATITUD = $event"
              @update:lng="form.CUR_COORD_LONGITUD = $event"
            />
          </div>
          <div class="form-group"><label>Latitud</label><InputBase v-model="form.CUR_COORD_LATITUD" readonly /></div>
          <div class="form-group"><label>Longitud</label><InputBase v-model="form.CUR_COORD_LONGITUD" readonly /></div>

          <div class="form-group span-2"><label>Observaciones</label><textarea v-model="form.CUR_OBSERVACION" rows="3"></textarea></div>
        </div>

        <!-- Sección de Gestión de Fechas -->
        <div class="fechas-section" v-if="esEdicion">
          <hr class="section-divider">
          <h4>Períodos del Curso</h4>
          
          <!-- Tabla de Fechas Existentes -->
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Inicio</th>
                <th>Término</th>
                <th>Tipo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="fechasCurso.length === 0">
                <td colspan="4" class="no-results-small">No hay períodos definidos.</td>
              </tr>
              <tr v-for="fecha in fechasCurso" :key="fecha.CUF_ID">
                <td>{{ formatDateSimple(fecha.CUF_FECHA_INICIO) }}</td>
                <td>{{ formatDateSimple(fecha.CUF_FECHA_TERMINO) }}</td>
                <td>{{ opcionesTipoFecha.find(t => t.value === fecha.CUF_TIPO)?.text }}</td>
                <td>
                  <BaseButton @click="eliminarFecha(fecha.CUF_ID)" variant="danger" size="sm">Eliminar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Formulario para Añadir Nueva Fecha -->
          <div class="add-fecha-form">
            <div class="form-group">
              <label>Fecha Inicio</label>
              <InputBase type="date" v-model="nuevoPeriodo.CUF_FECHA_INICIO" />
            </div>
            <div class="form-group">
              <label>Fecha Término</label>
              <InputBase type="date" v-model="nuevoPeriodo.CUF_FECHA_TERMINO" />
            </div>
            <div class="form-group">
              <label>Tipo</label>
              <BaseSelect v-model="nuevoPeriodo.CUF_TIPO" :options="opcionesTipoFecha" optionLabel="text" />
            </div>
            <BaseButton @click="agregarFecha" class="add-button">Añadir Período</BaseButton>
          </div>
        </div>

      </div>
      <template #footer>
        <BaseButton @click="cerrarModal" variant="secondary">Cancelar</BaseButton>
        <BaseButton @click="guardarCurso">Guardar Cambios</BaseButton>
      </template>
    </BaseModal>

    <!-- Modal de Gestión de Secciones -->
    <BaseModal v-model="mostrarModalSecciones" @close="cerrarModalSecciones">
      <template #title>Gestionar Secciones del Curso</template>
      <div class="modal-body">
        <p v-if="cursoSeleccionado"><strong>Curso:</strong> {{ cursoSeleccionado.CUR_DESCRIPCION }}</p>
        
        <!-- Tabla de Secciones Existentes -->
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Sección N°</th>
              <th>Rama</th>
              <th>N° Participantes</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="seccionesCurso.length === 0">
              <td colspan="4" class="no-results-small">No hay secciones definidas para este curso.</td>
            </tr>
            <tr v-for="seccion in seccionesCurso" :key="seccion.CUS_ID">
              <td>{{ seccion.CUS_SECCION }}</td>
              <td>{{ getRamaName(seccion.RAM_ID) }}</td>
              <td>{{ seccion.CUS_CANT_PARTICIPANTE }}</td>
              <td>
                <BaseButton @click="eliminarSeccion(seccion.CUS_ID)" variant="danger" size="sm">Eliminar</BaseButton>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Formulario para Añadir Nueva Sección -->
        <div class="add-fecha-form section-divider">
          <div class="form-group">
            <label>N° de Sección</label>
            <InputBase type="number" v-model="nuevaSeccion.CUS_SECCION" />
          </div>
          <div class="form-group">
            <label>Rama</label>
            <BaseSelect v-model="nuevaSeccion.RAM_ID" :options="ramasOptions" optionLabel="text" />
          </div>
          <div class="form-group">
            <label>N° Participantes</label>
            <InputBase type="number" v-model="nuevaSeccion.CUS_CANT_PARTICIPANTE" />
          </div>
          <BaseButton @click="agregarSeccion" class="add-button">Añadir Sección</BaseButton>
        </div>
      </div>
      <template #footer>
        <BaseButton @click="cerrarModalSecciones" variant="secondary">Cerrar</BaseButton>
      </template>
    </BaseModal>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
// Se comentan los servicios reales
// import { cursos, fechas } from '@/services/cursosService.js'
// import { personas } from '@/services/personasService.js'
// import mantenedores from '@/services/mantenedoresService.js'

// Se importan los datos estáticos
import { mockCursos, mockPersonas, mockTiposCurso, mockRamas, mockSecciones } from '@/services/mockData.js'

import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import MapEmbed from '@/components/Reutilizables/MapEmbed.vue'

// --- Estado y Reactividad ---
const isLoading = ref(true)
const cursosList = ref([])
const personasList = ref([])
const tiposCursoList = ref([])
const fechasCurso = ref([])
const ramaslist = ref([]) // Para el modal de secciones
const seccionesList = ref([]) // Lista completa de secciones
const seccionesCurso = ref([]) // Secciones del curso seleccionado
const mostrarModalSecciones = ref(false)
const cursoSeleccionado = ref(null)

const mostrarModal = ref(false)
const esEdicion = ref(false)
const isTrulyNew = ref(false) // Para diferenciar un nuevo curso de uno existente

const currentPage = ref(1)
const itemsPerPage = ref(10)

const filtros = ref({
  searchQuery: '',
  estado: null,
  tipoCurso: null,
  responsable: null,
})

const form = ref(null)

const inicializarFormulario = () => ({
  CUR_ID: null,
  CUR_DESCRIPCION: 'Curso de Liderazgo Juvenil',
  CUR_CODIGO: 'CUR-2025-01',
  TCU_ID: null, // Se mantiene nulo para forzar la selección
  PER_ID_RESPONSABLE: null, // Se mantiene nulo para forzar la selección
  CUR_FECHA_SOLICITUD: new Date().toISOString().split('T')[0], // Sugiere la fecha de hoy
  CUR_COTA_CON_ALMUERZO: 25000,
  CUR_COTA_SIN_ALMUERZO: 20000,
  CUR_MODALIDAD: 1, // Internado
  CUR_TIPO_CURSO: 1, // Presencial
  CUR_LUGAR: 'Campo Escuela "El Canelo"',
  CUR_COORD_LATITUD: '-33.5983',
  CUR_COORD_LONGITUD: '-70.5211',
  CUR_ESTADO: 0, // Pendiente
  CUR_OBSERVACION: 'Curso de ejemplo para demostración de la funcionalidad.',
})

form.value = inicializarFormulario()

// --- Opciones para Selects (deberían ser dinámicas o constantes) ---
const opcionesEstado = [
  { value: 0, text: 'Pendiente' },
  { value: 1, text: 'Vigente' },
  { value: 2, text: 'Anulado' },
  { value: 3, text: 'Finalizado' },
]
const opcionesModalidad = [
  { value: 1, text: 'Internado' },
  { value: 2, text: 'Externado' },
  { value: 3, text: 'Internado/Externado' },
]
const opcionesTipoPresencial = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]
const opcionesTipoFecha = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]

// --- Lógica de Carga de Datos ---
async function cargarDatos() {
  isLoading.value = true
  try {
    // Simular una pequeña demora de red
    await new Promise(resolve => setTimeout(resolve, 500))

    // Cargar datos desde el archivo mock
    cursosList.value = JSON.parse(JSON.stringify(mockCursos)) // Usar JSON para crear una copia profunda y evitar mutaciones
    personasList.value = mockPersonas
    tiposCursoList.value = mockTiposCurso
    ramaslist.value = mockRamas
    seccionesList.value = JSON.parse(JSON.stringify(mockSecciones))

  } catch (e) {
    console.error('Error cargando datos estáticos:', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(cargarDatos)

// --- Lógica de Filtros y Paginación ---
const cursosFiltrados = computed(() => {
  let items = cursosList.value
  const { searchQuery, estado, tipoCurso, responsable } = filtros.value

  if (searchQuery) {
    const q = searchQuery.toLowerCase()
    items = items.filter(c => 
      (c.CUR_DESCRIPCION || '').toLowerCase().includes(q) ||
      (c.CUR_CODIGO || '').toLowerCase().includes(q)
    )
  }
  if (estado !== null) {
    items = items.filter(c => c.CUR_ESTADO === estado)
  }
  if (tipoCurso !== null) {
    items = items.filter(c => c.TCU_ID === tipoCurso)
  }
  if (responsable !== null) {
    items = items.filter(c => c.PER_ID_RESPONSABLE === responsable)
  }
  return items
})

const totalPages = computed(() => Math.max(1, Math.ceil(cursosFiltrados.value.length / itemsPerPage.value)))

const cursosPaginados = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return cursosFiltrados.value.slice(start, start + itemsPerPage.value)
})

watch(totalPages, (newTotal) => {
  if (currentPage.value > newTotal) {
    currentPage.value = newTotal
  }
})

// --- Lógica del Modal de Secciones ---
const nuevaSeccion = ref({
  CUS_SECCION: 1,
  RAM_ID: null,
  CUS_CANT_PARTICIPANTE: 20,
})

const ramasOptions = computed(() => 
  ramaslist.value.map(r => ({ value: r.RAM_ID, text: r.RAM_DESCRIPCION }))
)

function getRamaName(id) {
  const rama = ramaslist.value.find(r => r.RAM_ID === id)
  return rama ? rama.RAM_DESCRIPCION : 'No definida'
}

function abrirModalSecciones(curso) {
  cursoSeleccionado.value = curso
  // Filtrar las secciones que pertenecen al curso seleccionado
  seccionesCurso.value = seccionesList.value.filter(s => s.CUR_ID === curso.CUR_ID)
  mostrarModalSecciones.value = true
}

function cerrarModalSecciones() {
  mostrarModalSecciones.value = false
  cursoSeleccionado.value = null
}

function agregarSeccion() {
  if (!nuevaSeccion.value.RAM_ID) {
    alert('Debe seleccionar una rama.')
    return
  }
  
  const seccion = {
    CUS_ID: Date.now(), // ID temporal
    CUR_ID: cursoSeleccionado.value.CUR_ID,
    ...nuevaSeccion.value
  }
  
  seccionesList.value.push(seccion) // Añadir a la lista global
  seccionesCurso.value.push(seccion) // Añadir a la lista del modal

  // Limpiar formulario
  nuevaSeccion.value.CUS_SECCION = Math.max(...seccionesCurso.value.map(s => s.CUS_SECCION), 0) + 1
  nuevaSeccion.value.RAM_ID = null
}

function eliminarSeccion(seccionId) {
  if (!window.confirm('¿Seguro que desea eliminar esta sección?')) return

  seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
  seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
}


// --- Lógica del Modal (Crear/Editar) ---
async function abrirModalCrear() {
  form.value = inicializarFormulario()
  form.value.CUR_ID = Date.now() // Asignar un ID temporal para la gestión local
  isTrulyNew.value = true
  esEdicion.value = true // Activar modo "edición" para mostrar las sub-secciones
  fechasCurso.value = []
  seccionesCurso.value = []
  mostrarModal.value = true
}

async function abrirModalEditar(curso) {
  isTrulyNew.value = false
  esEdicion.value = true
  form.value = {
    ...curso,
    CUR_FECHA_SOLICITUD: curso.CUR_FECHA_SOLICITUD ? curso.CUR_FECHA_SOLICITUD.split('T')[0] : '',
  }
  await cargarFechasDelCurso(curso.CUR_ID)
  mostrarModal.value = true
}

function cerrarModal() {
  mostrarModal.value = false
}

// --- Lógica de Fechas del Curso ---
const nuevoPeriodo = ref({
  CUF_FECHA_INICIO: '',
  CUF_FECHA_TERMINO: '',
  CUF_TIPO: 1,
})

async function cargarFechasDelCurso(cursoId) {
  if (!cursoId) {
    fechasCurso.value = []
    return
  }
  // Simulación: encontrar las fechas en los datos estáticos
  const curso = cursosList.value.find(c => c.CUR_ID === cursoId)
  fechasCurso.value = curso ? JSON.parse(JSON.stringify(curso.fechas)) : []
}

async function agregarFecha() {
  if (!form.value.CUR_ID) {
    alert('Guarde primero el curso para poder añadirle fechas.')
    return
  }
  if (!nuevoPeriodo.value.CUF_FECHA_INICIO || !nuevoPeriodo.value.CUF_FECHA_TERMINO) {
    alert('Debe seleccionar fecha de inicio y término.')
    return
  }
  
  // Simulación: añadir la fecha a la lista local
  const nuevaFecha = {
    CUF_ID: Date.now(), // ID único temporal
    ...nuevoPeriodo.value,
    CUR_ID: form.value.CUR_ID,
  }
  fechasCurso.value.push(nuevaFecha)

  // Actualizar también la lista principal de cursos
  const cursoIndex = cursosList.value.findIndex(c => c.CUR_ID === form.value.CUR_ID)
  if (cursoIndex !== -1) {
    cursosList.value[cursoIndex].fechas.push(nuevaFecha)
  }

  nuevoPeriodo.value.CUF_FECHA_INICIO = ''
  nuevoPeriodo.value.CUF_FECHA_TERMINO = ''
}

async function eliminarFecha(fechaId) {
  if (!window.confirm('¿Seguro que desea eliminar este período?')) return
  
  // Simulación: eliminar de la lista local
  fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)

  // Actualizar también la lista principal de cursos
  const cursoIndex = cursosList.value.findIndex(c => c.CUR_ID === form.value.CUR_ID)
  if (cursoIndex !== -1) {
    cursosList.value[cursoIndex].fechas = cursosList.value[cursoIndex].fechas.filter(f => f.CUF_ID !== fechaId)
  }
}

// --- Lógica de Guardado Principal ---
async function guardarCurso() {
  try {
    const payload = { ...form.value }
    payload.CUR_COTA_CON_ALMUERZO = Number(payload.CUR_COTA_CON_ALMUERZO)
    payload.CUR_COTA_SIN_ALMUERZO = Number(payload.CUR_COTA_SIN_ALMUERZO)

    if (isTrulyNew.value) {
      // Simulación: añadir el nuevo curso a la lista
      const nuevoCurso = {
        ...payload,
        fechas: [...fechasCurso.value] // Adjuntar las fechas temporales
      }
      cursosList.value.unshift(nuevoCurso)
      isTrulyNew.value = false // Ya no es nuevo
    } else {
      // Simulación: encontrar y actualizar el curso en la lista
      const index = cursosList.value.findIndex(c => c.CUR_ID === payload.CUR_ID)
      if (index !== -1) {
        cursosList.value[index] = { 
          ...cursosList.value[index], 
          ...payload,
          fechas: [...fechasCurso.value] // Actualizar también las fechas
        }
      }
    }
    cerrarModal();
  } catch (e) {
    console.error('Error al guardar el curso (simulación):', e)
    alert('Error al guardar el curso. Revisa la consola para más detalles.')
  }
}

// --- Lógica de Eliminación ---
async function confirmarEliminacion(id) {
  if (!window.confirm('¿Estás seguro de que deseas eliminar este curso?')) return
  
  // Simulación: eliminar el curso de la lista
  cursosList.value = cursosList.value.filter(c => c.CUR_ID !== id)
  // No es necesario recargar datos
}

// --- Funciones de Formato y Ayuda ---
const personasOptions = computed(() => 
  personasList.value.map(p => ({ value: p.PER_ID, text: `${p.PER_NOMBRE} ${p.PER_APELLIDO_PATERNO}` }))
)

const tiposCursoOptions = computed(() => 
  tiposCursoList.value.map(tc => ({ value: tc.TCU_ID, text: tc.TCU_DESCRIPCION }))
)

function formatDates(curso) {
  if (curso.fechas && curso.fechas.length > 0) {
    const primera = curso.fechas[0].CUF_FECHA_INICIO
    const ultima = curso.fechas[curso.fechas.length - 1].CUF_FECHA_TERMINO
    return `${formatDateSimple(primera)} - ${formatDateSimple(ultima)} (${curso.fechas.length} per.)`
  }
  return 'Sin períodos'
}

function formatDateSimple(dateStr) {
  if (!dateStr) return '?'
  const opts = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString('es-CL', opts)
}

function getPersonaName(id) {
  const p = personasList.value.find(x => x.PER_ID === id)
  return p ? `${p.PER_NOMBRE} ${p.PER_APELLIDO_PATERNO}` : 'No asignado'
}

function getTipoCursoName(id) {
  const tc = tiposCursoList.value.find(x => x.TCU_ID === id)
  return tc ? tc.TCU_DESCRIPCION : 'No definido'
}

function getEstadoText(e) {
  return opcionesEstado.find(o => o.value === e)?.text || 'Desconocido'
}

function getEstadoClass(e) {
  const map = { 0: 'badge-warning', 1: 'badge-success', 2: 'badge-danger', 3: 'badge-secondary' }
  return map[e] || 'badge-dark'
}
</script>

<style scoped>
.crud-cursos-container {
  padding: 24px;
  background-color: #f9fafb;
  font-family: 'Inter', sans-serif;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
}

.filters-card {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  flex-grow: 1;
  margin-right: 16px;
}

.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow-x: auto;
}

.courses-table {
  width: 100%;
  border-collapse: collapse;
}

.courses-table th, .courses-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  font-size: 14px;
}

.courses-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.actions-cell {
  display: flex;
  gap: 8px;
}

.no-results {
  text-align: center;
  padding: 32px;
  color: #6b7280;
}

.loading-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  font-size: 16px;
  color: #6b7280;
  gap: 10px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.modal-body {
  padding: 24px;
}

.form-grid-modal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-group label {
  font-weight: 500;
  margin-bottom: 6px;
  font-size: 14px;
  color: #374151;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}
.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-warning { background-color: #fef3c7; color: #92400e; }
.badge-success { background-color: #d1fae5; color: #065f46; }
.badge-secondary { background-color: #f3f4f6; color: #4b5563; }
.badge-danger { background-color: #fee2e2; color: #991b1b; }
.badge-dark { background-color: #e5e7eb; color: #1f2937; }

/* Estilos para la sección de fechas */
.fechas-section {
  margin-top: 24px;
}
.section-divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 24px 0;
}
.fechas-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}
.fechas-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}
.fechas-table th, .fechas-table td {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  text-align: left;
  font-size: 14px;
}
.fechas-table th {
  background-color: #f9fafb;
}
.no-results-small {
  text-align: center;
  color: #6b7280;
  padding: 16px;
}
.add-fecha-form {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 16px;
  align-items: flex-end;
}
.add-button {
  height: fit-content;
}
</style>