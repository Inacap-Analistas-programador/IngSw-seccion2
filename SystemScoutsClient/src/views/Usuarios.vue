<template>
  <div class="usuarios-roles">
    <ModernMainScrollbar>
      <!-- Encabezado de la sección -->
      <header class="page-header">
        <h3>Gestión de Usuarios</h3>
        <p class="page-description">Administra, crea y organiza los usuarios del sistema.</p>
      </header>

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <InputBase 
        v-model="searchQuery" 
        placeholder="Buscar por nombre o usuario..." 
        class="filtro-item"
      />
      <BaseSelect 
        v-model="filtroRol" 
        :options="rolesOptions" 
        placeholder="Todos los roles"
        class="filtro-item"
      />
      <BaseSelect 
        v-model="filtroEstado" 
        :options="estadoOptions" 
        placeholder="Todos los estados"
        class="filtro-item"
      />
      <BaseButton 
        variant="primary" 
        @click="filtrarUsuarios"
        class="filtro-item"
      >
        <AppIcons name="search" :size="16" />
        Buscar
      </BaseButton>
    </div>

    <!-- Indicador de carga -->
    <div v-if="cargando" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando usuarios...</p>
    </div>

    <!-- Tabla de usuarios -->
    <div v-else class="table-container">
      <div class="table-header-bar">
        <h3 class="table-title">Lista de Usuarios</h3>
        <div class="table-actions">
          <BaseButton 
            variant="secondary" 
            @click="editarSeleccionado"
            :disabled="selectedIds.length !== 1"
          >
            <AppIcons name="edit" :size="16" />
            Editar
          </BaseButton>
          <BaseButton 
            variant="secondary" 
            @click="toggleEstadoSeleccionados"
            :disabled="selectedIds.length === 0"
          >
            <AppIcons :name="botonEstadoIcon" :size="16" />
            {{ botonEstadoLabel }}
          </BaseButton>
          <BaseButton 
            variant="primary" 
            @click="abrirModalCrear"
          >
            <AppIcons name="plus" :size="16" />
            Nuevo Usuario
          </BaseButton>
        </div>
      </div>
      
      <div class="table-wrapper">
        <table class="usuarios-table">
          <thead>
            <tr>
              <th></th>
              <th>Usuario</th>
              <th>Contraseña</th>
              <th>Perfil</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="usuario in usuariosFiltrados" 
              :key="usuario.id"
              :class="{ 
                'usuario-inactivo': !usuario.activo,
                'row-selected': isSelected(usuario.id)
              }"
              @click="toggleRowSelection(usuario)"
            >
              <td data-label="Foto" class="foto-cell">
                <div class="user-avatar">
                  <img 
                    v-if="usuario.foto" 
                    :src="usuario.foto" 
                    :alt="usuario.username"
                    class="avatar-image"
                  />
                  <div v-else class="avatar-placeholder">
                    <AppIcons name="user" :size="24" />
                  </div>
                </div>
              </td>
              <td data-label="Usuario">{{ usuario.username }}</td>
              <td data-label="Contraseña">••••••••</td>
              <td data-label="Perfil">
                <span class="badge rol-badge" :class="rolClass(usuario)">
                  {{ getRolLabel(usuario.perfil_id) || usuario.rol }}
                </span>
              </td>
              <td data-label="Estado">
                <span class="badge" :class="usuario.activo ? 'badge-activo' : 'estado-inactivo'">
                  {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              
            </tr>
            <tr v-if="usuariosFiltrados.length === 0" class="empty-row">
              <td colspan="5">
                <div class="empty-state">
                  <p>No se encontraron usuarios</p>
                  <BaseButton variant="primary" @click="limpiarFiltros">
                    <AppIcons name="refresh" :size="16" />
                    Mostrar todos
                  </BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    </ModernMainScrollbar>

    <!-- Modal para crear/editar usuario -->
    <BaseModal v-model="modalVisible" @close="cerrarModal">
      <template #default>
        <div class="modal-usuario">
              <header class="modal-header">
                <h3>{{ modoEdicion ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}</h3>
              </header>

              <div class="modal-body-wrapper">
                <form @submit.prevent="guardarUsuario" class="usuario-form">
                  <!-- Sección de Foto y Datos Básicos en una sola fila -->
                  <div class="form-section datos-basicos">
                    <div class="section-title">
                      <AppIcons name="user" :size="20" />
                      <span>Información Personal</span>
                    </div>
                  
                    <div class="form-row form-row-triple">
                      <!-- Foto de perfil -->
                      <div class="form-group photo-group-inline">
                        <label>Foto de perfil</label>
                        <div class="photo-upload-inline" @click="triggerFotoSeleccion">
                          <div class="photo-preview-inline">
                            <img 
                              v-if="usuarioForm.fotoPreview" 
                              :src="usuarioForm.fotoPreview" 
                              alt="Vista previa"
                              class="preview-image-inline"
                            />
                            <div v-else class="preview-placeholder-inline">
                              <AppIcons name="camera" :size="28" />
                            </div>
                            <button 
                              v-if="usuarioForm.fotoPreview" 
                              type="button" 
                              class="remove-foto-btn" 
                              @click.stop="eliminarFoto"
                              :disabled="procesando"
                              aria-label="Eliminar foto"
                              title="Eliminar foto"
                            >
                              ×
                            </button>
                          </div>
                          <span class="photo-hint">{{ usuarioForm.fotoPreview ? 'Click para cambiar' : 'Click para subir' }}</span>
                          <input 
                            ref="fileInput"
                            type="file" 
                            accept="image/*"
                            @change="handleFileChange"
                            style="display: none"
                          />
                        </div>
                        <small class="form-hint-compact">Click en la foto para {{ usuarioForm.fotoPreview ? 'cambiar' : 'subir' }}</small>
                      </div>

                      <!-- Nombre de usuario -->
                      <div class="form-group flex-1">
                        <label for="username">Nombre de Usuario <span class="required">*</span></label>
                        <InputBase 
                          id="username"
                          v-model="usuarioForm.username" 
                          placeholder="Ej: jperez"
                          required
                          :disabled="procesando"
                        />
                      </div>

                      <!-- Rol -->
                      <div class="form-group flex-1">
                        <label for="rol">Perfil <span class="required">*</span></label>
                        <BaseSelect 
                          id="rol"
                          v-model="usuarioForm.rol" 
                          :options="rolesOptions"
                          placeholder="Seleccionar rol"
                          required
                          :disabled="procesando"
                        />
                      </div>
                    </div>

                    <!-- Estado con toggle switch -->
                    <div class="form-row" style="margin-top: 1rem;">
                      <div class="form-group" style="flex-direction: row; align-items: center; gap: 1rem;">
                        <label style="margin-bottom: 0; font-weight: 600; color: #2c3e50;">Estado del Usuario:</label>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                          <BaseSwitch v-model="usuarioForm.activo" />
                          <span :class="['estado-badge', usuarioForm.activo ? 'badge-activo' : 'estado-inactivo']">
                            {{ usuarioForm.activo ? 'Activo' : 'Inactivo' }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Sección de Seguridad -->
                  <div class="form-section">
                    <div class="section-title">
                      <AppIcons name="lock" :size="20" />
                      <span>Seguridad</span>
                    </div>

                    <div class="form-row">
                      <div class="form-group flex-1">
                        <label for="password">Contraseña <span class="required">{{ modoEdicion ? '' : '*' }}</span></label>
                        <InputBase 
                          id="password"
                          v-model="usuarioForm.password" 
                          type="password"
                          :placeholder="modoEdicion ? 'Dejar vacío para no cambiar' : 'Mínimo 6 caracteres'"
                          :required="!modoEdicion"
                          :disabled="procesando"
                        />
                      </div>

                      <div class="form-group flex-1">
                        <label for="confirmPassword">Confirmar Contraseña <span class="required" v-if="usuarioForm.password">*</span></label>
                        <InputBase 
                          id="confirmPassword"
                          v-model="usuarioForm.confirmPassword" 
                          type="password"
                          placeholder="Repetir contraseña"
                          :required="!!usuarioForm.password"
                          :disabled="procesando || !usuarioForm.password"
                        />
                      </div>
                    </div>

                    <div v-if="usuarioForm.password && usuarioForm.confirmPassword && usuarioForm.password !== usuarioForm.confirmPassword" class="error-message">
                      <AppIcons name="alert" :size="16" />
                      Las contraseñas no coinciden
                    </div>
                  </div>

                  <div class="form-actions">
                    <BaseButton 
                      type="button" 
                      variant="secondary"
                      @click="cerrarModal"
                      :disabled="procesando"
                    >
                      Cancelar
                    </BaseButton>
                    <BaseButton 
                      type="submit" 
                      variant="primary"
                      :disabled="procesando || !formularioValido"
                    >
                      <AppIcons v-if="!procesando" :name="modoEdicion ? 'save' : 'add'" :size="18" />
                      {{ procesando ? 'Guardando...' : (modoEdicion ? 'Guardar Cambios' : 'Crear Usuario') }}
                    </BaseButton>
                  </div>
                </form>
              </div>
        </div>
      </template>
    </BaseModal>

    <!-- Modal de confirmación -->
    <BaseModal v-model="modalConfirmacionVisible" @close="cancelarAccion">
      <template #default>
        <div class="modal-confirmacion">
          <h3>{{ tituloConfirmacion }}</h3>
          <p>{{ mensajeConfirmacion }}</p>
          <div class="form-actions">
            <BaseButton 
              variant="secondary" 
              @click="cancelarAccion"
              :disabled="procesando"
            >
              Cancelar
            </BaseButton>
            <BaseButton 
              variant="danger" 
              @click="ejecutarAccion"
              :disabled="procesando"
            >
              {{ procesando ? 'Procesando...' : 'Confirmar' }}
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseModal>

    <!-- Notificaciones -->
    <NotificationToast 
      v-if="notificacion.visible"
      :message="notificacion.mensaje"
      :type="notificacion.tipo"
      @close="cerrarNotificacion"
    />
  </div>
</template>

<script>
// Conectado a la API - usa servicios reales
import { useRouter } from 'vue-router'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import BaseSelect from '../components/BaseSelect.vue'
import BaseCheckBox from '../components/BaseCheckBox.vue'
import BaseSwitch from '../components/BaseSwitch.vue'
import InputBase from '../components/InputBase.vue'
import NotificationToast from '../components/NotificationToast.vue'
import AppIcons from '../components/icons/AppIcons.vue'
import PermisosToggle from '../components/PermisosToggle.vue'
import ModernMainScrollbar from '../components/ModernMainScrollbar.vue'
import { usuarios as usuariosService, perfiles as perfilesService } from '@/services/usuariosService'

export default {
  name: 'UsuariosRoles',
  components: {
    BaseButton,
    BaseModal,
    BaseSelect,
    BaseCheckBox,
    BaseSwitch,
    InputBase,
    NotificationToast,
    AppIcons,
    PermisosToggle,
    ModernMainScrollbar
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      usuarios: [],
      usuariosFiltrados: [],
      selectedIds: [], // IDs de usuarios seleccionados
      aplicaciones: [], // Módulos del sistema con permisos
      searchQuery: '',
      filtroRol: '',
      filtroEstado: '',
      cargando: false,
      procesando: false,
  // Permisos por usuario guardados en memoria (simula la API)
  userPerms: {},
      
      // Modal
      modalVisible: false,
      modoEdicion: false,
      usuarioForm: {
        id: null,
        username: '',
        rol: '',
        password: '',
        confirmPassword: '',
        activo: true,
        foto: null,
        fotoPreview: null
      },
      
      // Confirmación
      modalConfirmacionVisible: false,
      accionConfirmacion: null,
      tituloConfirmacion: '',
      mensajeConfirmacion: '',
      
      // Notificaciones
      notificacion: {
        visible: false,
        mensaje: '',
        tipo: 'info'
      },
      
      // Opciones
      rolesOptions: [],
      estadoOptions: [
        { value: '', label: 'Todos los estados' },
        { value: 'activo', label: 'Activos' },
        { value: 'inactivo', label: 'Inactivos' }
      ]
      ,
      // Foto por defecto cuando no se sube ninguna
      defaultFoto: 'https://via.placeholder.com/96.png?text=Avatar'
    }
  },
  computed: {
    formularioValido() {
      if (!this.usuarioForm.username || !this.usuarioForm.rol) {
        return false
      }
      
      // En modo edición, la contraseña es opcional
      if (this.modoEdicion) {
        // Si hay contraseña, validarla
        if (this.usuarioForm.password) {
          if (!this.usuarioForm.confirmPassword) return false
          if (this.usuarioForm.password !== this.usuarioForm.confirmPassword) return false
          if (this.usuarioForm.password.length < 6) return false
        }
        return true
      }
      
      // En modo creación, la contraseña es obligatoria
      if (!this.usuarioForm.password || !this.usuarioForm.confirmPassword) {
        return false
      }
      if (this.usuarioForm.password !== this.usuarioForm.confirmPassword) {
        return false
      }
      if (this.usuarioForm.password.length < 6) {
        return false
      }
      
      return true
    },
    botonEstadoLabel() {
      if (this.selectedIds.length === 0) return 'Desactivar'
      const seleccionados = this.usuarios.filter(u => this.selectedIds.includes(u.id))
      const todosActivos = seleccionados.every(u => u.activo)
      const todosInactivos = seleccionados.every(u => !u.activo)
      if (todosActivos) return 'Desactivar'
      if (todosInactivos) return 'Activar'
      return 'Cambiar Estado'
    },
    botonEstadoIcon() {
      if (this.selectedIds.length === 0) return 'x'
      const seleccionados = this.usuarios.filter(u => this.selectedIds.includes(u.id))
      const todosActivos = seleccionados.every(u => u.activo)
      const todosInactivos = seleccionados.every(u => !u.activo)
      if (todosActivos) return 'x'
      if (todosInactivos) return 'check'
      return 'ban'
    }
  },
  async mounted() {
    console.log('UsuariosRoles mounted')
    await this.cargarDatos()
  },
  methods: {
    getRolLabel(perfilId) {
      if (perfilId === null || perfilId === undefined || perfilId === '') return ''
      const opt = this.rolesOptions.find(r => String(r.value) === String(perfilId))
      return opt ? opt.label : ''
    },

    rolClass(usuario) {
      const label = this.getRolLabel(usuario.perfil_id) || usuario.rol || ''
      return `rol-${String(label).toLowerCase()}`
    },

    async cargarDatos() {
      this.cargando = true
      try {
        // Cargar perfiles (roles) desde la API
        const perfilesResponse = await perfilesService.list()
        const perfilesList = Array.isArray(perfilesResponse) ? perfilesResponse : (perfilesResponse.results || perfilesResponse.data || [])
        
        const roles = perfilesList.map(p => ({
          value: p.PEL_ID || p.id,
          label: p.PEL_DESCRIPCION || p.descripcion || p.nombre || `Perfil ${p.PEL_ID || p.id}`
        }))

        this.rolesOptions = [{ value: '', label: 'Todos los roles' }, ...roles]

        // Cargar usuarios desde la API
        const usuariosResponse = await usuariosService.list()
        const usuariosList = Array.isArray(usuariosResponse) ? usuariosResponse : (usuariosResponse.results || usuariosResponse.data || [])
        
        this.usuarios = usuariosList.map(u => ({
          id: u.USU_ID || u.id,
          nombre: u.USU_USERNAME || u.nombre || u.username || '',
          username: u.USU_USERNAME || u.username || '',
          perfil_id: u.PEL_ID || u.perfil_id || u.perfil || null,
          rol: this.getRolLabelById(u.PEL_ID || u.perfil_id || u.perfil, roles),
          activo: u.USU_VIGENTE !== undefined ? u.USU_VIGENTE : (u.vigente !== undefined ? u.vigente : true),
          foto: u.USU_RUTA_FOTO || u.foto || null,
          password_hash: u.USU_PASSWORD || u.password || null
        }))

        // Inicializar permisos por usuario (vacíos por ahora)
        this.usuarios.forEach(u => {
          this.userPerms[u.id] = null
        })

        this.usuariosFiltrados = [...this.usuarios]
      } catch (error) {
        console.error('Error al cargar datos desde la API:', error)
        this.mostrarNotificacion('Error al cargar los datos: ' + (error.message || 'Error desconocido'), 'error')
        // En caso de error, inicializar vacío en lugar de usar mocks
        this.usuarios = []
        this.usuariosFiltrados = []
        this.rolesOptions = [{ value: '', label: 'Todos los roles' }]
      } finally {
        this.cargando = false
      }
    },
    
    getRolLabelById(perfilId, rolesList) {
      if (!perfilId) return ''
      const rol = rolesList.find(r => r.value === perfilId)
      return rol ? rol.label : ''
    },
    
    filtrarUsuarios() {
      let resultado = [...this.usuarios]
      
      // Filtrar por búsqueda
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        resultado = resultado.filter(u => 
          u.nombre.toLowerCase().includes(query) ||
          u.username.toLowerCase().includes(query)
        )
      }
      
      // Filtrar por rol (comparar por perfil_id que es el value en rolesOptions)
      if (this.filtroRol) {
        resultado = resultado.filter(u => String(u.perfil_id || '') === String(this.filtroRol))
      }
      
      // Filtrar por estado
      if (this.filtroEstado === 'activo') {
        resultado = resultado.filter(u => u.activo)
      } else if (this.filtroEstado === 'inactivo') {
        resultado = resultado.filter(u => !u.activo)
      }
      
      this.usuariosFiltrados = resultado
    },
    
    limpiarFiltros() {
      this.searchQuery = ''
      this.filtroRol = ''
      this.filtroEstado = ''
      this.filtrarUsuarios()
    },
    
    getFormularioVacio() {
      return {
        id: null,
        username: '',
        rol: '',
        password: '',
        confirmPassword: '',
        activo: true,
        foto: null,
        fotoPreview: null
      }
    },
    
    handleFileChange(event) {
      const file = event.target.files[0]
      if (!file) return

      // Validar tamaño (2MB)
      if (file.size > 2 * 1024 * 1024) {
        this.mostrarNotificacion('La imagen no debe superar los 2MB', 'warning')
        return
      }

      // Validar tipo
      if (!file.type.startsWith('image/')) {
        this.mostrarNotificacion('Solo se permiten archivos de imagen', 'warning')
        return
      }

      // Crear vista previa
      const reader = new FileReader()
      reader.onload = (e) => {
        this.usuarioForm.fotoPreview = e.target.result
        this.usuarioForm.foto = file
      }
      reader.readAsDataURL(file)
    },

    eliminarFoto() {
      this.usuarioForm.foto = null
      this.usuarioForm.fotoPreview = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },

    triggerFotoSeleccion() {
      if (this.procesando) return;
      const input = this.$refs.fileInput;
      if (input) input.click();
    },
    
    abrirModalCrear() {
      this.modoEdicion = false
      this.usuarioForm = this.getFormularioVacio()
      this.modalVisible = true
    },
    
    async abrirModalEditar(usuario) {
      this.modoEdicion = true
      this.usuarioForm = {
        id: usuario.id,
        username: usuario.username,
        rol: usuario.perfil_id,
        password: '',
        confirmPassword: '',
        activo: usuario.activo,
        foto: null,
        fotoPreview: usuario.foto || null
      }
      this.modalVisible = true
    },
    
    cerrarModal() {
      this.modalVisible = false
      this.usuarioForm = this.getFormularioVacio()
    },
    
    async guardarUsuario() {
      if (!this.formularioValido) {
        this.mostrarNotificacion('Por favor complete todos los campos requeridos', 'warning')
        return
      }
      
      this.procesando = true
      try {
        const roleOpt = this.rolesOptions.find(r => String(r.value) === String(this.usuarioForm.rol))
        
        // Preparar datos para la API
        const usuarioData = {
          USU_USERNAME: this.usuarioForm.username,
          PEL_ID: this.usuarioForm.rol,
          USU_VIGENTE: this.usuarioForm.activo,
          // Si no hay foto, enviar una URL por defecto (el backend requiere que no sea vacío)
          USU_RUTA_FOTO: this.usuarioForm.fotoPreview || this.defaultFoto
        }

        // Solo incluir password si hay uno nuevo
        if (this.usuarioForm.password) {
          usuarioData.USU_PASSWORD = this.usuarioForm.password
        }

        if (this.modoEdicion) {
          // Actualizar usuario existente
          console.log('Editando usuario ID:', this.usuarioForm.id, 'con datos:', usuarioData)
          const usuarioActualizado = await usuariosService.partialUpdate(this.usuarioForm.id, usuarioData)
          
          // Actualizar en el array local
          const idx = this.usuarios.findIndex(u => u.id === this.usuarioForm.id)
          if (idx !== -1) {
            this.usuarios[idx] = {
              id: usuarioActualizado.USU_ID || usuarioActualizado.id || this.usuarioForm.id,
              nombre: usuarioActualizado.USU_USERNAME || this.usuarioForm.username,
              username: usuarioActualizado.USU_USERNAME || this.usuarioForm.username,
              perfil_id: usuarioActualizado.PEL_ID || this.usuarioForm.rol,
              rol: roleOpt ? roleOpt.label : '',
              activo: usuarioActualizado.USU_VIGENTE !== undefined ? usuarioActualizado.USU_VIGENTE : this.usuarioForm.activo,
              foto: usuarioActualizado.USU_RUTA_FOTO || this.usuarioForm.fotoPreview || this.defaultFoto
            }
          }
          
          this.mostrarNotificacion('Usuario actualizado exitosamente', 'success')
        } else {
          // Crear nuevo usuario
          const nuevoUsuario = await usuariosService.create(usuarioData)
          
          // Agregar al array local
          this.usuarios.push({
            id: nuevoUsuario.USU_ID || nuevoUsuario.id,
            nombre: nuevoUsuario.USU_USERNAME || this.usuarioForm.username,
            username: nuevoUsuario.USU_USERNAME || this.usuarioForm.username,
            perfil_id: nuevoUsuario.PEL_ID || this.usuarioForm.rol,
            rol: roleOpt ? roleOpt.label : '',
            activo: nuevoUsuario.USU_VIGENTE !== undefined ? nuevoUsuario.USU_VIGENTE : true,
            foto: nuevoUsuario.USU_RUTA_FOTO || this.usuarioForm.fotoPreview || this.defaultFoto
          })
          
          this.mostrarNotificacion('Usuario creado exitosamente', 'success')
        }
        
        this.usuariosFiltrados = [...this.usuarios]
        this.cerrarModal()
      } catch (error) {
        console.error('Error al guardar usuario:', error)
        this.mostrarNotificacion(
          error.message || 'Error al guardar el usuario',
          'error'
        )
      } finally {
        this.procesando = false
      }
    },
    
    confirmarCambioEstado(usuario, nuevoEstado) {
      this.tituloConfirmacion = nuevoEstado ? 'Activar Usuario' : 'Desactivar Usuario'
      this.mensajeConfirmacion = `¿Está seguro que desea ${nuevoEstado ? 'activar' : 'desactivar'} al usuario "${usuario.nombre}"?`
      this.accionConfirmacion = () => this.cambiarEstado(usuario, nuevoEstado)
      this.modalConfirmacionVisible = true
    },
    
    async cambiarEstado(usuario, nuevoEstado) {
      this.procesando = true
      try {
        // Actualizar en el backend
        await usuariosService.partialUpdate(usuario.id, {
          USU_VIGENTE: nuevoEstado
        })
        
        // Actualizar en memoria
        const idx = this.usuarios.findIndex(u => u.id === usuario.id)
        if (idx !== -1) {
          this.usuarios[idx].activo = nuevoEstado
          this.mostrarNotificacion(`Usuario ${nuevoEstado ? 'activado' : 'desactivado'} exitosamente`, 'success')
          this.usuariosFiltrados = [...this.usuarios]
        }
        this.modalConfirmacionVisible = false
      } catch (error) {
        console.error('Error al cambiar estado:', error)
        this.mostrarNotificacion('Error al cambiar el estado del usuario: ' + (error.message || ''), 'error')
      } finally {
        this.procesando = false
      }
    },
    
    // Nota: la eliminación de usuarios se ha deshabilitado. Solo está permitido desactivar/activar usuarios.
    
    ejecutarAccion() {
      if (this.accionConfirmacion) {
        this.accionConfirmacion()
      }
    },
    
    cancelarAccion() {
      this.modalConfirmacionVisible = false
      this.accionConfirmacion = null
    },
    
    mostrarNotificacion(mensaje, tipo = 'info') {
      this.notificacion = {
        visible: true,
        mensaje,
        tipo
      }
      
      setTimeout(() => {
        this.cerrarNotificacion()
      }, 4000)
    },
    
    cerrarNotificacion() {
      this.notificacion.visible = false
    },

    // Métodos de selección
    isSelected(id) {
      return this.selectedIds.includes(id)
    },

    toggleRowSelection(usuario) {
      const id = usuario.id
      const idx = this.selectedIds.indexOf(id)
      if (idx === -1) {
        this.selectedIds.push(id)
      } else {
        this.selectedIds.splice(idx, 1)
      }
    },

    clearSelection() {
      this.selectedIds = []
    },

    editarSeleccionado() {
      if (this.selectedIds.length !== 1) return
      const usuario = this.usuarios.find(u => u.id === this.selectedIds[0])
      if (usuario) {
        this.abrirModalEditar(usuario)
      }
    },

    toggleEstadoSeleccionados() {
      if (this.selectedIds.length === 0) return
      const usuariosSeleccionados = this.usuarios.filter(u => this.selectedIds.includes(u.id))

      // Si solo hay un usuario seleccionado, usar la confirmación individual para un mensaje más claro
      if (usuariosSeleccionados.length === 1) {
        const usuario = usuariosSeleccionados[0]
        const nuevoEstado = !usuario.activo
        this.confirmarCambioEstado(usuario, nuevoEstado)
        return
      }

      const todosActivos = usuariosSeleccionados.every(u => u.activo)
      const todosInactivos = usuariosSeleccionados.every(u => !u.activo)

      if (todosActivos) {
        // Preparar desactivación masiva
        this.tituloConfirmacion = 'Desactivar Usuarios'
        this.mensajeConfirmacion = `¿Está seguro que desea desactivar ${usuariosSeleccionados.length} usuario(s)?`
        this.accionConfirmacion = () => this.ejecutarCambioEstadoMasivo(false)
      } else if (todosInactivos) {
        // Preparar activación masiva
        this.tituloConfirmacion = 'Activar Usuarios'
        this.mensajeConfirmacion = `¿Está seguro que desea activar ${usuariosSeleccionados.length} usuario(s)?`
        this.accionConfirmacion = () => this.ejecutarCambioEstadoMasivo(true)
      } else {
        // Mixtos: alternar cada uno (activos->inactivo, inactivos->activo)
        this.tituloConfirmacion = 'Cambiar Estado de Usuarios'
        this.mensajeConfirmacion = `¿Desea alternar el estado de ${usuariosSeleccionados.length} usuario(s)? (Activos se desactivarán y viceversa)`
        this.accionConfirmacion = () => this.ejecutarAlternanciaEstadoMasivo()
      }
      this.modalConfirmacionVisible = true
    },

    async ejecutarCambioEstadoMasivo(nuevoEstado) {
      this.procesando = true
      try {
        let modificados = 0
        // Actualizar en el backend
        const promesas = this.selectedIds.map(async (id) => {
          try {
            await usuariosService.partialUpdate(id, { USU_VIGENTE: nuevoEstado })
            return id
          } catch (err) {
            console.error(`Error al actualizar usuario ${id}:`, err)
            return null
          }
        })
        
        const resultados = await Promise.all(promesas)
        
        // Actualizar en memoria solo los que se actualizaron exitosamente
        this.usuarios.forEach(u => {
          if (resultados.includes(u.id)) {
            if (u.activo !== nuevoEstado) {
              u.activo = nuevoEstado
              modificados++
            }
          }
        })
        
        this.usuariosFiltrados = [...this.usuarios]
        this.mostrarNotificacion(`${modificados} usuario(s) ${nuevoEstado ? 'activado(s)' : 'desactivado(s)'} exitosamente`, 'success')
        this.clearSelection()
        this.modalConfirmacionVisible = false
      } catch (error) {
        console.error('Error al cambiar estado masivo:', error)
        this.mostrarNotificacion('Error al cambiar estado masivo: ' + (error.message || ''), 'error')
      } finally {
        this.procesando = false
      }
    },

    async ejecutarAlternanciaEstadoMasivo() {
      this.procesando = true
      try {
        let modificados = 0
        // Actualizar en el backend
        const promesas = this.usuarios
          .filter(u => this.selectedIds.includes(u.id))
          .map(async (u) => {
            try {
              const nuevoEstado = !u.activo
              await usuariosService.partialUpdate(u.id, { USU_VIGENTE: nuevoEstado })
              return { id: u.id, nuevoEstado }
            } catch (err) {
              console.error(`Error al actualizar usuario ${u.id}:`, err)
              return null
            }
          })
        
        const resultados = await Promise.all(promesas)
        
        // Actualizar en memoria solo los que se actualizaron exitosamente
        this.usuarios.forEach(u => {
          const resultado = resultados.find(r => r && r.id === u.id)
          if (resultado) {
            u.activo = resultado.nuevoEstado
            modificados++
          }
        })
        
        this.usuariosFiltrados = [...this.usuarios]
        this.mostrarNotificacion(`${modificados} usuario(s) con estado alternado exitosamente`, 'success')
        this.clearSelection()
        this.modalConfirmacionVisible = false
      } catch (error) {
        console.error('Error al alternar estado masivo:', error)
        this.mostrarNotificacion('Error al alternar estado masivo: ' + (error.message || ''), 'error')
      } finally {
        this.procesando = false
      }
    }
  }
}
</script>

<style scoped>
.usuarios-roles {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
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

.page-description {
  margin: 0;
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: 400;
}

/* Filtros */
.filtros {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filtros .filtro-item {
  width: 100%;
}

.filtros :deep(.input-base),
.filtros :deep(.base-select),
.filtros :deep(.base-button) {
  margin: 0;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  gap: 0.75rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Tabla */
.table-container {
  margin-bottom: 1rem;
}

.table-header-bar {
  background: white;
  padding: 0.85rem 1rem;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e0e0e0;
}

.table-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e3a8a;
  position: relative;
  padding-left: 12px;
}

.table-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: #1e3a8a;
  border-radius: 2px;
}

.table-actions {
  display: flex;
  gap: 0.6rem;
}

.table-actions :deep(button) {
  min-width: 110px;
  font-weight: 600;
  padding: 0.5rem 0.85rem;
}

.table-wrapper {
  background: white;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-table thead {
  background: #3d4f5f;
  color: white;
}

.usuarios-table th {
  padding: 0.75rem 0.85rem;
  text-align: left;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

.usuarios-table tbody tr {
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.2s;
  cursor: pointer;
  user-select: none;
}

.usuarios-table tbody tr:hover {
  background-color: #f8f9fa;
}

.usuarios-table tbody tr.row-selected {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.usuarios-table tbody tr.row-selected:hover {
  background-color: #bbdefb;
}

.usuarios-table tbody tr.usuario-inactivo {
  opacity: 0.6;
}

.usuarios-table td {
  padding: 0.75rem 0.85rem;
  vertical-align: middle;
}

/* row-actions removed: use header buttons for actions */

/* User Avatar in Table */
.foto-cell {
  width: 70px;
  padding: 0.6rem !important;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-image {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.avatar-image:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.avatar-placeholder {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.avatar-placeholder:hover {
  transform: scale(1.1);
}

/* Badges */
.badges-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
}

.badge {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  border: 1px solid transparent;
}

.rol-badge {
  text-transform: capitalize;
}

.rol-administrador {
  background-color: #e74c3c;
  color: white;
}

.rol-coordinador {
  background-color: #3498db;
  color: white;
}

.rol-dirigente {
  background-color: #9b59b6;
  color: white;
}

.rol-apoderado {
  background-color: #f39c12;
  color: white;
}

.rol-participante {
  background-color: #95a5a6;
  color: white;
}

.badge-activo {
  background-color: #27ae60;
  color: white;
}

.estado-activo {
  background-color: #27ae60;
  color: white;
}

.estado-inactivo {
  background-color: #95a5a6;
  color: white;
}

/* Empty state */
.empty-row td {
  padding: 2rem 1rem;
}

.empty-state {
  text-align: center;
  color: #7f8c8d;
}

.empty-state p {
  margin-bottom: 0.85rem;
  font-size: 1rem;
}

/* Modal */
.modal-usuario {
  padding: 0;
  width: 100%;
  max-width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  /* Allow modal content to scroll when it grows taller than the viewport */
  max-height: 92vh;
  overflow-y: auto;
  /* keep rounded corners consistent with header */
  border-radius: 16px;
}

.modal-header {
  margin-bottom: 0;
  padding: 1.5rem 2rem 1rem 2rem;
  background: #ffffff;
  /* clip header so curved corners are clean */
  border-radius: 16px 16px 0 0;
  /* mantener espacio estándar a la derecha (alineado con BaseModal) */
  padding-right: 3rem;
  flex-shrink: 0;
  position: sticky; /* keep header visible while scrolling */
  top: 0;
  z-index: 30;
  /* subtle shadow to separate header from body */
  box-shadow: 0 8px 24px rgba(16,24,40,0.06);
  border-bottom: 1px solid rgba(15,23,42,0.04);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #0f172a;
  font-weight: 700;
}

/* If the modal close button or other controls sit on top of the header edge,
   ensure they don't create a visible misaligned corner. This targets
   potential close-button wrappers from BaseModal but keeps rules low-impact. */
:deep(.base-modal__close) {
  /* keep the close button inside the header area and visually consistent */
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12);
  /* ensure it sits above the header shadow */
  z-index: 40;
}

/* Target actual close button class used by BaseModal */
:deep(.close-btn) {
  background: #ffffff;
  color: #0f172a;
  border-radius: 50%;
  box-shadow: 0 6px 18px rgba(16,24,40,0.12);
  z-index: 60; /* above header */
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

:deep(.close-btn:hover) {
  background: #e74c3c;
  color: #fff;
  transform: rotate(90deg) scale(1.05);
}

/* Nota: la posición del botón cerrar la controla `BaseModal.vue`. Evitamos duplicar reglas aquí */

/* Slimmer modal scrollbar (WebKit) + cross-browser hint */
.modal-usuario,
.modal-body-wrapper,
:deep(.modal-body-scroll),
:deep(.modal-body-content) {
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: rgba(15,23,42,0.18) transparent; /* Firefox */
}

.modal-usuario::-webkit-scrollbar,
.modal-body-wrapper::-webkit-scrollbar,
:deep(.modal-body-scroll)::-webkit-scrollbar,
:deep(.modal-body-content)::-webkit-scrollbar {
  width: 6px;
}

.modal-usuario::-webkit-scrollbar-track,
.modal-body-wrapper::-webkit-scrollbar-track,
:deep(.modal-body-scroll)::-webkit-scrollbar-track,
:deep(.modal-body-content)::-webkit-scrollbar-track {
  background: transparent;
}

.modal-usuario::-webkit-scrollbar-thumb,
.modal-body-wrapper::-webkit-scrollbar-thumb,
:deep(.modal-body-scroll)::-webkit-scrollbar-thumb,
:deep(.modal-body-content)::-webkit-scrollbar-thumb {
  background: rgba(15,23,42,0.12);
  border-radius: 999px;
  border: 1px solid transparent; /* give it a little breathing space */
}

.usuario-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
  flex: 1;
  overflow: visible;
}

/* Form Sections */
.form-section {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid #e0e0e0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #2563eb;
}

.form-row {
  display: flex;
  gap: 0.85rem;
  align-items: flex-end;
}

.form-row-triple {
  display: grid;
  grid-template-columns: 140px 1fr 1fr; /* foto fija + 2 columnas iguales */
  gap: 1rem;
  align-items: flex-end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group.flex-1 {
  flex: 1;
}

.form-group.photo-group-inline {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.85rem;
}

.form-group .required {
  color: #e74c3c;
}

.form-hint-compact {
  font-size: 0.7rem;
  color: #7f8c8d;
  margin-top: 0.2rem;
}

/* Photo Upload Inline */
.photo-upload-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e6e9ee;
  cursor: pointer;
  transition: all 0.18s ease;
  width: 112px; /* fixed compact box */
  min-width: 112px;
  position: relative;
}

.photo-upload-inline:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.15);
  transform: translateY(-2px);
}

.photo-preview-inline {
  flex-shrink: 0;
  position: relative;
  width: 96px;
  height: 96px;
}

.preview-image-inline {
  width: 96px;
  height: 96px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid #2b82d6;
  box-shadow: 0 6px 18px rgba(43,130,214,0.12);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.photo-upload-inline:hover .preview-image-inline {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.3);
}

.preview-placeholder-inline {
  width: 96px;
  height: 96px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.photo-upload-inline:hover .preview-placeholder-inline {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.photo-hint {
  font-size: 0.72rem;
  color: #6b7280;
  font-weight: 500;
  text-align: center;
  margin-top: 0.25rem;
}

/* Reduce overall vertical rhythm for a tighter look */
.usuario-form { gap: 1.25rem; padding: 1.25rem; }

/* Align rows vertically center so avatar and inputs line up */
.form-row, .form-row-triple { align-items: center; }

/* Slightly more compact section spacing */
.form-section { padding: 1rem; }

/* Make labels slightly smaller and consistent */
.form-group label { font-size: 0.86rem; margin-bottom: 0.3rem; }

/* Ensure the avatar column doesn't push layout on small screens */
.form-row-triple { grid-template-columns: 112px 1fr 1fr; gap: 1.5rem; }

/* Hide helper text next to the avatar to keep the photo area clean */
.photo-upload-inline .photo-hint,
.photo-upload-inline .form-hint-compact {
  display: none;
}

/* Add a little breathing room to the left of the content when avatar is present */
.photo-upload-inline { margin-right: 0.75rem; }

/* Inputs/selects full width and consistent */
.form-group.flex-1 :deep(.base-field),
.form-group.flex-1 :deep(.base-select__element) {
  height: 44px; padding: 8px 12px; border-radius: 8px;
}

/* Make form inputs look more squared, uniform and aligned */
.usuario-form :deep(.base-field) {
  border-radius: 8px;
  padding: 10px 12px;
  min-height: 44px;
  background: #ffffff;
  border: 1px solid #d1d5db;
}

.usuario-form :deep(.base-label) {
  font-weight: 700;
  color: #1f2937;
}

/* Ensure select components match input sizing */
.usuario-form :deep(.base-select),
.usuario-form :deep(select) {
  min-height: 44px;
  border-radius: 8px;
}

/* Make the photo box and adjacent fields align neatly */
.form-row-triple {
  grid-template-columns: 100px 1fr 1fr; /* slightly smaller photo column for cleaner alignment */
}

/* Tighter, more square labels/inputs spacing */
.form-group { gap: 0.5rem; }

.form-section { padding: 1.25rem; }

.section-title { padding-bottom: 0.4rem; }

.photo-upload-inline:hover .photo-hint {
  color: #3498db;
}

.remove-foto-btn {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 26px;
  height: 26px;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: #fff;
  border: 2px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.4);
  transition: all 0.2s ease;
  z-index: 10;
}

.remove-foto-btn:hover {
  background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.6);
}

.remove-foto-btn:active {
  transform: scale(0.95) rotate(90deg);
}

/* Forzar mismos anchos/altos de controles en columnas flex-1 */
/* Unificar alto/estilo de InputBase (input) y BaseSelect (select) */
.form-group.flex-1 :deep(.base-field),
.form-group.flex-1 :deep(.base-select__element) {
  height: 42px;
  line-height: 42px;
  padding: 0 12px;
  font-size: 14px;
  border-width: 1px;
  border-radius: 6px;
  box-sizing: border-box;
  width: 100%;
}

/* Ajuste específico del select: más espacio para el ícono de despliegue */
.form-group.flex-1 :deep(.base-select__element) {
  padding-right: 2rem;
}

/* Error Message */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c33;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 0.85rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e0e0e0;
}

.form-actions :deep(button) {
  min-width: 130px;
}

/* Estado badge in form */
.estado-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.badge-activo {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.estado-inactivo {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

/* Switch styling in form */
:deep(.switch-container) {
  pointer-events: auto;
}

/* Permisos Container - Estilo Discord */
.permisos-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-height: 600px;
  overflow-y: auto;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.aplicacion-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.aplicacion-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #3498db;
}

.aplicacion-icon {
  color: #3498db;
}

.aplicacion-nombre {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: #2c3e50;
}

.permisos-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

/* Photo upload - Legacy styles for backward compatibility */
.photo-upload-container {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #cbd5e0;
}

.photo-preview {
  flex-shrink: 0;
}

.preview-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #3498db;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.preview-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #95a5a6;
  gap: 0.5rem;
}

.preview-placeholder span {
  font-size: 0.85rem;
  font-weight: 500;
}

.photo-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.photo-actions :deep(button) {
  width: 100%;
  justify-content: center;
}

/* Modal confirmación */
.modal-confirmacion {
  padding: 1.5rem;
  text-align: center;
}

.modal-confirmacion h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.modal-confirmacion p {
  margin-bottom: 1.5rem;
  color: #7f8c8d;
  font-size: 1.05rem;
}

/* Responsive */
@media (max-width: 768px) {
  .usuarios-roles {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filtros {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .table-header-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .table-actions {
    width: 100%;
    flex-direction: column;
  }

  .table-actions :deep(button) {
    width: 100%;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .usuarios-table {
    display: block;
  }

  .usuarios-table thead {
    display: none;
  }

  .usuarios-table tbody,
  .usuarios-table tr,
  .usuarios-table td {
    display: block;
    width: 100%;
  }

  .usuarios-table tr {
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
  }

  .usuarios-table td {
    padding: 0.5rem 0;
    border: none;
    text-align: left;
  }

  .usuarios-table td::before {
    content: attr(data-label);
    font-weight: 600;
    display: inline-block;
    width: 120px;
    color: #34495e;
  }

  .foto-cell::before {
    display: none;
  }

  .foto-cell {
    text-align: center;
    padding: 0.75rem 0 !important;
  }

  /* Modal responsive */
  .modal-usuario {
    padding: 1rem;
    width: 95vw;
    max-height: 85vh;
  }

  .modal-header h3 {
    font-size: 1.25rem;
  }

  .form-row {
    flex-direction: column;
  }

  .form-group.photo-group {
    min-width: 100%;
  }

  .photo-upload-compact {
    flex-direction: column;
    text-align: center;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions :deep(button) {
    width: 100%;
  }
}
</style>