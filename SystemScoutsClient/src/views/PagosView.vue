<template>
  <div class="gestion-pagos">
    <!-- Encabezado -->
    <header class="header">
      <h2>Gestión de Pagos</h2>
    </header>
    <NotificationToast v-if="toastVisible" :message="toastMessage" :icon="toastIcon" @close="toastVisible = false" />

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
      <button :class="{ active: tab === 'comprobantes' }" @click="tab = 'comprobantes'">
        Comprobantes
      </button>
      <button :class="{ active: tab === 'proveedores' }" @click="tab = 'proveedores'">
        Pagos a Proveedores
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
            <label>Tipo de Pago *</label>
            <div class="button-group">
              <BaseButton
                :variant="formInd.tipoPago === 'ingreso' ? 'primary' : 'secondary'"
                @click="formInd.tipoPago = 'ingreso'">
                Ingreso
              </BaseButton>
              <BaseButton
                :variant="formInd.tipoPago === 'egreso' ? 'primary' : 'secondary'"
                @click="formInd.tipoPago = 'egreso'">
                Egreso
              </BaseButton>
            </div>
          </div>

          <div class="col">
            <label>Concepto *</label>
            <BaseSelect
              v-model="formInd.COC_ID"
              :options="conceptosOptions"
              placeholder="Seleccione concepto"
            />
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
            <label>Comprobante de transferencia {{ formInd.tipoPago === 'egreso' ? '(Opcional)' : '' }}</label>
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
            :disabled="!puedeRegistrarIndividual || submittingIndividual"
            @click="registrarPagoIndividual"
          >
            <AppIcons v-if="!submittingIndividual" name="save" :size="16" />
            <AppIcons v-else name="spinner" :size="16" />
            <span v-if="!submittingIndividual"> Registrar Pago</span>
            <span v-else> Registrando...</span>
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
          <div class="col">
            <label>Tipo de Pago *</label>
            <BaseSelect
              v-model="formMasivo.tipoPago"
              :options="[{value: 'ingreso', label: 'Ingreso'}, {value: 'egreso', label: 'Egreso'}]"
              placeholder="Seleccione tipo"
            />
          </div>
          <div class="col">
            <label>Concepto *</label>
            <BaseSelect
              v-model="formMasivo.COC_ID"
              :options="conceptosOptions"
              placeholder="Seleccione concepto"
            />
          </div>
          <div class="col half">
            <label>Valor Total *</label>
            <div class="with-prefix">
              <span class="prefix">$</span>
              <input
                type="number"
                min="0"
                step="100"
                v-model.number="formMasivo.PAP_MONTO"
                placeholder="Ingrese el monto total"
                :disabled="!seleccionados.length"
              />
            </div>
          </div>
          <div class="col half">
            <label>Fecha de Pago *</label>
            <InputBase 
              type="date" 
              v-model="formMasivo.PAP_FECHA_PAGO" 
              :disabled="!seleccionados.length"
            />
          </div>
          <div class="col auto full-width">
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
          <div class="col span-2">
            <label>Comentario / Observación (máx. 200 caracteres)</label>
            <textarea
              class="comentario-input"
              v-model="formMasivo.observacion"
              maxlength="200"
              placeholder="Detalle general del pago; se aplicará a todos."
            />
          </div>
          <div class="col span-2 comprobante-wrapper">
            <label>Comprobante de transferencia grupal {{ formMasivo.tipoPago === 'egreso' ? '(Opcional)' : '' }}</label>
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
          <div>Valor por persona: <strong>${{ valorPorPersonaMasivo.toLocaleString('es-CL') }}</strong></div>
          <div class="total">
            Total:
            <strong>
              ${{
                (formMasivo.PAP_MONTO).toLocaleString('es-CL')
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
      <div class="filtros filtros-historico" style="align-items: flex-end;">
        <div style="display: flex; flex-direction: column;">
          <label>Buscar</label>
          <InputBase class="filtro-busqueda filtro-corto" v-model="filtroQ" placeholder="NOMBRE / RUT / EMAIL" title="Buscar por Nombre, RUT o Email" />
        </div>
        <div style="display: flex; flex-direction: column;">
          <label>Curso</label>
          <BaseSelect class="filtro-corto" v-model="filtroCurso" :options="[{ value: '', label: 'Todos los cursos' }, ...cursoOptions]" title="Filtrar por Curso" />
        </div>
        <div style="display: flex; flex-direction: column;">
          <label>Grupo</label>
          <BaseSelect class="filtro-corto" v-model="filtroGrupo" :options="[{ value: '', label: 'Todos los grupos' }, ...grupoOptions]" title="Filtrar por Grupo" />
        </div>
        <div style="display: flex; flex-direction: column;">
          <label>Estado de Pago</label>
          <BaseSelect class="filtro-corto" v-model="filtroEstado" :options="[{ value: '', label: 'Todos' }, { value: 'pagado', label: 'Pagado' }, { value: 'pendiente', label: 'Pendiente' }, { value: 'anulado', label: 'Anulado' }]" title="Filtrar por Estado de Pago" />
        </div>
        <BaseButton class="btn-standard" variant="primary" @click="cargarPagos(true)">
          <AppIcons name="search" :size="16" /> Buscar
        </BaseButton>
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <BaseButton class="btn-standard" variant="secondary" @click="exportarExcel">
          <AppIcons name="download" :size="16" />
          Exportar
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
                  @click="abrirCambioPersona(p)"
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

    <!-- ===================== SECCIÓN: COMPROBANTES ===================== -->
    <div v-else-if="tab === 'comprobantes'" class="card card-registro">
      <section class="panel panel-box">
        <div class="panel-title">
          <h3>Generación de Comprobantes</h3>
          <p>Filtra los pagos y genera un comprobante en formato PDF.</p>
        </div>

        <!-- Filtros para Comprobantes -->
        <div class="grid grid-comprobantes">
          <div class="col">
            <label>Tipo de Comprobante</label>
            <BaseSelect v-model="formComprobante.tipo" :options="[{value: 'ingreso', label: 'Ingreso'}, {value: 'egreso', label: 'Egreso'}]" />
          </div>
          <div class="col">
            <label>Concepto</label>
            <BaseSelect v-model="formComprobante.COC_ID" :options="conceptosOptions" placeholder="Todos los conceptos" />
          </div>
          <div class="col">
            <label>Curso</label>
            <BaseSelect v-model="formComprobante.CUR_ID" :options="cursoOptions" placeholder="Todos los cursos" />
          </div>
          <div class="col">
            <label>Grupo</label>
            <BaseSelect v-model="formComprobante.GRU_ID" :options="grupoOptions" placeholder="Todos los grupos" />
          </div>
          <div class="col">
            <label>Fecha Desde</label>
            <InputBase type="date" v-model="formComprobante.fechaDesde" />
          </div>
          <div class="col">
            <label>Fecha Hasta</label>
            <InputBase type="date" v-model="formComprobante.fechaHasta" />
          </div>
          <div class="col auto">
            <label class="invisible">Buscar</label>
            <BaseButton class="btn-standard" variant="primary" @click="buscarPagosParaComprobante" :disabled="cargandoPagosComprobante">
              <AppIcons name="search" :size="16" /> {{ cargandoPagosComprobante ? 'Buscando...' : 'Buscar Pagos' }}
            </BaseButton>
          </div>
        </div>

        <!-- Tabla de resultados para comprobantes -->
        <div v-if="pagosBuscadosComprobante" class="lista" style="margin-top: 20px;">
          <div class="lista-header">
            <h5>Pagos Encontrados ({{ pagosParaComprobante.length }})</h5>
            <div class="acciones">
              <BaseButton size="sm" variant="secondary" @click="toggleSelectAllComprobante(true)">Seleccionar todos</BaseButton>
              <BaseButton size="sm" variant="secondary" @click="toggleSelectAllComprobante(false)">Deseleccionar</BaseButton>
            </div>
          </div>
          <div class="table-wrapper" style="max-height: 300px;">
            <table>
              <thead>
                <tr>
                  <th style="width: 32px;"><input type="checkbox" @change="toggleSelectAllComprobante($event.target.checked)" /></th>
                  <th>Nombre</th>
                  <th>Concepto</th>
                  <th>Monto</th>
                  <th>Fecha</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="cargandoPagosComprobante"><td colspan="5" class="placeholder">Cargando...</td></tr>
                <tr v-else-if="!pagosParaComprobante.length"><td colspan="5" class="placeholder">No se encontraron pagos con esos filtros.</td></tr>
                <tr v-for="p in pagosParaComprobante" :key="p.PAP_ID">
                  <td><input type="checkbox" :value="p.PAP_ID" v-model="seleccionadosComprobante" /></td>
                  <td data-label="Nombre">{{ p.persona_nombre }}</td>
                  <td data-label="Concepto">{{ p.concepto_descripcion }}</td>
                  <td data-label="Monto">${{ (p.PAP_MONTO || 0).toLocaleString('es-CL') }}</td>
                  <td data-label="Fecha">{{ dateCL(p.PAP_FECHA_PAGO) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Acciones para comprobantes -->
        <div v-if="seleccionadosComprobante.length" class="acciones center" style="margin-top: 20px;">
          <div class="resumen" style="margin-bottom: 10px;">
            <div>Seleccionados: <strong>{{ seleccionadosComprobante.length }}</strong></div>
            <div class="total">Total: <strong>${{ totalSeleccionadoComprobante.toLocaleString('es-CL') }}</strong></div>
          </div>
          <BaseButton variant="success" class="btn-standard" @click="generarComprobantePDF">
            <AppIcons name="download" :size="16" /> Generar Comprobante PDF
          </BaseButton>
        </div>
      </section>
    </div>

    <!-- ===================== SECCIÓN: PAGOS A PROVEEDORES ===================== -->
    <div v-else-if="tab === 'proveedores'" class="card card-registro">
      <section class="panel panel-box">
        <div class="panel-title">
          <h3>Pagos a Proveedores</h3>
          <p>Registra egresos destinados a proveedores de servicios o productos.</p>
        </div>

        <div class="grid grid-proveedor">
          <div class="col"><label>Nombre o Razón Social *</label><InputBase v-model="formProveedor.nombre" placeholder="Ej: Imprenta Central" /></div>
          <div class="col"><label>RUT del Proveedor *</label><InputBase v-model="formProveedor.rut" placeholder="Ej: 76.123.456-7" /></div>
          <div class="col"><label>Concepto de Egreso *</label><BaseSelect v-model="formProveedor.COC_ID" :options="conceptosEgresoOptions" placeholder="Seleccione concepto" /></div>
          <div class="col half"><label>Valor Pagado *</label><div class="with-prefix"><span class="prefix">$</span><input type="number" min="0" v-model.number="formProveedor.PAP_MONTO" /></div></div>
          <div class="col half"><label>Fecha de Pago *</label><InputBase type="date" v-model="formProveedor.PAP_FECHA_PAGO" /></div>
          <div class="col span-2"><label>Comentario / Observación</label><textarea class="comentario-input" v-model="formProveedor.observacion" maxlength="200" placeholder="Nº de factura, detalle del servicio, etc."></textarea></div>
          <div class="col full comprobante-wrapper"><label>Comprobante (Opcional)</label><input ref="fileProveedorRef" type="file" accept=".pdf,.jpg,.jpeg,.png" @change="onFileProveedor" /></div>
        </div>

        <div class="acciones center acciones-individual">
          <BaseButton variant="success" class="btn-standard" :disabled="!puedeRegistrarProveedor" @click="registrarPagoProveedor"><AppIcons name="save" :size="16" /> Registrar Egreso</BaseButton>
          <BaseButton variant="secondary" class="btn-standard" @click="limpiarProveedor"><AppIcons name="x" :size="16" /> Limpiar</BaseButton>
        </div>
      </section>
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

    <!-- Modal Confirmar Cambios de Edición -->
    <BaseModal v-model="modalConfirmarEdicion" class="pago-modal">
      <template #default>
        <div class="confirm-content">
          <div class="confirm-icon">✏️</div>
          <p style="font-weight: 600; margin-bottom: 12px;">Se modificarán los siguientes campos:</p>
          <div style="text-align: left; background: #f9fafb; padding: 12px; border-radius: 6px; margin-bottom: 16px;">
            <div v-for="(cambio, index) in cambiosDetectados" :key="index" style="margin-bottom: 6px; font-size: 13px;">
              • {{ cambio }}
            </div>
          </div>
          <p style="font-weight: 600;">¿Está seguro de guardar estos cambios?</p>
          <div class="confirm-actions modal-actions">
            <BaseButton
              variant="secondary"
              class="btn-modal"
              @click="cancelarEdicion"
            >
              <AppIcons name="x" :size="16" /> Cancelar
            </BaseButton>
            <BaseButton
              variant="success"
              class="btn-modal"
              @click="confirmarEdicion"
            >
              <AppIcons name="check" :size="16" /> Guardar
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
          <div v-if="buscandoPersonasTransferir" class="estado-carga">
            <div class="spinner"></div> Buscando...
          </div>
          <div v-if="personasEncontradasTransferir.length" class="resultados" @click="seleccionarPersonaParaTransferir(p)">
             <div
              v-for="p in personasEncontradasTransferir"
              :key="p.id"
              class="resultado"
              @click="seleccionarPersonaParaTransferir(p)"
            >
              <div class="resultado-left">
                <strong>{{ p.nombre }}</strong>
                <span class="muted">{{ p.rut }}</span>
              </div>
              <BaseButton size="sm" variant="secondary" class="btn-action">Elegir</BaseButton>
            </div>
          </div>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre nuevo participante</label>
              <InputBase v-model="transferForm.nombre" readonly placeholder="Selecciona una persona" />
            </div>
            <div class="row">
              <label>RUT nuevo participante</label>
              <InputBase v-model="transferForm.rut" readonly />
            </div>
            <div class="row">
              <label>Tipo de devolución</label>
              <select v-model="transferForm.tipo" disabled>
                <option value="total">Devolución / Transferencia Total</option>
                <option value="parcial">Devolución / Transferencia Parcial</option>
              </select>
            </div>
            <div class="row" v-if="transferForm.tipo === 'parcial'">
              <label>Monto a transferir</label>
              <input
                type="number"
                min="0"
                disabled
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
              :disabled="!transferForm.personaId"
            >
              <AppIcons name="check" :size="16" /> Confirmar
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal Ver Detalle -->
    <BaseModal v-model="modalVerDetalle" class="pago-modal">
      <template #default>
        <div class="modal-edit">
          <header class="modal-header">
            <h3>Detalle del Pago</h3>
            <BaseButton
              variant="secondary"
              size="sm"
              @click="modalVerDetalle = false"
            >
              <AppIcons name="x" :size="16" /> Cerrar
            </BaseButton>
          </header>

          <div class="form-fields-grid">
            <div class="row">
              <label>Nombre</label>
              <input type="text" :value="pagoDetalle.nombre" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>RUT</label>
              <input type="text" :value="pagoDetalle.rut" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Curso</label>
              <input type="text" :value="pagoDetalle.curso" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Grupo</label>
              <input type="text" :value="pagoDetalle.grupo" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Concepto</label>
              <input type="text" :value="pagoDetalle.concepto" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Monto</label>
              <input type="text" :value="pagoDetalle.monto" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Fecha de Pago</label>
              <input type="text" :value="pagoDetalle.fecha" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row">
              <label>Método de Pago</label>
              <input type="text" :value="pagoDetalle.metodo" readonly disabled style="background: #f9fafb; border: 1px solid #d1d5db; padding: 8px 10px; border-radius: 6px; color: #374151; pointer-events: none; cursor: not-allowed;" />
            </div>
            <div class="row full-width">
              <label>Observación</label>
              <textarea 
                class="comentario-input" 
                :value="pagoDetalle.observacion" 
                readonly
                disabled
                style="resize: none; background: #f9fafb; color: #374151; pointer-events: none; cursor: not-allowed;"
              ></textarea>
            </div>
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
import authService from '@/services/authService.js'
import NotificationToast from '@/components/NotificationToast.vue'
import { format, parseISO } from 'date-fns'
import jsPDF from 'jspdf'
import * as XLSX from 'xlsx'
import 'jspdf-autotable'


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
  } catch {
    return f;
  }
}

export default {
  name: 'PagosView',
  components: { AppIcons, InputBase, BaseSelect, BaseButton, BaseModal, NotificationToast },
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
      filtroEstado: '',
      filtroCurso: '',
      filtroGrupo: '',
      pagos: [],
      cargandoPagos: false,
      errorPagos: null,
      seleccionadosHistorico: [],

      modalEditar: false,
      pagoEdit: {},
      pagoEditOriginal: {},
      guardando: false,
      modalConfirmarEdicion: false,
      cambiosDetectados: [],

      modalAnular: false,
      pagoAnular: null,

      modalTransferir: false,
      pagoTransferir: null,
      buscandoPersonasTransferir: false,
      personasEncontradasTransferir: [],
      transferForm: {
        q: '',
        personaId: null,
        nombre: '', // Nombre de la nueva persona
        rut: '',
        email: '',
        tipo: 'total',
        monto_parcial: null
      },

      modalVerDetalle: false,
      pagoDetalle: {
        nombre: '',
        rut: '',
        curso: '',
        grupo: '',
        concepto: '',
        monto: '',
        fecha: '',
        metodo: '',
        observacion: ''
      }
      ,
      formComprobante: {
        tipo: 'ingreso',
        fechaDesde: '',
        fechaHasta: '',
        CUR_ID: '',
        GRU_ID: '',
      seccion: '',
        COC_ID: ''
      },
      pagosParaComprobante: [],
      cargandoPagosComprobante: false,
      pagosBuscadosComprobante: false, // Para saber si ya se hizo una búsqueda
      seleccionadosComprobante: [],
      conceptosOptions: [],

      formProveedor: {
        nombre: '',
        rut: '',
        COC_ID: null,
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      },
      // UI state
      submittingIndividual: false,
      toastVisible: false,
      toastMessage: '',
      toastIcon: '',
      debounceTimer: null
    };
  },
  watch: {
    tab(newTab, oldTab) {
      if (newTab === 'historico' && oldTab !== 'historico') {
        this.cargarPagos(true); // Forzar recarga al cambiar a la pestaña de histórico
      }
    },
    // Implementa debounce para la búsqueda de personas en el registro individual
    buscarPersonaQ(newQuery) {
      if (this.debounceTimer) clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.buscarPersonas(newQuery), 300);
      },
    // Implementa debounce para la búsqueda en el histórico
    filtroQ() {
      if (this.debounceTimer) clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.cargarPagos(true), 300);
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
      const isEgreso = this.formInd.tipoPago === 'egreso';
      return (
        this.formInd.personaId &&
        this.formInd.CUR_ID &&
        this.formInd.COC_ID &&
        this.formInd.tipoPago &&
        this.formInd.PAP_MONTO > 0 &&
        this.formInd.PAP_FECHA_PAGO &&
        (isEgreso || this.formInd.file)
      );
    },
    puedeRegistrarMasivo () {
      return (
        this.seleccionados.length &&
        this.formMasivo.CUR_ID &&
        this.formMasivo.GRU_ID &&
        this.formMasivo.COC_ID &&
        this.formMasivo.tipoPago &&
        this.formMasivo.PAP_MONTO > 0 &&
        this.formMasivo.PAP_FECHA_PAGO &&
        (this.formMasivo.tipoPago === 'egreso' || this.formMasivo.file)
      );
    },
    valorPorPersonaMasivo() {
      if (!this.formMasivo.PAP_MONTO || !this.seleccionados.length) return 0;
      return Math.round(this.formMasivo.PAP_MONTO / this.seleccionados.length);
    },
    totalSeleccionadoComprobante() {
      if (!this.seleccionadosComprobante.length) return 0;
      return this.pagosParaComprobante
        .filter(p => this.seleccionadosComprobante.includes(p.PAP_ID))
        .reduce((total, p) => total + (p.PAP_MONTO || 0), 0);
    },
    conceptosEgresoOptions() {
      return this.conceptosOptions.filter(c => c.tipo === 'egreso');
    },
    puedeRegistrarProveedor() {
      return this.formProveedor.nombre &&
             this.formProveedor.rut &&
             this.formProveedor.COC_ID &&
             this.formProveedor.PAP_MONTO > 0 &&
             this.formProveedor.PAP_FECHA_PAGO;
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
        const cursosResponse = await cursosService.cursos.list({ page_size: 20 })
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

      try {
        const conceptosResponse = await mantenedoresService.conceptoContable.list();
        const conceptos = Array.isArray(conceptosResponse) ? conceptosResponse : (conceptosResponse.results || []);
        this.conceptosOptions = conceptos.map(c => ({
          value: c.COC_ID,
          label: c.COC_DESCRIPCION,
          tipo: c.COC_TIPO
        }));
      } catch (e) {
        console.error('Error cargando conceptos contables:', e);
        this.conceptosOptions = [];
      }
    },

    // Helper expuesto para el template: formatea fechas para mostrar en CL
    dateCL (f) {
            try {
        return dateCL(f)
      } catch {
        return f || '-'
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
      const termRaw = (q || '').trim();
      if (!termRaw) {
        this.personasEncontradas = []
        return
      }

      // Normalizar entrada (quitar puntos, espacios)
      const termClean = termRaw.replace(/\./g, '').replace(/\s+/g, '')
      let params = {}

      // Detectar si es solo dígitos (parcial o completo RUT)
      if (/^\d+$/.test(termClean)) {
        // Es un RUT parcial o completo: buscar por run
        params = { run: termClean }
      } else if (/^\d{7,8}[0-9kK]$/i.test(termClean)) {
        // RUT con DV: separar y enviar ambos
        const rutMatch = termClean.match(/^(\d{7,8})([0-9kK])$/i)
        if (rutMatch) {
          params = { run: rutMatch[1], dv: rutMatch[2].toUpperCase() }
        }
      } else {
        // Buscar por nombre y/o apellido
        const parts = termRaw.split(/\s+/)
        if (parts.length === 1) params = { nombre: termRaw }
        else params = { nombre: parts[0], apellido: parts.slice(1).join(' ') }
      }

      this.buscandoPersonas = true
      try {
        const response = await personasService.personas.list(params)
        const arr = Array.isArray(response) ? response : (response.results || [])
        this.personasEncontradas = arr.map(p => ({
          id: p.PER_ID || p.id,
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
        tipoPago: 'ingreso',
        COC_ID: null,
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
      if (this.submittingIndividual) return
      this.submittingIndividual = true
      try {
        const fd = new FormData()
        // Campos esperados por el backend (modelo): PER_ID, CUR_ID, USU_ID, PAP_VALOR, PAP_FECHA_HORA, PAP_OBSERVACION, PAP_TIPO
        fd.append('PER_ID', this.formInd.personaId)
        if (this.formInd.CUR_ID) fd.append('CUR_ID', this.formInd.CUR_ID)
        // PAP_VALOR en vez de PAP_MONTO (modelo usa PAP_VALOR)
        if (this.formInd.PAP_MONTO !== null && this.formInd.PAP_MONTO !== undefined) fd.append('PAP_VALOR', this.formInd.PAP_MONTO)
        if (this.formInd.COC_ID) fd.append('COC_ID', this.formInd.COC_ID)
        // En el backend se usa PAP_FECHA_HORA; enviar la fecha seleccionada como PAP_FECHA_HORA
        if (this.formInd.PAP_FECHA_PAGO) fd.append('PAP_FECHA_HORA', this.formInd.PAP_FECHA_PAGO)
        if (this.formInd.observacion) {
          fd.append('PAP_OBSERVACION', this.formInd.observacion)
        }
        if (this.formInd.file) fd.append('comprobante', this.formInd.file)
        // PAP_TIPO: 1 = Ingreso, 2 = Egreso
        fd.append('PAP_TIPO', this.formInd.tipoPago === 'egreso' ? 2 : 1)
        // PAP_ESTADO: 1 = Pagado (al registrar pago individual asumimos pagado)
        fd.append('PAP_ESTADO', 1)

        // Intentar resolver USU_ID desde el token para cumplir con el campo requerido en el modelo
        try {
          const current = await authService.getCurrentUser()
          const usuId = current && (current.id || current.USU_ID || (current.payload && current.payload.USU_ID)) ? (current.id || current.USU_ID || current.payload?.USU_ID) : null
          if (usuId) fd.append('USU_ID', usuId)
        } catch (e) {
          // no bloquear el envío si no se puede resolver el usuario; el backend puede inferirlo
          console.warn('No se pudo resolver USU_ID localmente:', e && e.message)
        }

        await pagosService.pagos.create(fd)
        // Mostrar toast exitoso
        this.toastMessage = 'Pago individual registrado correctamente'
        this.toastIcon = 'check'
        this.toastVisible = true
        this.limpiarIndividual()
        this.cargarPagos()
      } catch (e) {
        console.error('Error registrando pago individual', e)
        this.toastMessage = 'Error registrando pago: ' + (e && e.message ? e.message : '')
        this.toastIcon = 'x'
        this.toastVisible = true
      } finally {
        this.submittingIndividual = false
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
          grupo: this.formMasivo.GRU_ID, curso: this.formMasivo.CUR_ID
        })
        const arr = Array.isArray(response) ? response : (response.results || [])
        this.participantes = arr.map(p => ({
          id: p.PER_ID,
          nombre: `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: (p.PER_RUN && p.PER_DV) ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
          email: p.PER_MAIL || ''
                }))
        this.seleccionados = []
      } catch {
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
        tipoPago: 'ingreso',
        COC_ID: null,
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
        fd.append('COC_ID', this.formMasivo.COC_ID);
        fd.append('PAP_FECHA_PAGO', this.formMasivo.PAP_FECHA_PAGO)
        if (this.formMasivo.observacion) {
          fd.append('PAP_OBSERVACION', this.formMasivo.observacion)
        }
        // PAP_TIPO: 1 = Ingreso, 2 = Egreso
        fd.append('PAP_TIPO', this.formMasivo.tipoPago === 'egreso' ? 2 : 1)
        this.seleccionados.forEach(id =>
          fd.append('PER_IDS', id)
        )
        fd.append('comprobante', this.formMasivo.file)
        fd.append('MET_ID', 1) // Asumiendo 1 para Transferencia
        
        await pagosService.pagos.createMasivo(fd)

        this.toastMessage = 'Pago masivo registrado correctamente'
        this.toastIcon = 'check'
        this.toastVisible = true
                this.limpiarMasivo()
        this.cargarPagos()
      } catch {
        this.toastMessage = 'Error registrando pago masivo'
        this.toastIcon = 'x'
        this.toastVisible = true
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
      if (this.cargandoPagos && !force) return;
      this.cargandoPagos = true
      this.errorPagos = null
      try {
        let searchTerm = (this.filtroQ || '').trim();
        if (/^\d{7,8}$/.test(searchTerm)) {
          searchTerm = this.formatRut(searchTerm);
        }

        const estadoMap = { pagado: 1, anulado: 2 }
        const params = {}
        if (searchTerm) params.search = searchTerm
        if (this.filtroCurso) params.CUR_ID = this.filtroCurso
        if (this.filtroGrupo) params.GRU_ID = this.filtroGrupo
        if (this.filtroEstado) {
          const mapped = estadoMap[this.filtroEstado]
          if (mapped) params.estado = mapped
        }

        const response = await pagosService.pagos.list(params)
        let rawList = []
        if (Array.isArray(response)) rawList = response
        else if (response && Array.isArray(response.results)) rawList = response.results
        else {
          console.warn('La respuesta de la API de pagos no es un array:', response)
          rawList = []
        }

        // Normalizar cada pago para que la plantilla use campos consistentes
        this.pagos = rawList.map(r => {
          const persona = r.persona || r.PER_ID || null
          const personaNombre = persona && (persona.PER_NOMBRES || persona.name || persona.nombre)
            ? `${persona.PER_NOMBRES || ''} ${persona.PER_APELPTA || persona.PER_APELLIDO || ''}`.trim()
            : (r.persona_nombre || r.PER_NOMBRE || '')
          const personaRut = persona && (persona.PER_RUN || persona.run)
            ? `${persona.PER_RUN || persona.run}${persona.PER_DV ? ('-' + persona.PER_DV) : ''}`
            : (r.persona_rut || r.PER_RUN || '')

          const monto = r.PAP_VALOR !== undefined ? Number(r.PAP_VALOR) : (r.PAP_MONTO !== undefined ? Number(r.PAP_MONTO) : null)
          const fecha = r.PAP_FECHA_HORA || r.PAP_FECHA_PAGO || r.PAP_FECHA || null

          return {
            // conservar campos originales por si otras funciones los usan
            ...r,
            id: r.PAP_ID || r.id,
            PAP_ID: r.PAP_ID || r.id,
            PAP_MONTO: monto,
            PAP_VALOR: monto,
            PAP_FECHA_PAGO: fecha,
            persona_nombre: personaNombre || r.persona_nombre || '',
            persona_rut: personaRut || r.persona_rut || '',
            MET_DESCRIPCION: r.MET_DESCRIPCION || r.met_descripcion || r.METODO || 'Transferencia'
          }
        })
      } catch (e) {
        console.error('Error al cargar pagos:', e)
        this.pagos = []
        this.errorPagos = 'No fue posible cargar pagos. Verifica el backend.'
      } finally {
        this.cargandoPagos = false
      }
    },
    /**
     * Exporta los pagos actualmente visibles en la tabla a un archivo CSV.
     */
    exportarExcel () {
      if (this.pagos.length === 0) {
        this.toastMessage = 'No hay datos para exportar'
        this.toastIcon = 'alert-circle'
        this.toastVisible = true
        return;
      }

      const rowsToExport = this.pagos.map(p => {
        const valorCuota = p.valor_cuota || 0; // Assuming this data comes from the API
        const valorPagado = p.PAP_MONTO || 0;
        return {
          'Rut': p.persona_rut,
          'Nombre': p.persona_nombre?.split(' ')[0] || '',
          'Apellidos': p.persona_nombre?.split(' ').slice(1).join(' ') || '',
          'Correo electrónico': p.persona_email || '',
          'Grupo': p.grupo_nombre || '',
          'Distrito': p.distrito_nombre || '',
          'Zona': p.zona_nombre || '',
          'Curso': this.cursoLabel(p.CUR_ID),
          'Valor Cuota': valorCuota,
          'Valor Pagado': valorPagado,
          'Valor Adeudado': valorCuota - valorPagado,
          'Fecha Ultimo Pago': dateCL(p.PAP_FECHA_PAGO)
        };
      });

      const ws = XLSX.utils.json_to_sheet(rowsToExport);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Pagos");
      XLSX.writeFile(wb, "Pagos_Historico.xlsx");
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

    // ===================================================================
    // ACCIONES DE FILA (Ver, Editar, Anular, etc.)
    // ===================================================================
    /**
     * Muestra el detalle completo de un pago en un modal.
     * @param {object} p - El objeto del pago.
     */
    verDetalle (p) {
      // Buscar el nombre del grupo
      const grupo = this.grupoOptions.find(g => String(g.value) === String(p.GRU_ID));
      const grupoNombre = grupo ? grupo.label : (p.GRU_ID || '-');
      
      // Buscar el nombre del concepto
      const concepto = this.conceptosOptions.find(c => String(c.value) === String(p.COC_ID));
      const conceptoNombre = concepto ? concepto.label : (p.COC_ID || '-');

      this.pagoDetalle = {
        nombre: p.persona_nombre || '-',
        rut: p.persona_rut || '-',
        curso: this.cursoLabel(p.CUR_ID),
        grupo: grupoNombre,
        concepto: conceptoNombre,
        monto: `$${(p.PAP_MONTO || 0).toLocaleString('es-CL')}`,
        fecha: this.dateCL(p.PAP_FECHA_PAGO),
        metodo: p.MET_DESCRIPCION || 'Transferencia',
        observacion: p.PAP_OBSERVACION || 'Sin observaciones'
      };
      this.modalVerDetalle = true;
    },
    /**
     * Abre el modal para transferir un pago a otra persona.
     * @param {object} p - El objeto del pago a transferir.
     */
    abrirCambioPersona (p) {
      this.personasEncontradasTransferir = [];
      this.buscandoPersonasTransferir = false;
      this.pagoCambio = p
      this.cambioForm = {
        nombre: '',
        rut: '',
        email: '',
        tipo: 'total',
        monto_parcial: null
      }
      this.modalTransferir = true
    },
    /**
     * Selecciona una persona de la lista de resultados de búsqueda para la transferencia
     * y rellena el formulario de transferencia con sus datos.
     * @param {object} p - El objeto de la persona seleccionada.
     */
    seleccionarPersonaParaTransferir(p) {
      this.transferForm.personaId = p.id;
      this.transferForm.nombre = p.nombre;
      this.transferForm.rut = p.rut;
      this.transferForm.email = p.email;
      this.personasEncontradasTransferir = []; // Ocultar resultados
      this.transferForm.q = p.nombre; // Poner el nombre en el input de búsqueda
    },
    /**
     * Confirma la transferencia de un pago. (Lógica de API pendiente)
     */
    async confirmarTransferencia () {
      if (!this.pagoTransferir || !this.transferForm.personaId) {
        this.toastMessage = 'Debes seleccionar una persona para realizar la transferencia'
        this.toastIcon = 'alert-circle'
        this.toastVisible = true
        return;
      }

      try {
        const payload = {
          pago_id: this.pagoTransferir.PAP_ID,
          nueva_persona_id: this.transferForm.personaId,
          // Aquí podrías agregar más datos si la API lo requiere, como el tipo de transferencia
        };

        console.log("Enviando payload de transferencia:", payload);

        // Suponiendo que tienes un nuevo endpoint para esto en tu servicio
        await pagosService.pagos.transferir(payload);

        this.toastMessage = `Pago transferido exitosamente a ${this.transferForm.nombre}`
        this.toastIcon = 'check-circle'
        this.toastVisible = true
        this.modalTransferir = false;
        await this.cargarPagos(true); // Recargar el historial para ver el cambio

      } catch (error) {
        console.error("Error al confirmar la transferencia:", error);
        this.toastMessage = 'Ocurrió un error al intentar transferir el pago'
        this.toastIcon = 'x'
        this.toastVisible = true
      }
    },
    /**
     * Busca una persona para realizar la transferencia de un pago.
     */
    async buscarPersonaParaTransferir() {
      const qRaw = (this.transferForm.q || '').trim()
      if (!qRaw) {
        this.personasEncontradasTransferir = []
        return
      }

      // Reutilizar la lógica de búsqueda por RUT/nombre
      const termClean = qRaw.replace(/\./g, '').replace(/\s+/g, '')
      let params = {}
      if (/^\d+$/.test(termClean)) {
        params = { run: termClean }
      } else if (/^\d{7,8}[0-9kK]$/i.test(termClean)) {
        const rutMatch = termClean.match(/^(\d{7,8})([0-9kK])$/i)
        if (rutMatch) {
          params = { run: rutMatch[1], dv: rutMatch[2].toUpperCase() }
        }
      } else {
        const parts = qRaw.split(/\s+/)
        if (parts.length === 1) params = { nombre: qRaw }
        else params = { nombre: parts[0], apellido: parts.slice(1).join(' ') }
      }

      this.buscandoPersonasTransferir = true
      try {
        const response = await personasService.personas.list(params)
        const arr = Array.isArray(response) ? response : (response.results || [])
        this.personasEncontradasTransferir = arr.map(p => ({
          id: p.PER_ID || p.id,
          nombre: `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''}`.trim(),
          rut: (p.PER_RUN && p.PER_DV) ? `${p.PER_RUN}-${p.PER_DV}` : (p.PER_RUN || ''),
          email: p.PER_MAIL || ''
        }))
      } catch {
        this.personasEncontradasTransferir = []
      } finally {
        this.buscandoPersonasTransferir = false
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
      // Guardar valores originales para comparación
      this.pagoEditOriginal = {
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
          this.toastMessage = 'El campo "Curso" es obligatorio'
          this.toastIcon = 'alert-circle'
          this.toastVisible = true
          return;
        }
        if (!this.pagoEdit.monto || this.pagoEdit.monto <= 0) {
          this.toastMessage = 'El campo "Monto" debe ser un valor positivo'
          this.toastIcon = 'alert-circle'
          this.toastVisible = true
          return;
        }
        if (!this.pagoEdit.fecha) {
          this.toastMessage = 'El campo "Fecha" es obligatorio'
          this.toastIcon = 'alert-circle'
          this.toastVisible = true
          return;
        }

        // Detectar cambios
        const cambios = []
        if (String(this.pagoEdit.curso) !== String(this.pagoEditOriginal.curso)) {
          const cursoAnterior = this.cursoLabel(this.pagoEditOriginal.curso)
          const cursoNuevo = this.cursoLabel(this.pagoEdit.curso)
          cambios.push(`Curso: "${cursoAnterior}" → "${cursoNuevo}"`)
        }
        if (Number(this.pagoEdit.monto) !== Number(this.pagoEditOriginal.monto)) {
          cambios.push(`Monto: $${Number(this.pagoEditOriginal.monto).toLocaleString('es-CL')} → $${Number(this.pagoEdit.monto).toLocaleString('es-CL')}`)
        }
        if (this.pagoEdit.fecha !== this.pagoEditOriginal.fecha) {
          cambios.push(`Fecha: ${this.dateCL(this.pagoEditOriginal.fecha)} → ${this.dateCL(this.pagoEdit.fecha)}`)
        }
        if (this.pagoEdit.observacion !== this.pagoEditOriginal.observacion) {
          cambios.push(`Observación: "${this.pagoEditOriginal.observacion || 'Sin observación'}" → "${this.pagoEdit.observacion || 'Sin observación'}"`)
        }

        // Si no hay cambios, mostrar mensaje
        if (cambios.length === 0) {
          this.toastMessage = 'No se detectaron cambios'
          this.toastIcon = 'info'
          this.toastVisible = true
          return;
        }

        // Guardar los cambios detectados y mostrar modal de confirmación
        this.cambiosDetectados = cambios
        this.modalConfirmarEdicion = true
      } catch (e) {
        console.error('Error validando edición:', e)
        this.toastMessage = 'Error validando cambios'
        this.toastIcon = 'x'
        this.toastVisible = true
      }
    },
    /**
     * Cancela la edición y cierra el modal de confirmación.
     */
    cancelarEdicion () {
      this.modalConfirmarEdicion = false
      this.toastMessage = 'Cambios cancelados'
      this.toastIcon = 'info'
      this.toastVisible = true
    },
    /**
     * Confirma y guarda los cambios de edición.
     */
    async confirmarEdicion () {
      try {
        this.modalConfirmarEdicion = false
        this.guardando = true
        const body = {
          CUR_ID: this.pagoEdit.curso,
          PAP_VALOR: this.pagoEdit.monto,
          PAP_FECHA_HORA: this.pagoEdit.fecha,
          PAP_OBSERVACION: this.pagoEdit.observacion
        }
        await pagosService.pagos.partialUpdate(this.pagoEdit.id, body)
        this.modalEditar = false
        await this.cargarPagos()
        this.toastMessage = 'Pago actualizado correctamente'
        this.toastIcon = 'check-circle'
        this.toastVisible = true
      } catch (e) {
        console.error('Error actualizando pago:', e)
        this.toastMessage = 'Error actualizando pago: ' + (e.message || '')
        this.toastIcon = 'x'
        this.toastVisible = true
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
        this.toastMessage = 'Pago anulado correctamente'
        this.toastIcon = 'check-circle'
        this.toastVisible = true
      } catch {
        this.toastMessage = 'Error al anular pago'
        this.toastIcon = 'x'
        this.toastVisible = true
      }
    },

    // ===================================================================
    // MÉTODOS PARA GENERACIÓN DE COMPROBANTES
    // ===================================================================
    async buscarPagosParaComprobante() {
      this.cargandoPagosComprobante = true;
      this.pagosBuscadosComprobante = true;
      this.pagosParaComprobante = [];
      this.seleccionadosComprobante = [];

      try {
        // Construir parámetros de búsqueda
        const params = {
          tipo: this.formComprobante.tipo,
          fecha_desde: this.formComprobante.fechaDesde || undefined,
          fecha_hasta: this.formComprobante.fechaHasta || undefined,
          CUR_ID: this.formComprobante.CUR_ID || undefined,
          GRU_ID: this.formComprobante.GRU_ID || undefined,
          COC_ID: this.formComprobante.COC_ID || undefined,
        };

        // Simulación de llamada a API. Reemplazar con el servicio real.
        // const response = await pagosService.pagos.list(params);
        // this.pagosParaComprobante = response.results || response;
        
        // Usamos los pagos existentes para la demo
        const todosLosPagos = await pagosService.pagos.list({});
        this.pagosParaComprobante = (todosLosPagos.results || todosLosPagos).filter(p => {
            const concepto = this.conceptosOptions.find(c => c.value === p.COC_ID);
            const tipoConcepto = concepto ? concepto.tipo : 'ingreso';
            
            const coincideTipo = tipoConcepto === this.formComprobante.tipo;
            const coincideFechaDesde = !params.fecha_desde || new Date(p.PAP_FECHA_PAGO) >= new Date(params.fecha_desde);
                        const coincideFechaHasta = !params.fecha_hasta || new Date(p.PAP_FECHA_PAGO) <= new Date(params.fecha_hasta);
            const coincideCurso = !params.CUR_ID || String(p.CUR_ID) === String(params.CUR_ID);
            const coincideGrupo = !params.GRU_ID || String(p.GRU_ID) === String(params.GRU_ID);
            const coincideConcepto = !params.COC_ID || String(p.COC_ID) === String(params.COC_ID);

            return coincideTipo && coincideFechaDesde && coincideFechaHasta && coincideCurso && coincideGrupo && coincideConcepto;
        });

      } catch (e) {
        console.error("Error buscando pagos para comprobante:", e);
        alert("No se pudieron cargar los pagos para el comprobante.");
      } finally {
        this.cargandoPagosComprobante = false;
      }
    },

    toggleSelectAllComprobante(checked) {
      this.seleccionadosComprobante = checked ? this.pagosParaComprobante.map(p => p.PAP_ID) : [];
    },

    async generarComprobantePDF() {
      const seleccionados = this.pagosParaComprobante.filter(p => this.seleccionadosComprobante.includes(p.PAP_ID));
      if (seleccionados.length === 0) {
        this.toastMessage = 'No hay pagos seleccionados para generar el comprobante'
        this.toastIcon = 'alert-circle'
        this.toastVisible = true
        return;
      }

      const doc = new jsPDF();
      const tipoComprobante = this.formComprobante.tipo.charAt(0).toUpperCase() + this.formComprobante.tipo.slice(1);

      // Encabezado
      doc.setFontSize(18);
      doc.text(`Comprobante de ${tipoComprobante}`, 14, 22);
      doc.setFontSize(11);
      doc.setTextColor(100);
      doc.text(`Fecha de generación: ${format(new Date(), 'dd-MM-yyyy')}`, 14, 30);

      // Resumen
      doc.setFontSize(12);
      doc.text('Resumen', 14, 45);
      doc.autoTable({
        startY: 50,
        head: [['Concepto', 'Valor']],
        body: [
          ['Monto Total', `$${this.totalSeleccionadoComprobante.toLocaleString('es-CL')}`],
          ['Cantidad de Transacciones', seleccionados.length],
        ],
        theme: 'striped',
        headStyles: { fillColor: [44, 90, 160] },
      });

      // Detalle de pagos
      const tableBody = seleccionados.map(p => [
        dateCL(p.PAP_FECHA_PAGO),
        p.persona_nombre,
        p.persona_rut,
        p.concepto_descripcion,
        `$${(p.PAP_MONTO || 0).toLocaleString('es-CL')}`
      ]);

      doc.autoTable({
        head: [['Fecha', 'Nombre', 'RUT', 'Concepto', 'Monto']],
        body: tableBody,
        startY: doc.autoTable.previous.finalY + 10,
        headStyles: { fillColor: [44, 90, 160] },
      });

      // Guardar el PDF
      doc.save(`Comprobante_${tipoComprobante}_${format(new Date(), 'yyyyMMdd')}.pdf`);
    },
    // ===================================================================
    // MÉTODOS PARA PAGOS A PROVEEDORES
    // ===================================================================
    onFileProveedor(e) {
      this.formProveedor.file = e.target.files?.[0] || null;
    },

    limpiarProveedor() {
      this.formProveedor = {
        nombre: '',
        rut: '',
        COC_ID: null,
        PAP_MONTO: null,
        PAP_FECHA_PAGO: hoyISO(),
        observacion: '',
        file: null
      };
      if (this.$refs.fileProveedorRef) {
        this.$refs.fileProveedorRef.value = '';
      }
    },

    async registrarPagoProveedor() {
      if (!this.puedeRegistrarProveedor) return;
      try {
        const fd = new FormData();
        fd.append('proveedor_nombre', this.formProveedor.nombre);
        fd.append('proveedor_rut', this.formProveedor.rut);
        fd.append('COC_ID', this.formProveedor.COC_ID);
        fd.append('PAP_MONTO', this.formProveedor.PAP_MONTO);
        fd.append('PAP_FECHA_PAGO', this.formProveedor.PAP_FECHA_PAGO);
        if (this.formProveedor.observacion) fd.append('PAP_OBSERVACION', this.formProveedor.observacion);
        if (this.formProveedor.file) fd.append('comprobante', this.formProveedor.file);
        
        // Se necesitará un nuevo endpoint en el servicio, por ejemplo:
        // await pagosService.proveedores.create(fd);

        this.toastMessage = 'Pago a proveedor registrado correctamente (simulación)'
        this.toastIcon = 'check-circle'
        this.toastVisible = true
        this.limpiarProveedor();
      } catch (e) {
        this.toastMessage = 'Error registrando pago a proveedor'
        this.toastIcon = 'x'
        this.toastVisible = true
        console.error("Error en registrarPagoProveedor:", e);
      }
    }
    , // Mantener la coma

    /**
     * Formatea un RUT numérico (ej: 12345678) a un formato con puntos (ej: 12.345.678).
     * @param {string} rut - El RUT sin formato.
     * @returns {string} El RUT formateado.
     */
    formatRut(rut) {
      if (!rut) return '';
      const rutLimpio = String(rut).replace(/[^0-9]/g, '');
            if (rutLimpio.length < 2) return rutLimpio;
      const cuerpo = rutLimpio.slice(0, -1);
      // const dv = rutLimpio.slice(-1); // Aunque no se usa el DV para el formato con puntos, lo separamos.
      return cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
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
  flex-wrap: nowrap;
  gap: 4px;
  justify-content: center;
  align-items: center;
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

/* Ocultar la X del BaseModal en los modales de pagos */
.pago-modal :deep(.close-btn) {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
}

/* Regla adicional sin :deep() por si acaso */
.pago-modal .close-btn {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
}

/* Ajustar el ancho del modal-content dentro de pago-modal */
.pago-modal :deep(.modal-content) {
  width: auto !important;
  max-width: 550px !important;
}

.modal-edit,
.modal-transfer {
  width: 100%;
  max-width: 100%;
  max-height: 90vh;
  overflow: visible;
  padding: 0;
}

.modal-edit .modal-header,
.modal-transfer .modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-edit .form-fields-grid,
.modal-transfer .form-fields-grid {
  padding: 20px 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
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
  padding: 16px 20px 12px;
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
}

.confirm-icon {
  font-size: 36px;
  margin-bottom: 6px;
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

  /* En móvil, permitir que los botones se envuelvan */
  .acciones-buttons {
    flex-wrap: wrap;
  }
}

/* Estilo para texto largo en tablas */
.texto-largo {
  max-width: 200px; /* o el ancho que prefieras */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.button-group {
  display: flex;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 2px; /* Alineación visual */
}

.button-group .base-button {
  flex: 1;
  border-radius: 0;
  border: none !important;
  box-shadow: none !important;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.button-group .base-button:not(:last-child) {
  border-right: 1px solid #d1d5db;
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
