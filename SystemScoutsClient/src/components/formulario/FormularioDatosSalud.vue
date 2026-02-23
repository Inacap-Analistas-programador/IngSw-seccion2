<template>
  <section class="glass-section">
    <div id="seccion-3" class="anchor-offset"></div>
    <div class="section-header-modern">
      <AppIcons name="heart" :size="24" />
      <h2>Salud y Logística</h2>
    </div>
  
    <div class="section-grid">
      <div class="campo">
        <label for="salud">¿Tiene alergias, enfermedad a considerar?</label>
        <FilterSelect 
          v-model="tieneAlergiaEnfermedad" 
          :options="opcionesSiNo" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />

        <transition name="desplegar">
          <div v-if="tieneAlergiaEnfermedad === 'Si'" style="margin-top: 12px;">
            <label for="detalleSalud">Detalle alergias, enfermedad o limitación:</label>
            <textarea
              id="detalleSalud"
              v-model="detalleAlergiaEnfermedad"
              placeholder="Ingrese las alergias, enfermedad o limitación"
              rows="3"
              maxlength="255"
            ></textarea>
          </div>
        </transition>
      </div>

      <div class="campo">
        <label for="limitacion">¿Tiene alguna limitación?</label>
        <FilterSelect 
          v-model="tieneLimitacion" 
          :options="opcionesSiNo" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />

        <transition name="desplegar">
          <div v-if="tieneLimitacion === 'Si'" style="margin-top: 12px;">
            <label for="detalleLimitacion">Detalle de la limitación:</label>
            <textarea
              id="detalleLimitacion"
              v-model="detalleLimitacion"
              placeholder="Ingrese la limitación"
              rows="3"
              maxlength="255"
            ></textarea>
          </div>
        </transition>
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="nombreEmergencia">Nombre de contacto de emergencia:</label>
        <input id="nombreEmergencia" v-model="nombreEmergencia" type="text" placeholder="Ej: Alan Dave" />
      </div>

      <div class="campo">
        <label for="numeroEmergencia">Número de celular de emergencia:</label>
        <div style="display:flex; gap:8px; align-items:center;">
          <span class="prefix">+56</span>
          <input
            id="numeroEmergencia"
            v-model="numeroEmergencia"
            type="tel"
            placeholder="974643210"
            maxlength="9"
            required
          />
        </div>
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="vehiculoPropio">¿Viene en vehículo propio?</label>
        <FilterSelect 
          v-model="vehiculoPropio" 
          :options="opcionesSiNoMin" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />
      </div>

      <div class="campo">
        <label for="alimentacion">Opciones de alimentación (según tu curso):</label>
        <FilterSelect 
          v-model="tipoAlimentacion" 
          :options="listaAlimentacionApi" 
          valueKey="ali_id" 
          labelKey="label" 
          defaultLabel="Seleccione su opción de alimentación" 
          :disabled="!cursoSeleccionado"
        />
      </div>
    </div>

    <transition name="desplegar">
      <div v-if="vehiculoPropio === 'si'" class="campo" style="margin-top: 20px;">
        <div class="section-grid-3">
          <div class="campo">
            <label for="patentePropia">Patente (formato: ABCD12)</label>
            <input
              id="patentePropia"
              v-model="patentePropia"
              type="text"
              placeholder="Ej: ABCD12"
              maxlength="6"
              @input="patentePropia = $event.target.value.toUpperCase()"
            />
          </div>
          <div class="campo">
            <label for="marcaPropia">Marca:</label>
            <input id="marcaPropia" v-model="marcaPropia" type="text" placeholder="Ej: Toyota" />
          </div>
          <div class="campo">
            <label for="modeloPropio">Modelo:</label>
            <input id="modeloPropio" v-model="modeloPropio" type="text" placeholder="Ej: Yaris" />
          </div>
        </div>
      </div>
    </transition>

    <div class="contenedor-boton-subir" style="margin-top: 30px; text-align: center;">
      <BaseButton 
        variant="primary" 
        @click.prevent="openFileSelector"
      >
        <AppIcons name="upload" :size="20" style="margin-right: 8px;" />
        Subir Ficha Médica
      </BaseButton>
      <input 
        type="file" 
        id="fichaMedicaInput"
        ref="fichaMedicaRef" 
        @change="handleFileUpload" 
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
        style="display: none;"
      />
      <p v-if="fichaMedicaNombre" class="archivo-seleccionado" style="margin-top: 10px; color: #10b981; font-weight: 600;">
        <AppIcons name="check" :size="16" /> Archivo: {{ fichaMedicaNombre }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { cursos as cursosApi } from '@/services/cursosService';
import AppIcons from '@/components/icons/AppIcons.vue';
import BaseButton from '@/components/BaseButton.vue';
import FilterSelect from '@/components/common/FilterSelect.vue';

const props = defineProps({
  cursoSeleccionado: {
    type: [Number, String],
    default: null
  }
});

// Models
const tieneAlergiaEnfermedad = defineModel('tieneAlergiaEnfermedad');
const detalleAlergiaEnfermedad = defineModel('detalleAlergiaEnfermedad');
const tieneLimitacion = defineModel('tieneLimitacion');
const detalleLimitacion = defineModel('detalleLimitacion');
const nombreEmergencia = defineModel('nombreEmergencia');
const numeroEmergencia = defineModel('numeroEmergencia');
const vehiculoPropio = defineModel('vehiculoPropio');
const tipoAlimentacion = defineModel('tipoAlimentacion');
const patentePropia = defineModel('patentePropia');
const marcaPropia = defineModel('marcaPropia');
const modeloPropio = defineModel('modeloPropio');
const fichaMedicaNombre = defineModel('fichaMedicaNombre');
const fichaMedicaArchivo = defineModel('fichaMedicaArchivo');

// Local Data
const listaAlimentacionApi = ref([]);
const fichaMedicaRef = ref(null);
const opcionesSiNo = [
  { value: 'Si', label: 'Sí' },
  { value: 'No', label: 'No' }
];
const opcionesSiNoMin = [
  { value: 'si', label: 'Sí' },
  { value: 'no', label: 'No' }
];

// Methods
const cargarAlimentacionCurso = async (cursoId) => {
  if (!cursoId) {
    listaAlimentacionApi.value = [];
    return;
  }
  try {
    const resp = await cursosApi.get_alimentacion_curso(cursoId);
    listaAlimentacionApi.value = resp.results || resp || [];
  } catch (e) {
    console.error("Error loading course alimentation", e);
    listaAlimentacionApi.value = [];
  }
};
const openFileSelector = () => {
  fichaMedicaRef.value.click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    fichaMedicaNombre.value = file.name;
    fichaMedicaArchivo.value = file;
  }
};

watch(() => props.cursoSeleccionado, (newVal) => {
  tipoAlimentacion.value = null; // Reiniciar selección al cambiar curso
  cargarAlimentacionCurso(newVal);
});

onMounted(async () => {
  if (props.cursoSeleccionado) {
    cargarAlimentacionCurso(props.cursoSeleccionado);
  }
});
</script>

<style scoped>
.contenedor-boton-subir {
  padding: 20px;
  background: rgba(37, 99, 235, 0.03);
  border-radius: 15px;
  border: 1px dashed rgba(37, 99, 235, 0.3);
}

.prefix {
  font-weight: 700;
  color: #1e293b;
}

.archivo-seleccionado {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
