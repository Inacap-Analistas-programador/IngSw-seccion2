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
  max-width: 600px;
  margin: 0 auto;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
}

h2 {
  color: #555;
  margin-bottom: 15px;
  font-size: 1.3em;
  border-bottom: 2px solid #eee;
  padding-bottom: 5px;
  text-align: center;
}

.verification-result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  font-size: 1.4em; 
  font-weight: bold;
  min-height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.5s ease-in-out;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  text-align: center;
}
.rojo {
  background-color: #dc3545; 
}
.verde {
  background-color: #28a745; 
}

#texto_escaneado {
  margin-top: 15px;
  font-style: italic;
  text-align: center;
  color: #666;
}

/* Estilos responsivos */

#lector {
  min-height: 250px;
  width: 100%; 
  overflow: hidden; 
  border-radius: 8px;
  border: 1px solid #eee;
  
  /* Flexbox para ordenar el video y la UI */
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Estilos para el video y el canvas (el visor)
 se usa 'order' para asegurarnos de que el video aparezca primero */
#lector :deep(video),
#lector :deep(canvas) {
  width: 100% !important;
  height: auto !important;
  order: 1;
}

/* Estilos para la UI (botones y selector) que añade la librería */
#lector :deep(button),
#lector :deep(select) {
  width: 95%; 
  max-width: 400px; /* Un máximo para que no se vea gigante en tablets */
  padding: 10px;
  margin-top: 10px; 
  font-size: 0.9em;
  font-weight: bold;
  border-radius: 6px;
  border: 1px solid #ddd;
  box-sizing: border-box;
  order: 3; /* 3. Muestra los botones/selectores al final */
  background-color: #f8f8f8;
  cursor: pointer;
}

#lector :deep(button:hover) {
  background-color: #eee;
}

/* Estilos para los textos de estado */
#lector :deep(span) {
  text-align: center;
  font-size: 0.9em;
  color: #666;
  margin-top: 10px;
  padding: 5px;
  order: 2; /* Muestra el texto de estado después del video */
  width: 100%;
}


/* Media Query para pantallas pequeñas */
@media (max-width: 480px) {
  .verification-result {
    font-size: 1.1em;
    min-height: 60px;
  }
  h2 {
    font-size: 1.2em;
  }
  
  /* Botones y selectores un poco más pequeños en móviles */
  #lector :deep(button),
  #lector :deep(select) {
     font-size: 0.85em;
     padding: 8px;
  }
}
</style>