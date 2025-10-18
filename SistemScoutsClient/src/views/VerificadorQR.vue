<template>
  <div>
    <h2>Pantalla de Verificación</h2>
    <div id="lector" ref="lectorRef"></div>

    <div :class="['verification-result', resultadoClase]">
      {{ resultadoTexto }}
    </div>

    <p id="texto_escaneado">ID Escaneado: {{ idEscaneado }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Html5QrcodeScanner } from 'html5-qrcode' 

const ID_Prueba = [
  'ID-1234',
  'ID-5678',
  'ID-9012',
  'ID-3456'
]
const TIEMPO_VERIFICACION = 2000
const TIEMPO_MOSTRAR_RESULTADO = 5000

const resultadoTexto = ref('Esperando escaneo...')
const idEscaneado = ref('Ninguno')
const resultadoClase = ref('')
const lectorRef = ref(null)
let QR_Scanner = null

function verificarUsuarioEnAPI(id) {
  return new Promise(resolve => {
    setTimeout(() => {
      const idLimpio = id.trim()
      const acreditado = ID_Prueba.includes(idLimpio)

      resolve({
        id: idLimpio,
        verificado: acreditado,
        nombre: acreditado ? 'Usuario Acreditado' : 'Usuario Desconocido'
      })
    }, TIEMPO_VERIFICACION)
  })
}


async function Acreditacion(verificar) {

  resultadoClase.value = ''
  resultadoTexto.value = '🔄 Verificando ID...'
  idEscaneado.value = verificar

  try {
    const resultadoVerificacion = await verificarUsuarioEnAPI(verificar)

    if (resultadoVerificacion.verificado) {
      resultadoClase.value = 'verde'
      resultadoTexto.value = `✅ ACREDITADO: ${resultadoVerificacion.nombre}`
    } else {
      resultadoClase.value = 'rojo'
      resultadoTexto.value = `❌ NO ACREDITADO: ${resultadoVerificacion.nombre}`
    }
  } catch (error) {

    console.error('Error durante la verificación:', error)
    resultadoClase.value = 'rojo'
    resultadoTexto.value = '⚠️ ERROR DE CONEXIÓN CON EL SERVIDOR'
  }

  setTimeout(() => {
    resultadoTexto.value = 'Esperando escaneo...'
    resultadoClase.value = ''
    idEscaneado.value = 'Ninguno'
  }, TIEMPO_MOSTRAR_RESULTADO)
}

async function EscaneoExitoso(text) {
  if (QR_Scanner) {
    try {
      await QR_Scanner.pause()
    } catch (e) {
      console.warn('Error al pausar el escáner:', e)
    }
  }

  await Acreditacion(text)

  setTimeout(() => {
    if (QR_Scanner) {
      try {
        QR_Scanner.resume()
      } catch (e) {
        console.warn('Error al reanudar el escáner:', e)
      }
    }
  }, TIEMPO_MOSTRAR_RESULTADO + 1000) 
}

onMounted(() => {
  if (lectorRef.value) {
    QR_Scanner = new Html5QrcodeScanner(
      'lector',
      { fps: 10, qrbox: { width: 200, height: 200 } },
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
h2 {
  color: #555;
  margin-bottom: 15px;
  font-size: 1.3em;
  border-bottom: 2px solid #eee;
  padding-bottom: 5px;
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

#lector {
  min-height: 250px;
}
</style>