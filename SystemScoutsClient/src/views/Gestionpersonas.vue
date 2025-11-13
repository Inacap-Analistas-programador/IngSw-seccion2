<template>
  <div class="gestion-personas">
  <!-- Vista: la NavBar se renderiza globalmente en App.vue, no incluirla aquí -->

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <div class="filtros-left">
        <InputBase v-model="searchQuery" placeholder="Buscar por nombre, RUT, email..." @keydown.enter.prevent="filtrar" />
        <BaseSelect v-model="selectedRole" :options="roleOptions" placeholder="Todos los roles" />
        <BaseSelect v-model="selectedCourse" :options="courseOptions" placeholder="Todos los grupos" />
        <BaseSelect v-model="selectedRama" :options="ramaOptions" placeholder="Todas las ramas" />
      </div>
      <div class="filtros-right">
        <BaseButton class="btn-search" variant="primary" @click="filtrar">🔎 Buscar</BaseButton>
        <BaseButton class="btn-add" variant="success" @click="abrirModalCrear">➕ Nueva Persona</BaseButton>
        <BaseButton class="btn-import" variant="info" @click="abrirModalImportar">📥 Importar Excel</BaseButton>
        <BaseButton class="btn-export" variant="secondary" @click="exportarExcel">📊 Exportar</BaseButton>
      </div>
    </div>

    <!-- Indicadores de carga y error -->
    <div v-if="cargandoPersonas" class="estado-carga">
      <p>🔄 Cargando personas...</p>
    </div>
    
    <div v-if="errorCarga" class="mensaje-error">
      <p>❌ {{ errorCarga }}</p>
      <BaseButton @click="cargarPersonas" variant="primary">🔄 Reintentar</BaseButton>
    </div>

    <!-- Mensaje de filtro activo -->
    <div v-if="filtroAplicado && filtrosActivos.length > 0" class="filtro-activo" role="status" aria-live="polite">
      {{ filtroMensaje }}
    </div>

    <!-- Contenedor principal: tabla + detallet (scroll interno) -->
    <div class="main-area">
      <!-- Tabla de participantes (se muestra solo tras filtrar) -->
      <div v-if="filtroAplicado" class="table-wrapper">
      <table>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>RUT</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Rama</th>
          <th>Grupo</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in personasFiltradas" :key="p.PER_RUN" :class="{ 'persona-anulada': !p.PER_VIGENTE }">
          <td data-label="Nombre">{{ `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim() }}</td>
          <td data-label="RUT">{{ p.PER_RUN }}-{{ p.PER_DV }}</td>
          <td data-label="Email">{{ p.PER_MAIL }}</td>
          <td data-label="Rol">{{ p.PER_ROL || 'Sin rol' }}</td>
          <td data-label="Rama">{{ p.PER_RAMA || 'Sin rama' }}</td>
          <td data-label="Grupo">{{ p.PER_GRUPO || 'Sin grupo' }}</td>
          <td data-label="Estado">
            <span
              :class="['estado', p.PER_VIGENTE ? 'activo' : 'inactivo']"
            >
              {{ p.PER_VIGENTE ? 'Activo' : 'Inactivo' }}
            </span>
          </td>
          <td>
            <div class="acciones-buttons">
              <BaseButton class="btn-ver btn-view" variant="info" @click="abrirModalVer(p)">Ver</BaseButton>
              <BaseButton 
                v-if="esAdministrador" 
                class="btn-editar btn-edit" 
                variant="secondary" 
                @click="abrirModalEditar(p)"
              >
                Editar
              </BaseButton>
              <BaseButton 
                v-if="esAdministrador" 
                class="btn-anular btn-cancel" 
                variant="warning" 
                @click="anularPersona(p)"
              >
                Anular
              </BaseButton>
            </div>
          </td>
        </tr>
        <tr v-if="personasFiltradas.length === 0" class="placeholder-row">
          <td data-label="Nombre" colspan="8">No hay participantes para mostrar</td>
        </tr>
      </tbody>
      </table>
    </div>

      <!-- Si aún no se filtra, mostrar mensaje instructivo -->
      <div v-else class="no-filtro" style="padding:32px; text-align:center; color:#666;">
        Aplica filtros y presiona "Buscar" para ver la lista de personas.
      </div>

  <!-- Ver/Editar persona -->
  <BaseModal v-model="editModalVisible" @close="cancelarEdicion" class="persona-modal">
        <template #default>
          <div class="modal-edit">
                <header class="modal-header">
                  <h3>{{ modoSoloLectura ? 'Ver' : 'Editar' }} - {{ `${personaEditada?.PER_NOMBRES || ''} ${personaEditada?.PER_APELPTA || ''}`.trim() }}</h3>
                  <div class="header-actions" v-if="!modoSoloLectura">
                    <BaseButton 
                      class="btn-save" 
                      type="button" 
                      variant="primary" 
                      @click="guardarEdicion"
                      :disabled="guardandoPersona"
                    >
                      {{ guardandoPersona ? '⏳ Guardando...' : '💾 Guardar' }}
                    </BaseButton>
                  </div>
                </header>

                <div class="modal-tabs">
                  <button :class="{active: modalTab === 'info'}" @click="modalTab='info'">Info</button>
                  <button :class="{active: modalTab === 'hist'}" @click="modalTab='hist'">Historial</button>
                </div>

                <form v-if="modalTab==='info'" @submit.prevent="" class="modal-form">
                  <!-- Sección de Foto de Perfil -->
                  <div class="foto-perfil-section">
                    <div class="foto-container">
                      <img 
                        v-if="personaEditada.foto" 
                        :src="personaEditada.foto" 
                        :alt="`Foto de ${personaEditada.PER_NOMBRES}`"
                        class="foto-perfil"
                        @error="handleImageError"
                      />
                      <div v-else class="foto-placeholder">
                        <span class="foto-icon">👤</span>
                        <span class="foto-text">Sin foto</span>
                      </div>
                      <div v-if="!modoSoloLectura" class="foto-actions">
                        <input 
                          ref="fotoInput"
                          type="file" 
                          accept="image/*" 
                          @change="handleFileUpload"
                          style="display: none"
                        />
                        <button 
                          type="button" 
                          @click="$refs.fotoInput?.click()" 
                          class="btn-foto-upload"
                        >
                          📷 {{ personaEditada.foto ? 'Cambiar' : 'Subir' }} Foto
                        </button>
                        <button 
                          v-if="personaEditada.foto" 
                          type="button" 
                          @click="removePhoto" 
                          class="btn-foto-remove"
                        >
                          🗑️ Eliminar
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div class="row">
                    <label>Nombre</label>
                    <input v-model="personaEditada.PER_NOMBRES" :readonly="modoSoloLectura" required />
                  </div>
                  <div class="row">
                    <label>Apellido Paterno</label>
                    <input v-model="personaEditada.PER_APELPTA" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Apellido Materno</label>
                    <input v-model="personaEditada.PER_APELMAT" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>RUT</label>
                    <div class="rut-container">
                      <input v-model="personaEditada.PER_RUN" :readonly="modoSoloLectura" />
                      <span class="rut-separator">-</span>
                      <input v-model="personaEditada.PER_DV" :readonly="modoSoloLectura" class="rut-dv" maxlength="1" />
                    </div>
                  </div>
                  <div class="row">
                    <label>Email</label>
                    <input v-model="personaEditada.PER_MAIL" :readonly="modoSoloLectura" type="email" />
                  </div>
                  <div class="row">
                    <label>Teléfono</label>
                    <input v-model="personaEditada.PER_FONO" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Profesión</label>
                    <input v-model="personaEditada.PER_PROFESION" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Fecha Nac.</label>
                    <input v-model="personaEditada.PER_FECHA_NAC" :readonly="modoSoloLectura" type="date" />
                  </div>
                  <div class="row">
                    <label>Dirección</label>
                    <input v-model="personaEditada.PER_DIRECCION" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Contacto Emerg.</label>
                    <input v-model="personaEditada.PER_CONTACTO_EMERGENCIA" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Tel. Emerg.</label>
                    <input v-model="personaEditada.PER_TELEFONO_EMERGENCIA" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Alergias</label>
                    <input v-model="personaEditada.PER_ALERGIAS" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Limitación</label>
                    <input v-model="personaEditada.PER_LIMITACION" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Apodo</label>
                    <input v-model="personaEditada.PER_APODO" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Religión</label>
                    <input v-model="personaEditada.PER_RELIGION" :readonly="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Tiempo NNAJ</label>
                    <input v-model="personaEditada.PER_TIEMPO_NNAJ" :readonly="modoSoloLectura" type="number" />
                  </div>
                  <div class="row">
                    <label>Tiempo Adulto</label>
                    <input v-model="personaEditada.PER_TIEMPO_ADULTO" :readonly="modoSoloLectura" type="number" />
                  </div>
                  <div class="row">
                    <label>Vigente</label>
                    <select v-model="personaEditada.PER_VIGENTE" :disabled="modoSoloLectura">
                      <option :value="true">Si</option>
                      <option :value="false">No</option>
                    </select>
                  </div>
                  <div class="row">
                    <label>Rol</label>
                    <BaseSelect v-model="personaEditada.PER_ROL" :options="roleOptions" :disabled="modoSoloLectura" />
                  </div>
                  <div class="row">
                    <label>Rama</label>
                    <BaseSelect v-model="personaEditada.PER_RAMA" :options="ramaOptions" :disabled="modoSoloLectura" />
                  </div>
                </form>

                <div v-else class="historial-panel" :class="{ 'historial-anulado': personaEditada.estado === 'Anulado' }">
                  <div class="hist-list">
                    <div v-if="(personaEditada.historial || []).length === 0">No hay participaciones previas.</div>
                    <ul>
                      <li v-for="(h, idx) in (personaEditada.historial || [])" :key="idx" 
                          :class="['historial-item', { 'historial-item-anulado': personaEditada.estado === 'Anulado' }]">
                        <div class="historial-content" :class="{ 'historial-content-anulado': personaEditada.estado === 'Anulado' }">
                          <div class="historial-main" :class="{ 'historial-main-anulado': personaEditada.estado === 'Anulado' }">
                            <strong>{{ h.fecha }}</strong>: {{ h.descripcion }}
                          </div>
                          <div v-if="h.curso" class="historial-curso">
                            <span class="curso-badge" :class="{ 'curso-badge-anulado': personaEditada.estado === 'Anulado' }">{{ getCursoLabel(h.curso) }}</span>
                            <span :class="['aprobacion-badge', h.aprobado ? 'aprobado' : 'no-aprobado', { 'aprobacion-badge-anulado': personaEditada.estado === 'Anulado' }]">
                              {{ h.aprobado ? '✅ Aprobado' : '❌ No Aprobado' }}
                            </span>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
        </template>
      </BaseModal>

      <!-- Modal de Confirmación -->
      <BaseModal v-model="confirmModalVisible" title="Confirmar Cambios">
        <template #default>
          <div class="confirm-content">
            <div class="confirm-icon">⚠️</div>
            <p>{{ mensajeConfirmacion }}</p>
            <div class="confirm-actions">
              <BaseButton @click="cancelarConfirmacion" variant="secondary" class="btn-modal-cancel">
                ❌ Cancelar
              </BaseButton>
              <BaseButton @click="confirmarGuardado" variant="primary" class="btn-modal-confirm">
                ✅ Confirmar
              </BaseButton>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Confirmación para Anular -->
      <BaseModal v-model="confirmModalAnularVisible" title="Confirmar Anulación">
        <template #default>
          <div class="confirm-content">
            <div class="confirm-icon">⚠️</div>
            <p>¿Estás seguro de que deseas anular a <strong>{{ personaAAnular?.nombre }}</strong>?</p>
            <p class="confirm-warning">Esta acción marcará a la persona en gris y cambiará su estado.</p>
            <div class="confirm-actions">
              <BaseButton @click="cancelarAnulacion" variant="secondary" class="btn-modal-cancel">
                ❌ Cancelar
              </BaseButton>
              <BaseButton @click="confirmarAnulacion" variant="warning" class="btn-modal-anular">
                ⚠️ Anular
              </BaseButton>
            </div>
          </div>
        </template>
      </BaseModal>
      
      <!-- Modal de Creación de Persona -->
      <BaseModal v-model="crearModalVisible" title="Nueva Persona" @close="cerrarModalCrear" class="persona-modal">
        <template #default>
          <div class="modal-crear">
            <form @submit.prevent="guardarPersonaNueva" class="modal-form">
              <div class="row">
                <label>Nombres *</label>
                <InputBase 
                  v-model="personaNueva.PER_NOMBRES" 
                  placeholder="Ej: Juan Carlos" 
                  :disabled="guardandoPersona"
                  required
                />
              </div>
              
              <div class="row">
                <label>Apellido Paterno *</label>
                <InputBase 
                  v-model="personaNueva.PER_APELPTA" 
                  placeholder="Ej: González" 
                  :disabled="guardandoPersona"
                  required
                />
              </div>
              
              <div class="row">
                <label>Apellido Materno</label>
                <InputBase 
                  v-model="personaNueva.PER_APELMAT" 
                  placeholder="Ej: Pérez" 
                  :disabled="guardandoPersona"
                />
              </div>
              
              <div class="row">
                <label>RUT *</label>
                <div class="rut-container">
                  <InputBase 
                    v-model="personaNueva.PER_RUN" 
                    placeholder="12345678" 
                    :disabled="guardandoPersona"
                    required
                  />
                  <span class="rut-separator">-</span>
                  <InputBase 
                    v-model="personaNueva.PER_DV" 
                    placeholder="9" 
                    maxlength="1"
                    class="rut-dv"
                    :disabled="guardandoPersona"
                    required
                  />
                </div>
              </div>
              
              <div class="row">
                <label>Email *</label>
                <InputBase 
                  v-model="personaNueva.PER_MAIL" 
                  type="email"
                  placeholder="juan.gonzalez@email.com" 
                  :disabled="guardandoPersona"
                  required
                />
              </div>

              <div class="row">
                <label>Teléfono</label>
                <InputBase 
                  v-model="personaNueva.PER_FONO" 
                  placeholder="+56912345678" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Tipo de Teléfono</label>
                <BaseSelect 
                  v-model="personaNueva.PER_TIPO_FONO" 
                  :options="[
                    { value: 1, label: 'Fono Fijo' },
                    { value: 2, label: 'Celular' },
                    { value: 3, label: 'Celular/WhatsApp' },
                    { value: 4, label: 'WhatsApp' }
                  ]"
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Profesión</label>
                <InputBase 
                  v-model="personaNueva.PER_PROFESION" 
                  placeholder="Ej: Ingeniero" 
                  :disabled="guardandoPersona"
                />
              </div>
              
              <div class="row">
                <label>Fecha de Nacimiento *</label>
                <InputBase 
                  v-model="personaNueva.PER_FECHA_NAC" 
                  type="date"
                  :disabled="guardandoPersona"
                  required
                />
              </div>
              
              <div class="row">
                <label>Dirección</label>
                <InputBase 
                  v-model="personaNueva.PER_DIRECCION" 
                  placeholder="Calle Los Pinos #123" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Contacto Emergencia</label>
                <InputBase 
                  v-model="personaNueva.PER_CONTACTO_EMERGENCIA" 
                  placeholder="María González" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Tel. Emergencia</label>
                <InputBase 
                  v-model="personaNueva.PER_TELEFONO_EMERGENCIA" 
                  placeholder="+56987654321" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Alergias</label>
                <InputBase 
                  v-model="personaNueva.PER_ALERGIAS" 
                  placeholder="Ninguna conocida" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Limitación</label>
                <InputBase 
                  v-model="personaNueva.PER_LIMITACION" 
                  placeholder="Ninguna" 
                  :disabled="guardandoPersona"
                />
              </div>
              
              <div class="row">
                <label>Apodo</label>
                <InputBase 
                  v-model="personaNueva.PER_APODO" 
                  placeholder="Ej: Juanito" 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Religión</label>
                <InputBase 
                  v-model="personaNueva.PER_RELIGION" 
                  placeholder="Católica, Evangélica, etc." 
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Tiempo NNAJ</label>
                <InputBase 
                  v-model="personaNueva.PER_TIEMPO_NNAJ" 
                  placeholder="0" 
                  type="number"
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Tiempo Adulto</label>
                <InputBase 
                  v-model="personaNueva.PER_TIEMPO_ADULTO" 
                  placeholder="0" 
                  type="number"
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Vigente</label>
                <BaseSelect 
                  v-model="personaNueva.PER_VIGENTE" 
                  :options="[
                    { value: true, label: 'Sí' },
                    { value: false, label: 'No' }
                  ]"
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Rol</label>
                <BaseSelect 
                  v-model="personaNueva.PER_ROL" 
                  :options="roleOptions"
                  :disabled="guardandoPersona"
                />
              </div>

              <div class="row">
                <label>Rama</label>
                <BaseSelect 
                  v-model="personaNueva.PER_RAMA" 
                  :options="ramaOptions"
                  :disabled="guardandoPersona"
                />
              </div>
              
              <div class="form-actions">
                <BaseButton 
                  type="button" 
                  variant="secondary" 
                  @click="cerrarModalCrear"
                  :disabled="guardandoPersona"
                >
                  Cancelar
                </BaseButton>
                <BaseButton 
                  type="submit" 
                  variant="primary"
                  :disabled="guardandoPersona"
                >
                  {{ guardandoPersona ? '⏳ Guardando...' : '💾 Guardar Persona' }}
                </BaseButton>
              </div>
            </form>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Importar Excel -->
      <BaseModal v-model="importarModalVisible" title="Importar Personas desde Excel" @close="cerrarModalImportar" class="persona-modal">
        <template #default>
          <div class="modal-importar">
            <div class="import-content">
              
              <!-- Instrucciones -->
              <div class="import-instructions">
                <h4>📋 Instrucciones:</h4>
                <ul>
                  <li>El archivo debe ser formato Excel (.xlsx o .xls)</li>
                  <li>La primera fila debe contener los encabezados</li>
                  <li>Columnas requeridas: <strong>PER_NOMBRES, PER_APELPTA, PER_RUN, PER_DV, PER_MAIL</strong></li>
                  <li>Columnas opcionales: PER_APELMAT, PER_FECHA_NAC, PER_DIRECCION, PER_FONO, etc.</li>
                </ul>
              </div>

              <!-- Selector de archivo -->
              <div class="file-selector">
                <input 
                  ref="excelInput"
                  type="file" 
                  accept=".xlsx,.xls"
                  @change="handleFileSelect"
                  style="display: none"
                />
                <BaseButton 
                  @click="$refs.excelInput?.click()" 
                  variant="primary"
                  :disabled="importandoPersonas"
                >
                  📁 Seleccionar Archivo Excel
                </BaseButton>
                <span v-if="archivoSeleccionado" class="file-name">
                  ✅ {{ archivoSeleccionado.name }}
                </span>
              </div>

              <!-- Vista previa de datos -->
              <div v-if="datosVistaPreviaExcel.length > 0" class="preview-section">
                <h4>📊 Vista Previa (primeras 5 filas):</h4>
                <div class="preview-table">
                  <table>
                    <thead>
                      <tr>
                        <th v-for="header in encabezadosExcel" :key="header">{{ header }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(fila, index) in datosVistaPreviaExcel.slice(0, 5)" :key="index">
                        <td v-for="header in encabezadosExcel" :key="header">
                          {{ fila[header] || '-' }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <p class="preview-info">
                  Total de filas a importar: <strong>{{ datosVistaPreviaExcel.length }}</strong>
                </p>
              </div>

              <!-- Acciones -->
              <div class="import-actions">
                <BaseButton 
                  @click="cerrarModalImportar"
                  variant="secondary"
                  :disabled="importandoPersonas"
                >
                  ❌ Cancelar
                </BaseButton>
                <BaseButton 
                  @click="importarPersonasExcel"
                  variant="success"
                  :disabled="!archivoSeleccionado || importandoPersonas"
                >
                  {{ importandoPersonas ? '⏳ Importando...' : '📥 Importar Personas' }}
                </BaseButton>
              </div>

            </div>
          </div>
        </template>
      </BaseModal>
    </div>
  </div>
</template>


<script>
import InputBase from '@/components/InputBase.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseModal from '@/components/BaseModal.vue'
import personasService from '@/services/personasService.js'
import * as XLSX from 'xlsx'

export default {
  name: 'GestionPersonas',
  components: { InputBase, BaseSelect, BaseButton, BaseAlert, BaseModal },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRama: '',
  selectedCourse: '',
      roleOptions: [
        { value: '', label: 'Todos los roles' }
      ],
      ramaOptions: [
        { value: '', label: 'Todas las ramas' }
      ],
      courseOptions: [
        { value: '', label: 'Todos los grupos' }
      ],
  personaSeleccionada: null,
  editModalVisible: false,
  personaEditada: null,
  modalTab: 'info',
  modoSoloLectura: false,
  confirmModalVisible: false,
  mensajeConfirmacion: '',
  confirmModalAnularVisible: false,
  personaAAnular: null,
  
  // Modal de creación
  crearModalVisible: false,
  personaNueva: null,
  guardandoPersona: false,
  
  // Modal de importación
  importarModalVisible: false,
  importandoPersonas: false,
  archivoSeleccionado: null,
  datosVistaPreviaExcel: [],
  encabezadosExcel: [],
  
  // Privilegios del usuario - vendrá de la BD en producción/ Puede que necesite ajustes :P
  esAdministrador: true, // Activado para pruebas - se obtendrá de la BD
  
    filtroAplicado: false,
    filteredPersonas: [],
    filtrandoEnProceso: false,
    cargandoPersonas: false,
    errorCarga: null,
      personas: [] // Será cargado desde la BD en producción
    };
  },
  computed: {
    filtrosActivos() {
      const filtros = [];
      
      if (this.searchQuery && this.searchQuery.trim()) {
        filtros.push(`Búsqueda: "${this.searchQuery.trim()}"`);
      }
      
      if (this.selectedRole) {
        const rolLabel = this.roleOptions.find(r => r.value === this.selectedRole)?.label || this.selectedRole;
        filtros.push(`Rol: ${rolLabel}`);
      }
      
      if (this.selectedRama) {
        const ramaLabel = this.ramaOptions.find(r => r.value === this.selectedRama)?.label || this.selectedRama;
        filtros.push(`Rama: ${ramaLabel}`);
      }
      
      if (this.selectedCourse) {
        const cursoLabel = this.courseOptions.find(c => c.value === this.selectedCourse)?.label || this.selectedCourse;
        filtros.push(`Curso: ${cursoLabel}`);
      }
      
      return filtros;
    },
    
    filtroMensaje() {
      const filtros = this.filtrosActivos;
      if (filtros.length === 0) return '';
      
      if (filtros.length === 1) {
        return `Filtro activo: ${filtros[0]}`;
      } else {
        return `Filtros activos: ${filtros.join(' | ')}`;
      }
    },
    // Mostrar la instantánea de personas filtradas. Vacío hasta presionar Buscar.
    personasFiltradas() {
      return this.filteredPersonas || [];
    }
  },
  methods: {
    seleccionar(persona) {
      // mantener compatibilidad - también abrir modal para editar
      this.abrirModal(persona);
    },
    abrirModal(persona) {
      // clon profundo para que historial y objetos anidados queden aislados hasta guardar
      this.personaEditada = JSON.parse(JSON.stringify(persona || {}));
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      this.newHistEntry = { fecha: '', descripcion: '' };
      this.modalTab = 'info';
      this.editModalVisible = true;
      // también mantener referencia al elemento original para la lógica de guardado
      this.personaSeleccionada = persona;
  this.pendingSave = false;
    },
    abrirModalVer(persona) {
      // Abrir modal solo para ver - mostrar info pero sin editar
      this.personaEditada = JSON.parse(JSON.stringify(persona || {}));
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      this.modalTab = 'info';
      this.modoSoloLectura = true;
      this.editModalVisible = true;
      this.personaSeleccionada = persona;
      this.pendingSave = false;
    },
    abrirModalEditar(persona) {
      // Abrir modal solo para editar - forzar tab de info
      this.personaEditada = JSON.parse(JSON.stringify(persona || {}));
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      this.newHistEntry = { fecha: '', descripcion: '' };
      this.modalTab = 'info';
      this.modoSoloLectura = false;
      this.editModalVisible = true;
      this.personaSeleccionada = persona;
      this.pendingSave = false;
    },
    cancelarEdicion() {
      // cerrar modal usando la propiedad reactiva
      this.editModalVisible = false;
      this.personaEditada = null;
      this.personaSeleccionada = null;
      this.pendingSave = false;
    },
    cerrarDetalle() {
      this.personaSeleccionada = null;
    },
    filtrar() {
      // Evitar doble ejecución usando debounce
      if (this.filtrandoEnProceso) {
        return;
      }
      this.filtrandoEnProceso = true;
      
      // Usar setTimeout para asegurar que solo se ejecute una vez
      setTimeout(() => {
        this.ejecutarFiltrado();
        this.filtrandoEnProceso = false;
      }, 10);
    },
    ejecutarFiltrado() {
      // Verificar que al menos un filtro esté activo
      const q = (this.searchQuery || '').toLowerCase().trim();
      const selectedRoleNorm = (this.selectedRole || '').toString().trim();
      const selectedRamaNorm = (this.selectedRama || '').toString().trim();
      const selectedCourseNorm = (this.selectedCourse || '').toString().trim();

      const tieneAlgunFiltro = q || selectedRoleNorm || selectedRamaNorm || selectedCourseNorm;
      
      if (!tieneAlgunFiltro) {
        alert('Debe usar al menos un filtro para buscar (nombre/RUT/email, rol, rama o grupo).');
        return;
      }

      // Marcar que el usuario aplicó el filtro para mostrar la lista
      this.filtroAplicado = true;
      // cerrar detalle si estaba abierto
      this.personaSeleccionada = null;

      // Calcular la instantánea filtrada una vez
      console.log('🔍 Aplicando filtros:', {
        busqueda: q,
        rol: selectedRoleNorm,
        rama: selectedRamaNorm,
        grupo: selectedCourseNorm
      });
      console.log('📊 Total personas disponibles:', this.personas.length);

      this.filteredPersonas = this.personas.filter((p) => {
        // Usar los campos reales del modelo Django
        const nombre = (p.PER_NOMBRES || '').toLowerCase();
        const apellidoPat = (p.PER_APELPTA || '').toLowerCase();
        const apellidoMat = (p.PER_APELMAT || '').toLowerCase();
        const nombreCompleto = `${nombre} ${apellidoPat} ${apellidoMat}`.toLowerCase();
        const rut = (p.PER_RUN || '').toString().toLowerCase();
        const email = (p.PER_MAIL || '').toLowerCase();

        const coincideBusqueda = !q || nombreCompleto.includes(q) || rut.includes(q) || email.includes(q);

        // Filtros de rol, rama y grupo usando los nuevos campos
        const pRol = (p.PER_ROL || '').toString().trim();
        const pRama = (p.PER_RAMA || '').toString().trim();
        const pGrupo = (p.PER_GRUPO || '').toString().trim();

        const coincideRol = !selectedRoleNorm || pRol === selectedRoleNorm;
        const coincideRama = !selectedRamaNorm || pRama === selectedRamaNorm;
        const coincideGrupo = !selectedCourseNorm || pGrupo === selectedCourseNorm;

        return coincideBusqueda && coincideRol && coincideRama && coincideGrupo;
      });
      
      console.log('✅ Personas filtradas:', this.filteredPersonas.length);

      // pequeño comportamiento UX: scrollear la tabla hacia la vista
      this.$nextTick(() => {
        const el = document.querySelector('.table-wrapper');
        if (el && typeof el.scrollIntoView === 'function') el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    },
    // enriquecer objetos persona con campos adicionales tipo BD
    enrichPersonas() {
      const now = new Date().toISOString();
      this.personas = (this.personas || []).map((p, idx) => {
        const rawRut = (p.rut || '').toString().trim();
        let per_run = null;
        let per_dv = '';
        const m = rawRut.match(/([0-9\.]+)-?([0-9kK])/);
        if (m) {
          per_run = Number(m[1].replace(/\./g, '')) || null;
          per_dv = m[2] || '';
        }

  // dividir nombre en apellidos / nombres
        const nameParts = (p.nombre || '').toString().trim().split(/\s+/);
        let apelpat = '';
        let apelmat = '';
        let nombres = p.nombre || '';
        if (nameParts.length >= 2) {
          apelpat = nameParts[nameParts.length - 2] || '';
          apelmat = nameParts[nameParts.length - 1] || '';
          nombres = nameParts.slice(0, nameParts.length - 2).join(' ') || nombres;
          }

        const enriched = Object.assign({}, p, {
          PER_ID: idx + 1,
          ESC_ID: null,
          COM_ID: null,
          USU_ID: null,
          PER_FECHA_HORA: now,
          PER_RUN: per_run,
          PER_DV: per_dv,
          PER_APELPAT: apelpat,
          PER_APELMAT: apelmat,
          PER_NOMBRES: nombres || p.nombre,
          PER_EMAIL: p.email || '',
          PER_FECHA_NAC: p.fecha_nac || '1990-01-01',
          PER_DIRECCION: p.direccion || '',
          PER_TIPO_FONO: 'Móvil',
          PER_FONO: p.telefono || '',
          PER_ALERGIA_ENFERMEDAD: p.alergias || '',
          PER_LIMITACION: p.limitacion || '',
          PER_NOM_EMERGENCIA: p.contacto_emergencia || '',
          PER_FONO_EMERGENCIA: p.telefono_emergencia || '',
          PER_OTROS: p.otros || '',
          PER_NUM_MMAA: p.num_mmaa || 0,
          PER_PROFESION: p.profesion || '',
          PER_TIEMPO_NNAJ: p.tiempo_nnaj || '',
          PER_TIEMPO_ADULTO: p.tiempo_adulto || '',
          PER_RELIGION: p.religion || '',
          PER_APODO: p.apodo || '',
          PER_FOTO: p.foto || null,
          PER_VIGENTE: p.vigente === undefined ? true : !!p.vigente,
          cursos: p.cursos || [],
          historial: p.historial || []
        });

        return enriched;
      });
    },
    exportarExcel() {
      const datos = this.personasFiltradas.map((p) => ({
        Nombre: p.nombre,
        RUT: p.rut,
        Email: p.email,
        Rol: p.rol,
        Rama: p.rama,
        Grupo: p.grupo,
        Estado: p.estado
      }));
  // Exportar como CSV
      const keys = datos.length ? Object.keys(datos[0]) : ['Nombre','RUT','Email','Rol','Rama','Grupo','Estado'];
      const rows = [];
      rows.push(keys.join(','));

      for (const item of datos) {
        const values = keys.map((k) => {
          const v = item[k] ?? '';
          const safe = String(v).replace(/"/g, '""');
          return `"${safe}"`;
        });
        rows.push(values.join(','));
      }

      const csv = rows.join('\r\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });

  // Crear enlace de descarga
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.setAttribute('download', 'GestionPersonas.csv');
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    ,
    guardarEdicion() {
      if (!this.personaEditada || !this.personaEditada.PER_RUN || !this.personaEditada.PER_NOMBRES) {
        // validación mínima usando campos correctos
        alert('Nombre y RUT son obligatorios');
        return;
      }

      // Validar RUT si están separados los campos
      if (!this.personaEditada.PER_DV && this.personaEditada.PER_RUN) {
        alert('El dígito verificador del RUT es obligatorio');
        return;
      }

      // Validar formato del RUT
      if (this.personaEditada.PER_RUN && this.personaEditada.PER_DV) {
        if (!this.validarRutChileno(this.personaEditada.PER_RUN, this.personaEditada.PER_DV)) {
          alert('El RUT ingresado no es válido');
          return;
        }
      }

      // Mostrar popup de confirmación
      this.mensajeConfirmacion = `¿Seguro que quieres guardar estos cambios para ${this.personaEditada.PER_NOMBRES} ${this.personaEditada.PER_APELPTA}?`;
      this.confirmModalVisible = true;
    },
    
    async confirmarGuardado() {
      // Prevenir ejecución doble
      if (this.guardandoPersona) {
        console.log('⚠️ Ya se está guardando, ignorando solicitud duplicada');
        return;
      }
      
      try {
        this.confirmModalVisible = false;
        this.guardandoPersona = true;
        
        if (!this.personaEditada) {
          alert('No hay datos para guardar');
          return;
        }
        
        if (!this.personaEditada.PER_ID) {
          alert('Error: No se encontró el ID de la persona');
          console.error('❌ Persona sin ID:', this.personaEditada);
          return;
        }
        
        console.log('💾 Guardando cambios en persona:', this.personaEditada);
        console.log('📝 ID de persona:', this.personaEditada.PER_ID);
        
        // Validaciones básicas
        if (!this.personaEditada.PER_NOMBRES) {
          alert('El nombre es obligatorio');
          return;
        }
        
        if (!this.personaEditada.PER_RUN) {
          alert('El RUT es obligatorio');
          return;
        }

        if (!this.personaEditada.PER_DV) {
          alert('El dígito verificador del RUT es obligatorio');
          return;
        }

        // Validar formato de email si está presente
        if (this.personaEditada.PER_MAIL && !this.validarEmail(this.personaEditada.PER_MAIL)) {
          alert('El formato del email no es válido');
          return;
        }
        
        // Preparar datos para actualización - Solo campos básicos primero
        const datosActualizados = {
          PER_NOMBRES: this.personaEditada.PER_NOMBRES,
          PER_APELPTA: this.personaEditada.PER_APELPTA || '',
          PER_APELMAT: this.personaEditada.PER_APELMAT || '',
          PER_RUN: this.personaEditada.PER_RUN,
          PER_DV: this.personaEditada.PER_DV,
          PER_MAIL: this.personaEditada.PER_MAIL || '',
          PER_FECHA_NAC: this.personaEditada.PER_FECHA_NAC || null,
          PER_DIRECCION: this.personaEditada.PER_DIRECCION || '',
          PER_FONO: this.personaEditada.PER_FONO || '',
          PER_VIGENTE: this.personaEditada.PER_VIGENTE !== undefined ? this.personaEditada.PER_VIGENTE : true
        };
        
        console.log('📤 Datos a enviar:', datosActualizados);
        console.log('🌐 URL de actualización: personas/personas/' + this.personaEditada.PER_ID + '/');
        
        // Usar la API para actualizar (PATCH para actualización parcial)
        const personaActualizada = await personasService.personas.partialUpdate(
          this.personaEditada.PER_ID, 
          datosActualizados
        );
        
        console.log('✅ Persona actualizada:', personaActualizada);
        
        // Actualizar la lista de personas
        await this.cargarPersonas();
        
        // Cerrar modal
        this.editModalVisible = false;
        this.personaEditada = null;
        this.personaSeleccionada = null;
        
        console.log('✅ ¡Persona actualizada exitosamente!');
        alert('¡Persona actualizada exitosamente!');
        
      } catch (error) {
        console.error('❌ Error actualizando persona:', error);
        console.error('📋 Detalles del error:', {
          status: error.status,
          statusText: error.statusText,
          message: error.message,
          response: error.response
        });
        
        // Mostrar mensaje de error más específico
        let mensajeError = 'Error al actualizar la persona. ';
        
        if (error.status === 400) {
          mensajeError += 'Datos inválidos. Verifica que todos los campos estén correctos.';
        } else if (error.status === 404) {
          mensajeError += 'Persona no encontrada.';
        } else if (error.status === 500) {
          mensajeError += 'Error interno del servidor.';
        } else {
          mensajeError += 'Verifica tu conexión e intenta nuevamente.';
        }
        
        alert(mensajeError);
      } finally {
        this.guardandoPersona = false;
      }
    },
    
    cancelarConfirmacion() {
      // Cerrar modal de confirmación sin guardar
      this.confirmModalVisible = false;
    },
    
    anularPersona(persona) {
      // Guardar referencia a la persona a anular
      this.personaAAnular = persona;
      // Mostrar modal de confirmación
      this.confirmModalAnularVisible = true;
    },
    
    cancelarAnulacion() {
      // Cerrar modal de confirmación de anulación
      this.confirmModalAnularVisible = false;
      this.personaAAnular = null;
    },
    
    confirmarAnulacion() {
      if (!this.personaAAnular) return;
      
      // Marcar persona como anulada (gris)
      this.personaAAnular.estado = 'Anulado';
      this.personaAAnular.inscripcion = 'Anulado';
      this.personaAAnular.vigente = false;
      
      // Buscar en el array principal y actualizar
      const idx = this.personas.findIndex((p) => p.rut === this.personaAAnular.rut);
      if (idx !== -1) {
        this.$set ? this.$set(this.personas, idx, Object.assign({}, this.personaAAnular)) : 
                   (this.personas.splice(idx, 1, Object.assign({}, this.personaAAnular)));
      }
      
      // Actualizar en filteredPersonas si existe
      if (this.filteredPersonas && this.filteredPersonas.length) {
        const fidx = this.filteredPersonas.findIndex((p) => p.rut === this.personaAAnular.rut);
        if (fidx !== -1) {
          this.filteredPersonas.splice(fidx, 1, Object.assign({}, this.personaAAnular));
        }
      }
      
      // Cerrar modal
      this.confirmModalAnularVisible = false;
      this.personaAAnular = null;
    },
    
    addHistEntry() {
      if (!this.personaEditada) return;
      const fecha = (this.newHistEntry.fecha || '').trim();
      const descripcion = (this.newHistEntry.descripcion || '').trim();
      if (!fecha || !descripcion) {
        alert('Fecha y descripción son obligatorias para agregar al historial');
        return;
      }
      this.personaEditada.historial = this.personaEditada.historial || [];
      this.personaEditada.historial.unshift({ fecha, descripcion });
      this.newHistEntry = { fecha: '', descripcion: '' };
    },
    
    getCursoLabel(cursoCodigo) {
      const curso = this.courseOptions.find(c => c.value === cursoCodigo);
      return curso ? curso.label : cursoCodigo;
    },
    
    // Métodos para manejo de fotos de perfil
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Validar tipo de archivo
      if (!file.type.startsWith('image/')) {
        alert('Por favor selecciona un archivo de imagen válido.');
        return;
      }
      
      // Validar tamaño (máximo 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('El archivo es demasiado grande. Por favor selecciona una imagen menor a 5MB.');
        return;
      }
      
      // Convertir a base64 para almacenar en la aplicación
      const reader = new FileReader();
      reader.onload = (e) => {
        this.personaEditada.foto = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    removePhoto() {
      this.personaEditada.foto = null;
    },
    
    handleImageError() {
      // Si hay error al cargar la imagen, mostrar placeholder
      this.personaEditada.foto = null;
    },

    // === MÉTODOS PARA API ===
    async cargarPersonas() {
      try {
        this.cargandoPersonas = true;
        this.errorCarga = null;
        
        console.log('🔄 Intentando cargar personas con relaciones desde API...');
        const response = await personasService.personasCompletas.list();
        console.log('📡 Respuesta de la API:', response);
        
        // Procesar la respuesta
        if (Array.isArray(response)) {
          this.personas = response;
        } else if (response && response.results && Array.isArray(response.results)) {
          this.personas = response.results;
        } else {
          this.personas = [];
        }
        
        console.log('✅ Personas cargadas:', this.personas.length);
        
      } catch (error) {
        console.error('❌ Error cargando personas:', error);
        this.errorCarga = 'Error al cargar las personas. Verifica que el backend esté funcionando.';
        this.personas = [];
      } finally {
        this.cargandoPersonas = false;
      }
    },

    async cargarOpcionesFiltros() {
      try {
        console.log('🔄 Cargando opciones de filtros...');
        
        // Cargar roles
        console.log('📋 Obteniendo roles...');
        const roles = await personasService.obtenerRoles();
        this.roleOptions = [{ value: '', label: 'Todos los roles' }, ...roles];
        console.log('✅ Roles cargados:', roles.length, roles);
        
        // Cargar ramas
        console.log('🌿 Obteniendo ramas...');
        const ramas = await personasService.obtenerRamas();
        this.ramaOptions = [{ value: '', label: 'Todas las ramas' }, ...ramas];
        console.log('✅ Ramas cargadas:', ramas.length, ramas);
        
        // Cargar grupos
        console.log('👥 Obteniendo grupos...');
        const grupos = await personasService.obtenerGrupos();
        this.courseOptions = [{ value: '', label: 'Todos los grupos' }, ...grupos];
        console.log('✅ Grupos cargados:', grupos.length, grupos);
        
        console.log('🎉 Todas las opciones de filtros cargadas exitosamente');
        
      } catch (error) {
        console.error('❌ Error cargando opciones de filtros:', error);
        // Usar opciones básicas de respaldo
        this.roleOptions = [
          { value: '', label: 'Todos los roles' },
          { value: 'Participante', label: 'Participante' },
          { value: 'Formador Principal', label: 'Formador Principal' },
          { value: 'Coordinador', label: 'Coordinador' }
        ];
        this.ramaOptions = [
          { value: '', label: 'Todas las ramas' },
          { value: 'Castores', label: 'Castores' },
          { value: 'Lobatos', label: 'Lobatos' },
          { value: 'Scouts', label: 'Scouts' }
        ];
        this.courseOptions = [
          { value: '', label: 'Todos los grupos' },
          { value: 'Grupo San Jorge', label: 'Grupo San Jorge' },
          { value: 'Grupo Baden Powell', label: 'Grupo Baden Powell' }
        ];
      }
    },

    // === MÉTODOS PARA CREAR PERSONAS ===
    abrirModalCrear() {
      this.personaNueva = {
        PER_NOMBRES: '',
        PER_APELPTA: '',
        PER_APELMAT: '',
        PER_RUN: '',
        PER_DV: '',
        PER_MAIL: '',
        PER_FECHA_NAC: '',
        PER_DIRECCION: '',
        PER_TIPO_FONO: 2, // Celular por defecto
        PER_FONO: '',
        PER_APODO: '',
        PER_PROFESION: '',
        PER_CONTACTO_EMERGENCIA: '',
        PER_TELEFONO_EMERGENCIA: '',
        PER_ALERGIAS: '',
        PER_LIMITACION: '',
        PER_RELIGION: '',
        PER_TIEMPO_NNAJ: 0,
        PER_TIEMPO_ADULTO: 0,
        PER_VIGENTE: true,
        PER_ROL: '',
        PER_RAMA: ''
      };
      this.crearModalVisible = true;
    },

    cerrarModalCrear() {
      this.crearModalVisible = false;
      this.personaNueva = null;
    },

    // === MÉTODOS PARA IMPORTAR PERSONAS ===
    abrirModalImportar() {
      this.importarModalVisible = true;
      this.archivoSeleccionado = null;
      this.datosVistaPreviaExcel = [];
      this.encabezadosExcel = [];
    },

    cerrarModalImportar() {
      this.importarModalVisible = false;
      this.archivoSeleccionado = null;
      this.datosVistaPreviaExcel = [];
      this.encabezadosExcel = [];
    },

    handleFileSelect(event) {
      const archivo = event.target.files[0];
      if (!archivo) return;

      this.archivoSeleccionado = archivo;
      this.procesarArchivoExcel(archivo);
    },

    async procesarArchivoExcel(archivo) {
      try {
        console.log('📁 Procesando archivo:', archivo.name);
        
        // Leer el archivo usando FileReader
        const reader = new FileReader();
        
        reader.onload = (e) => {
          try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            
            // Obtener la primera hoja
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            
            // Convertir a JSON
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            
            if (jsonData.length === 0) {
              alert('El archivo Excel está vacío');
              return;
            }
            
            // La primera fila contiene los encabezados
            this.encabezadosExcel = jsonData[0];
            
            // Las filas restantes contienen los datos
            const filasDatos = jsonData.slice(1);
            
            // Convertir a objetos usando los encabezados
            this.datosVistaPreviaExcel = filasDatos.map(fila => {
              const objeto = {};
              this.encabezadosExcel.forEach((encabezado, index) => {
                objeto[encabezado] = fila[index] || '';
              });
              return objeto;
            }).filter(objeto => {
              // Filtrar filas vacías
              return Object.values(objeto).some(valor => valor && valor.toString().trim() !== '');
            });
            
            console.log('✅ Archivo procesado:', this.datosVistaPreviaExcel.length, 'filas encontradas');
            
          } catch (error) {
            console.error('❌ Error al procesar el contenido del archivo:', error);
            alert('Error al procesar el archivo. Verifica que sea un archivo Excel válido.');
          }
        };
        
        reader.onerror = () => {
          console.error('❌ Error al leer el archivo');
          alert('Error al leer el archivo');
        };
        
        // Leer el archivo como ArrayBuffer
        reader.readAsArrayBuffer(archivo);
        
      } catch (error) {
        console.error('❌ Error procesando archivo Excel:', error);
        alert('Error al procesar el archivo. Verifica que sea un archivo Excel válido.');
      }
    },

    async importarPersonasExcel() {
      if (!this.archivoSeleccionado || this.datosVistaPreviaExcel.length === 0) {
        alert('Selecciona un archivo válido primero');
        return;
      }

      try {
        this.importandoPersonas = true;
        
        console.log('📥 Iniciando importación de', this.datosVistaPreviaExcel.length, 'personas');
        
        let personasImportadas = 0;
        let errores = [];

        for (const fila of this.datosVistaPreviaExcel) {
          try {
            // Validar datos obligatorios
            if (!fila.PER_NOMBRES || !fila.PER_RUN || !fila.PER_DV) {
              errores.push(`Fila con datos incompletos: ${JSON.stringify(fila)}`);
              continue;
            }

            // Preparar datos para crear persona
            const datosPersona = {
              PER_NOMBRES: fila.PER_NOMBRES,
              PER_APELPTA: fila.PER_APELPTA || '',
              PER_APELMAT: fila.PER_APELMAT || '',
              PER_RUN: fila.PER_RUN,
              PER_DV: fila.PER_DV,
              PER_MAIL: fila.PER_MAIL || '',
              PER_FECHA_NAC: fila.PER_FECHA_NAC || null,
              PER_DIRECCION: fila.PER_DIRECCION || '',
              PER_FONO: fila.PER_FONO || '',
              PER_VIGENTE: true,
              ESC_ID: 1,
              COM_ID: 1,
              USU_ID: 1
            };

            // Crear persona usando el servicio
            await personasService.personas.create(datosPersona);
            personasImportadas++;

          } catch (error) {
            console.error('❌ Error creando persona:', error);
            errores.push(`Error con ${fila.PER_NOMBRES}: ${error.message}`);
          }
        }

        // Recargar lista de personas
        await this.cargarPersonas();

        // Cerrar modal
        this.cerrarModalImportar();

        // Mostrar resultado
        let mensaje = `✅ Importación completada!\n`;
        mensaje += `Personas importadas: ${personasImportadas}\n`;
        if (errores.length > 0) {
          mensaje += `Errores: ${errores.length}\n\n`;
          mensaje += errores.slice(0, 5).join('\n');
          if (errores.length > 5) {
            mensaje += `\n... y ${errores.length - 5} errores más.`;
          }
        }
        alert(mensaje);

      } catch (error) {
        console.error('❌ Error en importación:', error);
        alert('Error durante la importación. Verifica los datos e intenta nuevamente.');
      } finally {
        this.importandoPersonas = false;
      }
    },

    validarRutChileno(rut, dv) {
      if (!rut || !dv) return false;
      
      const rutNumerico = parseInt(rut.replace(/\./g, ''));
      if (isNaN(rutNumerico)) return false;
      
      let suma = 0;
      let multiplicador = 2;
      
      const rutString = rutNumerico.toString();
      for (let i = rutString.length - 1; i >= 0; i--) {
        suma += parseInt(rutString[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
      }
      
      const resto = suma % 11;
      let dvCalculado = 11 - resto;
      
      if (dvCalculado === 11) dvCalculado = '0';
      else if (dvCalculado === 10) dvCalculado = 'K';
      else dvCalculado = dvCalculado.toString();
      
      return dv.toUpperCase() === dvCalculado;
    },

    validarEmail(email) {
      if (!email) return true; // Email es opcional
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },

    async guardarPersonaNueva() {
      try {
        this.guardandoPersona = true;
        
        // Validaciones
        if (!this.personaNueva.PER_NOMBRES) {
          alert('El nombre es obligatorio');
          return;
        }
        
        if (!this.personaNueva.PER_APELPTA) {
          alert('El apellido paterno es obligatorio');
          return;
        }
        
        if (!this.personaNueva.PER_RUN || !this.personaNueva.PER_DV) {
          alert('El RUT es obligatorio');
          return;
        }
        
        if (!this.validarRutChileno(this.personaNueva.PER_RUN, this.personaNueva.PER_DV)) {
          alert('El RUT ingresado no es válido');
          return;
        }
        
        if (!this.personaNueva.PER_MAIL) {
          alert('El email es obligatorio');
          return;
        }
        
        if (!this.personaNueva.PER_FECHA_NAC) {
          alert('La fecha de nacimiento es obligatoria');
          return;
        }
        
        // Preparar datos para envío
        const datosPersona = {
          ...this.personaNueva,
          ESC_ID: 1, // Estado civil por defecto (soltero)
          COM_ID: 1, // Comuna por defecto 
          USU_ID: 1  // Usuario por defecto
        };
        
        console.log('💾 Guardando nueva persona:', datosPersona);
        
        const personaCreada = await personasService.personas.create(datosPersona);
        console.log('✅ Persona creada:', personaCreada);
        
        // Actualizar lista de personas
        await this.cargarPersonas();
        
        // Cerrar modal
        this.cerrarModalCrear();
        
        alert('¡Persona creada exitosamente!');
        
      } catch (error) {
        console.error('❌ Error creando persona:', error);
        alert('Error al crear la persona. Verifica los datos e intenta nuevamente.');
      } finally {
        this.guardandoPersona = false;
      }
    }
  },
  
  async mounted() {
    // Cargar personas y opciones de filtros al montar el componente
    await Promise.all([
      this.cargarPersonas(),
      this.cargarOpcionesFiltros()
    ]);
  }
};
</script>

<style>
.gestion-personas {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px; 
  background: #ffffff;
  color: #111;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: Arial, sans-serif;
  width: 1400px;                
  max-width: calc(100% - 48px);
  height: auto;
  max-height: calc(100vh - 48px);
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(16,24,40,0.08);
  overflow: hidden;            
}

.main-area { 
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header h2 {
  background-color: #214e9c;
  color: #fff;
  padding: 14px 18px;
  border-radius: 6px;
  margin: 0 0 4px 0;
}

.header h3 {
  margin: 6px 0 0 0;
  color: #444;
  font-weight: 500;
}

.filtros {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 0 0 auto;
  padding: 12px 0;
  min-height: 56px;
  flex-wrap: wrap; 
  box-sizing: border-box;
  padding-right: 8px;
}

.filtros-left { display:flex; gap:12px; align-items:center; flex: 1 1 auto; min-width: 0 }
.filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

.filtros input,
.filtros select {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  color: #222;
  background: #fff;
}

.filtros input {
  flex: 1 1 0;
}
.filtros select {
  flex: 0 0 160px;
}


.filtros .base-input {
  flex: 1 1 420px; 
  min-width: 180px;
  max-width: 720px;
  margin-bottom: 0; 
}
.filtros .base-input .base-field {
  padding: 10px 12px;
  font-size: 14px;
}
.filtros .base-select {
  flex: 0 0 160px; 
  min-width: 120px;
  max-width: 220px;
  margin-bottom: 0;
}
.filtros .base-select .base-select__element {
  padding: 8px 10px;
  font-size: 14px;
}
.filtros button {
  flex: 0 0 auto;
  flex-shrink: 0; 
}

.buscar, .exportar {
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-search, .buscar { background: linear-gradient(180deg,#2b6cb0,#154c8c); color: #fff; box-shadow: 0 6px 18px rgba(33,78,156,0.12); border: none; }
.btn-export, .exportar { background: linear-gradient(180deg,#16a34a,#15803d); color: #fff; box-shadow: 0 6px 18px rgba(16,185,129,0.08); border: none; }

.btn-edit { background: linear-gradient(180deg,#facc15,#f59e0b); color: #111; box-shadow: 0 6px 18px rgba(250,204,21,0.08); }
.btn-ver { background: linear-gradient(180deg,#3b82f6,#1d4ed8); color: #fff; box-shadow: 0 6px 18px rgba(59,130,246,0.12); }
.btn-editar { background: linear-gradient(180deg,#facc15,#f59e0b); color: #111; box-shadow: 0 6px 18px rgba(250,204,21,0.08); }
.btn-anular { background: linear-gradient(180deg,#ef4444,#dc2626); color: #fff; box-shadow: 0 6px 18px rgba(239,68,68,0.12); }
.btn-save { background: linear-gradient(180deg,#2563eb,#1e40af); color:#fff; box-shadow: 0 8px 24px rgba(37,99,235,0.12); }
.btn-confirm { background: linear-gradient(180deg,#059669,#047857); color:#fff; box-shadow: 0 8px 24px rgba(5,150,105,0.12); }

.btn-search, .btn-export, .btn-edit, .btn-ver, .btn-editar, .btn-anular, .btn-save, .btn-confirm {
  padding: 8px 14px;
  border-radius: 8px;
  font-weight:700;
  transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
}
.btn-search:hover, .btn-export:hover, .btn-edit:hover, .btn-ver:hover, .btn-editar:hover, .btn-anular:hover, .btn-save:hover, .btn-confirm:hover { transform: translateY(-2px); }
.btn-search:active, .btn-export:active, .btn-edit:active, .btn-ver:active, .btn-editar:active, .btn-anular:active, .btn-save:active, .btn-confirm:active { transform: translateY(0); }
.btn-search:focus, .btn-export:focus, .btn-edit:focus, .btn-ver:focus, .btn-editar:focus, .btn-anular:focus, .btn-save:focus, .btn-confirm:focus { outline: 3px solid rgba(33,78,156,0.12); }

.acciones-buttons {
  display: flex;
  gap: 3px;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}

.acciones-buttons .base-button {
  font-size: 11px;
  padding: 3px 6px;
  min-width: auto;
  white-space: nowrap;
}

.editar { padding: 6px 10px; }

.filtro-activo {
  background-color: #f4faf5;
  color: #115e26;
  padding: 8px;
  margin-bottom: 6px;
  border-radius: 4px;
}

.table-wrapper {
  flex: 1 1 auto;
  overflow: auto;
  padding-right: 12px; 
  -webkit-overflow-scrolling: touch;
  min-height: 0; 
}

.main-area {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  overflow: hidden; 
  min-height: 0; 
}

table {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  background-color: #fff;
  min-width: 0; 
  font-size: 14px;
}

th, td {
  padding: 14px 12px;
  border-bottom: 1px solid #ececec;
  text-align: left;
  color: #222; 
  opacity: 1;
}

th {
  background-color: #f7f7f7;
  color: #222;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 2;
}

.editar {
  background-color: #facc15;
  color: #111;
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
}

.estado { padding: 4px 8px; border-radius: 12px; font-size: 12px; white-space: nowrap; }
.estado.vigente { background:#d1fae5; color:#065f46 }
.estado.no-vigente { background:#fbbf24; color:#1f2937 }
.estado.anulado { background:#e5e7eb; color:#374151; text-decoration: line-through; }
.estado.confirmado { background:#d1fae5; color:#065f46 }
.estado.aprobada { background:#d1fae5; color:#065f46 }
.estado.pendiente { background:#fff4db; color:#8f5b00 }

/* Estilos para filas de personas anuladas :c*/
.persona-anulada {
  background-color: #f3f4f6 !important;
  opacity: 0.7;
}

.persona-anulada td {
  color: #6b7280 !important;
  text-decoration: line-through;
}

.persona-anulada .estado.anulado {
  background: #d1d5db !important;
  color: #4b5563 !important;
}

.historial-anulado {
  opacity: 0.7;
}

.historial-item-anulado {
  background-color: #f3f4f6 !important;
  opacity: 0.8;
}

.historial-content-anulado {
  opacity: 0.9;
}

.historial-main-anulado {
  color: #6b7280 !important;
  text-decoration: line-through;
}

.historial-main-anulado strong {
  color: #6b7280 !important;
  text-decoration: line-through;
}

.curso-badge-anulado {
  background: #d1d5db !important;
  color: #4b5563 !important;
  text-decoration: line-through;
}

.aprobacion-badge-anulado {
  opacity: 0.6;
  text-decoration: line-through;
}

.aprobacion-badge-anulado.aprobado {
  background: #e5e7eb !important;
  color: #6b7280 !important;
}

.aprobacion-badge-anulado.no-aprobado {
  background: #e5e7eb !important;
  color: #6b7280 !important;
}

.detail-panel .detalle { flex: 0 0 auto; margin-top: 18px; padding: 14px 18px; background: #f6f7f9; border-radius: 6px; }
.detail-panel .detalle h4 { margin: 0 0 10px 0; color:#1e3a8a; font-size: 20px; font-weight:700 }

.placeholder-row td {
  text-align: center;
  color: #666;
  padding: 48px 10px;
  background: linear-gradient(180deg,#fff,#fbfbfb);
}

@media (max-width: 960px) {
  .filtros { flex-wrap: wrap; }
}

@media (max-width: 520px) {
  .gestion-personas { padding: 12px; }
  .filtros { flex-direction: column; align-items: stretch; }
  .filtros-left, .filtros-right { width: 100%; justify-content: space-between }
  .filtros input, .filtros select, .filtros .base-input, .filtros .base-select { width: 100%; }

  thead { display: none; }
  tr { display: block; margin-bottom: 12px; box-shadow: none; }
  td { display: flex; justify-content: space-between; border-bottom: 0; padding: 8px 6px; }
  .table-wrapper { overflow:auto; }
  td[data-label]::before { content: attr(data-label) ": "; font-weight:600; margin-right:6px; color:#333; }
}

@media (max-width: 1400px) {
  .gestion-personas {
    width: calc(100% - 32px);
    height: auto;
    margin: 12px auto;
    border-radius: 6px;
  }
}

@media (min-width: 1400px) {
  .main-area {
    flex-direction: row;
    align-items: flex-start;
    gap: 24px;
  }
  .table-wrapper {
    flex: 1 1 auto;
    max-height: calc(820px - 240px); 
    overflow: auto;
  }
  .detalle {
    flex: 0 0 420px;
    max-width: 420px;
  }
  .detail-panel .detalle { padding: 20px; }
}

.detail-panel .detalle {
  background: #f2f5f9; 
  border-radius: 6px;
  padding: 18px 18px 16px 18px;
  border: 1px solid rgba(33,78,156,0.08);
  color: #222;
  font-size: 15px;
  line-height: 1.4;
}
.detalle { box-shadow: 0 6px 20px rgba(16,24,40,0.06); }
.detail-panel .detalle h4 {
  background: transparent;
  color: #214e9c; 
  padding: 0;
  margin: 0 0 10px 0;
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
}
.detalle-contenido {
  display: flex;
  gap: 48px;
  align-items: flex-start;
  justify-content: space-between;
  border-top: 2px solid #214e9c; 
  padding-top: 14px;
  margin-top: 10px;
}


.detalle-header {
  background: #214e9c;
  color: #fff;
  padding: 12px 16px;
  border-radius: 6px 6px 0 0;
  margin-bottom: 12px;
  position: relative;
}
.detalle-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}
.cerrar-detalle {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  line-height: 1;
  padding: 6px 8px;
  border-radius: 4px;
}
.cerrar-detalle:hover { background: rgba(255,255,255,0.06); }
.detalle-body {
  background: #fff;
  border-radius: 0 0 6px 6px;
  padding: 18px;
  border: 1px solid #eef2f6;
}
.detalle-contenido .col {
  flex: 1 1 0;
  padding: 6px 8px;
}
.detalle-contenido .col:nth-child(1) { max-width: 420px; }
.detalle-contenido .col:nth-child(2) { max-width: 380px; }
.detalle-contenido .col:nth-child(3) { max-width: 260px; }
.detalle h5 { margin: 6px 0 8px 0; font-size: 15px; color: #111; font-weight: 700; line-height:1.2; display:block; text-transform: none; }
.detalle p { margin: 6px 0; color: #222; }
.detalle strong { display: inline-block; min-width: 110px; font-weight: 700; color: #111; }


td[data-label="Nombre"] { 
  text-transform: uppercase; 
  font-weight:600; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  max-width: 180px; 
}

td[data-label="RUT"] { 
  white-space: nowrap; 
}

.estado-carga {
  text-align: center;
  padding: 20px;
  color: #555;
  font-style: italic;
}

.mensaje-error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  margin: 10px 0;
  text-align: center;
}

.mensaje-error button {
  margin-top: 10px;
}

/* Estilos para el modal de creación */
.modal-crear {
  width: 800px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 24px 32px;
}

.modal-crear .modal-form {
  display:flex;
  flex-direction:column;
  gap:15px;
  padding-right: 8px;
}

.modal-crear .modal-form .row {
  display:flex;
  align-items:center;
  gap:12px;
  width: 100%;
}

.modal-crear .modal-form .row label {
  width: 180px;
  flex-shrink: 0;
  font-weight: 500;
  color: #333;
  font-size: 14px;
  text-align: left;
  padding-right: 8px;
}

.modal-crear .modal-form .row input,
.modal-crear .modal-form .row select {
  flex: 1;
  min-width: 280px;
}

.modal-crear .row:has(.rut-container) {
  flex-direction: column;
  align-items: flex-start;
}

.modal-crear .row:has(.rut-container) label {
  width: auto;
  margin-bottom: 8px;
}

.modal-crear .rut-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 280px;
  max-width: 280px;
}

.modal-crear .rut-container input:first-child {
  flex: 1;
  max-width: 200px;
}

.modal-crear .rut-separator {
  font-weight: bold;
  color: #666;
  font-size: 16px;
  margin: 0 4px;
}

.modal-crear .rut-dv {
  width: 60px !important;
  min-width: 60px !important;
  max-width: 60px !important;
  text-align: center;
  flex: none !important;
}

.modal-crear .form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  margin-top: 10px;
}

@media (max-width: 600px) {
  .modal-crear .modal-form .row {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .modal-crear .modal-form .row label {
    width: auto;
  }
  
  .modal-crear .modal-form .row input,
  .modal-crear .modal-form .row select {
    min-width: auto;
  }
  
  .modal-crear .form-actions {
    flex-direction: column;
  }
}


</style>

<style scoped>
/* Modal específico para personas - centrado completo */
.persona-modal :deep(.modal-overlay) {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  z-index: 9999 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.modal-edit {
  width: 800px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 24px 32px;
}
.modal-header { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:20px; }
.modal-header h3 { margin:0; font-size:18px; color:#214e9c }
.modal-close { background:transparent; border:none; font-size:18px; cursor:pointer }
.modal-header .header-actions { display:flex; gap:8px; align-items:center }
.modal-header .header-actions .base-button { padding:6px 10px }

@media (max-width: 520px) {
  .modal-header { flex-direction: column; align-items: stretch; gap:8px }
  .modal-header .header-actions { justify-content: flex-end }
  .modal-header .header-actions .base-button { padding:8px 12px }
}
.modal-form {
  display:flex;
  flex-direction:column;
  gap:15px;
  padding-right: 8px;
}

/* Grid de dos columnas para aprovechar mejor el espacio */
.form-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px 24px;
  margin-top: 10px;
}

.form-fields-grid .row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-fields-grid .row.full-width {
  grid-column: 1 / -1;
}

.form-fields-grid .row label {
  font-weight: 700;
  color: #222;
  font-size: 14px;
}

.form-fields-grid .row input,
.form-fields-grid .row select {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #e6e6e6;
  border-radius: 6px;
}

.form-fields-grid .row input:disabled,
.form-fields-grid .row select:disabled {
  background-color: #f5f5f5;
  color: #666;
  cursor: not-allowed;
}

.form-fields-grid .row input[readonly],
.form-fields-grid .row select[readonly] {
  background-color: #f9f9f9;
  color: #555;
}

/* Responsive: una columna en pantallas pequeñas */
@media (max-width: 768px) {
  .form-fields-grid {
    grid-template-columns: 1fr;
  }
  
  .form-fields-grid .row.full-width {
    grid-column: 1;
  }
}

.modal-form .row { display:flex; gap:15px; align-items:center; flex-wrap:wrap; width: 100%; }
.modal-form .row label { width:180px; min-width:140px; font-weight:700; color:#222; text-align: left; }
.modal-form .row input, .modal-form .row select { flex:1; min-width:280px; padding:12px 15px; border:1px solid #e6e6e6; border-radius:6px }
.modal-form .row input:disabled, .modal-form .row select:disabled { background-color:#f5f5f5; color:#666; cursor:not-allowed }
.modal-form .row input[readonly], .modal-form .row select[readonly] { background-color:#f9f9f9; color:#555 }
.modal-form .actions { justify-content:flex-end; margin-top:12px }
.modal-form .actions .base-button { margin-left:8px }

/* Estilos específicos para RUT en modal de editar */
.modal-form .row:has(.rut-container) {
  flex-direction: column;
  align-items: flex-start;
}

.modal-form .row:has(.rut-container) label {
  width: auto;
  margin-bottom: 8px;
}

.modal-form .rut-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 280px;
  max-width: 280px;
}

.modal-form .rut-container input:first-child {
  flex: 1;
  max-width: 200px;
}

.modal-form .rut-separator {
  font-weight: bold;
  color: #666;
  font-size: 16px;
  margin: 0 4px;
}

.modal-form .rut-dv {
  width: 60px !important;
  min-width: 60px !important;
  max-width: 60px !important;
  text-align: center;
  flex: none !important;
}

/* Estiloss para foto de perfil */
.foto-perfil-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.foto-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.foto-perfil {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.foto-perfil:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.foto-placeholder {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: #e2e8f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid #cbd5e1;
  color: #64748b;
}

.foto-icon {
  font-size: 50px;
  margin-bottom: 6px;
}

.foto-text {
  font-size: 14px;
  font-weight: 600;
}

.foto-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-foto-upload {
  background: linear-gradient(180deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.btn-foto-upload:hover {
  background: linear-gradient(180deg, #1d4ed8, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-foto-remove {
  background: linear-gradient(180deg, #ef4444, #dc2626);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

.btn-foto-remove:hover {
  background: linear-gradient(180deg, #dc2626, #b91c1c);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
</style>

<style scoped>
.modal-tabs { display:flex; gap:8px; margin-bottom:12px }
.modal-tabs button { padding:8px 12px; border-radius:6px; border:1px solid #e6e6e6; background:#fff; cursor:pointer }
.modal-tabs button.active { background:#214e9c; color:#fff; border-color:#214e9c }
.historial-panel { display:flex; gap:20px; align-items:flex-start }
.historial-panel { max-height: calc(100vh - 260px); overflow: auto; }
.hist-list { flex:1; overflow:auto; }
.hist-list ul { list-style:none; padding:0; margin:0 }
.hist-list li { padding:8px 10px; border-bottom:1px solid #eee }
.hist-add { width:320px; border-left:1px solid #f0f0f0; padding-left:16px }

.historial-item {
  padding: 12px 16px !important;
  border-bottom: 1px solid #e5e7eb !important;
  background: #fafafa;
  margin-bottom: 8px;
  border-radius: 6px;
}

.historial-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.historial-main {
  font-size: 14px;
  color: #374151;
  line-height: 1.4;
}

.historial-curso {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.curso-badge {
  background: #e0e7ff;
  color: #3730a3;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.aprobacion-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.aprobacion-badge.aprobado {
  background: #dcfce7;
  color: #166534;
}

.aprobacion-badge.no-aprobado {
  background: #fef2f2;
  color: #dc2626;
}

.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px 24px;
  background: linear-gradient(135deg, #fafafa, #f3f4f6);
  border-radius: 12px;
  margin: -16px;
}

.confirm-icon {
  font-size: 64px;
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.confirm-content p {
  font-size: 18px;
  color: #1f2937;
  margin-bottom: 8px;
  line-height: 1.6;
  font-weight: 500;
  max-width: 400px;
}

.confirm-content p:last-of-type {
  margin-bottom: 24px;
}

.confirm-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.confirm-warning {
  font-size: 14px;
  color: #d97706;
  font-style: italic;
  margin-bottom: 16px !important;
}

.btn-modal-cancel {
  background: linear-gradient(180deg, #6b7280, #4b5563) !important;
  color: #fff !important;
  border: none !important;
  padding: 12px 24px !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  min-width: 120px !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 4px 12px rgba(107, 114, 128, 0.25) !important;
}

.btn-modal-cancel:hover {
  background: linear-gradient(180deg, #4b5563, #374151) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 16px rgba(107, 114, 128, 0.35) !important;
}

.btn-modal-confirm {
  background: linear-gradient(180deg, #10b981, #059669) !important;
  color: #fff !important;
  border: none !important;
  padding: 12px 24px !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  min-width: 120px !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
}

.btn-modal-confirm:hover {
  background: linear-gradient(180deg, #059669, #047857) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35) !important;
}

.btn-modal-anular {
  background: linear-gradient(180deg, #ef4444, #dc2626) !important;
  color: #fff !important;
  border: none !important;
  padding: 12px 24px !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  min-width: 120px !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25) !important;
}

.btn-modal-anular:hover {
  background: linear-gradient(180deg, #dc2626, #b91c1c) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.35) !important;
}

.btn-modal-cancel:active,
.btn-modal-confirm:active,
.btn-modal-anular:active {
  transform: translateY(0) !important;
}

/* Estilos para el modal de importar Excel */
.modal-importar {
  width: 800px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 24px 32px;
}

.import-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.import-instructions {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
}

.import-instructions h4 {
  margin: 0 0 12px 0;
  color: #334155;
  font-size: 16px;
}

.import-instructions ul {
  margin: 0;
  padding-left: 20px;
}

.import-instructions li {
  margin-bottom: 8px;
  color: #64748b;
}

.file-selector {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
}

.file-name {
  font-weight: 500;
  color: #059669;
}

.preview-section {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
}

.preview-section h4 {
  margin: 0 0 16px 0;
  color: #334155;
}

.preview-table {
  overflow-x: auto;
  margin-bottom: 12px;
}

.preview-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.preview-table th,
.preview-table td {
  padding: 8px 12px;
  text-align: left;
  border: 1px solid #e2e8f0;
}

.preview-table th {
  background: #f1f5f9;
  font-weight: 600;
  color: #334155;
}

.preview-table td {
  background: white;
  color: #64748b;
}

.preview-info {
  margin: 0;
  font-weight: 500;
  color: #059669;
}

.import-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

@media (max-width: 600px) {
  .modal-importar {
    padding: 16px;
  }
  
  .file-selector {
    flex-direction: column;
    text-align: center;
  }
  
  .import-actions {
    flex-direction: column;
  }
}
</style>
