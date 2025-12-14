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
export const personasCompletas = makeCrud('personas/personas') // Usar el mismo endpoint que personas
export const grupos = makeCrud('personas/grupos')
export const formadores = makeCrud('personas/formadores')
export const individuales = makeCrud('personas/individuales')
export const niveles = makeCrud('personas/niveles')
// Alias históricos esperados por algunos componentes
export const personaCursos = makeCrud('personas/cursos')
export const estadoCursos = makeCrud('personas/estado-cursos')
export const vehiculos = makeCrud('personas/vehiculos')

// Exportaciones SIN prefijo (para otros componentes que lo necesiten)
export const personasSinPrefijo = makeCrud('personas')
export const personasCompletasSinPrefijo = makeCrud('personas') // Usar el mismo endpoint
export const gruposSinPrefijo = makeCrud('grupos')
export const formadoresSinPrefijo = makeCrud('formadores')
export const individualesSinPrefijo = makeCrud('individuales')
export const nivelesSinPrefijo = makeCrud('niveles')
export const personaCursosSinPrefijo = makeCrud('cursos')
export const estadoCursosSinPrefijo = makeCrud('estado-cursos')
export const vehiculosSinPrefijo = makeCrud('vehiculos')

// ✨ NUEVAS EXPORTACIONES PARA FORMULARIO 2.VUE
// Estas son las exportaciones específicas que necesita Formulario 2.vue
export const personaGrupos = makeCrud('personas/grupos') // Reutiliza el endpoint de grupos
export const personaNiveles = makeCrud('personas/niveles') // Reutiliza el endpoint de niveles
export const personaIndividuales = makeCrud('personas/individuales') // Reutiliza el endpoint de individuales

// Nota: personaCursos ya está exportado arriba, así que no necesita duplicarse

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
  // NUEVAS EXPORTACIONES PARA FORMULARIO 2.VUE
  personaGrupos,
  personaNiveles,
  personaIndividuales,
  obtenerRoles,
  obtenerRamas,
  obtenerGrupos,
  // Orquestador: crear Persona -> Persona_Curso -> Persona_Vehiculo
  createPersonaWithCourseAndVehicle: async ({ personaData, cursoData = null, vehiculoData = null, formadorData = null, ramasData = null, grupoData = null }) => {
    // 1) Crear persona
    const personaCreada = await personas.create(personaData);

    let personaCursoCreado = null;
    let vehiculoCreado = null;
    let formadorCreado = null;
    let grupoCreado = null;
    let ramasCreadas = [];

    // Validar ID de persona (puede venir como per_id o PER_ID según serializador)
    const perId = personaCreada.per_id || personaCreada.PER_ID;

    // 2) Si se solicita crear curso (Persona_Curso)
    if (cursoData && cursoData.cus_id && cursoData.rol_id) {
      const cursoPayload = {
        per_id: perId,
        cus_id: Number(cursoData.cus_id),
        rol_id: Number(cursoData.rol_id)
      };
      // Incluir ali_id si fue provisto
      if (cursoData.ali_id) {
        cursoPayload.ali_id = Number(cursoData.ali_id);
      }
      // Incluir niv_id si fue provisto
      if (cursoData.niv_id) {
        cursoPayload.niv_id = Number(cursoData.niv_id);
      }

      try {
        personaCursoCreado = await personaCursos.create(cursoPayload);
      } catch (err) {
        // Propagar información pero continuar
        console.warn(`Error creando Persona_Curso: ${err && err.message ? err.message : err}`);
        // No lanzamos error fatal porque queremos intentar guardar lo demás
      }
    }

    // 3) Si se solicita crear vehículo
    if (vehiculoData) {
      // Necesitamos pec_id. Puede venir de personaCursoCreado (si se creó recién) o de input si ya existía (no es el caso común aquí)
      const pecId = (personaCursoCreado && (personaCursoCreado.pec_id || personaCursoCreado.PEC_ID)) || vehiculoData.pec_id || null;

      if (pecId) {
        const vehPayload = {
          pec_id: pecId,
          pev_patente: vehiculoData.pev_patente,
          pev_marca: vehiculoData.pev_marca || '',
          pev_modelo: vehiculoData.pev_modelo || ''
        };

        try {
          vehiculoCreado = await vehiculos.create(vehPayload);
        } catch (err) {
          console.warn(`Error creando Persona_Vehiculo: ${err}`);
        }
      } else {
        console.warn('No se pudo crear vehículo: falta PEC_ID (curso no creado o falló)');
      }
    }

    // 4) Si se solicita crear datos de Formador (Persona_Formador)
    if (formadorData) {
      const formadorPayload = {
        per_id: perId,
        pef_hab_1: formadorData.pef_hab_1 || false,
        pef_hab_2: formadorData.pef_hab_2 || false,
        pef_verif: formadorData.pef_verif || false,
        pef_historial: formadorData.pef_historial || ''
      };

      try {
        formadorCreado = await formadores.create(formadorPayload);
      } catch (err) {
        console.warn("Error creando Formador:", err);
      }
    }

    // 5) Si se solicitan Ramas (Persona_Nivel)
    if (ramasData && Array.isArray(ramasData) && ramasData.length > 0) {
      for (const rama of ramasData) {
        const ramaPayload = {
          per_id: perId,
          niv_id: rama.niv_id,
          ram_id: rama.ram_id
        };
        try {
          const res = await personaNiveles.create(ramaPayload);
          ramasCreadas.push(res);
        } catch (err) {
          console.warn(`Error creando Rama (Nivel ${rama.niv_id}, ID ${rama.ram_id}):`, err);
        }
      }
    }

    // 6) Si se solicita crear Grupo (Persona_Grupo)
    if (grupoData && grupoData.gru_id) {
      const grupoPayload = {
        per_id: perId,
        gru_id: grupoData.gru_id,
        peg_vigente: grupoData.peg_vigente !== undefined ? grupoData.peg_vigente : true
      };
      try {
        grupoCreado = await personaGrupos.create(grupoPayload);
      } catch (err) {
        console.warn("Error creando Persona_Grupo:", err);
      }
    }

    // 7) Crear estado inicial curso (Persona_Estado_Curso)
    // Estado 1 = Pre Inscrito (según modelo)
    if (personaCursoCreado && personaCursoCreado.pec_id) {
      try {
        await estadoCursos.create({
          usu_id: personaData.usu_id, // Same user who created persona
          pec_id: personaCursoCreado.pec_id,
          peu_estado: 1, // Pre Inscrito
          peu_vigente: true
        });
      } catch (err) {
        console.warn("Error creando Estado inicial de Curso:", err);
      }
    }

    return {
      persona: personaCreada,
      personaCurso: personaCursoCreado,
      vehiculo: vehiculoCreado,
      formador: formadorCreado,
      ramas: ramasCreadas,
      grupo: grupoCreado
    };
  },
  // Método personalizado para obtener cursos de una persona
  obtenerCursosPersona: (personaId) => request(`personas/personas/${personaId}/cursos/`),
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