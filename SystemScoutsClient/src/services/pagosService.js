import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  // create/update helpers: if data is FormData, pass it directly so apiClient
  // doesn't set Content-Type and allows file uploads. Otherwise stringify JSON.
  create: (data) => {
    const opts = { method: 'POST' }
    if (data instanceof FormData) opts.body = data
    else opts.body = JSON.stringify(data)
    return request(base, opts)
  },
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
})

export const proveedor = makeCrud('pagos/proveedor')
export const comprobantePago = makeCrud('pagos/comprobante-pago')
export const pagoComprobante = makeCrud('pagos/pago-comprobante')
export const pagoPersona = makeCrud('pagos/pago-persona')
export const prepago = makeCrud('pagos/prepago')

// Add a compatibility alias `pagos` used by older components (e.g. PagosView.vue)
// and provide a couple of convenience methods the UI expects.
const pagos = {
  ...pagoPersona,
  // Bulk create endpoint — the backend may implement a custom route for this.
  createMasivo: (data) => {
    // Try a dedicated endpoint first, fallback to regular create
    try {
      return request('pagos/pago-persona/masivo/', { method: 'POST', body: data instanceof FormData ? data : JSON.stringify(data) })
    } catch (e) {
      return pagoPersona.create(data)
    }
  },
  // Transfer helper — UI expects this; backend should provide an endpoint.
  transferir: (payload) => request('pagos/pago-persona/transferir/', { method: 'POST', body: JSON.stringify(payload) })
}

export default { proveedor, comprobantePago, pagoComprobante, pagoPersona, prepago, pagos }
