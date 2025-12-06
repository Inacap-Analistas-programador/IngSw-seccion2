import { request } from './apiClient.js'

export default {
  // Corresponds to backend view `qr_token` in ApiCoreScouts.Api_Views.auth_views
  async qr_token(payload = {}) {
    return request('personas/qr-token', { method: 'POST', body: JSON.stringify(payload) })
  },

  // Corresponds to backend view `qr_email` in ApiCoreScouts.Api_Views.auth_views
  async qr_email(payload = {}) {
    return request('personas/qr-email', { method: 'POST', body: JSON.stringify(payload) })
  },

  // Extras: manual accreditation endpoints
  // Use the generic personas list endpoint for search (GET /api/personas/personas?search=term)
  async acreditacion_manual_search(term = '') {
    const q = encodeURIComponent(String(term || '').trim())
    return request(`personas/personas${q ? `?search=${q}` : ''}`)
  },

  // Keep acreditar endpoint as POST (existing backend view)
  async acreditacion_manual_acreditar(payload = {}) {
    return request('personas/acreditacion_manual_acreditar', { method: 'POST', body: JSON.stringify(payload) })
  }
}
