import { request } from './apiClient'

// Manual accreditation endpoints
// POST /api/personas/acreditacion/manual/search/  { term }
// POST /api/personas/acreditacion/manual/acreditar/  { rut | per_id }

function mapToParticipant(payload) {
  if (!payload || !payload.found) return null
  const p = payload.persona || {}
  const c = payload.curso || null
  return {
    name: p.nombre || 'Sin nombre',
    rut: p.rut || '',
    currentCourse: c?.descripcion || c?.codigo || '—',
    paymentStatus: payload.paymentStatus || 'Confirmado',
    acreditationStatus: payload.acreditado ? 'Acreditado' : 'Pendiente',
    paymentConfirmed: (payload.paymentStatus || 'Confirmado') === 'Confirmado',
    per_id: p.per_id,
    raw: payload,
  }
}

export default {
  async buscar(term) {
    const res = await request('personas/acreditacion/manual/search', {
      method: 'POST',
      body: JSON.stringify({ term })
    })
    return mapToParticipant(res)
  },

  async acreditar({ rut, per_id }) {
    const res = await request('personas/acreditacion/manual/acreditar', {
      method: 'POST',
      body: JSON.stringify({ rut, per_id })
    })
    return res && res.ok === true
  }
}
