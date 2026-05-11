<template>
  <div class="sandbox">
    <PageHeader 
      title="Component Lab" 
      subtitle="Prueba los componentes modulares del formulario en aislamiento" 
    />

    <div class="sandbox-controls">
      <div class="campo">
        <label>Seleccionar Componente:</label>
        <select v-model="activeComponent">
          <option value="FormularioDatosCurso">1. Curso y Sección</option>
          <option value="FormularioDatosPersona">2. Datos Personales</option>
          <option value="FormularioDatosAsociacion">3. Datos Asociación</option>
          <option value="FormularioDatosSalud">4. Salud y Logística</option>
          <option value="FormularioDatosAdicional">5. Datos Adicionales</option>
        </select>
      </div>
    </div>

    <div class="sandbox-stage">
      <div class="stage-info">
        <p><strong>Estado del Mock:</strong> {{ JSON.stringify(formData, null, 2) }}</p>
      </div>

      <component 
        :is="componentMap[activeComponent]"
        v-bind="formData"
        @update:cursoSeleccionado="formData.cursoSeleccionado = $event"
        @update:seccionCurso="formData.seccionCurso = $event"
        @update:nombres="formData.nombres = $event"
        @update:apellidoPaterno="formData.apellidoPaterno = $event"
        @update:apellidoMaterno="formData.apellidoMaterno = $event"
        @update:email="formData.email = $event"
        @update:rut="formData.rut = $event"
        @update:fechaNacimiento="formData.fechaNacimiento = $event"
        @update:regionSeleccionada="formData.regionSeleccionada = $event"
        @update:provinciaSeleccionada="formData.provinciaSeleccionada = $event"
        @update:direccion="formData.direccion = $event"
        @update:comunaSeleccionada="formData.comunaSeleccionada = $event"
        @update:estadoCivil="formData.estadoCivil = $event"
        @update:apodoCredencial="formData.apodoCredencial = $event"
        @update:tipoContactoSeleccionado="formData.tipoContactoSeleccionado = $event"
        @update:numeroContacto="formData.numeroContacto = $event"
        @update:religion="formData.religion = $event"
        @update:esFormador="formData.esFormador = $event"
        @update:habilidad1="formData.habilidad1 = $event"
        @update:habilidad2="formData.habilidad2 = $event"
        @update:verificado="formData.verificado = $event"
        @update:zonaSeleccionada="formData.zonaSeleccionada = $event"
        @update:otraZona="formData.otraZona = $event"
        @update:distritoSeleccionado="formData.distritoSeleccionado = $event"
        @update:grupoPertenece="formData.grupoPertenece = $event"
        @update:cargoSeleccionado="formData.cargoSeleccionado = $event"
        @update:rolSeleccionado="formData.rolSeleccionado = $event"
        @update:rolOtro="formData.rolOtro = $event"
        @update:nivelFormacion="formData.nivelFormacion = $event"
        @update:ramasMedioSeleccionadas="formData.ramasMedioSeleccionadas = $event"
        @update:ramasAvanzadoSeleccionadas="formData.ramasAvanzadoSeleccionadas = $event"
        @update:mmaaValor="formData.mmaaValor = $event"
        @update:tieneAlergiaEnfermedad="formData.tieneAlergiaEnfermedad = $event"
        @update:detalleAlergiaEnfermedad="formData.detalleAlergiaEnfermedad = $event"
        @update:tieneLimitacion="formData.tieneLimitacion = $event"
        @update:detalleLimitacion="formData.detalleLimitacion = $event"
        @update:nombreEmergencia="formData.nombreEmergencia = $event"
        @update:numeroEmergencia="formData.numeroEmergencia = $event"
        @update:vehiculoPropio="formData.vehiculoPropio = $event"
        @update:tipoAlimentacion="formData.tipoAlimentacion = $event"
        @update:patentePropia="formData.patentePropia = $event"
        @update:marcaPropia="formData.marcaPropia = $event"
        @update:modeloPropio="formData.modeloPropio = $event"
        @update:fichaMedicaNombre="formData.fichaMedicaNombre = $event"
        @update:fichaMedicaArchivo="formData.fichaMedicaArchivo = $event"
        @update:haTrabajadoConNinos="formData.haTrabajadoConNinos = $event"
        @update:añosTrabajoNinos="formData.añosTrabajoNinos = $event"
        @update:mesesTrabajoNinos="formData.mesesTrabajoNinos = $event"
        @update:esBeneficiario="formData.esBeneficiario = $event"
        @update:añosTiempoBeneficiario="formData.añosTiempoBeneficiario = $event"
        @update:mesesTiempoBeneficiario="formData.mesesTiempoBeneficiario = $event"
        @update:esMiembroActivo="formData.esMiembroActivo = $event"
        @update:necesitaAlojamiento="formData.necesitaAlojamiento = $event"
        @update:profesion="formData.profesion = $event"
        @update:consideraciones="formData.consideraciones = $event"
        @seccion-change="logEvent('Sección Cambiada')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, markRaw } from 'vue';
import PageHeader from '@/components/common/PageHeader.vue';

// Modular Components
import FormularioDatosCurso from '@/components/formulario/FormularioDatosCurso.vue';
import FormularioDatosPersona from '@/components/formulario/FormularioDatosPersona.vue';
import FormularioDatosAsociacion from '@/components/formulario/FormularioDatosAsociacion.vue';
import FormularioDatosSalud from '@/components/formulario/FormularioDatosSalud.vue';
import FormularioDatosAdicional from '@/components/formulario/FormularioDatosAdicional.vue';

const activeComponent = ref('FormularioDatosCurso');

const componentMap = {
  FormularioDatosCurso: markRaw(FormularioDatosCurso),
  FormularioDatosPersona: markRaw(FormularioDatosPersona),
  FormularioDatosAsociacion: markRaw(FormularioDatosAsociacion),
  FormularioDatosSalud: markRaw(FormularioDatosSalud),
  FormularioDatosAdicional: markRaw(FormularioDatosAdicional)
};

const formData = reactive({
  // Curso
  cursoSeleccionado: '',
  seccionCurso: '',
  // Persona
  nombres: 'Prueba',
  apellidoPaterno: 'Mock',
  apellidoMaterno: '',
  email: 'test@example.com',
  rut: '',
  fechaNacimiento: '',
  regionSeleccionada: '',
  provinciaSeleccionada: '',
  direccion: '',
  comunaSeleccionada: '',
  estadoCivil: '',
  apodoCredencial: '',
  tipoContactoSeleccionado: '',
  numeroContacto: '',
  religion: '',
  esFormador: '',
  habilidad1: 'no',
  habilidad2: 'no',
  verificado: 'no',
  fotoUrl: null,
  // Asociacion
  zonaSeleccionada: '',
  otraZona: '',
  distritoSeleccionado: '',
  grupoPertenece: '',
  cargoSeleccionado: '',
  rolSeleccionado: '',
  rolOtro: '',
  nivelFormacion: '',
  ramasMedioSeleccionadas: [],
  ramasAvanzadoSeleccionadas: [],
  mmaaValor: '',
  // Salud
  tieneAlergiaEnfermedad: '',
  detalleAlergiaEnfermedad: '',
  tieneLimitacion: '',
  detalleLimitacion: '',
  nombreEmergencia: '',
  numeroEmergencia: '',
  vehiculoPropio: '',
  tipoAlimentacion: '',
  patentePropia: '',
  marcaPropia: '',
  modeloPropio: '',
  fichaMedicaNombre: '',
  fichaMedicaArchivo: null,
  // Adicional
  haTrabajadoConNinos: '',
  añosTrabajoNinos: '',
  mesesTrabajoNinos: '',
  esBeneficiario: '',
  añosTiempoBeneficiario: '',
  mesesTiempoBeneficiario: '',
  esMiembroActivo: '',
  necesitaAlojamiento: 'no',
  profesion: '',
  consideraciones: ''
});

const logEvent = (name) => {
  console.log(`[Sandbox Event] ${name}`);
};
</script>

<style scoped>
.sandbox {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.sandbox-controls {
  max-width: 1100px;
  margin: 0 auto 30px;
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.sandbox-stage {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
}

.sandbox-output {
  max-width: 1100px;
  margin: 30px auto 0;
  background: #1e293b;
  color: #f8fafc;
  padding: 20px;
  border-radius: 15px;
  font-family: monospace;
}

.output-title {
  margin: 0 0 10px 0;
  font-size: 0.9rem;
  color: #94a3b8;
  text-transform: uppercase;
}

.output-log {
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.85rem;
  line-height: 1.5;
}

.log-entry { margin-bottom: 4px; }
.log-time { color: #64748b; margin-right: 8px; }
.log-event { color: #38bdf8; font-weight: 700; }

.stage-info {
  background: #1e293b;
  color: #38bdf8;
  padding: 15px;
  border-radius: 12px;
  font-family: monospace;
  font-size: 0.85rem;
  overflow-x: auto;
  height: fit-content;
}

@media (max-width: 900px) {
  .sandbox-stage {
    grid-template-columns: 1fr;
  }
}
</style>
