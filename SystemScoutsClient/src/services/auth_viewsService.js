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

  // Extras: manual accreditation endpoints (same names as backend views)
  async acreditacion_manual_search(payload = {}) {
    return request('personas/acreditacion_manual_search', { method: 'POST', body: JSON.stringify(payload) })
  },

  async acreditacion_manual_acreditar(payload = {}) {
    return request('personas/acreditacion_manual_acreditar', { method: 'POST', body: JSON.stringify(payload) })
  }
}
