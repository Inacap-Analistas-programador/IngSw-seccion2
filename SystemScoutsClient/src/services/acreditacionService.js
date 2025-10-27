import { request } from './apiClient'

// Datos mock para presentación
const MOCK_PERSONAS = [
  { nombre: 'Juan Pérez', rut: '12345678-9', curso: 'Curso Básico de Formación', acreditado: false, pagado: true, per_id: 1 },
  { nombre: 'María González', rut: '98765432-1', curso: 'Técnicas de Campamento', acreditado: true, pagado: true, per_id: 2 },
  { nombre: 'Pedro Silva', rut: '11223344-5', curso: 'Liderazgo Scout', acreditado: false, pagado: false, per_id: 3 },
  { nombre: 'Ana Martínez', rut: '55667788-9', curso: 'Curso Básico de Formación', acreditado: false, pagado: true, per_id: 4 }
]

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
    try {
      const res = await request('personas/acreditacion/manual/search', {
        method: 'POST',
        body: JSON.stringify({ term })
      })
      return mapToParticipant(res)
    } catch (e) {
      console.warn('Búsqueda falla, usando mock:', e)
      // Buscar en mock por rut o nombre
      const found = MOCK_PERSONAS.find(p => 
        p.rut.includes(term) || 
        p.nombre.toLowerCase().includes(term.toLowerCase())
      )
      if (!found) return null
      return {
        name: found.nombre,
        rut: found.rut,
        currentCourse: found.curso,
        paymentStatus: found.pagado ? 'Confirmado' : 'Pendiente',
        acreditationStatus: found.acreditado ? 'Acreditado' : 'Pendiente',
        paymentConfirmed: found.pagado,
        per_id: found.per_id,
        raw: found
      }
    }
  },

  async acreditar({ rut, per_id }) {
    try {
      const res = await request('personas/acreditacion/manual/acreditar', {
        method: 'POST',
        body: JSON.stringify({ rut, per_id })
      })
      return res && res.ok === true
    } catch (e) {
      console.warn('Acreditación falla, simulando éxito:', e)
      return true // Simular éxito en presentación
    }
  }
}
