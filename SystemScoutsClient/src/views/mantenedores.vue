<template>
  <div class="mantenedores-scouts">
    <!-- Error Alert -->
    <div v-if="error" class="error-alert">
      <p>{{ error }}</p>
      <button @click="error = null">×</button>
    </div>

    <!-- Indicador de carga centrado con fondo difuminado -->
    <div v-if="cargando" class="loading-overlay" role="status" aria-live="polite">
      <div class="loading-content">
        <div class="spinner" aria-hidden="true"></div>
        <p>Cargando datos...</p>
      </div>
    </div>

    <!-- Selector de Mantenedores Fijo -->
    <div class="mantenedor-selector-fixed">
      <div class="selector-container">
        <div class="selector-header">
          <h2>⚙️ Mantenedores</h2>
        </div>
        <div class="selector-dropdown" ref="dropdownContainer">
          <button 
            class="mantenedor-dropdown-toggle"
            :class="{ 'active': isDropdownOpen }"
            @click="toggleDropdown"
          >
            <span class="selected-option">
              {{ getSelectedTabInfo().icon }} {{ getSelectedTabInfo().label }}
            </span>
            <div class="dropdown-icon" :class="{ 'rotate': isDropdownOpen }">▼</div>
          </button>
          
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <div 
              v-for="tab in tabs" 
              :key="tab.id"
              class="dropdown-item"
              :class="{ 'active': activeTab === tab.id }"
              @click="selectTab(tab.id)"
            >
              <span class="dropdown-item-icon">{{ tab.icon }}</span>
              <span class="dropdown-item-text">{{ tab.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content-expanded">
      <!-- Header eliminado para un diseño más limpio -->
      
      <!-- Zonas -->
      <MantenedorZonas 
        v-if="activeTab === 'zonas'" 
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />

      <!-- Modal de Confirmación Anular/Activar -->
      <div v-if="confirmModal && confirmModal.visible" class="modal-overlay" role="dialog" aria-modal="true">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ confirmModal.titulo }}</h3>
            <button class="modal-close" @click="cancelarConfirmacion">✕</button>
          </div>
          <div class="modal-body" style="padding:16px;">
            <p>{{ confirmModal.mensaje }}</p>
            <p v-if="confirmModal.elemento">
              <strong>Elemento:</strong> {{ confirmModal.elemento.descripcion }}
            </p>
          </div>
          <div class="modal-footer" style="display:flex; gap:8px; justify-content:flex-end; padding:16px;">
            <BaseButton variant="secondary" @click="cancelarConfirmacion"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
            <BaseButton :variant="confirmModal.accion === 'anular' ? 'secondary' : 'primary'" @click="confirmarConfirmacion" :disabled="confirmLoading">
              <AppIcons :name="confirmModal.accion === 'anular' ? 'block' : 'check'" :size="16" />
              <span v-if="!confirmLoading">{{ confirmModal.accion === 'anular' ? 'Confirmar Anulación' : 'Confirmar Activación' }}</span>
              <span v-else>Procesando...</span>
            </BaseButton>
          </div>
        </div>
      </div>
      
      <!-- Distritos -->
      <MantenedorDistritos
        v-if="activeTab === 'distritos'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />
      
      <!-- Grupos -->
      <MantenedorGrupos
        v-if="activeTab === 'grupos'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />
      
        <!-- Ramas -->
        <MantenedorRamas v-if="activeTab === 'ramas'" @show-message="handleMessage" @confirm-action="handleConfirmAction" />

        <!-- Tipos de Curso -->
        <MantenedorTiposCurso v-if="activeTab === 'tipos-curso'" @show-message="handleMessage" @confirm-action="handleConfirmAction" />
      
      <!-- Cargos -->
      <MantenedorCargos
        v-if="activeTab === 'cargos'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />
      
      <!-- Proveedores -->
      <MantenedorProveedores
        v-if="activeTab === 'proveedores'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />

      <!-- Alimentación -->
      <MantenedorAlimentacion
        v-if="activeTab === 'alimentacion'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />

      <!-- Comunas -->
      <MantenedorComunas
        v-if="activeTab === 'comunas'"
        @show-message="handleMessage"
        @confirm-action="handleConfirmAction"
      />

      <!-- Provincias -->
      <div v-if="activeTab === 'provincias'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🏞️ Gestión de Provincias</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('provincia')">
            <AppIcons name="plus" :size="16" /> Nueva Provincia
          </BaseButton>
        </div>
        
        <ModernMainScrollbar>
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>REGIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="provincia in provincias" :key="provincia.id">
                <td>{{ provincia.descripcion }}</td>
                <td>{{ getRegionNombre(provincia.region_id) }}</td>
                <td>
                  <span class="status-badge" :class="provincia.vigente ? 'status-active' : 'status-inactive'">
                    {{ provincia.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('provincia', provincia)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('provincia', provincia)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="provincia.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('provincia', provincia)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('provincia', provincia, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </ModernMainScrollbar>
      </div>

      <!-- Regiones -->
      <div v-if="activeTab === 'regiones'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🗾 Gestión de Regiones</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('region')">
            <AppIcons name="plus" :size="16" /> Nueva Región
          </BaseButton>
        </div>
        
        <ModernMainScrollbar>
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="region in regiones" :key="region.id">
                <td>{{ region.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="region.vigente ? 'status-active' : 'status-inactive'">
                    {{ region.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('region', region)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('region', region)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="region.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('region', region)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('region', region, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </ModernMainScrollbar>
      </div>

      <!-- Niveles -->
      <div v-if="activeTab === 'niveles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📊 Gestión de Niveles</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('nivel')">
            <AppIcons name="plus" :size="16" /> Nuevo Nivel
          </BaseButton>
        </div>
        
        <ModernMainScrollbar>
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="nivel in niveles" :key="nivel.id">
                <td>{{ nivel.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="nivel.vigente ? 'status-active' : 'status-inactive'">
                    {{ nivel.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('nivel', nivel)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('nivel', nivel)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="nivel.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('nivel', nivel)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('nivel', nivel, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </ModernMainScrollbar>
      </div>

      <!-- Estado Civil -->
      <div v-if="activeTab === 'estados-civiles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>💑 Gestión de Estado Civil</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('estadoCivil')">
            <AppIcons name="plus" :size="16" /> Nuevo Estado Civil
          </BaseButton>
        </div>
        
        <ModernMainScrollbar>
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="estadoCivil in estadosCiviles" :key="estadoCivil.id">
                <td>{{ estadoCivil.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="estadoCivil.vigente ? 'status-active' : 'status-inactive'">
                    {{ estadoCivil.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('estadoCivil', estadoCivil)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('estadoCivil', estadoCivil)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="estadoCivil.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('estadoCivil', estadoCivil)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('estadoCivil', estadoCivil, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </ModernMainScrollbar>
      </div>

      <!-- Roles -->
      <div v-if="activeTab === 'roles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>👤 Gestión de Roles</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('rol')">
            <AppIcons name="plus" :size="16" /> Nuevo Rol
          </BaseButton>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rol in roles" :key="rol.id">
                <td>{{ rol.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="rol.vigente ? 'status-active' : 'status-inactive'">
                    {{ rol.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('rol', rol)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('rol', rol)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="rol.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('rol', rol)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('rol', rol, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Conceptos Contables -->
      <div v-if="activeTab === 'conceptos-contables'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>💰 Gestión de Conceptos Contables</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('conceptoContable')">
            <AppIcons name="plus" :size="16" /> Nuevo Concepto
          </BaseButton>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>TIPO</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="concepto in conceptosContables" :key="concepto.id">
                <td>{{ concepto.descripcion }}</td>
                <td>{{ concepto.tipo }}</td>
                <td>
                  <span class="status-badge" :class="concepto.vigente ? 'status-active' : 'status-inactive'">
                    {{ concepto.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('conceptoContable', concepto)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('conceptoContable', concepto)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="concepto.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('conceptoContable', concepto)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('conceptoContable', concepto, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tipos de Archivo -->
      <div v-if="activeTab === 'tipos-archivo'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📁 Gestión de Tipos de Archivo</h2>
          <BaseButton variant="primary" @click="abrirModalCrear('tipoArchivo')">
            <AppIcons name="plus" :size="16" /> Nuevo Tipo
          </BaseButton>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>EXTENSIÓN</th>
                <th>ESTADO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoArchivo in tiposArchivo" :key="tipoArchivo.id">
                <td>{{ tipoArchivo.descripcion }}</td>
                <td>{{ tipoArchivo.extension }}</td>
                <td>
                  <span class="status-badge" :class="tipoArchivo.vigente ? 'status-active' : 'status-inactive'">
                    {{ tipoArchivo.vigente ? 'VIGENTE' : 'NO VIGENTE' }}
                  </span>
                </td>
                <td class="actions">
                  <BaseButton variant="secondary" class="btn-action" @click="verElemento('tipoArchivo', tipoArchivo)"><AppIcons name="eye" :size="16" /> Ver</BaseButton>
                  <BaseButton variant="secondary" class="btn-action" @click="editarElemento('tipoArchivo', tipoArchivo)"><AppIcons name="edit" :size="16" /> Editar</BaseButton>
                  <BaseButton v-if="tipoArchivo.vigente" variant="secondary" class="btn-action" @click="abrirConfirmacion('tipoArchivo', tipoArchivo)"><AppIcons name="block" :size="16" /> Anular</BaseButton>
                  <BaseButton v-else variant="primary" class="btn-action" @click="abrirConfirmacion('tipoArchivo', tipoArchivo, 'activar')"><AppIcons name="check" :size="16" /> Activar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Visualización -->
    <div v-if="modalActivo === 'ver'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 VISUALIZAR {{ getTipoNombre(tipoElemento) }}</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">UNILATERAL:</label>
              <div class="view-value">{{ elementoSeleccionado.unilateral ? 'SÍ' : 'NO' }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ESTADO:</label>
              <div class="view-value">
                <span class="status-badge" :class="elementoSeleccionado.vigente ? 'status-active' : 'status-inactive'">
                  {{ elementoSeleccionado.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </div>
            </div>

            <!-- Campos para otros tipos de elementos -->
            <div v-if="tipoElemento !== 'zona'" class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="['distrito', 'grupo', 'comuna', 'provincia'].includes(tipoElemento)" class="view-group">
              <label class="view-label">{{ getRelacionNombre(tipoElemento) }}:</label>
              <div class="view-value">{{ getRelacionValor(tipoElemento) }}</div>
            </div>
            <div v-if="['tipoCurso', 'alimentacion', 'conceptoContable'].includes(tipoElemento)" class="view-group">
              <label class="view-label">TIPO:</label>
              <div class="view-value">{{ elementoSeleccionado.tipo }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoCurso'" class="view-group">
              <label class="view-label">CANT. PARTICIPANTES:</label>
              <div class="view-value">{{ elementoSeleccionado.cant_participante }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoArchivo'" class="view-group">
              <label class="view-label">EXTENSIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.extension }}</div>
            </div>
          </div>
          <div class="form-actions">
            <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cerrar</BaseButton>
          </div>
        </div>
      </div>
    </div>


    <!-- Modal de Edición/Creación para Zonas ELIMINADO (Manejado por MantenedorZonas.vue) -->

    <!-- Modal de Edición/Creación para Distritos ELIMINADO (Manejado por MantenedorDistritos.vue) -->

    <!-- Modal de Edición/Creación para Grupos ELIMINADO (Manejado por MantenedorGrupos.vue) -->

    <!-- Modal de Edición/Creación para Ramas -->
    <!-- Modal de Edición/Creación para Ramas ELIMINADO (Manejado por MantenedorRamas.vue) -->

    <!-- Modal de Edición/Creación para Tipos de Curso -->
    <div v-if="modalActivo === 'crear-tipoCurso' || modalActivo === 'editar-tipoCurso'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} TIPO DE CURSO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarTipoCurso">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoCurso.descripcion"
                @input="formTipoCurso.descripcion = formTipoCurso.descripcion.toUpperCase()"
                placeholder="EJ: CURSO BÁSICO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formTipoCurso.tipo" required>
                <option :value="1">INICIAL</option>
                <option :value="2">MEDIO</option>
                <option :value="3">AVANZADO</option>
                <option :value="4">HABILITACIÓN</option>
                <option :value="5">VERIFICACIÓN</option>
                <option :value="6">INSTITUCIONAL</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">CANT. PARTICIPANTES:</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formTipoCurso.cant_participante"
                placeholder="EJ: 30"
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Cargos -->
    <div v-if="modalActivo === 'crear-cargo' || modalActivo === 'editar-cargo'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} CARGO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarCargo">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formCargo.descripcion"
                @input="formCargo.descripcion = formCargo.descripcion.toUpperCase()"
                placeholder="EJ: JEFE DE GRUPO"
                required
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Proveedores -->
    <div v-if="modalActivo === 'crear-proveedor' || modalActivo === 'editar-proveedor'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} PROVEEDOR</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarProveedor">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input type="text" class="form-control" v-model="formProveedor.descripcion" @input="formProveedor.descripcion = formProveedor.descripcion.toUpperCase()" placeholder="EJ: PROVEEDOR ABC" required />
            </div>
            <div class="form-group">
              <label class="form-label">CELULAR 1:</label>
              <input type="text" class="form-control" v-model="formProveedor.celular1" placeholder="+56 9 ..." />
            </div>
            <div class="form-group">
              <label class="form-label">CELULAR 2:</label>
              <input type="text" class="form-control" v-model="formProveedor.celular2" placeholder="Opcional" />
            </div>
            <div class="form-group">
              <label class="form-label">DIRECCIÓN:</label>
              <input type="text" class="form-control" v-model="formProveedor.direccion" placeholder="DIRECCIÓN" />
            </div>
            <div class="form-group">
              <label class="form-label">OBSERVACIÓN:</label>
              <input type="text" class="form-control" v-model="formProveedor.observacion" placeholder="Opcional" />
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Alimentación -->
    <div v-if="modalActivo === 'crear-alimentacion' || modalActivo === 'editar-alimentacion'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} ALIMENTACIÓN</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarAlimentacion">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formAlimentacion.descripcion"
                @input="formAlimentacion.descripcion = formAlimentacion.descripcion.toUpperCase()"
                placeholder="EJ: DIETA REGULAR"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formAlimentacion.tipo" required>
                <option :value="1">CON ALMUERZO</option>
                <option :value="2">SIN ALMUERZO</option>
              </select>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Comunas -->
    <div v-if="modalActivo === 'crear-comuna' || modalActivo === 'editar-comuna'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} COMUNA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarComuna">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formComuna.descripcion"
                @input="formComuna.descripcion = formComuna.descripcion.toUpperCase()"
                placeholder="EJ: CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">PROVINCIA:</label>
              <select class="form-control" v-model="formComuna.provincia_id" required>
                <option value="">SELECCIONE UNA PROVINCIA</option>
                <option v-for="provincia in provincias" :key="provincia.id" :value="provincia.id">
                  {{ provincia.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Provincias -->
    <div v-if="modalActivo === 'crear-provincia' || modalActivo === 'editar-provincia'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} PROVINCIA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarProvincia">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formProvincia.descripcion"
                @input="formProvincia.descripcion = formProvincia.descripcion.toUpperCase()"
                placeholder="EJ: CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">REGIÓN:</label>
              <select class="form-control" v-model="formProvincia.region_id" required>
                <option value="">SELECCIONE UNA REGIÓN</option>
                <option v-for="region in regiones" :key="region.id" :value="region.id">
                  {{ region.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Regiones -->
    <div v-if="modalActivo === 'crear-region' || modalActivo === 'editar-region'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} REGIÓN</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRegion">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRegion.descripcion"
                @input="formRegion.descripcion = formRegion.descripcion.toUpperCase()"
                placeholder="EJ: REGIÓN DEL BIOBÍO"
                required
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Niveles -->
    <div v-if="modalActivo === 'crear-nivel' || modalActivo === 'editar-nivel'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} NIVEL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarNivel">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formNivel.descripcion"
                @input="formNivel.descripcion = formNivel.descripcion.toUpperCase()"
                placeholder="EJ: NIVEL BÁSICO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">ORDEN:</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formNivel.orden"
                placeholder="EJ: 1"
                required
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Estado Civil -->
    <div v-if="modalActivo === 'crear-estadoCivil' || modalActivo === 'editar-estadoCivil'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} ESTADO CIVIL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarEstadoCivil">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formEstadoCivil.descripcion"
                @input="formEstadoCivil.descripcion = formEstadoCivil.descripcion.toUpperCase()"
                placeholder="EJ: SOLTERO/A"
                required
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Roles -->
    <div v-if="modalActivo === 'crear-rol' || modalActivo === 'editar-rol'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} ROL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRol">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRol.descripcion"
                @input="formRol.descripcion = formRol.descripcion.toUpperCase()"
                placeholder="EJ: ADMINISTRADOR"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formRol.tipo" required>
                <option :value="1">PARTICIPANTE</option>
                <option :value="2">FORMADORES</option>
                <option :value="3">APOYO FORMADORES</option>
                <option :value="4">ORGANIZACIÓN</option>
                <option :value="5">SERVICIO</option>
                <option :value="6">SALUD</option>
              </select>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Conceptos Contables -->
    <div v-if="modalActivo === 'crear-conceptoContable' || modalActivo === 'editar-conceptoContable'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} CONCEPTO CONTABLE</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarConceptoContable">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formConceptoContable.descripcion"
                @input="formConceptoContable.descripcion = formConceptoContable.descripcion.toUpperCase()"
                placeholder="EJ: MATRÍCULA"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formConceptoContable.tipo" required>
                <option value="">SELECCIONE UN TIPO</option>
                <option value="INGRESO">INGRESO</option>
                <option value="EGRESO">EGRESO</option>
              </select>
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Tipos de Archivo -->
    <div v-if="modalActivo === 'crear-tipoArchivo' || modalActivo === 'editar-tipoArchivo'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} TIPO DE ARCHIVO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarTipoArchivo">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoArchivo.descripcion"
                @input="formTipoArchivo.descripcion = formTipoArchivo.descripcion.toUpperCase()"
                placeholder="EJ: DOCUMENTO PDF"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">EXTENSIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoArchivo.extension"
                placeholder="EJ: .PDF"
                required
              >
            </div>
            <div class="form-actions">
              <BaseButton variant="secondary" @click="cerrarModal"><AppIcons name="close" :size="16" /> Cancelar</BaseButton>
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcons name="save" :size="16" />
                <span v-if="!saving">{{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}</span><span v-else>Procesando...</span>
              </BaseButton>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import MantenedorZonas from '@/components/mantenedores/MantenedorZonas.vue'
import MantenedorDistritos from '@/components/mantenedores/MantenedorDistritos.vue'
import MantenedorGrupos from '@/components/mantenedores/MantenedorGrupos.vue'
import MantenedorRamas from '@/components/mantenedores/MantenedorRamas.vue'
import MantenedorTiposCurso from '@/components/mantenedores/MantenedorTiposCurso.vue'
import MantenedorCargos from '@/components/mantenedores/MantenedorCargos.vue'
import MantenedorProveedores from '@/components/mantenedores/MantenedorProveedores.vue'
import MantenedorAlimentacion from '@/components/mantenedores/MantenedorAlimentacion.vue'
import MantenedorComunas from '@/components/mantenedores/MantenedorComunas.vue'

export default {
  name: 'MantenedoresScouts',
  components: { BaseButton, AppIcons, ModernMainScrollbar, MantenedorZonas, MantenedorDistritos, MantenedorGrupos, MantenedorRamas, MantenedorTiposCurso, MantenedorCargos, MantenedorProveedores, MantenedorAlimentacion, MantenedorComunas },
  setup() {
    // Estado reactivo
    const activeTab = ref('zonas')
    const modalActivo = ref('')
    const editando = ref(false)
    const tipoElemento = ref('')
    const elementoSeleccionado = ref(null)
    const isDropdownOpen = ref(false)
    const dropdownContainer = ref(null)
    const cargando = ref(false)
    const error = ref(null)
    const confirmModal = reactive({ visible: false, titulo: '', mensaje: '', accion: 'anular', tipo: '', elemento: null })
    const confirmLoading = ref(false)
    const saving = ref(false)
    const pendingConfirmAction = ref(null)
    
    // Estados de búsqueda
    const searchZonas = ref('')
    const searchDistritos = ref('')
    const searchGrupos = ref('')
    const filtroZona = ref('')
    const filtroDistrito = ref('')

    // Tabs de navegación (sidebar)
    const tabs = [
      { id: 'zonas', label: 'Zonas', icon: '🗺️' },
      { id: 'distritos', label: 'Distritos', icon: '📍' },
      { id: 'grupos', label: 'Grupos', icon: '👥' },
      { id: 'ramas', label: 'Ramas', icon: '🏕️' },
      { id: 'cargos', label: 'Cargos', icon: '👔' },
      { id: 'proveedores', label: 'Proveedores', icon: '🏷️' },
      { id: 'alimentacion', label: 'Alimentación', icon: '🍽️' },
      { id: 'comunas', label: 'Comunas', icon: '🏘️' },
      { id: 'provincias', label: 'Provincias', icon: '🏞️' },
      { id: 'regiones', label: 'Regiones', icon: '🗾' },
      { id: 'niveles', label: 'Niveles', icon: '📊' },
      { id: 'estados-civiles', label: 'Estado Civil', icon: '💑' },
      { id: 'roles', label: 'Roles', icon: '👤' },
      { id: 'conceptos-contables', label: 'Conceptos Contables', icon: '💰' },
      { id: 'tipos-archivo', label: 'Tipos de Archivo', icon: '📁' }
    ]

    // Datos reactivos para todos los mantenedores (inicialmente vacíos, se llenan desde la API)
    const regiones = ref([])
    const cargos = ref([])
    const provincias = ref([])
    const niveles = ref([])
    const estadosCiviles = ref([])
    const roles = ref([])
    const conceptosContables = ref([])
    const tiposArchivo = ref([])


    // Carga perezosa por pestaña: solo traer lo necesario según la vista activa
    const cargarDatos = async () => {
      cargando.value = true
      error.value = null // Limpiar errores previos
      try {
        // Función auxiliar para extraer el array de datos, venga con paginación o sin ella
        const getData = (resp) => {
          if (!resp) return []
          if (Array.isArray(resp)) return resp
          // soportar distintas envolturas de respuesta
          const r = resp
          return r.results || (r.data?.results) || r.data || r.items || []
        }
        // Determinar pestaña activa y cargar solo lo requerido
        const tab = activeTab.value
        const normalize = (arr, mapFn) => (arr || []).map(mapFn)

        if (tab === 'provincias') {
          const [respProvincias, respRegiones] = await Promise.all([
            mantenedoresService.provincia.list().catch(e => { console.error('Provincias:', e); return [] }),
            mantenedoresService.region.list().catch(e => { console.error('Regiones:', e); return [] })
          ])
          provincias.value = normalize(getData(respProvincias), p => ({ id: p.pro_id ?? p.PRO_ID ?? p.id, descripcion: (p.pro_descripcion ?? p.PRO_DESCRIPCION ?? p.DESCRIPCION ?? p.descripcion ?? '').toString(), region_id: (p.reg_id?.reg_id ?? p.REG_ID?.REG_ID ?? p.reg_id ?? p.REG_ID ?? p.region_id ?? null), vigente: (p.pro_vigente ?? p.PRO_VIGENTE ?? p.vigente ?? true) ? true : false }))
          regiones.value = normalize(getData(respRegiones), r => ({ id: r.reg_id ?? r.REG_ID ?? r.id, descripcion: (r.reg_descripcion ?? r.REG_DESCRIPCION ?? r.DESCRIPCION ?? r.descripcion ?? '').toString(), vigente: (r.reg_vigente ?? r.REG_VIGENTE ?? r.vigente ?? true) ? true : false }))
        } else if (tab === 'regiones') {
          const respRegiones = await mantenedoresService.region.list().catch(e => { console.error('Regiones:', e); return [] })
          regiones.value = normalize(getData(respRegiones), r => ({ id: r.reg_id ?? r.REG_ID ?? r.id, descripcion: (r.reg_descripcion ?? r.REG_DESCRIPCION ?? r.DESCRIPCION ?? r.descripcion ?? '').toString(), vigente: (r.reg_vigente ?? r.REG_VIGENTE ?? r.vigente ?? true) ? true : false }))
        } else if (tab === 'niveles') {
          const respNiveles = await mantenedoresService.nivel.list().catch(e => { console.error('Niveles:', e); return [] })
          niveles.value = normalize(getData(respNiveles), n => ({ id: n.niv_id ?? n.NIV_ID ?? n.id, descripcion: (n.niv_descripcion ?? n.NIV_DESCRIPCION ?? n.DESCRIPCION ?? n.descripcion ?? '').toString(), orden: n.niv_orden ?? n.NIV_ORDEN ?? n.orden ?? 0, vigente: (n.niv_vigente ?? n.NIV_VIGENTE ?? n.vigente ?? true) ? true : false }))
        } else if (tab === 'estados-civiles') {
          const respEstadosCiviles = await mantenedoresService.estadoCivil.list().catch(e => { console.error('EstadosCiviles:', e); return [] })
          estadosCiviles.value = normalize(getData(respEstadosCiviles), e => ({ id: e.esc_id ?? e.ESC_ID ?? e.id, descripcion: (e.esc_descripcion ?? e.ESC_DESCRIPCION ?? e.DESCRIPCION ?? e.descripcion ?? '').toString(), vigente: (e.esc_vigente ?? e.ESC_VIGENTE ?? e.vigente ?? true) ? true : false }))
        } else if (tab === 'roles') {
          const respRoles = await mantenedoresService.rol.list().catch(e => { console.error('Roles:', e); return [] })
          roles.value = normalize(getData(respRoles), r => ({ id: r.rol_id ?? r.ROL_ID ?? r.id, descripcion: (r.rol_descripcion ?? r.ROL_DESCRIPCION ?? r.DESCRIPCION ?? r.descripcion ?? '').toString(), tipo: r.rol_tipo ?? r.ROL_TIPO ?? r.tipo ?? '', vigente: (r.rol_vigente ?? r.ROL_VIGENTE ?? r.vigente ?? true) ? true : false }))
        } else if (tab === 'conceptos-contables') {
          const respConceptos = await mantenedoresService.conceptoContable.list().catch(e => { console.error('Conceptos:', e); return [] })
          conceptosContables.value = normalize(getData(respConceptos), c => ({ id: c.coc_id ?? c.COC_ID ?? c.id, descripcion: (c.coc_descripcion ?? c.COC_DESCRIPCION ?? c.DESCRIPCION ?? c.descripcion ?? '').toString(), vigente: (c.coc_vigente ?? c.COC_VIGENTE ?? c.vigente ?? true) ? true : false }))
        } else if (tab === 'tipos-archivo') {
          const respTiposArchivo = await mantenedoresService.tipoArchivos.list().catch(e => { console.error('TiposArchivo:', e); return [] })
          tiposArchivo.value = normalize(getData(respTiposArchivo), t => ({ id: t.tar_id ?? t.TAR_ID ?? t.id, descripcion: (t.tar_descripcion ?? t.TAR_DESCRIPCION ?? t.DESCRIPCION ?? t.descripcion ?? '').toString(), extension: t.TAR_EXTENSION ?? t.extension ?? '', vigente: (t.tar_vigente ?? t.TAR_VIGENTE ?? t.vigente ?? true) ? true : false }))
        }
      } catch (err) {
        error.value = 'Error al cargar datos: ' + err.message
        console.error(err)
      } finally {
        cargando.value = false
      }
    }

    onMounted(() => {
      cargarDatos()
      document.addEventListener('click', handleClickOutside)
    })

    // Recarga tras crear/editar/eliminar
    const recargar = cargarDatos

    // Formularios



    // Formularios adicionales para otros mantenedores
    const formProvincia = reactive({ id: null, descripcion: '', region_id: null, vigente: true })
    const formRegion = reactive({ id: null, descripcion: '', vigente: true })
    const formNivel = reactive({ id: null, descripcion: '', orden: 1, vigente: true })
    const formEstadoCivil = reactive({ id: null, descripcion: '', vigente: true })
    const formRol = reactive({ id: null, descripcion: '', tipo: 1, vigente: true })
    const formConceptoContable = reactive({ id: null, descripcion: '', tipo: '', vigente: true })
    const formTipoArchivo = reactive({ id: null, descripcion: '', extension: '', vigente: true })

    // Computed properties para filtros


    // Métodos de búsqueda activados por los botones "Buscar"




    // Métodos auxiliares

    const getProvinciaNombre = (provinciaId) => {
      const provincia = provincias.value.find(p => p.id === provinciaId)
      return provincia ? provincia.descripcion : 'NO ENCONTRADA'
    }

    const getRegionNombre = (regionId) => {
      const region = regiones.value.find(r => r.id === regionId)
      return region ? region.descripcion : 'NO ENCONTRADA'
    }

    const getTipoNombre = (tipo) => {
      const nombres = {
        'zona': 'ZONA',
        'distrito': 'DISTRITO',
        'grupo': 'GRUPO',
        'provincia': 'PROVINCIA',
        'region': 'REGIÓN',
        'nivel': 'NIVEL',
        'estadoCivil': 'ESTADO CIVIL',
        'rol': 'ROL',
        'conceptoContable': 'CONCEPTO CONTABLE',
        'tipoArchivo': 'TIPO DE ARCHIVO'
      }
      return nombres[tipo] || 'ELEMENTO'
    }

    const getRelacionNombre = (tipo) => {
      const relaciones = {
        'distrito': 'ZONA',
        'grupo': 'DISTRITO',
        'provincia': 'REGIÓN'
      }
      return relaciones[tipo] || ''
    }

    const getRelacionValor = (tipo) => {
      switch (tipo) {
        case 'comuna':
          return getProvinciaNombre(elementoSeleccionado.value.provincia_id)
        case 'provincia':
          return getRegionNombre(elementoSeleccionado.value.region_id)
        default:
          return ''
      }
    }

    // Métodos para el dropdown personalizado
    const getSelectedTabInfo = () => {
      const tab = tabs.find(t => t.id === activeTab.value)
      return tab || tabs[0]
    }

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const selectTab = async (tabId) => {
      activeTab.value = tabId
      isDropdownOpen.value = false // Cerrar dropdown después de seleccionar
      await cargarDatos()
    }

    // Cerrar dropdown al hacer clic fuera
    const handleClickOutside = (event) => {
      if (dropdownContainer.value && !dropdownContainer.value.contains(event.target)) {
        isDropdownOpen.value = false
      }
    }

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    // Métodos principales
    const abrirModalCrear = (tipo) => {
      modalActivo.value = `crear-${tipo}`
      editando.value = false
      tipoElemento.value = tipo
      elementoSeleccionado.value = null
      limpiarFormularios()
    }

    const verElemento = (tipo, elemento) => {
      modalActivo.value = 'ver'
      editando.value = false
      tipoElemento.value = tipo
      elementoSeleccionado.value = elemento
    }

    const editarElemento = (tipo, elemento) => {
      modalActivo.value = `editar-${tipo}`
      editando.value = true
      tipoElemento.value = tipo
      elementoSeleccionado.value = elemento
      cargarDatosFormulario(tipo, elemento)
    }

    const abrirConfirmacion = (tipo, elemento, accion = 'anular') => {
      confirmModal.visible = true
      confirmModal.tipo = tipo
      confirmModal.elemento = elemento
      confirmModal.accion = accion
      confirmModal.titulo = accion === 'anular' ? 'Confirmar Anulación' : 'Confirmar Activación'
      confirmModal.mensaje = accion === 'anular'
        ? '¿Está seguro que desea anular este registro?'
        : '¿Desea activar nuevamente este registro?'
    }
    const cancelarConfirmacion = () => {
      confirmModal.visible = false
      confirmModal.tipo = ''
      confirmModal.elemento = null
    }
    const confirmarConfirmacion = async () => {
      confirmLoading.value = true
      try {
        if (pendingConfirmAction.value) {
            await pendingConfirmAction.value()
            pendingConfirmAction.value = null
        } else if (confirmModal.accion === 'activar') {
          await habilitarElemento()
        } else {
          await anularElemento()
        }
        confirmModal.visible = false
      } catch (err) {
        console.error('Error confirmación:', err)
      } finally {
        confirmLoading.value = false
      }
    }


    // Nuevos métodos para anular y habilitar
    const anularElemento = async (tipo, elemento) => {
      try {
        // Resolver ID flexible (puede venir como id, <tipo>_id, etc.)
        const id = elemento?.id ?? elemento?.zon_id ?? elemento?.dis_id ?? elemento?.gru_id ?? elemento?.ram_id ?? elemento?.tcu_id ?? elemento?.car_id ?? elemento?.ali_id ?? elemento?.com_id ?? elemento?.pro_id ?? elemento?.reg_id ?? elemento?.niv_id ?? elemento?.esc_id ?? elemento?.rol_id ?? elemento?.coc_id ?? elemento?.tar_id
        if (!id) throw new Error('ID no disponible')

        // Mapear el nombre del campo vigente esperado por el backend
        const fieldMap = {
          zona: 'zon_vigente',
          distrito: 'dis_vigente',
          grupo: 'gru_vigente',
          rama: 'ram_vigente',
          tipoCurso: 'tcu_vigente',
          cargo: 'car_vigente',
          alimentacion: 'ali_vigente',
          comuna: 'com_vigente',
          provincia: 'pro_vigente',
          region: 'reg_vigente',
          nivel: 'niv_vigente',
          estadoCivil: 'esc_vigente',
          rol: 'rol_vigente',
          conceptoContable: 'coc_vigente',
          tipoArchivo: 'tar_vigente'
          ,proveedor: 'prv_vigente'
        }

        const fieldName = fieldMap[tipo] || 'vigente'
        const datosAPI = { [fieldName]: false }

        // Llamar al servicio correspondiente
        switch (tipo) {
          case 'zona':
            await mantenedoresService.zona.partialUpdate(id, datosAPI)
            break
          case 'distrito':
            await mantenedoresService.distrito.partialUpdate(id, datosAPI)
            break
          case 'grupo':
            await mantenedoresService.grupo.partialUpdate(id, datosAPI)
            break
          case 'tipoCurso':
            await mantenedoresService.tipoCursos.partialUpdate(id, datosAPI)
            break
          case 'cargo':
            await mantenedoresService.cargo.partialUpdate(id, datosAPI)
            break
          case 'alimentacion':
            await mantenedoresService.alimentacion.partialUpdate(id, datosAPI)
            break
          case 'comuna':
            await mantenedoresService.comuna.partialUpdate(id, datosAPI)
            break
          case 'provincia':
            await mantenedoresService.provincia.partialUpdate(id, datosAPI)
            break
          case 'region':
            await mantenedoresService.region.partialUpdate(id, datosAPI)
            break
          case 'nivel':
            await mantenedoresService.nivel.partialUpdate(id, datosAPI)
            break
          case 'estadoCivil':
            await mantenedoresService.estadoCivil.partialUpdate(id, datosAPI)
            break
          case 'rol':
            await mantenedoresService.rol.partialUpdate(id, datosAPI)
            break
          case 'conceptoContable':
            await mantenedoresService.conceptoContable.partialUpdate(id, datosAPI)
            break
          case 'proveedor':
            await mantenedoresService.proveedorPago.partialUpdate(id, datosAPI)
            break
          case 'tipoArchivo':
            await mantenedoresService.tipoArchivos.partialUpdate(id, datosAPI)
            break
        }
        // recargar removed from here; handled by caller to allow immediate UI close
      } catch (err) {
        error.value = 'ERROR AL ANULAR ELEMENTO: ' + (err.message || 'error desconocido')
      }
    }

    const habilitarElemento = async (tipo, elemento) => {
      try {
        const id = elemento?.id ?? elemento?.zon_id ?? elemento?.dis_id ?? elemento?.gru_id ?? elemento?.ram_id ?? elemento?.tcu_id ?? elemento?.car_id ?? elemento?.ali_id ?? elemento?.com_id ?? elemento?.pro_id ?? elemento?.reg_id ?? elemento?.niv_id ?? elemento?.esc_id ?? elemento?.rol_id ?? elemento?.coc_id ?? elemento?.tar_id
        if (!id) throw new Error('ID no disponible')

        const fieldMap = {
          zona: 'zon_vigente',
          distrito: 'dis_vigente',
          grupo: 'gru_vigente',
          rama: 'ram_vigente',
          tipoCurso: 'tcu_vigente',
          cargo: 'car_vigente',
          alimentacion: 'ali_vigente',
          comuna: 'com_vigente',
          provincia: 'pro_vigente',
          region: 'reg_vigente',
          nivel: 'niv_vigente',
          estadoCivil: 'esc_vigente',
          rol: 'rol_vigente',
          conceptoContable: 'coc_vigente',
          tipoArchivo: 'tar_vigente'
          ,proveedor: 'prv_vigente'
        }


        const fieldName = fieldMap[tipo] || 'vigente'
        const datosAPI = { [fieldName]: true }

        switch (tipo) {
          case 'zona':
            await mantenedoresService.zona.partialUpdate(id, datosAPI)
            break
          case 'distrito':
            await mantenedoresService.distrito.partialUpdate(id, datosAPI)
            break
          case 'grupo':
            await mantenedoresService.grupo.partialUpdate(id, datosAPI)
            break
          case 'tipoCurso':
            await mantenedoresService.tipoCursos.partialUpdate(id, datosAPI)
            break
          case 'cargo':
            await mantenedoresService.cargo.partialUpdate(id, datosAPI)
            break
          case 'alimentacion':
            await mantenedoresService.alimentacion.partialUpdate(id, datosAPI)
            break
          case 'comuna':
            await mantenedoresService.comuna.partialUpdate(id, datosAPI)
            break
          case 'provincia':
            await mantenedoresService.provincia.partialUpdate(id, datosAPI)
            break
          case 'region':
            await mantenedoresService.region.partialUpdate(id, datosAPI)
            break
          case 'nivel':
            await mantenedoresService.nivel.partialUpdate(id, datosAPI)
            break
          case 'estadoCivil':
            await mantenedoresService.estadoCivil.partialUpdate(id, datosAPI)
            break
          case 'rol':
            await mantenedoresService.rol.partialUpdate(id, datosAPI)
            break
          case 'conceptoContable':
            await mantenedoresService.conceptoContable.partialUpdate(id, datosAPI)
            break
          case 'tipoArchivo':
            await mantenedoresService.tipoArchivos.partialUpdate(id, datosAPI)
            break
          case 'proveedor':
            await mantenedoresService.proveedorPago.partialUpdate(id, datosAPI)
            break
        }
        // recargar removed from here; handled by caller to allow immediate UI close
      } catch (err) {
        error.value = 'ERROR AL HABILITAR ELEMENTO: ' + (err.message || 'error desconocido')
      }
    }

    // Aplica un cambio optimista en la colección reactiva correspondiente
    const applyOptimisticCambio = (tipo, elemento, vigente) => {
      try {
        const id = elemento?.id ?? elemento?.zon_id ?? elemento?.dis_id ?? elemento?.gru_id ?? elemento?.ram_id ?? elemento?.tcu_id ?? elemento?.car_id ?? elemento?.ali_id ?? elemento?.com_id ?? elemento?.pro_id ?? elemento?.reg_id ?? elemento?.niv_id ?? elemento?.esc_id ?? elemento?.rol_id ?? elemento?.coc_id ?? elemento?.tar_id
        if (!id) return
        switch (tipo) {
          case 'zona': {
            const idx = zonas.value.findIndex(z => z.id === id)
            if (idx !== -1) zonas.value[idx].vigente = !!vigente
            break
          }
          
          case 'distrito': {
            const idx = distritos.value.findIndex(d => d.id === id)
            if (idx !== -1) distritos.value[idx].vigente = !!vigente
            break
          }
          case 'grupo': {
            const idx = grupos.value.findIndex(g => g.id === id)
            if (idx !== -1) grupos.value[idx].vigente = !!vigente
            break
          }
          case 'alimentacion': {
            const idx = alimentacion.value.findIndex(a => a.id === id)
            if (idx !== -1) alimentacion.value[idx].vigente = !!vigente
            break
          }
          case 'comuna': {
            const idx = comunas.value.findIndex(c => c.id === id)
            if (idx !== -1) comunas.value[idx].vigente = !!vigente
            break
          }
          case 'provincia': {
            const idx = provincias.value.findIndex(p => p.id === id)
            if (idx !== -1) provincias.value[idx].vigente = !!vigente
            break
          }
          case 'region': {
            const idx = regiones.value.findIndex(r => r.id === id)
            if (idx !== -1) regiones.value[idx].vigente = !!vigente
            break
          }
          case 'nivel': {
            const idx = niveles.value.findIndex(n => n.id === id)
            if (idx !== -1) niveles.value[idx].vigente = !!vigente
            break
          }
          case 'estadoCivil': {
            const idx = estadosCiviles.value.findIndex(e => e.id === id)
            if (idx !== -1) estadosCiviles.value[idx].vigente = !!vigente
            break
          }
          case 'rol': {
            const idx = roles.value.findIndex(r => r.id === id)
            if (idx !== -1) roles.value[idx].vigente = !!vigente
            break
          }
          case 'conceptoContable': {
            const idx = conceptosContables.value.findIndex(c => c.id === id)
            if (idx !== -1) conceptosContables.value[idx].vigente = !!vigente
            break
          }
          case 'tipoArchivo': {
            const idx = tiposArchivo.value.findIndex(t => t.id === id)
            if (idx !== -1) tiposArchivo.value[idx].vigente = !!vigente
            break
          }
        }
      } catch (err) {
        console.error('applyOptimisticCambio error', err)
      }
    }

    // Recargar sólo la entidad afectada para reducir peticiones y latencia
    const recargarTipo = async (tipo) => {
      try {
        const getData = (resp) => {
          if (!resp) return []
          if (Array.isArray(resp)) return resp
          return resp.results || resp.data || resp.items || []
        }
        switch (tipo) {
          case 'zona': {
            const resp = await mantenedoresService.zona.list()
            const raw = getData(resp)
            zonas.value = (raw || []).map(z => ({ id: z.zon_id ?? z.ZON_ID ?? z.id, descripcion: (z.zon_descripcion ?? z.ZON_DESCRIPCION ?? z.descripcion ?? '').toString(), unilateral: !!(z.zon_unilateral ?? z.ZON_UNILATERAL ?? z.unilateral), vigente: !!(z.zon_vigente ?? z.ZON_VIGENTE ?? z.vigente) }))
            break
          }
          case 'distrito': {
            const resp = await mantenedoresService.distrito.list()
            const raw = getData(resp)
            distritos.value = (raw || []).map(d => ({ id: d.dis_id ?? d.DIS_ID ?? d.id, descripcion: (d.dis_descripcion ?? d.DIS_DESCRIPCION ?? d.descripcion ?? '').toString(), zona_id: d.zon_id ?? d.ZON_ID ?? null, vigente: !!(d.dis_vigente ?? d.DIS_VIGENTE ?? d.vigente) }))
            break
          }
          case 'grupo': {
            const resp = await mantenedoresService.grupo.list()
            const raw = getData(resp)
            grupos.value = (raw || []).map(g => ({ id: g.gru_id ?? g.GRU_ID ?? g.id, descripcion: (g.gru_descripcion ?? g.GRU_DESCRIPCION ?? g.descripcion ?? '').toString(), distrito_id: g.dis_id ?? g.DIS_ID ?? null, vigente: !!(g.gru_vigente ?? g.GRU_VIGENTE ?? g.vigente) }))
            break
          }
          case 'provincia': {
            const resp = await mantenedoresService.provincia.list()
            const raw = getData(resp)
            provincias.value = (raw || []).map(p => ({ id: p.pro_id ?? p.PRO_ID ?? p.id, descripcion: (p.pro_descripcion ?? p.PRO_DESCRIPCION ?? p.descripcion ?? '').toString(), region_id: p.reg_id ?? p.REG_ID ?? null, vigente: !!(p.pro_vigente ?? p.PRO_VIGENTE ?? p.vigente) }))
            break
          }
          case 'region': {
            const resp = await mantenedoresService.region.list()
            const raw = getData(resp)
            regiones.value = (raw || []).map(r => ({ id: r.reg_id ?? r.REG_ID ?? r.id, descripcion: (r.reg_descripcion ?? r.REG_DESCRIPCION ?? r.descripcion ?? '').toString(), vigente: !!(r.reg_vigente ?? r.REG_VIGENTE ?? r.vigente) }))
            break
          }
          case 'nivel': {
            const resp = await mantenedoresService.nivel.list()
            const raw = getData(resp)
            niveles.value = (raw || []).map(n => ({ id: n.niv_id ?? n.NIV_ID ?? n.id, descripcion: (n.niv_descripcion ?? n.NIV_DESCRIPCION ?? n.descripcion ?? '').toString(), orden: n.niv_orden ?? n.NIV_ORDEN ?? n.orden ?? 0, vigente: !!(n.niv_vigente ?? n.NIV_VIGENTE ?? n.vigente) }))
            break
          }
          case 'estadoCivil': {
            const resp = await mantenedoresService.estadoCivil.list()
            const raw = getData(resp)
            estadosCiviles.value = (raw || []).map(e => ({ id: e.esc_id ?? e.ESC_ID ?? e.id, descripcion: (e.esc_descripcion ?? e.ESC_DESCRIPCION ?? e.descripcion ?? '').toString(), vigente: !!(e.esc_vigente ?? e.ESC_VIGENTE ?? e.vigente) }))
            break
          }
          case 'rol': {
            const resp = await mantenedoresService.rol.list()
            const raw = getData(resp)
            roles.value = (raw || []).map(r => ({ id: r.rol_id ?? r.ROL_ID ?? r.id, descripcion: (r.rol_descripcion ?? r.ROL_DESCRIPCION ?? r.descripcion ?? '').toString(), tipo: r.rol_tipo ?? r.ROL_TIPO ?? r.tipo ?? '', vigente: !!(r.rol_vigente ?? r.ROL_VIGENTE ?? r.vigente) }))
            break
          }
          case 'conceptoContable': {
            const resp = await mantenedoresService.conceptoContable.list()
            const raw = getData(resp)
            conceptosContables.value = (raw || []).map(c => ({ id: c.coc_id ?? c.COC_ID ?? c.id, descripcion: (c.coc_descripcion ?? c.COC_DESCRIPCION ?? c.descripcion ?? '').toString(), vigente: !!(c.coc_vigente ?? c.COC_VIGENTE ?? c.vigente) }))
            break
          }
          case 'tipoArchivo': {
            const resp = await mantenedoresService.tipoArchivos.list()
            const raw = getData(resp)
            tiposArchivo.value = (raw || []).map(t => ({ id: t.tar_id ?? t.TAR_ID ?? t.id, descripcion: (t.tar_descripcion ?? t.TAR_DESCRIPCION ?? t.descripcion ?? '').toString(), extension: t.TAR_EXTENSION ?? t.extension ?? '', vigente: !!(t.tar_vigente ?? t.TAR_VIGENTE ?? t.vigente) }))
            break
          }
          default:
            // Si no conocemos el tipo, recargar todo como fallback
            await recargar()
        }
      } catch (err) {
        console.error('recargarTipo error:', err)
      }
    }

    const cargarDatosFormulario = (tipo, elemento) => {
      switch (tipo) {
        case 'zona':
          Object.assign(formZona, elemento)
          break
        case 'distrito':
          Object.assign(formDistrito, elemento)
          break
        case 'grupo':
          Object.assign(formGrupo, elemento)
          break
        case 'provincia':
          Object.assign(formProvincia, elemento)
          break
        case 'region':
          Object.assign(formRegion, elemento)
          break
        case 'nivel':
          Object.assign(formNivel, elemento)
          break
        case 'estadoCivil':
          Object.assign(formEstadoCivil, elemento)
          break
        case 'rol':
          Object.assign(formRol, { id: elemento.id, descripcion: elemento.descripcion, tipo: elemento.tipo, vigente: elemento.vigente })
          break
        case 'conceptoContable':
          Object.assign(formConceptoContable, elemento)
          break
        case 'tipoArchivo':
          Object.assign(formTipoArchivo, elemento)
          break
      }
    }

    const limpiarFormularios = () => {
      Object.assign(formZona, {
        id: null,
        descripcion: '',
        unilateral: false,
        vigente: true
      })
      Object.assign(formDistrito, {
        id: null,
        descripcion: '',
        zona_id: null,
        vigente: true
      })
      Object.assign(formGrupo, {
        id: null,
        descripcion: '',
        distrito_id: null,
        vigente: true
      })
      Object.assign(formProvincia, { id: null, descripcion: '', region_id: null, vigente: true })
      Object.assign(formRegion, { id: null, descripcion: '', vigente: true })
      Object.assign(formNivel, { id: null, descripcion: '', orden: 1, vigente: true })
      Object.assign(formEstadoCivil, { id: null, descripcion: '', vigente: true })
      Object.assign(formRol, { id: null, descripcion: '', tipo: 1, vigente: true })
      Object.assign(formConceptoContable, { id: null, descripcion: '', tipo: '', vigente: true })
      Object.assign(formTipoArchivo, { id: null, descripcion: '', extension: '', vigente: true })
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      editando.value = false
      tipoElemento.value = ''
      elementoSeleccionado.value = null
      limpiarFormularios()
    }

    // Métodos de guardado

    // Métodos CRUD para zonas, distritos, grupos, ramas



    // Guardar otros mantenedores
    const guardarTipoCurso = async () => {
      saving.value = true
      try {
        const payload = { tcu_descripcion: formTipoCurso.descripcion, tcu_tipo: formTipoCurso.tipo, tcu_cant_participante: formTipoCurso.cant_participante, tcu_vigente: !!formTipoCurso.vigente }
        if (editando.value) {
          const id = formTipoCurso.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de tipo de curso no disponible para edición')
          await mantenedoresService.tipoCursos.partialUpdate(id, payload)
          const idx = tiposCurso.value.findIndex(t => t.id === id)
          if (idx !== -1) Object.assign(tiposCurso.value[idx], { descripcion: formTipoCurso.descripcion, tipo: formTipoCurso.tipo, cant_participante: formTipoCurso.cant_participante, vigente: !!formTipoCurso.vigente })
        } else {
          await mantenedoresService.tipoCursos.create(payload)
        }
        cerrarModal()
        recargarTipo('tipoCurso').catch(e => console.error('Error recargando tiposCurso', e))
      } catch (err) { console.error('Error guardarTipoCurso', err); error.value = 'No se pudo guardar el tipo de curso: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }





    const guardarProvincia = async () => {
      saving.value = true
      try { const payload = { pro_descripcion: formProvincia.descripcion, reg_id: formProvincia.region_id, pro_vigente: !!formProvincia.vigente };
        if (editando.value) {
          const id = formProvincia.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de provincia no disponible para edición')
          await mantenedoresService.provincia.partialUpdate(id, payload)
          const idx = provincias.value.findIndex(p => p.id === id)
          if (idx !== -1) Object.assign(provincias.value[idx], { descripcion: formProvincia.descripcion, region_id: formProvincia.region_id, vigente: !!formProvincia.vigente })
        } else { await mantenedoresService.provincia.create(payload) }
        cerrarModal()
        recargarTipo('provincia').catch(e => console.error('Error recargando provincias', e))
      } catch (err) { console.error('Error guardarProvincia', err); error.value = 'No se pudo guardar la provincia: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarRegion = async () => {
      saving.value = true
      try { const payload = { reg_descripcion: formRegion.descripcion, reg_vigente: !!formRegion.vigente };
        if (editando.value) {
          const id = formRegion.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de región no disponible para edición')
          await mantenedoresService.region.partialUpdate(id, payload)
          const idx = regiones.value.findIndex(r => r.id === id)
          if (idx !== -1) Object.assign(regiones.value[idx], { descripcion: formRegion.descripcion, vigente: !!formRegion.vigente })
        } else { await mantenedoresService.region.create(payload) }
        cerrarModal()
        recargarTipo('region').catch(e => console.error('Error recargando regiones', e))
      } catch (err) { console.error('Error guardarRegion', err); error.value = 'No se pudo guardar la región: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarNivel = async () => {
      saving.value = true
      try { const payload = { niv_descripcion: formNivel.descripcion, niv_orden: formNivel.orden, niv_vigente: !!formNivel.vigente };
        if (editando.value) {
          const id = formNivel.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de nivel no disponible para edición')
          await mantenedoresService.nivel.partialUpdate(id, payload)
          const idx = niveles.value.findIndex(n => n.id === id)
          if (idx !== -1) Object.assign(niveles.value[idx], { descripcion: formNivel.descripcion, orden: formNivel.orden, vigente: !!formNivel.vigente })
        } else { await mantenedoresService.nivel.create(payload) }
        cerrarModal()
        recargarTipo('nivel').catch(e => console.error('Error recargando niveles', e))
      } catch (err) { console.error('Error guardarNivel', err); error.value = 'No se pudo guardar el nivel: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarEstadoCivil = async () => {
      saving.value = true
      try { const payload = { esc_descripcion: formEstadoCivil.descripcion, esc_vigente: !!formEstadoCivil.vigente };
        if (editando.value) {
          const id = formEstadoCivil.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de estado civil no disponible para edición')
          await mantenedoresService.estadoCivil.partialUpdate(id, payload)
          const idx = estadosCiviles.value.findIndex(e => e.id === id)
          if (idx !== -1) Object.assign(estadosCiviles.value[idx], { descripcion: formEstadoCivil.descripcion, vigente: !!formEstadoCivil.vigente })
        } else { await mantenedoresService.estadoCivil.create(payload) }
        cerrarModal()
        recargarTipo('estadoCivil').catch(e => console.error('Error recargando estadosCiviles', e))
      } catch (err) { console.error('Error guardarEstadoCivil', err); error.value = 'No se pudo guardar el estado civil: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarRol = async () => {
      saving.value = true
      try { const payload = { rol_descripcion: formRol.descripcion, rol_tipo: formRol.tipo, rol_vigente: !!formRol.vigente };
        if (editando.value) {
          const id = formRol.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de rol no disponible para edición')
          await mantenedoresService.rol.partialUpdate(id, payload)
          const idx = roles.value.findIndex(r => r.id === id)
          if (idx !== -1) Object.assign(roles.value[idx], { descripcion: formRol.descripcion, tipo: formRol.tipo, vigente: !!formRol.vigente })
        } else { await mantenedoresService.rol.create(payload) }
        cerrarModal()
        recargarTipo('rol').catch(e => console.error('Error recargando roles', e))
      } catch (err) { console.error('Error guardarRol', err); error.value = 'No se pudo guardar el rol: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarConceptoContable = async () => {
      saving.value = true
      try { const payload = { coc_descripcion: formConceptoContable.descripcion, coc_vigente: !!formConceptoContable.vigente };
        if (editando.value) {
          const id = formConceptoContable.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de concepto contable no disponible para edición')
          await mantenedoresService.conceptoContable.partialUpdate(id, payload)
          const idx = conceptosContables.value.findIndex(c => c.id === id)
          if (idx !== -1) Object.assign(conceptosContables.value[idx], { descripcion: formConceptoContable.descripcion, vigente: !!formConceptoContable.vigente })
        } else { await mantenedoresService.conceptoContable.create(payload) }
        cerrarModal()
        recargarTipo('conceptoContable').catch(e => console.error('Error recargando conceptosContables', e))
      } catch (err) { console.error('Error guardarConceptoContable', err); error.value = 'No se pudo guardar el concepto contable: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }

    const guardarTipoArchivo = async () => {
      saving.value = true
      try { const payload = { tar_descripcion: formTipoArchivo.descripcion, tar_vigente: !!formTipoArchivo.vigente };
        if (editando.value) {
          const id = formTipoArchivo.id ?? elementoSeleccionado.value?.id
          if (!id) throw new Error('ID de tipo de archivo no disponible para edición')
          await mantenedoresService.tipoArchivos.partialUpdate(id, payload)
          const idx = tiposArchivo.value.findIndex(t => t.id === id)
          if (idx !== -1) Object.assign(tiposArchivo.value[idx], { descripcion: formTipoArchivo.descripcion, vigente: !!formTipoArchivo.vigente })
        } else { await mantenedoresService.tipoArchivos.create(payload) }
        cerrarModal()
        recargarTipo('tipoArchivo').catch(e => console.error('Error recargando tiposArchivo', e))
      } catch (err) { console.error('Error guardarTipoArchivo', err); error.value = 'No se pudo guardar el tipo de archivo: ' + (err.message || 'error desconocido') } finally { saving.value = false }
    }



    return {
      activeTab,
      modalActivo,
      editando,
      tipoElemento,
      elementoSeleccionado,
      isDropdownOpen,
      dropdownContainer,
      cargando,
      error,
      confirmModal,
      tabs,
      provincias,
      regiones,
      niveles,
      estadosCiviles,
      roles,
      conceptosContables,
      tiposArchivo,
      formProvincia,
      formRegion,
      formNivel,
      formEstadoCivil,
      formRol,
      formConceptoContable,
      formTipoArchivo,
      getProvinciaNombre,
      getRegionNombre,
      getTipoNombre,
      getRelacionNombre,
      getRelacionValor,
      getSelectedTabInfo,
      toggleDropdown,
      selectTab,
      abrirModalCrear,
      verElemento,
      editarElemento,
      abrirConfirmacion,
      cancelarConfirmacion,
      confirmarConfirmacion,
      confirmLoading,
      saving,
      anularElemento,
      habilitarElemento,
      cerrarModal,
      guardarProvincia,
      guardarRegion,
      guardarNivel,
      guardarEstadoCivil,
      guardarRol,
      guardarConceptoContable,
      guardarTipoArchivo,
      recargar,
      handleMessage: (msg) => {
        if (msg.type === 'error') error.value = msg.text
        // Si hay sistema de notificaciones globales, usarlo aquí para success
      },
      handleConfirmAction: (conf) => {
        confirmModal.titulo = conf.titulo
        confirmModal.mensaje = conf.mensaje
        confirmModal.visible = true
        // Sobreescribimos la acción de confirmar para ejecutar la callback del componente hijo
        // Esto es un hack rápido, idealmente el componente hijo maneja su propio modal o pasamos la función de otra forma.
        // Pero dado que confirmModal es global en este archivo...
        // Mejor opción: que el hijo maneje su confirmación o emitir evento de confirmación aceptada.
        // Vamos a usar una variable temporal para guardar la acción del hijo.
        pendingConfirmAction.value = conf.accion
      }
    }
  }
} 
</script>

<style scoped>
.mantenedores-scouts {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(60,60,60,0.08);
  padding: 24px;
  margin-bottom: 24px;
  color: #111;
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
  width: 100%;
  height: 100%;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  min-height: calc(100vh - var(--navbar-height, 64px));
  margin-top: 0px;
  border-radius: 6px;
  overflow: hidden;
}

/* Error Alert */
.error-alert {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 15px 20px;
  margin: 10px 20px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-alert p {
  margin: 0;
}

.error-alert button {
  background: none;
  border: none;
  color: #721c24;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Indicador de carga global, centrado con fondo difuminado */
.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(18, 25, 38, 0.35);
  backdrop-filter: blur(3px);
}
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 24px 28px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 28px rgba(0,0,0,0.18);
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #dde3f0;
  border-top-color: #3949ab;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Selector de Mantenedores Fijo - CORREGIDO */
.mantenedor-selector-fixed {
  background: #1a237e;
  color: white;
  padding: 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  width: 100%;
}

.selector-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  max-width: 100%;
  margin: 0 auto;
}

.selector-header {
  flex-shrink: 0;
}

.selector-header h2 {
  margin: 0;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
}

/* Nuevos estilos para el dropdown personalizado - MEJORADO */
.selector-dropdown {
  position: relative;
  max-width: 400px;
  width: 100%;
  margin-left: 20px;
}

.mantenedor-dropdown-toggle {
  width: 100%;
  padding: 12px 45px 12px 16px;
  border: 2px solid #3949ab;
  border-radius: 8px;
  background: white;
  color: #333;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 500;
}

.mantenedor-dropdown-toggle:hover {
  border-color: #ff6b35;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.2);
}

.mantenedor-dropdown-toggle.active {
  border-color: #ff6b35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.selected-option {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-weight: 500;
}

.dropdown-icon {
  color: #3949ab;
  transition: transform 0.3s ease;
  font-size: 0.9rem;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #3949ab;
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1001;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item.active {
  background: #e3f2fd;
  color: #3949ab;
  font-weight: 600;
}

.dropdown-item-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.dropdown-item-text {
  color: #333;
  font-weight: 500;
  flex: 1;
}

.dropdown-item.active .dropdown-item-text {
  color: #3949ab;
  font-weight: 600;
}

.dropdown-item:hover .dropdown-item-text {
  color: #1a237e;
}

/* Main Content Expandido */
.main-content-expanded {
  flex: 1;
  padding: 0;
  min-height: calc(100vh - var(--navbar-height, 64px) - 80px);
  height: calc(100vh - var(--navbar-height, 64px));
  overflow: hidden; /* Evita scroll de página, usa scroll interno en tablas */
  width: 100%;
  margin: 0;
}

.header-expanded {
  background: #1a237e;
  color: white;
  padding: 30px 20px;
  margin: 0;
  width: 100%;
}

.header-expanded h1 {
  font-size: 1.8rem;
  margin-bottom: 8px;
  margin-top: 0;
}

.header-expanded p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.mantenedor-section-expanded {
  padding: 30px 20px;
  animation: fadeIn 0.5s ease;
  width: 100%;
  margin: 0;
  box-sizing: border-box;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 3px solid #3949ab;
  width: 100%;
  box-sizing: border-box;
}

.mantenedor-header h2 {
  color: #1a237e;
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.btn-primary {
  background: linear-gradient(180deg,#2b6cb0,#154c8c);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 14px;
  min-height: 44px;
  box-shadow: 0 6px 18px rgba(33,78,156,0.12);
}

.btn-primary:hover {
  background: linear-gradient(180deg,#1e40af,#1e3a8a);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(57, 73, 171, 0.3);
}

.search-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: flex-end;
  width: 100%;
  box-sizing: border-box;
}

/* Compact variant for search bars (used in distritos) to reduce vertical space */
.search-bar--compact {
  gap: 10px;
  margin-bottom: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #3949ab;
  box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
}

.select-filter {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 200px;
  box-sizing: border-box;
}

.table-container-expanded {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: auto; /* Permite scroll dentro de la tabla */
  width: 100%;
  box-sizing: border-box;
  max-height: calc(100vh - 280px); /* Ajusta según encabezado y barras */
  padding-bottom: 16px; /* Evita que el último elemento quede cortado */
  scroll-padding-bottom: 24px; /* Asegura espacio al hacer scroll hasta el final */
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
  box-sizing: border-box;
}

.data-table-expanded thead {
  background: #f8f9fa;
}

.data-table-expanded th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #1a237e;
  border-bottom: 2px solid #e1e5e9;
}

.data-table-expanded td {
  padding: 14px 12px;
  border-bottom: 1px solid #e1e5e9;
}

.data-table-expanded tr:hover {
  background: #f8f9fa;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-height: 32px;
}

.btn-view {
  background: #e3f2fd;
  color: #1565c0;
}

.btn-edit {
  background: #fff3cd;
  color: #856404;
}

.btn-anular {
  background: #f8d7da;
  color: #721c24;
}

.btn-habilitar {
  background: #d4edda;
  color: #155724;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 25px 30px 20px;
  border-bottom: 2px solid #3949ab;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #1a237e;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #1a237e;
}

.modal-body {
  padding: 25px 30px;
}

/* View Container Styles */
.view-container {
  margin-bottom: 20px;
}

.view-group {
  margin-bottom: 20px;
}

.view-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #39424b;
}

.view-value {
  padding: 12px 16px;
  background: #f8f9fa;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 14px;
  min-height: 44px;
}

.btn-secondary:hover {
  background: #5a6268;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #39424b;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3949ab;
  box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-checkbox input {
  width: 18px;
  height: 18px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 768px) {
  .selector-container {
    flex-direction: column;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .selector-dropdown {
    margin-left: 0;
    max-width: 100%;
  }
  
  .mantenedor-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .search-input, .select-filter {
    min-width: 100%;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .table-container-expanded {
    overflow-x: auto;
  }
  
  .data-table-expanded {
    min-width: 600px;
  }
  
  .dropdown-menu {
    max-height: 300px;
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Estilos adaptados de message.txt */
.btn-standard {
  min-width: 160px !important;
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

.btn-standard:hover {
  filter: brightness(0.95) !important;
  box-shadow: 0 4px 16px rgba(40,92,168,0.13) !important;
  transform: translateY(-1px) !important;
}

.estado { 
  padding: 6px 12px; 
  border-radius: 12px; 
  font-size: 12px; 
  white-space: nowrap;
  font-weight: 600;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.estado.activo { 
  background: #d1fae5; 
  color: #065f46;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.estado.inactivo { 
  background: #fee2e2; 
  color: #991b1b;
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.estado.vigente { background:#d1fae5; color:#065f46 }
.estado.no-vigente { background:#fbbf24; color:#1f2937 }
.estado.anulado { background:#e5e7eb; color:#374151; text-decoration: line-through; }

/* Mejoras responsivas adicionales */
@media (max-width: 480px) {
  .mantenedores-scouts {
    padding: 16px;
  }
  
  .mantenedor-section-expanded {
    padding: 20px 16px;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    justify-content: center;
  }
  
  .actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-action {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 1024px) {
  .mantenedores-scouts {
    margin: 12px;
    width: calc(100% - 24px);
  }
}
</style>