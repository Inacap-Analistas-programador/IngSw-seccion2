<template>
  <div class="pago-view">
    
    <div class="navegacion-vistas">
      <button 
        @click="cambiarVista('buscar')" 
        :class="{ active: vistaActiva === 'buscar' }">
        <i class="fas fa-search"></i> Buscar Inscripciones
      </button>
      <button 
        @click="cambiarVista('registrar')" 
        :class="{ active: vistaActiva === 'registrar' }">
        <i class="fas fa-plus"></i> Registrar Pagos
      </button>
    </div>

    <div v-if="vistaActiva === 'buscar'" class="vista-buscar">
      <div class="header-acciones">
        <h2>Listado de Pagos</h2>
        <div class="filtros">
          <input 
            type="text" 
            v-model="filtroBusqueda" 
            placeholder="Buscar por Nombre o RUT..."
            class="input-busqueda"
            @keyup.enter="buscar" 
          />
          <button @click="buscar" class="btn btn-primario">
            <i class="fas fa-search"></i> Buscar
          </button>
          <button @click="limpiarBusqueda" class="btn btn-secundario">
            Limpiar
          </button>
          <button @click="exportarCSV" class="btn btn-secundario">
            <i class="fas fa-file-csv"></i> Exportar
          </button>
        </div>
      </div>
      
      <DataTable
        :rows="pagosFiltrados" 
        :columns="columns"
        @editar="abrirModal"        @anular="abrirModalAnular"  />
    </div>

    <div v-if="vistaActiva === 'registrar'" class="vista-registrar">
      
      <div class="card-registro">
        <h3><i class="fas fa-user"></i> Registro Individual</h3>
        <p>Registra un nuevo pago para un participante específico. Esto abrirá el formulario de inscripción individual.</p>
        <button @click="abrirModal(null)" class="btn btn-primario">
          Registrar Pago Individual
        </button>
      </div>

      <div class="card-registro">
        <h3><i class="fas fa-users"></i> Registro Masivo</h3>
        <p>Registra un pago grupal (ej. depósito de grupo) y asígnalo a múltiples participantes del mismo grupo y curso.</p>
        
        <form @submit.prevent="registrarPagoMasivo" class="form-masivo">
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
           <div class="form-group">
            <label for="comprobanteMasivo">Comprobante Grupal</label>
            <input type="file" id="comprobanteMasivo" @change="handleFileMasivo" required>
          </div>
          <button type="submit" class="btn btn-primario">Registrar Pago Masivo</button>
        </form>
      </div>
    </div>

    <BaseModal
      v-if="showModal"
      :pago="pagoSeleccionado"
      @cerrar="cerrarModal"
      @guardar="guardarPago"
    />

    <!-- <ConfirmDialog
      v-if="showModalAnular"
      :pago="pagoSeleccionado"
      @cerrar="cerrarModalAnular"
      @confirmar="confirmarAnulacion"
    /> -->

    <NotificationToast :mensaje="alerta.mensaje" :tipo="alerta.tipo" v-if="alerta.mensaje" />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

// --- SECCIÓN DE IMPORTS ---
import pagosService from '@/services/pagosService.js' 
import DataTable from '@/components/Reutilizables/DataTable.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
// -------------------------------------

// --- DEFINICIÓN DE COLUMNAS ---
const columns = ref([
  { name: 'nombre', label: 'Nombre', field: 'nombre', sortable: true, align: 'left' },
  { name: 'rut', label: 'RUT', field: 'rut', align: 'left' },
  { name: 'curso', label: 'Curso', field: 'curso', sortable: true },
  { name: 'valor_pagado', label: 'Valor', field: 'valor_pagado', align: 'right' },
  { name: 'tipo_pago', label: 'Tipo Pago', field: 'tipo_pago' },
  { name: 'fecha_pago', label: 'Fecha Pago', field: 'fecha_pago' },
  // Esta línea le dice a DataTable.vue que renderice los botones:
  { name: 'actions', label: 'Acciones', field: 'actions', align: 'center' }
]);
// ------------------------------------

// --- ESTADO PRINCIPAL ---
const pagos = ref([]) 
const alerta = ref({ mensaje: '', tipo: '' })

// --- ESTADO PARA BÚSQUEDA MANUAL ---
const filtroBusqueda = ref('') // El texto en el input
const terminoBuscado = ref('') // El texto que se busca

// --- ESTADO PARA PESTAÑAS ---
const vistaActiva = ref('buscar') 

const cambiarVista = (vista) => {
  vistaActiva.value = vista
}

// --- LÓGICA DE MODALES ---
const showModal = ref(false)
const showModalAnular = ref(false)
const pagoSeleccionado = ref(null)

// Esta función maneja VER y MODIFICAR
const abrirModal = (pago) => {
  pagoSeleccionado.value = pago ? { ...pago } : null
  showModal.value = true
}
const cerrarModal = () => {
  showModal.value = false
}

// Esta función maneja ELIMINAR
const abrirModalAnular = (pago) => {
  pagoSeleccionado.value = pago
  showModalAnular.value = true
}
const cerrarModalAnular = () => {
  showModalAnular.value = false
}

// --- LÓGICA DE DATOS ---
onMounted(cargarPagos)

async function cargarPagos() {
  try {
    const data = await pagosService.obtenerPagos()
    pagos.value = Array.isArray(data) ? data : [] 
  } catch (error) {
    console.error("Error detallado al cargar pagos:", error);
    mostrarAlerta('Error al cargar los pagos. Revisa la consola.', 'error')
    pagos.value = [] 
  }
}

// --- LÓGICA DE BÚSQUEDA MANUAL ---
const buscar = () => {
  terminoBuscado.value = filtroBusqueda.value
}

const limpiarBusqueda = () => {
  filtroBusqueda.value = ''
  terminoBuscado.value = ''
}

const pagosFiltrados = computed(() => {
  if (!terminoBuscado.value) {
    return pagos.value
  }
  const busqueda = terminoBuscado.value.toLowerCase()
  if (!Array.isArray(pagos.value)) return [] 
  
  return pagos.value.filter(pago =>
    pago.nombre.toLowerCase().includes(busqueda) ||
    pago.rut.toLowerCase().includes(busqueda)
  )
})
// ---------------------------------

async function guardarPago(pagoData) {
  try {
    if (pagoData.id) {
      await pagosService.actualizarPago(pagoData.id, pagoData)
      mostrarAlerta('Pago actualizado correctamente', 'exito')
    } else {
      await pagosService.crearPago(pagoData)
      mostrarAlerta('Pago registrado correctamente', 'exito')
    }
    cargarPagos() 
    cerrarModal()
  } catch (error) {
    mostrarAlerta('Error al guardar el pago', 'error')
  }
}

async function confirmarAnulacion(pago) {
  try {
    // (Tu lógica de anulación aquí...)
    mostrarAlerta('Pago anulado correctamente', 'exito')
    cargarPagos()
    cerrarModalAnular()
  } catch (error) {
    mostrarAlerta('Error al anular el pago', 'error')
  }
}

function mostrarAlerta(mensaje, tipo) {
  alerta.value = { mensaje, tipo }
  setTimeout(() => {
    alerta.value = { mensaje: '', tipo: '' }
  }, 3000)
}

// --- LÓGICA NUEVA: REGISTRO MASIVO ---
const formMasivo = ref({
  grupo: '',
  curso: '',
  file: null
})

const handleFileMasivo = (event) => {
  formMasivo.value.file = event.target.files[0]
}

const registrarPagoMasivo = async () => {
  if (!formMasivo.value.grupo || !formMasivo.value.curso || !formMasivo.value.file) {
    mostrarAlerta('Complete todos los campos del formulario masivo', 'error')
    return
  }

  try {
    console.log('Registrando pago masivo:', formMasivo.value)
    mostrarAlerta('Lógica de pago masivo aún no implementada', 'info')
    
    formMasivo.value = { grupo: '', curso: '', file: null }
    document.getElementById('comprobanteMasivo').value = null 
    
  } catch (error) {
    mostrarAlerta('Error en el registro masivo', 'error')
  }
}

// Lógica de Exportar CSV (Existente)
const exportarCSV = () => {
  console.log('Exportando CSV...')
  mostrarAlerta('Función de exportar CSV ejecutada', 'info')
}

</script>

<style scoped>
/* --- ESTILOS PARA LAS PESTAÑAS --- */
.navegacion-vistas {
  display: flex;
  border-bottom: 2px solid #ccc;
  margin-bottom: 2rem;
}

.navegacion-vistas button {
  padding: 1rem 1.5rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 1.1rem;
  color: #555;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  margin-bottom: -2px; /* Alinea con el borde inferior */
}

.navegacion-vistas button i {
  margin-right: 8px;
}

.navegacion-vistas button.active {
  color: var(--color-primario, #005A9C); /* Usa tu variable de color primario */
  border-bottom-color: var(--color-primario, #005A9C);
}

.navegacion-vistas button:hover:not(.active) {
  background-color: #f4f4f4;
}

/* --- ESTILOS VISTA BÚSQUEDA (Existentes) --- */
.header-acciones {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.header-acciones h2 {
  margin: 0;
  color: #333;
}

.filtros {
  display: flex;
  gap: 1rem;
  align-items: center; /* Asegura que el input y botones estén alineados */
}

.input-busqueda {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 300px;
}

/* --- ESTILOS VISTA REGISTRO (Nuevos) --- */
.vista-registrar {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.card-registro {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-registro h3 {
  margin-top: 0;
  color: var(--color-primario, #005A9C);
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-registro p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

/* Formulario Masivo */
.form-masivo {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #444;
}

.form-group select,
.form-group input {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
}

/* Botones (reutilizando estilos genéricos) */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  white-space: nowrap; /* Evita que el texto del botón se parta */
}

.btn-primario {
  background-color: var(--color-primario, #005A9C);
  color: white;
}
.btn-primario:hover {
  background-color: #004a80;
}

.btn-secundario {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
}
.btn-secundario:hover {
  background-color: #e0e0e0;
}

/* Responsive */
@media (max-width: 900px) {
  .vista-registrar {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-acciones {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .filtros {
    flex-direction: column;
    width: 100%;
    align-items: stretch; /* Estira los botones y el input */
  }
  .input-busqueda {
    min-width: auto;
    width: 100%;
  }
}
</style>