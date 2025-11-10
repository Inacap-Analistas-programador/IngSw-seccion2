<template>
  <div class="gestion-pagos">
    <!-- ENCABEZADO -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
      <h3>Registro Individual, Masivo y Consulta</h3>
    </header>

    <!-- PESTAÑAS -->
    <div class="tabs">
      <button :class="{ active: tab === 'registro' }" @click="tab = 'registro'">
        Registro
      </button>
      <button :class="{ active: tab === 'historico' }" @click="tab = 'historico'">
        Histórico
      </button>
    </div>

    <!-- ===================== REGISTRO ===================== -->
    <div v-if="tab === 'registro'" class="card">
      <!-- SUBTABS -->
      <div class="subtabs">
        <button :class="{ active: subTab === 'individual' }" @click="subTab = 'individual'">
          Individual
        </button>
        <button :class="{ active: subTab === 'masivo' }" @click="subTab = 'masivo'">
          Masivo
        </button>
      </div>

      <!-- ===================== INDIVIDUAL ===================== -->
      <section v-if="subTab === 'individual'" class="panel">
        <div class="subheader-box">
          <h4>Registro Individual de Pagos</h4>
          <p>Busca un participante, selecciona el curso y registra el pago.</p>
        </div>

        <!-- Buscar persona -->
        <div class="grid-ind">
          <div class="col full">
            <label>Buscar Participante (Nombre / RUT / Email)</label>
            <InputBase
              v-model="buscarPersonaQ"
              placeholder="Ej: 12.345.678-9 o Juan Pérez"
              @keydown.enter.prevent="buscarPersonas"
            />
            <div class="acciones mt-4">
              <button
                type="button"
                class="btn btn-primary"
                @click="buscarPersonas"
              >
                Buscar
              </button>
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
                  <strong class="txt-small">{{ p.nombre }}</strong>
                  <span class="muted txt-small">
                    {{ p.rut }} · {{ p.email }}
                  </span>
                </div>
                <button type="button" class="btn btn-light-sm">
                  Elegir
                </button>
              </div>
            </div>

            <div
              v-else-if="buscarPersonaQ && !buscandoPersonas"
              class="no-result"
            >
              Sin resultados
            </div>
          </div>

          <!-- Datos compactos -->
          <div class="col">
            <label>Nombre</label>
            <InputBase
              v-model="formInd.nombre"
              readonly
              class="small-field"
            />
          </div>
          <div class="col">
            <label>RUT</label>
            <InputBase
              v-model="formInd.rut"
              readonly
              class="small-field"
            />
          </div>
          <div class="col">
            <label>Email</label>
            <InputBase
              v-model="formInd.email"
              readonly
              class="small-field"
            />
          </div>
          <div class="col">
            <label>Curso / Capacitación *</label>
            <BaseSelect
              v-model="formInd.curso"
              :options="cursoOptions"
              placeholder="Seleccione curso"
              class="small-field"
            />
          </div>
          <div class="col">
            <label>Valor Pagado *</label>
            <div class="with-prefix small-input">
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
            <InputBase
              type="date"
              v-model="formInd.fecha_pago"
              class="small-field"
            />
          </div>
          <div class="col full">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              v-model="formInd.observacion"
              class="textarea"
              maxlength="200"
              placeholder="Detalle del pago, referencia de transferencia, etc."
            ></textarea>
          </div>
          <div class="col full">
            <label>Comprobante (opcional)</label>
            <input
              ref="fileIndRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileInd"
            />
          </div>
        </div>

        <!-- Acciones individual -->
        <div class="acciones center mt-10">
          <button
            type="button"
            class="btn btn-primary"
            :disabled="!formInd.personaId || !formInd.curso || !formInd.valor_pagado || !formInd.fecha_pago"
            @click="registrarPagoIndividual"
          >
            Registrar Pago Individual
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            @click="limpiarIndividual"
          >
            Limpiar
          </button>
        </div>
      </section>

      <!-- ===================== MASIVO ===================== -->
      <section v-else class="panel">
        <div class="subheader-box">
          <h4>Registro Masivo de Pagos</h4>
          <p>Seleccione grupo, curso, participantes y registre un pago masivo.</p>
        </div>

        <!-- Fila grupo / curso / cargar -->
        <div class="grid">
          <div class="col">
            <label>Grupo *</label>
            <BaseSelect
              v-model="formMasivo.grupo"
              :options="grupoOptions"
              placeholder="Seleccione grupo"
              class="small-field"
            />
          </div>
          <div class="col">
            <label>Curso/Capacitación *</label>
            <BaseSelect
              v-model="formMasivo.curso"
              :options="cursoOptions"
              placeholder="Seleccione curso"
              class="small-field"
            />
          </div>
          <div class="col auto">
            <label class="invisible">Cargar</label>
            <button
              type="button"
              class="btn btn-primary w-100"
              :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoParticipantes"
              @click="cargarParticipantes"
            >
              {{ cargandoParticipantes ? 'Cargando participantes...' : 'Cargar participantes' }}
            </button>
          </div>
        </div>

        <!-- Lista participantes -->
        <div v-if="participantes.length" class="lista">
          <div class="lista-header">
            <h5>Participantes disponibles ({{ participantes.length }})</h5>
            <div class="acciones">
              <button
                type="button"
                class="btn btn-light-sm"
                @click="selectAll"
              >
                Seleccionar todos
              </button>
              <button
                type="button"
                class="btn btn-light-sm"
                @click="unselectAll"
              >
                Deseleccionar
              </button>
            </div>
          </div>
          <div class="lista-items">
            <label
              v-for="u in participantes"
              :key="u.id"
              class="item"
            >
              <input
                type="checkbox"
                :value="u.id"
                v-model="seleccionados"
              />
              <div class="info">
                <strong class="txt-small">{{ u.nombre }}</strong>
                <span class="muted txt-small">
                  {{ u.rut }} · {{ u.email }}
                </span>
              </div>
            </label>
          </div>
        </div>

        <!-- Form masivo -->
        <div v-if="seleccionados.length" class="grid mt-10">
          <div class="col">
            <label>Valor por Persona *</label>
            <div class="with-prefix small-input">
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
            <InputBase
              type="date"
              v-model="formMasivo.fecha_pago"
              class="small-field"
            />
          </div>

          <div class="col full">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              v-model="formMasivo.observacion"
              class="textarea"
              maxlength="200"
              placeholder="Detalle del pago masivo, referencia, etc."
            ></textarea>
          </div>

          <div class="col full">
            <label>Comprobante Grupal (opcional)</label>
            <input
              ref="fileMasivoRef"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="onFileMasivo"
            />
          </div>
        </div>

        <!-- Resumen -->
        <div
          class="resumen"
          v-if="seleccionados.length && formMasivo.valor_pagado"
        >
          <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
          <div>
            Valor por persona:
            <strong>${{ formMasivo.valor_pagado.toLocaleString('es-CL') }}</strong>
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

        <!-- Acciones masivo -->
        <div
          class="acciones center"
          v-if="seleccionados.length"
        >
          <button
            type="button"
            class="btn btn-primary"
            :disabled="!formMasivo.valor_pagado || !formMasivo.fecha_pago"
            @click="registrarPagoMasivo"
          >
            Registrar Pago Masivo
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            @click="limpiarMasivo"
          >
            Limpiar
          </button>
        </div>
      </section>
    </div>

    <!-- ===================== HISTÓRICO ===================== -->
    <div v-else class="card">
      <div class="subheader-box">
        <h4>Histórico de Pagos</h4>
        <p>Consulta, exporta y gestiona los pagos registrados.</p>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <InputBase
          v-model="filtroQ"
          placeholder="Nombre / RUT / Email"
          @keydown.enter.prevent="cargarPagos"
          class="small-field"
        />
        <BaseSelect
          v-model="filtroCurso"
          :options="[{ value: '', label: 'Todos los cursos' }, ...cursoOptions]"
          class="small-field"
        />
        <BaseSelect
          v-model="filtroGrupo"
          :options="[{ value: '', label: 'Todos los grupos' }, ...grupoOptions]"
          class="small-field"
        />
        <button
          type="button"
          class="btn btn-primary"
          @click="cargarPagos"
        >
          Buscar
        </button>
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <button
          type="button"
          class="btn btn-outline"
          @click="exportarCSV"
        >
          <span class="btn-icon">⬇️</span> Exportar Correos
        </button>
        <button
          type="button"
          class="btn btn-primary"
          :disabled="!seleccionadosHistorico.length"
          @click="marcarEnviado"
        >
          <span class="btn-icon">✓</span> Marcar Enviado
        </button>
        <button
          type="button"
          class="btn btn-blue"
          :disabled="!seleccionadosHistorico.length"
          @click="enviarPorCorreo"
        >
          <span class="btn-icon">✈️</span> Enviar por correo
        </button>
      </div>

      <!-- Estado -->
      <div v-if="cargandoPagos" class="estado-carga">
        Cargando pagos...
      </div>
      <div v-if="errorPagos" class="mensaje-error">
        {{ errorPagos }}
        <div>
          <button
            type="button"
            class="btn btn-primary mt-6"
            @click="cargarPagos"
          >
            Reintentar
          </button>
        </div>
      </div>

      <!-- Tabla -->
      <div
        class="table-wrapper"
        v-if="!cargandoPagos"
      >
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
              <th class="th-nombre">Nombre</th>
              <th class="th-rut">RUT</th>
              <th class="th-curso">Curso</th>
              <th class="th-monto">Monto</th>
              <th>Fecha</th>
              <th>Método</th>
              <th style="width: 260px;">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="p in pagos"
              :key="p.id"
            >
              <td>
                <input
                  type="checkbox"
                  :value="p.id"
                  v-model="seleccionadosHistorico"
                />
              </td>
              <td class="td-nombre">
                <strong>{{ p.nombre }}</strong>
              </td>
              <td class="td-rut">
                {{ p.rut }}
              </td>
              <td class="td-curso">
                {{ cursoLabel(p.curso) }}
              </td>
              <td class="td-monto">
                ${{ (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL') }}
              </td>
              <td>{{ dateCL(p.fecha || p.fecha_pago) }}</td>
              <td>{{ p.metodo || 'Transferencia' }}</td>
              <td class="acciones-buttons">
                <button
                  type="button"
                  class="btn-action btn-view"
                  @click="verDetalle(p)"
                >
                  <span class="icon">👁</span> Ver
                </button>
                <button
                  type="button"
                  class="btn-action btn-edit"
                  @click="abrirEditar(p)"
                >
                  <span class="icon">✏</span> Editar
                </button>
                <button
                  type="button"
                  class="btn-action btn-cancel"
                  @click="abrirAnular(p)"
                >
                  <span class="icon">⛔</span> Anular
                </button>
                <button
                  v-if="p.comprobante_url || p.comprobante"
                  type="button"
                  class="btn-action btn-doc"
                  @click="descargarComprobante(p)"
                >
                  <span class="icon">📄</span> Comprobante
                </button>
              </td>
            </tr>
            <tr v-if="!pagos.length">
              <td
                colspan="8"
                class="placeholder"
              >
                No hay pagos para mostrar
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL EDITAR -->
    <BaseModal v-model="modalEditar" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="guardando"
              @click="guardarEdicion"
            >
              {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <input v-model="pagoEdit.nombre" readonly class="small-field" />
            </div>
            <div class="row">
              <label>RUT</label>
              <input v-model="pagoEdit.rut" readonly class="small-field" />
            </div>
            <div class="row">
              <label>Curso</label>
              <BaseSelect
                v-model="pagoEdit.curso"
                :options="cursoOptions"
                class="small-field"
              />
            </div>
            <div class="row">
              <label>Monto</label>
              <input
                type="number"
                v-model.number="pagoEdit.monto"
                class="small-field"
              />
            </div>
            <div class="row">
              <label>Fecha</label>
              <input
                type="date"
                v-model="pagoEdit.fecha"
                class="small-field"
              />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <input
                v-model="pagoEdit.observacion"
                maxlength="200"
              />
            </div>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- MODAL ANULAR -->
    <BaseModal v-model="modalAnular" title="Confirmar Anulación">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">⚠️</div>
          <p>
            ¿Anular pago de
            <strong>{{ pagoAnular?.nombre }}</strong>?
          </p>
          <div class="confirm-actions">
            <button
              type="button"
              class="btn btn-secondary"
              @click="modalAnular = false"
            >
              Cancelar
            </button>
            <button
              type="button"
              class="btn btn-cancel-strong"
              @click="confirmarAnulacion"
            >
              Anular
            </button>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script>
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'

const API_BASE = 'http://localhost:8000/api' // ajusta si tu API expone otro path

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
async function fetchJSON (url, options = {}) {
  const token = localStorage.getItem('authToken')
  const headers = {
    ...(options.headers || {}),
    Accept: 'application/json'
  }
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] =
      headers['Content-Type'] || 'application/json'
  }
  if (token) {
    headers.Authorization = `Token ${token}`
  }
  const res = await fetch(url, { ...options, headers })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(txt || `Error HTTP ${res.status}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export default {
  name: 'Pagos',
  components: { InputBase, BaseSelect, BaseModal },
  data () {
    return {
      tab: 'registro',
      subTab: 'individual',

      cursoOptions: [],
      grupoOptions: [],

      // Individual
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

      // Masivo
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

      // Histórico
      filtroQ: '',
      filtroCurso: '',
      filtroGrupo: '',
      pagos: [],
      cargandoPagos: false,
      errorPagos: null,
      seleccionadosHistorico: [],

      // Modales
      modalEditar: false,
      pagoEdit: {},
      guardando: false,

      modalAnular: false,
      pagoAnular: null
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

    // ==== Catálogos ====
    async cargarCatalogos () {
      try {
        const data = await fetchJSON(`${API_BASE}/cursos/`)
        const arr = Array.isArray(data) ? data : (data.results || [])
        this.cursoOptions = arr.map(c => ({
          value: c.id,
          label: c.nombre || c.descripcion || `Curso ${c.id}`
        }))
      } catch {
        this.cursoOptions = []
      }

      try {
        const dataG = await fetchJSON(`${API_BASE}/grupos/`)
        const arrG = Array.isArray(dataG) ? dataG : (dataG.results || [])
        this.grupoOptions = arrG.map(g => ({
          value: g.id,
          label: g.nombre || g.descripcion || `Grupo ${g.id}`
        }))
      } catch {
        this.grupoOptions = []
      }
    },

    // ==== Individual ====
    async buscarPersonas () {
      const q = (this.buscarPersonaQ || '').trim()
      if (!q) {
        this.personasEncontradas = []
        return
      }
      this.buscandoPersonas = true
      try {
        const url = `${API_BASE}/personas/?q=${encodeURIComponent(q)}`
        const data = await fetchJSON(url)
        const arr = Array.isArray(data) ? data : (data.results || [])
        this.personasEncontradas = arr.map(p => ({
          id: p.id,
          nombre:
            p.nombre ||
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ||
            (p.PER_RUN && p.PER_DV
              ? `${p.PER_RUN}-${p.PER_DV}`
              : ''),
          email: p.email || p.PER_MAIL || ''
        }))
      } catch {
        this.personasEncontradas = []
        alert('Error al buscar personas. Revisa /api/personas/.')
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
      if (this.$refs.fileIndRef) this.$refs.fileIndRef.value = ''
    },
    async registrarPagoIndividual () {
      try {
        const payload = {
          persona: this.formInd.personaId,
          curso: this.formInd.curso,
          valor_pagado: this.formInd.valor_pagado,
          fecha_pago: this.formInd.fecha_pago,
          observacion: this.formInd.observacion
        }

        let options
        if (this.formInd.file) {
          const fd = new FormData()
          Object.entries(payload).forEach(([k, v]) => {
            if (v !== null && v !== undefined) fd.append(k, v)
          })
          fd.append('file', this.formInd.file)
          options = { method: 'POST', body: fd }
        } else {
          options = {
            method: 'POST',
            body: JSON.stringify(payload)
          }
        }

        // Ajusta URL según tu backend: aquí se asume /pagos/individual/
        await fetchJSON(`${API_BASE}/pagos/individual/`, options)
        alert('Pago individual registrado correctamente')
        this.limpiarIndividual()
      } catch {
        alert(
          'Error registrando pago individual. Ajusta la URL /api/pagos/individual/ según tu API.'
        )
      }
    },

    // ==== Masivo ====
    onFileMasivo (e) {
      this.formMasivo.file = e.target.files?.[0] || null
    },
    async cargarParticipantes () {
      if (!this.formMasivo.grupo || !this.formMasivo.curso) return
      this.cargandoParticipantes = true
      try {
        const url = `${API_BASE}/personas/?grupo=${encodeURIComponent(
          this.formMasivo.grupo
        )}&curso=${encodeURIComponent(this.formMasivo.curso)}`
        const data = await fetchJSON(url)
        const arr = Array.isArray(data) ? data : (data.results || [])
        this.participantes = arr.map(p => ({
          id: p.id,
          nombre:
            p.nombre ||
            `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut:
            p.rut ||
            (p.PER_RUN && p.PER_DV
              ? `${p.PER_RUN}-${p.PER_DV}`
              : ''),
          email: p.email || p.PER_MAIL || ''
        }))
        this.seleccionados = []
      } catch {
        this.participantes = []
        alert('Error cargando participantes. Revisa /api/personas/.')
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
      if (this.$refs.fileMasivoRef) this.$refs.fileMasivoRef.value = ''
    },
    async registrarPagoMasivo () {
      try {
        const payload = {
          grupo: this.formMasivo.grupo,
          curso: this.formMasivo.curso,
          valor_pagado: this.formMasivo.valor_pagado,
          fecha_pago: this.formMasivo.fecha_pago,
          observacion: this.formMasivo.observacion,
          participantes: this.seleccionados
        }

        let options
        if (this.formMasivo.file) {
          const fd = new FormData()
          Object.entries(payload).forEach(([k, v]) => {
            if (k === 'participantes') {
              v.forEach(id => fd.append('participantes', id))
            } else if (v !== null && v !== undefined) {
              fd.append(k, v)
            }
          })
          fd.append('file', this.formMasivo.file)
          options = { method: 'POST', body: fd }
        } else {
          options = {
            method: 'POST',
            body: JSON.stringify(payload)
          }
        }

        // Ajusta según tu API (ejemplo: /pagos/masivo/)
        await fetchJSON(`${API_BASE}/pagos/masivo/`, options)
        alert('Pago masivo registrado correctamente')
        this.limpiarMasivo()
      } catch {
        alert(
          'Error registrando pago masivo. Ajusta la URL /api/pagos/masivo/ según tu API.'
        )
      }
    },

    // ==== Histórico ====
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
        const params = new URLSearchParams()
        if (this.filtroQ) params.append('q', this.filtroQ.trim())
        if (this.filtroCurso) params.append('curso', this.filtroCurso)
        if (this.filtroGrupo) params.append('grupo', this.filtroGrupo)
        const url = `${API_BASE}/pagos/${
          params.toString() ? `?${params.toString()}` : ''
        }`
        const data = await fetchJSON(url)
        this.pagos = Array.isArray(data) ? data : (data.results || [])
      } catch {
        this.errorPagos =
          'No fue posible cargar pagos. Verifica la API /api/pagos/.'
        this.pagos = []
      } finally {
        this.cargandoPagos = false
      }
    },
    exportarCSV () {
      if (!this.pagos.length) {
        alert('No hay datos para exportar.')
        return
      }
      const rows = this.pagos.map(p => ({
        Nombre: p.nombre,
        RUT: p.rut,
        Curso: this.cursoLabel(p.curso),
        Monto: p.monto ?? p.valor_pagado,
        Fecha: dateCL(p.fecha || p.fecha_pago),
        Metodo: p.metodo || 'Transferencia'
      }))
      const headers = Object.keys(rows[0])
      const csv = [
        headers.join(','),
        ...rows.map(r =>
          headers
            .map(h =>
              `"${String(r[h] ?? '')
                .replace(/"/g, '""')}"`
            )
            .join(',')
        )
      ].join('\r\n')
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
        `Simulación envío correos a IDs: ${this.seleccionadosHistorico.join(
          ', '
        )}`
      )
    },

    // ==== Acciones fila ====
    verDetalle (p) {
      alert(
        `Pago de ${p.nombre}\nMonto: $${
          (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL') || 0
        }\nFecha: ${dateCL(p.fecha || p.fecha_pago)}`
      )
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
        await fetchJSON(`${API_BASE}/pagos/${this.pagoEdit.id}/`, {
          method: 'PATCH',
          body: JSON.stringify(body)
        })
        this.modalEditar = false
        await this.cargarPagos()
        alert('Pago actualizado correctamente')
      } catch {
        alert(
          'Error actualizando pago. Revisa /api/pagos/<id>/ (PATCH) en el backend.'
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
      if (!this.pagoAnular) return
      try {
        await fetchJSON(
          `${API_BASE}/pagos/${this.pagoAnular.id}/anular/`,
          { method: 'POST' }
        )
        this.modalAnular = false
        await this.cargarPagos()
        alert('Pago anulado correctamente')
      } catch {
        alert(
          'Error al anular. Ajusta la URL si tu API usa otro endpoint.'
        )
      }
    },
    descargarComprobante (p) {
      const url = p.comprobante_url || p.comprobante
      if (!url) {
        alert('No hay comprobante disponible.')
        return
      }
      window.open(url, '_blank')
    }
  },
  async mounted () {
    await this.cargarCatalogos()
    await this.cargarPagos()
  }
}
</script>

<style scoped>
.gestion-pagos {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px;
  background: #ffffff;
  color: #111827;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: Arial, sans-serif;
  width: 1200px;
  max-width: calc(100% - 48px);
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(16, 24, 40, 0.08);
}

.header h2 {
  background: #214e9c;
  color: #ffffff;
  padding: 14px 18px;
  border-radius: 6px;
  margin: 0 0 4px 0;
  text-align: center;
}
.header h3 {
  margin: 6px 0 0 0;
  color: #4b5563;
  font-weight: 500;
  text-align: center;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.tabs button {
  padding: 6px 14px;
  border-radius: 18px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  cursor: pointer;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
}
.tabs button.active {
  background: #214e9c;
  color: #ffffff;
  border-color: #214e9c;
}

/* Subtabs */
.subtabs {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.subtabs button {
  padding: 5px 12px;
  border-radius: 14px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
}
.subtabs button.active {
  background: #214e9c;
  color: #ffffff;
  border-color: #214e9c;
}

/* Card + subheader boxes */
.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}
.subheader-box {
  border: 2px solid #214e9c;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 12px;
  background: #eff6ff;
}
.subheader-box h4 {
  margin: 0;
  color: #1f2937;
  font-size: 17px;
}
.subheader-box p {
  margin: 2px 0 0;
  color: #6b7280;
  font-size: 12px;
}

/* Panel */
.panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Grids */
.grid,
.grid-ind {
  display: grid;
  grid-template-columns: 1.3fr 1.3fr 1fr;
  gap: 10px;
}
.grid .col,
.grid-ind .col {
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
  color: #1f2937;
  font-size: 12px;
}
.invisible {
  visibility: hidden;
}

/* Campos compactos */
.small-field {
  max-width: 220px;
}
.small-input {
  max-width: 160px;
}
.txt-small {
  font-size: 11px;
}

/* with-prefix */
.with-prefix {
  display: flex;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}
.with-prefix .prefix {
  background: #f3f4f6;
  padding: 6px 8px;
  font-weight: 600;
  color: #4b5563;
  border-right: 1px solid #e5e7eb;
}
.with-prefix input {
  border: none;
  padding: 6px 8px;
  flex: 1;
  outline: none;
  font-size: 12px;
}

/* Textarea */
.textarea {
  width: 100%;
  min-height: 70px;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  resize: vertical;
  font-family: inherit;
  font-size: 12px;
}

/* Lista participantes */
.lista {
  margin-top: 8px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}
.lista-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}
.lista-items {
  max-height: 220px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.item {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 6px 10px;
  border-bottom: 1px solid #f3f4f6;
}
.item:last-child {
  border-bottom: none;
}
.item .info .muted {
  color: #6b7280;
  font-size: 10px;
  display: block;
}

/* Resumen */
.resumen {
  margin-top: 10px;
  padding: 8px 12px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #93c5fd;
  border-radius: 8px;
  display: flex;
  gap: 14px;
  justify-content: center;
  font-weight: 600;
  color: #1d4ed8;
  font-size: 12px;
}
.resumen .total {
  text-transform: uppercase;
}

/* Filtros + toolbar */
.filtros {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

/* Botones base */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid transparent;
  cursor: pointer;
  font-size: 12px;
  background: #e5e7eb;
  color: #111827;
  transition: background 0.15s, transform 0.02s;
}
.btn:active {
  transform: translateY(1px);
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-primary {
  background: #1e40af;
  color: #ffffff;
  border-color: #1e40af;
}
.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
}
.btn-secondary {
  background: #6b7280;
  color: #ffffff;
  border-color: #6b7280;
}
.btn-outline {
  background: #f3f4f6;
  color: #111827;
  border-color: #d1d5db;
}
.btn-blue {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}
.btn-light-sm {
  padding: 3px 8px;
  font-size: 11px;
  background: #f9fafb;
  border-color: #e5e7eb;
}
.btn-cancel-strong {
  background: #dc2626;
  color: #ffffff;
  border-color: #b91c1c;
}
.btn-icon {
  font-size: 12px;
}

/* Tabla */
.table-wrapper {
  overflow: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
  font-size: 12px;
}
th,
td {
  padding: 8px 8px;
  border-bottom: 1px solid #f3f4f6;
  text-align: left;
}

/* Encabezados compactos */
.th-nombre { width: 150px; }
.th-rut { width: 90px; }
.th-curso { width: 140px; }
.th-monto { width: 90px; }

/* Celdas compactas */
.td-nombre,
.td-rut,
.td-curso,
.td-monto {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.placeholder {
  text-align: center;
  color: #6b7280;
  padding: 24px 10px;
}

/* Estados */
.estado-carga {
  text-align: center;
  padding: 8px;
  color: #4b5563;
  font-style: italic;
}
.mensaje-error {
  background: #fef2f2;
  color: #b91c1c;
  padding: 8px;
  border: 1px solid #fecaca;
  border-radius: 6px;
  text-align: center;
}

/* Acciones fila */
.acciones {
  display: flex;
  gap: 8px;
}
.acciones.center {
  justify-content: center;
}
.acciones-buttons {
  display: flex;
  gap: 4px;
  align-items: center;
  flex-wrap: wrap;
}
.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 7px;
  font-size: 10px;
  border-radius: 14px;
  border: 1px solid transparent;
  cursor: pointer;
  background: #ffffff;
}
.btn-action .icon {
  font-size: 11px;
}
.btn-view {
  border-color: #bfdbfe;
  color: #1d4ed8;
  background: #eff6ff;
}
.btn-edit {
  border-color: #feecc8;
  color: #b45309;
  background: #fffbeb;
}
.btn-cancel {
  border-color: #fecaca;
  color: #b91c1c;
  background: #fef2f2;
}
.btn-doc {
  border-color: #d1d5db;
  color: #374151;
  background: #f9fafb;
}

/* Modal */
.pago-modal :deep(.modal-overlay) {
  position: fixed !important;
  inset: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 9999 !important;
}
.modal-edit {
  width: 540px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 80px);
  overflow: auto;
  padding: 16px 20px;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}
.modal-header h3 {
  margin: 0;
  color: #214e9c;
}
.form-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 12px;
}
.row {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.row.full-width {
  grid-column: 1 / -1;
}
.row input,
.row select {
  padding: 6px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
}

/* Modal anulación */
.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 18px;
}
.confirm-icon {
  font-size: 40px;
  margin-bottom: 6px;
}
.confirm-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

/* Utils */
.mt-4 {
  margin-top: 4px;
}
.mt-6 {
  margin-top: 6px;
}
.mt-10 {
  margin-top: 10px;
}
.w-100 {
  width: 100%;
}

/* Responsive */
@media (max-width: 860px) {
  .grid,
  .grid-ind {
    grid-template-columns: 1fr;
  }
  .acciones-buttons {
    justify-content: flex-start;
  }
}
</style>


