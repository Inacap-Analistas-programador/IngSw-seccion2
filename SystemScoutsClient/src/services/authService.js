const API_URL = 'http://127.0.0.1:8000';

export default {
  async login(username, password) {
    const response = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ USU_USERNAME: username, password })
    });

    // Leer el body una sola vez
    const text = await response.text(); // siempre funciona
    let data;
    try {
      data = JSON.parse(text); // intenta parsear como JSON
    } catch (e) {
      console.error('No JSON received:', text);
      throw new Error('Respuesta inesperada del servidor');
    }

    if (!response.ok) {
      throw new Error(data.detail || 'Error al iniciar sesión');
    }

    if (data.access) {
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
    }

    return data;
  },

  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  getAccessToken() {
    return localStorage.getItem('accessToken');
  }
};
