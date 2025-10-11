<script setup>
import { ref } from "vue";

// Pasos del Stepper
const pasos = ["Información", "Detalles", "Confirmación"];
const pasoActual = ref(0);

function siguientePaso() {
  if (pasoActual.value < pasos.length - 1) {
    pasoActual.value++;
  }
}

function pasoAnterior() {
  if (pasoActual.value > 0) {
    pasoActual.value--;
  }
}
</script>

<template>
  <div class="ancho-completo max-ancho-xl margen-auto relleno-6">
    <!-- Encabezado del Stepper -->
    <div class="flex items-center justify-between margen-abajo-8">
      <div
        v-for="(paso, indice) in pasos"
        :key="indice"
        class="flex-1 flex items-center"
      >
        <!-- Círculo -->
        <div
          class="relativo flex items-center justify-center ancho-10 alto-10 redondo borde-2"
          :class="{
            'fondo-azul-500 borde-azul-500 texto-blanco': pasoActual.value >= indice,
            'borde-gris-300 texto-gris-500': pasoActual.value < indice
          }"
        >
          {{ indice + 1 }}
        </div>
        <!-- Línea -->
        <div
          v-if="indice < pasos.length - 1"
          class="flex-1 alto-1"
          :class="pasoActual.value > indice ? 'fondo-azul-500' : 'fondo-gris-300'"
        ></div>
      </div>
    </div>

    <!-- Contenido del paso -->
    <div class="texto-centro relleno-6 borde redondo-sombra">
      <h2 class="texto-xl fuente-semi margen-abajo-4">
        Paso {{ pasoActual.value + 1 }}: {{ pasos[pasoActual.value] }}
      </h2>
      <p class="texto-gris-600">
        Aquí iría el contenido correspondiente al paso
        <b>{{ pasos[pasoActual.value] }}</b>.
      </p>
    </div>

    <!-- Botones -->
    <div class="flex justify-between margen-arriba-6">
      <button
        @click="pasoAnterior"
        :disabled="pasoActual.value === 0"
        class="relleno-x-4 relleno-y-2 redondo borde-gris-300 texto-gris-700 disabled:opacidad-50"
      >
        Atrás
      </button>
      <button
        @click="siguientePaso"
        :disabled="pasoActual.value === pasos.length - 1"
        class="relleno-x-4 relleno-y-2 redondo fondo-azul-500 texto-blanco disabled:opacidad-50"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>

<style scoped>
.ancho-completo { width: 100%; }
.max-ancho-xl { max-width: 36rem; }
.margen-auto { margin-left: auto; margin-right: auto; }
.relleno-6 { padding: 1.5rem; }
.margen-abajo-8 { margin-bottom: 2rem; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.flex-1 { flex: 1 1 0%; }
.redondo { border-radius: 9999px; }
.borde-2 { border-width: 2px; }
.fondo-azul-500 { background-color: #3b82f6; }
.borde-azul-500 { border-color: #3b82f6; }
.texto-blanco { color: #fff; }
.borde-gris-300 { border-color: #d1d5db; }
.texto-gris-500 { color: #6b7280; }
.alto-1 { height: 0.25rem; }
.fondo-gris-300 { background-color: #d1d5db; }
.texto-centro { text-align: center; }
.borde { border-width: 1px; }
.redondo-sombra { border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.texto-xl { font-size: 1.25rem; }
.fuente-semi { font-weight: 600; }
.margen-abajo-4 { margin-bottom: 1rem; }
.texto-gris-600 { color: #4b5563; }
.margen-arriba-6 { margin-top: 1.5rem; }
.relleno-x-4 { padding-left: 1rem; padding-right: 1rem; }
.relleno-y-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.texto-gris-700 { color: #374151; }
.disabled\:opacidad-50:disabled { opacity: 0.5; }
</style>
