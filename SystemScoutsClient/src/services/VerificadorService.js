import { ref } from 'vue' // solo usamos refs dentro del factory
import { Html5QrcodeScanner, Html5QrcodeScanType } from 'html5-qrcode'
import { request } from './apiClient'
// La librería principal para escanear código QR y ScanType para limitar tipos de escaneo

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// Asumiendo que esta función se llama desde algún lugar con los valores
export async function ObtenerDatos(rut, curso) {
  
    // 1. Crea un objeto para manejar los parámetros de la URL
    const params = new URLSearchParams();
    
    // 2. Añade tus parámetros
    // (Solo se añaden si tienen un valor)
    if (rut) {
        params.append('rut', rut);
    }
    if (curso) {
        params.append('curso', curso);
    }

    // 3. Construye la URL final
    // (Asegúrate de que la URL base '/api/cursos/' sea correcta)
    const url = `/api/cursos/?${params.toString()}`;

    console.log("Solicitando a:", url); // Útil para depurar

    try {
        // 4. Realiza la petición
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        return data;

    } catch (error) {
        console.error("Error al obtener datos:", error);
        // Maneja el error como prefieras
    }
}

// Constantes de temporización
const TIEMPO_VERIFICACION = 2000
const TIEMPO_MOSTRAR_RESULTADO = 5000

// NOTA: Este archivo expone utilidades y una fábrica createVerifier().
// La fábrica devuelve refs y métodos para controlar el lector desde un componente.

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
  // kept for backwards compatibility but not used by factory directly
  // This function is left to not break existing imports; prefer createVerifier().
  return verificarUsuarioEnAPI(verificar)
}

async function EscaneoExitoso(text) {
  // kept for backwards compatibility; prefer EscaneoExitosoLocal returned by factory
  return Acreditacion(text)
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
// Factory que crea una instancia controlable del verificador.
export function createVerifier(options = {}) {
  // options: { lectorRef, elementId }
  const lectorRef = options.lectorRef || null

  const resultadoTexto = ref('Esperando escaneo...')
  const idEscaneado = ref('Ninguno')
  const resultadoClase = ref('')

  let QR_Scanner = null

  async function verificarUsuarioEnAPISim(id) {
    // simula verificación (usa la misma lógica que verificarUsuarioEnAPI)
    return new Promise(resolve => {
      setTimeout(() => {
        const idLimpio = id.trim()
        const acreditado = (typeof ID_Prueba !== 'undefined') ? ID_Prueba.includes(idLimpio) : false
        resolve({ id: idLimpio, verificado: acreditado, nombre: acreditado ? 'Usuario Acreditado' : 'Usuario Desconocido' })
      }, TIEMPO_VERIFICACION)
    })
  }

  async function AcreditacionLocal(verificar) {
    resultadoClase.value = ''
    resultadoTexto.value = '🔄 Verificando ID...'
    idEscaneado.value = verificar

    try {
      const resultadoVerificacion = await verificarUsuarioEnAPISim(verificar)
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

  async function EscaneoExitosoLocal(text) {
    if (QR_Scanner && typeof QR_Scanner.pause === 'function') {
      try { await QR_Scanner.pause() } catch (e) { console.warn('Error al pausar el escáner:', e) }
    }

    await AcreditacionLocal(text)

    setTimeout(() => {
      if (QR_Scanner && typeof QR_Scanner.resume === 'function') {
        try { QR_Scanner.resume() } catch (e) { console.warn('Error al reanudar el escáner:', e) }
      }
    }, TIEMPO_MOSTRAR_RESULTADO + 1000)
  }

  function start() {
    const elementId = (lectorRef && lectorRef.value && lectorRef.value.id) ? lectorRef.value.id : (options.elementId || 'lector')
    if (QR_Scanner) return
    QR_Scanner = new Html5QrcodeScanner(
      elementId,
      {
        fps: 10,
        qrbox: calcularQrBox,
        supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
      },
      false
    )
    QR_Scanner.render(EscaneoExitosoLocal)
  }

  function stop() {
    if (!QR_Scanner) return
    try { QR_Scanner.clear() } catch (err) { console.warn('Error al detener el escáner:', err) }
    QR_Scanner = null
  }

  function pause() { if (QR_Scanner && QR_Scanner.pause) QR_Scanner.pause().catch(()=>{}) }
  function resume() { if (QR_Scanner && QR_Scanner.resume) QR_Scanner.resume().catch(()=>{}) }

  return {
    start,
    stop,
    pause,
    resume,
    resultadoTexto,
    resultadoClase,
    idEscaneado
  }
}