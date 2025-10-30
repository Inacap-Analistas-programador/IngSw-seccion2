<template>
  <div class="gestion-personas"> <!-- Clase principal consistente -->
    <header class="page-header">
      <h3>Gestión de Cursos</h3>
    </header>

    <div class="filtros"> <!-- Estructura de filtros consistente -->
      <div class="filtros-left">
        <InputBase v-model="searchQuery" placeholder="Buscar por nombre o código..." />
      </div>
      <div class="filtros-right">
        <BaseButton @click="abrirModalCrear" class="btn-success">+ Nuevo Curso</BaseButton>
      </div>
    </div>

    <div class="main-area">
      <div class="table-wrapper">
        <table class="table-cursos">
          <thead>
            <tr>
              <th>Nombre del Curso</th>
              <th>Código</th>
              <th>Tipo</th>
              <th>Fechas</th>
              <th>Responsable</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td colspan="7" class="text-center">Cargando...</td>
            </tr>
            <tr v-else-if="cursosPaginados.length === 0">
              <td colspan="7" class="text-center">No se encontraron cursos.</td>
            </tr>
            <tr v-for="curso in cursosPaginados" :key="curso.CUR_ID">
              <td>{{ curso.CUR_DESCRIPCION }}</td>
              <td>{{ curso.CUR_CODIGO }}</td>
              <td>{{ getTipoCurso(curso.CUR_TIPO_CURSO)?.TIP_CUR_DESCRIPCION || 'N/A' }}</td>
              <td>{{ formatearFechas(curso.CUR_FECHA_INICIO, curso.CUR_FECHA_TERMINO) }}</td>
              <td>{{ getPersona(curso.PER_ID_RESPONSABLE)?.PER_NOMBRE || 'N/A' }}</td>
              <td>
                <span :class="['badge', getEstadoClass(curso.CUR_ESTADO)]">{{ getEstadoTexto(curso.CUR_ESTADO) }}</span>
              </td>
              <td class="actions-cell">
                <BaseButton @click="abrirModalEditar(curso)" class="btn-warning" small>Editar</BaseButton>
                <BaseButton @click="confirmarEliminacion(curso.CUR_ID)" class="btn-danger" small>Eliminar</BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="pagination-controls" v-if="totalPages > 1">
      <BaseButton @click="cambiarPagina(currentPage - 1)" :disabled="currentPage === 1">Anterior</BaseButton>
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      <BaseButton @click="cambiarPagina(currentPage + 1)" :disabled="currentPage === totalPages">Siguiente</BaseButton>
    </div>

    <BaseModal v-model="mostrarModal">
      <div class="modal-contenido">
        <h3>{{ esEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</h3>
        <form @submit.prevent="guardarCurso" class="form-curso">
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre del Curso:</label>
              <InputBase v-model="form.CUR_DESCRIPCION" required />
            </div>
            <div class="form-group">
              <label>Código:</label>
              <InputBase v-model="form.CUR_CODIGO" required />
            </div>
            <div class="form-group">
              <label>Fecha Inicio:</label>
              <InputBase type="date" v-model="form.CUR_FECHA_INICIO" required />
            </div>
            <div class="form-group">
              <label>Fecha Fin:</label>
              <InputBase type="date" v-model="form.CUR_FECHA_TERMINO" required />
            </div>
            <div class="form-group">
              <label>Responsable:</label>
              <BaseSelect v-model="form.PER_ID_RESPONSABLE" :options="personasOptions" required />
            </div>
            <div class="form-group">
              <label>Tipo de Curso:</label>
              <BaseSelect v-model="form.CUR_TIPO_CURSO" :options="tiposCursoOptions" required />
            </div>
             <div class="form-group">
              <label>Estado:</label>
              <BaseSelect v-model="form.CUR_ESTADO" :options="estadosOptions" required />
            </div>
          </div>
          <div class="form-actions">
            <BaseButton @click="cerrarModal" type="button" class="btn-secondary">Cancelar</BaseButton>
            <BaseButton type="submit" class="btn-primary">{{ esEdicion ? 'Actualizar' : 'Guardar' }}</BaseButton>
          </div>
        </form>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import gestioncursosService from '@/services/gestioncursosService';
import personasService from '@/services/personasService';
import BaseButton from '@/components/Reutilizables/BaseButton.vue';
import BaseModal from '@/components/Reutilizables/BaseModal.vue';
import InputBase from '@/components/Reutilizables/InputBase.vue';
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue';

const cursos = ref([]);
const personas = ref([]);
const tiposCurso = ref([
  { TIP_CUR_ID: 1, TIP_CUR_DESCRIPCION: 'Formación Inicial' },
  { TIP_CUR_ID: 2, TIP_CUR_DESCRIPCION: 'Formación Avanzada' },
  { TIP_CUR_ID: 3, TIP_CUR_DESCRIPCION: 'Especialización' },
]);
const isLoading = ref(true);
const mostrarModal = ref(false);
const esEdicion = ref(false);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;

const form = reactive({
  CUR_ID: null,
  CUR_DESCRIPCION: '',
  CUR_CODIGO: '',
  CUR_FECHA_INICIO: '',
  CUR_FECHA_TERMINO: '',
  PER_ID_RESPONSABLE: null,
  CUR_TIPO_CURSO: null,
  CUR_ESTADO: 'P',
});

const estadosOptions = [
    { value: 'P', label: 'Planificado' },
    { value: 'E', label: 'En Curso' },
    { value: 'F', label: 'Finalizado' },
    { value: 'C', label: 'Cancelado' },
];

const cargarDatos = async () => {
  try {
    isLoading.value = true;
    const [cursosRes, personasRes] = await Promise.all([
      cursosService.getCursos(),
      personasService.getPersonas(),
    ]);
    cursos.value = cursosRes.data;
    personas.value = personasRes.data;
  } catch (error) {
    console.error('Error al cargar datos:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(cargarDatos);

const cursosFiltrados = computed(() => {
  if (!searchQuery.value) {
    return cursos.value;
  }
  return cursos.value.filter(c =>
    c.CUR_DESCRIPCION.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    c.CUR_CODIGO.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const totalPages = computed(() => Math.ceil(cursosFiltrados.value.length / itemsPerPage));
const cursosPaginados = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return cursosFiltrados.value.slice(start, end);
});

const cambiarPagina = (page) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const personasOptions = computed(() =>
  personas.value.map(p => ({ value: p.PER_ID, label: `${p.PER_NOMBRE} ${p.PER_APELLIDO_PATERNO}` }))
);

const tiposCursoOptions = computed(() =>
  tiposCurso.value.map(t => ({ value: t.TIP_CUR_ID, label: t.TIP_CUR_DESCRIPCION }))
);

const getPersona = (id) => personas.value.find(p => p.PER_ID === id);
const getTipoCurso = (id) => tiposCurso.value.find(t => t.TIP_CUR_ID === id);

const resetForm = () => {
  Object.assign(form, {
    CUR_ID: null,
    CUR_DESCRIPCION: '',
    CUR_CODIGO: '',
    CUR_FECHA_INICIO: '',
    CUR_FECHA_TERMINO: '',
    PER_ID_RESPONSABLE: null,
    CUR_TIPO_CURSO: null,
    CUR_ESTADO: 'P',
  });
};

const abrirModalCrear = () => {
  esEdicion.value = false;
  resetForm();
  mostrarModal.value = true;
};

const abrirModalEditar = (curso) => {
  esEdicion.value = true;
  Object.assign(form, {
    CUR_ID: curso.CUR_ID,
    CUR_DESCRIPCION: curso.CUR_DESCRIPCION,
    CUR_CODIGO: curso.CUR_CODIGO,
    CUR_FECHA_INICIO: curso.CUR_FECHA_INICIO.split('T')[0],
    CUR_FECHA_TERMINO: curso.CUR_FECHA_TERMINO.split('T')[0],
    PER_ID_RESPONSABLE: curso.PER_ID_RESPONSABLE,
    CUR_TIPO_CURSO: curso.CUR_TIPO_CURSO,
    CUR_ESTADO: curso.CUR_ESTADO,
  });
  mostrarModal.value = true;
};

const cerrarModal = () => {
  mostrarModal.value = false;
};

const guardarCurso = async () => {
  try {
    if (esEdicion.value) {
      await cursosService.updateCurso(form.CUR_ID, form);
    } else {
      await cursosService.createCurso(form);
    }
    cerrarModal();
    await cargarDatos();
  } catch (error) {
    console.error('Error al guardar el curso:', error);
  }
};

const confirmarEliminacion = async (id) => {
  if (window.confirm('¿Estás seguro de que deseas eliminar este curso?')) {
    try {
      await cursosService.deleteCurso(id);
      await cargarDatos();
      alert('Curso eliminado con éxito.');
    } catch (error) {
      console.error('Error al eliminar el curso:', error);
      alert('Error al eliminar el curso.');
    }
  }
};

const formatearFechas = (inicio, fin) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  const fechaInicio = new Date(inicio).toLocaleDateString('es-CL', options);
  const fechaFin = new Date(fin).toLocaleDateString('es-CL', options);
  return `${fechaInicio} - ${fechaFin}`;
};

const getEstadoTexto = (estado) => {
    const estadoMap = { P: 'Planificado', E: 'En Curso', F: 'Finalizado', C: 'Cancelado' };
    return estadoMap[estado] || 'Desconocido';
};

const getEstadoClass = (estado) => {
    const classMap = { P: 'badge-info', E: 'badge-success', F: 'badge-secondary', C: 'badge-danger' };
    return classMap[estado] || 'badge-dark';
};
</script>

<style scoped>
/* Estilos eliminados para heredar los globales y mantener consistencia */
</style>




<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseCheckBox from '@/components/Reutilizables/BaseCheckBox.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import cursosService from '@/services/cursosService.js'
import personasService from '@/services/personasService.js'
import mantenedoresService from '@/services/mantenedoresService.js'

// Lista de cursos y personas
const cursos = reactive([])
const personas = ref([])
const tiposCurso = ref([])
const comunas = ref([])
const cargos = ref([])

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

const nuevoCoordinador = reactive({
  persona: null,
  cargo: null
})

const modalidadOptions = [
  { value: 1, label: 'Presencial' },
  { value: 2, label: 'Virtual' },
  { value: 3, label: 'Híbrido' }
]

// Lógica de filtros
const searchQuery = ref('')
const cursosFiltrados = ref([])

// Paginación
const currentPage = ref(1)
const itemsPerPage = ref(10)

const paginatedCursos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return cursosFiltrados.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(cursosFiltrados.value.length / itemsPerPage.value)
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

async function cargarDatos() {
  try {
    // Intentar cargar datos reales del backend
    const [cursosResponse, personasResponse, tiposCursoResponse, comunasResponse, cargosResponse] = await Promise.all([
      cursosService.obtenerCursos(),
      personasService.listarBasic(),
      mantenedoresService.obtenerTiposCurso(),
      mantenedoresService.obtenerComunas(),
      mantenedoresService.obtenerCargos()
    ]);
    
    cursos.splice(0, cursos.length, ...cursosResponse.map(c => ({
      ...c,
      responsableNombre: personasResponse.find(p => p.id === c.PER_ID_RESPONSABLE)?.nombre || 'No asignado'
    })));
    
    personas.value = personasResponse.map(p => ({
      value: p.id,
      label: p.nombre
    }));
    
    tiposCurso.value = tiposCursoResponse.map(t => ({
      value: t.TCU_ID,
      label: t.TCU_DESCRIPCION
    }));
    
    comunas.value = comunasResponse.map(c => ({
      value: c.COM_ID,
      label: c.COM_NOMBRE
    }));
    
    cargos.value = cargosResponse.map(c => ({
      value: c.CAR_ID,
      label: c.CAR_NOMBRE
    }));
    
    filtrarCursos();
  } catch (error) {
    console.warn("Backend no disponible. Usando datos de prueba:", error);
    
    // Datos de prueba - Personas
    personas.value = [
      { value: 1, label: 'Juan Pérez González' },
      { value: 2, label: 'María García Silva' },
      { value: 3, label: 'Carlos Rodríguez Muñoz' },
      { value: 4, label: 'Ana López Fernández' },
      { value: 5, label: 'Pedro Martínez Díaz' }
    ];
    
    // Datos de prueba - Tipos de Curso
    tiposCurso.value = [
      { value: 1, label: 'Formación de Dirigentes' },
      { value: 2, label: 'Capacitación Técnica' },
      { value: 3, label: 'Desarrollo Personal' },
      { value: 4, label: 'Liderazgo' }
    ];
    
    // Datos de prueba - Comunas
    comunas.value = [
      { value: 1, label: 'Concepción' },
      { value: 2, label: 'Talcahuano' },
      { value: 3, label: 'Chiguayante' },
      { value: 4, label: 'San Pedro de la Paz' },
      { value: 5, label: 'Coronel' }
    ];
    
    // Datos de prueba - Cargos
    cargos.value = [
      { value: 1, label: 'Coordinador General' },
      { value: 2, label: 'Instructor' },
      { value: 3, label: 'Asistente' },
      { value: 4, label: 'Evaluador' }
    ];
    
    // Datos de prueba - Cursos
    const cursosPrueba = [
      {
        CURS_ID: 1,
        CUR_DESCRIPCION: 'Formación Básica de Dirigentes',
        CUR_CODIGO: 'FBD-2024-01',
        CUR_TIPO_CURSO: 1,
        fechaInicio: '2024-11-15',
        fechaTermino: '2024-11-17',
        PER_ID_RESPONSABLE: 1,
        responsableNombre: 'Juan Pérez González',
        CUR_ESTADO: 1,
        habilitado: true
      },
      {
        CURS_ID: 2,
        CUR_DESCRIPCION: 'Capacitación en Primeros Auxilios',
        CUR_CODIGO: 'CPA-2024-02',
        CUR_TIPO_CURSO: 2,
        fechaInicio: '2024-12-01',
        fechaTermino: '2024-12-03',
        PER_ID_RESPONSABLE: 2,
        responsableNombre: 'María García Silva',
        CUR_ESTADO: 2,
        habilitado: true
      },
      {
        CURS_ID: 3,
        CUR_DESCRIPCION: 'Liderazgo y Trabajo en Equipo',
        CUR_CODIGO: 'LTE-2024-03',
        CUR_TIPO_CURSO: 4,
        fechaInicio: '2024-10-10',
        fechaTermino: '2024-10-12',
        PER_ID_RESPONSABLE: 3,
        responsableNombre: 'Carlos Rodríguez Muñoz',
        CUR_ESTADO: 3,
        habilitado: false
      },
      {
        CURS_ID: 4,
        CUR_DESCRIPCION: 'Desarrollo de Habilidades Sociales',
        CUR_CODIGO: 'DHS-2024-04',
        CUR_TIPO_CURSO: 3,
        fechaInicio: '2024-11-20',
        fechaTermino: '2024-11-22',
        PER_ID_RESPONSABLE: 4,
        responsableNombre: 'Ana López Fernández',
        CUR_ESTADO: 1,
        habilitado: true
      },
      {
        CURS_ID: 5,
        CUR_DESCRIPCION: 'Gestión de Proyectos Scouts',
        CUR_CODIGO: 'GPS-2024-05',
        CUR_TIPO_CURSO: 2,
        fechaInicio: '2024-09-05',
        fechaTermino: '2024-09-07',
        PER_ID_RESPONSABLE: 5,
        responsableNombre: 'Pedro Martínez Díaz',
        CUR_ESTADO: 3,
        habilitado: false
      }
    ];
    
    cursos.splice(0, cursos.length, ...cursosPrueba);
    filtrarCursos();
  }
}

function filtrarCursos() {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) {
    cursosFiltrados.value = cursos
    return
  }
  cursosFiltrados.value = cursos.filter(curso => {
    return (
      curso.nombre.toLowerCase().includes(query) ||
      curso.codigo.toLowerCase().includes(query)
    )
  })
}

// Inicializar datos
onMounted(cargarDatos)

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

  const cursoData = {
    CUR_DESCRIPCION: form.nombre,
    CUR_CODIGO: form.codigo,
    CUR_FECHA_SOLICITUD: new Date().toISOString().split('T')[0], // Fecha actual
    PER_ID_RESPONSABLE: form.responsable,
    // Añadir otros campos necesarios por el modelo de Django
    TCU_ID: 1, // Ejemplo, esto debería venir de un select
    CAR_ID_RESPONSABLE: 1, // Ejemplo
    COM_ID_LUGAR: 1, // Ejemplo
    CUR_ADMINISTRA: 1,
    CUR_COTA_CON_ALMUERZO: 0,
    CUR_COTA_SIN_ALMUERZO: 0,
    CUR_MODALIDAD: 1,
    CUR_TIPO_CURSO: 1,
    CUR_LUGAR: 'Lugar de ejemplo',
    CUR_ESTADO: 1,
  };

  try {
    if (modoEdicion.value) {
      // Actualizar curso existente
      const cursoId = cursos[indiceEdicion.value].CURS_ID;
      await cursosService.actualizarCurso(cursoId, cursoData);
    } else {
      // Crear nuevo curso
      await cursosService.agregarCurso(cursoData);
    }
    await cargarDatos(); // Recargar datos para ver los cambios
    limpiarFormulario();
  } catch (error) {
    console.error("Error al guardar el curso:", error);
    alert("Hubo un error al guardar el curso. Revisa la consola para más detalles.");
  }
}

// Editar curso existente
function editarCurso(index) {
  const curso = cursos[index]
  
  // Llenar el formulario con los datos del curso a editar
  form.nombre = curso.CUR_DESCRIPCION
  form.codigo = curso.CUR_CODIGO
  
  // Formatear la fecha para el input type="date" (YYYY-MM-DD)
  if (curso.CUR_FECHA_SOLICITUD) {
    form.fechaInicio = new Date(curso.CUR_FECHA_SOLICITUD).toISOString().split('T')[0]
  } else {
    form.fechaInicio = ''
  }
  // Asumimos que no hay fecha de fin en el modelo principal, se deja en blanco
  form.fechaFin = '' 
  
  form.responsable = curso.PER_ID_RESPONSABLE
  form.jerarquias = [] // Este campo se puede desarrollar más adelante

  modoEdicion.value = true
  indiceEdicion.value = index
  mostrarFormulario.value = true
}// Toggle de preinscripción
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

// Funciones auxiliares
function getTipoCursoText(tipoId) {
  const tipo = tiposCurso.value.find(t => t.value === tipoId)
  return tipo ? tipo.label : 'Sin tipo'
}

function getEstadoInfo(estado) {
  const estados = {
    1: { text: 'Activo', class: 'badge-success' },
    2: { text: 'Pendiente', class: 'badge-warning' },
    3: { text: 'Finalizado', class: 'badge-secondary' },
    4: { text: 'Cancelado', class: 'badge-danger' }
  }
  return estados[estado] || { text: 'Desconocido', class: 'badge-info' }
}

function gestionarParticipantes(cursoId) {
  // TODO: Implementar modal de participantes
  console.log('Gestionar participantes del curso:', cursoId)
  alert('Funcionalidad en desarrollo')
}

function agregarCoordinador() {
  if (!nuevoCoordinador.persona || !nuevoCoordinador.cargo) {
    alert('Selecciona persona y cargo')
    return
  }
  
  form.coordinadores.push({
    PER_ID: nuevoCoordinador.persona,
    CAR_ID: nuevoCoordinador.cargo
  })
  
  nuevoCoordinador.persona = null
  nuevoCoordinador.cargo = null
}

function eliminarCoordinador(index) {
  form.coordinadores.splice(index, 1)
}

function getPersonaNombre(perId) {
  const persona = personas.value.find(p => p.value === perId)
  return persona ? persona.label : 'Desconocido'
}

function getCargoNombre(carId) {
  const cargo = cargos.value.find(c => c.value === carId)
  return cargo ? cargo.label : 'Desconocido'
}
</script>

<style scoped>
.crud-cursos {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px; 
  background: #ffffff;
  color: #111;
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
  background-color: #214e9c;
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
  color: #444;
  font-weight: 500;
}

.courses-table {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  background-color: #fff;
  min-width: 0; 
  font-size: 14px;
}

.courses-table th, .courses-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #ececec;
  text-align: left;
  color: #222; 
  opacity: 1;
}

.courses-table th {
  background-color: #f7f7f7;
  color: #222;
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
  background-color: #f9fafb;
  border-radius: 8px;
}

.create-card {
  background: #f2f5f9; 
  border-radius: 6px;
  padding: 18px 18px 16px 18px;
  border: 1px solid rgba(33,78,156,0.08);
  color: #222;
  font-size: 15px;
  line-height: 1.4;
  margin-top: 16px;
}

.create-card h5 {
  margin: 0 0 10px 0;
  color:#1e3a8a;
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
  color: #333;
}

.hierarchy-section {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #dde4ee;
}

.hierarchy-section > label {
  display: block;
  margin-bottom: 12px;
  font-weight: 600;
  color: #333;
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
  border: 1px solid #dde4ee;
  text-align: left;
}

.coordinador-table th {
  background-color: #eef2f7;
}

.no-coordinadores {
  color: #6b7280;
  font-style: italic;
  padding: 10px;
  background-color: #f9fafb;
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
  color: #1e3a8a;
  border-bottom: 2px solid #1e3a8a;
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
  border: 1px solid #e5e7eb;
  text-align: left;
}

.participantes-table th {
  background-color: #f9fafb;
}

.hierarchy {
  margin-top: 16px;
}
</style>