<template>
  <div class="pagos-view">
    <h2>💰 Gestión de Pagos</h2>
    <p>Filtre, registre y administre los pagos del Sistema Scouts Biobío</p>

    <!-- ==================== -->
    <!-- FILTRO INICIAL -->
    <!-- ==================== -->
    <section class="filtros">
      <BaseInput v-model="filtro.nombreRut" label="Buscar por Nombre o RUT" placeholder="Ej: Juan Pérez o 12.345.678-9" />
      <BaseSelect
        v-model="modoPago"
        label="Seleccione modo de pago"
        :options="['Individual', 'Masivo']"
      />
    </section>

    <!-- ==================== -->
    <!-- PAGO INDIVIDUAL -->
    <!-- ==================== -->
    <section v-if="modoPago === 'Individual'" class="pago-individual">
      <h3>Pago Individual</h3>
      <BaseInput v-model="nuevoPago.nombre" label="Nombre del Participante" />
      <BaseInput v-model="nuevoPago.rut" label="RUT" />
      <BaseSelect v-model="nuevoPago.curso" :options="cursosDisponibles" label="Curso" />
      <BaseSelect v-model="nuevoPago.alimentacion" :options="['Completa','Vegetariana','Sin restricción']" label="Tipo de Alimentación" />
      <BaseInput v-model="nuevoPago.valorPagado" label="Valor Pagado ($)" type="number" />
      
      <FileUploader @upload="handleFileUpload" />
      <BaseButton label="Registrar Pago Individual" color="verde" @click="registrarPagoIndividual" />
    </section>

    <!-- ==================== -->
    <!-- PAGO MASIVO -->
    <!-- ==================== -->
    <section v-if="modoPago === 'Masivo'" class="pago-masivo">
      <h3>Pago Masivo</h3>
      <div class="filtros-masivo">
        <BaseSelect v-model="filtrosMasivo.grupo" :options="gruposDisponibles" label="Grupo" />
        <BaseSelect v-model="filtrosMasivo.curso" :options="cursosDisponibles" label="Curso Activo" />
        <BaseInput v-model="filtrosMasivo.persona" label="Filtrar por persona (opcional)" />
      </div>

      <DataTable
        :columns="columnas"
        :rows="pagosFiltrados"
        @view="cargarPersona"
        @edit="editarPago"
        @delete="eliminarPago"
        @anular="anularPago"
        @refund="abrirModalDevolucion"
      />

      <FileUploader @upload="handleFileUploadMasivo" />
      <BaseButton label="Asociar Comprobante a Seleccionados" color="azul" />
    </section>

    <!-- ==================== -->
    <!-- MODAL: DEVOLUCIÓN DE DINERO -->
    <!-- ==================== -->
    <BaseModal v-if="mostrarModalDevolucion" title="Registrar Devolución de Dinero" @close="mostrarModalDevolucion = false">
      <form @submit.prevent="registrarDevolucion">
        <p><strong>Pago asociado:</strong> {{ pagoSeleccionado?.nombre }} ({{ pagoSeleccionado?.rut }})</p>
        <BaseInput v-model="datosDevolucion.monto" label="Monto devuelto ($)" type="number" />
        <BaseInput v-model="datosDevolucion.motivo" label="Motivo de la devolución" />
        <BaseButton type="submit" label="Registrar Devolución" color="verde" />
      </form>
    </BaseModal>

    <!-- ==================== -->
    <!-- EXPORTAR -->
    <!-- ==================== -->
    <div class="acciones-finales">
      <BaseButton label="📤 Exportar Lista de Pagos por Grupo" color="azul" @click="exportarPagosGrupo" />
    </div>

    <NotificationToast v-if="notificacion" :message="notificacion" @close="notificacion = ''" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Componentes
import BaseInput from '@/components/Reutilizables/InputBase.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import FileUploader from '@/components/Reutilizables/FileUploader.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'

// Servicio
import pagosService from '@/services/pagosService.js'

// Variables reactivas
// Mostrar la tabla por defecto: modo "Masivo"
const modoPago = ref('Masivo')
const filtro = ref({ nombreRut: '' })
const nuevoPago = ref({ nombre: '', rut: '', curso: '', alimentacion: '', valorPagado: 0, email: '', direccion: '', telefono: '' })
const filtrosMasivo = ref({ grupo: '', curso: '', persona: '' })
const notificacion = ref('')

// Modal de devolución
const mostrarModalDevolucion = ref(false)
const pagoSeleccionado = ref(null)
const datosDevolucion = ref({ monto: 0, motivo: '' })

// Datos simulados
const cursosDisponibles = ['Formación Dirigentes', 'Campamento Avanzado', 'Primeros Auxilios']
const gruposDisponibles = ['Grupo Ñuble', 'Grupo Hualpén', 'Grupo Talcahuano']

const pagos = ref([])

const columnas = [
  { key: 'id', label: 'ID', sortable: true },
  { key: 'nombre', label: 'Nombre', sortable: true },
  { key: 'rut', label: 'RUT', sortable: true },
  { key: 'email', label: 'Email' },
  { key: 'direccion', label: 'Dirección' },
  { key: 'telefono', label: 'Teléfono' }
]

onMounted(async () => {
  try {
    pagos.value = await pagosService.obtenerPagos()
  } catch (err) {
    console.error('Error cargando pagos:', err)
    notificacion.value = 'Error cargando datos del servidor.'
  }
})

// Filtrar pagos por nombre o RUT
const pagosFiltrados = computed(() => {
  const term = filtro.value.nombreRut.toLowerCase()
  return pagos.value.filter(p =>
    p.nombre.toLowerCase().includes(term) || p.rut.includes(term)
  )
})

// Funciones principales
function registrarPagoIndividual() {
  // preparar payload simplificado para create_persona en backend
  const parts = nuevoPago.value.nombre.trim().split(' ')
  const nombres = parts.slice(0, parts.length - 2).join(' ') || parts[0] || ''
  const apelpt = parts.length >= 2 ? parts[parts.length - 2] : ''
  const apelmat = parts.length >= 1 ? parts[parts.length - 1] : ''
  const rutParts = (nuevoPago.value.rut || '').split('-')
  const payload = {
    nombres,
    apelpt,
    apelmat,
    run: (rutParts[0] || '').replace(/\D/g, ''),
    dv: (rutParts[1] || '').replace(/\D/g, ''),
    mail: nuevoPago.value.email || '',
    direccion: nuevoPago.value.direccion || '',
    fono: nuevoPago.value.telefono || ''
  }

  pagosService.createPersona(payload).then(res => {
    notificacion.value = '✅ Persona creada correctamente.'
    // recargar lista
    return pagosService.obtenerPagos()
  }).then(list => {
    pagos.value = list
  }).catch(err => {
    console.error(err)
    notificacion.value = 'Error creando persona.'
  })
}

function editarPago(p) {
  alert(`Editar pago de ${p.nombre}`)
  // implementar edición si se requiere
}

function cargarPersona(p) {
  // prefilling form fields with persona data
  nuevoPago.value.nombre = p.nombre || ''
  nuevoPago.value.rut = p.rut || ''
  nuevoPago.value.email = p.email || ''
  nuevoPago.value.direccion = p.direccion || ''
  nuevoPago.value.telefono = p.telefono || ''
  modoPago.value = 'Individual'
}

function eliminarPago(p) {
  pagosService.eliminarPago(p.id).then(() => {
    pagos.value = pagos.value.filter(x => x.id !== p.id)
    notificacion.value = '🗑 Pago eliminado correctamente.'
  }).catch(err => {
    console.error(err)
    notificacion.value = 'Error eliminando pago.'
  })
}

function anularPago(p) {
  pagosService.anularPago(p.id).then(() => {
    notificacion.value = '⚠️ Pago anulado. Puede registrar devolución si aplica.'
  }).catch(err => {
    console.error(err)
    notificacion.value = 'Error al anular pago.'
  })
}

function abrirModalDevolucion(p) {
  pagoSeleccionado.value = p
  mostrarModalDevolucion.value = true
}

function registrarDevolucion() {
  pagosService.registrarDevolucion(pagoSeleccionado.value.id, datosDevolucion.value)
  pagosService.registrarAuditoria('devolucion', {
    ...pagoSeleccionado.value,
    devolucion: datosDevolucion.value
  })
  mostrarModalDevolucion.value = false
  notificacion.value = '💸 Devolución registrada correctamente.'
}

function handleFileUpload(file) {
  console.log('Archivo individual:', file.name)
}

function handleFileUploadMasivo(file) {
  console.log('Archivo masivo:', file.name)
}

function exportarPagosGrupo() {
  alert('Exportando lista de pagos del grupo...')
}
</script>

<style scoped>
.pagos-view {
  padding: 20px;
  background: #fff;
  color: #2c5aa0;
  border-radius: 10px;
  max-width: 1000px;
  margin: auto;
}

h2 {
  color: #2c5aa0;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.filtros, .pago-individual, .pago-masivo {
  margin-bottom: 22px;
  padding: 14px;
  border: 1px solid #d8e3f7;
  border-radius: 8px;
  background: #f9fbff;
}

.filtros-masivo {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.acciones-finales {
  text-align: right;
  margin-top: 20px;
}
</style>
