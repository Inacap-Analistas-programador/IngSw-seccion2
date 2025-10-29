import { request } from './apiClient'
import personasService from './personasService'

// Servicio específico para la Dashboard
// Centraliza las consultas necesarias y normaliza mínimamente los datos

function parseIntSafe(v, def = 0) {
  const n = parseInt(v, 10)
  return Number.isFinite(n) ? n : def
}

export async function obtenerCursosResumen() {
  const cursos = await request('cursos/cursos')
  if (!Array.isArray(cursos)) return []
  return cursos.map(c => ({
    id: c.CURS_ID || c.CUR_ID || c.id || c.ID,
    title: c.CUR_DESCRIPCION || c.CUR_CODIGO || c.CURS_ID || 'Curso',
    inscritos: parseIntSafe(c._inscritos_count ?? c.INSCRITOS ?? 0, 0),
    capacidad: parseIntSafe(
      c.CUR_COTA_CON_ALMUERZO ?? c.CUR_COTA_SIN_ALMUERZO ?? c.CUR_CANT_PARTICIPANTE ?? c.CAPACIDAD ?? 0,
      0
    ),
    valor: 0,
    estado: 1, // normalizamos a 1 como solicitaste previamente
  }))
}

export async function obtenerCuotasPorCurso() {
  const cuotas = await request('cursos/cuotas')
  if (!Array.isArray(cuotas)) return {}
  const byCourse = {}
  cuotas.forEach(q => {
    const curId = q.CUR_ID || q.curso_id || q.cur_id || null
    if (!curId) return
    const val = Number(q.CUU_VALOR || q.valor || 0)
    const date = q.CUU_FECHA || ''
    const prev = byCourse[curId]
    // Usamos la cuota de mayor valor o la más reciente, lo que aplique primero
    if (!prev || val > prev.val || (date && prev.date && date > prev.date)) {
      byCourse[curId] = { val, date }
    }
  })
  // Devuelve solo el valor por simplicidad
  const result = {}
  Object.keys(byCourse).forEach(id => { result[id] = byCourse[id].val })
  return result
}

export async function getTotalPersonas() {
  // Si en el backend hay un endpoint más eficiente (count), cámbialo aquí
  const personas = await personasService.obtenerPersonas()
  return Array.isArray(personas) ? personas.length : 0
}

export default {
  obtenerCursosResumen,
  obtenerCuotasPorCurso,
  getTotalPersonas,
}
