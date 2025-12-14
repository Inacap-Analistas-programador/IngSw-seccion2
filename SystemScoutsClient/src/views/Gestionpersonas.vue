<template>
  <div class="gestion-personas">
  <!-- Vista: la NavBar se renderiza globalmente en App.vue, no incluirla aquí -->

    <!-- Encabezado estándar de pantalla -->
    <div class="header">
      <h2>Gestión de Personas</h2>
      <h3>Administra, crea y organiza el registro de personas.</h3>
    </div>

    <!-- Barra de búsqueda y filtros: separar móvil y escritorio para evitar que se mezclen -->
    <!-- Versión móvil: dos columnas, toggle y sin acciones de escritorio -->
    <div v-if="isMobile" :class="['filtros filtros-mobile', filtrosColapsados ? 'filtros-collapsed' : '']">
      <div class="filtros-toggle-mobile">
        <button type="button" class="btn-standard btn-toggle-filtros" @click="toggleFiltros">
          <AppIcons :name="filtrosColapsados ? 'chevron-down' : 'chevron-up'" :size="18" />
          {{ filtrosColapsados ? 'Mostrar filtros' : 'Ocultar filtros' }}
        </button>
      </div>
      <div class="filtros-left" v-if="!filtrosColapsados">
        <InputBase v-model="searchQuery" placeholder="Buscar por nombre, RUT, email..." @input="filtrar({ immediate: false })" @keydown.enter.prevent="filtrar" @focus="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedRole" :options="roleOptions" placeholder="Todos los roles" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedCourse" :options="courseOptions" placeholder="Todos los grupos" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedCurso" :options="cursosOptions" placeholder="Seleccione Curso" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedRama" :options="ramaOptions" placeholder="Todas las ramas" @click="ensureFiltrosLoaded" />
        <BaseButton class="btn-search btn-standard" variant="primary" @click="filtrar"><AppIcons name="search" :size="16" /> Buscar</BaseButton>
      </div>
    </div>

    <!-- Versión escritorio: fila con filtros a la izquierda y acciones a la derecha -->
    <div v-else class="filtros">
      <div class="filtros-left">
        <InputBase v-model="searchQuery" placeholder="Buscar por nombre, RUT, email..." @input="filtrar({ immediate: false })" @keydown.enter.prevent="filtrar" @focus="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedRole" :options="roleOptions" placeholder="Todos los roles" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedCourse" :options="courseOptions" placeholder="Todos los grupos" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedCurso" :options="cursosOptions" placeholder="Seleccione Curso" @click="ensureFiltrosLoaded" />
        <BaseSelect v-model="selectedRama" :options="ramaOptions" placeholder="Todas las ramas" @click="ensureFiltrosLoaded" />
        <BaseButton class="btn-search btn-standard" variant="primary" @click="filtrar"><AppIcons name="search" :size="16" /> Buscar</BaseButton>
      </div>
      <div class="filtros-right">
        <BaseButton v-if="canCreate" class="btn-add btn-standard" variant="primary" @click="abrirRutPopup"><AppIcons name="plus" :size="16" /> Nueva Persona</BaseButton>
        <BaseButton v-if="canCreate" class="btn-import btn-standard" variant="secondary" @click="abrirModalImportar"><AppIcons name="download" :size="16" /> Importar Excel</BaseButton>
        <BaseButton class="btn-export btn-standard" variant="secondary" @click="abrirModalExportar"><AppIcons name="upload" :size="16" /> Exportar</BaseButton>
      </div>
    </div>

            <!-- Desktop actions are now rendered inside the filters right area so they -->

    <!-- Acciones principales para mobile: se muestran debajo de los filtros cuando están visibles o colapsadas -->
    <div class="acciones-top" v-if="isMobile">
      <BaseButton v-if="canCreate" class="btn-add btn-standard" variant="primary" @click="abrirRutPopup"><AppIcons name="plus" :size="16" /> Nueva Persona</BaseButton>
      <BaseButton v-if="canCreate" class="btn-import btn-standard" variant="secondary" @click="abrirModalImportar"><AppIcons name="download" :size="16" /> Importar Excel</BaseButton>
      <BaseButton class="btn-export btn-standard" variant="secondary" @click="abrirModalExportar"><AppIcons name="upload" :size="16" /> Exportar</BaseButton>
    </div>

    <!-- Mensaje informativo de permisos limitados -->


    <!-- Indicadores de carga y error -->
    <div v-if="cargandoPersonas" class="estado-carga">
      <p><AppIcons name="refresh" :size="16" /> Cargando personas...</p>
    </div>
    <div v-if="filtrandoEnProceso" class="estado-carga">
      <p><AppIcons name="refresh" :size="16" /> Filtrando resultados...</p>
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
      <div v-if="filtroAplicado" class="table-container">
      <table class="courses-table">
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
            <span class="truncate">{{ `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim() }}</span>
          </td>
          <td data-label="RUT">{{ p.PER_RUN }}-{{ p.PER_DV }}</td>
          <td data-label="Email" :title="p.PER_MAIL || 'Sin email'">
            <span class="truncate">{{ p.PER_MAIL }}</span>
          </td>
          <td data-label="Rol" :title="p.PER_ROL || 'Sin rol'">
            <span class="truncate">{{ (p.PER_ROL || 'Sin rol').trim() }}</span>
          </td>
          <td data-label="Teléfono/Celular">{{ p.PER_FONO || p.PER_CEL || 'Sin teléfono' }}</td>
          <td data-label="Estado">
            <span :class="['badge', p.PER_VIGENTE ? 'vigente' : 'anulado']">
              {{ p.PER_VIGENTE ? 'Activo' : 'Inactivo' }}
            </span>
          </td>
          <td class="actions-cell">
            <div class="acciones-buttons">
              <BaseButton class="btn-ver btn-action" variant="info" size="sm" @click="abrirModalVer(p)" title="Ver"><AppIcons name="eye" :size="14" /><span class="btn-label">Ver</span></BaseButton>
              <BaseButton v-if="canEdit" class="btn-editar btn-action" variant="secondary" size="sm" @click="abrirModalEditar(p)" title="Editar"><AppIcons name="edit" :size="14" /><span class="btn-label">Editar</span></BaseButton>
              <BaseButton v-if="canDelete && p.PER_VIGENTE" class="btn-anular btn-action" variant="danger" size="sm" @click="anularPersona(p)" title="Anular"><AppIcons name="x" :size="14" /><span class="btn-label">Anular</span></BaseButton>
              <BaseButton v-if="canDelete && !p.PER_VIGENTE" class="btn-reactivar btn-action" variant="success" size="sm" @click="reactivarPersona(p)" title="Reactivar"><AppIcons name="check" :size="14" /><span class="btn-label">Reactivar</span></BaseButton>
            </div>
          </td>
        </tr>
        <tr v-if="personasFiltradas.length === 0">
           <td colspan="7" class="no-results">No se encontraron personas que coincidan con los filtros.</td>
        </tr>
      </tbody>
      </table>
    </div>

        <!-- Mostrar mensaje instructivo hasta que el usuario aplique el filtro -->
        <div v-if="!filtroAplicado" class="no-filtro" style="padding:16px; text-align:center; color:#666;">
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
                  <div class="header-actions">
                    <BaseButton 
                      v-if="!modoSoloLectura"
                      class="btn-cancel btn-modal-header" 
                      type="button" 
                      variant="secondary" 
                      @click="cancelarEdicion"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons name="x" :size="16" />
                      Cancelar
                    </BaseButton>
                    <BaseButton 
                      v-if="!modoSoloLectura"
                      class="btn-save btn-modal-header" 
                      type="button" 
                      variant="primary" 
                      @click="guardarEdicion"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons :name="guardandoPersona ? 'clock' : 'save'" :size="16" />
                      {{ guardandoPersona ? 'Guardando...' : 'Guardar Cambios' }}
                    </BaseButton>
                    <BaseButton 
                      v-if="modoSoloLectura"
                      class="btn-cancel btn-modal-header" 
                      type="button" 
                      variant="secondary" 
                      @click="cancelarEdicion"
                    >
                      <AppIcons name="x" :size="16" />
                      Cerrar
                    </BaseButton>
                  </div>
                </header>

                <div class="modal-tabs">
                  <button :class="{active: modalTab === 'info'}" @click="modalTab='info'">Info</button>
                  <button :class="{active: modalTab === 'hist'}" @click="modalTab='hist'">Historial</button>
                </div>

                <form v-if="modalTab==='info'" @submit.prevent="" class="modal-form-editar">
                  <!-- Información Personal -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="person" :size="18" />
                      Información Personal
                    </h3>
                    
                    <!-- Foto de Perfil integrada -->
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
                          <AppIcons name="person" :size="60" />
                          <span class="foto-text">Sin foto</span>
                        </div>
                      </div>
                      <div v-if="!modoSoloLectura" class="foto-actions-editar">
                        <input 
                          ref="fotoInput"
                          type="file" 
                          accept="image/png, image/jpeg, image/jpg" 
                          @change.stop="handleFileUpload($event, 'editar')"
                          style="display: none"
                        />
                        <BaseButton 
                          type="button" 
                          @click.stop="$refs.fotoInput?.click()" 
                          variant="primary"
                          class="btn-foto"
                        >
                          <AppIcons name="camera" :size="16" /> {{ personaEditada.foto ? 'Cambiar Foto' : 'Subir Foto' }}
                        </BaseButton>
                        <BaseButton 
                          v-if="personaEditada.foto" 
                          type="button" 
                          @click="removePhoto('editar')" 
                          variant="secondary"
                          class="btn-foto"
                        >
                          <AppIcons name="trash" :size="16" /> Eliminar
                        </BaseButton>
                      </div>
                      <div class="foto-info">
                        <small>PNG o JPG • Máx. 5MB</small>
                      </div>
                    </div>
                    
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Nombres *</label>
                        <InputBase v-model="personaEditada.PER_NOMBRES" :readonly="modoSoloLectura" required placeholder="Ingrese nombres" />
                      </div>
                      <div class="form-field">
                        <label>Apellido Paterno *</label>
                        <InputBase v-model="personaEditada.PER_APELPTA" :readonly="modoSoloLectura" placeholder="Ingrese apellido paterno" />
                      </div>
                      <div class="form-field">
                        <label>Apellido Materno</label>
                        <InputBase v-model="personaEditada.PER_APELMAT" :readonly="modoSoloLectura" placeholder="Ingrese apellido materno" />
                      </div>
                      <div class="form-field">
                        <label>RUT *</label>
                        <div class="rut-container">
                          <InputBase v-model="personaEditada.PER_RUN" :readonly="modoSoloLectura" @input="calcularDvEditada" placeholder="12345678" />
                          <span class="rut-separator">-</span>
                          <InputBase v-model="personaEditada.PER_DV" :readonly="modoSoloLectura" class="rut-dv" maxlength="1" placeholder="9" />
                        </div>
                      </div>
                      <div class="form-field">
                        <label>Fecha de Nacimiento *</label>
                        <InputBase v-model="personaEditada.PER_FECHA_NAC" :readonly="modoSoloLectura" type="date" />
                      </div>
                      <div class="form-field">
                        <label>Estado Civil *</label>
                        <BaseSelect v-model="personaEditada.ESC_ID" :options="estadoCivilOptions" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Apodo *</label>
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
                        <label>Email *</label>
                        <InputBase v-model="personaEditada.PER_MAIL" :readonly="modoSoloLectura" type="email" placeholder="correo@ejemplo.com" />
                      </div>
                      <div class="form-field">
                        <label>Teléfono *</label>
                        <div class="phone-input-wrapper">
                          <span class="phone-prefix">+56</span>
                          <InputBase v-model="personaEditada.PER_FONO" :readonly="modoSoloLectura" placeholder="912345678" class="phone-input" />
                        </div>
                      </div>
                      <div class="form-field full-width">
                        <label>Dirección *</label>
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
                        <label>Comuna *</label>
                        <BaseSelect v-model="personaEditada.COM_ID" :options="comunaOptionsEditar" :disabled="modoSoloLectura || !personaEditada.PRO_ID" />
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
                      <!-- Rama seleccionado desde Nivel y Rama (evitar duplicado) -->
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

                  <!-- Información de Grupo -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="users" :size="18" />
                      Grupo Scout
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Grupo</label>
                        <BaseSelect v-model="personaEditada.GRU_ID" :options="gruposOptions" :disabled="modoSoloLectura" placeholder="Seleccione grupo" />
                      </div>
                      <div class="form-field">
                        <label>Vigente en Grupo</label>
                        <BaseSelect v-model="personaEditada.PEG_VIGENTE" :options="[{value: true, label: 'Sí'}, {value: false, label: 'No'}]" :disabled="modoSoloLectura" />
                      </div>
                    </div>
                  </div>

                  <!-- Información de Formador -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="award" :size="18" />
                      Datos de Formador
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Habilitación 1</label>
                        <BaseSelect v-model="personaEditada.PEF_HAB_1" :options="[{value: true, label: 'Sí'}, {value: false, label: 'No'}]" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Habilitación 2</label>
                        <BaseSelect v-model="personaEditada.PEF_HAB_2" :options="[{value: true, label: 'Sí'}, {value: false, label: 'No'}]" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field">
                        <label>Verificado</label>
                        <BaseSelect v-model="personaEditada.PEF_VERIF" :options="[{value: true, label: 'Sí'}, {value: false, label: 'No'}]" :disabled="modoSoloLectura" />
                      </div>
                      <div class="form-field full-width">
                        <label>Historial de Formador</label>
                        <InputBase v-model="personaEditada.PEF_HISTORIAL" :readonly="modoSoloLectura" placeholder="Historial de formación" />
                      </div>
                    </div>
                  </div>

                  <!-- Información Individual -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="person" :size="18" />
                      Información Individual
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Cargo</label>
                        <BaseSelect v-model="personaEditada.CAR_ID" :options="cargosOptions" :disabled="modoSoloLectura" placeholder="Seleccione cargo" />
                      </div>
                      <div class="form-field">
                        <label>Distrito</label>
                        <BaseSelect v-model="personaEditada.DIS_ID" :options="distritosOptions" :disabled="modoSoloLectura" placeholder="Seleccione distrito" />
                      </div>
                      <div class="form-field">
                        <label>Zona</label>
                        <BaseSelect v-model="personaEditada.ZON_ID" :options="zonasOptions" :disabled="modoSoloLectura" placeholder="Seleccione zona" />
                      </div>
                      <div class="form-field">
                        <label>Vigente Individual</label>
                        <BaseSelect v-model="personaEditada.PEI_VIGENTE" :options="[{value: true, label: 'Sí'}, {value: false, label: 'No'}]" :disabled="modoSoloLectura" />
                      </div>
                    </div>
                  </div>

                  <!-- Información de Nivel -->
                  <div class="form-section">
                    <div class="section-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                      <h3 class="section-title" style="margin-bottom: 0;">
                        <AppIcons name="star" :size="18" />
                        Nivel y Rama
                      </h3>
                      <BaseButton 
                        v-if="!modoSoloLectura"
                        type="button" 
                        variant="secondary" 
                        size="sm" 
                        @click="agregarRama('editar')"
                        :disabled="guardandoPersona"
                      >
                        <AppIcons name="plus" :size="14" /> Agregar
                      </BaseButton>
                    </div>
                    
                    <div v-for="(ramaItem, index) in personaEditada.ramas" :key="index" class="rama-row" style="display: flex; gap: 1rem; align-items: flex-end; margin-bottom: 12px; border-bottom: 1px dashed #eee; padding-bottom: 12px;">
                      <div class="form-field" style="flex: 1;">
                        <label>Nivel {{ index + 1 }}</label>
                        <BaseSelect 
                          v-model="ramaItem.NIV_ID" 
                          :options="nivelesOptions" 
                          :disabled="modoSoloLectura" 
                          placeholder="Seleccione nivel" 
                        />
                      </div>
                      <div class="form-field" style="flex: 1;">
                        <label>Rama (Nivel) {{ index + 1 }}</label>
                        <BaseSelect 
                          v-model="ramaItem.RAM_ID_NIVEL" 
                          :options="ramaOptions" 
                          :disabled="modoSoloLectura" 
                          placeholder="Seleccione rama" 
                        />
                      </div>
                      
                       <div style="padding-bottom: 4px;">
                         <BaseButton 
                          v-if="!modoSoloLectura && personaEditada.ramas.length > 1"
                          type="button" 
                          variant="danger" 
                          @click="eliminarRama(index, 'editar')"
                          :disabled="guardandoPersona"
                          title="Eliminar"
                          style="padding: 8px;"
                        >
                          <AppIcons name="trash" :size="16" />
                        </BaseButton>
                      </div>
                    </div>
                  </div>

                  <!-- Información de Vehículo -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="truck" :size="18" />
                      Vehículo
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Patente</label>
                        <InputBase v-model="personaEditada.PEV_PATENTE" :readonly="modoSoloLectura" placeholder="AA-BB-12" />
                      </div>
                      <div class="form-field">
                        <label>Marca</label>
                        <InputBase v-model="personaEditada.PEV_MARCA" :readonly="modoSoloLectura" placeholder="Toyota" />
                      </div>
                      <div class="form-field">
                        <label>Modelo</label>
                        <InputBase v-model="personaEditada.PEV_MODELO" :readonly="modoSoloLectura" placeholder="Corolla" />
                      </div>
                      <!-- Año/Color/Capacidad removidos: la BD no los almacena actualmente -->
                    </div>
                  </div>
              
                  <!-- Salud y Alimentación (Formulario 2) -->
                  <div class="form-section">
                    <h3 class="section-title">
                      <AppIcons name="heart" :size="18" />
                      Salud y Alimentación
                    </h3>
                    <div class="form-grid">
                      <div class="form-field">
                        <label>Tipo de Alimentación</label>
                        <BaseSelect v-model="personaEditada.ALI_ID" :options="alimentacionOptions" :disabled="modoSoloLectura" />
                      </div>

                      <div class="form-field full-width">
                        <label>Alergias / Enfermedades</label>
                        <InputBase v-model="personaEditada.PER_ALERGIA_ENFERMEDAD" :readonly="modoSoloLectura" />
                      </div>

                      <div class="form-field full-width">
                        <label>Limitaciones</label>
                        <InputBase v-model="personaEditada.PER_LIMITACION" :readonly="modoSoloLectura" />
                      </div>

                      <div class="form-field">
                        <label>Contacto Emergencia</label>
                        <InputBase v-model="personaEditada.PER_NOM_EMERGENCIA" :readonly="modoSoloLectura" placeholder="Nombre del contacto" />
                      </div>
                      <div class="form-field">
                        <label>Tel. Emergencia</label>
                        <div class="phone-input-wrapper">
                          <span class="phone-prefix">+56</span>
                          <InputBase v-model="personaEditada.PER_FONO_EMERGENCIA" :readonly="modoSoloLectura" placeholder="912345678" class="phone-input" />
                        </div>
                      </div>
                    </div>
                  </div>

                  
                </form>

                <div v-else class="historial-panel" :class="{ 'historial-anulado': personaEditada.estado === 'Anulado' }">
                  <div class="hist-list">
                    <h4>Cursos Realizados</h4>
                    <div v-if="!personaEditada.cursosHistorial || personaEditada.cursosHistorial.length === 0" class="no-cursos-msg">
                      Esta persona no tiene cursos registrados.
                    </div>
                    <ul v-else>
                      <li v-for="curso in personaEditada.cursosHistorial" :key="curso.PEC_ID" 
                          class="historial-curso-item">
                        <div class="curso-item-content" @click="navegarACurso(curso.CUS_ID)" :title="'Clic para ver detalles del curso'">
                          <div class="curso-header">
                            <strong class="curso-nombre">{{ curso.CUR_NOMBRE || 'Curso sin nombre' }}</strong>
                            <span class="curso-codigo">#{{ curso.CUR_CODIGO || curso.CUS_ID }}</span>
                          </div>
                          <div class="curso-info">
                            <span class="curso-rol">{{ curso.ROL_DESCRIPCION || 'Sin rol' }}</span>
                            <span v-if="curso.ESTADO_APROBACION" class="curso-estado" :class="curso.ESTADO_APROBACION.aprobado ? 'aprobado' : 'no-aprobado'">
                              {{ curso.ESTADO_APROBACION.texto }}
                            </span>
                            <span v-if="curso.CUR_FECHAINICIO" class="curso-fecha">
                              {{ formatearFecha(curso.CUR_FECHAINICIO) }}
                              <span v-if="curso.CUR_FECHAFIN"> - {{ formatearFecha(curso.CUR_FECHAFIN) }}</span>
                            </span>
                          </div>
                          <div v-if="curso.CUR_DESCRIPCION" class="curso-descripcion">
                            {{ curso.CUR_DESCRIPCION }}
                          </div>
                        </div>
                        <div class="curso-actions">
                          <BaseButton 
                            variant="primary" 
                            class="btn-ver-pagos"
                            @click.stop="navegarAPagos(curso.CUS_ID, personaEditada)"
                            title="Ver pagos de este curso"
                          >
                            <AppIcons name="dollar-sign" :size="14" /> Pagos
                          </BaseButton>
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
              <BaseButton @click="confirmarAnulacion" variant="primary" class="btn-modal-anular btn-modal">
                <AppIcons name="alert-triangle" :size="16" /> Anular
              </BaseButton>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Confirmación de Reactivación -->
      <BaseModal v-model="confirmModalReactivarVisible" title="Confirmar Reactivación">
        <template #default>
          <div class="confirm-content">
            <div class="confirm-icon success-icon"><AppIcons name="check" :size="48" /></div>
            <p>¿Estás seguro de que deseas reactivar a <strong>{{ personaAReactivar?.PER_NOMBRES }} {{ personaAReactivar?.PER_APELPTA }}</strong>?</p>
            <p class="confirm-warning">Esta acción marcará a la persona como vigente en la base de datos.</p>
            <div class="confirm-actions">
              <BaseButton @click="cancelarReactivacion" variant="secondary" class="btn-modal-cancel btn-modal">
                <AppIcons name="x" :size="16" /> Cancelar
              </BaseButton>
              <BaseButton @click="confirmarReactivacion" variant="primary" class="btn-modal-reactivar btn-modal">
                <AppIcons name="check" :size="16" /> Reactivar
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
                  class="btn-cancel btn-modal-header" 
                  type="button" 
                  variant="secondary" 
                  @click="cerrarModalCrear"
                  :disabled="guardandoPersona"
                >
                  <AppIcons name="x" :size="16" />
                  Cancelar
                </BaseButton>
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
              
              <!-- Información Personal -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="person" :size="18" />
                  Información Personal
                </h3>
                
                <!-- Foto de Perfil integrada -->
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
                      <AppIcons name="person" :size="60" />
                      <span class="foto-text">Sin foto</span>
                    </div>
                  </div>
                  <div class="foto-actions-crear">
                    <input 
                      ref="fotoInputNueva"
                      type="file" 
                      accept="image/png, image/jpeg, image/jpg" 
                      @change.stop="handleFileUpload($event, 'nueva')"
                      style="display: none"
                    />
                    <BaseButton 
                      type="button" 
                      @click.stop="$refs.fotoInputNueva?.click()" 
                      variant="primary"
                      class="btn-foto"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons name="camera" :size="16" /> {{ personaNueva.foto ? 'Cambiar Foto' : 'Subir Foto' }}
                    </BaseButton>
                    <BaseButton 
                      v-if="personaNueva.foto" 
                      type="button" 
                      @click="removePhoto('nueva')" 
                      variant="secondary"
                      class="btn-foto"
                      :disabled="guardandoPersona"
                    >
                      <AppIcons name="trash" :size="16" /> Eliminar
                    </BaseButton>
                  </div>
                  <div class="foto-info">
                    <small>PNG o JPG • Máx. 5MB</small>
                  </div>
                </div>
                
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
                    <small v-if="rutNuevoInvalido" class="error-message">⚠️ Debe ingresar un RUT válido</small>
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
                    <label>Estado Civil *</label>
                    <BaseSelect 
                      v-model="personaNueva.ESC_ID" 
                      :options="estadoCivilOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Apodo *</label>
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
                    <label>Teléfono *</label>
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
                    <label>Tipo de Teléfono *</label>
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
                    <label>Dirección *</label>
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
                    <label>Comuna *</label>
                    <BaseSelect 
                      v-model="personaNueva.COM_ID" 
                      :options="comunaOptions"
                      :disabled="guardandoPersona || !personaNueva.PRO_ID"
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

                  <!-- Rama seleccionado desde Nivel y Rama (evitar duplicado) -->

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
              
              <!-- Grupo Scout -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="people" :size="18" />
                  Grupo Scout
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Grupo</label>
                    <BaseSelect 
                      v-model="personaNueva.GRU_ID" 
                      :options="gruposOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                    <div class="form-field">
                      <label>Curso / Sección (requerido para registrar vehículo)</label>
                      <BaseSelect
                        v-model="personaNueva.CUS_ID"
                        :options="cursosOptions"
                        :disabled="guardandoPersona"
                      />
                    </div>

                  <div class="form-field">
                    <label>Vigente</label>
                    <BaseSelect 
                      v-model="personaNueva.PEG_VIGENTE" 
                      :options="[
                        { value: true, label: 'Sí' },
                        { value: false, label: 'No' }
                      ]"
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>

              <!-- Datos de Formador -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="school" :size="18" />
                  Datos de Formador
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Habilitación 1</label>
                    <BaseSelect
                      v-model="personaNueva.PEF_HAB_1"
                      :options="[{ value: true, label: 'Sí' }, { value: false, label: 'No' }]"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Habilitación 2</label>
                    <BaseSelect
                      v-model="personaNueva.PEF_HAB_2"
                      :options="[{ value: true, label: 'Sí' }, { value: false, label: 'No' }]"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Verificado</label>
                    <BaseSelect 
                      v-model="personaNueva.PEF_VERIF" 
                      :options="[
                        { value: true, label: 'Sí' },
                        { value: false, label: 'No' }
                      ]"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field full-width">
                    <label>Historial</label>
                    <InputBase 
                      v-model="personaNueva.PEF_HISTORIAL" 
                      placeholder="Historial de formador" 
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>

              <!-- Información Individual -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="person" :size="18" />
                  Información Individual
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Cargo</label>
                    <BaseSelect 
                      v-model="personaNueva.CAR_ID" 
                      :options="cargosOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Distrito</label>
                    <BaseSelect 
                      v-model="personaNueva.DIS_ID" 
                      :options="distritosOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Zona</label>
                    <BaseSelect 
                      v-model="personaNueva.ZON_ID" 
                      :options="zonasOptions"
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Vigente</label>
                    <BaseSelect 
                      v-model="personaNueva.PEI_VIGENTE" 
                      :options="[
                        { value: true, label: 'Sí' },
                        { value: false, label: 'No' }
                      ]"
                      :disabled="guardandoPersona"
                    />
                  </div>
                </div>
              </div>

              <!-- Nivel y Rama -->
              <!-- Nivel y Rama -->
              <div class="form-section">
                <div class="section-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                  <h3 class="section-title" style="margin-bottom: 0;">
                    <AppIcons name="layers" :size="18" />
                    Nivel y Rama
                  </h3>
                  <BaseButton 
                    type="button" 
                    variant="secondary" 
                    size="sm" 
                    @click="agregarRama('nueva')"
                    :disabled="guardandoPersona"
                  >
                    <AppIcons name="plus" :size="14" /> Agregar
                  </BaseButton>
                </div>
                
                <div v-for="(ramaItem, index) in personaNueva.ramas" :key="index" class="rama-row" style="display: flex; gap: 1rem; align-items: flex-end; margin-bottom: 12px; border-bottom: 1px dashed #eee; padding-bottom: 12px;">
                  <div class="form-field" style="flex: 1;">
                    <label>Nivel {{ index + 1 }}</label>
                    <BaseSelect 
                      v-model="ramaItem.NIV_ID" 
                      :options="nivelesOptions"
                      :disabled="guardandoPersona"
                      placeholder="Seleccionar Nivel"
                    />
                  </div>

                  <div class="form-field" style="flex: 1;">
                    <label>Rama {{ index + 1 }}</label>
                    <BaseSelect 
                      v-model="ramaItem.RAM_ID_NIVEL" 
                      :options="ramaOptions"
                      :disabled="guardandoPersona"
                      placeholder="Seleccionar Rama"
                    />
                  </div>
                  
                  <div style="padding-bottom: 4px;">
                     <BaseButton 
                      v-if="personaNueva.ramas.length > 1"
                      type="button" 
                      variant="danger" 
                      @click="eliminarRama(index, 'nueva')"
                      :disabled="guardandoPersona"
                      title="Eliminar"
                      style="padding: 8px;"
                    >
                      <AppIcons name="trash" :size="16" />
                    </BaseButton>
                  </div>
                </div>
              </div>

              <!-- Vehículo -->
              <div class="form-section">
                <h3 class="section-title">
                  <AppIcons name="car" :size="18" />
                  Vehículo
                </h3>
                <div class="form-grid">
                  <div class="form-field">
                    <label>Patente</label>
                    <InputBase 
                      v-model="personaNueva.PEV_PATENTE" 
                      placeholder="XXXX00" 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Marca</label>
                    <InputBase 
                      v-model="personaNueva.PEV_MARCA" 
                      placeholder="Toyota, Nissan, etc." 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <div class="form-field">
                    <label>Modelo</label>
                    <InputBase 
                      v-model="personaNueva.PEV_MODELO" 
                      placeholder="Corolla, Versa, etc." 
                      :disabled="guardandoPersona"
                    />
                  </div>

                  <!-- Año/Color/Capacidad removidos: la BD no los almacena actualmente -->
                </div>
              </div>
              
                <!-- Salud y Alimentación (agregado desde Formulario 2.vue) -->
                <div class="form-section">
                  <h3 class="section-title">
                    <AppIcons name="heart" :size="18" />
                    Salud y Alimentación
                  </h3>
                  <div class="form-grid">
                      <div class="form-field">
                        <label>Tipo de Alimentación</label>
                        <BaseSelect v-model="personaNueva.ALI_ID" :options="alimentacionOptions" :disabled="guardandoPersona" />
                      </div>
          
                      <div class="form-field full-width">
                        <label>Alergias / Enfermedades</label>
                        <InputBase v-model="personaNueva.PER_ALERGIA_ENFERMEDAD" :disabled="guardandoPersona" />
                      </div>
          
                      <div class="form-field full-width">
                        <label>Limitaciones</label>
                        <InputBase v-model="personaNueva.PER_LIMITACION" :disabled="guardandoPersona" />
                      </div>
          
                      <div class="form-field">
                        <label>Contacto Emergencia</label>
                        <InputBase v-model="personaNueva.PER_NOM_EMERGENCIA" :disabled="guardandoPersona" placeholder="María González" />
                      </div>
                      <div class="form-field">
                        <label>Tel. Emergencia</label>
                        <div class="phone-input-wrapper">
                          <span class="phone-prefix">+56</span>
                          <InputBase v-model="personaNueva.PER_FONO_EMERGENCIA" :disabled="guardandoPersona" placeholder="912345678" class="phone-input" />
                        </div>
                      </div>
          
                      <div class="form-field full-width">
                        <label>Ficha Médica (opcional)</label>
                        <InputBase v-model="personaNueva.FICHA_MEDICA" placeholder="Url o identificador de ficha" :disabled="guardandoPersona" />
                      </div>
                  </div>
                </div>

                

                <!-- Botón cancelar al final del formulario eliminado según request -->
            </form>
          </div>
        </template>
      </BaseModal>

      <!-- Small RUT Search Popup (opened before full 'Nueva Persona' modal) -->
      <BaseModal v-model="rutModalVisible" @close="cancelarRutPopup" class="persona-modal rut-search-modal">
        <template #default>
          <div class="modal-crear">
            <header class="modal-header-crear">
              <div class="header-title">
                <h2>Buscar por RUT</h2>
                <p class="subtitle">Ingrese RUT y presione Buscar. Si existe, irá a editar; si no, podrá crear una nueva persona.</p>
              </div>
              <div class="header-actions">
                <BaseButton class="btn-cancel btn-modal-header" type="button" variant="secondary" @click="cancelarRutPopup">
                  <AppIcons name="x" :size="16" /> Cancelar
                </BaseButton>
              </div>
            </header>

            <form @submit.prevent="buscarRutPopup" class="rut-form" style="padding:16px;">
              <div class="rut-row">
                <InputBase class="rut-input" v-model="rutPopup.run" placeholder="12345678" @input="calcularDvPopup" />
                <span class="rut-separator">-</span>
                <InputBase class="rut-dv" v-model="rutPopup.dv" placeholder="9" maxlength="1" />
                <BaseButton class="btn-search" type="submit" variant="primary" :disabled="rutPopup.searching || !rutPopup.run || rutPopupInvalido">
                  <AppIcons name="search" :size="14" /> Buscar
                </BaseButton>
              </div>
              <small v-if="rutPopupInvalido" class="error-message">⚠️ Debe ingresar un RUT válido</small>
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
                  class="btn-cancel btn-modal-header" 
                  type="button" 
                  variant="secondary" 
                  @click="cerrarModalImportar"
                  :disabled="importandoPersonas"
                >
                  <AppIcons name="x" :size="16" />
                  Cancelar
                </BaseButton>
                <BaseButton 
                  class="btn-import-header" 
                  type="button" 
                  variant="primary" 
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
                    <li><strong>Estado Civil:</strong> Escribe el nombre completo (Ej: "Soltero", "Casado", "Divorciado", "Viudo")</li>
                    <li><strong>Región, Provincia, Comuna, Grupo:</strong> Escribe el nombre completo (Ej: "Región del Biobío", "Concepción")</li>
                    <li><strong>Campos Sí/No:</strong> Vigente, Vigente en Grupo, Habilitación 1, Habilitación 2, Verificado - Escribe "Sí" o "No"</li>
                    <li>Completa los datos y sube el archivo</li>
                  </ul>
                  
                  <!-- Botón para descargar plantilla -->
                  <div class="template-download">
                    <BaseButton 
                      @click="descargarPlantillaExcel"
                      variant="primary"
                      class="btn-search btn-standard"
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

              <!-- Botón cancelar al final eliminado según request -->
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Exportación -->
      <BaseModal v-model="exportarModalVisible" @close="cerrarModalExportar" class="persona-modal modal-exportar-opciones">
        <template #default>
          <div class="modal-exportar">
            <header class="modal-header-exportar">
              <div class="header-title">
                <h2>Exportar Lista</h2>
                <p class="subtitle">Selecciona qué quieres exportar</p>
              </div>
              <div class="header-actions">
                <BaseButton class="btn-cancel btn-modal-header" type="button" variant="secondary" @click="cerrarModalExportar">
                  <AppIcons name="x" :size="16" /> Cerrar
                </BaseButton>
              </div>
            </header>
            <div class="export-options">
              <BaseButton class="btn-standard" variant="primary" @click="exportarExcel('todos')">
                <AppIcons name="table" :size="16" /> Exportar todos los datos
              </BaseButton>
              <BaseButton class="btn-standard" variant="secondary" @click="exportarExcel('emails')" style="margin-left:8px;">
                <AppIcons name="mail" :size="16" /> Solo correos electrónicos
              </BaseButton>
              <p class="hint">Se exporta la lista actualmente visible (según filtros).</p>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Modal de Recorte de Foto -->
      <BaseModal v-model="cropperVisible" @close="closeCropper" class="persona-modal modal-cropper-foto">
        <template #default>
          <div class="modal-cropper">
            <header class="modal-header-cropper">
              <div class="header-title">
                <h2><AppIcons name="image" :size="24" /> Ajustar Foto de Perfil</h2>
                <p class="subtitle">Selecciona la parte de la imagen que deseas usar</p>
              </div>
              <div class="header-actions">
                <BaseButton class="btn-cancel btn-modal-header" type="button" variant="secondary" @click="closeCropper">
                  <AppIcons name="x" :size="16" /> Cerrar
                </BaseButton>
              </div>
            </header>
            
            <div class="cropper-content">
              <!-- Vista previa circular -->
              <div class="cropper-preview-section">
                <div class="cropper-frame">
                  <img 
                    :src="cropperImageUrl" 
                    alt="Preview" 
                    class="cropper-image" 
                    :style="cropStyle()" 
                  />
                  <div class="cropper-mask"></div>
                </div>
                <p class="preview-hint">Vista previa del avatar</p>
              </div>

              <!-- Controles de ajuste -->
              <div class="cropper-controls">
                <div class="control-group">
                  <label class="control-label">
                    <AppIcons name="zoom-in" :size="16" />
                    Zoom
                  </label>
                  <div class="control-slider-wrapper">
                    <span class="slider-value">{{ Math.round((cropZoom - 0.5) / 2.5 * 100) }}%</span>
                    <input 
                      class="control-range" 
                      type="range" 
                      min="0.5" 
                      max="3" 
                      step="0.05" 
                      v-model.number="cropZoom" 
                    />
                  </div>
                </div>

                <div class="control-group">
                  <label class="control-label">
                    <AppIcons name="move-horizontal" :size="16" />
                    Posición Horizontal
                  </label>
                  <div class="control-slider-wrapper">
                    <input 
                      class="control-range" 
                      type="range" 
                      min="-200" 
                      max="200" 
                      step="1" 
                      v-model.number="cropOffsetX" 
                    />
                  </div>
                </div>

                <div class="control-group">
                  <label class="control-label">
                    <AppIcons name="move-vertical" :size="16" />
                    Posición Vertical
                  </label>
                  <div class="control-slider-wrapper">
                    <input 
                      class="control-range" 
                      type="range" 
                      min="-200" 
                      max="200" 
                      step="1" 
                      v-model.number="cropOffsetY" 
                    />
                  </div>
                </div>

                <div class="control-group upload-group">
                  <input 
                    ref="cropperFileInput" 
                    type="file" 
                    accept="image/png, image/jpeg, image/jpg" 
                    @change="changeImageInCropper" 
                    hidden 
                  />
                  <BaseButton 
                    type="button" 
                    class="btn-standard btn-upload" 
                    variant="secondary" 
                    @click="$refs.cropperFileInput?.click()"
                  >
                    <AppIcons name="upload" :size="16" /> Cargar otra imagen
                  </BaseButton>
                </div>
              </div>
            </div>

            <footer class="modal-footer-cropper">
              <BaseButton variant="secondary" class="btn-standard" @click="closeCropper">
                <AppIcons name="x" :size="16" /> Cancelar
              </BaseButton>
              <BaseButton variant="primary" class="btn-standard" @click="finalizeCrop">
                <AppIcons name="check" :size="16" /> Usar esta foto
              </BaseButton>
            </footer>
          </div>
        </template>
      </BaseModal>
    </div>
  </div>
</template>


<script>
import { defineAsyncComponent } from 'vue'
const InputBase = defineAsyncComponent(() => import('@/components/InputBase.vue'))
const BaseSelect = defineAsyncComponent(() => import('@/components/BaseSelect.vue'))
const BaseButton = defineAsyncComponent(() => import('@/components/BaseButton.vue'))
const BaseModal = defineAsyncComponent(() => import('@/components/BaseModal.vue'))
const AppIcons = defineAsyncComponent(() => import('@/components/icons/AppIcons.vue'))
import personasService from '@/services/personasService.js'
import mantenedoresService from '@/services/mantenedoresService.js'
import cursosService from '@/services/cursosService.js'
import authService from '@/services/authService.js'
import * as XLSX from 'xlsx'
import { usePermissions } from '@/composables/usePermissions'
import { ref, onMounted, nextTick } from 'vue'

// Helper to normalize keys to Uppercase (for frontend compatibility)
const toUpperKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj
  const newObj = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    const upperKey = key.toUpperCase()
    newObj[upperKey] = obj[key]
    // Keep original key if different
    if (upperKey !== key) newObj[key] = obj[key]
  }
  return newObj
}

export default {
  name: 'GestionPersonas',
  components: { InputBase, BaseSelect, BaseButton, BaseModal, AppIcons },
  setup() {
    const { isAdmin, canCreate, canEdit, canDelete, isReadOnly } = usePermissions()
    const filtrosColapsados = ref(false)
    const isMobile = ref(false)
    const toggleFiltros = async () => {
      filtrosColapsados.value = !filtrosColapsados.value
      // Recalcular altura disponible cuando se colapsan/expanden filtros.
      // Usar nextTick y un pequeño timeout para asegurar que el layout del DOM se haya estabilizado
      // (los headers sticky / scrollbars pueden cambiar posiciones asincrónicamente).
      try {
        await nextTick()
        if (window.__updateCardsViewportHeight) window.__updateCardsViewportHeight()
                // Pequeño delay adicional para manejar el reflow del navegador en algunos dispositivos
        setTimeout(() => {
          try { if (window.__updateCardsViewportHeight) window.__updateCardsViewportHeight() } catch { /* ignore */ }
        }, 80)
      } catch {
        /* ignore */
      }
    }
    const checkMobile = () => {
      try {
        // Preferir media query CSS por confiabilidad (breakpoint ligeramente más amplio para diseño móvil)
        if (window.matchMedia) {
          isMobile.value = window.matchMedia('(max-width: 880px)').matches
          return
        }
        // Respaldo: medir el ancho del contenedor/contenido principal cuando esté disponible
        const container = document.querySelector('.app-layout .main-content') || document.querySelector('.gestion-personas') || document.body
        const width = container?.clientWidth || window.innerWidth
        isMobile.value = width <= 880
      } catch {
        isMobile.value = window.innerWidth <= 880
      }
    }
    // Calcula la altura disponible para las tarjetas (debajo del .table-wrapper)
    const updateCardsViewportHeight = () => {
      try {
        const tw = document.querySelector('.table-wrapper')
        if (!tw) return
        const top = tw.getBoundingClientRect().top
        const available = Math.max(120, window.innerHeight - top - 16) // mínimo 120px
                // setear variable CSS en el elemento .table-wrapper (o en root)
        tw.style.setProperty('--cards-viewport-height', `${available}px`)
      } catch {
        // noop
      }
    }
    // Exponerla globalmente para que métodos del Options API la invoquen fácilmente
    window.__updateCardsViewportHeight = updateCardsViewportHeight
    onMounted(() => {
      checkMobile()
      window.addEventListener('resize', checkMobile)
      window.addEventListener('resize', updateCardsViewportHeight)
      // También escuchar cambios en media queries para mejor precisión
      try {
        const mq = window.matchMedia('(max-width: 880px)')
        const mqHandler = (e) => { isMobile.value = e.matches }
        mq.addEventListener ? mq.addEventListener('change', mqHandler) : mq.addListener(mqHandler)
      } catch {}
      // ejecutar una vez para inicializar tamaños
      updateCardsViewportHeight()
    })
    return {
      isAdmin,
      canCreate,
      canEdit,
      canDelete,
      isReadOnly,
      filtrosColapsados,
      isMobile,
      toggleFiltros
    }
  },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRama: '',
  selectedCourse: '',
  selectedCurso: '',
      roleOptions: [
        { value: '', label: 'Todos los roles' }
      ],
      ramaOptions: [
        { value: '', label: 'Todas las ramas' }
      ],
      ramasOptions: [],
      courseOptions: [
        { value: '', label: 'Todos los grupos' }
      ],
      gruposOptions: [],
      cargosOptions: [],
      alimentacionOptions: [],
      distritosOptions: [],
      zonasOptions: [],
      nivelesOptions: [],
      cursosOptions: [],
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
  confirmModalReactivarVisible: false,
  personaAReactivar: null,
  
  crearModalVisible: false,
  personaNueva: null,
  guardandoPersona: false,
  rutModalVisible: false,
  rutPopup: { run: '', dv: '', searching: false },
  rutPopupInvalido: false,
  
  importarModalVisible: false,
  exportarModalVisible: false,
  importandoPersonas: false,
  seleccionandoArchivo: false,
  archivoSeleccionado: null,
  datosVistaPreviaExcel: [],
  encabezadosExcel: [],
  
  esAdministrador: true,
  
  cropperVisible: false,
  cropperImageUrl: '',
  cropperModo: '',
  cropZoom: 1,
  cropOffsetX: 0,
  cropOffsetY: 0,
  
  rutNuevoInvalido: false,
  
    filtroAplicado: false,
    filteredPersonas: [],
    filtrandoEnProceso: false,
    currentFetchController: null,
    cargandoPersonas: false,
    errorCarga: null,
    personas: [],
    loadingMore: false,
    // Metadatos de caché de filtros (para evitar solicitudes lentas repetidas)
    filtersCachedAt: null,
          filtersCacheTTL: 1000 * 60 * 60 * 24, // 24 horas
      cargandoPersonasInFlight: false,
      cargandoFiltrosInFlight: false,
      latenciaMs: 0,
      latenciaDetalle: ''
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
      
      if (this.selectedCurso) {
        const cursoLabel2 = this.cursosOptions.find(c => c.value === this.selectedCurso)?.label || this.selectedCurso;
        filtros.push(`Inscrito: ${cursoLabel2}`);
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
      // Si no se ha aplicado el filtro, no mostrar nada
      if (!this.filtroAplicado) {
        return [];
      }
      // Si se aplicó el filtro, devolver el resultado (aunque esté vacío)
      return this.filteredPersonas;
    }
  },
  methods: {
    authReady() {
      try {
        const cookies = typeof document !== 'undefined' ? document.cookie : '';
        const hasCookieToken = /access_token=|token=|accessToken=/.test(cookies);
        const lsToken = typeof localStorage !== 'undefined' ? (localStorage.getItem('token') || localStorage.getItem('accessToken')) : null;
        return Boolean(hasCookieToken || lsToken);
      } catch { return false; }
    },
    abrirModalExportar() {
      if (!this.filtroAplicado || this.personasFiltradas.length === 0) {
        alert('No hay datos para exportar. Usa los filtros y presiona "Buscar" primero.');
        return;
      }
      this.exportarModalVisible = true;
    },
        ensureFiltrosLoaded() {
          // Evitar cargar mantenedores cuando no está autenticado para prevenir delays 401
          if (!this.authReady()) return;
          if (this.filtersCachedAt && (Date.now() - this.filtersCachedAt) < this.filtersCacheTTL) return;
          if (this.cargandoFiltrosInFlight) return;
          this.cargandoFiltrosInFlight = true;
          this.cargarOpcionesFiltros().finally(() => { this.cargandoFiltrosInFlight = false; });
        },
    cerrarModalExportar() {
      this.exportarModalVisible = false;
    },
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
      
      // Initialize multiple ramas array
      this.personaEditada.ramas = [];
      
      // Load 1:N Ramas/Niveles
      if (this.personaEditada.PER_ID) {
         try {
             // Fetch all levels/ramas
             const nivelesAll = await personasService.niveles.list();
             // Filter for this person
             const misNiveles = nivelesAll.filter(n => Number(n.PER_ID) === Number(this.personaEditada.PER_ID));
             
             if (misNiveles.length > 0) {
                 this.personaEditada.ramas = misNiveles.map(n => ({
                     PEN_ID: n.PEN_ID, // keep ID for updates
                     NIV_ID: n.NIV_ID,
                     RAM_ID_NIVEL: n.RAM_ID
                 }));
             } else {
                 // Try to use legacy/flat properties if no 1:N records found
                 if (this.personaEditada.NIV_ID || this.personaEditada.RAM_ID || this.personaEditada.PER_RAMA) {
                      this.personaEditada.ramas.push({
                          NIV_ID: this.personaEditada.NIV_ID,
                          RAM_ID_NIVEL: this.personaEditada.RAM_ID // or resolve from PER_RAMA if needed
                      });
                 }
             }
         } catch (e) {
             console.warn('Error loading niveles for person:', e);
         }
      }
      // Ensure at least one row if empty and not readonly (optional, or just show empty list)
      if (!soloLectura && this.personaEditada.ramas.length === 0) {
          this.personaEditada.ramas.push({ NIV_ID: '', RAM_ID_NIVEL: '' });
      }

       // Cargar cursos de la persona
       if (this.personaEditada.PER_ID) {
         try {
           const cursosData = await personasService.obtenerCursosPersona(this.personaEditada.PER_ID);
           this.personaEditada.cursosHistorial = cursosData || [];
         } catch {
           this.personaEditada.cursosHistorial = [];
         }
       } else {
         this.personaEditada.cursosHistorial = [];
       }
      
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      // Asegurar propiedades nuevas del formulario (compatibilidad)
      const defaults = {
        ALI_ID: this.personaEditada.ALI_ID || '',
        FICHA_MEDICA: this.personaEditada.FICHA_MEDICA || null,
        TIENE_VEHICULO: this.personaEditada.TIENE_VEHICULO !== undefined ? this.personaEditada.TIENE_VEHICULO : false,
        REQUIERE_ALOJAMIENTO: this.personaEditada.REQUIERE_ALOJAMIENTO !== undefined ? this.personaEditada.REQUIERE_ALOJAMIENTO : false,
        TRABAJA_CON_NNAJ: this.personaEditada.TRABAJA_CON_NNAJ !== undefined ? this.personaEditada.TRABAJA_CON_NNAJ : false,
        BENEFICIARIO: this.personaEditada.BENEFICIARIO !== undefined ? this.personaEditada.BENEFICIARIO : false,
        RANGO_EDAD_NNAJ: this.personaEditada.RANGO_EDAD_NNAJ || ''
      };
      // Asegurar que existan las claves de vehículo para evitar undefined durante ediciones
      Object.assign(defaults, {
        PEV_PATENTE: this.personaEditada.PEV_PATENTE || '',
        PEV_MARCA: this.personaEditada.PEV_MARCA || '',
        PEV_MODELO: this.personaEditada.PEV_MODELO || '',
        // Campos de vehículo: solo mantener los almacenados en BD (patente, marca, modelo)
      });
      this.personaEditada = Object.assign({}, this.personaEditada, defaults);
      this.newHistEntry = { fecha: '', descripcion: '' };
      this.modalTab = 'info';
      this.modoSoloLectura = soloLectura;
      this.editModalVisible = true;
      this.personaSeleccionada = persona;
      this.pendingSave = false;
      
      // Si tiene COM_ID pero falta REG_ID o PRO_ID, intentar inferirlos
      if (this.personaEditada.COM_ID && (!this.personaEditada.REG_ID || !this.personaEditada.PRO_ID)) {
        try {
            // ... (inference logic elided for brevity if unchanged, but included if needed to match context)
             // Preferir opciones en caché existentes; recurrir a API solo si está vacío
          let comunas = Array.isArray(this.comunaOptionsEditar) && this.comunaOptionsEditar.length
                      ? this.comunaOptionsEditar.map(c => ({ COM_ID: c.value, PRO_ID: c.PRO_ID }))
            : null;
          if (!comunas || comunas.length === 0) {
            try { comunas = await mantenedoresService.comuna.list(); } catch { comunas = []; }
          }
          const comunaActual = (comunas || []).find(c => c.COM_ID === this.personaEditada.COM_ID);
          if (comunaActual && !this.personaEditada.PRO_ID) {
            this.personaEditada.PRO_ID = comunaActual.PRO_ID;
          }
          // Inferir región desde provincia si falta
          if ((this.personaEditada.PRO_ID) && !this.personaEditada.REG_ID) {
            // Provincias: usar solo opciones en caché; omitir llamadas al backend para evitar error 500
            let provincias = Array.isArray(this.provinciaOptionsEditar) && this.provinciaOptionsEditar.length
              ? this.provinciaOptionsEditar.map(p => ({ PRO_ID: p.value, REG_ID: p.REG_ID }))
              : (Array.isArray(this.provinciaOptions) && this.provinciaOptions.length
                  ? this.provinciaOptions.map(p => ({ PRO_ID: p.value, REG_ID: p.REG_ID }))
                  : []);
            const provinciaActual = (provincias || []).find(p => p.PRO_ID === this.personaEditada.PRO_ID);
            if (provinciaActual) {
              this.personaEditada.REG_ID = provinciaActual.REG_ID;
            }
          }
        } catch { /* warn suppressed */ }
      }
      
      // Cargar cascada
      try {
        if (this.personaEditada.REG_ID) await this.cargarProvinciasPorRegionEditar();
        if (this.personaEditada.PRO_ID) await this.cargarComunasPorProvinciaEditar();
      } catch { /* ignore */ }
    },


    navegarACurso(cursoId) {
      // Navegar a la vista de cursos con el curso seleccionado
      this.$router.push({ 
        name: 'cursoscapacitaciones', 
        query: { cursoId: cursoId } 
      });
    },
    
    navegarAPagos(cursoId, persona) {
      // Navegar a la vista de pagos con filtros aplicados
      // Construir el texto de búsqueda con el nombre completo de la persona
      const nombreCompleto = `${persona.PER_NOMBRES || ''} ${persona.PER_APELPTA || ''} ${persona.PER_APELMAT || ''}`.trim();
      
      this.$router.push({ 
        name: 'pagos', 
        query: { 
          personaQuery: nombreCompleto || persona.PER_RUN,
          cursoId: cursoId,
          autoSearch: 'true'
        } 
      });
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
    filtrar({ immediate = true } = {}) {
      // Debounce cuando se llama desde tipeo; ejecutar inmediatamente al presionar Buscar
      if (!immediate) {
        clearTimeout(this._debounceTimer);
        this._debounceTimer = setTimeout(() => this.filtrar({ immediate: true }), 150);
        return;
      }
      if (this.filtrandoEnProceso) return;
      this.filtrandoEnProceso = true;
      (async () => {
        await this.ejecutarFiltrado();
        try { if (this.isMobile) this.filtrosColapsados = true } catch {}
        try { if (window.__updateCardsViewportHeight) window.__updateCardsViewportHeight() } catch {}
        this.filtrandoEnProceso = false;
      })();
    },
    async ejecutarFiltrado() {
      // Cancelar petición anterior si existe
      if (this.currentFetchController) {
        this.currentFetchController.abort();
      }
      const controller = new AbortController();
      this.currentFetchController = controller;
      const t0 = performance && performance.now ? performance.now() : Date.now();
      
      const q = (this.searchQuery || '').toLowerCase().trim();
      // Values are now IDs (or empty strings)
      const selectedRole = this.selectedRole;
      const selectedRama = this.selectedRama;
      const selectedGroup = this.selectedCourse; // selectedCourse is actually Group ID in this component context
      const selectedCurso = this.selectedCurso; // Enrollment Course ID

      const tieneAlgunFiltro = q || selectedRole || selectedRama || selectedGroup || selectedCurso;
      
      if (!tieneAlgunFiltro) {
        alert('Debe usar al menos un filtro para buscar (nombre/RUT/email, rol, rama o grupo).');
        return;
      }

      this.filtroAplicado = true;
      this.personaSeleccionada = null;

      // Server-side filtering parameters
      // IMPORTANT: Use lowercase snake_case for backend compatibility
      const params = {};
      if (q) params.search = q; // 'q' often maps to 'search' in DRF, or keep 'q' if custom
      if (selectedRole) params.rol_id = selectedRole;
      if (selectedRama) params.ram_id = selectedRama;
      if (selectedGroup) params.gru_id = selectedGroup;
      if (selectedCurso) params.cur_id = selectedCurso;
      
      params.page_size = 50; // Increased page size

      const cacheKey = `gs_personas_filtered_v2:${JSON.stringify(params)}`;
      const nowTs = Date.now();
      try {
        const cached = JSON.parse(localStorage.getItem(cacheKey) || 'null');
        if (cached && (nowTs - cached.ts) < 2 * 60 * 1000) { // TTL de 2 minutos
          this.personas = cached.data;
          this.filteredPersonas = cached.data;
          this.enrichPersonas(); // Ensure display names are mapped
          this.currentFetchController = null;
          return;
        }
      } catch {}

      let fetched = [];
      let tFetchEnd = t0;
      try {
        const resp = await personasService.personas.list(params, { signal: controller.signal });
        tFetchEnd = performance && performance.now ? performance.now() : Date.now();
        const rawList = Array.isArray(resp) ? resp : (resp && Array.isArray(resp.results) ? resp.results : []);
        
        // Helper to convert keys to uppercase
        const toUpperKeys = (obj) => {
          if (!obj || typeof obj !== 'object') return obj;
          const newObj = Array.isArray(obj) ? [] : {};
          for (const key in obj) {
            const upperKey = key.toUpperCase();
            newObj[upperKey] = obj[key];
            if (upperKey !== key) newObj[key] = obj[key];
          }
          return newObj;
        };
        // Normalize immediately
        fetched = rawList.map(toUpperKeys);
      } catch (e) {
        if (e.name !== 'AbortError') fetched = [];
      }

      // Client-side fallback filtering
      if (fetched.length) {
        const qLower = q;
        fetched = fetched.filter(p => {
          // Filtering logic
          const nombre = (p.PER_NOMBRES || '').toLowerCase();
          const apellidoPat = (p.PER_APELPTA || p.PER_APELPAT || '').toLowerCase();
          const apellidoMat = (p.PER_APELMAT || '').toLowerCase();
          const nombreCompleto = `${nombre} ${apellidoPat} ${apellidoMat}`.trim();
          const rutStr = (p.PER_RUN || '').toString().toLowerCase();
          const emailStr = (p.PER_MAIL || p.PER_EMAIL || '').toLowerCase();

          const coincideBusqueda = !qLower || nombreCompleto.includes(qLower) || rutStr.includes(qLower) || emailStr.includes(qLower);

          // ID comparisons (loose for string vs number)
          // Ensure p properties exist (backend should send them)
          const coincideRol = !selectedRole || p.ROL_ID == selectedRole || p.PER_ROL == selectedRole; 
          const coincideRama = !selectedRama || p.RAM_ID == selectedRama || p.PER_RAMA == selectedRama;
          const coincideGrupo = !selectedGroup || p.GRU_ID == selectedGroup || p.PER_GRUPO == selectedGroup;
          
          // For course enrollment, we might need to check p.cursos array or p.CUR_ID if returned flattened
          // Assuming flattened or p.cursos check:
          let coincideCurso = !selectedCurso;
          if (selectedCurso && !coincideCurso) {
             if (p.CUR_ID == selectedCurso) coincideCurso = true;
             else if (Array.isArray(p.CURSOS) && p.CURSOS.some(c => c.CUR_ID == selectedCurso)) coincideCurso = true;
             else if (Array.isArray(p.cursos) && p.cursos.some(c => c.CUR_ID == selectedCurso)) coincideCurso = true;
          }

          return coincideBusqueda && coincideRol && coincideRama && coincideGrupo && coincideCurso;
        });
      }

      const tProcessEnd = performance && performance.now ? performance.now() : Date.now();
      this.latenciaMs = Math.round((tFetchEnd - t0));
      this.latenciaDetalle = `red: ${Math.round(tFetchEnd - t0)}ms, proc: ${Math.round(tProcessEnd - tFetchEnd)}ms`;
      
      this.personas = fetched; // Update main list
      this.enrichPersonas(); // Apply display mappings
      this.filteredPersonas = this.personas; // Update filtered list AFTER enrichment
      
      try { localStorage.setItem(cacheKey, JSON.stringify({ ts: nowTs, data: this.personas })); } catch {}
      this.currentFetchController = null;
      
      this.$nextTick(() => {
        const el = document.querySelector('.table-wrapper');
        if (el && typeof el.scrollIntoView === 'function') el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    },
    enrichPersonas() {
      // This is now mostly redundant if we normalize upstream, but kept for compatibility and formatting
      const now = new Date().toISOString();
      const roleMap = new Map((this.roleOptions || []).map(r => [String(r.value), r.label]));
      const ramaMap = new Map((this.ramaOptions || []).map(r => [String(r.value), r.label]));
      // Note: Groups might need similar mapping if displayed, but table doesn't show them currently.

      this.personas = (this.personas || []).map((p, idx) => {
        // p is already toUpperKeys normalized from fetch
        
        // Ensure IDs are present
        const per_id = Number(p.PER_ID || (idx + 1));
        const rol_id = p.ROL_ID || p.rol_id;
        const per_rol_orig = p.PER_ROL || p.per_rol;
        
        // Resolve Role Name: Try mapping ID -> Label, otherwise fallback to original string
        let resolvedRol = per_rol_orig;
        if (rol_id && roleMap.has(String(rol_id))) {
          resolvedRol = roleMap.get(String(rol_id));
        } else if (per_rol_orig && roleMap.has(String(per_rol_orig))) {
           // If original was already an ID
           resolvedRol = roleMap.get(String(per_rol_orig));
        }

        return {
          ...p,
          PER_ID: per_id,
          // Ensure display strings if only IDs are present (optional, can be done in template via lookups)
          // But preserving original logic:
          PER_NOMBRES: p.PER_NOMBRES || '',
          PER_APELPTA: p.PER_APELPTA || p.PER_APELPAT || '',
          PER_APELMAT: p.PER_APELMAT || '',
          PER_RUN: p.PER_RUN,
          PER_DV: p.PER_DV,
          PER_MAIL: p.PER_MAIL || p.PER_EMAIL || '',
          PER_ROL: resolvedRol || 'Sin rol', // Display resolved name
          ROL_ID: rol_id,
          RAM_ID: p.RAM_ID || p.ram_id,
          GRU_ID: p.GRU_ID || p.gru_id,
          PER_VIGENTE: p.PER_VIGENTE !== undefined ? p.PER_VIGENTE : true,
          // ... preserve others, adding resolved names for Rama/Grupo if needed for future
          RAM_NOMBRE: (p.RAM_ID && ramaMap.has(String(p.RAM_ID))) ? ramaMap.get(String(p.RAM_ID)) : (p.PER_RAMA || ''),
        };
      });
    },
    exportarExcel(tipo = 'todos') {
      const datos = this.personasFiltradas.map((p) => {
        // Buscar nombres descriptivos
        const regionNombre = this.regionOptions.find(r => r.value === p.REG_ID)?.label || '';
        const provinciaNombre = this.provinciaOptions.find(pr => pr.value === p.PRO_ID)?.label || '';
        const comunaNombre = this.comunaOptions.find(c => c.value === p.COM_ID)?.label || '';
        const estadoCivilNombre = this.estadoCivilOptions.find(ec => ec.value === p.ESC_ID)?.label || '';
        const grupoNombre = this.gruposOptions.find(g => g.value === p.GRU_ID)?.label || '';
        if (tipo === 'emails') {
          return {
            'ID': p.PER_ID || '',
            'Nombre': `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim(),
            'Email': p.PER_MAIL || ''
          };
        }
        return {
          'ID': p.PER_ID || '',
          'Nombres': p.PER_NOMBRES || '',
          'Apellido Paterno': p.PER_APELPTA || '',
          'Apellido Materno': p.PER_APELMAT || '',
          'RUT': p.PER_RUN || '',
          'DV': p.PER_DV || '',
          'Email': p.PER_MAIL || '',
          'Fecha de Nacimiento': p.PER_FECHA_NAC || '',
          'Dirección': p.PER_DIRECCION || '',
          'Región': regionNombre,
          'Provincia': provinciaNombre,
          'Comuna': comunaNombre,
          'Tipo de Teléfono': p.PER_TIPO_FONO === 1 ? 'Fijo' : (p.PER_TIPO_FONO === 2 ? 'Celular' : ''),
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
          'Grupo': grupoNombre,
          'Vigente en Grupo': p.PEG_VIGENTE !== undefined ? (p.PEG_VIGENTE ? 'Sí' : 'No') : '',
          'Estado Civil': estadoCivilNombre,
          'Habilitación 1': p.PEF_HAB_1 !== undefined ? (p.PEF_HAB_1 ? 'Sí' : 'No') : '',
          'Habilitación 2': p.PEF_HAB_2 !== undefined ? (p.PEF_HAB_2 ? 'Sí' : 'No') : '',
          'Verificado': p.PEF_VERIF !== undefined ? (p.PEF_VERIF ? 'Sí' : 'No') : '',
          'Vigente': p.PER_VIGENTE !== undefined ? (p.PER_VIGENTE ? 'Sí' : 'No') : 'Sí'
        };
      });

      const ws = XLSX.utils.json_to_sheet(datos);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, tipo === 'emails' ? 'Emails' : 'Personas');
      
      const fecha = new Date().toISOString().split('T')[0];
      const nombre = tipo === 'emails' ? `Emails_${fecha}.xlsx` : `Personas_${fecha}.xlsx`;
      XLSX.writeFile(wb, nombre);
      this.cerrarModalExportar();
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
        /* log suppressed */
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
          /* error suppressed */
          this.guardandoPersona = false;
          return;
        }
        
        /* logs suppressed */
        
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
        
        // Convertir payload a minúsculas (snake_case)
        const datosActualizados = {
          per_nombres: this.personaEditada.PER_NOMBRES,
          per_apelpta: this.personaEditada.PER_APELPTA || '',
          per_apelmat: this.personaEditada.PER_APELMAT || '',
          per_run: this.personaEditada.PER_RUN,
          per_dv: this.personaEditada.PER_DV,
          per_mail: this.personaEditada.PER_MAIL || '',
          per_fecha_nac: this.personaEditada.PER_FECHA_NAC || null,
          per_direccion: this.personaEditada.PER_DIRECCION || null,
          per_tipo_fono: this.personaEditada.PER_TIPO_FONO || 2,
          per_fono: this.personaEditada.PER_FONO ? '+56' + this.personaEditada.PER_FONO.replace(/^\+56/, '') : null,
          per_apodo: this.personaEditada.PER_APODO || null,
          per_profesion: this.personaEditada.PER_PROFESION || null,
          per_rol: this.personaEditada.PER_ROL || null,
          per_nom_emergencia: this.personaEditada.PER_NOM_EMERGENCIA || null,
          per_fono_emergencia: this.personaEditada.PER_FONO_EMERGENCIA ? '+56' + this.personaEditada.PER_FONO_EMERGENCIA.replace(/^\+56/, '') : null,
          per_alergia_enfermedad: this.personaEditada.PER_ALERGIA_ENFERMEDAD || null,
          per_limitacion: this.personaEditada.PER_LIMITACION || null,
          per_religion: this.personaEditada.PER_RELIGION || null,
          per_tiempo_nnaj: this.personaEditada.PER_TIEMPO_NNAJ || null,
          per_tiempo_adulto: this.personaEditada.PER_TIEMPO_ADULTO || null,
          per_num_mma: this.personaEditada.PER_NUM_MMA || null,
          per_otros: this.personaEditada.PER_OTROS || null,
          esc_id: this.personaEditada.ESC_ID && this.personaEditada.ESC_ID !== '' ? Number(this.personaEditada.ESC_ID) : 1,
          reg_id: this.personaEditada.REG_ID && this.personaEditada.REG_ID !== '' ? Number(this.personaEditada.REG_ID) : null,
          pro_id: this.personaEditada.PRO_ID && this.personaEditada.PRO_ID !== '' ? Number(this.personaEditada.PRO_ID) : null,
          com_id: this.personaEditada.COM_ID && this.personaEditada.COM_ID !== '' ? Number(this.personaEditada.COM_ID) : 1,
          per_vigente: this.personaEditada.PER_VIGENTE !== undefined ? this.personaEditada.PER_VIGENTE : true,
          tiene_vehiculo: this.personaEditada.TIENE_VEHICULO !== undefined ? this.personaEditada.TIENE_VEHICULO : false
        };
        
        try {
          await personasService.personas.partialUpdate(
            this.personaEditada.PER_ID, 
            datosActualizados
          );
        } catch (updateError) {
          console.error('Error al actualizar persona:', updateError);
          if (updateError.response && updateError.response.data) {
            console.error('Detalles del error:', updateError.response.data);
            const errores = updateError.response.data;
            let mensajeDetallado = 'Error al actualizar:\n\n';
            
            if (typeof errores === 'object') {
              for (const [campo, mensajes] of Object.entries(errores)) {
                const msg = Array.isArray(mensajes) ? mensajes.join(', ') : mensajes;
                mensajeDetallado += `${campo}: ${msg}\n`;
              }
            } else {
              mensajeDetallado += errores;
            }
            
            alert(mensajeDetallado);
          } else {
            alert('Error al actualizar la persona. Por favor verifica los datos e intenta nuevamente.');
          }
          throw updateError;
        }
        
        const personaId = this.personaEditada.PER_ID;
        
        // Actualizar/Crear Grupo Scout
        if (this.personaEditada.GRU_ID && this.personaEditada.GRU_ID !== '') {
          try {
            const gruposActuales = await personasService.grupos.list();
            const grupoPersona = gruposActuales.find(g => g.per_id === personaId || g.PER_ID === personaId);
            
            const grupoData = {
              gru_id: Number(this.personaEditada.GRU_ID),
              peg_vigente: this.personaEditada.PEG_VIGENTE !== undefined ? this.personaEditada.PEG_VIGENTE : true
            };
            
            if (grupoPersona) {
              await personasService.grupos.partialUpdate(grupoPersona.peg_id || grupoPersona.PEG_ID, grupoData);
              /* log suppressed */
            } else {
              await personasService.grupos.create({
                per_id: personaId,
                ...grupoData
              });
              /* log suppressed */
            }
          } catch {
            /* warn suppressed */
          }
        }
        
        // Actualizar/Crear Datos de Formador
        if (this.personaEditada.PEF_HAB_1 !== '' || this.personaEditada.PEF_HAB_2 !== '' || this.personaEditada.PER_ROL) {
          try {
            const formadoresActuales = await personasService.formadores.list();
            const formadorPersona = formadoresActuales.find(f => f.PER_ID === personaId);
            
            const formadorData = {
              PEF_HAB_1: this.personaEditada.PEF_HAB_1 || null,
              PEF_HAB_2: this.personaEditada.PEF_HAB_2 || null,
              PEF_VERIF: this.personaEditada.PEF_VERIF !== undefined ? this.personaEditada.PEF_VERIF : false,
              PEF_HISTORIAL: this.personaEditada.PEF_HISTORIAL || null
            };
            
            if (formadorPersona) {
              await personasService.formadores.partialUpdate(formadorPersona.PEF_ID, formadorData);
              /* log suppressed */
            } else {
              await personasService.formadores.create({
                PER_ID: personaId,
                ...formadorData
              });
              /* log suppressed */
            }
          } catch {
            /* warn suppressed */
          }
        }
        
        // Actualizar/Crear Información Individual
        if (this.personaEditada.CAR_ID || this.personaEditada.DIS_ID || this.personaEditada.ZON_ID) {
          try {
            const individualesActuales = await personasService.individuales.list();
            const individualPersona = individualesActuales.find(i => i.PER_ID === personaId);
            
            const individualData = {
              CAR_ID: this.personaEditada.CAR_ID && this.personaEditada.CAR_ID !== '' ? Number(this.personaEditada.CAR_ID) : null,
              DIS_ID: this.personaEditada.DIS_ID && this.personaEditada.DIS_ID !== '' ? Number(this.personaEditada.DIS_ID) : null,
              ZON_ID: this.personaEditada.ZON_ID && this.personaEditada.ZON_ID !== '' ? Number(this.personaEditada.ZON_ID) : null,
              PEI_VIGENTE: this.personaEditada.PEI_VIGENTE !== undefined ? this.personaEditada.PEI_VIGENTE : true
            };
            
            if (individualPersona) {
              await personasService.individuales.partialUpdate(individualPersona.PEI_ID, individualData);
              /* log suppressed */
            } else {
              await personasService.individuales.create({
                PER_ID: personaId,
                ...individualData
              });
              /* log suppressed */
            }
          } catch {
            /* warn suppressed */
          }
        }
        
        // Actualizar/Crear Nivel y Rama (Múltiples 1:N)
        if (this.personaEditada.ramas && this.personaEditada.ramas.length > 0) {
          try {
             // 1. Obtener registros actuales de BD
            const allNiveles = await personasService.niveles.list();
             // Filtrar por ID de persona (asegurar compatibilidad de tipos)
            const nivelesActuales = allNiveles.filter(n => Number(n.PER_ID || n.per_id) === Number(personaId));
            
             // 2. Identificar IDs que permanecen en la UI
            const uiIds = this.personaEditada.ramas
                .map(r => r.PEN_ID)
                .filter(id => id); // solo los que tienen ID definido
            
             // 3. Eliminar los que ya no están en la UI
            for (const nivelDB of nivelesActuales) {
                const dbId = nivelDB.PEN_ID || nivelDB.pen_id;
                if (!uiIds.includes(dbId)) {
                    await personasService.niveles.remove(dbId);
                }
            }

             // 4. Crear o Actualizar según corresponda
            for (const ramaUI of this.personaEditada.ramas) {
                 const payload = {
                     per_id: personaId,
                     niv_id: ramaUI.NIV_ID ? Number(ramaUI.NIV_ID) : 1, 
                     ram_id: ramaUI.RAM_ID_NIVEL ? Number(ramaUI.RAM_ID_NIVEL) : null
                 };
                 
                 // Fallback para RAM_ID si viene vacío pero había texto legado (menos probable en edit, pero por seguridad)
                 if (!payload.ram_id && this.personaEditada.PER_RAMA) {
                      if (!this._cachedRamasToId) {
                         try { this._cachedRamasToId = await mantenedoresService.rama.list(); } catch { this._cachedRamasToId = []; }
                      }
                      const rFound = this._cachedRamasToId.find(r => r.RAM_DESCRIPCION === this.personaEditada.PER_RAMA);
                      if (rFound) payload.ram_id = rFound.RAM_ID;
                 }


                 if (ramaUI.PEN_ID) {
                      // Update existing
                     await personasService.niveles.partialUpdate(ramaUI.PEN_ID, payload);
                 } else {
                      // Create new
                      if (payload.niv_id || payload.ram_id) {
                         await personasService.niveles.create(payload);
                      }
                 }
            }
          } catch (e) { console.warn('Error sincronizando niveles:', e); }
        } else if ((this.personaEditada.NIV_ID && this.personaEditada.NIV_ID !== '') || this.personaEditada.PER_RAMA) {
             // Fallback legado si el array ramas está vacío (pero hay datos planos)
            try {
             const nivelesActuales = await personasService.niveles.list();
             const nivelPersona = nivelesActuales.find(n => Number(n.PER_ID) === Number(personaId));
             
             const ramId = this.personaEditada.RAM_ID_NIVEL ? Number(this.personaEditada.RAM_ID_NIVEL) : null;
             /* ... lógica de inferencia eliminada por brevedad, asumiendo datos directos ... */
             
              const nivelesData = {
                per_id: personaId,
                niv_id: this.personaEditada.NIV_ID ? Number(this.personaEditada.NIV_ID) : 1,
                ram_id: ramId
              };

              if (nivelPersona) {
                await personasService.niveles.partialUpdate(nivelPersona.PEN_ID || nivelPersona.pen_id, nivelesData);
              } else {
                await personasService.niveles.create(nivelesData);
              }
            } catch { /* ignore */ }
        }

        // Actualizar/Crear Persona_Curso para persistir ALI_ID (Tipo de Alimentación)
        try {
          const personaCursosActuales = await personasService.personaCursos.list();
          const cursoPersona = personaCursosActuales.find(c => Number(c.PER_ID) === Number(personaId));

          const aliIdToSet = this.personaEditada.ALI_ID && this.personaEditada.ALI_ID !== '' ? Number(this.personaEditada.ALI_ID) : null;

          if (cursoPersona) {
            if (aliIdToSet !== null && Number(cursoPersona.ALI_ID) !== aliIdToSet) {
              await personasService.personaCursos.partialUpdate(cursoPersona.PEC_ID, { ALI_ID: aliIdToSet });
              /* log suppressed */
            }
          } else if (aliIdToSet !== null) {
            // Intentar crear Persona_Curso si existe CUS_ID o PER tiene CUS_ID asignado
            const cusIdToUse = this.personaEditada.CUS_ID && this.personaEditada.CUS_ID !== '' ? Number(this.personaEditada.CUS_ID) : null;
            let rolIdToUse = null;
            if (this.personaEditada.PER_ROL) {
              try {
                const rolesList = await mantenedoresService.rol.list();
                const rolFound = rolesList.find(r => r.ROL_DESCRIPCION === this.personaEditada.PER_ROL || String(r.ROL_ID) === String(this.personaEditada.PER_ROL));
                if (rolFound) rolIdToUse = rolFound.ROL_ID;
              } catch {
                /* warn suppressed */
              }
            }

            if (cusIdToUse && rolIdToUse) {
              try {
                await personasService.personaCursos.create({ PER_ID: personaId, CUS_ID: cusIdToUse, ROL_ID: rolIdToUse, ALI_ID: aliIdToSet });
                /* log suppressed */
              } catch {
                /* warn suppressed */
              }
            }
          }
        } catch {
          /* warn suppressed */
        }
        
        // Actualizar/Crear Vehículo (ahora requiere PEC_ID desde Persona_Curso)
        if (this.personaEditada.PEV_PATENTE && this.personaEditada.PEV_PATENTE !== '') {
          try {
            // Buscar curso asociado a la persona (Persona_Curso)
            const cursosActuales = await personasService.personaCursos.list();
            const cursoPersona = cursosActuales.find(c => Number(c.PER_ID) === Number(personaId));

            let pecId = cursoPersona ? cursoPersona.PEC_ID : null;

            // Si no existe curso y hay información de rol/curso, intentar crear Persona_Curso
            if (!pecId) {
              const cusIdToUse = this.personaEditada.CUS_ID && this.personaEditada.CUS_ID !== '' ? Number(this.personaEditada.CUS_ID) : null;
              // intentar resolver ROL_ID desde descripción PER_ROL
              let rolIdToUse = null;
              if (this.personaEditada.PER_ROL) {
                try {
                  const rolesList = await mantenedoresService.rol.list();
                  const rolFound = rolesList.find(r => r.ROL_DESCRIPCION === this.personaEditada.PER_ROL || String(r.ROL_ID) === String(this.personaEditada.PER_ROL));
                  if (rolFound) rolIdToUse = rolFound.ROL_ID;
                } catch {
                  /* warn suppressed */
                }
              }
              // fallback a primer rol disponible
              if (!rolIdToUse) {
                try {
                                  const rolesList = await mantenedoresService.rol.list();
                  if (rolesList && rolesList.length) rolIdToUse = rolesList[0].ROL_ID;
                } catch {
                  // dejar rolIdToUse nulo si fallo
                }
              }

              if (cusIdToUse && rolIdToUse) {
                const nuevoCurso = await personasService.personaCursos.create({ PER_ID: personaId, CUS_ID: cusIdToUse, ROL_ID: rolIdToUse });
                pecId = nuevoCurso.PEC_ID;
                /* log suppressed */
              } else {
                /* warn suppressed */
              }
            }

            if (pecId) {
              // Buscar vehículo por PEC_ID
              const vehiculosActuales = await personasService.vehiculos.list();
              const vehiculoPersona = vehiculosActuales.find(v => Number(v.PEC_ID) === Number(pecId));

              // Construir payload con los campos que existen en el backend
              const vehPayload = {
                PEC_ID: pecId,
                PEV_PATENTE: this.personaEditada.PEV_PATENTE || '',
                PEV_MARCA: this.personaEditada.PEV_MARCA || '',
                PEV_MODELO: this.personaEditada.PEV_MODELO || ''
              };

              if (vehiculoPersona) {
                // En update no enviamos PEC_ID en el body (se usa en la URL)
                const updatePayload = {
                  PEV_PATENTE: vehPayload.PEV_PATENTE,
                  PEV_MARCA: vehPayload.PEV_MARCA,
                  PEV_MODELO: vehPayload.PEV_MODELO
                };
                await personasService.vehiculos.partialUpdate(vehiculoPersona.PEV_ID, updatePayload);
                /* log suppressed */
              } else {
                await personasService.vehiculos.create(vehPayload);
                /* log suppressed */
              }
            }
          } catch {
            /* warn suppressed */
          }
        }
        
        /* log suppressed */
        await this.cargarPersonas(true);
        // Forzar recarga de filtros para actualizar cache inmediatamente
        try { await this.cargarOpcionesFiltros(true); } catch{ /* warn suppressed */ }
        
        if (this.filtroAplicado) {
          /* log suppressed */
          await this.filtrar();
        }
        
        this.editModalVisible = false;
        this.personaEditada = null;
        this.personaSeleccionada = null;
        
        alert('✅ Persona actualizada exitosamente!');
        
      } catch (error) {
        /* errors suppressed */
        
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
          /* error suppressed */
        } else if (error.status === 404) {
          mensajeError += 'Persona no encontrada.';
        } else if (error.status === 500) {
          mensajeError += 'Error interno del servidor.';
        }
        
        
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
      
      /* log suppressed */
      
      try {
        /* logs suppressed */
        
        const datosAnulacion = {
          PER_VIGENTE: false
        };
        
        /* log suppressed */
        
        await personasService.personas.partialUpdate(this.personaAAnular.PER_ID, datosAnulacion);
        
        /* logs suppressed */
        
        
        
        this.confirmModalAnularVisible = false;
        this.personaAAnular = null;
        
      } catch {
        /* error suppressed */
        
        return;
      }
      
      try {
        /* log suppressed */
        await this.cargarPersonas(true);
        
        if (this.filtroAplicado) {
          /* log suppressed */
          await this.filtrar();
        }
      } catch {
        /* warn suppressed */
      }
      
      /* log suppressed */
    },
    
    reactivarPersona(persona) {
      this.personaAReactivar = persona;
      this.confirmModalReactivarVisible = true;
    },
    
    cancelarReactivacion() {
      this.confirmModalReactivarVisible = false;
      this.personaAReactivar = null;
    },
    
    async confirmarReactivacion() {
      if (!this.personaAReactivar) return;
      
      try {
        
        
        
        const datosReactivacion = {
          PER_VIGENTE: true
        };
        
        
        
        await personasService.personas.partialUpdate(this.personaAReactivar.PER_ID, datosReactivacion);
        
        
        
        
        
        this.confirmModalReactivarVisible = false;
        this.personaAReactivar = null;
        
      } catch (error) {
        console.error('❌ Error al reactivar persona:', error);
        
        let mensajeError = 'Error al reactivar la persona. ';
        if (error.message) {
          mensajeError += error.message;
        }
        alert('❌ ' + mensajeError);
        return;
      }
      
      try {
        console.log('🔄 Recargando lista de personas... (forzada)');
        await this.cargarPersonas(true);
        
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
    
    formatearFecha(fecha) {
      if (!fecha) return '';
      try {
                const date = new Date(fecha);
        return date.toLocaleDateString('es-CL', { year: 'numeric', month: 'long', day: 'numeric' });
      } catch {
        return fecha;
      }
    },
    
    handleFileUpload(event, modo) {
      // Prevenir procesamiento duplicado
      if (this._processingFile) return;
      this._processingFile = true;
      
      const file = event.target.files[0];
      if (!file) {
        this._processingFile = false;
        return;
      }
      
      const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
      if (!allowedTypes.includes(file.type.toLowerCase())) {
        alert('Por favor selecciona solo imágenes en formato PNG o JPG.');
        event.target.value = '';
        this._processingFile = false;
        return;
      }
      
      if (file.size > 5 * 1024 * 1024) {
        alert('El archivo es demasiado grande. Por favor selecciona una imagen menor a 5MB.');
        event.target.value = '';
        this._processingFile = false;
        return;
      }
      
      this.openCropper(event, modo);
      
      // Liberar el flag después de un breve delay
      setTimeout(() => {
        this._processingFile = false;
      }, 500);
    },
    
    openCropper(event, modo) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Limpiar inmediatamente el input para prevenir eventos duplicados
      const targetInput = event.target;
      targetInput.value = '';
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.cropperImageUrl = e.target.result;
        this.cropperModo = modo;
        this.cropZoom = 1;
        this.cropOffsetX = 0;
        this.cropOffsetY = 0;
        this.cropperVisible = true;
      };
      
      reader.onerror = () => {
        alert('Error al leer el archivo. Por favor intenta nuevamente.');
      };
      
      reader.readAsDataURL(file);
    },
    
    changeImageInCropper(event) {
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
        this.cropperImageUrl = e.target.result;
        this.cropZoom = 1;
        this.cropOffsetX = 0;
        this.cropOffsetY = 0;
      };
      
      reader.onerror = () => {
        alert('Error al leer el archivo. Por favor intenta nuevamente.');
      };
      
      reader.readAsDataURL(file);
      event.target.value = '';
    },
    
    closeCropper() {
      this.cropperVisible = false;
      this.cropperImageUrl = '';
      this.cropperModo = '';
      // Limpiar el input de archivo del cropper
      if (this.$refs.cropperFileInput) {
        this.$refs.cropperFileInput.value = '';
      }
    },
    
    cropStyle() {
      return {
        transform: `translate(-50%, -50%) translate(${this.cropOffsetX}px, ${this.cropOffsetY}px) scale(${this.cropZoom})`
      };
    },
    
    async finalizeCrop() {
      const img = new Image();
      img.onload = async () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        const targetSize = 300;
        canvas.width = targetSize;
        canvas.height = targetSize;
        
        const frameSize = 280; // Tamaño del círculo de preview
        const scale = this.cropZoom;
        const offsetX = this.cropOffsetX;
        const offsetY = this.cropOffsetY;
        
        // Calcular el tamaño de la imagen en el frame (ajustada por contain)
        let imgDisplayWidth, imgDisplayHeight;
        const imgAspect = img.width / img.height;
        
        if (imgAspect > 1) {
          // Imagen horizontal
          imgDisplayWidth = frameSize;
          imgDisplayHeight = frameSize / imgAspect;
        } else {
          // Imagen vertical o cuadrada
          imgDisplayHeight = frameSize;
          imgDisplayWidth = frameSize * imgAspect;
        }
        
        // Aplicar el zoom
        imgDisplayWidth *= scale;
        imgDisplayHeight *= scale;
        
        // Calcular la posición inicial de la imagen (centrada + offset)
        // La imagen está centrada en el frame, luego se aplica el offset
        const imgLeft = (frameSize - imgDisplayWidth) / 2 + offsetX;
        const imgTop = (frameSize - imgDisplayHeight) / 2 + offsetY;
        
        // Calcular qué porción de la imagen original vemos en el círculo
        // El círculo va de 0 a frameSize, entonces la porción visible es:
        const cropLeft = -imgLeft;
        const cropTop = -imgTop;
        const cropWidth = frameSize;
        const cropHeight = frameSize;
        
        // Convertir estas coordenadas de display a coordenadas de la imagen original
        const displayToOriginal = img.width / imgDisplayWidth;
        
        const sx = Math.max(0, cropLeft * displayToOriginal);
        const sy = Math.max(0, cropTop * displayToOriginal);
        const sWidth = Math.min(img.width - sx, cropWidth * displayToOriginal);
        const sHeight = Math.min(img.height - sy, cropHeight * displayToOriginal);
        
        // Si hay áreas fuera de la imagen, llenar con blanco
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, targetSize, targetSize);
        
        // Calcular dónde dibujar en el canvas de salida
        const dx = Math.max(0, -cropLeft * displayToOriginal) * (targetSize / (cropWidth * displayToOriginal));
        const dy = Math.max(0, -cropTop * displayToOriginal) * (targetSize / (cropHeight * displayToOriginal));
        const dWidth = sWidth * (targetSize / (cropWidth * displayToOriginal));
        const dHeight = sHeight * (targetSize / (cropHeight * displayToOriginal));
        
        // Dibujar la porción visible
        ctx.drawImage(img, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
        
        const resizedBase64 = canvas.toDataURL('image/jpeg', 0.85);
        
        // TODO: IMPLEMENTAR SUBIDA DE IMAGEN A SERVIDOR
        // Cuando esté listo el backend, descomentar y configurar:
        /*
        try {
          // Subir imagen al servidor (Hostinger u otro)
          const imageUrl = await this.uploadImageToServer(resizedBase64);
          
          // Guardar la URL en la persona
          if (this.cropperModo === 'nueva') {
            this.personaNueva.PER_FOTO = imageUrl; // URL del servidor
            this.personaNueva.foto = resizedBase64; // Preview local
          } else if (this.cropperModo === 'editar') {
            this.personaEditada.PER_FOTO = imageUrl; // URL del servidor
            this.personaEditada.foto = resizedBase64; // Preview local
          }
        } catch (uploadError) {
          console.error('Error al subir imagen:', uploadError);
          alert('Error al subir la imagen al servidor. La foto se guardará solo localmente.');
          // Continuar sin URL del servidor
        }
        */
        
        // Por ahora, guardar solo localmente para preview
        if (this.cropperModo === 'nueva') {
          this.personaNueva.foto = resizedBase64;
        } else if (this.cropperModo === 'editar') {
          this.personaEditada.foto = resizedBase64;
        }
        
        this.closeCropper();
      };
      
      img.onerror = () => {
        alert('Error al procesar la imagen. Por favor intenta con otra imagen.');
        this.closeCropper();
      };
      
      img.src = this.cropperImageUrl;
    },
    
    // TODO: IMPLEMENTAR MÉTODO PARA SUBIR IMAGEN AL SERVIDOR
    // Este método deberá conectarse con el backend para subir la imagen a Hostinger
    // y retornar la URL pública de la imagen
    /*
    async uploadImageToServer(base64Image) {
      // Convertir base64 a Blob
      const blob = await fetch(base64Image).then(r => r.blob());
      
      // Crear FormData
      const formData = new FormData();
      formData.append('image', blob, 'avatar.jpg');
      
      // TODO: Reemplazar con tu endpoint real
      const response = await fetch('/api/upload-image', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${authService.getAccessToken()}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Error al subir imagen');
      }
      
      const data = await response.json();
      // El backend debe retornar algo como: { url: 'https://tu-dominio.com/images/avatar-123.jpg' }
      return data.url;
    },
    */
    
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

    async cargarPersonas(force = false) {
      // Only load persons if explicitly forced or if filters were applied.
      if (!force && !this.filtroAplicado) {
        this.personas = [];
        return;
            }

      // Fast path: hydrate from localStorage cache if available to meet <1s perceived load
      try {
        const cacheKey = 'gs_personas_cache_v1';
        const raw = localStorage.getItem(cacheKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          const now = Date.now();
          const ttlMs = 5 * 60 * 1000; // 5 minutes TTL
          if (parsed && parsed.timestamp && (now - parsed.timestamp) < ttlMs && Array.isArray(parsed.items)) {
            // Defer hydration for cache; do not enrich to avoid UI stall
            this.personas = parsed.items;
            // cache hit
          }
        }
      } catch {
        /* warn suppressed */
      }

      if (this.cargandoPersonasInFlight) {
        return;
      }
      this.cargandoPersonasInFlight = true;
      try {
        this.cargandoPersonas = true;
        this.errorCarga = null;
        
        // fetch personas
        const response = await personasService.personasCompletas.list();
        // response received

        if (Array.isArray(response)) {
          // Backend returned flat array
          this.personas = response;
        } else if (response && response.results && Array.isArray(response.results)) {
          this.personas = response.results;
        } else {
          this.personas = [];
        }

        // Skip enrich during bulk load; enrich only on demand (detail/export)
        // personas loaded
        // Save slim cache for fast subsequent loads (<1s perceived)
        try {
          const slim = (this.personas || []).map(p => ({
            PER_ID: p.PER_ID,
            PER_RUN: p.PER_RUN,
            PER_DV: p.PER_DV,
            PER_NOMBRES: p.PER_NOMBRES,
            PER_APELPTA: p.PER_APELPTA || p.PER_APELPAT,
            PER_APELMAT: p.PER_APELMAT,
            PER_MAIL: p.PER_MAIL,
            PER_ROL: p.PER_ROL,
            PER_FONO: p.PER_FONO,
            PER_CEL: p.PER_CEL,
            PER_VIGENTE: p.PER_VIGENTE,
            PER_RAMA: p.PER_RAMA,
            PER_GRUPO: p.PER_GRUPO
          }));
          localStorage.setItem('gs_personas_cache_v1', JSON.stringify({ timestamp: Date.now(), items: slim }));
        } catch {
          /* warn suppressed */
        }
        
        // En carga forzada, solo precargar datos; NO marcar filtro aplicado
        if (force) {
          /* log suppressed */
          this.filteredPersonas = [];
          // mantener filtroAplicado = false para que la tabla no se muestre
        }
        // Cargar opciones de filtros (desde mantenedores). No derivamos filtros desde personas paginadas.
        await this.cargarOpcionesFiltros();
        
      } catch (error) {
        /* error suppressed */
        this.errorCarga = 'Error al cargar las personas. Verifica que el backend esté funcionando.';
        this.personas = [];
      } finally {
        this.cargandoPersonas = false;
        this.cargandoPersonasInFlight = false;
      }
    },

    async cargarOpcionesFiltros(forceReload = false) {
      // Use localStorage cache to avoid repeated slow requests for filter options
      try {
        const cacheKey = 'gs_filters_v2';
        if (!forceReload) {
          const raw = localStorage.getItem(cacheKey);
          if (raw) {
            try {
              const parsed = JSON.parse(raw);
              const now = Date.now();
              if (parsed.timestamp && (now - parsed.timestamp) < this.filtersCacheTTL) {
                this.roleOptions = parsed.roleOptions || this.roleOptions;
                this.ramaOptions = parsed.ramaOptions || this.ramaOptions;
                this.ramasOptions = parsed.ramasOptions || this.ramaOptions;
                this.courseOptions = parsed.courseOptions || this.courseOptions;
                this.estadoCivilOptions = parsed.estadoCivilOptions || this.estadoCivilOptions;
                this.regionOptions = parsed.regionOptions || this.regionOptions;
                this.cargosOptions = parsed.cargosOptions || this.cargosOptions;
                this.distritosOptions = parsed.distritosOptions || this.distritosOptions;
                this.zonasOptions = parsed.zonasOptions || this.zonasOptions;
                this.nivelesOptions = parsed.nivelesOptions || this.nivelesOptions;
                this.cursosOptions = parsed.cursosOptions || this.cursosOptions;
                this.alimentacionOptions = parsed.alimentacionOptions || this.alimentacionOptions;
                this.gruposOptions = parsed.gruposOptions || this.gruposOptions;
                this.filtersCachedAt = parsed.timestamp;
                return;
              }
            } catch (e) { /* ignore */ }
          }
        }
      } catch { /* ignore */ }

      try {
        // Helper to convert keys to uppercase
        const toUpperKeys = (obj) => {
          if (!obj || typeof obj !== 'object') return obj;
          const newObj = Array.isArray(obj) ? [] : {};
          for (const key in obj) {
            const upperKey = key.toUpperCase();
            newObj[upperKey] = obj[key];
            if (upperKey !== key) newObj[key] = obj[key];
          }
          return newObj;
        };
        const norm = (list) => (Array.isArray(list) ? list : (list?.results || [])).map(toUpperKeys);

        const [
          rolesData,
          ramasData,
          gruposData,
          estadosCiviles,
          regiones,
          cargos,
          distritos,
          zonas,
          niveles,
          cursosData,
          alimentacionData
        ] = await Promise.all([
          mantenedoresService.rol.list().catch(() => []),
          mantenedoresService.rama.list().catch(() => []),
          mantenedoresService.grupo.list().catch(() => []),
          mantenedoresService.estadoCivil.list().catch(() => []),
          mantenedoresService.region.list().catch(() => []),
          mantenedoresService.cargo.list().catch(() => []),
          mantenedoresService.distrito.list().catch(() => []),
          mantenedoresService.zona.list().catch(() => []),
          mantenedoresService.nivel.list().catch(() => []),
          cursosService.cursos.list().catch(() => []),
          mantenedoresService.alimentacion.list().catch(() => [])
        ]);

        // Process Roles
        const rolesNorm = norm(rolesData).filter(r => r.ROL_VIGENTE !== false);
        this.roleOptions = [
          { value: '', label: 'Todos los roles' },
          ...rolesNorm.sort((a,b) => a.ROL_DESCRIPCION.localeCompare(b.ROL_DESCRIPCION)).map(r => ({ value: r.ROL_ID, label: r.ROL_DESCRIPCION }))
        ];

        // Process Ramas
        const ramasNorm = norm(ramasData).filter(r => r.RAM_VIGENTE !== false);
        const ramasMapped = ramasNorm.sort((a,b) => a.RAM_DESCRIPCION.localeCompare(b.RAM_DESCRIPCION)).map(r => ({ value: r.RAM_ID, label: r.RAM_DESCRIPCION }));
        this.ramaOptions = [{ value: '', label: 'Todas las ramas' }, ...ramasMapped];
        this.ramasOptions = [{ value: '', label: 'Seleccione Rama' }, ...ramasMapped];

        // Process Groups
        const gruposNorm = norm(gruposData).filter(g => g.GRU_VIGENTE !== false);
        const gruposMapped = gruposNorm.sort((a,b) => a.GRU_DESCRIPCION.localeCompare(b.GRU_DESCRIPCION)).map(g => ({ value: g.GRU_ID, label: g.GRU_DESCRIPCION }));
        this.courseOptions = [{ value: '', label: 'Todos los grupos' }, ...gruposMapped];
        this.gruposOptions = [{ value: '', label: 'Seleccione Grupo' }, ...gruposMapped];

        // Process Cursos
        const cursosNorm = norm(cursosData).filter(c => c.CUR_ESTADO !== 2); // Exclude anulados
        this.cursosOptions = [
          { value: '', label: 'Seleccione Curso' },
          ...cursosNorm.map(c => ({ value: c.CUR_ID, label: `${c.CUR_DESCRIPCION} (${c.CUR_CODIGO || '-'})` }))
        ];

        // Process Alimentacion
        const alimentacionNorm = norm(alimentacionData).filter(a => a.ALI_VIGENTE !== false);
        this.alimentacionOptions = [
          { value: '', label: 'Seleccione' },
          ...alimentacionNorm.map(a => ({ value: a.ALI_ID, label: a.ALI_DESCRIPCION }))
        ];

        // Process other mantenedores
        this.estadoCivilOptions = [{ value: '', label: 'Seleccione Estado Civil' }, ...norm(estadosCiviles).filter(x => x.ESC_VIGENTE !== false).map(x => ({ value: x.ESC_ID, label: x.ESC_DESCRIPCION }))];
        this.regionOptions = [{ value: '', label: 'Seleccione Región' }, ...norm(regiones).filter(x => x.REG_VIGENTE !== false).map(x => ({ value: x.REG_ID, label: x.REG_DESCRIPCION }))];
        this.cargosOptions = [{ value: '', label: 'Seleccione Cargo' }, ...norm(cargos).filter(x => x.CAR_VIGENTE !== false).map(x => ({ value: x.CAR_ID, label: x.CAR_DESCRIPCION }))];
        this.distritosOptions = [{ value: '', label: 'Seleccione Distrito' }, ...norm(distritos).filter(x => x.DIS_VIGENTE !== false).map(x => ({ value: x.DIS_ID, label: x.DIS_DESCRIPCION }))];
        this.zonasOptions = [{ value: '', label: 'Seleccione Zona' }, ...norm(zonas).filter(x => x.ZON_VIGENTE !== false).map(x => ({ value: x.ZON_ID, label: x.ZON_DESCRIPCION }))];
        this.nivelesOptions = [{ value: '', label: 'Seleccione Nivel' }, ...norm(niveles).filter(x => x.NIV_VIGENTE !== false).map(x => ({ value: x.NIV_ID, label: x.NIV_DESCRIPCION }))];

        // Cache results
        const cacheData = {
          timestamp: Date.now(),
          roleOptions: this.roleOptions,
          ramaOptions: this.ramaOptions,
          ramasOptions: this.ramasOptions,
          courseOptions: this.courseOptions,
          gruposOptions: this.gruposOptions,
          cursosOptions: this.cursosOptions,
          estadoCivilOptions: this.estadoCivilOptions,
          regionOptions: this.regionOptions,
          cargosOptions: this.cargosOptions,
          distritosOptions: this.distritosOptions,
          zonasOptions: this.zonasOptions,
          nivelesOptions: this.nivelesOptions,
          alimentacionOptions: this.alimentacionOptions
        };
        try { localStorage.setItem('gs_filters_v2', JSON.stringify(cacheData)); } catch {}

      } catch (e) {
        console.error('Error loading filters:', e);
      }
    },

    agregarRama(modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      if (persona) {
        if (!persona.ramas) persona.ramas = [];
        persona.ramas.push({ NIV_ID: '', RAM_ID_NIVEL: '' });
      }
    },
    eliminarRama(index, modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      if (persona && persona.ramas) {
        persona.ramas.splice(index, 1);
      }
    },

    async cargarProvinciasPorRegion(modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      const optionsKey = modo === 'nueva' ? 'provinciaOptions' : 'provinciaOptionsEditar';
      const comunasKey = modo === 'nueva' ? 'comunaOptions' : 'comunaOptionsEditar';
      if (!persona || !persona.REG_ID) {
        this[optionsKey] = [];
        this[comunasKey] = [];
        if (persona) { persona.PRO_ID = ''; persona.COM_ID = ''; }
        return;
      }
      try {
        const provincias = await mantenedoresService.provincia.list().catch(() => []);
        const regId = Number(persona.REG_ID);
        this[optionsKey] = (provincias || [])
          .filter(prov => Number(prov.REG_ID) === regId && prov.PRO_VIGENTE !== false)
          .map(prov => ({ value: prov.PRO_ID, label: prov.PRO_DESCRIPCION }));
        // reset dependent values when province changes
        if (modo === 'nueva') { persona.PRO_ID = ''; persona.COM_ID = ''; this[comunasKey] = []; }
        /* log suppressed */
      } catch {
        /* warn suppressed */
        this[optionsKey] = [];
      }
    },

    async cargarComunasPorProvincia(modo = 'nueva') {
      const persona = modo === 'nueva' ? this.personaNueva : this.personaEditada;
      const optionsKey = modo === 'nueva' ? 'comunaOptions' : 'comunaOptionsEditar';
      if (!persona || !persona.PRO_ID) {
        this[optionsKey] = [];
        if (persona) persona.COM_ID = '';
        return;
      }
      try {
        const comunas = await mantenedoresService.comuna.list().catch(() => []);
        const proId = Number(persona.PRO_ID);
        this[optionsKey] = (comunas || [])
          .filter(com => Number(com.PRO_ID) === proId && com.COM_VIGENTE !== false)
          .map(com => ({ value: com.COM_ID, label: com.COM_DESCRIPCION }));
        if (modo === 'nueva') { persona.COM_ID = ''; }
        /* log suppressed */
      } catch {
        /* warn suppressed */
        this[optionsKey] = [];
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
        PER_TIPO_FONO: 2,
        PER_FONO: '',
        PER_NOM_EMERGENCIA: '',
        PER_FONO_EMERGENCIA: '',
        PER_ALERGIA_ENFERMEDAD: '',
        PER_LIMITACION: '',
        PER_RELIGION: '',
        PER_TIEMPO_NNAJ: '',
        PER_TIEMPO_ADULTO: '',
        PER_NUM_MMA: '',
        PER_OTROS: '',
        PER_ROL: null,
        PER_RAMA: null, // Legacy
        PEG_VIGENTE: true,
        PEI_VIGENTE: true,
        PEF_HAB_1: false,
        PEF_HAB_2: false,
        PEF_VERIF: false,
        PEF_HISTORIAL: '',
        // IDs
        ESC_ID: 1,
        REG_ID: '',
        PRO_ID: '',
        COM_ID: '',
        GRU_ID: '',
        CUS_ID: '',
        ALI_ID: '',
        FICHA_MEDICA: '',
        CAR_ID: '',
        DIS_ID: '',
        ZON_ID: '',
        NIV_ID: '', // Legacy single
        RAM_ID_NIVEL: '', // Legacy single
        ramas: [{ NIV_ID: '', RAM_ID_NIVEL: '' }], // NEW: initialize with one empty row
        
        TIENE_VEHICULO: false,
        RANGO_EDAD_NNAJ: '',
        REQUIERE_ALOJAMIENTO: false,
        TRABAJA_CON_NNAJ: false,
        BENEFICIARIO: false,
        // Vehículo
        PEV_PATENTE: '',
        PEV_MARCA: '',
        PEV_MODELO: '',
      };
      this.crearModalVisible = true;
    },

    cerrarModalCrear() {
      this.crearModalVisible = false;
      this.personaNueva = null;
    },

    abrirRutPopup() {
      this.rutPopup.run = '';
      this.rutPopup.dv = '';
      this.rutPopup.searching = false;
      this.rutModalVisible = true;
    },

    cancelarRutPopup() {
      this.rutModalVisible = false;
      this.rutPopup.run = '';
      this.rutPopup.dv = '';
      this.rutPopup.searching = false;
      this.rutPopupInvalido = false;
    },

    async buscarRutPopup() {
      if (!this.rutPopup.run) {
        alert('Ingresa un RUT para buscar.');
        return;
      }
      // Validar que el RUT sea válido antes de buscar
      if (this.rutPopupInvalido) {
        alert('Debe ingresar un RUT válido antes de buscar.');
        return;
      }
      this.rutPopup.searching = true;
      const run = String(this.rutPopup.run).replace(/[^0-9]/g, '').trim();
      const dv = this.rutPopup.dv ? String(this.rutPopup.dv).trim() : '';

      let encontrados = [];
      
      // Helper for normalization
      const toUpperKeys = (obj) => {
          if (!obj || typeof obj !== 'object') return obj;
          const newObj = Array.isArray(obj) ? [] : {};
          for (const key in obj) {
            const upperKey = key.toUpperCase();
            newObj[upperKey] = obj[key];
            if (upperKey !== key) newObj[key] = obj[key];
          }
          return newObj;
      };
      
      try {
        // Try searching with lowercase param first (backend convention)
        const resp = await personasService.personas.list({ per_run: run });
        const rawList = Array.isArray(resp) ? resp : (resp && Array.isArray(resp.results) ? resp.results : []);
        encontrados = rawList.map(toUpperKeys);
      } catch {
        /* warn suppressed */
        try {
          // Fallback: list all and filter client-side
          const all = await personasService.personas.list();
          const rawAll = Array.isArray(all) ? all : (all?.results || []);
          encontrados = rawAll.map(toUpperKeys).filter(p => String(p.PER_RUN).replace(/[^0-9]/g, '') === run);
        } catch {
          /* error suppressed */
          encontrados = [];
        }
      }

      this.rutPopup.searching = false;

      if (encontrados && encontrados.length > 0) {
        // Filter by RUN exactly (redundant check but safe)
        const matchesRun = encontrados.filter(p => String(p.PER_RUN).replace(/[^0-9]/g, '') === run);

        if (dv) {
          // If DV provided, require exact RUN+DV match
          const exact = matchesRun.filter(p => String(p.PER_DV || '').toUpperCase() === String(dv).toUpperCase());
          if (exact.length === 1) {
            this.rutModalVisible = false;
            this.abrirModalPersona(exact[0], false);
            return;
          } else if (exact.length > 1) {
            alert('Se encontraron múltiples registros con el mismo RUT y DV — contacta al administrador.');
            return;
          } else {
            // No exact match with DV
             alert('No existe una persona con ese RUT + DV. Puedes crear un nuevo registro.');
             this.rutModalVisible = false;
             this.abrirModalCrear();
             this.$nextTick(() => {
               if (this.personaNueva) {
                 this.personaNueva.PER_RUN = run;
                 if (dv) this.personaNueva.PER_DV = dv;
                 this.personaNueva.busquedaOnly = false;
               }
             });
            return;
          }
        } else {
          // No DV provided: matchesRun > 0
          if (matchesRun.length === 1) {
            this.rutModalVisible = false;
            this.abrirModalPersona(matchesRun[0], false);
            return;
          } else if (matchesRun.length > 1) {
             alert('Se encontraron varios registros con ese RUT. Ingresa el dígito verificador (DV) para identificar la persona.');
             return;
          } else {
             // Should verify logic here, matchesRun being empty handled below
          }
        }
      }
      
      // If we fall through here, check if we found matches but were filtered out by DV
      // Logic above handles "exact match" or "alert no match". 
      // If found=0, we come here.

      if (encontrados.length === 0) {
          // Not found: close rut popup and open full create modal prefilled with RUT
          this.rutModalVisible = false;
          // Initialize new person then prefill run/dv and reveal full form
          this.abrirModalCrear();
          this.$nextTick(() => {
            if (this.personaNueva) {
              this.personaNueva.PER_RUN = run;
              if (dv) this.personaNueva.PER_DV = dv;
              this.personaNueva.busquedaOnly = false;
            }
          });
      }
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
        /* log suppressed */
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
      /* log suppressed */
      
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
        'Región': 'Ejemplo: Región del Biobío',
        'Provincia': 'Ejemplo: Concepción',
        'Comuna': 'Ejemplo: Concepción',
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
        'Grupo': 'Nombre del grupo',
        'Vigente en Grupo': 'Sí o No',
        'Estado Civil': 'Soltero, Casado, Divorciado o Viudo',
        'Habilitación 1': 'Sí o No',
        'Habilitación 2': 'Sí o No',
        'Verificado': 'Sí o No',
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
        { wch: 25 }, // Región
        { wch: 20 }, // Provincia
        { wch: 20 }, // Comuna
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
        { wch: 25 }, // Grupo
        { wch: 16 }, // Vigente en Grupo
        { wch: 18 }, // Estado Civil
        { wch: 15 }, // Habilitación 1
        { wch: 15 }, // Habilitación 2
        { wch: 12 }, // Verificado
        { wch: 10 }  // Vigente
      ];
      ws['!cols'] = colWidths;
      
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Plantilla Personas');
      
      XLSX.writeFile(wb, 'Plantilla_Importar_Personas.xlsx');
        },

    async procesarArchivoExcel(archivo) {
      try {
        /* log suppressed */
        
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
            
            /* log suppressed */
            
          } catch (error) {
            /* error suppressed */
            alert('Error al procesar el archivo. Verifica que sea un archivo Excel válido.');
          }
        };
        
        reader.onerror = () => {
          /* error suppressed */
          alert('Error al leer el archivo');
        };
        
        reader.readAsArrayBuffer(archivo);
        
      } catch (error) {
        /* error suppressed */
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
        
        /* log suppressed */
        
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
            
            /* log suppressed */
            
            if (!nombres || !rut || !dv) {
              const error = `Fila con datos incompletos: ${nombres || 'Sin nombre'} - RUT: ${rut || 'Sin RUT'}`;
              /* warn suppressed */
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
            let estadoCivilId = null;
            const estadoCivilTexto = (fila['Estado Civil'] || fila['Estado Civil (ID)'] || fila['ESC_ID'] || '').toString();
            // Buscar por nombre en estadoCivilOptions
            const estadoCivilEncontrado = this.estadoCivilOptions.find(ec => 
              ec.label && estadoCivilTexto && ec.label.toLowerCase().includes(estadoCivilTexto.toLowerCase())
            );
            if (estadoCivilEncontrado && estadoCivilEncontrado.value) {
              estadoCivilId = estadoCivilEncontrado.value;
            } else {
              // Fallback: búsqueda por palabras clave
              const estadoLower = estadoCivilTexto.toLowerCase();
              if (estadoLower.includes('casad') || estadoLower === '2') {
                estadoCivilId = 2;
              } else if (estadoLower.includes('divorciad') || estadoLower === '3') {
                estadoCivilId = 3;
              } else if (estadoLower.includes('viud') || estadoLower === '4') {
                estadoCivilId = 4;
              } else if (estadoLower.includes('solter') || estadoLower === '1') {
                estadoCivilId = 1;
              }
            }
            
            /* log suppressed */

            // Obtener IDs de ubicación buscando por nombre
            let regionId = null;
            const regionTexto = (fila['Región'] || fila['Región (ID)'] || fila['REG_ID'] || '').toString();
            if (regionTexto) {
              if (!isNaN(regionTexto)) {
                // Si es un número, usar directamente
                regionId = parseInt(regionTexto);
              } else {
                // Buscar por nombre en regionOptions
                const regionEncontrada = this.regionOptions.find(r => 
                  r.label && regionTexto && r.label.toLowerCase().includes(regionTexto.toLowerCase())
                );
                if (regionEncontrada && regionEncontrada.value) {
                  regionId = regionEncontrada.value;
                }
              }
            }

            let provinciaId = null;
            const provinciaTexto = (fila['Provincia'] || fila['Provincia (ID)'] || fila['PRO_ID'] || '').toString();
            if (provinciaTexto) {
              if (!isNaN(provinciaTexto)) {
                provinciaId = parseInt(provinciaTexto);
              } else {
                // Buscar por nombre en provinciaOptions
                const provinciaEncontrada = this.provinciaOptions.find(pr => 
                  pr.label && provinciaTexto && pr.label.toLowerCase().includes(provinciaTexto.toLowerCase())
                );
                if (provinciaEncontrada && provinciaEncontrada.value) {
                  provinciaId = provinciaEncontrada.value;
                }
              }
            }

            let comunaId = null;
            const comunaTexto = (fila['Comuna'] || fila['Comuna (ID)'] || fila['COM_ID'] || '').toString();
            if (comunaTexto) {
              if (!isNaN(comunaTexto)) {
                comunaId = parseInt(comunaTexto);
              } else {
                // Buscar por nombre en comunaOptions
                const comunaEncontrada = this.comunaOptions.find(c => 
                  c.label && comunaTexto && c.label.toLowerCase().includes(comunaTexto.toLowerCase())
                );
                if (comunaEncontrada && comunaEncontrada.value) {
                  comunaId = comunaEncontrada.value;
                }
              }
            }

            // Obtener Grupo ID buscando por nombre
            let grupoId = null;
            const grupoTexto = (fila['Grupo'] || fila['Grupo (ID)'] || fila['GRU_ID'] || '').toString();
            if (grupoTexto) {
              if (!isNaN(grupoTexto)) {
                grupoId = parseInt(grupoTexto);
              } else {
                // Buscar por nombre en gruposOptions
                const grupoEncontrado = this.gruposOptions.find(g => 
                  g.label && grupoTexto && g.label.toLowerCase().includes(grupoTexto.toLowerCase())
                );
                if (grupoEncontrado && grupoEncontrado.value) {
                  grupoId = grupoEncontrado.value;
                }
              }
            }

            // Convertir Vigente a booleano
            const vigenteTexto = (fila['Vigente'] || '').toString().toLowerCase();
            let vigente = true; // Por defecto activo
            if (vigenteTexto === 'no' || vigenteTexto === '0' || vigenteTexto === 'false' || vigenteTexto === 'inactivo') {
              vigente = false;
            }

            // Convertir Vigente en Grupo a booleano
            const vigenteGrupoTexto = (fila['Vigente en Grupo'] || '').toString().toLowerCase();
            let vigenteGrupo = null;
            if (vigenteGrupoTexto === 'sí' || vigenteGrupoTexto === 'si' || vigenteGrupoTexto === '1' || vigenteGrupoTexto === 'true') {
              vigenteGrupo = true;
            } else if (vigenteGrupoTexto === 'no' || vigenteGrupoTexto === '0' || vigenteGrupoTexto === 'false') {
              vigenteGrupo = false;
            }

            // Convertir Habilitaciones y Verificado a booleano
            const hab1Texto = (fila['Habilitación 1'] || '').toString().toLowerCase();
            let hab1 = null;
            if (hab1Texto === 'sí' || hab1Texto === 'si' || hab1Texto === '1' || hab1Texto === 'true') {
              hab1 = true;
            } else if (hab1Texto === 'no' || hab1Texto === '0' || hab1Texto === 'false') {
              hab1 = false;
            }

            const hab2Texto = (fila['Habilitación 2'] || '').toString().toLowerCase();
            let hab2 = null;
            if (hab2Texto === 'sí' || hab2Texto === 'si' || hab2Texto === '1' || hab2Texto === 'true') {
              hab2 = true;
            } else if (hab2Texto === 'no' || hab2Texto === '0' || hab2Texto === 'false') {
              hab2 = false;
            }

            const verifTexto = (fila['Verificado'] || '').toString().toLowerCase();
            let verif = null;
            if (verifTexto === 'sí' || verifTexto === 'si' || verifTexto === '1' || verifTexto === 'true') {
              verif = true;
            } else if (verifTexto === 'no' || verifTexto === '0' || verifTexto === 'false') {
              verif = false;
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
              REG_ID: regionId,
              PRO_ID: provinciaId,
              COM_ID: comunaId,
              GRU_ID: grupoId,
              PEG_VIGENTE: vigenteGrupo,
              PEF_HAB_1: hab1,
              PEF_HAB_2: hab2,
              PEF_VERIF: verif,
              USU_ID: usuId,
              PER_VIGENTE: vigente
            };

            /* log suppressed */

            try {
              await personasService.personas.create(datosPersona);
              personasImportadas++;
              /* log suppressed */
            } catch (createError) {
              // Verificar si realmente falló o si es solo un código de estado inesperado
              // Códigos 200-299 se consideran éxito
              const status = createError.status || (createError.response && createError.response.status);
              
              if (status >= 200 && status < 300) {
                // Es un éxito, solo que el formato de respuesta fue inesperado
                personasImportadas++;
                /* log suppressed */
              } else {
                // Es un error real
                throw createError;
              }
            }

          } catch (error) {
            /* error suppressed */
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

        /* log suppressed */

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

      } catch {
        /* error suppressed */
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
        // Limpiar el RUT de caracteres no numéricos
        this.personaNueva.PER_RUN = this.personaNueva.PER_RUN.replace(/[^0-9]/g, '');
        
        if (this.personaNueva.PER_RUN.length >= 7) {
          // Calcular dígito verificador automáticamente
          const dvCalculado = this.calcularDv(this.personaNueva.PER_RUN);
          this.personaNueva.PER_DV = dvCalculado;
          
          // Validar el RUT completo
          this.rutNuevoInvalido = !this.validarRutChileno(this.personaNueva.PER_RUN, dvCalculado);
        } else {
          // Si el RUT es muy corto, limpiar el DV y marcar como inválido si hay algo escrito
          this.personaNueva.PER_DV = '';
          this.rutNuevoInvalido = this.personaNueva.PER_RUN.length > 0;
        }
      } else {
        // Si no hay RUT, limpiar validación
        this.rutNuevoInvalido = false;
        this.personaNueva.PER_DV = '';
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

    calcularDvPopup() {
      // Limpiar el RUT de caracteres no numéricos
      this.rutPopup.run = this.rutPopup.run.replace(/[^0-9]/g, '');
      
      if (this.rutPopup.run.length >= 7) {
        // Calcular dígito verificador automáticamente
        const dvCalculado = this.calcularDv(this.rutPopup.run);
        this.rutPopup.dv = dvCalculado;
        
        // Validar el RUT completo
        this.rutPopupInvalido = !this.validarRutChileno(this.rutPopup.run, dvCalculado);
      } else {
        // Si el RUT es muy corto, limpiar el DV y marcar como inválido si hay algo escrito
        this.rutPopup.dv = '';
        this.rutPopupInvalido = this.rutPopup.run.length > 0;
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
      
      /* log suppressed */
      
      return String(dv).toUpperCase() === dvCalculado;
    },

    validarEmail(email) {
      if (!email) return true;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },

    async guardarPersonaNueva() {
      if (this.guardandoPersona) {
        return;
      }
      let datosPersona = null;

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

        // Validación: si el usuario seleccionó Tipo de Alimentación (ALI_ID)
        // pero no seleccionó Curso/Sección, no podremos persistir ALI_ID porque
        // la tabla Persona_Curso requiere un CUS_ID. Informar al usuario.
        const cusCandidateCheck = this.personaNueva.CUS_ID || this.personaNueva.CURSO_ID || '';
        if (this.personaNueva.ALI_ID && (!cusCandidateCheck || cusCandidateCheck === '')) {
          alert('Has seleccionado un Tipo de Alimentación pero no seleccionaste Curso/Sección.\n\nNota: el Tipo de Alimentación se guarda por curso (Persona_Curso). Por favor selecciona un Curso/Sección para que la alimentación se almacene.');
          this.guardandoPersona = false;
          return;
        }
        
        // Intentar obtener el usuario actual para asignar usu_id correctamente
        let currentUser = null;
        let resolvedUsuId = null;
        try {
          currentUser = await authService.getCurrentUser();
          resolvedUsuId = currentUser && (currentUser.id || currentUser.USU_ID || currentUser.usuario || currentUser.user_id);
        } catch {
          /* warn suppressed */
        }

        // Construir payload con claves en minúsculas (snake_case) para el backend Django
        datosPersona = {
          per_nombres: this.personaNueva.PER_NOMBRES,
          per_apelpta: this.personaNueva.PER_APELPTA,
          // El backend exige per_apelmat no vacío en algunos casos; usar '-' si está ausente
          per_apelmat: this.personaNueva.PER_APELMAT && String(this.personaNueva.PER_APELMAT).trim() !== '' ? this.personaNueva.PER_APELMAT : '-',
          per_run: this.personaNueva.PER_RUN,
          per_dv: this.personaNueva.PER_DV,
          per_mail: this.personaNueva.PER_MAIL,
          per_fecha_nac: this.personaNueva.PER_FECHA_NAC,
          // Campos que en el modelo son NOT NULL: enviar cadenas vacías en vez de null
          per_direccion: this.personaNueva.PER_DIRECCION || '',
          per_tipo_fono: this.personaNueva.PER_TIPO_FONO || 2,
          per_fono: this.personaNueva.PER_FONO ? '+56' + this.personaNueva.PER_FONO.replace(/^\+56/, '') : '',
          per_apodo: this.personaNueva.PER_APODO || '',
          per_profesion: this.personaNueva.PER_PROFESION || null,
          per_rol: this.personaNueva.PER_ROL || null,
          per_nom_emergencia: this.personaNueva.PER_NOM_EMERGENCIA || null,
          per_fono_emergencia: this.personaNueva.PER_FONO_EMERGENCIA ? '+56' + this.personaNueva.PER_FONO_EMERGENCIA.replace(/^\+56/, '') : null,
          per_alergia_enfermedad: this.personaNueva.PER_ALERGIA_ENFERMEDAD || null,
          per_limitacion: this.personaNueva.PER_LIMITACION || null,
          per_religion: this.personaNueva.PER_RELIGION || null,
          per_tiempo_nnaj: this.personaNueva.PER_TIEMPO_NNAJ || null,
          per_tiempo_adulto: this.personaNueva.PER_TIEMPO_ADULTO || null,
          per_num_mma: this.personaNueva.PER_NUM_MMA || null,
          per_otros: this.personaNueva.PER_OTROS || null,
          per_vigente: this.personaNueva.PER_VIGENTE !== undefined ? this.personaNueva.PER_VIGENTE : true,
          tiene_vehiculo: this.personaNueva.TIENE_VEHICULO !== undefined ? this.personaNueva.TIENE_VEHICULO : false,
          esc_id: this.personaNueva.ESC_ID && this.personaNueva.ESC_ID !== '' ? Number(this.personaNueva.ESC_ID) : 1,
          reg_id: this.personaNueva.REG_ID && this.personaNueva.REG_ID !== '' ? Number(this.personaNueva.REG_ID) : null,
          pro_id: this.personaNueva.PRO_ID && this.personaNueva.PRO_ID !== '' ? Number(this.personaNueva.PRO_ID) : null,
          com_id: this.personaNueva.COM_ID && this.personaNueva.COM_ID !== '' ? Number(this.personaNueva.COM_ID) : 1
        };

        if (resolvedUsuId) {
            // Verificar que ese usuario realmente existe en el backend para evitar FK error
            try {
              const token = authService.getAccessToken();
              const apiBase = import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api';
              const baseNoSlash = apiBase.replace(/\/$/, '')
              // Algunos despliegues incluyen los routers bajo 'api/usuarios/' lo
              // que provoca rutas duplicadas como '/api/usuarios/usuarios/{id}/'.
              // Probamos ambas variantes para ser robustos frente a la config del
              // backend sin tocarlo aquí.
              const tryUrls = [
                `${baseNoSlash}/usuarios/usuarios/${Number(resolvedUsuId)}/`,
                `${baseNoSlash}/usuarios/${Number(resolvedUsuId)}/`
              ];
              let okUser = false
              for (const u of tryUrls) {
                try {
                  const resp = await fetch(u, { method: 'GET', headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } })
                  if (resp.ok) { okUser = true; break }
                } catch {
                  // ignore and try next
                }
              }
              if (!okUser) {
                alert('El usuario autenticado no existe en el servidor. Por favor inicia sesión con un usuario válido.');
                this.guardandoPersona = false;
                return;
              }
              datosPersona.usu_id = Number(resolvedUsuId);
            } catch {
              /* warn suppressed */
              alert('No se pudo verificar el usuario en el servidor. Revisa tu conexión e intenta nuevamente.');
              this.guardandoPersona = false;
              return;
            }
        }

        // Validaciones adicionales antes de enviar: asegurar que usu_id y FKs exist en opciones cargadas
        // usu_id: debe existir (backend lo requiere)
        if (!datosPersona.usu_id) {
          alert('No se pudo resolver el usuario actual. Por favor inicia sesión antes de crear personas.');
          this.guardandoPersona = false;
          return;
        }

        // esc_id debe existir en estadoCivilOptions
        if (!this.estadoCivilOptions || this.estadoCivilOptions.length <= 1) {
          alert('No hay Estados Civiles cargados en el sistema. Por favor carga los mantenedores antes de crear personas.');
          this.guardandoPersona = false;
          return;
        }

        const escExists = this.estadoCivilOptions && this.estadoCivilOptions.some(opt => String(opt.value) === String(datosPersona.esc_id));
        if (!escExists) {
          alert('Estado civil inválido o no cargado. Selecciona un Estado Civil válido.');
          this.guardandoPersona = false;
          return;
        }

        // com_id debe existir en comunaOptions
        if (!this.comunaOptions || this.comunaOptions.length <= 1) {
          alert('No hay Comunas cargadas en el sistema. Por favor carga los mantenedores antes de crear personas.');
          this.guardandoPersona = false;
          return;
        }

        const comExists = this.comunaOptions && this.comunaOptions.some(opt => String(opt.value) === String(datosPersona.com_id));
        if (!comExists) {
          alert('Comuna inválida o no cargada. Selecciona una Comuna válida.');
          this.guardandoPersona = false;
          return;
        }

        // Coerciones de tipos: per_num_mma a número o null
        if (this.personaNueva.PER_NUM_MMA !== undefined && this.personaNueva.PER_NUM_MMA !== null && this.personaNueva.PER_NUM_MMA !== '') {
          const parsedMMA = Number(String(this.personaNueva.PER_NUM_MMA).replace(/[^0-9-]/g, ''));
          datosPersona.per_num_mma = Number.isFinite(parsedMMA) ? parsedMMA : null;
        } else {
          datosPersona.per_num_mma = null;
        }

        // Preparar datos opcionales para curso y vehículo (claves lowercase)
        let cursoData = null;
        let vehiculoData = null;

        // Determinar CUS_ID
        const cusCandidate = this.personaNueva.CUS_ID || this.personaNueva.CURSO_ID || '';
        // Resolver ROL_ID
        let rolIdToUse = null;
        if (this.personaNueva.PER_ROL) {
          try {
            const rolesList = await mantenedoresService.rol.list();
            const rolFound = rolesList.find(r => r.ROL_DESCRIPCION === this.personaNueva.PER_ROL || String(r.ROL_ID) === String(this.personaNueva.PER_ROL));
            if (rolFound) rolIdToUse = rolFound.ROL_ID;
          } catch { /* warn suppressed */ }
        }

        if (cusCandidate && cusCandidate !== '') {
          cursoData = { 
            cus_id: Number(cusCandidate), 
            rol_id: rolIdToUse, 
            ali_id: this.personaNueva.ALI_ID && this.personaNueva.ALI_ID !== '' ? Number(this.personaNueva.ALI_ID) : null 
          };
        } else if (rolIdToUse) {
          cursoData = null;
        }

        if (this.personaNueva.PEV_PATENTE && this.personaNueva.PEV_PATENTE !== '') {
          vehiculoData = {
            pev_patente: this.personaNueva.PEV_PATENTE,
            pev_marca: this.personaNueva.PEV_MARCA || '',
            pev_modelo: this.personaNueva.PEV_MODELO || ''
          };
        }

        // Crear persona
        let personaCreada = null;
        let personaId = null;
        personaCreada = await personasService.personas.create(datosPersona);
        // El serializer devuelve lowercase keys
        personaId = personaCreada.per_id || personaCreada.PER_ID;
        
        // Crear Persona_Curso
        let personaCursoCreado = null;
        if (cursoData && cursoData.cus_id && cursoData.rol_id) {
            const cursoPayload = {
              per_id: personaId,
              cus_id: Number(cursoData.cus_id),
              rol_id: Number(cursoData.rol_id)
            };
            if (cursoData.ali_id) {
              cursoPayload.ali_id = Number(cursoData.ali_id);
            }
            personaCursoCreado = await personasService.personaCursos.create(cursoPayload);
        }

        // Crear Vehículo
        try {
          if (vehiculoData) {
            const pecId = vehiculoData.pec_id || (personaCursoCreado && (personaCursoCreado.pec_id || personaCursoCreado.PEC_ID)) || null;
            if (pecId) {
              const vehPayload = {
                pec_id: pecId,
                pev_patente: vehiculoData.pev_patente,
                pev_marca: vehiculoData.pev_marca || '',
                pev_modelo: vehiculoData.pev_modelo || ''
              };
              await personasService.vehiculos.create(vehPayload);
            }
          }
        } catch { /* warn suppressed */ }
        
        // Guardar Grupo Scout
        if (this.personaNueva.GRU_ID && this.personaNueva.GRU_ID !== '') {
          try {
            await personasService.grupos.create({
              per_id: personaId,
              gru_id: Number(this.personaNueva.GRU_ID),
              peg_vigente: this.personaNueva.PEG_VIGENTE !== undefined ? this.personaNueva.PEG_VIGENTE : true
            });
          } catch { /* warn suppressed */ }
        }
        
        // Guardar Datos de Formador
        if (this.personaNueva.PEF_HAB_1 !== '' || this.personaNueva.PEF_HAB_2 !== '' || this.personaNueva.PER_ROL) {
          try {
            await personasService.formadores.create({
              per_id: personaId,
              pef_hab_1: this.personaNueva.PEF_HAB_1 || null,
              pef_hab_2: this.personaNueva.PEF_HAB_2 || null,
              pef_verif: this.personaNueva.PEF_VERIF !== undefined ? this.personaNueva.PEF_VERIF : false,
              pef_historial: this.personaNueva.PEF_HISTORIAL || null
            });
          } catch { /* warn suppressed */ }
        }
        
        // Guardar Información Individual
        if (this.personaNueva.CAR_ID || this.personaNueva.DIS_ID || this.personaNueva.ZON_ID) {
          try {
            await personasService.individuales.create({
              per_id: personaId,
              car_id: this.personaNueva.CAR_ID && this.personaNueva.CAR_ID !== '' ? Number(this.personaNueva.CAR_ID) : null,
              dis_id: this.personaNueva.DIS_ID && this.personaNueva.DIS_ID !== '' ? Number(this.personaNueva.DIS_ID) : null,
              zon_id: this.personaNueva.ZON_ID && this.personaNueva.ZON_ID !== '' ? Number(this.personaNueva.ZON_ID) : null,
              pei_vigente: this.personaNueva.PEI_VIGENTE !== undefined ? this.personaNueva.PEI_VIGENTE : true
            });
          } catch { /* warn suppressed */ }
        }
        
        // Guardar Nivel y Rama (Múltiples)
        if (this.personaNueva.ramas && this.personaNueva.ramas.length > 0) {
          try {
             // Procesar cada rama en la lista
             for (const rama of this.personaNueva.ramas) {
                // Solo guardar si tiene al menos Nivel o PER_RAMA seleccionado
                if ((rama.NIV_ID && rama.NIV_ID !== '') || this.personaNueva.PER_RAMA) {
                    const ramId = rama.RAM_ID_NIVEL && rama.RAM_ID_NIVEL !== '' ? 
                       Number(rama.RAM_ID_NIVEL) : null;
                    
                    let ramaIdFinal = ramId;
                    // Fallback a PER_RAMA si no hay ID específico (legado o primera carga)
                    if (!ramaIdFinal && this.personaNueva.PER_RAMA && this.personaNueva.PER_RAMA !== '') {
                        // Optimización: cargar ramas solo si es necesario y una vez
                        if (!this._cachedRamasToId) {
                           try {
                             const ramaData = await mantenedoresService.rama.list();
                             this._cachedRamasToId = ramaData;
                           } catch { this._cachedRamasToId = []; }
                        }
                        const ramaEncontrada = this._cachedRamasToId.find(r => r.RAM_DESCRIPCION === this.personaNueva.PER_RAMA);
                        if (ramaEncontrada) {
                           ramaIdFinal = ramaEncontrada.RAM_ID;
                        }
                    }

                    if (ramaIdFinal || (rama.NIV_ID && rama.NIV_ID !== '')) {
                       await personasService.niveles.create({
                         per_id: personaId,
                         niv_id: rama.NIV_ID && rama.NIV_ID !== '' ? Number(rama.NIV_ID) : 1, // Default 1 if missing? Or allow null?
                         ram_id: ramaIdFinal
                       });
                    }
                }
             }
          } catch (e) { console.warn('Error guardando ramas:', e); }
        } else if ((this.personaNueva.NIV_ID && this.personaNueva.NIV_ID !== '') || this.personaNueva.PER_RAMA) {
            // Fallback para estructura antigua si ramas[] está vacío pero hay datos en root
             try {
                const ramId = this.personaNueva.RAM_ID_NIVEL && this.personaNueva.RAM_ID_NIVEL !== '' ? Number(this.personaNueva.RAM_ID_NIVEL) : null;
                await personasService.niveles.create({
                    per_id: personaId,
                    niv_id: this.personaNueva.NIV_ID ? Number(this.personaNueva.NIV_ID) : 1,
                    ram_id: ramId
                });
             } catch {}
        }
        
        console.log('🔄 Recargando lista de personas... (forzada)');
        await this.cargarPersonas(true);
        // Forzar recarga de filtros
        try { await this.cargarOpcionesFiltros(true); } catch(e){ console.warn('No se pudo forzar recarga de filtros tras creación:', e); }
        
        if (this.filtroAplicado) {
          console.log('🔍 Reaplicando filtros...');
          await this.filtrar();
        }
        
        this.cerrarModalCrear();
        
        alert('¡Persona creada exitosamente!');
        
      } catch (error) {
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
        alert(mensajeError);
      } finally {
        this.guardandoPersona = false;
      }
    }
    ,
    
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
    // Do NOT auto-load mantenedores/filter options on mount to avoid 401 delays.
    // Lazy-load when the user opens each dropdown.
    // Do NOT auto-load personas on mount; wait until the user applies filtros.
  },
};
</script>

<style>
.gestion-personas {
  box-sizing: border-box;
  margin: 0;
    /* The outer layout (`.main-content`) already applies a top padding
      to account for the navbar height. Avoid adding an extra margin
      here which caused double spacing on desktop. */
    margin-top: 0;
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
  /* Let the container size naturally; do not force full-viewport
     absolute sizing which conflicted with the navbar and sticky filters. */
  height: auto;
  max-width: 100%;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;

  /* Provide BaseButton design tokens locally so variants render correctly */
  --color-primary: #1d4ed8;              /* blue */
  --color-primary-hover: #1e40af;        /* darker blue */
  --color-secondary: #4b5563;            /* gray */
  --color-secondary-hover: #374151;      /* darker gray */
  --color-success: #16a34a;              /* green */
  --color-success-hover: #15803d;
  --color-info: #3b82f6;                 /* info blue */
  --color-info-hover: #1d4ed8;
  --color-warning: #f59e0b;              /* amber */
  --color-warning-hover: #d97706;
  --color-danger: #ef4444;               /* red */
  --color-danger-hover: #dc2626;
  --color-text: #111827;
  --btn-radius: 8px;
  --btn-font-weight: 600;
  --btn-shadow: 0 2px 8px rgba(40,92,168,0.08);
  --ring-color: rgba(33, 78, 156, 0.25);
  --ring-color-weak: rgba(75, 85, 99, 0.25);
}

.gestion-personas .header h2 {
  color: #111;
  font-size: 1.5rem; /* ~24px, similar a Envío de Correos */
  font-weight: 700;
  line-height: 1.25;
  margin: 0 0 6px 0;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  text-align: left !important;
  text-transform: none !important;
  text-shadow: none !important;
  letter-spacing: normal !important;
}

.gestion-personas .header h3 {
  margin: 0 0 8px 0;
  color: #6b7280; /* gris suave */
  font-weight: 500;
  font-size: 0.95rem; /* ~15px */
  line-height: 1.5;
  background: transparent !important;
  text-align: left !important;
  text-transform: none !important;
  text-shadow: none !important;
  letter-spacing: normal !important;
}

/* Header container styled like Emails screen: plain text with subtle divider */
.gestion-personas .header {
  padding: 4px 0 10px 0;
  border-bottom: 1px solid #e5e7eb; /* línea fina como en la imagen */
  margin-bottom: 12px;
  background: transparent !important;
}

.gestion-personas .filtros {
  display: flex;
  gap: 10px;
  align-items: center;
  flex: 0 0 auto;
  padding: 10px 24px;
  min-height: 44px;
  max-height: none;
  flex-wrap: wrap;
  box-sizing: border-box;
  background: #fff;
  z-index: 10;
  border-bottom: 1px solid #e0e0e0;
}
.gestion-personas .filtros-left { display:flex; gap:12px; align-items:center; flex: 1 1 auto; min-width: 0 }
.gestion-personas .filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

.gestion-personas .filtros input,
.gestion-personas .filtros select {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  color: #222;
  background: var(--color-background-soft);
}

.gestion-personas .filtros input { flex: 1 1 0; }
.gestion-personas .filtros select { flex: 0 0 160px; }

.gestion-personas .filtros .base-input { flex: 1 1 420px; min-width: 180px; max-width: 720px; margin-bottom: 0; }
.gestion-personas .filtros .base-input .base-field { padding: 10px 12px; font-size: 14px; }
.gestion-personas .filtros .base-select { flex: 0 0 160px; min-width: 120px; max-width: 220px; margin-bottom: 0; }
.gestion-personas .filtros .base-select .base-select__element { padding: 8px 10px; font-size: 14px; }
.gestion-personas .filtros button { flex: 0 0 auto; flex-shrink: 0; }

.filtros-left { display:flex; gap:12px; align-items:center; flex: 1 1 auto; min-width: 0 }
.filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

/* Acciones principales (siempre visibles) */
.gestion-personas .acciones-top {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
  padding: 8px 24px;
  box-sizing: border-box;
}
.gestion-personas .acciones-top-desktop {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: flex-end;
}

.gestion-personas .filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

/* Desktop placement: actions inside the filters right area (do not overlap content) */
.acciones-top-desktop {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: flex-end;
}

/* Ensure the filters right area keeps its content aligned correctly */
.filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

@media (max-width: 768px) {
  .gestion-personas .acciones-top { padding-left: 16px; padding-right: 16px; gap: 10px; justify-content: space-between; }
}

/* Very narrow mobile screens (tall 21:9 phones): stack buttons vertically for usability */
@media (max-width: 420px), (max-aspect-ratio: 9/21) {
  .gestion-personas .acciones-top {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    align-items: stretch !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    overflow-x: visible !important;
    white-space: normal !important;
  }

  .gestion-personas .acciones-top .btn-standard {
    width: 100% !important;
    min-width: 0 !important;
    padding: 12px 14px !important;
    font-size: 15px !important;
  }

  /* Ensure labels are visible */
  .acciones-top .btn-label { display: inline !important; }
}

/* Mobile: compact action buttons — prefer a single row that wraps when needed.
   This avoids creating extra vertical space which caused the scrollbar in the
   user's screenshot. Buttons will center and shrink as required on narrow
   viewports while keeping labels visible. */
@media (max-width: 480px) {
  .gestion-personas .acciones-top {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: center;
    padding-left: 12px;
    padding-right: 12px;
    box-sizing: border-box;
    overflow-x: hidden; /* prevent horizontal scrolling */
    -webkit-overflow-scrolling: touch;
    max-height: none !important;
  }

  .gestion-personas .acciones-top .btn-standard {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-width: 0 !important;        /* allow shrink */
    flex: 0 1 auto !important;      /* shrink when needed */
    padding: 10px 12px !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06) !important;
    white-space: nowrap !important;
  }

  .gestion-personas .acciones-top .btn-add {
    background: linear-gradient(180deg,#1e40af,#1e3a8a) !important;
    color: #fff !important;
    border: none !important;
  }

  .gestion-personas .acciones-top .btn-import,
  .gestion-personas .acciones-top .btn-export {
    background: linear-gradient(180deg,#6b7280,#4b5563) !important;
    color: #fff !important;
    border: none !important;
  }

  /* Keep icons tidy */
  .gestion-personas .acciones-top .btn-standard svg,
  .gestion-personas .acciones-top .btn-standard .icon {
    width: 16px;
    height: 16px;
  }
}

/* Reinforce mobile behavior up to 768px: keep top action buttons stacked and
   fully labeled (do not collapse to icons). This ensures older mobile styles
   are preserved even after other responsive tweaks. */
@media (max-width: 768px) {
  /* Keep top action buttons on a single horizontal line on mobile; allow
     horizontal scroll if needed. Maintain mobile sizing but prevent collapse
     into stacked layout. */
  .gestion-personas .acciones-top {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
    align-items: center !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    overflow-x: hidden !important;
    -webkit-overflow-scrolling: touch !important;
    white-space: nowrap !important;
  }

  .gestion-personas .acciones-top .btn-standard {
    flex: 0 0 auto !important;
    min-width: 120px !important;
    padding: 10px 12px !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    box-shadow: 0 6px 18px rgba(16,24,40,0.06) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
  }

  .gestion-personas .acciones-top .btn-add {
    background: linear-gradient(180deg,#1e40af,#1e3a8a) !important;
    color: #fff !important;
    border: none !important;
  }

  .gestion-personas .acciones-top .btn-import,
  .gestion-personas .acciones-top .btn-export {
    background: linear-gradient(180deg,#6b7280,#4b5563) !important;
    color: #fff !important;
    border: none !important;
  }

  .gestion-personas .acciones-top .btn-standard svg,
  .gestion-personas .acciones-top .btn-standard .icon {
    width: 16px !important;
    height: 16px !important;
  }

  /* Ensure top actions always show labels on mobile */
  .gestion-personas .acciones-top .btn-label { display: inline !important; }
}

/* Medium-small screens: allow wrapping so buttons always quepan on screen */
@media (max-width: 768px) and (min-width: 481px) {
  .gestion-personas .acciones-top {
    flex-wrap: wrap;
    gap: 10px;
    padding-left: 16px;
    padding-right: 16px;
    justify-content: center;
  }

  /* Make buttons share the row but allow them to shrink and wrap */
  .gestion-personas .acciones-top .btn-standard {
    flex: 1 1 calc(33.333% - 12px);
    min-width: 0;
    padding: 10px 12px;
    font-size: 15px;
    border-radius: 8px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
  }

  /* If space is too narrow, two per row is fine — the calc will wrap */
  .gestion-personas .acciones-top .btn-add { order: 0; }
  .gestion-personas .acciones-top .btn-import { order: 1; }
  .gestion-personas .acciones-top .btn-export { order: 2; }
}

/* Small tweak to avoid large horizontal shadows causing overflow */
.gestion-personas .acciones-top .btn-standard { overflow: hidden; }

.gestion-personas .filtros input,
.gestion-personas .filtros select {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  color: #222;
  background: var(--color-background-soft);
}

.gestion-personas .filtros input {
  flex: 1 1 0;
}
.gestion-personas .filtros select {
  flex: 0 0 160px;
}


.gestion-personas .filtros .base-input {
  flex: 1 1 420px; 
  min-width: 180px;
  max-width: 720px;
  margin-bottom: 0; 
}
.gestion-personas .filtros .base-input .base-field {
  padding: 10px 12px;
  font-size: 14px;
}
.gestion-personas .filtros .base-select {
  flex: 0 0 160px; 
  min-width: 120px;
  max-width: 220px;
  margin-bottom: 0;
}
.gestion-personas .filtros .base-select .base-select__element {
  padding: 8px 10px;
  font-size: 14px;
}
.gestion-personas .filtros button {
  flex: 0 0 auto;
  flex-shrink: 0; 
}

.gestion-personas .buscar, .gestion-personas .exportar {
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
/* Let BaseButton control visual styling via its variant classes */
/* (Do not override background/color for BaseButton instances) */

/* Action buttons use BaseButton variants; avoid overriding their visuals here */

.gestion-personas .btn-search, .gestion-personas .btn-export, .gestion-personas .btn-edit, .gestion-personas .btn-ver, .gestion-personas .btn-editar, .gestion-personas .btn-anular, .gestion-personas .btn-save, .gestion-personas .btn-confirm {
  padding: 8px 14px;
  border-radius: 8px;
  font-weight:700;
  transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
}
.gestion-personas .btn-search:hover, .gestion-personas .btn-export:hover, .gestion-personas .btn-edit:hover, .gestion-personas .btn-ver:hover, .gestion-personas .btn-editar:hover, .gestion-personas .btn-anular:hover, .gestion-personas .btn-save:hover, .gestion-personas .btn-confirm:hover { transform: translateY(-2px); }
.gestion-personas .btn-search:active, .gestion-personas .btn-export:active, .gestion-personas .btn-edit:active, .gestion-personas .btn-ver:active, .gestion-personas .btn-editar:active, .gestion-personas .btn-anular:active, .gestion-personas .btn-save:active, .gestion-personas .btn-confirm:active { transform: translateY(0); }
/* Allow BaseButton to render its focus ring */
.gestion-personas .btn-search:focus, .gestion-personas .btn-export:focus, .gestion-personas .btn-edit:focus, .gestion-personas .btn-ver:focus, .gestion-personas .btn-editar:focus, .gestion-personas .btn-anular:focus, .gestion-personas .btn-save:focus, .gestion-personas .btn-confirm:focus { outline: auto; }

/* Nuevos estilos estandarizados basados en la pantalla de correos */
.gestion-personas .btn-standard {
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

.gestion-personas .btn-standard:hover {
  filter: brightness(0.95) !important;
  box-shadow: 0 4px 16px rgba(40,92,168,0.13) !important;
  transform: translateY(-1px) !important;
}

.gestion-personas .btn-action {
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

.gestion-personas .btn-action:hover {
  filter: brightness(0.95) !important;
  box-shadow: 0 2px 8px rgba(40,92,168,0.1) !important;
  transform: translateY(-1px) !important;
}

.gestion-personas .btn-modal {
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
  gap: 6px;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  padding-right: 12px;
}

.acciones-buttons .base-button {
  font-size: 12px;
  padding: 6px 10px;
  min-width: 0;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
}

/* When horizontal space is constrained (e.g. sidebar expanded), show icon-only
  buttons in the actions column to avoid horizontal overflow. Apply this only
  to intermediate desktop widths (769px - 1200px) so mobile behavior stays
  intact (<=768px). */
@media (min-width: 769px) and (max-width: 1200px) {
  .acciones-buttons {
    gap: 6px;
  }

  .acciones-buttons .btn-label {
    display: none !important;
  }

  .acciones-buttons .base-button,
  .acciones-buttons .btn-action {
    padding: 6px !important;
    min-width: 40px !important;
    font-size: 0 !important; /* hide any stray text; icons are sized separately */
  }

  .acciones-buttons .base-button svg,
  .acciones-buttons .btn-action svg {
    width: 18px !important;
    height: 18px !important;
  }

  .acciones-buttons .base-button::after { content: none; }

  /* When sidebar is expanded (narrower content area), reduce width given to
     Rol and Email columns so action buttons remain on-screen. */
  tbody td[data-label="Rol"],
  tbody td[data-label="Email"] {
    max-width: 120px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
  }
}

/* Sidebar-aware adjustments: ensure this view adapts when the sidebar
   is expanded or collapsed. App layout sets `margin-left` on `.main-content`
   using `--sidebar-width` / `--sidebar-collapsed-width`, so we only need
   to tweak internal padding and table sizing to avoid overflow. */
@media (min-width: 769px) {
  .app-layout .sidebar + .main-content .gestion-personas {
    /* keep full width inside main content but add comfortable padding */
    padding-left: 24px;
    padding-right: 24px;
    box-sizing: border-box;
  }

  .app-layout .sidebar.collapsed + .main-content .gestion-personas {
    /* slightly reduce horizontal padding when sidebar is collapsed */
    padding-left: 16px;
    padding-right: 16px;
  }

  .app-layout .sidebar + .main-content .gestion-personas .table-wrapper {
    max-width: 100%;
    overflow-x: auto;
  }

  /* When sidebar is collapsed we can show full button labels more often. */
  .app-layout .sidebar.collapsed + .main-content .gestion-personas .acciones-buttons .btn-label {
    display: inline !important;
  }
}

.editar { padding: 6px 10px; }

.filtro-activo {
  background-color: var(--color-background-mute);
  color: #115e26;
  padding: 6px 8px;
  border-radius: 4px;
  flex: 0 0 auto;
  font-size: 13px;
}

/* Standardized Table Styles from CRUDcursos.vue */
.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow-x: auto;
  flex: 1 1 auto;
  min-height: 0;
  position: relative;
}

.courses-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
  background-color: #ffffff; /* Explicit white background */
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
  white-space: nowrap; /* Prevent headers from breaking awkwardly */
}

.courses-table tbody tr { transition: background-color .12s ease; }
.courses-table tbody tr:hover { background:#f1f5f9; }

/* Column adjustments */
.courses-table th:nth-child(1){ min-width:180px; } /* Nombre */
.courses-table th:nth-child(2){ min-width:110px; } /* RUT */
.courses-table th:nth-child(3){ min-width:160px; } /* Email */
.courses-table th:nth-child(4){ min-width:120px; } /* Rol */
.courses-table th:nth-child(5){ min-width:120px; } /* Fono */
.courses-table th:nth-child(6){ min-width:100px; } /* Estado */
.courses-table th:last-child { min-width: 180px; padding-right: 16px; } /* Acciones */

.actions-cell {
  display: flex;
  gap: 8px;
  align-items: center;
}

.no-results {
  text-align: center;
  padding: 32px;
  color: #6b7280;
  background-color: #fff;
}

/* Badges Standardized */
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
  border: none; /* Reset border from old implementation */
  box-shadow: none; /* Reset shadow from old implementation */
}

.badge.activo, .badge.vigente, .badge.confirmado, .badge.aprobado { background-color: #d1fae5; color: #065f46; }
.badge.inactivo, .badge.no-vigente, .badge.no-aprobado { background-color: #fee2e2; color: #991b1b; }
.badge.pendiente { background-color: #fef3c7; color: #92400e; }
.badge.anulado { background-color: #e5e7eb; color: #374151; text-decoration: line-through; }

/* Anulado row styling adaptation */
.persona-anulada {
  background-color: #f3f4f6 !important;
}
.persona-anulada td {
  color: #9ca3af !important;
}
.persona-anulada .badge.anulado {
  background: #e5e7eb !important;
  color: #6b7280 !important;
}

/* Legacy styles for history panel (unchanged but cleaned up if needed) */
.historial-anulado { opacity: 0.7; }
.historial-item-anulado { background-color: #f3f4f6 !important; opacity: 0.8; }
.historial-content-anulado { opacity: 0.9; }
.historial-main-anulado, .historial-main-anulado strong { color: #6b7280 !important; text-decoration: line-through; }
.curso-badge-anulado { background: #d1d5db !important; color: #4b5563 !important; text-decoration: line-through; }
.aprobacion-badge-anulado { opacity: 0.6; text-decoration: line-through; }
.aprobacion-badge-anulado.aprobado, .aprobacion-badge-anulado.no-aprobado { background: #e5e7eb !important; color: #6b7280 !important; }

.detail-panel .detalle { flex: 0 0 auto; margin-top: 18px; padding: 14px 18px; background: #f6f7f9; border-radius: 6px; }
.detail-panel .detalle h4 { margin: 0 0 10px 0; color:#1e3a8a; font-size: 20px; font-weight:700 }


/* Responsive para tablets y pantallas medianas */
@media (max-width: 1200px) {
  .filtros {
    flex-wrap: wrap;
    padding: 12px 24px;
  }
  
  .filtros .base-input {
    flex: 1 1 300px;
  }
  
  .main-area {
    padding: 12px 24px;
  }
}

/* Responsive para tablets pequeñas */
@media (max-width: 960px) {
  .filtros {
    flex-wrap: wrap;
    gap: 10px;
    padding: 12px 20px;
  }
  
  .filtros-left {
    width: 100%;
  }
  
  .filtros-right {
    width: 100%;
  }
  
  .main-area {
    padding: 12px 20px;
  }
}

/* Responsive para móviles (incluyendo 21:9) */
@media (max-width: 768px) {
  /* Hide desktop-only actions on mobile */
  .acciones-top-desktop { display: none !important; }
  /* Do not show desktop actions embedded in filters on mobile */
  .filtros-right { display: none !important; }

  .gestion-personas {
    border-radius: 0;
  }
  
  /* Two-row mobile layout: Row 1 = search (full width), Row 2 = selects + Buscar arranged into two columns */
  .filtros-mobile {
    display: grid;
    grid-template-columns: 260px 260px; /* fixed widths for symmetric columns */
    grid-auto-rows: auto;
    align-items: start;
    justify-content: center; /* center the grid itself */
    gap: 8px 12px;
    padding: 8px 12px;
    max-width: 560px;
    margin: 0 auto;
  }
  
  .filtros-mobile .filtros-left,
  .filtros-mobile .filtros-right {
    width: 100%;
    display: contents; /* let children participate directly in the grid */
  }
  
  /* Row 1: the first input (search) spans full width */
  .filtros-mobile .base-input:first-child {
    grid-row: 1;
    grid-column: 1 / -1;
    width: 100% !important;
    max-width: 560px !important;
    margin: 0 auto !important;
  }

  /* Row 2+: subsequent controls fill the two columns and wrap as needed */
  .filtros-mobile .base-select,
  .filtros-mobile .btn-search,
  .filtros-mobile .base-button.btn-search {
    grid-row: auto;
    grid-column: span 1;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    width: 100% !important;
    max-width: 260px !important;
    justify-self: center; /* center each control inside its grid cell */
  }

  /* Place Buscar button spanning both columns at the end for clarity */
  .filtros-mobile .btn-search {
    grid-column: 1 / -1;
    max-width: 560px !important;
    justify-content: center;
    justify-self: center; /* ensure centered spanning button */
  }

  /* Ensure inner elements fill their containers for consistent sizes */
  .filtros-mobile .base-input .base-field,
  .filtros-mobile .base-select .base-select__element {
    width: 100% !important;
    box-sizing: border-box;
  }

  /* Make the row scroll horizontally on very narrow screens rather than stacking into many rows */
  .filtros-mobile { overflow-x: hidden; }

  /* Reduce vertical whitespace between filter controls on mobile */
  .filtros-mobile .base-input,
  .filtros-mobile .base-select,
  .filtros-mobile .btn-search {
    margin: 0 !important; /* remove extra margins added by inner components */
  }
  .filtros-mobile .base-input .base-field,
  .filtros-mobile .base-select .base-select__element {
    margin: 0 !important;
  }
  /* Compact padding to avoid tall gaps */
  .filtros-mobile .base-input .base-field {
    padding: 10px 12px !important;
  }
  .filtros-mobile .base-select .base-select__element {
    padding: 10px 12px !important;
  }

  /* Reduce vertical whitespace between filter controls on mobile */
  .filtros-mobile .base-input,
  .filtros-mobile .base-select,
  .filtros-mobile .btn-search {
    margin: 0 !important; /* remove extra margins added by inner components */
  }
  .filtros-mobile .base-input .base-field,
  .filtros-mobile .base-select .base-select__element {
    margin: 0 !important;
  }
  /* Compact padding to avoid tall gaps */
  .filtros-mobile .base-input .base-field {
    padding: 10px 12px !important;
  }
  .filtros-mobile .base-select .base-select__element {
    padding: 10px 12px !important;
  }
  
  /* Tabla responsiva estilo tarjetas */
  .table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  table {
    min-width: 100%;
  }
  
  thead {
    display: none;
  }
  
  tbody tr {
    display: block;
    margin-bottom: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    background: var(--color-surface);
  }
  
  tbody td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #f0f0f0;
    text-align: left;
  }
  
  tbody td:last-child {
    border-bottom: none;
  }
  
  td[data-label]::before {
    content: attr(data-label) ": ";
    font-weight: 600;
    color: #333;
    margin-right: 8px;
  }
  
  /* Botones de acción en móviles */
  td .btn-action {
    font-size: 12px;
    padding: 6px 12px;
  }
  /* Botón toggle de filtros en móvil */
  .filtros-toggle-mobile {
    display: block;
    text-align: center; /* center the toggle */
    padding: 0 16px 8px;
    z-index: 120; /* keep toggle above other elements */
    position: relative;
  }
  .btn-toggle-filtros {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    font-size: 14px;
    border-radius: 8px;
    margin: 0 auto; /* center inline-flex button */
    /* No sobrescribir colores/box-shadow: usar las reglas de `.btn-standard` para mantener diseño consistente */
  }

  /* Cuando está colapsado en móvil, minimizar visualmente la barra */
  .filtros-mobile.filtros-collapsed {
    background: transparent !important;
    border-bottom: none !important;
    padding-top: 6px !important;
    padding-bottom: 6px !important;
    min-height: 0 !important;
  }
  .filtros-mobile.filtros-collapsed .filtros-left,
  .filtros-mobile.filtros-collapsed .filtros-right {
    display: none !important;
  }
  /* Fuerza ocultamiento de componentes internos (InputBase, BaseSelect, botón Buscar) */
  .filtros-mobile.filtros-collapsed .base-input,
  .filtros-mobile.filtros-collapsed .base-select,
  .filtros-mobile.filtros-collapsed .btn-search,
  .filtros-mobile.filtros-collapsed .base-button:not(.btn-toggle-filtros) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
  }
  
  /* Ajustar detalle en móviles */
  .detalle {
    width: 100%;
    max-width: 100%;
  }
}

/* Móviles pequeños y pantallas 21:9 */
@media (max-width: 520px) {
  .filtros {
    padding: 8px 12px;
  }
  
  .main-area {
    padding: 8px 12px;
    gap: 12px;
  }
  
  .btn-standard {
    padding: 10px 16px;
    font-size: 14px;
  }
  
  tbody tr {
    margin-bottom: 8px;
  }
  

  /* Mejorar presentación de las filas (tarjetas) en móvil: etiquetas arriba, valores legibles */
  tbody tr {
    padding: 8px 10px;
    border-radius: 8px;
  }

  /* Compact inline mobile layout: labels and values on the same line */
  tbody td {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 4px 8px; /* further reduced padding */
    border-bottom: 1px solid rgba(240,240,240,0.9);
    line-height: 1.05;
    white-space: normal;
    overflow: visible;
  }

  td[data-label]::before {
    display: inline-block;
    margin-right: 8px;
    color: #6b7280;
    font-size: 11px; /* smaller label */
    font-weight: 600;
    text-transform: none;
    flex: 0 0 70px; /* slightly narrower label column to give more space to values */
    max-width: 70px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* value area */
  td[data-label] {
    color: #111;
    font-size: 12px;
    flex: 1 1 auto;
    min-width: 0; /* allow flex children to shrink */
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Name: allow wrapping across 1-2 lines and keep it prominent */
  td[data-label="Nombre"] {
    font-size: 14px;
    font-weight: 700;
    /* default: allow wrapping on mobile — overridden in desktop rules */
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
  }

  /* Rol: allow wrapping and align to top so the role value can occupy more space and wrap nicely */
  td[data-label="Rol"] {
    font-size: 12px;
    white-space: normal;
    overflow: visible;
    align-items: flex-start;
  }

  /* Email: behave like Nombre/Rol on mobile — allow up to 2 lines, then ellipsis */
  td[data-label="Email"] {
    font-size: 12px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
  }

  /* On mobile we allow the truncate span to expand to 2 lines; override display */
  @media (max-width: 768px) {
    td[data-label] .truncate {
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: normal;
      max-width: 100%;
    }
  }

  /* Ensure mobile forces wrapping for role even if other rules exist */
  td[data-label="Rol"] * { white-space: normal !important; }
  td[data-label="Rol"] { white-space: normal !important; align-items: flex-start !important; }

  /* Estado: compact badge */
  td[data-label="Estado"] { display: flex; align-items: center; justify-content: space-between; }
  .estado { padding: 4px 8px; font-size: 12px; border-radius: 10px; }

  /* Actions: smaller, tighter, wrap */
  .acciones-buttons {
    justify-content: flex-start;
    gap: 6px;
    padding: 8px 12px 12px 12px;
    flex-wrap: wrap;
  }

  .acciones-buttons .base-button {
    font-size: 12px;
    padding: 6px 8px;
    border-radius: 8px;
    min-width: auto;
  }

  /* Reduce card margins to fit more on screen */
  tbody tr { margin-bottom: 6px; }

  /* Hide less important fields on very narrow/wide-tall screens to save space */
  @media (max-width: 420px) {
    td[data-label="Email"],
    td[data-label="Teléfono/Celular"] {
      display: none;
    }
    /* further compact the name */
    td[data-label="Nombre"] { font-size: 14px; }
  }
  tbody td {
    padding: 8px 10px;
    font-size: 13px;
  }
  /* Force the list of cards to fit the viewport so ~3 items are visible on mobile.
     Adjust the `160px` value if your header/filters area height differs. */
  .table-wrapper {
    max-height: calc(100vh - 160px);
    /* Fallback using viewport units to ensure consistent behaviour across layouts */
    max-height: var(--cards-viewport-height, 62vh) !important;
  }

  /* When filters are collapsed on mobile, make sure the table-wrapper uses
     the full available viewport height below the action buttons by using the
     precomputed CSS variable. This prevents leaving unused white space and
     lets the list fill the remaining area. */
  .filtros.filtros-collapsed ~ .main-area .table-wrapper {
    max-height: var(--cards-viewport-height, 62vh) !important;
    height: var(--cards-viewport-height, 62vh) !important;
    overflow-y: auto !important;
  }

  tbody {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  tbody tr {
    flex: 0 0 calc((100% - 16px) / 3);
    /* Explicit fallback: approximately one third of viewport height */
    height: calc((var(--cards-viewport-height, 62vh) - 16px) / 3) !important;
    margin-bottom: 8px;
    overflow: hidden;
  }

  tbody td {
    padding: 6px 8px;
  }
  
  /* Ajustar modales para móviles */
  .modal-edit,
  .modal-crear {
    width: 100% !important;
    max-width: 100% !important;
    height: 100% !important;
    max-height: 100vh !important;
    border-radius: 0 !important;
  }
  
  .modal-header-editar,
  .modal-header-crear {
    padding: 12px 16px;
  }
  
  .modal-tabs {
    padding: 12px 16px 0 16px !important;
    gap: 4px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .modal-tabs button {
    padding: 8px 12px !important;
    font-size: 13px !important;
    white-space: nowrap;
  }
  
  .form-grid-editar,
  .modal-form-crear {
    padding: 16px !important;
  }
}

/* Pantallas muy estrechas (21:9 en posición vertical) */
@media (max-width: 380px) {
  .filtros {
    padding: 8px;
  }
  
  .main-area {
    padding: 8px;
  }
  
  .filtros-right {
    flex-direction: column;
  }
  
  tbody td {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  td[data-label]::before {
    display: block;
    margin-bottom: 4px;
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

/* Desktop / tablet: restore table layout and clamp long fields so roles don't stretch the list */
@media (min-width: 769px) {
  /* Ensure header/table are visible (desktop layout) */
  thead { display: table-header-group !important; }

  /* Reset mobile card styles to table behaviour */
  tbody td,
  tbody td[data-label="Nombre"],
  tbody td[data-label="Rol"],
  tbody td[data-label="Email"] {
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Ensure the actions column is always visible on desktop: prevent clipping
     and keep action buttons in a single non-wrapping row. */
  tbody td:last-child,
  thead th:last-child {
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: initial !important;
    min-width: 180px !important;
    width: auto !important;
  }

  .acciones-top,
  .acciones-buttons {
    justify-content: flex-end;
  }

  .acciones-buttons .base-button,
  .acciones-buttons button {
    display: inline-flex !important;
  }

  /* Desktop action placement: style buttons to match original desktop look */
  .acciones-top-desktop .btn-standard {
    min-width: auto !important;
    padding: 10px 16px !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    box-shadow: 0 6px 18px rgba(16,24,40,0.06) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
  }

  .acciones-top-desktop .btn-add {
    background: linear-gradient(180deg,#1e40af,#1e3a8a) !important;
    color: #fff !important;
    border: none !important;
  }
  .acciones-top-desktop .btn-import,
  .acciones-top-desktop .btn-export {
    background: linear-gradient(180deg,#6b7280,#4b5563) !important;
    color: #fff !important;
    border: none !important;
  }

  /* Ensure top actions outside the collapsible filters keep their labels */
  .acciones-top-desktop .btn-label { display: inline !important; }

  /* Position desktop actions to the right of the filters visually. We keep
     the markup outside the filters (so mobile collapse won't hide them),
     but visually pin them to the right edge of the filters area. */
  .acciones-top-desktop {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: flex-end;
  }

  /* Keep action buttons in a single row on desktop */
  .acciones-buttons {
    flex-wrap: nowrap !important;
    gap: 8px !important;
  }

  .acciones-buttons .base-button {
    font-size: 12px !important;
    padding: 6px 10px !important;
  }

  /* Prevent very long values from changing column widths */
  td[data-label="Rol"],
  td[data-label="Nombre"],
  td[data-label="Email"] {
    max-width: 220px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
  }

  /* Improve horizontal use of space: fixed table layout + explicit column widths */
  .table-wrapper table {
    table-layout: fixed;
    width: 100%;
  }
  .table-wrapper table th:nth-child(7),
  .table-wrapper table td:nth-child(7) {
    /* Fixed width for actions column so buttons always fit */
    width: 180px !important;
  }

  /* Distribute remaining width among other columns proportionally using calc
     subtracting the fixed actions width so layout doesn't overflow when sidebar
     is expanded. Ratios sum to 1 (28%+10%+26%+18%+10%+8% = 100% of remaining). */
  .table-wrapper table th:nth-child(1), .table-wrapper table td:nth-child(1) { width: calc((100% - 180px) * 0.28); } /* Nombre */
  .table-wrapper table th:nth-child(2), .table-wrapper table td:nth-child(2) { width: calc((100% - 180px) * 0.10); } /* RUT */
  .table-wrapper table th:nth-child(3), .table-wrapper table td:nth-child(3) { width: calc((100% - 180px) * 0.26); } /* Email */
  .table-wrapper table th:nth-child(4), .table-wrapper table td:nth-child(4) { width: calc((100% - 180px) * 0.18); } /* Rol */
  .table-wrapper table th:nth-child(5), .table-wrapper table td:nth-child(5) { width: calc((100% - 180px) * 0.10); } /* Tel */
  .table-wrapper table th:nth-child(6), .table-wrapper table td:nth-child(6) { width: calc((100% - 180px) * 0.08); }  /* Estado */

  /* Allow the inner truncate span to expand to the full column width on desktop */
  td[data-label] .truncate { max-width: 100%; display: inline-block; }

  td[data-label="Rol"], td[data-label="Nombre"] { white-space: nowrap !important; }
  /* Desktop: force uppercase and truncation for Nombre */
  td[data-label="Nombre"] {
    text-transform: uppercase !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    max-width: 220px !important;
  }

  /* Desktop: make Email uppercase as well to match Nombre/Rol */
  td[data-label="Email"] {
    text-transform: uppercase !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    max-width: 220px !important;
  }
  /* Ensure the inner truncate span enforces single-line ellipsis in desktop */
  td[data-label] .truncate {
    display: inline-block;
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: middle;
  }
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
  background: var(--color-surface);
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


/* desktop-specific name styling moved into the desktop media query to avoid overriding mobile rules */

td[data-label="RUT"] { 
  white-space: nowrap; 
}

.estado-carga {
  text-align: center;
  padding: 20px;
  color: #555;
  font-style: italic;
  flex: 0 0 auto;
}

.mensaje-error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  text-align: center;
  flex: 0 0 auto;
}

.mensaje-error button {
  margin-top: 10px;
}

/* Estilos para el modal de creación */
/* ===== ESTILOS PARA MODAL CREAR PERSONA MEJORADO ===== */
.modal-crear {
  width: 100%;
  max-width: 100%;
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
  padding: 16px 20px;
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
  padding: 20px;
}

/* Sección de Foto para Crear */
.foto-container-crear {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 100%;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.foto-perfil-crear {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.foto-perfil-crear:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.foto-placeholder-crear {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  color: #64748b;
  gap: 4px;
  flex-shrink: 0;
}

.foto-placeholder-crear .foto-text {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
}

.foto-actions-crear {
  display: flex;
  flex-direction: row;
  gap: 8px;
  justify-content: center;
}

.foto-actions-crear .btn-foto {
  width: auto;
  min-width: 140px;
  justify-content: center;
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
/* Export modal improved styles */
.modal-exportar-opciones .modal-exportar {
  padding: 16px;
}
.modal-exportar-opciones .modal-header-exportar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
  padding: 8px 0 12px;
}
.modal-exportar-opciones .modal-header-exportar .header-title h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}
.modal-exportar-opciones .modal-header-exportar .subtitle {
  margin: 2px 0 0;
  color: #6b7280;
  font-size: 13px;
}
.modal-exportar-opciones .export-options {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 14px;
}
.modal-exportar-opciones .export-options .hint {
  width: 100%;
  margin-top: 8px;
  color: #6b7280;
  font-size: 12px;
}
/* Make modal compact and centered */
.modal-exportar-opciones .persona-modal {
  max-width: 520px;
}
/* Button emphasis: primary for full export, secondary for emails */
.modal-exportar-opciones .btn-standard {
  min-width: 180px;
}
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
  width: 100%;
  max-width: 100%;
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
  padding: 16px 20px;
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

/* Ocultar el botón X del componente BaseModal en modales de persona */
.persona-modal :deep(.close-btn) {
  display: none !important;
}

/* Tabs mejorados */
  .modal-edit .modal-tabs {
  display: flex;
  gap: 8px;
  padding: 16px 32px 0 32px;
  background: var(--color-surface);
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
  background: var(--color-surface);
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
  background: var(--color-surface);
}

/* Contenedor de formulario con padding */
.modal-edit .modal-form-editar {
  padding: 20px;
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

/* Mensaje de error para validación */
.error-message {
  color: #dc2626;
  font-size: 12px;
  margin-top: 4px;
  display: block;
  font-weight: 500;
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

/* ===== ESTILOS PARA FORMULARIO DE EDICIÓN MEJORADO ===== */
.modal-form-editar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-right: 4px;
  max-height: calc(100vh - 280px);
  overflow-y: auto;
  padding-bottom: 16px;
}

/* Sección de Formulario */
.form-section {
  background: var(--color-surface);
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
  padding: 12px;
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
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
  background: var(--color-surface);
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
  gap: 6px;
  width: 100%;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.foto-preview-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.foto-perfil-editar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.foto-perfil-editar:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.foto-placeholder-editar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  color: #64748b;
  gap: 4px;
  flex-shrink: 0;
}

.foto-placeholder-editar .foto-text {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
}

.foto-actions-editar {
  display: flex;
  flex-direction: row;
  gap: 8px;
  justify-content: center;
}

.foto-actions-editar .btn-foto {
  width: auto;
  min-width: 140px;
  justify-content: center;
}

/* Información de foto */
.foto-info {
  text-align: center;
  margin-top: 0;
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
     background: #fff;
     border-radius: 12px;
     box-shadow: 0 4px 24px rgba(60,60,60,0.08);
  }
  
  .form-section {
     padding: 16px;
     background: #fff;
     border-radius: 12px;
     box-shadow: 0 4px 24px rgba(60,60,60,0.08);
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
  background: var(--color-surface);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.hist-list h4 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 12px;
}

.no-cursos-msg {
  padding: 32px;
  text-align: center;
  color: #64748b;
  font-size: 14px;
}

.hist-list ul { 
  list-style: none; 
  padding: 0; 
  margin: 0;
}

/* Estilos para cursos clickeables */
.historial-curso-item {
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: var(--color-surface);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.historial-curso-item:hover {
  background: #f1f5f9;
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.curso-item-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  cursor: pointer;
  flex: 1;
}

.curso-item-content:hover {
  opacity: 0.9;
}

.curso-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: 8px;
  border-top: 1px solid #e2e8f0;
}

.btn-ver-pagos {
  font-size: 13px;
  padding: 6px 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.curso-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.curso-nombre {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
}

.curso-codigo {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 4px;
}

.curso-info {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.curso-rol {
  font-size: 13px;
  color: #3b82f6;
  font-weight: 500;
  background: #eff6ff;
  padding: 4px 10px;
  border-radius: 4px;
}

.curso-estado {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.curso-estado.aprobado {
  color: #10b981;
  background: #d1fae5;
}

.curso-estado.no-aprobado {
  color: #ef4444;
  background: #fee2e2;
}

.curso-fecha {
  font-size: 13px;
  color: #64748b;
}

.curso-descripcion {
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
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
  background: var(--color-surface);
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
  padding: 40px 32px;
  background: linear-gradient(135deg, #fafafa, #f3f4f6);
  border-radius: 12px;
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

.confirm-icon.success-icon {
  color: #10b981;
  filter: drop-shadow(0 4px 8px rgba(16, 185, 129, 0.3));
}

.confirm-content p {
  font-size: 17px;
  color: #1f2937;
  margin-bottom: 8px;
  line-height: 1.6;
  font-weight: 500;
  max-width: 500px;
}

.confirm-content p:last-of-type {
  margin-bottom: 16px;
}

.confirm-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 24px;
}

.confirm-warning {
  font-size: 14px;
  color: #d97706;
  font-style: italic;
  margin-bottom: 16px !important;
}

/* Los botones de modal ahora usan los estilos del componente BaseButton */
.btn-modal {
  min-width: 120px;
}

/* Estilos para el modal de importar Excel - Diseño mejorado */
.modal-importar {
  width: 100%;
  max-width: 100%;
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
  padding: 16px 20px;
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
  background: var(--color-surface);
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
  background: var(--color-surface);
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
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
  flex: 0 0 auto;
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
  
  /* En móviles, ocultar sidebar y usar todo el espacio */
  .gestion-personas {
    margin-left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
  }
}

/* Adaptación específica para pantallas 21:9 en orientación vertical */
@media (max-aspect-ratio: 9/21) and (max-width: 480px) {
  .gestion-personas {
    padding: 8px;
    gap: 10px;
  }
  
  .filtros {
    gap: 8px;
  }
  
  .btn-standard {
    font-size: 13px;
    padding: 8px 12px;
  }
  
  tbody td {
    font-size: 13px;
    padding: 8px 10px;
  }
}

/* Force stacking for ultra-narrow/tall phones so mobile UX is usable */
@media (max-width: 420px), (max-aspect-ratio: 9/21) {
  .acciones-top {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    overflow-x: visible !important;
    white-space: normal !important;
  }

  .acciones-top .btn-standard {
    width: 100% !important;
    min-width: 0 !important;
    padding: 12px 14px !important;
    font-size: 15px !important;
    border-radius: 10px !important;
  }

  /* Ensure labels remain visible when stacked */
  .acciones-top .btn-label { display: inline !important; }
}

/* Adaptación para pantallas 21:9 en orientación horizontal */
@media (min-aspect-ratio: 21/9) and (max-height: 480px) {
  .gestion-personas {
    max-height: calc(100vh - 80px);
    margin: 8px auto;
  }
  
  .table-wrapper {
    max-height: calc(100vh - 220px);
  }
  
  .modal-edit,
  .modal-crear {
    max-height: calc(100vh - 40px) !important;
  }
}

/* Desktop: Usar todo el ancho disponible */
@media (min-width: 769px) {
  .gestion-personas {
    width: calc(100% - 40px);
    margin: 20px;
  }
}

/* Transiciones suaves en todos los tamaños */
* {
  -webkit-tap-highlight-color: transparent;
}

.gestion-personas,
.filtros,
.table-wrapper,
.modal-edit,
.modal-crear {
  transition: all 0.3s ease;
}

/* Override ordering: ensure on small mobile widths the three main action
   buttons try to stay on the same line by shrinking equally and aligning
   to the start (avoid centering wrapped rows). This rule is placed late
   so it overrides earlier, broader media queries. */
@media (max-width: 520px) {
  .acciones-top {
    justify-content: flex-start !important;
    gap: 8px !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
  }

  .acciones-top .btn-standard {
    flex: 1 1 calc((100% - 16px) / 3) !important; /* three equal buttons */
    min-width: 0 !important;
    max-width: calc((100% - 16px) / 3) !important;
    box-sizing: border-box !important;
    padding: 8px 10px !important;
    font-size: 13px !important;
  }

  /* If labels are too long, allow them to truncate but keep icons visible */
  .acciones-top .btn-standard .btn-label {
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    display: inline-block !important;
    max-width: 70% !important;
  }
}
</style>

<style>
/* DEBUG LAYOUT HELPERS (temporary)
   Add class `debug-layout` to the body to enable outlines.
   Example (in browser console): document.body.classList.add('debug-layout')
   Remove with: document.body.classList.remove('debug-layout') */
.debug-layout .app-layout .sidebar {
  outline: 3px dashed rgba(220, 38, 38, 0.85) !important;
  background: rgba(220, 38, 38, 0.03) !important;
}
.debug-layout .app-layout .main-content {
  outline: 3px dashed rgba(16, 185, 129, 0.85) !important;
  background: rgba(16, 185, 129, 0.02) !important;
}
.debug-layout .gestion-personas {
  outline: 3px dashed rgba(37, 99, 235, 0.85) !important;
  background: rgba(37, 99, 235, 0.02) !important;
}
.debug-layout .table-wrapper {
  outline: 3px dashed rgba(245, 158, 11, 0.85) !important;
  background: rgba(245, 158, 11, 0.02) !important;
}

</style>

<style scoped>
/* RUT popup sizing and layout tweaks (scoped, high specificity) */
.rut-search-modal .rut-row,
.persona-modal.rut-search-modal .rut-row {
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
  justify-content: flex-start !important;
}
.rut-search-modal .rut-input,
.persona-modal.rut-search-modal .rut-input {
  flex: 0 0 30% !important; /* occupy ~30% of the popup width */
  min-width: 140px !important;
  max-width: 420px !important;
}
.rut-search-modal .rut-input input,
.persona-modal.rut-search-modal .rut-input input {
  width: 100% !important;
  box-sizing: border-box !important;
}
.rut-search-modal .rut-dv,
.rut-search-modal .rut-dv input,
.persona-modal.rut-search-modal .rut-dv,
.persona-modal.rut-search-modal .rut-dv input {
  width: 60px !important;
  min-width: 60px !important;
  max-width: 60px !important;
  text-align: center !important;
  box-sizing: border-box !important;
  /* Match form input appearance */
  padding: 12px 15px !important;
  border: 1px solid #e6e6e6 !important;
  border-radius: 6px !important;
  background: #fff !important;
  font-size: 13px !important;
  line-height: 1 !important;
}
.rut-search-modal .btn-search,
.persona-modal.rut-search-modal .btn-search {
  white-space: nowrap !important;
}

@media (max-width: 520px) {
  .rut-search-modal .rut-input,
  .persona-modal.rut-search-modal .rut-input {
    flex: 0 0 48vw !important;
    max-width: 320px !important;
    min-width: 120px !important;
  }
  .rut-search-modal .rut-row,
  .persona-modal.rut-search-modal .rut-row {
    justify-content: center !important;
    flex-wrap: nowrap !important;
  }
}

.persona-modal.rut-search-modal :deep(.modal-overlay) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 24px !important;
  background: rgba(2,6,23,0.45) !important;
}
.persona-modal.rut-search-modal :deep(.modal-content) {
  width: auto !important;
  max-width: 720px !important; /* constrain the BaseModal content */
  box-sizing: border-box !important;
  margin: 0 auto !important;
  border-radius: 12px !important;
  overflow: visible !important;
  background: transparent !important; /* allow inner .modal-crear to provide card background */
}
.persona-modal.rut-search-modal :deep(.modal-content) .modal-crear {
  width: 100% !important;
  max-width: 720px !important;
  background: #fff !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}
.persona-modal.rut-search-modal :deep(.modal-overlay) .modal-crear > * {
  box-sizing: border-box !important;
}
/* Ensure the RUT popup modal-crear does not inherit global full-width rules */
.persona-modal.rut-search-modal .modal-crear {
  width: auto !important;
  max-width: 820px !important;
  box-sizing: border-box !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  margin: 16px auto !important;
}

/* ===========================
   CROPPER MODAL STYLES
   =========================== */
.modal-cropper-foto :deep(.modal-content) {
  max-width: 680px;
  width: 95%;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-cropper {
  display: flex;
  flex-direction: column;
  background: #fff;
}

.modal-header-cropper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-bottom: none;
}

.modal-header-cropper .header-title {
  flex: 1;
}

.modal-header-cropper .header-title h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 6px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
}

.modal-header-cropper .header-title .subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
}

.modal-header-cropper .btn-modal-header {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}

.modal-header-cropper .btn-modal-header:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.cropper-content {
  display: flex;
  gap: 24px;
  padding: 28px;
  background: #f9fafb;
}

.cropper-preview-section {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.cropper-frame {
  position: relative;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  overflow: hidden;
  background: #1a1a1a;
  border: 4px solid #fff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.cropper-image {
  position: absolute;
  top: 50%;
  left: 50%;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  transform-origin: center center;
}

.cropper-mask {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  pointer-events: none;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.4);
}

.preview-hint {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  text-align: center;
  font-weight: 500;
}

.cropper-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 12px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.control-slider-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.slider-value {
  font-size: 13px;
  font-weight: 600;
  color: #667eea;
  min-width: 42px;
  text-align: right;
}

.control-range {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e5e7eb;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.control-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
  transition: all 0.2s ease;
}

.control-range::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 3px 10px rgba(102, 126, 234, 0.6);
}

.control-range::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
  transition: all 0.2s ease;
}

.control-range::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 3px 10px rgba(102, 126, 234, 0.6);
}

.upload-group {
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.btn-upload {
  width: 100%;
  justify-content: center;
}

.modal-footer-cropper {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 28px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
  .cropper-content {
    flex-direction: column;
    align-items: center;
    padding: 20px;
    gap: 20px;
  }

  .cropper-frame {
    width: 240px;
    height: 240px;
  }

  .cropper-controls {
    width: 100%;
  }

  .modal-header-cropper {
    padding: 20px;
  }

  .modal-header-cropper .header-title h2 {
    font-size: 20px;
  }

  .modal-footer-cropper {
    padding: 16px 20px;
  }
}
</style>

