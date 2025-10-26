<template>
  <div class="pago-view">
    <div class="navegacion-vistas">
      <button @click="cambiarVista('buscar')" :class="{ active: vistaActiva === 'buscar' }">
        <i class="fas fa-search"></i> Buscar Inscripciones
      </button>
      <button @click="cambiarVista('registrar')" :class="{ active: vistaActiva === 'registrar' }">
        <i class="fas fa-plus"></i> Registrar Pagos
      </button>
    </div>

    <div v-if="vistaActiva === 'buscar'" class="vista-buscar">
      <div class="header-acciones">
        <h2>Listado de Pagos</h2>
        <div class="filtros">
          <input type="text" v-model="filtroBusqueda" placeholder="Buscar por Nombre o RUT..." class="input-busqueda" @keyup.enter="buscar" />
          <button @click="buscar" class="btn btn-primario"><i class="fas fa-search"></i> Buscar</button>
          <button @click="limpiarBusqueda" class="btn btn-secundario">Limpiar</button>
          <button @click="exportarCSV" class="btn btn-secundario"><i class="fas fa-file-csv"></i> Exportar</button>
        </div>
      </div>

      <DataTable :rows="pagosFiltrados" :columns="columns" @editar="abrirModal" @anular="abrirModalAnular" />
    </div>

    <div v-if="vistaActiva === 'registrar'" class="vista-registrar">
      <div class="card-registro">
        <h3><i class="fas fa-user"></i> Registro Individual</h3>
        <p>Completa el formulario para un participante específico. (Pendiente conexión API)</p>
        <form @submit.prevent="registrarPagoIndividual" class="form-registro-individual">
          <div class="form-group">
            <label for="indNombre">Nombre Completo</label>
            <input id="indNombre" v-model="formIndividual.nombre" type="text" required placeholder="Ej: Juan Pérez González">
          </div>
          <div class="form-group">
            <label for="indRUT">RUT</label>
            <input id="indRUT" v-model="formIndividual.rut" type="text" required placeholder="Ej: 12.345.678-9">
          </div>
          <div class="form-group">
            <label for="indCurso">Curso</label>
            <select id="indCurso" v-model="formIndividual.curso" required>
              <option value="">Seleccione un curso</option>
              <option value="Formación de Dirigentes">Formación de Dirigentes</option>
            </select>
          </div>
          <div class="form-group">
            <label for="indValor">Valor Pagado</label>
            <input id="indValor" v-model.number="formIndividual.valor_pagado" type="number" required placeholder="Ej: 25000">
          </div>
          <div class="form-group">
            <label for="indFecha">Fecha de Pago</label>
            <input id="indFecha" v-model="formIndividual.fecha_pago" type="date" required>
          </div>
          <div class="form-group">
            <label for="indGrupo">Grupo</label>
            <select id="indGrupo" v-model="formIndividual.grupo" required>
              <option value="">Seleccione un grupo</option>
              <option value="Ñuble">Ñuble</option>
              <option value="Biobío">Biobío</option>
            </select>
          </div>
          <div class="form-group">
            <label for="indComprobante">Comprobante (Opcional)</label>
            <input type="file" id="indComprobante" @change="handleFileIndividual">
          </div>
          <button type="submit" class="btn btn-primario">Registrar Pago Individual</button>
        </form>
      </div>

      <div class="card-registro">
        <h3><i class="fas fa-users"></i> Registro Masivo</h3>
        <p>1. Filtra por Grupo/Curso. 2. Selecciona participantes. 3. Sube el comprobante. (Pendiente conexión API)</p>
        <form @submit.prevent="registrarPagoMasivo" class="form-registro-masivo">
          <div class="form-group">
            <label for="grupoMasivo">Grupo</label>
            <select id="grupoMasivo" v-model="formMasivo.grupo" required>
              <option value="">Seleccione un grupo</option>
              <option value="Ñuble">Ñuble</option>
              <option value="Biobío">Biobío</option>
            </select>
          </div>
          <div class="form-group">
            <label for="cursoMasivo">Curso</label>
            <select id="cursoMasivo" v-model="formMasivo.curso" required>
              <option value="">Seleccione un curso</option>
              <option value="Formación de Dirigentes">Formación de Dirigentes</option>
            </select>
          </div>
          <button type="button" @click="cargarParticipantesParaMasivo" :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoUsuarios" class="btn btn-secundario">
            <i v-if="cargandoUsuarios" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-download"></i>
            Cargar Participantes
          </button>
          <div v-if="participantesCargados.length > 0" class="lista-usuarios-masivo">
            <label>Participantes encontrados ({{ participantesCargados.length }}):</label>
            <div v-for="user in participantesCargados" :key="user.id" class="checkbox-item">
              <input type="checkbox" :id="'user-' + user.id" :value="user" v-model="participantesSeleccionados">
              <label :for="'user-' + user.id">{{ user.nombre }} ({{ user.rut }})</label>
            </div>
          </div>
          <div class="form-group">
            <label for="comprobanteMasivo">Comprobante Grupal</label>
            <input type="file" id="comprobanteMasivo" @change="handleFileMasivo" required>
          </div>
          <button type="submit" class="btn btn-primario" :disabled="participantesSeleccionados.length === 0 || !formMasivo.file">
            Registrar Pago para ({{ participantesSeleccionados.length }}) Usuarios
          </button>
        </form>
      </div>
    </div>

    <BaseModal v-if="showModal" :pago="pagoSeleccionado" @cerrar="cerrarModal" @guardar="guardarPago" />

    <NotificationToast :mensaje="alerta.mensaje" :tipo="alerta.tipo" v-if="alerta.mensaje" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
import pagoPersonaService from '@/services/pagoPersonaService.js'

const columns = ref([
  { name: 'nombre', label: 'Nombre', field: 'nombre', sortable: true, align: 'left' },
  { name: 'rut', label: 'RUT', field: 'rut', align: 'left' },
  { name: 'curso', label: 'Curso', field: 'curso', sortable: true },
  { name: 'valor_pagado', label: 'Valor', field: 'valor_pagado', align: 'right' },
  { name: 'fecha_pago', label: 'Fecha Pago', field: 'fecha_pago' },
  { name: 'actions', label: 'Acciones', field: 'actions', align: 'center' }
])

const pagos = ref([])
const alerta = ref({ mensaje: '', tipo: '' })
const filtroBusqueda = ref('')
const terminoBuscado = ref('')
const vistaActiva = ref('buscar')
const cambiarVista = (vista) => { vistaActiva.value = vista }

const showModal = ref(false)
const showModalAnular = ref(false)
const pagoSeleccionado = ref(null)
const abrirModal = (pago) => { if (!pago) return; pagoSeleccionado.value = { ...pago }; showModal.value = true }
const cerrarModal = () => { showModal.value = false }
const abrirModalAnular = (pago) => { pagoSeleccionado.value = pago; showModalAnular.value = true }
const cerrarModalAnular = () => { showModalAnular.value = false }

onMounted(cargarPagos)
async function cargarPagos() {
  try {
    const data = await pagoPersonaService.listar()
    pagos.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Error detallado al cargar pagos:', error)
    mostrarAlerta('Error al cargar los pagos. Revisa la consola.', 'error')
    pagos.value = []
  }
}

const buscar = () => { terminoBuscado.value = filtroBusqueda.value }
const limpiarBusqueda = () => { filtroBusqueda.value = ''; terminoBuscado.value = '' }
const pagosFiltrados = computed(() => {
  if (!terminoBuscado.value) return pagos.value
  const busqueda = terminoBuscado.value.toLowerCase()
  if (!Array.isArray(pagos.value)) return []
  return pagos.value.filter(pago =>
    (pago.nombre && pago.nombre.toLowerCase().includes(busqueda)) ||
    (pago.rut && pago.rut.toLowerCase().includes(busqueda))
  )
})

async function guardarPago() { mostrarAlerta('Edición de pago aún no implementada con API', 'info'); cerrarModal() }
async function confirmarAnulacion() { mostrarAlerta('Anulación aún no implementada con API', 'info'); cerrarModalAnular() }
function mostrarAlerta(mensaje, tipo) { alerta.value = { mensaje, tipo }; setTimeout(() => { alerta.value = { mensaje: '', tipo: '' } }, 3000) }

const getInitialFormIndividual = () => ({ nombre: '', rut: '', curso: '', valor_pagado: null, tipo_alimentacion: 'Estándar', tipo_pago: 'Individual', grupo: '', fecha_pago: new Date().toISOString().split('T')[0], file: null, comprobante_url: '' })
const formIndividual = ref(getInitialFormIndividual())
const handleFileIndividual = (e) => { formIndividual.value.file = e.target.files[0] }
const registrarPagoIndividual = async () => {
  if (!formIndividual.value.nombre || !formIndividual.value.rut || !formIndividual.value.curso || !formIndividual.value.valor_pagado) {
    mostrarAlerta('Nombre, RUT, Curso y Valor son obligatorios', 'error'); return
  }
  mostrarAlerta('Registro individual simulado. Integración con API pendiente.', 'info')
  formIndividual.value = getInitialFormIndividual()
  const el = document.getElementById('indComprobante'); if (el) el.value = null
  await cargarPagos()
}

const getInitialFormMasivo = () => ({ grupo: '', curso: '', file: null })
const formMasivo = ref(getInitialFormMasivo())
const participantesCargados = ref([])
const participantesSeleccionados = ref([])
const cargandoUsuarios = ref(false)
const handleFileMasivo = (e) => { formMasivo.value.file = e.target.files[0] }
async function cargarParticipantesParaMasivo() { cargandoUsuarios.value = true; participantesCargados.value = []; participantesSeleccionados.value = []; mostrarAlerta('Carga de participantes simulada. Integración con API pendiente.', 'info'); cargandoUsuarios.value = false }
const registrarPagoMasivo = async () => {
  if (participantesSeleccionados.value.length === 0) { mostrarAlerta('Debe seleccionar al menos un participante.', 'error'); return }
  if (!formMasivo.value.file) { mostrarAlerta('Debe adjuntar un comprobante de pago.', 'error'); return }
  mostrarAlerta(`Pago masivo (simulado) para ${participantesSeleccionados.value.length} usuarios.`, 'info')
  formMasivo.value = getInitialFormMasivo(); participantesCargados.value = []; participantesSeleccionados.value = []
  const el = document.getElementById('comprobanteMasivo'); if (el) el.value = null
}
</script>

<style scoped>
.navegacion-vistas { display: flex; border-bottom: 2px solid #ccc; margin-bottom: 2rem; }
.navegacion-vistas button { padding: 1rem 1.5rem; border: none; background-color: transparent; cursor: pointer; font-size: 1.1rem; color: #555; font-weight: 500; border-bottom: 3px solid transparent; transition: all 0.3s ease; margin-bottom: -2px; }
.navegacion-vistas button i { margin-right: 8px; }
.navegacion-vistas button.active { color: var(--color-primario, #005A9C); border-bottom-color: var(--color-primario, #005A9C); }
.navegacion-vistas button:hover:not(.active) { background-color: #f4f4f4; }

.header-acciones { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; }
.header-acciones h2 { margin: 0; color: #333; }
.filtros { display: flex; gap: 1rem; align-items: center; }
.input-busqueda { padding: 0.75rem 1rem; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; min-width: 300px; }

.vista-registrar { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
.card-registro { background-color: #fff; border: 1px solid #e0e0e0; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }
.card-registro h3 { margin-top: 0; color: var(--color-primario, #005A9C); display: flex; align-items: center; gap: 10px; }
.card-registro p { color: #666; line-height: 1.6; margin-bottom: 1.5rem; }
.form-registro-individual, .form-registro-masivo { display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem; }
.form-group { display: flex; flex-direction: column; }
.form-group label { font-weight: 600; margin-bottom: 0.5rem; color: #444; }
.form-group select, .form-group input { padding: 0.75rem 1rem; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; width: 100%; }
.form-group input[type="file"] { padding: 0.5rem; }
.lista-usuarios-masivo { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-top: 0.5rem; max-height: 200px; overflow-y: auto; background-color: #f9f9f9; }
.lista-usuarios-masivo label { font-weight: 600; color: #333; display: block; margin-bottom: 0.5rem; }
.checkbox-item { display: flex; align-items: center; gap: 10px; padding: 0.5rem 0; }
.checkbox-item input[type="checkbox"] { width: auto; }
.checkbox-item label { font-weight: normal; color: #555; margin-bottom: 0; }

.btn { padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem; transition: all 0.3s ease; white-space: nowrap; }
.btn-primario { background-color: var(--color-primario, #005A9C); color: white; }
.btn-primario:hover { background-color: #004a80; }
.btn-secundario { background-color: #f0f0f0; color: #333; border: 1px solid #ccc; }
.btn-secundario:hover { background-color: #e0e0e0; }
.btn:disabled { background-color: #ccc; cursor: not-allowed; opacity: 0.7; }

@media (max-width: 900px) { .vista-registrar { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .header-acciones { flex-direction: column; align-items: flex-start; gap: 1rem; } .filtros { flex-direction: column; width: 100%; align-items: stretch; } .input-busqueda { min-width: auto; width: 100%; } }
</style>