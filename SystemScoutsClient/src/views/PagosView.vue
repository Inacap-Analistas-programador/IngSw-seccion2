<template>
  <div class="gestion-pagos">
    <!-- Encabezado -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
    </header>

    <!-- Pestañas -->
    <div class="tabs">
      <button :class="{ active: tab === 'registro' }" @click="tab = 'registro'">
        Registro
      </button>
      <button :class="{ active: tab === 'historico' }" @click="tab = 'historico'">
        Histórico
      </button>
    </div>

    <!-- ===================== REGISTRO ===================== -->
    <div v-if="tab === 'registro'" class="card registro-wrapper">
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
      <section v-if="subTab === 'individual'" class="panel">
        <div class="panel-card">
          <div class="panel-title center">
            <h4>Registro Individual de Pagos</h4>
            <p class="panel-subtitle">
              Busca un participante, selecciona el curso y registra el pago.
            </p>
          </div>

          <!-- Buscar participante -->
          <div class="buscar-row">
            <label>Buscar Participante (Nombre / RUT / Email)</label>
            <div class="buscar-input-group">
              <InputBase
                v-model="buscarPersonaQ"
                class="input-buscar"
                placeholder="Ej: 12.345.678-9 o Juan Pérez"
                @keydown.enter.prevent="buscarPersonas"
              />
              <BaseButton class="btn-main" @click="buscarPersonas">
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
                <BaseButton size="sm" class="btn-sec">
                  Elegir
                </BaseButton>
              </div>
            </div>

            <div
              v-else-if="buscarPersonaQ && !buscandoPersonas"
              class="no-result"
            >
              Sin resultados
            </div>
          </div>

          <!-- Datos pago individual -->
          <div class="grid grid-compact">
            <div class="col small">
              <label>Nombre</label>
              <InputBase v-model="formInd.nombre" readonly />
            </div>
            <div class="col small">
              <label>RUT</label>
              <InputBase v-model="formInd.rut" readonly />
            </div>
            <div class="col small">
              <label>Email</label>
              <InputBase v-model="formInd.email" readonly />
            </div>

            <div class="col small">
              <label>Curso / Capacitación *</label>
              <BaseSelect
                v-model="formInd.curso"
                :options="cursoOptions"
                placeholder="Seleccione curso"
              />
            </div>

            <div class="col tiny">
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

            <div class="col small">
              <label>Fecha de Pago *</label>
              <InputBase type="date" v-model="formInd.fecha_pago" />
            </div>
          </div>

          <!-- Comentario centrado -->
          <div class="comment-block">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              v-model="formInd.observacion"
              maxlength="200"
              class="comment-textarea"
              placeholder="Detalle del pago, referencia de transferencia, etc."
            ></textarea>
          </div>

          <!-- Comprobante obligatorio -->
          <div class="file-block">
            <label>Comprobante (obligatorio)</label>
            <input
              ref="fileIndRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileInd"
            />
          </div>

          <!-- Botones -->
          <div class="acciones center acciones-bottom">
            <BaseButton
              class="btn-main"
              :disabled="
                !formInd.personaId ||
                !formInd.curso ||
                !formInd.valor_pagado ||
                !formInd.fecha_pago ||
                !formInd.file
              "
              @click="registrarPagoIndividual"
            >
              Registrar Pago Individual
            </BaseButton>
            <BaseButton class="btn-main-outline" @click="limpiarIndividual">
              Limpiar
            </BaseButton>
          </div>
        </div>
      </section>

      <!-- -------- Registro Masivo -------- -->
      <section v-else class="panel">
        <div class="panel-card">
          <div class="panel-title center">
            <h4>Registro Masivo de Pagos</h4>
            <p class="panel-subtitle">
              Selecciona grupo y curso, carga participantes y registra el pago.
            </p>
          </div>

          <div class="grid grid-compact">
            <div class="col small">
              <label>Grupo *</label>
              <BaseSelect
                v-model="formMasivo.grupo"
                :options="grupoOptions"
                placeholder="Seleccione grupo"
              />
            </div>
            <div class="col small">
              <label>Curso / Capacitación *</label>
              <BaseSelect
                v-model="formMasivo.curso"
                :options="cursoOptions"
                placeholder="Seleccione curso"
              />
            </div>
            <div class="col auto">
              <label class="invisible">.</label>
              <BaseButton
                class="btn-main"
                :disabled="
                  !formMasivo.grupo || !formMasivo.curso || cargandoParticipantes
                "
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
                <BaseButton size="sm" class="btn-main-outline" @click="selectAll">
                  Seleccionar todos
                </BaseButton>
                <BaseButton
                  size="sm"
                  class="btn-main-outline"
                  @click="unselectAll"
                >
                  Deseleccionar
                </BaseButton>
              </div>
            </div>

            <div class="lista-items">
              <label v-for="u in participantes" :key="u.id" class="item">
                <input
                  type="checkbox"
                  :value="u.id"
                  v-model="seleccionados"
                />
                <div class="info">
                  <strong>{{ u.nombre }}</strong>
                  <span class="muted">{{ u.rut }} · {{ u.email }}</span>
                </div>
              </label>
            </div>
          </div>

          <div v-if="seleccionados.length" class="grid grid-compact">
            <div class="col tiny">
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
            <div class="col small">
              <label>Fecha de Pago *</label>
              <InputBase type="date" v-model="formMasivo.fecha_pago" />
            </div>
          </div>

          <div v-if="seleccionados.length" class="comment-block">
            <label>Comentario / Observación (aplica a todos)</label>
            <textarea
              v-model="formMasivo.observacion"
              maxlength="200"
              class="comment-textarea"
              placeholder="Comentario general del pago masivo (opcional)"
            ></textarea>
          </div>

          <div v-if="seleccionados.length" class="file-block">
            <label>Comprobante Grupal (obligatorio)</label>
            <input
              ref="fileMasivoRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileMasivo"
            />
          </div>

          <div
            v-if="seleccionados.length && formMasivo.valor_pagado"
            class="resumen"
          >
            <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
            <div>
              Valor por persona:
              <strong>
                ${{
                  formMasivo.valor_pagado.toLocaleString('es-CL')
                }}
              </strong>
            </div>
            <div class="total">
              Total:
              <strong>
                ${{
                  (seleccionados.length * formMasivo.valor_pagado).toLocaleString(
                    'es-CL'
                  )
                }}
              </strong>
            </div>
          </div>

          <div
            class="acciones center acciones-bottom"
            v-if="seleccionados.length"
          >
            <BaseButton
              class="btn-main"
              :disabled="
                !formMasivo.valor_pagado ||
                !formMasivo.fecha_pago ||
                !formMasivo.file
              "
              @click="registrarPagoMasivo"
            >
              Registrar Pago Masivo
            </BaseButton>
            <BaseButton class="btn-main-outline" @click="limpiarMasivo">
              Limpiar
            </BaseButton>
          </div>
        </div>
      </section>
    </div>

    <!-- ===================== HISTÓRICO ===================== -->
    <div v-else class="card">
      <!-- Filtros -->
      <div class="filtros">
        <InputBase
          v-model="filtroQ"
          class="filtro-input"
          placeholder="Nombre / RUT / Email"
          @keydown.enter.prevent="cargarPagos"
        />
        <BaseSelect
          v-model="filtroCurso"
          :options="[{ value: '', label: 'Todos los cursos' }, ...cursoOptions]"
        />
        <BaseSelect
          v-model="filtroGrupo"
          :options="[{ value: '', label: 'Todos los grupos' }, ...grupoOptions]"
        />
        <BaseButton class="btn-main" @click="cargarPagos">
          Buscar
        </BaseButton>
      </div>

      <!-- Barra de acciones -->
      <div class="toolbar">
        <button class="toolbar-btn" @click="exportarCSV">
          Exportar Correos
        </button>
        <button
          class="toolbar-btn"
          :disabled="!seleccionadosHistorico.length"
          @click="marcarEnviado"
        >
          Marcar Enviado
        </button>
        <button
          class="toolbar-btn"
          :disabled="!seleccionadosHistorico.length"
          @click="enviarPorCorreo"
        >
          Enviar por correo
        </button>
      </div>

      <!-- Estado de carga y error -->
      <div v-if="cargandoPagos" class="estado-carga">
        Cargando pagos...
      </div>
      <div v-if="errorPagos" class="mensaje-error">
        {{ errorPagos }}
        <div>
          <BaseButton class="btn-main" @click="cargarPagos">
            Reintentar
          </BaseButton>
        </div>
      </div>

      <!-- Tabla -->
      <div class="table-wrapper" v-if="!cargandoPagos">
        <table>
          <thead>
            <tr>
              <th style="width: 36px;">
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
              <td>
                ${{
                  (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL')
                }}
              </td>
              <td>{{ dateCL(p.fecha || p.fecha_pago) }}</td>
              <td>{{ p.metodo || 'Transferencia' }}</td>
              <td class="acciones-buttons">
                <BaseButton
                  size="sm"
                  class="btn-main btn-sm"
                  @click="verDetalle(p)"
                >
                  Ver
                </BaseButton>
                <BaseButton
                  size="sm"
                  class="btn-main btn-sm"
                  @click="abrirEditar(p)"
                >
                  Editar
                </BaseButton>
                <BaseButton
                  size="sm"
                  class="btn-main btn-sm"
                  @click="abrirTransferir(p)"
                >
                  Transferir
                </BaseButton>
                <BaseButton
                  size="sm"
                  class="btn-main btn-sm"
                  @click="abrirAnular(p)"
                >
                  Anular
                </BaseButton>
                <BaseButton
                  v-if="p.comprobante || p.comprobante_url"
                  size="sm"
                  class="btn-main-outline btn-sm"
                  @click="descargarComprobante(p)"
                >
                  Comprobante
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

    <!-- MODALES (Editar, Anular, Transferir) -->
    <BaseModal v-model="modalEditar" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <BaseButton
              class="btn-main"
              type="button"
              @click="guardarEdicion"
              :disabled="guardando"
            >
              {{ guardando ? 'Guardando...' : 'Guardar' }}
            </BaseButton>
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
              <BaseSelect
                v-model="pagoEdit.curso"
                :options="cursoOptions"
              />
            </div>
            <div class="row">
              <label>Monto</label>
              <input
                type="number"
                v-model.number="pagoEdit.monto"
              />
            </div>
            <div class="row">
              <label>Fecha</label>
              <input
                type="date"
                v-model="pagoEdit.fecha"
              />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <input v-model="pagoEdit.observacion" />
            </div>
          </div>
        </div>
      </template>
    </BaseModal>

    <BaseModal v-model="modalAnular">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">!</div>
          <p>
            ¿Anular pago de
            <strong>{{ pagoAnular?.nombre }}</strong>?
          </p>
          <div class="confirm-actions">
            <BaseButton
              class="btn-main-outline"
              @click="modalAnular = false"
            >
              Cancelar
            </BaseButton>
            <BaseButton
              class="btn-main"
              @click="confirmarAnulacion"
            >
              Confirmar Anulación
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <BaseModal v-model="modalTransferir">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Transferir Pago</h3>
          </header>

          <p class="modal-note">
            Transferir pago de
            <strong>{{ pagoTransfer?.nombre }}</strong>
            (id {{ pagoTransfer?.id }}) a otra persona/curso.
          </p>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nuevo Nombre</label>
              <input v-model="transferForm.nombre" />
            </div>
            <div class="row">
              <label>Nuevo RUT</label>
              <input v-model="transferForm.rut" />
            </div>
            <div class="row">
              <label>Nuevo Email</label>
              <input v-model="transferForm.email" />
            </div>
            <div class="row">
              <label>Nuevo Curso</label>
              <BaseSelect
                v-model="transferForm.curso"
                :options="cursoOptions"
              />
            </div>
            <div class="row full-width">
              <label>Tipo de Devolución</label>
              <div class="radio-row">
                <label>
                  <input
                    type="radio"
                    value="total"
                    v-model="transferForm.devolucionTipo"
                  />
                  Total
                </label>
                <label>
                  <input
                    type="radio"
                    value="parcial"
                    v-model="transferForm.devolucionTipo"
                  />
                  Parcial
                </label>
              </div>
            </div>
            <div
              class="row"
              v-if="transferForm.devolucionTipo === 'parcial'"
            >
              <label>Monto a devolver</label>
              <input
                type="number"
                min="0"
                v-model.number="transferForm.montoDevolucion"
              />
            </div>
          </div>

          <div class="confirm-actions">
            <BaseButton
              class="btn-main-outline"
              @click="modalTransferir = false"
            >
              Cancelar
            </BaseButton>
            <BaseButton
              class="btn-main"
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
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'

import pagosService from '@/services/pagosService.js'
import personasService from '@/services/personasService.js'

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
  name: 'Pagos',
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
      pagoTransfer: null,
      transferForm: {
        nombre: '',
        rut: '',
        email: '',
        curso: '',
        devolucionTipo: 'total',
        montoDevolucion: null
      }
    }
  },
  computed: {
    allChecked () {
      return (
        this.pagos.length > 0 &&
        this.seleccionadosHistorico.length === this.pagos.length
      )
    }
  },
  methods: {
    dateCL,

    async cargarCatalogos () {
      try {
        const mod = await import('@/services/cursosService.js')
        const svc = mod.default || mod
        const r = svc.cursos?.list
          ? await svc.cursos.list()
          : svc.list
            ? await svc.list()
            : []
        const arr = Array.isArray(r) ? r : r?.results || []
        this.cursoOptions = arr.map(x => ({
          value:
            x.id ??
            x.value ??
            x.CUR_ID ??
            String(x.nombre || x.label || 'curso'),
          label:
            x.nombre ??
            x.label ??
            x.CUR_NOMBRE ??
            `Curso ${x.id ?? ''}`.trim()
        }))
      } catch {
        this.cursoOptions = []
      }

      try {
        const modG = await import('@/services/usuariosService.js')
        const svcG = modG.default || modG
        const rG = svcG.grupos?.list
          ? await svcG.grupos.list()
          : svcG.listGrupos
            ? await svcG.listGrupos()
            : []
        const arrG = Array.isArray(rG) ? rG : rG?.results || []
        this.grupoOptions = arrG.map(g => ({
          value: g.id ?? g.value ?? g.GRU_ID ?? String(g.nombre || g.label),
          label:
            g.nombre ?? g.label ?? g.GRU_NOMBRE ?? `Grupo ${g.id ?? ''}`
        }))
      } catch {
        this.grupoOptions = []
      }
    },

    // INDIVIDUAL
    async buscarPersonas () {
      const q = (this.buscarPersonaQ || '').trim()
      if (!q) {
        this.personasEncontradas = []
        return
      }
      try {
        this.buscandoPersonas = true
        let r = []
        if (personasService.personas?.search) {
          r = await personasService.personas.search({ q })
        } else if (personasService.search) {
          r = await personasService.search({ q })
        }
        const arr = Array.isArray(r) ? r : r?.results || []
        this.personasEncontradas = arr.map(p => ({
          id: p.id ?? p.PER_ID ?? p.id_persona,
          nombre:
            p.nombre ??
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ??
            (p.PER_RUN && p.PER_DV
              ? `${p.PER_RUN}-${p.PER_DV}`
              : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }))
      } catch {
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
        if (!this.formInd.file) {
          throw new Error('Debe adjuntar comprobante')
        }

        const fd = new FormData()
        Object.entries(this.formInd).forEach(([k, v]) => {
          if (v !== null && v !== undefined) fd.append(k, v)
        })

        if (pagosService.pagos?.createIndividualForm) {
          await pagosService.pagos.createIndividualForm(fd)
        } else if (pagosService.createIndividualForm) {
          await pagosService.createIndividualForm(fd)
        } else if (pagosService.pagos?.create) {
          await pagosService.pagos.create(fd)
        } else {
          throw new Error('Endpoint no disponible para FormData')
        }

        alert('Pago individual registrado')
        this.limpiarIndividual()
        this.cargarPagos()
      } catch (e) {
        alert(
          'Error registrando pago individual: ' +
            (e?.message || 'ver consola')
        )
      }
    },

    // MASIVO
    onFileMasivo (e) {
      this.formMasivo.file = e.target.files?.[0] || null
    },
    async cargarParticipantes () {
      try {
        this.cargandoParticipantes = true
        let r = []
        if (personasService.personas?.byGrupoCurso) {
          r = await personasService.personas.byGrupoCurso({
            grupo: this.formMasivo.grupo,
            curso: this.formMasivo.curso
          })
        } else if (personasService.byGrupoCurso) {
          r = await personasService.byGrupoCurso({
            grupo: this.formMasivo.grupo,
            curso: this.formMasivo.curso
          })
        }
        const arr = Array.isArray(r) ? r : r?.results || []
        this.participantes = arr.map(p => ({
          id: p.id ?? p.PER_ID ?? p.id_persona,
          nombre:
            p.nombre ??
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ??
            (p.PER_RUN && p.PER_DV
              ? `${p.PER_RUN}-${p.PER_DV}`
              : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }))
        this.seleccionados = []
      } catch {
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
        if (!this.formMasivo.file) {
          throw new Error('Debe adjuntar comprobante grupal')
        }

        const payload = {
          grupo: this.formMasivo.grupo,
          curso: this.formMasivo.curso,
          valor_pagado: this.formMasivo.valor_pagado,
          fecha_pago: this.formMasivo.fecha_pago,
          observacion: this.formMasivo.observacion,
          participantes: this.seleccionados
        }

        const fd = new FormData()
        Object.entries(payload).forEach(([k, v]) => {
          if (k === 'participantes') {
            v.forEach(id => fd.append('participantes[]', id))
          } else if (v !== null && v !== undefined) {
            fd.append(k, v)
          }
        })
        fd.append('file', this.formMasivo.file)

        if (pagosService.pagos?.createMasivoForm) {
          await pagosService.pagos.createMasivoForm(fd)
        } else if (pagosService.createMasivoForm) {
          await pagosService.createMasivoForm(fd)
        } else {
          throw new Error(
            'Endpoint no disponible para masivo con FormData'
          )
        }

        alert('Pago masivo registrado')
        this.limpiarMasivo()
        this.cargarPagos()
      } catch (e) {
        alert(
          'Error registrando pago masivo: ' +
            (e?.message || 'ver consola')
        )
      }
    },

    // HISTÓRICO
    cursoLabel (id) {
      const c = this.cursoOptions.find(
        x => String(x.value) === String(id)
      )
      return c ? c.label : id
    },
    async cargarPagos () {
      try {
        this.cargandoPagos = true
        this.errorPagos = null
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
        this.pagos = Array.isArray(r) ? r : r?.results || []
      } catch (e) {
        this.pagos = []
        this.errorPagos =
          'No fue posible cargar pagos. Verifica la API.'
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
                `"${String(r[h] ?? '')
                  .replace(/"/g, '""')}"`
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
        `Enviando correos a IDs: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },

    // Acciones fila
    verDetalle (p) {
      alert(
        `Pago de ${p.nombre}\nMonto: $${(p.monto ??
          p.valor_pagado)?.toLocaleString(
          'es-CL'
        )}\nFecha: ${dateCL(p.fecha || p.fecha_pago)}`
      )
    },
    abrirTransferir (p) {
      this.pagoTransfer = p
      this.transferForm = {
        nombre: '',
        rut: '',
        email: '',
        curso: '',
        devolucionTipo: 'total',
        montoDevolucion: null
      }
      this.modalTransferir = true
    },
    async confirmarTransferencia () {
      try {
        const body = {
          pago_id: this.pagoTransfer.id,
          nuevo_nombre: this.transferForm.nombre,
          nuevo_rut: this.transferForm.rut,
          nuevo_email: this.transferForm.email,
          nuevo_curso: this.transferForm.curso,
          devolucion_tipo: this.transferForm.devolucionTipo,
          devolucion_monto:
            this.transferForm.devolucionTipo === 'parcial'
              ? this.transferForm.montoDevolucion
              : null
        }

        if (pagosService.pagos?.transferir) {
          await pagosService.pagos.transferir(body)
        } else if (pagosService.transferir) {
          await pagosService.transferir(body)
        } else {
          alert(
            'Simulación de transferencia. Implementa el endpoint pagos/transferir en la API.'
          )
        }

        this.modalTransferir = false
        await this.cargarPagos()
      } catch (e) {
        alert(
          'Error al transferir pago: ' +
            (e?.message || 'ver consola')
        )
      }
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
        } else if (pagosService.partialUpdate) {
          await pagosService.partialUpdate(
            this.pagoEdit.id,
            body
          )
        } else if (pagosService.pagos?.update) {
          await pagosService.pagos.update(
            this.pagoEdit.id,
            body
          )
        } else {
          throw new Error(
            'Endpoint no disponible para actualizar'
          )
        }
        this.modalEditar = false
        await this.cargarPagos()
        alert('Pago actualizado')
      } catch (e) {
        alert(
          'Error actualizando pago: ' +
            (e?.message || 'ver consola')
        )
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
        } else {
          throw new Error(
            'Endpoint no disponible para anular'
          )
        }
        this.modalAnular = false
        await this.cargarPagos()
        alert('Pago anulado')
      } catch (e) {
        alert(
          'Error al anular: ' +
            (e?.message || 'ver consola')
        )
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
  }
}
</script>

<style scoped>
/* CONTENEDOR PRINCIPAL MÁS GRANDE Y CÓMODO */
.gestion-pagos {
  box-sizing: border-box;
  margin: 24px auto 32px;
  padding: 24px 48px 40px;
  background: #ffffff;
  color: #111827;
  display: flex;
  flex-direction: column;
  gap: 18px;
  font-family: Arial, sans-serif;
  width: 1400px;                    /* más ancho */
  max-width: calc(100% - 64px);     /* respeta bordes de la pantalla */
  border-radius: 10px;
  box-shadow: 0 12px 36px rgba(15, 23, 42, 0.10);
}

.header h2 {
  background: #1d4ed8;
  color: #ffffff;
  padding: 16px 20px;
  border-radius: 8px;
  margin: 0 0 4px 0;
  text-align: center;
  font-size: 24px;
  font-weight: 600;
}

.tabs,
.subtabs {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.tabs button,
.subtabs button {
  padding: 8px 20px;
  border-radius: 20px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  color: #374151;
}

.tabs button.active,
.subtabs button.active {
  background: #1d4ed8;
  color: #ffffff;
  border-color: #1d4ed8;
}

.card {
  background: #ffffff;
  border-radius: 10px;
  padding: 18px 20px 22px;
  border: 1px solid #e5e7eb;
}

.subtabs {
  margin-top: 0;
  margin-bottom: 10px;
}

/* PANEL INTERNO MÁS AMPLIO */
.panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel-card {
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  padding: 20px 22px 26px;
  background: #f9fafb;
}

.panel-title.center {
  text-align: center;
}

.panel-title h4 {
  margin: 0;
  color: #1d4ed8;
  font-size: 19px;
  font-weight: 600;
}

.panel-subtitle {
  margin: 5px 0 10px;
  font-size: 13px;
  color: #6b7280;
}

/* Buscar */
.buscar-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 10px;
}

.buscar-row label {
  font-weight: 600;
  color: #1f2937;
  font-size: 13px;
}

.buscar-input-group {
  display: flex;
  gap: 10px;
  align-items: center;
  max-width: 620px;
}

.input-buscar {
  flex: 1;
}

/* GRID MÁS ESPACIOSO */
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px 24px;
  margin-top: 8px;
}

.grid-compact {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.col.small {
  max-width: 280px;
}

.col.tiny {
  max-width: 200px;
}

.col.auto {
  align-self: flex-end;
}

label {
  font-weight: 600;
  color: #1f2937;
  font-size: 13px;
}

.invisible {
  visibility: hidden;
}

.with-prefix {
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
  background: #ffffff;
}
.with-prefix .prefix {
  background: #e5e7eb;
  padding: 8px 10px;
  font-weight: 600;
  color: #374151;
  border-right: 1px solid #d1d5db;
}
.with-prefix input {
  border: none;
  padding: 7px 10px;
  flex: 1;
  outline: none;
  font-size: 13px;
}

/* Resultados búsqueda */
.resultados {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 4px;
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
  display: block;
}

.no-result {
  margin-top: 4px;
  font-size: 12px;
  color: #9ca3af;
}

/* Lista masivo */
.lista {
  margin-top: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
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
  padding: 7px 10px;
  border-bottom: 1px solid #f9fafb;
}
.item:last-child {
  border-bottom: none;
}
.item .info .muted {
  color: #6b7280;
  font-size: 11px;
  display: block;
}

/* Comentario centrado + más espacio */
.comment-block {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}
.comment-block label {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}
.comment-textarea {
  width: 75%;
  min-height: 70px;
  max-height: 120px;
  padding: 9px 11px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 13px;
  resize: vertical;
}

/* Comprobante + buen espacio con botones */
.file-block {
  margin-top: 14px;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
}

/* Botones */
.acciones {
  display: flex;
  gap: 10px;
}
.acciones.center {
  justify-content: center;
}
.acciones-bottom {
  margin-top: 20px;
}

/* Resumen masivo */
.resumen {
  margin-top: 12px;
  padding: 10px 14px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  display: flex;
  gap: 18px;
  justify-content: center;
  font-weight: 600;
  color: #1d4ed8;
}
.resumen .total {
  text-transform: uppercase;
}

/* Filtros + toolbar */
.filtros {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.filtro-input {
  min-width: 240px;
}
.toolbar {
  display: flex;
  gap: 8px;
  margin: 4px 0 10px;
}
.toolbar-btn {
  padding: 7px 14px;
  border-radius: 6px;
  background: #1d4ed8;
  color: #ffffff;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}
.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Tabla */
.table-wrapper {
  overflow: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
}
th,
td {
  padding: 10px 9px;
  border-bottom: 1px solid #f3f4f6;
  text-align: left;
  font-size: 13px;
}
th {
  background: #f9fafb;
  position: sticky;
  top: 0;
  z-index: 1;
  font-weight: 600;
  color: #4b5563;
}
.placeholder {
  text-align: center;
  color: #6b7280;
  padding: 24px 8px;
}

/* Estados */
.estado-carga {
  text-align: left;
  padding: 4px 0;
  color: #6b7280;
  font-style: italic;
  font-size: 12px;
}
.mensaje-error {
  background: #fee2e2;
  color: #b91c1c;
  padding: 8px;
  border-radius: 6px;
  margin-top: 4px;
  font-size: 13px;
}

/* Botones base en azul */
.btn-main {
  background: #1d4ed8 !important;
  color: #ffffff !important;
  border-radius: 6px !important;
  border: none !important;
  padding: 7px 14px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}
.btn-main-outline {
  background: #ffffff !important;
  color: #1d4ed8 !important;
  border-radius: 6px !important;
  border: 1px solid #1d4ed8 !important;
  padding: 7px 14px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}
.btn-sec {
  background: #e5e7eb !important;
  color: #111827 !important;
  border-radius: 6px !important;
  padding: 4px 10px !important;
  font-size: 12px !important;
}
.btn-sm {
  padding: 4px 9px !important;
  font-size: 11px !important;
}

.acciones-buttons {
  display: flex;
  gap: 4px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-start;
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
.modal-edit {
  width: 640px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 80px);
  overflow: auto;
  padding: 18px 22px 20px;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}
.modal-header h3 {
  margin: 0;
  color: #1d4ed8;
}
.form-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 16px;
}
.row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
}
.row.full-width {
  grid-column: 1 / -1;
}
.row input,
.row select {
  padding: 7px 9px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
}
.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px;
  text-align: center;
}
.confirm-icon {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: #fee2e2;
  color: #b91c1c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin-bottom: 4px;
}
.confirm-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
}
.modal-note {
  font-size: 12px;
  color: #6b7280;
  margin: 0 0 8px;
}
.radio-row {
  display: flex;
  gap: 14px;
  font-size: 13px;
}

@media (max-width: 900px) {
  .grid-compact {
    grid-template-columns: 1fr 1fr;
  }
  .comment-textarea {
    width: 100%;
  }
}
</style>
