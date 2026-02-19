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

  // Endpoint optimizado para búsqueda manual
  async acreditacion_manual_search(term = '', curso_id = null) {
    const params = new URLSearchParams()
    if (term) params.append('search', term)
    if (curso_id) params.append('curso_id', curso_id)

    return request(`personas/personas/search_acreditacion/?${params.toString()}`)
  },

  // Keep acreditar endpoint as POST (existing backend view)
  async acreditacion_manual_acreditar(payload = {}) {
    return request('personas/personas/acreditacion_manual_acreditar/', { method: 'POST', body: JSON.stringify(payload) })
  }
}
