<template>
  <section class="glass-section">
    <div id="seccion-1" class="anchor-offset"></div>
    <div class="section-header-modern">
      <AppIcons name="user" :size="24" />
      <h2>Datos Personales</h2>
    </div>

    <!-- :::::::::::::::::: INPUTS BÁSICOS ::::::::::::::::::::::::: -->
    <div class="section-grid">
      <div class="campo">
        <label for="nombres">Nombres:</label>
        <input id="nombres" v-model="nombres" type="text" placeholder="Primer y segundo nombre" />
      </div>
      <div class="campo">
        <label for="apellidoPaterno">Apellido Paterno:</label>
        <input id="apellidoPaterno" v-model="apellidoPaterno" type="text" placeholder="Apellido paterno" />
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="apellidoMaterno">Apellido Materno:</label>
        <input id="apellidoMaterno" v-model="apellidoMaterno" type="text" placeholder="Apellido materno" />
      </div>

      <div class="campo">
        <label for="rut">RUT:</label>
        <input 
          id="rut" 
          type="text" 
          v-model="rutFormateado" 
          maxlength="12" 
          placeholder="Ej: 12.345.678-9" 
          :class="{ invalido: !esRutValido && rut.length > 0 }" 
          required
        />
        <span v-if="!esRutValido && rut.length > 0" class="error-mensaje">RUT inválido</span>
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="fechaNacimiento">Fecha de Nacimiento:</label>
        <input id="fechaNacimiento" v-model="fechaNacimiento" type="date" max="9999-12-31" />
      </div>
      <div class="campo">
        <label for="email">Correo Electrónico:</label>
        <input id="email" v-model="email" type="email" placeholder="Ingrese email" />
      </div>
    </div>

    <!-- :::::::::::::::::: SELECTOR DE REGIONES Y DIRECCIÓN ::::::::::::::::::::::::: -->
    <div class="section-grid">
      <div class="campo">
        <label for="Region">Región:</label>
        <FilterSelect 
          v-model="regionSeleccionada" 
          :options="listaRegionApi" 
          valueKey="reg_id" 
          labelKey="reg_descripcion" 
          defaultLabel="Seleccione una región" 
        />
      </div>

      <div class="campo">
        <label for="Provincia">Provincia:</label>
        <FilterSelect 
          v-model="provinciaSeleccionada" 
          :disabled="!regionSeleccionada" 
          :options="listaProvinciaApi" 
          valueKey="pro_id" 
          labelKey="pro_descripcion" 
          defaultLabel="Seleccione una provincia" 
        />
      </div>
    </div>

    <div class="section-grid">  
      <div class="campo">
          <label for="comuna">Comuna:</label>
          <FilterSelect 
            v-model="comunaSeleccionada" 
            :disabled="!provinciaSeleccionada" 
            :options="listaComunaApi" 
            valueKey="com_id" 
            labelKey="com_descripcion" 
            defaultLabel="Seleccione una comuna" 
          />
        </div>

      <div class="campo">
          <label for="direccion">Dirección:</label>
          <input id="direccion" v-model="direccion" type="text" placeholder="Ingrese dirección" />
      </div>
    </div>

    <!-- :::::::::::::::::: SELECTOR DE ESTADO CIVIL Y APODO ::::::::::::::::::::::::: -->
    <div class="section-grid">
      <div class="campo">
        <label for="estadoCivil">Estado Civil:</label>
        <FilterSelect 
          v-model="estadoCivil" 
          :options="listaEstadoCivilApi" 
          valueKey="esc_id" 
          labelKey="esc_descripcion" 
          defaultLabel="Seleccione su estado civil" 
        />
      </div>

      <div class="campo">
        <label for="apodoCredencial">Apodo para Credencial:</label>
        <input
          id="apodoCredencial"
          v-model="apodoCredencial"
          type="text"
          placeholder="Ingrese su apodo o nombre para credencial"
          maxlength="50"
        />
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="tipoContacto">Tipo de contacto:</label>
        <FilterSelect 
          v-model="tipoContactoSeleccionado" 
          :options="opcionesTipoContacto" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />
          <div v-if="tipoContactoSeleccionado" style="margin-top: 12px;">
            <label for="numeroContacto">Número de contacto:</label>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-weight: 600; color: #333;">+56</span>
              <input 
                id="numeroContacto" 
                v-model="numeroContacto" 
                type="text" 
                placeholder="Ej: 912345678"
                maxlength="9"
                @input="numeroContacto = numeroContacto.replace(/[^0-9]/g, '')"
              />
            </div>
          </div>
      </div>

      <div class="campo">
          <label for="formador">¿Eres Formador?</label>
          <FilterSelect 
            v-model="esFormador" 
            :options="opcionesSiNoMin" 
            valueKey="value" 
            labelKey="label" 
            defaultLabel="Seleccione una opción" 
          />
          <div v-if="esFormador === 'si'" class="campos-formador" style="margin-top: 12px;">
            <label for="habilitaciones">Habilitaciones:</label>
            <div class="checkbox-list-horizontal" style="margin-top: 8px;">
              <div>
                <input id="habilitacion1" type="checkbox" class="correos-checkbox custom-checkbox-spacing" v-model="habilidad1" true-value="si" false-value="no" />
                <label for="habilitacion1">Habilitación 1</label>
              </div>
              <div>
                <input id="habilitacion2" type="checkbox" class="correos-checkbox custom-checkbox-spacing" v-model="habilidad2" true-value="si" false-value="no" />
                <label for="habilitacion2">Habilitación 2</label>
              </div>
              <div>
                <input id="verificado" type="checkbox" class="correos-checkbox custom-checkbox-spacing" v-model="verificado" true-value="si" false-value="no" />
                <label for="verificado">Verificado</label>
              </div>
            </div>
          </div>
        </div>
    </div>
    
    <div class="section-grid">
      <div class="campo">
        <label for="religion">Religión:</label>
        <input id="religion" v-model="religion" type="text" placeholder="Ingrese su religión" />
      </div>

    <!-- ::::::::::::::::::::: FOTO ::::::::::::::::::::: -->
    <div class="section-photo-full">
      <div class="campo">
        <div class="campo" style="display: none;">
          <input
            type="file"
            id="foto"
            accept="image/png, image/jpeg"
            :disabled="camaraActiva || !!fotoUrl"
            @change="procesarFoto"
            ref="inputFoto"
          />
        </div>

        <div class="campo botones-inline">
          <label class="label-foto">¿Deseas subir una foto o tomar una foto?</label>
          <div class="botones-grupo">
            <BaseButton
              class="foto-btn"
              type="button"
              variant="secondary"
              @click="$refs.inputFoto.click()"
              :disabled="camaraActiva || !!fotoUrl"
              title="Subir foto"
            >
              <AppIcons name="arrow-up" :size="20" />
            </BaseButton>

            <BaseButton
              class="foto-btn"
              type="button"
              variant="primary"
              @click="abrirCamara"
              :disabled="fotoSubida || !!fotoUrl"
              title="Tomar foto"
            >
              <AppIcons name="camera" :size="20" />
            </BaseButton>

            <BaseButton
              v-if="fotoUrl"
              class="foto-btn"
              type="button"
              variant="danger"
              @click="eliminarFoto"
              title="Eliminar"
            >
              <AppIcons name="trash" :size="20" />
            </BaseButton>
          </div>
        </div>

        <!-- Vista previa estilizada (estilo formador) -->
        <div v-if="fotoUrl" class="preview-bloque" style="margin-top: 15px;">
          <div class="preview-container">
            <img :src="fotoUrl" alt="Vista previa de la foto" />
          </div>
        </div>
      </div>

      <!-- Modal Cámara Premium -->
      <Teleport to="body">
        <transition name="fade-scale">
          <div v-if="mostrarCamara" class="modal-overlay-glass" @mousedown.self="cerrarCamara">
            <div class="modal-content-premium camara-modal-popup" role="dialog" aria-modal="true">
              <div class="modal-header-premium">
                <div class="header-title">
                  <AppIcons name="camera" :size="24" />
                  <h3>Capturar Foto</h3>
                </div>
                <button type="button" class="modal-close-btn" @click="cerrarCamara">✕</button>
              </div>
              <div class="modal-body-premium">
                <div class="video-container-premium">
                  <video ref="video" autoplay playsinline></video>
                  <div class="camera-overlay-guide"></div>
                </div>
                <canvas ref="canvas" style="display: none;"></canvas>
              </div>
              <div class="modal-footer-premium">
                <BaseButton variant="secondary" @click="cerrarCamara" class="btn-large">Cancelar</BaseButton>
                <BaseButton variant="primary" @click="capturarFoto" class="btn-large">
                  <AppIcons name="camera" :size="20" style="margin-right: 10px;" />
                  Capturar Ahora
                </BaseButton>
              </div>
            </div>
          </div>
        </transition>
      </Teleport>
    </div>
  </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { regionApi } from '@/services/regionService';
import { provinciaApi } from '@/services/provinciaService';
import { comunaApi } from '@/services/comunaService';
import { estadoCivilApi } from '@/services/estadoCivilService';
import AppIcons from '@/components/icons/AppIcons.vue';
import BaseButton from '@/components/BaseButton.vue';
import FilterSelect from '@/components/common/FilterSelect.vue';

// Models
const nombres = defineModel('nombres');
const apellidoPaterno = defineModel('apellidoPaterno');
const apellidoMaterno = defineModel('apellidoMaterno');
const rut = defineModel('rut'); // Almacena el raw value (ej: "123456789" o "12345678K")
const fechaNacimiento = defineModel('fechaNacimiento');
const email = defineModel('email');
const regionSeleccionada = defineModel('regionSeleccionada');
const provinciaSeleccionada = defineModel('provinciaSeleccionada');
const comunaSeleccionada = defineModel('comunaSeleccionada');
const direccion = defineModel('direccion');
const estadoCivil = defineModel('estadoCivil');
const apodoCredencial = defineModel('apodoCredencial');
const tipoContactoSeleccionado = defineModel('tipoContactoSeleccionado');
const numeroContacto = defineModel('numeroContacto');
const religion = defineModel('religion');
const fotoUrl = defineModel('fotoUrl');
const fotoArchivo = defineModel('fotoArchivo');
const esFormador = defineModel('esFormador');
const habilidad1 = defineModel('habilidad1');
const habilidad2 = defineModel('habilidad2');
const verificado = defineModel('verificado');

// Local Data
const listaRegionApi = ref([]);
const listaProvinciaApi = ref([]);
const listaComunaApi = ref([]);
const listaEstadoCivilApi = ref([]);

// Camera Data
const opcionesSiNoMin = [
  { value: 'si', label: 'Sí' },
  { value: 'no', label: 'No' }
];
const opcionesTipoContacto = [
  { value: 'telefono_fijo', label: 'Teléfono Fijo' },
  { value: 'celular', label: 'Celular' },
  { value: 'celular_whatsapp', label: 'Celular con WhatsApp' },
  { value: 'whatsapp', label: 'WhatsApp' }
];
const mostrarCamara = ref(false);
const video = ref(null);
const canvas = ref(null);
const camaraActiva = ref(false);
const fotoSubida = ref(false);
let stream = null;

// --- RUT Logic ---
const cleanRut = (value) => {
  if (!value) return '';
  return value.replace(/[^0-9kK]/g, '').toUpperCase();
};

const formatRut = (rawRut) => {
  if (!rawRut) return '';
  const cleaned = cleanRut(rawRut);
  if (cleaned.length <= 1) return cleaned;
  
  let result = cleaned.slice(-1);
  let body = cleaned.slice(0, -1);
  
  result = '-' + result;
  
  while (body.length > 3) {
    result = '.' + body.slice(-3) + result;
    body = body.slice(0, -3);
  }
  return body + result;
};

const validarRutModulo11 = (rawRut) => {
  const cleaned = cleanRut(rawRut);
  if (cleaned.length < 2) return false;

  const dv = cleaned.slice(-1);
  let rutBody = parseInt(cleaned.slice(0, -1), 10);
  if (isNaN(rutBody)) return false;

  let m = 0;
  let s = 1;
  for (; rutBody; rutBody = Math.floor(rutBody / 10)) {
    s = (s + rutBody % 10 * (9 - m++ % 6)) % 11;
  }
  const calcDv = s ? String(s - 1) : 'K';

  return calcDv === dv;
};

const rutFormateado = computed({
  get() {
    return formatRut(rut.value);
  },
  set(newValue) {
    rut.value = cleanRut(newValue);
  }
});

const esRutValido = computed(() => {
  if (!rut.value || rut.value.length === 0) return true; // Don't show error if empty
  return validarRutModulo11(rut.value);
});
// --- End RUT Logic ---

// --- Image Compression Logic ---
/**
 * Comprime una imagen usando Canvas.
 * @param {File|Blob} file - El archivo original.
 * @param {number} quality - Calidad de 0 a 1 (ej: 0.7).
 * @param {number} maxWidth - Ancho máximo deseado.
 * @returns {Promise<Blob>} - El Blob comprimido.
 */
const comprimirImagen = (file, quality = 0.7, targetSize = 400) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = () => {
        const canvasComp = document.createElement('canvas');
        canvasComp.width = targetSize;
        canvasComp.height = targetSize;
        const ctx = canvasComp.getContext('2d');

        // Calcular recorte para mantener proporción y centrar (Center Crop)
        let sourceX = 0;
        let sourceY = 0;
        let sourceSize = Math.min(img.width, img.height);
        
        sourceX = (img.width - sourceSize) / 2;
        sourceY = (img.height - sourceSize) / 2;

        ctx.drawImage(
          img,
          sourceX, sourceY, sourceSize, sourceSize, // Recorte original (centro)
          0, 0, targetSize, targetSize             // Destino (400x400)
        );

        // Convertir a JPEG con la calidad definida
        canvasComp.toBlob(
          (blob) => {
            if (blob) resolve(blob);
            else reject(new Error('Error al comprimir imagen'));
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = (err) => reject(err);
    };
    reader.onerror = (err) => reject(err);
  });
};

// Methods
const openFileDialog = () => {
  const input = document.getElementById('foto');
  if (input) input.click();
};

const procesarFoto = async (event) => {
  const file = event.target.files[0];
  if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
    try {
      // Comprimimos la imagen antes de guardarla (ahora recorta a 400x400)
      console.log(`Tamaño original: ${(file.size / 1024).toFixed(2)} KB`);
      const blobComprimido = await comprimirImagen(file, 0.7, 400);
      console.log(`Tamaño cuadrado (400x400): ${(blobComprimido.size / 1024).toFixed(2)} KB`);

      fotoUrl.value = URL.createObjectURL(blobComprimido);
      fotoArchivo.value = new File([blobComprimido], `foto_${Date.now()}.jpg`, { type: 'image/jpeg' });
      fotoSubida.value = true;
    } catch (err) {
      console.error('Error al procesar/comprimir imagen:', err);
      alert('Hubo un error al procesar la imagen.');
    }
  } else {
    alert('Solo se permiten imágenes en formato JPG o PNG.');
  }
};

const abrirCamara = async () => {
    try {
    mostrarCamara.value = true;
    camaraActiva.value = true;
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    setTimeout(() => {
        if (video.value) video.value.srcObject = stream;
    }, 100);
  } catch {
    alert('No se pudo acceder a la cámara. Verifica permisos o hardware disponible.');
  }
};

const capturarFoto = () => {
  const context = canvas.value.getContext('2d');
  const targetSize = 400;
  
  canvas.value.width = targetSize;
  canvas.value.height = targetSize;
  
  // Calcular recorte central del video
  const videoWidth = video.value.videoWidth;
  const videoHeight = video.value.videoHeight;
  const sourceSize = Math.min(videoWidth, videoHeight);
  const sourceX = (videoWidth - sourceSize) / 2;
  const sourceY = (videoHeight - sourceSize) / 2;

  context.drawImage(
    video.value, 
    sourceX, sourceY, sourceSize, sourceSize, // Recorte original (centro)
    0, 0, targetSize, targetSize             // Destino (400x400)
  );
  
  // Capturar directamente como JPEG con compresión 0.7
  canvas.value.toBlob(
    (blob) => {
      if (blob) {
        console.log(`Captura cámara cuadrado (400x400): ${(blob.size / 1024).toFixed(2)} KB`);
        fotoUrl.value = URL.createObjectURL(blob);
        fotoArchivo.value = new File([blob], `captura_${Date.now()}.jpg`, { type: 'image/jpeg' });
        fotoSubida.value = true;
        cerrarCamara();
      }
    },
    'image/jpeg',
    0.7
  );
};

const cerrarCamara = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
  mostrarCamara.value = false;
  camaraActiva.value = false;
};

const eliminarFoto = () => {
  fotoUrl.value = null;
  fotoArchivo.value = null;
  fotoSubida.value = false;
  camaraActiva.value = false;
  cerrarCamara();
  const input = document.getElementById('foto');
  if (input) input.value = '';
};

// Cascading Watchers
watch(regionSeleccionada, async (newVal) => {
  provinciaSeleccionada.value = "";
  comunaSeleccionada.value = "";
  listaProvinciaApi.value = [];
  listaComunaApi.value = [];
  if (newVal) {
    try {
      const resp = await provinciaApi.list({ region_id: newVal, vigente: true });
      listaProvinciaApi.value = resp.results || resp || [];
    } catch (e) {
      console.error('Error fetching provinces:', e);
    }
  }
});

watch(provinciaSeleccionada, async (newVal) => {
  comunaSeleccionada.value = "";
  listaComunaApi.value = [];
  if (newVal) {
    try {
      const resp = await comunaApi.list({ provincia_id: newVal, vigente: true });
      listaComunaApi.value = resp.results || resp || [];
    } catch (e) {
      console.error('Error fetching comunas:', e);
    }
  }
});

onMounted(async () => {
  try {
    const [regionResp, estadoResp] = await Promise.all([
      regionApi.list({ vigente: true }),
      estadoCivilApi.list({ vigente: true })
    ]);
    listaRegionApi.value = regionResp.results || regionResp || [];
    listaEstadoCivilApi.value = estadoResp.results || estadoResp || [];
  } catch (e) {
    console.error("Error loading initial data", e);
  }
});
</script>

<style scoped>
.foto-section-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.label-foto {
  font-weight: 600;
  color: #475569;
  margin-top: 0px;
  text-align: left;
}

.section-photo-full {
  width: 100%;

}

.botones-grupo {
  display: flex;
  gap: 8px;
}

.foto-btn {
  height: 40px !important;
  width: 40px !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 8px;
}

.foto-btn :deep(svg) {
  margin: 0 !important;
}

.preview-bloque {
  width: 100%;
  max-width: 460px; /* 400px image + 15px*2 padding + 15px buffer */
  background: rgba(248, 250, 252, 0.5);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-sizing: border-box;
}

.preview-container {
  display: flex;
  justify-content: center;
}

.preview-container img {
  width: 400px;
  height: 400px;
  max-width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  border: 4px solid #fff;
  background-color: #f1f5f9;
}

.bloque-formador {
  width: 100%;
  background: rgba(248, 250, 252, 0.5);
  border-radius: 15px;
  padding: 20px;
  margin-top: 12px;
}

.checkbox-list-horizontal {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.checkbox-list-horizontal > div {
  display: flex;
  align-items: center;
  gap: 8px;
}

.camara-body video {
  width: 100%;
  border-radius: 10px;
  background: #000;
}

/* Modal Premium Styles */
.modal-overlay-glass {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content-premium {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 24px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header-premium {
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #1e293b;
}

.header-title h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-close-btn {
  background: #f1f5f9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.modal-close-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
  transform: rotate(90deg);
}

.modal-body-premium {
  padding: 24px;
}

.video-container-premium {
  position: relative;
  width: 100%;
  max-width: 450px;
  aspect-ratio: 1 / 1;
  margin: 0 auto;
  background: #000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
}

.video-container-premium video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-overlay-guide {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(255, 255, 255, 0.2);
  pointer-events: none;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.3); /* Letterbox effect */
}

.modal-footer-premium {
  padding: 20px 24px;
  background: rgba(248, 250, 252, 0.5);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-large {
  padding: 12px 24px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
}



/* Modal Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}


input.invalido {
  border-color: #ef4444;
  background-color: #fef2f2;
}

input.invalido:focus {
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

.error-mensaje {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 4px;
  font-weight: 500;
}

/* Styles for checkboxes to match Correos.vue */
.correos-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #1a237e;
  transition: transform 0.2s ease;
}

.correos-checkbox:hover {
  transform: scale(1.1);
}

.custom-checkbox-spacing {
  margin-right: 4px;
}

/* Transitions */
.desplegar-enter-active,
.desplegar-leave-active {
  transition: all 0.3s ease-out;
  max-height: 500px;
  overflow: hidden;
}

.desplegar-enter-from,
.desplegar-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}
</style>
