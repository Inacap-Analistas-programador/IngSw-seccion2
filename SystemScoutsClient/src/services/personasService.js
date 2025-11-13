import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

// The API registers these resources under the 'personas' prefix (see API root).
export const personas = makeCrud('personas/personas')
export const grupos = makeCrud('personas/grupos')
export const formadores = makeCrud('personas/formadores')
export const individuales = makeCrud('personas/individuales')
export const niveles = makeCrud('personas/niveles')
export const personaCursos = makeCrud('personas/cursos') // persona-curso router registered under personas
export const estadoCursos = makeCrud('personas/estado-cursos')
export const vehiculos = makeCrud('personas/vehiculos')

// ✨ Funciones auxiliares para obtener datos de filtros
export const obtenerRoles = async () => {
  try {
    // Obtener personas completas y extraer roles únicos
    const data = await personasCompletas.list();
    const rolesUnicos = [...new Set(data
      .map(persona => persona.PER_ROL)
      .filter(rol => rol && rol.trim() !== '')
    )];
    
    console.log('🎭 Roles encontrados:', rolesUnicos);
    return rolesUnicos.map(rol => ({ value: rol, label: rol }));
  } catch (error) {
    console.warn('Error obteniendo roles:', error);
  }
};

export const obtenerRamas = async () => {
  try {
    // Obtener personas completas y extraer ramas únicas
    const data = await personasCompletas.list();
    const ramasUnicas = [...new Set(data
      .map(persona => persona.PER_RAMA)
      .filter(rama => rama && rama.trim() !== '')
    )];
    
    console.log('🌿 Ramas encontradas:', ramasUnicas);
    return ramasUnicas.map(rama => ({ value: rama, label: rama }));
  } catch (error) {
    console.warn('Error obteniendo ramas:', error);
  }
};

export const obtenerGrupos = async () => {
  try {
    // Obtener personas completas y extraer grupos únicos
    const data = await personasCompletas.list();
    const gruposUnicos = [...new Set(data
      .map(persona => persona.PER_GRUPO)
      .filter(grupo => grupo && grupo.trim() !== '')
    )];
    
    console.log('👥 Grupos encontrados:', gruposUnicos);
    return gruposUnicos.map(grupo => ({ value: grupo, label: grupo }));
  } catch (error) {
    console.warn('Error obteniendo grupos:', error);
  }
};

export default { 
  personas,
  grupos, 
  formadores, 
  individuales, 
  niveles, 
  personaCursos, 
  estadoCursos, 
  vehiculos,
  obtenerRoles,
  obtenerRamas,
  obtenerGrupos
}
