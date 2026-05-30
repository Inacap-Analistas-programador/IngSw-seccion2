/**
 * useUsuarios.js
 * Composable que centraliza toda la lógica de negocio de Usuarios.vue.
 *
 * Responsabilidades:
 * - Estado reactivo de usuarios, filtros, paginación, modales y notificaciones
 * - Operaciones CRUD: cargar, crear, editar, toggle estado (individual y masivo)
 * - Lógica de selección de filas multi-selección
 *
 * Uso en Usuarios.vue:
 *   const {
 *     usuarios, usuariosFiltrados, displayedUsuarios,
 *     cargando, procesando, selectedIds, searchQuery,
 *     filtroRol, filtroEstado, rolesOptions, estadoOptions,
 *     modalVisible, modoEdicion, usuarioForm,
 *     modalConfirmacionVisible, tituloConfirmacion, mensajeConfirmacion,
 *     notificacion, currentPage, perPage, totalCount, totalPages,
 *     can,
 *     cargarDatos, filtrarUsuarios, limpiarFiltros,
 *     abrirModalCrear, abrirModalEditar, cerrarModal, guardarUsuario,
 *     isSelected, toggleRowSelection, clearSelection, editarSeleccionado,
 *     toggleEstadoSeleccionados, ejecutarAccion, cancelarAccion,
 *     cerrarNotificacion,
 *   } = useUsuarios()
 */
import { ref, computed } from 'vue'
import usuariosService from '@/services/usuariosService'
import { usePermissions } from '@/composables/usePermissions'

const ESTADO_OPTIONS = [
  { value: '', label: 'Todos los estados' },
  { value: 'activo', label: 'Activos' },
  { value: 'inactivo', label: 'Inactivos' },
]

export function useUsuarios() {
  // ─── Permisos ────────────────────────────────────────────────────────────
  const { can } = usePermissions('Usuarios')

  // ─── Estado principal ────────────────────────────────────────────────────
  const usuarios = ref([])
  const usuariosFiltrados = ref([])
  const selectedIds = ref([])
  const rolesOptions = ref([])
  const estadoOptions = ref(ESTADO_OPTIONS)

  // ─── Filtros ─────────────────────────────────────────────────────────────
  const searchQuery = ref('')
  const filtroRol = ref('')
  const filtroEstado = ref('')

  // ─── Paginación (server-side) ─────────────────────────────────────────────
  const currentPage = ref(1)
  const perPage = ref(50)
  const totalCount = ref(0)
  const serverSide = ref(true)
  const perPageOptions = [10, 20, 50, 100]

  // ─── Carga ────────────────────────────────────────────────────────────────
  const cargando = ref(false)
  const procesando = ref(false)

  // ─── Modal usuario ────────────────────────────────────────────────────────
  const modalVisible = ref(false)
  const modoEdicion = ref(false)
  const usuarioFormDefault = () => ({
    id: null, username: '', email: '', rol: '',
    password: '', confirmPassword: '', activo: true, foto: null, fotoPreview: null
  })
  const usuarioForm = ref(usuarioFormDefault())

  // ─── Modal confirmación ───────────────────────────────────────────────────
  const modalConfirmacionVisible = ref(false)
  const tituloConfirmacion = ref('')
  const mensajeConfirmacion = ref('')
  let accionConfirmacionFn = null

  // ─── Notificaciones ───────────────────────────────────────────────────────
  const notificacion = ref({ visible: false, mensaje: '', tipo: 'info' })
  let notifTimeout = null

  // ─── Computed ─────────────────────────────────────────────────────────────
  const displayedUsuarios = computed(() => {
    if (serverSide.value) return usuariosFiltrados.value
    const start = (currentPage.value - 1) * perPage.value
    return usuariosFiltrados.value.slice(start, start + perPage.value)
  })

  const totalPages = computed(() => {
    const total = serverSide.value ? totalCount.value : usuariosFiltrados.value.length
    return Math.max(1, Math.ceil(total / perPage.value))
  })

  const showingRange = computed(() => {
    const total = serverSide.value ? totalCount.value : usuariosFiltrados.value.length
    if (!total) return '0-0 de 0'
    const start = (currentPage.value - 1) * perPage.value + 1
    const end = Math.min(total, currentPage.value * perPage.value)
    return `${start}-${end} de ${total}`
  })

  const formularioValido = computed(() => {
    const f = usuarioForm.value
    if (!f.username || !f.rol) return false
    if (modoEdicion.value) {
      if (f.password) {
        return !!f.confirmPassword &&
          f.password === f.confirmPassword &&
          f.password.length >= 6
      }
      return true
    }
    return !!f.password &&
      !!f.confirmPassword &&
      f.password === f.confirmPassword &&
      f.password.length >= 6
  })

  const botonEstadoLabel = computed(() => {
    if (!selectedIds.value.length) return 'Cambiar Estado'
    const seleccionados = usuarios.value.filter(u => selectedIds.value.includes(u.id))
    const todosActivos = seleccionados.every(u => u.activo)
    return todosActivos ? 'Desactivar' : 'Activar'
  })

  const botonEstadoIcon = computed(() => {
    const seleccionados = usuarios.value.filter(u => selectedIds.value.includes(u.id))
    return seleccionados.every(u => u.activo) ? 'toggle-off' : 'toggle-on'
  })

  // ─── Helpers ──────────────────────────────────────────────────────────────
  function mostrarNotificacion(mensaje, tipo = 'info') {
    clearTimeout(notifTimeout)
    notificacion.value = { visible: true, mensaje, tipo }
    notifTimeout = setTimeout(() => { notificacion.value.visible = false }, 4000)
  }

  function cerrarNotificacion() {
    notificacion.value.visible = false
  }

  function getRolLabel(perfilId) {
    const op = rolesOptions.value.find(r => r.value === perfilId)
    return op?.label || null
  }

  function rolClass(usuario) {
    const label = (getRolLabel(usuario.perfil_id) || usuario.rol || '').toLowerCase()
    const map = {
      administrador: 'rol-administrador',
      coordinador:   'rol-coordinador',
      dirigente:     'rol-dirigente',
      apoderado:     'rol-apoderado',
      participante:  'rol-participante',
    }
    return Object.entries(map).find(([k]) => label.includes(k))?.[1] || ''
  }

  // ─── Selección ────────────────────────────────────────────────────────────
  const isSelected = (id) => selectedIds.value.includes(id)

  function toggleRowSelection(usuario) {
    const idx = selectedIds.value.indexOf(usuario.id)
    if (idx === -1) selectedIds.value.push(usuario.id)
    else selectedIds.value.splice(idx, 1)
  }

  function clearSelection() {
    selectedIds.value = []
  }

  function editarSeleccionado() {
    if (selectedIds.value.length !== 1) return
    const usuario = usuarios.value.find(u => u.id === selectedIds.value[0])
    if (usuario) abrirModalEditar(usuario)
  }

  // ─── Carga de datos ───────────────────────────────────────────────────────
  async function cargarDatos(page = 1) {
    cargando.value = true
    try {
      const params = {
        page,
        page_size: perPage.value,
        ...(searchQuery.value && { search: searchQuery.value }),
        ...(filtroRol.value && { perfil_id: filtroRol.value }),
        ...(filtroEstado.value && { activo: filtroEstado.value === 'activo' }),
      }
      const data = await usuariosService.list(params)
      const items = data?.results ?? data ?? []
      totalCount.value = data?.count ?? items.length
      usuarios.value = items
      usuariosFiltrados.value = items
      currentPage.value = page
    } catch (e) {
      mostrarNotificacion('Error al cargar usuarios: ' + (e.message || ''), 'error')
    } finally {
      cargando.value = false
    }
  }

  async function cargarRoles() {
    try {
      const data = await usuariosService.listPerfiles?.() ?? []
      rolesOptions.value = (data?.results ?? data).map(r => ({
        value: r.pel_id ?? r.id,
        label: r.pel_descripcion ?? r.descripcion ?? `Perfil ${r.id}`,
      }))
    } catch { /* roles no crítico */ }
  }

  function filtrarUsuarios() {
    cargarDatos(1)
  }

  function limpiarFiltros() {
    searchQuery.value = ''
    filtroRol.value = ''
    filtroEstado.value = ''
    cargarDatos(1)
  }

  // ─── Modal ────────────────────────────────────────────────────────────────
  function abrirModalCrear() {
    usuarioForm.value = usuarioFormDefault()
    modoEdicion.value = false
    modalVisible.value = true
  }

  function abrirModalEditar(usuario) {
    usuarioForm.value = {
      id: usuario.id,
      username: usuario.username || '',
      email: usuario.email || '',
      rol: usuario.perfil_id || '',
      password: '',
      confirmPassword: '',
      activo: usuario.activo ?? true,
      foto: usuario.foto || null,
      fotoPreview: usuario.foto || null,
    }
    modoEdicion.value = true
    modalVisible.value = true
  }

  function cerrarModal() {
    modalVisible.value = false
    usuarioForm.value = usuarioFormDefault()
  }

  async function guardarUsuario() {
    if (!formularioValido.value) return
    procesando.value = true
    try {
      const payload = {
        USU_USERNAME: usuarioForm.value.username,
        USU_EMAIL: usuarioForm.value.email,
        PEL_ID: usuarioForm.value.rol,
        is_active: usuarioForm.value.activo,
      }
      if (usuarioForm.value.password) {
        payload.password = usuarioForm.value.password
      }

      if (modoEdicion.value) {
        await usuariosService.partialUpdate(usuarioForm.value.id, payload)
        mostrarNotificacion('Usuario actualizado correctamente', 'success')
      } else {
        await usuariosService.create(payload)
        mostrarNotificacion('Usuario creado correctamente', 'success')
      }

      cerrarModal()
      await cargarDatos(currentPage.value)
    } catch (e) {
      mostrarNotificacion('Error al guardar usuario: ' + (e.message || ''), 'error')
    } finally {
      procesando.value = false
    }
  }

  // ─── Toggle estado ────────────────────────────────────────────────────────
  function confirmarCambioEstado(usuario, nuevoEstado) {
    tituloConfirmacion.value = nuevoEstado ? 'Activar Usuario' : 'Desactivar Usuario'
    mensajeConfirmacion.value = `¿Está seguro que desea ${nuevoEstado ? 'activar' : 'desactivar'} al usuario "${usuario.username}"?`
    accionConfirmacionFn = () => _ejecutarCambioEstado(usuario, nuevoEstado)
    modalConfirmacionVisible.value = true
  }

  async function _ejecutarCambioEstado(usuario, nuevoEstado) {
    procesando.value = true
    try {
      await usuariosService.partialUpdate(usuario.id, { is_active: nuevoEstado })
      usuario.activo = nuevoEstado
      usuariosFiltrados.value = [...usuarios.value]
      mostrarNotificacion(`Usuario ${nuevoEstado ? 'activado' : 'desactivado'} exitosamente`, 'success')
      clearSelection()
      modalConfirmacionVisible.value = false
    } catch (e) {
      mostrarNotificacion('Error al cambiar estado: ' + (e.message || ''), 'error')
    } finally {
      procesando.value = false
    }
  }

  function toggleEstadoSeleccionados() {
    if (!selectedIds.value.length) return
    const sel = usuarios.value.filter(u => selectedIds.value.includes(u.id))
    if (sel.length === 1) {
      confirmarCambioEstado(sel[0], !sel[0].activo)
      return
    }
    const todosActivos = sel.every(u => u.activo)
    const todosInactivos = sel.every(u => !u.activo)
    tituloConfirmacion.value = todosActivos ? 'Desactivar Usuarios' : todosInactivos ? 'Activar Usuarios' : 'Cambiar Estado'
    mensajeConfirmacion.value = `¿Confirmar cambio de estado para ${sel.length} usuario(s)?`
    accionConfirmacionFn = () => _ejecutarCambioEstadoMasivo(sel, todosActivos ? false : todosInactivos ? true : null)
    modalConfirmacionVisible.value = true
  }

  async function _ejecutarCambioEstadoMasivo(seleccionados, nuevoEstado) {
    procesando.value = true
    try {
      await Promise.all(
        seleccionados.map(u => {
          const estado = nuevoEstado ?? !u.activo
          return usuariosService.partialUpdate(u.id, { is_active: estado })
            .then(() => { u.activo = estado })
            .catch(() => null)
        })
      )
      usuariosFiltrados.value = [...usuarios.value]
      mostrarNotificacion(`Estado actualizado para ${seleccionados.length} usuario(s)`, 'success')
      clearSelection()
      modalConfirmacionVisible.value = false
    } catch (e) {
      mostrarNotificacion('Error en cambio masivo: ' + (e.message || ''), 'error')
    } finally {
      procesando.value = false
    }
  }

  function ejecutarAccion() {
    accionConfirmacionFn?.()
  }

  function cancelarAccion() {
    modalConfirmacionVisible.value = false
    accionConfirmacionFn = null
  }

  // ─── Init ─────────────────────────────────────────────────────────────────
  async function init() {
    await Promise.all([cargarDatos(), cargarRoles()])
  }

  return {
    // Estado
    can, usuarios, usuariosFiltrados, displayedUsuarios,
    selectedIds, rolesOptions, estadoOptions,
    searchQuery, filtroRol, filtroEstado,
    currentPage, perPage, perPageOptions, totalCount, totalPages, showingRange,
    cargando, procesando,
    modalVisible, modoEdicion, usuarioForm, formularioValido,
    modalConfirmacionVisible, tituloConfirmacion, mensajeConfirmacion,
    notificacion, botonEstadoLabel, botonEstadoIcon,
    // Métodos
    init, cargarDatos, filtrarUsuarios, limpiarFiltros,
    abrirModalCrear, abrirModalEditar, cerrarModal, guardarUsuario,
    isSelected, toggleRowSelection, clearSelection, editarSeleccionado,
    toggleEstadoSeleccionados, ejecutarAccion, cancelarAccion,
    cerrarNotificacion, getRolLabel, rolClass,
  }
}
