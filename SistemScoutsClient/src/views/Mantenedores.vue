<template>
  <div class="mantenedores-scouts">
    <!-- Main Content -->
    <div class="main-content">
      <!-- Header con Selector de Mantenedores -->
      <div class="header">
        <div class="header-content">
          <div class="header-title">
            <h1>Módulo de Mantenedores</h1>
            <p>Gestión de Datos Maestros del Sistema Scout</p>
          </div>
          <div class="mantenedor-selector">
            <label for="mantenedor-select">Mantenedor:</label>
            <select 
              id="mantenedor-select" 
              class="mantenedor-dropdown" 
              v-model="activeTab"
            >
              <option 
                v-for="tab in tabs" 
                :key="tab.id" 
                :value="tab.id"
              >
                {{ tab.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Zonas -->
      <div v-if="activeTab === 'zonas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🗺️ Gestión de Zonas</h2>
          <button class="btn-primary" @click="abrirModal('crear-zona')">
            + Nueva Zona
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las zonas son agrupaciones geográficas de distritos scouts.
          </div>
        </div>
        
        <!-- Barra de búsqueda mantenida -->
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar zona por descripción..."
            v-model="searchZonas"
          >
          <button class="btn-primary">🔍 Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Unilateral</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="zona in filteredZonas" :key="zona.id">
                <td>{{ zona.descripcion }}</td>
                <td>{{ zona.unilateral ? 'Sí' : 'No' }}</td>
                <td>
                  <span class="status-badge" :class="zona.vigente ? 'status-active' : 'status-inactive'">
                    {{ zona.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verZona(zona)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarZona(zona)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularZona(zona)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Distritos -->
      <div v-if="activeTab === 'distritos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>📍 Gestión de Distritos</h2>
          <button class="btn-primary" @click="abrirModal('crear-distrito')">
            + Nuevo Distrito
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los distritos agrupan varios grupos scouts dentro de una zona específica.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar distrito..."
            v-model="searchDistritos"
          >
          <select class="select-filter" v-model="filtroZona">
            <option value="">Todas las zonas</option>
            <option v-for="zona in zonas" :key="zona.id" :value="zona.descripcion">
              {{ zona.descripcion }}
            </option>
          </select>
          <button class="btn-primary">🔍 Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Zona</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="distrito in filteredDistritos" :key="distrito.id">
                <td>{{ distrito.descripcion }}</td>
                <td>{{ getZonaNombre(distrito.zona_id) }}</td>
                <td>
                  <span class="status-badge" :class="distrito.vigente ? 'status-active' : 'status-inactive'">
                    {{ distrito.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verDistrito(distrito)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarDistrito(distrito)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularDistrito(distrito)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Grupos Scout -->
      <div v-if="activeTab === 'grupos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>👥 Gestión de Grupos Scout</h2>
          <button class="btn-primary" @click="abrirModal('crear-grupo')">
            + Nuevo Grupo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los grupos scout son las unidades operativas donde se desarrollan las actividades con los jóvenes.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar grupo..."
            v-model="searchGrupos"
          >
          <select class="select-filter" v-model="filtroDistrito">
            <option value="">Todos los distritos</option>
            <option v-for="distrito in distritos" :key="distrito.id" :value="distrito.descripcion">
              {{ distrito.descripcion }}
            </option>
          </select>
          <button class="btn-primary">🔍 Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Distrito</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="grupo in filteredGrupos" :key="grupo.id">
                <td>{{ grupo.descripcion }}</td>
                <td>{{ getDistritoNombre(grupo.distrito_id) }}</td>
                <td>
                  <span class="status-badge" :class="grupo.vigente ? 'status-active' : 'status-inactive'">
                    {{ grupo.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verGrupo(grupo)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarGrupo(grupo)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularGrupo(grupo)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Ramas -->
      <div v-if="activeTab === 'ramas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🏕️ Gestión de Ramas</h2>
          <button class="btn-primary" @click="abrirModal('crear-rama')">
            + Nueva Rama
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las ramas definen las divisiones por edad dentro del movimiento scout.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rama in ramas" :key="rama.id">
                <td>{{ rama.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="rama.vigente ? 'status-active' : 'status-inactive'">
                    {{ rama.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verRama(rama)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarRama(rama)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularRama(rama)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Tipos de Curso -->
      <div v-if="activeTab === 'tipos-curso'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>📚 Gestión de Tipos de Curso</h2>
          <button class="btn-primary" @click="abrirModal('crear-tipo-curso')">
            + Nuevo Tipo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los tipos de curso definen las categorías de formación disponibles en el sistema.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Tipo</th>
                <th>Cant. Participantes</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoCurso in tiposCurso" :key="tipoCurso.id">
                <td>{{ tipoCurso.descripcion }}</td>
                <td>{{ tipoCurso.tipo }}</td>
                <td>{{ tipoCurso.cant_participante }}</td>
                <td>
                  <span class="status-badge" :class="tipoCurso.vigente ? 'status-active' : 'status-inactive'">
                    {{ tipoCurso.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verTipoCurso(tipoCurso)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarTipoCurso(tipoCurso)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularTipoCurso(tipoCurso)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Cargos -->
      <div v-if="activeTab === 'cargos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>👔 Gestión de Cargos</h2>
          <button class="btn-primary" @click="abrirModal('crear-cargo')">
            + Nuevo Cargo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los cargos definen las responsabilidades dentro de la organización scout.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cargo in cargos" :key="cargo.id">
                <td>{{ cargo.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="cargo.vigente ? 'status-active' : 'status-inactive'">
                    {{ cargo.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verCargo(cargo)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarCargo(cargo)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularCargo(cargo)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Alimentación -->
      <div v-if="activeTab === 'alimentacion'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🍽️ Gestión de Alimentación</h2>
          <button class="btn-primary" @click="abrirModal('crear-alimentacion')">
            + Nueva Alimentación
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Tipos de alimentación disponibles para los participantes de cursos.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="alimentacionItem in alimentacion" :key="alimentacionItem.id">
                <td>{{ alimentacionItem.descripcion }}</td>
                <td>{{ alimentacionItem.tipo }}</td>
                <td>
                  <span class="status-badge" :class="alimentacionItem.vigente ? 'status-active' : 'status-inactive'">
                    {{ alimentacionItem.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verAlimentacion(alimentacionItem)">👁 Ver</button>
                  <button class="btn-action btn-edit" @click="editarAlimentacion(alimentacionItem)">✏ Editar</button>
                  <button class="btn-action btn-anular" @click="anularAlimentacion(alimentacionItem)">🚫 Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modales (se mantienen igual que antes) -->
    <!-- Modal Zona -->
    <div v-if="modalActivo === 'crear-zona'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'Editar' : 'Nueva' }} Zona</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarZona">
            <div class="form-group">
              <label class="form-label">Descripción:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formZona.descripcion"
                placeholder="Ej: ZONA NORTE BIOBÍO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-checkbox">
                <input type="checkbox" v-model="formZona.unilateral">
                Zona Unilateral
              </label>
            </div>
            <div class="form-group">
              <label class="form-label">Estado:</label>
              <select class="form-control" v-model="formZona.vigente" required>
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'Actualizar' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Los demás modales se mantienen con la misma estructura -->
  </div>
</template>

<script>
import { ref, computed, reactive } from 'vue'

export default {
  name: 'MantenedoresScouts',
  setup() {
    // Estado reactivo
    const activeTab = ref('zonas')
    const modalActivo = ref('')
    const editando = ref(false)
    const searchZonas = ref('')
    const searchDistritos = ref('')
    const searchGrupos = ref('')
    const filtroZona = ref('')
    const filtroDistrito = ref('')

    // Tabs de navegación (ahora para el dropdown)
    const tabs = [
      { id: 'zonas', label: 'Zonas' },
      { id: 'distritos', label: 'Distritos' },
      { id: 'grupos', label: 'Grupos Scout' },
      { id: 'ramas', label: 'Ramas' },
      { id: 'tipos-curso', label: 'Tipos Curso' },
      { id: 'cargos', label: 'Cargos' },
      { id: 'alimentacion', label: 'Alimentación' }
    ]

    // Datos de ejemplo (se mantienen igual)
    const zonas = ref([
      { id: 1, descripcion: 'ZONA NORTE BIOBÍO', unilateral: true, vigente: true },
      { id: 2, descripcion: 'ZONA SUR BIOBÍO', unilateral: false, vigente: true },
      { id: 3, descripcion: 'ZONA COSTA BIOBÍO', unilateral: true, vigente: true },
      { id: 4, descripcion: 'ZONA CORDILLERA BIOBÍO', unilateral: false, vigente: false }
    ])

    const distritos = ref([
      { id: 1, descripcion: 'DISTRITO CONCEPCIÓN', zona_id: 1, vigente: true },
      { id: 2, descripcion: 'DISTRITO TALCAHUANO', zona_id: 1, vigente: true },
      { id: 3, descripcion: 'DISTRITO LOS ÁNGELES', zona_id: 2, vigente: true }
    ])

    const grupos = ref([
      { id: 1, descripcion: 'GRUPO ARAUCO', distrito_id: 1, vigente: true },
      { id: 2, descripcion: 'GRUPO LAUTARO', distrito_id: 2, vigente: true },
      { id: 3, descripcion: 'GRUPO CAUPOLICÁN', distrito_id: 3, vigente: true }
    ])

    const ramas = ref([
      { id: 1, descripcion: 'LOBATOS', vigente: true },
      { id: 2, descripcion: 'SCOUTS', vigente: true },
      { id: 3, descripcion: 'PIONEROS', vigente: true },
      { id: 4, descripcion: 'ROVERS', vigente: true }
    ])

    const tiposCurso = ref([
      { id: 1, descripcion: 'CURSO BÁSICO', tipo: 1, cant_participante: 30, vigente: true },
      { id: 2, descripcion: 'CURSO INTERMEDIO', tipo: 2, cant_participante: 25, vigente: true },
      { id: 3, descripcion: 'CURSO AVANZADO', tipo: 3, cant_participante: 20, vigente: true }
    ])

    const cargos = ref([
      { id: 1, descripcion: 'JEFE DE GRUPO', vigente: true },
      { id: 2, descripcion: 'SUBJEFE', vigente: true },
      { id: 3, descripcion: 'TESORERO', vigente: true },
      { id: 4, descripcion: 'SECRETARIO', vigente: true }
    ])

    const alimentacion = ref([
      { id: 1, descripcion: 'DIETA REGULAR', tipo: 1, vigente: true },
      { id: 2, descripcion: 'DIETA VEGETARIANA', tipo: 2, vigente: true },
      { id: 3, descripcion: 'DIETA VEGANA', tipo: 3, vigente: true }
    ])

    // Formularios
    const formZona = reactive({
      id: null,
      descripcion: '',
      unilateral: false,
      vigente: true
    })

    // Computed properties para filtros (se mantienen igual)
    const filteredZonas = computed(() => {
      if (!searchZonas.value) return zonas.value
      return zonas.value.filter(zona => 
        zona.descripcion.toLowerCase().includes(searchZonas.value.toLowerCase())
      )
    })

    const filteredDistritos = computed(() => {
      let filtered = distritos.value
      
      if (searchDistritos.value) {
        filtered = filtered.filter(distrito => 
          distrito.descripcion.toLowerCase().includes(searchDistritos.value.toLowerCase())
        )
      }
      
      if (filtroZona.value) {
        const zona = zonas.value.find(z => z.descripcion === filtroZona.value)
        if (zona) {
          filtered = filtered.filter(distrito => distrito.zona_id === zona.id)
        }
      }
      
      return filtered
    })

    const filteredGrupos = computed(() => {
      let filtered = grupos.value
      
      if (searchGrupos.value) {
        filtered = filtered.filter(grupo => 
          grupo.descripcion.toLowerCase().includes(searchGrupos.value.toLowerCase())
        )
      }
      
      if (filtroDistrito.value) {
        const distrito = distritos.value.find(d => d.descripcion === filtroDistrito.value)
        if (distrito) {
          filtered = filtered.filter(grupo => grupo.distrito_id === distrito.id)
        }
      }
      
      return filtered
    })

    // Métodos auxiliares
    const getZonaNombre = (zonaId) => {
      const zona = zonas.value.find(z => z.id === zonaId)
      return zona ? zona.descripcion : 'No encontrada'
    }

    const getDistritoNombre = (distritoId) => {
      const distrito = distritos.value.find(d => d.id === distritoId)
      return distrito ? distrito.descripcion : 'No encontrado'
    }

    // Métodos principales
    const abrirModal = (tipo) => {
      modalActivo.value = tipo
      editando.value = false
      // Limpiar formulario
      Object.assign(formZona, {
        id: null,
        descripcion: '',
        unilateral: false,
        vigente: true
      })
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      editando.value = false
    }

    const guardarZona = () => {
      if (editando.value) {
        const index = zonas.value.findIndex(z => z.id === formZona.id)
        if (index !== -1) {
          zonas.value[index] = { ...formZona }
        }
      } else {
        const nuevaZona = {
          id: Math.max(...zonas.value.map(z => z.id)) + 1,
          ...formZona
        }
        zonas.value.push(nuevaZona)
      }
      cerrarModal()
    }

    const editarZona = (zona) => {
      Object.assign(formZona, zona)
      modalActivo.value = 'crear-zona'
      editando.value = true
    }

    const anularZona = (zona) => {
      if (confirm(`¿Está seguro que desea anular la zona ${zona.descripcion}?`)) {
        const index = zonas.value.findIndex(z => z.id === zona.id)
        if (index !== -1) {
          zonas.value[index].vigente = false
        }
      }
    }

    // Métodos placeholder para otras acciones (se mantienen igual)
    const verZona = (zona) => alert(`Viendo zona: ${zona.descripcion}`)
    const verDistrito = (distrito) => alert(`Viendo distrito: ${distrito.descripcion}`)
    const editarDistrito = (distrito) => alert(`Editando distrito: ${distrito.descripcion}`)
    const anularDistrito = (distrito) => {
      if (confirm(`¿Anular distrito ${distrito.descripcion}?`)) {
        const index = distritos.value.findIndex(d => d.id === distrito.id)
        if (index !== -1) distritos.value[index].vigente = false
      }
    }
    const verGrupo = (grupo) => alert(`Viendo grupo: ${grupo.descripcion}`)
    const editarGrupo = (grupo) => alert(`Editando grupo: ${grupo.descripcion}`)
    const anularGrupo = (grupo) => {
      if (confirm(`¿Anular grupo ${grupo.descripcion}?`)) {
        const index = grupos.value.findIndex(g => g.id === grupo.id)
        if (index !== -1) grupos.value[index].vigente = false
      }
    }
    const verRama = (rama) => alert(`Viendo rama: ${rama.descripcion}`)
    const editarRama = (rama) => alert(`Editando rama: ${rama.descripcion}`)
    const anularRama = (rama) => {
      if (confirm(`¿Anular rama ${rama.descripcion}?`)) {
        const index = ramas.value.findIndex(r => r.id === rama.id)
        if (index !== -1) ramas.value[index].vigente = false
      }
    }
    const verTipoCurso = (tipoCurso) => alert(`Viendo tipo curso: ${tipoCurso.descripcion}`)
    const editarTipoCurso = (tipoCurso) => alert(`Editando tipo curso: ${tipoCurso.descripcion}`)
    const anularTipoCurso = (tipoCurso) => {
      if (confirm(`¿Anular tipo curso ${tipoCurso.descripcion}?`)) {
        const index = tiposCurso.value.findIndex(t => t.id === tipoCurso.id)
        if (index !== -1) tiposCurso.value[index].vigente = false
      }
    }
    const verCargo = (cargo) => alert(`Viendo cargo: ${cargo.descripcion}`)
    const editarCargo = (cargo) => alert(`Editando cargo: ${cargo.descripcion}`)
    const anularCargo = (cargo) => {
      if (confirm(`¿Anular cargo ${cargo.descripcion}?`)) {
        const index = cargos.value.findIndex(c => c.id === cargo.id)
        if (index !== -1) cargos.value[index].vigente = false
      }
    }
    const verAlimentacion = (alimentacionItem) => alert(`Viendo alimentación: ${alimentacionItem.descripcion}`)
    const editarAlimentacion = (alimentacionItem) => alert(`Editando alimentación: ${alimentacionItem.descripcion}`)
    const anularAlimentacion = (alimentacionItem) => {
      if (confirm(`¿Anular alimentación ${alimentacionItem.descripcion}?`)) {
        const index = alimentacion.value.findIndex(a => a.id === alimentacionItem.id)
        if (index !== -1) alimentacion.value[index].vigente = false
      }
    }

    return {
      activeTab,
      modalActivo,
      editando,
      searchZonas,
      searchDistritos,
      searchGrupos,
      filtroZona,
      filtroDistrito,
      tabs,
      zonas,
      distritos,
      grupos,
      ramas,
      tiposCurso,
      cargos,
      alimentacion,
      formZona,
      filteredZonas,
      filteredDistritos,
      filteredGrupos,
      getZonaNombre,
      getDistritoNombre,
      abrirModal,
      cerrarModal,
      guardarZona,
      editarZona,
      anularZona,
      verZona,
      verDistrito,
      editarDistrito,
      anularDistrito,
      verGrupo,
      editarGrupo,
      anularGrupo,
      verRama,
      editarRama,
      anularRama,
      verTipoCurso,
      editarTipoCurso,
      anularTipoCurso,
      verCargo,
      editarCargo,
      anularCargo,
      verAlimentacion,
      editarAlimentacion,
      anularAlimentacion
    }
  }
}
</script>

<style scoped>
.mantenedores-scouts {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Main Content Styles */
.main-content {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #2c5aa0 0%, #1e3d73 100%);
  color: white;
  padding: 25px 30px;
  margin-bottom: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.header-title h1 {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.header-title p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.mantenedor-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mantenedor-selector label {
  font-weight: 600;
  font-size: 1.1rem;
}

.mantenedor-dropdown {
  padding: 10px 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  min-width: 200px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mantenedor-dropdown:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.mantenedor-dropdown:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.mantenedor-dropdown option {
  background: white;
  color: #333;
}

.mantenedor-section {
  padding: 30px;
  animation: fadeIn 0.5s ease;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 3px solid #2c5aa0;
}

.mantenedor-header h2 {
  color: #2c5aa0;
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.btn-primary {
  background: #2c5aa0;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #1e3d73;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
}

.alert {
  background: #e3f2fd;
  border: 1px solid #bbdefb;
  color: #1565c0;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 25px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.alert-icon {
  font-size: 1.2rem;
  margin-top: 2px;
}

.search-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.select-filter {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 200px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f8f9fa;
}

.data-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c5aa0;
  border-bottom: 2px solid #e1e5e9;
}

.data-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #e1e5e9;
}

.data-table tr:hover {
  background: #f8f9fa;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.btn-view {
  background: #e3f2fd;
  color: #1565c0;
}

.btn-edit {
  background: #fff3cd;
  color: #856404;
}

.btn-anular {
  background: #f8d7da;
  color: #721c24;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 25px 30px 20px;
  border-bottom: 2px solid #2c5aa0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #2c5aa0;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #2c5aa0;
}

.modal-body {
  padding: 25px 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #39424b;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-checkbox input {
  width: 18px;
  height: 18px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .mantenedor-selector {
    width: 100%;
  }
  
  .mantenedor-dropdown {
    flex: 1;
    min-width: auto;
  }
  
  .mantenedor-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .search-input, .select-filter {
    min-width: 100%;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .table-container {
    overflow-x: auto;
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>