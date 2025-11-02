<!-- src/views/PagosView.vue -->
<template>
  <div class="pago-view compact">
    <!-- Navegación / Logo -->
    <div class="navegacion-vistas">
      <div class="logo-wrap" v-if="logoUrl">
        <img :src="logoUrl" alt="Logo" class="header-logo" />
      </div>

      <button @click="cambiarVista('registro')" :class="{ active: vistaActiva === 'registro' }">
        <AppIcons name="clipboard" :size="20" />
        <span>Registro de Pago</span>
      </button>

      <button @click="cambiarVista('historico')" :class="{ active: vistaActiva === 'historico' }">
        <AppIcons name="chart-bar" :size="20" />
        <span>Histórico</span>
      </button>
    </div>

    <!-- ================== REGISTRO ================== -->
    <div v-if="vistaActiva === 'registro'" class="vista-registrar">
      <div class="card-registro">
        <div class="card-header">
          <h3><AppIcons name="clipboard" :size="24" /> Registro de Pago</h3>
          <p>El método de pago permitido es únicamente <strong>Transferencia bancaria</strong>.</p>
        </div>

        <!-- Selector Individual / Masivo -->
        <div class="tipo-registro-selector">
          <button type="button" @click="tipoRegistro = 'individual'" :class="['tipo-btn', { active: tipoRegistro === 'individual' }]">
            <AppIcons name="user" :size="20" />
            <span>Individual</span>
          </button>
          <button type="button" @click="tipoRegistro = 'masivo'" :class="['tipo-btn', { active: tipoRegistro === 'masivo' }]">
            <AppIcons name="users" :size="20" />
            <span>Masivo</span>
          </button>
        </div>

        <!-- --------- FORMULARIO INDIVIDUAL --------- -->
        <form v-if="tipoRegistro === 'individual'" @submit.prevent="registrarPagoIndividual" class="form-registro-individual">
          <!-- Buscar persona -->
          <div class="search-section">
            <div class="form-group search-group">
              <label>Buscar Participante (Nombre o RUT) *</label>
              <div class="search-input-wrapper">
                <input
                  v-model="busquedaPersona"
                  type="text"
                  placeholder="Ej: 12.345.678-9 o Juan Pérez"
                  @input="buscarPersona"
                  class="search-input"
                />
                <span class="search-icon"><AppIcons name="search" :size="18" /></span>
              </div>
            </div>

            <!-- Resultados -->
            <div v-if="resultadosBusqueda.length > 0" class="resultados-busqueda">
              <div
                v-for="persona in resultadosBusqueda"
                :key="persona.id"
                @click="seleccionarPersona(persona)"
                class="resultado-item"
              >
                <div class="resultado-info">
                  <strong>{{ persona.nombre }}</strong>
                  <span class="rut">{{ persona.rut }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="busquedaPersona && !buscando" class="no-resultados">
              No se encontraron personas con ese criterio
            </div>
          </div>

          <!-- Datos persona (solo lectura) -->
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre Completo</label>
              <input v-model="formIndividual.nombre" type="text" readonly class="readonly-input" />
            </div>
            <div class="form-group">
              <label>RUT</label>
              <input v-model="formIndividual.rut" type="text" readonly class="readonly-input" />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="formIndividual.email" type="email" readonly class="readonly-input" />
            </div>
            <div class="form-group">
              <label>Teléfono</label>
              <input v-model="formIndividual.telefono" type="text" readonly class="readonly-input" />
            </div>
            <div class="form-group">
              <label>Dirección</label>
              <input v-model="formIndividual.direccion" type="text" readonly class="readonly-input" />
            </div>
          </div>

          <!-- Pago -->
          <div class="form-divider"><h4>💵 Información del Pago</h4></div>
          <div class="form-grid">
            <div class="form-group">
              <label>Curso / Capacitación *</label>
              <select v-model="formIndividual.curso" required>
                <option value="">Seleccione un curso</option>
                <option v-for="curso in cursos" :key="curso.value" :value="curso.value">{{ curso.label }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Valor Pagado *</label>
              <div class="input-with-prefix">
                <span class="prefix">$</span>
                <input v-model.number="formIndividual.valor_pagado" type="number" min="0" required placeholder="25000" />
              </div>
            </div>
            <div class="form-group">
              <label>Fecha de Pago *</label>
              <input v-model="formIndividual.fecha_pago" type="date" required />
            </div>
            <div class="form-group">
              <label>Método de Pago</label>
              <div class="badge-metodo">Transferencia bancaria</div>
              <input type="hidden" v-model="formIndividual.metodo_pago" />
            </div>
            <div class="form-group full-width">
              <label>Observación</label>
              <input v-model="formIndividual.observacion" type="text" maxlength="100" placeholder="Comentario u observación (opcional)" />
            </div>
          </div>

          <div class="form-group full-width">
            <label>Comprobante de Transferencia (opcional)</label>
            <div class="file-upload-wrapper">
              <input id="file-individual" type="file" @change="handleFileIndividual" accept=".pdf,.jpg,.jpeg,.png" />
              <label for="file-individual" class="file-upload-label">
                <AppIcons name="file" :size="18" />
                <span>{{ formIndividual.file ? formIndividual.file.name : 'Seleccionar archivo' }}</span>
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primario" :disabled="!formIndividual.personaId">
              <AppIcons name="check" :size="16" /> Registrar Pago
            </button>
            <button type="button" @click="limpiarFormularioIndividual" class="btn btn-secundario">
              <AppIcons name="x" :size="16" /> Limpiar
            </button>
          </div>
        </form>

        <!-- --------- FORMULARIO MASIVO --------- -->
        <form v-if="tipoRegistro === 'masivo'" @submit.prevent="registrarPagoMasivo" class="form-registro-masivo">
          <div class="form-grid">
            <div class="form-group">
              <label>Grupo Scout *</label>
              <select v-model="formMasivo.grupo" required @change="filtrarParticipantesPorGrupo">
                <option value="">Seleccione un grupo</option>
                <option v-for="grupo in grupos" :key="grupo.value" :value="grupo.value">{{ grupo.label }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Curso / Capacitación *</label>
              <select v-model="formMasivo.curso" required>
                <option value="">Seleccione un curso</option>
                <option v-for="curso in cursos" :key="curso.value" :value="curso.value">{{ curso.label }}</option>
              </select>
            </div>
          </div>

          <button
            type="button"
            @click="cargarParticipantesParaMasivo"
            class="btn btn-info"
            :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoUsuarios"
          >
            <span v-if="cargandoUsuarios" class="spinner"></span>
            <AppIcons v-else name="users" :size="16" />
            {{ cargandoUsuarios ? 'Cargando...' : 'Cargar Participantes' }}
          </button>

          <div v-if="participantesCargados.length > 0" class="participantes-section">
            <div class="participantes-header">
              <h4>Participantes Disponibles ({{ participantesCargados.length }})</h4>
              <div class="seleccion-acciones">
                <button type="button" @click="seleccionarTodos" class="btn-link">Seleccionar todos</button>
                <button type="button" @click="deseleccionarTodos" class="btn-link">Deseleccionar todos</button>
              </div>
            </div>

            <div class="participantes-lista">
              <div v-for="user in participantesCargados" :key="user.id" class="participante-item">
                <input
                  type="checkbox"
                  :id="'user-' + user.id"
                  :value="user"
                  v-model="participantesSeleccionados"
                  class="checkbox-styled"
                />
                <label :for="'user-' + user.id" class="participante-label">
                  <div class="participante-info">
                    <strong>{{ user.nombre }}</strong>
                    <span class="rut">{{ user.rut }}</span>
                  </div>
                  <span class="email">{{ user.email }}</span>
                </label>
              </div>
            </div>
          </div>

          <div class="form-divider" v-if="participantesSeleccionados.length > 0"><h4>💵 Pago Masivo</h4></div>

          <div class="form-grid" v-if="participantesSeleccionados.length > 0">
            <div class="form-group">
              <label>Valor por Persona *</label>
              <div class="input-with-prefix">
                <span class="prefix">$</span>
                <input v-model.number="formMasivo.valor_pagado" type="number" min="0" required placeholder="25000" />
              </div>
            </div>
            <div class="form-group">
              <label>Fecha de Pago *</label>
              <input v-model="formMasivo.fecha_pago" type="date" required />
            </div>
            <div class="form-group">
              <label>Método de Pago</label>
              <div class="badge-metodo">Transferencia bancaria</div>
              <input type="hidden" v-model="formMasivo.metodo_pago" />
            </div>
            <div class="form-group full-width">
              <label>Observación (aplica a todos)</label>
              <input v-model="formMasivo.observacion" type="text" maxlength="100" placeholder="Comentario u observación (opcional)" />
            </div>
          </div>

          <div class="form-group full-width" v-if="participantesSeleccionados.length > 0">
            <label>Comprobante Grupal *</label>
            <div class="file-upload-wrapper">
              <input id="file-masivo" type="file" @change="handleFileMasivo" accept=".pdf,.jpg,.jpeg,.png" required />
              <label for="file-masivo" class="file-upload-label">
                <AppIcons name="file" :size="18" />
                <span>{{ formMasivo.file ? formMasivo.file.name : 'Seleccionar archivo' }}</span>
              </label>
            </div>
          </div>

          <div class="resumen-masivo" v-if="participantesSeleccionados.length > 0 && formMasivo.valor_pagado">
            <div class="resumen-item">
              <span>Participantes seleccionados:</span>
              <strong>{{ participantesSeleccionados.length }}</strong>
            </div>
            <div class="resumen-item">
              <span>Valor por persona:</span>
              <strong>${{ formMasivo.valor_pagado.toLocaleString('es-CL') }}</strong>
            </div>
            <div class="resumen-item total">
              <span>Total a registrar:</span>
              <strong>${{ (participantesSeleccionados.length * formMasivo.valor_pagado).toLocaleString('es-CL') }}</strong>
            </div>
          </div>

          <div class="form-actions" v-if="participantesSeleccionados.length > 0">
            <button type="submit" class="btn btn-primario" :disabled="!formMasivo.file || !formMasivo.valor_pagado">
              <AppIcons name="check" :size="16" />
              Registrar Pago Masivo ({{ participantesSeleccionados.length }})
            </button>
            <button type="button" @click="limpiarFormularioMasivo" class="btn btn-secundario">
              <AppIcons name="x" :size="16" />
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ================== HISTÓRICO ================== -->
    <div v-if="vistaActiva === 'historico'" class="vista-buscar">
      <div class="card-registro">
        <div class="card-header">
          <h3><AppIcons name="chart-bar" :size="24" /> Histórico de Pagos</h3>
          <p>Consulta y administra todos los pagos</p>
        </div>

        <div class="filtros-avanzados">
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre o RUT</label>
              <input
                type="text"
                v-model="filtroPersona"
                placeholder="Ej: María o 11.223.344-5"
                class="search-input"
                @keyup.enter="aplicarFiltros"
              />
            </div>
          </div>

          <div class="filtros-acciones">
            <button @click="aplicarFiltros" class="btn btn-primario">
              <AppIcons name="search" :size="16" />
              Buscar
            </button>
            <button @click="limpiarFiltros" class="btn btn-secundario">
              <AppIcons name="refresh" :size="16" />
              Limpiar
            </button>
            <button @click="exportarExcel" class="btn btn-success">
              <AppIcons name="download" :size="16" />
              Exportar Excel
            </button>
          </div>
        </div>

        <div class="tabla-pagos">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>RUT</th>
                <th>Curso</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cargandoPagos">
                <td colspan="6" class="loading-cell">
                  <span class="spinner"></span> Cargando pagos...
                </td>
              </tr>
              <tr v-else-if="pagosFiltrados.length === 0">
                <td colspan="6" class="no-results">No se encontraron pagos con los filtros aplicados</td>
              </tr>
              <tr v-else v-for="pago in paginatedPagos" :key="pago.id">
                <td><strong>{{ pago.nombre }}</strong></td>
                <td>{{ pago.rut }}</td>
                <td>{{ pago.curso }}</td>
                <td class="monto">${{ pago.monto.toLocaleString('es-CL') }}</td>
                <td>{{ formatearFecha(pago.fecha) }}</td>
                <td class="actions-cell">
                  <button @click="verHistorial(pago.perId)" class="btn-icon btn-ver" title="Historial">
                    <AppIcons name="history" :size="18" />
                  </button>
                  <button @click="abrirModal(pago)" class="btn-icon btn-editar" title="Editar">
                    <AppIcons name="edit" :size="18" />
                  </button>
                  <button @click="abrirModalAnular(pago)" class="btn-icon btn-anular" title="Anular">
                    <AppIcons name="trash" :size="18" />
                  </button>
                  <button @click="abrirModalTransferir(pago)" class="btn-icon" title="Transferir">
                    <AppIcons name="repeat" :size="18" />
                  </button>
                  <button v-if="pago.comprobante" @click="descargarComprobante(pago)" class="btn-icon" title="Descargar comprobante">
                    <AppIcons name="paperclip" :size="18" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination" v-if="totalPages > 1">
          <button @click="cambiarPagina(paginaActual - 1)" :disabled="paginaActual === 1" class="btn-pag">← Anterior</button>
          <div class="pagination-info">
            Página {{ paginaActual }} de {{ totalPages }}
            <span class="separator">|</span>
            Mostrando
            {{ (paginaActual - 1) * itemsPorPagina + 1 }} -
            {{ Math.min(paginaActual * itemsPorPagina, pagosFiltrados.length) }}
            de {{ pagosFiltrados.length }}
          </div>
          <button @click="cambiarPagina(paginaActual + 1)" :disabled="paginaActual === totalPages" class="btn-pag">
            Siguiente →
          </button>
        </div>
      </div>
    </div>

    <!-- ================== MODALES ================== -->
    <!-- Editar Pago -->
    <BaseModal v-model="showModal" @close="cerrarModal">
      <template #title>Editar Pago</template>

      <div class="modal-editar-pago">
        <div class="form-group"><label>Nombre</label><input v-model="pagoSeleccionado.nombre" type="text" readonly /></div>
        <div class="form-group"><label>RUT</label><input v-model="pagoSeleccionado.rut" type="text" readonly /></div>
        <div class="form-group"><label>Email</label><input v-model="pagoSeleccionado.email" type="email" /></div>
        <div class="form-group"><label>Teléfono</label><input v-model="pagoSeleccionado.telefono" type="text" /></div>
        <div class="form-group"><label>Dirección</label><input v-model="pagoSeleccionado.direccion" type="text" /></div>
      </div>

      <template #footer>
        <button @click="guardarPago" class="btn btn-primario">Guardar</button>
        <button @click="cerrarModal" class="btn btn-secundario">Cancelar</button>
      </template>
    </BaseModal>

    <!-- Anular pago -->
    <BaseModal v-model="showModalAnular" @close="cerrarModalAnular">
      <template #title>Anular pago</template>

      <div class="modal-confirmar">
        <p>¿Anulación total o parcial del pago de <strong>{{ pagoSeleccionado?.nombre }}</strong>?</p>

        <div class="form-group">
          <label>Tipo de anulación</label>
          <select v-model="anulacionTipo">
            <option value="total">Total</option>
            <option value="parcial">Parcial</option>
          </select>
        </div>

        <div class="form-group" v-if="anulacionTipo==='parcial'">
          <label>Monto a devolver</label>
          <div class="input-with-prefix">
            <span class="prefix">$</span>
            <input type="number" v-model.number="anulacionMonto" min="0" :max="pagoSeleccionado?.monto || 0" />
          </div>
          <small>Máximo: ${{ (pagoSeleccionado?.monto||0).toLocaleString('es-CL') }}</small>
        </div>

        <div class="form-group">
          <label>Motivo / Observación</label>
          <input v-model="anulacionObs" maxlength="100" placeholder="Ej: desistimiento, error, etc." />
        </div>
      </div>

      <template #footer>
        <button @click="confirmarAnulacionConDetalle" class="btn btn-danger">Confirmar</button>
        <button @click="cerrarModalAnular" class="btn btn-secundario">Cancelar</button>
      </template>
    </BaseModal>

    <!-- Transferir pago -->
    <BaseModal v-model="showModalTransferir" @close="cerrarModalTransferir">
      <template #title>Transferir pago a otra persona</template>

      <div class="modal-editar-pago">
        <div class="form-group">
          <label>Buscar nuevo beneficiario (Nombre o RUT)</label>
          <input v-model="busquedaTransfer" type="text" @input="buscarTransfer" placeholder="Ej: 12.345.678-9 o Juan..." />
          <div v-if="resultadosTransfer.length" class="resultados-busqueda">
            <div v-for="p in resultadosTransfer" :key="p.id" class="resultado-item" @click="seleccionarTransfer(p)">
              <div class="resultado-info">
                <strong>{{ p.nombre }}</strong> <span class="rut">{{ p.rut }}</span>
              </div>
            </div>
          </div>
          <div v-else-if="busquedaTransfer && !resultadosTransfer.length" class="no-resultados">Sin coincidencias</div>
        </div>
      </div>

      <template #footer>
        <button :disabled="!nuevoBeneficiario" @click="confirmarTransferencia" class="btn btn-primario">Confirmar</button>
        <button @click="cerrarModalTransferir" class="btn btn-secundario">Cancelar</button>
      </template>
    </BaseModal>

    <!-- Historial por persona -->
    <BaseModal v-model="showHistorial" @close="showHistorial = false">
      <template #title>Historial de {{ historialPersona?.nombre }}</template>

      <div class="modal-editar-pago">
        <div v-if="!historialEventos.length" class="no-resultados">Sin eventos</div>
        <ul v-else class="historial-lista">
          <li v-for="ev in historialEventos" :key="ev.id" class="historial-item">
            <span class="historial-fecha">{{ formatearFecha(ev.fecha) }}</span>
            <span class="historial-tipo">{{ ev.tipo }}</span>
            <span class="historial-detalle">{{ ev.detalle }}</span>
          </li>
        </ul>
      </div>

      <template #footer>
        <button @click="showHistorial = false" class="btn btn-secundario">Cerrar</button>
      </template>
    </BaseModal>

    <!-- Toast -->
    <NotificationToast
      v-if="alerta.mensaje"
      :message="alerta.mensaje"
      :type="alerta.tipo"
      @close="alerta.mensaje = ''"
    />
  </div>
</template>

<script setup>
/**
 * PagosView.vue
 * - Búsqueda por Nombre/RUT (registro e histórico)
 * - Fecha de pago por defecto = día de ingreso
 * - Método de pago fijo: Transferencia bancaria
 * - Observación opcional
 * - Masivo: permite no seleccionar a nadie (muestra alerta)
 * - Historial por persona (modal)
 * - Anulación total/parcial (pide monto y registra egreso simulado)
 * - Transferencia de pago a otro beneficiario (simulada)
 */
import { ref, computed, onMounted } from 'vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

const props = defineProps({ logoUrl: { type: String, default: '' } })

// --------- Helpers UI ---------
function todayISO () {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}
function formatearFecha (fecha) {
  if (!fecha) return '-'
  const d = new Date(fecha)
  return d.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric' })
}
function mostrarAlerta (mensaje, tipo = 'info') {
  alerta.value = { mensaje, tipo }
  setTimeout(() => (alerta.value = { mensaje: '', tipo: '' }), 3000)
}

// --------- Estado principal ---------
const vistaActiva = ref('registro')
const tipoRegistro = ref('individual')

const personas = ref([])
const cursos = ref([])
const grupos = ref([])
const pagos = ref([])
const cargandoPagos = ref(false)
const alerta = ref({ mensaje: '', tipo: '' })

// Buscar/seleccionar persona (registro individual)
const busquedaPersona = ref('')
const resultadosBusqueda = ref([])
const buscando = ref(false)

// Formularios
const formIndividual = ref({
  personaId: null,
  nombre: '',
  rut: '',
  email: '',
  telefono: '',
  direccion: '',
  curso: '',
  valor_pagado: '',
  fecha_pago: todayISO(),
  metodo_pago: 'Transferencia',
  observacion: '',
  file: null
})
const formMasivo = ref({
  grupo: '',
  curso: '',
  valor_pagado: '',
  fecha_pago: todayISO(),
  metodo_pago: 'Transferencia',
  observacion: '',
  file: null
})
const participantesCargados = ref([])
const participantesSeleccionados = ref([])
const cargandoUsuarios = ref(false)

// Filtros histórico
const filtroPersona = ref('')
const paginaActual = ref(1)
const itemsPorPagina = ref(10)

// Modales
const showModal = ref(false)
const showModalAnular = ref(false)
const showModalTransferir = ref(false)
const showHistorial = ref(false)
const pagoSeleccionado = ref(null)

// Historial persona
const historialPersona = ref(null)
const historialEventos = ref([])

// Anulación
const anulacionTipo = ref('total')
const anulacionMonto = ref(0)
const anulacionObs = ref('')

// Transferencia
const busquedaTransfer = ref('')
const resultadosTransfer = ref([])
const nuevoBeneficiario = ref(null)

// --------- Demo data (reemplazar por backend) ---------
const PERSONAS_FICTICIAS = [
  { id: 1, nombre: 'Juan Pérez González', rut: '12.345.678-9', email: 'juan.perez@scouts.cl', telefono: '+56 9 8765 4321', direccion: 'Av. O\'Higgins 123, Concepción' },
  { id: 2, nombre: 'María González Silva', rut: '98.765.432-1', email: 'maria.gonzalez@scouts.cl', telefono: '+56 9 1234 5678', direccion: 'Calle Libertad 456, Chillán' },
  { id: 3, nombre: 'Pedro Silva Rojas', rut: '11.223.344-5', email: 'pedro.silva@scouts.cl', telefono: '+56 9 5555 6666', direccion: 'Pasaje Los Pinos 789, Los Ángeles' }
]
const CURSOS_FICTICIOS = [
  { value: 1, label: 'Formación de Dirigentes Básico - FDB 2025' },
  { value: 2, label: 'Curso de Especialidad en Montañismo - CEM 2025' },
  { value: 3, label: 'Formación de Dirigentes Avanzado - FDA 2025' }
]
const GRUPOS_FICTICIOS = [
  { value: 1, label: 'Grupo Scout Biobío' },
  { value: 2, label: 'Grupo Scout Ñuble' }
]
const PAGOS_FICTICIOS = [
  { id: 1, perId: 1, nombre: 'Juan Pérez González', rut: '12.345.678-9', curso: 'Formación de Dirigentes Básico', monto: 25000, fecha: '2025-10-20', comprobante: null, email: 'juan.perez@scouts.cl', telefono: '+56 9 8765 4321', direccion: 'Av. O\'Higgins 123' },
  { id: 2, perId: 2, nombre: 'María González Silva', rut: '98.765.432-1', curso: 'Curso de Especialidad en Montañismo', monto: 30000, fecha: '2025-10-18', comprobante: 'comprobante123.pdf', email: 'maria.gonzalez@scouts.cl', telefono: '+56 9 1234 5678', direccion: 'Calle Libertad 456' },
  { id: 3, perId: 3, nombre: 'Pedro Silva Rojas', rut: '11.223.344-5', curso: 'Formación de Dirigentes Avanzado', monto: 35000, fecha: '2025-10-15', comprobante: 'comprobante456.pdf', email: 'pedro.silva@scouts.cl', telefono: '+56 9 5555 6666', direccion: 'Pasaje Los Pinos 789' }
]

// --------- Ciclo de vida ---------
onMounted(() => {
  personas.value = PERSONAS_FICTICIAS
  cursos.value = CURSOS_FICTICIOS
  grupos.value = GRUPOS_FICTICIOS
  pagos.value = PAGOS_FICTICIOS
})

// --------- Navegación ---------
const cambiarVista = (vista) => {
  vistaActiva.value = vista
  if (vista === 'historico') cargarPagos()
  if (vista === 'registro') {
    // asegurar fecha por defecto del día de ingreso
    if (!formIndividual.value.fecha_pago) formIndividual.value.fecha_pago = todayISO()
    if (!formMasivo.value.fecha_pago) formMasivo.value.fecha_pago = todayISO()
  }
}

// --------- Búsqueda persona (registro individual) ---------
const buscarPersona = () => {
  if (!busquedaPersona.value || busquedaPersona.value.length < 2) {
    resultadosBusqueda.value = []
    return
  }
  const q = busquedaPersona.value.toLowerCase()
  resultadosBusqueda.value = personas.value
    .filter(p => p.nombre.toLowerCase().includes(q) || p.rut.toLowerCase().includes(q))
    .slice(0, 5)
}
const seleccionarPersona = (persona) => {
  formIndividual.value = {
    ...formIndividual.value,
    personaId: persona.id,
    nombre: persona.nombre,
    rut: persona.rut,
    email: persona.email,
    telefono: persona.telefono,
    direccion: persona.direccion
  }
  resultadosBusqueda.value = []
  busquedaPersona.value = persona.nombre
}
const limpiarFormularioIndividual = () => {
  formIndividual.value = {
    personaId: null,
    nombre: '',
    rut: '',
    email: '',
    telefono: '',
    direccion: '',
    curso: '',
    valor_pagado: '',
    fecha_pago: todayISO(),
    metodo_pago: 'Transferencia',
    observacion: '',
    file: null
  }
  busquedaPersona.value = ''
  resultadosBusqueda.value = []
}

// --------- Registro Individual ---------
const handleFileIndividual = (e) => { formIndividual.value.file = e.target.files[0] }
const registrarPagoIndividual = async () => {
  try {
    if (!formIndividual.value.personaId) {
      mostrarAlerta('Debes buscar y seleccionar una persona.', 'error')
      return
    }
    if (!formIndividual.value.fecha_pago) formIndividual.value.fecha_pago = todayISO()
    // TODO: enviar a backend
    mostrarAlerta('Pago individual registrado correctamente', 'exito')
    limpiarFormularioIndividual()
  } catch (error) {
    mostrarAlerta('Error al registrar pago: ' + error.message, 'error')
  }
}

// --------- Registro Masivo ---------
const handleFileMasivo = (e) => { formMasivo.value.file = e.target.files[0] }
const filtrarParticipantesPorGrupo = () => {
  participantesCargados.value = []
  participantesSeleccionados.value = []
}
const cargarParticipantesParaMasivo = async () => {
  try {
    cargandoUsuarios.value = true
    // Demo: trae todos; en backend filtra por grupo real
    participantesCargados.value = [...personas.value]
    mostrarAlerta(`${participantesCargados.value.length} participantes cargados`, 'exito')
  } catch (error) {
    mostrarAlerta('Error al cargar participantes: ' + error.message, 'error')
  } finally {
    cargandoUsuarios.value = false
  }
}
const seleccionarTodos = () => { participantesSeleccionados.value = [...participantesCargados.value] }
const deseleccionarTodos = () => {
  participantesSeleccionados.value = []
  mostrarAlerta('No hay participantes seleccionados. Debes elegir al menos uno para registrar.', 'info')
}
const limpiarFormularioMasivo = () => {
  formMasivo.value = {
    grupo: '',
    curso: '',
    valor_pagado: '',
    fecha_pago: todayISO(),
    metodo_pago: 'Transferencia',
    observacion: '',
    file: null
  }
  participantesCargados.value = []
  participantesSeleccionados.value = []
}
const registrarPagoMasivo = async () => {
  try {
    if (participantesSeleccionados.value.length === 0) {
      mostrarAlerta('No puedes registrar un pago masivo sin participantes.', 'error')
      return
    }
    if (!formMasivo.value.fecha_pago) formMasivo.value.fecha_pago = todayISO()
    // TODO: enviar a backend
    mostrarAlerta(`Pago masivo registrado para ${participantesSeleccionados.value.length} usuarios`, 'exito')
    limpiarFormularioMasivo()
  } catch (error) {
    mostrarAlerta('Error al registrar pago masivo: ' + error.message, 'error')
  }
}

// --------- Histórico ---------
async function cargarPagos () {
  try {
    cargandoPagos.value = true
    // TODO: pagos.value = await api
    pagos.value = PAGOS_FICTICIOS
  } finally {
    cargandoPagos.value = false
  }
}
const aplicarFiltros = () => { paginaActual.value = 1 }
const limpiarFiltros = () => { filtroPersona.value = ''; paginaActual.value = 1 }
const pagosFiltrados = computed(() => {
  const q = filtroPersona.value.trim().toLowerCase()
  return q
    ? pagos.value.filter(p => p.nombre?.toLowerCase().includes(q) || p.rut?.toLowerCase().includes(q))
    : [...pagos.value]
})
const totalPages = computed(() => Math.ceil(pagosFiltrados.value.length / itemsPorPagina.value))
const paginatedPagos = computed(() => {
  const start = (paginaActual.value - 1) * itemsPorPagina.value
  return pagosFiltrados.value.slice(start, start + itemsPorPagina.value)
})
const cambiarPagina = (pagina) => {
  if (pagina >= 1 && pagina <= totalPages.value) paginaActual.value = pagina
}

// --------- Editar ---------
const abrirModal = (p) => { pagoSeleccionado.value = { ...p }; showModal.value = true }
const cerrarModal = () => { showModal.value = false; pagoSeleccionado.value = null }
const guardarPago = async () => {
  try {
    const idx = pagos.value.findIndex(p => p.id === pagoSeleccionado.value.id)
    if (idx !== -1) pagos.value[idx] = { ...pagoSeleccionado.value }
    // TODO: update backend
    mostrarAlerta('Pago actualizado correctamente', 'exito')
    cerrarModal()
  } catch (e) {
    mostrarAlerta('Error al guardar pago: ' + e.message, 'error')
  }
}

// --------- Historial por persona ---------
const verHistorial = async (perId) => {
  try {
    historialPersona.value = personas.value.find(p => p.id === perId)
    // TODO: traer del backend
    historialEventos.value = [
      { id: 1, tipo: 'Pago', detalle: 'Curso FDB 2025 · $25.000', fecha: '2025-10-20' },
      { id: 2, tipo: 'Transferencia', detalle: 'Pago transferido a María González', fecha: '2025-10-22' },
      { id: 3, tipo: 'Devolución parcial', detalle: '$10.000', fecha: '2025-10-25' }
    ]
    showHistorial.value = true
  } catch {
    mostrarAlerta('No fue posible cargar el historial', 'error')
  }
}

// --------- Anulación (egreso / parcial-total) ---------
const abrirModalAnular = (p) => {
  pagoSeleccionado.value = p
  anulacionTipo.value = 'total'
  anulacionMonto.value = 0
  anulacionObs.value = ''
  showModalAnular.value = true
}
const cerrarModalAnular = () => { showModalAnular.value = false; pagoSeleccionado.value = null }
const confirmarAnulacionConDetalle = async () => {
  try {
    const total = pagoSeleccionado.value.monto
    const monto = anulacionTipo.value === 'total' ? total : (anulacionMonto.value || 0)
    if (monto <= 0 || monto > total) {
      mostrarAlerta('Monto inválido para devolución', 'error')
      return
    }
    // TODO: backend:
    // 1) generar egreso (devolución)
    // 2) crear registro de anulación por -monto (si parcial, solo el porcentaje)
    mostrarAlerta(`Anulación ${anulacionTipo.value} registrada ($${monto.toLocaleString('es-CL')})`, 'exito')
    cerrarModalAnular()
  } catch (e) {
    mostrarAlerta('Error al anular: ' + e.message, 'error')
  }
}

// --------- Transferir pago (cambiar beneficiario) ---------
const abrirModalTransferir = (pago) => { pagoSeleccionado.value = pago; showModalTransferir.value = true }
const cerrarModalTransferir = () => { showModalTransferir.value = false; busquedaTransfer.value = ''; resultadosTransfer.value = []; nuevoBeneficiario.value = null }
const buscarTransfer = () => {
  const q = busquedaTransfer.value.trim().toLowerCase()
  resultadosTransfer.value = q.length < 2
    ? []
    : personas.value.filter(p => p.nombre.toLowerCase().includes(q) || p.rut.toLowerCase().includes(q)).slice(0, 5)
}
const seleccionarTransfer = (p) => { nuevoBeneficiario.value = p; resultadosTransfer.value = []; busquedaTransfer.value = p.nombre }
const confirmarTransferencia = async () => {
  try {
    if (!nuevoBeneficiario.value) { mostrarAlerta('Selecciona el nuevo beneficiario.', 'error'); return }
    // TODO backend: cambiar beneficiario + registrar fecha de cambio
    mostrarAlerta(`Pago transferido a ${nuevoBeneficiario.value.nombre}`, 'exito')
    cerrarModalTransferir()
  } catch (e) {
    mostrarAlerta('Error al transferir: ' + e.message, 'error')
  }
}

// --------- Utilidades tabla ---------
const descargarComprobante = (pago) => {
  console.log('Descargar comprobante:', pago.comprobante)
  mostrarAlerta('Descarga de comprobante próximamente', 'info')
}
const exportarExcel = () => {
  console.log('Exportar a Excel')
  mostrarAlerta('Función de exportación próximamente', 'info')
}
</script>

<style scoped>
.pago-view { max-width: 1400px; margin: 0 auto; padding: 24px; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

/* compacta inputs (achica espacios de texto) */
.compact { max-width: 900px; }
.compact .form-group input,
.compact .form-group select,
.compact .search-input,
.compact .file-upload-label { padding: 8px 10px !important; font-size: 0.9rem !important; }
.compact .navegacion-vistas button, .compact .btn { padding: 8px 12px; font-size: 0.9rem; }
.compact .card-header { padding: 16px 20px; }
.compact .tipo-registro-selector { padding: 12px 16px; }
.compact .form-divider { margin: 20px 0 12px; padding-top: 12px; }
.compact .tabla-pagos th, .compact .tabla-pagos td { padding: 10px 8px; }

/* Header / Tabs */
.navegacion-vistas { display: flex; gap: 8px; border-bottom: 2px solid #e5e7eb; margin-bottom: 24px; background: white; border-radius: 8px 8px 0 0; overflow: hidden; align-items: center; }
.logo-wrap { padding-left: 12px; display: flex; align-items: center; }
.header-logo { height: 28px; width: auto; margin-right: 8px; }
.navegacion-vistas button { flex: 1; padding: 16px 24px; border: none; background: transparent; cursor: pointer; font-size: 1rem; font-weight: 500; color: #6b7280; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.3s ease; border-bottom: 3px solid transparent; position: relative; }
.navegacion-vistas button:hover:not(.active) { background: #f9fafb; color: var(--color-primary, #1e40af); }
.navegacion-vistas button.active { color: var(--color-primary, #1e40af); border-bottom-color: var(--color-primary, #1e40af); background: #eff6ff; font-weight: 600; }

/* Card */
.vista-registrar, .vista-buscar { display: flex; flex-direction: column; gap: 16px; }
.card-registro { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; transition: box-shadow 0.3s ease; width: min(100%, 980px); margin-inline: auto; }
.card-registro:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.card-header { background: linear-gradient(to right, #f9fafb, #ffffff); padding: 24px 32px; border-bottom: 2px solid #e5e7eb; }
.card-header h3 { margin: 0 0 8px 0; font-size: 1.5rem; font-weight: 600; color: #111827; display: flex; align-items: center; gap: 8px; }
.card-header p { margin: 0; color: #6b7280; font-size: 0.95rem; }

/* Selector tipo de registro */
.tipo-registro-selector { display: flex; gap: 12px; padding: 24px 32px; background: #f9fafb; border-bottom: 2px solid #e5e7eb; }
.tipo-btn { flex: 1; padding: 16px 24px; border: 2px solid #e5e7eb; border-radius: 8px; background: white; cursor: pointer; font-size: 1rem; font-weight: 500; color: #6b7280; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s ease; }
.tipo-btn:hover:not(.active) { background: #eff6ff; border-color: var(--color-primary, #1e40af); color: var(--color-primary, #1e40af); }
.tipo-btn.active { background: var(--color-primary, #1e40af); border-color: var(--color-primary, #1e40af); color: white; font-weight: 600; box-shadow: 0 4px 6px rgba(30,64,175,0.2); }

/* Formularios centrados y responsivos */
.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding: 16px 20px; max-width: 760px; margin-inline: auto; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-weight: 600; color: #374151; font-size: 0.9rem; }
.form-group input, .form-group select { padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 1rem; transition: all 0.2s; background: white; color: #111827; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: var(--color-primary, #1e40af); box-shadow: 0 0 0 3px rgba(30,64,175,0.1); }
.readonly-input { background: #f9fafb !important; cursor: not-allowed; color: #6b7280; }

/* Input con prefijo $ */
.input-with-prefix { display: flex; align-items: center; border: 2px solid #e5e7eb; border-radius: 8px; overflow: hidden; transition: all 0.2s ease; }
.input-with-prefix:focus-within { border-color: var(--color-primary, #1e40af); box-shadow: 0 0 0 3px rgba(30,64,175,0.1); }
.input-with-prefix .prefix { background: #f3f4f6; padding: 12px 16px; font-weight: 600; color: #6b7280; border-right: 2px solid #e5e7eb; }
.input-with-prefix input { flex: 1; border: none; padding: 12px 16px; font-size: 1rem; }
.input-with-prefix input:focus { outline: none; box-shadow: none; }

/* Búsqueda */
.search-section { margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #e5e7eb; }
.search-group { position: relative; max-width: 760px; margin-inline: auto; }
.search-input-wrapper { position: relative; }
.search-input { width: 100%; padding: 12px 44px 12px 12px !important; border: 2px solid #e5e7eb !important; border-radius: 12px !important; }
.search-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); font-size: 1.1rem; pointer-events: none; }
.search-icon svg { margin-right: 0; }
.resultados-busqueda { margin-top: 8px; border: 2px solid #e5e7eb; border-radius: 8px; background: white; max-height: 260px; overflow-y: auto; max-width: 760px; margin-inline: auto; }
.resultado-item { padding: 12px; cursor: pointer; border-bottom: 1px solid #f3f4f6; transition: all 0.2s ease; display: flex; justify-content: space-between; align-items: center; }
.resultado-item:last-child { border-bottom: none; }
.resultado-item:hover { background: #eff6ff; }
.resultado-info { display: flex; flex-direction: column; gap: 2px; }
.resultado-info strong { color: #111827; font-size: 0.95rem; }
.resultado-info .rut { color: #6b7280; font-size: 0.85rem; }
.no-resultados { padding: 14px; text-align: center; color: #9ca3af; font-style: italic; max-width: 760px; margin-inline: auto; }

/* Divider */
.form-divider { margin: 24px 0 14px; padding-top: 12px; border-top: 2px solid #e5e7eb; max-width: 760px; margin-inline: auto; }
.form-divider h4 { margin: 0; font-size: 1.1rem; font-weight: 600; color: #111827; display: flex; align-items: center; gap: 8px; }

/* File upload */
.file-upload-wrapper input[type="file"] { display: none; }
.file-upload-label { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border: 2px dashed #d1d5db; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; background: #f9fafb; color: #6b7280; font-weight: 500; max-width: 760px; margin-inline: auto; }
.file-upload-label:hover { border-color: var(--color-primary, #1e40af); background: #eff6ff; color: var(--color-primary, #1e40af); }

/* Participantes masivo */
.participantes-section { margin-top: 16px; padding: 14px; background: #f9fafb; border-radius: 8px; border: 2px solid #e5e7eb; max-width: 860px; margin-inline: auto; }
.participantes-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 2px solid #e5e7eb; }
.participantes-header h4 { margin: 0; font-size: 1rem; font-weight: 600; color: #111827; }
.seleccion-acciones { display: flex; gap: 8px; }
.btn-link { background: none; border: none; color: var(--color-primary, #1e40af); cursor: pointer; font-size: 0.9rem; text-decoration: underline; padding: 2px 4px; }
.btn-link:hover { color: #1e3a8a; }
.participantes-lista { max-height: 260px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; }
.participante-item { display: flex; align-items: center; gap: 10px; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e5e7eb; transition: all 0.2s ease; }
.participante-item:hover { border-color: var(--color-primary, #1e40af); background: #eff6ff; }
.checkbox-styled { width: 18px; height: 18px; cursor: pointer; }
.participante-label { flex: 1; cursor: pointer; display: flex; justify-content: space-between; align-items: center; margin: 0; }
.participante-info { display: flex; flex-direction: column; gap: 2px; }
.participante-info strong { color: #111827; font-size: 0.9rem; }
.participante-info .rut { color: #6b7280; font-size: 0.8rem; }
.participante-label .email { color: #6b7280; font-size: 0.8rem; }

/* Resumen masivo */
.resumen-masivo { margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 8px; border: 2px solid #93c5fd; max-width: 760px; margin-inline: auto; }
.resumen-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; color: #1e40af; }
.resumen-item span { font-size: 0.95rem; }
.resumen-item strong { font-size: 1rem; font-weight: 600; }
.resumen-item.total { margin-top: 10px; padding-top: 10px; border-top: 2px solid #93c5fd; font-size: 1.05rem; }
.resumen-item.total strong { font-size: 1.2rem; color: #1e3a8a; }

/* Botones */
.form-actions { display: flex; gap: 10px; margin-top: 16px; justify-content: center; }
.btn { padding: 12px 24px; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.btn-primario { background: var(--color-primary, #1e40af); color: white; }
.btn-primario:hover:not(:disabled) { background: #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.15); transform: translateY(-1px); }
.btn-secundario { background: #f3f4f6; color: #374151; }
.btn-secundario:hover { background: #e5e7eb; }
.btn-info { background: #0ea5e9; color: white; width: 100%; justify-content: center; margin-bottom: 12px; }
.btn-info:hover:not(:disabled) { background: #0284c7; }
.btn-success { background: #10b981; color: white; }
.btn-success:hover { background: #059669; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Tabla */
.filtros-avanzados { margin-bottom: 16px; }
.filtros-acciones { display: flex; gap: 10px; margin-top: 12px; justify-content: center; }
.tabla-pagos { overflow-x: auto; margin-top: 12px; border-radius: 8px; border: 1px solid #e5e7eb; }
.tabla-pagos table { width: 100%; border-collapse: collapse; background: white; table-layout: auto; min-width: 920px; }
.tabla-pagos thead { background: linear-gradient(to right, #1e40af, #1e3a8a); color: white; }
.tabla-pagos th { padding: 16px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
.tabla-pagos td { padding: 16px; border-bottom: 1px solid #f3f4f6; }
.tabla-pagos th, .tabla-pagos td { vertical-align: middle; overflow: hidden; text-overflow: ellipsis; }
.tabla-pagos th:nth-child(4), .tabla-pagos td:nth-child(4) { text-align: right; }
.tabla-pagos th:nth-child(5), .tabla-pagos td:nth-child(5) { white-space: nowrap; }
.tabla-pagos th:nth-child(6), .tabla-pagos td:nth-child(6) { width: 220px; white-space: nowrap; text-align: left; }
.tabla-pagos tbody tr { transition: all 0.2s ease; }
.tabla-pagos tbody tr:hover { background: #f9fafb; }
.tabla-pagos .monto { font-weight: 600; color: #059669; }

.actions-cell { display: flex; gap: 8px; align-items: center; justify-content: flex-start; }
.btn-icon { border: none; font-size: 0; cursor: pointer; padding: 8px 12px; border-radius: 6px; transition: all 0.2s ease; color: white; font-weight: 500; }
.btn-icon.btn-ver { background: #2563eb; }
.btn-icon.btn-ver:hover { background: #1d4ed8; transform: scale(1.05); }
.btn-icon.btn-editar { background: #f59e0b; }
.btn-icon.btn-editar:hover { background: #d97706; transform: scale(1.05); }
.btn-icon.btn-anular { background: #dc2626; }
.btn-icon.btn-anular:hover { background: #b91c1c; transform: scale(1.05); }
.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular) { background: #6b7280; }
.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular):hover { background: #4b5563; transform: scale(1.05); }
.actions-cell svg { margin-right: 0 !important; filter: brightness(0) invert(1); }

.loading-cell, .no-results { text-align: center; padding: 24px; color: #9ca3af; font-size: 0.95rem; }

/* Paginación */
.pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding: 12px 16px; background: #f9f9fb; border-radius: 8px; border: 1px solid #e5e7eb; }
.pagination-info { color: #6b7280; font-size: 0.9rem; }
.pagination-info .separator { margin: 0 8px; color: #d1d5db; }
.btn-pag { padding: 8px 12px; background: white; border: 1px solid #e5e7eb; border-radius: 6px; cursor: pointer; font-weight: 500; color: #374151; transition: all 0.2s ease; }
.btn-pag:hover:not(:disabled) { background: var(--color-primary, #1e40af); color: white; border-color: var(--color-primary, #1e40af); }
.btn-pag:disabled { opacity: 0.4; cursor: not-allowed; }

/* Modales */
.modal-editar-pago, .modal-confirmar { padding: 24px; max-width: 520px; margin: 0 auto; }
.modal-editar-pago h3, .modal-confirmar h3 { margin: 0 0 16px; font-size: 1.3rem; font-weight: 600; color: #111827; }
.modal-confirmar p { margin-bottom: 16px; color: #6b7280; font-size: 0.95rem; line-height: 1.6; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 16px; }
.btn-danger { background: #dc2626; color: white; }
.btn-danger:hover { background: #b91c1c; }

/* Historial modal */
.historial-lista { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
.historial-item { display: grid; grid-template-columns: 110px 140px 1fr; gap: 8px; align-items: center; padding: 10px; border: 1px solid #e5e7eb; border-radius: 8px; }
.historial-fecha { color: #374151; font-weight: 600; }
.historial-tipo { background: #eff6ff; color: #1e40af; padding: 4px 10px; border-radius: 999px; font-size: 0.85rem; text-align: center; }

/* Responsive */
@media (max-width: 768px) {
  .pago-view { padding: 16px; }
  .form-grid { grid-template-columns: 1fr; }
  .navegacion-vistas button { font-size: 0.9rem; padding: 12px 16px; }
  .tabla-pagos { font-size: 0.85rem; }
  .tabla-pagos th, .tabla-pagos td { padding: 12px 8px; }
  .pagination { flex-direction: column; gap: 10px; }
  .historial-item { grid-template-columns: 100px 1fr; }
  .historial-tipo { justify-self: start; }
}
</style>
