import apiClient from './apiClient';

const cursosService = {
  getCursos() {
    return apiClient.get('/cursos/');
  },
  getCurso(id) {
    return apiClient.get(`/cursos/${id}/`);
  },
  createCurso(data) {
    return apiClient.post('/cursos/', data);
  },
  updateCurso(id, data) {
    return apiClient.put(`/cursos/${id}/`, data);
  },
  deleteCurso(id) {
    return apiClient.delete(`/cursos/${id}/`);
  },
  // Aquí se pueden añadir más llamadas a los otros endpoints si es necesario
  // Por ejemplo, para gestionar coordinadores, fechas, etc.
  getCoordinadores(cursoId) {
    return apiClient.get(`/cursos/${cursoId}/coordinadores/`);
  },
  addCoordinador(cursoId, data) {
    return apiClient.post(`/cursos/${cursoId}/coordinadores/`, data);
  }
};

export default cursosService;
