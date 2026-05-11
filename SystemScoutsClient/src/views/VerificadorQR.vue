<template>
  <div class="verificador-container">
    <PageHeader 
      title="App Verificador" 
      subtitle="Escanea el código QR de los participantes para validar su acreditación."
    />
    
    <div class="scanner-wrapper">
      <div id="lector" ref="lectorRef"></div>
      <!-- Overlay personalizado -->
      <div class="scanner-overlay">
        <div class="scanner-corners">
          <div class="corner top-left"></div>
          <div class="corner top-right"></div>
          <div class="corner bottom-left"></div>
          <div class="corner bottom-right"></div>
        </div>
        <div class="scanner-laser"></div>
      </div>
    </div>

    <div :class="['verification-result', resultadoClase]">
      <div v-if="resultadoClase === 'verde'" class="result-icon-box">
        <AppIcons name="check-circle" :size="28" stroke-width="2.5" />
      </div>
      <div v-else-if="resultadoClase === 'rojo'" class="result-icon-box">
        <AppIcons name="x-circle" :size="28" stroke-width="2.5" />
      </div>
      <div v-else class="result-icon-box idle">
        <AppIcons name="qrcode" :size="28" stroke-width="2" />
      </div>
      
      <span class="result-text">{{ resultadoTexto }}</span>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '@/components/common/PageHeader.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import {verificarUsuario} from '@/services/VerificadorService.js'

const { 
  resultadoTexto, 
  resultadoClase, 
  lectorRef 
} = verificarUsuario()
</script>


<style scoped>
/* Contenedor principal */
.verificador-container {
  max-width: 500px; /* Reducido de 600px */
  margin: 0 auto;
  padding: 1.5rem;
  width: 100%;
  box-sizing: border-box;
}

/* Título ya manejado por PageHeader, quitamos estilos de h2 */

/* Envoltura del escáner */
.scanner-wrapper {
  position: relative;
  width: 100%;
  max-width: 360px; /* Reducido de 500px para PC */
  aspect-ratio: 1 / 1; /* Forzamos que sea un cuadrado perfecto */
  margin: 0 auto;
  background: #f8fafc;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 0.5px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
}

#lector {
  width: 100% !important;
  height: 100% !important;
  border: none !important;
  background: transparent !important;
  overflow: hidden;
}

/* Caja de Resultado */
.verification-result {
  margin: 1.5rem auto 0;
  max-width: 360px;
  max-height: 62px;
  padding: 1rem;
  border-radius: 6px;
  /* min-height: 90px; */
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  color: #64748b;
  background: #f8fafc;
  text-align: left;
  box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
  border: 0.5px solid #e2e8f0;
  font-family: 'Inter', Arial, sans-serif;
}

.result-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.verde .result-icon-box { background: rgba(255, 255, 255, 0.2); }
.rojo .result-icon-box { background: rgba(255, 255, 255, 0.2); }
.idle { background: #f1f5f9; color: #94a3b8; }

.result-text {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.025em;
  text-transform: uppercase;
}


.verification-result.verde, .verification-result.rojo {
  color: white;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: none;
}

.rojo {
  background: #ef4444;
}

.verde {
  background: #22c55e;
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
  width: 100% !important;
  height: 100% !important;
  order: 1;
  border-radius: 6px; 
  object-fit: cover !important; 
  display: block;
}

/* Ocultar la región sombreada de la librería para usar nuestro overlay */
#lector :deep(#qr-shaded-region) {
  display: none !important;
}

/* Overlay Personalizado */
.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scanner-corners {
  position: relative;
  width: 80%; /* Sincronizado con el qrbox s = Math.min(w, h) * 0.8 */
  height: 80%;
}

.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 4px solid #fff;
  filter: drop-shadow(0 0 5px rgba(0,0,0,0.5));
}

.top-left { top: -2px; left: -2px; border-right: none; border-bottom: none; border-top-left-radius: 12px; }
.top-right { top: -2px; right: -2px; border-left: none; border-bottom: none; border-top-right-radius: 12px; }
.bottom-left { bottom: -2px; left: -2px; border-right: none; border-top: none; border-bottom-left-radius: 12px; }
.bottom-right { bottom: -2px; right: -2px; border-left: none; border-top: none; border-bottom-right-radius: 12px; }

.scanner-laser {
  position: absolute;
  width: 80%;
  height: 2px;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 15px 2px rgba(255, 255, 255, 0.6);
  z-index: 11;
  animation: scanning 2s ease-in-out infinite;
  opacity: 0.6;
}

@keyframes scanning {
  0%, 100% { top: 10%; }
  50% { top: 90%; }
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
  padding: 0.5rem 1rem; 
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

/* Esconder elementos innecesarios generados por la librería */
#lector :deep(img[alt="Info icon"]) { display: none !important; }
#lector :deep(img[alt="Camera menu icon"]) { display: none !important; }

/* Media Query - Ajustes para móviles pequeños */
@media (max-width: 480px) {
  .verificador-container {
    padding: 1rem; /* Menos padding en bordes */
  }

  .verification-result {
    padding: 1.25rem;
    min-height: 80px;
    gap: 12px;
  }
  
  .result-text {
    font-size: 1rem;
  }
  
  .result-icon-box {
    width: 40px;
    height: 40px;
  }
  
  h2 {
    font-size: 1.2em; 
    margin-bottom: 1.5rem;
  }

  #lector :deep(button),
  #lector :deep(select) {
     font-size: 0.85em;
     padding: 8px 10px; /* Reducido de 10px */
     padding-right: 2rem !important;
     background-position: right 0.5rem center;
  }
}
</style>