const API_URL = 'http://127.0.0.1:8000';

export default {
  async login(username, password) {
    const response = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // Con AUTH_USER_MODEL=ApiCoreScouts.Usuario, el USERNAME_FIELD es 'USU_USERNAME'
      // SimpleJWT usa get_user_model().USERNAME_FIELD, por lo que el backend espera 'USU_USERNAME'
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
      // Guardar con dos claves para compatibilidad con el resto del frontend
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      localStorage.setItem('token', data.access);
    }

    return data;
  },

  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('token');
  },

  getAccessToken() {
    return localStorage.getItem('accessToken') || localStorage.getItem('token');
  },

  // Función temporal que devuelve datos básicos del usuario
  // TODO: reemplazar con llamada real al backend cuando esté disponible
  async getCurrentUser() {
    const token = this.getAccessToken();
    if (!token) {
      return null;
    }
    
    // Por ahora devolver usuario por defecto
    // En producción, hacer fetch a /api/user/ o similar
    return {
      name: 'Admin',
      role: 'Administrador',
      avatarUrl: null
    };
  }
};
