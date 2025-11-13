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
      <div class="filters-actions">
        <BaseButton @click="aplicarFiltros" class="search-button">Buscar</BaseButton>
        <BaseButton @click="limpiarFiltros" variant="secondary">Limpiar</BaseButton>
        <BaseButton @click="abrirModalCrear" class="create-button">+ Nuevo Curso</BaseButton>
      </div>
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
          <tr v-for="c in cursosFiltrados" :key="c.CUR_ID">
            <td>{{ c.CUR_DESCRIPCION || '-' }}</td>
            <td>{{ c.CUR_CODIGO || '-' }}</td>
            <td>{{ getTipoCursoName(c.TCU_ID) }}</td>
            <td>{{ formatDates(c) }}</td>
            <td>{{ getPersonaName(c.PER_ID_RESPONSABLE) }}</td>
            <td><span :class="['badge', getEstadoClass(c.CUR_ESTADO)]">{{ getEstadoText(c.CUR_ESTADO) }}</span></td>
            <td class="actions-cell">
              <BaseButton @click="abrirModalEditar(c)" variant="secondary" size="sm">Editar</BaseButton>
              <BaseButton @click="deshabilitarCurso(c)" variant="danger" size="sm">Deshabilitar</BaseButton>
              <BaseButton @click="abrirModalVer(c)" variant="tertiary" size="sm">Ver</BaseButton>
            </td>
          </tr>
          <tr v-if="cursosFiltrados.length === 0">
            <td colspan="7" class="no-results">No se encontraron cursos que coincidan con los filtros.</td>
          </tr>
        </tbody>
      </table>
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
          <div class="form-group"><label>Administra</label><BaseSelect v-model="form.CUR_ADMINISTRA" :options="opcionesAdministra" optionLabel="text" /></div>
          <div class="form-group"><label>Comuna (lugar)</label><BaseSelect v-model="form.COM_ID_LUGAR" :options="comunasOptions" optionLabel="text" /></div>
          <div class="form-group"><label>Cargo Responsable</label><BaseSelect v-model="form.CAR_ID_RESPONSABLE" :options="cargosOptions" optionLabel="text" /></div>
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

          <!-- Sección de Gestión de Secciones -->
          <hr class="section-divider">
          <h4>Secciones del Curso</h4>
          
          <!-- Tabla de Secciones Existentes -->
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Sección</th>
                <th>Rama</th>
                <th>Participantes</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="seccionesCurso.length === 0">
                <td colspan="4" class="no-results-small">No hay secciones definidas.</td>
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
          <div class="add-fecha-form">
            <div class="form-group">
              <label>Sección #</label>
              <InputBase type="number" v-model="nuevaSeccion.CUS_SECCION" placeholder="Ej: 1, 2, 3..." />
            </div>
            <div class="form-group">
              <label>Rama</label>
              <BaseSelect v-model="nuevaSeccion.RAM_ID" :options="ramasOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Participantes</label>
              <InputBase type="number" v-model="nuevaSeccion.CUS_CANT_PARTICIPANTE" placeholder="Cantidad" />
            </div>
            <BaseButton @click="agregarSeccion" class="add-button">Añadir Sección</BaseButton>
          </div>
        </div>

      </div>
      <template #footer>
        <BaseButton @click="cerrarModal" variant="secondary">Cancelar</BaseButton>
        <BaseButton @click="guardarCurso">Guardar Cambios</BaseButton>
      </template>
    </BaseModal>

    <!-- Modal de Detalle de Curso -->
    <BaseModal v-model="mostrarModalVer" @close="cerrarModalVer">
      <template #title>Detalle del Curso</template>
      <div class="modal-body">
        <div v-if="cursoSeleccionado" class="detalle-curso">
          <p><strong>Descripción:</strong> {{ cursoSeleccionado.CUR_DESCRIPCION }}</p>
          <p><strong>Código:</strong> {{ cursoSeleccionado.CUR_CODIGO }}</p>
          <p><strong>Tipo:</strong> {{ getTipoCursoName(cursoSeleccionado.TCU_ID) }}</p>
          <p><strong>Responsable:</strong> {{ getPersonaName(cursoSeleccionado.PER_ID_RESPONSABLE) }}</p>
          <p><strong>Estado:</strong> {{ getEstadoText(cursoSeleccionado.CUR_ESTADO) }}</p>
          <p><strong>Lugar:</strong> {{ cursoSeleccionado.CUR_LUGAR }}</p>
          <p><strong>Coordenadas:</strong> {{ cursoSeleccionado.CUR_COORD_LATITUD }}, {{ cursoSeleccionado.CUR_COORD_LONGITUD }}</p>
          <p><strong>Observación:</strong> {{ cursoSeleccionado.CUR_OBSERVACION || '-' }}</p>
        </div>
        <h4 class="mt-16">Períodos</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Inicio</th>
              <th>Término</th>
              <th>Tipo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="fechasCurso.length === 0"><td colspan="3" class="no-results-small">Sin períodos</td></tr>
            <tr v-for="f in fechasCurso" :key="f.CUF_ID">
              <td>{{ formatDateSimple(f.CUF_FECHA_INICIO) }}</td>
              <td>{{ formatDateSimple(f.CUF_FECHA_TERMINO) }}</td>
              <td>{{ opcionesTipoFecha.find(t => t.value === f.CUF_TIPO)?.text }}</td>
            </tr>
          </tbody>
        </table>
        <h4 class="mt-16">Secciones</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Sección</th>
              <th>Rama</th>
              <th>Participantes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="seccionesCurso.length === 0"><td colspan="3" class="no-results-small">Sin secciones</td></tr>
            <tr v-for="s in seccionesCurso" :key="s.CUS_ID">
              <td>{{ s.CUS_SECCION }}</td>
              <td>{{ getRamaName(s.RAM_ID) }}</td>
              <td>{{ s.CUS_CANT_PARTICIPANTE }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <template #footer>
        <BaseButton @click="cerrarModalVer" variant="secondary">Cerrar</BaseButton>
      </template>
    </BaseModal>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { request } from '@/services/apiClient.js'
import { cursos as cursosApi, fechas as fechasApi, secciones as seccionesApi } from '@/services/cursosService.js'

import InputBase from '@/components/InputBase.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import MapEmbed from '@/components/MapEmbed.vue'

// --- Estado y Reactividad ---
const isLoading = ref(true)
const isLoadingData = ref(false) // Guard para prevenir cargas duplicadas
const cursosList = ref([])
const cursosFiltrados = ref([])
const personasList = ref([])
const tiposCursoList = ref([])
const fechasCurso = ref([])
const fechasCursoList = ref([]) // Caché de todas las fechas
const ramaslist = ref([])
const seccionesList = ref([])
const seccionesCurso = ref([])
const mostrarModalVer = ref(false)
const cursoSeleccionado = ref(null)

const mostrarModal = ref(false)
const esEdicion = ref(false)
const isTrulyNew = ref(false)
const isSaving = ref(false) // Bandera para prevenir múltiples clics
const isDisabling = ref(false) // Bandera para prevenir múltiples deshabilitar

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

// --- Cargar datos desde API ---
async function cargarDatos() {
  // Guard: prevenir múltiples cargas simultáneas (Vue 3 Strict Mode ejecuta setup 2x)
  if (isLoadingData.value) return
  isLoadingData.value = true
  isLoading.value = true
  
  try {
    const [cursosData, personasApi, tiposApi, ramasApi, seccionesData, fechasData, comunasApi, cargosApi] = await Promise.all([
      cursosApi.list(),
      request('personas/personas'),
      request('mantenedores/tipo-cursos'),
      request('mantenedores/rama'),
      seccionesApi.list().catch(() => []),
      fechasApi.list().catch(() => []),
      request('mantenedores/comuna').catch(() => []),
      request('mantenedores/cargo').catch(() => []),
    ])
    // Enlazar fechas a cada curso para mostrar rango en la tabla
    const fechasByCurso = (fechasData || []).reduce((acc, f) => {
      const id = f.CUR_ID
      if (!acc[id]) acc[id] = []
      acc[id].push(f)
      return acc
    }, {})
    cursosList.value = (cursosData || []).map(c => ({
      ...c,
      fechas: fechasByCurso[c.CUR_ID] ? fechasByCurso[c.CUR_ID].sort((a,b) => new Date(a.CUF_FECHA_INICIO) - new Date(b.CUF_FECHA_INICIO)) : []
    }))
    personasList.value = personasApi || []
    tiposCursoList.value = tiposApi || []
    ramaslist.value = ramasApi || []
    fechasCursoList.value = fechasData || [] // Guardar en caché
  seccionesList.value = seccionesData || []
  comunasList.value = comunasApi || []
  cargosList.value = cargosApi || []
    aplicarFiltros()
  } catch (e) {
    console.error('Error cargando datos desde API:', e)
    cursosList.value = []
    cursosFiltrados.value = []
  } finally {
    isLoading.value = false
    isLoadingData.value = false
  }
}

onMounted(cargarDatos)

// --- Filtros controlados por botón ---
function aplicarFiltros() {
  let items = [...cursosList.value]
  const { searchQuery, estado, tipoCurso, responsable } = filtros.value
  if (searchQuery) {
    const q = String(searchQuery).toLowerCase()
    items = items.filter(c => (c.CUR_DESCRIPCION || '').toLowerCase().includes(q) || (c.CUR_CODIGO || '').toLowerCase().includes(q))
  }
  if (estado !== null && estado !== undefined && estado !== '') items = items.filter(c => Number(c.CUR_ESTADO) === Number(estado))
  if (tipoCurso !== null && tipoCurso !== undefined && tipoCurso !== '') items = items.filter(c => Number(c.TCU_ID) === Number(tipoCurso))
  if (responsable !== null && responsable !== undefined && responsable !== '') items = items.filter(c => Number(c.PER_ID_RESPONSABLE) === Number(responsable))
  cursosFiltrados.value = items
}

function limpiarFiltros() {
  filtros.value = { searchQuery: '', estado: null, tipoCurso: null, responsable: null }
  aplicarFiltros()
}

const ramasOptions = computed(() => ramaslist.value.map(r => ({ value: r.RAM_ID, text: r.RAM_DESCRIPCION })))

function getRamaName(id) {
  const rama = ramaslist.value.find(r => r.RAM_ID === id)
  return rama ? rama.RAM_DESCRIPCION : 'No definida'
}


// --- Lógica del Modal (Crear/Editar) ---
async function abrirModalCrear() {
  form.value = inicializarFormulario()
  isTrulyNew.value = true
  esEdicion.value = true // Activar modo "edición" para mostrar las sub-secciones
  fechasCurso.value = []
  seccionesCurso.value = []
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
  nuevaSeccion.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
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
  await cargarSeccionesDelCurso(curso.CUR_ID)
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
  nuevaSeccion.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
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

// --- Lógica de Fechas del Curso ---
async function cargarFechasDelCurso(cursoId) {
  if (!cursoId) {
    fechasCurso.value = []
    return
  }
  try {
    // Solo cargar si aún no tenemos fechas en caché
    if (!Array.isArray(fechasCursoList.value) || fechasCursoList.value.length === 0) {
      const todas = await fechasApi.list()
      fechasCursoList.value = todas || []
    }
    fechasCurso.value = (fechasCursoList.value || []).filter(f => Number(f.CUR_ID) === Number(cursoId))
  } catch (e) {
    console.error('Error cargando fechas:', e)
    fechasCurso.value = []
  }
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
  
  const creada = await fechasApi.create({ ...nuevoPeriodo.value, CUR_ID: form.value.CUR_ID })
  fechasCurso.value.push(creada)
  fechasCursoList.value.push(creada) // Actualizar caché

  nuevoPeriodo.value.CUF_FECHA_INICIO = ''
  nuevoPeriodo.value.CUF_FECHA_TERMINO = ''
  alert('Período agregado exitosamente.')
}

async function eliminarFecha(fechaId) {
  if (!window.confirm('¿Seguro que desea eliminar este período?')) return
  
  await fechasApi.remove(fechaId)
  fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)
  fechasCursoList.value = fechasCursoList.value.filter(f => f.CUF_ID !== fechaId) // Actualizar caché
  alert('Período eliminado exitosamente.')
}

// --- Lógica de Secciones del Curso ---
const nuevaSeccion = ref({
  CUS_SECCION: '',
  RAM_ID: null,
  CUS_CANT_PARTICIPANTE: '',
})

async function cargarSeccionesDelCurso(cursoId) {
  try {
    if (!Array.isArray(seccionesList.value) || seccionesList.value.length === 0) {
      const all = await seccionesApi.list()
      seccionesList.value = all || []
    }
    seccionesCurso.value = (seccionesList.value || []).filter(s => Number(s.CUR_ID) === Number(cursoId))
  } catch (e) {
    console.error('Error cargando secciones:', e)
    seccionesCurso.value = []
  }
}

async function agregarSeccion() {
  if (!form.value.CUR_ID) {
    alert('Guarde primero el curso para poder añadirle secciones.')
    return
  }
  if (!nuevaSeccion.value.CUS_SECCION || !nuevaSeccion.value.RAM_ID || !nuevaSeccion.value.CUS_CANT_PARTICIPANTE) {
    alert('Debe llenar todos los campos de la sección.')
    return
  }
  
  const payload = {
    CUR_ID: form.value.CUR_ID,
    CUS_SECCION: Number(nuevaSeccion.value.CUS_SECCION),
    RAM_ID: Number(nuevaSeccion.value.RAM_ID),
    CUS_CANT_PARTICIPANTE: Number(nuevaSeccion.value.CUS_CANT_PARTICIPANTE)
  }
  
  const creada = await seccionesApi.create(payload)
  seccionesCurso.value.push(creada)
  seccionesList.value.push(creada)

  nuevaSeccion.value.CUS_SECCION = ''
  nuevaSeccion.value.RAM_ID = null
  nuevaSeccion.value.CUS_CANT_PARTICIPANTE = ''
  
  alert('Sección agregada exitosamente.')
}

async function eliminarSeccion(seccionId) {
  if (!window.confirm('¿Seguro que desea eliminar esta sección?')) return
  
  await seccionesApi.remove(seccionId)
  seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
  seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
  
  alert('Sección eliminada exitosamente.')
}

// --- Lógica de Guardado Principal ---
async function guardarCurso() {
  // Prevenir múltiples clics
  if (isSaving.value) return
  isSaving.value = true

  try {
    // Validar campos obligatorios
    if (!form.value.CUR_DESCRIPCION?.trim()) {
      alert('La descripción del curso es obligatoria.')
      return
    }
    if (!form.value.CUR_CODIGO?.trim()) {
      alert('El código del curso es obligatorio.')
      return
    }
    if (!form.value.TCU_ID) {
      alert('Debes seleccionar un tipo de curso.')
      return
    }
    if (!form.value.PER_ID_RESPONSABLE) {
      alert('Debes seleccionar un responsable.')
      return
    }

    const payload = { ...form.value }
    // Sanitizar payload: eliminar campos calculados / solo lectura
    delete payload.fechas
    delete payload.secciones
    delete payload.CUR_FECHA_HORA
    payload.CUR_COTA_CON_ALMUERZO = Number(payload.CUR_COTA_CON_ALMUERZO)
    payload.CUR_COTA_SIN_ALMUERZO = Number(payload.CUR_COTA_SIN_ALMUERZO)
    // Convertir FKs y enums a números por seguridad
    payload.TCU_ID = Number(payload.TCU_ID)
    payload.PER_ID_RESPONSABLE = Number(payload.PER_ID_RESPONSABLE)
    payload.CAR_ID_RESPONSABLE = payload.CAR_ID_RESPONSABLE ? Number(payload.CAR_ID_RESPONSABLE) : null
    payload.COM_ID_LUGAR = payload.COM_ID_LUGAR ? Number(payload.COM_ID_LUGAR) : null
    payload.CUR_MODALIDAD = Number(payload.CUR_MODALIDAD || 1)
    payload.CUR_TIPO_CURSO = Number(payload.CUR_TIPO_CURSO || 1)
    payload.CUR_ADMINISTRA = Number(payload.CUR_ADMINISTRA || 1)
    payload.CUR_ESTADO = Number(payload.CUR_ESTADO !== undefined ? payload.CUR_ESTADO : 0)

    if (isTrulyNew.value) {
      // Obtener usuario actual para USU_ID
      try {
        const perfil = await request('auth/perfil')
        if (perfil?.usuario?.user_id) {
          payload.USU_ID = perfil.usuario.user_id
        } else {
          payload.USU_ID = 1 // Fallback
        }
      } catch (e) {
        console.warn('No se pudo obtener USU_ID, usando default:', e)
        payload.USU_ID = 1 // Default fallback
      }

      const creado = await cursosApi.create(payload)
      cursosList.value.unshift(creado)
      await cargarFechasDelCurso(creado.CUR_ID)
      await cargarSeccionesDelCurso(creado.CUR_ID)
      isTrulyNew.value = false
      alert('Curso creado exitosamente.')
    } else {
      // En edición, no modifica USU_ID
      const actualizado = await cursosApi.update(payload.CUR_ID, payload)
      const index = cursosList.value.findIndex(c => c.CUR_ID === payload.CUR_ID)
      if (index !== -1) {
        // preservar fechas y secciones ya cargadas en memoria si existen
        const fechasLocal = cursosList.value[index].fechas
        const seccionesLocal = cursosList.value[index].secciones
        cursosList.value[index] = { ...actualizado, fechas: fechasLocal || [], secciones: seccionesLocal || [] }
      }
      alert('Curso actualizado exitosamente.')
    }
    aplicarFiltros()
    cerrarModal()
  } catch (e) {
    console.error('Error al guardar el curso:', e)
    console.error('Response:', e.response?.data)
    alert(`Error al guardar: ${e.response?.data?.detail || e.message || 'Error desconocido'}`)
  } finally {
    isSaving.value = false
  }
}

// --- Deshabilitar (CUR_ESTADO=2) ---
async function deshabilitarCurso(curso) {
  if (!window.confirm('¿Deshabilitar este curso?')) return
  if (isDisabling.value) return // Prevenir múltiples clics
  isDisabling.value = true
  
  try {
    // El modelo no tiene CUR_VIGENTE, usamos CUR_ESTADO=2 (Anulado)
    const actualizado = await cursosApi.partialUpdate(curso.CUR_ID, { CUR_ESTADO: 2 })
    Object.assign(curso, actualizado)
    aplicarFiltros()
    alert('Curso deshabilitado exitosamente.')
  } catch (e) {
    console.error('Error al deshabilitar curso:', e)
    console.error('Response:', e.response?.data)
    alert(`Error al deshabilitar: ${e.response?.data?.detail || e.message || 'Error desconocido'}`)
  } finally {
    isDisabling.value = false
  }
}

// --- Funciones de Formato y Ayuda ---
const personasOptions = computed(() => personasList.value.map(p => ({ value: p.PER_ID, text: `${p.PER_NOMBRE} ${p.PER_APELLIDO_PATERNO}` })))

const tiposCursoOptions = computed(() => 
  tiposCursoList.value.map(tc => ({ value: tc.TCU_ID, text: tc.TCU_DESCRIPCION }))
)

const comunasList = ref([])
const cargosList = ref([])
const comunasOptions = computed(() => comunasList.value.map(c => ({ value: c.COM_ID, text: c.COM_DESCRIPCION })))
const cargosOptions = computed(() => cargosList.value.map(c => ({ value: c.CAR_ID, text: c.CAR_DESCRIPCION })))

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

const opcionesAdministra = [
  { value: 1, text: 'Zona' },
  { value: 2, text: 'Distrito' },
]

function abrirModalVer(curso) {
  cursoSeleccionado.value = curso
  cargarFechasDelCurso(curso.CUR_ID)
  seccionesCurso.value = seccionesList.value.filter(s => s.CUR_ID === curso.CUR_ID)
  mostrarModalVer.value = true
}

function cerrarModalVer() {
  mostrarModalVer.value = false
  cursoSeleccionado.value = null
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