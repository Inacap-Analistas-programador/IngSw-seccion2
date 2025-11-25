import { request } from './apiClient';

const makeCrud = base => ({
  list: (params) => request(`${base}/${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => request(`${base}/${id}/`),
  create: (data) => request(`${base}/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`${base}/${id}/`, { method: 'DELETE' }),
});

// Ajusta el endpoint base según tu backend
export const ramas = makeCrud('mantenedores/rama');

export default { ramas };
