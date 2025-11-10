<template>
  <ModernMainScrollbar>
  <div class="cursos-bg">
    <div class="cursos-container">
      <div class="cursos-header">
        <div class="page-header">
          <h3>Gestión de Cursos</h3>
          <p>Administra, crea y organiza los cursos de formación.</p>
        </div>
      </div>

      <!-- Barra de filtros global -->
      <div class="filters-bar">
        <label>
          Buscar
          <input v-model="filtros.searchQuery" type="text" placeholder="Por nombre o código..." />
        </label>

        <label>
          Estado
          <select v-model="filtros.estado">
            <option value="">Todos</option>
            <option v-for="opt in opcionesEstado" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
          </select>
        </label>

        <label>
          Tipo de Curso
          <select v-model="filtros.tipoCurso">
            <option value="">Todos</option>
            <option v-for="opt in tiposCursoOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
          </select>
        </label>

        <label>
          Responsable
          <select v-model="filtros.responsable">
            <option value="">Todos</option>
            <option v-for="opt in personasOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
          </select>
        </label>

        <!-- Botón Buscar -->
        <BaseButton variant="primary" @click="aplicarFiltros" style="align-self: end; margin-left: 8px;">
          <AppIcons name="search" :size="16" /> Buscar
        </BaseButton>
      </div>

      <!-- Lista de Cursos -->
      <section class="cursos-card">
        <div class="cursos-card-header">
          <span class="cursos-card-title blue-bar">Lista de Cursos</span>
          <div class="cursos-card-actions">
            <BaseButton @click="limpiarFiltros" variant="secondary"><AppIcons name="rotate-ccw" :size="16" /> Limpiar</BaseButton>
            <BaseButton variant="primary" @click="abrirModalCrear"><AppIcons name="plus" :size="16" /> Nuevo Curso</BaseButton>
          </div>
        </div>
        <div class="cursos-card-desc">
          <span v-if="isLoading" style="color: var(--color-info); font-weight: 600;"> (Cargando...)</span>
          <span v-if="error" style="color: var(--color-danger); font-weight: 600;"> ⚠️ {{ error }}</span>
        </div>
        <div class="datatable-visual">
          <table class="datatable-table">
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
              <tr v-if="isLoading">
                <td colspan="7" style="text-align: center; padding: 20px;">Cargando cursos...</td>
              </tr>
              <tr v-else-if="error">
                <td colspan="7" style="text-align: center; padding: 20px; color: var(--color-danger);">{{ error }}</td>
              </tr>
              <tr v-else-if="!cursosFiltrados.length">
                <td colspan="7" style="text-align: center; padding: 20px;">No hay cursos que coincidan con los filtros</td>
              </tr>
              <tr v-else v-for="c in cursosFiltrados" :key="c.CUR_ID">
                <td class="cell-desc">{{ c.CUR_DESCRIPCION || '-' }}</td>
                <td>{{ c.CUR_CODIGO || '-' }}</td>
                <td>{{ getTipoCursoName(c.TCU_ID) }}</td>
                <td>{{ formatDates(c) }}</td>
                <td>{{ getPersonaName(c.PER_ID_RESPONSABLE) }}</td>
                <td>
                  <span :class="['badge', getEstadoClass(c.CUR_ESTADO)]">
                    {{ getEstadoText(c.CUR_ESTADO) }}
                  </span>
                </td>
                <td class="actions-cell">
                  <BaseButton @click="abrirModalEditar(c)" variant="secondary" size="sm"><AppIcons name="edit-2" :size="14" /> Editar</BaseButton>
                  <BaseButton @click="deshabilitarCurso(c)" variant="danger" size="sm"><AppIcons name="x" :size="14" /> Deshabilitar</BaseButton>
                  <BaseButton @click="abrirModalVer(c)" variant="ghost" size="sm"><AppIcons name="eye" :size="14" /> Ver</BaseButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Modal de Creación/Edición -->
      <div v-if="mostrarModal" class="modal-overlay" @click.self="cerrarModal">
        <div class="modal-container">
          <div class="modal-header">
            <h2>{{ esEdicion ? 'Editar Curso' : 'Crear Nuevo Curso' }}</h2>
            <button class="modal-close" @click="cerrarModal">✕</button>
          </div>
          
          <div class="modal-body">
            <div class="form-grid">
              <div class="form-group span-2">
                <label>Descripción del Curso *</label>
                <input v-model="form.CUR_DESCRIPCION" type="text" placeholder="Ej: Curso de Liderazgo Juvenil" />
              </div>
              <div class="form-group">
                <label>Código *</label>
                <input v-model="form.CUR_CODIGO" type="text" maxlength="10" placeholder="Ej: CUR-2501" />
              </div>
              <div class="form-group">
                <label>Tipo de Curso *</label>
                <select v-model="form.TCU_ID">
                  <option value="">Selecciona...</option>
                  <option v-for="opt in tiposCursoOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Responsable *</label>
                <select v-model="form.PER_ID_RESPONSABLE">
                  <option value="">Selecciona...</option>
                  <option v-for="opt in personasOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Fecha de Solicitud</label>
                <input v-model="form.CUR_FECHA_SOLICITUD" type="date" />
              </div>
              <div class="form-group">
                <label>Estado</label>
                <select v-model="form.CUR_ESTADO">
                  <option v-for="opt in opcionesEstado" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Cuota con Almuerzo</label>
                <input v-model.number="form.CUR_COTA_CON_ALMUERZO" type="number" />
              </div>
              <div class="form-group">
                <label>Cuota sin Almuerzo</label>
                <input v-model.number="form.CUR_COTA_SIN_ALMUERZO" type="number" />
              </div>
              <div class="form-group">
                <label>Modalidad</label>
                <select v-model="form.CUR_MODALIDAD">
                  <option v-for="opt in opcionesModalidad" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Tipo (Presencial/Online)</label>
                <select v-model="form.CUR_TIPO_CURSO">
                  <option v-for="opt in opcionesTipoPresencial" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Administra</label>
                <select v-model="form.CUR_ADMINISTRA">
                  <option v-for="opt in opcionesAdministra" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Comuna (Lugar)</label>
                <select v-model="form.COM_ID_LUGAR">
                  <option value="">Selecciona...</option>
                  <option v-for="opt in comunasOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Cargo Responsable</label>
                <select v-model="form.CAR_ID_RESPONSABLE">
                  <option value="">Selecciona...</option>
                  <option v-for="opt in cargosOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                </select>
              </div>
              <div class="form-group span-2">
                <label>Lugar</label>
                <input v-model="form.CUR_LUGAR" type="text" placeholder="Ej: Sala 101" />
              </div>
              <div class="form-group span-2">
                <label>Ubicación en Mapa</label>
                <div v-if="form.CUR_COORD_LATITUD && form.CUR_COORD_LONGITUD" class="map-preview">
                  <MapEmbed 
                    :lat="form.CUR_COORD_LATITUD" 
                    :lng="form.CUR_COORD_LONGITUD"
                    @update:lat="form.CUR_COORD_LATITUD = $event"
                    @update:lng="form.CUR_COORD_LONGITUD = $event"
                  />
                </div>
                <div v-else class="map-placeholder">Mapa no disponible. Ingresa coordenadas manualmente.</div>
              </div>
              <div class="form-group">
                <label>Latitud</label>
                <input v-model.number="form.CUR_COORD_LATITUD" type="number" step="0.0001" />
              </div>
              <div class="form-group">
                <label>Longitud</label>
                <input v-model.number="form.CUR_COORD_LONGITUD" type="number" step="0.0001" />
              </div>
              <div class="form-group span-2">
                <label>Observaciones</label>
                <textarea v-model="form.CUR_OBSERVACION" rows="3" placeholder="Notas adicionales..."></textarea>
              </div>
            </div>

            <!-- Sección de Formadores (edición y creación) -->
            <div class="subsection">
              <h3>Equipo Formadores</h3>
              <div class="subsection-table">
                <table class="datatable-table">
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
                      <td colspan="5" style="text-align:center; padding: 12px;">Sin formadores</td>
                    </tr>
                    <tr v-for="f in formadoresCurso" :key="f.CUF_ID || ('tmp-' + (f.__tmpId || 0))">
                      <td>{{ getPersonaName(f.PER_ID) }}</td>
                      <td>{{ rolesList.find(r => r.ROL_ID === f.ROL_ID)?.ROL_DESCRIPCION || '-' }}</td>
                      <td>{{ seccionesCurso.find(s => s.CUS_ID === f.CUS_ID)?.CUS_SECCION || '-' }}</td>
                      <td>{{ f.CUO_DIRECTOR ? 'Sí' : 'No' }}</td>
                      <td><BaseButton @click="eliminarFormadorItem(f)" variant="danger" size="sm">Eliminar</BaseButton></td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Agregar formador -->
              <div class="add-form">
                <h4>Agregar Formador</h4>
                <div class="form-row">
                  <div class="form-group">
                    <label>Persona</label>
                    <select v-model="nuevaFormador.PER_ID">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in personasOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Rol</label>
                    <select v-model="nuevaFormador.ROL_ID">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in rolesOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Sección</label>
                    <select v-model="nuevaFormador.CUS_ID">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in seccionesOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Director</label>
                    <input type="checkbox" v-model="nuevaFormador.CUO_DIRECTOR" />
                  </div>
                  <BaseButton @click="agregarFormador" style="align-self: flex-end;">Añadir</BaseButton>
                </div>
              </div>
            </div>

            <!-- Sección de Alimentación (edición y creación) -->
            <div class="subsection">
              <h3>Alimentación</h3>
              <div class="subsection-table">
                <table class="datatable-table">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Tiempo</th>
                      <th>Alimento</th>
                      <th>Descripción</th>
                      <th>Adic.</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="!alimentacionesCurso.length">
                      <td colspan="6" style="text-align:center; padding: 12px;">Sin alimentación</td>
                    </tr>
                    <tr v-for="a in alimentacionesCurso" :key="a.CUA_ID || ('tmp-' + (a.__tmpId || 0))">
                      <td>{{ formatDateSimple(a.CUA_FECHA) }}</td>
                      <td>{{ tiempoAlimentacionOptions.find(t => t.value === a.CUA_TIEMPO)?.text }}</td>
                      <td>{{ alimentacionCatalogo.find(x => x.ALI_ID === a.ALI_ID)?.ALI_DESCRIPCION || '-' }}</td>
                      <td>{{ a.CUA_DESCRIPCION }}</td>
                      <td>{{ a.CUA_CANTIDAD_ADICIONAL }}</td>
                      <td><BaseButton @click="eliminarAlimentacionItem(a)" variant="danger" size="sm">Eliminar</BaseButton></td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="add-form">
                <h4>Agregar Alimentación</h4>
                <div class="form-row">
                  <div class="form-group">
                    <label>Fecha</label>
                    <input v-model="nuevaAlimentacion.CUA_FECHA" type="date" />
                  </div>
                  <div class="form-group">
                    <label>Tiempo</label>
                    <select v-model="nuevaAlimentacion.CUA_TIEMPO">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in tiempoAlimentacionOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Alimento</label>
                    <select v-model="nuevaAlimentacion.ALI_ID">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in alimentacionOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Descripción</label>
                    <input v-model="nuevaAlimentacion.CUA_DESCRIPCION" type="text" placeholder="Descripción" />
                  </div>
                  <div class="form-group">
                    <label>Adicional</label>
                    <input v-model.number="nuevaAlimentacion.CUA_CANTIDAD_ADICIONAL" type="number" min="0" />
                  </div>
                  <BaseButton @click="agregarAlimentacion" style="align-self: flex-end;">Añadir</BaseButton>
                </div>
              </div>
            </div>

            <!-- Sección de Fechas (edición y creación) -->
            <div class="subsection">
              <h3>Períodos del Curso</h3>
              <div class="subsection-table">
                <table class="datatable-table">
                  <thead>
                    <tr>
                      <th>Inicio</th>
                      <th>Término</th>
                      <th>Tipo</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="!fechasCurso.length">
                      <td colspan="4" style="text-align: center; padding: 12px;">No hay períodos definidos</td>
                    </tr>
                    <tr v-for="fecha in fechasCurso" :key="fecha.CUF_ID || ('tmp-' + (fecha.__tmpId || 0))">
                      <td>{{ formatDateSimple(fecha.CUF_FECHA_INICIO) }}</td>
                      <td>{{ formatDateSimple(fecha.CUF_FECHA_TERMINO) }}</td>
                      <td>{{ opcionesTipoFecha.find(t => t.value === fecha.CUF_TIPO)?.text }}</td>
                      <td><BaseButton @click="eliminarFechaItem(fecha)" variant="danger" size="sm">Eliminar</BaseButton></td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Agregar fecha -->
              <div class="add-form">
                <h4>Agregar Nuevo Período</h4>
                <div class="form-row">
                  <div class="form-group">
                    <label>Fecha Inicio</label>
                    <input v-model="nuevoPeriodo.CUF_FECHA_INICIO" type="date" />
                  </div>
                  <div class="form-group">
                    <label>Fecha Término</label>
                    <input v-model="nuevoPeriodo.CUF_FECHA_TERMINO" type="date" />
                  </div>
                  <div class="form-group">
                    <label>Tipo</label>
                    <select v-model="nuevoPeriodo.CUF_TIPO">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in opcionesTipoFecha" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <BaseButton @click="agregarFecha" style="align-self: flex-end;">Añadir</BaseButton>
                </div>
              </div>
            </div>

            <!-- Sección de Secciones (edición y creación) -->
            <div class="subsection">
              <h3>Secciones del Curso</h3>
              <div class="subsection-table">
                <table class="datatable-table">
                  <thead>
                    <tr>
                      <th>Sección</th>
                      <th>Rama</th>
                      <th>Participantes</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="!seccionesCurso.length">
                      <td colspan="4" style="text-align: center; padding: 12px;">No hay secciones definidas</td>
                    </tr>
                    <tr v-for="seccion in seccionesCurso" :key="seccion.CUS_ID || ('tmp-' + (seccion.__tmpId || 0))">
                      <td>{{ seccion.CUS_SECCION }}</td>
                      <td>{{ getRamaName(seccion.RAM_ID) }}</td>
                      <td>{{ seccion.CUS_CANT_PARTICIPANTE }}</td>
                      <td><BaseButton @click="eliminarSeccionItem(seccion)" variant="danger" size="sm">Eliminar</BaseButton></td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Agregar sección -->
              <div class="add-form">
                <h4>Agregar Nueva Sección</h4>
                <div class="form-row">
                  <div class="form-group">
                    <label>Sección #</label>
                    <input v-model.number="nuevaSeccion.CUS_SECCION" type="number" placeholder="1, 2, 3..." />
                  </div>
                  <div class="form-group">
                    <label>Rama</label>
                    <select v-model="nuevaSeccion.RAM_ID">
                      <option value="">Selecciona...</option>
                      <option v-for="opt in ramasOptions" :key="opt.value" :value="opt.value">{{ opt.text }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Participantes</label>
                    <input v-model.number="nuevaSeccion.CUS_CANT_PARTICIPANTE" type="number" placeholder="Cantidad" />
                  </div>
                  <BaseButton @click="agregarSeccion" style="align-self: flex-end;">Añadir</BaseButton>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <BaseButton @click="cerrarModal" variant="secondary">Cancelar</BaseButton>
            <BaseButton @click="guardarCurso" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : 'Guardar Cambios' }}
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Modal de Detalle -->
      <div v-if="mostrarModalVer" class="modal-overlay" @click.self="cerrarModalVer">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Detalle del Curso</h2>
            <button class="modal-close" @click="cerrarModalVer">✕</button>
          </div>

          <div class="modal-body">
            <div v-if="cursoSeleccionado" class="detalle-grid">
              <div class="detail-item">
                <strong>Descripción:</strong>
                <p>{{ cursoSeleccionado.CUR_DESCRIPCION }}</p>
              </div>
              <div class="detail-item">
                <strong>Código:</strong>
                <p>{{ cursoSeleccionado.CUR_CODIGO }}</p>
              </div>
              <div class="detail-item">
                <strong>Tipo:</strong>
                <p>{{ getTipoCursoName(cursoSeleccionado.TCU_ID) }}</p>
              </div>
              <div class="detail-item">
                <strong>Responsable:</strong>
                <p>{{ getPersonaName(cursoSeleccionado.PER_ID_RESPONSABLE) }}</p>
              </div>
              <div class="detail-item">
                <strong>Estado:</strong>
                <span :class="['badge', getEstadoClass(cursoSeleccionado.CUR_ESTADO)]">
                  {{ getEstadoText(cursoSeleccionado.CUR_ESTADO) }}
                </span>
              </div>
              <div class="detail-item">
                <strong>Lugar:</strong>
                <p>{{ cursoSeleccionado.CUR_LUGAR || '-' }}</p>
              </div>
              <div class="detail-item">
                <strong>Coordenadas:</strong>
                <p>{{ cursoSeleccionado.CUR_COORD_LATITUD }}, {{ cursoSeleccionado.CUR_COORD_LONGITUD }}</p>
              </div>
              <div class="detail-item full">
                <strong>Observaciones:</strong>
                <p>{{ cursoSeleccionado.CUR_OBSERVACION || '-' }}</p>
              </div>
            </div>

            <h3 class="mt-20">Períodos</h3>
            <div class="subsection-table">
              <table class="datatable-table">
                <thead>
                  <tr>
                    <th>Inicio</th>
                    <th>Término</th>
                    <th>Tipo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!fechasCurso.length">
                    <td colspan="3" style="text-align: center; padding: 12px;">Sin períodos</td>
                  </tr>
                  <tr v-for="f in fechasCurso" :key="f.CUF_ID">
                    <td>{{ formatDateSimple(f.CUF_FECHA_INICIO) }}</td>
                    <td>{{ formatDateSimple(f.CUF_FECHA_TERMINO) }}</td>
                    <td>{{ opcionesTipoFecha.find(t => t.value === f.CUF_TIPO)?.text }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-20">Secciones</h3>
            <div class="subsection-table">
              <table class="datatable-table">
                <thead>
                  <tr>
                    <th>Sección</th>
                    <th>Rama</th>
                    <th>Participantes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!seccionesCurso.length">
                    <td colspan="3" style="text-align: center; padding: 12px;">Sin secciones</td>
                  </tr>
                  <tr v-for="s in seccionesCurso" :key="s.CUS_ID">
                    <td>{{ s.CUS_SECCION }}</td>
                    <td>{{ getRamaName(s.RAM_ID) }}</td>
                    <td>{{ s.CUS_CANT_PARTICIPANTE }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-20">Equipo del Curso</h3>
            <div class="subsection-table">
              <table class="datatable-table">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Nombre</th>
                    <th>Cargo/Rol</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!equipoCurso.coordinadores.length && !equipoCurso.formadores.length">
                    <td colspan="3" style="text-align:center; padding: 12px;">Sin equipo registrado</td>
                  </tr>
                  <tr v-for="c in equipoCurso.coordinadores" :key="`coord-${c.CUC_ID}`">
                    <td>Coordinador</td>
                    <td>{{ c.persona ? `${c.persona.PER_NOMBRES} ${c.persona.PER_APELPTA}` : '-' }}</td>
                    <td>{{ c.cargo ? c.cargo.CAR_DESCRIPCION : (c.CUC_CARGO || '-') }}</td>
                  </tr>
                  <tr v-for="f in equipoCurso.formadores" :key="`form-${f.CUF_ID}`">
                    <td>Formador</td>
                    <td>{{ f.persona ? `${f.persona.PER_NOMBRES} ${f.persona.PER_APELPTA}` : '-' }}</td>
                    <td>{{ f.rol ? f.rol.ROL_DESCRIPCION : '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-20">Participantes Inscritos</h3>
            <div class="subsection-table">
              <table class="datatable-table">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Sección</th>
                    <th>Rol</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!participantesInscritos.length">
                    <td colspan="3" style="text-align:center; padding: 12px;">Sin inscritos</td>
                  </tr>
                  <tr v-for="i in participantesInscritos" :key="i.PEC_ID">
                    <td>{{ i.persona ? `${i.persona.PER_NOMBRES} ${i.persona.PER_APELPTA}` : '-' }}</td>
                    <td>{{ seccionesList.find(s => s.CUS_ID === i.CUS_ID)?.CUS_SECCION || '-' }}</td>
                    <td>{{ i.rol ? i.rol.ROL_DESCRIPCION : '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-20">Formadores</h3>
            <div class="subsection-table">
              <table class="datatable-table">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Rol</th>
                    <th>Sección</th>
                    <th>Director</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!formadoresVer.length">
                    <td colspan="4" style="text-align:center; padding: 12px;">Sin formadores</td>
                  </tr>
                  <tr v-for="f in formadoresVer" :key="f.CUF_ID">
                    <td>{{ f.persona ? `${f.persona.PER_NOMBRES} ${f.persona.PER_APELPTA}` : '-' }}</td>
                    <td>{{ f.rol ? f.rol.ROL_DESCRIPCION : '-' }}</td>
                    <td>{{ f.seccion ? f.seccion.CUS_SECCION : '-' }}</td>
                    <td>{{ f.CUO_DIRECTOR ? 'Sí' : 'No' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-20">Alimentación del Curso</h3>
            <div class="subsection-table">
              <table class="datatable-table">
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
                  <tr v-if="!alimentacionesCurso.length">
                    <td colspan="5" style="text-align:center; padding: 12px;">Sin alimentación</td>
                  </tr>
                  <tr v-for="a in alimentacionesCurso" :key="a.CUA_ID">
                    <td>{{ formatDateSimple(a.CUA_FECHA) }}</td>
                    <td>{{ tiempoAlimentacionOptions.find(t => t.value === a.CUA_TIEMPO)?.text }}</td>
                    <td>{{ alimentacionCatalogo.find(x => x.ALI_ID === a.ALI_ID)?.ALI_DESCRIPCION || '-' }}</td>
                    <td>{{ a.CUA_DESCRIPCION }}</td>
                    <td>{{ a.CUA_CANTIDAD_ADICIONAL }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="modal-footer">
            <BaseButton @click="cerrarModalVer" variant="secondary">Cerrar</BaseButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  </ModernMainScrollbar>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/Reutilizables/ModernMainScrollbar.vue'
import MapEmbed from '@/components/Reutilizables/MapEmbed.vue'
// Servicios desacoplados específicos de la pantalla
import cursoScreenService, { loadAllData, getPersonaNombre, getTipoCursoNombre, estadoText, estadoClass, loadCoordinadoresByCurso, loadFormadoresByCurso, loadPersonaCursosByCurso } from '@/services/cursoScreenService'
// (Se mantienen importaciones directas si alguna acción CRUD específica las requiere más adelante)
import { cursos as cursosApi, fechas as fechasApi, secciones as seccionesApi, formadores as formadoresApi, alimentaciones as cursoAlimentacionesApi } from '@/services/cursosService'
import mantenedores from '@/services/mantenedoresService'

// ===== Estado =====
const isLoading = ref(true)
const isLoadingData = ref(false)
const error = ref(null)
const isSaving = ref(false)
const isDisabling = ref(false)

const cursosList = ref([])
const personasList = ref([])
const tiposCursoList = ref([])
const fechasCursoList = ref([])
const ramaslist = ref([])
const seccionesList = ref([])
const comunasList = ref([])
const cargosList = ref([])
const rolesList = ref([])
const coordinadoresList = ref([])
const formadoresList = ref([])
const personaCursosList = ref([])
// Formadores y alimentación (buffers similares a fechas/secciones)
const formadoresCurso = ref([]) // elementos visibles (persistidos o temporales)
const nuevaFormador = ref({ PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false })
const alimentacionesCurso = ref([])
const nuevaAlimentacion = ref({ ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 })
const alimentacionCatalogo = ref([])
const isAddingFormador = ref(false)
const isDeletingFormador = ref(false)
const isAddingAlimentacion = ref(false)
const isDeletingAlimentacion = ref(false)

const cursosFiltrados = ref([])
const fechasCurso = ref([])
const seccionesCurso = ref([])

const mostrarModal = ref(false)
const mostrarModalVer = ref(false)
const esEdicion = ref(false)
const cursoSeleccionado = ref(null)

const filtros = ref({
  searchQuery: '',
  estado: null,
  tipoCurso: null,
  responsable: null,
})

function defaultForm() {
  return {
    CUR_ID: null,
    CUR_DESCRIPCION: '',
    CUR_CODIGO: '',
    TCU_ID: null,
    PER_ID_RESPONSABLE: null,
    CUR_FECHA_SOLICITUD: '',
    CUR_ESTADO: 0, // 0: Pendiente (alineado backend)
    CUR_COTA_CON_ALMUERZO: 0,
    CUR_COTA_SIN_ALMUERZO: 0,
    CUR_MODALIDAD: 1, // 1 Internado, 2 Externado, 3 Internado/Externado
    CUR_TIPO_CURSO: 1, // 1 Presencial, 2 Online, 3 Hibrido
    CUR_ADMINISTRA: 1, // 1 Zona, 2 Distrito
    COM_ID_LUGAR: null,
    CAR_ID_RESPONSABLE: null,
    CUR_LUGAR: '',
    CUR_COORD_LATITUD: -36.7201,
    CUR_COORD_LONGITUD: -73.0449,
    CUR_OBSERVACION: '',
  }
}
const form = ref(defaultForm())

const nuevoPeriodo = ref({
  CUF_FECHA_INICIO: '',
  CUF_FECHA_TERMINO: '',
  CUF_TIPO: null,
})

// Flags para evitar doble envío rápido
const isAddingPeriodo = ref(false)
const isDeletingPeriodo = ref(false)
const isAddingSeccion = ref(false)
const isDeletingSeccion = ref(false)

const nuevaSeccion = ref({
  CUS_SECCION: null,
  RAM_ID: null,
  CUS_CANT_PARTICIPANTE: null,
})

let _tmpIdCounter = 1

// ===== Opciones =====
// Estados según backend: 0 Pendiente, 1 Vigente, 2 Anulado, 3 Finalizado
const opcionesEstado = [
  { value: 0, text: 'Pendiente' },
  { value: 1, text: 'Vigente' },
  { value: 2, text: 'Anulado' },
  { value: 3, text: 'Finalizado' },
]

// Modalidad administrativa del curso (modelo: 1 Internado, 2 Externado, 3 Internado/Externado)
const opcionesModalidad = [
  { value: 1, text: 'Internado' },
  { value: 2, text: 'Externado' },
  { value: 3, text: 'Internado/Externado' },
]

// Tipo operativo: 1 Presencial, 2 Online, 3 Hibrido
const opcionesTipoPresencial = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]

const opcionesAdministra = [
  { value: 1, text: 'Zona' },
  { value: 2, text: 'Distrito' },
]

const opcionesTipoFecha = [
  { value: 1, text: 'Presencial' },
  { value: 2, text: 'Online' },
  { value: 3, text: 'Híbrido' },
]

// ===== Computed =====
const tiposCursoOptions = computed(() => tiposCursoList.value.map(t => ({ value: t.TCU_ID, text: t.TCU_DESCRIPCION })))

const personasOptions = computed(() => personasList.value.map(p => ({ value: p.PER_ID, text: `${p.PER_NOMBRES} ${p.PER_APELPTA}` })))

const comunasOptions = computed(() => comunasList.value.map(c => ({ value: c.COM_ID, text: c.COM_DESCRIPCION })))
const cargosOptions = computed(() => cargosList.value.map(c => ({ value: c.CAR_ID, text: c.CAR_DESCRIPCION })))
const ramasOptions = computed(() => ramaslist.value.map(r => ({ value: r.RAM_ID, text: r.RAM_DESCRIPCION })))
const rolesOptions = computed(() => rolesList.value.map(r => ({ value: r.ROL_ID, text: r.ROL_DESCRIPCION })))
const seccionesOptions = computed(() => seccionesCurso.value.map(s => ({ value: s.CUS_ID || s.__tmpId, text: `Sección ${s.CUS_SECCION}` })))
const alimentacionOptions = computed(() => alimentacionCatalogo.value.map(a => ({ value: a.ALI_ID, text: a.ALI_DESCRIPCION })))
const tiempoAlimentacionOptions = [
  { value: 1, text: 'Desayuno' },
  { value: 2, text: 'Almuerzo' },
  { value: 3, text: 'Once' },
  { value: 4, text: 'Cena' },
  { value: 5, text: 'Once/Cena' },
]

const equipoCurso = computed(() => {
  if (!cursoSeleccionado.value) return { coordinadores: [], formadores: [] }
  const curId = cursoSeleccionado.value.CUR_ID
  const coords = coordinadoresList.value.filter(c => c.CUR_ID === curId).map(c => ({
    ...c,
    persona: personasList.value.find(p => p.PER_ID === c.PER_ID) || null,
    cargo: cargosList.value.find(x => x.CAR_ID === c.CAR_ID) || null,
  }))
  const forms = formadoresList.value.filter(f => f.CUR_ID === curId).map(f => ({
    ...f,
    persona: personasList.value.find(p => p.PER_ID === f.PER_ID) || null,
    rol: rolesList.value.find(x => x.ROL_ID === f.ROL_ID) || null,
  }))
  return { coordinadores: coords, formadores: forms }
})

const participantesInscritos = computed(() => {
  if (!cursoSeleccionado.value) return []
  const curId = cursoSeleccionado.value.CUR_ID
  const seccionesIds = seccionesList.value.filter(s => s.CUR_ID === curId).map(s => s.CUS_ID)
  const pecs = personaCursosList.value.filter(pc => seccionesIds.includes(pc.CUS_ID))
  return pecs.map(pc => ({
    ...pc,
    persona: personasList.value.find(p => p.PER_ID === pc.PER_ID) || null,
    rol: rolesList.value.find(r => r.ROL_ID === pc.ROL_ID) || null,
  }))
})

const formadoresVer = computed(() => {
  if (!cursoSeleccionado.value) return []
  const curId = cursoSeleccionado.value.CUR_ID
  const seccionesCursoMap = new Map(seccionesList.value.filter(s => s.CUR_ID === curId).map(s => [s.CUS_ID, s]))
  return formadoresList.value
    .filter(f => f.CUR_ID === curId)
    .map(f => ({
      ...f,
      persona: personasList.value.find(p => p.PER_ID === f.PER_ID) || null,
      rol: rolesList.value.find(r => r.ROL_ID === f.ROL_ID) || null,
      seccion: seccionesCursoMap.get(f.CUS_ID) || null,
    }))
})

// ===== Métodos =====
async function cargarDatos() {
  if (isLoadingData.value) return
  isLoadingData.value = true
  isLoading.value = true
  console.log('🔄 [cargarDatos] Iniciando carga desacoplada...')
  try {
    const { cursosData, fechasData, seccionesData, personasData, tiposCursoData, comunasData, cargosData, ramasData, rolesData } = await loadAllData()
    cursosList.value = cursosData
    fechasCursoList.value = fechasData
    seccionesList.value = seccionesData
    personasList.value = personasData
    tiposCursoList.value = tiposCursoData
    comunasList.value = comunasData
    cargosList.value = cargosData
    ramaslist.value = ramasData
  rolesList.value = rolesData
    // cargar catálogo alimentación (ligero)
    try {
  alimentacionCatalogo.value = await mantenedores.list('alimentacion')
    } catch (e) { console.warn('No se pudo cargar catálogo de alimentación:', e?.message) }
    cursosFiltrados.value = cursosList.value
    console.log(`✅ [cargarDatos] Cursos:${cursosList.value.length} Fechas:${fechasCursoList.value.length} Secciones:${seccionesList.value.length} Personas:${personasList.value.length} TiposCurso:${tiposCursoList.value.length}`)
    error.value = null
  } catch (e) {
    console.error('❌ [cargarDatos] Error general:', e)
    error.value = 'Error al cargar los datos'
  } finally {
    isLoading.value = false
    isLoadingData.value = false
  }
}

function getTipoCursoName(id) {
  return getTipoCursoNombre(tiposCursoList.value.find(x => x.TCU_ID === id))
}

function getPersonaName(id) {
  return getPersonaNombre(personasList.value.find(x => x.PER_ID === id))
}

function getRamaName(id) {
  const r = ramaslist.value.find(x => x.RAM_ID === id)
  return r ? r.RAM_DESCRIPCION : 'No definida'
}

function getEstadoText(estado) {
  return estadoText(estado)
}

function getEstadoClass(estado) {
  return estadoClass(estado)
}

function formatDates(curso) {
  const fechas = fechasCursoList.value.filter(f => f.CUR_ID === curso.CUR_ID)
  if (fechas.length === 0) return '-'
  const inicio = fechas[0].CUF_FECHA_INICIO?.split('T')[0]
  const termino = fechas[fechas.length - 1].CUF_FECHA_TERMINO?.split('T')[0]
  return `${inicio} a ${termino}`
}

function formatDateSimple(dateStr) {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

function aplicarFiltros() {
  cursosFiltrados.value = cursosList.value.filter(c => {
    const q = (filtros.value.searchQuery || '').toLowerCase().trim()
    const responsableNombre = getPersonaName(c.PER_ID_RESPONSABLE).toLowerCase()
    const matchSearchQuery = !q || 
      c.CUR_DESCRIPCION?.toLowerCase().includes(q) ||
      c.CUR_CODIGO?.toLowerCase().includes(q) ||
      responsableNombre.includes(q)
    
    const matchEstado = !filtros.value.estado || c.CUR_ESTADO === parseInt(filtros.value.estado)
    const matchTipo = !filtros.value.tipoCurso || c.TCU_ID === parseInt(filtros.value.tipoCurso)
    const matchResponsable = !filtros.value.responsable || c.PER_ID_RESPONSABLE === parseInt(filtros.value.responsable)
    
    return matchSearchQuery && matchEstado && matchTipo && matchResponsable
  })
}

function limpiarFiltros() {
  filtros.value = { searchQuery: '', estado: null, tipoCurso: null, responsable: null }
  cursosFiltrados.value = cursosList.value
}

function abrirModalCrear() {
  esEdicion.value = false
  form.value = defaultForm()
  fechasCurso.value = []
  seccionesCurso.value = []
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: null }
  nuevaSeccion.value = { CUS_SECCION: null, RAM_ID: null, CUS_CANT_PARTICIPANTE: null }
  mostrarModal.value = true
}

function abrirModalEditar(curso) {
  esEdicion.value = true
  // Garantizar que todos los campos esperados existan
  form.value = Object.assign({}, defaultForm(), curso)
  cargarFechasDelCurso(curso.CUR_ID)
  seccionesCurso.value = seccionesList.value.filter(s => s.CUR_ID === curso.CUR_ID)
  formadoresCurso.value = formadoresList.value.filter(f => f.CUR_ID === curso.CUR_ID)
  alimentacionesCurso.value = [] // se cargarán diferido si se requiere
  nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: null }
  nuevaSeccion.value = { CUS_SECCION: null, RAM_ID: null, CUS_CANT_PARTICIPANTE: null }
  nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
  nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
  mostrarModal.value = true
}

function cargarFechasDelCurso(cursoId) {
  fechasCurso.value = fechasCursoList.value.filter(f => f.CUR_ID === cursoId)
}

function resolverSeccionIdParaFormador(tmpOrRealId) {
  // Si la sección aún es temporal, después de persistir se actualizará.
  const seccion = seccionesCurso.value.find(s => (s.CUS_ID || s.__tmpId) === tmpOrRealId)
  return seccion?.CUS_ID || null
}

async function agregarFormador() {
  if (isAddingFormador.value) return
  if (!nuevaFormador.value.PER_ID || !nuevaFormador.value.ROL_ID || !nuevaFormador.value.CUS_ID) {
    alert('Completa persona, rol y sección para el formador.')
    return
  }
  try {
    isAddingFormador.value = true
    const item = {
      CUR_ID: form.value.CUR_ID || null,
      PER_ID: nuevaFormador.value.PER_ID,
      ROL_ID: nuevaFormador.value.ROL_ID,
      CUS_ID: resolverSeccionIdParaFormador(nuevaFormador.value.CUS_ID),
      CUO_DIRECTOR: nuevaFormador.value.CUO_DIRECTOR ? true : false,
    }
    if (form.value.CUR_ID && item.CUS_ID) {
      const creado = await formadoresApi.create({ ...item, CUR_ID: form.value.CUR_ID })
      formadoresCurso.value.push(creado)
      formadoresList.value.push(creado)
    } else {
      item.__tmpId = _tmpIdCounter++
      formadoresCurso.value.push(item)
    }
    nuevaFormador.value = { PER_ID: null, ROL_ID: null, CUS_ID: null, CUO_DIRECTOR: false }
  } catch (e) {
    console.error('Error agregando formador:', e)
    alert(`Error: ${e?.message || 'No se pudo agregar formador'}`)
  } finally {
    isAddingFormador.value = false
  }
}

function eliminarFormadorItem(f) {
  if (!f) return
  const id = f.CUF_ID
  if (!id) {
    formadoresCurso.value = formadoresCurso.value.filter(x => (x.__tmpId || null) !== (f.__tmpId || null))
    return
  }
  eliminarFormador(id)
}

async function eliminarFormador(id) {
  if (isDeletingFormador.value) return
  if (!confirm('Eliminar formador?')) return
  try {
    isDeletingFormador.value = true
    await formadoresApi.remove(id)
    formadoresCurso.value = formadoresCurso.value.filter(x => x.CUF_ID !== id)
    formadoresList.value = formadoresList.value.filter(x => x.CUF_ID !== id)
  } catch (e) {
    if (/404/.test(e.message)) {
      formadoresCurso.value = formadoresCurso.value.filter(x => x.CUF_ID !== id)
      formadoresList.value = formadoresList.value.filter(x => x.CUF_ID !== id)
    } else {
      console.error('Error eliminando formador:', e)
      alert(`Error: ${e?.message || 'No se pudo eliminar formador'}`)
    }
  } finally {
    isDeletingFormador.value = false
  }
}

async function agregarAlimentacion() {
  if (isAddingAlimentacion.value) return
  const a = nuevaAlimentacion.value
  if (!a.ALI_ID || !a.CUA_FECHA || !a.CUA_TIEMPO || !a.CUA_DESCRIPCION) {
    alert('Completa alimento, fecha, tiempo y descripción.')
    return
  }
  try {
    isAddingAlimentacion.value = true
    const item = {
      CUR_ID: form.value.CUR_ID || null,
      ALI_ID: a.ALI_ID,
      CUA_FECHA: a.CUA_FECHA,
      CUA_TIEMPO: a.CUA_TIEMPO,
      CUA_DESCRIPCION: a.CUA_DESCRIPCION.trim(),
      CUA_CANTIDAD_ADICIONAL: parseInt(a.CUA_CANTIDAD_ADICIONAL || 0, 10),
    }
    if (form.value.CUR_ID) {
      const creado = await cursoAlimentacionesApi.create({ ...item, CUR_ID: form.value.CUR_ID })
      alimentacionesCurso.value.push(creado)
    } else {
      item.__tmpId = _tmpIdCounter++
      alimentacionesCurso.value.push(item)
    }
    nuevaAlimentacion.value = { ALI_ID: null, CUA_FECHA: '', CUA_TIEMPO: null, CUA_DESCRIPCION: '', CUA_CANTIDAD_ADICIONAL: 0 }
  } catch (e) {
    console.error('Error agregando alimentación:', e)
    alert(`Error: ${e?.message || 'No se pudo agregar alimentación'}`)
  } finally {
    isAddingAlimentacion.value = false
  }
}

function eliminarAlimentacionItem(a) {
  if (!a) return
  const id = a.CUA_ID
  if (!id) {
    alimentacionesCurso.value = alimentacionesCurso.value.filter(x => (x.__tmpId || null) !== (a.__tmpId || null))
    return
  }
  eliminarAlimentacion(id)
}

async function eliminarAlimentacion(id) {
  if (isDeletingAlimentacion.value) return
  if (!confirm('Eliminar alimentación?')) return
  try {
    isDeletingAlimentacion.value = true
    await cursoAlimentacionesApi.remove(id)
    alimentacionesCurso.value = alimentacionesCurso.value.filter(x => x.CUA_ID !== id)
  } catch (e) {
    if (/404/.test(e.message)) {
      alimentacionesCurso.value = alimentacionesCurso.value.filter(x => x.CUA_ID !== id)
    } else {
      console.error('Error eliminando alimentación:', e)
      alert(`Error: ${e?.message || 'No se pudo eliminar alimentación'}`)
    }
  } finally {
    isDeletingAlimentacion.value = false
  }
}

function abrirModalVer(curso) {
  cursoSeleccionado.value = curso
  cargarFechasDelCurso(curso.CUR_ID)
  seccionesCurso.value = seccionesList.value.filter(s => s.CUR_ID === curso.CUR_ID)
  // Carga diferida de datos pesados para optimizar la primera carga
  if (curso?.CUR_ID) cargarEquipoYParticipantes(curso.CUR_ID)
  // Alimentación: carga diferida también
  if (!alimentacionCatalogo.value.length) {
    mantenedores.list('alimentacion').then(res => { alimentacionCatalogo.value = res }).catch(() => {})
  }
  // Si deseas cargar alimentación desde backend por curso, aquí sería el lugar.
  mostrarModalVer.value = true
}

// Carga diferida de equipo (coordinadores, formadores) y participantes inscritos de un curso específico.
// Evita traer toda la data pesada en la primera carga de la pantalla.
function mergeUnique(target, incoming, keyField) {
  const existingIds = new Set(target.map(x => x[keyField]))
  incoming.forEach(item => {
    if (!existingIds.has(item[keyField])) {
      target.push(item)
    }
  })
}

async function cargarEquipoYParticipantes(curId) {
  if (!curId) return
  try {
    const yaCargadosCoords = coordinadoresList.value.some(c => c.CUR_ID === curId)
    const yaCargadosForms = formadoresList.value.some(f => f.CUR_ID === curId)
    // Para personaCursos verificamos si hay algún PEC_ID asociado a secciones del curso
    const seccionesCursoIds = seccionesList.value.filter(s => s.CUR_ID === curId).map(s => s.CUS_ID)
    const yaCargadosPecs = personaCursosList.value.some(pc => seccionesCursoIds.includes(pc.CUS_ID))

    if (yaCargadosCoords && yaCargadosForms && yaCargadosPecs) {
      console.log('ℹ️ [cargarEquipoYParticipantes] Datos ya presentes para curso', curId)
      return
    }

    console.log('📥 [cargarEquipoYParticipantes] Cargando equipo y participantes del curso', curId)
    const [coords, forms, pecs] = await Promise.all([
      loadCoordinadoresByCurso(curId),
      loadFormadoresByCurso(curId),
      loadPersonaCursosByCurso(curId),
    ])

    mergeUnique(coordinadoresList.value, coords, 'CUC_ID')
    mergeUnique(formadoresList.value, forms, 'CUF_ID')
    mergeUnique(personaCursosList.value, pecs, 'PEC_ID')

    console.log(`✅ [cargarEquipoYParticipantes] Coord:${coords.length} Form:${forms.length} Inscritos:${pecs.length}`)
  } catch (e) {
    console.error('❌ [cargarEquipoYParticipantes] Error cargando datos diferidos:', e)
  }
}

function cerrarModal() {
  mostrarModal.value = false
  form.value = defaultForm()
}

function cerrarModalVer() {
  mostrarModalVer.value = false
  cursoSeleccionado.value = null
}

async function guardarCurso() {
  if (isSaving.value) return
  
  if (!form.value.CUR_DESCRIPCION || !form.value.CUR_CODIGO || !form.value.TCU_ID || !form.value.PER_ID_RESPONSABLE) {
    alert('Por favor completa todos los campos requeridos (*).')
    return
  }

  isSaving.value = true
  try {
    // Mapear y normalizar payload según modelo backend
    // Choices backend: CUR_MODALIDAD (1 Internado,2 Externado,3 Internado/Externado)
    const modalidadMap = { 'Internado': 1, 'Externado': 2, 'Internado/Externado': 3 }
    const tipoCursoOperativoMap = { 'Presencial': 1, 'Online': 2, 'Hibrido': 3, 'Híbrido': 3 }
    const administraMap = { Zona: 1, Distrito: 2 }

    const fechaSolicitudISO = (() => {
      const f = form.value.CUR_FECHA_SOLICITUD
      if (!f) return new Date().toISOString().split('T')[0] // default hoy
      // aceptar dd-mm-aaaa o yyyy-mm-dd
      if (/^\d{2}-\d{2}-\d{4}$/.test(f)) {
        const [dd, mm, yyyy] = f.split('-')
        return `${yyyy}-${mm}-${dd}`
      }
      if (/^\d{4}-\d{2}-\d{2}$/.test(f)) return f
      // fallback parse
      try { return new Date(f).toISOString().split('T')[0] } catch { return new Date().toISOString().split('T')[0] }
    })()

    // Determinar USU_ID: intentar leer de localStorage (si se guardó), sino usar 1 por defecto
  // Obtener USU_ID válido: priorizar localStorage, luego '2' (admin), luego fallback configurable
  let usuIdRaw = localStorage.getItem('USU_ID')
  let usuId = parseInt(usuIdRaw || '2', 10)
  if (Number.isNaN(usuId) || usuId <= 0) usuId = 2

    const datos = {
      CUR_ID: form.value.CUR_ID || undefined,
      USU_ID: usuId,
      TCU_ID: form.value.TCU_ID, // viene numérico del select de tipos curso
      PER_ID_RESPONSABLE: form.value.PER_ID_RESPONSABLE,
      CAR_ID_RESPONSABLE: form.value.CAR_ID_RESPONSABLE || 1, // fallback cargo responsable
      COM_ID_LUGAR: form.value.COM_ID_LUGAR || 1, // fallback comuna
      CUR_FECHA_SOLICITUD: fechaSolicitudISO,
      CUR_CODIGO: form.value.CUR_CODIGO.trim().slice(0,10),
      CUR_DESCRIPCION: form.value.CUR_DESCRIPCION.trim(),
      CUR_OBSERVACION: form.value.CUR_OBSERVACION || '',
      CUR_ADMINISTRA: typeof form.value.CUR_ADMINISTRA === 'number' ? form.value.CUR_ADMINISTRA : administraMap[form.value.CUR_ADMINISTRA] || 1,
      CUR_COTA_CON_ALMUERZO: parseInt(form.value.CUR_COTA_CON_ALMUERZO || 0, 10),
      CUR_COTA_SIN_ALMUERZO: parseInt(form.value.CUR_COTA_SIN_ALMUERZO || 0, 10),
      CUR_MODALIDAD: typeof form.value.CUR_MODALIDAD === 'number' ? form.value.CUR_MODALIDAD : modalidadMap[form.value.CUR_MODALIDAD] || 1,
      CUR_TIPO_CURSO: typeof form.value.CUR_TIPO_CURSO === 'number' ? form.value.CUR_TIPO_CURSO : tipoCursoOperativoMap[form.value.CUR_TIPO_CURSO] || 1,
      CUR_LUGAR: (form.value.CUR_LUGAR || 'Por definir').trim(),
      CUR_COORD_LATITUD: String(form.value.CUR_COORD_LATITUD || ''),
      CUR_COORD_LONGITUD: String(form.value.CUR_COORD_LONGITUD || ''),
      CUR_ESTADO: typeof form.value.CUR_ESTADO === 'number' ? form.value.CUR_ESTADO : parseInt(form.value.CUR_ESTADO || 1, 10),
    }

    console.log('🚀 Payload curso a enviar:', datos)

    // Validaciones mínimas antes de enviar
    const faltantes = []
    if (!datos.USU_ID) faltantes.push('USU_ID')
    if (!datos.TCU_ID) faltantes.push('TCU_ID')
    if (!datos.PER_ID_RESPONSABLE) faltantes.push('PER_ID_RESPONSABLE')
    if (!datos.CUR_CODIGO) faltantes.push('CUR_CODIGO')
    if (!datos.CUR_DESCRIPCION) faltantes.push('CUR_DESCRIPCION')
    if (!datos.CUR_LUGAR) faltantes.push('CUR_LUGAR')
    if (faltantes.length) {
      alert('Faltan campos requeridos: ' + faltantes.join(', '))
      isSaving.value = false
      return
    }

    if (form.value.CUR_ID) {
      await cursosApi.update(form.value.CUR_ID, datos)
      alert('Curso actualizado exitosamente')
    } else {
      const res = await cursosApi.create(datos)
      form.value.CUR_ID = res.CUR_ID
      // Persistir períodos y secciones en buffer ahora que existe CUR_ID
      if (fechasCurso.value.length) {
        for (const f of fechasCurso.value) {
          if (!f.CUF_ID) {
            try {
              const creado = await fechasApi.create({
                CUR_ID: form.value.CUR_ID,
                CUF_FECHA_INICIO: f.CUF_FECHA_INICIO,
                CUF_FECHA_TERMINO: f.CUF_FECHA_TERMINO,
                CUF_TIPO: f.CUF_TIPO,
              })
              // Reemplazar el temporal
              Object.assign(f, creado)
              fechasCursoList.value.push(creado)
            } catch (e) {
              console.error('❌ Error creando período post-curso:', e)
            }
          }
        }
      }
      if (seccionesCurso.value.length) {
        for (const s of seccionesCurso.value) {
          if (!s.CUS_ID) {
            try {
              const creadoS = await seccionesApi.create({
                CUR_ID: form.value.CUR_ID,
                CUS_SECCION: s.CUS_SECCION,
                RAM_ID: s.RAM_ID,
                CUS_CANT_PARTICIPANTE: s.CUS_CANT_PARTICIPANTE,
              })
              Object.assign(s, creadoS)
              seccionesList.value.push(creadoS)
            } catch (e) {
              console.error('❌ Error creando sección post-curso:', e)
            }
          }
        }
      }
      if (formadoresCurso.value.length) {
        for (const fm of formadoresCurso.value) {
          if (!fm.CUF_ID) {
            try {
              const creadoF = await formadoresApi.create({
                CUR_ID: form.value.CUR_ID,
                PER_ID: fm.PER_ID,
                ROL_ID: fm.ROL_ID,
                CUS_ID: resolverSeccionIdParaFormador(fm.CUS_ID || fm.__tmpId),
                CUO_DIRECTOR: fm.CUO_DIRECTOR ? true : false,
              })
              Object.assign(fm, creadoF)
              formadoresList.value.push(creadoF)
            } catch (e) {
              console.error('❌ Error creando formador post-curso:', e)
            }
          }
        }
      }
      if (alimentacionesCurso.value.length) {
        for (const al of alimentacionesCurso.value) {
          if (!al.CUA_ID) {
            try {
              const creadoA = await cursoAlimentacionesApi.create({
                CUR_ID: form.value.CUR_ID,
                ALI_ID: al.ALI_ID,
                CUA_FECHA: al.CUA_FECHA,
                CUA_TIEMPO: al.CUA_TIEMPO,
                CUA_DESCRIPCION: al.CUA_DESCRIPCION,
                CUA_CANTIDAD_ADICIONAL: al.CUA_CANTIDAD_ADICIONAL,
              })
              Object.assign(al, creadoA)
            } catch (e) {
              console.error('❌ Error creando alimentación post-curso:', e)
            }
          }
        }
      }
      alert('Curso creado exitosamente')
    }
    cerrarModal()
    await cargarDatos()
  } catch (e) {
    console.error('Error guardando curso:', e)
    alert(`Error: ${e?.message || 'No se pudo guardar'}`)
  } finally {
    isSaving.value = false
  }
}

async function deshabilitarCurso(curso) {
  if (isDisabling.value) return
  if (!confirm(`¿Deseas deshabilitar el curso "${curso.CUR_DESCRIPCION}"?`)) return

  isDisabling.value = true
  try {
    await cursosApi.partialUpdate(curso.CUR_ID, { CUR_ESTADO: 2 })
    alert('Curso deshabilitado exitosamente')
    await cargarDatos()
  } catch (e) {
    console.error('Error deshabilitando curso:', e)
    alert(`Error: ${e?.message || 'No se pudo deshabilitar'}`)
  } finally {
    isDisabling.value = false
  }
}

async function agregarFecha() {
  if (isAddingPeriodo.value) return
  if (!nuevoPeriodo.value.CUF_FECHA_INICIO || !nuevoPeriodo.value.CUF_FECHA_TERMINO || !nuevoPeriodo.value.CUF_TIPO) {
    alert('Por favor completa todos los campos de la fecha.')
    return
  }
  
  try {
    isAddingPeriodo.value = true
    const item = {
      CUR_ID: form.value.CUR_ID || null,
      CUF_FECHA_INICIO: nuevoPeriodo.value.CUF_FECHA_INICIO,
      CUF_FECHA_TERMINO: nuevoPeriodo.value.CUF_FECHA_TERMINO,
      CUF_TIPO: parseInt(nuevoPeriodo.value.CUF_TIPO, 10),
    }
    if (form.value.CUR_ID) {
      console.log('📤 Enviando fecha:', item)
      const res = await fechasApi.create({ ...item, CUR_ID: form.value.CUR_ID })
      console.log('✅ Fecha creada:', res)
      fechasCurso.value.push(res)
      fechasCursoList.value.push(res)
    } else {
      // buffer temporal hasta guardar curso
      item.__tmpId = _tmpIdCounter++
      fechasCurso.value.push(item)
    }
    nuevoPeriodo.value = { CUF_FECHA_INICIO: '', CUF_FECHA_TERMINO: '', CUF_TIPO: null }
    alert('Período agregado exitosamente')
  } catch (e) {
    console.error('❌ Error agregando fecha:', e)
    alert(`Error: ${e?.message || 'No se pudo agregar'}`)
  } finally {
    isAddingPeriodo.value = false
  }
}

function eliminarFechaItem(fecha) {
  if (!fecha) return
  const fechaId = fecha.CUF_ID
  if (!fechaId) {
    // solo en buffer
    fechasCurso.value = fechasCurso.value.filter(f => (f.__tmpId || null) !== (fecha.__tmpId || null))
    return
  }
  return eliminarFecha(fechaId)
}

async function eliminarFecha(fechaId) {
  if (isDeletingPeriodo.value) return
  if (!confirm('¿Deseas eliminar este período?')) return
  try {
    isDeletingPeriodo.value = true
    await fechasApi.remove(fechaId)
    // Actualizar listas locales
    fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)
    fechasCursoList.value = fechasCursoList.value.filter(f => f.CUF_ID !== fechaId)
    alert('Período eliminado exitosamente')
  } catch (e) {
    // Manejar 404 silencioso (ya eliminado o doble clic)
    if (/404/.test(e.message)) {
      console.warn('⚠️ Fecha ya no existe (404) fechaId=', fechaId)
      fechasCurso.value = fechasCurso.value.filter(f => f.CUF_ID !== fechaId)
      fechasCursoList.value = fechasCursoList.value.filter(f => f.CUF_ID !== fechaId)
      alert('El período ya había sido eliminado.')
    } else {
      console.error('Error eliminando fecha:', e)
      alert(`Error: ${e?.message || 'No se pudo eliminar'}`)
    }
  } finally {
    isDeletingPeriodo.value = false
  }
}

async function agregarSeccion() {
  if (isAddingSeccion.value) return
  if (!nuevaSeccion.value.CUS_SECCION || !nuevaSeccion.value.RAM_ID || !nuevaSeccion.value.CUS_CANT_PARTICIPANTE) {
    alert('Por favor completa todos los campos de la sección.')
    return
  }
  
  try {
    isAddingSeccion.value = true
    const item = {
      CUR_ID: form.value.CUR_ID || null,
      CUS_SECCION: nuevaSeccion.value.CUS_SECCION,
      RAM_ID: nuevaSeccion.value.RAM_ID,
      CUS_CANT_PARTICIPANTE: nuevaSeccion.value.CUS_CANT_PARTICIPANTE,
    }
    if (form.value.CUR_ID) {
      const res = await seccionesApi.create({ ...item, CUR_ID: form.value.CUR_ID })
      seccionesCurso.value.push(res)
      seccionesList.value.push(res)
    } else {
      item.__tmpId = _tmpIdCounter++
      seccionesCurso.value.push(item)
    }
    nuevaSeccion.value = { CUS_SECCION: null, RAM_ID: null, CUS_CANT_PARTICIPANTE: null }
    alert('Sección agregada exitosamente')
  } catch (e) {
    console.error('Error agregando sección:', e)
    alert(`Error: ${e?.message || 'No se pudo agregar'}`)
  } finally {
    isAddingSeccion.value = false
  }
}

function eliminarSeccionItem(seccion) {
  if (!seccion) return
  const seccionId = seccion.CUS_ID
  if (!seccionId) {
    // solo buffer temporal
    seccionesCurso.value = seccionesCurso.value.filter(s => (s.__tmpId || null) !== (seccion.__tmpId || null))
    return
  }
  return eliminarSeccion(seccionId)
}

async function eliminarSeccion(seccionId) {
  if (isDeletingSeccion.value) return
  if (!confirm('¿Deseas eliminar esta sección?')) return
  try {
    isDeletingSeccion.value = true
    await seccionesApi.remove(seccionId)
    seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
    seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
    alert('Sección eliminada exitosamente')
  } catch (e) {
    if (/404/.test(e.message)) {
      console.warn('⚠️ Sección ya no existe (404) seccionId=', seccionId)
      seccionesCurso.value = seccionesCurso.value.filter(s => s.CUS_ID !== seccionId)
      seccionesList.value = seccionesList.value.filter(s => s.CUS_ID !== seccionId)
      alert('La sección ya había sido eliminada.')
    } else {
      console.error('Error eliminando sección:', e)
      alert(`Error: ${e?.message || 'No se pudo eliminar'}`)
    }
  } finally {
    isDeletingSeccion.value = false
  }
}

onMounted(async () => {
  console.log('🔍 DEBUG onMounted')
  
  // Test directo
  // Cargar datos iniciales de la pantalla
  await cargarDatos()
})

// Actualizar coordenadas al cambiar la comuna (placeholder simple: asigna valores ficticios diferenciados)
watch(() => form.value.COM_ID_LUGAR, (newComuna) => {
  if (!newComuna) return
  // Buscar comuna para asignar coordenadas aproximadas (reemplazar con geocoding real si se requiere)
  const idx = comunasList.value.findIndex(c => c.COM_ID === newComuna)
  if (idx >= 0) {
    // Distribuir coordenadas base mediante offset
    const baseLat = -36.8201
    const baseLng = -73.0443
    form.value.CUR_COORD_LATITUD = (baseLat + (idx * 0.01)).toFixed(4)
    form.value.CUR_COORD_LONGITUD = (baseLng + (idx * 0.01)).toFixed(4)
  }
})

// Aplicar filtros reactivamente al escribir en searchQuery
watch(() => filtros.value.searchQuery, () => {
  aplicarFiltros()
})
</script>

<style scoped>
.cursos-bg {
  min-height: 100vh;
  background: var(--color-background);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cursos-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 16px 32px 16px;
}

.cursos-header {
  width: 100%;
  max-width: 1300px;
  margin: 0 auto 20px auto;
  padding: 0 22px;
  box-sizing: border-box;
}

.page-header { margin-bottom: 12px; }

.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px 0;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.filters-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: flex-start;
  margin: 10px auto 0 auto;
  padding: 0 22px 12px 22px;
  flex-wrap: wrap;
  width: 100%;
  max-width: 1300px;
  box-sizing: border-box;
}

.filters-bar label {
  font-weight: 600;
  color: var(--color-text);
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
}

.filters-bar input,
.filters-bar select {
  margin-top: 6px;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 0.95rem;
  min-width: 180px;
}

.cursos-card {
  background: var(--color-surface);
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(40,92,168,0.13);
  margin: 0 auto 28px auto;
  padding: 22px 22px 16px 22px;
  max-width: 1300px;
  width: 100%;
  box-sizing: border-box;
  border: 1.5px solid var(--color-border);
}

.cursos-card-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  gap: 10px;
}

.cursos-card-title {
  font-size: 1.18rem;
  font-weight: 700;
  color: var(--color-primary);
  position: relative;
  padding-left: 14px;
}

.blue-bar::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 6px;
  background: var(--color-primary);
  border-radius: 4px;
}

.cursos-card-actions {
  display: flex;
  flex-wrap: nowrap;
  gap: 12px;
  justify-content: flex-end;
}

.cursos-card-actions :deep(button) {
  min-width: 140px;
  padding: 10px 16px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(40,92,168,0.08);
  border: none;
}

.cursos-card-desc {
  color: #444;
  font-size: 1rem;
  margin-bottom: 10px;
}

.datatable-visual {
  width: 100%;
  overflow-x: auto;
}

.datatable-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--color-background-soft);
  border-radius: 10px;
  overflow: hidden;
  font-size: 1.05rem;
  margin-bottom: 0;
}

.datatable-table th {
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 700;
  padding: 12px 10px;
  border-bottom: 2px solid var(--color-border);
  text-align: left;
}

.datatable-table td {
  padding: 12px 10px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.datatable-table tr:nth-child(even) {
  background: var(--color-background-soft);
}

.datatable-table tr:last-child td {
  border-bottom: none;
}

.actions-cell {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.badge {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 1em;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  border: 1px solid transparent;
}

.badge-success {
  background: var(--color-semaforo-green);
  color: #fff;
}

.badge-warning {
  background: var(--color-semaforo-yellow);
  color: #fff;
}

.badge-danger {
  background: var(--color-semaforo-red);
  color: #fff;
}

.badge-secondary {
  background: #e9ecef;
  color: #334155;
  border-color: #cbd5e1;
}

/* ===== MODAL STYLES ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding-top: 70px; /* Dejar espacio para header azul fijo */
}

.modal-container {
  background: var(--color-surface);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  max-width: 900px;
  width: 90%;
  max-height: calc(100vh - 90px); /* Ajuste considerando offset superior */
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px; /* Reducir altura del header para más espacio de contenido */
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: var(--color-background);
  color: var(--color-text);
}

.modal-body {
  padding: 12px 16px 16px 16px; /* Más compacto todavía */
  overflow-y: auto;
  flex: 1;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 0.95rem;
  color: var(--color-text);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  font-size: 0.95rem;
  background: var(--color-background);
  color: var(--color-text);
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.map-preview {
  height: 300px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.map-placeholder {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
  border-radius: 6px;
  border: 1px dashed var(--color-border);
  color: #999;
  font-size: 0.9rem;
}

.subsection {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 2px solid var(--color-border);
}

.subsection h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 16px 0;
}

.subsection-table {
  margin-bottom: 20px;
  overflow-x: auto;
}

.add-form {
  background: var(--color-background);
  padding: 16px;
  border-radius: 8px;
  margin-top: 16px;
}

.add-form h4 {
  margin: 0 0 12px 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  align-items: flex-end;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
}

.modal-footer :deep(button) {
  min-width: 120px;
}

/* ===== DETALLE STYLES ===== */
.detalle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px; /* Menor gap para compactar */
  margin-bottom: 12px; /* Reducido */
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full {
  grid-column: span 2;
}

.detail-item strong {
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 4px;
}

.detail-item p {
  margin: 0;
  color: #555;
  font-size: 0.9rem; /* Leve reducción para más contenido visible */
}

.mt-20 {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-bar label {
    width: 100%;
  }

  .filters-bar input,
  .filters-bar select {
    min-width: auto;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid .form-group.span-2 {
    grid-column: auto;
  }

  .modal-container {
    width: 95%;
  }

  .detalle-grid {
    grid-template-columns: 1fr;
  }

  .detail-item.full {
    grid-column: auto;
  }

  .cursos-card-actions {
    width: 100%;
  }

  .cursos-card-actions :deep(button) {
    flex: 1;
    min-width: auto;
  }
}
</style>
