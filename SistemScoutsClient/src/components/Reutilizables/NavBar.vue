<script setup>
import { ref } from 'vue'
import logoSrc from '@/assets/Logo_Boyscout_Chile.png' // asegúrate de que el archivo exista

// Estado reactivo del menú (para móviles)
const menuActive = ref(false)
</script>

<template>
  <nav class="navbar">
    <!-- Logo y título -->
    <div class="navbar-left">
      <img :src="logoSrc" alt="Logo Scouts" class="logo" />
      <span class="title">Sistema Scouts Región del Biobío</span>
    </div>

    <!-- Enlaces de navegación -->
    <ul :class="['navbar-links', { active: menuActive }]">
      <li><a href="#">Inicio</a></li>
      <li><a href="#">Panel de Control</a></li>
      <li><a href="#">Usuarios y Roles</a></li>
      <li><a href="#">Cursos y Capacitaciones</a></li>
      <li><a href="#">Inscripciones</a></li>
      <li><a href="#">Gestión de Personas</a></li>
      <li><a href="#">Pagos</a></li>
      <li><a href="#">Envío de Correos</a></li>
      <li><a href="#">Reportes</a></li>
      <li><a href="#">Acreditación QR</a></li>
    </ul>

    <!-- Botón para menú móvil -->
    <button 
      class="navbar-menu" 
      @click="menuActive = !menuActive" 
      aria-label="Alternar menú">
      ☰
    </button>
  </nav>
</template>

<style scoped>
/* ====== Barra de navegación ====== */
.navbar {
  background: #2c5aa0; /* Azul institucional Scouts */
  color: white;
  padding: 14px 26px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  font-family: "Segoe UI", Arial, sans-serif;
}

/* ====== Sección izquierda ====== */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 18px;
}

.logo {
  width: 60px;          /* 🔹 Tamaño aumentado del logo */
  height: 60px;         /* 🔹 */
  border-radius: 50%;
  border: 3px solid #ffcc00; /* Amarillo brillante */
  background: white;
  object-fit: cover;
  box-shadow: 0 3px 6px rgba(0,0,0,0.18);
}

.title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 0.6px;
}

/* ====== Enlaces ====== */
.navbar-links {
  display: flex;
  gap: 26px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar-links a {
  font-weight: 600;
  text-decoration: none;
  color: white;
  transition: color 0.3s, border-bottom 0.3s;
  border-bottom: 2px solid transparent;
}

.navbar-links a:hover {
  color: #ffcc00;
  border-bottom: 2px solid #ffcc00;
}

/* ====== Botón móvil ====== */
.navbar-menu {
  display: none;
  background: #ffcc00;
  color: #2c5aa0;
  font-size: 1.6rem;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  margin-left: 14px;
}

/* ====== Modo responsive ====== */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 15px 20px;
  }

  .navbar-links {
    flex-direction: column;
    gap: 10px;
    width: 100%;
    display: none;
    margin-top: 12px;
  }

  .navbar-links.active {
    display: flex;
  }

  .navbar-menu {
    display: block;
    align-self: flex-end;
  }
}
</style>
