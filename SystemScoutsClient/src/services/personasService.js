import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

// Exportaciones CON prefijo 'personas/' (para componentes actuales como Gestionpersonas.vue)
export const personas = makeCrud('personas/personas')
export const personasCompletas = makeCrud('personas/personas-completas')
export const grupos = makeCrud('personas/grupos')
export const formadores = makeCrud('personas/formadores')
export const individuales = makeCrud('personas/individuales')
export const niveles = makeCrud('personas/niveles')
export const personaCursos = makeCrud('personas/cursos')
export const estadoCursos = makeCrud('personas/estado-cursos')
export const vehiculos = makeCrud('personas/vehiculos')

// Exportaciones SIN prefijo (para otros componentes que lo necesiten)
export const personasSinPrefijo = makeCrud('personas')
export const personasCompletasSinPrefijo = makeCrud('personas-completas')
export const gruposSinPrefijo = makeCrud('grupos')
export const formadoresSinPrefijo = makeCrud('formadores')
export const individualesSinPrefijo = makeCrud('individuales')
export const nivelesSinPrefijo = makeCrud('niveles')
export const personaCursosSinPrefijo = makeCrud('cursos')
export const estadoCursosSinPrefijo = makeCrud('estado-cursos')
export const vehiculosSinPrefijo = makeCrud('vehiculos')

// ✨ Funciones auxiliares para obtener datos de filtros
export const obtenerRoles = async () => {
  try {
    const rolesSet = new Set();
    
    // Obtener de personas completas
    try {
      const data = await personasCompletas.list();
      data.forEach(persona => {
        if (persona.PER_ROL && persona.PER_ROL.trim() !== '') {
          rolesSet.add(persona.PER_ROL);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar roles desde personas-completas:', error.message);
    }
    
    // Obtener de formadores (tabla de relación)
    try {
      const formadoresData = await formadores.list();
      formadoresData.forEach(formador => {
        if (formador.rol || formador.FOR_ROL) {
          rolesSet.add(formador.rol || formador.FOR_ROL);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar roles desde formadores:', error.message);
    }
    
    const rolesUnicos = Array.from(rolesSet);
    console.log('Roles encontrados:', rolesUnicos);
    return rolesUnicos.map(rol => ({ value: rol, label: rol }));
  } catch (error) {
    console.warn('Error obteniendo roles:', error);
    return [];
  }
};

export const obtenerRamas = async () => {
  try {
    const ramasSet = new Set();
    
    // Obtener de personas completas
    try {
      const data = await personasCompletas.list();
      data.forEach(persona => {
        if (persona.PER_RAMA && persona.PER_RAMA.trim() !== '') {
          ramasSet.add(persona.PER_RAMA);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar ramas desde personas-completas:', error.message);
    }
    
    // Obtener de individuales (tabla de relación)
    try {
      const individualesData = await individuales.list();
      individualesData.forEach(individual => {
        if (individual.rama || individual.IND_RAMA) {
          ramasSet.add(individual.rama || individual.IND_RAMA);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar ramas desde individuales:', error.message);
    }
    
    const ramasUnicas = Array.from(ramasSet);
    console.log('Ramas encontradas:', ramasUnicas);
    return ramasUnicas.map(rama => ({ value: rama, label: rama }));
  } catch (error) {
    console.warn('Error obteniendo ramas:', error);
    return [];
  }
};

export const obtenerGrupos = async () => {
  try {
    const gruposSet = new Set();
    
    // Obtener de personas completas
    try {
      const data = await personasCompletas.list();
      data.forEach(persona => {
        if (persona.PER_GRUPO && persona.PER_GRUPO.trim() !== '') {
          gruposSet.add(persona.PER_GRUPO);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar grupos desde personas-completas:', error.message);
    }
    
    // Obtener de grupos (tabla de relación)
    try {
      const gruposData = await grupos.list();
      gruposData.forEach(grupo => {
        if (grupo.nombre || grupo.GRU_NOMBRE) {
          gruposSet.add(grupo.nombre || grupo.GRU_NOMBRE);
        }
      });
    } catch (error) {
      console.warn('No se pudieron cargar grupos desde tabla grupos:', error.message);
    }
    
    const gruposUnicos = Array.from(gruposSet);
    console.log('Grupos encontrados:', gruposUnicos);
    return gruposUnicos.map(grupo => ({ value: grupo, label: grupo }));
  } catch (error) {
    console.warn('Error obteniendo grupos:', error);
    return [];
  }
};

export default { 
  personas, 
  personasCompletas, 
  grupos, 
  formadores, 
  individuales, 
  niveles, 
  personaCursos, 
  estadoCursos, 
  vehiculos,
  obtenerRoles,
  obtenerRamas,
  obtenerGrupos,
  // Versiones sin prefijo también accesibles desde el objeto
  sinPrefijo: {
    personas: personasSinPrefijo,
    personasCompletas: personasCompletasSinPrefijo,
    grupos: gruposSinPrefijo,
    formadores: formadoresSinPrefijo,
    individuales: individualesSinPrefijo,
    niveles: nivelesSinPrefijo,
    personaCursos: personaCursosSinPrefijo,
    estadoCursos: estadoCursosSinPrefijo,
    vehiculos: vehiculosSinPrefijo,
  }
}
