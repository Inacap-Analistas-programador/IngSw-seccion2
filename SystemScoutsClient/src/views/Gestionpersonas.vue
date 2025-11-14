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
        <BaseButton class="btn-search btn-standard" variant="primary" @click="filtrar"><AppIcons name="search" :size="16" /> Buscar</BaseButton>
      </div>
      <div class="filtros-right">
        <BaseButton v-if="canCreate" class="btn-add btn-standard" variant="success" @click="abrirModalCrear"><AppIcons name="plus" :size="16" /> Nueva Persona</BaseButton>
        <BaseButton v-if="canCreate" class="btn-import btn-standard" variant="info" @click="abrirModalImportar"><AppIcons name="download" :size="16" /> Importar Excel</BaseButton>
        <BaseButton class="btn-export btn-standard" variant="secondary" @click="exportarExcel"><AppIcons name="upload" :size="16" /> Exportar</BaseButton>
      </div>
    </div>

    <!-- Mensaje informativo de permisos limitados -->
    <div v-if="isReadOnly" class="mensaje-info-permisos">
      <AppIcons name="info" :size="18" />
      <span>Estás viendo este módulo en modo solo lectura. Contacta al administrador para solicitar permisos de edición.</span>
    </div>

    <!-- Indicadores de carga y error -->
    <div v-if="cargandoPersonas" class="estado-carga">
      <p><AppIcons name="refresh" :size="16" /> Cargando personas...</p>
    </div>
    
    <div v-if="errorCarga" class="mensaje-error">
      <p><AppIcons name="alert-circle" :size="16" /> {{ errorCarga }}</p>
      <BaseButton @click="cargarPersonas" variant="primary" class="btn-standard"><AppIcons name="refresh" :size="16" /> Reintentar</BaseButton>
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
          <th>Teléfono/Celular</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in personasFiltradas" :key="p.PER_RUN" :class="{ 'persona-anulada': !p.PER_VIGENTE }">
          <td data-label="Nombre" :title="`${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim()">
            {{ `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim() }}
          </td>
          <td data-label="RUT">{{ p.PER_RUN }}-{{ p.PER_DV }}</td>
          <td data-label="Email">{{ p.PER_MAIL }}</td>
          <td data-label="Rol">{{ p.PER_ROL || 'Sin rol' }}</td>
          <td data-label="Teléfono/Celular">{{ p.PER_FONO || p.PER_CEL || 'Sin teléfono' }}</td>
          <td data-label="Estado">
            <span
              :class="['estado', p.PER_VIGENTE ? 'activo' : 'inactivo']"
            >
              {{ p.PER_VIGENTE ? 'Activo' : 'Inactivo' }}
            </span>
          </td>
          <td>
            <div class="acciones-buttons">
              <BaseButton class="btn-ver btn-action" variant="info" @click="abrirModalVer(p)"><AppIcons name="eye" :size="14" /> Ver</BaseButton>
              <BaseButton 
                v-if="canEdit" 
                class="btn-editar btn-action" 
                variant="secondary" 
                @click="abrirModalEditar(p)"
              >
                <AppIcons name="edit" :size="14" /> Editar
              </BaseButton>
              <BaseButton 
                v-if="canDelete && p.PER_VIGENTE" 
                class="btn-anular btn-action" 
                variant="warning" 
                @click="anularPersona(p)"
              >
                <AppIcons name="x" :size="14" /> Anular
              </BaseButton>
              <BaseButton 
                v-if="canDelete && !p.PER_VIGENTE" 
                class="btn-reactivar btn-action" 
                variant="success" 
                @click="reactivarPersona(p)"
              >
                <AppIcons name="check" :size="14" /> Reactivar
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
  <BaseModal v-model="editModalVisible" @close="cancelarEdicion" class="persona-modal modal-editar-mejorado">
        <template #default>
          <div class="modal-edit">
                <header class="modal-header-editar">
                  <div class="header-title">
                    <h2>{{ modoSoloLectura ? 'Ver Persona' : 'Editar Persona' }}</h2>
                    <p class="subtitle">{{ `${personaEditada?.PER_NOMBRES || ''} ${personaEditada?.PER_APELPTA || ''}`.trim() }}</p>
                  </div>
                  <div class="header-actions" v-if="!modoSoloLectura">
                    <BaseButton 
                      class="btn-save btn-modal-header" 
                      type="button" 
                      variant="primary" 
                      @click="guardarEdicion"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons :name="guardandoPersona ? 'clock' : 'save'" :size="16" />
                      {{ guardandoPersona ? 'Guardando...' : 'Guardar Cambios' }}
                    </BaseButton>
                  </div>
                </header>

                <div class="modal-tabs">
                  <button :class="{active: modalTab === 'info'}" @click="modalTab='info'">Info</button>
                  <button :class="{active: modalTab === 'hist'}" @click="modalTab='hist'">Historial</button>
                </div>

                <form v-if="modalTab==='info'" @submit.prevent="" class="modal-form-editar">
                  <!-- Sección de Foto de Perfil -->
                  <div class="form-section foto-section">
                    <div class="foto-container-editar">
                      <div class="foto-preview-wrapper">
                        <img 
                          v-if="personaEditada.foto" 
                          :src="personaEditada.foto" 
                          :alt="`Foto de ${personaEditada.PER_NOMBRES}`"
                          class="foto-perfil-editar"
                          @error="handleImageError('editar')"
                        />
                        <div v-else class="foto-placeholder-editar">
                          <AppIcons name="person" :size="80" />
                          <span class="foto-text">Sin foto</span>
                        </div>
                      </div>
                      <div v-if="!modoSoloLectura" class="foto-actions-editar">
                        <input 
                          ref="fotoInput"
                          type="file" 
                          accept="image/png, image/jpeg, image/jpg" 
                          @change="handleFileUpload($event, 'editar')"
                          style="display: none"
                        />
                        <button 
                          type="button" 
                          @click="$refs.fotoInput?.click()" 
                          class="btn-foto-upload"
                        >
                          <AppIcons name="camera" :size="16" /> {{ personaEditada.foto ? 'Cambiar Foto' : 'Subir Foto' }}
                        </button>
                        <button 
                          v-if="personaEditada.foto" 
                          type="button" 
                          @click="removePhoto('editar')" 
                          class="btn-foto-remove"
                        >
                          <AppIcons name="trash" :size="16" /> Eliminar
                        </button>
                      </div>
                      <div class="foto-info">
                        <small>PNG o JPG • Máx. 5MB • Se redimensiona a 300x300px</small>
                      </div>
                    </div>
                  </div>

                  <!-- Información Personal -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="person" :size="18" />
                      Información Personal
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Nombres *</label>
                        <InputBase v-model="personaEditada.PER_NOMBRES" :readonly="modoSoloLectura" required placeholder="Ingrese nombres" />
                      </div>
                      <div class="form-field">
                        <label>Apellido Paterno</label>
                        <InputBase v-model="personaEditada.PER_APELPTA" :readonly="modoSoloLectura" placeholder="Ingrese apellido paterno" />
                      </div>
                      <div class="form-field">
                        <label>Apellido Materno</label>
                        <InputBase v-model="personaEditada.PER_APELMAT" :readonly="modoSoloLectura" placeholder="Ingrese apellido materno" />
                      </div>
                      <div class="form-field">
                        <label>RUT</label>
                        <div class="rut-container">
                          <InputBase v-model="personaEditada.PER_RUN" :readonly="modoSoloLectura" @input="calcularDvEditada" placeholder="12345678" />
                          <span class="rut-separator">-</span>
                          <InputBase v-model="personaEditada.PER_DV" :readonly="modoSoloLectura" class="rut-dv" maxlength="1" placeholder="9" />
                        </div>
                      </div>
                      <div class="form-field">
                        <label>Fecha de Nacimiento</label>
                        <InputBase v-model="personaEditada.PER_FECHA_NAC" :readonly="modoSoloLectura" type="date" />
                      </div>
                      <div class="form-field">
                        <label>Estado Civil</label>
                        <BaseSelect v-model="personaEditada.ESC_ID" :options="estadoCivilOptions" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Apodo</label>
                        <InputBase v-model="personaEditada.PER_APODO" :readonly="modoSoloLectura" placeholder="Ingrese apodo" />
                      </div>
                      <div class="form-field">
                        <label>Religión</label>
                        <InputBase v-model="personaEditada.PER_RELIGION" :readonly="modoSoloLectura" placeholder="Ingrese religión" />
                      </div>
                    </div>
                  </div>

                  <!-- Información de Contacto -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="phone" :size="18" />
                      Información de Contacto
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Email</label>
                        <InputBase v-model="personaEditada.PER_MAIL" :readonly="modoSoloLectura" type="email" placeholder="correo@ejemplo.com" />
                      </div>
                      <div class="form-field">
                        <label>Teléfono</label>
                        <div class="phone-input-wrapper">
                          <span class="phone-prefix">+56</span>
                          <InputBase v-model="personaEditada.PER_FONO" :readonly="modoSoloLectura" placeholder="912345678" class="phone-input" />
                        </div>
                      </div>
                      <div class="form-field full-width">
                        <label>Dirección</label>
                        <InputBase v-model="personaEditada.PER_DIRECCION" :readonly="modoSoloLectura" placeholder="Ingrese dirección completa" />
                      </div>
                      <div class="form-field">
                        <label>Región</label>
                        <BaseSelect v-model="personaEditada.REG_ID" :options="regionOptions" :disabled="modoSoloLectura" @change="cargarProvinciasPorRegionEditar" />
                      </div>
                      <div class="form-field">
                        <label>Provincia</label>
                        <BaseSelect v-model="personaEditada.PRO_ID" :options="provinciaOptionsEditar" :disabled="modoSoloLectura || !personaEditada.REG_ID" @change="cargarComunasPorProvinciaEditar" />
                      </div>
                      <div class="form-field">
                        <label>Comuna</label>
                        <BaseSelect v-model="personaEditada.COM_ID" :options="comunaOptionsEditar" :disabled="modoSoloLectura || !personaEditada.PRO_ID" />
                      </div>
                    </div>
                  </div>

                  <!-- Información de Emergencia -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="alert" :size="18" />
                      Información de Emergencia
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Contacto de Emergencia</label>
                        <InputBase v-model="personaEditada.PER_NOM_EMERGENCIA" :readonly="modoSoloLectura" placeholder="Nombre del contacto" />
                      </div>
                      <div class="form-field">
                        <label>Teléfono de Emergencia</label>
                        <div class="phone-input-wrapper">
                          <span class="phone-prefix">+56</span>
                          <InputBase v-model="personaEditada.PER_FONO_EMERGENCIA" :readonly="modoSoloLectura" placeholder="912345678" class="phone-input" />
                        </div>
                      </div>
                      <div class="form-field full-width">
                        <label>Alergias / Enfermedades</label>
                        <InputBase v-model="personaEditada.PER_ALERGIA_ENFERMEDAD" :readonly="modoSoloLectura" placeholder="Describa alergias o enfermedades" />
                      </div>
                      <div class="form-field full-width">
                        <label>Limitaciones</label>
                        <InputBase v-model="personaEditada.PER_LIMITACION" :readonly="modoSoloLectura" placeholder="Describa limitaciones físicas o médicas" />
                      </div>
                    </div>
                  </div>

                  <!-- Información -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="badge" :size="18" />
                      Información
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Rol</label>
                        <BaseSelect v-model="personaEditada.PER_ROL" :options="roleOptions" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Rama</label>
                        <BaseSelect v-model="personaEditada.PER_RAMA" :options="ramaOptions" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Profesión</label>
                        <InputBase v-model="personaEditada.PER_PROFESION" :readonly="modoSoloLectura" placeholder="Ingrese profesión" />
                      </div>
                      <div class="form-field">
                        <label>Número MMA</label>
                        <InputBase v-model="personaEditada.PER_NUM_MMA" :readonly="modoSoloLectura" type="number" placeholder="Número de miembro" />
                      </div>
                      <div class="form-field">
                        <label>Tiempo NNAJ</label>
                        <InputBase v-model="personaEditada.PER_TIEMPO_NNAJ" :readonly="modoSoloLectura" placeholder="Ej: 5 años" />
                      </div>
                      <div class="form-field">
                        <label>Tiempo Adulto</label>
                        <InputBase v-model="personaEditada.PER_TIEMPO_ADULTO" :readonly="modoSoloLectura" placeholder="Ej: 3 años" />
                      </div>
                      <div class="form-field">
                        <label>Estado</label>
                        <BaseSelect v-model="personaEditada.PER_VIGENTE" :options="[{value: true, label: 'Vigente'}, {value: false, label: 'No Vigente'}]" :disabled="modoSoloLectura" />
                      </div>
                    </div>
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
            <div class="confirm-icon warning-icon"><AppIcons name="alert-triangle" :size="48" /></div>
            <p>{{ mensajeConfirmacion }}</p>
            <div class="confirm-actions">
              <BaseButton @click="cancelarConfirmacion" variant="secondary" class="btn-modal-cancel btn-modal">
                <AppIcons name="x" :size="16" /> Cancelar
              </BaseButton>
              <BaseButton @click="confirmarGuardado" variant="primary" class="btn-modal-confirm btn-modal">
                <AppIcons name="check" :size="16" /> Confirmar
              </BaseButton>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Confirmación para Anular -->
      <BaseModal v-model="confirmModalAnularVisible" title="Confirmar Anulación">
        <template #default>
          <div class="confirm-content">
            <div class="confirm-icon warning-icon"><AppIcons name="alert-triangle" :size="48" /></div>
            <p>¿Estás seguro de que deseas anular a <strong>{{ personaAAnular?.PER_NOMBRES }} {{ personaAAnular?.PER_APELPTA }}</strong>?</p>
            <p class="confirm-warning">Esta acción marcará a la persona como no vigente en la base de datos.</p>
            <div class="confirm-actions">
              <BaseButton @click="cancelarAnulacion" variant="secondary" class="btn-modal-cancel btn-modal">
                <AppIcons name="x" :size="16" /> Cancelar
              </BaseButton>
              <BaseButton @click="confirmarAnulacion" variant="warning" class="btn-modal-anular btn-modal">
                <AppIcons name="alert-triangle" :size="16" /> Anular
              </BaseButton>
            </div>
          </div>
        </template>
      </BaseModal>
      
      <!-- Modal de Creación de Persona -->
      <BaseModal v-model="crearModalVisible" @close="cerrarModalCrear" class="persona-modal modal-crear-mejorado">
        <template #default>
          <div class="modal-crear">
            <!-- Header mejorado -->
            <header class="modal-header-crear">
              <div class="header-title">
                <h2>Nueva Persona</h2>
                <p class="subtitle">Completa la información para crear un nuevo registro</p>
              </div>
              <div class="header-actions">
                <BaseButton 
                  class="btn-save btn-modal-header" 
                  type="button" 
                  variant="primary" 
                  @click.prevent="guardarPersonaNueva"
                  :disabled="guardandoPersona"
                >
                  <AppIcons :name="guardandoPersona ? 'clock' : 'save'" :size="16" />
                  {{ guardandoPersona ? 'Guardando...' : 'Guardar Persona' }}
                </BaseButton>
              </div>
            </header>

            <form @submit.prevent="guardarPersonaNueva" class="modal-form-crear">
              
              <!-- Sección de Foto de Perfil -->
              <div class="form-section foto-section">
                <div class="foto-container-crear">
                  <div class="foto-preview-wrapper">
                    <img 
                      v-if="personaNueva.foto" 
                      :src="personaNueva.foto" 
                      alt="Foto de perfil"
                      class="foto-perfil-crear"
                      @error="handleImageError('nueva')"
                    />
                    <div v-else class="foto-placeholder-crear">
                      <AppIcons name="person" :size="80" />
                      <span class="foto-text">Sin foto</span>
                    </div>
                  </div>
                  <div class="foto-actions-crear">
                    <input 
                      ref="fotoInputNueva"
                      type="file" 
                      accept="image/png, image/jpeg, image/jpg" 
                      @change="handleFileUpload($event, 'nueva')"
                      style="display: none"
                    />
                    <button 
                      type="button" 
                      @click="$refs.fotoInputNueva?.click()" 
                      class="btn-foto-upload"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons name="camera" :size="16" /> {{ personaNueva.foto ? 'Cambiar Foto' : 'Subir Foto' }}
                    </button>
                    <button 
                      v-if="personaNueva.foto" 
                      type="button" 
                      @click="removePhoto('nueva')" 
                      class="btn-foto-remove"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons name="trash" :size="16" /> Eliminar
                    </button>
                  </div>
                  <div class="foto-info">
                    <small>PNG o JPG • Máx. 5MB • Se redimensiona a 300x300px</small>
                  </div>
                </div>
              </div>

              <!-- Información Personal -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="person" :size="18" />
                  Información Personal
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Nombres *</label>
                    <InputBase 
                      v-model="personaNueva.PER_NOMBRES" 
                      placeholder="Ej: Juan Carlos" 
                      :disabled="guardandoPersona"
                      required
                    />
                  </div>
                  
                  <div class="form-field">
                    <label>Apellido Paterno *</label>
                    <InputBase 
                      v-model="personaNueva.PER_APELPTA" 
                      placeholder="Ej: González" 
                      :disabled="guardandoPersona"
                      required
                    />
                  </div>
                  
                  <div class="form-field">
                    <label>Apellido Materno</label>
                    <InputBase 
                      v-model="personaNueva.PER_APELMAT" 
                      placeholder="Ej: Pérez" 
                      :disabled="guardandoPersona"
                    />
                  </div>
                  
                  <div class="form-field">
                    <label>RUT *</label>
                    <div class="rut-container">
                      <InputBase 
                        v-model="personaNueva.PER_RUN" 
                        placeholder="12345678" 
                        :disabled="guardandoPersona"
                        @input="calcularDvNueva"
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

                  <div class="form-field">
                    <label>Fecha de Nacimiento *</label>
                    <InputBase 
                      v-model="personaNueva.PER_FECHA_NAC" 
                      type="date"
                      :disabled="guardandoPersona"
                      required
                    />
                  </div>

                  <div class="form-field">
                    <label>Estado Civil</label>
                    <BaseSelect 
                      v-model="personaNueva.ESC_ID" 
                      :options="estadoCivilOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Apodo</label>
                    <InputBase 
                      v-model="personaNueva.PER_APODO" 
                      placeholder="Ej: Juanito" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Religión</label>
                    <InputBase 
                      v-model="personaNueva.PER_RELIGION" 
                      placeholder="Católica, Evangélica, etc." 
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>

              <!-- Información de Contacto -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="phone" :size="18" />
                  Información de Contacto
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Email *</label>
                    <InputBase 
                      v-model="personaNueva.PER_MAIL" 
                      type="email"
                      placeholder="juan.gonzalez@email.com" 
                      :disabled="guardandoPersona"
                      required
                    />
                  </div>

                  <div class="form-field">
                    <label>Teléfono</label>
                    <div class="phone-input-wrapper">
                      <span class="phone-prefix">+56</span>
                      <InputBase 
                        v-model="personaNueva.PER_FONO" 
                        placeholder="912345678" 
                        :disabled="guardandoPersona"
                        class="phone-input"
                      />
                    </div>
                  </div>

                  <div class="form-field">
                    <label>Tipo de Teléfono</label>
                    <BaseSelect 
                      v-model="personaNueva.PER_TIPO_FONO" 
                      :options="[
                        { value: 1, label: 'Teléfono Fijo' },
                        { value: 2, label: 'Celular' }
                      ]"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field full-width">
                    <label>Dirección</label>
                    <InputBase 
                      v-model="personaNueva.PER_DIRECCION" 
                      placeholder="Calle Los Pinos #123" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Región</label>
                    <BaseSelect 
                      v-model="personaNueva.REG_ID" 
                      :options="regionOptions"
                      :disabled="guardandoPersona"
                      @change="() => cargarProvinciasPorRegion('nueva')"
                    />
                  </div>

                  <div class="form-field">
                    <label>Provincia</label>
                    <BaseSelect 
                      v-model="personaNueva.PRO_ID" 
                      :options="provinciaOptions"
                      :disabled="guardandoPersona || !personaNueva.REG_ID"
                      @change="() => cargarComunasPorProvincia('nueva')"
                    />
                  </div>

                  <div class="form-field">
                    <label>Comuna</label>
                    <BaseSelect 
                      v-model="personaNueva.COM_ID" 
                      :options="comunaOptions"
                      :disabled="guardandoPersona || !personaNueva.PRO_ID"
                    />
                  </div>
                </div>
              </div>

              <!-- Información de Emergencia -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="alert" :size="18" />
                  Información de Emergencia
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Contacto Emergencia</label>
                    <InputBase 
                      v-model="personaNueva.PER_NOM_EMERGENCIA" 
                      placeholder="María González" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Tel. Emergencia</label>
                    <div class="phone-input-wrapper">
                      <span class="phone-prefix">+56</span>
                      <InputBase 
                        v-model="personaNueva.PER_FONO_EMERGENCIA" 
                        placeholder="912345678" 
                        :disabled="guardandoPersona"
                        class="phone-input"
                      />
                    </div>
                  </div>

                  <div class="form-field full-width">
                    <label>Alergias / Enfermedades</label>
                    <InputBase 
                      v-model="personaNueva.PER_ALERGIA_ENFERMEDAD" 
                      placeholder="Ninguna conocida" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field full-width">
                    <label>Limitación</label>
                    <InputBase 
                      v-model="personaNueva.PER_LIMITACION" 
                      placeholder="Ninguna" 
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>

              <!-- Información -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="badge" :size="18" />
                  Información
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Rol</label>
                    <BaseSelect 
                      v-model="personaNueva.PER_ROL" 
                      :options="roleOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Rama</label>
                    <BaseSelect 
                      v-model="personaNueva.PER_RAMA" 
                      :options="ramaOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Profesión</label>
                    <InputBase 
                      v-model="personaNueva.PER_PROFESION" 
                      placeholder="Ej: Ingeniero" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Número MMA</label>
                    <InputBase 
                      v-model="personaNueva.PER_NUM_MMA" 
                      placeholder="Ej: 12345" 
                      type="number"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Tiempo NNAJ</label>
                    <InputBase 
                      v-model="personaNueva.PER_TIEMPO_NNAJ" 
                      placeholder="Ej: 3 años" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Tiempo Adulto</label>
                    <InputBase 
                      v-model="personaNueva.PER_TIEMPO_ADULTO" 
                      placeholder="Ej: 5 años" 
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Botón de cancelar al final del formulario -->
              <div class="form-actions-bottom">
                <BaseButton 
                  type="button" 
                  variant="secondary" 
                  class="btn-cancelar-grande"
                  @click="cerrarModalCrear"
                  :disabled="guardandoPersona"
                >
                  <AppIcons name="x" :size="16" /> Cancelar
                </BaseButton>
              </div>
            </form>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Importar Excel -->
      <BaseModal v-model="importarModalVisible" @close="cerrarModalImportar" class="persona-modal modal-importar-mejorado">
        <template #default>
          <div class="modal-importar">
            <!-- Header mejorado -->
            <header class="modal-header-importar">
              <div class="header-title">
                <h2>Importar Personas desde Excel</h2>
                <p class="subtitle">Carga personas masivamente usando un archivo Excel</p>
              </div>
              <div class="header-actions">
                <BaseButton 
                  class="btn-import-header" 
                  type="button" 
                  variant="success" 
                  @click="importarPersonasExcel"
                  :disabled="!archivoSeleccionado || importandoPersonas"
                >
                  <AppIcons :name="importandoPersonas ? 'clock' : 'download'" :size="16" />
                  {{ importandoPersonas ? 'Importando...' : 'Importar Personas' }}
                </BaseButton>
              </div>
            </header>

            <div class="modal-form-importar">
              <!-- Instrucciones -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="info" :size="18" />
                  Instrucciones de Uso
                </h3>
                <div class="import-instructions">
                  <ul>
                    <li>Descarga la plantilla Excel para tener el formato correcto</li>
                    <li>El archivo debe ser formato Excel (.xlsx o .xls)</li>
                    <li>La primera fila debe contener los encabezados</li>
                    <li>Columnas requeridas: <strong>Nombres, Apellido Paterno, RUT, DV, Email</strong></li>
                    <li><strong>Tipo de Teléfono:</strong> Escribe "Celular" o "Fijo"</li>
                    <li><strong>Estado Civil:</strong> Escribe "Soltero", "Casado", "Divorciado" o "Viudo"</li>
                    <li><strong>Vigente:</strong> Escribe "Sí" o "No"</li>
                    <li>Completa los datos y sube el archivo</li>
                  </ul>
                  
                  <!-- Botón para descargar plantilla -->
                  <div class="template-download">
                    <BaseButton 
                      @click="descargarPlantillaExcel"
                      variant="info"
                      class="btn-template"
                    >
                      <AppIcons name="download" :size="16" /> Descargar Plantilla Excel
                    </BaseButton>
                  </div>
                </div>
              </div>

              <!-- Selector de archivo -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="upload" :size="18" />
                  Seleccionar Archivo
                </h3>
                <div class="file-selector">
                  <input 
                    ref="excelInput"
                    type="file" 
                    accept=".xlsx,.xls"
                    style="display: none"
                  />
                  <BaseButton 
                    @click.stop.prevent="abrirSelectorExcel" 
                    variant="primary"
                    class="btn-select-file"
                    :disabled="importandoPersonas"
                  >
                    <AppIcons name="file" :size="16" /> Seleccionar Archivo Excel
                  </BaseButton>
                  <span v-if="archivoSeleccionado" class="file-name">
                    <AppIcons name="check" :size="16" style="color: #22c55e;" />
                    {{ archivoSeleccionado.name }}
                  </span>
                </div>
              </div>

              <!-- Vista previa de datos -->
              <div v-if="datosVistaPreviaExcel.length > 0" class="form-section">
                <h3 class="section-title">
                  <AppIcons name="table" :size="18" />
                  Vista Previa (primeras 5 filas)
                </h3>
                <div class="preview-section">
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
              </div>

              <!-- Botón cancelar al final -->
              <div class="form-actions-bottom">
                <BaseButton 
                  @click="cerrarModalImportar"
                  variant="secondary"
                  class="btn-cancelar-grande"
                  :disabled="importandoPersonas"
                >
                  <AppIcons name="x" :size="16" /> Cancelar
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
import AppIcons from '@/components/icons/AppIcons.vue'
import personasService from '@/services/personasService.js'
import mantenedoresService from '@/services/mantenedoresService.js'
import authService from '@/services/authService.js'
import * as XLSX from 'xlsx'
import { usePermissions } from '@/composables/usePermissions'

export default {
  name: 'GestionPersonas',
  components: { InputBase, BaseSelect, BaseButton, BaseAlert, BaseModal, AppIcons },
  setup() {
    const { isAdmin, canCreate, canEdit, canDelete, isReadOnly } = usePermissions()
    return {
      isAdmin,
      canCreate,
      canEdit,
      canDelete,
      isReadOnly
    }
  },
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
      estadoCivilOptions: [
        { value: '', label: 'Seleccione Estado Civil' }
      ],
      regionOptions: [
        { value: '', label: 'Seleccione Región' }
      ],
      provinciaOptions: [],
      comunaOptions: [],
      provinciaOptionsEditar: [],
      comunaOptionsEditar: [],
  personaSeleccionada: null,
  editModalVisible: false,
  personaEditada: null,
  modalTab: 'info',
  modoSoloLectura: false,
  confirmModalVisible: false,
  mensajeConfirmacion: '',
  confirmModalAnularVisible: false,
  personaAAnular: null,
  
  crearModalVisible: false,
  personaNueva: null,
  guardandoPersona: false,
  
  importarModalVisible: false,
  importandoPersonas: false,
  seleccionandoArchivo: false,
  archivoSeleccionado: null,
  datosVistaPreviaExcel: [],
  encabezadosExcel: [],
  
  esAdministrador: true,
  
    filtroAplicado: false,
    filteredPersonas: [],
    filtrandoEnProceso: false,
    cargandoPersonas: false,
    errorCarga: null,
    personas: []
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
    personasFiltradas() {
      return this.filteredPersonas.length > 0 ? this.filteredPersonas : this.personas;
    }
  },
  methods: {
    seleccionar(persona) {
      this.abrirModal(persona);
    },
    async abrirModalPersona(persona, soloLectura = false) {
      this.personaEditada = JSON.parse(JSON.stringify(persona || {}));
      
      if (this.personaEditada.PER_FONO) {
        this.personaEditada.PER_FONO = String(this.personaEditada.PER_FONO).replace(/^\+56/, '');
      }
      if (this.personaEditada.PER_FONO_EMERGENCIA) {
        this.personaEditada.PER_FONO_EMERGENCIA = String(this.personaEditada.PER_FONO_EMERGENCIA).replace(/^\+56/, '');
      }
      
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      this.newHistEntry = { fecha: '', descripcion: '' };
      this.modalTab = 'info';
      this.modoSoloLectura = soloLectura;
      this.editModalVisible = true;
      this.personaSeleccionada = persona;
      this.pendingSave = false;
      
      if (this.personaEditada.COM_ID && (!this.personaEditada.REG_ID || !this.personaEditada.PRO_ID)) {
        try {
          const comunas = await mantenedoresService.comuna.list();
          const comunaActual = comunas.find(c => c.COM_ID === this.personaEditada.COM_ID);
          if (comunaActual) {
            this.personaEditada.PRO_ID = comunaActual.PRO_ID;
            
            const provincias = await mantenedoresService.provincia.list();
            const provinciaActual = provincias.find(p => p.PRO_ID === comunaActual.PRO_ID);
            if (provinciaActual) {
              this.personaEditada.REG_ID = provinciaActual.REG_ID;
            }
          }
        } catch (error) {
          console.error('Error derivando región/provincia de comuna:', error);
        }
      }
      
      if (this.personaEditada.REG_ID) {
        await this.cargarProvinciasPorRegionEditar();
      }
      if (this.personaEditada.PRO_ID) {
        await this.cargarComunasPorProvinciaEditar();
      }
    },

    abrirModal(persona) {
      return this.abrirModalPersona(persona, false);
    },
    
    abrirModalVer(persona) {
      return this.abrirModalPersona(persona, true);
    },
    
    abrirModalEditar(persona) {
      return this.abrirModalPersona(persona, false);
    },
    cancelarEdicion() {
      this.editModalVisible = false;
      this.personaEditada = null;
      this.personaSeleccionada = null;
      this.pendingSave = false;
    },
    cerrarDetalle() {
      this.personaSeleccionada = null;
    },
    filtrar() {
      if (this.filtrandoEnProceso) {
        return;
      }
      this.filtrandoEnProceso = true;
      
      setTimeout(() => {
        this.ejecutarFiltrado();
        this.filtrandoEnProceso = false;
      }, 10);
    },
    ejecutarFiltrado() {
      const q = (this.searchQuery || '').toLowerCase().trim();
      const selectedRoleNorm = (this.selectedRole || '').toString().trim();
      const selectedRamaNorm = (this.selectedRama || '').toString().trim();
      const selectedCourseNorm = (this.selectedCourse || '').toString().trim();

      const tieneAlgunFiltro = q || selectedRoleNorm || selectedRamaNorm || selectedCourseNorm;
      
      if (!tieneAlgunFiltro) {
        alert('Debe usar al menos un filtro para buscar (nombre/RUT/email, rol, rama o grupo).');
        return;
      }

      this.filtroAplicado = true;
      this.personaSeleccionada = null;

      console.log('🔍 Aplicando filtros:', {
        busqueda: q,
        rol: selectedRoleNorm,
        rama: selectedRamaNorm,
        grupo: selectedCourseNorm
      });
      console.log('📊 Total personas disponibles:', this.personas.length);

      this.filteredPersonas = this.personas.filter((p) => {
        const nombre = (p.PER_NOMBRES || '').toLowerCase();
        const apellidoPat = (p.PER_APELPTA || '').toLowerCase();
        const apellidoMat = (p.PER_APELMAT || '').toLowerCase();
        const nombreCompleto = `${nombre} ${apellidoPat} ${apellidoMat}`.toLowerCase();
        const rut = (p.PER_RUN || '').toString().toLowerCase();
        const email = (p.PER_MAIL || '').toLowerCase();

        const coincideBusqueda = !q || nombreCompleto.includes(q) || rut.includes(q) || email.includes(q);

        const pRol = (p.PER_ROL || '').toString().trim();
        const pRama = (p.PER_RAMA || '').toString().trim();
        const pGrupo = (p.PER_GRUPO || '').toString().trim();

        const coincideRol = !selectedRoleNorm || pRol === selectedRoleNorm;
        const coincideRama = !selectedRamaNorm || pRama === selectedRamaNorm;
        const coincideGrupo = !selectedCourseNorm || pGrupo === selectedCourseNorm;

        return coincideBusqueda && coincideRol && coincideRama && coincideGrupo;
      });
      
      console.log('✅ Personas filtradas:', this.filteredPersonas.length);

      this.$nextTick(() => {
        const el = document.querySelector('.table-wrapper');
        if (el && typeof el.scrollIntoView === 'function') el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    },
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
        'ID': p.PER_ID || '',
        'Nombres': p.PER_NOMBRES || '',
        'Apellido Paterno': p.PER_APELPTA || '',
        'Apellido Materno': p.PER_APELMAT || '',
        'RUT': p.PER_RUN || '',
        'DV': p.PER_DV || '',
        'Email': p.PER_MAIL || '',
        'Fecha de Nacimiento': p.PER_FECHA_NAC || '',
        'Dirección': p.PER_DIRECCION || '',
        'Tipo de Teléfono': p.PER_TIPO_FONO || '',
        'Teléfono': p.PER_FONO || '',
        'Celular': p.PER_CEL || '',
        'Apodo': p.PER_APODO || '',
        'Profesión': p.PER_PROFESION || '',
        'Nombre de Emergencia': p.PER_NOM_EMERGENCIA || '',
        'Teléfono de Emergencia': p.PER_FONO_EMERGENCIA || '',
        'Alergia o Enfermedad': p.PER_ALERGIA_ENFERMEDAD || '',
        'Limitación': p.PER_LIMITACION || '',
        'Religión': p.PER_RELIGION || '',
        'Tiempo NNAJ': p.PER_TIEMPO_NNAJ || '',
        'Tiempo Adulto': p.PER_TIEMPO_ADULTO || '',
        'Número MMA': p.PER_NUM_MMA || '',
        'Otros': p.PER_OTROS || '',
        'Rol': p.PER_ROL || '',
        'Rama': p.PER_RAMA || '',
        'Grupo': p.PER_GRUPO || '',
        'Estado Civil (ID)': p.ESC_ID || 1,
        'Comuna (ID)': p.COM_ID || 1,
        'Vigente': p.PER_VIGENTE !== undefined ? (p.PER_VIGENTE ? 'Sí' : 'No') : 'Sí'
      }));

      const ws = XLSX.utils.json_to_sheet(datos);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Personas');
      
      const fecha = new Date().toISOString().split('T')[0];
      XLSX.writeFile(wb, `Personas_${fecha}.xlsx`);
    }
    ,
    guardarEdicion() {
      if (!this.personaEditada || !this.personaEditada.PER_RUN || !this.personaEditada.PER_NOMBRES) {
        alert('Nombre y RUT son obligatorios');
        return;
      }

      if (!this.personaEditada.PER_DV && this.personaEditada.PER_RUN) {
        alert('El dígito verificador del RUT es obligatorio');
        return;
      }

      if (this.personaEditada.PER_RUN && this.personaEditada.PER_DV) {
        if (!this.validarRutChileno(this.personaEditada.PER_RUN, this.personaEditada.PER_DV)) {
          alert('El RUT ingresado no es válido');
          return;
        }
      }

      this.mensajeConfirmacion = `¿Seguro que quieres guardar estos cambios para ${this.personaEditada.PER_NOMBRES} ${this.personaEditada.PER_APELPTA}?`;
      this.confirmModalVisible = true;
    },
    
    async confirmarGuardado() {
      if (this.guardandoPersona) {
        console.log('⚠️ Ya se está guardando, ignorando solicitud duplicada');
        return;
      }
      
      try {
        this.confirmModalVisible = false;
        this.guardandoPersona = true;
        
        if (!this.personaEditada) {
          alert('No hay datos para guardar');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaEditada.PER_ID) {
          alert('Error: No se encontró el ID de la persona');
          console.error('❌ Persona sin ID:', this.personaEditada);
          this.guardandoPersona = false;
          return;
        }
        
        console.log('💾 Guardando cambios en persona:', this.personaEditada);
        console.log('📝 ID de persona:', this.personaEditada.PER_ID);
        
        if (!this.personaEditada.PER_NOMBRES) {
          alert('El nombre es obligatorio');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaEditada.PER_RUN) {
          alert('El RUT es obligatorio');
          this.guardandoPersona = false;
          return;
        }

        if (!this.personaEditada.PER_DV) {
          alert('El dígito verificador del RUT es obligatorio');
          this.guardandoPersona = false;
          return;
        }

        if (this.personaEditada.PER_MAIL && !this.validarEmail(this.personaEditada.PER_MAIL)) {
          alert('El formato del email no es válido');
          this.guardandoPersona = false;
          return;
        }
        
        const datosActualizados = {
          PER_NOMBRES: this.personaEditada.PER_NOMBRES,
          PER_APELPTA: this.personaEditada.PER_APELPTA || '',
          PER_APELMAT: this.personaEditada.PER_APELMAT || '',
          PER_RUN: this.personaEditada.PER_RUN,
          PER_DV: this.personaEditada.PER_DV,
          PER_MAIL: this.personaEditada.PER_MAIL || '',
          PER_FECHA_NAC: this.personaEditada.PER_FECHA_NAC || null,
          PER_DIRECCION: this.personaEditada.PER_DIRECCION || null,
          PER_TIPO_FONO: this.personaEditada.PER_TIPO_FONO || 2,
          PER_FONO: this.personaEditada.PER_FONO ? '+56' + this.personaEditada.PER_FONO.replace(/^\+56/, '') : null,
          PER_APODO: this.personaEditada.PER_APODO || null,
          PER_PROFESION: this.personaEditada.PER_PROFESION || null,
          PER_NOM_EMERGENCIA: this.personaEditada.PER_NOM_EMERGENCIA || null,
          PER_FONO_EMERGENCIA: this.personaEditada.PER_FONO_EMERGENCIA ? '+56' + this.personaEditada.PER_FONO_EMERGENCIA.replace(/^\+56/, '') : null,
          PER_ALERGIA_ENFERMEDAD: this.personaEditada.PER_ALERGIA_ENFERMEDAD || null,
          PER_LIMITACION: this.personaEditada.PER_LIMITACION || null,
          PER_RELIGION: this.personaEditada.PER_RELIGION || null,
          PER_TIEMPO_NNAJ: this.personaEditada.PER_TIEMPO_NNAJ || null,
          PER_TIEMPO_ADULTO: this.personaEditada.PER_TIEMPO_ADULTO || null,
          PER_NUM_MMA: this.personaEditada.PER_NUM_MMA || null,
          PER_OTROS: this.personaEditada.PER_OTROS || null,
          PER_FOTO: this.personaEditada.foto || null,
          ESC_ID: this.personaEditada.ESC_ID && this.personaEditada.ESC_ID !== '' ? Number(this.personaEditada.ESC_ID) : 1,
          COM_ID: this.personaEditada.COM_ID && this.personaEditada.COM_ID !== '' ? Number(this.personaEditada.COM_ID) : 1,
          PER_VIGENTE: this.personaEditada.PER_VIGENTE !== undefined ? this.personaEditada.PER_VIGENTE : true
        };
        
        console.log('📤 Datos a enviar:', datosActualizados);
        console.log('🌐 URL de actualización: personas/personas/' + this.personaEditada.PER_ID + '/');
        
        const personaActualizada = await personasService.personas.partialUpdate(
          this.personaEditada.PER_ID, 
          datosActualizados
        );
        
        console.log('✅ Persona actualizada:', personaActualizada);
        
        const personaId = this.personaEditada.PER_ID;
        
        if (this.personaEditada.PER_RAMA && this.personaEditada.PER_RAMA !== '') {
          try {
            const nivelesActuales = await personasService.niveles.list();
            const nivelPersona = nivelesActuales.find(n => n.PER_ID === personaId);
            
            const ramaData = await mantenedoresService.rama.list();
            const ramaEncontrada = ramaData.find(r => r.RAM_DESCRIPCION === this.personaEditada.PER_RAMA);
            
            if (ramaEncontrada) {
              if (nivelPersona) {
                await personasService.niveles.partialUpdate(nivelPersona.PEN_ID, {
                  RAM_ID: ramaEncontrada.RAM_ID
                });
                console.log('✅ Rama actualizada:', this.personaEditada.PER_RAMA);
              } else {
                await personasService.niveles.create({
                  PER_ID: personaId,
                  RAM_ID: ramaEncontrada.RAM_ID,
                  NIV_ID: 1
                });
                console.log('✅ Rama asignada:', this.personaEditada.PER_RAMA);
              }
            }
          } catch (error) {
            console.warn('⚠️ No se pudo actualizar la rama:', error);
            console.error('Error completo:', error);
          }
        }
        
        if (this.personaEditada.PER_ROL && this.personaEditada.PER_ROL !== '') {
          try {
            const formadoresActuales = await personasService.formadores.list();
            const esFormador = formadoresActuales.find(f => f.PER_ID === personaId);
            
            if (!esFormador) {
              await personasService.formadores.create({
                PER_ID: personaId
              });
              console.log('✅ Registrado como formador');
            } else {
              console.log('✅ Ya estaba registrado como formador');
            }
          } catch (error) {
            console.warn('⚠️ No se pudo actualizar el rol:', error);
            console.error('Error completo:', error);
          }
        }
        
        console.log('🔄 Recargando lista de personas...');
        await this.cargarPersonas();
        
        if (this.filtroAplicado) {
          console.log('🔍 Reaplicando filtros...');
          await this.filtrar();
        }
        
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
        
        let detallesError = '';
        if (error.response) {
          if (typeof error.response === 'object') {
            detallesError = '\n\nDetalles del servidor:\n' + JSON.stringify(error.response, null, 2);
          } else {
            detallesError = '\n\nDetalles del servidor:\n' + error.response;
          }
        }
        
        let mensajeError = 'Error al actualizar la persona. ';
        
        if (error.status === 400) {
          mensajeError += 'Datos inválidos. Verifica que todos los campos estén correctos.' + detallesError;
          console.error('🔍 Datos que se intentaron enviar:', datosActualizados);
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
      this.confirmModalVisible = false;
    },
    
    anularPersona(persona) {
      this.personaAAnular = persona;
      this.confirmModalAnularVisible = true;
    },
    
    cancelarAnulacion() {
      this.confirmModalAnularVisible = false;
      this.personaAAnular = null;
    },
    
    async confirmarAnulacion() {
      if (!this.personaAAnular) return;
      
      console.log('🔵 INICIO confirmarAnulacion - Timestamp:', Date.now());
      
      try {
        console.log('🔄 Anulando persona en BD:', this.personaAAnular.PER_NOMBRES);
        console.log('📋 ID de persona:', this.personaAAnular.PER_ID);
        
        const datosAnulacion = {
          PER_VIGENTE: false
        };
        
        console.log('📝 Datos a enviar:', datosAnulacion);
        
        const resultado = await personasService.personas.partialUpdate(this.personaAAnular.PER_ID, datosAnulacion);
        
        console.log('✅ Persona anulada en BD:', resultado);
        console.log('🟢 MOSTRANDO ALERT DE ÉXITO - Timestamp:', Date.now());
        
        alert('✅ Persona anulada correctamente en la base de datos');
        
        this.confirmModalAnularVisible = false;
        this.personaAAnular = null;
        
      } catch (error) {
        console.error('❌ Error al anular persona:', error);
        
        let mensajeError = 'Error al anular la persona. ';
        if (error.message) {
          mensajeError += error.message;
        }
        alert('❌ ' + mensajeError);
        return;
      }
      
      try {
        console.log('🔄 Recargando lista de personas...');
        await this.cargarPersonas();
        
        if (this.filtroAplicado) {
          console.log('🔍 Reaplicando filtros...');
          await this.filtrar();
        }
      } catch (error) {
        console.warn('⚠️ Error al recargar datos:', error);
      }
      
      console.log('🔵 FIN confirmarAnulacion - Timestamp:', Date.now());
    },
    
    async reactivarPersona(persona) {
      if (!confirm(`¿Estás seguro de que deseas reactivar a ${persona.PER_NOMBRES} ${persona.PER_APELPTA}?`)) {
        return;
      }
      
      try {
        console.log('🔄 Reactivando persona en BD:', persona.PER_NOMBRES);
        
        const datosReactivacion = {
          PER_VIGENTE: true
        };
        
        const resultado = await personasService.personas.partialUpdate(persona.PER_ID, datosReactivacion);
        
        console.log('✅ Persona reactivada en BD:', resultado);
        
        alert('✅ Persona reactivada correctamente en la base de datos');
        
      } catch (error) {
        console.error('❌ Error al reactivar persona:', error);
        alert('❌ Error al reactivar la persona. Inténtalo de nuevo.');
        return;
      }
      
      try {
        console.log('🔄 Recargando lista de personas...');
        await this.cargarPersonas();
        
        if (this.filtroAplicado) {
          console.log('🔍 Reaplicando filtros...');
          await this.filtrar();
        }
      } catch (error) {
        console.warn('⚠️ Error al recargar datos:', error);
      }
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
    
    handleFileUpload(event, modo) {
      const file = event.target.files[0];
      if (!file) return;
      
      const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
      if (!allowedTypes.includes(file.type.toLowerCase())) {
        alert('Por favor selecciona solo imágenes en formato PNG o JPG.');
        event.target.value = '';
        return;
      }
      
      if (file.size > 5 * 1024 * 1024) {
        alert('El archivo es demasiado grande. Por favor selecciona una imagen menor a 5MB.');
        event.target.value = '';
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          
          const targetSize = 300;
          canvas.width = targetSize;
          canvas.height = targetSize;
          
          let sx, sy, sWidth, sHeight;
          
          if (img.width > img.height) {
            sHeight = img.height;
            sWidth = img.height;
            sx = (img.width - img.height) / 2;
            sy = 0;
          } else {
            sWidth = img.width;
            sHeight = img.width;
            sx = 0;
            sy = (img.height - img.width) / 2;
          }
          
          ctx.drawImage(img, sx, sy, sWidth, sHeight, 0, 0, targetSize, targetSize);
          
          const resizedBase64 = canvas.toDataURL('image/jpeg', 0.60);
          
          const finalSize = Math.round((resizedBase64.length * 3) / 4 / 1024); // KB
          console.log(`📸 Foto redimensionada: ${finalSize}KB (original: ${Math.round(file.size / 1024)}KB)`);
          
          if (modo === 'nueva') {
            this.personaNueva.foto = resizedBase64;
          } else {
            this.personaEditada.foto = resizedBase64;
          }
          
          event.target.value = '';
        };
        
        img.onerror = () => {
          alert('Error al procesar la imagen. Por favor intenta con otra imagen.');
          event.target.value = '';
        };
        
        img.src = e.target.result;
      };
      
      reader.onerror = () => {
        alert('Error al leer el archivo. Por favor intenta nuevamente.');
        event.target.value = '';
      };
      
      reader.readAsDataURL(file);
    },
    
    removePhoto(modo) {
      if (modo === 'nueva') {
        this.personaNueva.foto = null;
      } else {
        this.personaEditada.foto = null;
      }
    },
    
    handleImageError(modo) {
      if (modo === 'nueva') {
        this.personaNueva.foto = null;
      } else {
        this.personaEditada.foto = null;
      }
    },

    async cargarPersonas() {
      try {
        this.cargandoPersonas = true;
        this.errorCarga = null;
        
        console.log('🔄 Intentando cargar personas con relaciones desde API...');
        const response = await personasService.personasCompletas.list();
        console.log('📡 Respuesta de la API:', response);
        
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
        console.log('Cargando opciones de filtros desde Base de Datos...');
        
        let rolesMantenedor = [];
        let ramasMantenedor = [];
        let gruposMantenedor = [];
        
        try {
          const rolesData = await mantenedoresService.rol.list();
          rolesMantenedor = rolesData
            .filter(rol => rol.ROL_VIGENTE !== false)
            .map(rol => ({ value: rol.ROL_DESCRIPCION, label: rol.ROL_DESCRIPCION, id: rol.ROL_ID }));
          console.log('Roles de mantenedores:', rolesMantenedor.length);
        } catch (error) {
          console.warn('No se pudieron cargar roles desde mantenedores:', error.message);
        }
        
        try {
          const ramasData = await mantenedoresService.rama.list();
          ramasMantenedor = ramasData
            .filter(rama => rama.RAM_VIGENTE !== false)
            .map(rama => ({ value: rama.RAM_DESCRIPCION, label: rama.RAM_DESCRIPCION, id: rama.RAM_ID }));
          console.log('Ramas de mantenedores:', ramasMantenedor.length);
        } catch (error) {
          console.warn('No se pudieron cargar ramas desde mantenedores:', error.message);
        }
        
        try {
          const gruposData = await mantenedoresService.grupo.list();
          gruposMantenedor = gruposData
            .filter(grupo => grupo.GRU_VIGENTE !== false)
            .map(grupo => ({ value: grupo.GRU_DESCRIPCION, label: grupo.GRU_DESCRIPCION, id: grupo.GRU_ID }));
          console.log('Grupos de mantenedores:', gruposMantenedor.length);
        } catch (error) {
          console.warn('No se pudieron cargar grupos desde mantenedores:', error.message);
        }
        
        const rolesPersonas = await personasService.obtenerRoles();
        const ramasPersonas = await personasService.obtenerRamas();
        const gruposPersonas = await personasService.obtenerGrupos();
        console.log('Valores de personas - Roles:', rolesPersonas.length, 'Ramas:', ramasPersonas.length, 'Grupos:', gruposPersonas.length);
        
        const combinarOpciones = (mantenedor, personas) => {
          const mapa = new Map();
          [...mantenedor, ...personas].forEach(item => {
            if (item.value) mapa.set(item.value, item);
          });
          return Array.from(mapa.values()).sort((a, b) => a.label.localeCompare(b.label));
        };
        
        this.roleOptions = [{ value: '', label: 'Todos los roles' }, ...combinarOpciones(rolesMantenedor, rolesPersonas)];
        this.ramaOptions = [{ value: '', label: 'Todas las ramas' }, ...combinarOpciones(ramasMantenedor, ramasPersonas)];
        this.courseOptions = [{ value: '', label: 'Todos los grupos' }, ...combinarOpciones(gruposMantenedor, gruposPersonas)];
        
        try {
          const estadosCiviles = await mantenedoresService.estadoCivil.list();
          this.estadoCivilOptions = [
            { value: '', label: 'Seleccione Estado Civil' },
            ...estadosCiviles
              .filter(ec => ec.ESC_VIGENTE !== false)
              .map(ec => ({ value: ec.ESC_ID, label: ec.ESC_DESCRIPCION }))
          ];
          console.log('Estados Civiles cargados:', this.estadoCivilOptions.length - 1);
        } catch (error) {
          console.warn('No se pudieron cargar estados civiles:', error.message);
        }
        
        try {
          const regiones = await mantenedoresService.region.list();
          this.regionOptions = [
            { value: '', label: 'Seleccione Región' },
            ...regiones
              .filter(reg => reg.REG_VIGENTE !== false)
              .map(reg => ({ value: reg.REG_ID, label: reg.REG_DESCRIPCION }))
          ];
          console.log('Regiones cargadas:', this.regionOptions.length - 1);
        } catch (error) {
          console.warn('No se pudieron cargar regiones:', error.message);
        }
        
        console.log('Filtros cargados: Roles:', this.roleOptions.length - 1, 'Ramas:', this.ramaOptions.length - 1, 'Grupos:', this.courseOptions.length - 1);
        
      } catch (error) {
        console.error('Error cargando opciones de filtros:', error);
        this.roleOptions = [{ value: '', label: 'Todos los roles' }];
        this.ramaOptions = [{ value: '', label: 'Todas las ramas' }];
        this.courseOptions = [{ value: '', label: 'Todos los grupos' }];
        console.log('No se pudieron cargar filtros. Filtros vacíos aplicados.');
      }
    },

    async cargarProvinciasPorRegion(modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      const optionsKey = modo === 'nueva' ? 'provinciaOptions' : 'provinciaOptionsEditar';
      const comunasKey = modo === 'nueva' ? 'comunaOptions' : 'comunaOptionsEditar';
      
      if (!persona.REG_ID) {
        this[optionsKey] = [];
        this[comunasKey] = [];
        persona.PRO_ID = '';
        persona.COM_ID = '';
        return;
      }
      
      try {
        console.log(`🔍 [${modo}] Cargando provincias para región:`, persona.REG_ID);
        const provincias = await mantenedoresService.provincia.list();
        const regionIdSeleccionada = Number(persona.REG_ID);
        
        this[optionsKey] = provincias
          .filter(prov => Number(prov.REG_ID) === regionIdSeleccionada && prov.PRO_VIGENTE !== false)
          .map(prov => ({ value: prov.PRO_ID, label: prov.PRO_DESCRIPCION }));
        
        console.log(`✅ [${modo}] Provincias filtradas:`, this[optionsKey].length);
        
        if (modo === 'editar' && persona.PRO_ID) {
          const provinciaExiste = this[optionsKey].some(p => p.value === persona.PRO_ID);
          if (!provinciaExiste) {
            persona.PRO_ID = '';
            persona.COM_ID = '';
            this[comunasKey] = [];
          }
        } else {
          persona.PRO_ID = '';
          persona.COM_ID = '';
          this[comunasKey] = [];
        }
      } catch (error) {
        console.error('Error cargando provincias:', error);
      }
    },

    async cargarComunasPorProvincia(modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      const optionsKey = modo === 'nueva' ? 'comunaOptions' : 'comunaOptionsEditar';
      
      if (!persona.PRO_ID) {
        this[optionsKey] = [];
        persona.COM_ID = '';
        return;
      }
      
      try {
        console.log(`🔍 [${modo}] Cargando comunas para provincia:`, persona.PRO_ID);
        const comunas = await mantenedoresService.comuna.list();
        const provinciaIdSeleccionada = Number(persona.PRO_ID);
        
        this[optionsKey] = comunas
          .filter(com => Number(com.PRO_ID) === provinciaIdSeleccionada && com.COM_VIGENTE !== false)
          .map(com => ({ value: com.COM_ID, label: com.COM_DESCRIPCION }));
        
        console.log(`✅ [${modo}] Comunas filtradas:`, this[optionsKey].length);
        
        if (modo === 'editar' && persona.COM_ID) {
          const comunaExiste = this[optionsKey].some(c => c.value === persona.COM_ID);
          if (!comunaExiste) {
            persona.COM_ID = '';
          }
        } else {
          persona.COM_ID = '';
        }
      } catch (error) {
        console.error('Error cargando comunas:', error);
      }
    },

    cargarProvinciasPorRegionEditar() {
      return this.cargarProvinciasPorRegion('editar');
    },

    cargarComunasPorProvinciaEditar() {
      return this.cargarComunasPorProvincia('editar');
    },

    abrirModalCrear() {
      this.personaNueva = {
        foto: null,
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
        PER_NOM_EMERGENCIA: '',
        PER_FONO_EMERGENCIA: '',
        PER_ALERGIA_ENFERMEDAD: '',
        PER_LIMITACION: '',
        PER_RELIGION: '',
        PER_TIEMPO_NNAJ: '',
        PER_TIEMPO_ADULTO: '',
        PER_NUM_MMA: null,
        PER_OTROS: '',
        ESC_ID: '',
        REG_ID: '',
        PRO_ID: '',
        COM_ID: '',
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

    abrirSelectorExcel() {
      if (this.seleccionandoArchivo) {
        console.log('⚠️ Ya hay un selector abierto, ignorando');
        return;
      }
      
      this.seleccionandoArchivo = true;
      const input = this.$refs.excelInput;
      
      if (!input) {
        this.seleccionandoArchivo = false;
        return;
      }
      
      // Limpiar cualquier listener previo
      input.onchange = null;
      
      // Asignar el handler directamente
      input.onchange = (event) => {
        this.handleFileSelect(event);
        this.seleccionandoArchivo = false;
      };
      
      // Abrir el selector
      input.click();
    },

    handleFileSelect(event) {
      const archivo = event.target.files[0];
      console.log('📁 handleFileSelect ejecutado, archivo:', archivo?.name || 'ninguno');
      
      if (!archivo) {
        return;
      }

      this.archivoSeleccionado = archivo;
      this.procesarArchivoExcel(archivo);
    },

    descargarPlantillaExcel() {
      const plantilla = [{
        'ID': '',
        'Nombres': '',
        'Apellido Paterno': '',
        'Apellido Materno': '',
        'RUT': '',
        'DV': '',
        'Email': '',
        'Fecha de Nacimiento': '',
        'Dirección': '',
        'Tipo de Teléfono': 'Celular o Fijo',
        'Teléfono': '',
        'Celular': '',
        'Apodo': '',
        'Profesión': '',
        'Nombre de Emergencia': '',
        'Teléfono de Emergencia': '',
        'Alergia o Enfermedad': '',
        'Limitación': '',
        'Religión': '',
        'Tiempo NNAJ': '',
        'Tiempo Adulto': '',
        'Número MMA': '',
        'Otros': '',
        'Rol': '',
        'Rama': '',
        'Grupo': '',
        'Estado Civil': 'Soltero, Casado, Divorciado, Viudo, etc.',
        'Comuna': 'Nombre de la comuna',
        'Vigente': 'Sí o No'
      }];

      const ws = XLSX.utils.json_to_sheet(plantilla);
      
      const colWidths = [
        { wch: 8 },  // ID
        { wch: 20 }, // Nombres
        { wch: 20 }, // Apellido Paterno
        { wch: 20 }, // Apellido Materno
        { wch: 12 }, // RUT
        { wch: 5 },  // DV
        { wch: 25 }, // Email
        { wch: 15 }, // Fecha de Nacimiento
        { wch: 30 }, // Dirección
        { wch: 18 }, // Tipo de Teléfono
        { wch: 15 }, // Teléfono
        { wch: 15 }, // Celular
        { wch: 15 }, // Apodo
        { wch: 20 }, // Profesión
        { wch: 25 }, // Nombre de Emergencia
        { wch: 20 }, // Teléfono de Emergencia
        { wch: 25 }, // Alergia o Enfermedad
        { wch: 20 }, // Limitación
        { wch: 15 }, // Religión
        { wch: 15 }, // Tiempo NNAJ
        { wch: 15 }, // Tiempo Adulto
        { wch: 15 }, // Número MMA
        { wch: 25 }, // Otros
        { wch: 20 }, // Rol
        { wch: 15 }, // Rama
        { wch: 15 }, // Grupo
        { wch: 18 }, // Estado Civil (ID)
        { wch: 15 }, // Comuna (ID)
        { wch: 10 }  // Vigente
      ];
      ws['!cols'] = colWidths;
      
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Plantilla Personas');
      
      XLSX.writeFile(wb, 'Plantilla_Importar_Personas.xlsx');
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
        
        const reader = new FileReader();
        
        reader.onload = (e) => {
          try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            
            if (jsonData.length === 0) {
              alert('El archivo Excel está vacío');
              return;
            }
            
            this.encabezadosExcel = jsonData[0];
            
            const filasDatos = jsonData.slice(1);
            
            this.datosVistaPreviaExcel = filasDatos.map(fila => {
              const objeto = {};
              this.encabezadosExcel.forEach((encabezado, index) => {
                objeto[encabezado] = fila[index] || '';
              });
              return objeto;
            }).filter(objeto => {
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
            const nombres = fila['Nombres'] || fila['PER_NOMBRES'] || '';
            const apellidoPaterno = fila['Apellido Paterno'] || fila['PER_APELPTA'] || '';
            const apellidoMaterno = fila['Apellido Materno'] || fila['PER_APELMAT'] || '';
            const rut = fila['RUT'] || fila['PER_RUN'] || '';
            const dv = fila['DV'] || fila['PER_DV'] || '';
            const email = fila['Email'] || fila['PER_MAIL'] || '';
            
            console.log('📋 Procesando fila:', { nombres, apellidoPaterno, rut, dv, email });
            
            if (!nombres || !rut || !dv) {
              const error = `Fila con datos incompletos: ${nombres || 'Sin nombre'} - RUT: ${rut || 'Sin RUT'}`;
              console.warn('⚠️', error);
              errores.push(error);
              continue;
            }

            // Convertir tipo de teléfono a número
            let tipoTelefono = 2; // Por defecto Celular
            const tipoTelefonoTexto = (fila['Tipo de Teléfono'] || fila['PER_TIPO_FONO'] || '').toString().toLowerCase();
            if (tipoTelefonoTexto.includes('fijo') || tipoTelefonoTexto === '1') {
              tipoTelefono = 1;
            } else if (tipoTelefonoTexto.includes('celular') || tipoTelefonoTexto.includes('móvil') || tipoTelefonoTexto === '2') {
              tipoTelefono = 2;
            }

            // Convertir Estado Civil de texto a ID
            let estadoCivilId = 1; // Por defecto Soltero
            const estadoCivilTexto = (fila['Estado Civil'] || fila['Estado Civil (ID)'] || fila['ESC_ID'] || '').toString().toLowerCase();
            if (estadoCivilTexto.includes('casad') || estadoCivilTexto === '2') {
              estadoCivilId = 2;
            } else if (estadoCivilTexto.includes('divorciad') || estadoCivilTexto === '3') {
              estadoCivilId = 3;
            } else if (estadoCivilTexto.includes('viud') || estadoCivilTexto === '4') {
              estadoCivilId = 4;
            } else if (estadoCivilTexto.includes('solter') || estadoCivilTexto === '1') {
              estadoCivilId = 1;
            }
            
            console.log(`🔄 Conversiones - Tipo Fono: ${tipoTelefono}, Estado Civil: ${estadoCivilId} (de: "${estadoCivilTexto}")`);

            // Para Comuna, intentar buscar por nombre (simplificado - usar ID 1 por defecto)
            // En el futuro se podría hacer una búsqueda real en la base de datos
            let comunaId = 1;
            const comunaTexto = fila['Comuna'] || fila['Comuna (ID)'] || fila['COM_ID'] || '';
            if (comunaTexto && !isNaN(comunaTexto)) {
              comunaId = parseInt(comunaTexto);
            }

            // Convertir Vigente a booleano
            const vigenteTexto = (fila['Vigente'] || '').toString().toLowerCase();
            let vigente = true; // Por defecto activo
            if (vigenteTexto === 'no' || vigenteTexto === '0' || vigenteTexto === 'false' || vigenteTexto === 'inactivo') {
              vigente = false;
            }

            // Obtener usuario actual desde authService (soporta cookies y localStorage)
            const currentUser = await authService.getCurrentUser();
            const usuId = currentUser.id || 1;

            const datosPersona = {
              PER_NOMBRES: nombres,
              PER_APELPTA: apellidoPaterno,
              PER_APELMAT: apellidoMaterno,
              PER_RUN: rut,
              PER_DV: dv,
              PER_MAIL: email,
              PER_FECHA_NAC: fila['Fecha de Nacimiento'] || fila['PER_FECHA_NAC'] || null,
              PER_DIRECCION: fila['Dirección'] || fila['PER_DIRECCION'] || null,
              PER_TIPO_FONO: tipoTelefono,
              PER_FONO: fila['Teléfono'] || fila['PER_FONO'] || null,
              PER_CEL: fila['Celular'] || fila['PER_CEL'] || null,
              PER_APODO: fila['Apodo'] || fila['PER_APODO'] || null,
              PER_PROFESION: fila['Profesión'] || fila['PER_PROFESION'] || null,
              PER_NOM_EMERGENCIA: fila['Nombre de Emergencia'] || fila['PER_NOM_EMERGENCIA'] || null,
              PER_FONO_EMERGENCIA: fila['Teléfono de Emergencia'] || fila['PER_FONO_EMERGENCIA'] || null,
              PER_ALERGIA_ENFERMEDAD: fila['Alergia o Enfermedad'] || fila['PER_ALERGIA_ENFERMEDAD'] || null,
              PER_LIMITACION: fila['Limitación'] || fila['PER_LIMITACION'] || null,
              PER_RELIGION: fila['Religión'] || fila['PER_RELIGION'] || null,
              PER_TIEMPO_NNAJ: fila['Tiempo NNAJ'] || fila['PER_TIEMPO_NNAJ'] || null,
              PER_TIEMPO_ADULTO: fila['Tiempo Adulto'] || fila['PER_TIEMPO_ADULTO'] || null,
              PER_NUM_MMA: fila['Número MMA'] || fila['PER_NUM_MMA'] || null,
              PER_OTROS: fila['Otros'] || fila['PER_OTROS'] || null,
              PER_ROL: fila['Rol'] || fila['PER_ROL'] || null,
              PER_RAMA: fila['Rama'] || fila['PER_RAMA'] || null,
              PER_GRUPO: fila['Grupo'] || fila['PER_GRUPO'] || null,
              ESC_ID: estadoCivilId,
              COM_ID: comunaId,
              USU_ID: usuId,
              PER_VIGENTE: vigente
            };

            console.log('📤 Creando persona:', datosPersona);

            try {
              const response = await personasService.personas.create(datosPersona);
              personasImportadas++;
              console.log(`✅ Persona ${nombres} ${apellidoPaterno} importada exitosamente`, response);
            } catch (createError) {
              // Verificar si realmente falló o si es solo un código de estado inesperado
              // Códigos 200-299 se consideran éxito
              const status = createError.status || (createError.response && createError.response.status);
              
              if (status >= 200 && status < 300) {
                // Es un éxito, solo que el formato de respuesta fue inesperado
                personasImportadas++;
                console.log(`✅ Persona ${nombres} ${apellidoPaterno} creada exitosamente (código ${status})`);
              } else {
                // Es un error real
                throw createError;
              }
            }

          } catch (error) {
            console.error('❌ Error creando persona:', error);
            const nombreError = `${fila['Nombres'] || fila['PER_NOMBRES'] || 'Desconocido'} ${fila['Apellido Paterno'] || fila['PER_APELPTA'] || ''}`.trim();
            const rutError = fila['RUT'] || fila['PER_RUN'] || '';
            const dvError = fila['DV'] || fila['PER_DV'] || '';
            
            // Extraer el mensaje de error del servidor
            let mensajeError = 'Error desconocido';
            if (error.response && error.response.data) {
              if (error.response.data.message) {
                mensajeError = error.response.data.message;
              } else if (error.response.data.error) {
                mensajeError = error.response.data.error;
              } else if (typeof error.response.data === 'string') {
                mensajeError = error.response.data;
              }
            } else if (error.message) {
              mensajeError = error.message;
            }
            
            // Si es error de RUT duplicado, hacer más claro
            if (mensajeError.includes('PER_RUN') && mensajeError.includes('already exists')) {
              mensajeError = `RUT ${rutError}-${dvError} ya existe en la base de datos`;
            }
            
            errores.push(`${nombreError}: ${mensajeError}`);
          }
        }

        console.log(`📊 Resumen de importación: ${personasImportadas} exitosas, ${errores.length} errores`);

        await this.cargarPersonas();

        this.cerrarModalImportar();

        // Solo mostrar mensaje si hay personas importadas o errores
        if (personasImportadas > 0 || errores.length > 0) {
          let mensaje = '';
          
          if (personasImportadas > 0) {
            mensaje = `✅ Importación completada!\n\n`;
            mensaje += `✓ ${personasImportadas} persona${personasImportadas === 1 ? '' : 's'} importada${personasImportadas === 1 ? '' : 's'} exitosamente\n`;
          }
          
          if (errores.length > 0) {
            if (personasImportadas === 0) {
              mensaje = `❌ Importación fallida\n\n`;
            } else {
              mensaje += `\n`;
            }
            mensaje += `✗ ${errores.length} error${errores.length === 1 ? '' : 'es'} encontrado${errores.length === 1 ? '' : 's'}:\n\n`;
            mensaje += errores.slice(0, 5).join('\n');
            if (errores.length > 5) {
              mensaje += `\n... y ${errores.length - 5} error${errores.length - 5 === 1 ? '' : 'es'} más.`;
            }
          }
          
          alert(mensaje);
        }

      } catch (error) {
        console.error('❌ Error en importación:', error);
        alert('Error durante la importación. Verifica los datos e intenta nuevamente.');
      } finally {
        this.importandoPersonas = false;
      }
    },

    calcularDv(rut) {
      if (!rut) return '';
      
      const rutLimpio = rut.toString().replace(/\./g, '').replace(/-/g, '');
      const rutNumerico = parseInt(rutLimpio);
      
      if (isNaN(rutNumerico)) return '';
      
      let suma = 0;
      let multiplicador = 2;
      
      const rutString = rutNumerico.toString();
      for (let i = rutString.length - 1; i >= 0; i--) {
        suma += parseInt(rutString[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
      }
      
      const resto = suma % 11;
      let dvCalculado = 11 - resto;
      
      if (dvCalculado === 11) return '0';
      else if (dvCalculado === 10) return 'K';
      else return dvCalculado.toString();
    },

    calcularDvNueva() {
      if (this.personaNueva && this.personaNueva.PER_RUN) {
        this.personaNueva.PER_RUN = this.personaNueva.PER_RUN.replace(/[^0-9]/g, '');
        
        if (this.personaNueva.PER_RUN.length >= 7) {
          this.personaNueva.PER_DV = this.calcularDv(this.personaNueva.PER_RUN);
        }
      }
    },

    calcularDvEditada() {
      if (this.personaEditada && this.personaEditada.PER_RUN) {
        this.personaEditada.PER_RUN = this.personaEditada.PER_RUN.replace(/[^0-9]/g, '');
        
        if (this.personaEditada.PER_RUN.length >= 7) {
          this.personaEditada.PER_DV = this.calcularDv(this.personaEditada.PER_RUN);
        }
      }
    },

    validarRutChileno(rut, dv) {
      if (!rut || !dv) return false;
      
      const rutString = String(rut).replace(/\./g, '').replace(/[^0-9]/g, '');
      const rutNumerico = parseInt(rutString);
      if (isNaN(rutNumerico) || rutString === '') return false;
      
      let suma = 0;
      let multiplicador = 2;
      
      for (let i = rutString.length - 1; i >= 0; i--) {
        suma += parseInt(rutString[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
      }
      
      const resto = suma % 11;
      let dvCalculado = 11 - resto;
      
      if (dvCalculado === 11) dvCalculado = '0';
      else if (dvCalculado === 10) dvCalculado = 'K';
      else dvCalculado = dvCalculado.toString();
      
      console.log('🔍 Validación RUT:', rutString, '- DV ingresado:', String(dv).toUpperCase(), '- DV calculado:', dvCalculado, '- ¿Válido?', String(dv).toUpperCase() === dvCalculado);
      
      return String(dv).toUpperCase() === dvCalculado;
    },

    validarEmail(email) {
      if (!email) return true;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },

    async guardarPersonaNueva() {
      if (this.guardandoPersona) {
        console.log('⚠️ Ya se está guardando, ignorando click duplicado');
        return;
      }
      
      try {
        this.guardandoPersona = true;
        
        // Validaciones
        if (!this.personaNueva.PER_NOMBRES) {
          alert('El nombre es obligatorio');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaNueva.PER_APELPTA) {
          alert('El apellido paterno es obligatorio');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaNueva.PER_RUN || !this.personaNueva.PER_DV) {
          alert('El RUT es obligatorio');
          this.guardandoPersona = false;
          return;
        }
        
        console.log('📝 Validando RUT:', this.personaNueva.PER_RUN, 'DV:', this.personaNueva.PER_DV);
        console.log('📝 Tipo RUT:', typeof this.personaNueva.PER_RUN, 'Tipo DV:', typeof this.personaNueva.PER_DV);
        
        if (!this.validarRutChileno(this.personaNueva.PER_RUN, this.personaNueva.PER_DV)) {
          alert('El RUT ingresado no es válido');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaNueva.PER_MAIL) {
          alert('El email es obligatorio');
          this.guardandoPersona = false;
          return;
        }
        
        if (!this.personaNueva.PER_FECHA_NAC) {
          alert('La fecha de nacimiento es obligatoria');
          this.guardandoPersona = false;
          return;
        }
        
        const datosPersona = {
          PER_NOMBRES: this.personaNueva.PER_NOMBRES,
          PER_APELPTA: this.personaNueva.PER_APELPTA,
          PER_APELMAT: this.personaNueva.PER_APELMAT || '',
          PER_RUN: this.personaNueva.PER_RUN,
          PER_DV: this.personaNueva.PER_DV,
          PER_MAIL: this.personaNueva.PER_MAIL,
          PER_FECHA_NAC: this.personaNueva.PER_FECHA_NAC,
          PER_DIRECCION: this.personaNueva.PER_DIRECCION || null,
          PER_TIPO_FONO: this.personaNueva.PER_TIPO_FONO || 2,
          PER_FONO: this.personaNueva.PER_FONO ? '+56' + this.personaNueva.PER_FONO.replace(/^\+56/, '') : null,
          PER_APODO: this.personaNueva.PER_APODO || null,
          PER_PROFESION: this.personaNueva.PER_PROFESION || null,
          PER_NOM_EMERGENCIA: this.personaNueva.PER_NOM_EMERGENCIA || null,
          PER_FONO_EMERGENCIA: this.personaNueva.PER_FONO_EMERGENCIA ? '+56' + this.personaNueva.PER_FONO_EMERGENCIA.replace(/^\+56/, '') : null,
          PER_ALERGIA_ENFERMEDAD: this.personaNueva.PER_ALERGIA_ENFERMEDAD || null,
          PER_LIMITACION: this.personaNueva.PER_LIMITACION || null,
          PER_RELIGION: this.personaNueva.PER_RELIGION || null,
          PER_TIEMPO_NNAJ: this.personaNueva.PER_TIEMPO_NNAJ || null,
          PER_TIEMPO_ADULTO: this.personaNueva.PER_TIEMPO_ADULTO || null,
          PER_NUM_MMA: this.personaNueva.PER_NUM_MMA || null,
          PER_OTROS: this.personaNueva.PER_OTROS || null,
          PER_FOTO: this.personaNueva.foto || null,
          PER_VIGENTE: this.personaNueva.PER_VIGENTE !== undefined ? this.personaNueva.PER_VIGENTE : true,
          ESC_ID: this.personaNueva.ESC_ID && this.personaNueva.ESC_ID !== '' ? Number(this.personaNueva.ESC_ID) : 1,
          COM_ID: this.personaNueva.COM_ID && this.personaNueva.COM_ID !== '' ? Number(this.personaNueva.COM_ID) : 1,
          USU_ID: 1
        };
        
        console.log('💾 Guardando nueva persona:', datosPersona);
        
        const personaCreada = await personasService.personas.create(datosPersona);
        console.log('✅ Persona creada:', personaCreada);
        
        const personaId = personaCreada.PER_ID;
        
        if (this.personaNueva.PER_RAMA && this.personaNueva.PER_RAMA !== '') {
          try {
            const ramaData = await mantenedoresService.rama.list();
            const ramaEncontrada = ramaData.find(r => r.RAM_DESCRIPCION === this.personaNueva.PER_RAMA);
            
            if (ramaEncontrada) {
              await personasService.niveles.create({
                PER_ID: personaId,
                RAM_ID: ramaEncontrada.RAM_ID,
                NIV_ID: 1
              });
              console.log('✅ Rama asignada:', this.personaNueva.PER_RAMA);
            }
          } catch (error) {
            console.warn('⚠️ No se pudo asignar la rama:', error);
            console.error('Error completo:', error);
          }
        }
        
        if (this.personaNueva.PER_ROL && this.personaNueva.PER_ROL !== '') {
          try {
            await personasService.formadores.create({
              PER_ID: personaId
            });
            console.log('✅ Registrado como formador');
          } catch (error) {
            console.warn('⚠️ No se pudo registrar como formador:', error);
            console.error('Error completo:', error);
          }
        }
        
        console.log('🔄 Recargando lista de personas...');
        await this.cargarPersonas();
        
        if (this.filtroAplicado) {
          console.log('🔍 Reaplicando filtros...');
          await this.filtrar();
        }
        
        this.cerrarModalCrear();
        
        alert('¡Persona creada exitosamente!');
        
      } catch (error) {
        console.error('❌ Error creando persona:', error);
        console.error('📋 Detalles del error:', {
          status: error.status,
          statusText: error.statusText,
          message: error.message,
          response: error.response
        });
        
        let mensajeError = 'Error al crear la persona. ';
        if (error.response) {
          if (typeof error.response === 'object') {
            mensajeError += '\n\nDetalles:\n' + JSON.stringify(error.response, null, 2);
          } else {
            mensajeError += '\n\n' + error.response;
          }
        } else {
          mensajeError += error.message || 'Verifica los datos e intenta nuevamente.';
        }
        
        console.error('🔍 Datos que se intentaron enviar:', datosPersona);
        alert(mensajeError);
      } finally {
        this.guardandoPersona = false;
      }
    }
  },
  
  watch: {
    'personaNueva.PER_FONO'(newValue) {
      if (newValue) {
        this.personaNueva.PER_FONO = newValue.replace(/[^0-9]/g, '');
      }
    },
    'personaEditada.PER_FONO'(newValue) {
      if (newValue) {
        const cleaned = String(newValue).replace(/^\+56/, '').replace(/[^0-9]/g, '');
        if (cleaned !== newValue) {
          this.personaEditada.PER_FONO = cleaned;
        }
      }
    },
    'personaEditada.PER_FONO_EMERGENCIA'(newValue) {
      if (newValue) {
        const cleaned = String(newValue).replace(/^\+56/, '').replace(/[^0-9]/g, '');
        if (cleaned !== newValue) {
          this.personaEditada.PER_FONO_EMERGENCIA = cleaned;
        }
      }
    },
    'personaNueva.PER_FONO_EMERGENCIA'(newValue) {
      if (newValue) {
        this.personaNueva.PER_FONO_EMERGENCIA = newValue.replace(/[^0-9]/g, '');
      }
    }
  },
  
  async mounted() {
    await this.cargarPersonas();
    await this.cargarOpcionesFiltros();
    
    console.log('🎯 ESTADO FINAL DE FILTROS:');
    console.log('📋 Roles disponibles:', this.roleOptions);
    console.log('🌿 Ramas disponibles:', this.ramaOptions);
    console.log('🏢 Grupos disponibles:', this.courseOptions);
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

/* Nuevos estilos estandarizados basados en la pantalla de correos */
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

.btn-action:hover {
  filter: brightness(0.95) !important;
  box-shadow: 0 2px 8px rgba(40,92,168,0.1) !important;
  transform: translateY(-1px) !important;
}

.btn-modal {
  min-width: 120px !important;
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
/* ===== ESTILOS PARA MODAL CREAR PERSONA MEJORADO ===== */
.modal-crear {
  width: 900px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 0;
}

/* Header mejorado del modal crear */
.modal-header-crear {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 32px 20px 32px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-bottom: 2px solid #bbf7d0;
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.modal-header-crear .header-title h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #166534;
  line-height: 1.2;
}

.modal-header-crear .header-title .subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  font-weight: 500;
  color: #15803d;
}

.modal-header-crear .header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.modal-header-crear .btn-modal-header {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
  transition: all 0.2s ease;
}

.modal-header-crear .btn-modal-header:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.modal-header-crear .btn-modal-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Formulario de crear con padding */
.modal-form-crear {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px 32px 20px 32px;
}

/* Sección de Foto para Crear */
.foto-container-crear {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.foto-perfil-crear {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ffffff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.foto-perfil-crear:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.foto-placeholder-crear {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid #ffffff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  color: #64748b;
  gap: 8px;
}

.foto-placeholder-crear .foto-text {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
}

.foto-actions-crear {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.foto-actions-crear .btn-foto-upload,
.foto-actions-crear .btn-foto-remove {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.foto-actions-crear .btn-foto-upload {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.foto-actions-crear .btn-foto-upload:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.foto-actions-crear .btn-foto-remove {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.foto-actions-crear .btn-foto-remove:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.foto-actions-crear button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Acciones del formulario */
/* Acciones del formulario (botones al final) */
.modal-crear .form-actions,
.modal-crear .form-actions-bottom {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding-top: 24px;
  border-top: 2px solid #e2e8f0;
  margin-top: 10px;
}

.modal-crear .form-actions .btn-modal,
.modal-crear .form-actions-bottom .btn-cancelar-grande {
  min-width: 180px;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
}

.modal-crear .form-actions-bottom .btn-cancelar-grande {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 2px solid #cbd5e1;
  transition: all 0.2s ease;
}

.modal-crear .form-actions-bottom .btn-cancelar-grande:hover:not(:disabled) {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  border-color: #94a3b8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(71, 85, 105, 0.15);
}

/* Responsive para modal crear */
@media (max-width: 768px) {
  .modal-crear {
    width: 100%;
    padding: 0;
  }
  
  .modal-header-crear {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 16px 20px;
  }
  
  .modal-header-crear .header-title h2 {
    font-size: 20px;
  }
  
  .modal-header-crear .header-actions {
    justify-content: stretch;
  }
  
  .modal-header-crear .btn-modal-header {
    width: 100%;
  }
  
  .modal-form-crear {
    gap: 16px;
    padding: 16px 20px;
  }
  
  .foto-perfil-crear,
  .foto-placeholder-crear {
    width: 120px;
    height: 120px;
  }
  
  .modal-crear .form-actions,
  .modal-crear .form-actions-bottom {
    flex-direction: column;
    gap: 10px;
  }
  
  .modal-crear .form-actions .btn-modal,
  .modal-crear .form-actions-bottom .btn-cancelar-grande {
    width: 100%;
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

/* ===== ESTILOS PARA MODAL EDITAR MEJORADO ===== */
.modal-edit {
  width: 900px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 0;
}

/* Header mejorado del modal editar */
.modal-header-editar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 32px 20px 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.modal-header-editar .header-title h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.modal-header-editar .header-title .subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
}

.modal-header-editar .header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.modal-header-editar .btn-modal-header {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  transition: all 0.2s ease;
}

.modal-header-editar .btn-modal-header:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.modal-header-editar .btn-modal-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Tabs mejorados */
.modal-edit .modal-tabs {
  display: flex;
  gap: 8px;
  padding: 16px 32px 0 32px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 86px;
  z-index: 9;
}

.modal-edit .modal-tabs button {
  padding: 10px 20px;
  border-radius: 8px 8px 0 0;
  border: 1px solid #e2e8f0;
  border-bottom: none;
  background: #f8fafc;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  transition: all 0.2s ease;
  position: relative;
}

.modal-edit .modal-tabs button:hover {
  background: #e0e7ff;
  color: #3b82f6;
}

.modal-edit .modal-tabs button.active {
  background: #ffffff;
  color: #214e9c;
  border-color: #214e9c;
  box-shadow: 0 -2px 8px rgba(33, 78, 156, 0.1);
}

.modal-edit .modal-tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #ffffff;
}

/* Contenedor de formulario con padding */
.modal-edit .modal-form-editar {
  padding: 24px 32px;
}

@media (max-width: 768px) {
  .modal-edit {
    width: 100%;
    padding: 0;
  }
  
  .modal-header-editar {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 16px 20px;
  }
  
  .modal-header-editar .header-title h2 {
    font-size: 20px;
  }
  
  .modal-header-editar .header-actions {
    justify-content: stretch;
  }
  
  .modal-header-editar .btn-modal-header {
    width: 100%;
  }
  
  .modal-edit .modal-tabs {
    padding: 12px 20px 0 20px;
    top: 120px;
  }
  
  .modal-edit .modal-form-editar {
    padding: 16px 20px;
  }
}

/* Mantener compatibilidad con estilos antiguos */
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
  width: 300px;
  height: 300px;
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
  width: 300px;
  height: 300px;
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

/* ===== ESTILOS PARA FORMULARIO DE EDICIÓN MEJORADO ===== */
.modal-form-editar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-right: 8px;
  max-height: calc(100vh - 280px);
  overflow-y: auto;
  padding-bottom: 20px;
}

/* Sección de Formulario */
.form-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.form-section:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

/* Sección de Foto Especial */
.form-section.foto-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
  border: 2px dashed #cbd5e1;
  padding: 24px;
}

/* Título de Sección */
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2e8f0;
}

/* Grid de Formulario */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field.full-width {
  grid-column: 1 / -1;
}

.form-field label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 2px;
}

/* Wrapper para inputs de teléfono con prefijo +56 */
.phone-input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  overflow: hidden;
  transition: all 0.2s ease;
}

.phone-input-wrapper:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.phone-prefix {
  padding: 10px 12px;
  background: #f1f5f9;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
  border-right: 1px solid #cbd5e1;
  user-select: none;
}

.phone-input-wrapper .phone-input {
  flex: 1;
  border: none !important;
  box-shadow: none !important;
  margin: 0;
  border-radius: 0;
}

.phone-input-wrapper .phone-input:focus {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

.form-field label::after {
  content: attr(data-required);
}

/* Contenedor de Foto Editar */
.foto-container-editar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.foto-preview-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.foto-perfil-editar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ffffff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.foto-perfil-editar:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.foto-placeholder-editar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid #ffffff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  color: #64748b;
  gap: 8px;
}

.foto-placeholder-editar .foto-text {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
}

.foto-actions-editar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.foto-actions-editar .btn-foto-upload,
.foto-actions-editar .btn-foto-remove {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.foto-actions-editar .btn-foto-upload {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.foto-actions-editar .btn-foto-upload:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.foto-actions-editar .btn-foto-remove {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.foto-actions-editar .btn-foto-remove:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* Información de foto */
.foto-info {
  text-align: center;
  margin-top: 8px;
}

.foto-info small {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
  background: rgba(100, 116, 139, 0.08);
  padding: 4px 12px;
  border-radius: 12px;
  display: inline-block;
}

/* Contenedor RUT en formulario editar */
.form-field .rut-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.form-field .rut-container .rut-separator {
  font-weight: bold;
  color: #64748b;
  font-size: 18px;
  margin: 0 4px;
}

.form-field .rut-container input:first-child {
  flex: 1;
}

.form-field .rut-container .rut-dv {
  width: 60px;
  text-align: center;
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-field.full-width {
    grid-column: 1;
  }
  
  .modal-form-editar {
    gap: 16px;
  }
  
  .form-section {
    padding: 16px;
  }
  
  .foto-perfil-editar,
  .foto-placeholder-editar {
    width: 120px;
    height: 120px;
  }
}

/* Animación de entrada */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-section {
  animation: fadeInUp 0.3s ease;
}

.form-section:nth-child(1) { animation-delay: 0s; }
.form-section:nth-child(2) { animation-delay: 0.05s; }
.form-section:nth-child(3) { animation-delay: 0.1s; }
.form-section:nth-child(4) { animation-delay: 0.15s; }
.form-section:nth-child(5) { animation-delay: 0.2s; }

/* Responsive para historial */
@media (max-width: 1024px) {
  .historial-panel {
    flex-direction: column;
    gap: 20px;
  }
  
  .hist-add {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .historial-panel {
    padding: 16px 20px;
  }
  
  .hist-list,
  .hist-add {
    padding: 16px;
  }
}
</style>

<style scoped>
/* Tabs ya están definidos arriba, estos son duplicados - comentados */
/* .modal-tabs { display:flex; gap:8px; margin-bottom:12px } */
/* .modal-tabs button { padding:8px 12px; border-radius:6px; border:1px solid #e6e6e6; background:#fff; cursor:pointer } */
/* .modal-tabs button.active { background:#214e9c; color:#fff; border-color:#214e9c } */

/* Panel de historial mejorado */
.historial-panel { 
  display: flex; 
  gap: 24px; 
  align-items: flex-start;
  padding: 24px 32px;
  max-height: calc(100vh - 340px); 
  overflow: auto;
  background: #f8fafc;
}

.hist-list { 
  flex: 1; 
  overflow: auto;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.hist-list ul { 
  list-style: none; 
  padding: 0; 
  margin: 0;
}

.hist-list li { 
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  transition: background 0.2s ease;
}

.hist-list li:hover {
  background: #f9fafb;
}

.hist-list li:last-child {
  border-bottom: none;
}

.hist-add { 
  width: 340px;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.hist-add h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 12px;
}

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
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirm-icon.warning-icon {
  color: #f59e0b;
  filter: drop-shadow(0 4px 8px rgba(245, 158, 11, 0.3));
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

/* Estilos para el modal de importar Excel - Diseño mejorado */
.modal-importar {
  width: 900px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 0;
}

/* Header mejorado del modal importar */
.modal-header-importar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 32px 20px 32px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-bottom: 2px solid #fbbf24;
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.modal-header-importar .header-title h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #78350f;
  line-height: 1.2;
}

.modal-header-importar .header-title .subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  font-weight: 500;
  color: #92400e;
}

.modal-header-importar .header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.modal-header-importar .btn-import-header {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
  transition: all 0.2s ease;
}

.modal-header-importar .btn-import-header:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.modal-header-importar .btn-import-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Formulario de importar con padding */
.modal-form-importar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px 32px 20px 32px;
}

.import-instructions {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
}

.import-instructions ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.import-instructions li {
  margin-bottom: 8px;
  color: #64748b;
  font-size: 14px;
}

.template-download {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.btn-template {
  background: linear-gradient(180deg, #3b82f6, #2563eb);
  color: white;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-template:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.file-selector {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.2s ease;
}

.file-selector:hover {
  border-color: #60a5fa;
  background: #eff6ff;
}

.btn-select-file {
  padding: 12px 24px;
  font-weight: 600;
}

.file-name {
  font-weight: 500;
  color: #059669;
  display: flex;
  align-items: center;
  gap: 8px;
}

.preview-section {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  background: #fafafa;
}

.preview-table {
  overflow-x: auto;
  margin-bottom: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.preview-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  background: white;
}

.preview-table th,
.preview-table td {
  padding: 12px 16px;
  text-align: left;
  border: 1px solid #e2e8f0;
}

.preview-table th {
  background: #f1f5f9;
  font-weight: 600;
  color: #334155;
  position: sticky;
  top: 0;
}

.preview-table td {
  background: white;
  color: #64748b;
}

.preview-table tbody tr:hover {
  background: #f8fafc;
}

.preview-info {
  margin: 12px 0 0 0;
  font-weight: 500;
  color: #059669;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f0fdf4;
  border-radius: 6px;
  border: 1px solid #bbf7d0;
}

.modal-importar .form-actions-bottom {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.modal-importar .form-actions-bottom .btn-cancelar-grande {
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.modal-importar .form-actions-bottom .btn-cancelar-grande:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@media (max-width: 600px) {
  .modal-importar {
    width: 100%;
  }

  .modal-header-importar {
    padding: 16px;
    flex-direction: column;
    align-items: flex-start;
  }

  .modal-header-importar .header-title h2 {
    font-size: 20px;
  }

  .modal-header-importar .header-actions {
    width: 100%;
  }

  .modal-header-importar .btn-import-header {
    width: 100%;
    justify-content: center;
  }

  .modal-form-importar {
    padding: 16px;
  }
  
  .file-selector {
    flex-direction: column;
    text-align: center;
  }

  .btn-select-file {
    width: 100%;
  }
  
  .modal-importar .form-actions-bottom {
    flex-direction: column;
  }

  .modal-importar .form-actions-bottom .btn-cancelar-grande {
    width: 100%;
  }
}

/* Mensaje informativo de permisos */
.mensaje-info-permisos {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 2px solid #3b82f6;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.mensaje-info-permisos span {
  color: #1e40af;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .mensaje-info-permisos {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 16px;
  }
}
</style>

