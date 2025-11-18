import { apiClient } from './apiClient';

const makeCrud = base => ({
  list: (params) => apiClient.request(`${base}${params ? `?${new URLSearchParams(params)}` : ''}`),
  get: (id) => apiClient.request(`${base}/${id}/`),
  create: (data) => apiClient.request(base, { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => apiClient.request(`${base}/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
    partialUpdate: (id, data) => apiClient.request(`${base}/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    remove: (id) => apiClient.request(`${base}/${id}/`, { method: 'DELETE' }),
});




