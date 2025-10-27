<template>
  <div class="pago-view">
    <!-- NUEVA NAVEGACIÓN DE VISTAS -->
    <div class="navegacion-vistas">
      <button 
        @click="cambiarVista('registro')" 
        :class="{ active: vistaActiva === 'registro' }">
        🧾 Registro / Ingreso
      </button>
      <button 
        @click="cambiarVista('historico')" 
        :class="{ active: vistaActiva === 'historico' }">
        📚 Histórico
      </button>
    </div>

    <!-- ✅ VISTA REGISTRO -->
    <div v-if="vistaActiva === 'registro'" class="vista-registrar">
      <div class="card-registro">
        <h3><i class="fas fa-user"></i> Registro Individual</h3>
        <p>Completa el formulario para registrar el pago de un participante.</p>
        
        <form @submit.prevent="registrarPagoIndividual" class="form-registro-individual">
          <div class="form-group">
            <label>Nombre Completo</label>
            <input v-model="formIndividual.nombre" type="text" required placeholder="Ej: Juan Pérez">
          </div>
          <div class="form-group">
            <label>RUT</label>
            <input v-model="formIndividual.rut" type="text" required placeholder="Ej: 12.345.678-9">
          </div>
          <div class="form-group">
            <label>Curso</label>
            <select v-model="formIndividual.curso" required>
              <option value="">Seleccione un curso</option>
              <option value="Formación de Dirigentes">Formación de Dirigentes</option>
            </select>
          </div>
          <div class="form-group">
            <label>Valor Pagado</label>
            <input v-model.number="formIndividual.valor_pagado" type="number" required placeholder="Ej: 25000">
          </div>
          <div class="form-group">
            <label>Fecha de Pago</label>
            <input v-model="formIndividual.fecha_pago" type="date" required>
          </div>
          <div class="form-group">
            <label>Grupo</label>
            <select v-model="formIndividual.grupo" required>
              <option value="">Seleccione un grupo</option>
              <option value="Ñuble">Ñuble</option>
              <option value="Biobío">Biobío</option>
            </select>
          </div>
          <div class="form-group">
            <label>Comprobante (opcional)</label>
            <input type="file" @change="handleFileIndividual">
          </div>
          <button type="submit" class="btn btn-primario">Registrar Pago</button>
        </form>
      </div>

      <div class="card-registro">
        <h3><i class="fas fa-users"></i> Registro Masivo</h3>
        <p>Seleccione grupo y curso, cargue participantes y suba comprobante grupal.</p>

        <form @submit.prevent="registrarPagoMasivo" class="form-registro-masivo">
          <div class="form-group">
            <label>Grupo</label>
            <select v-model="formMasivo.grupo" required>
              <option value="">Seleccione un grupo</option>
              <option value="Ñuble">Ñuble</option>
              <option value="Biobío">Biobío</option>
            </select>
          </div>
          <div class="form-group">
            <label>Curso</label>
            <select v-model="formMasivo.curso" required>
              <option value="">Seleccione un curso</option>
              <option value="Formación de Dirigentes">Formación de Dirigentes</option>
            </select>
          </div>

          <button 
            type="button" 
            @click="cargarParticipantesParaMasivo" 
            class="btn btn-secundario"
            :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoUsuarios">
            <i v-if="cargandoUsuarios" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-download"></i> Cargar Participantes
          </button>

          <div v-if="participantesCargados.length > 0" class="lista-usuarios-masivo">
            <label>Participantes encontrados ({{ participantesCargados.length }}):</label>
            <div v-for="user in participantesCargados" :key="user.id" class="checkbox-item">
              <input 
                type="checkbox" 
                :id="'user-' + user.id" 
                :value="user" 
                v-model="participantesSeleccionados">
              <label :for="'user-' + user.id">{{ user.nombre }} ({{ user.rut }})</label>
            </div>
          </div>

          <div class="form-group">
            <label>Comprobante Grupal</label>
            <input type="file" @change="handleFileMasivo" required>
          </div>

          <button 
            type="submit" 
            class="btn btn-primario" 
            :disabled="participantesSeleccionados.length === 0 || !formMasivo.file">
            Registrar Pago Masivo ({{ participantesSeleccionados.length }})
          </button>
        </form>
      </div>
    </div>

    <!-- ✅ VISTA HISTÓRICO -->
    <div v-if="vistaActiva === 'historico'" class="vista-buscar">
      <div class="header-acciones">
        <h2>Histórico de Pagos</h2>
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
        </div>
      </div>

      <div class="tabla-pagos">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>RUT</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Dirección</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="cargandoPagos">
              <td colspan="6" style="text-align: center;">Cargando pagos...</td>
            </tr>
            <tr v-else-if="pagosFiltrados.length === 0">
              <td colspan="6" style="text-align: center;">No se encontraron pagos</td>
            </tr>
            <tr v-else v-for="pago in pagosFiltrados" :key="pago.id">
              <td>{{ pago.nombre }}</td>
              <td>{{ pago.rut }}</td>
              <td>{{ pago.email || 'N/A' }}</td>
              <td>{{ pago.telefono || 'N/A' }}</td>
              <td>{{ pago.direccion || 'N/A' }}</td>
              <td>
                <button @click="abrirModal(pago)" class="btn-small btn-editar">Editar</button>
                <button @click="abrirModalAnular(pago)" class="btn-small btn-anular">Anular</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modales y alertas -->
    <BaseModal
      v-if="showModal"
      @close="cerrarModal"
    >
      <div class="modal-editar-pago">
        <h3>Editar Pago</h3>
        <div class="form-group">
          <label>Nombre</label>
          <input v-model="pagoSeleccionado.nombre" type="text" readonly>
        </div>
        <div class="form-group">
          <label>RUT</label>
          <input v-model="pagoSeleccionado.rut" type="text" readonly>
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="pagoSeleccionado.email" type="email">
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input v-model="pagoSeleccionado.telefono" type="text">
        </div>
        <div class="form-group">
          <label>Dirección</label>
          <input v-model="pagoSeleccionado.direccion" type="text">
        </div>
        <div class="modal-actions">
          <button @click="guardarPago" class="btn btn-primario">Guardar</button>
          <button @click="cerrarModal" class="btn btn-secundario">Cancelar</button>
        </div>
      </div>
    </BaseModal>

    <BaseModal
      v-if="showModalAnular"
      @close="cerrarModalAnular"
    >
      <div class="modal-confirmar">
        <h3>Confirmar Anulación</h3>
        <p>¿Está seguro de que desea anular el pago de <strong>{{ pagoSeleccionado?.nombre }}</strong>?</p>
        <div class="modal-actions">
          <button @click="confirmarAnulacion" class="btn btn-danger">Anular</button>
          <button @click="cerrarModalAnular" class="btn btn-secundario">Cancelar</button>
        </div>
      </div>
    </BaseModal>

    <NotificationToast 
      v-if="alerta.mensaje"
      :message="alerta.mensaje" 
      @close="alerta.mensaje = ''"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import pagosService from '@/services/pagosService.js'
import personasService from '@/services/personasService.js'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'

const vistaActiva = ref('registro')
const cambiarVista = (vista) => (vistaActiva.value = vista)

// Datos y estados
const pagos = ref([])
const cargandoPagos = ref(false)
const alerta = ref({ mensaje: '', tipo: '' })
const filtroBusqueda = ref('')
const terminoBuscado = ref('')
const showModal = ref(false)
const showModalAnular = ref(false)
const pagoSeleccionado = ref(null)

// Cargar pagos desde la API
onMounted(async () => {
  await cargarPagos()
})

async function cargarPagos() {
  try {
    cargandoPagos.value = true
    pagos.value = await pagosService.obtenerPagos()
  } catch (error) {
    console.error('Error al cargar pagos:', error)
    mostrarAlerta('Error al cargar pagos: ' + error.message, 'error')
  } finally {
    cargandoPagos.value = false
  }
}

const buscar = () => { terminoBuscado.value = filtroBusqueda.value }
const limpiarBusqueda = () => { filtroBusqueda.value = ''; terminoBuscado.value = '' }

const pagosFiltrados = computed(() => {
  if (!terminoBuscado.value) return pagos.value
  const q = terminoBuscado.value.toLowerCase()
  return pagos.value.filter(p =>
    p.nombre?.toLowerCase().includes(q) || p.rut?.toLowerCase().includes(q)
  )
})

// Modal
const abrirModal = (p) => { pagoSeleccionado.value = { ...p }; showModal.value = true }
const cerrarModal = () => { showModal.value = false; pagoSeleccionado.value = null }
const abrirModalAnular = (p) => { pagoSeleccionado.value = p; showModalAnular.value = true }
const cerrarModalAnular = () => { showModalAnular.value = false; pagoSeleccionado.value = null }

// Guardar cambios
const guardarPago = async () => {
  try {
    // Aquí deberías implementar la actualización en el backend
    // Por ahora solo actualiza localmente
    const index = pagos.value.findIndex(p => p.id === pagoSeleccionado.value.id)
    if (index !== -1) {
      pagos.value[index] = { ...pagoSeleccionado.value }
    }
    mostrarAlerta('Pago actualizado correctamente', 'exito')
    cerrarModal()
  } catch (error) {
    console.error('Error al guardar pago:', error)
    mostrarAlerta('Error al guardar pago: ' + error.message, 'error')
  }
}

// Anular pago
const confirmarAnulacion = async () => {
  try {
    await pagosService.anularPago(pagoSeleccionado.value.id)
    mostrarAlerta('Pago anulado correctamente', 'exito')
    cerrarModalAnular()
    await cargarPagos() // Recargar lista
  } catch (error) {
    console.error('Error al anular pago:', error)
    mostrarAlerta('Error al anular pago: ' + error.message, 'error')
  }
}

// Alerta
function mostrarAlerta(mensaje, tipo) {
  alerta.value = { mensaje, tipo }
  setTimeout(() => (alerta.value = { mensaje: '', tipo: '' }), 3000)
}

// Formularios
const formIndividual = ref({
  nombre: '', rut: '', curso: '', valor_pagado: '', fecha_pago: '', grupo: '', file: null
})
const handleFileIndividual = (e) => (formIndividual.value.file = e.target.files[0])
const registrarPagoIndividual = async () => {
  try {
    // TODO: Implementar registro individual cuando el backend esté listo
    mostrarAlerta('Pago individual registrado (pendiente implementación backend)', 'exito')
    // Limpiar formulario
    formIndividual.value = {
      nombre: '', rut: '', curso: '', valor_pagado: '', fecha_pago: '', grupo: '', file: null
    }
  } catch (error) {
    console.error('Error al registrar pago:', error)
    mostrarAlerta('Error al registrar pago: ' + error.message, 'error')
  }
}

const formMasivo = ref({ grupo: '', curso: '', file: null })
const participantesCargados = ref([])
const participantesSeleccionados = ref([])
const cargandoUsuarios = ref(false)

const handleFileMasivo = (e) => (formMasivo.value.file = e.target.files[0])

const cargarParticipantesParaMasivo = async () => {
  try {
    cargandoUsuarios.value = true
    const personas = await personasService.listarBasic()
    // Filtrar por grupo y/o curso si es necesario
    participantesCargados.value = personas.map(p => ({
      id: p.id,
      nombre: p.nombre,
      rut: p.rut || 'Sin RUT',
      email: p.email || 'Sin email'
    }))
    mostrarAlerta(`${participantesCargados.value.length} participantes cargados`, 'exito')
  } catch (error) {
    console.error('Error al cargar participantes:', error)
    mostrarAlerta('Error al cargar participantes: ' + error.message, 'error')
  } finally {
    cargandoUsuarios.value = false
  }
}

const registrarPagoMasivo = async () => {
  try {
    // TODO: Implementar registro masivo cuando el backend esté listo
    mostrarAlerta(`Pago masivo registrado para ${participantesSeleccionados.value.length} usuarios (pendiente implementación backend)`, 'exito')
    // Limpiar selección
    participantesSeleccionados.value = []
    participantesCargados.value = []
    formMasivo.value = { grupo: '', curso: '', file: null }
  } catch (error) {
    console.error('Error al registrar pago masivo:', error)
    mostrarAlerta('Error al registrar pago masivo: ' + error.message, 'error')
  }
}
</script>

<style scoped>
/* (Se mantiene tu mismo style, sin cambios visuales) */

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
  margin-bottom: -2px;
}
.navegacion-vistas button.active {
  color: var(--color-primario, #005A9C);
  border-bottom-color: var(--color-primario, #005A9C);
}
.navegacion-vistas button:hover:not(.active) {
  background-color: #f4f4f4;
}

/* Estilos para la tabla de pagos */
.tabla-pagos {
  width: 100%;
  overflow-x: auto;
  margin-top: 1rem;
}

.tabla-pagos table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.tabla-pagos thead {
  background: var(--color-primary, #1e40af);
  color: white;
}

.tabla-pagos th,
.tabla-pagos td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.tabla-pagos th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
}

.tabla-pagos tbody tr:hover {
  background-color: #f9fafb;
}

.btn-small {
  padding: 6px 12px;
  font-size: 0.875rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  margin-right: 8px;
  transition: all 0.2s;
}

.btn-editar {
  background: var(--color-warning, #f59e0b);
  color: white;
}

.btn-editar:hover {
  background: #d97706;
}

.btn-anular {
  background: var(--color-danger, #dc2626);
  color: white;
}

.btn-anular:hover {
  background: #b91c1c;
}

/* Estilos para modales */
.modal-editar-pago,
.modal-confirmar {
  padding: 24px;
  max-width: 500px;
}

.modal-editar-pago h3,
.modal-confirmar h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--color-primary, #1e40af);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-danger {
  background: var(--color-danger, #dc2626);
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

/* (resto de tus estilos se mantienen igual) */
</style>