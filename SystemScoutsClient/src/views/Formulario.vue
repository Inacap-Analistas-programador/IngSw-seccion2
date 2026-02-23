<template>
  <div class="formulario">
    <PageHeader 
      title="Ficha de Pre-Registro" 
      subtitle="Completa tus datos para participar en nuestros cursos y actividades."
    />

    <div class="form-outer">
      <form class="form-inner" @submit.prevent="enviarFormulario">
        
        <!-- ProgressBar / Step Indicator -->
        <div class="wizard-progress">
          <div class="wizard-steps-container">
            <div 
              v-for="step in 5" 
              :key="step" 
              class="wizard-step-indicator"
              :class="{ 'active': currentStep >= step, 'current': currentStep === step }"
            >
              <div class="step-circle">{{ step }}</div>
              <div class="step-label" v-if="step === 1">Curso</div>
              <div class="step-label" v-if="step === 2">Persona</div>
              <div class="step-label" v-if="step === 3">Asociación</div>
              <div class="step-label" v-if="step === 4">Salud</div>
              <div class="step-label" v-if="step === 5">Adicional</div>
            </div>
          </div>
          <div class="wizard-progress-line-bg">
            <div class="wizard-progress-line-fill" :style="{ width: ((currentStep - 1) / 4) * 100 + '%' }"></div>
          </div>
        </div>

        <transition name="slide-fade" mode="out-in">
          <div :key="currentStep" class="wizard-step-content">
            
            <FormularioDatosCurso 
              v-if="currentStep === 1"
              v-model:cursoSeleccionado="cursoSeleccionado" 
              v-model:seccionCurso="seccionCurso"
              @seccion-change="handleSeccionChange"
            />

            <FormularioDatosPersona
              v-if="currentStep === 2"
              v-model:nombres="nombres"
              v-model:apellidoPaterno="apellidoPaterno"
              v-model:apellidoMaterno="apellidoMaterno"
              v-model:rut="rut"
              v-model:fechaNacimiento="fechaNacimiento"
              v-model:email="email"
              v-model:regionSeleccionada="regionSeleccionada"
              v-model:provinciaSeleccionada="provinciaSeleccionada"
              v-model:comunaSeleccionada="comunaSeleccionada"
              v-model:direccion="direccion"
              v-model:estadoCivil="estadoCivil"
              v-model:apodoCredencial="apodoCredencial"
              v-model:tipoContactoSeleccionado="tipoContactoSeleccionado"
              v-model:numeroContacto="numeroContacto"
              v-model:religion="religion"
              v-model:fotoUrl="fotoUrl"
              v-model:fotoArchivo="fotoArchivo"
              v-model:esFormador="esFormador"
              v-model:habilidad1="habilidad1"
              v-model:habilidad2="habilidad2"
              v-model:verificado="verificado"
            />

            <FormularioDatosAsociacion
              v-if="currentStep === 3"
              v-model:zonaSeleccionada="zonaSeleccionada"
              v-model:otraZona="otraZona"
              v-model:distritoSeleccionado="distritoSeleccionado"
              v-model:grupoPertenece="grupoPertenece"
              v-model:cargoSeleccionado="cargoSeleccionado"
              v-model:rolSeleccionado="rolSeleccionado"
              v-model:rolOtro="rolOtro"
              v-model:nivelFormacion="nivelFormacion"
              v-model:ramasMedioSeleccionadas="ramasMedioSeleccionadas"
              v-model:ramasAvanzadoSeleccionadas="ramasAvanzadoSeleccionadas"
              v-model:mmaaValor="mmaaValor"
            />

            <FormularioDatosSalud
              v-if="currentStep === 4"
              v-model:tieneAlergiaEnfermedad="tieneAlergiaEnfermedad"
              v-model:detalleAlergiaEnfermedad="detalleAlergiaEnfermedad"
              v-model:tieneLimitacion="tieneLimitacion"
              v-model:detalleLimitacion="detalleLimitacion"
              v-model:nombreEmergencia="nombreEmergencia"
              v-model:numeroEmergencia="numeroEmergencia"
              v-model:vehiculoPropio="vehiculoPropio"
              v-model:tipoAlimentacion="tipoAlimentacion"
              v-model:patentePropia="patentePropia"
              v-model:marcaPropia="marcaPropia"
              v-model:modeloPropio="modeloPropio"
              v-model:fichaMedicaNombre="fichaMedicaNombre"
              v-model:fichaMedicaArchivo="fichaMedicaArchivo"
              :cursoSeleccionado="cursoSeleccionado"
            />

            <FormularioDatosAdicional
              v-if="currentStep === 5"
              v-model:haTrabajadoConNinos="haTrabajadoConNinos"
              v-model:añosTrabajoNinos="añosTrabajoNinos"
              v-model:mesesTrabajoNinos="mesesTrabajoNinos"
              v-model:esBeneficiario="esBeneficiario"
              v-model:añosTiempoBeneficiario="añosTiempoBeneficiario"
              v-model:mesesTiempoBeneficiario="mesesTiempoBeneficiario"
              v-model:esMiembroActivo="esMiembroActivo"
              v-model:necesitaAlojamiento="necesitaAlojamiento"
              v-model:consideraciones="consideraciones"
              v-model:profesion="profesion"
            />

            <!-- WIZARD NAVIGATION -->
            <!-- We only show navigation when a course is selected (except for Step 1, where course selection IS the step) -->
            <div class="wizard-navigation-container" v-if="(cursoSeleccionado && seccionCurso) || currentStep === 1">
              
              <div class="wizard-nav-left">
                <BaseButton 
                  v-if="currentStep > 1"
                  type="button" 
                  variant="secondary" 
                  size="lg" 
                  @click="prevStep"
                  class="wizard-btn-prev"
                >
                  <AppIcons name="chevron-left" :size="20" style="margin-right: 8px;" />
                  Atrás
                </BaseButton>
              </div>

              <div class="wizard-nav-right">
                <BaseButton 
                  v-if="currentStep < 5 && cursoSeleccionado && seccionCurso"
                  type="button" 
                  variant="primary" 
                  size="lg" 
                  @click="nextStep"
                  class="wizard-btn-next"
                >
                  Siguiente
                  <AppIcons name="chevron-right" :size="20" style="margin-left: 8px;" />
                </BaseButton>

                <div v-if="currentStep === 5" class="botones-formulario-modern">
                  <BaseButton 
                    type="button" 
                    variant="secondary" 
                    size="xl" 
                    @click="limpiarFormulario"
                  >
                    <AppIcons name="trash" :size="20" style="margin-right: 8px;" />
                    VACIAR
                  </BaseButton>
                  
                  <BaseButton 
                    type="submit" 
                    variant="primary" 
                    size="xl" 
                    :loading="false"
                    @click.prevent="enviarFormulario"
                  >
                    <AppIcons name="send" :size="20" style="margin-right: 8px;" />
                    ENVIAR REGISTRO
                  </BaseButton>
                </div>
              </div>
            </div>

          </div>
        </transition>
      </form>
    </div>

    <NotificationToast 
      v-if="toast.visible" 
      :message="toast.message" 
      :type="toast.type" 
      :icon="toast.icon" 
      @close="toast.visible = false" 
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import authService from '../services/authService';
import personasService from '../services/personasService';
import { nivel as nivelApi } from '../services/mantenedoresService';

// Components
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import PageHeader from '@/components/common/PageHeader.vue';
import NotificationToast from '@/components/NotificationToast.vue';

// Modular Components
import FormularioDatosCurso from '@/components/formulario/FormularioDatosCurso.vue';
import FormularioDatosPersona from '@/components/formulario/FormularioDatosPersona.vue';
import FormularioDatosAsociacion from '@/components/formulario/FormularioDatosAsociacion.vue';
import FormularioDatosSalud from '@/components/formulario/FormularioDatosSalud.vue';
import FormularioDatosAdicional from '@/components/formulario/FormularioDatosAdicional.vue';

// :::::::::::::::::: NOTIFICACIONES :::::::::::::::::::::::::
const toast = reactive({
  visible: false,
  message: '',
  type: 'info',
  icon: 'info'
});

const showToast = (message, type = 'success', icon = 'check') => {
  toast.message = message;
  toast.type = type;
  toast.icon = icon;
  toast.visible = true;
  setTimeout(() => {
    toast.visible = false;
  }, 5000);
};

// :::::::::::::::::: FORM STATE (Orchestrated in parent) :::::::::::::::::::::::::
// 0. Wizard Navigation
const currentStep = ref(1);

const nextStep = () => {
  if (currentStep.value < 5) currentStep.value++;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// 1. Curso
const cursoSeleccionado = ref("");
const seccionCurso = ref("");

// 2. Persona
const nombres = ref("");
const apellidoPaterno = ref("");
const apellidoMaterno = ref("");
const rut = ref("");
const fechaNacimiento = ref("");
const email = ref("");
const regionSeleccionada = ref("");
const provinciaSeleccionada = ref("");
const comunaSeleccionada = ref("");
const direccion = ref("");
const estadoCivil = ref("");
const apodoCredencial = ref("");
const tipoContactoSeleccionado = ref("");
const numeroContacto = ref("");
const religion = ref("");
const fotoUrl = ref(null);
const fotoArchivo = ref(null);
const esFormador = ref("");
const habilidad1 = ref("no");
const habilidad2 = ref("no");
const verificado = ref("no");

// 3. Asociacion
const zonaSeleccionada = ref("");
const otraZona = ref("");
const distritoSeleccionado = ref("");
const grupoPertenece = ref("");
const cargoSeleccionado = ref("");
const rolSeleccionado = ref("");
const rolOtro = ref("");
const nivelFormacion = ref("");
const ramasMedioSeleccionadas = ref([]);
const ramasAvanzadoSeleccionadas = ref([]);
const mmaaValor = ref("");

// 4. Salud
const tieneAlergiaEnfermedad = ref("");
const detalleAlergiaEnfermedad = ref("");
const tieneLimitacion = ref("");
const detalleLimitacion = ref("");
const nombreEmergencia = ref("");
const numeroEmergencia = ref("");
const vehiculoPropio = ref("");
const tipoAlimentacion = ref("");
const patentePropia = ref("");
const marcaPropia = ref("");
const modeloPropio = ref("");
const fichaMedicaNombre = ref("");
const fichaMedicaArchivo = ref(null);

// 5. Adicional
const haTrabajadoConNinos = ref("");
const añosTrabajoNinos = ref("");
const mesesTrabajoNinos = ref("");
const esBeneficiario = ref("");
const añosTiempoBeneficiario = ref("");
const mesesTiempoBeneficiario = ref("");
const esMiembroActivo = ref("");
const necesitaAlojamiento = ref("");
const consideraciones = ref("");
const profesion = ref("");


// :::::::::::::::::: NAVIGATION & UTILS :::::::::::::::::::::::::
const listaNivelApi = ref([]);

const handleSeccionChange = () => {
  if (!seccionCurso.value) {
    limpiarFormulario();
  } else {
    // Optionally auto-advance when a course is selected
    // if (currentStep.value === 1) nextStep();
  }
};

onMounted(async () => {
  try {
    const nivResp = await nivelApi.list();
    listaNivelApi.value = nivResp.results || nivResp || [];
  } catch (e) {
    console.error(e);
  }

  // Scroll spy logic
  const handleScroll = () => {
    const sections = [1, 2, 3, 4];
    const viewportCenter = window.innerHeight / 2;
    let closestSection = 1;
    let minDistance = Infinity;
    
    sections.forEach((num) => {
      const section = document.getElementById(`seccion-${num}`);
      if (section) {
        const rect = section.getBoundingClientRect();
        const sectionCenter = rect.top + rect.height / 2;
        const distance = Math.abs(sectionCenter - viewportCenter);
        if (distance < minDistance && rect.top < viewportCenter && rect.bottom > 0) {
          minDistance = distance;
          closestSection = num;
        }
      }
    });
    updateActiveNavItem(closestSection);
  };
  
  window.addEventListener('scroll', handleScroll);
  onBeforeUnmount(() => window.removeEventListener('scroll', handleScroll));
});

function limpiarFormulario() {
  currentStep.value = 1;
  cursoSeleccionado.value = "";
  seccionCurso.value = "";
  nombres.value = "";
  apellidoPaterno.value = "";
  apellidoMaterno.value = "";
  rut.value = "";
  fechaNacimiento.value = "";
  email.value = "";
  direccion.value = "";
  comunaSeleccionada.value = "";
  estadoCivil.value = "";
  religion.value = "";
  apodoCredencial.value = "";
  fotoUrl.value = null;
  fotoArchivo.value = null;
  esFormador.value = "";
  habilidad1.value = "no";
  habilidad2.value = "no";
  verificado.value = "no";
  zonaSeleccionada.value = "";
  otraZona.value = "";
  distritoSeleccionado.value = "";
  grupoPertenece.value = "";
  cargoSeleccionado.value = "";
  rolSeleccionado.value = "";
  nivelFormacion.value = "";
  ramasMedioSeleccionadas.value = [];
  ramasAvanzadoSeleccionadas.value = [];
  mmaaValor.value = "";
  tieneAlergiaEnfermedad.value = "";
  detalleAlergiaEnfermedad.value = "";
  tieneLimitacion.value = "";
  detalleLimitacion.value = "";
  nombreEmergencia.value = "";
  numeroEmergencia.value = "";
  vehiculoPropio.value = "";
  tipoAlimentacion.value = "";
  patentePropia.value = "";
  marcaPropia.value = "";
  modeloPropio.value = "";
  fichaMedicaNombre.value = "";
  fichaMedicaArchivo.value = null;
  haTrabajadoConNinos.value = "";
  esBeneficiario.value = "";
  esMiembroActivo.value = "";
  necesitaAlojamiento.value = "";
  consideraciones.value = "";
  profesion.value = "";
  
  showToast("Formulario vaciado correctamente.", "info", "trash");
}

const enviarFormulario = async () => {
  try {
    const currentUser = await authService.getCurrentUser();
    if (!currentUser || !currentUser.id) {
      showToast("Error: No se pudo identificar al usuario.", "danger", "alert-circle");
      return;
    }

    if (!rut.value || !nombres.value || !apellidoPaterno.value || !email.value || !fechaNacimiento.value) {
      showToast("Complete los campos obligatorios.", "warning", "alert");
      return;
    }

    // Validate that the year is not more than 4 digits
    const yearStr = fechaNacimiento.value.split('-')[0];
    if (yearStr && yearStr.length > 4) {
      showToast("El año de nacimiento no puede tener más de 4 dígitos.", "warning", "alert");
      return;
    }

    let run = '', dv = '';
    if (rut.value) {
      const cleaned = rut.value.replace(/[^0-9kK]/g, '').toUpperCase();
      if (cleaned.length > 1) {
        dv = cleaned.slice(-1);
        run = cleaned.slice(0, -1);
      } else {
        run = cleaned;
      }
    }
    
    const personaData = {
      usu_id: currentUser.id,
      per_run: run,
      per_dv: dv || '',
      per_nombres: nombres.value,
      per_apelpta: apellidoPaterno.value,
      per_apelmat: apellidoMaterno.value || '',
      per_mail: email.value,
      per_fecha_nac: fechaNacimiento.value ? `${fechaNacimiento.value}` : null,
      per_direccion: direccion.value,
      com_id: comunaSeleccionada.value,
      esc_id: estadoCivil.value,
      per_tipo_fono: parseInt(tipoContactoSeleccionado.value) || 2, // Default Celular
      per_fono: numeroContacto.value || '',
      per_nom_emergencia: nombreEmergencia.value,
      per_fono_emergencia: numeroEmergencia.value,
      per_alergia_enfermedad: detalleAlergiaEnfermedad.value || '',
      per_limitacion: detalleLimitacion.value || '',
      per_profesion: profesion.value || '',
      per_tiempo_adulto: (añosTiempoBeneficiario.value || 0) + ' años ' + (mesesTiempoBeneficiario.value || 0) + ' meses',
      per_num_mma: parseInt(mmaaValor.value) || null,
      per_religion: religion.value || '',
      per_apodo: apodoCredencial.value || '',
      per_otros: consideraciones.value || '',
      per_vigente: true
    };
    
    if (añosTrabajoNinos.value) personaData.per_tiempo_nnaj = añosTrabajoNinos.value;

    const cursoData = {
      cus_id: seccionCurso.value,
      rol_id: rolSeleccionado.value,
      ali_id: tipoAlimentacion.value,
      niv_id: nivelFormacion.value
    };

    let vehiculoData = null;
    if (vehiculoPropio.value === 'si') {
      vehiculoData = {
        pev_patente: patentePropia.value,
        pev_marca: marcaPropia.value, 
        pev_modelo: modeloPropio.value
      };
    }

    let formadorData = null;
    if (esFormador.value === 'si') {
      formadorData = {
        pef_hab_1: habilidad1.value === 'si',
        pef_hab_2: habilidad2.value === 'si',
        pef_verif: verificado.value === 'si',
        pef_historial: ''
      };
    }

    let ramasData = [];
    const getNivelId = (nombre) => {
      const nivel = listaNivelApi.value.find(n => n.niv_descripcion && n.niv_descripcion.toLowerCase().includes(nombre.toLowerCase()));
      return nivel ? nivel.niv_id : null;
    };
    const idMedio = getNivelId('Medio') || 2; 
    const idAvanzado = getNivelId('Avanzado') || 3; 

    ramasMedioSeleccionadas.value.forEach(rId => ramasData.push({ niv_id: idMedio, ram_id: rId }));
    ramasAvanzadoSeleccionadas.value.forEach(rId => ramasData.push({ niv_id: idAvanzado, ram_id: rId }));

    let grupoData = null;
    let individualData = null;
    if (grupoPertenece.value === 'individual') {
      individualData = {
        zon_id: zonaSeleccionada.value,
        dis_id: distritoSeleccionado.value,
        car_id: cargoSeleccionado.value
      };
    } else if (grupoPertenece.value) {
      grupoData = { gru_id: grupoPertenece.value, peg_vigente: true };
    }

    const payloadFinal = {
      personaData,
      cursoData,
      vehiculoData,
      formadorData,
      ramasData,
      grupoData,
      individualData,
      medicalFile: fichaMedicaArchivo.value,
      personalPhoto: fotoArchivo.value
    };

    console.log("PAYLOAD A ENVIAR:", JSON.stringify(payloadFinal, null, 2));

    await personasService.createPersonaWithCourseAndVehicle(payloadFinal);

    showToast("¡Formulario enviado exitosamente!", "success", "check");
    limpiarFormulario();
  } catch (error) {
    console.error("Error completo al enviar formulario:", error);
    showToast("Error al enviar el formulario. Revise la consola.", "danger", "alert-circle");
  }
};
</script>


  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::        STYLES CSS     :::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->

<style scoped>
.formulario {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-background-soft);
  padding-bottom: 50px;
}

.form-outer {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
}

.form-inner {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.botones-formulario-modern {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  align-items: center;
}

/* WIZARD PROGRESS BAR */
.wizard-progress {
  margin-bottom: 40px;
  position: relative;
  padding: 0 20px;
}

.wizard-steps-container {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}

.wizard-step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 60px;
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e2e8f0;
  color: #64748b;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 3px solid #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.wizard-step-indicator.active .step-circle {
  background-color: #2563eb;
  color: white;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

.wizard-step-indicator.current .step-circle {
  transform: scale(1.15);
}

.step-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  white-space: nowrap;
  transition: color 0.3s ease;
}

.wizard-step-indicator.active .step-label {
  color: #1e293b;
}

.wizard-step-indicator.current .step-label {
  color: #2563eb;
  font-weight: 700;
}

.wizard-progress-line-bg {
  position: absolute;
  top: 18px;
  left: 50px;
  right: 50px;
  height: 4px;
  background-color: #e2e8f0;
  z-index: 1;
  border-radius: 2px;
}

.wizard-progress-line-fill {
  height: 100%;
  background-color: #2563eb;
  border-radius: 2px;
  transition: width 0.4s ease;
}

/* WIZARD NAVIGATION (Bottom) */
.wizard-navigation-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid rgba(0,0,0,0.05);
}

.wizard-nav-left, .wizard-nav-right {
  display: flex;
  align-items: center;
}

.wizard-nav-right {
  margin-left: auto;
}

/* SLIDE TRANSITION */
.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-enter-from {
  transform: translateX(30px);
  opacity: 0;
}
.slide-fade-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}

@media (max-width: 768px) {
  .botones-formulario-modern {
    flex-direction: column-reverse;
    width: 100%;
  }
  .botones-formulario-modern > button {
    width: 100%;
  }

  .step-label {
    display: none;
  }
  .wizard-progress-line-bg {
    left: 40px;
    right: 40px;
  }
}
</style>
