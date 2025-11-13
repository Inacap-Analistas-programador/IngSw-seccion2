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
        placeholder="Todos los roles"
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

    <!-- Tabla de usuarios -->
    <div v-else class="table-wrapper">
      <table class="usuarios-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Usuario</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="usuario in usuariosFiltrados" 
            :key="usuario.id"
            :class="{ 'usuario-inactivo': !usuario.activo }"
          >
            <td data-label="Nombre">{{ usuario.nombre }}</td>
            <td data-label="Usuario">{{ usuario.username }}</td>
            <td data-label="Rol">
              <span class="rol-badge" :class="rolClass(usuario)">
                {{ getRolLabel(usuario.perfil_id) || usuario.rol }}
              </span>
            </td>
            <td data-label="Estado">
              <span 
                :class="['estado-badge', usuario.activo ? 'estado-activo' : 'estado-inactivo']"
              >
                {{ usuario.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td data-label="Acciones">
              <div class="acciones-buttons">
                <BaseButton 
                  class="btn-editar" 
                  variant="primary" 
                  size="sm"
                  @click="abrirModalEditar(usuario)"
                  title="Editar usuario"
                >
                  Editar
                </BaseButton>
                <BaseButton 
                  v-if="usuario.activo"
                  class="btn-desactivar" 
                  variant="danger" 
                  size="sm"
                  @click="confirmarCambioEstado(usuario, false)"
                  title="Desactivar usuario"
                >
                  Desactivar
                </BaseButton>
                <BaseButton 
                  v-else
                  class="btn-activar" 
                  variant="success" 
                  size="sm"
                  @click="cambiarEstado(usuario, true)"
                  title="Activar usuario"
                >
                  Activar
                </BaseButton>
                <BaseButton 
                  class="btn-eliminar" 
                  variant="danger" 
                  size="sm"
                  @click="confirmarEliminar(usuario)"
                  title="Eliminar usuario"
                >
                  Eliminar
                </BaseButton>
              </div>
            </td>
          </tr>
          <tr v-if="usuariosFiltrados.length === 0" class="empty-row">
            <td colspan="5">
              <div class="empty-state">
                <p>No se encontraron usuarios</p>
                <BaseButton variant="primary" @click="limpiarFiltros">
                  Mostrar todos
                </BaseButton>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para crear/editar usuario -->
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
                :disabled="procesando"
              />
              <small class="form-hint">Este nombre se mostrará en la tabla</small>
            </div>

            <div class="form-group">
              <label for="rol">Rol <span class="required">*</span></label>
              <BaseSelect 
                id="rol"
                v-model="usuarioForm.rol" 
                :options="rolesOptions"
                placeholder="Seleccionar rol"
                required
                :disabled="procesando"
                @change="cargarPermisosDelRol"
              />
            </div>

            <!-- Permisos personalizados por aplicación -->
            <div class="form-group" v-if="(modoEdicion || usuarioForm.rol) && aplicaciones.length > 0">
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
// Modo UI-only: eliminadas dependencias a la API. Los datos se cargan en memoria (mock).
import { useRouter } from 'vue-router'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import BaseSelect from '../components/BaseSelect.vue'
import BaseCheckBox from '../components/BaseCheckBox.vue'
import InputBase from '../components/InputBase.vue'
import NotificationToast from '../components/NotificationToast.vue'
import AppIcons from '../components/icons/AppIcons.vue'
import PermisosToggle from '../components/PermisosToggle.vue'

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
      if (!this.usuarioForm.username || !this.usuarioForm.rol) {
        return false
      }
      
      if (!this.modoEdicion) {
        if (!this.usuarioForm.password || !this.usuarioForm.confirmPassword) {
          return false
        }
        if (this.usuarioForm.password !== this.usuarioForm.confirmPassword) {
          return false
        }
        if (this.usuarioForm.password.length < 6) {
          return false
        }
      }
      
      return true
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

        this.rolesOptions = [ { value: '', label: 'Todos los roles' }, ...roles ]

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
            activo: this.usuarioForm.activo
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

.usuarios-table tbody tr {
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.2s;
}

.usuarios-table tbody tr:hover {
  background-color: #f8f9fa;
}

.usuarios-table tbody tr.usuario-inactivo {
  opacity: 0.6;
}

.usuarios-table td {
  padding: 1rem;
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
  padding: 2rem;
  max-width: 800px;
  width: 90vw;
}

.modal-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.75rem;
  color: #2c3e50;
}

.usuario-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-top: 0.25rem;
  margin-bottom: 1rem;
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
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
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
