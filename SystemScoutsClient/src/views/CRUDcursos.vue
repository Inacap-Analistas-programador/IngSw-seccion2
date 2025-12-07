<template>
  <div class="crud-cursos-container">
    <div class="page-header">
      <h3>Gestión de Cursos</h3>
  <p>Administra, crea y organiza los cursos de formación.</p>
    </div>

    <!-- Filtros y Acciones -->
    <div class="filters-card">
      <div class="filter-grid">
        <div class="filter-item">
          <InputBase v-model="filtros.searchQuery" placeholder="Buscar…" />
        </div>
        <div class="filter-item">
          <BaseSelect v-model="filtros.estado" :options="opcionesEstado" placeholder="Estado" optionLabel="text" />
        </div>
        <div class="filter-item">
          <BaseSelect v-model="filtros.tipoCurso" :options="tiposCursoOptions" placeholder="Tipo Curso" optionLabel="text" @focus="ensureCatalogo('tipos')" />
        </div>
        <div class="filter-item">
          <BaseSelect v-model="filtros.responsable" :options="personasOptions" placeholder="Responsable" optionLabel="text" @focus="ensureCatalogo('personas')" />
        </div>
      </div>
      <div class="filters-actions">
        <BaseButton @click="aplicarFiltros" :disabled="!hasAnyFilter" variant="primary"><AppIcons name="search" :size="16" /> Buscar</BaseButton>
        <BaseButton @click="limpiarFiltros" variant="neutral"><AppIcons name="x-circle" :size="16" /> Limpiar</BaseButton>
        <BaseButton @click="abrirModalCrear" variant="success"><AppIcons name="plus" :size="16" /> Nuevo Curso</BaseButton>
      </div>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      Cargando datos...
    </div>

    <!-- Tabla de Cursos -->
    <div v-else class="table-container">
      <table class="courses-table">
        <thead>
          <tr>
            <th>Descripción</th>
            <th>Código</th>
            <th>Tipo</th>
            <th>Fechas</th>
            <th>Responsable</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in cursosFiltrados" :key="c.CUR_ID">
            <td>{{ c.CUR_DESCRIPCION || '-' }}</td>
            <td>{{ c.CUR_CODIGO || '-' }}</td>
            <td>{{ getTipoCursoName(c.TCU_ID) }}</td>
            <td>{{ formatDates(c) }}</td>
            <td>
              <div>{{ getPersonaName(c.PER_ID_RESPONSABLE) }}</div>
              <div v-if="c.CAR_ID_RESPONSABLE" style="font-size: 0.85em; color: #666;">{{ getCargoName(c.CAR_ID_RESPONSABLE) }}</div>
            </td>
            <td><span :class="['badge', getEstadoClass(c.CUR_ESTADO)]">{{ getEstadoText(c.CUR_ESTADO) }}</span></td>
            <td class="actions-cell">
              <BaseButton @click="abrirModalEditar(c)" variant="secondary" size="sm"><AppIcons name="edit" :size="14" /> Modificar</BaseButton>
              <BaseButton @click="abrirModalCambioEstadoCurso(c)" variant="warning" size="sm"><AppIcons name="refresh" :size="14" /> Cambio Estado</BaseButton>
              <BaseButton @click="abrirModalVer(c)" variant="info" size="sm"><AppIcons name="eye" :size="14" /> Ver</BaseButton>
              <BaseButton @click="abrirDashboard(c)" variant="primary" size="sm"><AppIcons name="chart-bar" :size="14" /> Dashboard</BaseButton>
            </td>
          </tr>
            <tr v-if="!hasAnyFilter">
              <td colspan="7" class="no-results">Ingrese al menos un filtro para buscar cursos.</td>
            </tr>
            <tr v-else-if="cursosFiltrados.length === 0">
              <td colspan="7" class="no-results">No se encontraron cursos que coincidan con los filtros.</td>
            </tr>
        </tbody>
      </table>
    </div>

    

    <!-- Modal de Creación/Edición de Curso -->
    <BaseModal v-model="mostrarModal" @close="cerrarModal">
      <template #title>{{ esEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</template>
      <div class="modal-body">
        <div class="form-grid-modal">
          <!-- Campos del formulario -->
          <div class="form-group span-2"><label>Descripción del curso</label><InputBase v-model="form.CUR_DESCRIPCION" /><small class="field-hint">Ej: Curso Básico de Primeros Auxilios</small></div>
          <div class="form-group"><label>Código</label><InputBase v-model="form.CUR_CODIGO" /></div>
          <div class="form-group"><label>Tipo de Curso</label><BaseSelect v-model="form.TCU_ID" :options="tiposCursoOptions" optionLabel="text" /><small class="field-hint">Selecciona el tipo de curso</small></div>
          <div class="form-group"><label>Responsable</label><BaseSelect v-model="form.PER_ID_RESPONSABLE" :options="personasOptions" optionLabel="text" /><small class="field-hint">Selecciona a la persona responsable</small></div>
          <div class="form-group"><label>Cargo</label><BaseSelect v-model="form.CAR_ID_RESPONSABLE" :options="cargosOptions" optionLabel="text" /><small class="field-hint">Selecciona el cargo del responsable</small></div>
          <div class="form-group"><label>Fecha de Solicitud</label>
            <InputBase type="date" v-model="form.CUR_FECHA_SOLICITUD" />
            <small class="field-hint">Formato: AAAA-MM-DD (Ej: 2025-11-12)</small>
          </div>
          <!-- Estado ahora es automático; se elimina el selector manual -->
          <div class="form-group"><label>Modalidad</label><BaseSelect v-model="form.CUR_MODALIDAD" :options="opcionesModalidad" optionLabel="text" /><small class="field-hint">Selecciona la modalidad</small></div>
          <div class="form-group"><label>Tipo (Presencial/Online)</label><BaseSelect v-model="form.CUR_TIPO_CURSO" :options="opcionesTipoPresencial" optionLabel="text" /><small class="field-hint">Selecciona si es presencial u online</small></div>
          <div class="form-group"><label>Administra</label><BaseSelect v-model="form.CUR_ADMINISTRA" :options="opcionesAdministra" optionLabel="text" /><small class="field-hint">Indica quién administra el curso</small></div>
          <div class="form-group"><label>Comuna (lugar)</label><BaseSelect v-model="form.COM_ID_LUGAR" :options="comunasOptions" optionLabel="text" /><small class="field-hint">Selecciona la comuna donde se realiza</small></div>
          <div class="form-group span-2"><label>Lugar</label><InputBase v-model="form.CUR_LUGAR" /><small class="field-hint">Ej: Sede Central, Sala 3</small></div>
          
          <!-- Mapa Interactivo -->
          <div class="form-group span-2">
            <label>Ubicación (haz clic en el mapa para seleccionar)</label>
            <MapEmbed
              :lat="form.CUR_COORD_LATITUD"
              :lng="form.CUR_COORD_LONGITUD"
              @update:lat="form.CUR_COORD_LATITUD = $event"
              @update:lng="form.CUR_COORD_LONGITUD = $event"
            />
          </div>
          <div class="form-group"><label>Latitud</label><InputBase v-model="form.CUR_COORD_LATITUD" placeholder="Lat" /><small class="field-hint">Ej: -36.827 (Concepción)</small></div>
          <div class="form-group"><label>Longitud</label><InputBase v-model="form.CUR_COORD_LONGITUD" placeholder="Lng" /><small class="field-hint">Ej: -73.050 (Concepción)</small></div>

          <div class="form-group span-2"><label>Observaciones</label><textarea v-model="form.CUR_OBSERVACION" rows="3"></textarea><small class="field-hint">Notas internas, ej: traer proyector</small></div>
        </div>

        <!-- Sección de Gestión de Fechas -->
        <div class="fechas-section" v-if="esEdicion">
          <hr class="section-divider">
          <div class="section-box">
          <h4>Períodos del Curso</h4>
          
          <!-- Tabla de Fechas Existentes -->
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Inicio</th>
                <th>Término</th>
                <th>Tipo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="fechasCurso.length === 0">
                <td colspan="4" class="no-results-small">No hay períodos definidos.</td>
              </tr>
                <tr v-for="fecha in fechasCurso" :key="fecha.CUF_ID || ('tmp-' + (fecha.__tmpId || 0))">
                  <td>{{ formatDateSimple(fecha.CUF_FECHA_INICIO) }}</td>
                  <td>{{ formatDateSimple(fecha.CUF_FECHA_TERMINO) }}</td>
                  <td>{{ opcionesTipoFecha.find(t => t.value === fecha.CUF_TIPO)?.text }}</td>
                  <td>
                    <BaseButton @click="iniciarEdicionFecha(fecha)" variant="secondary" size="sm">Modificar</BaseButton>
                    <BaseButton @click="eliminarFecha(fecha.CUF_ID || ('tmp-' + (fecha.__tmpId || 0)))" variant="danger" size="sm">Eliminar</BaseButton>
                  </td>
                </tr>
            </tbody>
          </table>

          <!-- Formulario para Añadir Nueva Fecha -->
          <div class="add-fecha-form">
            <div class="form-group">
              <label>Fecha Inicio</label>
              <InputBase type="date" v-model="nuevoPeriodo.CUF_FECHA_INICIO" />
            </div>
            <div class="form-group">
              <label>Fecha Término</label>
              <InputBase type="date" v-model="nuevoPeriodo.CUF_FECHA_TERMINO" />
            </div>
            <div class="form-group">
              <label>Tipo</label>
              <BaseSelect v-model="nuevoPeriodo.CUF_TIPO" :options="opcionesTipoFecha" optionLabel="text" />
            </div>
            <BaseButton v-if="!editandoFecha" @click="agregarFecha" class="add-button">Añadir Período</BaseButton>
            <BaseButton v-if="editandoFecha" @click="guardarEdicionFecha" class="add-button" variant="primary">Guardar</BaseButton>
            <BaseButton v-if="editandoFecha" @click="cancelarEdicionFecha" class="add-button" variant="secondary">Cancelar</BaseButton>
          </div>
          </div>

          <!-- Sección de Gestión de Secciones -->
          <hr class="section-divider">
          <div class="section-box">
          <h4>Secciones del Curso</h4>
          
          <!-- Tabla de Secciones Existentes -->
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Sección</th>
                <th>Rama</th>
                <th>Participantes</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="seccionesCurso.length === 0">
                <td colspan="4" class="no-results-small">No hay secciones definidas.</td>
              </tr>
                <tr v-for="seccion in seccionesCurso" :key="seccion.CUS_ID || ('tmp-' + (seccion.__tmpId || 0))">
                  <td>{{ seccion.CUS_SECCION }}</td>
                  <td>{{ getRamaName(seccion.RAM_ID) }}</td>
                  <td>{{ seccion.CUS_CANT_PARTICIPANTE }}</td>
                  <td>
                    <BaseButton @click="iniciarEdicionSeccion(seccion)" variant="secondary" size="sm">Modificar</BaseButton>
                    <BaseButton @click="eliminarSeccion(seccion.CUS_ID || ('tmp-' + (seccion.__tmpId || 0)))" variant="danger" size="sm">Eliminar</BaseButton>
                  </td>
                </tr>
            </tbody>
          </table>

          <!-- Formulario para Añadir Nueva Sección -->
          <div class="add-fecha-form">
            <div class="form-group">
              <label>Sección #</label>
              <InputBase type="number" v-model="nuevaSeccion.CUS_SECCION" placeholder="Ej: 1, 2, 3..." />
            </div>
            <div class="form-group">
              <label>Rama</label>
              <BaseSelect v-model="nuevaSeccion.RAM_ID" :options="ramasOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Participantes</label>
              <InputBase type="number" v-model="nuevaSeccion.CUS_CANT_PARTICIPANTE" placeholder="Cantidad" />
            </div>
            <BaseButton v-if="!editandoSeccion" @click="agregarSeccion" class="add-button">Añadir Sección</BaseButton>
            <BaseButton v-if="editandoSeccion" @click="guardarEdicionSeccion" class="add-button" variant="primary">Guardar</BaseButton>
            <BaseButton v-if="editandoSeccion" @click="cancelarEdicionSeccion" class="add-button" variant="secondary">Cancelar</BaseButton>
          </div>

          </div>

          <!-- Sección Equipo Formadores -->
          <hr class="section-divider">
          <div class="section-box">
          <h4>Equipo Formadores</h4>
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Persona</th>
                <th>Rol</th>
                <th>Sección</th>
                <th>Director</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!formadoresCurso.length">
                <td colspan="5" class="no-results-small">Sin formadores</td>
              </tr>
              <tr v-for="f in formadoresCurso" :key="f.CUF_ID || ('tmp-' + (f.__tmpId || 0))">
                <td>{{ getPersonaName(f.PER_ID) }}</td>
                <td>{{ rolesList.find(r => r.ROL_ID === f.ROL_ID)?.ROL_DESCRIPCION || '-' }}</td>
                <td>{{ seccionesCurso.find(s => s.CUS_ID === f.CUS_ID)?.CUS_SECCION || '-' }}</td>
                <td>{{ f.CUO_DIRECTOR ? 'Sí' : 'No' }}</td>
                <td>
                  <BaseButton @click="iniciarEdicionFormador(f)" variant="secondary" size="sm">Modificar</BaseButton>
                  <BaseButton @click="eliminarFormador(f)" variant="danger" size="sm">Eliminar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="add-fecha-form add-formadores-form">
            <div class="form-group">
              <label>Persona</label>
              <BaseSelect v-model="nuevaFormador.PER_ID" :options="personasOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Rol</label>
              <BaseSelect v-model="nuevaFormador.ROL_ID" :options="rolesOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Sección</label>
              <BaseSelect v-model="nuevaFormador.CUS_ID" :options="seccionesOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Director</label>
              <input type="checkbox" v-model="nuevaFormador.CUO_DIRECTOR" />
            </div>
            <BaseButton v-if="!editandoFormador" @click="agregarFormador" class="add-button">Añadir Formador</BaseButton>
            <BaseButton v-if="editandoFormador" @click="guardarEdicionFormador" class="add-button" variant="primary">Guardar</BaseButton>
            <BaseButton v-if="editandoFormador" @click="cancelarEdicionFormador" class="add-button" variant="secondary">Cancelar</BaseButton>
          </div>

          </div>

          <!-- Sección Alimentación -->
          <hr class="section-divider">
          <div class="section-box">
          <h4>Cuotas y Alimentación</h4>
          <div class="cuotas-grid">
            <div class="form-group">
              <label>Cuota con Almuerzo</label>
              <InputBase type="number" v-model="form.CUR_COTA_CON_ALMUERZO" />
              <small class="field-hint">Monto en CLP, ej: 15000</small>
            </div>
            <div class="form-group">
              <label>Cuota sin Almuerzo</label>
              <InputBase type="number" v-model="form.CUR_COTA_SIN_ALMUERZO" />
              <small class="field-hint">Monto en CLP, ej: 10000</small>
            </div>
          </div>
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Tiempo</th>
                <th>Tipo Alimentación</th>
                <th>Descripción</th>
                <th>Adic.</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!alimentacionesCurso.length">
                <td colspan="6" class="no-results-small">Sin alimentación</td>
              </tr>
              <tr v-for="a in alimentacionesCurso" :key="a.CUA_ID || ('tmp-' + (a.__tmpId || 0))">
                <td>{{ formatDateSimple(a.CUA_FECHA) }}</td>
                <td>{{ tiempoAlimentacionOptions.find(t => t.value === a.CUA_TIEMPO)?.text }}</td>
                <td>{{ alimentacionCatalogo.find(x => x.ALI_ID === a.ALI_ID)?.ALI_DESCRIPCION || '-' }}</td>
                <td>{{ a.CUA_DESCRIPCION }}</td>
                <td>{{ a.CUA_CANTIDAD_ADICIONAL }}</td>
                <td>
                  <BaseButton @click="iniciarEdicionAlimentacion(a)" variant="secondary" size="sm">Modificar</BaseButton>
                  <BaseButton @click="eliminarAlimentacion(a)" variant="danger" size="sm">Eliminar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="add-fecha-form add-alimentacion-form">
            <div class="form-group">
              <label>Fecha</label>
              <InputBase type="date" v-model="nuevaAlimentacion.CUA_FECHA" />
            </div>
            <div class="form-group">
              <label>Tiempo</label>
              <BaseSelect v-model="nuevaAlimentacion.CUA_TIEMPO" :options="tiempoAlimentacionOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Tipo Alimentación</label>
              <BaseSelect v-model="nuevaAlimentacion.ALI_ID" :options="alimentacionOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <InputBase v-model="nuevaAlimentacion.CUA_DESCRIPCION" />
            </div>
            <div class="form-group">
              <label>Adicional</label>
              <InputBase type="number" v-model="nuevaAlimentacion.CUA_CANTIDAD_ADICIONAL" />
            </div>
            <BaseButton v-if="!editandoAlimentacion" @click="agregarAlimentacion" class="add-button">Añadir Alimentación</BaseButton>
            <BaseButton v-if="editandoAlimentacion" @click="guardarEdicionAlimentacion" class="add-button" variant="primary">Guardar</BaseButton>
            <BaseButton v-if="editandoAlimentacion" @click="cancelarEdicionAlimentacion" class="add-button" variant="secondary">Cancelar</BaseButton>
          </div>

          </div>

          <!-- Sección Cuotas del Curso -->
          <hr class="section-divider">
          <div class="section-box">
          <h4>Cuotas del Curso</h4>
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Fecha</th>
                <th>Monto</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!cuotasCurso.length">
                <td colspan="4" class="no-results-small">Sin cuotas</td>
              </tr>
              <tr v-for="c in cuotasCurso" :key="c.CUU_ID || ('tmp-' + (c.__tmpId || 0))">
                <td>{{ c.CUU_TIPO === 1 ? 'Con Almuerzo' : 'Sin Almuerzo' }}</td>
                <td>{{ formatDateSimple(c.CUU_FECHA) }}</td>
                <td>${{ c.CUU_VALOR }}</td>
                <td>
                  <BaseButton @click="eliminarCuota(c)" variant="danger" size="sm">Eliminar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="add-fecha-form add-cuota-form">
            <div class="form-group">
              <label>Tipo</label>
              <BaseSelect v-model="nuevaCuota.CUU_TIPO" :options="[{value:1,text:'Con Almuerzo'},{value:2,text:'Sin Almuerzo'}]" />
            </div>
            <div class="form-group">
              <label>Fecha</label>
              <InputBase type="date" v-model="nuevaCuota.CUU_FECHA" />
            </div>
            <div class="form-group">
              <label>Monto</label>
              <InputBase type="number" v-model="nuevaCuota.CUU_VALOR" placeholder="15000" />
            </div>
            <BaseButton @click="agregarCuota" class="add-button">Añadir Cuota</BaseButton>
          </div>

          </div>

          <!-- Sección Coordinadores del Curso -->
          <hr class="section-divider">
          <div class="section-box">
          <h4>Coordinadores del Curso</h4>
          <table class="fechas-table">
            <thead>
              <tr>
                <th>Persona</th>
                <th>Cargo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!coordinadoresCurso.length">
                <td colspan="3" class="no-results-small">Sin coordinadores</td>
              </tr>
              <tr v-for="coord in coordinadoresCurso" :key="coord.CUC_ID || ('tmp-' + (coord.__tmpId || 0))">
                <td>{{ getPersonaName(coord.PER_ID) }}</td>
                <td>{{ cargosList.find(c => c.CAR_ID === coord.CAR_ID)?.CAR_DESCRIPCION || '-' }}</td>
                <td>
                  <BaseButton @click="eliminarCoordinador(coord)" variant="danger" size="sm">Eliminar</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="add-fecha-form add-coordinador-form">
            <div class="form-group">
              <label>Persona</label>
              <BaseSelect v-model="nuevoCoordinador.PER_ID" :options="personasOptions" optionLabel="text" />
            </div>
            <div class="form-group">
              <label>Cargo</label>
              <BaseSelect v-model="nuevoCoordinador.CAR_ID" :options="cargosOptions" optionLabel="text" />
            </div>
            <BaseButton @click="agregarCoordinador" class="add-button">Añadir Coordinador</BaseButton>
          </div>
          </div>
        </div>
      </div>
      <template #footer>
        <BaseButton @click="cerrarModal" variant="secondary">Cancelar</BaseButton>
        <BaseButton @click="guardarCurso">Guardar Cambios</BaseButton>
      </template>
    </BaseModal>

    <!-- Modal de Detalle de Curso -->
    <BaseModal v-model="mostrarModalVer" @close="cerrarModalVer">
      <template #title>Detalle del Curso</template>
      <div class="modal-body">
        <div v-if="cursoSeleccionado" class="detalle-curso">
          <p><strong>Descripción:</strong> {{ cursoSeleccionado.CUR_DESCRIPCION }}</p>
          <p><strong>Código:</strong> {{ cursoSeleccionado.CUR_CODIGO }}</p>
          <p><strong>Tipo:</strong> {{ getTipoCursoName(cursoSeleccionado.TCU_ID) }}</p>
          <p><strong>Responsable:</strong> {{ getPersonaName(cursoSeleccionado.PER_ID_RESPONSABLE) }}</p>
          <p><strong>Estado:</strong> {{ getEstadoText(cursoSeleccionado.CUR_ESTADO) }}</p>
          <p><strong>Lugar:</strong> {{ cursoSeleccionado.CUR_LUGAR }}</p>
          <p><strong>Coordenadas:</strong> {{ cursoSeleccionado.CUR_COORD_LATITUD }}, {{ cursoSeleccionado.CUR_COORD_LONGITUD }}</p>
          <p><strong>Observación:</strong> {{ cursoSeleccionado.CUR_OBSERVACION || '-' }}</p>
        </div>
        <h4 class="mt-16">Períodos</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Inicio</th>
              <th>Término</th>
              <th>Tipo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="fechasCurso.length === 0"><td colspan="3" class="no-results-small">Sin períodos</td></tr>
            <tr v-for="f in fechasCurso" :key="f.CUF_ID">
              <td>{{ formatDateSimple(f.CUF_FECHA_INICIO) }}</td>
              <td>{{ formatDateSimple(f.CUF_FECHA_TERMINO) }}</td>
              <td>{{ opcionesTipoFecha.find(t => t.value === f.CUF_TIPO)?.text }}</td>
            </tr>
          </tbody>
        </table>
        <h4 class="mt-16">Secciones</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Sección</th>
              <th>Rama</th>
              <th>Participantes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="seccionesCurso.length === 0"><td colspan="3" class="no-results-small">Sin secciones</td></tr>
            <tr v-for="s in seccionesCurso" :key="s.CUS_ID">
              <td>{{ s.CUS_SECCION }}</td>
              <td>{{ getRamaName(s.RAM_ID) }}</td>
              <td>{{ s.CUS_CANT_PARTICIPANTE }}</td>
            </tr>
          </tbody>
        </table>

        <h4 class="mt-16">Formadores</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Rol</th>
              <th>Sección</th>
              <th>Director</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!formadoresCurso.length"><td colspan="4" class="no-results-small">Sin formadores</td></tr>
            <tr v-for="f in formadoresCurso" :key="f.CUF_ID">
              <td>{{ getPersonaName(f.PER_ID) }}</td>
              <td>{{ rolesList.find(r => r.ROL_ID === f.ROL_ID)?.ROL_DESCRIPCION || '-' }}</td>
              <td>{{ seccionesList.find(s => s.CUS_ID === f.CUS_ID)?.CUS_SECCION || '-' }}</td>
              <td>{{ f.CUO_DIRECTOR ? 'Sí' : 'No' }}</td>
            </tr>
          </tbody>
        </table>

        <h4 class="mt-16">Alimentación</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Tiempo</th>
              <th>Alimento</th>
              <th>Descripción</th>
              <th>Adic.</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!alimentacionesCurso.length"><td colspan="5" class="no-results-small">Sin alimentación</td></tr>
            <tr v-for="a in alimentacionesCurso" :key="a.CUA_ID">
              <td>{{ formatDateSimple(a.CUA_FECHA) }}</td>
              <td>{{ tiempoAlimentacionOptions.find(t => t.value === a.CUA_TIEMPO)?.text }}</td>
              <td>{{ alimentacionCatalogo.find(x => x.ALI_ID === a.ALI_ID)?.ALI_DESCRIPCION || '-' }}</td>
              <td>{{ a.CUA_DESCRIPCION }}</td>
              <td>{{ a.CUA_CANTIDAD_ADICIONAL }}</td>
            </tr>
          </tbody>
        </table>

        <h4 class="mt-16">Cuotas</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Fecha</th>
              <th>Monto</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!cuotasCurso.length"><td colspan="3" class="no-results-small">Sin cuotas</td></tr>
            <tr v-for="c in cuotasCurso" :key="c.CUU_ID">
              <td>{{ c.CUU_TIPO === 1 ? 'Con Almuerzo' : 'Sin Almuerzo' }}</td>
              <td>{{ formatDateSimple(c.CUU_FECHA) }}</td>
              <td>${{ c.CUU_VALOR }}</td>
            </tr>
          </tbody>
        </table>

        <h4 class="mt-16">Coordinadores</h4>
        <table class="fechas-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Cargo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!coordinadoresCurso.length"><td colspan="2" class="no-results-small">Sin coordinadores</td></tr>
            <tr v-for="coord in coordinadoresCurso" :key="coord.CUC_ID">
              <td>{{ getPersonaName(coord.PER_ID) }}</td>
              <td>{{ cargosList.find(c => c.CAR_ID === coord.CAR_ID)?.CAR_DESCRIPCION || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <template #footer>
        <BaseButton @click="cerrarModalVer" variant="secondary">Cerrar</BaseButton>
      </template>
    </BaseModal>

    <!-- Modal Cambio de Estado -->
    <BaseModal :show="mostrarModalCambioEstado" @close="cerrarModalCambioEstado" title="Cambio de Estado">
      <div class="modal-form">
        <div class="form-group">
          <label>Estado Actual: <strong>{{ cursoParaCambioEstado ? (opcionesEstado.find(e => e.value === cursoParaCambioEstado.CUR_ESTADO)?.text || 'Desconocido') : '-' }}</strong></label>
        </div>
        <div class="form-group">
          <label for="nuevo-estado">Nuevo Estado *</label>
          <BaseSelect v-model="nuevoEstado" :options="opcionesEstado" optionLabel="text" optionValue="value" id="nuevo-estado" />
        </div>
      </div>
      <template #footer>
        <BaseButton @click="guardarCambioEstado" variant="primary" :disabled="isDisabling">
          {{ isDisabling ? 'Guardando...' : 'Guardar' }}
        </BaseButton>
        <BaseButton @click="cerrarModalCambioEstado" variant="secondary" :disabled="isDisabling">Cancelar</BaseButton>
      </template>
    </BaseModal>

  <!-- Dashboard del Curso - Overlay completo -->
  <Teleport to="body">
    <div v-if="mostrarDashboard" class="dashboard-overlay">
      <CursoDashboard 
        :cursoId="cursoIdDashboard" 
        @close="cerrarDashboard"
      />
    </div>
  </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { request } from '@/services/apiClient.js'
import cursosService from '@/services/cursosService.js'
import CursoDashboard from './CursoDashboard.vue'
import personasService from '@/services/personasService.js'
import mantenedores from '@/services/mantenedoresService.js'

// Local aliases matching legacy names used across this component
const cursosApi = cursosService.cursos
const seccionesApi = cursosService.secciones
const fechasApi = cursosService.fechas
const formadoresApi = cursosService.formadores
const alimentacionesApi = cursosService.alimentaciones
const cuotasApi = cursosService.cuotas
const coordinadoresApi = cursosService.coordinadores

import InputBase from '@/components/InputBase.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import MapEmbed from '@/components/MapEmbed.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import { comunasCoords } from '@/data/comunasChile.js'

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

// Helper to normalize keys to Lowercase (for backend compatibility)
const toLowerKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj
  const newObj = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    newObj[key.toLowerCase()] = obj[key]
  }
  return newObj
}

// --- Estado y Reactividad ---
const isLoading = ref(false)
const isLoadingData = ref(false) // Guard para prevenir cargas duplicadas
const cursosList = ref([])
const cursosFiltrados = ref([])
const personasList = ref([])
const tiposCursoList = ref([])
const fechasCurso = ref([])
const fechasCursoList = ref([]) // Caché de todas las fechas
const ramaslist = ref([])
const seccionesList = ref([])
const seccionesCurso = ref([])
// Equipo y logística
const rolesList = ref([])
const formadoresCurso = ref([])
const nuevaFormador = ref({ PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false })
const alimentacionesCurso = ref([])
const nuevaAlimentacion = ref({ ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 })
const alimentacionCatalogo = ref([])
const cuotasCurso = ref([])
const nuevaCuota = ref({ CUU_TIPO: 1, CUU_FECHA: '', CUU_VALOR: '' })
const coordinadoresCurso = ref([])
const nuevoCoordinador = ref({ PER_ID: null, CAR_ID: null })
const mostrarModalVer = ref(false)
const cursoSeleccionado = ref(null)
const mostrarDashboard = ref(false)
const cursoIdDashboard = ref(null)
const mostrarModalCambioEstado = ref(false)
const cursoParaCambioEstado = ref(null)
const nuevoEstado = ref(null)

const mostrarModal = ref(false)
const esEdicion = ref(false)
const isTrulyNew = ref(false)
const originalCursoBackup = ref(null)
const originalBuffersBackup = ref({ fechas: [], secciones: [], formadores: [], alimentaciones: [] })
const isSaving = ref(false) // Bandera para prevenir múltiples clics
const isDisabling = ref(false) // Bandera para prevenir múltiples deshabilitar
// Flags de sub-acciones para evitar doble clic
const isAddingPeriodo = ref(false)
const isDeletingPeriodo = ref(false)
const isAddingSeccion = ref(false)
const isDeletingSeccion = ref(false)
const isAddingFormador = ref(false)
const isDeletingFormador = ref(false)
const isAddingAlimentacion = ref(false)
const isDeletingAlimentacion = ref(false)
const isAddingCuota = ref(false)
const isDeletingCuota = ref(false)
const isAddingCoordinador = ref(false)
const isDeletingCoordinador = ref(false)

// Estados de edición para cada sección
const editandoFecha = ref(null)
const editandoSeccion = ref(null)
const editandoFormador = ref(null)
const editandoAlimentacion = ref(null)

const filtros = ref({
  searchQuery: '',
  estado: null,
  tipoCurso: null,
  responsable: null,
})

const hasAnyFilter = computed(() => {
  const f = filtros.value
  return Boolean((f.searchQuery && f.searchQuery.trim()) || f.estado || f.tipoCurso || f.responsable)
})

const form = ref(null)

const inicializarFormulario = () => ({
  CUR_ID: null,
  CUR_DESCRIPCION: '',
  CUR_CODIGO: '',
  TCU_ID: null, // Forzar selección
  PER_ID_RESPONSABLE: null, // Forzar selección
  CUR_FECHA_SOLICITUD: '', // Dejar vacío para que usuario elija
  CUR_COTA_CON_ALMUERZO: null,
  CUR_COTA_SIN_ALMUERZO: null,
  CUR_MODALIDAD: null,
  CUR_TIPO_CURSO: null,
  CUR_LUGAR: '',
  CUR_COORD_LATITUD: '',
  CUR_COORD_LONGITUD: '',
  CUR_ESTADO: null,
  CUR_OBSERVACION: '',
})

form.value = inicializarFormulario()

// --- Opciones para Selects (deberían ser dinámicas o constantes) ---
const opcionesEstado = [
  { value: 0, text: 'Pendiente' },
  { value: 1, text: 'Vigente' },
  { value: 2, text: 'Anulado' },
  { value: 3, text: 'Finalizado' },
]
const opcionesModalidad = [
  { value: 1, text: 'Internado' },
  { value: 2, text: 'Externado' },
  { value: 3, text: 'Internado/Externado' },
]
const opcionesTipoPresencial = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]
const opcionesTipoFecha = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]

// --- Utilities: cache, debounce, safe API wrapper and abort support ---
const _cache = new Map()
function cacheKey(path, params) { return `${path}|${JSON.stringify(params || {})}` }

function debounce(fn, wait = 250) {
  let t
  return (...args) => {
    clearTimeout(t)
    t = setTimeout(() => fn(...args), wait)
  }
}

// Safe list wrapper: intenta usar un objeto API global si existe (e.g., cursosApi),
// si no, hace fallback a `request(path)` (con querystring si params)
async function safeList(apiName, path, params) {
  try {
    const globalObj = typeof globalThis !== 'undefined' ? globalThis[`${apiName}`] : undefined
    if (globalObj && typeof globalObj.list === 'function') {
      return await globalObj.list(params)
    }
  } catch (e) { /* ignore */ }

  // Build querystring for simple GETs
  const qs = params && Object.keys(params).length ? `?${new URLSearchParams(params).toString()}` : ''
  return await request(`${path}${qs}`)
}

// Abort support for fetch: guardamos el controller y cancelamos la carga anterior
const lastController = { ctrl: null }

async function cargarDatos({ page = 1, page_size = 20, search = '' } = {}) {
  if (isLoadingData.value) return
  // Requerir al menos un filtro antes de cargar
  if (!hasAnyFilter.value) {
    cursosList.value = []
    cursosFiltrados.value = []
    return
  }
  isLoadingData.value = true
  isLoading.value = true

  // No bloquear por token aquí: permitimos que el cliente HTTP maneje 401/refresh

  // cancelar carga previa si existe
  try {
    if (lastController.ctrl) lastController.ctrl.abort()
  } catch { /* noop */ }
  lastController.ctrl = new AbortController()
  const signal = lastController.ctrl.signal

  try {
    // Pedir cursos desde el servicio específico y catálogos relacionados
    const cursosCacheKey = cacheKey('cursos/cursos', { page, page_size, search })
    let cursosDataPromise
    if (_cache.has(cursosCacheKey)) {
      cursosDataPromise = _cache.get(cursosCacheKey)
    } else {
      cursosDataPromise = cursosApi.list({ page, page_size, search })
      _cache.set(cursosCacheKey, cursosDataPromise)
    }

    const cursosData = await cursosDataPromise

    // Catálogos y recursos asociados (usar servicios concretos)
    // Solo solicitar catálogos que aún no estén cargados en memoria.
    const fetchPromises = []

    const personasPromise = (Array.isArray(personasList.value) && personasList.value.length) ? Promise.resolve(personasList.value) : personasService.personas.list()
    fetchPromises.push(personasPromise)

    const tiposPromise = (Array.isArray(tiposCursoList.value) && tiposCursoList.value.length) ? Promise.resolve(tiposCursoList.value) : mantenedores.tipoCursos.list()
    fetchPromises.push(tiposPromise)

    const ramasPromise = (Array.isArray(ramaslist.value) && ramaslist.value.length) ? Promise.resolve(ramaslist.value) : mantenedores.rama.list()
    fetchPromises.push(ramasPromise)

    const seccionesPromise = (Array.isArray(seccionesList.value) && seccionesList.value.length) ? Promise.resolve(seccionesList.value) : seccionesApi.list()
    fetchPromises.push(seccionesPromise)

    const fechasPromise = (Array.isArray(fechasCursoList.value) && fechasCursoList.value.length) ? Promise.resolve(fechasCursoList.value) : fechasApi.list()
    fetchPromises.push(fechasPromise)

    const comunasPromise = (Array.isArray(comunasList?.value) && comunasList.value.length) ? Promise.resolve(comunasList.value) : mantenedores.comuna.list()
    fetchPromises.push(comunasPromise)

    const cargosPromise = (Array.isArray(cargosList?.value) && cargosList.value.length) ? Promise.resolve(cargosList.value) : mantenedores.cargo.list()
    fetchPromises.push(cargosPromise)

    const rolesPromise = (Array.isArray(rolesList.value) && rolesList.value.length) ? Promise.resolve(rolesList.value) : mantenedores.rol.list()
    fetchPromises.push(rolesPromise)

    const alimentacionPromise = (Array.isArray(alimentacionCatalogo.value) && alimentacionCatalogo.value.length) ? Promise.resolve(alimentacionCatalogo.value) : mantenedores.alimentacion.list()
    fetchPromises.push(alimentacionPromise)

    const [personasApi, tiposApi, ramasApi, seccionesData, fechasData, comunasApi, cargosApi, rolesApi, alimentacionCat] = await Promise.all(fetchPromises)

    // Normalizar cursos (puede venir paginado)
    let cursosArray = Array.isArray(cursosData) ? cursosData : (cursosData?.results || [])
    cursosArray = cursosArray.map(toUpperKeys)

    // Normalizar listas relacionadas
    const fechasListNorm = (Array.isArray(fechasData) ? fechasData : (fechasData?.results || [])).map(toUpperKeys)
    const seccionesListNorm = (Array.isArray(seccionesData) ? seccionesData : (seccionesData?.results || [])).map(toUpperKeys)
    const formadoresListNorm = [] // Se cargan bajo demanda o si estuvieran aquí
    const alimentacionListNorm = [] // Se cargan bajo demanda
    const cuotasListNorm = [] // Se cargan bajo demanda
    const coordinadoresListNorm = [] // Se cargan bajo demanda

    // Enlazar fechas a cada curso para mostrar rango en la tabla si tenemos fechas
    const fechasByCurso = fechasListNorm.reduce((acc, f) => {
      const id = f.CUR_ID
      if (!acc[id]) acc[id] = []
      acc[id].push(f)
      return acc
    }, {})

    cursosList.value = cursosArray.map(c => ({
      ...c,
      fechas: fechasByCurso[c.CUR_ID] ? fechasByCurso[c.CUR_ID].sort((a,b) => new Date(a.CUF_FECHA_INICIO) - new Date(b.CUF_FECHA_INICIO)) : []
    }))

    // Asignar catálogos (normalizar resultados si vienen paginados)
    personasList.value = (Array.isArray(personasApi) ? personasApi : (personasApi?.results || [])).map(toUpperKeys)
    tiposCursoList.value = (Array.isArray(tiposApi) ? tiposApi : (tiposApi?.results || [])).map(toUpperKeys)
    ramaslist.value = (Array.isArray(ramasApi) ? ramasApi : (ramasApi?.results || [])).map(toUpperKeys)
    fechasCursoList.value = fechasListNorm
    seccionesList.value = seccionesListNorm
    comunasList.value = (Array.isArray(comunasApi) ? comunasApi : (comunasApi?.results || [])).map(toUpperKeys)
    cargosList.value = (Array.isArray(cargosApi) ? cargosApi : (cargosApi?.results || [])).map(toUpperKeys)
    rolesList.value = (Array.isArray(rolesApi) ? rolesApi : (rolesApi?.results || [])).map(toUpperKeys)
    alimentacionCatalogo.value = (Array.isArray(alimentacionCat) ? alimentacionCat : (alimentacionCat?.results || [])).map(toUpperKeys)

    // Filtrado cliente como fallback; cuando uses búsqueda remota, pasar `search` hará que el servidor filtre
    aplicarFiltros()
  } catch (e) {
    if (e.name === 'AbortError') {
      console.info('Carga de datos abortada')
    } else {
      console.error('Error cargando datos desde API:', e)
      cursosList.value = []
      cursosFiltrados.value = []
    }
  } finally {
    isLoading.value = false
    isLoadingData.value = false
  }
}

onMounted(() => {
  // No cargar cursos sin filtros: el usuario debe aplicar al menos un filtro
  // cargarDatos() se invocará cuando el usuario presione Buscar y haya filtros
  // Cargar catálogos para filtros sin cargar cursos
  preloadCatalogosMin()
  // Reintento diferido: si no había token al montar (login recién hecho en otra vista), esperar y reintentar
  const tokenEarly = localStorage.getItem('accessToken') || localStorage.getItem('token')
  if (!tokenEarly) {
    setTimeout(() => {
      const tokenLate = localStorage.getItem('accessToken') || localStorage.getItem('token')
      if (tokenLate && cursosList.value.length === 0) {
        console.info('[CRUDcursos] Token apareció luego del montaje. Reintentando carga de datos...')
        cargarDatos()
      }
    }, 800)
  }
})

async function cargarCatalogos() {
  try {
    const [personasApi, tiposApi, ramasApi] = await Promise.all([
      personasService.personas.list(),
      mantenedores.tipoCursos.list(),
      mantenedores.rama.list(),
    ])
    personasList.value = (Array.isArray(personasApi) ? personasApi : (personasApi?.results || [])).map(toUpperKeys)
    tiposCursoList.value = (Array.isArray(tiposApi) ? tiposApi : (tiposApi?.results || [])).map(toUpperKeys)
    ramaslist.value = (Array.isArray(ramasApi) ? ramasApi : (ramasApi?.results || [])).map(toUpperKeys)
  } catch (e) {
    console.error('Error cargando catálogos iniciales:', e)
  }
}

// Preload minimal catalogs from fast endpoints and cache to localStorage
async function preloadCatalogosMin() {
  try {
    const ttlMs = 15 * 60 * 1000
    const now = Date.now()
    const personasCache = JSON.parse(localStorage.getItem('personas_min_cache') || 'null')
    const tiposCache = JSON.parse(localStorage.getItem('tipos_curso_min_cache') || 'null')

    if (personasCache && (now - personasCache.timestamp) < ttlMs) {
      personasList.value = personasCache.data.map(toUpperKeys)
    }
    if (tiposCache && (now - tiposCache.timestamp) < ttlMs) {
      tiposCursoList.value = tiposCache.data.map(toUpperKeys)
    }

    // If not present or empty, do a quick blocking fetch so filters are usable immediately
    if (!personasList.value.length || !tiposCursoList.value.length) {
      const [pMin, tMin] = await Promise.all([
        request('/personas/min?limit=200'),
        request('/mantenedores/tipo-curso/min?limit=200')
      ])
      const pData = (Array.isArray(pMin?.results) ? pMin.results : (pMin || [])).map(r => ({ id: r.id, nombre: r.nombre }))
      const tData = (Array.isArray(tMin?.results) ? tMin.results : (tMin || [])).map(r => ({ id: r.id, nombre: r.nombre }))
      personasList.value = pData.map(toUpperKeys)
      tiposCursoList.value = tData.map(toUpperKeys)
      localStorage.setItem('personas_min_cache', JSON.stringify({ timestamp: Date.now(), data: pData }))
      localStorage.setItem('tipos_curso_min_cache', JSON.stringify({ timestamp: Date.now(), data: tData }))
    } else {
      // Otherwise refresh in background
      Promise.all([
        request('/personas/min?limit=200'),
        request('/mantenedores/tipo-curso/min?limit=200')
      ]).then(([pMin, tMin]) => {
        const pData = (Array.isArray(pMin?.results) ? pMin.results : (pMin || [])).map(r => ({ id: r.id, nombre: r.nombre }))
        const tData = (Array.isArray(tMin?.results) ? tMin.results : (tMin || [])).map(r => ({ id: r.id, nombre: r.nombre }))
        personasList.value = pData.map(toUpperKeys)
        tiposCursoList.value = tData.map(toUpperKeys)
        localStorage.setItem('personas_min_cache', JSON.stringify({ timestamp: Date.now(), data: pData }))
        localStorage.setItem('tipos_curso_min_cache', JSON.stringify({ timestamp: Date.now(), data: tData }))
      }).catch(e => console.warn('No se pudo refrescar catálogos mínimos:', e))
    }
  } catch (e) {
    console.error('Error en preloadCatalogosMin:', e)
  }
}

// Debounced server search: cuando el usuario escribe, evitamos múltiples llamadas
const _debouncedLoad = debounce((q) => cargarDatos({ page: 1, page_size: 20, search: (q || '').trim() }), 450)
watch(() => filtros.value.searchQuery, (v) => {
  // Si se borra la búsqueda, recargar sin filtro de servidor
  if (!v) {
    // No cargar sin filtros
    return
  }
  if (hasAnyFilter.value) _debouncedLoad(v)
})

// Listener de almacenamiento (multi-tab / login en otra pestaña)
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === 'token' || e.key === 'accessToken') {
      const t = localStorage.getItem('accessToken') || localStorage.getItem('token')
      if (t && cursosList.value.length === 0) {
        console.info('[CRUDcursos] Detectado cambio de token vía storage event. Cargando datos...')
        cargarDatos()
      }
    }
  })
}

// --- Filtros controlados por botón ---
function aplicarFiltros() {
  let items = [...cursosList.value]
  const { searchQuery, estado, tipoCurso, responsable } = filtros.value
  if (!hasAnyFilter.value) {
    cursosFiltrados.value = []
    return
  }
  // Si no hay cursos cargados aún, solicitar al servidor con los filtros actuales
  if (!items.length) {
    const search = (searchQuery || '').trim()
    cargarDatos({ page: 1, page_size: 20, search })
    return
  }
  if (searchQuery) {
    const q = String(searchQuery).toLowerCase()
    items = items.filter(c => (c.CUR_DESCRIPCION || '').toLowerCase().includes(q) || (c.CUR_CODIGO || '').toLowerCase().includes(q))
  }
  if (estado !== null && estado !== undefined && estado !== '') items = items.filter(c => Number(c.CUR_ESTADO) === Number(estado))
  if (tipoCurso !== null && tipoCurso !== undefined && tipoCurso !== '') items = items.filter(c => Number(c.TCU_ID) === Number(tipoCurso))
  if (responsable !== null && responsable !== undefined && responsable !== '') items = items.filter(c => Number(c.PER_ID_RESPONSABLE) === Number(responsable))
  
  // Ordenar por ESTADO (ascendente 0-3) y luego por DESCRIPCIÓN (ascendente)
  items.sort((a, b) => {
    const estadoA = Number(a.CUR_ESTADO) || 0
    const estadoB = Number(b.CUR_ESTADO) || 0
    if (estadoA !== estadoB) return estadoA - estadoB
    const descA = (a.CUR_DESCRIPCION || '').toLowerCase()
    const descB = (b.CUR_DESCRIPCION || '').toLowerCase()
    return descA.localeCompare(descB)
  })
  
  cursosFiltrados.value = items
}

function limpiarFiltros() {
  filtros.value = { searchQuery: '', estado: null, tipoCurso: null, responsable: null }
  aplicarFiltros()
}

const ramasOptions = computed(() => ramaslist.value.map(r => ({ value: r.RAM_ID, text: r.RAM_DESCRIPCION })))

function getRamaName(id) {
  const rama = ramaslist.value.find(r => r.RAM_ID === id)
  return rama ? rama.RAM_DESCRIPCION : 'No definida'
}

// Lazy load helpers for select catalogs
async function ensureCatalogo(kind) {
  try {
    if (kind === 'personas' && (!personasList.value || personasList.value.length === 0)) {
      const personasApi = await personasService.personas.list({ page: 1, page_size: 50 })
      personasList.value = (Array.isArray(personasApi) ? personasApi : (personasApi?.results || [])).map(toUpperKeys)
    } else if (kind === 'tipos' && (!tiposCursoList.value || tiposCursoList.value.length === 0)) {
      const tiposApi = await mantenedores.tipoCursos.list({ page: 1, page_size: 50 })
      tiposCursoList.value = (Array.isArray(tiposApi) ? tiposApi : (tiposApi?.results || [])).map(toUpperKeys)
    }
  } catch (e) {
    console.error('Error cargando catálogo', kind, e)
  }
}


// --- Lógica del Modal (Crear/Editar) ---
async function abrirModalCrear() {
  form.value = inicializarFormulario()
  isTrulyNew.value = true
  esEdicion.value = true // Activar modo "edición" para mostrar las sub-secciones
  fechasCurso.value = []
  seccionesCurso.value = []
  formadoresCurso.value = []
  alimentacionesCurso.value = []
  cuotasCurso.value = []
  coordinadoresCurso.value = []
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
  nuevaSeccion.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
  nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
  nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
  nuevaCuota.value = { CUC_NUMERO: '', CUC_MONTO: '', CUC_FECHA_VENCIMIENTO: '' }
  nuevoCoordinador.value = { PER_ID: null, CAR_ID: null }
  // Si aún no se han cargado catálogos (persona, tipos, comunas, cargos, ramas) forzar carga rápida
  if (
    personasList.value.length === 0 ||
    tiposCursoList.value.length === 0 ||
    comunasList.value?.length === 0 ||
    cargosList.value?.length === 0 ||
    ramaslist.value.length === 0
  ) {
    try { await cargarDatos() } catch (e) { console.warn('No se pudieron refrescar catálogos antes de crear:', e) }
  }
  mostrarModal.value = true
}

async function abrirModalEditar(curso) {
  isTrulyNew.value = false
  esEdicion.value = true
  form.value = {
    ...curso,
    CUR_FECHA_SOLICITUD: curso.CUR_FECHA_SOLICITUD ? curso.CUR_FECHA_SOLICITUD.split('T')[0] : '',
  }
  originalCursoBackup.value = JSON.parse(JSON.stringify(form.value))
  await cargarFechasDelCurso(curso.CUR_ID)
  await cargarSeccionesDelCurso(curso.CUR_ID)
  // Cargar equipo, alimentación, cuotas y coordinadores del curso
  try {
    const [forms, alims, cuots, coords] = await Promise.all([
      formadoresApi.list({ CUR_ID: curso.CUR_ID }).catch(() => []),
      alimentacionesApi.list({ CUR_ID: curso.CUR_ID }).catch(() => []),
      cuotasApi.list({ CUR_ID: curso.CUR_ID }).catch(() => []),
      coordinadoresApi.list({ CUR_ID: curso.CUR_ID }).catch(() => []),
    ])
    formadoresCurso.value = (Array.isArray(forms?.results) ? forms.results : (forms || [])).map(toUpperKeys)
    alimentacionesCurso.value = (Array.isArray(alims?.results) ? alims.results : (alims || [])).map(toUpperKeys)
    cuotasCurso.value = (Array.isArray(cuots?.results) ? cuots.results : (cuots || [])).map(toUpperKeys)
    coordinadoresCurso.value = (Array.isArray(coords?.results) ? coords.results : (coords || [])).map(toUpperKeys)
  } catch (e) { console.warn('No se pudo cargar datos relacionados:', e) }
  originalBuffersBackup.value = {
    fechas: JSON.parse(JSON.stringify(fechasCurso.value)),
    secciones: JSON.parse(JSON.stringify(seccionesCurso.value)),
    formadores: JSON.parse(JSON.stringify(formadoresCurso.value)),
    alimentaciones: JSON.parse(JSON.stringify(alimentacionesCurso.value)),
    cuotas: JSON.parse(JSON.stringify(cuotasCurso.value)),
    coordinadores: JSON.parse(JSON.stringify(coordinadoresCurso.value)),
  }
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
  nuevaSeccion.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
  nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
  nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
  nuevaCuota.value = { CUU_TIPO: 1, CUU_FECHA: '', CUU_VALOR: '' }
  nuevoCoordinador.value = { PER_ID: null, CAR_ID: null }
  mostrarModal.value = true
}

function cerrarModal() {
  mostrarModal.value = false
}

// --- Lógica de Fechas del Curso ---
const nuevoPeriodo = ref({
  CUF_FECHA_INICIO: '',
  CUF_FECHA_TERMINO: '',
  CUF_TIPO: 1,
})

// --- Lógica de Fechas del Curso ---
async function cargarFechasDelCurso(cursoId) {
  if (!cursoId) {
    fechasCurso.value = []
    return
  }
  try {
    // Solo cargar si aún no tenemos fechas en caché
    // Cargar directamente solo las fechas del curso para evitar traer todas
    const res = await fechasApi.list({ CUR_ID: cursoId, page_size: 20 })
    const raw = Array.isArray(res?.results) ? res.results : (Array.isArray(res) ? res : [])
    fechasCursoList.value = raw.map(toUpperKeys)
    fechasCurso.value = (fechasCursoList.value || []).filter(f => Number(f.CUR_ID) === Number(cursoId))
  } catch (e) {
    console.error('Error cargando fechas:', e)
    fechasCurso.value = []
  }
}

async function agregarFecha() {
  if (isAddingPeriodo.value) return
  if (!nuevoPeriodo.value.CUF_FECHA_INICIO || !nuevoPeriodo.value.CUF_FECHA_TERMINO) {
    alert('Debe seleccionar fecha de inicio y término.')
    return
  }
  // Validación simple de rango
  if (new Date(nuevoPeriodo.value.CUF_FECHA_TERMINO) < new Date(nuevoPeriodo.value.CUF_FECHA_INICIO)) {
    alert('La fecha de término no puede ser anterior al inicio.')
    return
  }
  try {
    isAddingPeriodo.value = true
    if (!form.value.CUR_ID) {
      // buffer temporal hasta guardar curso
      fechasCurso.value.push({ ...nuevoPeriodo.value, __tmpId: Date.now() })
    } else {
      const creadaRaw = await fechasApi.create(toLowerKeys({ ...nuevoPeriodo.value, CUR_ID: form.value.CUR_ID }))
      const creada = toUpperKeys(creadaRaw)
      fechasCurso.value.push(creada)
      fechasCursoList.value.push(creada) // Actualizar caché
    }
    nuevoPeriodo.value.CUF_FECHA_INICIO = ''
    nuevoPeriodo.value.CUF_FECHA_TERMINO = ''
    alert('Período agregado exitosamente.')
  } finally { isAddingPeriodo.value = false }
}

function iniciarEdicionFecha(fecha) {
  editandoFecha.value = fecha.CUF_ID || `tmp-${fecha.__tmpId}`
  nuevoPeriodo.value = { ...fecha }
}

async function guardarEdicionFecha() {
  if (!nuevoPeriodo.value.CUF_FECHA_INICIO || !nuevoPeriodo.value.CUF_FECHA_TERMINO) {
    alert('Debe completar fecha de inicio y término.')
    return
  }
  if (new Date(nuevoPeriodo.value.CUF_FECHA_TERMINO) < new Date(nuevoPeriodo.value.CUF_FECHA_INICIO)) {
    alert('La fecha de término no puede ser anterior al inicio.')
    return
  }
  try {
    if (typeof editandoFecha.value === 'string' && editandoFecha.value.startsWith('tmp-')) {
      // Actualizar en buffer temporal
      const idx = fechasCurso.value.findIndex(f => `tmp-${f.__tmpId}` === editandoFecha.value)
      if (idx !== -1) fechasCurso.value[idx] = { ...nuevoPeriodo.value }
    } else {
      // Actualizar en API
      await fechasApi.update(editandoFecha.value, toLowerKeys(nuevoPeriodo.value))
      const idx = fechasCurso.value.findIndex(f => f.CUF_ID === editandoFecha.value)
      if (idx !== -1) fechasCurso.value[idx] = { ...nuevoPeriodo.value, CUF_ID: editandoFecha.value }
      // Actualizar caché
      const cacheIdx = fechasCursoList.value.findIndex(f => f.CUF_ID === editandoFecha.value)
      if (cacheIdx !== -1) fechasCursoList.value[cacheIdx] = { ...nuevoPeriodo.value, CUF_ID: editandoFecha.value }
    }
    cancelarEdicionFecha()
    alert('Período actualizado exitosamente.')
  } catch (e) {
    console.error('Error actualizando período:', e)
    alert('Error al actualizar el período.')
  }
}

function cancelarEdicionFecha() {
  editandoFecha.value = null
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: 1 }
}

async function eliminarFecha(fechaId) {
  // Si es temporal (__tmpId), remover directo
  if (!fechaId && fechaId !== 0) return
  if (typeof fechaId === 'string' && fechaId.startsWith('tmp-')) {
    fechasCurso.value = fechasCurso.value.filter(f => `tmp-${f.__tmpId}` !== fechaId)
    return
  }
  if (!window.confirm('¿Seguro que desea eliminar este período?')) return
  if (isDeletingPeriodo.value) return
  try {
    isDeletingPeriodo.value = true
    await fechasApi.remove(fechaId)
    fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)
    fechasCursoList.value = fechasCursoList.value.filter(f => f.CUF_ID !== fechaId) // Actualizar caché
    alert('Período eliminado exitosamente.')
  } catch (e) {
    // Manejar 404 silencioso si ya no existe
    if (/404/.test(String(e?.message))) {
      fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)
      fechasCursoList.value = fechasCursoList.value.filter(f => f.CUF_ID !== fechaId)
    } else { throw e }
  } finally { isDeletingPeriodo.value = false }
}

// --- Lógica de Secciones del Curso ---
const nuevaSeccion = ref({
  CUS_SECCION: '',
  RAM_ID: null,
  CUS_CANT_PARTICIPANTE: '',
})

async function cargarSeccionesDelCurso(cursoId) {
  try {
    // Cargar directamente solo las secciones del curso para evitar traer todas
    const all = await seccionesApi.list({ CUR_ID: cursoId, page_size: 500 })
    const raw = Array.isArray(all?.results) ? all.results : (Array.isArray(all) ? all : [])
    seccionesList.value = raw.map(toUpperKeys)
    seccionesCurso.value = (seccionesList.value || []).filter(s => Number(s.CUR_ID) === Number(cursoId))
  } catch (e) {
    console.error('Error cargando secciones:', e)
    seccionesCurso.value = []
  }
}

async function agregarSeccion() {
  if (!nuevaSeccion.value.CUS_SECCION || !nuevaSeccion.value.RAM_ID || !nuevaSeccion.value.CUS_CANT_PARTICIPANTE) {
    alert('Debe llenar todos los campos de la sección.')
    return
  }
  if (isAddingSeccion.value) return
  const payload = {
    CUR_ID: form.value.CUR_ID,
    CUS_SECCION: Number(nuevaSeccion.value.CUS_SECCION),
    RAM_ID: Number(nuevaSeccion.value.RAM_ID),
    CUS_CANT_PARTICIPANTE: Number(nuevaSeccion.value.CUS_CANT_PARTICIPANTE)
  }
  try {
    isAddingSeccion.value = true
    if (!form.value.CUR_ID) {
      seccionesCurso.value.push({ ...payload, __tmpId: Date.now() })
    } else {
      const creadaRaw = await seccionesApi.create(toLowerKeys(payload))
      const creada = toUpperKeys(creadaRaw)
      seccionesCurso.value.push(creada)
      seccionesList.value.push(creada)
    }
    nuevaSeccion.value.CUS_SECCION = ''
    nuevaSeccion.value.RAM_ID = null
    nuevaSeccion.value.CUS_CANT_PARTICIPANTE = ''
    alert('Sección agregada exitosamente.')
  } finally { isAddingSeccion.value = false }
}

function iniciarEdicionSeccion(seccion) {
  editandoSeccion.value = seccion.CUS_ID || `tmp-${seccion.__tmpId}`
  nuevaSeccion.value = { ...seccion }
}

async function guardarEdicionSeccion() {
  if (!nuevaSeccion.value.CUS_SECCION || !nuevaSeccion.value.RAM_ID || !nuevaSeccion.value.CUS_CANT_PARTICIPANTE) {
    alert('Debe completar todos los campos.')
    return
  }
  try {
    if (typeof editandoSeccion.value === 'string' && editandoSeccion.value.startsWith('tmp-')) {
      const idx = seccionesCurso.value.findIndex(s => `tmp-${s.__tmpId}` === editandoSeccion.value)
      if (idx !== -1) seccionesCurso.value[idx] = { ...nuevaSeccion.value }
    } else {
      await seccionesApi.update(editandoSeccion.value, toLowerKeys(nuevaSeccion.value))
      const idx = seccionesCurso.value.findIndex(s => s.CUS_ID === editandoSeccion.value)
      if (idx !== -1) seccionesCurso.value[idx] = { ...nuevaSeccion.value, CUS_ID: editandoSeccion.value }
      const cacheIdx = seccionesList.value.findIndex(s => s.CUS_ID === editandoSeccion.value)
      if (cacheIdx !== -1) seccionesList.value[cacheIdx] = { ...nuevaSeccion.value, CUS_ID: editandoSeccion.value }
    }
    cancelarEdicionSeccion()
    alert('Sección actualizada exitosamente.')
  } catch (e) {
    console.error('Error actualizando sección:', e)
    alert('Error al actualizar la sección.')
  }
}

function cancelarEdicionSeccion() {
  editandoSeccion.value = null
  nuevaSeccion.value = { CUS_SECCION: '', RAM_ID: null, CUS_CANT_PARTICIPANTE: '' }
}

async function eliminarSeccion(seccionId) {
  // Si es temporal
  if (typeof seccionId === 'string' && seccionId.startsWith('tmp-')) {
    seccionesCurso.value = seccionesCurso.value.filter(s => `tmp-${s.__tmpId}` !== seccionId)
    return
  }
  if (!window.confirm('¿Seguro que desea eliminar esta sección?')) return
  if (isDeletingSeccion.value) return
  try {
    isDeletingSeccion.value = true
    await seccionesApi.remove(seccionId)
    seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
    seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
    
    alert('Sección eliminada exitosamente.')
  } catch (e) {
    if (/404/.test(String(e?.message))) {
      seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
      seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
    } else { throw e }
  } finally { isDeletingSeccion.value = false }
}

// --- Lógica de Guardado Principal ---
async function guardarCurso() {
  // Prevenir múltiples clics
  if (isSaving.value) return
  isSaving.value = true

  try {
    // Validar campos obligatorios
    if (!form.value.CUR_DESCRIPCION?.trim()) {
      alert('La descripción del curso es obligatoria.')
      return
    }
    if (!form.value.CUR_CODIGO?.trim()) {
      alert('El código del curso es obligatorio.')
      return
    }
    if (!form.value.TCU_ID) {
      alert('Debes seleccionar un tipo de curso.')
      return
    }
    if (!form.value.PER_ID_RESPONSABLE) {
      alert('Debes seleccionar un responsable.')
      return
    }

    const payload = { ...form.value }
    // Sanitizar payload: eliminar campos calculados / solo lectura
    delete payload.fechas
    delete payload.secciones
    delete payload.CUR_FECHA_HORA
    payload.CUR_COTA_CON_ALMUERZO = Number(payload.CUR_COTA_CON_ALMUERZO)
    payload.CUR_COTA_SIN_ALMUERZO = Number(payload.CUR_COTA_SIN_ALMUERZO)
    // Convertir FKs y enums a números por seguridad
    payload.TCU_ID = Number(payload.TCU_ID)
    payload.PER_ID_RESPONSABLE = Number(payload.PER_ID_RESPONSABLE)
    payload.CAR_ID_RESPONSABLE = payload.CAR_ID_RESPONSABLE ? Number(payload.CAR_ID_RESPONSABLE) : null
    payload.COM_ID_LUGAR = payload.COM_ID_LUGAR ? Number(payload.COM_ID_LUGAR) : null
    payload.CUR_MODALIDAD = Number(payload.CUR_MODALIDAD || 1)
    payload.CUR_TIPO_CURSO = Number(payload.CUR_TIPO_CURSO || 1)
    payload.CUR_ADMINISTRA = Number(payload.CUR_ADMINISTRA || 1)
    // Estado automático: si estaba Anulado (2), mantener; si no, calcular según períodos
    const originalEstado = originalCursoBackup.value?.CUR_ESTADO
    if (Number(originalEstado) === 2) {
      payload.CUR_ESTADO = 2
    } else {
      payload.CUR_ESTADO = computeAutoEstadoFromFechas(fechasCurso.value)
    }

    // Prepare payload for API (lowercase)
    const apiPayload = toLowerKeys(payload)

    if (isTrulyNew.value) {
      // Obtener usuario actual para USU_ID
      try {
        const perfil = await request('auth/perfil')
        if (perfil?.usuario?.user_id) {
          apiPayload.usu_id = perfil.usuario.user_id
        } else {
          apiPayload.usu_id = 1 // Fallback
        }
      } catch (e) {
        console.warn('No se pudo obtener USU_ID, usando default:', e)
        apiPayload.usu_id = 1 // Default fallback
      }

      const creadoRaw = await cursosApi.create(apiPayload)
      const creado = toUpperKeys(creadoRaw)
      cursosList.value.unshift(creado)
      // Persistir buffers (fechas, secciones, formadores, alimentación)
      // Fechas
      for (const f of (fechasCurso.value || [])) {
        if (!f.CUF_ID) {
          try {
            const createdFRaw = await fechasApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              CUF_FECHA_INICIO: f.CUF_FECHA_INICIO,
              CUF_FECHA_TERMINO: f.CUF_FECHA_TERMINO,
              CUF_TIPO: f.CUF_TIPO,
            }))
            const createdF = toUpperKeys(createdFRaw)
            Object.assign(f, createdF)
            fechasCursoList.value.push(createdF)
          } catch (e) { console.warn('No se pudo crear período post-curso:', e) }
        }
      }
      // Secciones
      for (const s of (seccionesCurso.value || [])) {
        if (!s.CUS_ID) {
          try {
            const createdSRaw = await seccionesApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              CUS_SECCION: s.CUS_SECCION,
              RAM_ID: s.RAM_ID,
              CUS_CANT_PARTICIPANTE: s.CUS_CANT_PARTICIPANTE,
            }))
            const createdS = toUpperKeys(createdSRaw)
            Object.assign(s, createdS)
            seccionesList.value.push(createdS)
          } catch (e) { console.warn('No se pudo crear sección post-curso:', e) }
        }
      }
      // Formadores
      for (const fm of (formadoresCurso.value || [])) {
        if (!fm.CUF_ID) {
          try {
            // Remap seccion temporal si corresponde
            let resolvedCusId = null
            if (typeof fm.CUS_ID === 'number') {
              resolvedCusId = fm.CUS_ID
            } else if (typeof fm.CUS_ID === 'string' && fm.CUS_ID.startsWith('tmp-')) {
              const tmpNumeric = Number(fm.CUS_ID.replace('tmp-', ''))
              const matched = seccionesCurso.value.find(s => s.__tmpId === tmpNumeric)
              if (matched && matched.CUS_ID) resolvedCusId = matched.CUS_ID
            }
            const createdFmRaw = await formadoresApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              PER_ID: fm.PER_ID,
              ROL_ID: fm.ROL_ID,
              CUS_ID: resolvedCusId,
              CUO_DIRECTOR: !!fm.CUO_DIRECTOR,
            }))
            const createdFm = toUpperKeys(createdFmRaw)
            Object.assign(fm, createdFm)
          } catch (e) { console.warn('No se pudo crear formador post-curso:', e) }
        }
      }
      // Alimentaciones
      for (const al of (alimentacionesCurso.value || [])) {
        if (!al.CUA_ID) {
          try {
            const createdAlRaw = await alimentacionesApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              ALI_ID: al.ALI_ID,
              CUA_FECHA: al.CUA_FECHA,
              CUA_TIEMPO: al.CUA_TIEMPO,
              CUA_DESCRIPCION: al.CUA_DESCRIPCION,
              CUA_CANTIDAD_ADICIONAL: Number(al.CUA_CANTIDAD_ADICIONAL || 0),
            }))
            const createdAl = toUpperKeys(createdAlRaw)
            Object.assign(al, createdAl)
          } catch (e) { console.warn('No se pudo crear alimentación post-curso:', e) }
        }
      }
      // Cuotas
      for (const cuota of (cuotasCurso.value || [])) {
        if (!cuota.CUU_ID) {
          try {
            const createdCuotaRaw = await cuotasApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              CUU_TIPO: Number(cuota.CUU_TIPO),
              CUU_FECHA: cuota.CUU_FECHA,
              CUU_VALOR: Number(cuota.CUU_VALOR),
            }))
            const createdCuota = toUpperKeys(createdCuotaRaw)
            Object.assign(cuota, createdCuota)
          } catch (e) { console.warn('No se pudo crear cuota post-curso:', e) }
        }
      }
      // Coordinadores
      for (const coord of (coordinadoresCurso.value || [])) {
        if (!coord.CUC_ID) {
          try {
            const createdCoordRaw = await coordinadoresApi.create(toLowerKeys({
              CUR_ID: creado.CUR_ID,
              PER_ID: coord.PER_ID,
              CAR_ID: coord.CAR_ID,
            }))
            const createdCoord = toUpperKeys(createdCoordRaw)
            Object.assign(coord, createdCoord)
          } catch (e) { console.warn('No se pudo crear coordinador post-curso:', e) }
        }
      }
      await cargarFechasDelCurso(creado.CUR_ID)
      await cargarSeccionesDelCurso(creado.CUR_ID)
      isTrulyNew.value = false
      alert('Curso creado exitosamente.')
    } else {
      // En edición: prevenir update si no hay cambios relevantes
      const camposClave = ['CUR_DESCRIPCION','CUR_CODIGO','TCU_ID','PER_ID_RESPONSABLE','CUR_FECHA_SOLICITUD','CUR_COTA_CON_ALMUERZO','CUR_COTA_SIN_ALMUERZO','CUR_MODALIDAD','CUR_TIPO_CURSO','CUR_LUGAR','CUR_COORD_LATITUD','CUR_COORD_LONGITUD','CUR_ESTADO','CUR_OBSERVACION','CUR_ADMINISTRA','COM_ID_LUGAR','CAR_ID_RESPONSABLE']
      const huboCambios = camposClave.some(k => String(originalCursoBackup.value?.[k] ?? '') !== String(payload[k] ?? ''))
      if (!huboCambios) {
        alert('No hay cambios para guardar.')
        return
      }
      // Usar PATCH para edición parcial y evitar requerir todos los campos
      const actualizadoRaw = await cursosApi.partialUpdate(payload.CUR_ID, apiPayload)
      const actualizado = toUpperKeys(actualizadoRaw)
      const index = cursosList.value.findIndex(c => c.CUR_ID === payload.CUR_ID)
      if (index !== -1) {
        // preservar fechas y secciones ya cargadas en memoria si existen
        const fechasLocal = cursosList.value[index].fechas
        const seccionesLocal = cursosList.value[index].secciones
        cursosList.value[index] = { ...actualizado, fechas: fechasLocal || [], secciones: seccionesLocal || [] }
      }
      originalCursoBackup.value = JSON.parse(JSON.stringify(form.value))
      originalBuffersBackup.value = {
        fechas: JSON.parse(JSON.stringify(fechasCurso.value)),
        secciones: JSON.parse(JSON.stringify(seccionesCurso.value)),
        formadores: JSON.parse(JSON.stringify(formadoresCurso.value)),
        alimentaciones: JSON.parse(JSON.stringify(alimentacionesCurso.value)),
        cuotas: JSON.parse(JSON.stringify(cuotasCurso.value)),
        coordinadores: JSON.parse(JSON.stringify(coordinadoresCurso.value)),
      }
      alert('Curso actualizado exitosamente.')
    }
    aplicarFiltros()
    cerrarModal()
  } catch (e) {
    console.error('Error al guardar el curso:', e)
    console.error('Response:', e.response?.data)
    alert(`Error al guardar: ${e.response?.data?.detail || e.message || 'Error desconocido'}`)
  } finally {
    isSaving.value = false
  }
}

// --- Estado automático basado en fechas ---
function computeAutoEstadoFromFechas(fechas) {
  try {
    const list = Array.isArray(fechas) ? fechas : []
    if (!list.length) return 0 // Pendiente
    const starts = list.map(f => new Date(f.CUF_FECHA_INICIO)).filter(d => !isNaN(d))
    const ends = list.map(f => new Date(f.CUF_FECHA_TERMINO || f.CUF_FECHA_INICIO)).filter(d => !isNaN(d))
    if (!starts.length || !ends.length) return 0
    const minStart = new Date(Math.min(...starts))
    const maxEnd = new Date(Math.max(...ends))
    const today = new Date()
    const t = new Date(today.getFullYear(), today.getMonth(), today.getDate())
    const ms = new Date(minStart.getFullYear(), minStart.getMonth(), minStart.getDate())
    const me = new Date(maxEnd.getFullYear(), maxEnd.getMonth(), maxEnd.getDate())
    if (t < ms) return 0 // Pendiente
    if (t > me) return 3 // Finalizado
    return 1 // Vigente
  } catch {
    return 0
  }
}

// --- Cambio de Estado ---
function abrirModalCambioEstadoCurso(curso) {
  cursoParaCambioEstado.value = curso
  nuevoEstado.value = curso.CUR_ESTADO
  mostrarModalCambioEstado.value = true
}

function cerrarModalCambioEstado() {
  mostrarModalCambioEstado.value = false
  cursoParaCambioEstado.value = null
  nuevoEstado.value = null
}

async function guardarCambioEstado() {
  if (nuevoEstado.value === null || nuevoEstado.value === undefined) {
    alert('Debe seleccionar un estado')
    return
  }
  
  const selectedValue = typeof nuevoEstado.value === 'object' && nuevoEstado.value !== null
    ? (nuevoEstado.value.value ?? nuevoEstado.value.VALOR ?? nuevoEstado.value)
    : (nuevoEstado.value ?? nuevoEstado)
  const estadoNumber = Number(selectedValue)
  const estadoTexto = opcionesEstado.find(e => e.value === estadoNumber)?.text || 'Desconocido'
  if (!window.confirm(`¿Confirma cambiar el estado a "${estadoTexto}"?`)) return
  
  if (isDisabling.value) return
  isDisabling.value = true
  
  try {
    const actualizadoRaw = await cursosApi.partialUpdate(cursoParaCambioEstado.value.CUR_ID, toLowerKeys({ CUR_ESTADO: estadoNumber }))
    const actualizado = toUpperKeys(actualizadoRaw)
    Object.assign(cursoParaCambioEstado.value, actualizado)
    aplicarFiltros()
    alert('Estado actualizado exitosamente.')
    cerrarModalCambioEstado()
  } catch (e) {
    console.error('Error al cambiar estado:', e)
    console.error('Response:', e.response?.data)
    alert(`Error al cambiar estado: ${e.response?.data?.detail || e.message || 'Error desconocido'}`)
  } finally {
    isDisabling.value = false
  }
}

// --- Funciones de Formato y Ayuda ---
const personasOptions = computed(() => personasList.value.map(p => ({ value: p.PER_ID || p.id, text: (p.PER_NOMBRES || p.PER_NOMBRE || p.nombre || '').trim() })))

const tiposCursoOptions = computed(() => 
  tiposCursoList.value.map(tc => ({ value: tc.TCU_ID || tc.id, text: tc.TCU_DESCRIPCION || tc.nombre }))
)

const comunasList = ref([])
const cargosList = ref([])
const comunasOptions = computed(() => comunasList.value.map(c => ({ value: c.COM_ID, text: c.COM_DESCRIPCION })))

// Ubicar mapa según comuna seleccionada (coordenadas importadas de todas las comunas de Chile)
const comunaCoords = comunasCoords

watch(() => form.value.COM_ID_LUGAR, (newComunaId) => {
  if (!newComunaId) return
  const comunaObj = comunasList.value.find(c => Number(c.COM_ID) === Number(newComunaId))
  if (!comunaObj) {
    console.warn('[CRUDcursos] Comuna no encontrada con ID:', newComunaId)
    return
  }
  const nombre = comunaObj.COM_DESCRIPCION
  console.log('[CRUDcursos] Comuna seleccionada:', nombre)
  const coords = comunaCoords[nombre]
  if (coords) {
    console.log('[CRUDcursos] Actualizando coordenadas a:', coords)
    form.value.CUR_COORD_LATITUD = coords.lat
    form.value.CUR_COORD_LONGITUD = coords.lng
  } else {
    console.warn('[CRUDcursos] No hay coordenadas definidas para:', nombre)
    // Usar coordenadas por defecto de Santiago
    form.value.CUR_COORD_LATITUD = -33.45694
    form.value.CUR_COORD_LONGITUD = -70.64827
  }
})
const cargosOptions = computed(() => cargosList.value.map(c => ({ value: c.CAR_ID, text: c.CAR_DESCRIPCION })))

function formatDates(curso) {
  if (curso.fechas && curso.fechas.length > 0) {
    const primera = curso.fechas[0].CUF_FECHA_INICIO
    const ultima = curso.fechas[curso.fechas.length - 1].CUF_FECHA_TERMINO
    return `${formatDateSimple(primera)} - ${formatDateSimple(ultima)} (${curso.fechas.length} per.)`
  }
  return 'Sin períodos'
}

function formatDateSimple(dateStr) {
  if (!dateStr) return '?'
  const opts = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString('es-CL', opts)
}

function getPersonaName(id) {
  const p = personasList.value.find(x => Number(x.PER_ID ?? x.ID ?? x.id) === Number(id))
  const nombre = p?.PER_NOMBRES || p?.PER_NOMBRE || p?.NOMBRE || p?.nombre || ''
  const apellido = p?.PER_APELPTA || p?.PER_APELLIDO_PATERNO || p?.APELLIDO || p?.apellido || ''
  const full = `${(nombre || '').trim()} ${(apellido || '').trim()}`.trim()
  return p ? (full || nombre || '-') : 'No asignado'
}

function getCargoName(id) {
  const c = cargosList.value.find(x => Number(x.CAR_ID ?? x.ID ?? x.id) === Number(id))
  return c ? (c.CAR_DESCRIPCION || c.DESCRIPCION || c.nombre || c.NOMBRE || '-') : ''
}

function getTipoCursoName(id) {
  const tc = tiposCursoList.value.find(x => Number(x.TCU_ID ?? x.ID ?? x.id) === Number(id))
  return tc ? (tc.TCU_DESCRIPCION || tc.DESCRIPCION || tc.nombre || tc.NOMBRE || 'No definido') : 'No definido'
}

function getEstadoText(e) {
  return opcionesEstado.find(o => o.value === e)?.text || 'Desconocido'
}

function getEstadoClass(e) {
  const map = { 0: 'badge-warning', 1: 'badge-success', 2: 'badge-danger', 3: 'badge-secondary' }
  return map[e] || 'badge-dark'
}

const opcionesAdministra = [
  { value: 1, text: 'Zona' },
  { value: 2, text: 'Distrito' },
]

// ====== Equipo Formadores ======
const rolesOptions = computed(() => rolesList.value.map(r => ({ value: r.ROL_ID, text: r.ROL_DESCRIPCION })))
const seccionesOptions = computed(() => seccionesCurso.value.map(s => {
  const rama = ramaslist.value.find(r => r.RAM_ID === s.RAM_ID)
  const ramaText = rama ? rama.RAM_DESCRIPCION : ''
  return { value: s.CUS_ID || `tmp-${s.__tmpId}`, text: `SECCION N° ${s.CUS_SECCION} (${ramaText})` }
}))
async function agregarFormador() {
  if (isAddingFormador.value) return
  const f = nuevaFormador.value
  if (!f.PER_ID || !f.ROL_ID) { alert('Completa persona y rol.'); return }
  try {
    isAddingFormador.value = true
    if (!form.value.CUR_ID) {
      formadoresCurso.value.push({ ...f, __tmpId: Date.now() })
    } else {
      const creadoRaw = await formadoresApi.create(toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        PER_ID: f.PER_ID,
        ROL_ID: f.ROL_ID,
        CUS_ID: typeof f.CUS_ID === 'number' ? f.CUS_ID : null,
        CUO_DIRECTOR: !!f.CUO_DIRECTOR,
      }))
      const creado = toUpperKeys(creadoRaw)
      formadoresCurso.value.push(creado)
    }
    nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
  } finally { isAddingFormador.value = false }
}

function iniciarEdicionFormador(formador) {
  editandoFormador.value = formador.CUF_ID || `tmp-${formador.__tmpId}`
  nuevaFormador.value = { ...formador }
}

async function guardarEdicionFormador() {
  const f = nuevaFormador.value
  if (!f.PER_ID || !f.ROL_ID) {
    alert('Completa persona y rol.')
    return
  }
  try {
    if (typeof editandoFormador.value === 'string' && editandoFormador.value.startsWith('tmp-')) {
      const idx = formadoresCurso.value.findIndex(x => `tmp-${x.__tmpId}` === editandoFormador.value)
      if (idx !== -1) formadoresCurso.value[idx] = { ...f }
    } else {
      await formadoresApi.update(editandoFormador.value, toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        PER_ID: f.PER_ID,
        ROL_ID: f.ROL_ID,
        CUS_ID: typeof f.CUS_ID === 'number' ? f.CUS_ID : null,
        CUO_DIRECTOR: !!f.CUO_DIRECTOR,
      }))
      const idx = formadoresCurso.value.findIndex(x => x.CUF_ID === editandoFormador.value)
      if (idx !== -1) formadoresCurso.value[idx] = { ...f, CUF_ID: editandoFormador.value }
    }
    cancelarEdicionFormador()
    alert('Formador actualizado exitosamente.')
  } catch (e) {
    console.error('Error actualizando formador:', e)
    alert('Error al actualizar el formador.')
  }
}

function cancelarEdicionFormador() {
  editandoFormador.value = null
  nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
}

async function eliminarFormador(item) {
  if (!item) return
  if (!item.CUF_ID) {
    formadoresCurso.value = formadoresCurso.value.filter(x => x !== item)
    return
  }
  if (!confirm('Eliminar formador?')) return
  if (isDeletingFormador.value) return
  try {
    isDeletingFormador.value = true
    await formadoresApi.remove(item.CUF_ID)
    formadoresCurso.value = formadoresCurso.value.filter(x => x.CUF_ID !== item.CUF_ID)
  } catch (e) {
    if (/404/.test(String(e?.message))) {
      formadoresCurso.value = formadoresCurso.value.filter(x => x.CUF_ID !== item.CUF_ID)
    } else { throw e }
  } finally { isDeletingFormador.value = false }
}

// ====== Alimentación ======
const alimentacionOptions = computed(() => alimentacionCatalogo.value.map(a => ({ value: a.ALI_ID, text: a.ALI_DESCRIPCION })))
const tiempoAlimentacionOptions = [
  { value: 1, text: 'Desayuno' },
  { value: 2, text: 'Almuerzo' },
  { value: 3, text: 'Once' },
  { value: 4, text: 'Cena' },
  { value: 5, text: 'Once/Cena' },
]
async function agregarAlimentacion() {
  if (isAddingAlimentacion.value) return
  const a = nuevaAlimentacion.value
  if (!a.ALI_ID || !a.CUA_FECHA || !a.CUA_TIEMPO || !a.CUA_DESCRIPCION) { alert('Completa todos los campos.'); return }
  try {
    isAddingAlimentacion.value = true
    if (!form.value.CUR_ID) {
      alimentacionesCurso.value.push({ ...a, __tmpId: Date.now() })
    } else {
      const creadoRaw = await alimentacionesApi.create(toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        ALI_ID: a.ALI_ID,
        CUA_FECHA: a.CUA_FECHA,
        CUA_TIEMPO: a.CUA_TIEMPO,
        CUA_DESCRIPCION: a.CUA_DESCRIPCION,
        CUA_CANTIDAD_ADICIONAL: Number(a.CUA_CANTIDAD_ADICIONAL || 0),
      }))
      const creado = toUpperKeys(creadoRaw)
      alimentacionesCurso.value.push(creado)
    }
    nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
  } finally { isAddingAlimentacion.value = false }
}

function iniciarEdicionAlimentacion(alimentacion) {
  editandoAlimentacion.value = alimentacion.CUA_ID || `tmp-${alimentacion.__tmpId}`
  nuevaAlimentacion.value = { ...alimentacion }
}

async function guardarEdicionAlimentacion() {
  const a = nuevaAlimentacion.value
  if (!a.ALI_ID || !a.CUA_FECHA || !a.CUA_TIEMPO || !a.CUA_DESCRIPCION) {
    alert('Completa todos los campos.')
    return
  }
  try {
    if (typeof editandoAlimentacion.value === 'string' && editandoAlimentacion.value.startsWith('tmp-')) {
      const idx = alimentacionesCurso.value.findIndex(x => `tmp-${x.__tmpId}` === editandoAlimentacion.value)
      if (idx !== -1) alimentacionesCurso.value[idx] = { ...a }
    } else {
      await alimentacionesApi.update(editandoAlimentacion.value, toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        ALI_ID: a.ALI_ID,
        CUA_FECHA: a.CUA_FECHA,
        CUA_TIEMPO: a.CUA_TIEMPO,
        CUA_DESCRIPCION: a.CUA_DESCRIPCION,
        CUA_CANTIDAD_ADICIONAL: Number(a.CUA_CANTIDAD_ADICIONAL || 0),
      }))
      const idx = alimentacionesCurso.value.findIndex(x => x.CUA_ID === editandoAlimentacion.value)
      if (idx !== -1) alimentacionesCurso.value[idx] = { ...a, CUA_ID: editandoAlimentacion.value }
    }
    cancelarEdicionAlimentacion()
    alert('Alimentación actualizada exitosamente.')
  } catch (e) {
    console.error('Error actualizando alimentación:', e)
    alert('Error al actualizar la alimentación.')
  }
}

function cancelarEdicionAlimentacion() {
  editandoAlimentacion.value = null
  nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
}

async function eliminarAlimentacion(item) {
  if (!item) return
  if (!item.CUA_ID) {
    alimentacionesCurso.value = alimentacionesCurso.value.filter(x => x !== item)
    return
  }
  if (!confirm('Eliminar alimentación?')) return
  if (isDeletingAlimentacion.value) return
  try {
    isDeletingAlimentacion.value = true
    await alimentacionesApi.remove(item.CUA_ID)
    alimentacionesCurso.value = alimentacionesCurso.value.filter(x => x.CUA_ID !== item.CUA_ID)
  } catch (e) {
    if (/404/.test(String(e?.message))) {
      alimentacionesCurso.value = alimentacionesCurso.value.filter(x => x.CUA_ID !== item.CUA_ID)
    } else { throw e }
  } finally { isDeletingAlimentacion.value = false }
}

// ====== Cuotas del Curso ======
async function agregarCuota() {
  if (isAddingCuota.value) return
  const c = nuevaCuota.value
  if (!c.CUU_TIPO || !c.CUU_FECHA || !c.CUU_VALOR) { alert('Completa todos los campos.'); return }
  try {
    isAddingCuota.value = true
    if (!form.value.CUR_ID) {
      cuotasCurso.value.push({ ...c, __tmpId: Date.now() })
    } else {
      const creadoRaw = await cuotasApi.create(toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        CUU_TIPO: Number(c.CUU_TIPO),
        CUU_FECHA: c.CUU_FECHA,
        CUU_VALOR: Number(c.CUU_VALOR),
      }))
      const creado = toUpperKeys(creadoRaw)
      cuotasCurso.value.push(creado)
    }
    nuevaCuota.value = { CUU_TIPO: 1, CUU_FECHA: '', CUU_VALOR: '' }
  } finally { isAddingCuota.value = false }
}
async function eliminarCuota(item) {
  if (!item) return
  if (!item.CUU_ID) {
    cuotasCurso.value = cuotasCurso.value.filter(x => x !== item)
    return
  }
  if (!confirm('¿Eliminar cuota?')) return
  if (isDeletingCuota.value) return
  try {
    isDeletingCuota.value = true
    await cuotasApi.remove(item.CUU_ID)
    cuotasCurso.value = cuotasCurso.value.filter(x => x.CUU_ID !== item.CUU_ID)
  } catch (e) {
    if (/404/.test(String(e?.message))) {
      cuotasCurso.value = cuotasCurso.value.filter(x => x.CUU_ID !== item.CUU_ID)
    } else { throw e }
  } finally { isDeletingCuota.value = false }
}

// ====== Coordinadores del Curso ======
// cargosOptions ya está definido arriba en la sección de edición
async function agregarCoordinador() {
  if (isAddingCoordinador.value) return
  const coord = nuevoCoordinador.value
  if (!coord.PER_ID || !coord.CAR_ID) { alert('Completa persona y cargo.'); return }
  try {
    isAddingCoordinador.value = true
    if (!form.value.CUR_ID) {
      coordinadoresCurso.value.push({ ...coord, __tmpId: Date.now() })
    } else {
      const creadoRaw = await coordinadoresApi.create(toLowerKeys({
        CUR_ID: form.value.CUR_ID,
        PER_ID: coord.PER_ID,
        CAR_ID: coord.CAR_ID,
      }))
      const creado = toUpperKeys(creadoRaw)
      coordinadoresCurso.value.push(creado)
    }
    nuevoCoordinador.value = { PER_ID: null, CAR_ID: null }
  } finally { isAddingCoordinador.value = false }
}
async function eliminarCoordinador(item) {
  if (!item) return
  if (!item.CUC_ID) {
    coordinadoresCurso.value = coordinadoresCurso.value.filter(x => x !== item)
    return
  }
  if (!confirm('¿Eliminar coordinador?')) return
  if (isDeletingCoordinador.value) return
  try {
    isDeletingCoordinador.value = true
    await coordinadoresApi.remove(item.CUC_ID)
    coordinadoresCurso.value = coordinadoresCurso.value.filter(x => x.CUC_ID !== item.CUC_ID)
  } catch (e) {
    if (/404/.test(String(e?.message))) {
      coordinadoresCurso.value = coordinadoresCurso.value.filter(x => x.CUC_ID !== item.CUC_ID)
    } else { throw e }
  } finally { isDeletingCoordinador.value = false }
}

async function abrirModalVer(curso) {
  cursoSeleccionado.value = curso
  mostrarModalVer.value = true // Abrir modal inmediatamente para mostrar al usuario
  
  // Cargar datos en segundo plano
  try {
    await cargarFechasDelCurso(curso.CUR_ID)
    seccionesCurso.value = seccionesList.value.filter(s => Number(s.CUR_ID) === Number(curso.CUR_ID))
    
    // Cargar formadores, alimentación, cuotas y coordinadores en paralelo pero sin bloquear UI
    const [forms, alims, cuots, coords] = await Promise.all([
      formadoresApi.list({ CUR_ID: curso.CUR_ID, page_size: 500 }).catch(() => []),
      alimentacionesApi.list({ CUR_ID: curso.CUR_ID, page_size: 500 }).catch(() => []),
      cuotasApi.list({ CUR_ID: curso.CUR_ID, page_size: 500 }).catch(() => []),
      coordinadoresApi.list({ CUR_ID: curso.CUR_ID, page_size: 500 }).catch(() => []),
    ])
    
    formadoresCurso.value = (Array.isArray(forms?.results) ? forms.results : (forms || [])).map(toUpperKeys)
    alimentacionesCurso.value = (Array.isArray(alims?.results) ? alims.results : (alims || [])).map(toUpperKeys)
    cuotasCurso.value = (Array.isArray(cuots?.results) ? cuots.results : (cuots || [])).map(toUpperKeys)
    coordinadoresCurso.value = (Array.isArray(coords?.results) ? coords.results : (coords || [])).map(toUpperKeys)
    
    // Cargar catálogo de alimentación solo si es necesario
    if (!alimentacionCatalogo.value.length) {
      const cat = await mantenedores.alimentacion.list().catch(() => [])
      alimentacionCatalogo.value = Array.isArray(cat?.results) ? cat.results : (cat || [])
    }
  } catch (e) {
    console.error('[abrirModalVer] Error cargando datos:', e)
  }
}

function cerrarModalVer() {
  mostrarModalVer.value = false
  cursoSeleccionado.value = null
}

function abrirDashboard(curso) {
  cursoIdDashboard.value = curso.CUR_ID
  mostrarDashboard.value = true
}

function cerrarDashboard() {
  mostrarDashboard.value = false
  cursoIdDashboard.value = null
}
</script>

<style scoped>
.crud-cursos-container {
  padding: 24px;
  background-color: #f9fafb;
  font-family: 'Inter', sans-serif;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
}

.filters-card {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  flex-grow: 1;
  margin-right: 16px;
}

.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow-x: auto;
}

.courses-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

.courses-table th, .courses-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  font-size: 14px;
}

.courses-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
  position: sticky;
  top: 0;
  z-index: 2;
}
.courses-table tbody tr { transition: background-color .12s ease; }
.courses-table tbody tr:hover { background:#f1f5f9; }
.courses-table th:nth-child(1){min-width:180px}
.courses-table th:nth-child(2){min-width:120px}
.courses-table th:nth-child(3){min-width:130px}
.courses-table th:nth-child(4){min-width:170px}
.courses-table th:nth-child(5){min-width:170px}
.courses-table th:nth-child(6){min-width:110px}
.courses-table th:nth-child(7){min-width:200px}

.actions-cell {
  display: flex;
  gap: 8px;
}

.no-results {
  text-align: center;
  padding: 32px;
  color: #6b7280;
}

.loading-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  font-size: 16px;
  color: #6b7280;
  gap: 10px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.modal-body { padding: 16px; max-height: calc(92vh - 160px); overflow-y: auto; }
/* Compactar un poco el contenido del modal para mayor comodidad visual */
.modal-body { padding: 12px; }

.form-grid-modal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-group label {
  font-weight: 500;
  margin-bottom: 4px;
  font-size: 14px;
  color: #374151;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 4px 8px; /* compact padding */
  border: 1.5px solid #4b5563; /* más contraste */
  border-radius: 5px;
  font-size: 13px; /* ligeramente menor */
  background: #ffffff;
  line-height: 1.25;
}
.form-group :deep(input), .form-group :deep(select), .form-group :deep(textarea) {
  padding: 4px 8px;
  border: 1.5px solid #4b5563;
  font-size: 13px;
  background: #ffffff;
  border-radius: 5px;
  line-height: 1.25;
}
.form-group :deep(input:focus), .form-group :deep(select:focus), .form-group :deep(textarea:focus),
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}
.form-group :deep(input::placeholder), .form-group :deep(textarea::placeholder) {
  color: #374151;
  opacity: 0.6;
}
.field-hint {
  margin-top: 4px;
  color: #6b7280;
  font-size: 12px;
}
.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-warning { background-color: #fef3c7; color: #92400e; }
.badge-success { background-color: #d1fae5; color: #065f46; }
.badge-secondary { background-color: #f3f4f6; color: #4b5563; }
.badge-danger { background-color: #fee2e2; color: #991b1b; }
.badge-dark { background-color: #e5e7eb; color: #1f2937; }

/* Estilos para la sección de fechas */
.fechas-section {
  margin-top: 24px;
}
.section-divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 24px 0;
}
.fechas-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}
.fechas-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}
.fechas-table th, .fechas-table td {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  text-align: left;
  font-size: 14px;
}
.fechas-table th {
  background-color: #f9fafb;
}
.no-results-small {
  text-align: center;
  color: #6b7280;
  padding: 16px;
}
.add-fecha-form {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 10px;
  align-items: flex-end;
}
.add-button {
  height: fit-content;
}

/* Icono dentro de inputs de fecha */
.input-icon { position: relative; }
.input-icon :deep(input) { padding-right: 28px; }
.input-icon .icon { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); color: #6b7280; pointer-events: none; }
/* Ocultar el ícono nativo del datepicker cuando usamos icono personalizado,
   manteniendo el área clickeable para abrir el calendario */
.input-icon :deep(input[type="date"])::-webkit-calendar-picker-indicator {
  opacity: 0;
  display: block;
  width: 20px;
  height: 20px;
}
/* Evitar iconos duplicados en otros motores cuando apliquen */
.input-icon :deep(input[type="date"]) {
  background-image: none;
}

/* Grid para cuotas */
.cuotas-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 12px;
}

/* Línea de agregado específica para 4 campos + botón */
.add-formadores-form {
  grid-template-columns: 1fr 1fr 1fr 1fr auto;
}
/* Línea de agregado específica para 5 campos + botón */
.add-alimentacion-form {
  grid-template-columns: 1fr 1fr 1fr 1fr 0.8fr auto;
}

/* Estilos para section-box - Marco visual de secciones */
.section-box {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9fafb;
}

/* Hacer controles más pequeños */
.section-box .form-group label {
  font-size: 13px;
  margin-bottom: 4px;
}
.section-box .fechas-table th, 
.section-box .fechas-table td {
  padding: 6px 10px;
  font-size: 13px;
}
.section-box .add-fecha-form {
  gap: 8px;
}
.section-box h4 {
  font-size: 16px;
  margin-bottom: 12px;
}

/* Dashboard Overlay */
.dashboard-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  z-index: 9999;
  overflow-y: auto;
}
</style>