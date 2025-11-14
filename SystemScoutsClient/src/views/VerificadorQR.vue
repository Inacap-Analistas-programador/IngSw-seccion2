<template>
  <div class="verificador-container">
    <h2>Pantalla de Verificación</h2>
    <div id="lector" ref="lectorRef"></div>

    <div :class="['verification-result', resultadoClase]">
      {{ resultadoTexto }}
    </div>

    <p id="texto_escaneado">ID Escaneado: {{ idEscaneado }}</p>
  </div>
</template>

<script setup>
import {verificarUsuario} from '@/services/VerificadorService.js'

const { 
  resultadoTexto, 
  idEscaneado, 
  resultadoClase, 
  lectorRef 
} = verificarUsuario()
</script>


<style scoped>
/* Contenedor principal (basado en .roles-view) */
.verificador-container {
  max-width: 700px; 
  margin: 0 auto;
  padding: 1.5rem;
  width: 100%;
  box-sizing: border-box;
}

/* Título (basado en .page-header de Roles.vue y Usuarios.vue) */
h2 {
  font-size: 24px; /* */
  font-weight: 600; /* */
  color: #111827; /* */
  margin: 0;
  margin-bottom: 2rem; /* */
  padding-bottom: 1rem; /* */
  border-bottom: 2px solid #e0e0e0; /* */
  text-align: left; 
}

/* Caja del Lector (basado en .table-wrapper y .form-section) */
#lector {
  background: #fff; /* */
  border-radius: 8px; /* */
  box-shadow: 0 2px 8px rgba(0,0,0,.08); /* */
  overflow: hidden; 
  padding: 1rem;
  border: 1px solid #e0e0e0; /* */
  
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem; 
  min-height: 250px;
}

/* Caja de Resultado */
.verification-result {
  margin-top: 1.5rem; 
  padding: 1.25rem;
  border-radius: 8px; 
  font-size: 1.5em; 
  font-weight: 700; 
  min-height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease; 
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,.1); 
  border: 1px solid transparent;
}

/* Estilo .rojo (basado en el rojo de error de Usuarios.vue) */
.rojo {
  background-color: #e74c3c; /* */
  border-color: #c0392b;
}

/* Estilo .verde (basado en .badge-activo de Roles.vue) */
.verde {
  background-color: #27ae60; /* */
  border-color: #229954;
}

/* Texto de ID Escaneado (basado en .page-description) */
#texto_escaneado {
  margin-top: 1rem;
  font-size: 14px; /* */
  text-align: center;
  color: #6b7280; /* */
  font-style: normal; 
}

/* --- Estilos :deep() para la librería --- */

/* Video y Canvas */
#lector :deep(video),
#lector :deep(canvas) {
  width: 100% !important;
  height: auto !important;
  order: 1;
  border-radius: 6px; 
}

/* Texto de estado (ej: "Scanning") */
#lector :deep(span) {
  text-align: center;
  font-size: 0.9em;
  color: #6b7280; 
  margin-top: 0.5rem;
  padding: 5px;
  order: 2; 
  width: 100%;
}

/* Estilo para el SELECTOR DE CÁMARA (Estilo Secundario/Blanco) */
#lector :deep(select) {
  width: 98%; 
  max-width: 400px;
  padding: 0.75rem 1rem; 
  margin-top: 0.5rem; 
  font-size: 0.9rem;
  font-weight: 600; 
  border-radius: 8px; 
  border: 1px solid #d1d5db; 
  box-sizing: border-box;
  order: 3;
  background-color: #ffffff; 
  color: #1f2937; 
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); 
}

#lector :deep(select:hover) {
  background-color: #f9fafb; 
  border-color: #adb5bd;
}

/* Estilo para los BOTONES (Estilo Primario/Azul) */
#lector :deep(button) {
  width: 98%; 
  max-width: 400px;
  padding: 0.75rem 1rem; 
  margin-top: 0.5rem; 
  font-size: 0.9rem;
  font-weight: 600; 
  border-radius: 8px; 
  box-sizing: border-box;
  order: 3;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  
  /* --- ESTILOS DEL BOTÓN AZUL PRIMARIO --- */
  /* (Color tomado de los botones de tus otras pantallas) */
  background-color: #2563eb; 
  color: white; 
  border: 1px solid #2563eb; 
}

#lector :deep(button:hover) {
  /* (Color hover tomado de tus otras pantallas) */
  background-color: #1d4ed8; 
  border-color: #1d4ed8;
  transform: translateY(-1px); /* */
}

/* Media Query (Tu código original estaba bien) */
@media (max-width: 480px) {
  .verification-result {
    font-size: 1.1em;
    min-height: 60px;
  }
  h2 {
    font-size: 1.2em; 
  }
  
  #lector :deep(button),
  #lector :deep(select) {
     font-size: 0.85em;
     padding: 8px;
  }
}
</style>