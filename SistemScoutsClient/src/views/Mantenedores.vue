<template>
  <div class="mantenedores-scouts">
    <!-- Header -->
    <div class="header">
      <h1>⚙️ Módulo de Mantenedores</h1>
      <p>Gestión de Datos Maestros del Sistema</p>
    </div>
    
    <!-- Navigation Tabs -->
    <div class="nav-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="nav-tab" 
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>
    
    <!-- Main Content -->
    <div class="mantenedor-content">
      <!-- Zonas -->
      <div v-if="activeTab === 'zonas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🗺️ Gestión de Zonas Scout</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-zona')">
            + Nueva Zona
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Las zonas son agrupaciones geográficas de distritos scouts. Cada zona agrupa varios distritos de la región."
        />
        
        <div class="stats-cards">
          <DataCard 
            v-for="stat in zonaStats" 
            :key="stat.title"
            :title="stat.title" 
            :value="stat.value" 
            :description="stat.description"
          />
        </div>
        
        <div class="search-bar">
          <InputBase 
            v-model="searchZonas"
            placeholder="Buscar zona por nombre o código..."
            class="search-input"
          />
          <BaseButton variant="primary">🔍 Buscar</BaseButton>
        </div>
        
        <DataTable 
          :columns="columnsZonas"
          :rows="filteredZonas"
          :pageSize="5"
          @view="verZona"
          @edit="editarZona"
          @delete="eliminarZona"
        />
      </div>
      
      <!-- Distritos -->
      <div v-if="activeTab === 'distritos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>📍 Gestión de Distritos</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-distrito')">
            + Nuevo Distrito
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Los distritos agrupan varios grupos scouts dentro de una zona específica."
        />
        
        <div class="search-bar">
          <InputBase 
            v-model="searchDistritos"
            placeholder="Buscar distrito..."
            class="search-input"
          />
          <BaseSelect 
            v-model="filtroZona"
            :options="opcionesZonas"
            placeholder="Todas las zonas"
          />
          <BaseButton variant="primary">🔍 Buscar</BaseButton>
        </div>
        
        <DataTable 
          :columns="columnsDistritos"
          :rows="filteredDistritos"
          :pageSize="5"
          @view="verDistrito"
          @edit="editarDistrito"
          @delete="eliminarDistrito"
        />
      </div>
      
      <!-- Grupos Scout -->
      <div v-if="activeTab === 'grupos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>👥 Gestión de Grupos Scout</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-grupo')">
            + Nuevo Grupo
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Los grupos scout son las unidades operativas donde se desarrollan las actividades con los jóvenes."
        />
        
        <div class="search-bar">
          <InputBase 
            v-model="searchGrupos"
            placeholder="Buscar grupo..."
            class="search-input"
          />
          <BaseSelect 
            v-model="filtroDistrito"
            :options="opcionesDistritos"
            placeholder="Todos los distritos"
          />
          <BaseButton variant="primary">🔍 Buscar</BaseButton>
        </div>
        
        <DataTable 
          :columns="columnsGrupos"
          :rows="filteredGrupos"
          :pageSize="5"
          @view="verGrupo"
          @edit="editarGrupo"
          @delete="eliminarGrupo"
        />
      </div>
      
      <!-- Secciones -->
      <div v-if="activeTab === 'secciones'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🏕️ Gestión de Secciones</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-seccion')">
            + Nueva Sección
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Las secciones son las divisiones por edad dentro del movimiento scout."
        />
        
        <DataTable 
          :columns="columnsSecciones"
          :rows="secciones"
          :pageSize="10"
          @view="verSeccion"
          @edit="editarSeccion"
        />
      </div>
      
      <!-- Tipos de Curso -->
      <div v-if="activeTab === 'tipos-curso'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>📚 Gestión de Tipos de Curso</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-tipo-curso')">
            + Nuevo Tipo
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Los tipos de curso definen las categorías de formación disponibles en el sistema."
        />
        
        <DataTable 
          :columns="columnsTiposCurso"
          :rows="tiposCurso"
          :pageSize="5"
          @view="verTipoCurso"
          @edit="editarTipoCurso"
          @delete="eliminarTipoCurso"
        />
      </div>
      
      <!-- Modalidades -->
      <div v-if="activeTab === 'modalidades'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>💻 Gestión de Modalidades</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-modalidad')">
            + Nueva Modalidad
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Las modalidades definen el formato de realización de los cursos."
        />
        
        <DataTable 
          :columns="columnsModalidades"
          :rows="modalidades"
          :pageSize="5"
          @view="verModalidad"
          @edit="editarModalidad"
          @delete="eliminarModalidad"
        />
      </div>
      
      <!-- Estados -->
      <div v-if="activeTab === 'estados'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🔄 Gestión de Estados del Sistema</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-estado')">
            + Nuevo Estado
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Los estados definen el flujo de trabajo de inscripciones y participantes en el sistema."
        />
        
        <DataTable 
          :columns="columnsEstados"
          :rows="estados"
          :pageSize="10"
          @view="verEstado"
          @edit="editarEstado"
        />
      </div>
    </div>
    
    <!-- Modales -->
    <BaseModal 
      v-if="modalActivo === 'crear-zona'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nueva'} Zona Scout`"
    >
      <form @submit.prevent="guardarZona">
        <div class="form-group">
          <InputBase 
            v-model="formZona.codigo"
            label="Código de Zona:"
            placeholder="Ej: ZN-005"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formZona.nombre"
            label="Nombre de la Zona:"
            placeholder="Ej: ZONA CENTRAL BIOBÍO"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formZona.region"
            :options="regiones"
            label="Región:"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formZona.descripcion"
            label="Descripción:"
            type="textarea"
            placeholder="Descripción de la zona..."
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formZona.estado"
            :options="estadosSistema"
            label="Estado:"
            required
          />
        </div>
        
        <div class="form-actions">
          <BaseButton type="button" variant="secondary" @click="cerrarModal">
            Cancelar
          </BaseButton>
          <BaseButton type="submit" variant="primary">
            💾 {{ editando ? 'Actualizar' : 'Guardar' }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>
    
    <!-- Modal Distrito -->
    <BaseModal 
      v-if="modalActivo === 'crear-distrito'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Distrito`"
    >
      <form @submit.prevent="guardarDistrito">
        <div class="form-group">
          <InputBase 
            v-model="formDistrito.codigo"
            label="Código de Distrito:"
            placeholder="Ej: DT-004"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formDistrito.nombre"
            label="Nombre del Distrito:"
            placeholder="Ej: DISTRITO CHILLÁN"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formDistrito.zona"
            :options="opcionesZonasSelect"
            label="Zona:"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formDistrito.responsable"
            label="Responsable del Distrito:"
            placeholder="Nombre del responsable"
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formDistrito.email"
            label="Email Contacto:"
            type="email"
            placeholder="contacto@distrito.cl"
            rules="email"
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formDistrito.estado"
            :options="estadosSistema"
            label="Estado:"
            required
          />
        </div>
        
        <div class="form-actions">
          <BaseButton type="button" variant="secondary" @click="cerrarModal">
            Cancelar
          </BaseButton>
          <BaseButton type="submit" variant="primary">
            💾 {{ editando ? 'Actualizar' : 'Guardar' }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>
    
    <!-- Modal Grupo -->
    <BaseModal 
      v-if="modalActivo === 'crear-grupo'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Grupo Scout`"
    >
      <form @submit.prevent="guardarGrupo">
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.numero"
            label="Número de Grupo:"
            placeholder="Ej: GP-004"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.nombre"
            label="Nombre del Grupo:"
            placeholder="Ej: GRUPO GALVARINO"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formGrupo.distrito"
            :options="opcionesDistritosSelect"
            label="Distrito:"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.comuna"
            label="Comuna:"
            placeholder="Ej: CONCEPCIÓN"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.direccion"
            label="Dirección:"
            placeholder="Dirección de la sede"
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.jefe"
            label="Jefe de Grupo:"
            placeholder="Nombre del jefe de grupo"
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.email"
            label="Email Contacto:"
            type="email"
            placeholder="contacto@grupo.cl"
            rules="email"
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.telefono"
            label="Teléfono:"
            placeholder="+56 9 1234 5678"
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.fechaFundacion"
            label="Fecha de Fundación:"
            type="date"
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formGrupo.estado"
            :options="estadosSistema"
            label="Estado:"
            required
          />
        </div>
        
        <div class="form-actions">
          <BaseButton type="button" variant="secondary" @click="cerrarModal">
            Cancelar
          </BaseButton>
          <BaseButton type="submit" variant="primary">
            💾 {{ editando ? 'Actualizar' : 'Guardar' }}
          </BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import InputBase from '@/components/Reutilizables/InputBase.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import DataCard from '@/components/Reutilizables/DataCard.vue'

// Estado reactivo
const activeTab = ref('zonas')
const modalActivo = ref('')
const editando = ref(false)
const searchZonas = ref('')
const searchDistritos = ref('')
const searchGrupos = ref('')
const filtroZona = ref('')
const filtroDistrito = ref('')

// Tabs de navegación
const tabs = [
  { id: 'zonas', label: 'Zonas', icon: '🗺️' },
  { id: 'distritos', label: 'Distritos', icon: '📍' },
  { id: 'grupos', label: 'Grupos Scout', icon: '👥' },
  { id: 'secciones', label: 'Secciones', icon: '🏕️' },
  { id: 'tipos-curso', label: 'Tipos de Curso', icon: '📚' },
  { id: 'modalidades', label: 'Modalidades', icon: '💻' },
  { id: 'estados', label: 'Estados', icon: '🔄' }
]

// Datos de ejemplo
const zonas = ref([
  { id: 1, codigo: 'ZN-001', nombre: 'ZONA NORTE BIOBÍO', region: 'Biobío', distritos: 3, estado: 'Activo' },
  { id: 2, codigo: 'ZN-002', nombre: 'ZONA SUR BIOBÍO', region: 'Biobío', distritos: 4, estado: 'Activo' },
  { id: 3, codigo: 'ZN-003', nombre: 'ZONA COSTA BIOBÍO', region: 'Biobío', distritos: 2, estado: 'Activo' },
  { id: 4, codigo: 'ZN-004', nombre: 'ZONA CORDILLERA BIOBÍO', region: 'Biobío', distritos: 3, estado: 'Activo' }
])

const distritos = ref([
  { id: 1, codigo: 'DT-001', nombre: 'DISTRITO CONCEPCIÓN', zona: 'ZONA NORTE BIOBÍO', grupos: 15, responsable: 'Juan Pérez', estado: 'Activo' },
  { id: 2, codigo: 'DT-002', nombre: 'DISTRITO TALCAHUANO', zona: 'ZONA NORTE BIOBÍO', grupos: 8, responsable: 'María González', estado: 'Activo' },
  { id: 3, codigo: 'DT-003', nombre: 'DISTRITO LOS ÁNGELES', zona: 'ZONA SUR BIOBÍO', grupos: 10, responsable: 'Carlos Ramírez', estado: 'Activo' }
])

const grupos = ref([
  { id: 1, numero: 'GP-001', nombre: 'GRUPO ARAUCO', distrito: 'DISTRITO CONCEPCIÓN', comuna: 'Concepción', integrantes: 85, estado: 'Activo' },
  { id: 2, numero: 'GP-002', nombre: 'GRUPO LAUTARO', distrito: 'DISTRITO TALCAHUANO', comuna: 'Talcahuano', integrantes: 72, estado: 'Activo' },
  { id: 3, numero: 'GP-003', nombre: 'GRUPO CAUPOLICÁN', distrito: 'DISTRITO LOS ÁNGELES', comuna: 'Los Ángeles', integrantes: 68, estado: 'Activo' }
])

const secciones = ref([
  { id: 1, codigo: 'SC-001', nombre: '🦫 CASTORES', edad: '5 - 7 años', color: 'Café', estado: 'Activo' },
  { id: 2, codigo: 'SC-002', nombre: '🐺 LOBATOS', edad: '7 - 11 años', color: 'Amarillo', estado: 'Activo' },
  { id: 3, codigo: 'SC-003', nombre: '🏕️ SCOUTS', edad: '11 - 15 años', color: 'Verde', estado: 'Activo' },
  { id: 4, codigo: 'SC-004', nombre: '⛺ PIONEROS', edad: '15 - 17 años', color: 'Rojo', estado: 'Activo' },
  { id: 5, codigo: 'SC-005', nombre: '🎒 ROVERS', edad: '17 - 21 años', color: 'Rojo Oscuro', estado: 'Activo' }
])

const tiposCurso = ref([
  { id: 1, codigo: 'TC-001', nombre: 'BÁSICO', descripcion: 'Curso de formación inicial', duracion: '3 días', estado: 'Activo' },
  { id: 2, codigo: 'TC-002', nombre: 'INTERMEDIO', descripcion: 'Curso de profundización', duracion: '4 días', estado: 'Activo' },
  { id: 3, codigo: 'TC-003', nombre: 'AVANZADO', descripcion: 'Curso de especialización', duracion: '5 días', estado: 'Activo' },
  { id: 4, codigo: 'TC-004', nombre: 'ESPECIALIZACIÓN', descripcion: 'Cursos temáticos específicos', duracion: '2 días', estado: 'Activo' }
])

const modalidades = ref([
  { id: 1, codigo: 'MD-001', nombre: 'PRESENCIAL', descripcion: 'Curso realizado completamente en formato presencial', estado: 'Activo' },
  { id: 2, codigo: 'MD-002', nombre: 'ONLINE', descripcion: 'Curso realizado completamente en formato virtual', estado: 'Activo' },
  { id: 3, codigo: 'MD-003', nombre: 'HÍBRIDO', descripcion: 'Curso con sesiones presenciales y virtuales', estado: 'Activo' }
])

const estados = ref([
  { id: 1, codigo: 'EST-001', nombre: 'PREINSCRITO', modulo: 'Inscripciones', descripcion: 'Solicitud de inscripción recibida', color: 'Amarillo' },
  { id: 2, codigo: 'EST-002', nombre: 'INSCRITO', modulo: 'Inscripciones', descripcion: 'Inscripción confirmada por administrador', color: 'Verde' },
  { id: 3, codigo: 'EST-003', nombre: 'REGISTRADO', modulo: 'Inscripciones', descripcion: 'Pago confirmado, registro completo', color: 'Azul' },
  { id: 4, codigo: 'EST-004', nombre: 'VIGENTE', modulo: 'Inscripciones', descripcion: 'Participante validado y asistiendo', color: 'Verde Oscuro' },
  { id: 5, codigo: 'EST-005', nombre: 'FINALIZADO', modulo: 'Inscripciones', descripcion: 'Curso completado por el participante', color: 'Gris' },
  { id: 6, codigo: 'EST-006', nombre: 'ANULADO', modulo: 'Inscripciones', descripcion: 'Inscripción cancelada (requiere justificación)', color: 'Rojo' },
  { id: 7, codigo: 'EST-007', nombre: 'LISTA DE ESPERA', modulo: 'Inscripciones', descripcion: 'En espera por cupos completos', color: 'Gris Claro' }
])

// Formularios
const formZona = reactive({
  id: null,
  codigo: '',
  nombre: '',
  region: '',
  descripcion: '',
  estado: 'Activo'
})

const formDistrito = reactive({
  id: null,
  codigo: '',
  nombre: '',
  zona: '',
  responsable: '',
  email: '',
  estado: 'Activo'
})

const formGrupo = reactive({
  id: null,
  numero: '',
  nombre: '',
  distrito: '',
  comuna: '',
  direccion: '',
  jefe: '',
  email: '',
  telefono: '',
  fechaFundacion: '',
  estado: 'Activo'
})

// Opciones para selects
const regiones = ref(['Biobío', 'Ñuble', 'Araucanía'])
const estadosSistema = ref(['Activo', 'Inactivo'])

const opcionesZonas = computed(() => {
  return ['Todas las zonas', ...new Set(zonas.value.map(z => z.nombre))]
})

const opcionesDistritos = computed(() => {
  return ['Todos los distritos', ...new Set(distritos.value.map(d => d.nombre))]
})

const opcionesZonasSelect = computed(() => {
  return zonas.value.map(z => ({ value: z.nombre, label: z.nombre }))
})

const opcionesDistritosSelect = computed(() => {
  return distritos.value.map(d => ({ value: d.nombre, label: d.nombre }))
})

// Estadísticas
const zonaStats = ref([
  { title: 'Zonas Activas', value: '4', description: 'Total registrado' },
  { title: 'Distritos Asociados', value: '12', description: 'En todas las zonas' },
  { title: 'Grupos Totales', value: '45', description: 'Distribuidos por zona' }
])

// Columnas para DataTable
const columnsZonas = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Zona', sortable: true },
  { key: 'region', label: 'Región', sortable: true },
  { key: 'distritos', label: 'N° Distritos', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsDistritos = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Distrito', sortable: true },
  { key: 'zona', label: 'Zona', sortable: true },
  { key: 'grupos', label: 'N° Grupos', sortable: true },
  { key: 'responsable', label: 'Responsable', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsGrupos = ref([
  { key: 'numero', label: 'N° Grupo', sortable: true },
  { key: 'nombre', label: 'Nombre', sortable: true },
  { key: 'distrito', label: 'Distrito', sortable: true },
  { key: 'comuna', label: 'Comuna', sortable: true },
  { key: 'integrantes', label: 'N° Integrantes', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsSecciones = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Sección', sortable: true },
  { key: 'edad', label: 'Rango de Edad', sortable: true },
  { key: 'color', label: 'Color Distintivo', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsTiposCurso = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Tipo', sortable: true },
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'duracion', label: 'Duración Típica', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsModalidades = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Modalidad', sortable: true },
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'estado', label: 'Estado', sortable: true }
])

const columnsEstados = ref([
  { key: 'codigo', label: 'Código', sortable: true },
  { key: 'nombre', label: 'Nombre Estado', sortable: true },
  { key: 'modulo', label: 'Módulo', sortable: true },
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'color', label: 'Color', sortable: true }
])

// Computed para filtros
const filteredZonas = computed(() => {
  if (!searchZonas.value) return zonas.value
  const term = searchZonas.value.toLowerCase()
  return zonas.value.filter(zona => 
    zona.nombre.toLowerCase().includes(term) || 
    zona.codigo.toLowerCase().includes(term)
  )
})

const filteredDistritos = computed(() => {
  let filtered = distritos.value
  
  if (searchDistritos.value) {
    const term = searchDistritos.value.toLowerCase()
    filtered = filtered.filter(distrito => 
      distrito.nombre.toLowerCase().includes(term)
    )
  }
  
  if (filtroZona.value && filtroZona.value !== 'Todas las zonas') {
    filtered = filtered.filter(distrito => distrito.zona === filtroZona.value)
  }
  
  return filtered
})

const filteredGrupos = computed(() => {
  let filtered = grupos.value
  
  if (searchGrupos.value) {
    const term = searchGrupos.value.toLowerCase()
    filtered = filtered.filter(grupo => 
      grupo.nombre.toLowerCase().includes(term)
    )
  }
  
  if (filtroDistrito.value && filtroDistrito.value !== 'Todos los distritos') {
    filtered = filtered.filter(grupo => grupo.distrito === filtroDistrito.value)
  }
  
  return filtered
})

// Métodos
const abrirModal = (tipo) => {
  modalActivo.value = tipo
  editando.value = false
  // Limpiar formularios
  Object.keys(formZona).forEach(key => formZona[key] = '')
  Object.keys(formDistrito).forEach(key => formDistrito[key] = '')
  Object.keys(formGrupo).forEach(key => formGrupo[key] = '')
}

const cerrarModal = () => {
  modalActivo.value = ''
  editando.value = false
}

const guardarZona = () => {
  if (editando.value) {
    // Actualizar zona existente
    const index = zonas.value.findIndex(z => z.id === formZona.id)
    if (index !== -1) {
      zonas.value[index] = { ...formZona }
    }
  } else {
    // Crear nueva zona
    const nuevaZona = {
      id: zonas.value.length + 1,
      ...formZona
    }
    zonas.value.push(nuevaZona)
  }
  cerrarModal()
}

const guardarDistrito = () => {
  if (editando.value) {
    // Actualizar distrito existente
    const index = distritos.value.findIndex(d => d.id === formDistrito.id)
    if (index !== -1) {
      distritos.value[index] = { ...formDistrito }
    }
  } else {
    // Crear nuevo distrito
    const nuevoDistrito = {
      id: distritos.value.length + 1,
      ...formDistrito
    }
    distritos.value.push(nuevoDistrito)
  }
  cerrarModal()
}

const guardarGrupo = () => {
  if (editando.value) {
    // Actualizar grupo existente
    const index = grupos.value.findIndex(g => g.id === formGrupo.id)
    if (index !== -1) {
      grupos.value[index] = { ...formGrupo }
    }
  } else {
    // Crear nuevo grupo
    const nuevoGrupo = {
      id: grupos.value.length + 1,
      ...formGrupo
    }
    grupos.value.push(nuevoGrupo)
  }
  cerrarModal()
}

// Métodos para acciones
const verZona = (zona) => {
  console.log('Ver zona:', zona)
}

const editarZona = (zona) => {
  Object.assign(formZona, zona)
  modalActivo.value = 'crear-zona'
  editando.value = true
}

const eliminarZona = (zona) => {
  if (confirm(`¿Está seguro que desea eliminar la zona ${zona.nombre}?`)) {
    zonas.value = zonas.value.filter(z => z.id !== zona.id)
  }
}

const verDistrito = (distrito) => {
  console.log('Ver distrito:', distrito)
}

const editarDistrito = (distrito) => {
  Object.assign(formDistrito, distrito)
  modalActivo.value = 'crear-distrito'
  editando.value = true
}

const eliminarDistrito = (distrito) => {
  if (confirm(`¿Está seguro que desea eliminar el distrito ${distrito.nombre}?`)) {
    distritos.value = distritos.value.filter(d => d.id !== distrito.id)
  }
}

const verGrupo = (grupo) => {
  console.log('Ver grupo:', grupo)
}

const editarGrupo = (grupo) => {
  Object.assign(formGrupo, grupo)
  modalActivo.value = 'crear-grupo'
  editando.value = true
}

const eliminarGrupo = (grupo) => {
  if (confirm(`¿Está seguro que desea eliminar el grupo ${grupo.nombre}?`)) {
    grupos.value = grupos.value.filter(g => g.id !== grupo.id)
  }
}

const verSeccion = (seccion) => {
  console.log('Ver sección:', seccion)
}

const editarSeccion = (seccion) => {
  console.log('Editar sección:', seccion)
}

const verTipoCurso = (tipoCurso) => {
  console.log('Ver tipo curso:', tipoCurso)
}

const editarTipoCurso = (tipoCurso) => {
  console.log('Editar tipo curso:', tipoCurso)
}

const eliminarTipoCurso = (tipoCurso) => {
  if (confirm(`¿Está seguro que desea eliminar el tipo de curso ${tipoCurso.nombre}?`)) {
    tiposCurso.value = tiposCurso.value.filter(t => t.id !== tipoCurso.id)
  }
}

const verModalidad = (modalidad) => {
  console.log('Ver modalidad:', modalidad)
}

const editarModalidad = (modalidad) => {
  console.log('Editar modalidad:', modalidad)
}

const eliminarModalidad = (modalidad) => {
  if (confirm(`¿Está seguro que desea eliminar la modalidad ${modalidad.nombre}?`)) {
    modalidades.value = modalidades.value.filter(m => m.id !== modalidad.id)
  }
}

const verEstado = (estado) => {
  console.log('Ver estado:', estado)
}

const editarEstado = (estado) => {
  console.log('Editar estado:', estado)
}
</script>

<style scoped>
.mantenedores-scouts {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: #f5f5f5;
  min-height: 100vh;
}

.header {
  background: #2c5aa0;
  color: white;
  padding: 20px;
  border-radius: 8px 8px 0 0;
  margin-bottom: 0;
}

.header h1 {
  margin: 0 0 8px 0;
  font-size: 1.8rem;
}

.header p {
  margin: 0;
  opacity: 0.9;
}

.nav-tabs {
  background: #1e3d73;
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 20px;
  border-radius: 0 0 8px 8px;
}

.nav-tab {
  background: #1e3d73;
  color: white;
  border: none;
  padding: 15px 20px;
  cursor: pointer;
  border-right: 1px solid #2c5aa0;
  transition: background 0.3s;
  font-size: 0.9rem;
  flex: 1;
  min-width: 120px;
}

.nav-tab:hover {
  background: #2c5aa0;
}

.nav-tab.active {
  background: #ff6b35;
  font-weight: bold;
}

.mantenedor-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.mantenedor-section {
  padding: 20px;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.mantenedor-header h2 {
  margin: 0;
  color: #2c5aa0;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.search-input {
  flex: 1;
  min-width: 250px;
}

.form-group {
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

/* Responsive */
@media (max-width: 768px) {
  .mantenedores-scouts {
    padding: 10px;
  }
  
  .nav-tabs {
    flex-direction: column;
  }
  
  .nav-tab {
    border-right: none;
    border-bottom: 1px solid #2c5aa0;
  }
  
  .mantenedor-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .search-input {
    min-width: 100%;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>