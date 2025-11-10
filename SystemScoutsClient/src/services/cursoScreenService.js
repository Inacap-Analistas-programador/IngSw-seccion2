// src/services/cursoScreenService.js
// Servicio especializado para la pantalla CRUD de Cursos
// Desacopla la lógica de carga, añade caché, fallback local y normalización

import { cursos, fechas, secciones, coordinadores as coordinadoresSrv, formadores as formadoresSrv } from './cursosService'
import { personas as personasSrv, personaCursos as personaCursosSrv } from './personasService'
import { request } from './apiClient'
import { mockCursos, mockTiposCurso, mockPersonas, mockSecciones } from './mockData'

// TTL en ms para data "semi-estática" (personas, tipos curso)
const TTL = 5 * 60 * 1000 // 5 minutos

function now() { return Date.now() }

function readCache(key) {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) return null
    const obj = JSON.parse(raw)
    if (!obj.expires || obj.expires < now()) {
      localStorage.removeItem(key)
      return null
    }
    return obj.data
  } catch { return null }
}

function writeCache(key, data, ttl = TTL) {
  try {
    localStorage.setItem(key, JSON.stringify({ data, expires: now() + ttl }))
  } catch {}
}

async function safeList(fn, { fallback = [], cacheKey, useCache = true } = {}) {
  if (useCache && cacheKey) {
    const c = readCache(cacheKey)
    if (c) return c
  }
  try {
    const data = await fn()
    // Unwrap DRF paginated responses { count, results, ... }
    const arr = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : null)
    if (arr) {
      if (cacheKey) writeCache(cacheKey, arr)
      return arr
    }
    return fallback
  } catch (e) {
    console.warn(`[cursoScreenService] Error list(${cacheKey || 'no-key'}):`, e)
    return fallback
  }
}

export async function loadCursos() {
  return safeList(() => cursos.list(), { fallback: mockCursos })
}
export async function loadFechas() {
  return safeList(() => fechas.list(), { fallback: [] })
}
export async function loadSecciones() {
  return safeList(() => secciones.list(), { fallback: mockSecciones })
}
export async function loadPersonas() {
  // Personas pueden ser grandes: limitar a primeras 500 para combos
  return safeList(() => personasSrv.list(), { fallback: mockPersonas, cacheKey: 'cache.personas' })
}
export async function loadTiposCurso() {
  // Usar el prefijo correcto de mantenedores para evitar dependencias cruzadas
  const fetchTipos = () => request('mantenedores/tipo-cursos')
  return safeList(fetchTipos, { fallback: mockTiposCurso, cacheKey: 'cache.tiposCurso' })
}

export async function loadComunas() {
  const fetcher = () => request('mantenedores/comuna')
  return safeList(fetcher, { fallback: [], cacheKey: 'cache.comunas' })
}
export async function loadCargos() {
  const fetcher = () => request('mantenedores/cargo')
  return safeList(fetcher, { fallback: [], cacheKey: 'cache.cargos' })
}
export async function loadRamas() {
  const fetcher = () => request('mantenedores/rama')
  return safeList(fetcher, { fallback: [], cacheKey: 'cache.ramas' })
}
export async function loadRoles() {
  const fetcher = () => request('mantenedores/rol')
  return safeList(fetcher, { fallback: [], cacheKey: 'cache.roles' })
}
export async function loadCoordinadores() {
  return safeList(() => coordinadoresSrv.list(), { fallback: [], cacheKey: 'cache.coordinadores' })
}
export async function loadFormadores() {
  return safeList(() => formadoresSrv.list(), { fallback: [], cacheKey: 'cache.formadores' })
}
export async function loadPersonaCursos() {
  return safeList(() => personaCursosSrv.list(), { fallback: [], cacheKey: 'cache.personaCursos' })
}

// Cargas livianas por curso (prefiere endpoints filtrados en backend)
export async function loadCoordinadoresByCurso(curId) {
  return safeList(() => coordinadoresSrv.list({ CUR_ID: curId }), { fallback: [], cacheKey: `cache.coordinadores.cur_${curId}` })
}
export async function loadFormadoresByCurso(curId) {
  return safeList(() => formadoresSrv.list({ CUR_ID: curId }), { fallback: [], cacheKey: `cache.formadores.cur_${curId}` })
}
export async function loadPersonaCursosByCurso(curId) {
  return safeList(() => personaCursosSrv.list({ CUR_ID: curId }), { fallback: [], cacheKey: `cache.personaCursos.cur_${curId}` })
}

export async function loadAllData() {
  // Carga inicial: evita grandes colecciones (coordinadores/formadores/persona-cursos)
  const [cursosData, fechasData, seccionesData, personasData, tiposCursoData, comunasData, cargosData, ramasData, rolesData] = await Promise.all([
    loadCursos(),
    loadFechas(),
    loadSecciones(),
    loadPersonas(),
    loadTiposCurso(),
    loadComunas(),
    loadCargos(),
    loadRamas(),
    loadRoles(),
  ])
  return { cursosData, fechasData, seccionesData, personasData, tiposCursoData, comunasData, cargosData, ramasData, rolesData }
}

// Helpers de mapeo centralizados
export function getPersonaNombre(p) {
  if (!p) return 'No asignado'
  // Normalizar nombres según backend y mock
  const nombre = p.PER_NOMBRES || p.PER_NOMBRE || ''
  const apellido = p.PER_APELPTA || p.PER_APELLIDO_PATERNO || ''
  return `${nombre} ${apellido}`.trim() || 'Sin nombre'
}
export function getTipoCursoNombre(t) {
  if (!t) return 'No definido'
  return t.TCU_DESCRIPCION || 'Sin descripción'
}

// Estados centralizados para evitar hardcode repetido
export const estadosCurso = [
  { value: 1, text: 'Vigente' },
  { value: 0, text: 'No Vigente' },
  { value: 2, text: 'Deshabilitado' },
]
export function estadoText(v) { return estadosCurso.find(e => e.value === v)?.text || 'Desconocido' }
export function estadoClass(v) {
  switch (v) {
    case 1: return 'badge-success'
    case 0: return 'badge-warning'
    case 2: return 'badge-danger'
    default: return 'badge-secondary'
  }
}

export default {
  loadAllData,
  loadCursos,
  loadFechas,
  loadSecciones,
  loadPersonas,
  loadTiposCurso,
  loadComunas,
  loadCargos,
  loadRamas,
  loadRoles,
  loadCoordinadores,
  loadFormadores,
  loadPersonaCursos,
  loadCoordinadoresByCurso,
  loadFormadoresByCurso,
  loadPersonaCursosByCurso,
  getPersonaNombre,
  getTipoCursoNombre,
  estadosCurso,
  estadoText,
  estadoClass,
}
