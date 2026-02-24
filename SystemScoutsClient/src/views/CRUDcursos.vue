<template>
  <div class="crud-cursos-container">
    <!-- Toasts de notificación -->
    <div class="toast-container">
      <NotificationToast
        v-for="(alerta, index) in alertas"
        :key="alerta.id"
        :message="alerta.message"
        :icon="alerta.type === 'success' ? 'check' : 'alert-circle'"
        @close="removerAlerta(alerta.id)"
        :style="{ marginBottom: `${index * 60}px` }"
      />
    </div>
    <PageHeader 
      title="Gestión de Cursos" 
      subtitle="Administra, crea y organiza los cursos de formación." 
    />

    <!-- Filtros y Acciones -->
    <CursoFilters 
      v-model:filtros="filtros"
      v-model:tempSearchQuery="tempSearchQuery"
      :opcionesEstado="opcionesEstado"
      :tiposCursoOptions="tiposCursoOptions"
      :personasOptions="personasOptions"
      :hasAnyFilter="hasAnyFilter"
      @aplicar="aplicarFiltros"
      @limpiar="limpiarFiltros"
      @ensureCatalogo="ensureCatalogo"
    />

    <!-- Header estilo Mantenedor -->
    <div class="mantenedor-header">
      <div class="header-content">
        <h2>Cursos</h2>
        <div class="header-actions-group">
          <BaseButton class="header-icon-btn" variant="primary" @click="abrirModalCrear" title="Nuevo Curso">
            <AppIcons name="plus" :size="20" />
            <span class="btn-label-desktop">Nuevo</span>
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      Cargando datos...
    </div>

    <!-- Tabla de Cursos -->
    <CursoTable 
      v-else
      :cursos="cursosFiltrados"
      :hasAnyFilter="hasAnyFilter"
      :getTipoCursoName="getTipoCursoName"
      :formatDates="formatDates"
      :getPersonaName="getPersonaName"
      :getCargoName="getCargoName"
      :getEstadoClass="getEstadoClass"
      :getEstadoText="getEstadoText"
      @ver="abrirModalVer"
      @editar="abrirModalEditar"
      @cambioEstado="abrirModalCambioEstadoCurso"
      @dashboard="abrirDashboard"
    />

    

    <!-- Modal de Creación/Edición de Curso -->
    <BaseModal v-model="mostrarModal" @close="cerrarModal" class="curso-modal modal-editar-mejorado">
      <template #title>
        {{ modoVer ? 'Detalle del Curso' : (isTrulyNew ? 'Crear Nuevo Curso' : 'Editar Curso') }}
      </template>
      <template #default>
        <CursoForm 
          :form="form"
          v-model:lists="formLists"
          :options="formOptions"
          :modoVer="modoVer"
          :isTrulyNew="isTrulyNew"
          :esEdicion="esEdicion"
          :isSaving="isSaving"
          @save="guardarCurso"
          @cancel="cerrarModal"
          @show-alert="mostrarAlerta($event.message, $event.type)"
        />
      </template>
    </BaseModal>

    <!-- Modal Cambio de Estado -->
    <BaseModal v-model="mostrarModalCambioEstado" @close="cerrarModalCambioEstado" size="sm">
      <template #title>Cambio de Estado</template>
      <div class="modal-form">
        <div class="form-group">
          <label>Estado Actual: <strong>{{ cursoParaCambioEstado ? (opcionesEstado.find(e => e.value === cursoParaCambioEstado.CUR_ESTADO)?.text || 'Desconocido') : '-' }}</strong></label>
        </div>
        <div class="form-group">
          <label for="nuevo-estado">Nuevo Estado *</label>
          <BaseSelect v-model="nuevoEstado" :options="opcionesEstado" optionLabel="text" optionValue="value" id="nuevo-estado" />
        </div>
      </div>
      <template #footer>
        <BaseButton @click="guardarCambioEstado" variant="primary" :disabled="isDisabling">
          {{ isDisabling ? 'Guardando...' : 'Guardar' }}
        </BaseButton>
        <BaseButton @click="cerrarModalCambioEstado" variant="secondary" :disabled="isDisabling">Cancelar</BaseButton>
      </template>
    </BaseModal>

  <!-- Dashboard del Curso - Overlay completo -->
  <Teleport to="body">
    <div v-if="mostrarDashboard" class="dashboard-overlay">
      <CursoDashboard 
        :cursoId="cursoIdDashboard" 
        @close="cerrarDashboard"
      />
    </div>
  </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { request } from '@/services/apiClient.js'
import cursosService from '@/services/cursosService.js'
import CursoDashboard from './CursoDashboard.vue'
import personasService from '@/services/personasService.js'
import mantenedores from '@/services/mantenedoresService.js'

// Import Sub-components
import CursoFilters from '@/components/cursos/CursoFilters.vue'
import CursoTable from '@/components/cursos/CursoTable.vue'
import CursoForm from '@/components/cursos/CursoForm.vue'

// Local aliases matching legacy names used across this component
const cursosApi = cursosService.cursos
const seccionesApi = cursosService.secciones
const fechasApi = cursosService.fechas
const formadoresApi = cursosService.formadores
const alimentacionesApi = cursosService.alimentaciones
const cuotasApi = cursosService.cuotas
const coordinadoresApi = cursosService.coordinadores

import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import { comunasCoords } from '@/data/comunasChile.js'

// --- Constantes Estáticas ---
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
const opcionesAdministra = [
  { value: 1, text: 'Zona' },
  { value: 2, text: 'Distrito' },
]
const comunaCoordsMap = comunasCoords

// Helper to normalize keys to Uppercase (for frontend compatibility)
const toUpperKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj
  const newObj = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    const upperKey = key.toUpperCase()
    newObj[upperKey] = obj[key]
    // Keep original key if different
    if (upperKey !== key) newObj[key] = obj[key]
  }
  return newObj
}

// Helper to normalize keys to Lowercase (for backend compatibility)
const toLowerKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj
  const newObj = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    newObj[key.toLowerCase()] = obj[key]
  }
  return newObj
}

// --- Estado y Reactividad ---
const alertas = ref([])
const mostrarAlerta = (mensaje, tipo = 'error') => {
  alertas.value.push({
    id: Date.now(),
    message: mensaje,
    type: tipo
  })
  // Auto-cerrar después de 5s
  setTimeout(() => {
    removerAlerta(alertas.value[alertas.value.length - 1]?.id)
  }, 5000)
}
const removerAlerta = (id) => {
  if (!id) return
  alertas.value = alertas.value.filter(a => a.id !== id)
}

const isLoading = ref(false)
const isLoadingData = ref(false) // Guard para prevenir cargas duplicadas
const cursosList = ref([])
const cursosFiltrados = ref([])
const personasList = ref([])
const tiposCursoList = ref([])
// Listas locales para edición (v-model de subcomponentes)
const fechasCurso = ref([])
const ramaslist = ref([])
const seccionesCurso = ref([]) // Se eliminó cache global
// Equipo y logística

const rolesList = ref([])
const formadoresCurso = ref([])
const alimentacionesCurso = ref([])
const alimentacionCatalogo = ref([])
const cuotasCurso = ref([])
const coordinadoresCurso = ref([])

const mostrarModalVer = ref(false)
const cursoSeleccionado = ref(null)
const mostrarDashboard = ref(false)
const cursoIdDashboard = ref(null)
const mostrarModalCambioEstado = ref(false)
const cursoParaCambioEstado = ref(null)
const nuevoEstado = ref(null)

const mostrarModal = ref(false)
const esEdicion = ref(false)
const modoVer = ref(false)
const isTrulyNew = ref(false)
const originalCursoBackup = ref(null)
// Backups para detectar cambios en sublistas si se desea optimizar PATCH, 
// aunque en integración completa solemos enviar todo o diffs.
const originalBuffersBackup = ref({ fechas: [], secciones: [], formadores: [], alimentaciones: [] })
const isSaving = ref(false) // Bandera para prevenir múltiples clics
const isDisabling = ref(false) // Bandera para prevenir múltiples deshabilitar

// (Eliminados estados de edición manuales ahora en subcomponentes)


const filtros = ref({
  searchQuery: '',
  estado: null,
  tipoCurso: null,
  responsable: null,
})
const tempSearchQuery = ref('')

const hasAnyFilter = computed(() => {
  const f = filtros.value
  return Boolean((f.searchQuery && f.searchQuery.trim()) || f.estado || f.tipoCurso || f.responsable)
})

const form = ref(null)

// Agrupación de opciones para pasar a CursoForm
const formOptions = computed(() => ({
  tiposCurso: tiposCursoOptions.value,
  personas: personasOptions.value,
  cargos: cargosOptions.value,
  comunas: comunasOptions.value,
  ramas: ramasOptions.value,
  roles: rolesOptions.value,
  alimentacion: alimentacionOptions.value,
  modalidad: opcionesModalidad,
  tipoPresencial: opcionesTipoPresencial,
  administra: opcionesAdministra,
  secciones: seccionesOptions.value
}))

// Agrupación de listas para v-model en CursoForm
const formLists = computed({
  get: () => ({
    fechas: fechasCurso.value,
    secciones: seccionesCurso.value,
    formadores: formadoresCurso.value,
    alimentaciones: alimentacionesCurso.value,
    cuotas: cuotasCurso.value
  }),
  set: (val) => {
    fechasCurso.value = val.fechas
    seccionesCurso.value = val.secciones
    formadoresCurso.value = val.formadores
    alimentacionesCurso.value = val.alimentaciones
    cuotasCurso.value = val.cuotas
  }
})

const inicializarFormulario = () => ({
  CUR_ID: null,
  CUR_DESCRIPCION: '',
  CUR_CODIGO: '',
  TCU_ID: null,
  PER_ID_RESPONSABLE: null,
  CAR_ID_RESPONSABLE: null,
  CUR_FECHA_SOLICITUD: '',
  CUR_COTA_CON_ALMUERZO: null,
  CUR_COTA_SIN_ALMUERZO: null,
  CUR_MODALIDAD: null,
  CUR_TIPO_CURSO: null,
  CUR_ADMINISTRA: null,
  COM_ID_LUGAR: null,
  CUR_LUGAR: '',
  CUR_COORD_LATITUD: '',
  CUR_COORD_LONGITUD: '',
  CUR_ESTADO: null,
  CUR_OBSERVACION: '',
})

form.value = inicializarFormulario()

const route = useRoute()
const router = useRouter()

// --- Utilities: cache, debounce, safe API wrapper and abort support ---

// --- Utilities: cache, debounce, safe API wrapper and abort support ---
const _cache = new Map()
function cacheKey(path, params) { return `${path}|${JSON.stringify(params || {})}` }

function debounce(fn, wait = 250) {
  let t
  return (...args) => {
    clearTimeout(t)
    t = setTimeout(() => fn(...args), wait)
  }
}

// Safe list wrapper: intenta usar un objeto API global si existe (e.g., cursosApi),
// si no, hace fallback a `request(path)` (con querystring si params)
// Currently unused but kept for future use
// async function safeList(apiName, path, params) {
//   try {
//     const globalObj = typeof globalThis !== 'undefined' ? globalThis[`${apiName}`] : undefined
//     if (globalObj && typeof globalObj.list === 'function') {
//       return await globalObj.list(params)
//     }
//   } catch (e) { /* ignore */ }

//   // Build querystring for simple GETs
//   const qs = params && Object.keys(params).length ? `?${new URLSearchParams(params).toString()}` : ''
//   return await request(`${path}${qs}`)
// }

// Abort support for fetch: guardamos el controller y cancelamos la carga anterior
const lastController = { ctrl: null }

// Helper safe data extraction
const getData = (resp) => {
  if (!resp) return []
  if (Array.isArray(resp)) return resp
  // soportar distintas envolturas de respuesta
  const r = resp
  return r.results || (r.data?.results) || r.data || r.items || []
}

async function cargarDatos({ page = 1, page_size = 20, search = '' } = {}) {
  if (isLoadingData.value) return
  // Permitir carga sin filtros para mostrar todos los cursos inicialmente
  isLoadingData.value = true
  isLoading.value = true

  // cancelar carga previa si existe
  try {
    if (lastController.ctrl) lastController.ctrl.abort()
  } catch { /* noop */ }
  lastController.ctrl = new AbortController()

  try {
    // Pedir cursos desde el servicio específico y catálogos relacionados
    const cursosCacheKey = cacheKey('cursos/cursos', { page, page_size, search })
    let cursosDataPromise
    if (_cache.has(cursosCacheKey)) {
      cursosDataPromise = _cache.get(cursosCacheKey)
    } else {
      cursosDataPromise = cursosApi.paraMantenedor({ page, page_size, search })
      _cache.set(cursosCacheKey, cursosDataPromise)
    }

    const cursosData = await cursosDataPromise

    // Catálogos y recursos asociados (usar servicios concretos)
    const fetchPromises = []
    
    // Solo solicitar catálogos reales (personas, tipos, ramas, comunas, cargos, roles, alimentacion).
    // Secciones, Fechas, Cuotas, etc. vienen anidados en el curso gracias al nuevo Serializer.
    
    const personasPromise = (Array.isArray(personasList.value) && personasList.value.length) ? Promise.resolve(personasList.value) : personasService.personas.list()
    fetchPromises.push(personasPromise)

    const tiposPromise = (Array.isArray(tiposCursoList.value) && tiposCursoList.value.length) ? Promise.resolve(tiposCursoList.value) : mantenedores.tipoCursos.list()
    fetchPromises.push(tiposPromise)

    const ramasPromise = (Array.isArray(ramaslist.value) && ramaslist.value.length) ? Promise.resolve(ramaslist.value) : mantenedores.rama.list()
    fetchPromises.push(ramasPromise)

    // seccionesApi.list y fechasApi.list ELIMINADOS de aquí por ineficientes (traían todo paginado).
    // Ahora vienen en el payload del curso.

    const comunasPromise = (Array.isArray(comunasList?.value) && comunasList.value.length) ? Promise.resolve(comunasList.value) : mantenedores.comuna.list()
    fetchPromises.push(comunasPromise)

    const cargosPromise = (Array.isArray(cargosList?.value) && cargosList.value.length) ? Promise.resolve(cargosList.value) : mantenedores.cargo.list()
    fetchPromises.push(cargosPromise)

    const rolesPromise = (Array.isArray(rolesList.value) && rolesList.value.length) ? Promise.resolve(rolesList.value) : mantenedores.rol.list()
    fetchPromises.push(rolesPromise)

    const alimentacionPromise = (Array.isArray(alimentacionCatalogo.value) && alimentacionCatalogo.value.length) ? Promise.resolve(alimentacionCatalogo.value) : mantenedores.alimentacion.list()
    fetchPromises.push(alimentacionPromise)

    const [personasApi, tiposApi, ramasApi, comunasApi, cargosApi, rolesApi, alimentacionCat] = await Promise.all(fetchPromises)

    // Normalizar cursos (puede venir paginado)
    let cursosArray = getData(cursosData)
    cursosArray = cursosArray.map(toUpperKeys)

    // Asignar catálogos
    personasList.value = (Array.isArray(personasApi) ? personasApi : (personasApi?.results || [])).map(toUpperKeys)
    tiposCursoList.value = (Array.isArray(tiposApi) ? tiposApi : (tiposApi?.results || [])).map(toUpperKeys)
    ramaslist.value = (Array.isArray(ramasApi) ? ramasApi : (ramasApi?.results || [])).map(toUpperKeys)
    comunasList.value = (Array.isArray(comunasApi) ? comunasApi : (comunasApi?.results || [])).map(toUpperKeys)
    cargosList.value = (Array.isArray(cargosApi) ? cargosApi : (cargosApi?.results || [])).map(toUpperKeys)
    rolesList.value = (Array.isArray(rolesApi) ? rolesApi : (rolesApi?.results || [])).map(toUpperKeys)
    alimentacionCatalogo.value = (Array.isArray(alimentacionCat) ? alimentacionCat : (alimentacionCat?.results || [])).map(toUpperKeys)

    // Procesar cursos para extraer listas anidadas normalizadas
    cursosList.value = cursosArray.map(c => {
      // Normalizar sub-listas si existen (backend response > toUpperKeys > propiedades FECHAS/SECCIONES/etc)
      // Nota: toUpperKeys mantiene las claves originales, así que 'fechas' o 'FECHAS' funciona.
      const rawFechas = c.FECHAS || c.fechas || []
      const rawSecciones = c.SECCIONES || c.secciones || []
      const rawFormadores = c.FORMADORES || c.formadores || []
      
      const fechasNorm = rawFechas.map(toUpperKeys).sort((a,b) => new Date(a.CUF_FECHA_INICIO) - new Date(b.CUF_FECHA_INICIO))
      
      return {
        ...c,
        fechas: fechasNorm, // Sobrescribir con normalizado
        secciones: rawSecciones.map(toUpperKeys),
        formadores: rawFormadores.map(toUpperKeys) 
      }
    })
    
    // Listas globales eliminadas

    // Filtrado cliente como fallback; cuando uses búsqueda remota, pasar `search` hará que el servidor filtre
    aplicarFiltros()
  } catch (e) {
    if (e.name === 'AbortError') {
      console.info('Carga de datos abortada')
    } else {
      console.error('Error cargando datos desde API:', e)
      cursosList.value = []
      cursosFiltrados.value = []
    }
  } finally {
    isLoading.value = false
    isLoadingData.value = false
  }
}

onMounted(() => {
  preloadCatalogosMin()
  // No cargar datos automáticamente. Esperar a que el usuario filtre.
  // cargarDatos()
  
  // Reintento diferido: solo si se requiere (por ejemplo si hubo un reload rápido), pero ahora supeditado a filtro
  const tokenEarly = localStorage.getItem('accessToken') || localStorage.getItem('token')
  if (!tokenEarly) {
    // Si no hay token, esperamos un poco por si está en proceso de setearse (login redirect)
    // Pero NO llamamos a cargarDatos a menos que haya filtros activos en URL
    setTimeout(() => {
       const tokenLate = localStorage.getItem('accessToken') || localStorage.getItem('token')
       if (tokenLate) checkRouteActions() 
    }, 800)
  } else {
    // Si viene parametro search, aplicarlo y cargar
    const { search } = route.query
    if (search) {
      filtros.value.searchQuery = search
      // Esperar un tick para que reactividad funcione o llamar directo
      setTimeout(() => aplicarFiltros(), 100) 
    }
    checkRouteActions()
  }
})

async function checkRouteActions() {
  const { action, id } = route.query
  if (action === 'edit' && id) {
    console.log('Detectada acción de editar para curso ID:', id)
    // Intentar encontrar el curso en la lista actual
    let curso = cursosList.value.find(c => Number(c.CUR_ID) === Number(id))
    
    // Si no está (porque no se cargó nada o paginación), intentar buscarlo específicamente
    if (!curso) {
      try {
        const res = await request(`/cursos/cursos/${id}/`)
        // Normalizar respuesta si es necesario
        curso = toUpperKeys(res)
      } catch (e) {
        console.error('Error buscando curso para editar:', e)
      }
    }
    
    if (curso) {
      abrirModalEditar(curso)
      // Limpiar query para no reabrir al recargar, opcional
      router.replace({ query: {} })
    }
  }
}




// Preload minimal catalogs from fast endpoints and cache to localStorage
async function preloadCatalogosMin() {
  try {
    const ttlMs = 15 * 60 * 1000
    const now = Date.now()
    const personasCache = JSON.parse(localStorage.getItem('personas_min_cache') || 'null')
    const tiposCache = JSON.parse(localStorage.getItem('tipos_curso_min_cache') || 'null')

    if (personasCache && (now - personasCache.timestamp) < ttlMs) {
      personasList.value = personasCache.data.map(toUpperKeys)
    }
    if (tiposCache && (now - tiposCache.timestamp) < ttlMs) {
      tiposCursoList.value = tiposCache.data.map(toUpperKeys)
    }

    // If not present or empty, do a quick blocking fetch so filters are usable immediately
    if (!personasList.value.length || !tiposCursoList.value.length) {
      const [pMin, tMin] = await Promise.all([
        personasService.personas.list({ page: 1, page_size: 200 }),
        mantenedores.tipoCursos.list({ page: 1, page_size: 100 })
      ])
      const pData = (Array.isArray(pMin?.results) ? pMin.results : (pMin || [])).map(r => ({ 
        ...r,
        id: r.id || r.PER_ID, 
        nombre: r.nombre || r.PER_NOMBRE_COMPLETO || `${r.PER_NOMBRES || ''} ${r.PER_APELLIDOS || ''}`.trim() 
      }))
      const tData = (Array.isArray(tMin?.results) ? tMin.results : (tMin || [])).map(r => ({ 
        ...r,
        id: r.id || r.TCU_ID, 
        nombre: r.nombre || r.TCU_DESCRIPCION || r.TCU_NOMBRE 
      }))
      personasList.value = pData.map(toUpperKeys)
      tiposCursoList.value = tData.map(toUpperKeys)
      localStorage.setItem('personas_min_cache', JSON.stringify({ timestamp: Date.now(), data: pData }))
      localStorage.setItem('tipos_curso_min_cache', JSON.stringify({ timestamp: Date.now(), data: tData }))
    } else {
      // Otherwise refresh in background
      Promise.all([
        personasService.personas.list({ page: 1, page_size: 200 }),
        mantenedores.tipoCursos.list({ page: 1, page_size: 100 })
      ]).then(([pMin, tMin]) => {
        const pData = (Array.isArray(pMin?.results) ? pMin.results : (pMin || [])).map(r => ({ 
          ...r,
          id: r.id || r.PER_ID, 
          nombre: r.nombre || r.PER_NOMBRE_COMPLETO || `${r.PER_NOMBRES || ''} ${r.PER_APELLIDOS || ''}`.trim() 
        }))
        const tData = (Array.isArray(tMin?.results) ? tMin.results : (tMin || [])).map(r => ({ 
          ...r,
          id: r.id || r.TCU_ID, 
          nombre: r.nombre || r.TCU_DESCRIPCION || r.TCU_NOMBRE 
        }))
        personasList.value = pData.map(toUpperKeys)
        tiposCursoList.value = tData.map(toUpperKeys)
        localStorage.setItem('personas_min_cache', JSON.stringify({ timestamp: Date.now(), data: pData }))
        localStorage.setItem('tipos_curso_min_cache', JSON.stringify({ timestamp: Date.now(), data: tData }))
      }).catch(e => console.warn('No se pudo refrescar catálogos mínimos:', e))
    }
  } catch (e) {
    console.error('Error en preloadCatalogosMin:', e)
  }
}

// Debounced server search ELIMINADO para búsqueda manual
// const _debouncedLoad = debounce((q) => cargarDatos({ page: 1, page_size: 20, search: (q || '').trim() }), 450)
// watch(() => filtros.value.searchQuery, (v) => { ... })

// Listener de almacenamiento (multi-tab / login en otra pestaña)
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === 'token' || e.key === 'accessToken') {
      const t = localStorage.getItem('accessToken') || localStorage.getItem('token')
      if (t && cursosList.value.length === 0) {
        console.info('[CRUDcursos] Detectado cambio de token vía storage event. Cargando datos...')
        cargarDatos()
      }
    }
  })
}

// --- Filtros controlados por botón ---
function aplicarFiltros() {
  // Sincronizar búsqueda manual
  filtros.value.searchQuery = tempSearchQuery.value

  let items = [...cursosList.value]
  const { searchQuery, estado, tipoCurso, responsable } = filtros.value
  if (!hasAnyFilter.value) {
    cursosFiltrados.value = items
    return
  }
  // Si no hay cursos cargados aún, solicitar al servidor
  if (!items.length) {
    cargarDatos({ page: 1, page_size: 20 })
    return
  }
  if (searchQuery) {
    const q = String(searchQuery).toLowerCase()
    items = items.filter(c => (c.CUR_DESCRIPCION || '').toLowerCase().includes(q) || (c.CUR_CODIGO || '').toLowerCase().includes(q))
  }
  if (estado !== null && estado !== undefined && estado !== '') items = items.filter(c => Number(c.CUR_ESTADO) === Number(estado))
  if (tipoCurso !== null && tipoCurso !== undefined && tipoCurso !== '') items = items.filter(c => Number(c.TCU_ID) === Number(tipoCurso))
  if (responsable !== null && responsable !== undefined && responsable !== '') items = items.filter(c => Number(c.PER_ID_RESPONSABLE) === Number(responsable))
  
  // Ordenar por ESTADO (ascendente 0-3) y luego por DESCRIPCIÓN (ascendente)
  items.sort((a, b) => {
    const estadoA = Number(a.CUR_ESTADO) || 0
    const estadoB = Number(b.CUR_ESTADO) || 0
    if (estadoA !== estadoB) return estadoA - estadoB
    const descA = (a.CUR_DESCRIPCION || '').toLowerCase()
    const descB = (b.CUR_DESCRIPCION || '').toLowerCase()
    return descA.localeCompare(descB)
  })
  
  cursosFiltrados.value = items
}

function limpiarFiltros() {
  filtros.value = { searchQuery: '', estado: null, tipoCurso: null, responsable: null }
  aplicarFiltros()
}


function getRamaName(id) {
  const rama = ramaslist.value.find(r => r.RAM_ID === id)
  return rama ? rama.RAM_DESCRIPCION : 'No definida'
}

// Lazy load helpers for select catalogs
async function ensureCatalogo(kind) {
  try {
    isLoading.value = true
    if (kind === 'personas' && (!personasList.value || personasList.value.length === 0)) {
      const personasApi = await personasService.personas.list({ page: 1, page_size: 200 })
      personasList.value = (Array.isArray(personasApi) ? personasApi : (personasApi?.results || [])).map(toUpperKeys)
    } else if (kind === 'tipos' && (!tiposCursoList.value || tiposCursoList.value.length === 0)) {
      const tiposApi = await mantenedores.tipoCursos.list({ page: 1, page_size: 200 })
      tiposCursoList.value = (Array.isArray(tiposApi) ? tiposApi : (tiposApi?.results || [])).map(toUpperKeys)
    }
  } catch (e) {
    console.error('Error cargando catálogo', kind, e)
  } finally {
    isLoading.value = false
  }
}


// --- Lógica del Modal (Crear/Editar) ---
async function abrirModalCrear() {
  form.value = inicializarFormulario()
  isTrulyNew.value = true
  esEdicion.value = true // Activar modo "edición" para mostrar las sub-secciones
  modoVer.value = false
  fechasCurso.value = []
  seccionesCurso.value = []
  formadoresCurso.value = []
  alimentacionesCurso.value = []
  cuotasCurso.value = []
// (Reset local implícito)

  // Si aún no se han cargado catálogos (persona, tipos, comunas, cargos, ramas) forzar carga rápida
  if (
    personasList.value.length === 0 ||
    tiposCursoList.value.length === 0 ||
    comunasList.value?.length === 0 ||
    cargosList.value?.length === 0 ||
    ramaslist.value.length === 0
  ) {
    try { await cargarDatos() } catch (e) { console.warn('No se pudieron refrescar catálogos antes de crear:', e) }
  }
  mostrarModal.value = true
}

async function abrirModalEditar(cursoMin) {
  isTrulyNew.value = false
  esEdicion.value = true
  modoVer.value = false
  
  isLoading.value = true
  let curso = cursoMin
  try {
    const fullData = await cursosApi.get(cursoMin.CUR_ID)
    curso = toUpperKeys(fullData)
  } catch (e) {
    mostrarAlerta('Error cargando detalles del curso', 'error')
  } finally {
    isLoading.value = false
  }

  form.value = {
    ...inicializarFormulario(),
    ...curso,
    CUR_FECHA_SOLICITUD: curso.CUR_FECHA_SOLICITUD ? curso.CUR_FECHA_SOLICITUD.split('T')[0] : '',
    TCU_ID: curso.TCU_ID ? Number(curso.TCU_ID) : null,
    PER_ID_RESPONSABLE: curso.PER_ID_RESPONSABLE ? Number(curso.PER_ID_RESPONSABLE) : null,
    CAR_ID_RESPONSABLE: curso.CAR_ID_RESPONSABLE ? Number(curso.CAR_ID_RESPONSABLE) : null,
    COM_ID_LUGAR: curso.COM_ID_LUGAR ? Number(curso.COM_ID_LUGAR) : null,
    CUR_MODALIDAD: curso.CUR_MODALIDAD ? Number(curso.CUR_MODALIDAD) : null,
    CUR_TIPO_CURSO: curso.CUR_TIPO_CURSO ? Number(curso.CUR_TIPO_CURSO) : null,
    CUR_ADMINISTRA: curso.CUR_ADMINISTRA ? Number(curso.CUR_ADMINISTRA) : null,
  }
  originalCursoBackup.value = JSON.parse(JSON.stringify(form.value))
  await cargarFechasDelCurso(curso.CUR_ID)
  await cargarSeccionesDelCurso(curso.CUR_ID)
  // Cargar equipo, alimentación, cuotas y coordinadores del curso
  try {
    const [forms, alims, cuots] = await Promise.all([
      formadoresApi.list({ cur_id: curso.CUR_ID }).catch(() => []),
      alimentacionesApi.list({ cur_id: curso.CUR_ID }).catch(() => []),
      cuotasApi.list({ cur_id: curso.CUR_ID }).catch(() => []),
    ])
    formadoresCurso.value = (Array.isArray(forms?.results) ? forms.results : (forms || [])).map(toUpperKeys)
    alimentacionesCurso.value = (Array.isArray(alims?.results) ? alims.results : (alims || [])).map(toUpperKeys)
    cuotasCurso.value = (Array.isArray(cuots?.results) ? cuots.results : (cuots || [])).map(toUpperKeys)

    // Populate global quota fields from the list
    const quotaCon = cuotasCurso.value.find(q => Number(q.CUU_TIPO) === 1)
    const quotaSin = cuotasCurso.value.find(q => Number(q.CUU_TIPO) === 2)
    form.value.CUR_COTA_CON_ALMUERZO = quotaCon ? Number(quotaCon.CUU_VALOR) : 0
    form.value.CUR_COTA_SIN_ALMUERZO = quotaSin ? Number(quotaSin.CUU_VALOR) : 0

  } catch (e) { console.warn('No se pudo cargar datos relacionados:', e) }
  originalBuffersBackup.value = {
    fechas: JSON.parse(JSON.stringify(fechasCurso.value)),
    secciones: JSON.parse(JSON.stringify(seccionesCurso.value)),
    formadores: JSON.parse(JSON.stringify(formadoresCurso.value)),
    alimentaciones: JSON.parse(JSON.stringify(alimentacionesCurso.value)),
    cuotas: JSON.parse(JSON.stringify(cuotasCurso.value)),
  }
// (Reset de sub-buffers locales implícito al asignar array vacío)
  mostrarModal.value = true

}

function cerrarModal() {
  mostrarModal.value = false
}

// --- Funciones de Carga de Sub-Entidades (Solo Lectura Inicial) ---

async function cargarFechasDelCurso(cursoId) {
  if (!cursoId) {
    fechasCurso.value = []
    return
  }
  try {
    const res = await fechasApi.list({ cur_id: cursoId, page_size: 20 })
    const raw = Array.isArray(res?.results) ? res.results : (Array.isArray(res) ? res : [])
    // Mapeo directo a local state
    fechasCurso.value = raw.map(toUpperKeys)
  } catch (e) {
    console.error('Error cargando fechas:', e)
    fechasCurso.value = []
  }
}

async function cargarSeccionesDelCurso(cursoId) {
  try {
    const all = await seccionesApi.list({ cur_id: cursoId, page_size: 500 })
    const raw = Array.isArray(all?.results) ? all.results : (Array.isArray(all) ? all : [])
    seccionesCurso.value = raw.map(toUpperKeys)
  } catch (e) {
    console.error('Error cargando secciones:', e)
    seccionesCurso.value = []
  }
}

// --- Sync Helper for Sub-Entities ---
async function syncCollection(api, currentList, originalList, idField, curId, transformPayload, onCreated) {
  // 1. Delete: Items present in original but not in current (based on ID)
  // Filter out any temp IDs from the current list's ID set
  const currentIds = new Set(
    currentList
      .map(x => x[idField])
      .filter(id => id && typeof id !== 'string' && !String(id).startsWith('tmp'))
  )
  
  for (const original of originalList) {
    if (original[idField] && !currentIds.has(original[idField])) {
       try { 
         await api.remove(original[idField]) 
       } catch (e) { 
         console.warn(`[Sync] Delete failed for ${idField}=${original[idField]}:`, e) 
       }
    }
  }

  // 2. Create / Update
  for (const item of currentList) {
    const payload = transformPayload(item)
    payload.CUR_ID = curId // Ensure context
    
    const idVal = item[idField]
    const isNew = !idVal || String(idVal).startsWith('tmp')
    
    try {
      if (isNew) {
         const res = await api.create(toLowerKeys(payload))
         const saved = toUpperKeys(res)
         // Update local item with real ID and data
         const exactId = saved[idField]
         if (exactId) {
            item[idField] = exactId
            Object.assign(item, saved)
         }
         if (onCreated) onCreated(item, saved)
      } else {
         // Update existing
         await api.update(idVal, toLowerKeys(payload))
      }
    } catch (e) {
      console.warn(`[Sync] Save failed for item:`, item, e)
    }
  }
}

// --- Lógica de Guardado Principal ---
async function guardarCurso() {
  // Prevenir múltiples clics
  if (isSaving.value) return
  isSaving.value = true

  try {
    // Validar campos obligatorios
    if (!form.value.CUR_DESCRIPCION?.trim()) {
      mostrarAlerta('La descripción del curso es obligatoria.', 'warning')
      return
    }
    if (!form.value.CUR_CODIGO?.trim()) {
      mostrarAlerta('El código del curso es obligatorio.', 'warning')
      return
    }
    if (!form.value.TCU_ID) {
      mostrarAlerta('Debes seleccionar un tipo de curso.', 'warning')
      return
    }
    if (!form.value.PER_ID_RESPONSABLE) {
      mostrarAlerta('Debes seleccionar un responsable.', 'warning')
      return
    }

    // Sync global quotas from local list before saving
    const quotaCon = cuotasCurso.value.find(q => Number(q.CUU_TIPO) === 1)
    const quotaSin = cuotasCurso.value.find(q => Number(q.CUU_TIPO) === 2)
    form.value.CUR_COTA_CON_ALMUERZO = quotaCon ? Number(quotaCon.CUU_VALOR) : 0
    form.value.CUR_COTA_SIN_ALMUERZO = quotaSin ? Number(quotaSin.CUU_VALOR) : 0

    const payload = { ...form.value }
    // Sanitizar payload: eliminar buffers locales
    delete payload.fechas
    delete payload.secciones
    delete payload.formadores
    delete payload.alimentaciones
    delete payload.cuotas
    delete payload.coordinadores
    delete payload.CUR_FECHA_HORA
    
    // Casteos
    payload.CUR_COTA_CON_ALMUERZO = Number(payload.CUR_COTA_CON_ALMUERZO)
    payload.CUR_COTA_SIN_ALMUERZO = Number(payload.CUR_COTA_SIN_ALMUERZO)
    payload.TCU_ID = Number(payload.TCU_ID)
    payload.PER_ID_RESPONSABLE = Number(payload.PER_ID_RESPONSABLE)
    payload.CAR_ID_RESPONSABLE = payload.CAR_ID_RESPONSABLE ? Number(payload.CAR_ID_RESPONSABLE) : null
    payload.COM_ID_LUGAR = payload.COM_ID_LUGAR ? Number(payload.COM_ID_LUGAR) : null
    payload.CUR_MODALIDAD = Number(payload.CUR_MODALIDAD || 1)
    payload.CUR_TIPO_CURSO = Number(payload.CUR_TIPO_CURSO || 1)
    payload.CUR_ADMINISTRA = Number(payload.CUR_ADMINISTRA || 1)
    
    // Estado automático: si estaba Anulado (2), mantener; si no, calcular según períodos
    const originalEstado = originalCursoBackup.value?.CUR_ESTADO
    if (Number(originalEstado) === 2) {
      payload.CUR_ESTADO = 2
    } else {
      payload.CUR_ESTADO = computeAutoEstadoFromFechas(fechasCurso.value)
    }

    // CLEANUP: Filtrar solo las llaves en mayúscula (source of truth del formulario)
    // para evitar que llaves minúsculas antiguas (inyectadas por toUpperKeys) sobrescriban los cambios
    const cleanPayload = {}
    Object.keys(payload).forEach(key => {
      // Asumimos que las llaves editables son las que están en Main Uppercase o Snake Uppercase
      // Si existe una versión mayúscula y una minúscula, la mayúscula es la que tiene el v-model
      if (key === key.toUpperCase()) {
        cleanPayload[key] = payload[key]
      }
    })

    // Prepare payload for API (lowercase)
    const apiPayload = toLowerKeys(cleanPayload)
    let cursoGuardado = null

    if (isTrulyNew.value) {
      // Creation
      apiPayload.usu_id = 1 // TODO: Implementar identity real
      const creadoRaw = await cursosApi.create(apiPayload)
      cursoGuardado = toUpperKeys(creadoRaw)
      cursosList.value.unshift(cursoGuardado)
      // En modo 'Nuevo', todos los buffers son para crear, y originalBuffersBackup debería estar vacío.
    } else {
      // Update
      const camposClave = ['CUR_DESCRIPCION','CUR_CODIGO','TCU_ID','PER_ID_RESPONSABLE','CUR_FECHA_SOLICITUD','CUR_COTA_CON_ALMUERZO','CUR_COTA_SIN_ALMUERZO','CUR_MODALIDAD','CUR_TIPO_CURSO','CUR_LUGAR','CUR_COORD_LATITUD','CUR_COORD_LONGITUD','CUR_ESTADO','CUR_OBSERVACION','CUR_ADMINISTRA','COM_ID_LUGAR','CAR_ID_RESPONSABLE']
      // Check changes? (Optional optimization, but we probably want to save anyway to trigger sub-entity sync)
      const actualizadoRaw = await cursosApi.partialUpdate(payload.CUR_ID, apiPayload)
      cursoGuardado = toUpperKeys(actualizadoRaw)
      
      const index = cursosList.value.findIndex(c => c.CUR_ID === payload.CUR_ID)
      if (index !== -1) {
        // preserve nested arrays to avoid flicker
        const old = cursosList.value[index]
        cursosList.value[index] = { ...cursoGuardado, fechas: old.fechas, secciones: old.secciones } 
      }
    }
    
    const curId = cursoGuardado.CUR_ID
    const origBuffers = originalBuffersBackup.value || {}

    // --- Persistir Sub-Entidades (Sync) ---
    
    // 1. Fechas
    await syncCollection(fechasApi, fechasCurso.value, origBuffers.fechas || [], 'CUF_ID', curId, (item) => ({
        CUF_FECHA_INICIO: item.CUF_FECHA_INICIO,
        CUF_FECHA_TERMINO: item.CUF_FECHA_TERMINO,
        CUF_TIPO: item.CUF_TIPO
    }))

    // 2. Secciones (Mapping temp IDs needed for Formadores)
    const sectionsMap = {} // __tmpId -> real CUS_ID
    await syncCollection(seccionesApi, seccionesCurso.value, origBuffers.secciones || [], 'CUS_ID', curId, (item) => ({
        CUS_SECCION: item.CUS_SECCION,
        RAM_ID: item.RAM_ID,
        CUS_CANT_PARTICIPANTE: item.CUS_CANT_PARTICIPANTE
    }), (item, saved) => {
        if (item.__tmpId) sectionsMap[item.__tmpId] = saved.CUS_ID
    })

    // 3. Formadores
    await syncCollection(formadoresApi, formadoresCurso.value, origBuffers.formadores || [], 'CUF_ID', curId, (item) => {
        let rCusId = item.CUS_ID
        // Resolve temp reference
        if (typeof rCusId === 'string' && rCusId.startsWith('tmp-')) {
          const tId = Number(rCusId.replace('tmp-', ''))
          if (sectionsMap[tId]) rCusId = sectionsMap[tId]
        }
        return {
           PER_ID: item.PER_ID,
           ROL_ID: item.ROL_ID,
           CUS_ID: typeof rCusId === 'number' ? rCusId : null,
           CUO_DIRECTOR: !!item.CUO_DIRECTOR
        }
    })

    // 4. Alimentaciones
    await syncCollection(alimentacionesApi, alimentacionesCurso.value, origBuffers.alimentaciones || [], 'CUA_ID', curId, (item) => ({
        ALI_ID: item.ALI_ID,
        CUA_FECHA: item.CUA_FECHA,
        CUA_TIEMPO: item.CUA_TIEMPO,
        CUA_DESCRIPCION: item.CUA_DESCRIPCION,
        CUA_CANTIDAD_ADICIONAL: Number(item.CUA_CANTIDAD_ADICIONAL || 0)
    }))

    // 5. Cuotas
    await syncCollection(cuotasApi, cuotasCurso.value, origBuffers.cuotas || [], 'CUU_ID', curId, (item) => ({
        CUU_TIPO: Number(item.CUU_TIPO),
        CUU_FECHA: item.CUU_FECHA,
        CUU_VALOR: Number(item.CUU_VALOR)
    }))

    // 6. Coordinadores
    await syncCollection(coordinadoresApi, coordinadoresCurso.value, origBuffers.coordinadores || [], 'CUC_ID', curId, (item) => ({
        PER_ID: item.PER_ID,
        CAR_ID: item.CAR_ID
    }))

    // Update Backups for next edit
    originalCursoBackup.value = JSON.parse(JSON.stringify(form.value))
    originalBuffersBackup.value = {
        fechas: JSON.parse(JSON.stringify(fechasCurso.value)),
        secciones: JSON.parse(JSON.stringify(seccionesCurso.value)),
        formadores: JSON.parse(JSON.stringify(formadoresCurso.value)),
        alimentaciones: JSON.parse(JSON.stringify(alimentacionesCurso.value)),
        cuotas: JSON.parse(JSON.stringify(cuotasCurso.value)),
        coordinadores: JSON.parse(JSON.stringify(coordinadoresCurso.value)),
    }
    
    // Refrescar buffers locales (para asegurar IDs limpios y orden)
    await cargarFechasDelCurso(curId)
    await cargarSeccionesDelCurso(curId)

    mostrarAlerta(isTrulyNew.value ? 'Curso creado exitosamente.' : 'Curso actualizado exitosamente.', 'success')
    isTrulyNew.value = false
    aplicarFiltros()
    cerrarModal()

  } catch (e) {
    console.error('Error al guardar el curso:', e)
    mostrarAlerta(`Error al guardar: ${e.response?.data?.detail || e.message || 'Error desconocido'}`, 'error')
  } finally {
    isSaving.value = false
  }
}

// --- Estado automático basado en fechas ---
function computeAutoEstadoFromFechas(fechas) {
  try {
    const list = Array.isArray(fechas) ? fechas : []
    if (!list.length) return 0 // Pendiente
    const starts = list.map(f => new Date(f.CUF_FECHA_INICIO)).filter(d => !isNaN(d))
    const ends = list.map(f => new Date(f.CUF_FECHA_TERMINO || f.CUF_FECHA_INICIO)).filter(d => !isNaN(d))
    if (!starts.length || !ends.length) return 0
    const minStart = new Date(Math.min(...starts))
    const maxEnd = new Date(Math.max(...ends))
    const today = new Date()
    const t = new Date(today.getFullYear(), today.getMonth(), today.getDate())
    const ms = new Date(minStart.getFullYear(), minStart.getMonth(), minStart.getDate())
    const me = new Date(maxEnd.getFullYear(), maxEnd.getMonth(), maxEnd.getDate())
    if (t < ms) return 0 // Pendiente
    if (t > me) return 3 // Finalizado
    return 1 // Vigente
  } catch {
    return 0
  }
}

// --- Cambio de Estado ---
function abrirModalCambioEstadoCurso(curso) {
  cursoParaCambioEstado.value = curso
  nuevoEstado.value = curso.CUR_ESTADO
  mostrarModalCambioEstado.value = true
}

function cerrarModalCambioEstado() {
  mostrarModalCambioEstado.value = false
  cursoParaCambioEstado.value = null
  nuevoEstado.value = null
}

async function guardarCambioEstado() {
  if (nuevoEstado.value === null || nuevoEstado.value === undefined) {
    mostrarAlerta('Debe seleccionar un estado', 'warning')
    return
  }
  
  let rawValue = nuevoEstado.value
  if (rawValue && typeof rawValue === 'object') {
     rawValue = rawValue.value ?? rawValue.VALOR ?? rawValue.id
  }
  const estadoNumber = Number(rawValue)
  
  if (isDisabling.value) return
  isDisabling.value = true
  
  try {
    const payload = toLowerKeys({ CUR_ESTADO: estadoNumber })
    const actualizadoRaw = await cursosApi.partialUpdate(cursoParaCambioEstado.value.CUR_ID, payload)
    const actualizado = toUpperKeys(actualizadoRaw)
    
    Object.assign(cursoParaCambioEstado.value, actualizado)
    
    // Update global list
    const idx = cursosList.value.findIndex(c => c.CUR_ID === actualizado.CUR_ID)
    if (idx !== -1) {
       cursosList.value[idx] = { ...cursosList.value[idx], ...actualizado }
    }

    aplicarFiltros()
    mostrarAlerta('Estado actualizado exitosamente.', 'success')
    cerrarModalCambioEstado()
  } catch (e) {
    console.error('Error al cambiar estado:', e)
    mostrarAlerta(`Error al cambiar estado: ${e.response?.data?.detail || e.message}`, 'error')
  } finally {
    isDisabling.value = false
  }
}

// --- Funciones de Formato y Ayuda ---
const personasOptions = computed(() => personasList.value
  .filter(p => p.PER_VIGENTE === true)
  .map(p => {
    const name = p.PER_NOMBRE_COMPLETO || p.PER_NOMBRE || p.PER_NOMBRES || p.nombre || p.NOMBRE || ''
    const fullName = name.trim() || (p.PER_NOMBRES ? `${p.PER_NOMBRES} ${p.PER_APELLIDOS || ''}`.trim() : 'Sin nombre')
    return { 
      value: p.PER_ID || p.id || p.ID, 
      text: fullName
    }
  })
)

const tiposCursoOptions = computed(() => 
  tiposCursoList.value
    .filter(tc => tc.TCU_VIGENTE === true)
    .map(tc => ({ 
      value: tc.TCU_ID || tc.id || tc.ID, 
      text: tc.TCU_DESCRIPCION || tc.TCU_NOMBRE || tc.nombre || tc.NOMBRE || 'Sin descripción' 
    }))
)

const comunasList = ref([])
const cargosList = ref([])
const comunasOptions = computed(() => comunasList.value.filter(c => c.COM_VIGENTE === true).map(c => ({ value: c.COM_ID, text: c.COM_DESCRIPCION })))

// Ubicar mapa según comuna seleccionada

watch(() => form.value.COM_ID_LUGAR, (newComunaId) => {
  if (!newComunaId) return
  const comunaObj = comunasList.value.find(c => Number(c.COM_ID) === Number(newComunaId))
  if (!comunaObj) return
  const colName = comunaObj.COM_DESCRIPCION
  const coords = comunaCoordsMap[colName]
  if (coords) {
    form.value.CUR_COORD_LATITUD = coords.lat
    form.value.CUR_COORD_LONGITUD = coords.lng
  } else {
    // Default STGO
    form.value.CUR_COORD_LATITUD = -33.45694
    form.value.CUR_COORD_LONGITUD = -70.64827
  }
})

const cargosOptions = computed(() => cargosList.value.filter(c => c.CAR_VIGENTE === true).map(c => ({ value: c.CAR_ID, text: c.CAR_DESCRIPCION })))

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
  const p = personasList.value.find(x => Number(x.PER_ID ?? x.ID ?? x.id) === Number(id))
  const nombre = p?.PER_NOMBRES || p?.PER_NOMBRE || p?.nombre || ''
  const apellido = p?.PER_APELPAT || p?.PER_APELLIDO_PATERNO || p?.APELLIDO || p?.apellido || ''
  const full = `${(nombre || '').trim()} ${(apellido || '').trim()}`.trim()
  return p ? (full || nombre || '-') : 'No asignado'
}

function getCargoName(id) {
  const c = cargosList.value.find(x => Number(x.CAR_ID ?? x.ID ?? x.id) === Number(id))
  return c ? (c.CAR_DESCRIPCION || c.DESCRIPCION || c.nombre || '-') : ''
}

function getTipoCursoName(id) {
  const tc = tiposCursoList.value.find(x => Number(x.TCU_ID ?? x.ID ?? x.id) === Number(id))
  return tc ? (tc.TCU_DESCRIPCION || tc.NOMBRE || tc.nombre || '-') : 'No definido'
}

function getEstadoText(e) {
  return opcionesEstado.find(o => o.value === e)?.text || 'Desconocido'
}

function getEstadoClass(e) {
  const map = { 
    0: 'badge-warning', // Pendiente
    1: 'status-active',  // Vigente
    2: 'status-inactive', // Anulado
    3: 'status-info'      // Finalizado
  }
  return map[e] || 'badge-dark'
}


const rolesOptions = computed(() => rolesList.value.filter(r => r.ROL_VIGENTE === true).map(r => ({ value: r.ROL_ID, text: r.ROL_DESCRIPCION })))
const ramasOptions = computed(() => ramaslist.value.filter(r => r.RAM_VIGENTE === true).map(r => ({ value: r.RAM_ID, text: r.RAM_DESCRIPCION })))
const alimentacionOptions = computed(() => alimentacionCatalogo.value.filter(a => a.ALI_VIGENTE === true).map(a => ({ value: a.ALI_ID, text: a.ALI_DESCRIPCION })))

const seccionesOptions = computed(() => seccionesCurso.value.map(s => {
  const rama = ramaslist.value.find(r => r.RAM_ID === s.RAM_ID)
  const ramaText = rama ? rama.RAM_DESCRIPCION : ''
  return { value: s.CUS_ID || `tmp-${s.__tmpId}`, text: `SECCION N° ${s.CUS_SECCION} (${ramaText})` }
}))



async function abrirModalVer(curso) {
  // Reutilizar la lógica de carga de edición pero en modo solo lectura
  await abrirModalEditar(curso)
  modoVer.value = true
}

function cerrarModalVer() {
  // Legacy cleanup if needed
  mostrarModalVer.value = false
}

function abrirDashboard(curso) {
  cursoIdDashboard.value = curso.CUR_ID
  mostrarDashboard.value = true
}

function cerrarDashboard() {
  mostrarDashboard.value = false
  cursoIdDashboard.value = null
}
</script>

<style scoped>
/* Correos-like Standardized Layout */
.crud-cursos-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 24px;
  font-family: 'Inter', Arial, sans-serif;
  height: 100%;
  overflow: hidden;
  box-sizing: border-box;
}

.mantenedor-header { 
  margin-bottom: 20px; 
  padding: 32px 0px 16px; 
  border-bottom: 2px solid #3949ab; 
}
.header-content { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  width: 100%; 
}
.mantenedor-header h2 { 
  color: #1a237e; 
  font-size: 1.5rem; 
  display: flex; 
  align-items: center; 
  margin: 0; 
  font-weight: 700;
}

.header-actions-group { display: flex; gap: 8px; }

.header-icon-btn {
  height: 40px !important;
  min-width: 40px !important;
  padding: 0 16px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 6px;
  font-weight: 600 !important;
}

.btn-label-desktop {
  margin-left: 8px;
}
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
}

/* Dashboard Overlay */
.dashboard-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  z-index: 9999;
  overflow-y: auto;
}

.btn-close-x {
  opacity: 0.6;
  transition: opacity 0.2s;
  padding: 4px !important;
}
.btn-close-x:hover {
  opacity: 1;
  background: #f3f4f6;
}
</style>