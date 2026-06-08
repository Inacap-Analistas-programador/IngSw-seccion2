<template>
  <div class="lab-container">
    <div class="lab-sidebar">
      <h3>Panel de Control Lab</h3>
      <div class="control-group">
        <label><input type="checkbox" v-model="isEdit"> Modo Edición</label>
        <label><input type="checkbox" v-model="isReadOnly"> Solo Lectura</label>
        <label><input type="checkbox" v-model="loading"> Simulando Carga</label>
      </div>
      
      <div class="data-preview">
        <h4>Datos Emitidos (Guardar)</h4>
        <pre>{{ savedData ? JSON.stringify(savedData, null, 2) : 'Aún no se ha guardado' }}</pre>
      </div>

      <div class="data-preview">
        <h4>Eventos Emitidos</h4>
        <ul>
          <li v-for="(ev, idx) in eventsLog" :key="idx">{{ ev }}</li>
        </ul>
        <button v-if="eventsLog.length" @click="eventsLog = []" class="btn-clear">Limpiar Eventos</button>
      </div>
    </div>

    <div class="lab-content">
      <PersonaForm 
        :initial-data="mockInitialData"
        :options="mockOptions"
        :history="mockHistory"
        :is-edit="isEdit"
        :is-read-only="isReadOnly"
        :loading="loading"
        @save="onSave"
        @cancel="onCancel"
        @region-change="onRegionChange"
        @provincia-change="onProvinciaChange"
        @nav-course="onNavCourse"
        @show-alert="onShowAlert"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import PersonaForm from '@/components/personas/PersonaForm.vue'

// Controles de estado del Lab
const isEdit = ref(false)
const isReadOnly = ref(false)
const loading = ref(false)
const savedData = ref(null)
const eventsLog = ref([])

const logEvent = (name, payload) => {
  const time = new Date().toLocaleTimeString()
  eventsLog.value.unshift(`[${time}] ${name}: ${JSON.stringify(payload)}`)
}

// Handlers del componente
const onSave = (data) => {
  savedData.value = data
  logEvent('save', 'Datos recibidos')
  alert('Guardado (Ver en el panel)')
}
const onCancel = () => {
  logEvent('cancel', null)
}
const onRegionChange = (val) => {
  logEvent('region-change', val)
}
const onProvinciaChange = (val) => {
  logEvent('provincia-change', val)
}
const onNavCourse = (id) => {
  logEvent('nav-course', id)
}
const onShowAlert = (alertData) => {
  logEvent('show-alert', alertData)
  alert(`Alerta interna: ${alertData.text}`)
}

// Datos de prueba (Mocks)
const mockInitialData = reactive({
  PER_NOMBRES: 'Juan Pablo',
  PER_APELPTA: 'Pérez',
  PER_APELMAT: 'González',
  PER_RUN: '19123456',
  PER_DV: '9',
  PER_MAIL: 'juan.perez@example.com',
  PER_FONO: '912345678',
  PER_DIRECCION: 'Av. Siempre Viva 123',
  TIPO_ORGANIZACION: 'GRUPO',
  IS_FORMADOR: false,
  ramas: [{ NIV_ID: 1, RAM_ID_NIVEL: 1 }]
})

const mockHistory = ref([
  { PEC_ID: 1, CUS_ID: 101, CUR_NOMBRE: 'Curso Institucional Inicial', CUR_CODIGO: 'CII-2026', ROL_DESCRIPCION: 'Participante', ESTADO_APROBACION: { aprobado: true, texto: 'Aprobado' } },
  { PEC_ID: 2, CUS_ID: 102, CUR_NOMBRE: 'Taller de Primeros Auxilios', CUR_CODIGO: 'TPA-2026', ROL_DESCRIPCION: 'Formador', ESTADO_APROBACION: { aprobado: false, texto: 'Pendiente' } }
])

const mockOptions = reactive({
  roles: [
    { value: 1, label: 'Dirigente' },
    { value: 2, label: 'Guiadora' },
    { value: 3, label: 'Apoderado' }
  ],
  grupos: [
    { value: 1, label: 'Grupo San Miguel' },
    { value: 2, label: 'Grupo Los Leones' }
  ],
  cargos: [
    { value: 1, label: 'Jefe de Grupo' },
    { value: 2, label: 'Asistente de Rama' }
  ],
  ramas: [
    { value: 1, label: 'Golondrinas' },
    { value: 2, label: 'Lobatos' },
    { value: 3, label: 'Guías' },
    { value: 4, label: 'Scouts' }
  ],
  regiones: [
    { value: 13, label: 'Metropolitana' },
    { value: 5, label: 'Valparaíso' }
  ],
  provincias: [
    { value: 131, label: 'Santiago', zon_id: 1 },
    { value: 132, label: 'Cordillera', zon_id: 1 },
    { value: 51, label: 'Valparaíso', zon_id: 2 }
  ],
  comunas: [
    { value: 13101, label: 'Santiago Centro' },
    { value: 13114, label: 'Las Condes' }
  ],
  estadoCivil: [
    { value: 1, label: 'Soltero/a' },
    { value: 2, label: 'Casado/a' }
  ],
  alimentacion: [
    { value: 1, label: 'Omnívoro' },
    { value: 2, label: 'Vegetariano' },
    { value: 3, label: 'Celíaco' }
  ],
  niveles: [
    { value: 1, label: 'Nivel 1' },
    { value: 2, label: 'Nivel 2' }
  ],
  zonas: [
    { value: 1, label: 'Zona Centro' },
    { value: 2, label: 'Zona Costa' }
  ],
  distritos: [
    { value: 101, label: 'Distrito Norte', zon_id: 1 },
    { value: 102, label: 'Distrito Sur', zon_id: 1 },
    { value: 201, label: 'Distrito Viña', zon_id: 2 }
  ]
})
</script>

<style scoped>
.lab-container {
  display: flex;
  height: 100vh;
  background-color: #f1f5f9;
  font-family: 'Inter', sans-serif;
}

.lab-sidebar {
  width: 350px;
  background: white;
  padding: 20px;
  border-right: 1px solid #e2e8f0;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0,0,0,0.05);
}

.lab-sidebar h3 {
  margin-top: 0;
  color: #1e293b;
  border-bottom: 2px solid #3b82f6;
  padding-bottom: 10px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.control-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  cursor: pointer;
  color: #334155;
}

.data-preview {
  background: #1e293b;
  color: #10b981;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.data-preview h4 {
  margin: 0 0 10px 0;
  color: #f8fafc;
  font-size: 0.9rem;
}

.data-preview pre {
  font-size: 0.75rem;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}

.data-preview ul {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.8rem;
  max-height: 200px;
  overflow-y: auto;
  color: #94a3b8;
}

.data-preview li {
  padding: 4px 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.btn-clear {
  margin-top: 10px;
  background: #ef4444;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.lab-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  display: flex;
  justify-content: center;
}

.lab-content > * {
  width: 100%;
  max-width: 1100px;
}
</style>
