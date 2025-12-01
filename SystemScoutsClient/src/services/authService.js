const API_URL = (import.meta.env?.VITE_API_BASE || 'http://127.0.0.1:8000').replace(/\/api\/?$/, '');

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
    if (!token) return null;

    try {
      // Decodificar payload JWT (base64url)
      const parts = token.split('.');
      if (parts.length < 2) return null;
      const payloadB64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
      const padded = payloadB64.padEnd(payloadB64.length + (4 - (payloadB64.length % 4)) % 4, '=');
      const json = atob(padded);
      const payload = JSON.parse(json);

      // Preferir claims personalizados del backend (USU_ID, USU_USERNAME)
      const id = payload.USU_ID || payload.user_id || payload.id || null;
      const username = payload.USU_USERNAME || payload.username || payload.sub || null;
      const name = payload.name || username || 'Usuario';
      // Map role from token payload if backend includes 'perfil'
      const role = (payload.perfil && payload.perfil.PEL_DESCRIPCION) ? payload.perfil.PEL_DESCRIPCION : (payload.perfil && payload.perfil.PEL_DESCRIPCION) || null;
      // avatar may not be included in token; prefer USU_RUTA_FOTO if present
      const avatarUrl = payload.USU_RUTA_FOTO || payload.avatarUrl || null;

      return {
        id,
        username,
        name,
        role,
        avatarUrl,
        payload
      };
    } catch (e) {
      console.warn('No se pudo decodificar token JWT en getCurrentUser:', e);
      return null;
    }
  }
};