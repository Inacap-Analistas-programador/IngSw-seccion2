<template>
  <div class="gestion-pagos">
    <!-- Encabezado -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
      <h3>Registro Individual / Masivo y Consulta</h3>
    </header>

    <!-- Pestañas -->
    <div class="tabs">
      <button :class="{active: tab==='registro'}" @click="tab='registro'">🧾 Registro</button>
      <button :class="{active: tab==='historico'}" @click="tab='historico'">📑 Histórico</button>
    </div>

    <!-- ===================== REGISTRO ===================== -->
    <div v-if="tab==='registro'" class="card">
      <div class="subtabs">
        <button :class="{active: subTab==='individual'}" @click="subTab='individual'">👤 Individual</button>
        <button :class="{active: subTab==='masivo'}" @click="subTab='masivo'">👥 Masivo</button>
      </div>

      <!-- -------- Registro Individual -------- -->
      <section v-if="subTab==='individual'" class="panel">
        <div class="panel-title">
          <h4>Registro Individual</h4>
          <p>Solo se permite <strong>Transferencia bancaria</strong>.</p>
        </div>

        <div class="grid">
          <div class="col full">
            <label>Buscar Participante (Nombre / RUT / Email)</label>
            <InputBase v-model="buscarPersonaQ" placeholder="Ej: 12.345.678-9 o Juan Pérez" @keydown.enter.prevent="buscarPersonas" />
            <div class="acciones">
              <BaseButton variant="primary" class="btn-search" @click="buscarPersonas">🔎 Buscar</BaseButton>
            </div>

            <div v-if="buscandoPersonas" class="estado-carga">🔄 Buscando personas...</div>
            <div v-if="personasEncontradas.length" class="resultados">
              <div v-for="p in personasEncontradas" :key="p.id" class="resultado" @click="seleccionarPersona(p)">
                <div class="resultado-left">
                  <strong>{{ p.nombre }}</strong>
                  <span class="muted">{{ p.rut }} · {{ p.email }}</span>
                </div>
                <BaseButton size="sm" variant="secondary">Elegir</BaseButton>
              </div>
            </div>
            <div v-else-if="buscarPersonaQ && !buscandoPersonas" class="no-result">Sin resultados</div>
          </div>

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
            <label>Curso/Capacitación *</label>
            <BaseSelect v-model="formInd.curso" :options="cursoOptions" placeholder="Seleccione un curso" />
          </div>
          <div class="col">
            <label>Valor Pagado *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input type="number" min="0" step="1" v-model.number="formInd.valor_pagado" />
            </div>
          </div>
          <div class="col">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formInd.fecha_pago" />
          </div>
          <div class="col">
            <label>Método de Pago</label>
            <div class="badge">Transferencia bancaria</div>
          </div>
          <div class="col full">
            <label>Observación</label>
            <InputBase v-model="formInd.observacion" placeholder="Comentario (opcional)" />
          </div>
          <div class="col full">
            <label>Comprobante (opcional)</label>
            <input ref="fileIndRef" type="file" accept=".pdf,.jpg,.jpeg,.png" @change="onFileInd" />
          </div>
        </div>

        <div class="acciones center">
          <BaseButton
            variant="primary"
            :disabled="!formInd.personaId || !formInd.curso || !formInd.valor_pagado || !formInd.fecha_pago"
            @click="registrarPagoIndividual"
          >
            ✅ Registrar Pago
          </BaseButton>
          <BaseButton variant="secondary" @click="limpiarIndividual">🧹 Limpiar</BaseButton>
        </div>
      </section>

      <!-- -------- Registro Masivo -------- -->
      <section v-else class="panel">
        <div class="panel-title">
          <h4>Registro Masivo</h4>
          <p>Adjunta comprobante grupal y selecciona participantes.</p>
        </div>

        <div class="grid">
          <div class="col">
            <label>Grupo *</label>
            <BaseSelect v-model="formMasivo.grupo" :options="grupoOptions" placeholder="Seleccione grupo" />
          </div>
          <div class="col">
            <label>Curso/Capacitación *</label>
            <BaseSelect v-model="formMasivo.curso" :options="cursoOptions" placeholder="Seleccione curso" />
          </div>
          <div class="col auto">
            <label class="invisible">Cargar</label>
            <BaseButton variant="info" :disabled="!formMasivo.grupo || !formMasivo.curso || cargandoParticipantes" @click="cargarParticipantes">
              {{ cargandoParticipantes ? '⏳ Cargando...' : '👥 Cargar Participantes' }}
            </BaseButton>
          </div>
        </div>

        <div v-if="participantes.length" class="lista">
          <div class="lista-header">
            <h5>Participantes disponibles ({{ participantes.length }})</h5>
            <div class="acciones">
              <BaseButton size="sm" variant="secondary" @click="selectAll">Seleccionar todos</BaseButton>
              <BaseButton size="sm" variant="secondary" @click="unselectAll">Deseleccionar</BaseButton>
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

        <div v-if="seleccionados.length" class="grid">
          <div class="col">
            <label>Valor por Persona *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input type="number" min="0" step="1" v-model.number="formMasivo.valor_pagado" />
            </div>
          </div>
          <div class="col">
            <label>Fecha de Pago *</label>
            <InputBase type="date" v-model="formMasivo.fecha_pago" />
          </div>
          <div class="col full">
            <label>Observación (aplica a todos)</label>
            <InputBase v-model="formMasivo.observacion" placeholder="Comentario (opcional)" />
          </div>
          <div class="col full">
            <label>Comprobante Grupal *</label>
            <input ref="fileMasivoRef" type="file" accept=".pdf,.jpg,.jpeg,.png" @change="onFileMasivo" />
          </div>
        </div>

        <div class="resumen" v-if="seleccionados.length && formMasivo.valor_pagado">
          <div>Seleccionados: <strong>{{ seleccionados.length }}</strong></div>
          <div>Valor por persona: <strong>${{ formMasivo.valor_pagado.toLocaleString('es-CL') }}</strong></div>
          <div class="total">Total: <strong>${{ (seleccionados.length * formMasivo.valor_pagado).toLocaleString('es-CL') }}</strong></div>
        </div>

        <div class="acciones center" v-if="seleccionados.length">
          <BaseButton
            variant="primary"
            :disabled="!formMasivo.valor_pagado || !formMasivo.fecha_pago || !formMasivo.file"
            @click="registrarPagoMasivo"
          >
            ✅ Registrar Pago Masivo ({{ seleccionados.length }})
          </BaseButton>
          <BaseButton variant="secondary" @click="limpiarMasivo">🧹 Limpiar</BaseButton>
        </div>
      </section>
    </div>

    <!-- ===================== HISTÓRICO ===================== -->
    <div v-else class="card">
      <!-- Filtros -->
      <div class="filtros">
        <InputBase v-model="filtroQ" placeholder="Nombre / RUT / Email" @keydown.enter.prevent="cargarPagos" />
        <BaseSelect v-model="filtroCurso" :options="[{value:'',label:'Todos los cursos'}, ...cursoOptions]" />
        <BaseSelect v-model="filtroGrupo" :options="[{value:'',label:'Todos los grupos'}, ...grupoOptions]" />
        <BaseButton class="btn-search" variant="primary" @click="cargarPagos">🔎 Buscar</BaseButton>
      </div>

      <!-- BARRA DE ACCIONES estilo 'Gestión de Comunicaciones' -->
      <div class="toolbar">
        <button class="btn btn-outline" @click="exportarCSV">
          <span class="btn-icon">⬇️</span> Exportar Correos
        </button>
        <button class="btn btn-primary" :disabled="!seleccionadosHistorico.length" @click="marcarEnviado">
          <span class="btn-icon">✓</span> Marcar Enviado
        </button>
        <button class="btn btn-blue" :disabled="!seleccionadosHistorico.length" @click="enviarPorCorreo">
          <span class="btn-icon">✈️</span> Enviar por correo
        </button>
      </div>

      <!-- Estado de carga y error -->
      <div v-if="cargandoPagos" class="estado-carga">🔄 Cargando pagos...</div>
      <div v-if="errorPagos" class="mensaje-error">
        ❌ {{ errorPagos }}
        <div><BaseButton variant="primary" @click="cargarPagos">Reintentar</BaseButton></div>
      </div>

      <!-- Tabla -->
      <div class="table-wrapper" v-if="!cargandoPagos">
        <table>
          <thead>
            <tr>
              <th style="width:36px;">
                <input type="checkbox"
                       :checked="allChecked"
                       @change="toggleSelectAllHistorico($event.target.checked)" />
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
                <input type="checkbox"
                       :value="p.id"
                       v-model="seleccionadosHistorico" />
              </td>
              <td><strong>{{ p.nombre }}</strong></td>
              <td>{{ p.rut }}</td>
              <td>{{ cursoLabel(p.curso) }}</td>
              <td>${{ (p.monto ?? p.valor_pagado)?.toLocaleString('es-CL') }}</td>
              <td>{{ dateCL(p.fecha || p.fecha_pago) }}</td>
              <td>{{ p.metodo || 'Transferencia' }}</td>
              <td class="acciones-buttons">
                <!-- 👁️ Ver -->
                <BaseButton size="sm" variant="info" class="btn-with-icon" title="Ver detalle" @click="verDetalle(p)">
                  <span class="icon">👁️</span><span class="label">Ver</span>
                </BaseButton>
                <!-- ✏️ Modificar -->
                <BaseButton size="sm" variant="primary" class="btn-with-icon" title="Editar pago" @click="abrirEditar(p)">
                  <span class="icon">✏️</span><span class="label">Editar</span>
                </BaseButton>
                <!-- 🔁 Transferir -->
                <BaseButton size="sm" variant="secondary" class="btn-with-icon" title="Transferir pago" @click="abrirTransferir(p)">
                  <span class="icon">🔁</span><span class="label">Transferir</span>
                </BaseButton>
                <!-- 🗑️ Anular -->
                <BaseButton size="sm" variant="warning" class="btn-with-icon" title="Anular pago" @click="abrirAnular(p)">
                  <span class="icon">🗑️</span><span class="label">Anular</span>
                </BaseButton>
                <!-- 🧾 Comprobante -->
                <BaseButton
                  v-if="p.comprobante || p.comprobante_url"
                  size="sm"
                  variant="secondary"
                  class="btn-with-icon"
                  title="Descargar comprobante"
                  @click="descargarComprobante(p)"
                >
                  <span class="icon">🧾</span><span class="label">Comprobante</span>
                </BaseButton>
              </td>
            </tr>
            <tr v-if="!pagos.length">
              <td colspan="8" class="placeholder">No hay pagos para mostrar</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modales -->
    <BaseModal v-model="modalEditar" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Editar Pago</h3>
            <div class="header-actions">
              <BaseButton class="btn-save" type="button" variant="primary" @click="guardarEdicion" :disabled="guardando">
                {{ guardando ? '⏳ Guardando...' : '💾 Guardar' }}
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

    <BaseModal v-model="modalAnular" title="Confirmar Anulación">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">⚠️</div>
          <p>¿Anular pago de <strong>{{ pagoAnular?.nombre }}</strong>?</p>
          <div class="confirm-actions">
            <BaseButton @click="modalAnular=false" variant="secondary" class="btn-modal-cancel">❌ Cancelar</BaseButton>
            <BaseButton @click="confirmarAnulacion" variant="warning" class="btn-modal-anular">⚠️ Anular</BaseButton>
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

import pagosService from '@/services/pagosService.js'
import personasService from '@/services/personasService.js' // existe en tu repo

function hoyISO () {
  const d = new Date();
  const m = String(d.getMonth()+1).padStart(2,'0');
  const day = String(d.getDate()).padStart(2,'0');
  return `${d.getFullYear()}-${m}-${day}`;
}
function dateCL (f) {
  if (!f) return '-';
  return new Date(f).toLocaleDateString('es-CL', { day:'2-digit', month:'short', year:'numeric' });
}

export default {
  name: 'Pagos',
  components: { InputBase, BaseSelect, BaseButton, BaseModal },
  data () {
    return {
      // pestañas
      tab: 'registro',
      subTab: 'individual',

      // catálogos
      cursoOptions: [],
      grupoOptions: [],

      // ---- Individual
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

      // ---- Masivo
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

      // ---- Histórico
      filtroQ: '',
      filtroCurso: '',
      filtroGrupo: '',
      pagos: [],
      cargandoPagos: false,
      errorPagos: null,
      seleccionadosHistorico: [],

      // ---- Modales
      modalEditar: false,
      pagoEdit: {},
      guardando: false,

      modalAnular: false,
      pagoAnular: null
    };
  },
  computed: {
    allChecked () {
      return this.pagos.length > 0 &&
             this.seleccionadosHistorico.length === this.pagos.length
    }
  },
  methods: {
    // ====== Cargar catálogos (sin catalogosService)
    async cargarCatalogos () {
      // Intento opcional: cursosService.js si existe
      try {
        const mod = await import('@/services/cursosService.js');
        const svc = mod.default || mod;
        const resp = (svc.cursos?.list ? await svc.cursos.list()
                    : svc.list ? await svc.list()
                    : []);
        const arr = Array.isArray(resp) ? resp : (resp?.results || []);
        this.cursoOptions = arr.map(x => ({
          value: x.id ?? x.value ?? x.CUR_ID ?? x.cur_id ?? String(x.nombre || x.label || 'curso'),
          label: x.nombre ?? x.label ?? x.CUR_NOMBRE ?? `Curso ${x.id ?? ''}`.trim()
        }));
      } catch (e) {
        // si no existe el servicio, dejamos vacío (no rompe)
        this.cursoOptions = [];
      }

      // Opcional: grupos desde algún servicio si existiera
      try {
        const modG = await import('@/services/usuariosService.js'); // existe en repo
        const svcG = modG.default || modG;
        // probamos distintos nombres típicos
        const respG = svcG.grupos?.list
          ? await svcG.grupos.list()
          : (svcG.listGrupos ? await svcG.listGrupos() : []);
        const arrG = Array.isArray(respG) ? respG : (respG?.results || []);
        this.grupoOptions = arrG.map(g => ({
          value: g.id ?? g.value ?? g.GRU_ID ?? String(g.nombre || g.label || 'grupo'),
          label: g.nombre ?? g.label ?? g.GRU_NOMBRE ?? `Grupo ${g.id ?? ''}`.trim()
        }));
      } catch (e) {
        this.grupoOptions = [];
      }
    },

    // ====== REGISTRO INDIVIDUAL
    async buscarPersonas () {
      const q = (this.buscarPersonaQ || '').trim();
      if (!q) { this.personasEncontradas = []; return; }
      try {
        this.buscandoPersonas = true;
        // ajusta al método real de tu personasService
        const r = (personasService.personas?.search)
          ? await personasService.personas.search({ q })
          : (personasService.search ? await personasService.search({ q }) : []);
        const arr = Array.isArray(r) ? r : (r?.results || []);
        this.personasEncontradas = arr.map(p => ({
          id: p.id ?? p.PER_ID ?? p.id_persona,
          nombre: p.nombre ?? `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: p.rut ?? (p.PER_RUN && p.PER_DV ? `${p.PER_RUN}-${p.PER_DV}` : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }));
      } catch (e) {
        this.personasEncontradas = [];
      } finally {
        this.buscandoPersonas = false;
      }
    },
    seleccionarPersona (p) {
      this.formInd.personaId = p.id;
      this.formInd.nombre = p.nombre;
      this.formInd.rut = p.rut;
      this.formInd.email = p.email;
      this.personasEncontradas = [];
      this.buscarPersonaQ = p.nombre;
    },
    onFileInd (e) { this.formInd.file = e.target.files?.[0] || null; },
    limpiarIndividual () {
      this.formInd = { personaId: null, nombre:'', rut:'', email:'', curso:'', valor_pagado:null, fecha_pago:hoyISO(), observacion:'', file:null };
      this.buscarPersonaQ = '';
      this.personasEncontradas = [];
    },
    async registrarPagoIndividual () {
      try {
        if (this.formInd.file) {
          const fd = new FormData();
          Object.entries(this.formInd).forEach(([k,v]) => {
            if (v !== null && v !== undefined) fd.append(k, v);
          });
          // intenta método con form-data
          if (pagosService.pagos?.createIndividualForm) {
            await pagosService.pagos.createIndividualForm(fd);
          } else if (pagosService.createIndividualForm) {
            await pagosService.createIndividualForm(fd);
          } else if (pagosService.pagos?.create) {
            await pagosService.pagos.create(fd);
          } else {
            throw new Error('Endpoint no disponible para FormData');
          }
        } else {
          const payload = {
            personaId: this.formInd.personaId,
            curso: this.formInd.curso,
            valor_pagado: this.formInd.valor_pagado,
            fecha_pago: this.formInd.fecha_pago,
            observacion: this.formInd.observacion
          };
          if (pagosService.pagos?.createIndividual) {
            await pagosService.pagos.createIndividual(payload);
          } else if (pagosService.createIndividual) {
            await pagosService.createIndividual(payload);
          } else if (pagosService.pagos?.create) {
            await pagosService.pagos.create(payload);
          } else {
            throw new Error('Endpoint no disponible para createIndividual');
          }
        }
        alert('✅ Pago individual registrado');
        this.limpiarIndividual();
      } catch (e) {
        alert('❌ Error registrando pago: ' + (e?.message || 'ver consola'));
      }
    },

    // ====== REGISTRO MASIVO
    onFileMasivo (e) { this.formMasivo.file = e.target.files?.[0] || null; },
    async cargarParticipantes () {
      try {
        this.cargandoParticipantes = true;
        let r = [];
        if (personasService.personas?.byGrupoCurso) {
          r = await personasService.personas.byGrupoCurso({
            grupo: this.formMasivo.grupo, curso: this.formMasivo.curso
          });
        } else if (personasService.byGrupoCurso) {
          r = await personasService.byGrupoCurso({
            grupo: this.formMasivo.grupo, curso: this.formMasivo.curso
          });
        }
        const arr = Array.isArray(r) ? r : (r?.results || []);
        this.participantes = arr.map(p => ({
          id: p.id ?? p.PER_ID ?? p.id_persona,
          nombre: p.nombre ?? `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: p.rut ?? (p.PER_RUN && p.PER_DV ? `${p.PER_RUN}-${p.PER_DV}` : ''),
          email: p.email ?? p.PER_MAIL ?? ''
        }));
        this.seleccionados = [];
      } catch (e) {
        this.participantes = [];
      } finally {
        this.cargandoParticipantes = false;
      }
    },
    selectAll () { this.seleccionados = this.participantes.map(u => u.id); },
    unselectAll () { this.seleccionados = []; },
    limpiarMasivo () {
      this.formMasivo = { grupo:'', curso:'', valor_pagado:null, fecha_pago:hoyISO(), observacion:'', file:null };
      this.participantes = [];
      this.seleccionados = [];
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
        };

        if (this.formMasivo.file) {
          const fd = new FormData();
          Object.entries(payload).forEach(([k,v]) => {
            if (k === 'participantes') v.forEach(id => fd.append('participantes[]', id));
            else if (v !== null && v !== undefined) fd.append(k, v);
          });
          fd.append('file', this.formMasivo.file);

          if (pagosService.pagos?.createMasivoForm) {
            await pagosService.pagos.createMasivoForm(fd);
          } else if (pagosService.createMasivoForm) {
            await pagosService.createMasivoForm(fd);
          } else {
            throw new Error('Endpoint no disponible para Masivo FormData');
          }
        } else {
          if (pagosService.pagos?.createMasivo) {
            await pagosService.pagos.createMasivo(payload);
          } else if (pagosService.createMasivo) {
            await pagosService.createMasivo(payload);
          } else {
            throw new Error('Endpoint no disponible para createMasivo');
          }
        }
        alert('✅ Pago masivo registrado');
        this.limpiarMasivo();
      } catch (e) {
        alert('❌ Error registrando masivo: ' + (e?.message || 'ver consola'));
      }
    },

    // ====== HISTÓRICO
    cursoLabel (id) {
      const c = this.cursoOptions.find(x => String(x.value) === String(id));
      return c ? c.label : id;
    },
    async cargarPagos () {
      try {
        this.cargandoPagos = true;
        this.errorPagos = null;
        let r = [];
        const params = {
          q: (this.filtroQ || '').trim(),
          curso: this.filtroCurso || undefined,
          grupo: this.filtroGrupo || undefined
        };
        if (pagosService.pagos?.list) r = await pagosService.pagos.list(params);
        else if (pagosService.list) r = await pagosService.list(params);
        this.pagos = Array.isArray(r) ? r : (r?.results || []);
      } catch (e) {
        this.pagos = [];
        this.errorPagos = 'No fue posible cargar pagos. Verifica el backend.';
      } finally {
        this.cargandoPagos = false;
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
      }));
      const headers = rows.length ? Object.keys(rows[0]) : ['Nombre','RUT','Curso','Monto','Fecha','Metodo'];
      const csv = [headers.join(',')]
        .concat(rows.map(r => headers.map(h => `"${String(r[h] ?? '').replace(/"/g,'""')}"`).join(',')))
        .join('\r\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a'); a.href = url; a.download = 'Pagos.csv'; document.body.appendChild(a); a.click();
      document.body.removeChild(a); URL.revokeObjectURL(url);
    },

    // ====== Selección del histórico + acciones toolbar
    toggleSelectAllHistorico (checked) {
      if (checked) {
        this.seleccionadosHistorico = this.pagos.map(p => p.id)
      } else {
        this.seleccionadosHistorico = []
      }
    },
    async marcarEnviado () {
      if (!this.seleccionadosHistorico.length) return
      // Conecta aquí a tu endpoint real cuando lo tengas:
      // await pagosService.pagos.marcarEnviado({ ids: this.seleccionadosHistorico })
      alert(`✓ Marcados como enviados: ${this.seleccionadosHistorico.join(', ')}`)
    },
    async enviarPorCorreo () {
      if (!this.seleccionadosHistorico.length) return
      // Conecta aquí a tu endpoint real cuando lo tengas:
      // await pagosService.pagos.enviarCorreos({ ids: this.seleccionadosHistorico })
      alert(`✉️ Enviando correos a IDs: ${this.seleccionadosHistorico.join(', ')}`)
    },

    // ====== Acciones por fila
    verDetalle (p) {
      alert(`👁️ Pago de ${p.nombre}\nMonto: $${(p.monto ?? p.valor_pagado)?.toLocaleString('es-CL')}\nFecha: ${dateCL(p.fecha || p.fecha_pago)}`);
    },
    abrirTransferir (p) {
      alert(`🔁 Transferir pago de ${p.nombre} (id ${p.id})`);
    },

    // ====== EDICIÓN / ANULACIÓN
    abrirEditar (p) {
      this.pagoEdit = {
        id: p.id,
        nombre: p.nombre,
        rut: p.rut,
        curso: p.curso,
        monto: p.monto ?? p.valor_pagado,
        fecha: (p.fecha || p.fecha_pago || '').slice(0,10),
        observacion: p.observacion || ''
      };
      this.modalEditar = true;
    },
    async guardarEdicion () {
      try {
        this.guardando = true;
        const body = {
          curso: this.pagoEdit.curso,
          monto: this.pagoEdit.monto,
          fecha: this.pagoEdit.fecha,
          observacion: this.pagoEdit.observacion
        };
        if (pagosService.pagos?.partialUpdate) {
          await pagosService.pagos.partialUpdate(this.pagoEdit.id, body);
        } else if (pagosService.partialUpdate) {
          await pagosService.partialUpdate(this.pagoEdit.id, body);
        } else if (pagosService.pagos?.update) {
          await pagosService.pagos.update(this.pagoEdit.id, body);
        } else {
          throw new Error('Endpoint no disponible para actualizar');
        }
        this.modalEditar = false;
        await this.cargarPagos();
        alert('✅ Pago actualizado');
      } catch (e) {
        alert('❌ Error actualizando pago: ' + (e?.message || 'ver consola'));
      } finally {
        this.guardando = false;
      }
    },
    abrirAnular (p) {
      this.pagoAnular = p;
      this.modalAnular = true;
    },
    async confirmarAnulacion () {
      try {
        if (pagosService.pagos?.anular) {
          await pagosService.pagos.anular(this.pagoAnular.id);
        } else if (pagosService.anular) {
          await pagosService.anular(this.pagoAnular.id);
        } else {
          throw new Error('Endpoint no disponible para anular');
        }
        this.modalAnular = false;
        await this.cargarPagos();
        alert('✅ Pago anulado');
      } catch (e) {
        alert('❌ Error al anular: ' + (e?.message || 'ver consola'));
      }
    },
    descargarComprobante (p) {
      if (p.comprobante_url) {
        window.open(p.comprobante_url, '_blank');
      } else {
        alert('No hay comprobante disponible.');
      }
    }
  },
  async mounted () {
    await Promise.all([this.cargarCatalogos(), this.cargarPagos()]);
  }
};
</script>

<style>
.gestion-pagos{
  box-sizing:border-box;
  margin:20px auto;
  padding:16px 40px;
  background:#fff;
  color:#111;
  display:flex;
  flex-direction:column;
  gap:16px;
  font-family:Arial, sans-serif;
  width: 1200px;
  max-width: calc(100% - 48px);
  border-radius:8px;
  box-shadow:0 10px 30px rgba(16,24,40,0.08);
}

.header h2{
  background:#214e9c;
  color:#fff;
  padding:14px 18px;
  border-radius:6px;
  margin:0 0 4px 0;
  text-align:center;
}
.header h3{
  margin:6px 0 0 0;
  color:#444;
  font-weight:500;
  text-align:center;
}

.tabs, .subtabs{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.tabs button, .subtabs button{ padding:10px 14px; border-radius:8px; border:1px solid #e6e6e6; background:#fff; cursor:pointer; font-weight:700 }
.tabs button.active, .subtabs button.active{ background:#214e9c; color:#fff; border-color:#214e9c }

.card{ background:#fff; border:1px solid #eef2f6; border-radius:8px; padding:16px; }
.panel{ display:flex; flex-direction:column; gap:12px; }
.panel-title{ text-align:center; }
.panel-title h4{ margin:0; color:#1e3a8a; font-size:20px; }
.panel-title p{ margin:4px 0 0 0; color:#475569; }

.grid{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.col{ display:flex; flex-direction:column; gap:6px; }
.col.full{ grid-column:1 / -1; }
.col.auto{ align-self:end; }
label{ font-weight:700; color:#1e3a8a; }
.invisible{ visibility:hidden }

.with-prefix{ display:flex; align-items:center; border:1px solid #e6e6e6; border-radius:6px; overflow:hidden; }
.with-prefix .prefix{ background:#f1f5f9; padding:10px 12px; font-weight:700; color:#334155; border-right:1px solid #e6e6e6; }
.with-prefix input{ border:none; padding:10px 12px; flex:1; outline:none; }

.badge{ background:#e0e7ff; color:#3730a3; font-weight:700; padding:8px 10px; border-radius:8px; text-align:center; }

.resultados{ border:1px solid #e6e6e6; border-radius:8px; margin-top:6px; }
.resultado{ display:flex; align-items:center; justify-content:space-between; padding:10px 12px; border-bottom:1px solid #f1f1f1; cursor:pointer; }
.resultado:last-child{ border-bottom:none; }
.resultado:hover{ background:#f8fafc; }
.resultado .muted{ color:#64748b; font-size:12px; display:block; }

.lista{ margin-top:8px; border:1px solid #e6e6e6; border-radius:8px; }
.lista-header{ display:flex; align-items:center; justify-content:space-between; padding:10px 12px; border-bottom:1px solid #f1f1f1; }
.lista-items{ max-height:280px; overflow:auto; display:flex; flex-direction:column; }
.item{ display:flex; gap:10px; align-items:center; padding:10px 12px; border-bottom:1px solid #f6f6f6; }
.item:last-child{ border-bottom:none; }
.item .info .muted{ color:#64748b; font-size:12px; display:block; }

.resumen{ margin-top:12px; padding:12px; background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%); border:1px solid #93c5fd; border-radius:8px; display:flex; gap:16px; justify-content:center; font-weight:700; color:#1e40af; }
.resumen .total{ text-transform:uppercase; }

.filtros{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:8px; }
.estado-carga{ text-align:center; padding:12px; color:#555; font-style:italic; }
.mensaje-error{ background:#fde8e8; color:#9b1c1c; padding:10px; border:1px solid #f8b4b4; border-radius:6px; text-align:center; }

.table-wrapper{ overflow:auto; border:1px solid #eef2f6; border-radius:8px; }
table{ width:100%; border-collapse:collapse; background:#fff; }
th,td{ padding:14px 12px; border-bottom:1px solid #f1f1f1; text-align:left; }
th{ background:#f7f7f7; position:sticky; top:0; z-index:1; }
.placeholder{ text-align:center; color:#666; padding:40px 12px; }

.acciones{ display:flex; gap:8px; }
.acciones.center{ justify-content:center; }
.acciones-buttons{ display:flex; gap:6px; align-items:center; justify-content:center; flex-wrap:wrap; }

/* Botones con ícono y texto */
.btn-with-icon{ display:inline-flex; align-items:center; gap:6px; font-weight:700; }
.btn-with-icon .icon{ line-height:1; }
.btn-with-icon .label{ line-height:1; }

/* Barra superior estilo comunicación */
.toolbar{
  display:flex;
  gap:12px;
  margin:8px 0 14px;
}
.btn{
  display:inline-flex;
  align-items:center;
  gap:8px;
  font-weight:700;
  padding:10px 14px;
  border-radius:8px;
  border:1px solid transparent;
  cursor:pointer;
  transition:filter .15s ease, transform .02s ease;
}
.btn:active{ transform: translateY(1px); }
.btn:disabled{ opacity:.55; cursor:not-allowed; }
.btn-outline{
  background:#f3f4f6;
  border-color:#d1d5db;
  color:#1f2937;
}
.btn-outline:hover{ filter:brightness(0.98); }
.btn-primary{
  background:#1e40af;
  color:#fff;
}
.btn-primary:hover{ filter:brightness(1.05); }
.btn-blue{
  background:#1d4ed8;
  color:#fff;
}
.btn-blue:hover{ filter:brightness(1.05); }
.btn-icon{ font-size:14px; line-height:1; }

.btn-search{ background:linear-gradient(180deg,#2b6cb0,#154c8c); color:#fff; }
.btn-save{ background:linear-gradient(180deg,#2563eb,#1e40af); color:#fff; }

.pago-modal :deep(.modal-overlay){ position:fixed !important; inset:0 !important; display:flex !important; align-items:center !important; justify-content:center !important; z-index:9999 !important; }
.modal-edit{ width:700px; max-width:calc(100vw - 40px); max-height:calc(100vh - 96px); overflow:auto; padding:24px 32px; }
.modal-header{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:16px; }
.modal-header h3{ margin:0; color:#214e9c }
.form-fields-grid{ display:grid; grid-template-columns:1fr 1fr; gap:16px 24px; }
.row{ display:flex; flex-direction:column; gap:6px; }
.row.full-width{ grid-column:1 / -1; }
.row input, .row select{ padding:10px 12px; border:1px solid #e6e6e6; border-radius:6px; }

.confirm-content{ display:flex; flex-direction:column; align-items:center; text-align:center; padding:24px; }
.confirm-icon{ font-size:60px; margin-bottom:12px; }
.btn-modal-cancel{ background:linear-gradient(180deg,#6b7280,#4b5563) !important; color:#fff !important; }
.btn-modal-anular{ background:linear-gradient(180deg,#ef4444,#dc2626) !important; color:#fff !important; }

@media (max-width: 860px){
  .grid{ grid-template-columns:1fr; }
  .btn-with-icon .label{ display:none; } /* en móviles, solo iconos */
}
</style>

