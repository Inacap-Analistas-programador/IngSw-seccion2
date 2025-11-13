[file name]: Formulario 2.vue
[file content begin]
<template>
  <div class="formulario-scouts">
    <!-- Header del Formulario -->
    <div class="form-header">
      <div class="header-logo">
        <img src="@/assets/Logo_Boyscout_Chile.png" alt="Logo Scouts Chile" class="logo">
        <div class="header-text">
          <h1 class="page-title">Formulario de Pre-Inscripción</h1>
          <p class="page-subtitle">Zona Biobío</p>
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
            completed: step.completed,
            disabled: currentStep < index && !step.completed
          }]"
        >
          <div class="step-number">
            <span v-if="!step.completed">{{ index + 1 }}</span>
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
        <!-- Paso 1: Datos Personales -->
        <div v-show="currentStep === 0" class="form-step">
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
                v-model="formData.apellidoPaterno"
                label="Apellido Paterno *"
                placeholder="Ingrese su apellido paterno"
                :required="true"
                class="form-field"
              />
              
              <InputBase
                v-model="formData.apellidoMaterno"
                label="Apellido Materno"
                placeholder="Ingrese su apellido materno"
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

              <BaseSelect
                v-model="formData.estadoCivil"
                :options="estadosCiviles"
                label="Estado Civil *"
                placeholder="Seleccione su estado civil"
                :required="true"
                class="form-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Foto para Credencial</h3>
            <FileUploader
              v-model="formData.fotoParticipante"
              :preview-url="fotoPreviewUrl"
              label="Foto de cara del participante *"
              accept="image/jpeg,image/png,image/jpg"
              :required="true"
              class="form-field"
              @file-changed="handleFileChanged"
            />
            <p class="field-note">Formato: JPEG o PNG. Foto frontal clara para la credencial.</p>
            
            <div v-if="fotoPreviewUrl" class="photo-preview">
              <h4>Vista previa de la foto:</h4>
              <div class="preview-container">
                <img :src="fotoPreviewUrl" alt="Vista previa de la foto" class="preview-image" />
                <button type="button" @click="removePhoto" class="remove-photo-btn">
                  ❌ Eliminar foto
                </button>
              </div>
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
              
              <BaseSelect
                v-model="formData.tipoTelefono"
                :options="tiposTelefono"
                label="Tipo de Teléfono *"
                placeholder="Seleccione tipo"
                :required="true"
                class="form-field"
                @change="actualizarFormatoTelefono"
              />
              
              <InputBase
                v-model="formData.telefono"
                label="Teléfono *"
                :placeholder="telefonoPlaceholder"
                :required="true"
                class="form-field telefono-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Dirección</h3>
            <div class="form-grid">
              <InputBase
                v-model="formData.direccion"
                label="Dirección *"
                placeholder="Ingrese su dirección completa"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.region"
                :options="regiones"
                label="Región *"
                placeholder="Seleccione su región"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.provincia"
                :options="provincias"
                label="Provincia *"
                placeholder="Seleccione su provincia"
                :required="true"
                class="form-field"
              />
              
              <BaseSelect
                v-model="formData.comuna"
                :options="comunas"
                label="Comuna *"
                placeholder="Seleccione su comuna"
                :required="true"
                class="form-field"
              />
            </div>
          </div>
        </div>

        <!-- Paso 2: Información Scout -->
        <div v-show="currentStep === 1" class="form-step">
          <h2 class="step-title">Información Scout</h2>
          
          <div class="form-section">
            <h3 class="section-title">Pertenencia Scout</h3>
            <div class="form-grid">
              <BaseSelect
                v-model="formData.zona"
                :options="zonas"
                label="Zona *"
                placeholder="Seleccione su zona"
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
                label="Rama de Curso *"
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
                label="N° Niveles *"
                placeholder="Seleccione su nivel"
                :required="true"
                class="form-field"
              />
            </div>
            
            <InputBase
              v-if="mostrarCampoMMAA"
              v-model="formData.numeroMMAA"
              label="Número MMAA"
              placeholder="Ej: 5208"
              class="form-field"
            />

            <InputBase
              v-if="mostrarEducacionFormador"
              v-model="formData.nivelEducacion"
              label="Nivel de Educación *"
              placeholder="Ingrese su nivel de educación"
              :required="formData.rol === 2"
              class="form-field"
            />
          </div>
        </div>

        <!-- Paso 3: Salud y Alimentación -->
        <div v-show="currentStep === 2" class="form-step">
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
                type="textarea"
                :rows="4"
                class="form-field alergias-field"
              />
              
              <InputBase
                v-model="formData.limitaciones"
                label="Limitaciones Físicas"
                placeholder="Describa sus limitaciones físicas"
                type="textarea"
                :rows="4"
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
                class="form-field"
              />
            </div>
          </div>
        </div>

        <!-- Paso 4: Información Adicional -->
        <div v-show="currentStep === 3" class="form-step">
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
                v-model="formData.apodo"
                label="Apodo para Credencial"
                placeholder="Apodo que aparecerá en su credencial"
                class="form-field"
              />
            </div>

            <div class="checkbox-group">
              <BaseCheckBox
                v-model="formData.trabajaConNNAJ"
                label="¿Ha trabajado con Niños, Niñas y Jóvenes?"
                class="checkbox-field"
              />
              
              <InputBase
                v-if="formData.trabajaConNNAJ"
                v-model="formData.rangoEdadNNAJ"
                label="Rango de edad con el que trabaja *"
                placeholder="Ej: 6-12 años, 13-17 años"
                :required="formData.trabajaConNNAJ"
                class="form-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Logística</h3>
            
            <div class="checkbox-group">
              <BaseCheckBox
                v-model="formData.tieneVehiculo"
                label="¿Tiene vehículo disponible para el curso?"
                class="checkbox-field"
              />
              
              <div v-if="formData.tieneVehiculo" class="vehicle-info">
                <div class="form-grid">
                  <InputBase
                    v-model="formData.patenteVehiculo"
                    label="Patente del vehículo *"
                    placeholder="Ej: AB123CD"
                    :required="formData.tieneVehiculo"
                    class="form-field"
                  />
                  
                  <InputBase
                    v-model="formData.marcaVehiculo"
                    label="Marca del vehículo *"
                    placeholder="Ej: Toyota, Chevrolet"
                    :required="formData.tieneVehiculo"
                    class="form-field"
                  />
                  
                  <InputBase
                    v-model="formData.modeloVehiculo"
                    label="Modelo del vehículo *"
                    placeholder="Ej: Corolla, Cruze"
                    :required="formData.tieneVehiculo"
                    class="form-field"
                  />
                </div>
              </div>
              
              <BaseCheckBox
                v-model="formData.requiereAlojamiento"
                label="¿Requiere alojamiento durante el curso?"
                class="checkbox-field"
              />

              <BaseCheckBox
                v-model="formData.sobreCupo"
                label="¿Acepta ser considerado para sobre cupo?"
                class="checkbox-field"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Información Adicional</h3>
            
            <InputBase
              v-model="formData.consideraciones"
              label="Consideraciones Adicionales"
              placeholder="Otra información que considere importante"
              type="textarea"
              :rows="3"
              class="form-field"
            />
          </div>
        </div>

        <!-- Paso 5: Selección de Curso -->
        <div v-show="currentStep === 4" class="form-step">
          <h2 class="step-title">Selección de Curso</h2>
          <p class="step-description">Seleccione el curso al que desea pre-inscribirse</p>
          
          <div class="courses-grid">
            <div 
              v-for="curso in cursosDisponibles" 
              :key="curso.id"
              :class="['course-option', { 
                selected: formData.cursoId === curso.id,
                disponible: curso.estado === 'disponible',
                lleno: curso.estado === 'lleno'
              }]"
              @click="selectCurso(curso)"
            >
              <div class="course-icon">{{ curso.icono }}</div>
              <div class="course-info">
                <h3 class="course-name">{{ curso.nombre }}</h3>
                <p class="course-dates">{{ curso.fechas }}</p>
                <p class="course-location">📍 {{ curso.ubicacion }}</p>
                <div class="course-meta">
                  <span class="course-cupo">Cupos: {{ curso.inscritos }}/{{ curso.cupoMaximo }}</span>
                  <span v-if="curso.sobreCupo" class="sobre-cupo-badge">Sobre Cupo Disponible</span>
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
            <p v-if="getCursoSeleccionado().sobreCupo" class="sobre-cupo-info">
              ⚠️ Este curso acepta sobre cupo
            </p>
          </div>

          <div v-else class="no-course-selected">
            <p>⚠️ Por favor seleccione un curso para continuar</p>
          </div>
        </div>

        <!-- Paso 6: Resumen y Confirmación -->
        <div v-show="currentStep === 5" class="form-step">
          <h2 class="step-title">Resumen y Confirmación</h2>
          
          <div class="completion-message" v-if="allStepsCompleted">
            <div class="completion-badge">
              <div class="completion-icon">🎉</div>
              <h3>¡Todos los pasos completados exitosamente!</h3>
              <p>El formulario ha sido completado en su totalidad. Revise la información a continuación y confirme su pre-inscripción.</p>
            </div>
          </div>
          
          <div class="summary-container">
            <div class="summary-section">
              <h3 class="summary-title">Resumen de Pre-Inscripción</h3>
              
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
                <div v-if="formData.sobreCupo" class="summary-item">
                  <strong>Sobre Cupo:</strong>
                  <span>✅ Aceptado</span>
                </div>
              </div>
            </div>

            <div class="summary-section">
              <h3 class="summary-title">Datos del Participante</h3>
              
              <div class="summary-grid">
                <div class="summary-item">
                  <strong>Nombre Completo:</strong>
                  <span>{{ formData.nombres }} {{ formData.apellidoPaterno }} {{ formData.apellidoMaterno }}</span>
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
                  <strong>Teléfono:</strong>
                  <span>{{ formData.telefono }} ({{ getTipoTelefonoLabel(formData.tipoTelefono) }})</span>
                </div>
                <div class="summary-item">
                  <strong>Dirección:</strong>
                  <span>{{ formData.direccion }}, {{ getComunaLabel(formData.comuna) }}</span>
                </div>
                <div class="summary-item">
                  <strong>Grupo Scout:</strong>
                  <span>{{ getGrupoLabel(formData.grupo) }}</span>
                </div>
                <div class="summary-item">
                  <strong>Rama:</strong>
                  <span>{{ getRamaLabel(formData.rama) }}</span>
                </div>
                <div class="summary-item">
                  <strong>Rol:</strong>
                  <span>{{ getRolLabel(formData.rol) }}</span>
                </div>
                <div v-if="formData.tieneVehiculo" class="summary-item">
                  <strong>Vehículo:</strong>
                  <span>{{ formData.marcaVehiculo }} {{ formData.modeloVehiculo }} - {{ formData.patenteVehiculo }}</span>
                </div>
                <div class="summary-item">
                  <strong>Foto:</strong>
                  <span>{{ formData.fotoParticipante ? '✓ Subida' : '❌ Pendiente' }}</span>
                </div>
              </div>
            </div>

            <!-- Sección de Verificación -->
            <div class="verification-section">
              <div class="verification-badge">
                <img src="@/assets/Logo_Boyscout_Chile.png" alt="Logo Scouts Chile" class="verification-logo">
                <div class="verification-content">
                  <div class="verified-tick">✓</div>
                  <h3>¡Pre-inscripción Lista para Confirmar!</h3>
                  <p>El participante está listo para ser pre-inscrito en el sistema</p>
                  <p class="verification-note">Al confirmar, recibirá un correo de confirmación con los siguientes pasos</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Navegación del Formulario -->
        <div class="form-navigation">
          <BaseButton
            v-if="currentStep > 0"
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
            {{ submitting ? 'Enviando...' : '✅ Confirmar Pre-Inscripción' }}
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
        <h3>¡Pre-Inscripción Exitosa!</h3>
        <p>Su formulario ha sido registrado correctamente en el sistema Scouts Biobío.</p>
        
        <div class="success-details">
          <div class="detail-item">
            <strong>Curso:</strong>
            <span>{{ getCursoSeleccionado().nombre }}</span>
          </div>
          <div class="detail-item">
            <strong>Participante:</strong>
            <span>{{ formData.nombres }} {{ formData.apellidoPaterno }} {{ formData.apellidoMaterno }}</span>
          </div>
          <div class="detail-item">
            <strong>Rol:</strong>
            <span>{{ getRolLabel(formData.rol) }}</span>
          </div>
        </div>

        <!-- Logo y verificación en el modal -->
        <div class="modal-verification">
          <img src="@/assets/Logo_Boyscout_Chile.png" alt="Logo Scouts Chile" class="modal-logo">
          <div class="modal-verified">
            <span class="modal-tick">✓</span>
            <span>Pre-inscripción verificada</span>
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
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'

import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCheckBox from '@/components/BaseCheckBox.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import InputBase from '@/components/InputBase.vue'
import FileUploader from '@/components/FileUploader.vue'

export default {
  name: 'FormularioPreInscripcion2',
  components: {
    BaseAlert,
    BaseButton,
    BaseCheckBox,
    BaseModal,
    BaseSelect,
    InputBase,
    FileUploader
  },
  setup() {
    const currentStep = ref(0)
    const submitting = ref(false)
    const showSuccessModal = ref(false)
    const fotoPreviewUrl = ref('')
    const mostrarCampoMMAA = ref(false)
    const mostrarEducacionFormador = ref(false)
    const telefonoPlaceholder = ref('+56 9 1234 5678')

    const steps = ref([
      { label: 'Datos Personales', valid: false, completed: false },
      { label: 'Información Scout', valid: false, completed: false },
      { label: 'Salud', valid: false, completed: false },
      { label: 'Adicional', valid: false, completed: false },
      { label: 'Curso', valid: false, completed: false },
      { label: 'Confirmación', valid: false, completed: false }
    ])

    const formData = reactive({
      // Paso 1 - Datos Personales
      nombres: '',
      apellidoPaterno: '',
      apellidoMaterno: '',
      rut: '',
      fechaNacimiento: '',
      estadoCivil: '',
      direccion: '',
      region: '',
      provincia: '',
      comuna: '',
      email: '',
      tipoTelefono: 'movil',
      telefono: '',
      fotoParticipante: null,
      
      // Paso 2 - Información Scout
      zona: '',
      distrito: '',
      grupo: '',
      rama: '',
      rol: '',
      nivel: '',
      numeroMMAA: '',
      nivelEducacion: '',
      
      // Paso 3 - Salud
      alimentacion: '',
      alergias: '',
      limitaciones: '',
      contactoEmergenciaNombre: '',
      contactoEmergenciaTelefono: '',
      
      // Paso 4 - Adicional
      profesion: '',
      apodo: '',
      tieneVehiculo: false,
      patenteVehiculo: '',
      marcaVehiculo: '',
      modeloVehiculo: '',
      requiereAlojamiento: false,
      trabajaConNNAJ: false,
      rangoEdadNNAJ: '',
      sobreCupo: false,
      consideraciones: '',
      
      // Paso 5 - Curso
      cursoId: ''
    })

    const systemAlert = reactive({
      visible: false,
      type: 'informacion',
      title: 'Bienvenido al Sistema de Pre-Inscripción',
      message: 'Complete el formulario para pre-inscribirse en los cursos de la Zona Biobío.'
    })

    // Datos para selects y opciones
    const estadosCiviles = [
      { value: 1, label: 'Soltero' },
      { value: 2, label: 'Casado' },
      { value: 3, label: 'Divorciado' },
      { value: 4, label: 'Viudo' },
      { value: 5, label: 'Unión Civil' }
    ]

    const tiposTelefono = [
      { value: 'movil', label: 'Móvil' },
      { value: 'casa', label: 'Casa' },
      { value: 'trabajo', label: 'Trabajo' }
    ]

    const regiones = [
      { value: 1, label: 'Región del Biobío' }
    ]

    const provincias = [
      { value: 1, label: 'Provincia de Concepción' },
      { value: 2, label: 'Provincia de Biobío' },
      { value: 3, label: 'Provincia de Arauco' }
    ]

    const comunas = [
      { value: 1, label: 'Concepción' },
      { value: 2, label: 'Talcahuano' },
      { value: 3, label: 'Chiguayante' },
      { value: 4, label: 'San Pedro de la Paz' },
      { value: 5, label: 'Coronel' },
      { value: 6, label: 'Lota' },
      { value: 7, label: 'Penco' },
      { value: 8, label: 'Tomé' },
      { value: 9, label: 'Hualpén' },
      { value: 10, label: 'Florida' },
      { value: 11, label: 'Santa Juana' },
      { value: 12, label: 'Hualqui' },
      { value: 13, label: 'Los Ángeles' },
      { value: 14, label: 'Cabrero' },
      { value: 15, label: 'Yumbel' },
      { value: 16, label: 'Laja' },
      { value: 17, label: 'Mulchén' },
      { value: 18, label: 'Nacimiento' },
      { value: 19, label: 'Negrete' },
      { value: 20, label: 'Quilaco' },
      { value: 21, label: 'Quilleco' },
      { value: 22, label: 'San Rosendo' },
      { value: 23, label: 'Santa Bárbara' },
      { value: 24, label: 'Tucapel' },
      { value: 25, label: 'Antuco' },
      { value: 26, label: 'Alto Biobío' },
      { value: 27, label: 'Lebu' },
      { value: 28, label: 'Arauco' },
      { value: 29, label: 'Cañete' },
      { value: 30, label: 'Curanilahue' },
      { value: 31, label: 'Los Álamos' },
      { value: 32, label: 'Tirúa' },
      { value: 33, label: 'Contulmo' }
    ]

    const zonas = [
      { value: 1, label: 'Zona Centro' },
      { value: 2, label: 'Zona Norte' },
      { value: 3, label: 'Zona Sur' },
      { value: 4, label: 'Zona Costa' }
    ]

    const distritos = [
      { value: 1, label: 'Distrito Centro' },
      { value: 2, label: 'Distrito Norte' },
      { value: 3, label: 'Distrito Sur' },
      { value: 4, label: 'Distrito Costa' }
    ]

    const grupos = [
      { value: 1, label: 'Grupo Scout 1 - Concepción' },
      { value: 2, label: 'Grupo Scout 2 - Talcahuano' },
      { value: 3, label: 'Grupo Scout 3 - Chiguayante' },
      { value: 4, label: 'Grupo Scout 4 - San Pedro' },
      { value: 5, label: 'Grupo Scout 5 - Los Ángeles' },
      { value: 6, label: 'Grupo Scout 6 - Cabrero' }
    ]

    const ramas = [
      { value: 1, label: 'Manada' },
      { value: 2, label: 'Tropa' },
      { value: 3, label: 'Comunidad' },
      { value: 4, label: 'Clan' }
    ]

    const roles = [
      { value: 1, label: 'Participante' },
      { value: 2, label: 'Formador' },
      { value: 3, label: 'Director' },
      { value: 4, label: 'Coordinador' },
      { value: 5, label: 'Apoyo' }
    ]

    const niveles = [
      { value: 0, label: 'N° Niveles' },
      { value: 1, label: 'Nivel Inicial' },
      { value: 2, label: 'Nivel Medio' },
      { value: 3, label: 'Nivel Avanzado' }
    ]

    const tiposAlimentacion = [
      { value: 1, label: 'Normal' },
      { value: 2, label: 'Vegetariano' },
      { value: 3, label: 'Vegano' },
      { value: 4, label: 'Celíaco' },
      { value: 5, label: 'Diabético' },
      { value: 6, label: 'Sin Restricciones' }
    ]

    const cursosDisponibles = [
      {
        id: 1,
        nombre: 'Curso Medio - Liderazgo Scout',
        fechas: '01-03 Feb 2024',
        ubicacion: 'Campamento Los Pinos, Concepción',
        cupoMaximo: 26,
        inscritos: 18,
        estado: 'disponible',
        sobreCupo: true,
        icono: '🏕️'
      },
      {
        id: 2,
        nombre: 'Primeros Auxilios en Terreno',
        fechas: '10-11 Feb 2024',
        ubicacion: 'Sede Scouts Talcahuano',
        cupoMaximo: 20,
        inscritos: 20,
        estado: 'lleno',
        sobreCupo: false,
        icono: '🩹'
      },
      {
        id: 3,
        nombre: 'Educación Ambiental Scout',
        fechas: '15-16 Feb 2024',
        ubicacion: 'Reserva Nacional Nonguén',
        cupoMaximo: 25,
        inscritos: 12,
        estado: 'disponible',
        sobreCupo: true,
        icono: '🌿'
      }
    ]

    // Método para actualizar el formato del teléfono según el tipo seleccionado
    const actualizarFormatoTelefono = () => {
      // Limpiar el campo de teléfono cuando cambia el tipo
      formData.telefono = ''
      
      // Actualizar el placeholder según el tipo de teléfono
      switch (formData.tipoTelefono) {
        case 'movil':
          telefonoPlaceholder.value = '+56 9 1234 5678'
          break
        case 'casa':
          telefonoPlaceholder.value = '+56 41 123 4567'
          break
        case 'trabajo':
          telefonoPlaceholder.value = '+56 41 123 4567'
          break
        default:
          telefonoPlaceholder.value = '+56 9 1234 5678'
      }
    }

    // Computed properties corregidas
    const currentStepValid = computed(() => {
      switch (currentStep.value) {
        case 0: // Datos Personales
          return !!(
            formData.nombres &&
            formData.apellidoPaterno &&
            formData.rut &&
            formData.fechaNacimiento &&
            formData.estadoCivil &&
            formData.direccion &&
            formData.region &&
            formData.provincia &&
            formData.comuna &&
            formData.email &&
            formData.telefono &&
            formData.fotoParticipante
          )
        
        case 1: // Información Scout
          const scoutValid = !!(
            formData.zona &&
            formData.distrito &&
            formData.grupo &&
            formData.rama &&
            formData.rol &&
            formData.nivel
          )
          // Si es formador, validar nivel de educación
          if (formData.rol === 2) {
            return scoutValid && !!formData.nivelEducacion
          }
          return scoutValid
        
        case 2: // Salud
          return !!(
            formData.alimentacion &&
            formData.contactoEmergenciaNombre &&
            formData.contactoEmergenciaTelefono
          )
        
        case 3: // Adicional
          let adicionalValid = true
          // Validar vehículo si está marcado
          if (formData.tieneVehiculo) {
            adicionalValid = adicionalValid && !!(
              formData.patenteVehiculo &&
              formData.marcaVehiculo &&
              formData.modeloVehiculo
            )
          }
          // Validar rango de edad si trabaja con NNAJ
          if (formData.trabajaConNNAJ) {
            adicionalValid = adicionalValid && !!formData.rangoEdadNNAJ
          }
          return adicionalValid
        
        case 4: // Curso
          return !!formData.cursoId
        
        case 5: // Confirmación
          return true
        
        default:
          return false
      }
    })

    const formValid = computed(() => {
      return currentStepValid.value
    })

    const allStepsCompleted = computed(() => {
      return steps.value.slice(0, -1).every(step => step.completed)
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

    const getTipoTelefonoLabel = (value) => {
      const option = tiposTelefono.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    const getComunaLabel = (value) => {
      const option = comunas.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    const getGrupoLabel = (value) => {
      const option = grupos.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    const getRamaLabel = (value) => {
      const option = ramas.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    const getRolLabel = (value) => {
      const option = roles.find(opt => opt.value === value)
      return option ? option.label : ''
    }

    // Manejo de archivos de foto
    const handleFileChanged = (file) => {
      formData.fotoParticipante = file
    }

    const removePhoto = () => {
      formData.fotoParticipante = null
      if (fotoPreviewUrl.value) {
        URL.revokeObjectURL(fotoPreviewUrl.value)
        fotoPreviewUrl.value = ''
      }
    }

    // Navegación corregida
    const nextStep = () => {
      if (currentStepValid.value) {
        steps.value[currentStep.value].completed = true
        
        if (currentStep.value < steps.value.length - 1) {
          currentStep.value++
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }
      } else {
        showAlert('error', 'Campos incompletos', 'Por favor complete todos los campos requeridos antes de continuar.')
      }
    }

    const previousStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const submitForm = async () => {
      if (!formValid.value) {
        showAlert('error', 'Formulario incompleto', 'Por favor complete todos los campos requeridos.')
        return
      }

      submitting.value = true

      try {
        await new Promise(resolve => setTimeout(resolve, 3000))
        
        steps.value.forEach(step => {
          step.completed = true
          step.valid = true
        })
        
        showSuccessModal.value = true
        showAlert('exito', 'Pre-inscripción exitosa', 'Su pre-inscripción ha sido registrada correctamente.')
        
      } catch (error) {
        showAlert('error', 'Error en la pre-inscripción', 'Ha ocurrido un error al procesar su solicitud. Por favor intente nuevamente.')
      } finally {
        submitting.value = false
      }
    }

    const handleModalClose = () => {
      showSuccessModal.value = false
      // Resetear formulario
      Object.keys(formData).forEach(key => {
        if (typeof formData[key] === 'boolean') {
          formData[key] = false
        } else {
          formData[key] = ''
        }
      })
      formData.tipoTelefono = 'movil'
      formData.fotoParticipante = null
      
      if (fotoPreviewUrl.value) {
        URL.revokeObjectURL(fotoPreviewUrl.value)
        fotoPreviewUrl.value = ''
      }
      
      steps.value.forEach(step => {
        step.completed = false
        step.valid = false
      })
      
      currentStep.value = 0
      telefonoPlaceholder.value = '+56 9 1234 5678'
    }

    // Watchers para campos condicionales
    watch(() => formData.nivel, (newVal) => {
      // Mostrar número MMAA solo para niveles Medio (2) y Avanzado (3)
      mostrarCampoMMAA.value = (newVal == 2 || newVal == 3)
    })

    watch(() => formData.rol, (newVal) => {
      // Mostrar nivel de educación solo para el rol Formador (2)
      mostrarEducacionFormador.value = (newVal == 2)
    })

    // Watcher para vista previa de foto
    watch(() => formData.fotoParticipante, (newFile) => {
      if (newFile) {
        if (fotoPreviewUrl.value) {
          URL.revokeObjectURL(fotoPreviewUrl.value)
        }
        fotoPreviewUrl.value = URL.createObjectURL(newFile)
      } else {
        if (fotoPreviewUrl.value) {
          URL.revokeObjectURL(fotoPreviewUrl.value)
          fotoPreviewUrl.value = ''
        }
      }
    })

    onMounted(() => {
      console.log('Formulario de pre-inscripción Scouts Biobío montado')
      
      setTimeout(() => {
        systemAlert.visible = true
      }, 500)
    })

    return {
      currentStep,
      steps,
      formData,
      systemAlert,
      submitting,
      showSuccessModal,
      fotoPreviewUrl,
      mostrarCampoMMAA,
      mostrarEducacionFormador,
      telefonoPlaceholder,
      estadosCiviles,
      tiposTelefono,
      regiones,
      provincias,
      comunas,
      zonas,
      distritos,
      grupos,
      ramas,
      roles,
      niveles,
      tiposAlimentacion,
      cursosDisponibles,
      currentStepValid,
      formValid,
      allStepsCompleted,
      clearSystemAlert,
      selectCurso,
      getCursoSeleccionado,
      getTipoTelefonoLabel,
      getComunaLabel,
      getGrupoLabel,
      getRamaLabel,
      getRolLabel,
      handleFileChanged,
      removePhoto,
      nextStep,
      previousStep,
      submitForm,
      handleModalClose,
      actualizarFormatoTelefono
    }
  }
}
</script>

<style scoped>
/* Los estilos permanecen exactamente iguales */
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
  cursor: not-allowed;
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
  animation: fadeInUp 0.3s ease-out;
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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-field {
  margin-bottom: 1rem;
}

.field-note {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
  font-style: italic;
}

.vehicle-info {
  margin-left: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #2c5aa0;
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

.course-option.disponible {
  cursor: pointer;
}

.course-option.lleno {
  cursor: not-allowed;
  opacity: 0.6;
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

.sobre-cupo-badge {
  background: #ffc107;
  color: #856404;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
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

.sobre-cupo-info {
  color: #856404;
  background: #fff3cd;
  padding: 0.5rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}

.no-course-selected {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-top: 1rem;
  color: #856404;
}

/* Estilos para la vista previa de la foto */
.photo-preview {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.photo-preview h4 {
  color: #495057;
  margin-bottom: 1rem;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.preview-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  border: 2px solid #2c5aa0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.remove-photo-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.remove-photo-btn:hover {
  background: #c82333;
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

/* Mensaje de completado */
.completion-message {
  margin-bottom: 2rem;
}

.completion-badge {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 2px solid #28a745;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  color: #155724;
}

.completion-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.completion-badge h3 {
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.completion-badge p {
  font-size: 1.1rem;
  opacity: 0.9;
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
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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

/* Sección de verificación */
.verification-section {
  margin-top: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
  border-radius: 12px;
  border: 2px solid #28a745;
}

.verification-badge {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: left;
}

.verification-logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid #28a745;
  background: white;
  padding: 0.5rem;
}

.verification-content {
  flex: 1;
}

.verified-tick {
  width: 40px;
  height: 40px;
  background: #28a745;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.verification-note {
  font-size: 0.9rem;
  color: #28a745;
  font-style: italic;
  margin-top: 0.5rem;
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

.modal-verification {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8fff8;
  border-radius: 8px;
  border: 1px solid #28a745;
}

.modal-logo {
  width: 50px;
  height: 50px;
}

.modal-verified {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #28a745;
  font-weight: 600;
}

.modal-tick {
  width: 25px;
  height: 25px;
  background: #28a745;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
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

/* Campos de texto más grandes para alergias */
.alergias-field textarea {
  min-height: 100px;
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
  
  .verification-badge {
    flex-direction: column;
    text-align: center;
  }
  
  .modal-verification {
    flex-direction: column;
  }
  
  .completion-badge {
    padding: 1.5rem;
  }
  
  .completion-badge h3 {
    font-size: 1.3rem;
  }
  
  .preview-container {
    text-align: center;
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
  
  .vehicle-info {
    margin-left: 0;
  }
  
  .summary-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .photo-preview {
    padding: 1rem;
  }
  
  .preview-image {
    max-width: 150px;
    max-height: 150px;
  }
}
</style>
[file content end]