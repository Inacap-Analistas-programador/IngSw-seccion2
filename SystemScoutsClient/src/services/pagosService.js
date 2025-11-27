import { request } from './apiClient'

const makeCrud = base => ({
  list: (params) => {
    if (!params || Object.keys(params).length === 0) return request(base)
    const sp = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') sp.append(k, String(v))
    })
    return request(`${base}${sp.toString() ? `?${sp.toString()}` : ''}`)
  },
  get: (id) => request(`${base}${id}/`),
  // Detectar FormData y no serializarlo. request() maneja FormData correctamente.
  create: (data) => request(base, { method: 'POST', body: data instanceof FormData ? data : JSON.stringify(data) }),
  update: (id, data) => request(`${base}${id}/`, { method: 'PUT', body: data instanceof FormData ? data : JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}${id}/`, { method: 'PATCH', body: data instanceof FormData ? data : JSON.stringify(data) }),
  remove: (id) => request(`${base}${id}/`, { method: 'DELETE' }),
})

export const proveedor = makeCrud('pagos/proveedor')
export const comprobantePago = makeCrud('pagos/comprobante-pago')
export const pagoComprobante = makeCrud('pagos/pago-comprobante')
export const pagoPersona = makeCrud('pagos/pago-persona')
export const prepago = makeCrud('pagos/prepago')

// Alias histórico/usado por la vista: `pagos` apunta a `pagoPersona`.
// Además añadimos un helper `createMasivo` que llama al action backend `pago-persona/masivo/`.
const pagos = {
  ...pagoPersona,
  createMasivo: (data) => request('pagos/pago-persona/masivo/', { method: 'POST', body: data })
}

export default { proveedor, comprobantePago, pagoComprobante, pagoPersona, prepago, pagos }
