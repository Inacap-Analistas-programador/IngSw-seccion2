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
          <h2>🗺️ Gestión de Zonas</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-zona')">
            + Nueva Zona
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Las zonas son agrupaciones geográficas de distritos scouts."
        />
        
        <div class="stats-cards">
          <DataCard 
            title="Zonas Activas"
            :value="zonas.filter(z => z.vigente).length"
            description="Total registrado"
          />
          <DataCard 
            title="Distritos Asociados"
            :value="distritos.length"
            description="En todas las zonas"
          />
          <DataCard 
            title="Grupos Totales"
            :value="grupos.length"
            description="Distribuidos por zona"
          />
        </div>
        
        <div class="search-bar">
          <InputBase 
            v-model="searchZonas"
            placeholder="Buscar zona por descripción..."
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
          @delete="anularZona"
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
          @delete="anularDistrito"
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
          @delete="anularGrupo"
        />
      </div>
      
      <!-- Ramas -->
      <div v-if="activeTab === 'ramas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🏕️ Gestión de Ramas</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-rama')">
            + Nueva Rama
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Las ramas definen las divisiones por edad dentro del movimiento scout."
        />
        
        <DataTable 
          :columns="columnsRamas"
          :rows="ramas"
          :pageSize="10"
          @view="verRama"
          @edit="editarRama"
          @delete="anularRama"
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
          @delete="anularTipoCurso"
        />
      </div>
      
      <!-- Cargos -->
      <div v-if="activeTab === 'cargos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>👔 Gestión de Cargos</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-cargo')">
            + Nuevo Cargo
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Los cargos definen las responsabilidades dentro de la organización scout."
        />
        
        <DataTable 
          :columns="columnsCargos"
          :rows="cargos"
          :pageSize="10"
          @view="verCargo"
          @edit="editarCargo"
          @delete="anularCargo"
        />
      </div>
      
      <!-- Alimentación -->
      <div v-if="activeTab === 'alimentacion'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>🍽️ Gestión de Alimentación</h2>
          <BaseButton variant="primary" @click="abrirModal('crear-alimentacion')">
            + Nueva Alimentación
          </BaseButton>
        </div>
        
        <BaseAlert 
          type="info" 
          title="Información" 
          message="Tipos de alimentación disponibles para los participantes de cursos."
        />
        
        <DataTable 
          :columns="columnsAlimentacion"
          :rows="alimentacion"
          :pageSize="5"
          @view="verAlimentacion"
          @edit="editarAlimentacion"
          @delete="anularAlimentacion"
        />
      </div>
    </div>
    
    <!-- Modales -->
    
    <!-- Modal: Zona -->
    <BaseModal 
      v-if="modalActivo === 'crear-zona'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nueva'} Zona`"
    >
      <form @submit.prevent="guardarZona">
        <div class="form-group">
          <InputBase 
            v-model="formZona.descripcion"
            label="Descripción de la Zona:"
            placeholder="Ej: ZONA NORTE BIOBÍO"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseCheckBox 
            v-model="formZona.unilateral"
            label="Zona Unilateral"
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formZona.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Distrito -->
    <BaseModal 
      v-if="modalActivo === 'crear-distrito'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Distrito`"
    >
      <form @submit.prevent="guardarDistrito">
        <div class="form-group">
          <InputBase 
            v-model="formDistrito.descripcion"
            label="Descripción del Distrito:"
            placeholder="Ej: DISTRITO CONCEPCIÓN"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formDistrito.zona_id"
            :options="opcionesZonasSelect"
            label="Zona:"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formDistrito.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Grupo -->
    <BaseModal 
      v-if="modalActivo === 'crear-grupo'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Grupo Scout`"
    >
      <form @submit.prevent="guardarGrupo">
        <div class="form-group">
          <InputBase 
            v-model="formGrupo.descripcion"
            label="Descripción del Grupo:"
            placeholder="Ej: GRUPO ARAUCO"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formGrupo.distrito_id"
            :options="opcionesDistritosSelect"
            label="Distrito:"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formGrupo.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Rama -->
    <BaseModal 
      v-if="modalActivo === 'crear-rama'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nueva'} Rama`"
    >
      <form @submit.prevent="guardarRama">
        <div class="form-group">
          <InputBase 
            v-model="formRama.descripcion"
            label="Descripción de la Rama:"
            placeholder="Ej: LOBATOS"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formRama.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Tipo Curso -->
    <BaseModal 
      v-if="modalActivo === 'crear-tipo-curso'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Tipo de Curso`"
    >
      <form @submit.prevent="guardarTipoCurso">
        <div class="form-group">
          <InputBase 
            v-model="formTipoCurso.descripcion"
            label="Descripción del Tipo:"
            placeholder="Ej: CURSO BÁSICO"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formTipoCurso.tipo"
            label="Tipo:"
            type="number"
            placeholder="Ej: 1"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formTipoCurso.cant_participante"
            label="Cantidad de Participantes:"
            type="number"
            placeholder="Ej: 30"
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formTipoCurso.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Cargo -->
    <BaseModal 
      v-if="modalActivo === 'crear-cargo'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nuevo'} Cargo`"
    >
      <form @submit.prevent="guardarCargo">
        <div class="form-group">
          <InputBase 
            v-model="formCargo.descripcion"
            label="Descripción del Cargo:"
            placeholder="Ej: JEFE DE GRUPO"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formCargo.vigente"
            :options="estadosBooleanos"
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
    
    <!-- Modal: Alimentación -->
    <BaseModal 
      v-if="modalActivo === 'crear-alimentacion'" 
      @close="cerrarModal"
      :title="`${editando ? 'Editar' : 'Nueva'} Alimentación`"
    >
      <form @submit.prevent="guardarAlimentacion">
        <div class="form-group">
          <InputBase 
            v-model="formAlimentacion.descripcion"
            label="Descripción de la Alimentación:"
            placeholder="Ej: DIETA VEGETARIANA"
            required
          />
        </div>
        
        <div class="form-group">
          <InputBase 
            v-model="formAlimentacion.tipo"
            label="Tipo:"
            type="number"
            placeholder="Ej: 1"
            required
          />
        </div>
        
        <div class="form-group">
          <BaseSelect 
            v-model="formAlimentacion.vigente"
            :options="estadosBooleanos"
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
import BaseAlert from './BaseAlert.vue'
import BaseButton from './BaseButton.vue'
import BaseModal from './BaseModal.vue'
import BaseSelect from './BaseSelect.vue'
import BaseCheckBox from './BaseCheckBox.vue'
import InputBase from './InputBase.vue'
import DataTable from './DataTable.vue'
import DataCard from './DataCard.vue'

// Estado reactivo
const activeTab = ref('zonas')
const modalActivo = ref('')
const editando = ref(false)
const searchZonas = ref('')
const searchDistritos = ref('')
const searchGrupos = ref('')

// Tabs de navegación - Actualizadas según BD
const tabs = [
  { id: 'zonas', label: 'Zonas', icon: '🗺️' },
  { id: 'distritos', label: 'Distritos', icon: '📍' },
  { id: 'grupos', label: 'Grupos Scout', icon: '👥' },
  { id: 'ramas', label: 'Ramas', icon: '🏕️' },
  { id: 'tipos-curso', label: 'Tipos Curso', icon: '📚' },
  { id: 'cargos', label: 'Cargos', icon: '👔' },
  { id: 'alimentacion', label: 'Alimentación', icon: '🍽️' }
]

// Datos de ejemplo según estructura de BD
const zonas = ref([
  { id: 1, descripcion: 'ZONA NORTE BIOBÍO', unilateral: true, vigente: true },
  { id: 2, descripcion: 'ZONA SUR BIOBÍO', unilateral: false, vigente: true },
  { id: 3, descripcion: 'ZONA COSTA BIOBÍO', unilateral: true, vigente: true },
  { id: 4, descripcion: 'ZONA CORDILLERA BIOBÍO', unilateral: false, vigente: true }
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

const formDistrito = reactive({
  id: null,
  descripcion: '',
  zona_id: null,
  vigente: true
})

const formGrupo = reactive({
  id: null,
  descripcion: '',
  distrito_id: null,
  vigente: true
})

const formRama = reactive({
  id: null,
  descripcion: '',
  vigente: true
})

const formTipoCurso = reactive({
  id: null,
  descripcion: '',
  tipo: '',
  cant_participante: '',
  vigente: true
})

const formCargo = reactive({
  id: null,
  descripcion: '',
  vigente: true
})

const formAlimentacion = reactive({
  id: null,
  descripcion: '',
  tipo: '',
  vigente: true
})

// Opciones para selects
const estadosBooleanos = ref([
  { value: true, label: 'Activo' },
  { value: false, label: 'Inactivo' }
])

const opcionesZonas = computed(() => {
  return ['Todas las zonas', ...new Set(zonas.value.map(z => z.descripcion))]
})

const opcionesDistritos = computed(() => {
  return ['Todos los distritos', ...new Set(distritos.value.map(d => d.descripcion))]
})

const opcionesZonasSelect = computed(() => {
  return zonas.value.map(z => ({ value: z.id, label: z.descripcion }))
})

const opcionesDistritosSelect = computed(() => {
  return distritos.value.map(d => ({ value: d.id, label: d.descripcion }))
})

// Columnas para DataTable - Actualizadas según BD
const columnsZonas = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'unilateral', label: 'Unilateral', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsDistritos = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'zona_id', label: 'Zona', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsGrupos = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'distrito_id', label: 'Distrito', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsRamas = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsTiposCurso = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'tipo', label: 'Tipo', sortable: true },
  { key: 'cant_participante', label: 'Cant. Participantes', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsCargos = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

const columnsAlimentacion = ref([
  { key: 'descripcion', label: 'Descripción', sortable: true },
  { key: 'tipo', label: 'Tipo', sortable: true },
  { key: 'vigente', label: 'Estado', sortable: true }
])

// Computed para filtros
const filteredZonas = computed(() => {
  if (!searchZonas.value) return zonas.value
  const term = searchZonas.value.toLowerCase()
  return zonas.value.filter(zona => 
    zona.descripcion.toLowerCase().includes(term)
  )
})

const filteredDistritos = computed(() => {
  let filtered = distritos.value
  
  if (searchDistritos.value) {
    const term = searchDistritos.value.toLowerCase()
    filtered = filtered.filter(distrito => 
      distrito.descripcion.toLowerCase().includes(term)
    )
  }
  
  return filtered
})

const filteredGrupos = computed(() => {
  let filtered = grupos.value
  
  if (searchGrupos.value) {
    const term = searchGrupos.value.toLowerCase()
    filtered = filtered.filter(grupo => 
      grupo.descripcion.toLowerCase().includes(term)
    )
  }
  
  return filtered
})

// Métodos
const abrirModal = (tipo) => {
  modalActivo.value = tipo
  editando.value = false
  // Limpiar formularios según el tipo
  const forms = {
    'crear-zona': formZona,
    'crear-distrito': formDistrito,
    'crear-grupo': formGrupo,
    'crear-rama': formRama,
    'crear-tipo-curso': formTipoCurso,
    'crear-cargo': formCargo,
    'crear-alimentacion': formAlimentacion
  }
  
  const form = forms[tipo]
  if (form) {
    Object.keys(form).forEach(key => {
      if (key === 'vigente') {
        form[key] = true
      } else if (key === 'unilateral') {
        form[key] = false
      } else {
        form[key] = ''
      }
    })
    form.id = null
  }
}

const cerrarModal = () => {
  modalActivo.value = ''
  editando.value = false
}

// Métodos de guardado
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

const guardarDistrito = () => {
  if (editando.value) {
    const index = distritos.value.findIndex(d => d.id === formDistrito.id)
    if (index !== -1) {
      distritos.value[index] = { ...formDistrito }
    }
  } else {
    const nuevoDistrito = {
      id: Math.max(...distritos.value.map(d => d.id)) + 1,
      ...formDistrito
    }
    distritos.value.push(nuevoDistrito)
  }
  cerrarModal()
}

const guardarGrupo = () => {
  if (editando.value) {
    const index = grupos.value.findIndex(g => g.id === formGrupo.id)
    if (index !== -1) {
      grupos.value[index] = { ...formGrupo }
    }
  } else {
    const nuevoGrupo = {
      id: Math.max(...grupos.value.map(g => g.id)) + 1,
      ...formGrupo
    }
    grupos.value.push(nuevoGrupo)
  }
  cerrarModal()
}

const guardarRama = () => {
  if (editando.value) {
    const index = ramas.value.findIndex(r => r.id === formRama.id)
    if (index !== -1) {
      ramas.value[index] = { ...formRama }
    }
  } else {
    const nuevaRama = {
      id: Math.max(...ramas.value.map(r => r.id)) + 1,
      ...formRama
    }
    ramas.value.push(nuevaRama)
  }
  cerrarModal()
}

const guardarTipoCurso = () => {
  if (editando.value) {
    const index = tiposCurso.value.findIndex(t => t.id === formTipoCurso.id)
    if (index !== -1) {
      tiposCurso.value[index] = { ...formTipoCurso }
    }
  } else {
    const nuevoTipoCurso = {
      id: Math.max(...tiposCurso.value.map(t => t.id)) + 1,
      ...formTipoCurso
    }
    tiposCurso.value.push(nuevoTipoCurso)
  }
  cerrarModal()
}

const guardarCargo = () => {
  if (editando.value) {
    const index = cargos.value.findIndex(c => c.id === formCargo.id)
    if (index !== -1) {
      cargos.value[index] = { ...formCargo }
    }
  } else {
    const nuevoCargo = {
      id: Math.max(...cargos.value.map(c => c.id)) + 1,
      ...formCargo
    }
    cargos.value.push(nuevoCargo)
  }
  cerrarModal()
}

const guardarAlimentacion = () => {
  if (editando.value) {
    const index = alimentacion.value.findIndex(a => a.id === formAlimentacion.id)
    if (index !== -1) {
      alimentacion.value[index] = { ...formAlimentacion }
    }
  } else {
    const nuevaAlimentacion = {
      id: Math.max(...alimentacion.value.map(a => a.id)) + 1,
      ...formAlimentacion
    }
    alimentacion.value.push(nuevaAlimentacion)
  }
  cerrarModal()
}

// Métodos para acciones - Cambiados a "Anular"
const verZona = (zona) => {
  console.log('Ver zona:', zona)
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

const verDistrito = (distrito) => {
  console.log('Ver distrito:', distrito)
}

const editarDistrito = (distrito) => {
  Object.assign(formDistrito, distrito)
  modalActivo.value = 'crear-distrito'
  editando.value = true
}

const anularDistrito = (distrito) => {
  if (confirm(`¿Está seguro que desea anular el distrito ${distrito.descripcion}?`)) {
    const index = distritos.value.findIndex(d => d.id === distrito.id)
    if (index !== -1) {
      distritos.value[index].vigente = false
    }
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

const anularGrupo = (grupo) => {
  if (confirm(`¿Está seguro que desea anular el grupo ${grupo.descripcion}?`)) {
    const index = grupos.value.findIndex(g => g.id === grupo.id)
    if (index !== -1) {
      grupos.value[index].vigente = false
    }
  }
}

const verRama = (rama) => {
  console.log('Ver rama:', rama)
}

const editarRama = (rama) => {
  Object.assign(formRama, rama)
  modalActivo.value = 'crear-rama'
  editando.value = true
}

const anularRama = (rama) => {
  if (confirm(`¿Está seguro que desea anular la rama ${rama.descripcion}?`)) {
    const index = ramas.value.findIndex(r => r.id === rama.id)
    if (index !== -1) {
      ramas.value[index].vigente = false
    }
  }
}

const verTipoCurso = (tipoCurso) => {
  console.log('Ver tipo curso:', tipoCurso)
}

const editarTipoCurso = (tipoCurso) => {
  Object.assign(formTipoCurso, tipoCurso)
  modalActivo.value = 'crear-tipo-curso'
  editando.value = true
}

const anularTipoCurso = (tipoCurso) => {
  if (confirm(`¿Está seguro que desea anular el tipo de curso ${tipoCurso.descripcion}?`)) {
    const index = tiposCurso.value.findIndex(t => t.id === tipoCurso.id)
    if (index !== -1) {
      tiposCurso.value[index].vigente = false
    }
  }
}

const verCargo = (cargo) => {
  console.log('Ver cargo:', cargo)
}

const editarCargo = (cargo) => {
  Object.assign(formCargo, cargo)
  modalActivo.value = 'crear-cargo'
  editando.value = true
}

const anularCargo = (cargo) => {
  if (confirm(`¿Está seguro que desea anular el cargo ${cargo.descripcion}?`)) {
    const index = cargos.value.findIndex(c => c.id === cargo.id)
    if (index !== -1) {
      cargos.value[index].vigente = false
    }
  }
}

const verAlimentacion = (alimentacion) => {
  console.log('Ver alimentación:', alimentacion)
}

const editarAlimentacion = (alimentacion) => {
  Object.assign(formAlimentacion, alimentacion)
  modalActivo.value = 'crear-alimentacion'
  editando.value = true
}

const anularAlimentacion = (alimentacion) => {
  if (confirm(`¿Está seguro que desea anular la alimentación ${alimentacion.descripcion}?`)) {
    const index = alimentacion.value.findIndex(a => a.id === alimentacion.id)
    if (index !== -1) {
      alimentacion.value[index].vigente = false
    }
  }
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