<template>
  <div class="gestion-pagos">
    <!-- Encabezado -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
    </header>

    <!-- Tabs principales -->
    <div class="tabs">
      <button :class="{ active: tab === 'individual' }" @click="tab = 'individual'">
        Registro Individual
      </button>
      <button :class="{ active: tab === 'masivo' }" @click="tab = 'masivo'">
        Registro Masivo
      </button>
      <button :class="{ active: tab === 'historico' }" @click="tab = 'historico'">
        Histórico
      </button>
    </div>

    <!-- ===================== SECCIÓN: REGISTRO INDIVIDUAL ===================== -->
    <div v-if="tab === 'individual'" class="card card-registro">
      <section class="panel panel-box">
        <div class="panel-title">
          <h3>Registro Individual de Pagos</h3>
          <p>Busca un participante, selecciona el curso y registra el pago.</p>
        </div>

        <!-- Buscar persona -->
        <div class="row-buscar">
          <div class="buscar-input">
            <InputBase id="buscar-persona-input"
              v-model="buscarPersonaQ"
              placeholder="EJ: 12.345.678-9 O JUAN PÉREZ"
            />
          </div>
        </div>

        <div v-if="buscandoPersonas" class="estado-carga">
          <div class="spinner"></div> Buscando personas...
        </div>

        <div v-if="personasEncontradas.length" class="resultados">
          <div
            v-for="p in personasEncontradas"
            :key="p.id"
            class="resultado"
            @click="seleccionarPersona(p)"
          >
            <div class="resultado-left">
              <strong>{{ p.nombre }}</strong>
              <span class="muted">{{ p.rut }} · {{ p.email }}</span>
            </div>
            <BaseButton size="sm" variant="secondary" class="btn-action">
              Elegir
            </BaseButton>
          </div>
        </div>

        <!-- Form individual -->
        <div class="grid grid-individual">
          <div class="col">
            <label>Nombre</label>
            <InputBase v-model="formInd.nombre" readonly />
          </div>
          <div class="col">
            <label>RUT</label>
            <InputBase v-model="formInd.rut" readonly />
          </div>
          <div class="col">
            <label>Email</label>
            <InputBase v-model="formInd.email" readonly />
          </div>

          <div class="col">
            <label>Curso / Capacitación *</label>
            <BaseSelect
              v-model="formInd.CUR_ID"
              :options="cursoOptions"
              placeholder="Seleccione curso"
            />
          </div>

          <div class="col half">
            <label>Valor Pagado *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input
                type="number"
                min="0"
                step="100"
                v-model.number="formInd.PAP_MONTO"
              />
            </div>
          </div>

          <div class="col half">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formInd.PAP_FECHA_PAGO" />
          </div>
 
          <div class="col span-2">
            <label>Comentario / Observación</label>
            <textarea
              class="comentario-input"
              v-model="formInd.observacion"
              maxlength="200"
              placeholder="Detalle del pago, referencia de transferencia, etc."
            />
          </div>

          <div class="col full comprobante-wrapper">
            <label>Comprobante de transferencia *</label>
            <input
              ref="fileIndRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileInd"
            />
          </div>
        </div>

        <div class="acciones center acciones-individual">
          <BaseButton
            variant="success"
            class="btn-standard"
            :disabled="!puedeRegistrarIndividual"
            @click="registrarPagoIndividual"
          >
            <AppIcons name="save" :size="16" /> Registrar Pago
          </BaseButton>
          <BaseButton variant="secondary" class="btn-standard" @click="limpiarIndividual">
            <AppIcons name="x" :size="16" /> Limpiar
          </BaseButton>
        </div>
      </section>
    </div>

    <!-- ===================== SECCIÓN: REGISTRO MASIVO ===================== -->
    <div v-else-if="tab === 'masivo'" class="card card-registro">
      <section class="panel panel-box">
        <div class="panel-title">
          <h3>Registro Masivo de Pagos</h3>
          <p>Selecciona grupo y curso, participantes y registra pagos masivos.</p>
        </div>

        <div class="grid grid-masivo">
          <div class="col">
            <label>Grupo *</label>
            <BaseSelect
              v-model="formMasivo.GRU_ID"
              :options="grupoOptions"
              placeholder="Seleccione grupo"
            />
          </div>
          <div class="col">
            <label>Curso / Capacitación *</label>
            <BaseSelect
              v-model="formMasivo.CUR_ID"
              :options="cursoOptions"
              placeholder="Seleccione curso"
            />
          </div>
          <div class="col auto">
            <label class="invisible">Cargar</label>
            <BaseButton class="btn-standard"
              variant="primary"
              :disabled="!formMasivo.GRU_ID || !formMasivo.CUR_ID || cargandoParticipantes"
              @click="cargarParticipantes"
            >
              <AppIcons name="users" :size="16" /> {{ cargandoParticipantes ? 'Cargando...' : 'Cargar' }}
            </BaseButton>
          </div>
        </div>

        <div v-if="participantes.length" class="lista">
          <div class="lista-header">
            <h5>Participantes ({{ participantes.length }})</h5>
            <div class="acciones">
              <BaseButton size="sm" variant="secondary" @click="selectAll">
                Seleccionar todos
              </BaseButton>
              <BaseButton size="sm" variant="secondary" @click="unselectAll">
                Deseleccionar
              </BaseButton>
            </div>
          </div>

          <div class="lista-items">
            <label v-for="u in participantes" :key="u.id" class="item">
              <input type="checkbox" :value="u.id" v-model="seleccionados" />
              <div class="info">
                <strong>{{ u.nombre }}</strong>
                <span class="muted">{{ u.rut }} · {{ u.email }}</span>
              </div>
            </label>
          </div>
        </div>

        <div v-if="seleccionados.length" class="grid grid-masivo">
          <div class="col">
            <label>Valor por Persona *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input
                type="number"
                min="0"
                step="100"
                v-model.number="formMasivo.PAP_MONTO"
              />
            </div>
          </div>
          <div class="col">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formMasivo.PAP_FECHA_PAGO" />
          </div>
          <div class="col full">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              class="comentario-input"
              v-model="formMasivo.observacion"
              maxlength="200"
              placeholder="Detalle general del pago; se aplicará a todos."
            />
          </div>
          <div class="col full comprobante-wrapper">
            <label>Comprobante de transferencia grupal (obligatorio)</label>
            <input
              ref="fileMasivoRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileMasivo"
            />
          </div>
        </div>

        <div
          class="resumen"
          v-if="seleccionados.length && formMasivo.PAP_MONTO"
        >
          <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
          <div>Valor por persona: <strong>${{ formMasivo.PAP_MONTO.toLocaleString('es-CL') }}</strong></div>
          <div class="total">
            Total:
            <strong>
              ${{
                (seleccionados.length * formMasivo.PAP_MONTO).toLocaleString('es-CL')
              }}
            </strong>
          </div>
        </div>

        <div class="acciones center acciones-individual" v-if="seleccionados.length">
          <BaseButton
            variant="success"
            class="btn-standard"
            :disabled="!puedeRegistrarMasivo"
            @click="registrarPagoMasivo"
          >
            <AppIcons name="save" :size="16" /> Registrar Pago ({{ seleccionados.length }})
          </BaseButton>
          <BaseButton variant="secondary" class="btn-standard" @click="limpiarMasivo">
            <AppIcons name="x" :size="16" /> Limpiar
          </BaseButton>
        </div>
      </section>
    </div>

    <!-- ===================== SECCIÓN: HISTÓRICO DE PAGOS ===================== -->
    <div v-else-if="tab === 'historico'" class="card card-historico">
      <!-- Filtros compactos -->
      <div class="filtros filtros-historico">
        <InputBase class="filtro-busqueda filtro-corto"
          v-model="filtroQ"
          placeholder="NOMBRE / RUT / EMAIL"
        />
        <BaseSelect
          class="filtro-corto"
          v-model="filtroCurso"
          :options="[{ value: '', label: 'Todos los cursos' }, ...cursoOptions]"
        />
        <BaseSelect
          class="filtro-corto"
          v-model="filtroGrupo"
          :options="[{ value: '', label: 'Todos los grupos' }, ...grupoOptions]"
        />
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <BaseButton class="btn-standard" variant="secondary" @click="exportarCSV">
          <AppIcons name="download" :size="16" />
          Exportar CSV
        </BaseButton>

        <BaseButton
          class="btn-standard"
          variant="info"
          :disabled="!seleccionadosHistorico.length"
          @click="marcarEnviado"
        >
          <AppIcons name="check" :size="16" /> Marcar Enviado
        </BaseButton>

        <BaseButton
          class="btn-standard"
          variant="primary"
          :disabled="!seleccionadosHistorico.length"
          @click="enviarPorCorreo"
        >
          <AppIcons name="send" :size="16" /> Enviar por correo
        </BaseButton>
      </div>

      <!-- Estado -->
      <div v-if="cargandoPagos" class="estado-carga">
        <div class="spinner"></div> Cargando pagos...
      </div>
      <div v-if="errorPagos" class="mensaje-error">
        {{ errorPagos }}
        <div>
          <BaseButton variant="primary" @click="cargarPagos">Reintentar</BaseButton>
        </div>
      </div>

      <!-- Tabla -->
      <div class="table-wrapper" v-if="!cargandoPagos && !errorPagos">
        <table>
          <thead>
            <tr>
              <th style="width: 32px;">
                <input
                  type="checkbox"
                  :checked="allChecked"
                  @change="toggleSelectAllHistorico($event.target.checked)"
                />
              </th>
              <th>Nombre</th>
              <th>RUT</th>
              <th>Curso</th>
              <th>Monto</th>
              <th>Fecha</th>
              <th>Método</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in pagos" :key="p.id">
              <td>
                <input
                  type="checkbox"
                  :value="p.id"
                  v-model="seleccionadosHistorico"
                />
              </td>
              <td data-label="Nombre" class="texto-largo" :title="p.persona_nombre"><strong>{{ p.persona_nombre }}</strong></td>
              <td data-label="RUT">{{ p.persona_rut }}</td>
              <td data-label="Curso">{{ cursoLabel(p.CUR_ID) }}</td>
              <td data-label="Monto">${{ (p.PAP_MONTO)?.toLocaleString('es-CL') }}</td>
              <td data-label="Fecha">{{ dateCL(p.PAP_FECHA_PAGO) }}</td>
              <td data-label="Método">{{ p.MET_DESCRIPCION || 'Transferencia' }}</td>
              <td data-label="Acciones" class="acciones-buttons">
                <BaseButton class="btn-action"
                  size="sm"
                  variant="info"
                  @click="verDetalle(p)"
                >
                  <AppIcons name="eye" :size="14" /> Ver
                </BaseButton>
                <BaseButton class="btn-action"
                  size="sm"
                  variant="secondary"
                  @click="abrirEditar(p)"
                >
                  <AppIcons name="edit" :size="14" /> Editar
                </BaseButton>
                <BaseButton class="btn-action"
                  size="sm"
                  variant="secondary"
                  @click="abrirTransferir(p)"
                >
                  <AppIcons name="share" :size="14" /> Transferir
                </BaseButton>
                <BaseButton class="btn-action"
                  size="sm"
                  variant="danger"
                  @click="abrirAnular(p)"
                >
                  <AppIcons name="trash" :size="14" /> Anular
                </BaseButton>
                <BaseButton class="btn-action"
                  v-if="p.PAP_RUTA_COMPROBANTE"
                  size="sm"
                  variant="info"
                  @click="descargarComprobante(p)"
                >
                  <AppIcons name="download" :size="14" /> Comprobante
                </BaseButton>
              </td>
            </tr>
            <tr v-if="!pagos.length">
              <td colspan="8" class="placeholder">
                No hay pagos para mostrar
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- ===================== MODALES ===================== -->
    <!-- Modal Editar -->
    <BaseModal v-model="modalEditar" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <div class="header-actions">
              <BaseButton
                class="btn-save"
                variant="primary"
                @click="guardarEdicion"
                :disabled="guardando"
              >
                <AppIcons :name="guardando ? 'clock' : 'save'" :size="16" />
                {{ guardando ? 'Guardando...' : 'Guardar' }}
              </BaseButton>
            </div>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <InputBase v-model="pagoEdit.nombre" readonly />
            </div>
            <div class="row">
              <label>RUT</label>
              <InputBase v-model="pagoEdit.rut" readonly />
            </div>
            <div class="row">
              <label>Curso</label>
              <BaseSelect v-model="pagoEdit.curso" :options="cursoOptions" />
            </div>
            <div class="row">
              <label>Monto</label>
              <InputBase type="number" v-model.number="pagoEdit.monto" />
            </div>
            <div class="row">
              <label>Fecha</label>
              <InputBase type="date" v-model="pagoEdit.fecha" />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <InputBase v-model="pagoEdit.observacion" />
            </div>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Anular -->
    <BaseModal v-model="modalAnular" title="Confirmar Anulación">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">⚠️</div>
          <p>¿Anular pago de <strong>{{ pagoAnular?.persona_nombre }}</strong>?</p>
          <div class="confirm-actions modal-actions">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="modalAnular = false"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="danger"
              class="btn-modal"
              @click="confirmarAnulacion"
            >
              <AppIcons name="trash" :size="16" /> Anular
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Transferir -->
    <BaseModal v-model="modalTransferir" title="Transferir Pago">
      <template #default>
        <div class="modal-transfer">
          <h3>Transferir pago de {{ pagoTransferir?.persona_nombre }}</h3>
          <p class="muted">Busca al participante al que deseas transferir el pago.</p>

          <!-- Buscador de personas para transferencia -->
          <div class="row-buscar">
            <div class="buscar-input">
              <InputBase
                v-model="transferForm.q"
                placeholder="Buscar por RUT o nombre..."
                @keydown.enter.prevent="buscarPersonaParaTransferir"
              />
            </div>
            <BaseButton variant="primary" @click="buscarPersonaParaTransferir">Buscar</BaseButton>
          </div>
          <div v-if="buscandoPersonasTransferir" class="estado-carga">Buscando...</div>
          <div v-if="personasEncontradasTransferir.length" class="resultados">
             <!-- Resultados de la búsqueda -->
          </div>

          <div class="form-fields-grid">
            <div class="row">
              <label>RUT nuevo participante</label>
              <input v-model="transferForm.rut" />
            </div>
            <div class="row">
              <label>Email nuevo participante</label>
              <input v-model="transferForm.email" />
            </div>
            <div class="row">
              <label>Tipo de devolución</label>
              <select v-model="transferForm.tipo">
                <option value="total">Devolución / Transferencia Total</option>
                <option value="parcial">Devolución / Transferencia Parcial</option>
              </select>
            </div>
            <div class="row" v-if="transferForm.tipo === 'parcial'">
              <label>Monto a transferir</label>
              <input
                type="number"
                min="0"
                v-model.number="transferForm.monto_parcial"
              />
            </div>
          </div>

          <div class="confirm-actions modal-actions">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="modalTransferir = false"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="primary"
              class="btn-modal"
              @click="confirmarTransferencia"
            >
              <AppIcons name="check" :size="16" /> Confirmar
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import AppIcons from '@/components/icons/AppIcons.vue'
import InputBase from '@/components/InputBase.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import pagosService from '@/services/pagosService.js'
import personasService from '@/services/personasService.js'
import cursosService from '@/services/cursosService.js'
import mantenedoresService from '@/services/mantenedoresService.js'
import { format, parseISO } from 'date-fns'


function hoyISO () {
  const d = new Date()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day}`
}
function dateCL (f) {
  if (!f) return '-';
  try {
    const date = typeof f === 'string' ? parseISO(f) : f;
    return format(date, 'dd-MM-yyyy');
  } catch (e) {
    return f;
  }
}

export default {
  name: 'PagosView',
  components: { InputBase, BaseSelect, BaseButton, BaseModal, AppIcons },
  data () {
    return {
      tab: 'individual',

      cursoOptions: [],
      grupoOptions: [],

      buscarPersonaQ: '',
      buscandoPersonas: false,
      personasEncontradas: [],
      formInd: {
        personaId: null,
        nombre: '',
        rut: '',
        email: '',
        CUR_ID: '',
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      },
 
      formMasivo: {
        GRU_ID: '',
        CUR_ID: '',
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      },
      participantes: [],
      seleccionados: [],
      cargandoParticipantes: false,

      filtroQ: '',
      filtroCurso: '',
      filtroGrupo: '',
      pagos: [],
      cargandoPagos: false,
      errorPagos: null,
      seleccionadosHistorico: [],

      modalEditar: false,
      pagoEdit: {},
      guardando: false,

      modalAnular: false,
      pagoAnular: null,

      modalTransferir: false,
      pagoTransferir: null,
      buscandoPersonasTransferir: false,
      personasEncontradasTransferir: [],
      transferForm: {
        q: '',
        personaId: null,
        nombre: '',
        rut: '',
        email: '',
        tipo: 'total',
        monto_parcial: null
      }
    }
  },
  watch: {
    /**
     * Observa cambios en el campo de búsqueda de persona y ejecuta la búsqueda
     * con un debounce para no sobrecargar la API con cada pulsación de tecla.
     * @param {string} newValue El nuevo valor del campo de búsqueda.
     */
    buscarPersonaQ(newValue) {
      this.debounceBuscarPersonas(newValue);
    },
    /**
     * Observa cambios en la pestaña activa y recarga los pagos si se cambia a 'historico'.
     */
    tab(newTab, oldTab) {
      if (newTab === 'historico' && oldTab !== 'historico') {
        this.cargarPagos(true); // Forzar recarga al cambiar a la pestaña de histórico
      }
    }
  },
  created() {
    // Crear la función con debounce una vez que el componente es creado
    this.debounceBuscarPersonas = this.debounce(this.buscarPersonas, 400);
  },
  computed: {
    allChecked () {
      return (
        this.pagos.length > 0 &&
        this.seleccionadosHistorico.length === this.pagos.length
      )
    },
    puedeRegistrarIndividual () {
      return (
        this.formInd.personaId &&
        this.formInd.CUR_ID &&
        this.formInd.PAP_MONTO > 0 &&
        this.formInd.PAP_FECHA_PAGO &&
        this.formInd.file
      )
    },
    puedeRegistrarMasivo () {
      return (
        this.seleccionados.length &&
        this.formMasivo.CUR_ID &&
        this.formMasivo.GRU_ID &&
        this.formMasivo.PAP_MONTO > 0 &&
        this.formMasivo.PAP_FECHA_PAGO &&
        this.formMasivo.file
      )
    }
  },
  methods: {
    // ===================================================================
    // MÉTODOS DE CARGA DE DATOS Y CATÁLOGOS
    // ===================================================================
    /**
     * Carga los catálogos de cursos y grupos desde la API.
     * Estos datos se usan en los selectores de los formularios.
     */
    async cargarCatalogos () {
      try {
        const cursosResponse = await cursosService.cursos.list()
        const cursos = Array.isArray(cursosResponse)
          ? cursosResponse
          : cursosResponse.results || []
        this.cursoOptions = cursos.map(c => ({
          value: c.CUR_ID,
          label: c.CUR_DESCRIPCION || `Curso ${c.CUR_ID}`
        }))
      } catch (e) {
        console.error('Error cargando cursos:', e)
        this.cursoOptions = []
      }

      try {
        const gruposResponse = await mantenedoresService.grupo.list()
        const grupos = Array.isArray(gruposResponse) ? gruposResponse : (gruposResponse.results || [])
        this.grupoOptions = grupos.map(g => ({
          value: g.GRU_ID,
          label: g.GRU_DESCRIPCION || `Grupo ${g.GRU_ID}`
        }))
      } catch (e) {
        console.error('Error cargando grupos:', e)
        this.grupoOptions = []
      }
    },

    // ===================================================================
    // MÉTODOS PARA REGISTRO INDIVIDUAL
    // ===================================================================
    /**
     * Busca personas en la API según el texto ingresado.
     * Se activa al escribir en el campo de búsqueda (con debounce).
     * @param {string} q - El término de búsqueda.
     */
    async buscarPersonas (q) {
      if (!q) {
        this.personasEncontradas = []
        return
      }
      this.buscandoPersonas = true
      try {
        const response = await personasService.personas.list({ search: q })
        const arr = Array.isArray(response) ? response : (response.results || [])
        this.personasEncontradas = arr.map(p => ({
          id: p.PER_ID,
          nombre: `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: (p.PER_RUN && p.PER_DV) ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
          email: p.PER_MAIL || ''
        }))
      } catch (e) {
        console.error('Error buscando personas:', e)
        this.personasEncontradas = []
      } finally {
        this.buscandoPersonas = false
      }
    },
    /**
     * Selecciona una persona de la lista de resultados de búsqueda
     * y rellena el formulario de registro individual con sus datos.
     * @param {object} p - El objeto de la persona seleccionada.
     */
    seleccionarPersona (p) {
      this.formInd.personaId = p.id
      this.formInd.nombre = p.nombre
      this.formInd.rut = p.rut
      this.formInd.email = p.email
      this.personasEncontradas = []
      this.buscarPersonaQ = p.nombre
    },
    /**
     * Maneja la selección de un archivo de comprobante para el registro individual.
     * @param {Event} e - El evento del input de archivo.
     */
    onFileInd (e) {
      this.formInd.file = e.target.files?.[0] || null
    },
    /**
     * Limpia y resetea todos los campos del formulario de registro individual.
     */
    limpiarIndividual () {
      this.formInd = {
        personaId: null,
        nombre: '',
        rut: '',
        email: '',
        CUR_ID: '',
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      }
      this.buscarPersonaQ = ''
      this.personasEncontradas = []
    },
    /**
     * Envía el formulario de pago individual a la API.
     * Construye un FormData con los datos y el archivo del comprobante.
     */
    async registrarPagoIndividual () {
      try {
        const fd = new FormData()
        fd.append('PER_ID', this.formInd.personaId)
        fd.append('CUR_ID', this.formInd.CUR_ID)
        fd.append('PAP_MONTO', this.formInd.PAP_MONTO)
        fd.append('PAP_FECHA_PAGO', this.formInd.PAP_FECHA_PAGO)
        if (this.formInd.observacion) {
          fd.append('PAP_OBSERVACION', this.formInd.observacion)
        }
        fd.append('comprobante', this.formInd.file)
        fd.append('MET_ID', 1) // Asumiendo 1 para Transferencia
        await pagosService.pagos.create(fd)

        alert('Pago individual registrado correctamente')
        this.limpiarIndividual()
        this.cargarPagos()
      } catch (e) {
        alert('Error registrando pago individual')
      }
    },

    // ===================================================================
    // MÉTODOS PARA REGISTRO MASIVO
    // ===================================================================
    /**
     * Maneja la selección de un archivo de comprobante para el registro masivo.
     * @param {Event} e - El evento del input de archivo.
     */
    onFileMasivo (e) {
      this.formMasivo.file = e.target.files?.[0] || null
    },
    /**
     * Carga la lista de participantes de un grupo y curso específicos
     * para el registro de pago masivo.
     */
    async cargarParticipantes () {
      this.cargandoParticipantes = true
      this.participantes = []
      try {
        const response = await personasService.personas.list({
          GRU_ID: this.formMasivo.GRU_ID
        })
        const arr = Array.isArray(response) ? response : (response.results || [])
        this.participantes = arr.map(p => ({
          id: p.PER_ID,
          nombre: `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: (p.PER_RUN && p.PER_DV) ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
          email: p.PER_MAIL || ''
        }))
        this.seleccionados = []
      } catch (e) {
        this.participantes = []
      } finally {
        this.cargandoParticipantes = false
      }
    },
    /**
     * Selecciona a todos los participantes de la lista para el pago masivo.
     */
    selectAll () {
      this.seleccionados = this.participantes.map(u => u.id)
    },
    /**
     * Deselecciona a todos los participantes de la lista.
     */
    unselectAll () {
      this.seleccionados = []
    },
    /**
     * Limpia y resetea todos los campos del formulario de registro masivo.
     */
    limpiarMasivo () {
      this.formMasivo = {
        GRU_ID: '',
        CUR_ID: '',
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      }
      this.participantes = []
      this.seleccionados = []
    },
    /**
     * Envía el formulario de pago masivo a la API.
     * Construye un FormData con los datos y el archivo del comprobante.
     */
    async registrarPagoMasivo () {
      try {
        const fd = new FormData()
        fd.append('GRU_ID', this.formMasivo.GRU_ID)
        fd.append('CUR_ID', this.formMasivo.CUR_ID)
        fd.append('PAP_MONTO', this.formMasivo.PAP_MONTO)
        fd.append('PAP_FECHA_PAGO', this.formMasivo.PAP_FECHA_PAGO)
        if (this.formMasivo.observacion) {
          fd.append('PAP_OBSERVACION', this.formMasivo.observacion)
        }
        this.seleccionados.forEach(id =>
          fd.append('PER_IDS', id)
        )
        fd.append('comprobante', this.formMasivo.file)
        fd.append('MET_ID', 1) // Asumiendo 1 para Transferencia
        
        await pagosService.pagos.createMasivo(fd)

        alert('Pago masivo registrado correctamente')
        this.limpiarMasivo()
        this.cargarPagos()
      } catch (e) {
        alert('Error registrando pago masivo')
      }
    },

    // ===================================================================
    // MÉTODOS PARA LA PESTAÑA DE HISTÓRICO
    // ===================================================================
    /**
     * Obtiene la etiqueta (nombre) de un curso a partir de su ID.
     * @param {number} id - El ID del curso.
     * @returns {string} La etiqueta del curso o el ID si no se encuentra.
     */
    cursoLabel (id) {
      const c = this.cursoOptions.find(
        x => String(x.value) === String(id)
      )
      return c ? c.label : id
    },
    /**
     * Carga la lista de pagos desde la API, aplicando los filtros seleccionados.
     * @param {boolean} force - Si es true, fuerza la recarga aunque ya esté en proceso.
     */
    async cargarPagos (force = false) {
      // Evita cargas múltiples si ya hay una en progreso.
      if (this.cargandoPagos && !force) return;
      this.cargandoPagos = true
      this.errorPagos = null
      try {
        const params = {
          search: (this.filtroQ || '').trim() || undefined,
          CUR_ID: this.filtroCurso || undefined,
          GRU_ID: this.filtroGrupo || undefined
        }
        const response = await pagosService.pagos.list(params)
        // Asegurarse de que la respuesta es un array, incluso si la API devuelve otra cosa.
        if (Array.isArray(response)) {
          this.pagos = response;
        } else if (response && Array.isArray(response.results)) {
          this.pagos = response.results;
        } else {
          console.warn('La respuesta de la API de pagos no es un array:', response);
          this.pagos = []; // Previene errores si la respuesta no es un array
        }
      } catch (e) {
        console.error("Error al cargar pagos:", e);
        this.pagos = []
        this.errorPagos =
          'No fue posible cargar pagos. Verifica el backend.'
      } finally {
        this.cargandoPagos = false
      }
    },
    /**
     * Exporta los pagos actualmente visibles en la tabla a un archivo CSV.
     */
    exportarCSV () {
      const rows = this.pagos.map(p => ({
        Nombre: p.persona_nombre,
        RUT: p.persona_rut,
        Curso: p.curso_descripcion,
        Monto: p.PAP_MONTO,
        Fecha: dateCL(p.PAP_FECHA_PAGO),
        Metodo: p.metodo_descripcion
      }))
      const headers = rows.length
        ? Object.keys(rows[0])
        : ['Nombre', 'RUT', 'Curso', 'Monto', 'Fecha', 'Metodo']
      const csv = [headers.join(',')]
        .concat(
          rows.map(r =>
            headers
              .map(h =>
                `"${String(r[h] ?? '').replace(/"/g, '""')}"`
              )
              .join(',')
          )
        )
        .join('\r\n')
      const blob = new Blob([csv], {
        type: 'text/csv;charset=utf-8;'
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Pagos.csv'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
    /**
     * Selecciona o deselecciona todos los checkboxes de la tabla de historial.
     * @param {boolean} checked - El estado del checkbox principal.
     */
    toggleSelectAllHistorico (checked) {
      this.seleccionadosHistorico = checked
        ? this.pagos.map(p => p.id)
        : []
    },
    /**
     * Simula la acción de marcar pagos como "enviados".
     */
    marcarEnviado () {
      if (!this.seleccionadosHistorico.length) return
      alert(
        `Marcados como enviados: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },
    /**
     * Simula el envío de correos para los pagos seleccionados.
     */
    enviarPorCorreo () {
      if (!this.seleccionadosHistorico.length) return
      alert(
        `Simulación de envío de correos a IDs: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },

    // ===================================================================
    // ACCIONES DE FILA (Ver, Editar, Anular, etc.)
    // ===================================================================
    /**
     * Muestra un detalle simple de un pago en un alert.
     * @param {object} p - El objeto del pago.
     */
    verDetalle (p) {
      alert(
        `Pago de ${p.persona_nombre}\nMonto: $${(p.PAP_MONTO)?.toLocaleString('es-CL') || ''}\nFecha: ${dateCL(p.PAP_FECHA_PAGO)}`
      )
    },
    /**
     * Abre el modal para transferir un pago a otra persona.
     * @param {object} p - El objeto del pago a transferir.
     */
    abrirTransferir (p) {
      this.personasEncontradasTransferir = [];
      this.buscandoPersonasTransferir = false;
      this.pagoTransferir = p
      this.transferForm = {
        nombre: '',
        rut: '',
        email: '',
        tipo: 'total',
        monto_parcial: null
      }
      this.modalTransferir = true
    },
    /**
     * Confirma la transferencia de un pago. (Lógica de API pendiente)
     */
    async confirmarTransferencia () {
      if (!this.pagoTransferir) return
      // Aquí llamarías al endpoint real de transferencia/devolución
      console.log(
        `Transferencia registrada para pago ID ${this.pagoTransferir.id} (${this.transferForm.tipo})`
      )
      this.modalTransferir = false
    },
    /**
     * Busca una persona para realizar la transferencia de un pago.
     */
    async buscarPersonaParaTransferir() {
      const q = (this.transferForm.q || '').trim();
      if (!q) {
        this.personasEncontradasTransferir = [];
        return;
      }
      this.buscandoPersonasTransferir = true;
      try {
        const response = await personasService.personas.list({ search: q });
        const arr = Array.isArray(response) ? response : (response.results || []);
        this.personasEncontradasTransferir = arr.map(p => ({
          id: p.PER_ID,
          nombre: `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: (p.PER_RUN && p.PER_DV) ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
          email: p.PER_MAIL || ''
        }));
      } catch (e) {
        this.personasEncontradasTransferir = [];
      } finally {
        this.buscandoPersonasTransferir = false;
      }
    },
    /**
     * Abre el modal de edición con los datos del pago seleccionado.
     * @param {object} p - El objeto del pago a editar.
     */
    abrirEditar (p) {
      this.pagoEdit = {
        id: p.PAP_ID,
        nombre: p.persona_nombre,
        rut: p.persona_rut,
        curso: p.CUR_ID,
        monto: p.PAP_MONTO,
        fecha: (p.PAP_FECHA_PAGO || '').slice(0, 10),
        observacion: p.PAP_OBSERVACION || ''
      }
      this.modalEditar = true
    },
    /**
     * Guarda los cambios realizados en el modal de edición.
     */
    async guardarEdicion () {
      try {
        // Validación de campos obligatorios
        if (!this.pagoEdit.curso) {
          alert('El campo "Curso" es obligatorio.');
          return;
        }
        if (!this.pagoEdit.monto || this.pagoEdit.monto <= 0) {
          alert('El campo "Monto" debe ser un valor positivo.');
          return;
        }
        if (!this.pagoEdit.fecha) {
          alert('El campo "Fecha" es obligatorio.');
          return;
        }
        this.guardando = true
        const body = {
          CUR_ID: this.pagoEdit.curso,
          PAP_MONTO: this.pagoEdit.monto,
          PAP_FECHA_PAGO: this.pagoEdit.fecha,
          PAP_OBSERVACION: this.pagoEdit.observacion
        }
        await pagosService.pagos.partialUpdate(this.pagoEdit.id, body)
        this.modalEditar = false
        await this.cargarPagos()
        alert('Pago actualizado')
      } catch (e) {
        alert('Error actualizando pago')
      } finally {
        this.guardando = false
      }
    },

    /**
     * Abre el modal de confirmación para anular un pago.
     * @param {object} p - El objeto del pago a anular.
     */
    abrirAnular (p) {
      this.pagoAnular = p
      this.modalAnular = true
    },
    /**
     * Confirma y ejecuta la anulación de un pago.
     */
    async confirmarAnulacion () {
      if (!this.pagoAnular) return;
      try {
        await pagosService.pagos.remove(this.pagoAnular.PAP_ID)
        this.modalAnular = false
        await this.cargarPagos()
        alert('Pago anulado')
      } catch (e) {
        alert('Error al anular pago')
      }
    },
    /**
     * Función de debounce para retrasar la ejecución de una función.
     * Usado para la búsqueda de personas.
     */
    debounce(func, delay) {
      let timeout;
      return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
      };
    },
    /**
     * Abre el comprobante de pago en una nueva pestaña.
     * @param {object} p - El objeto del pago.
     */
    descargarComprobante (p) {
      if (p.PAP_RUTA_COMPROBANTE) {
        window.open(p.PAP_RUTA_COMPROBANTE, '_blank')
      } else {
        alert('No hay comprobante disponible.')
      }
    }
  },
  async mounted () {
    // Carga los datos iniciales necesarios para el componente (catálogos y pagos).
    try {
      // Se ejecutan en paralelo para mejorar el tiempo de carga inicial.
      await Promise.all([
        this.cargarCatalogos(),
        this.cargarPagos()
      ])
    } catch (error) {
      console.error('Error en la carga inicial de PagosView:', error)
      this.errorPagos = 'Ocurrió un error crítico al cargar la página. Por favor, recarga.'
    }
  },
}
</script>

<style>
.gestion-pagos {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 24px;
  background: #f5f7fb;
  font-family: Arial, sans-serif;
  max-width: calc(100% - 48px);
}

.header h2 {
  background: #214e9c;
  color: #fff;
  padding: 14px 18px;
  border-radius: 6px;
  margin: 0 0 18px 0;
  text-align: center; 
}

.tabs,
.subtabs {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.tabs button,
.subtabs button {
  padding: 8px 18px;
  border-radius: 999px;
  border: 1px solid #d1d5db;
  background: #fff;
  cursor: pointer;
  font-weight: 600;
  color: #1f2937;
}

.tabs button.active,
.subtabs button.active {
  background: #214e9c;
  color: #fff;
  border-color: #214e9c;
}

.card {
  background: #ffffff;
  border-radius: 14px;
  padding: 22px 28px 32px;
  max-width: 1400px;
  margin: 12px auto;
  margin-top: 12px;
  box-shadow: 0 8px 26px rgba(15, 23, 42, 0.08);
}

.card-registro {
  min-height: 460px;
}

.card-historico {
  min-height: 360px;
}

/* Paneles y cajas */
.panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 12px;
}

.panel-box {
  border-radius: 12px;
  padding: 16px 18px 22px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.panel-title {
  text-align: center;
  margin-bottom: 10px;
}

.panel-title h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 700;
}

.panel-title p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}

/* Buscar persona */
.row-buscar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.buscar-input {
  flex: 0 0 400px;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px 16px;
  margin-top: 8px;
}
.grid-individual {
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 18px;
}
.grid-masivo {
  grid-template-columns: repeat(2, 1fr);
  gap: 12px 18px;
}



.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.col.full {
  grid-column: 1 / -1;
}

.col.span-2 {
  grid-column: span 2;
}

.col.auto {
  align-self: flex-end;
}

label {
  font-weight: 600;
  color: #111827;
  font-size: 13px;
}

.invisible {
  visibility: hidden;
}

/* Inputs con prefijo $ */
.with-prefix {
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}

.with-prefix .prefix {
  background: #eff6ff;
  padding: 8px 10px;
  font-weight: 700;
  color: #1d4ed8;
  border-right: 1px solid #d1d5db;
}

.with-prefix input {
  border: none;
  padding: 8px 10px;
  flex: 1;
  outline: none;
}

/* Comentario */
.comentario-input {
  width: 100%;
  min-height: 52px;
  max-height: 80px;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  resize: vertical;
  font-family: inherit;
  font-size: 13px;
}

/* Comprobante */
.comprobante-wrapper {
  margin-top: 8px;
}

/* Resultados búsqueda */
.resultados {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 4px;
  max-width: 480px;
  background: #ffffff;
}

.resultado {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
}

.resultado:last-child {
  border-bottom: none;
}

.resultado:hover {
  background: #f9fafb;
}

.resultado .muted {
  color: #6b7280;
  font-size: 11px;
}

/* Lista masivo */
.lista {
  margin-top: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
}

.lista-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid #f3f4f6;
}

.lista-items {
  max-height: 260px;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.item {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px 10px;
  border-bottom: 1px solid #f9fafb;
}

.item:last-child {
  border-bottom: none;
}

.item .info .muted {
  color: #6b7280;
  font-size: 11px;
}

/* Resumen */
.resumen {
  margin-top: 10px;
  padding: 10px 14px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  display: flex;
  gap: 16px;
  justify-content: center;
  font-weight: 600;
  color: #1d4ed8;
}

.resumen .total {
  text-transform: uppercase;
}

/* Filtros histórico */
.filtros {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start; /* Evita que los elementos se estiren */
  gap: 8px;
}

.filtros-historico {
  margin-bottom: 10px;
}

.filtros-historico .filtro-busqueda {
  width: 200px;
}

.filtros-historico .filtro-corto {
  width: 140px;
  width: 160px;
}

.filtros-historico .filtro-corto :deep(input),
.filtros-historico .filtro-corto :deep(select) {
  width: 100%;
}

/* Toolbar */
.toolbar {
  display: flex;
  gap: 10px;
  margin: 4px 0 12px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: background 0.15s ease, transform 0.03s ease;
}

.btn-primary {
  background: #214e9c;
  color: #fff;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary:not(:disabled):hover {
  background: #1d4ed8;
}

.btn-primary:active {
  transform: translateY(1px);
}

/* Acciones */
.acciones {
  display: flex;
  gap: 8px;
}

.acciones.center {
  justify-content: center;
}

.acciones-individual {
  margin-top: 14px;
}

.btn-search {
  background: #214e9c;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-weight: 600;
  cursor: pointer;
}

.btn-search:hover {
  background: #1d4ed8;
}

.btn-secundario {
  background: #4b6cb7 !important;
}

.btn-danger {
  background: #dc2626 !important;
  color: #fff !important;
}

/* Tabla */
.table-wrapper {
  overflow-y: auto;
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #fff;
  max-height: calc(100vh - var(--navbar-height) - var(--card-top-offset));
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th,
td {
  padding: 10px 10px;
  border-bottom: 1px solid #f3f4f6;
  text-align: left;
}

th {
  background: #f9fafb;
  font-weight: 600;
}

.placeholder {
  text-align: center;
  padding: 26px 10px;
  color: #6b7280;
}

/* Botones acciones tabla */
.acciones-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  justify-content: center;
}

.btn-with-icon {
  padding: 4px 8px;
  font-size: 11px;
  border-radius: 6px;
}

/* Estados */
.estado-carga {
  text-align: center;
  padding: 10px;
  color: #6b7280;
  font-style: italic;
}

.estado-carga .spinner {
  display: inline-block;
  vertical-align: middle;
}

.mensaje-error {
  background: #fee2e2;
  color: #b91c1c;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #fecaca;
  font-size: 13px;
}
.mensaje-error div {
  margin-top: 8px;
  text-align: center;
}



/* Modales */
.pago-modal :deep(.modal-overlay) {
  position: fixed !important;
  inset: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 9999 !important;
}

.modal-edit,
.modal-transfer {
  width: 640px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 80px);
  overflow: auto;
  padding: 20px 22px 18px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
}

.form-fields-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 18px;
}

.row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.row.full-width {
  grid-column: 1 / -1;
}

.row input,
.row select {
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}

.confirm-content {
  padding: 18px 20px;
  text-align: center;
}

.confirm-icon {
  font-size: 44px;
  margin-bottom: 8px;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
  .buscar-input {
    flex: 1 1 auto;
  }
  .filtros-historico .filtro-busqueda {
    width: 170px;
  }
  .filtros-historico .filtro-corto {
    width: 120px;
    width: 140px;
  }

  /* Tabla responsiva */
  .table-wrapper table thead {
    display: none;
  }
  .table-wrapper table tr {
    display: block;
    margin-bottom: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.5rem;
  }
  .table-wrapper table td {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #f3f4f6;
    padding: 0.75rem 0.5rem;
  }
  .table-wrapper table td[data-label]::before {
    content: attr(data-label);
    font-weight: 600;
    margin-right: 1rem;
    color: #374151;
  }
  .table-wrapper table td:last-child {
    border-bottom: none;
  }
}

/* Estilo para texto largo en tablas */
.texto-largo {
  max-width: 200px; /* o el ancho que prefieras */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
<style>
/* Estilos de botones estandarizados, inspirados en GestionPersonas */
.btn-standard {
  min-width: 140px !important;
  padding: 10px 16px !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(40,92,168,0.08) !important;
  border: none !important;
  transition: all 0.3s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.btn-action {
  padding: 6px 12px !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  box-shadow: 0 1px 4px rgba(40,92,168,0.06) !important;
  border: none !important;
  transition: all 0.3s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  min-width: auto !important;
}
</style>
