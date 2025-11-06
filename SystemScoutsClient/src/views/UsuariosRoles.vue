<template>
  <div class="usuarios-roles">
    <!-- Encabezado de la sección -->
    <header class="page-header">
      <h2>Gestión de Usuarios</h2>
      <BaseButton 
        class="btn-crear-usuario"
        variant="primary" 
        size="lg"
        @click="abrirModalCrear"
      >
        + Crear Usuario
      </BaseButton>
    </header>

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <InputBase 
        v-model="searchQuery" 
        placeholder="Buscar por nombre o usuario..." 
        class="filtro-item"
        @input="filtrarUsuarios"
      />
      <BaseSelect 
        v-model="filtroRol" 
        :options="rolesOptions" 
        placeholder="Todos los perfiles"
        class="filtro-item"
        @change="filtrarUsuarios"
      />
      <BaseSelect 
        v-model="filtroEstado" 
        :options="estadoOptions" 
        placeholder="Todos los estados"
        class="filtro-item"
        @change="filtrarUsuarios"
      />
      <BaseButton 
        variant="primary" 
        @click="filtrarUsuarios"
        class="filtro-item"
      >
        <AppIcons name="search" :size="18" />
        Buscar
      </BaseButton>
    </div>

    <!-- Indicador de carga -->
    <div v-if="cargando" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando usuarios...</p>
    </div>

    <!-- Card estilo Correos -->
    <section class="correos-card usuarios-card">
      <div class="correos-card-header">
        <span class="correos-card-title blue-bar">Lista de Usuarios</span>
        <div class="correos-card-actions">
          <BaseButton variant="primary" @click="cambiarEstadoMasivo(false)" :disabled="selectedCount === 0" title="Desactivar todos los seleccionados">
            <AppIcons name="alert" :size="16" /> Desactivar
          </BaseButton>
          <BaseButton variant="primary" @click="cambiarEstadoMasivo(true)" :disabled="selectedCount === 0" title="Activar todos los seleccionados">
            <AppIcons name="check" :size="16" /> Activar
          </BaseButton>
          <BaseButton variant="primary" @click="accionEditarSelected" :disabled="!canEditOne" title="Editar usuario seleccionado">
            <AppIcons name="edit" :size="16" /> Editar
          </BaseButton>
          <BaseButton variant="primary" @click="abrirModalCrear" title="Crear nuevo usuario">
            <AppIcons name="add" :size="16" /> Nuevo
          </BaseButton>
        </div>
      </div>
      <div class="usuarios-seleccion-resumen">
        <span>Seleccionados: <strong>{{ selectedCount }}</strong></span>
        <template v-if="canEditOne && selectedUsuario">
          <span> | Usuario: <strong>{{ selectedUsuario.username }}</strong></span>
          <span class="badge-mini" :class="selectedUsuario.activo ? 'mini-ok' : 'mini-off'">{{ selectedUsuario.activo ? 'Activo' : 'Inactivo' }}</span>
        </template>
      </div>

  <!-- Tabla de usuarios -->
  <div v-if="!cargando" class="table-wrapper usuarios-table-wrapper">
      <table class="usuarios-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>PERFIL</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="usuario in usuariosFiltrados" 
            :key="usuario.id"
            :class="{ 'usuario-inactivo': !usuario.activo, 'row-selected': isSelected(usuario.id) }"
            @click="toggleRowSelection(usuario)"
          >
            <td data-label="Usuario">
              <div class="user-cell">
                <img
                  class="avatar"
                  :src="usuario.foto || avatarDataUrl(usuario.nombre || usuario.username)"
                  :alt="`Foto de ${usuario.username}`"
                />
                <span class="username">{{ usuario.username }}</span>
              </div>
            </td>
            <td data-label="Perfil" :class="{ 'col-perfil': true }">
              <span class="rol-badge" :class="rolClass(usuario)">
                {{ getRolLabel(usuario.perfil_id) || usuario.rol }}
              </span>
            </td>
            <td data-label="Estado">
              <span :class="['estado-badge', usuario.activo ? 'estado-activo' : 'estado-inactivo']">
                {{ usuario.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
          </tr>
          <tr v-if="usuariosFiltrados.length === 0" class="empty-row">
            <td colspan="3">
              <div class="empty-state">
                <p>No se encontraron usuarios</p>
                <BaseButton variant="primary" @click="limpiarFiltros">Mostrar todos</BaseButton>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
  </div>
  </section>

    <BaseModal v-model="modalVisible" @close="cerrarModal">
      <template #default>
        <div class="modal-usuario">
          <header class="modal-header">
            <h3>{{ modoEdicion ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}</h3>
          </header>

          <form @submit.prevent="guardarUsuario" class="usuario-form">
            <div class="form-group">
              <label for="username">Nombre de Usuario <span class="required">*</span></label>
              <InputBase 
                id="username"
                v-model="usuarioForm.username" 
                placeholder="Ej: jperez"
                required
              />
              <small class="form-hint">Este nombre se mostrará en la tabla</small>
            </div>

            <div class="form-group">
              <label for="rol">Perfil <span class="required">*</span></label>
              <BaseSelect 
                id="rol"
                v-model="usuarioForm.rol" 
                :options="rolesOptions"
                placeholder="Seleccionar perfil"
                required
                :disabled="procesando"
                @change="cargarPermisosDelRol"
              />
            </div>

            <!-- Foto de Usuario (solo se muestra siempre, pero requerida por pedido para edición) -->
            <div class="form-group">
              <label for="foto">Foto de Usuario</label>
              <input id="foto" class="file-input" type="file" accept="image/*" @change="onFotoChange" :disabled="procesando" />
              <div v-if="usuarioForm.foto" class="avatar-preview-wrapper">
                <img :src="usuarioForm.foto" alt="Preview Foto" class="avatar-preview" />
              </div>
              <small class="form-hint">Opcional. Si no se selecciona, se mostrarán iniciales.</small>
            </div>

            <!-- Permisos personalizados por aplicación -->
            <!-- Permisos ocultos en modo edición segun requerimiento -->
            <div class="form-group" v-if="(!modoEdicion && usuarioForm.rol) && aplicaciones.length > 0">
              <label>Permisos del Usuario</label>
              <p class="form-hint">Configure los permisos específicos para este usuario en cada módulo del sistema</p>
              
              <div class="permisos-container">
                <div 
                  v-for="aplicacion in aplicaciones" 
                  :key="aplicacion.APL_ID || aplicacion.id"
                  class="aplicacion-section"
                >
                  <div class="aplicacion-header">
                    <AppIcons name="book" :size="20" class="aplicacion-icon" />
                    <h4 class="aplicacion-nombre">{{ aplicacion.APL_DESCRIPCION || aplicacion.nombre }}</h4>
                  </div>
                  
                  <div class="permisos-list" v-if="usuarioForm.permisos[aplicacion.APL_ID || aplicacion.id]">
                    <PermisosToggle
                      v-model="usuarioForm.permisos[aplicacion.APL_ID || aplicacion.id].consultar"
                      label="Ver / Consultar"
                      description="Permite visualizar la información y listados del módulo"
                      icon-name="view"
                      :disabled="procesando"
                    />
                    <PermisosToggle
                      v-model="usuarioForm.permisos[aplicacion.APL_ID || aplicacion.id].ingresar"
                      label="Crear / Ingresar"
                      description="Permite agregar nuevos registros al sistema"
                      icon-name="add"
                      :disabled="procesando"
                    />
                    <PermisosToggle
                      v-model="usuarioForm.permisos[aplicacion.APL_ID || aplicacion.id].modificar"
                      label="Modificar / Editar"
                      description="Permite editar y actualizar registros existentes"
                      icon-name="modify"
                      :disabled="procesando"
                    />
                    <PermisosToggle
                      v-model="usuarioForm.permisos[aplicacion.APL_ID || aplicacion.id].eliminar"
                      label="Eliminar / Borrar"
                      description="Permite eliminar registros del sistema"
                      icon-name="delete"
                      :disabled="procesando"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Gestión de contraseña -->
            <!-- Modo crear: pedir contraseña -->
            <div class="form-group" v-if="!modoEdicion">
              <label for="password">Contraseña <span class="required">*</span></label>
              <InputBase
                id="password"
                v-model="usuarioForm.password"
                type="password"
                placeholder="Ingrese contraseña (mínimo 6 caracteres)"
                :required="!modoEdicion"
                :disabled="procesando"
              />
              <small class="form-hint">La contraseña debe tener al menos 6 caracteres</small>
            </div>

            <div class="form-group" v-if="!modoEdicion">
              <label for="confirmPassword">Confirmar Contraseña <span class="required">*</span></label>
              <InputBase
                id="confirmPassword"
                v-model="usuarioForm.confirmPassword"
                type="password"
                placeholder="Confirme contraseña"
                :required="!modoEdicion"
                :disabled="procesando"
              />
              <small class="form-hint" v-if="usuarioForm.password && usuarioForm.confirmPassword && usuarioForm.password !== usuarioForm.confirmPassword" style="color: #e74c3c;">
                Las contraseñas no coinciden
              </small>
            </div>

            <!-- Modo edición: mostrar contraseña enmascarada y opción para cambiar -->
            <div class="form-group" v-if="modoEdicion">
              <label>Contraseña</label>
              <div v-if="!changePassword" class="password-masked-row">
                <span class="password-masked" title="Contraseña protegida">••••••••</span>
                <BaseButton size="sm" variant="primary" type="button" @click="activarCambioPassword" :disabled="procesando">Cambiar</BaseButton>
              </div>
              <div v-else class="password-change-fields">
                <InputBase
                  id="newPassword"
                  v-model="usuarioForm.password"
                  type="password"
                  placeholder="Nueva contraseña"
                  :disabled="procesando"
                />
                <InputBase
                  id="newPassword2"
                  v-model="usuarioForm.confirmPassword"
                  type="password"
                  placeholder="Confirmar nueva contraseña"
                  :disabled="procesando"
                />
                <div class="password-actions-inline">
                  <BaseButton size="sm" variant="primary" type="button" @click="confirmarNuevoPassword" :disabled="procesando || !passwordTemporalValido">Aplicar</BaseButton>
                  <BaseButton size="sm" variant="primary" type="button" @click="cancelarCambioPassword" :disabled="procesando">Cancelar</BaseButton>
                </div>
                <small class="form-hint" v-if="usuarioForm.password && usuarioForm.password.length < 6" style="color:#e74c3c;">Mínimo 6 caracteres</small>
                <small class="form-hint" v-if="usuarioForm.password && usuarioForm.confirmPassword && usuarioForm.password !== usuarioForm.confirmPassword" style="color:#e74c3c;">Las contraseñas no coinciden</small>
              </div>
            </div>

            

            <div class="form-actions">
              <BaseButton 
                type="button" 
                variant="primary" 
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
                {{ procesando ? 'Guardando...' : (modoEdicion ? 'Actualizar' : 'Crear Usuario') }}
              </BaseButton>
            </div>
          </form>
        </div>
      </template>
    </BaseModal>

    <!-- Modal de confirmación para eliminar -->
    <BaseModal v-model="modalConfirmacionVisible" @close="cancelarAccion">
      <template #default>
        <div class="modal-confirmacion">
          <h3>{{ tituloConfirmacion }}</h3>
          <p>{{ mensajeConfirmacion }}</p>
          <div class="form-actions">
            <BaseButton 
              variant="primary" 
              @click="cancelarAccion"
              :disabled="procesando"
            >
              Cancelar
            </BaseButton>
            <BaseButton 
              variant="primary" 
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
// Modo UI-only: eliminadas dependencias a la API. Los datos se cargan en memoria (mock).
import { useRouter } from 'vue-router'
import BaseButton from '../components/Reutilizables/BaseButton.vue'
import BaseModal from '../components/Reutilizables/BaseModal.vue'
import BaseSelect from '../components/Reutilizables/BaseSelect.vue'
import BaseCheckBox from '../components/Reutilizables/BaseCheckBox.vue'
import InputBase from '../components/Reutilizables/InputBase.vue'
import NotificationToast from '../components/Reutilizables/NotificationToast.vue'
import AppIcons from '../components/icons/AppIcons.vue'
import PermisosToggle from '../components/Reutilizables/PermisosToggle.vue'

export default {
  name: 'UsuariosRoles',
  components: {
    BaseButton,
    BaseModal,
    BaseSelect,
    BaseCheckBox,
    InputBase,
    NotificationToast,
    AppIcons,
    PermisosToggle
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
    usuarios: [],
    usuariosFiltrados: [],
    selectedIds: [],
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
      changePassword: false,
      usuarioForm: {
        username: '',
        rol: '',
        password: '',
        confirmPassword: '',
        activo: true,
        permisos: {}
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
    }
  },
  computed: {
    formularioValido() {
      if (!this.usuarioForm.username || !this.usuarioForm.rol) return false

      // Validación en modo creación (password obligatorio)
      if (!this.modoEdicion) {
        if (!this.usuarioForm.password || !this.usuarioForm.confirmPassword) return false
        if (this.usuarioForm.password !== this.usuarioForm.confirmPassword) return false
        if (this.usuarioForm.password.length < 6) return false
      }

      // En modo edición solo validar si se decidió cambiar la contraseña
      if (this.modoEdicion && this.changePassword) {
        if (!this.usuarioForm.password || !this.usuarioForm.confirmPassword) return false
        if (this.usuarioForm.password !== this.usuarioForm.confirmPassword) return false
        if (this.usuarioForm.password.length < 6) return false
      }
      return true
    }
    ,
    selectedCount() {
      return this.selectedIds.length
    },
    canEditOne() {
      return this.selectedIds.length === 1
    },
    selectedUsuario() {
      if (this.selectedIds.length !== 1) return null
      const id = this.selectedIds[0]
      return this.usuariosFiltrados.find(u => u.id === id) || this.usuarios.find(u => u.id === id) || null
    },
    allSelected() {
      return this.usuariosFiltrados.length > 0 && this.selectedIds.length === this.usuariosFiltrados.length
    }
  },
  async mounted() {
    console.log('UsuariosRoles mounted')
    await this.cargarDatos()
  },
  methods: {
    getIniciales(texto) {
      if (!texto) return 'U'
      const partes = String(texto).trim().split(/\s+/)
      const ini = (partes[0]?.[0] || '') + (partes[1]?.[0] || '')
      return ini.toUpperCase() || (String(texto)[0] || 'U').toUpperCase()
    },

    avatarDataUrl(texto) {
      const initials = this.getIniciales(texto)
      const bg = '#E6F0FF'
      const fg = '#1E40AF'
      const svg = `<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><defs><clipPath id="r"><rect rx="32" ry="32" width="64" height="64"/></clipPath></defs><g clip-path="url(#r)"><rect width="64" height="64" fill="${bg}"/><text x="50%" y="50%" dominant-baseline="central" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="24" fill="${fg}">${initials}</text></g></svg>`
      return 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg)
    },

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
      // Cargar datos mock en memoria para modo solo-pantallas
      this.cargando = true
      try {
        // Aplicaciones (módulos)
        this.aplicaciones = [
          { APL_ID: 1, APL_DESCRIPCION: 'Gestión Personas' },
          { APL_ID: 2, APL_DESCRIPCION: 'Cursos' },
          { APL_ID: 3, APL_DESCRIPCION: 'Pagos' }
        ]

        // Roles disponibles (value = id de perfil, label = texto)
        const roles = [
          { value: 6, label: 'Administrador' },
          { value: 7, label: 'Coordinador' },
          { value: 8, label: 'Dirigente' },
          { value: 9, label: 'Apoderado' }
        ]

  this.rolesOptions = [ { value: '', label: 'Todos los perfiles' }, ...roles ]

        // Usuarios mock — campos usados en la vista
        this.usuarios = [
          { id: 1, nombre: 'Ariel Ichi', username: 'Arielichi', rol: 'Administrador', perfil_id: 6, activo: true },
          { id: 2, nombre: 'Rosa Muñoz', username: 'munozrosa', rol: 'Coordinador', perfil_id: 7, activo: true },
          { id: 3, nombre: 'Carlos Muñoz', username: 'munozcarlos', rol: 'Administrador', perfil_id: 6, activo: true },
          { id: 4, nombre: 'Luis Pérez', username: 'luis42', rol: 'Coordinador', perfil_id: 7, activo: false },
          { id: 5, nombre: 'Pedro González', username: 'pedrogonzalez', rol: 'Administrador', perfil_id: 6, activo: true }
        ]

        // Inicializar permisos por usuario (vacíos)
        this.usuarios.forEach(u => {
          this.userPerms[u.id] = null // nulo = sin personalizados, se usan permisos por rol
        })

        this.usuariosFiltrados = [...this.usuarios]
      } catch (error) {
        console.error('Error al cargar datos mock:', error)
        this.mostrarNotificacion('Error al inicializar la vista', 'error')
      } finally {
        this.cargando = false
      }
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
      // Inicializar permisos vacíos para cada aplicación
      const permisosVacios = {}
      if (this.aplicaciones && this.aplicaciones.length > 0) {
        this.aplicaciones.forEach(app => {
          const appId = app.APL_ID || app.id
          console.log(`Creando contenedor de permisos para app ID: ${appId} (${app.APL_DESCRIPCION})`)
          permisosVacios[appId] = {
            consultar: false,
            ingresar: false,
            modificar: false,
            eliminar: false
          }
        })
      }
      console.log('Contenedores de permisos creados:', Object.keys(permisosVacios))
      
      return {
        username: '',
        rol: '',
        password: '',
        confirmPassword: '',
        activo: true,
        foto: '',
        permisos: permisosVacios
      }
    },
    
    async cargarPermisosDelRol() {
      if (!this.usuarioForm.rol) return

      // Determinar si el rol corresponde a Administrador
      const roleOption = this.rolesOptions.find(r => String(r.value) === String(this.usuarioForm.rol))
      const roleLabel = roleOption ? roleOption.label : null
      const esAdmin = roleLabel === 'Administrador' || String(this.usuarioForm.rol) === '6'

      const nuevosPermisos = {}
      this.aplicaciones.forEach(app => {
        const appId = app.APL_ID || app.id
        if (esAdmin) {
          nuevosPermisos[appId] = { consultar: true, ingresar: true, modificar: true, eliminar: true }
        } else if (roleLabel === 'Coordinador') {
          nuevosPermisos[appId] = { consultar: true, ingresar: true, modificar: true, eliminar: false }
        } else {
          // Valores por defecto para otros roles
          nuevosPermisos[appId] = { consultar: true, ingresar: false, modificar: false, eliminar: false }
        }
      })

      this.usuarioForm.permisos = nuevosPermisos
      await this.$nextTick()
    },
    
    abrirModalCrear() {
      this.modoEdicion = false
      this.usuarioForm = this.getFormularioVacio()
      this.modalVisible = true
    },
    
    async abrirModalEditar(usuario) {
      this.modoEdicion = true
      this.changePassword = false
      console.log('Usuario a editar:', usuario)
      console.log('Perfil ID del usuario:', usuario.perfil_id)

      // Inicializar permisos vacíos
      const permisosForm = {}
      this.aplicaciones.forEach(app => {
        permisosForm[app.APL_ID || app.id] = {
          consultar: false,
          ingresar: false,
          modificar: false,
          eliminar: false
        }
      })

      this.usuarioForm = {
        id: usuario.id,
        username: usuario.username,
        rol: usuario.perfil_id || usuario.rol,
        activo: usuario.activo,
        password: '',
        confirmPassword: '',
        foto: usuario.foto || '',
        permisos: permisosForm
      }

      // Cargar permisos personalizados del usuario desde memoria (userPerms)
      const permisosUsuario = this.userPerms[usuario.id]
      if (permisosUsuario) {
        // Mapear permisos personalizados al formulario
        Object.entries(permisosUsuario).forEach(([aplId, p]) => {
          if (this.usuarioForm.permisos[aplId]) {
            this.usuarioForm.permisos[aplId] = {
              consultar: !!p.consultar,
              ingresar: !!p.ingresar,
              modificar: !!p.modificar,
              eliminar: !!p.eliminar
            }
          }
        })
        console.log('Permisos personalizados cargados (memoria):', this.usuarioForm.permisos)
      } else {
        // Si no hay personalizados, cargar los del rol
        await this.cargarPermisosDelRol()
      }

      this.modalVisible = true
    },
    
    cerrarModal() {
      this.modalVisible = false
      this.usuarioForm = this.getFormularioVacio()
      this.changePassword = false
    },
    
    async guardarUsuario() {
      if (!this.formularioValido) {
        this.mostrarNotificacion('Por favor complete todos los campos requeridos', 'warning')
        return
      }
      
      this.procesando = true
      try {
        const datosUsuario = {
          username: this.usuarioForm.username,
          perfil_id: this.usuarioForm.rol,
          activo: this.usuarioForm.activo
        }
        
        if (!this.modoEdicion) {
          datosUsuario.password = this.usuarioForm.password
        } else if (this.changePassword) {
          datosUsuario.password = this.usuarioForm.password
        }
        
        let usuarioId
        // Operación en memoria (UI-only)
        if (this.modoEdicion) {
          const idx = this.usuarios.findIndex(u => u.id === this.usuarioForm.id)
          if (idx !== -1) {
            const roleOpt = this.rolesOptions.find(r => String(r.value) === String(this.usuarioForm.rol))
            this.usuarios[idx].username = this.usuarioForm.username
            this.usuarios[idx].nombre = this.usuarioForm.username
            this.usuarios[idx].perfil_id = this.usuarioForm.rol
            this.usuarios[idx].rol = roleOpt ? roleOpt.label : this.usuarios[idx].rol
            this.usuarios[idx].activo = this.usuarioForm.activo
            this.usuarios[idx].foto = this.usuarioForm.foto
            usuarioId = this.usuarioForm.id
            this.mostrarNotificacion('Usuario actualizado exitosamente', 'success')
          } else {
            throw new Error('Usuario no encontrado para actualizar')
          }
        } else {
          const newId = this.usuarios.length > 0 ? Math.max(...this.usuarios.map(u => u.id)) + 1 : 1
          const roleOpt = this.rolesOptions.find(r => String(r.value) === String(this.usuarioForm.rol))
          const nuevoUsuario = {
            id: newId,
            nombre: this.usuarioForm.username,
            username: this.usuarioForm.username,
            perfil_id: this.usuarioForm.rol,
            rol: roleOpt ? roleOpt.label : '',
            activo: this.usuarioForm.activo,
            foto: this.usuarioForm.foto || ''
          }
          this.usuarios.push(nuevoUsuario)
          usuarioId = newId
          this.mostrarNotificacion('Usuario creado exitosamente', 'success')
        }
        
        // Guardar permisos personalizados en memoria
        if (this.usuarioForm.permisos) {
          this.userPerms[usuarioId] = JSON.parse(JSON.stringify(this.usuarioForm.permisos))
        }
        
        this.cerrarModal()
        await this.cargarDatos()
      } catch (error) {
        console.error('Error al guardar usuario (memoria):', error)
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
        // Actualizar en memoria
        const idx = this.usuarios.findIndex(u => u.id === usuario.id)
        if (idx !== -1) {
          this.usuarios[idx].activo = nuevoEstado
          this.mostrarNotificacion(`Usuario ${nuevoEstado ? 'activado' : 'desactivado'} exitosamente`, 'success')
          this.usuariosFiltrados = [...this.usuarios]
        } else {
          throw new Error('Usuario no encontrado')
        }
        this.modalConfirmacionVisible = false
      } catch (error) {
        console.error('Error al cambiar estado:', error)
        this.mostrarNotificacion('Error al cambiar el estado del usuario', 'error')
      } finally {
        this.procesando = false
      }
    },
    
    confirmarEliminar(usuario) {
      this.tituloConfirmacion = 'Eliminar Usuario'
      this.mensajeConfirmacion = `¿Está seguro que desea eliminar al usuario "${usuario.nombre}"? Esta acción no se puede deshacer.`
      this.accionConfirmacion = () => this.eliminarUsuario(usuario)
      this.modalConfirmacionVisible = true
    },
    
    async eliminarUsuario(usuario) {
      this.procesando = true
      try {
        const idx = this.usuarios.findIndex(u => u.id === usuario.id)
        if (idx !== -1) {
          this.usuarios.splice(idx, 1)
          delete this.userPerms[usuario.id]
          this.usuariosFiltrados = [...this.usuarios]
          this.mostrarNotificacion('Usuario eliminado exitosamente', 'success')
          this.modalConfirmacionVisible = false
        } else {
          throw new Error('Usuario no encontrado')
        }
      } catch (error) {
        console.error('Error al eliminar usuario:', error)
        this.mostrarNotificacion('Error al eliminar el usuario', 'error')
      } finally {
        this.procesando = false
      }
    },
    
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
    isSelected(id) {
      return this.selectedIds.includes(id)
    },
    toggleRowSelection(usuario) {
      const id = usuario.id
      const idx = this.selectedIds.indexOf(id)
      if (idx === -1) this.selectedIds.push(id)
      else this.selectedIds.splice(idx, 1)
    },
    toggleSelectAll(e) {
      const checked = e.target.checked
      if (checked) this.selectedIds = this.usuariosFiltrados.map(u => u.id)
      else this.selectedIds = []
    },
    accionEditarSelected() {
      if (this.canEditOne && this.selectedUsuario) {
        this.abrirModalEditar(this.selectedUsuario)
      }
    },
    cambiarEstadoMasivo(nuevoEstado) {
      if (this.selectedIds.length === 0) return
      this.procesando = true
      try {
        let cambios = 0
        this.usuarios.forEach(u => {
          if (this.selectedIds.includes(u.id)) {
            u.activo = nuevoEstado
            cambios += 1
          }
        })
        this.usuariosFiltrados = [...this.usuarios]
        this.mostrarNotificacion(`${cambios} usuario(s) ${nuevoEstado ? 'activado(s)' : 'desactivado(s)'}`, 'success')
      } finally {
        this.procesando = false
      }
    },
    activarCambioPassword() {
      this.changePassword = true
      this.usuarioForm.password = ''
      this.usuarioForm.confirmPassword = ''
    },
    cancelarCambioPassword() {
      this.changePassword = false
      this.usuarioForm.password = ''
      this.usuarioForm.confirmPassword = ''
    },
    confirmarNuevoPassword() {
      if (this.formularioValido) {
        this.mostrarNotificacion('Nueva contraseña lista para guardar', 'success')
      } else {
        this.mostrarNotificacion('Revise la nueva contraseña', 'warning')
      }
    },
    onFotoChange(e) {
      const file = e.target.files && e.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = (evt) => {
        this.usuarioForm.foto = evt.target.result
      }
      reader.readAsDataURL(file)
    }
  }
}
</script>

<style scoped>
.usuarios-roles {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.page-header h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}

/* Filtros */
.filtros {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
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
  padding: 4rem 2rem;
  gap: 1rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Tabla */
.table-wrapper {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* Asegura que el header abarque todo el ancho y no se descuadre */
}

.usuarios-table thead {
  background: #34495e;
  color: white;
}

.usuarios-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.col-check { width: 36px; text-align: center; }
.col-check input { cursor: pointer; }

.usuarios-table tbody tr {
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.2s;
  cursor: pointer;
  position: relative; /* Para estabilizar pseudo-elemento y evitar cualquier "salto" visual */
}

/* Reservar siempre el espacio visual de la barra azul para que al seleccionar no parezca que se mueve */
.usuarios-table tbody tr::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 5px; /* Igual que la barra de selección */
  background: transparent; /* Invisible cuando no está seleccionado */
  pointer-events: none;
}

.usuarios-table tbody tr:hover {
  background-color: #f8f9fa;
}

/* Selección más notoria */
.usuarios-table tbody tr.row-selected {
  /* Más azul y sin cambios de layout */
  background: linear-gradient(90deg, #c7d2fe 0%, #e3edff 70%);
  position: relative;
  box-shadow: inset 0 0 0 1px #bfdbfe;
}
.usuarios-table tbody tr.row-selected:hover {
  /* Mantener el mismo fondo al hacer hover para que no "se mueva" visualmente */
  background: linear-gradient(90deg, #c7d2fe 0%, #e3edff 70%);
}
.usuarios-table tbody tr.row-selected::before {
  background: #1d4ed8; /* Solo cambiamos el color; ya existe el pseudo-elemento en todas las filas */
}
.usuarios-table tbody tr.row-selected .username {
  /* Mantener el mismo grosor para evitar reflow, solo cambiar color */
  color: #1d4ed8;
}

.usuarios-table tbody tr.usuario-inactivo {
  opacity: 0.6;
}

.usuarios-table td {
  padding: 1rem;
  vertical-align: middle;
}

/* Usuario + Avatar */
.user-cell {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0; /* para que el ellipsis funcione dentro de celdas de ancho fijo */
}

.user-cell .avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e6eef8;
  background: #eef2f7;
}

.user-cell .username {
  font-weight: 600;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Badges */
.rol-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
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

.estado-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.estado-activo {
  background-color: #27ae60;
  color: white;
}

.estado-inactivo {
  background-color: #95a5a6;
  color: white;
}

/* Acciones */
.acciones-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Toolbar superior */

/* Card estilo Correos reutilizado */
.correos-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(40,92,168,0.13);
  margin: 0 auto 28px auto;
  padding: 22px 22px 16px 22px;
  max-width: 1400px;
  width: 100%;
  box-sizing: border-box;
  border: 1.5px solid #dbe4f3;
}
.correos-card-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  gap: 10px;
}
.correos-card-title {
  font-size: 1.18rem;
  font-weight: 700;
  color: #1d4ed8;
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
  background: #1d4ed8;
  border-radius: 4px;
}
.correos-card-actions {
  display: flex;
  flex-wrap: nowrap;
  gap: 12px;
  justify-content: flex-end;
}
.correos-card-actions :deep(button),
.correos-card-actions button {
  min-width: 150px;
  padding: 10px 16px;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(40,92,168,0.08);
  border: none;
  transition: all 0.25s ease;
}
.correos-card-actions button:hover {
  filter: brightness(0.95);
  box-shadow: 0 4px 16px rgba(40,92,168,0.13);
}
.usuarios-seleccion-resumen {
  font-size: 0.85rem;
  color: #475569;
  margin-bottom: 8px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
.badge-mini {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.65rem;
  font-weight: 600;
  background: #e5e7eb;
  color: #374151;
}
.badge-mini.mini-ok { background:#d1fae5; color:#065f46; }
.badge-mini.mini-off { background:#e5e7eb; color:#555; }
.usuarios-table-wrapper { margin-top: 4px; }

/* Eliminado duplicado de estilos de selección que sobreescribía el gradiente */

/* Empty state */
.empty-row td {
  padding: 3rem 1rem;
}

.empty-state {
  text-align: center;
  color: #7f8c8d;
}

.empty-state p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

/* Modal */
.modal-usuario {
  padding: 1.5rem 1.75rem; /* compactar */
  max-width: 720px; /* más angosto */
  width: 90vw;
}

.modal-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem; /* título más pequeño */
  font-weight: 600;
  color: #2c3e50;
}

.usuario-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem; /* más compacto */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem; /* menor separación */
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.form-group .required {
  color: #e74c3c;
}

.form-hint {
  font-size: 0.78rem; /* más pequeño */
  color: #64748b;
  margin-top: 0.1rem;
  margin-bottom: 0.5rem;
}

/* Password change area */
.password-masked-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.password-masked {
  display: inline-block;
  letter-spacing: 2px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px 10px; /* más bajo */
  color: #475569;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

.password-actions-inline {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

/* Avatar preview in modal */
.avatar-preview-wrapper {
  margin-top: 0.4rem;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: #f8fafc;
  padding: 6px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
}
.avatar-preview {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #dbe4f3;
  background: #eef2f7;
}

/* Estilo para input de archivo para cuadrar con inputs */
input[type="file"].file-input {
  display: block;
  width: 100%;
  padding: 8px 12px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #1f2937;
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

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
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
    width: 100px;
    color: #34495e;
  }

  .acciones-buttons {
    justify-content: flex-start;
    margin-top: 0.5rem;
  }
}
</style>
