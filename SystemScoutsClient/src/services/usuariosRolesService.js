// Servicio para gestión de usuarios y roles
// Centraliza las consultas necesarias y normaliza los datos
import { request } from './apiClient'

/**
 * Normaliza los datos de un usuario desde la API
 * @param {Object} usuario - Usuario desde la API
 * @returns {Object} Usuario normalizado
 */
function normalizarUsuario(usuario) {
  return {
    id: usuario.USU_ID || usuario.id,
    nombre: usuario.USU_USERNAME || usuario.username || 'Sin nombre', // Usar username como nombre por defecto
    username: usuario.USU_USERNAME || usuario.username || '',
    rol: usuario.rol || usuario.perfil?.PEL_DESCRIPCION || 'Sin rol',
    perfil_id: usuario.perfil_id || usuario.PEL_ID || null,
    activo: usuario.USU_VIGENTE ?? usuario.activo ?? true,
    foto: usuario.USU_RUTA_FOTO || usuario.foto || ''
  }
}

/**
 * Obtener todos los usuarios con datos normalizados
 * @returns {Promise<Array>} Lista de usuarios
 */
export async function obtenerUsuarios() {
  try {
    const data = await request('usuarios/usuarios')
    console.log('Datos recibidos de usuarios:', data) // Debug
    if (!Array.isArray(data)) {
      console.warn('La respuesta no es un array:', data)
      return []
    }
    return data.map(normalizarUsuario)
  } catch (error) {
    console.error('Error al obtener usuarios:', error)
    return []
  }
}

/**
 * Obtener un usuario por ID
 * @param {number|string} id - ID del usuario
 * @returns {Promise<Object>} Datos del usuario
 */
export async function obtenerUsuario(id) {
  try {
    const data = await request(`usuarios/usuarios/${id}`)
    return normalizarUsuario(data)
  } catch (error) {
    console.error(`Error al obtener usuario ${id}:`, error)
    throw error
  }
}

/**
 * Crear un nuevo usuario
 * @param {Object} usuario - Datos del nuevo usuario
 * @returns {Promise<Object>} Usuario creado
 */
export async function crearUsuario(usuario) {
  try {
    const payload = {
      USU_USERNAME: usuario.username,
      USU_PASSWORD: usuario.password,
      PEL_ID: usuario.perfil_id || usuario.rol,
      USU_RUTA_FOTO: usuario.foto || '',
      USU_VIGENTE: usuario.activo ?? true
    }
    
    const data = await request('usuarios/usuarios', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    return normalizarUsuario(data)
  } catch (error) {
    console.error('Error al crear usuario:', error)
    throw error
  }
}

/**
 * Actualizar un usuario existente
 * @param {number|string} id - ID del usuario
 * @param {Object} usuario - Datos actualizados del usuario
 * @returns {Promise<Object>} Usuario actualizado
 */
export async function actualizarUsuario(id, usuario) {
  try {
    // Enviar solo los campos que realmente cambian y usar PATCH para evitar requerir password/foto
    const payload = {}

    if (usuario.username !== undefined) payload.USU_USERNAME = usuario.username
    if (usuario.perfil_id !== undefined || usuario.rol !== undefined) {
      payload.PEL_ID = usuario.perfil_id ?? usuario.rol
    }
    // No enviar foto si viene vacía; evita el error "may not be blank"
    if (usuario.foto) {
      payload.USU_RUTA_FOTO = usuario.foto
    }
    if (typeof usuario.activo === 'boolean') payload.USU_VIGENTE = usuario.activo
    if (usuario.password) payload.USU_PASSWORD = usuario.password

    const data = await request(`usuarios/usuarios/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
    return normalizarUsuario(data)
  } catch (error) {
    console.error(`Error al actualizar usuario ${id}:`, error)
    throw error
  }
}

/**
 * Cambiar el estado de un usuario (activar/desactivar)
 * @param {number|string} id - ID del usuario
 * @param {boolean} activo - Estado del usuario
 * @returns {Promise<Object>} Usuario actualizado
 */
export async function cambiarEstadoUsuario(id, activo) {
  try {
    const data = await request(`usuarios/usuarios/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ USU_VIGENTE: activo })
    })
    return normalizarUsuario(data)
  } catch (error) {
    console.error(`Error al cambiar estado del usuario ${id}:`, error)
    throw error
  }
}

/**
 * Eliminar un usuario
 * @param {number|string} id - ID del usuario
 * @returns {Promise<void>}
 */
export async function eliminarUsuario(id) {
  try {
    await request(`usuarios/usuarios/${id}`, {
      method: 'DELETE'
    })
  } catch (error) {
    console.error(`Error al eliminar usuario ${id}:`, error)
    throw error
  }
}

/**
 * Obtener todos los perfiles/roles disponibles
 * @returns {Promise<Array>} Lista de perfiles
 */
export async function obtenerPerfiles() {
  try {
    const data = await request('usuarios/perfiles')
    if (!Array.isArray(data)) return []
    
    return data
      .filter(p => p.PEL_VIGENTE !== false)
      .map(p => ({
        value: p.PEL_ID,
        label: p.PEL_DESCRIPCION || 'Sin nombre'
      }))
  } catch (error) {
    console.error('Error al obtener perfiles:', error)
    // Retornar array vacío si falla - no usar fallback
    return []
  }
}

/**
 * Obtener todas las aplicaciones (módulos) disponibles
 * @returns {Promise<Array>} Lista de aplicaciones
 */
export async function obtenerAplicaciones() {
  try {
    const data = await request('usuarios/aplicaciones')
    if (!Array.isArray(data)) return []
    
    return data.filter(app => app.APL_VIGENTE !== false)
  } catch (error) {
    console.error('Error al obtener aplicaciones:', error)
    return []
  }
}

/**
 * Obtener permisos de un perfil específico
 * @param {number|string} perfilId - ID del perfil
 * @returns {Promise<Array>} Lista de permisos del perfil
 */
export async function obtenerPermisosDelPerfil(perfilId) {
  try {
    const data = await request(`usuarios/perfil-aplicaciones?PEL_ID=${perfilId}`)
    return Array.isArray(data) ? data : []
  } catch (error) {
    console.error(`Error al obtener permisos del perfil ${perfilId}:`, error)
    return []
  }
}

/**
 * Obtener permisos personalizados de un usuario específico
 * @param {number|string} usuarioId - ID del usuario
 * @returns {Promise<Array>} Lista de permisos del usuario
 */
export async function obtenerPermisosDelUsuario(usuarioId) {
  try {
    // Primero obtener el perfil del usuario
    const usuario = await obtenerUsuario(usuarioId)
    if (!usuario.perfil_id) return []
    // Intentar obtener permisos personalizados del usuario
    const permisosUsuario = await request(`usuarios/usuario-aplicaciones?USU_ID=${usuarioId}`)
    if (Array.isArray(permisosUsuario) && permisosUsuario.length > 0) {
      return permisosUsuario
    }

    // Si no hay personalizados, obtener permisos del perfil
    return await obtenerPermisosDelPerfil(usuario.perfil_id)
  } catch (error) {
    console.error(`Error al obtener permisos del usuario ${usuarioId}:`, error)
    return []
  }
}

/**
 * Guardar permisos personalizados de un usuario
 * @param {number|string} usuarioId - ID del usuario
 * @param {Object} permisos - Permisos a asignar { aplicacionId: { consultar, ingresar, modificar, eliminar } }
 * @returns {Promise<void>}
 */
export async function guardarPermisosUsuario(usuarioId, permisos) {
  try {
    const usuario = await obtenerUsuario(usuarioId)
    if (!usuario.perfil_id) {
      throw new Error('El usuario no tiene un perfil asignado')
    }
    
    const promesas = []
    
    for (const [aplicacionId, permisosCrud] of Object.entries(permisos)) {
      // Solo guardar si al menos un permiso está activo
      if (permisosCrud.consultar || permisosCrud.ingresar || permisosCrud.modificar || permisosCrud.eliminar) {
        const payload = {
          USU_ID: usuarioId,
          APL_ID: parseInt(aplicacionId),
          UAP_CONSULTAR: permisosCrud.consultar || false,
          UAP_INGRESAR: permisosCrud.ingresar || false,
          UAP_MODIFICAR: permisosCrud.modificar || false,
          UAP_ELIMINAR: permisosCrud.eliminar || false
        }

        // Crear o actualizar permisos personalizados del usuario
        promesas.push(
          request('usuarios/usuario-aplicaciones', {
            method: 'POST',
            body: JSON.stringify(payload)
          }).catch(err => {
            console.warn(`Error al guardar permiso para aplicación ${aplicacionId}:`, err)
          })
        )
      }
    }
    
    await Promise.all(promesas)
  } catch (error) {
    console.error(`Error al guardar permisos del usuario ${usuarioId}:`, error)
    throw error
  }
}

export default {
  obtenerUsuarios,
  obtenerUsuario,
  crearUsuario,
  actualizarUsuario,
  cambiarEstadoUsuario,
  eliminarUsuario,
  obtenerPerfiles,
  obtenerAplicaciones,
  obtenerPermisosDelPerfil,
  obtenerPermisosDelUsuario,
  guardarPermisosUsuario
}
