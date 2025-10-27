<template>
  <div class="pago-view">
    <!-- Navegación de Vistas -->
    <div class="navegacion-vistas">
      <button 
        @click="cambiarVista('registro')" 
        :class="{ active: vistaActiva === 'registro' }">
        <AppIcons name="clipboard" :size="20" />
        <span>Registro de Pago</span>
      </button>
      <button 
        @click="cambiarVista('historico')" 
        :class="{ active: vistaActiva === 'historico' }">
        <AppIcons name="chart-bar" :size="20" />
        <span>Histórico</span>
      </button>
    </div>

    <!-- ✅ VISTA REGISTRO -->
    <div v-if="vistaActiva === 'registro'" class="vista-registrar">
      <div class="card-registro">
        <div class="card-header">
          <h3><AppIcons name="clipboard" :size="24" /> Registro de Pago</h3>
          <p>Selecciona el tipo de registro y completa la información</p>
        </div>
        
        <!-- Selector de Tipo de Registro -->
        <div class="tipo-registro-selector">
          <button 
            type="button"
            @click="tipoRegistro = 'individual'" 
            :class="['tipo-btn', { active: tipoRegistro === 'individual' }]">
            <AppIcons name="user" :size="20" />
            <span>Individual</span>
          </button>
          <button 
            type="button"
            @click="tipoRegistro = 'masivo'" 
            :class="['tipo-btn', { active: tipoRegistro === 'masivo' }]">
            <AppIcons name="users" :size="20" />
            <span>Masivo</span>
          </button>
        </div>

        <!-- FORMULARIO INDIVIDUAL -->
        <form v-if="tipoRegistro === 'individual'" @submit.prevent="registrarPagoIndividual" class="form-registro-individual">
          <!-- Búsqueda de Persona -->
          <div class="search-section">
            <div class="form-group search-group">
              <label>Buscar Participante</label>
              <div class="search-input-wrapper">
                <input 
                  v-model="busquedaPersona" 
                  type="text" 
                  placeholder="Buscar por RUT, Nombre o Grupo..."
                  @input="buscarPersona"
                  class="search-input">
                <span class="search-icon"><AppIcons name="search" :size="18" /></span>
              </div>
            </div>

            <!-- Resultados de búsqueda -->
            <div v-if="resultadosBusqueda.length > 0" class="resultados-busqueda">
              <div 
                v-for="persona in resultadosBusqueda" 
                :key="persona.id"
                @click="seleccionarPersona(persona)"
                class="resultado-item">
                <div class="resultado-info">
                  <strong>{{ persona.nombre }}</strong>
                  <span class="rut">{{ persona.rut }}</span>
                </div>
                <div class="resultado-extra">
                  <span class="grupo">{{ persona.grupo }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="busquedaPersona && !buscando" class="no-resultados">
              No se encontraron personas con ese criterio
            </div>
          </div>

          <!-- Datos de la Persona (solo lectura) -->
          <div class="form-grid">
            <div class="form-group">
              <label>Nombre Completo</label>
              <input v-model="formIndividual.nombre" type="text" readonly class="readonly-input">
            </div>
            <div class="form-group">
              <label>RUT</label>
              <input v-model="formIndividual.rut" type="text" readonly class="readonly-input">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="formIndividual.email" type="email" readonly class="readonly-input">
            </div>
            <div class="form-group">
              <label>Teléfono</label>
              <input v-model="formIndividual.telefono" type="text" readonly class="readonly-input">
            </div>
            <div class="form-group">
              <label>Grupo Scout</label>
              <input v-model="formIndividual.grupo" type="text" readonly class="readonly-input">
            </div>
            <div class="form-group">
              <label>Dirección</label>
              <input v-model="formIndividual.direccion" type="text" readonly class="readonly-input">
            </div>
          </div>

          <!-- Datos del Pago -->
          <div class="form-divider">
            <h4>💵 Información del Pago</h4>
          </div>

          <div class="form-grid">
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
                <input v-model.number="formIndividual.valor_pagado" type="number" required placeholder="25000">
              </div>
            </div>
            <div class="form-group">
              <label>Fecha de Pago *</label>
              <input v-model="formIndividual.fecha_pago" type="date" required>
            </div>
            <div class="form-group">
              <label>Método de Pago</label>
              <select v-model="formIndividual.metodo_pago">
                <option value="Transferencia">Transferencia</option>
                <option value="Efectivo">Efectivo</option>
                <option value="Tarjeta">Tarjeta</option>
              </select>
            </div>
          </div>

          <div class="form-group full-width">
            <label>Comprobante de Pago (opcional)</label>
            <div class="file-upload-wrapper">
              <input type="file" @change="handleFileIndividual" id="file-individual" accept=".pdf,.jpg,.jpeg,.png">
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

        <!-- FORMULARIO MASIVO -->
        <form v-if="tipoRegistro === 'masivo'" @submit.prevent="registrarPagoMasivo" class="form-registro-masivo">
          <div class="form-grid">
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
          </div>

          <button 
            type="button" 
            @click="cargarParticipantesParaMasivo" 
            class="btn btn-info"
            :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoUsuarios">
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
                  class="checkbox-styled">
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

          <div class="form-divider" v-if="participantesSeleccionados.length > 0">
            <h4>💵 Información del Pago Masivo</h4>
          </div>

          <div class="form-grid" v-if="participantesSeleccionados.length > 0">
            <div class="form-group">
              <label>Valor por Persona *</label>
              <div class="input-with-prefix">
                <span class="prefix">$</span>
                <input v-model.number="formMasivo.valor_pagado" type="number" required placeholder="25000">
              </div>
            </div>
            <div class="form-group">
              <label>Fecha de Pago *</label>
              <input v-model="formMasivo.fecha_pago" type="date" required>
            </div>
            <div class="form-group">
              <label>Método de Pago</label>
              <select v-model="formMasivo.metodo_pago">
                <option value="Transferencia">Transferencia</option>
                <option value="Efectivo">Efectivo</option>
                <option value="Tarjeta">Tarjeta</option>
              </select>
            </div>
          </div>

          <div class="form-group full-width" v-if="participantesSeleccionados.length > 0">
            <label>Comprobante Grupal *</label>
            <div class="file-upload-wrapper">
              <input type="file" @change="handleFileMasivo" id="file-masivo" accept=".pdf,.jpg,.jpeg,.png" required>
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
            <button 
              type="submit" 
              class="btn btn-primario" 
              :disabled="!formMasivo.file || !formMasivo.valor_pagado">
              <AppIcons name="check" :size="16" /> 
              Registrar Pago Masivo ({{ participantesSeleccionados.length }})
            </button>
            <button type="button" @click="limpiarFormularioMasivo" class="btn btn-secundario">
              <AppIcons name="x" :size="16" /> Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ✅ VISTA HISTÓRICO -->
    <div v-if="vistaActiva === 'historico'" class="vista-buscar">
      <div class="card-registro">
        <div class="card-header">
          <h3><AppIcons name="chart-bar" :size="24" /> Histórico de Pagos</h3>
          <p>Consulta y administra todos los pagos registrados</p>
        </div>

        <div class="filtros-avanzados">
          <div class="form-grid">
            <div class="form-group">
              <label>Buscar</label>
              <input 
                type="text" 
                v-model="filtroBusqueda" 
                placeholder="Nombre, RUT, Email..."
                class="search-input"
                @keyup.enter="buscar" 
              />
            </div>
            <div class="form-group">
              <label>Curso</label>
              <select v-model="filtroCurso">
                <option value="">Todos los cursos</option>
                <option v-for="curso in cursos" :key="curso.value" :value="curso.value">
                  {{ curso.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Grupo</label>
              <select v-model="filtroGrupo">
                <option value="">Todos los grupos</option>
                <option v-for="grupo in grupos" :key="grupo.value" :value="grupo.value">
                  {{ grupo.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Estado</label>
              <select v-model="filtroEstado">
                <option value="">Todos</option>
                <option value="Confirmado">Confirmado</option>
                <option value="Pendiente">Pendiente</option>
                <option value="Anulado">Anulado</option>
              </select>
            </div>
          </div>
          
          <div class="filtros-acciones">
            <button @click="aplicarFiltros" class="btn btn-primario">
              <AppIcons name="search" :size="16" /> Buscar
            </button>
            <button @click="limpiarFiltros" class="btn btn-secundario">
              <AppIcons name="refresh" :size="16" /> Limpiar Filtros
            </button>
            <button @click="exportarExcel" class="btn btn-success">
              <AppIcons name="download" :size="16" /> Exportar Excel
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
                <th>Grupo</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cargandoPagos">
                <td colspan="8" class="loading-cell">
                  <span class="spinner"></span> Cargando pagos...
                </td>
              </tr>
              <tr v-else-if="pagosFiltrados.length === 0">
                <td colspan="8" class="no-results">
                  No se encontraron pagos con los filtros aplicados
                </td>
              </tr>
              <tr v-else v-for="pago in paginatedPagos" :key="pago.id">
                <td><strong>{{ pago.nombre }}</strong></td>
                <td>{{ pago.rut }}</td>
                <td>{{ pago.curso }}</td>
                <td>
                  <span class="badge-grupo">{{ pago.grupo }}</span>
                </td>
                <td class="monto">${{ pago.monto.toLocaleString('es-CL') }}</td>
                <td>{{ formatearFecha(pago.fecha) }}</td>
                <td>
                  <span :class="['badge-estado', `estado-${pago.estado.toLowerCase()}`]">
                    {{ pago.estado }}
                  </span>
                </td>
                <td class="actions-cell">
                  <button @click="verDetalle(pago)" class="btn-icon btn-ver" title="Ver detalle">
                    <AppIcons name="eye" :size="18" />
                  </button>
                  <button @click="abrirModal(pago)" class="btn-icon btn-editar" title="Editar">
                    <AppIcons name="edit" :size="18" />
                  </button>
                  <button 
                    @click="abrirModalAnular(pago)" 
                    class="btn-icon btn-anular" 
                    title="Anular"
                    v-if="pago.estado !== 'Anulado'">
                    <AppIcons name="trash" :size="18" />
                  </button>
                  <button 
                    v-if="pago.comprobante"
                    @click="descargarComprobante(pago)" 
                    class="btn-icon" 
                    title="Descargar comprobante">
                    <AppIcons name="paperclip" :size="18" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1">
          <button @click="cambiarPagina(paginaActual - 1)" :disabled="paginaActual === 1" class="btn-pag">
            ← Anterior
          </button>
          <div class="pagination-info">
            Página {{ paginaActual }} de {{ totalPages }}
            <span class="separator">|</span>
            Mostrando {{ (paginaActual - 1) * itemsPorPagina + 1 }} - 
            {{ Math.min(paginaActual * itemsPorPagina, pagosFiltrados.length) }} de {{ pagosFiltrados.length }}
          </div>
          <button @click="cambiarPagina(paginaActual + 1)" :disabled="paginaActual === totalPages" class="btn-pag">
            Siguiente →
          </button>
        </div>
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
import cursosService from '@/services/cursosService.js'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'
import NotificationToast from '@/components/Reutilizables/NotificationToast.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

const vistaActiva = ref('registro')
const tipoRegistro = ref('individual') // 'individual' o 'masivo'

const cambiarVista = (vista) => {
  vistaActiva.value = vista
  if (vista === 'historico') {
    cargarPagos()
  }
}

// ==================== DATOS FICTICIOS ====================
const PERSONAS_FICTICIAS = [
  { id: 1, nombre: 'Juan Pérez González', rut: '12.345.678-9', email: 'juan.perez@scouts.cl', telefono: '+56 9 8765 4321', grupo: 'Biobío', direccion: 'Av. O\'Higgins 123, Concepción' },
  { id: 2, nombre: 'María González Silva', rut: '98.765.432-1', email: 'maria.gonzalez@scouts.cl', telefono: '+56 9 1234 5678', grupo: 'Ñuble', direccion: 'Calle Libertad 456, Chillán' },
  { id: 3, nombre: 'Pedro Silva Rojas', rut: '11.223.344-5', email: 'pedro.silva@scouts.cl', telefono: '+56 9 5555 6666', grupo: 'Biobío', direccion: 'Pasaje Los Pinos 789, Los Ángeles' },
  { id: 4, nombre: 'Ana Martínez López', rut: '55.667.788-9', email: 'ana.martinez@scouts.cl', telefono: '+56 9 7777 8888', grupo: 'Ñuble', direccion: 'Av. Brasil 321, Chillán' },
  { id: 5, nombre: 'Carlos Rojas Mendoza', rut: '99.887.766-5', email: 'carlos.rojas@scouts.cl', telefono: '+56 9 9999 0000', grupo: 'Biobío', direccion: 'Calle Principal 654, Talcahuano' },
  { id: 6, nombre: 'Daniela Torres Vargas', rut: '22.334.455-6', email: 'daniela.torres@scouts.cl', telefono: '+56 9 1111 2222', grupo: 'Ñuble', direccion: 'Av. Collín 147, Chillán' },
  { id: 7, nombre: 'Roberto Morales Castro', rut: '33.445.566-7', email: 'roberto.morales@scouts.cl', telefono: '+56 9 3333 4444', grupo: 'Biobío', direccion: 'Calle Freire 258, Concepción' }
]

const CURSOS_FICTICIOS = [
  { value: 1, label: 'Formación de Dirigentes Básico - FDB 2025' },
  { value: 2, label: 'Curso de Especialidad en Montañismo - CEM 2025' },
  { value: 3, label: 'Formación de Dirigentes Avanzado - FDA 2025' },
  { value: 4, label: 'Taller de Primeros Auxilios - TPA 2025' },
  { value: 5, label: 'Curso de Campismo y Vida al Aire Libre - CCVAL 2025' }
]

const GRUPOS_FICTICIOS = [
  { value: 1, label: 'Grupo Scout Biobío' },
  { value: 2, label: 'Grupo Scout Ñuble' },
  { value: 3, label: 'Grupo Scout Concepción' },
  { value: 4, label: 'Grupo Scout Los Ángeles' }
]

const PAGOS_FICTICIOS = [
  { id: 1, nombre: 'Juan Pérez González', rut: '12.345.678-9', curso: 'Formación de Dirigentes Básico', monto: 25000, estado: 'Pendiente', fecha: '2025-10-20', grupo: 'Biobío', comprobante: null, email: 'juan.perez@scouts.cl', telefono: '+56 9 8765 4321' },
  { id: 2, nombre: 'María González Silva', rut: '98.765.432-1', curso: 'Curso de Especialidad en Montañismo', monto: 30000, estado: 'Confirmado', fecha: '2025-10-18', grupo: 'Ñuble', comprobante: 'comprobante123.pdf', email: 'maria.gonzalez@scouts.cl', telefono: '+56 9 1234 5678' },
  { id: 3, nombre: 'Pedro Silva Rojas', rut: '11.223.344-5', curso: 'Formación de Dirigentes Avanzado', monto: 35000, estado: 'Confirmado', fecha: '2025-10-15', grupo: 'Biobío', comprobante: 'comprobante456.pdf', email: 'pedro.silva@scouts.cl', telefono: '+56 9 5555 6666' },
  { id: 4, nombre: 'Ana Martínez López', rut: '55.667.788-9', curso: 'Formación de Dirigentes Básico', monto: 25000, estado: 'Pendiente', fecha: '2025-10-22', grupo: 'Ñuble', comprobante: null, email: 'ana.martinez@scouts.cl', telefono: '+56 9 7777 8888' },
  { id: 5, nombre: 'Carlos Rojas Mendoza', rut: '99.887.766-5', curso: 'Taller de Primeros Auxilios', monto: 28000, estado: 'Confirmado', fecha: '2025-10-17', grupo: 'Biobío', comprobante: 'comprobante789.pdf', email: 'carlos.rojas@scouts.cl', telefono: '+56 9 9999 0000' }
]

// ==================== DATOS Y ESTADOS ====================
const pagos = ref([])
const personas = ref([])
const cursos = ref([])
const grupos = ref([])
const cargandoPagos = ref(false)
const alerta = ref({ mensaje: '', tipo: '' })
const showModal = ref(false)
const showModalAnular = ref(false)
const pagoSeleccionado = ref(null)

// Búsqueda de persona
const busquedaPersona = ref('')
const resultadosBusqueda = ref([])
const buscando = ref(false)

// Formulario Individual
const formIndividual = ref({
  personaId: null,
  nombre: '',
  rut: '',
  email: '',
  telefono: '',
  grupo: '',
  direccion: '',
  curso: '',
  valor_pagado: '',
  fecha_pago: '',
  metodo_pago: 'Transferencia',
  file: null
})

// Formulario Masivo
const formMasivo = ref({
  grupo: '',
  curso: '',
  valor_pagado: '',
  fecha_pago: '',
  metodo_pago: 'Transferencia',
  file: null
})

const participantesCargados = ref([])
const participantesSeleccionados = ref([])
const cargandoUsuarios = ref(false)

// Filtros histórico
const filtroBusqueda = ref('')
const filtroCurso = ref('')
const filtroGrupo = ref('')
const filtroEstado = ref('')
const terminoBuscado = ref('')
const paginaActual = ref(1)
const itemsPorPagina = ref(10)

// (Ordenamiento UI removido). Mantén el orden original de los datos o ajusta desde backend.

// ==================== CARGAR DATOS INICIALES ====================
onMounted(async () => {
  // Modo ficticios
  personas.value = PERSONAS_FICTICIAS
  cursos.value = CURSOS_FICTICIOS
  grupos.value = GRUPOS_FICTICIOS
  pagos.value = PAGOS_FICTICIOS

  /* MODO BACKEND: Descomentar para usar datos reales
  try {
    const [personasData, cursosData] = await Promise.all([
      personasService.listarBasic(),
      cursosService.listar()
    ])
    
    personas.value = personasData.map(p => ({
      id: p.id,
      nombre: p.nombre,
      rut: p.rut || 'Sin RUT',
      email: p.email || '',
      telefono: p.telefono || '',
      grupo: p.grupo || '',
      direccion: p.direccion || ''
    }))
    
    cursos.value = cursosData.map(c => ({
      value: c.id,
      label: `${c.nombre} - ${c.codigo}`
    }))
  } catch (error) {
    console.error('Error cargando datos:', error)
  }
  */
})

// ==================== BÚSQUEDA DE PERSONA ====================
const buscarPersona = () => {
  if (!busquedaPersona.value || busquedaPersona.value.length < 2) {
    resultadosBusqueda.value = []
    return
  }

  const query = busquedaPersona.value.toLowerCase()
  resultadosBusqueda.value = personas.value.filter(p =>
    p.nombre.toLowerCase().includes(query) ||
    p.rut.toLowerCase().includes(query) ||
    (p.grupo && p.grupo.toLowerCase().includes(query))
  ).slice(0, 5) // Máximo 5 resultados
}

const seleccionarPersona = (persona) => {
  formIndividual.value = {
    personaId: persona.id,
    nombre: persona.nombre,
    rut: persona.rut,
    email: persona.email,
    telefono: persona.telefono,
    grupo: persona.grupo,
    direccion: persona.direccion,
    curso: formIndividual.value.curso,
    valor_pagado: formIndividual.value.valor_pagado,
    fecha_pago: formIndividual.value.fecha_pago,
    metodo_pago: formIndividual.value.metodo_pago,
    file: formIndividual.value.file
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
    grupo: '',
    direccion: '',
    curso: '',
    valor_pagado: '',
    fecha_pago: '',
    metodo_pago: 'Transferencia',
    file: null
  }
  busquedaPersona.value = ''
  resultadosBusqueda.value = []
}

// ==================== REGISTRO INDIVIDUAL ====================
const handleFileIndividual = (e) => {
  formIndividual.value.file = e.target.files[0]
}

const registrarPagoIndividual = async () => {
  try {
    // TODO: Implementar con backend
    mostrarAlerta('Pago individual registrado correctamente', 'exito')
    limpiarFormularioIndividual()
  } catch (error) {
    console.error('Error al registrar pago:', error)
    mostrarAlerta('Error al registrar pago: ' + error.message, 'error')
  }
}

// ==================== REGISTRO MASIVO ====================
const handleFileMasivo = (e) => {
  formMasivo.value.file = e.target.files[0]
}

const filtrarParticipantesPorGrupo = () => {
  participantesCargados.value = []
  participantesSeleccionados.value = []
}

const cargarParticipantesParaMasivo = async () => {
  try {
    cargandoUsuarios.value = true
    
    // Filtrar personas por grupo seleccionado
    const grupoSeleccionado = grupos.value.find(g => g.value === formMasivo.value.grupo)
    const grupoNombre = grupoSeleccionado?.label || ''
    
    participantesCargados.value = personas.value.filter(p => 
      grupoNombre.toLowerCase().includes(p.grupo.toLowerCase())
    )
    
    mostrarAlerta(`${participantesCargados.value.length} participantes cargados`, 'exito')
  } catch (error) {
    console.error('Error al cargar participantes:', error)
    mostrarAlerta('Error al cargar participantes: ' + error.message, 'error')
  } finally {
    cargandoUsuarios.value = false
  }
}

const seleccionarTodos = () => {
  participantesSeleccionados.value = [...participantesCargados.value]
}

const deseleccionarTodos = () => {
  participantesSeleccionados.value = []
}

const limpiarFormularioMasivo = () => {
  formMasivo.value = {
    grupo: '',
    curso: '',
    valor_pagado: '',
    fecha_pago: '',
    metodo_pago: 'Transferencia',
    file: null
  }
  participantesCargados.value = []
  participantesSeleccionados.value = []
}

const registrarPagoMasivo = async () => {
  try {
    // TODO: Implementar con backend
    mostrarAlerta(`Pago masivo registrado para ${participantesSeleccionados.value.length} usuarios`, 'exito')
    limpiarFormularioMasivo()
  } catch (error) {
    console.error('Error al registrar pago masivo:', error)
    mostrarAlerta('Error al registrar pago masivo: ' + error.message, 'error')
  }
}

// ==================== HISTÓRICO ====================
async function cargarPagos() {
  try {
    cargandoPagos.value = true
    // Modo ficticios
    pagos.value = PAGOS_FICTICIOS
    
    /* MODO BACKEND: Descomentar para usar datos reales
    pagos.value = await pagosService.obtenerPagos()
    */
  } catch (error) {
    console.error('Error al cargar pagos:', error)
  } finally {
    cargandoPagos.value = false
  }
}

const aplicarFiltros = () => {
  terminoBuscado.value = filtroBusqueda.value
  paginaActual.value = 1
}

const limpiarFiltros = () => {
  filtroBusqueda.value = ''
  filtroCurso.value = ''
  filtroGrupo.value = ''
  filtroEstado.value = ''
  terminoBuscado.value = ''
  paginaActual.value = 1
}

const pagosFiltrados = computed(() => {
  let resultado = [...pagos.value]

  // Filtro de búsqueda
  if (terminoBuscado.value) {
    const q = terminoBuscado.value.toLowerCase()
    resultado = resultado.filter(p =>
      p.nombre?.toLowerCase().includes(q) ||
      p.rut?.toLowerCase().includes(q) ||
      p.email?.toLowerCase().includes(q)
    )
  }

  // Filtro de curso
  if (filtroCurso.value) {
    resultado = resultado.filter(p => p.curso?.includes(filtroCurso.value))
  }

  // Filtro de grupo
  if (filtroGrupo.value) {
    resultado = resultado.filter(p => p.grupo === filtroGrupo.value)
  }

  // Filtro de estado
  if (filtroEstado.value) {
    resultado = resultado.filter(p => p.estado === filtroEstado.value)
  }

  return resultado
})

const totalPages = computed(() => Math.ceil(pagosFiltrados.value.length / itemsPorPagina.value))

const paginatedPagos = computed(() => {
  const start = (paginaActual.value - 1) * itemsPorPagina.value
  return pagosFiltrados.value.slice(start, start + itemsPorPagina.value)
})

const calcularMontoTotal = computed(() => {
  return pagosFiltrados.value
    .filter(p => p.estado !== 'Anulado')
    .reduce((sum, p) => sum + p.monto, 0)
})

const cambiarPagina = (pagina) => {
  if (pagina >= 1 && pagina <= totalPages.value) {
    paginaActual.value = pagina
  }
}

// funciones de ordenamiento removidas

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  const d = new Date(fecha)
  return d.toLocaleDateString('es-CL', { day: '2-digit', month: 'short', year: 'numeric' })
}

// Modales
const abrirModal = (p) => {
  pagoSeleccionado.value = { ...p }
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
  pagoSeleccionado.value = null
}

const abrirModalAnular = (p) => {
  pagoSeleccionado.value = p
  showModalAnular.value = true
}

const cerrarModalAnular = () => {
  showModalAnular.value = false
  pagoSeleccionado.value = null
}

const guardarPago = async () => {
  try {
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

const confirmarAnulacion = async () => {
  try {
    const index = pagos.value.findIndex(p => p.id === pagoSeleccionado.value.id)
    if (index !== -1) {
      pagos.value[index].estado = 'Anulado'
    }
    mostrarAlerta('Pago anulado correctamente', 'exito')
    cerrarModalAnular()
  } catch (error) {
    console.error('Error al anular pago:', error)
    mostrarAlerta('Error al anular pago: ' + error.message, 'error')
  }
}

const verDetalle = (pago) => {
  console.log('Ver detalle:', pago)
  // TODO: Implementar modal de detalle
}

const descargarComprobante = (pago) => {
  console.log('Descargar comprobante:', pago.comprobante)
  // TODO: Implementar descarga
}

const exportarExcel = () => {
  console.log('Exportar a Excel')
  // TODO: Implementar exportación
  mostrarAlerta('Función de exportación próximamente', 'info')
}

function mostrarAlerta(mensaje, tipo) {
  alerta.value = { mensaje, tipo }
  setTimeout(() => (alerta.value = { mensaje: '', tipo: '' }), 3000)
}
</script>

<style scoped>
.pago-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ==================== ENCABEZADO ==================== */
.page-header {
  background: linear-gradient(135deg, var(--color-primary, #1e40af) 0%, #1e3a8a 100%);
  color: white;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 2rem;
  font-weight: 700;
}

.page-header p {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

/* ==================== NAVEGACIÓN PESTAÑAS ==================== */
.navegacion-vistas {
  display: flex;
  gap: 8px;
  border-bottom: 2px solid #e5e7eb;
  margin-bottom: 32px;
  background: white;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}

.navegacion-vistas button {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  position: relative;
}

.navegacion-vistas button .icon {
  font-size: 1.25rem;
}

.navegacion-vistas button:hover:not(.active) {
  background: #f9fafb;
  color: var(--color-primary, #1e40af);
}

.navegacion-vistas button.active {
  color: var(--color-primary, #1e40af);
  border-bottom-color: var(--color-primary, #1e40af);
  background: #eff6ff;
  font-weight: 600;
}

/* ==================== CARDS ==================== */
.vista-registrar,
.vista-buscar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card-registro {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.card-registro:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-header {
  background: linear-gradient(to right, #f9fafb, #ffffff);
  padding: 24px 32px;
  border-bottom: 2px solid #e5e7eb;
}

.card-header h3 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header p {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

/* ==================== SELECTOR DE TIPO DE REGISTRO ==================== */
.tipo-registro-selector {
  display: flex;
  gap: 12px;
  padding: 24px 32px;
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.tipo-btn {
  flex: 1;
  padding: 16px 24px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.tipo-btn:hover:not(.active) {
  background: #eff6ff;
  border-color: var(--color-primary, #1e40af);
  color: var(--color-primary, #1e40af);
}

.tipo-btn.active {
  background: var(--color-primary, #1e40af);
  border-color: var(--color-primary, #1e40af);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(30, 64, 175, 0.2);
}

/* ==================== FORMULARIOS ==================== */
form {
  padding: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
  color: #111827;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--color-primary, #1e40af);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.readonly-input {
  background: #f9fafb !important;
  cursor: not-allowed;
  color: #6b7280;
}

.input-with-prefix {
  display: flex;
  align-items: center;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.input-with-prefix:focus-within {
  border-color: var(--color-primary, #1e40af);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.input-with-prefix .prefix {
  background: #f3f4f6;
  padding: 12px 16px;
  font-weight: 600;
  color: #6b7280;
  border-right: 2px solid #e5e7eb;
}

.input-with-prefix input {
  flex: 1;
  border: none;
  padding: 12px 16px;
  font-size: 1rem;
}

.input-with-prefix input:focus {
  outline: none;
  box-shadow: none;
}

/* ==================== BÚSQUEDA ==================== */
.search-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #e5e7eb;
}

.search-group {
  position: relative;
}

.search-input-wrapper {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 14px 48px 14px 16px !important;
  font-size: 1.1rem !important;
  border: 2px solid #e5e7eb !important;
  border-radius: 12px !important;
}

.search-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  pointer-events: none;
}
/* remove default svg right margin inside the positioned icon */
.search-icon svg { margin-right: 0; }

.resultados-busqueda {
  margin-top: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  max-height: 300px;
  overflow-y: auto;
}

.resultado-item {
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resultado-item:last-child {
  border-bottom: none;
}

.resultado-item:hover {
  background: #eff6ff;
}

.resultado-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.resultado-info strong {
  color: #111827;
  font-size: 1rem;
}

.resultado-info .rut {
  color: #6b7280;
  font-size: 0.9rem;
}

.resultado-extra .grupo {
  background: #dbeafe;
  color: #1e40af;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.no-resultados {
  padding: 20px;
  text-align: center;
  color: #9ca3af;
  font-style: italic;
}

/* ==================== DIVIDER ==================== */
.form-divider {
  margin: 32px 0 24px 0;
  padding-top: 24px;
  border-top: 2px solid #e5e7eb;
}

.form-divider h4 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ==================== FILE UPLOAD ==================== */
.file-upload-wrapper input[type="file"] {
  display: none;
}

.file-upload-label {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f9fafb;
  color: #6b7280;
  font-weight: 500;
}

.file-upload-label:hover {
  border-color: var(--color-primary, #1e40af);
  background: #eff6ff;
  color: var(--color-primary, #1e40af);
}

.file-upload-label .icon {
  font-size: 1.5rem;
}

/* ==================== PARTICIPANTES MASIVO ==================== */
.participantes-section {
  margin-top: 24px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
}

.participantes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e5e7eb;
}

.participantes-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #111827;
}

.seleccion-acciones {
  display: flex;
  gap: 12px;
}

.btn-link {
  background: none;
  border: none;
  color: var(--color-primary, #1e40af);
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: underline;
  padding: 4px 8px;
}

.btn-link:hover {
  color: #1e3a8a;
}

.participantes-lista {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.participante-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.participante-item:hover {
  border-color: var(--color-primary, #1e40af);
  background: #eff6ff;
}

.checkbox-styled {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.participante-label {
  flex: 1;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;
}

.participante-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.participante-info strong {
  color: #111827;
  font-size: 0.95rem;
}

.participante-info .rut {
  color: #6b7280;
  font-size: 0.85rem;
}

.participante-label .email {
  color: #6b7280;
  font-size: 0.85rem;
}

/* ==================== RESUMEN MASIVO ==================== */
.resumen-masivo {
  margin-top: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 8px;
  border: 2px solid #93c5fd;
}

.resumen-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  color: #1e40af;
}

.resumen-item span {
  font-size: 1rem;
}

.resumen-item strong {
  font-size: 1.1rem;
  font-weight: 600;
}

.resumen-item.total {
  margin-top: 12px;
  padding-top: 16px;
  border-top: 2px solid #93c5fd;
  font-size: 1.2rem;
}

.resumen-item.total strong {
  font-size: 1.5rem;
  color: #1e3a8a;
}

/* ==================== BOTONES ==================== */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  justify-content: flex-start;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn .icon {
  font-size: 1.1rem;
}

.btn-primario {
  background: var(--color-primary, #1e40af);
  color: white;
}

.btn-primario:hover:not(:disabled) {
  background: #1e3a8a;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.btn-secundario {
  background: #f3f4f6;
  color: #374151;
}

.btn-secundario:hover {
  background: #e5e7eb;
}

.btn-info {
  background: #0ea5e9;
  color: white;
  width: 100%;
  justify-content: center;
  margin-bottom: 16px;
}

.btn-info:hover:not(:disabled) {
  background: #0284c7;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover {
  background: #059669;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ==================== FILTROS HISTÓRICO ==================== */
.filtros-avanzados {
  margin-bottom: 24px;
}

.filtros-acciones {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

/* ==================== ESTADÍSTICAS ==================== */
.estadisticas-resumen {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
}

.stat-value.confirmado {
  color: #10b981;
}

.stat-value.pendiente {
  color: #f59e0b;
}

/* ==================== TABLA ==================== */
.tabla-pagos {
  overflow-x: auto;
  margin-top: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.tabla-pagos table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  table-layout: auto; /* deja que las columnas se ajusten al contenido más largo */
  min-width: 1300px; /* activa scroll horizontal cuando el viewport es menor y asegura ver la última columna */
}

.tabla-pagos thead {
  background: linear-gradient(to right, #1e40af, #1e3a8a);
  color: white;
}

.tabla-pagos th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.tabla-pagos td {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
}

/* Column alignment + overflow behavior */
.tabla-pagos th, .tabla-pagos td {
  vertical-align: middle;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tabla-pagos th:nth-child(2), .tabla-pagos td:nth-child(2) { /* RUT */
  white-space: nowrap;
}
.tabla-pagos th:nth-child(5), .tabla-pagos td:nth-child(5) { /* Monto */
  text-align: right;
}
.tabla-pagos th:nth-child(6), .tabla-pagos td:nth-child(6) { /* Fecha */
  white-space: nowrap;
}
.tabla-pagos th:nth-child(7), .tabla-pagos td:nth-child(7) { /* Estado */
  text-align: center;
}
.tabla-pagos th:nth-child(8), .tabla-pagos td:nth-child(8) { /* Acciones (4 íconos) */
  width: 200px; /* espacio fijo para 4 íconos */
  white-space: nowrap;
  text-align: left;
}

.tabla-pagos tbody tr {
  transition: all 0.2s ease;
}

.tabla-pagos tbody tr:hover {
  background: #f9fafb;
}

.tabla-pagos .monto {
  font-weight: 600;
  color: #059669;
}

.badge-grupo {
  background: #dbeafe;
  color: #1e40af;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge-estado {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.estado-confirmado {
  background: #d1fae5;
  color: #065f46;
}

.estado-pendiente {
  background: #fef3c7;
  color: #92400e;
}

.estado-anulado {
  background: #fee2e2;
  color: #991b1b;
}

.actions-cell {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: flex-start; /* mantiene alineación consistente entre filas */
}

.btn-icon {
  border: none;
  font-size: 0; /* Evita espacio extra con inline SVGs */
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  color: white;
  font-weight: 500;
}

/* Botón Ver - Azul */
.btn-icon.btn-ver {
  background: #2563eb;
}

.btn-icon.btn-ver:hover {
  background: #1d4ed8;
  transform: scale(1.05);
}

/* Botón Editar - Amarillo/Ámbar */
.btn-icon.btn-editar {
  background: #f59e0b;
}

.btn-icon.btn-editar:hover {
  background: #d97706;
  transform: scale(1.05);
}

/* Botón Anular - Rojo */
.btn-icon.btn-anular {
  background: #dc2626;
}

.btn-icon.btn-anular:hover {
  background: #b91c1c;
  transform: scale(1.05);
}

/* Botón Descargar - Gris (neutral) */
.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular) {
  background: #6b7280;
}

.btn-icon:not(.btn-ver):not(.btn-editar):not(.btn-anular):hover {
  background: #4b5563;
  transform: scale(1.05);
}

/* Evita margen-right del icono dentro de botones de acción */
.actions-cell svg {
  margin-right: 0 !important;
  filter: brightness(0) invert(1); /* Fuerza iconos blancos */
}

/* ==================== AJUSTES VISTA HISTÓRICO ==================== */
.vista-buscar .actions-cell {
  min-width: 200px; /* 4 íconos sin cortar */
}

.loading-cell,
.no-results {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  font-size: 1rem;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 3px solid #e5e7eb;
  border-top-color: var(--color-primary, #1e40af);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ==================== PAGINACIÓN ==================== */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding: 16px 20px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.pagination-info {
  color: #6b7280;
  font-size: 0.95rem;
}

.pagination-info .separator {
  margin: 0 8px;
  color: #d1d5db;
}

.btn-pag {
  padding: 8px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s ease;
}

.btn-pag:hover:not(:disabled) {
  background: var(--color-primary, #1e40af);
  color: white;
  border-color: var(--color-primary, #1e40af);
}

.btn-pag:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* (Estilos de headers ordenables removidos) */

/* ==================== MODALES ==================== */
.modal-editar-pago,
.modal-confirmar {
  padding: 32px;
  max-width: 500px;
}

.modal-editar-pago h3,
.modal-confirmar h3 {
  margin: 0 0 24px 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.modal-confirmar p {
  margin-bottom: 24px;
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .pago-view {
    padding: 16px;
  }

  .page-header {
    padding: 24px;
  }

  .page-header h2 {
    font-size: 1.5rem;
  }

  form {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .navegacion-vistas button {
    font-size: 0.9rem;
    padding: 12px 16px;
  }

  .tabla-pagos {
    font-size: 0.85rem;
  }

  .tabla-pagos th,
  .tabla-pagos td {
    padding: 12px 8px;
  }

  .estadisticas-resumen {
    grid-template-columns: 1fr 1fr;
  }

  .pagination {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
