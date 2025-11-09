import { ref, onMounted, onUnmounted } from 'vue' // Hooks de Vue para reactividad y ciclo de vida
import { Html5QrcodeScanner, Html5QrcodeScanType } from 'html5-qrcode'

// La librería principal para escanear código QR y ScanType para limitar tipos de escaneo

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function ObtenerDatos(rut, curso) {

  const params = new URLSearchParams()
  if (rut) {
    params.append('rut', rut)
  }
  if (curso) {
    params.append('curso', curso)
  }
  const url = `${API_BASE}/api/verificar-qr/?${params.toString()}`
  console.log('Solicitando a:', url)

  try {
    const response = await fetch(url) 
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener datos:', error)
  }
}


// Toda la lógica del escáner va dentro de esta función
export function verificarUsuario() {
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
        const acreditado = ID_Prueba.includes(idLimpio) // <--- Ahora usa la variable

        // Resuelve la promesa con el objeto de resultado
        resolve({
          id: idLimpio,
          verificado: acreditado,
          nombre: acreditado ? 'Usuario Acreditado' : 'Usuario Desconocido'
        })
      }, TIEMPO_VERIFICACION) // Espera 2 segundos
    })
  }

async function Acreditacion(textoDelQR) {
    // 'textoDelQR' es el texto completo del QR, ej: "12345678-9,CURSO101"
    
    resultadoClase.value = '' // Limpia el color (verde/rojo) anterior
    resultadoTexto.value = '🔄 Verificando QR...' // Muestra mensaje de carga
    idEscaneado.value = textoDelQR // Muestra el QR crudo primero

    try {
      // 1. Parsear el texto del QR
      // ASUMO que el formato es: "RUT,CURSO"
      const partes = textoDelQR.split(',');
      if (partes.length !== 2) {
        // Si el QR no tiene 2 partes (RUT y CURSO)
        throw new Error('Formato de QR no válido.'); 
      }
      
      const rut = partes[0].trim();
      const curso = partes[1].trim();

      // 2. Llamar a tu API REAL (la función que YA tenías)
      // Espera 2 segundos (TIEMPO_VERIFICACION) para que se vea el "Verificando..."
      await new Promise(resolve => setTimeout(resolve, TIEMPO_VERIFICACION));
      const datosRespuesta = await ObtenerDatos(rut, curso);

      // 3. Decidir si está acreditado (según tu nueva regla)
      // ASUMO que si 'datosRespuesta' trae algo, está acreditado.
      if (datosRespuesta && datosRespuesta.acreditado === true) { 
        // Éxito: Acreditado
        resultadoClase.value = 'verde'
        resultadoTexto.value = '✅ ACREDITADO' // <-- Texto simple
        idEscaneado.value = `RUT: ${rut} | Curso: ${curso}`; // Muestra datos limpios
      } else {
        // Falla: No Acreditado (si ObtenerDatos no devuelve nada)
        resultadoClase.value = 'rojo'
        resultadoTexto.value = '❌ NO ACREDITADO' // <-- Texto simple
        idEscaneado.value = `RUT: ${rut} | Curso: ${curso}`; // Muestra datos limpios
      }

    } catch (error) {
      // Manejo de errores (si la promesa falla, ej: error de red o formato)
      console.error('Error durante la acreditación:', error)
      resultadoClase.value = 'rojo'
      
      // Diferenciar error de formato de error de API
      if (error.message === 'Formato de QR no válido.') {
        resultadoTexto.value = '⚠️ QR Inválido';
        idEscaneado.value = textoDelQR; // Muestra el QR erróneo
      } else {
        resultadoTexto.value = '⚠️ ERROR DE CONEXIÓN'
      }
    }

    // Limpia la pantalla después de mostrar el resultado
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
          qrbox: calcularQrBox,
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

  // retorna las variables que el componente necesita
  return {
    resultadoTexto,
    idEscaneado,
    resultadoClase,
    lectorRef
  }
} 