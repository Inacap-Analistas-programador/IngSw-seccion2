import { ref, onMounted, onUnmounted } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8000').replace(/\/api\/?$/, '')

export async function ObtenerDatos(rut, curso) {
  const params = new URLSearchParams()
  if (rut) params.append('rut', rut)
  if (curso) params.append('curso', curso)

  const cleanBase = API_BASE.endsWith('/') ? API_BASE.slice(0, -1) : API_BASE
  const url = `${cleanBase}/api/verificar-qr/?${params.toString()}`

  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`)

    const text = await response.text()
    if (!text) return { acreditado: false }

    return JSON.parse(text)
  } catch (error) {
    console.error('Error al obtener datos:', error)
    return { acreditado: false, error: true }
  }
}

export function verificarUsuario() {
  const TIEMPO_VERIFICACION = 1500
  const TIEMPO_MOSTRAR_RESULTADO = 4000

  const resultadoTexto = ref('Esperando escaneo...')
  const idEscaneado = ref('Ninguno')
  const resultadoClase = ref('')
  const lectorRef = ref(null)
  let QR_Scanner = null

  async function Acreditacion(textoDelQR) {
    resultadoClase.value = ''
    resultadoTexto.value = 'Verificando...'

    try {
      const partes = textoDelQR.split(',')
      if (partes.length !== 2) throw new Error('Formato de QR no válido.')

      const rut = partes[0].trim()
      const curso = partes[1].trim()

      await new Promise(resolve => setTimeout(resolve, TIEMPO_VERIFICACION))
      const datosRespuesta = await ObtenerDatos(rut, curso)

      if (datosRespuesta && datosRespuesta.acreditado === true) {
        resultadoClase.value = 'verde'
        resultadoTexto.value = 'ACREDITADO'
      } else if (datosRespuesta && datosRespuesta.error === 'invalid_qr') {
        resultadoClase.value = 'rojo'
        resultadoTexto.value = 'QR INVÁLIDO'
      } else {
        resultadoClase.value = 'rojo'
        resultadoTexto.value = 'NO ACREDITADO'
      }
    } catch (error) {
      console.error('Error durante la acreditación:', error)
      resultadoClase.value = 'rojo'
      resultadoTexto.value = error.message === 'Formato de QR no válido.' ? 'QR INVÁLIDO' : 'ERROR DE SERVIDOR'
    }

    setTimeout(() => {
      resultadoTexto.value = 'Esperando escaneo...'
      resultadoClase.value = ''
      if (QR_Scanner) QR_Scanner.resume()
    }, TIEMPO_MOSTRAR_RESULTADO)
  }

  async function EscaneoExitoso(text) {
    if (QR_Scanner) {
      try {
        await QR_Scanner.pause()
      } catch (e) {
        console.warn('Error al pausar:', e)
      }
    }
    await Acreditacion(text)
  }

  onMounted(async () => {
    if (lectorRef.value) {
      QR_Scanner = new Html5Qrcode("lector")

      const config = {
        fps: 10,
        qrbox: (w, h) => {
          const s = Math.min(w, h) * 0.8
          return { width: s, height: s }
        },
        aspectRatio: 1.0
      }

      try {
        // Intentar iniciar con la cámara trasera automáticamente
        await QR_Scanner.start(
          { facingMode: "environment" },
          config,
          EscaneoExitoso
        )
      } catch (err) {
        console.error("Error al iniciar cámara:", err)
        resultadoTexto.value = '❌ ERROR CAMARA'
      }
    }
  })

  onUnmounted(async () => {
    if (QR_Scanner) {
      try {
        await QR_Scanner.stop()
      } catch (error) {
        console.warn('Error al detener al desmontar:', error)
      }
    }
  })

  return {
    resultadoTexto,
    idEscaneado,
    resultadoClase,
    lectorRef
  }
} 