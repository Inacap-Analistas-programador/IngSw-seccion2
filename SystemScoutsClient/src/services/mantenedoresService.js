import { request } from './apiClient'

// Función genérica para crear endpoints CRUD
const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

// Exportaciones individuales CON prefijo (para Gestionpersonas.vue y otros componentes actuales)
export const conceptoContable = makeCrud('mantenedores/concepto-contable')
export const tipoCursos = makeCrud('mantenedores/tipo-cursos')
export const tipoArchivos = makeCrud('mantenedores/tipo-archivos')
export const alimentacion = makeCrud('mantenedores/alimentacion')
export const rol = makeCrud('mantenedores/rol')
export const cargo = makeCrud('mantenedores/cargo')
export const rama = makeCrud('mantenedores/rama')
export const estadoCivil = makeCrud('mantenedores/estado-civil')
export const nivel = makeCrud('mantenedores/nivel')
export const zona = makeCrud('mantenedores/zona')
export const distrito = makeCrud('mantenedores/distrito')
export const grupo = makeCrud('mantenedores/grupo')
export const region = makeCrud('mantenedores/region')
export const provincia = makeCrud('mantenedores/provincia')
export const comuna = makeCrud('mantenedores/comuna')

// Exportaciones SIN prefijo (para otros componentes que lo necesiten)
export const conceptoContableSinPrefijo = makeCrud('concepto-contable')
export const tipoCursosSinPrefijo = makeCrud('tipo-cursos')
export const tipoArchivosSinPrefijo = makeCrud('tipo-archivos')
export const alimentacionSinPrefijo = makeCrud('alimentacion')
export const rolSinPrefijo = makeCrud('rol')
export const cargoSinPrefijo = makeCrud('cargo')
export const ramaSinPrefijo = makeCrud('rama')
export const estadoCivilSinPrefijo = makeCrud('estado-civil')
export const nivelSinPrefijo = makeCrud('nivel')
export const zonaSinPrefijo = makeCrud('zona')
export const distritoSinPrefijo = makeCrud('distrito')
export const grupoSinPrefijo = makeCrud('grupo')
export const regionSinPrefijo = makeCrud('region')
export const provinciaSinPrefijo = makeCrud('provincia')
export const comunaSinPrefijo = makeCrud('comuna')

// Objeto unificado para exportar (con prefijo en la función list genérica)
const mantenedores = {
  list: (mantenedor) => request(`mantenedores/${mantenedor}`),
  conceptoContable,
  tipoCursos,
  tipoArchivos,
  alimentacion,
  rol,
  cargo,
  rama,
  estadoCivil,
  nivel,
  zona,
  distrito,
  grupo,
  region,
  provincia,
  comuna,
  // Versiones sin prefijo también accesibles desde el objeto
  sinPrefijo: {
    conceptoContable: conceptoContableSinPrefijo,
    tipoCursos: tipoCursosSinPrefijo,
    tipoArchivos: tipoArchivosSinPrefijo,
    alimentacion: alimentacionSinPrefijo,
    rol: rolSinPrefijo,
    cargo: cargoSinPrefijo,
    rama: ramaSinPrefijo,
    estadoCivil: estadoCivilSinPrefijo,
    nivel: nivelSinPrefijo,
    zona: zonaSinPrefijo,
    distrito: distritoSinPrefijo,
    grupo: grupoSinPrefijo,
    region: regionSinPrefijo,
    provincia: provinciaSinPrefijo,
    comuna: comunaSinPrefijo,
  }
}

export default mantenedores

