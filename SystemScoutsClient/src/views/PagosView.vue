<template>
  <!-- Contenedor principal del módulo de pagos -->
  <div class="pago-view wide">
    <!-- Navegación + Logo -->
    <div class="navegacion-vistas">
      <div class="logo-wrap" v-if="logoUrl">
        <img :src="logoUrl" alt="Logo" class="header-logo" />
      </div>

      <button @click="cambiarVista('registro')" :class="{ active: vistaActiva === 'registro' }" aria-label="Ir a Registro de Pago">
        <AppIcons name="clipboard" :size="20" />
        <span>Registro de Pago</span>
      </button>

      <button @click="cambiarVista('historico')" :class="{ active: vistaActiva === 'historico' }" aria-label="Ir a Histórico de Pagos">
        <AppIcons name="chart-bar" :size="20" />
        <span>Histórico</span>
      </button>
    </div>

    <!-- ====================== REGISTRO ====================== -->
    <div v-if="vistaActiva === 'registro'" class="vista-registrar">
      <div class="card-registro">
        <div class="card-header">
          <h3>
            <AppIcons name="clipboard" :size="24" />
            Registro de Pago
          </h3>
          <p>El método de pago permitido es únicamente <strong>Transferencia bancaria</strong>.</p>
        </div>

        <!-- Selector Individual / Masivo (azul) -->
        <div class="tipo-registro-selector">
          <button
            type="button"
            @click="tipoRegistro = 'individual'"
            :class="['tipo-btn', { active: tipoRegistro === 'individual' }]"
            aria-pressed="tipoRegistro === 'individual'"
          >
            <AppIcons name="user" :size="20" />
            <span>Individual</span>
          </button>

          <button
            type="button"
            @click="tipoRegistro = 'masivo'"
            :class="['tipo-btn', { active: tipoRegistro === 'masivo' }]"
            aria-pressed="tipoRegistro === 'masivo'"
          >
            <AppIcons name="users" :size="20" />
            <span>Masivo</span>
          </button>
        </div>

        <!-- ---------------------- INDIVIDUAL ---------------------- -->
        <form
          v-if="tipoRegistro === 'individual'"
          @submit.prevent="registrarPagoIndividual"
          class="form-registro-individual"
        >
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
                <span class="search-icon">
                  <AppIcons name="search" :size="18" />
                </span>
              </div>
              <small class="help-text">Primero busca y selecciona a la persona. El botón “Registrar Pago” se habilita tras seleccionar.</small>
            </div>

            <!-- Resultados -->
            <div v-if="resultadosBusqueda.length > 0" class="resultados-busqueda">
              <div
                v-for="persona in resultadosBusqueda"
                :key="persona.id"
                @click="seleccionarPersona(persona)"
                class="resultado-item"
                role="button"
                tabindex="0"
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

          <!-- Datos de la Persona (solo lectura) -->
          <div class="form-grid form-padding">
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
            <div class="form-group full-width">
              <label>Dirección</label>
              <input v-model="formIndividual.direccion" type="text" readonly class="readonly-input" />
            </div>
          </div>

          <div class="form-divider"><h4>Información del Pago</h4></div>

          <!-- Información de pago -->
          <div class="form-grid form-padding">
            <div class="form-group">
              <label>Curso / Capacitación *</label>
              <select v-model="formIndividual.curso" required>
                <option value="">Seleccione un curso</option>
                <option v-for="curso in cursos" :key="curso.value" :value="curso.value">
                  {{ curso.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Valor Pagado *</label>
              <div class="input-with-prefix">
                <span class="prefix">$</span>
                <input
                  v-model.number="formIndividual.valor_pagado"
                  type="number"
                  min="0"
                  step="1"
                  required
                  placeholder="25000"
                />
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
              <input
                v-model="formIndividual.observacion"
                type="text"
                maxlength="100"
                placeholder="Comentario u observación (opcional)"
              />
            </div>
          </div>

          <!-- Comprobante -->
          <div class="form-group full-width form-padding">
            <label>Comprobante de Transferencia (opcional)</label>
            <div class="file-upload-wrapper">
              <input id="file-individual" type="file" @change="handleFileIndividual" accept=".pdf,.jpg,.jpeg,.png" />
              <label for="file-individual" class="file-upload-label">
                <AppIcons name="file" :size="18" />
                <span>{{ formIndividual.file ? formIndividual.file.name : 'Seleccionar archivo' }}</span>
              </label>
            </div>
          </div>

          <!-- Acciones -->
          <div class="form-actions form-padding">
            <button type="submit" class="btn btn-primario" :disabled="!formIndividual.personaId">
              <AppIcons name="check" :size="16" />
              Registrar Pago
            </button>
            <button type="button" @click="limpiarFormularioIndividual" class="btn btn-secundario">
              <AppIcons name="x" :size="16" />
              Limpiar
            </button>
          </div>
        </form>

        <!-- ---------------------- MASIVO ---------------------- -->
        <form
          v-if="tipoRegistro === 'masivo'"
          @submit.prevent="registrarPagoMasivo"
          class="form-registro-masivo"
        >
          <!-- Filtros en una sola línea (desktop) -->
          <div class="form-grid form-padding grid-inline-masivo">
            <div class="form-group">
              <label>Grupo Scout *</label>
              <select v-model="formMasivo.grupo" required @change="filtrarParticipantesPorGrupo">
                <option value="">Seleccione un grupo</option>
                <option v-for="grupo in grupos" :key="grupo.value" :value="grupo.value">
                  {{ grupo.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Curso / Capacitación *</label>
              <select v-model="formMasivo.curso" required>
                <option value="">Seleccione un curso</option>
                <option v-for="curso in cursos" :key="curso.value" :value="curso.value">
                  {{ curso.label }}
                </option>
              </select>
            </div>

            <div class="form-group align-end">
              <label class="label-invisible">Cargar</label>
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
            </div>
          </div>

          <!-- Lista de participantes -->
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

          <!-- Datos de pago masivo -->
          <div class="form-divider" v-if="participantesSeleccionados.length > 0">
            <h4>Pago Masivo</h4>
          </div>

          <div class="form-grid form-padding" v-if="participantesSeleccionados.length > 0">
            <div class="form-group">
              <label>Valor por Persona *</label>
              <div class="input-with-prefix">
                <span class="prefix">$</span>
                <input
                  v-model.number="formMasivo.valor_pagado"
                  type="number"
                  min="0"
                  step="1"
                  required
                  placeholder="25000"
                />
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
              <input
                v-model="formMasivo.observacion"
                type="text"
                maxlength="100"
                placeholder="Comentario u observación (opcional)"
              />
            </div>
          </div>

          <!-- Comprobante grupal -->
          <div class="form-group full-width form-padding" v-if="participantesSeleccionados.length > 0">
            <label>Comprobante Grupal *</label>
            <div class="file-upload-wrapper">
              <input id="file-masivo" type="file" @change="handleFileMasivo" accept=".pdf,.jpg,.jpeg,.png" required />
              <label for="file-masivo" class="file-upload-label">
                <AppIcons name="file" :size="18" />
                <span>{{ formMasivo.file ? formMasivo.file.name : 'Seleccionar archivo' }}</span>
              </label>
            </div>
          </div>

          <!-- Resumen + Acciones -->
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

          <div class="form-actions form-padding" v-if="participantesSeleccionados.length > 0">
            <button
              type="submit"
              class="btn btn-primario"
              :disabled="!formMasivo.file || !formMasivo.valor_pagado"
            >
              <AppIcons name="check" :size="16" />
              Registrar Pago Masivo ({{ participantesSeleccionados.length }})
            </button>
            <button type="button" @click="limpiarFormularioMasivo" class="btn btn-secundario">
              <AppIcons name="x" :size="16" />
              Cancelar
            </button>
          </div>

          <div
            v-if="participantesCargados.length > 0 && participantesSeleccionados.length === 0"
            class="no-resultados"
            role="status"
          >
            No hay participantes seleccionados. Debes elegir al menos uno para registrar.
          </div>
        </form>
      </div>
    </div>

    <!-- ====================== HISTÓRICO ====================== -->
    <div v-if="vistaActiva === 'historico'" class="vista-buscar">
      <div class="card-registro">
        <div class="card-header">
          <h3>
            <AppIcons name="chart-bar" :size="24" />
            Histórico de Pagos
          </h3>
          <p>Consulta y administra todos los pagos</p>
        </div>

        <div class="filtros-avanzados">
          <div class="form-grid form-padding grid-1">
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

        <!-- Tabla -->
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
                  <span class="spinner"></span>
                  Cargando pagos...
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
                  <button
                    @click="verHistorial(pago.perId)"
                    class="btn-icon btn-ver"
                    title="Historial"
                    aria-label="Ver historial de la persona"
                  >
                    <AppIcons name="history" :size="18" />
                  </button>

                  <button
                    @click="abrirModal(pago)"
                    class="btn-icon btn-editar"
                    title="Editar"
                    aria-label="Editar pago"
                  >
                    <AppIcons name="edit" :size="18" />
                  </button>

                  <button
                    @click="abrirModalAnular(pago)"
                    class="btn-icon btn-anular"
                    title="Anular (total o parcial)"
                    aria-label="Anular pago"
                  >
                    <AppIcons name="trash" :size="18" />
                  </button>

                  <button
                    @click="abrirModalTransferir(pago)"
                    class="btn-icon"
                    title="Transferir beneficiario"
                    aria-label="Transferir pago a otra persona"
                  >
                    <AppIcons name="repeat" :size="18" />
                  </button>

                  <button
                    v-if="pago.comprobante"
                    @click="descargarComprobante(pago)"
                    class="btn-icon"
                    title="Descargar comprobante"
                    aria-label="Descargar comprobante"
                  >
                    <AppIcons name="paperclip" :size="18" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1">
          <button
            @click="cambiarPagina(paginaActual - 1)"
            :disabled="paginaActual === 1"
            class="btn-pag"
          >
            ← Anterior
          </button>

          <div class="pagination-info">
            Página {{ paginaActual }} de {{ totalPages }}
            <span class="separator">|</span>
            Mostrando
            {{ (paginaActual - 1) * itemsPorPagina + 1 }} -
            {{ Math.min(paginaActual * itemsPorPagina, pagosFiltrados.length) }}
            de {{ pagosFiltrados.length }}
          </div>

          <button
            @click="cambiarPagina(paginaActual + 1)"
            :disabled="paginaActual === totalPages"
            class="btn-pag"
          >
            Siguiente →
          </button>
        </div>
      </div>
    </div>

    <!-- ====================== MODALES ====================== -->

    <!-- Editar pago -->
    <BaseModal v-if="showModal" @close="cerrarModal">
      <div class="modal-editar-pago">
        <h3>Editar Pago</h3>

        <div class="form-group">
          <label>Nombre</label>
          <input v-model="pagoSeleccionado.nombre" type="text" readonly />
        </div>

        <div class="form-group">
          <label>RUT</label>
          <input v-model="pagoSeleccionado.rut" type="text" readonly />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="pagoSeleccionado.email" type="email" />
        </div>

        <div class="form-group">
          <label>Teléfono</label>
          <input v-model="pagoSeleccionado.telefono" type="text" />
        </div>

        <div class="form-group">
          <label>Dirección</label>
          <input v-model="pagoSeleccionado.direccion" type="text" />
        </div>

        <div class="modal-actions">
          <button @click="guardarPago" class="btn btn-primario">Guardar</button>
          <button @click="cerrarModal" class="btn btn-secundario">Cancelar</button>
        </div>
      </div>
    </BaseModal>

    <!-- Anular pago -->
    <BaseModal v-if="showModalAnular" @close="cerrarModalAnular">
      <div class="modal-confirmar">
        <h3>Anular pago</h3>
        <p>
          ¿Anulación total o parcial del pago de
          <strong>{{ pagoSeleccionado?.nombre }}</strong>?
        </p>

        <div class="form-group">
          <label>Tipo de anulación</label>
          <select v-model="anulacionTipo">
            <option value="total">Total</option>
            <option value="parcial">Parcial</option>
          </select>
        </div>

        <div class="form-group" v-if="anulacionTipo === 'parcial'">
          <label>Monto a devolver</label>
          <div class="input-with-prefix">
            <span class="prefix">$</span>
            <input
              type="number"
              v-model.number="anulacionMonto"
              min="0"
              :max="pagoSeleccionado?.monto || 0"
            />
          </div>
          <small>Máximo: ${{ (pagoSeleccionado?.monto || 0).toLocaleString('es-CL') }}</small>
        </div>

        <div class="form-group">
          <label>Motivo / Observación</label>
          <input v-model="anulacionObs" maxlength="100" placeholder="Ej: desistimiento, error, etc." />
        </div>

        <div class="modal-actions">
          <button @click="confirmarAnulacionConDetalle" class="btn btn-danger">Confirmar</button>
          <button @click="cerrarModalAnular" class="btn btn-secundario">Cancelar</button>
        </div>
      </div>
    </BaseModal>

    <!-- Transferir beneficiario -->
    <BaseModal v-if="showModalTransferir" @close="cerrarModalTransferir">
      <div class="modal-editar-pago">
        <h3>Transferir pago a otra persona</h3>

        <div class="form-group">
          <label>Buscar nuevo beneficiario (Nombre o RUT)</label>
          <input
            v-model="busquedaTransfer"
            type="text"
            @input="buscarTransfer"
            placeholder="Ej: 12.345.678-9 o Juan..."
          />

          <div v-if="resultadosTransfer.length" class="resultados-busqueda">
            <div
              v-for="p in resultadosTransfer"
              :key="p.id"
              class="resultado-item"
              @click="seleccionarTransfer(p)"
            >
              <div class="resultado-info">
                <strong>{{ p.nombre }}</strong>
                <span class="rut">{{ p.rut }}</span>
              </div>
            </div>
          </div>

          <div v-else-if="busquedaTransfer && !resultadosTransfer.length" class="no-resultados">
            Sin coincidencias
          </div>
        </div>

        <div class="modal-actions">
          <button :disabled="!nuevoBeneficiario" @click="confirmarTransferencia" class="btn btn-primario">
            Confirmar
          </button>
          <button @click="cerrarModalTransferir" class="btn btn-secundario">Cancelar</button>
        </div>
      </div>
    </BaseModal>

    <!-- Historial por persona -->
    <BaseModal v-if="showHistorial" @close="() => (showHistorial = false)">
      <template #title>
        Historial de {{ historialPersona?.nombre }} — {{ historialPersona?.rut }}
      </template>

      <div class="modal-body-content">
        <ul>
          <li v-for="e in historialEventos" :key="e.id">
            <strong>{{ formatearFecha(e.fecha) }}</strong> — {{ e.tipo }}: {{ e.detalle }}
          </li>
        </ul>
      </div>

      <template #footer>
        <button class="btn btn-secundario" @click="showHistorial = false">Cerrar</button>
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
/*
  PagosView.vue
  -----------------------------------------------------------
  - Registro Individual/Masivo (método único: Transferencia)
  - Fecha por defecto: hoy (día del registro)
  - Búsqueda obligatoria por persona (individual)
  - Observación (opcional)
  - Histórico por persona
  - Anulación total/parcial con devolución
  - Transferencia de beneficiario
  - UI centrada, ordenada, y consistente con el style del proyecto
  - TODO: Reemplazar datos DEMO por servicios (API/BD).
*/
import { ref, computed, onMounted } from 'vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

// Recibir logo desde el padre: <PagosView :logo-url="..." />
defineProps({ logoUrl: { type: String, default: '' } })

/** Fecha actual formato ISO (YYYY-MM-DD) */
function todayISO () {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

/** Fecha legible es-CL */
function formatearFecha (fecha) {
  if (!fecha) return '-'
  const d = new Date(fecha)
  return d.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric' })
}

/** Toast simple */
const alerta = ref({ mensaje: '', tipo: '' })
function mostrarAlerta (mensaje, tipo = 'info') {
  alerta.value = { mensaje, tipo }
  setTimeout(() => (alerta.value = { mensaje: '', tipo: '' }), 3200)
}

/* ----------------------- ESTADO ----------------------- */
const vistaActiva = ref('registro')
const tipoRegistro = ref('individual')

const cambiarVista = (vista) => {
  vistaActiva.value = vista
  if (vista === 'historico') cargarPagos()
  if (vista === 'registro') {
    if (!formIndividual.value.fecha_pago) formIndividual.value.fecha_pago = todayISO()
    if (!formMasivo.value.fecha_pago) formMasivo.value.fecha_pago = todayISO()
  }
}

/* ----------------------- DATOS DEMO (reemplazar por API) ----------------------- */
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

/* ----------------------- REFS / FORMULARIOS ----------------------- */
const personas = ref([])
const cursos = ref([])
const grupos = ref([])
const pagos = ref([])
const cargandoPagos = ref(false)

const busquedaPersona = ref('')
const resultadosBusqueda = ref([])
const buscando = ref(false)

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

const filtroPersona = ref('')
const paginaActual = ref(1)
const itemsPorPagina = ref(10)

const showModal = ref(false)
const showModalAnular = ref(false)
const showModalTransferir = ref(false)
const pagoSeleccionado = ref(null)

const showHistorial = ref(false)
const historialPersona = ref(null)
const historialEventos = ref([])

const anulacionTipo = ref('total')
const anulacionMonto = ref(0)
const anulacionObs = ref('')

const busquedaTransfer = ref('')
const resultadosTransfer = ref([])
const nuevoBeneficiario = ref(null)

/* ----------------------- CICLO DE VIDA ----------------------- */
onMounted(() => {
  // Cargar datos DEMO. Reemplaza por llamadas reales:
  // personas.value = await personasService.listar()
  personas.value = PERSONAS_FICTICIAS
  cursos.value = CURSOS_FICTICIOS
  grupos.value = GRUPOS_FICTICIOS
  pagos.value = PAGOS_FICTICIOS
})

/* ----------------------- LÓGICA: INDIVIDUAL ----------------------- */
const buscarPersona = () => {
  if (!busquedaPersona.value || busquedaPersona.value.length < 2) {
    resultadosBusqueda.value = []
    return
  }
  const q = busquedaPersona.value.toLowerCase()
  resultadosBusqueda.value = personas.value
    .filter(p => p.nombre.toLowerCase().includes(q) || p.rut.toLowerCase().includes(q))
    .slice(0, 6)
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

const handleFileIndividual = e => (formIndividual.value.file = e.target.files[0])

const registrarPagoIndividual = async () => {
  try {
    if (!formIndividual.value.personaId) {
      mostrarAlerta('Debes seleccionar una persona antes de registrar.', 'error')
      return
    }
    if (!formIndividual.value.fecha_pago) formIndividual.value.fecha_pago = todayISO()

    // TODO: enviar al backend
    // await pagosService.registrarIndividual(formIndividual.value)

    mostrarAlerta('Pago individual registrado correctamente', 'exito')
    limpiarFormularioIndividual()
  } catch (error) {
    mostrarAlerta('Error al registrar pago: ' + error.message, 'error')
  }
}

/* ----------------------- LÓGICA: MASIVO ----------------------- */
const handleFileMasivo = e => (formMasivo.value.file = e.target.files[0])
const filtrarParticipantesPorGrupo = () => { participantesCargados.value = []; participantesSeleccionados.value = [] }

const cargarParticipantesParaMasivo = async () => {
  try {
    cargandoUsuarios.value = true
    // TODO: participantesCargados.value = await gruposService.obtenerParticipantes(formMasivo.grupo, formMasivo.curso)
    participantesCargados.value = [...personas.value] // DEMO
    mostrarAlerta(`${participantesCargados.value.length} participantes cargados`, 'exito')
  } catch (e) {
    mostrarAlerta('Error al cargar participantes: ' + e.message, 'error')
  } finally {
    cargandoUsuarios.value = false
  }
}

const seleccionarTodos = () => { participantesSeleccionados.value = [...participantesCargados.value] }
const deseleccionarTodos = () => { participantesSeleccionados.value = []; mostrarAlerta('No hay participantes seleccionados. Debes elegir al menos uno para registrar.', 'info') }

const limpiarFormularioMasivo = () => {
  formMasivo.value = { grupo: '', curso: '', valor_pagado: '', fecha_pago: todayISO(), metodo_pago: 'Transferencia', observacion: '', file: null }
  participantesCargados.value = []; participantesSeleccionados.value = []
}

const registrarPagoMasivo = async () => {
  try {
    if (participantesSeleccionados.value.length === 0) {
      mostrarAlerta('No puedes registrar un pago masivo sin participantes.', 'error')
      return
    }
    if (!formMasivo.value.fecha_pago) formMasivo.value.fecha_pago = todayISO()

    // TODO:
    // await pagosService.registrarMasivo({ ...formMasivo.value, participantes: participantesSeleccionados.value })

    mostrarAlerta(`Pago masivo registrado para ${participantesSeleccionados.value.length} usuarios`, 'exito')
    limpiarFormularioMasivo()
  } catch (error) {
    mostrarAlerta('Error al registrar pago masivo: ' + error.message, 'error')
  }
}

/* ----------------------- LÓGICA: HISTÓRICO ----------------------- */
async function cargarPagos () {
  try {
    cargandoPagos.value = true
    // TODO: pagos.value = await pagosService.listar({ q: filtroPersona.value })
    pagos.value = PAGOS_FICTICIOS
  } finally {
    cargandoPagos.value = false
  }
}
const aplicarFiltros = () => { paginaActual.value = 1 /* TODO: recargar con filtros */ }
const limpiarFiltros = () => { filtroPersona.value = ''; paginaActual.value = 1 /* TODO: recargar */ }

const pagosFiltrados = computed(() => {
  const q = filtroPersona.value.trim().toLowerCase()
  return q
    ? pagos.value.filter(p => p.nombre?.toLowerCase().includes(q) || p.rut?.toLowerCase().includes(q))
    : [...pagos.value]
})
const totalPages = computed(() => Math.ceil(pagosFiltrados.value.length / itemsPorPagina.value))
const paginatedPagos = computed(() => pagosFiltrados.value.slice((paginaActual.value - 1) * itemsPorPagina.value, paginaActual.value * itemsPorPagina.value))
const cambiarPagina = (pagina) => { if (pagina >= 1 && pagina <= totalPages.value) paginaActual.value = pagina }

/* ----------------------- LÓGICA: MODALES ----------------------- */
const abrirModal = (p) => { pagoSeleccionado.value = { ...p }; showModal.value = true }
const cerrarModal = () => { showModal.value = false; pagoSeleccionado.value = null }
const guardarPago = async () => {
  try {
    const idx = pagos.value.findIndex(p => p.id === pagoSeleccionado.value.id)
    if (idx !== -1) pagos.value[idx] = { ...pagoSeleccionado.value }
    // TODO: await pagosService.actualizar(pagoSeleccionado.value)
    mostrarAlerta('Pago actualizado correctamente', 'exito'); cerrarModal()
  } catch (e) { mostrarAlerta('Error al guardar pago: ' + e.message, 'error') }
}

const verHistorial = async (perId) => {
  try {
    historialPersona.value = personas.value.find(p => p.id === perId)
    // TODO: historialEventos.value = await pagosService.historialPorPersona(perId)
    historialEventos.value = [
      { id: 1, tipo: 'Pago', detalle: 'Curso FDB 2025 · $25.000', fecha: '2025-10-20' },
      { id: 2, tipo: 'Transferencia', detalle: 'Pago transferido a María González', fecha: '2025-10-22' },
      { id: 3, tipo: 'Devolución parcial', detalle: '$10.000', fecha: '2025-10-25' }
    ]
    showHistorial.value = true
  } catch (e) { mostrarAlerta('No fue posible cargar el historial', 'error') }
}

const abrirModalAnular = (p) => { pagoSeleccionado.value = p; anulacionTipo.value = 'total'; anulacionMonto.value = 0; anulacionObs.value = ''; showModalAnular.value = true }
const cerrarModalAnular = () => { showModalAnular.value = false; pagoSeleccionado.value = null }
const confirmarAnulacionConDetalle = async () => {
  try {
    const total = pagoSeleccionado.value.monto
    const monto = anulacionTipo.value === 'total' ? total : (anulacionMonto.value || 0)
    if (monto <= 0 || monto > total) { mostrarAlerta('Monto inválido para devolución', 'error'); return }
    // TODO: await pagosService.anular({ id: pagoSeleccionado.value.id, tipo: anulacionTipo.value, monto, motivo: anulacionObs.value })
    mostrarAlerta(`Anulación ${anulacionTipo.value} registrada ($${monto.toLocaleString('es-CL')})`, 'exito')
    cerrarModalAnular()
  } catch (e) { mostrarAlerta('Error al anular: ' + e.message, 'error') }
}

const abrirModalTransferir = (pago) => { pagoSeleccionado.value = pago; showModalTransferir.value = true }
const cerrarModalTransferir = () => { showModalTransferir.value = false; busquedaTransfer.value = ''; resultadosTransfer.value = []; nuevoBeneficiario.value = null }
const buscarTransfer = () => {
  const q = busquedaTransfer.value.trim().toLowerCase()
  resultadosTransfer.value = q.length < 2 ? [] : personas.value.filter(p => p.nombre.toLowerCase().includes(q) || p.rut.toLowerCase().includes(q)).slice(0, 6)
}
const seleccionarTransfer = (p) => { nuevoBeneficiario.value = p; resultadosTransfer.value = []; busquedaTransfer.value = p.nombre }
const confirmarTransferencia = async () => {
  try {
    if (!nuevoBeneficiario.value) { mostrarAlerta('Selecciona el nuevo beneficiario.', 'error'); return }
    // TODO: await pagosService.transferir({ id: pagoSeleccionado.value.id, nuevoPerId: nuevoBeneficiario.value.id })
    mostrarAlerta(`Pago transferido a ${nuevoBeneficiario.value.nombre}`, 'exito')
    cerrarModalTransferir()
  } catch (e) { mostrarAlerta('Error al transferir: ' + e.message, 'error') }
}

/* ----------------------- UTILIDADES ----------------------- */
const descargarComprobante = (pago) => { console.log('Descargar comprobante:', pago.comprobante); mostrarAlerta('Descarga de comprobante próximamente', 'info') }
const exportarExcel = () => { console.log('Exportar a Excel'); mostrarAlerta('Función de exportación próximamente', 'info') }
</script>

<style scoped>
/* ==================== CONTENEDOR GLOBAL ==================== */
.pago-view {
  margin: 0 auto;
  padding: 24px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Versión “amplia” del módulo */
.pago-view.wide {
  max-width: 1100px; /* tamaño cómodo, un poco más compacto */
}

/* Card contenedora centrada */
.card-registro {
  background: var(--surface, #ffffff);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}
.card-registro:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }

/* ==================== NAVEGACIÓN / LOGO ==================== */
.navegacion-vistas {
  display: flex;
  gap: 8px;
  border-bottom: 2px solid var(--border, #e5e7eb);
  margin-bottom: 24px;
  background: var(--surface, #fff);
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  align-items: center;
  justify-content: center; /* centrado */
}
.logo-wrap { padding-left: 12px; display: flex; align-items: center; }
.header-logo { height: 28px; width: auto; margin-right: 8px; }
.navegacion-vistas button {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: var(--muted-700, #6b7280);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  position: relative;
  max-width: 280px;
}
.navegacion-vistas button:hover:not(.active) { background: #f9fafb; color: var(--brand-700, #1e40af); }
.navegacion-vistas button.active {
  color: var(--brand-700, #1e40af);
  border-bottom-color: var(--brand-600, #1e40af);
  background: #eff6ff;
  font-weight: 600;
}

/* ==================== HEADERS / BLOQUES ==================== */
.card-header {
  background: linear-gradient(to right, #f9fafb, #ffffff);
  padding: 28px 36px; /* espacio interior amplio */
  border-bottom: 2px solid var(--border, #e5e7eb);
  text-align: center;  /* títulos centrados */
}
.card-header h3 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-900, #111827);
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
.card-header p { margin: 0; color: var(--muted-700, #6b7280); font-size: 0.95rem; }

/* Selector Individual/Masivo centrado (AZUL) */
.tipo-registro-selector {
  display: flex;
  gap: 12px;
  padding: 18px 24px;
  background: var(--surface, #fff);
  border-bottom: 2px solid var(--border, #e5e7eb);
  justify-content: center;
}
.tipo-btn {
  flex: 1;
  padding: 12px 20px;
  border-radius: 10px;
  background: #fff;
  border: 2px solid var(--brand-500, #3b82f6); /* delineado azul */
  color: var(--brand-700, #1e40af);
  font-weight: 700;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  transition: all 0.2s ease;
  max-width: 240px;
}
.tipo-btn:hover:not(.active) {
  background: var(--brand-50, #eff6ff);
  border-color: var(--brand-600, #2563eb);
  color: var(--brand-700, #1e40af);
}
.tipo-btn.active {
  background: var(--brand-600, #2563eb);  /* azul sólido */
  border-color: var(--brand-600, #2563eb);
  color: #fff;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
}

/* ==================== FORMULARIOS ==================== */
.vista-registrar, .vista-buscar { display: flex; flex-direction: column; gap: 16px; }

/* Rejilla base: centrada y con padding */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  padding: 0 20px;
}
.form-padding { padding: 16px 20px; }

/* Grupos centrados y con inputs legibles sobre fondo */
.form-group {
  display: flex; flex-direction: column; gap: 8px;
  text-align: center;
  max-width: 520px;
  margin: 0 auto;
}
.form-group.full-width { grid-column: 1 / -1; }

.form-group label {
  font-weight: 700;
  color: var(--text-800, #374151);
  font-size: 0.95rem;
  text-align: center;
}
.form-group input, .form-group select {
  padding: 12px 16px;
  border: 2px solid var(--border, #e5e7eb);
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #ffffff;                      /* casillas bien visibles */
  color: var(--text-900, #111827);
  text-align: center;
  box-shadow: 0 1px 0 rgba(0,0,0,0.02);
}
.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: var(--brand-500, #3b82f6);
  box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}
.readonly-input { background: #f9fafb !important; cursor: not-allowed; color: #6b7280; }

/* Campo con prefijo ($) */
.input-with-prefix {
  display: flex; align-items: center;
  border: 2px solid var(--border, #e5e7eb);
  border-radius: 10px; overflow: hidden; transition: all 0.2s ease;
  background: #fff;
}
.input-with-prefix:focus-within { border-color: var(--brand-500, #3b82f6); box-shadow: 0 0 0 3px rgba(59,130,246,0.15); }
.input-with-prefix .prefix {
  background: #f3f4f6; padding: 12px 16px; font-weight: 700; color: #6b7280; border-right: 2px solid var(--border, #e5e7eb);
}
.input-with-prefix input { flex: 1; border: none; padding: 12px 16px; font-size: 1rem; text-align: center; background: #fff; }
.input-with-prefix input:focus { outline: none; }

/* Búsqueda persona */
.search-section { margin-bottom: 16px; padding: 16px 20px; border-bottom: 2px solid var(--border, #e5e7eb); }
.search-group { position: relative; }
.search-input-wrapper { position: relative; }
.search-input {
  width: 100%;
  padding: 12px 44px 12px 12px !important;
  border: 2px solid var(--border, #e5e7eb) !important;
  border-radius: 12px !important;
  background: #fff;
}
.search-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); font-size: 1.1rem; pointer-events: none; }
.search-icon svg { margin-right: 0; }
.help-text { color: #6b7280; font-size: 0.85rem; }

/* Resultados búsqueda */
.resultados-busqueda {
  margin-top: 8px; border: 2px solid var(--border, #e5e7eb); border-radius: 8px; background: #fff; max-height: 260px; overflow-y: auto;
}
.resultado-item {
  padding: 12px; cursor: pointer; border-bottom: 1px solid #f3f4f6; transition: all 0.2s ease; display: flex; justify-content: space-between; align-items: center;
}
.resultado-item:last-child { border-bottom: none; }
.resultado-item:hover { background: var(--brand-50, #eff6ff); }
.resultado-info { display: flex; flex-direction: column; gap: 2px; }
.resultado-info strong { color: var(--text-900, #111827); font-size: 0.95rem; }
.resultado-info .rut { color: #6b7280; font-size: 0.85rem; }
.no-resultados { padding: 14px; text-align: center; color: #9ca3af; font-style: italic; }

/* Divider */
.form-divider { margin: 24px 0 14px; padding-top: 12px; border-top: 2px solid var(--border, #e5e7eb); }
.form-divider h4 { margin: 0; font-size: 1.1rem; font-weight: 700; color: var(--text-900, #111827); display: flex; align-items: center; gap: 8px; justify-content: center; }

/* Upload */
.file-upload-wrapper input[type="file"] { display: none; }
.file-upload-label {
  display: flex; align-items: center; gap: 10px; padding: 10px 14px;
  border: 2px dashed #d1d5db; border-radius: 10px; cursor: pointer; transition: all 0.2s ease;
  background: #fafafa; color: #6b7280; font-weight: 600;
}
.file-upload-label:hover { border-color: var(--brand-500, #3b82f6); background: var(--brand-50, #eff6ff); color: var(--brand-700, #1e40af); }
.file-upload-label .icon { font-size: 1.3rem; }

/* Masivo: listado participantes */
.participantes-section { margin-top: 16px; padding: 14px; background: #f9fafb; border-radius: 8px; border: 2px solid var(--border, #e5e7eb); }
.participantes-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 2px solid var(--border, #e5e7eb); }
.participantes-header h4 { margin: 0; font-size: 1rem; font-weight: 700; color: var(--text-900, #111827); }
.seleccion-acciones { display: flex; gap: 8px; }
.btn-link { background: none; border: none; color: var(--brand-700, #1e40af); cursor: pointer; font-size: 0.9rem; text-decoration: underline; padding: 2px 4px; }
.btn-link:hover { color: var(--brand-800, #1e3a8a); }
.participantes-lista { max-height: 260px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; }
.participante-item { display: flex; align-items: center; gap: 10px; padding: 10px; background: #fff; border-radius: 8px; border: 1px solid var(--border, #e5e7eb); transition: all 0.2s ease; }
.participante-item:hover { border-color: var(--brand-600, #2563eb); background: var(--brand-50, #eff6ff); }
.checkbox-styled { width: 18px; height: 18px; cursor: pointer; }
.participante-label { flex: 1; cursor: pointer; display: flex; justify-content: space-between; align-items: center; margin: 0; }
.participante-info { display: flex; flex-direction: column; gap: 2px; }
.participante-info strong { color: var(--text-900, #111827); font-size: 0.9rem; }
.participante-info .rut { color: #6b7280; font-size: 0.8rem; }
.participante-label .email { color: #6b7280; font-size: 0.8rem; }

/* Resumen masivo */
.resumen-masivo {
  margin-top: 16px; padding: 14px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 10px; border: 2px solid #93c5fd;
}
.resumen-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; color: var(--brand-800, #1e3a8a); }
.resumen-item span { font-size: 0.95rem; }
.resumen-item strong { font-size: 1rem; font-weight: 700; }
.resumen-item.total { margin-top: 10px; padding-top: 10px; border-top: 2px solid #93c5fd; font-size: 1.05rem; }
.resumen-item.total strong { font-size: 1.2rem; }

/* Acciones */
.form-actions { display: flex; gap: 10px; margin-top: 16px; justify-content: center; }
.btn {
  padding: 12px 20px; border: none; border-radius: 10px; font-size: 1rem; font-weight: 700;
  cursor: pointer; transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.btn-primario { background: var(--brand-600, #2563eb); color: #fff; }
.btn-primario:hover:not(:disabled) { background: var(--brand-700, #1d4ed8); box-shadow: 0 4px 6px rgba(0,0,0,0.12); transform: translateY(-1px); }
.btn-secundario { background: #f3f4f6; color: #374151; }
.btn-secundario:hover { background: #e5e7eb; }
.btn-info { background: var(--brand-500, #3b82f6); color: #fff; }
.btn-info:hover:not(:disabled) { background: var(--brand-600, #2563eb); }
.btn-success { background: #10b981; color: #fff; }
.btn-success:hover { background: #059669; }
.btn:disabled { opacity: 0.55; cursor: not-allowed; }

/* ==================== FILTROS HISTÓRICO ==================== */
.filtros-avanzados { margin-bottom: 16px; }
.filtros-acciones { display: flex; gap: 10px; margin-top: 12px; justify-content: center; }

/* ==================== TABLA ==================== */
.tabla-pagos { overflow-x: auto; margin-top: 12px; border-radius: 10px; border: 1px solid var(--border, #e5e7eb); }
.tabla-pagos table { width: 100%; border-collapse: collapse; background: #fff; table-layout: auto; min-width: 920px; }
.tabla-pagos thead { background: linear-gradient(to right, var(--brand-700, #1e40af), var(--brand-800, #1e3a8a)); color: #fff; }
.tabla-pagos th { padding: 16px; text-align: center; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
.tabla-pagos td { padding: 16px; border-bottom: 1px solid #f3f4f6; text-align: center; }
.tabla-pagos th:nth-child(4), .tabla-pagos td:nth-child(4) { text-align: right; }
.tabla-pagos th:nth-child(5), .tabla-pagos td:nth-child(5) { white-space: nowrap; }
.tabla-pagos th:nth-child(6), .tabla-pagos td:nth-child(6) { width: 260px; white-space: nowrap; }

/* Hover filas */
.tabla-pagos tbody tr { transition: all 0.2s ease; }
.tabla-pagos tbody tr:hover { background: #f9fafb; }

/* Monto resaltado */
.tabla-pagos .monto { font-weight: 700; color: #059669; }

/* ==================== ACCIONES / ICONOS ==================== */
.actions-cell { display: flex; gap: 8px; align-items: center; justify-content: center; }
.btn-icon {
  border: none; font-size: 0; cursor: pointer; padding: 8px 12px; border-radius: 10px;
  transition: all 0.2s ease; color: #fff; min-width: 36px; min-height: 36px;
  display: inline-flex; align-items: center; justify-content: center;
}
.btn-icon.btn-ver { background: #2563eb; }
.btn-icon.btn-ver:hover { background: #1d4ed8; transform: scale(1.05); }
.btn-icon.btn-editar { background: #f59e0b; }
.btn-icon.btn-editar:hover { background: #d97706; transform: scale(1.05); }
.btn-icon.btn-anular { background: #dc2626; }
.btn-icon.btn-anular:hover { background: #b91c1c; transform: scale(1.05); }
.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular) { background: #6b7280; }
.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular):hover { background: #4b5563; transform: scale(1.05); }
.actions-cell svg { margin-right: 0 !important; filter: brightness(0) invert(1); }

/* ==================== PAGINACIÓN ==================== */
.pagination {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 16px; padding: 12px 16px;
  background: #f9f9fb; border-radius: 10px; border: 1px solid var(--border, #e5e7eb);
}
.pagination-info { color: #6b7280; font-size: 0.9rem; }
.pagination-info .separator { margin: 0 8px; color: #d1d5db; }
.btn-pag { padding: 8px 12px; background: #fff; border: 1px solid var(--border, #e5e7eb); border-radius: 8px; cursor: pointer; font-weight: 700; color: #374151; transition: all 0.2s ease; }
.btn-pag:hover:not(:disabled) { background: var(--brand-600, #2563eb); color: #fff; border-color: var(--brand-600, #2563eb); }
.btn-pag:disabled { opacity: 0.4; cursor: not-allowed; }

/* ==================== MODALES ==================== */
.modal-editar-pago, .modal-confirmar { padding: 24px; max-width: 560px; }
.modal-editar-pago h3, .modal-confirmar h3 { margin: 0 0 16px 0; font-size: 1.3rem; font-weight: 700; color: var(--text-900, #111827); }
.modal-confirmar p { margin-bottom: 16px; color: #6b7280; font-size: 0.95rem; line-height: 1.6; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 16px; }
.btn-danger { background: #dc2626; color: #fff; }
.btn-danger:hover { background: #b91c1c; }

/* ==================== LAYOUTS ESPECIALES ==================== */
.grid-inline-masivo { grid-template-columns: 1fr 1fr auto; }
.align-end { align-self: end; }
.label-invisible { visibility: hidden; }

/* Forzar 1 columna en el grid simple de filtros históricos */
.grid-1 { grid-template-columns: 1fr; }

/* ==================== RESPONSIVE ==================== */
@media (max-width: 992px) {
  .grid-inline-masivo { grid-template-columns: 1fr; }
  .align-end .btn.btn-info { width: 100%; margin-top: 8px; }
}
@media (max-width: 768px) {
  .pago-view { padding: 16px; }
  .form-grid { grid-template-columns: 1fr; }
  .navegacion-vistas button { font-size: 0.9rem; padding: 12px 16px; }
  .tabla-pagos { font-size: 0.85rem; }
  .tabla-pagos th, .tabla-pagos td { padding: 12px 8px; }
  .pagination { flex-direction: column; gap: 10px; }
}
</style>

