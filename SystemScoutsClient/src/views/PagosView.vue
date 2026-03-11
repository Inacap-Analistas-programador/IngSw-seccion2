<template>
  <div class="gestion-pagos">
    <!-- Encabezado con PageHeader -->
    <PageHeader 
      title="Gestión de Pagos" 
      subtitle="Registra, busca y administra los pagos y egresos del sistema."
    />

    <!-- Tabs Principales -->
    <div class="tabs">
      <BaseButton
        :variant="tabPrincipal === 'registro' ? 'primary' : 'secondary'"
        @click="tabPrincipal = 'registro'"
      >
        <AppIcons name="plus-circle" :size="18" /> Registro de Pagos
      </BaseButton>
      <BaseButton
        :variant="tabPrincipal === 'historico' ? 'primary' : 'secondary'"
        @click="tabPrincipal = 'historico'"
      >
        <AppIcons name="history" :size="18" /> Historial de Pagos
      </BaseButton>
      <BaseButton
        :variant="tabPrincipal === 'comprobantes' ? 'primary' : 'secondary'"
        @click="tabPrincipal = 'comprobantes'"
      >
        <AppIcons name="file-text" :size="18" /> Comprobantes
      </BaseButton>
    </div>

    <!-- Contenido Tab Registro -->
    <div v-if="tabPrincipal === 'registro'" class="card card-registro">
      <div class="subtabs">
        <BaseButton
          size="sm"
          :variant="subTabRegistro === 'individual' ? 'primary' : 'secondary'"
          @click="subTabRegistro = 'individual'"
        >
          Individual
        </BaseButton>
        <BaseButton
          size="sm"
          :variant="subTabRegistro === 'masivo' ? 'primary' : 'secondary'"
          @click="subTabRegistro = 'masivo'"
        >
          Masivo
        </BaseButton>
        <BaseButton
          size="sm"
          :variant="subTabRegistro === 'proveedor' ? 'primary' : 'secondary'"
          @click="subTabRegistro = 'proveedor'"
        >
          Proveedores (Egresos)
        </BaseButton>
      </div>

      <div class="panel">
        <PagosIndividualForm
          v-if="subTabRegistro === 'individual'"
          :cursoOptions="cursoOptions"
          :conceptosOptions="conceptosOptions"
          @success="onSuccess"
          @error="onError"
        />

        <PagosMasivoForm
          v-if="subTabRegistro === 'masivo'"
          :grupoOptions="grupoOptions"
          :allCursoOptions="cursoOptions"
          :conceptosOptions="conceptosOptions"
          @success="onSuccess"
          @error="onError"
        />

        <PagosProveedoresForm
          v-if="subTabRegistro === 'proveedor'"
          :conceptosOptions="conceptosOptions"
          @success="onSuccess"
          @error="onError"
        />
      </div>
    </div>

    <!-- Contenido Tab Histórico -->
    <PagosHistorico
      v-if="tabPrincipal === 'historico'"
      ref="historicoRef"
      :cursoOptions="cursoOptions"
      :grupoOptions="grupoOptions"
      @ver-detalle="abrirDetalle"
      @editar="abrirEditar"
      @transferir="abrirTransferir"
      @anular="abrirAnular"
      @descargar-comprobante="descargarComprobante"
    />

    <!-- Contenido Tab Comprobantes -->
    <div v-if="tabPrincipal === 'comprobantes'" class="card">
      <PagosComprobantes
        :cursoOptions="cursoOptions"
        :grupoOptions="grupoOptions"
        :conceptosOptions="conceptosOptions"
        @success="onSuccess"
        @error="onError"
      />
    </div>

    <!-- Centralized Modals -->
    <PagosModals
      v-model:modalVerDetalle="modalVerDetalle"
      v-model:modalEditar="modalEditar"
      v-model:modalConfirmarEdicion="modalConfirmarEdicion"
      v-model:modalTransferir="modalTransferir"
      v-model:modalAnular="modalAnular"
      :pagoDetalle="pagoDetalle"
      :pagoEdit="pagoEdit"
      :pagoAnular="pagoAnular"
      :pagoTransferir="pagoTransferir"
      :cambiosDetectados="cambiosDetectados"
      :cursoOptions="cursoOptions"
      :loading="guardando"
      @guardar-edicion="validarEdicion"
      @cancelar-edicion="cancelarEdicion"
      @confirmar-edicion="confirmarEdicion"
      @confirmar-transferencia="confirmarTransferencia"
      @confirmar-anulacion="confirmarAnulacion"
    />

    <NotificationToast
      v-model:visible="toastVisible"
      :message="toastMessage"
      :icon="toastIcon"
      :duration="3000"
    />
  </div>
</template>

<script>
// Components
import AppIcons from '@/components/icons/AppIcons.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import BaseButton from '@/components/BaseButton.vue'
import NotificationToast from '@/components/NotificationToast.vue'

// Modular Components
import PagosIndividualForm from '@/components/pagos/PagosIndividualForm.vue'
import PagosMasivoForm from '@/components/pagos/PagosMasivoForm.vue'
import PagosHistorico from '@/components/pagos/PagosHistorico.vue'
import PagosComprobantes from '@/components/pagos/PagosComprobantes.vue'
import PagosProveedoresForm from '@/components/pagos/PagosProveedoresForm.vue'
import PagosModals from '@/components/pagos/PagosModals.vue'

// Services
import mantenedoresService from '@/services/mantenedoresService.js'
import cursosService from '@/services/cursosService.js'
import pagosService from '@/services/pagosService.js'

export default {
  name: 'PagosView',
  components: {
    AppIcons,
    PageHeader,
    BaseButton,
    NotificationToast,
    PagosIndividualForm,
    PagosMasivoForm,
    PagosHistorico,
    PagosComprobantes,
    PagosProveedoresForm,
    PagosModals
  },
  data() {
    return {
      tabPrincipal: 'registro',
      subTabRegistro: 'individual',
      
      // Shared options
      cursoOptions: [],
      grupoOptions: [],
      conceptosOptions: [],
      
      // Modal visibility states
      modalVerDetalle: false,
      modalEditar: false,
      modalConfirmarEdicion: false,
      modalTransferir: false,
      modalAnular: false,
      
      // Active data for modals
      pagoDetalle: {},
      pagoEdit: {},
      pagoEditOriginal: {},
      pagoAnular: null,
      pagoTransferir: null,
      cambiosDetectados: [],
      
      // Processing state
      guardando: false,
      toastVisible: false,
      toastMessage: '',
      toastIcon: ''
    }
  },
  async created() {
    // Initial loading of catalogues
    await this.cargarCatalogos()
  },
  methods: {
    /**
     * Loads the catalogues once in the parent to share with children
     */
    async cargarCatalogos() {
      try {
        const [cursosResp, gruposResp, conceptosResp] = await Promise.all([
          cursosService.cursos.list({ page_size: 1000 }),
          mantenedoresService.grupo.list(),
          mantenedoresService.conceptoContable.list()
        ])

        this.cursoOptions = this.normalizeOptions(cursosResp, 'CUR_ID', 'CUR_DESCRIPCION')
        this.grupoOptions = this.normalizeOptions(gruposResp, 'GRU_ID', 'GRU_DESCRIPCION')
        
        const conceptosRaw = this.getData(conceptosResp)
        this.conceptosOptions = conceptosRaw.map(c => ({
          value: c.coc_id || c.COC_ID,
          label: c.coc_descripcion || c.COC_DESCRIPCION,
          tipo: c.coc_tipo || c.COC_TIPO
        }))
      } catch (error) {
        console.error('Error cargando catálogos:', error)
        this.onError('Error al cargar catálogos iniciales')
      }
    },

    /**
     * Helper to normalize catalogue options
     */
    normalizeOptions(resp, idKey, labelKey) {
      const data = this.getData(resp)
      return data.map(item => ({
        value: item[idKey] || item[idKey.toLowerCase()],
        label: item[labelKey] || item[labelKey.toLowerCase()]
      }))
    },

    /**
     * Helper to extract results array from different service responses
     */
    getData(resp) {
      if (!resp) return []
      if (Array.isArray(resp)) return resp
      return resp.results || resp.data?.results || resp.data || resp.items || []
    },

    // --- Global Notifications ---
    onSuccess(message) {
      this.toastMessage = message
      this.toastIcon = 'check'
      this.toastVisible = true
      
      // If we registered a payment, we might want to refresh history
      if (this.tabPrincipal === 'historico' && this.$refs.historicoRef) {
        this.$refs.historicoRef.cargarPagos(true)
      }
    },

    onError(message) {
      this.toastMessage = message
      this.toastIcon = 'x'
      this.toastVisible = true
    },

    // --- Modal Orchestration ---

    abrirDetalle(pago) {
      this.pagoDetalle = { ...pago }
      this.modalVerDetalle = true
    },

    abrirEditar(pago) {
      this.pagoEdit = { ...pago }
      this.pagoEditOriginal = { ...pago }
      this.modalEditar = true
    },

    validarEdicion(cambios) {
      this.cambiosDetectados = cambios
      this.modalConfirmarEdicion = true
    },

    cancelarEdicion() {
      this.modalConfirmarEdicion = false
    },

    async confirmarEdicion() {
      this.guardando = true
      try {
        const payload = {
          cur_id: this.pagoEdit.CUR_ID,
          pap_valor: this.pagoEdit.monto,
          pap_fecha_hora: this.pagoEdit.fecha,
          pap_observacion: this.pagoEdit.observacion
        }
        await pagosService.pagos.update(this.pagoEdit.id, payload)
        this.onSuccess('Pago actualizado correctamente')
        this.modalConfirmarEdicion = false
        this.modalEditar = false
      } catch (error) {
        console.error('Error actualizando pago:', error)
        this.onError('Error al actualizar el pago')
      } finally {
        this.guardando = false
      }
    },

    abrirTransferir(pago) {
      this.pagoTransferir = pago
      this.modalTransferir = true
    },

    async confirmarTransferencia(form) {
      this.guardando = true
      try {
        await pagosService.pagos.transferir(this.pagoTransferir.id, {
          nueva_persona_id: form.personaId,
          tipo: form.tipo,
          monto_parcial: form.monto_parcial
        })
        this.onSuccess('Pago transferido correctamente')
        this.modalTransferir = false
      } catch (error) {
        console.error('Error transfiriendo pago:', error)
        this.onError('Error al transferir el pago')
      } finally {
        this.guardando = false
      }
    },

    abrirAnular(pago) {
      this.pagoAnular = pago
      this.modalAnular = true
    },

    async confirmarAnulacion() {
      this.guardando = true
      try {
        await pagosService.pagos.patch(this.pagoAnular.id, { pap_estado: 2 })
        this.onSuccess('Pago anulado correctamente')
        this.modalAnular = false
      } catch (error) {
        console.error('Error anulando pago:', error)
        this.onError('Error al anular el pago')
      } finally {
        this.guardando = false
      }
    },

    descargarComprobante(pago) {
      if (pago.PAP_RUTA_COMPROBANTE) {
        window.open(pago.PAP_RUTA_COMPROBANTE, '_blank')
      } else {
        this.onError('No hay un archivo de comprobante para este registro')
      }
    }
  }
}
</script>

<style>
.gestion-pagos {
  box-sizing: border-box;
  padding: 24px 24px;
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

.grid-individual, 
.grid-masivo {
  grid-template-columns: repeat(3, 1fr);
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
  max-height: 280px;
  overflow-y: auto;
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
  justify-content: flex-start;
  gap: 8px;
}

.filtros-historico {
  margin-bottom: 10px;
}

.filtros-historico .filtro-busqueda {
  width: 200px;
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

/* Tabla Estándar */
.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow-x: auto;
  flex: 1 1 auto;
  margin-top: 10px;
}

.courses-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
}

.courses-table th, .courses-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  font-size: 14px;
  color: #1f2937;
}

.courses-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
  position: sticky;
  top: 0;
  z-index: 2;
  white-space: nowrap;
}

.courses-table tbody tr:hover { 
  background: #f1f5f9; 
}

.placeholder {
  text-align: center;
  padding: 26px 10px;
  color: #6b7280;
}

/* Botones acciones tabla */
.acciones-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
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

/* Modales */
.pago-modal :deep(.modal-overlay) {
  position: fixed !important;
  inset: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 9999 !important;
}

.pago-modal :deep(.modal-content) {
  width: auto !important;
  max-width: 550px !important;
}

.form-fields-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 18px;
}

/* Responsive */
@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .courses-table, .courses-table thead, .courses-table tbody, .courses-table th, .courses-table td, .courses-table tr {
    display: block;
  }
  .courses-table thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
  .courses-table tr {
    margin-bottom: 12px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px;
  }
  .courses-table td {
    padding-left: 50%;
    text-align: right;
    display: flex;
    justify-content: space-between;
  }
  .courses-table td::before {
    content: attr(data-label);
    font-weight: 600;
  }
}
</style>
