<template>
  <div class="contenedor-generador">
    <h1>Generador de Código QR</h1>

    <div class="grupo-entrada">
      <input
        v-model="textoIngresado"
        type="text"
        placeholder="Escribe tu ID"
      />
      <button @click="generarQR">Generar QR</button>
    </div>

    <div id="CODIGO_QR"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let codigoQR = null;
const textoIngresado = ref("");

function generarQR() {
  if (!textoIngresado.value.trim()) {
    alert("Por favor, introduce el texto o URL para generar el código QR.");
    return;
  }

  const contenedorQR = document.getElementById("CODIGO_QR");
  contenedorQR.innerHTML = ""; // Limpiar QR anterior

  codigoQR = new QRCode(contenedorQR, {
    text: textoIngresado.value,
    width: 128,
    height: 128,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H,
  });
}

// Inicializamos QR vacío al montar el componente
onMounted(() => {
  const contenedorQR = document.getElementById("CODIGO_QR");
  contenedorQR.innerHTML = "";
});
</script>

<style scoped>
.contenedor-generador {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 90%;
  max-width: 400px;
  margin: 2rem auto;
}

h1 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5em;
}

.grupo-entrada {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.grupo-entrada input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
}

.grupo-entrada button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.grupo-entrada button:hover {
  background-color: #0056b3;
}

#CODIGO_QR {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  border: 1px dashed #ccc;
  border-radius: 5px;
  min-height: 150px;
  margin-top: 20px;
}
</style>

<!-- No olvides incluir el script de QRCode en tu index.html si no lo tienes -->
<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script> -->
