import { ref, onMounted, onUnmounted } from 'vue'
import { Html5QrcodeScanner, Html5QrcodeScanType } from 'html5-qrcode'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// ✅ Adaptado a tus filtros Django: run, dv, curso_codigo
export async function ObtenerDatos(run, dv, curso_codigo) {
  const params = new URLSearchParams()

  if (run) params.append('run', run)
  if (dv) params.append('dv', dv)
  if (curso_codigo) params.append('curso_codigo', curso_codigo)

  const url = `${API_BASE}/api/personas/cursos/?${params.toString()}`
  console.log('Solicitando a:', url)

  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`)
    const data = await response.json()

    // Si Django devuelve una lista de resultados, tomamos el primero
    return Array.isArray(data) ? data[0] : data
  } catch (error) {
    console.error('Error al obtener datos:', error)
    return null
  }
}

// ==========================================================
// ===============  LÓGICA DEL ESCÁNER QR ===================
// ==========================================================
export function verificarUsuario() {
  const TIEMPO_VERIFICACION = 2000
  const TIEMPO_MOSTRAR_RESULTADO = 5000

  const resultadoTexto = ref('Esperando escaneo...')
  const idEscaneado = ref('Ninguno')
  const resultadoClase = ref('')
  const lectorRef = ref(null)
  let QR_Scanner = null

  async function Acreditacion(textoDelQR) {
    resultadoClase.value = ''
    resultadoTexto.value = '🔄 Verificando QR...'
    idEscaneado.value = textoDelQR

    try {
      // Espera un momento para simular latencia
      await new Promise(resolve => setTimeout(resolve, TIEMPO_VERIFICACION))

      // ✅ Asumimos que el QR viene en formato: "RUN-DV,CURSO_CODIGO"
      const partes = textoDelQR.split(',')
      if (partes.length !== 2) throw new Error('Formato de QR no válido.')

      const [rutCompleto, curso_codigo] = partes.map(p => p.trim())
      const [run, dv] = rutCompleto.split('-')

      if (!run || !dv || !curso_codigo) throw new Error('QR incompleto.')

      // 🔍 Consultar a la API con tus filtros
      const datosRespuesta = await ObtenerDatos(run, dv, curso_codigo)

      if (datosRespuesta && datosRespuesta.PEC_ACREDITACION === true) {
        // ✅ Acreditado
        resultadoClase.value = 'verde'
        resultadoTexto.value = '✅ ACREDITADO'
        idEscaneado.value = `RUN: ${run}-${dv} | Curso: ${curso_codigo}`
      } else {
        // ❌ No acreditado
        resultadoClase.value = 'rojo'
        resultadoTexto.value = '❌ NO ACREDITADO'
        idEscaneado.value = `RUN: ${run}-${dv} | Curso: ${curso_codigo}`
      }

    } catch (error) {
      console.error('Error durante la acreditación:', error)
      resultadoClase.value = 'rojo'
      if (error.message.includes('Formato') || error.message.includes('incompleto')) {
        resultadoTexto.value = '⚠️ QR Inválido'
      } else {
        resultadoTexto.value = '⚠️ ERROR DE CONEXIÓN'
      }
    }

    // 🧹 Limpia la pantalla tras unos segundos
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

  const calcularQrBox = (ancho, alto) => {
    const borde = Math.min(ancho, alto)
    const qrboxSize = Math.floor(borde * 0.7)
    return { width: qrboxSize, height: qrboxSize }
  }

  onMounted(() => {
    if (lectorRef.value) {
      QR_Scanner = new Html5QrcodeScanner(
        'lector',
        {
          fps: 10,
          qrbox: calcularQrBox,
          supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
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

  return {
    resultadoTexto,
    idEscaneado,
    resultadoClase,
    lectorRef,
  }
}
