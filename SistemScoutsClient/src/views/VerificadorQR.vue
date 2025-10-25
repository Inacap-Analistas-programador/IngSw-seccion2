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
import { ref, onMounted, onUnmounted } from 'vue' // Hooks de Vue para reactividad y ciclo de vida
import { Html5QrcodeScanner, Html5QrcodeScanType } from 'html5-qrcode'  
// La librería principal para escanear código QR y ScanType para limitar tipos de escaneo


// Base de datos simulada. IDs que serán aceptados como válidos.
const ID_Prueba = [
  'ID-1234',
  'ID-5678',
  'ID-9012',
  'ID-3456'
]
// Simula el tiempo de respuesta de una API por 2 segundos
const TIEMPO_VERIFICACION = 2000
// Tiempo que el resultado (verde/rojo) permanece en pantalla 5 segundos
const TIEMPO_MOSTRAR_RESULTADO = 5000

// El texto principal que ve el usuario (Esperando..., Verificando...etc.)
const resultadoTexto = ref('Esperando escaneo...')
// Muestra el último ID que fue escaneado.
const idEscaneado = ref('Ninguno')
// Controla el color del cuadro de resultado (se asigna a 'verde' o 'rojo' en el CSS).
const resultadoClase = ref('')
// Referencia al <div id="lector"> en el template. Vue lo conectará al HTML.
const lectorRef = ref(null)
// Variable para guardar la instancia del escáner y poder usarla en todas las funciones.
let QR_Scanner = null

function verificarUsuarioEnAPI(id) {
  // Retorna una promesa para simular el tiempo de espera (asincronía)
  return new Promise(resolve => {
    // Simula la latencia de red usando el tiempo constante
    setTimeout(() => {
      const idLimpio = id.trim() // Limpia espacios en blanco del ID
      // Comprueba si el ID existe en nuestra base de datos simulada
      const acreditado = ID_Prueba.includes(idLimpio)

      // Resuelve la promesa con el objeto de resultado
      resolve({
        id: idLimpio,
        verificado: acreditado,
        nombre: acreditado ? 'Usuario Acreditado' : 'Usuario Desconocido'
      })
    }, TIEMPO_VERIFICACION) // Espera 2 segundos
  })
}

async function Acreditacion(verificar) {

  // Pone la UI en estado de "Cargando"
  resultadoClase.value = '' // Limpia el color (verde/rojo) anterior
  resultadoTexto.value = '🔄 Verificando ID...' // Muestra mensaje de carga
  idEscaneado.value = verificar // Muestra el ID que se está procesando

  try {
    // Llama a la API simulada y espera (await) su respuesta
    const resultadoVerificacion = await verificarUsuarioEnAPI(verificar)

    // Procesa la respuesta de la "API"
    if (resultadoVerificacion.verificado) {
      // Éxito: ID Acreditado
      resultadoClase.value = 'verde'
      resultadoTexto.value = `✅ ACREDITADO: ${resultadoVerificacion.nombre}`
    } else {
      // Falla: ID No Acreditado
      resultadoClase.value = 'rojo'
      resultadoTexto.value = `❌ NO ACREDITADO: ${resultadoVerificacion.nombre}`
    }
  } catch (error) {
    // Manejo de errores (si la promesa falla, ej: error de red)
    console.error('Error durante la verificación:', error)
    resultadoClase.value = 'rojo'
    resultadoTexto.value = '⚠️ ERROR DE CONEXIÓN CON EL SERVIDOR'
  }

  // Limpia la pantalla después de mostrar el resultado
  // Se ejecuta después de TIEMPO_MOSTRAR_RESULTADO (5 segundos)
  setTimeout(() => {
    resultadoTexto.value = 'Esperando escaneo...'
    resultadoClase.value = ''
    idEscaneado.value = 'Ninguno'
  }, TIEMPO_MOSTRAR_RESULTADO)
}

async function EscaneoExitoso(text) {
  // Pausa el escáner y Evita que escanee el mismo QR 10 veces mientras se verifica.
  if (QR_Scanner) {
    try {
      await QR_Scanner.pause()
    } catch (e) {
      console.warn('Error al pausar el escáner:', e)
    }
  }

  // Inicia el proceso de acreditación con el texto del QR
  await Acreditacion(text)

  // Reanuda el escáner después de mostrar el resultado
  // Espera 6 segundos del resultado para evitar posibles errores 
  setTimeout(() => {
    if (QR_Scanner) {
      try {
        QR_Scanner.resume() // Vuelve a encender el lector
      } catch (e) {
        console.warn('Error al reanudar el escáner:', e)
      }
    }
  }, TIEMPO_MOSTRAR_RESULTADO + 1000) // 5000ms + 1000ms = 6 segundos
}

// Función para que el tamaño del QrBox se adapte automáticamente
const calcularQrBox = (tamañoAncho, tamañoLargo) => {
  const borde = Math.min(tamañoAncho, tamañoLargo)
  // Calcula el 70% del borde más pequeño
  const qrboxSize = Math.floor(borde * 0.7) 
  return {
    width: qrboxSize,
    height: qrboxSize
  }
}

onMounted(() => {
  if (lectorRef.value) {
    QR_Scanner = new Html5QrcodeScanner(
      'lector',
      { 
        fps: 10, 
        // qrbox usa la función calcularQrBox de arriba para ajustar el tamaño de manera dinámica
        qrbox: calcularQrBox ,
        // supportedScanTypes limita el escaneo solo a cámara 
        supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
      },
      false 
    )

    QR_Scanner.render(EscaneoExitoso)
  }
})

onUnmounted(() => {
  if (QR_Scanner) {
    try {
      QR_Scanner.clear()
    } catch (error) {
      console.warn('Error al detener el escáner al desmontar:', error)
    }
  }
})
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