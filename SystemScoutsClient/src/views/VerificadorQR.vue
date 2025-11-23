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
/* Contenedor principal */
.verificador-container {
  max-width: 700px; 
  margin: 0 auto;
  padding: 1.5rem;
  width: 100%;
  box-sizing: border-box;
  /* Evita que el contenedor cause scroll horizontal */
  overflow-x: hidden;
}

/* Título */
h2 {
  font-size: 24px; 
  font-weight: 600; 
  color: #111827; 
  margin: 0;
  margin-bottom: 2rem; 
  padding-bottom: 1rem; 
  border-bottom: 2px solid #e0e0e0; 
  text-align: left; 
  /* Ajuste responsivo para el texto */
  word-wrap: break-word;
}

/* Caja del Lector */
#lector {
  background: #fff; 
  border-radius: 8px; 
  box-shadow: 0 2px 8px rgba(0,0,0,.08); 
  /* Overflow hidden recorta cualquier cosa que se salga */
  overflow: hidden; 
  padding: 1rem;
  border: 1px solid #e0e0e0; 
  
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem; 
  min-height: 250px;
  
  /* Asegura que el lector nunca sea más ancho que su padre */
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
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
  /* Ajuste responsivo */
  width: 100%;
  box-sizing: border-box;
}

.rojo {
  background-color: #e74c3c; 
  border-color: #c0392b;
}

.verde {
  background-color: #27ae60;
  border-color: #229954;
}

#texto_escaneado {
  margin-top: 1rem;
  font-size: 14px; 
  text-align: center;
  color: #6b7280; 
  font-style: normal; 
  /* Evita que un ID muy largo rompa el diseño */
  word-break: break-all;
}

/* Forzamos que video, imagen y canvas nunca excedan el 100% */
#lector :deep(video),
#lector :deep(canvas),
#lector :deep(img) {
  max-width: 100% !important;
  height: auto !important;
  order: 1;
  border-radius: 6px; 
  object-fit: cover; /* Asegura que el video llene el espacio sin estirarse */
}

/* Esto lo fuerza a adaptarse a la pantalla */
#lector :deep(div) {
  max-width: 100% !important;
  box-sizing: border-box;
}

#lector :deep(span) {
  text-align: center;
  font-size: 0.9em;
  color: #6b7280; 
  margin-top: 0.5rem;
  padding: 5px;
  order: 2; 
  width: 100%;
  display: block;
}

/* Estilo para el selector de cámara */
#lector :deep(select) {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236B7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center; 
  background-size: 1.25em; 
  padding-right: 2.5rem !important; 

  /* Cambiado width fijo por 100% relativo al padre */
  width: 100%; 
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
  /* Evita que el texto largo se salga */
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}

#lector :deep(select:hover) {
  background-color: #f9fafb; 
  border-color: #adb5bd;
}

/* Estilo para los botones */
#lector :deep(button) {
  /* Cambiado width fijo por 100% relativo al padre */
  width: 100%; 
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
  background-color: #2563eb; 
  color: white; 
  border: 1px solid #2563eb; 
}

#lector :deep(button:hover) {
  background-color: #1d4ed8; 
  border-color: #1d4ed8;
  transform: translateY(-1px); 
}

/* Media Query - Ajustes para móviles pequeños */
@media (max-width: 480px) {
  .verificador-container {
    padding: 1rem; /* Menos padding en bordes */
  }

  .verification-result {
    font-size: 1.1em;
    min-height: 60px;
    padding: 1rem;
  }
  
  h2 {
    font-size: 1.2em; 
    margin-bottom: 1.5rem;
  }
  
  #lector {
    padding: 0.5rem; /* Menos espacio interno en móvil para aprovechar pantalla */
  }

  #lector :deep(button),
  #lector :deep(select) {
     font-size: 0.85em;
     padding: 10px; /* Botones un poco más fáciles de presionar */
     padding-right: 2rem !important;
     background-position: right 0.5rem center;
  }
}
</style>