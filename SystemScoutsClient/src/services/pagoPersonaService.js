import { request } from './apiClient'

// Service for Pago_Persona endpoints
// Backend route (per urls.py + router): /api/pagos/pago-persona/
const BASE = 'pagos/pago-persona'

function mapPagoPersona(item) {
  const persona = item.persona || {}
  const curso = item.curso || {}
  const nombre = [persona.PER_NOMBRES, persona.PER_APELPTA, persona.PER_APELMAT].filter(Boolean).join(' ').trim()
  const rut = persona.PER_RUN && persona.PER_DV ? `${persona.PER_RUN}-${persona.PER_DV}` : (persona.PER_RUN || '')
  return {
    id: item.PAP_ID,
    persona_id: item.PER_ID,
    curso_id: item.CUR_ID,
    usuario_id: item.USU_ID,
    valor_pagado: item.PAP_VALOR,
    fecha_pago: item.PAP_FECHA_HORA,
    observacion: item.PAP_OBSERVACION || '',
    // Nested friendly fields for UI
    nombre,
    rut,
    curso: curso.CUR_DESCRIPCION || curso.CUR_CODIGO || String(item.CUR_ID || ''),
    raw: item,
  }
}

export default {
  async listar(params = {}) {
    // Basic list; if you need filtering server-side, add query params here
    const data = await request(`${BASE}`)
    return Array.isArray(data) ? data.map(mapPagoPersona) : []
  },

  async obtener(id) {
    const item = await request(`${BASE}/${id}`)
    return mapPagoPersona(item)
  },

  async crear(payload) {
    // payload should include PER_ID, CUR_ID, USU_ID, PAP_FECHA_HORA, PAP_VALOR, PAP_OBSERVACION
    return request(`${BASE}`, { method: 'POST', body: JSON.stringify(payload) })
  },

  async actualizar(id, payload) {
    return request(`${BASE}/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
  },

  async eliminar(id) {
    return request(`${BASE}/${id}`, { method: 'DELETE' })
  }
}
