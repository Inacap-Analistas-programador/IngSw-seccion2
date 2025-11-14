<template>
  <div class="gestion-pagos">
    <!-- Encabezado -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
    </header>

    <!-- Tabs principales -->
    <div class="tabs">
      <button :class="{ active: tab === 'registro' }" @click="tab = 'registro'">
        Registro
      </button>
      <button :class="{ active: tab === 'historico' }" @click="tab = 'historico'">
        Histórico
      </button>
    </div>

    <!-- ===================== REGISTRO ===================== -->
    <div v-if="tab === 'registro'" class="card card-registro">
      <!-- Subtabs -->
      <div class="subtabs">
        <button :class="{ active: subTab === 'individual' }" @click="subTab = 'individual'">
          Individual
        </button>
        <button :class="{ active: subTab === 'masivo' }" @click="subTab = 'masivo'">
          Masivo
        </button>
      </div>

      <!-- -------- Registro Individual -------- -->
      <section v-if="subTab === 'individual'" class="panel panel-box">
        <div class="panel-title">
          <h3>Registro Individual de Pagos</h3>
          <p>Busca un participante, selecciona el curso y registra el pago.</p>
        </div>

        <!-- Buscar persona -->
        <div class="row-buscar">
          <div class="buscar-input">
            <InputBase
              v-model="buscarPersonaQ"
              placeholder="EJ: 12.345.678-9 O JUAN PÉREZ"
              @keydown.enter.prevent="buscarPersonas"
            />
          </div>
          <BaseButton class="btn-search" variant="primary" @click="buscarPersonas">
            Buscar
          </BaseButton>
        </div>

        <div v-if="buscandoPersonas" class="estado-carga">
          Buscando personas...
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
            <BaseButton size="sm" variant="primary">
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
              v-model="formInd.curso"
              :options="cursoOptions"
              placeholder="Seleccione curso"
            />
          </div>

          <div class="col">
            <label>Valor Pagado *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input
                type="number"
                min="0"
                step="1"
                v-model.number="formInd.valor_pagado"
              />
            </div>
          </div>

          <div class="col">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formInd.fecha_pago" />
          </div>

          <div class="col full">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              class="comentario-input"
              v-model="formInd.observacion"
              maxlength="200"
              placeholder="Detalle del pago, referencia de transferencia, etc."
            />
          </div>

          <div class="col full comprobante-wrapper">
            <label>Comprobante de transferencia (obligatorio)</label>
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
            variant="primary"
            :disabled="!puedeRegistrarIndividual"
            @click="registrarPagoIndividual"
          >
            Registrar Pago Individual
          </BaseButton>
          <BaseButton variant="primary" class="btn-secundario" @click="limpiarIndividual">
            Limpiar
          </BaseButton>
        </div>
      </section>

      <!-- -------- Registro Masivo -------- -->
      <section v-else class="panel panel-box">
        <div class="panel-title">
          <h3>Registro Masivo de Pagos</h3>
          <p>Selecciona grupo y curso, participantes y registra pagos masivos.</p>
        </div>

        <div class="grid grid-masivo">
          <div class="col">
            <label>Grupo *</label>
            <BaseSelect
              v-model="formMasivo.grupo"
              :options="grupoOptions"
              placeholder="Seleccione grupo"
            />
          </div>
          <div class="col">
            <label>Curso / Capacitación *</label>
            <BaseSelect
              v-model="formMasivo.curso"
              :options="cursoOptions"
              placeholder="Seleccione curso"
            />
          </div>
          <div class="col auto">
            <label class="invisible">Cargar</label>
            <BaseButton
              variant="primary"
              :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoParticipantes"
              @click="cargarParticipantes"
            >
              {{ cargandoParticipantes ? 'Cargando...' : 'Cargar Participantes' }}
            </BaseButton>
          </div>
        </div>

        <div v-if="participantes.length" class="lista">
          <div class="lista-header">
            <h5>Participantes disponibles ({{ participantes.length }})</h5>
            <div class="acciones">
              <BaseButton size="sm" variant="primary" @click="selectAll">
                Seleccionar todos
              </BaseButton>
              <BaseButton size="sm" variant="primary" class="btn-secundario" @click="unselectAll">
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
                step="1"
                v-model.number="formMasivo.valor_pagado"
              />
            </div>
          </div>
          <div class="col">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formMasivo.fecha_pago" />
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
          v-if="seleccionados.length && formMasivo.valor_pagado"
        >
          <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
          <div>Valor por persona: <strong>${{ formMasivo.valor_pagado.toLocaleString('es-CL') }}</strong></div>
          <div class="total">
            Total:
            <strong>
              ${{
                (seleccionados.length * formMasivo.valor_pagado).toLocaleString('es-CL')
              }}
            </strong>
          </div>
        </div>

        <div class="acciones center acciones-individual" v-if="seleccionados.length">
          <BaseButton
            variant="primary"
            :disabled="!puedeRegistrarMasivo"
            @click="registrarPagoMasivo"
          >
            Registrar Pago Masivo ({{ seleccionados.length }})
          </BaseButton>
          <BaseButton variant="primary" class="btn-secundario" @click="limpiarMasivo">
            Limpiar
          </BaseButton>
        </div>
      </section>
    </div>

    <!-- ===================== HISTÓRICO ===================== -->
    <div v-else class="card card-historico">
      <!-- Filtros compactos -->
      <div class="filtros filtros-historico">
        <InputBase
          class="filtro-corto"
          v-model="filtroQ"
          placeholder="NOMBRE / RUT / EMAIL"
          @keydown.enter.prevent="cargarPagos"
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
        <BaseButton class="btn-search" variant="primary" @click="cargarPagos">
          Buscar
        </BaseButton>
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <button class="btn btn-primary" @click="exportarCSV">
          Exportar Correos
        </button>

        <button
          class="btn btn-primary"
          :disabled="!seleccionadosHistorico.length"
          @click="marcarEnviado"
        >
          Marcar Enviado
        </button>

        <button
          class="btn btn-primary"
          :disabled="!seleccionadosHistorico.length"
          @click="enviarPorCorreo"
        >
          Enviar por correo
        </button>
      </div>

      <!-- Estado -->
      <div v-if="cargandoPagos" class="estado-carga">
        Cargando pagos...
      </div>
      <div v-if="errorPagos" class="mensaje-error">
        {{ errorPagos }}
        <div>
          <BaseButton variant="primary" @click="cargarPagos">Reintentar</BaseButton>
        </div>
      </div>

      <!-- Tabla -->
      <div class="table-wrapper" v-if="!cargandoPagos">
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
              <td><strong>{{ p.nombre }}</strong></td>
              <td>{{ p.rut }}</td>
              <td>{{ cursoLabel(p.curso) }}</td>
              <td>${{ (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL') }}</td>
              <td>{{ dateCL(p.fecha || p.fecha_pago) }}</td>
              <td>{{ p.metodo || 'Transferencia' }}</td>
              <td class="acciones-buttons">
                <BaseButton
                  size="sm"
                  variant="primary"
                  class="btn-with-icon"
                  @click="verDetalle(p)"
                >
                  👁️ Ver
                </BaseButton>
                <BaseButton
                  size="sm"
                  variant="primary"
                  class="btn-with-icon"
                  @click="abrirEditar(p)"
                >
                  ✏️ Editar
                </BaseButton>
                <BaseButton
                  size="sm"
                  variant="primary"
                  class="btn-with-icon"
                  @click="abrirTransferir(p)"
                >
                  🔁 Transferir
                </BaseButton>
                <BaseButton
                  size="sm"
                  variant="primary"
                  class="btn-with-icon btn-danger"
                  @click="abrirAnular(p)"
                >
                  🗑️ Anular
                </BaseButton>
                <BaseButton
                  v-if="p.comprobante || p.comprobante_url"
                  size="sm"
                  variant="primary"
                  class="btn-with-icon btn-secundario"
                  @click="descargarComprobante(p)"
                >
                  🧾 Comprobante
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

    <!-- Modal Editar -->
    <BaseModal v-model="modalEditar" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <div class="header-actions">
              <BaseButton
                class="btn-save"
                type="button"
                variant="primary"
                @click="guardarEdicion"
                :disabled="guardando"
              >
                {{ guardando ? 'Guardando...' : 'Guardar' }}
              </BaseButton>
            </div>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <input v-model="pagoEdit.nombre" readonly />
            </div>
            <div class="row">
              <label>RUT</label>
              <input v-model="pagoEdit.rut" readonly />
            </div>
            <div class="row">
              <label>Curso</label>
              <BaseSelect v-model="pagoEdit.curso" :options="cursoOptions" />
            </div>
            <div class="row">
              <label>Monto</label>
              <input type="number" v-model.number="pagoEdit.monto" />
            </div>
            <div class="row">
              <label>Fecha</label>
              <input type="date" v-model="pagoEdit.fecha" />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <input v-model="pagoEdit.observacion" />
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
          <p>¿Anular pago de <strong>{{ pagoAnular?.nombre }}</strong>?</p>
          <div class="confirm-actions">
            <BaseButton
              variant="primary"
              class="btn-secundario"
              @click="modalAnular = false"
            >
              Cancelar
            </BaseButton>
            <BaseButton
              variant="primary"
              class="btn-danger"
              @click="confirmarAnulacion"
            >
              Anular
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Transferir -->
    <BaseModal v-model="modalTransferir" title="Transferir Pago">
      <template #default>
        <div class="modal-transfer">
          <h3>Transferir pago de {{ pagoTransferir?.nombre }}</h3>
          <p class="muted">
            Completa los datos del nuevo participante y el tipo de devolución.
          </p>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre nuevo participante</label>
              <input v-model="transferForm.nombre" />
            </div>
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

          <div class="confirm-actions">
            <BaseButton
              variant="primary"
              class="btn-secundario"
              @click="modalTransferir = false"
            >
              Cancelar
            </BaseButton>
            <BaseButton
              variant="primary"
              @click="confirmarTransferencia"
            >
              Confirmar Transferencia
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import InputBase from '@/components/InputBase.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'


function hoyISO () {
  const d = new Date()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day}`
}
function dateCL (f) {
  if (!f) return '-'
  return new Date(f).toLocaleDateString('es-CL', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

export default {
  name: 'PagosView',
  components: { InputBase, BaseSelect, BaseButton, BaseModal },
  data () {
    return {
      tab: 'registro',
      subTab: 'individual',

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
        curso: '',
        valor_pagado: null,
        fecha_pago: hoyISO(),
        observacion: '',
        file: null
      },

      formMasivo: {
        grupo: '',
        curso: '',
        valor_pagado: null,
        fecha_pago: hoyISO(),
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
      transferForm: {
        nombre: '',
        rut: '',
        email: '',
        tipo: 'total',
        monto_parcial: null
      }
    }
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
        this.formInd.curso &&
        this.formInd.valor_pagado &&
        this.formInd.fecha_pago &&
        this.formInd.file
      )
    },
    puedeRegistrarMasivo () {
      return (
        this.seleccionados.length &&
        this.formMasivo.curso &&
        this.formMasivo.grupo &&
        this.formMasivo.valor_pagado &&
        this.formMasivo.fecha_pago &&
        this.formMasivo.file
      )
    }
  },
  methods: {
    // ===== Carga catálogos (ajusta a tus endpoints reales) =====
    async cargarCatalogos () {
      try {
        if (pagosService.cursos && pagosService.cursos.list) {
          const cursos = await pagosService.cursos.list()
          const arr = Array.isArray(cursos) ? cursos : (cursos.results || [])
          this.cursoOptions = arr.map(c => ({
            value: c.id,
            label: c.nombre || c.descripcion || `Curso ${c.id}`
          }))
        }
      } catch (e) {
        this.cursoOptions = []
      }

      try {
        if (pagosService.grupos && pagosService.grupos.list) {
          const grupos = await pagosService.grupos.list()
          const arr = Array.isArray(grupos) ? grupos : (grupos.results || [])
          this.grupoOptions = arr.map(g => ({
            value: g.id,
            label: g.nombre || `Grupo ${g.id}`
          }))
        }
      } catch (e) {
        this.grupoOptions = []
      }
    },

    // ===== Registro Individual =====
    async buscarPersonas () {
      const q = (this.buscarPersonaQ || '').trim()
      if (!q) {
        this.personasEncontradas = []
        return
      }
      this.buscandoPersonas = true
      try {
        let r = []
        if (personasService.search) {
          r = await personasService.search({ q })
        } else if (personasService.personas?.search) {
          r = await personasService.personas.search({ q })
        }
        const arr = Array.isArray(r) ? r : (r.results || [])
        this.personasEncontradas = arr.map(p => ({
          id: p.id ?? p.PER_ID,
          nombre:
            p.nombre ??
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ||
            (p.PER_RUN && p.PER_DV ? `${p.PER_RUN}-${p.PER_DV}` : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }))
      } catch (e) {
        this.personasEncontradas = []
      } finally {
        this.buscandoPersonas = false
      }
    },
    seleccionarPersona (p) {
      this.formInd.personaId = p.id
      this.formInd.nombre = p.nombre
      this.formInd.rut = p.rut
      this.formInd.email = p.email
      this.personasEncontradas = []
      this.buscarPersonaQ = p.nombre
    },
    onFileInd (e) {
      this.formInd.file = e.target.files?.[0] || null
    },
    limpiarIndividual () {
      this.formInd = {
        personaId: null,
        nombre: '',
        rut: '',
        email: '',
        curso: '',
        valor_pagado: null,
        fecha_pago: hoyISO(),
        observacion: '',
        file: null
      }
      this.buscarPersonaQ = ''
      this.personasEncontradas = []
    },
    async registrarPagoIndividual () {
      try {
        const fd = new FormData()
        fd.append('persona', this.formInd.personaId)
        fd.append('curso', this.formInd.curso)
        fd.append('monto', this.formInd.valor_pagado)
        fd.append('fecha_pago', this.formInd.fecha_pago)
        if (this.formInd.observacion) {
          fd.append('observacion', this.formInd.observacion)
        }
        fd.append('comprobante', this.formInd.file)

        if (pagosService.pagos?.createIndividualForm) {
          await pagosService.pagos.createIndividualForm(fd)
        } else if (pagosService.pagos?.create) {
          await pagosService.pagos.create(fd)
        } else {
          throw new Error('No hay endpoint definido para registro individual')
        }

        alert('Pago individual registrado correctamente')
        this.limpiarIndividual()
        this.cargarPagos()
      } catch (e) {
        alert('Error registrando pago individual')
      }
    },

    // ===== Registro Masivo =====
    onFileMasivo (e) {
      this.formMasivo.file = e.target.files?.[0] || null
    },
    async cargarParticipantes () {
      this.cargandoParticipantes = true
      try {
        let r = []
        if (personasService.byGrupoCurso) {
          r = await personasService.byGrupoCurso({
            grupo: this.formMasivo.grupo,
            curso: this.formMasivo.curso
          })
        }
        const arr = Array.isArray(r) ? r : (r.results || [])
        this.participantes = arr.map(p => ({
          id: p.id ?? p.PER_ID,
          nombre:
            p.nombre ??
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ||
            (p.PER_RUN && p.PER_DV ? `${p.PER_RUN}-${p.PER_DV}` : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }))
        this.seleccionados = []
      } catch (e) {
        this.participantes = []
      } finally {
        this.cargandoParticipantes = false
      }
    },
    selectAll () {
      this.seleccionados = this.participantes.map(u => u.id)
    },
    unselectAll () {
      this.seleccionados = []
    },
    limpiarMasivo () {
      this.formMasivo = {
        grupo: '',
        curso: '',
        valor_pagado: null,
        fecha_pago: hoyISO(),
        observacion: '',
        file: null
      }
      this.participantes = []
      this.seleccionados = []
    },
    async registrarPagoMasivo () {
      try {
        const fd = new FormData()
        fd.append('grupo', this.formMasivo.grupo)
        fd.append('curso', this.formMasivo.curso)
        fd.append('valor_pagado', this.formMasivo.valor_pagado)
        fd.append('fecha_pago', this.formMasivo.fecha_pago)
        if (this.formMasivo.observacion) {
          fd.append('observacion', this.formMasivo.observacion)
        }
        this.seleccionados.forEach(id =>
          fd.append('participantes[]', id)
        )
        fd.append('comprobante', this.formMasivo.file)

        if (pagosService.pagos?.createMasivoForm) {
          await pagosService.pagos.createMasivoForm(fd)
        } else if (pagosService.pagos?.createMasivo) {
          await pagosService.pagos.createMasivo(fd)
        } else {
          throw new Error('No hay endpoint definido para registro masivo')
        }

        alert('Pago masivo registrado correctamente')
        this.limpiarMasivo()
        this.cargarPagos()
      } catch (e) {
        alert('Error registrando pago masivo')
      }
    },

    // ===== Histórico =====
    cursoLabel (id) {
      const c = this.cursoOptions.find(
        x => String(x.value) === String(id)
      )
      return c ? c.label : id
    },
    async cargarPagos () {
      this.cargandoPagos = true
      this.errorPagos = null
      try {
        let r = []
        const params = {
          q: (this.filtroQ || '').trim(),
          curso: this.filtroCurso || undefined,
          grupo: this.filtroGrupo || undefined
        }
        if (pagosService.pagos?.list) {
          r = await pagosService.pagos.list(params)
        } else if (pagosService.list) {
          r = await pagosService.list(params)
        }
        this.pagos = Array.isArray(r) ? r : (r.results || [])
      } catch (e) {
        this.pagos = []
        this.errorPagos =
          'No fue posible cargar pagos. Verifica el backend.'
      } finally {
        this.cargandoPagos = false
      }
    },
    exportarCSV () {
      const rows = this.pagos.map(p => ({
        Nombre: p.nombre,
        RUT: p.rut,
        Curso: this.cursoLabel(p.curso),
        Monto: p.monto ?? p.valor_pagado,
        Fecha: dateCL(p.fecha || p.fecha_pago),
        Metodo: p.metodo || 'Transferencia'
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
    toggleSelectAllHistorico (checked) {
      this.seleccionadosHistorico = checked
        ? this.pagos.map(p => p.id)
        : []
    },
    marcarEnviado () {
      if (!this.seleccionadosHistorico.length) return
      alert(
        `Marcados como enviados: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },
    enviarPorCorreo () {
      if (!this.seleccionadosHistorico.length) return
      alert(
        `Simulación de envío de correos a IDs: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },

    // ===== Acciones de fila =====
    verDetalle (p) {
      alert(
        `Pago de ${p.nombre}\nMonto: $${
          (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL') || ''
        }\nFecha: ${dateCL(p.fecha || p.fecha_pago)}`
      )
    },
    abrirTransferir (p) {
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
    async confirmarTransferencia () {
      if (!this.pagoTransferir) return
      // Aquí llamarías al endpoint real de transferencia/devolución
      alert(
        `Transferencia registrada para pago ID ${this.pagoTransferir.id} (${this.transferForm.tipo})`
      )
      this.modalTransferir = false
    },

    abrirEditar (p) {
      this.pagoEdit = {
        id: p.id,
        nombre: p.nombre,
        rut: p.rut,
        curso: p.curso,
        monto: p.monto ?? p.valor_pagado,
        fecha: (p.fecha || p.fecha_pago || '').slice(0, 10),
        observacion: p.observacion || ''
      }
      this.modalEditar = true
    },
    async guardarEdicion () {
      try {
        this.guardando = true
        const body = {
          curso: this.pagoEdit.curso,
          monto: this.pagoEdit.monto,
          fecha: this.pagoEdit.fecha,
          observacion: this.pagoEdit.observacion
        }
        if (pagosService.pagos?.partialUpdate) {
          await pagosService.pagos.partialUpdate(
            this.pagoEdit.id,
            body
          )
        } else if (pagosService.pagos?.update) {
          await pagosService.pagos.update(this.pagoEdit.id, body)
        }
        this.modalEditar = false
        await this.cargarPagos()
        alert('Pago actualizado')
      } catch (e) {
        alert('Error actualizando pago')
      } finally {
        this.guardando = false
      }
    },

    abrirAnular (p) {
      this.pagoAnular = p
      this.modalAnular = true
    },
    async confirmarAnulacion () {
      try {
        if (pagosService.pagos?.anular) {
          await pagosService.pagos.anular(this.pagoAnular.id)
        } else if (pagosService.anular) {
          await pagosService.anular(this.pagoAnular.id)
        }
        this.modalAnular = false
        await this.cargarPagos()
        alert('Pago anulado')
      } catch (e) {
        alert('Error al anular pago')
      }
    },
    descargarComprobante (p) {
      if (p.comprobante_url) {
        window.open(p.comprobante_url, '_blank')
      } else {
        alert('No hay comprobante disponible.')
      }
    }
  },
  async mounted () {
    await Promise.all([this.cargarCatalogos(), this.cargarPagos()])
  },
  filters: {
    dateCL
  }
}
</script>

<style>
.gestion-pagos {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px 32px;
  background: #f5f7fb;
  font-family: Arial, sans-serif;
  max-width: 1400px;
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
  padding: 18px 22px 26px;
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
  flex: 0 0 320px;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px 16px;
  margin-top: 8px;
}

.grid-individual .col:nth-child(1),
.grid-individual .col:nth-child(2),
.grid-individual .col:nth-child(3) {
  max-width: 280px;
}

.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.col.full {
  grid-column: 1 / -1;
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
  gap: 8px;
}

.filtros-historico {
  margin-bottom: 10px;
}

.filtros-historico .filtro-corto {
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
  overflow: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #fff;
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

.mensaje-error {
  background: #fee2e2;
  color: #b91c1c;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #fecaca;
  font-size: 13px;
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
  .filtros-historico .filtro-corto {
    width: 140px;
  }
}
</style>
