import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}${id}/`),
  create: (data) => request(base, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

export const proveedor = makeCrud('pagos/proveedor')
export const comprobantePago = makeCrud('pagos/comprobante-pago')
export const pagoComprobante = makeCrud('pagos/pago-comprobante')
export const pagoPersona = makeCrud('pagos/pago-persona')
export const prepago = makeCrud('pagos/prepago')

export default { proveedor, comprobantePago, pagoComprobante, pagoPersona, prepago }
