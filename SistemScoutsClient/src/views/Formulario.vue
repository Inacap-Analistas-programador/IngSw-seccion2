<template>
  <div class="formulario-scouts">
    <!-- Header del Formulario -->
    <div class="form-header">
      <div class="header-logo">
        <img src="@/assets/Logo_Boyscout_Chile.png" alt="Logo Scouts Chile" class="logo">
        <div class="header-text">
          <h1 class="page-title">Formulario de Inscripción</h1>
          <p class="page-subtitle">Curso Medio - Zona Biobío</p>
          <p class="institution">Asociación de Guías y Scouts de Chile</p>
        </div>
      </div>
    </div>

    <!-- Alertas del Sistema -->
    <BaseAlert
      v-if="systemAlert.visible"
      :type="systemAlert.type"
      :title="systemAlert.title"
      :message="systemAlert.message"
      :dismissible="true"
      @close="clearSystemAlert"
      class="form-alert"
    />

    <!-- Progreso del Formulario -->
    <div class="form-progress">
      <div class="progress-steps">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          :class="['step', { 
            active: currentStep === index, 
            completed: currentStep > index,
            disabled: currentStep < index
          }]"
        >
          <div class="step-number">
            <span v-if="currentStep <= index">{{ index + 1 }}</span>
            <span v-else>✓</span>
          </div>
          <div class="step-label">{{ step.label }}</div>
          <div class="step-line" v-if="index < steps.length - 1"></div>
        </div>
      </div>
    </div>

    <!-- Contenido del Formulario -->
    <div class="form-container">
      <form @submit.prevent="submitForm" class="scouts-form">
        <!-- Paso 1: Selección de Curso -->
        <div v-if="currentStep === 0" class="form-step">
          <h2 class="step-title">Selección de Curso</h2>
          <p class="step-description">Seleccione el curso al que desea inscribirse</p>
          
          <div class="courses-grid">
            <div 
              v-for="curso in cursosDisponibles" 
              :key="curso.id"
              :class="['course-option', { selected: formData.cursoId === curso.id }]"
              @click="selectCurso(curso)"
            >
              <div class="course-icon">{{ curso.icono }}</div>
              <div class="course-info">
                <h3 class="course-name">{{ curso.nombre }}</h3>
                <p class="course-dates">{{ curso.fechas }}</p>
                <p class="course-location">📍 {{ curso.ubicacion }}</p>
                <div class="course-meta">
                  <span class="course-cupo">Cupos: {{ curso.inscritos }}/{{ curso.cupoMaximo }}</span>
                  <span class="course-costo">${{ curso.costo.toLocaleString('es-CL') }}</span>
                </div>
              </div>
              <div class="course-status" :class="curso.estado">
                {{ curso.estado === 'disponible' ? 'Disponible' : 'Lleno' }}
              </div>
            </div>
          </div>

          <div v-if="formData.cursoId" class="selected-course-info">
            <h4>Curso seleccionado:</h4>
            <p><strong>{{ getCursoSeleccionado().nombre }}</strong></p>
            <p>{{ getCursoSeleccionado().fechas }} - {{ getCursoSeleccionado().ubicacion }}</p>
          </div>
        </div>

        <!-- Paso 2: Datos Personales -->
        <div v-if="currentStep === 1" class="form-step">
          <h2 class="step-title">Datos Personales</h2>
          
          <div class="form-section">
            <h3 class="section-title">Información Básica</h3>
            <div class="form-grid">
              <InputBase
                v-model="formData.nombres"
                label="Nombres *"
                placeholder="Ingrese sus nombres"
                :required="true"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.apellidos"
                label="Apellidos *"
                placeholder="Ingrese sus apellidos"
                :required="true"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.rut"
                label="RUT *"
                placeholder="12345678-9"
                :required="true"
                rules="rut"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.fechaNacimiento"
                label="Fecha de Nacimiento *"
                type="date"
                :required="true"
                class="form-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Contacto</h3>
            <div class="form-row">
              <InputBase
                v-model="formData.email"
                label="Correo Electrónico *"
                placeholder="ejemplo@correo.com"
                :required="true"
                rules="email"
                type="email"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.telefono"
                label="Teléfono *"
                placeholder="+56 9 1234 5678"
                :required="true"
                rules="number"
                class="form-field"
              />
            </div>
          </div>
        </div>

        <!-- Paso 3: Información Scout -->
        <div v-if="currentStep === 2" class="form-step">
          <h2 class="step-title">Información Scout</h2>
          
          <div class="form-section">
            <h3 class="section-title">Pertenencia Scout</h3>
            <div class="form-grid">
              <BaseSelect
                v-model="formData.region"
                :options="regiones"
                label="Región *"
                placeholder="Seleccione su región"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.distrito"
                :options="distritos"
                label="Distrito *"
                placeholder="Seleccione su distrito"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.grupo"
                :options="grupos"
                label="Grupo Scout *"
                placeholder="Seleccione su grupo"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.rama"
                :options="ramas"
                label="Rama *"
                placeholder="Seleccione su rama"
                :required="true"
                class="form-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Rol y Formación</h3>
            <div class="form-row">
              <BaseSelect
                v-model="formData.rol"
                :options="roles"
                label="Rol en el Curso *"
                placeholder="Seleccione su rol"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.nivel"
                :options="niveles"
                label="Nivel de Formación *"
                placeholder="Seleccione su nivel"
                :required="true"
                class="form-field"
              />
            </div>
            
            <InputBase
              v-model="formData.numeroMMAA"
              label="Número MMAA"
              placeholder="Ej: 5208"
              rules="number"
              class="form-field"
            />
          </div>
        </div>

        <!-- Paso 4: Salud y Alimentación -->
        <div v-if="currentStep === 3" class="form-step">
          <h2 class="step-title">Salud y Alimentación</h2>
          
          <div class="form-section">
            <h3 class="section-title">Preferencias y Restricciones</h3>
            
            <BaseSelect
              v-model="formData.alimentacion"
              :options="tiposAlimentacion"
              label="Tipo de Alimentación *"
              placeholder="Seleccione su tipo de alimentación"
              :required="true"
              class="form-field"
            />

            <div class="form-row">
              <InputBase
                v-model="formData.alergias"
                label="Alergias o Enfermedades"
                placeholder="Describa sus alergias o enfermedades"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.limitaciones"
                label="Limitaciones Físicas"
                placeholder="Describa sus limitaciones físicas"
                class="form-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Contacto de Emergencia</h3>
            <div class="form-grid">
              <InputBase
                v-model="formData.contactoEmergenciaNombre"
                label="Nombre Contacto Emergencia *"
                placeholder="Nombre completo"
                :required="true"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.contactoEmergenciaTelefono"
                label="Teléfono Emergencia *"
                placeholder="+56 9 1234 5678"
                :required="true"
                rules="number"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.contactoEmergenciaParentesco"
                label="Parentesco *"
                placeholder="Ej: Padre, Madre, etc."
                :required="true"
                class="form-field"
              />
            </div>
          </div>
        </div>

        <!-- Paso 5: Información Adicional -->
        <div v-if="currentStep === 4" class="form-step">
          <h2 class="step-title">Información Adicional</h2>
          
          <div class="form-section">
            <h3 class="section-title">Información Personal</h3>
            
            <div class="form-row">
              <InputBase
                v-model="formData.profesion"
                label="Profesión u Oficio"
                placeholder="Su profesión u oficio"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.estadoCivil"
                label="Estado Civil"
                placeholder="Su estado civil"
                class="form-field"
              />
            </div>

            <InputBase
              v-model="formData.apodo"
              label="Apodo para Credencial"
              placeholder="Apodo que aparecerá en su credencial"
              class="form-field"
            />
          </div>

          <div class="form-section">
            <h3 class="section-title">Logística</h3>
            
            <div class="checkbox-group">
              <BaseCheckBox
                v-model="formData.tieneVehiculo"
                label="¿Tiene vehículo disponible para el curso?"
                class="checkbox-field"
              />
              
              <BaseCheckBox
                v-model="formData.requiereAlojamiento"
                label="¿Requiere alojamiento durante el curso?"
                class="checkbox-field"
              />
              
              <BaseCheckBox
                v-model="formData.trabajaConNNAJ"
                label="¿Ha trabajado con Niños, Niñas y Jóvenes?"
                class="checkbox-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Términos y Condiciones</h3>
            
            <div class="terms-container">
              <div class="terms-content">
                <p><strong>Términos y Condiciones del Curso</strong></p>
                <p>Al enviar este formulario, acepta los términos y condiciones del curso, incluyendo:</p>
                <ul>
                  <li>Compromiso de asistencia completa al curso</li>
                  <li>Cumplimiento del código de conducta scout</li>
                  <li>Autorización para uso de datos personales según ley 19.628</li>
                  <li>Compromiso de pago oportuno de la cuota del curso</li>
                </ul>
              </div>
              
              <BaseCheckBox
                v-model="formData.aceptaTerminos"
                label="Acepto los términos y condiciones del curso *"
                :required="true"
                class="checkbox-field terms-checkbox"
              />
            </div>

            <InputBase
              v-model="formData.consideraciones"
              label="Consideraciones Adicionales"
              placeholder="Otra información que considere importante"
              type="textarea"
              class="form-field"
            />
          </div>
        </div>

        <!-- Paso 6: Resumen y Confirmación -->
        <div v-if="currentStep === 5" class="form-step">
          <h2 class="step-title">Resumen y Confirmación</h2>
          
          <div class="summary-container">
            <div class="summary-section">
              <h3 class="summary-title">Resumen de Inscripción</h3>
              
              <div class="summary-grid">
                <div class="summary-item">
                  <strong>Curso:</strong>
                  <span>{{ getCursoSeleccionado().nombre }}</span>
                </div>
                <div class="summary-item">
                  <strong>Fecha:</strong>
                  <span>{{ getCursoSeleccionado().fechas }}</span>
                </div>
                <div class="summary-item">
                  <strong>Ubicación:</strong>
                  <span>{{ getCursoSeleccionado().ubicacion }}</span>
                </div>
                <div class="summary-item">
                  <strong>Costo:</strong>
                  <span>${{ getCursoSeleccionado().costo.toLocaleString('es-CL') }}</span>
                </div>
              </div>
            </div>

            <div class="summary-section">
              <h3 class="summary-title">Datos del Participante</h3>
              
              <div class="summary-grid">
                <div class="summary-item">
                  <strong>Nombre:</strong>
                  <span>{{ formData.nombres }} {{ formData.apellidos }}</span>
                </div>
                <div class="summary-item">
                  <strong>RUT:</strong>
                  <span>{{ formData.rut }}</span>
                </div>
                <div class="summary-item">
                  <strong>Email:</strong>
                  <span>{{ formData.email }}</span>
                </div>
                <div class="summary-item">
                  <strong>Grupo Scout:</strong>
                  <span>{{ getLabel(grupos, formData.grupo) }}</span>
                </div>
                <div class="summary-item">
                  <strong>Rama:</strong>
                  <span>{{ getLabel(ramas, formData.rama) }}</span>
                </div>
              </div>
            </div>

            <div class="payment-info">
              <h3 class="summary-title">Información de Pago</h3>
              <div class="payment-details">
                <p><strong>Transferencia Bancaria</strong></p>
                <p>Banco: Scout Chile</p>
                <p>Cuenta Corriente: 123456789</p>
                <p>RUT: 12.345.678-9</p>
                <p>Email: tesoreria@scoutsbiobio.cl</p>
                <p class="payment-note">⚠️ Envíe su comprobante de transferencia al email indicado</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Navegación del Formulario -->
        <div class="form-navigation">
          <BaseButton
            v-if="currentStep > 0 && currentStep < steps.length - 1"
            type="button"
            variant="secondary"
            @click="previousStep"
            :disabled="submitting"
            class="nav-button"
          >
            ← Anterior
          </BaseButton>
          
          <div class="nav-spacer"></div>
          
          <BaseButton
            v-if="currentStep < steps.length - 1"
            type="button"
            variant="primary"
            @click="nextStep"
            :disabled="!currentStepValid"
            class="nav-button"
          >
            {{ currentStep === steps.length - 2 ? 'Revisar' : 'Siguiente' }} →
          </BaseButton>
          
          <BaseButton
            v-if="currentStep === steps.length - 1"
            type="submit"
            variant="success"
            :disabled="!formValid || submitting"
            :loading="submitting"
            class="nav-button submit-button"
          >
            {{ submitting ? 'Enviando...' : '✅ Confirmar Inscripción' }}
          </BaseButton>
        </div>
      </form>
    </div>

    <!-- Modal de Éxito -->
    <BaseModal
      v-model="showSuccessModal"
      @close="handleModalClose"
    >
      <div class="success-modal">
        <div class="success-icon">🎉</div>
        <h3>¡Inscripción Exitosa!</h3>
        <p>Su formulario ha sido registrado correctamente en el sistema Scouts Biobío.</p>
        
        <div class="success-details">
          <div class="detail-item">
            <strong>Número de Inscripción:</strong>
            <span class="inscription-number">#{{ numeroInscripcion }}</span>
          </div>
          <div class="detail-item">
            <strong>Curso:</strong>
            <span>{{ getCursoSeleccionado().nombre }}</span>
          </div>
          <div class="detail-item">
            <strong>Participante:</strong>
            <span>{{ formData.nombres }} {{ formData.apellidos }}</span>
          </div>
        </div>
        
        <div class="success-actions">
          <BaseButton
            variant="primary"
            @click="handleModalClose"
            class="action-button"
          >
            Aceptar
          </BaseButton>
          <BaseButton
            variant="outline"
            @click="imprimirComprobante"
            class="action-button"
          >
            📄 Imprimir Comprobante
          </BaseButton>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'

import BaseAlert from './components/reutilizables/BaseAlert.vue'
import BaseButton from './components/reutilizables/BaseButton.vue'
import BaseCheckBox from './components/reutilizables/BaseCheckBox.vue'
import BaseModal from './components/reutilizables/BaseModal.vue'
import BaseSelect from './components/reutilizables/BaseSelect.vue'
import InputBase from './components/reutilizables/InputBase.vue'

export default {
  name: 'FormularioInscripcion',
  components: {
    BaseAlert,
    BaseButton,
    BaseCheckBox,
    BaseModal,
    BaseSelect,
    InputBase
  },
  setup() {
    const currentStep = ref(0)
    const submitting = ref(false)
    const showSuccessModal = ref(false)
    const numeroInscripcion = ref('')

    const steps = [
      { label: 'Curso', valid: false },
      { label: 'Datos Personales', valid: false },
      { label: 'Información Scout', valid: false },
      { label: 'Salud', valid: false },
      { label: 'Adicional', valid: false },
      { label: 'Confirmación', valid: false }
    ]

    const formData = reactive({
      // Paso 1
      cursoId: '',
      
      // Paso 2
      nombres: '',
      apellidos: '',
      rut: '',
      fechaNacimiento: '',
      email: '',
      telefono: '',
      
      // Paso 3
      region: '',
      distrito: '',
      grupo: '',
      rama: '',
      rol: '',
      nivel: '',
      numeroMMAA: '',
      
      // Paso 4
      alimentacion: '',
      alergias: '',
      limitaciones: '',
      contactoEmergenciaNombre: '',
      contactoEmergenciaTelefono: '',
      contactoEmergenciaParentesco: '',
      
      // Paso 5
      profesion: '',
      estadoCivil: '',
      apodo: '',
      tieneVehiculo: false,
      requiereAlojamiento: false,
      trabajaConNNAJ: false,
      aceptaTerminos: false,
      consideraciones: ''
    })

    const systemAlert = reactive({
      visible: false,
      type: 'informacion',
      title: 'Bienvenido al Sistema de Inscripción',
      message: 'Complete el formulario para inscribirse en los cursos de la Zona Biobío.'
    })

    // Datos para selects y opciones
    const cursosDisponibles = [
      {
        id: 1,
        nombre: 'Curso Medio - Liderazgo Scout',
        fechas: '01-03 Feb 2024',
        ubicacion: 'Campamento Los Pinos, Concepción',
        cupoMaximo: 26,
        inscritos: 18,
        costo: 85000,
        estado: 'disponible',
        icono: '🏕️'
      },
      {
        id: 2,
        nombre: 'Primeros Auxilios en Terreno',
        fechas: '10-11 Feb 2024',
        ubicacion: 'Sede Scouts Talcahuano',
        cupoMaximo: 20,
        inscritos: 20,
        costo: 45000,
        estado: 'lleno',
        icono: '🩹'
      },
      {
        id: 3,
        nombre: 'Educación Ambiental Scout',
        fechas: '15-16 Feb 2024',
        ubicacion: 'Reserva Nacional Nonguén',
        cupoMaximo: 25,
        inscritos: 12,
        costo: 55000,
        estado: 'disponible',
        icono: '🌿'
      }
    ]

    const regiones = [
      { value: 'biobio', label: 'Región del Biobío' },
      { value: 'nuble', label: 'Región de Ñuble' },
      { value: 'araucania', label: 'Región de La Araucanía' }
    ]

    const distritos = [
      { value: 'norte', label: 'Distrito Norte' },
      { value: 'sur', label: 'Distrito Sur' },
      { value: 'centro', label: 'Distrito Centro' },
      { value: 'costa', label: 'Distrito Costa' }
    ]

    const grupos = [
      { value: 'grupo1', label: 'Grupo Scout 1 - Concepción' },
      { value: 'grupo2', label: 'Grupo Scout 2 - Talcahuano' },
      { value: 'grupo3', label: 'Grupo Scout 3 - Chiguayante' },
      { value: 'grupo4', label: 'Grupo Scout 4 - San Pedro' }
    ]

    const ramas = [
      { value: 'manada', label: 'Manada (7-10 años)' },
      { value: 'tropa', label: 'Tropa (11-14 años)' },
      { value: 'comunidad', label: 'Comunidad (15-17 años)' },
      { value: 'clan', label: 'Clan (18-20 años)' }
    ]

    const roles = [
      { value: 'participante', label: 'Participante' },
      { value: 'formador', label: 'Formador' },
      { value: 'director', label: 'Director de Rama' },
      { value: 'apoyo', label: 'Personal de Apoyo' }
    ]

    const niveles = [
      { value: 'inicial', label: 'Nivel Inicial' },
      { value: 'medio', label: 'Nivel Medio' },
      { value: 'avanzado', label: 'Nivel Avanzado' },
      { value: 'ninguno', label: 'Sin formación previa' }
    ]

    const tiposAlimentacion = [
      { value: 'normal', label: 'Alimentación Normal' },
      { value: 'vegetariano', label: 'Vegetariano' },
      { value: 'vegano', label: 'Vegano' },
      { value: 'celiaco', label: 'Celíaco' },
      { value: 'diabetico', label: 'Diabético' }
    ]

    // Computed properties
    const currentStepValid = computed(() => {
      const validations = {
        0: () => formData.cursoId !== '',
        1: () => formData.nombres && formData.apellidos && formData.rut && formData.email && formData.telefono,
        2: () => formData.region && formData.distrito && formData.grupo && formData.rama && formData.rol && formData.nivel,
        3: () => formData.alimentacion && formData.contactoEmergenciaNombre && formData.contactoEmergenciaTelefono && formData.contactoEmergenciaParentesco,
        4: () => formData.aceptaTerminos,
        5: () => true // Paso de confirmación siempre es válido
      }
      return validations[currentStep.value] ? validations[currentStep.value]() : false
    })

    const formValid = computed(() => {
      return currentStepValid.value && formData.aceptaTerminos
    })

    // Methods
    const showAlert = (type, title, message) => {
      systemAlert.type = type
      systemAlert.title = title
      systemAlert.message = message
      systemAlert.visible = true
    }

    const clearSystemAlert = () => {
      systemAlert.visible = false
    }

    const selectCurso = (curso) => {
      if (curso.estado === 'disponible') {
        formData.cursoId = curso.id
      } else {
        showAlert('error', 'Curso no disponible', 'Este curso ya ha alcanzado su cupo máximo. Por favor seleccione otro curso.')
      }
    }

    const getCursoSeleccionado = () => {
      return cursosDisponibles.find(curso => curso.id === formData.cursoId) || {}
    }

    const getLabel = (options, value) => {
      const option = options.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    const nextStep = () => {
      if (currentStepValid.value) {
        currentStep.value++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        showAlert('error', 'Campos incompletos', 'Por favor complete todos los campos requeridos antes de continuar.')
      }
    }

    const previousStep = () => {
      currentStep.value--
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const submitForm = async () => {
      if (!formValid.value) {
        showAlert('error', 'Formulario incompleto', 'Por favor complete todos los campos requeridos y acepte los términos y condiciones.')
        return
      }

      submitting.value = true

      try {
        // Simulación de envío a API Django
        await new Promise(resolve => setTimeout(resolve, 3000))
        
        // Generar número de inscripción
        const timestamp = new Date().getTime().toString().slice(-6)
        numeroInscripcion.value = `SC${timestamp}`
        
        showSuccessModal.value = true
        showAlert('exito', 'Inscripción exitosa', `Su inscripción #${numeroInscripcion.value} ha sido registrada correctamente.`)
        
      } catch (error) {
        showAlert('error', 'Error en la inscripción', 'Ha ocurrido un error al procesar su solicitud. Por favor intente nuevamente.')
      } finally {
        submitting.value = false
      }
    }

    const handleModalClose = () => {
      showSuccessModal.value = false
      // Resetear formulario para nueva inscripción
      Object.keys(formData).forEach(key => {
        if (typeof formData[key] === 'boolean') {
          formData[key] = false
        } else {
          formData[key] = ''
        }
      })
      currentStep.value = 0
    }

    const imprimirComprobante = () => {
      showAlert('informacion', 'Imprimir comprobante', 'La funcionalidad de impresión se implementará en la siguiente versión.')
    }

    onMounted(() => {
      // Inicialización cuando el componente se monta
      console.log('Formulario de inscripción Scouts Biobío montado')
    })

    return {
      currentStep,
      steps,
      formData,
      systemAlert,
      submitting,
      showSuccessModal,
      numeroInscripcion,
      cursosDisponibles,
      regiones,
      distritos,
      grupos,
      ramas,
      roles,
      niveles,
      tiposAlimentacion,
      currentStepValid,
      formValid,
      clearSystemAlert,
      selectCurso,
      getCursoSeleccionado,
      getLabel,
      nextStep,
      previousStep,
      submitForm,
      handleModalClose,
      imprimirComprobante
    }
  }
}
</script>

<style scoped>
.formulario-scouts {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.form-header {
  background: linear-gradient(135deg, #2c5aa0 0%, #1e3a8a 100%);
  color: white;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid #ffcc00;
  background: white;
  object-fit: cover;
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.page-subtitle {
  font-size: 1.3rem;
  opacity: 0.9;
  margin-bottom: 0.25rem;
}

.institution {
  font-size: 1rem;
  opacity: 0.8;
}

.form-alert {
  max-width: 1200px;
  margin: 2rem auto 0 auto;
  padding: 0 2rem;
}

.form-progress {
  background: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  border: 3px solid transparent;
}

.step.active .step-number {
  background: #2c5aa0;
  color: white;
  border-color: #1e3a8a;
  transform: scale(1.1);
}

.step.completed .step-number {
  background: #28a745;
  color: white;
  border-color: #1e7e34;
}

.step.disabled .step-number {
  background: #f8f9fa;
  color: #dee2e6;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6c757d;
  text-align: center;
}

.step.active .step-label {
  color: #2c5aa0;
}

.step.completed .step-label {
  color: #28a745;
}

.step-line {
  position: absolute;
  top: 25px;
  right: -50%;
  width: 100%;
  height: 3px;
  background: #e9ecef;
  z-index: 1;
}

.step.active .step-line,
.step.completed .step-line {
  background: #2c5aa0;
}

.form-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.scouts-form {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-step {
  padding: 2rem;
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-title {
  color: #2c5aa0;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  border-bottom: 3px solid #2c5aa0;
  padding-bottom: 0.5rem;
}

.step-description {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-title {
  color: #495057;
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  padding-left: 0.5rem;
  border-left: 4px solid #2c5aa0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-field {
  margin-bottom: 1rem;
}

/* Estilos para la selección de cursos */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.course-option {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  position: relative;
}

.course-option:hover {
  border-color: #2c5aa0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.1);
}

.course-option.selected {
  border-color: #2c5aa0;
  background: linear-gradient(135deg, #f8fbff 0%, #e3f2fd 100%);
}

.course-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.course-info {
  flex: 1;
}

.course-name {
  color: #2c5aa0;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.course-dates {
  color: #495057;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.course-location {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-cupo {
  color: #495057;
  font-size: 0.9rem;
}

.course-costo {
  color: #28a745;
  font-weight: 600;
  font-size: 1.1rem;
}

.course-status {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.course-status.disponible {
  background: #d4edda;
  color: #155724;
}

.course-status.lleno {
  background: #f8d7da;
  color: #721c24;
}

.selected-course-info {
  background: #e7f3ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-top: 1rem;
}

.selected-course-info h4 {
  color: #2c5aa0;
  margin-bottom: 0.5rem;
}

/* Estilos para checkboxes */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-field {
  margin-bottom: 0;
}

.terms-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.terms-content {
  margin-bottom: 1.5rem;
}

.terms-content p {
  margin-bottom: 0.75rem;
}

.terms-content ul {
  margin-left: 1.5rem;
  color: #495057;
}

.terms-content li {
  margin-bottom: 0.5rem;
}

.terms-checkbox {
  font-weight: 600;
}

/* Estilos para el resumen */
.summary-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.summary-title {
  color: #2c5aa0;
  font-size: 1.3rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #2c5aa0;
  padding-bottom: 0.5rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #2c5aa0;
}

.summary-item strong {
  color: #495057;
}

.payment-info {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1.5rem;
}

.payment-details {
  color: #856404;
}

.payment-details p {
  margin-bottom: 0.5rem;
}

.payment-note {
  font-weight: 600;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ffeaa7;
}

/* Navegación */
.form-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.nav-button {
  min-width: 150px;
}

.submit-button {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  border: none;
}

.nav-spacer {
  flex: 1;
}

/* Modal de éxito */
.success-modal {
  text-align: center;
  padding: 1rem;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-modal h3 {
  color: #28a745;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.success-details {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  text-align: left;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.detail-item:last-child {
  margin-bottom: 0;
  border-bottom: none;
}

.inscription-number {
  color: #2c5aa0;
  font-weight: 700;
  font-size: 1.2rem;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.action-button {
  min-width: 180px;
}

/* Responsive */
@media (max-width: 768px) {
  .form-header {
    padding: 1rem;
  }
  
  .header-logo {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .form-progress {
    padding: 1rem;
  }
  
  .progress-steps {
    flex-direction: column;
    gap: 1rem;
  }
  
  .step-line {
    display: none;
  }
  
  .form-container {
    padding: 0 1rem;
    margin: 1rem auto;
  }
  
  .form-step {
    padding: 1rem;
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid,
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-navigation {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-button {
    width: 100%;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .action-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .course-option {
    flex-direction: column;
    text-align: center;
  }
  
  .course-meta {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
}
</style>