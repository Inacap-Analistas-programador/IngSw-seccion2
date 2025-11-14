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

    <!-- Progreso del Formulario REORDENADO -->
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

    <!-- Contenido del Formulario REORDENADO -->
    <div class="form-container">
      <form @submit.prevent="submitForm" class="scouts-form">
        
        <!-- Paso 1: Selección de Curso (PRIMER PASO) -->
        <div v-show="currentStep === 0" class="form-step">
          <h2 class="step-title">Selección de Curso</h2>
          <p class="step-description">Seleccione el curso al que desea pre-inscribirse</p>
          
          <div class="intro-message">
            <p>Bienvenido al sistema de pre-inscripción de la Zona Biobío. Complete este formulario para participar en nuestros cursos de formación.</p>
          </div>
          
          <div class="courses-grid-uniform">
            <div 
              v-for="curso in cursosDisponibles" 
              :key="curso.id"
              :class="['course-option-uniform', { 
                selected: formData.cursoId === curso.id
              }]"
              @click="selectCurso(curso)"
            >
              <div class="course-icon-uniform">{{ curso.icono }}</div>
              <div class="course-info-uniform">
                <h3 class="course-name-uniform">{{ curso.nombre }}</h3>
                <p class="course-dates-uniform">{{ curso.fechas }}</p>
                <p class="course-location-uniform">📍 {{ curso.ubicacion }}</p>
                <div class="course-meta-uniform">
                  <span class="course-cupo-uniform">Cupos: {{ curso.inscritos }}/{{ curso.cupoMaximo }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="formData.cursoId" class="selected-course-info-uniform">
            <h4>Curso seleccionado:</h4>
            <p><strong>{{ getCursoSeleccionado().nombre }}</strong></p>
            <p>{{ getCursoSeleccionado().fechas }} - {{ getCursoSeleccionado().ubicacion }}</p>
          </div>

          <div v-else class="no-course-selected-uniform">
            <p>⚠️ Por favor seleccione un curso para continuar</p>
          </div>
        </div>

        <!-- Paso 2: Datos Personales (CON NUEVOS CAMPOS) -->
        <div v-show="currentStep === 1" class="form-step">
          <h2 class="step-title">Datos Personales</h2>
          
          <div class="form-section">
            <h3 class="section-title">Información Básica</h3>
            <div class="form-grid-expanded">
              <InputBase
                v-model="formData.nombres"
                label="Nombres *"
                placeholder="Ingrese sus nombres"
                :required="true"
                class="form-field-expanded"
              />
              
              <InputBase
                v-model="formData.apellidoPaterno"
                label="Apellido Paterno *"
                placeholder="Ingrese su apellido paterno"
                :required="true"
                class="form-field-expanded"
              />
              
              <InputBase
                v-model="formData.apellidoMaterno"
                label="Apellido Materno"
                placeholder="Ingrese su apellido materno"
                class="form-field-expanded"
              />
              
              <InputBase
                v-model="formData.rut"
                label="RUT *"
                placeholder="12345678-9"
                :required="true"
                rules="rut"
                class="form-field-expanded"
              />
              
              <InputBase
                v-model="formData.fechaNacimiento"
                label="Fecha de Nacimiento *"
                type="date"
                :required="true"
                class="form-field-expanded"
              />

              <BaseSelect
                v-model="formData.estadoCivil"
                :options="estadosCiviles"
                label="Estado Civil *"
                placeholder="Seleccione su estado civil"
                :required="true"
                class="form-field-expanded select-field-expanded"
              />

              <!-- NUEVO CAMPO: Religión -->
              <InputBase
                v-model="formData.religion"
                label="Religión"
                placeholder="RELIGIÓN"
                class="form-field-expanded"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Foto para Credencial</h3>
            <FileUploader
              v-model="formData.fotoParticipante"
              label="Foto de cara del participante *"
              accept="image/jpeg,image/png,image/jpg"
              :required="true"
              uploadType="image"
              class="form-field-expanded"
            />
            <p class="field-note">Formatos aceptados: JPG, PNG. Foto frontal clara para la credencial.</p>
          </div>

          <div class="form-section">
            <h3 class="section-title">Contacto</h3>
            <div class="form-row-contacto-expanded">
              <InputBase
                v-model="formData.email"
                label="Correo Electrónico *"
                placeholder="ejemplo@correo.com"
                :required="true"
                rules="email"
                type="email"
                class="form-field-expanded"
              />
              
              <div class="telefono-group-expanded">
                <BaseSelect
                  v-model="formData.tipoTelefono"
                  :options="tiposTelefono"
                  label="Tipo de Teléfono *"
                  placeholder="Seleccione tipo"
                  :required="true"
                  class="form-field-expanded select-field-expanded telefono-select-expanded"
                  @change="actualizarPlaceholderTelefono"
                />
                
                <div class="telefono-input-container-expanded">
                  <label class="input-label-expanded">Teléfono *</label>
                  <div class="telefono-input-wrapper-expanded">
                    <span class="telefono-prefijo-expanded">+56</span>
                    <input
                      v-model="formData.telefono"
                      :placeholder="telefonoPlaceholder"
                      :required="true"
                      class="telefono-input-expanded"
                      type="text"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Dirección</h3>
            <div class="form-grid-expanded">
              <InputBase
                v-model="formData.direccion"
                label="Dirección *"
                placeholder="Ingrese su dirección completa"
                :required="true"
                class="form-field-expanded"
              />
              
              <BaseSelect
                v-model="formData.region"
                :options="regiones"
                label="Región *"
                placeholder="Seleccione su región"
                :required="true"
                class="form-field-expanded select-field-expanded"
                @change="actualizarProvincias"
              />
              
              <BaseSelect
                v-model="formData.provincia"
                :options="provinciasFiltradas"
                label="Provincia *"
                placeholder="Seleccione su provincia"
                :required="true"
                :disabled="!formData.region"
                class="form-field-expanded select-field-expanded"
                @change="actualizarComunas"
              />
              
              <BaseSelect
                v-model="formData.comuna"
                :options="comunasFiltradas"
                label="Comuna *"
                placeholder="Seleccione su comuna"
                :required="true"
                :disabled="!formData.provincia"
                class="form-field-expanded select-field-expanded"
              />
            </div>
          </div>
        </div>

        <!-- Paso 3: Información Asociación Scout (RENOMBRADO) -->
        <div v-show="currentStep === 2" class="form-step">
          <h2 class="step-title">Información Asociación Scout</h2>
          
          <div class="form-grid-expanded">
            <BaseSelect
              v-model="formData.zona"
              :options="zonas"
              label="Zona"
              placeholder="Seleccione su zona"
              class="form-field-expanded select-field-expanded"
            />
            
            <BaseSelect
              v-model="formData.distrito"
              :options="distritos"
              label="Distrito"
              placeholder="Seleccione su distrito"
              class="form-field-expanded select-field-expanded"
            />
            
            <BaseSelect
              v-model="formData.grupo"
              :options="grupos"
              label="Grupo Scout"
              placeholder="Seleccione su grupo"
              class="form-field-expanded select-field-expanded"
            />
            
            <BaseSelect
              v-model="formData.rama"
              :options="ramas"
              label="Rama de Curso *"
              placeholder="Seleccione su rama"
              :required="true"
              class="form-field-expanded select-field-expanded"
            />
          </div>

          <div class="form-section">
            <h3 class="section-title">Rol y Formación</h3>
            <div class="form-row-expanded">
              <BaseSelect
                v-model="formData.rol"
                :options="roles"
                label="Rol en el Curso *"
                placeholder="Seleccione su rol"
                :required="true"
                class="form-field-expanded select-field-expanded"
              />
              
              <BaseSelect
                v-model="formData.nivel"
                :options="niveles"
                label="N° Niveles *"
                placeholder="Seleccione su nivel"
                :required="true"
                class="form-field-expanded select-field-expanded"
              />
            </div>
            
            <InputBase
              v-if="mostrarCampoMMAA"
              v-model="formData.numeroMMAA"
              label="Número MMAA"
              placeholder="Ej: 5208"
              class="form-field-expanded"
            />

            <InputBase
              v-if="mostrarEducacionFormador"
              v-model="formData.nivelEducacion"
              label="Nivel de Educación"
              placeholder="Ingrese su nivel de educación"
              class="form-field-expanded"
            />
          </div>
        </div>

        <!-- Paso 4: Salud y Alimentación (CON FICHA MÉDICA) -->
        <div v-show="currentStep === 3" class="form-step">
          <h2 class="step-title">Salud y Alimentación</h2>
          
          <div class="form-section">
            <h3 class="section-title">Preferencias y Restricciones</h3>
            
            <BaseSelect
              v-model="formData.alimentacion"
              :options="tiposAlimentacion"
              label="Tipo de Alimentación *"
              placeholder="Seleccione su tipo de alimentación"
              :required="true"
              class="form-field-expanded select-field-expanded"
            />

            <div class="form-row-expanded">
              <InputBase
                v-model="formData.alergias"
                label="Alergias o Enfermedades"
                placeholder="Describa sus alergias o enfermedades"
                type="textarea"
                :rows="8"
                class="form-field-expanded textarea-field-expanded extra-large-textarea"
              />
              
              <InputBase
                v-model="formData.limitaciones"
                label="Limitaciones"
                placeholder="Describa sus limitaciones"
                type="textarea"
                :rows="8"
                class="form-field-expanded textarea-field-expanded extra-large-textarea"
              />
            </div>

            <!-- NUEVO: Subida de Ficha Médica -->
            <FileUploader
              v-model="formData.fichaMedica"
              label="Ficha Médica (Opcional)"
              accept=".pdf,.doc,.docx,.txt"
              uploadType="document"
              class="form-field-expanded"
            />
            <p class="field-note">Formatos aceptados: PDF, Word, TXT</p>
          </div>

          <div class="form-section">
            <h3 class="section-title">Contacto de Emergencia</h3>
            <div class="form-grid-expanded">
              <InputBase
                v-model="formData.contactoEmergenciaNombre"
                label="Nombre Contacto Emergencia *"
                placeholder="Nombre completo"
                :required="true"
                class="form-field-expanded"
              />
              
              <div class="telefono-input-container-expanded">
                <label class="input-label-expanded">Teléfono Emergencia *</label>
                <div class="telefono-input-wrapper-expanded">
                  <span class="telefono-prefijo-expanded">+56</span>
                  <input
                    v-model="formData.contactoEmergenciaTelefono"
                    placeholder="8 1234 5678"
                    :required="true"
                    class="telefono-input-expanded"
                    type="text"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paso 5: Información Adicional (CON NUEVOS CAMPOS) -->
        <div v-show="currentStep === 4" class="form-step">
          <h2 class="step-title">Información Adicional</h2>
          
          <div class="form-section">
            <h3 class="section-title">Información Personal</h3>
            
            <div class="form-row-expanded">
              <InputBase
                v-model="formData.profesion"
                label="Profesión u Oficio"
                placeholder="Su profesión u oficio"
                class="form-field-expanded"
              />
              
              <InputBase
                v-model="formData.apodo"
                label="Apodo para Credencial"
                placeholder="Apodo que aparecerá en su credencial"
                class="form-field-expanded"
              />
            </div>

            <!-- NUEVO: Campo Beneficiario (TEXTO MODIFICADO) -->
            <div class="checkbox-group-expanded">
              <BaseCheckBox
                v-model="formData.beneficiario"
                label="¿Ha sido beneficiario?"
                class="checkbox-field-expanded"
              />
              
              <BaseCheckBox
                v-model="formData.trabajaConNNAJ"
                label="¿Ha trabajado con Niños, Niñas y Jóvenes?"
                class="checkbox-field-expanded"
              />
              
              <InputBase
                v-if="formData.trabajaConNNAJ"
                v-model="formData.rangoEdadNNAJ"
                label="Rango de edad con el que trabaja"
                placeholder="Ej: 6-12 años, 13-17 años"
                class="form-field-expanded"
              />
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-title">Logística</h3>
            
            <div class="checkbox-group-expanded">
              <BaseCheckBox
                v-model="formData.tieneVehiculo"
                label="¿Tiene vehículo disponible para el curso?"
                class="checkbox-field-expanded"
              />
              
              <div v-if="formData.tieneVehiculo" class="vehicle-info-expanded">
                <div class="form-grid-expanded">
                  <InputBase
                    v-model="formData.patenteVehiculo"
                    label="Patente del vehículo"
                    placeholder="Ej: CBDJ-K7"
                    class="form-field-expanded"
                  />
                  
                  <InputBase
                    v-model="formData.marcaVehiculo"
                    label="Marca del vehículo"
                    placeholder="Ej: Toyota, Chevrolet"
                    class="form-field-expanded"
                  />
                  
                  <InputBase
                    v-model="formData.modeloVehiculo"
                    label="Modelo del vehículo"
                    placeholder="Ej: Corolla, Cruze"
                    class="form-field-expanded"
                  />
                </div>
              </div>
              
              <BaseCheckBox
                v-model="formData.requiereAlojamiento"
                label="¿Requiere alojamiento durante el curso?"
                class="checkbox-field-expanded"
              />
            </div>
          </div>

          <!-- NUEVO: Campo Observaciones (AGRANDADO) -->
          <div class="form-section">
            <h3 class="section-title">Observaciones</h3>
            
            <InputBase
              v-model="formData.observaciones"
              label="Observaciones Generales"
              placeholder="Otra información que considere importante"
              type="textarea"
              :rows="36"
              class="form-field-expanded textarea-field-expanded extra-large-textarea super-large-textarea"
              @keydown.enter.prevent="handleObservacionesEnter"
            />
            <p class="field-note">Presione Enter para ir a revisar sus datos, o use el botón 'Revisar' →</p>
          </div>
        </div>

        <!-- Paso 6: Resumen y Confirmación (SIMPLIFICADO) -->
        <div v-show="currentStep === 5" class="form-step">
          <h2 class="step-title">Resumen y Confirmación</h2>
          
          <div class="summary-container-expanded">
            <!-- Resumen simplificado sin información extra -->
            <div class="summary-section-expanded">
              <h3 class="summary-title-expanded">Resumen de Pre-Inscripción</h3>
              
              <div class="summary-grid-expanded">
                <div class="summary-item-expanded">
                  <strong>Curso:</strong>
                  <span>{{ getCursoSeleccionado().nombre }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Participante:</strong>
                  <span>{{ formData.nombres }} {{ formData.apellidoPaterno }} {{ formData.apellidoMaterno }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>RUT:</strong>
                  <span>{{ formData.rut }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Teléfono:</strong>
                  <span>+56 {{ formData.telefono }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Región:</strong>
                  <span>{{ getRegionLabel(formData.region) }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Provincia:</strong>
                  <span>{{ getProvinciaLabel(formData.provincia) }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Comuna:</strong>
                  <span>{{ getComunaLabel(formData.comuna) }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Dirección:</strong>
                  <span>{{ formData.direccion }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Email:</strong>
                  <span>{{ formData.email }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Rama:</strong>
                  <span>{{ getRamaLabel(formData.rama) }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Rol:</strong>
                  <span>{{ getRolLabel(formData.rol) }}</span>
                </div>
                <div class="summary-item-expanded">
                  <strong>Nivel:</strong>
                  <span>{{ getNivelLabel(formData.nivel) }}</span>
                </div>
              </div>
            </div>

            <!-- Solo una alerta al final -->
            <BaseAlert
              v-if="showFinalAlert"
              type="informacion"
              title="Verifique sus datos"
              message="Revise que toda la información sea correcta antes de confirmar la pre-inscripción."
              class="final-alert-expanded"
            />
          </div>
        </div>

        <!-- Navegación del Formulario CORREGIDA -->
        <div class="form-navigation-expanded">
          <BaseButton
            v-if="currentStep > 0"
            type="button"
            variant="secondary"
            @click="previousStep"
            :disabled="submitting || isNavigating"
            class="nav-button-expanded"
          >
            ← Anterior
          </BaseButton>
          
          <div class="nav-spacer-expanded"></div>
          
          <BaseButton
            v-if="currentStep < steps.length - 1"
            type="button"
            variant="primary"
            @click="nextStep"
            :disabled="!isStepValid(currentStep) || submitting || isNavigating"
            class="nav-button-expanded"
          >
            {{ currentStep === 4 ? 'Revisar' : 'Siguiente' }} →
          </BaseButton>
          
          <BaseButton
            v-if="currentStep === steps.length - 1"
            type="submit"
            variant="success"
            :disabled="!isFormValid || submitting || isNavigating"
            :loading="submitting"
            class="nav-button-expanded submit-button-expanded"
          >
            {{ submitting ? 'Enviando...' : '✅ Confirmar Pre-Inscripción' }}
          </BaseButton>
        </div>
      </form>
    </div>

    <!-- Modal de Éxito SIMPLIFICADO -->
    <BaseModal
      v-model="showSuccessModal"
      @close="handleModalClose"
    >
      <div class="success-modal-expanded">
        <div class="success-icon-expanded">🎉</div>
        <h3>¡Pre-Inscripción Exitosa!</h3>
        <p>Su formulario ha sido registrado correctamente en el sistema Scouts Biobío.</p>
        
        <div class="success-actions-expanded">
          <BaseButton
            variant="primary"
            @click="handleModalClose"
            class="action-button-expanded"
          >
            Aceptar
          </BaseButton>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'

// Componentes
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
    const showFinalAlert = ref(true)
    const mostrarCampoMMAA = ref(false)
    const mostrarEducacionFormador = ref(false)
    const telefonoPlaceholder = ref('8 1234 5678') // MODIFICADO: Cambiado de 9 a 8
    const isNavigating = ref(false)

    // PASOS CORREGIDOS - Curso como primer paso
    const steps = ref([
      { label: 'Curso', valid: false, completed: false },
      { label: 'Datos Personales', valid: false, completed: false },
      { label: 'Asociación Scout', valid: false, completed: false },
      { label: 'Salud', valid: false, completed: false },
      { label: 'Adicional', valid: false, completed: false },
      { label: 'Confirmación', valid: false, completed: false }
    ])

    const formData = reactive({
      // Paso 1 - Curso (primer paso)
      cursoId: '',
      
      // Paso 2 - Datos Personales (CON NUEVOS CAMPOS)
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
      religion: '', // NUEVO CAMPO
      
      // Paso 3 - Información Asociación Scout
      zona: '',
      distrito: '',
      grupo: '',
      rama: '',
      rol: '',
      nivel: '',
      numeroMMAA: '',
      nivelEducacion: '',
      
      // Paso 4 - Salud (CON VALORES POR DEFECTO)
      alimentacion: '',
      alergias: '',
      limitaciones: '',
      contactoEmergenciaNombre: '',
      contactoEmergenciaTelefono: '',
      fichaMedica: null, // NUEVO CAMPO
      
      // Paso 5 - Adicional (CON NUEVOS CAMPOS)
      profesion: '',
      apodo: '',
      tieneVehiculo: false,
      patenteVehiculo: '',
      marcaVehiculo: '',
      modeloVehiculo: '',
      requiereAlojamiento: false,
      trabajaConNNAJ: false,
      rangoEdadNNAJ: '',
      beneficiario: false, // NUEVO CAMPO
      observaciones: '' // NUEVO CAMPO
    })

    // DATOS DE LOCALIDAD DE CHILE COMPLETOS
    const regiones = ref([
      { value: '1', label: 'Región de Arica y Parinacota' },
      { value: '2', label: 'Región de Tarapacá' },
      { value: '3', label: 'Región de Antofagasta' },
      { value: '4', label: 'Región de Atacama' },
      { value: '5', label: 'Región de Coquimbo' },
      { value: '6', label: 'Región de Valparaíso' },
      { value: '7', label: 'Región Metropolitana de Santiago' },
      { value: '8', label: 'Región del Libertador General Bernardo O\'Higgins' },
      { value: '9', label: 'Región del Maule' },
      { value: '10', label: 'Región de Ñuble' },
      { value: '11', label: 'Región del Biobío' },
      { value: '12', label: 'Región de La Araucanía' },
      { value: '13', label: 'Región de Los Ríos' },
      { value: '14', label: 'Región de Los Lagos' },
      { value: '15', label: 'Región de Aysén del General Carlos Ibáñez del Campo' },
      { value: '16', label: 'Región de Magallanes y de la Antártica Chilena' }
    ])

    const provincias = ref([
      // Región del Biobío (11)
      { value: '38', regionId: '11', label: 'Provincia de Concepción' },
      { value: '39', regionId: '11', label: 'Provincia de Biobío' },
      { value: '40', regionId: '11', label: 'Provincia de Arauco' },
      
      // Otras regiones (ejemplos)
      { value: '1', regionId: '1', label: 'Provincia de Arica' },
      { value: '2', regionId: '1', label: 'Provincia de Parinacota' },
      { value: '22', regionId: '7', label: 'Provincia de Santiago' },
      { value: '23', regionId: '7', label: 'Provincia de Cordillera' }
    ])

    const comunas = ref([
      // Provincia de Concepción (38)
      { value: '219', provinciaId: '38', label: 'Concepción' },
      { value: '220', provinciaId: '38', label: 'Coronel' },
      { value: '221', provinciaId: '38', label: 'Chiguayante' },
      { value: '222', provinciaId: '38', label: 'Florida' },
      { value: '223', provinciaId: '38', label: 'Hualpén' },
      { value: '224', provinciaId: '38', label: 'Hualqui' },
      { value: '225', provinciaId: '38', label: 'Lota' },
      { value: '226', provinciaId: '38', label: 'Penco' },
      { value: '227', provinciaId: '38', label: 'San Pedro de la Paz' },
      { value: '228', provinciaId: '38', label: 'Santa Juana' },
      { value: '229', provinciaId: '38', label: 'Talcahuano' },
      { value: '230', provinciaId: '38', label: 'Tomé' },
      
      // Provincia de Biobío (39)
      { value: '231', provinciaId: '39', label: 'Los Ángeles' },
      { value: '232', provinciaId: '39', label: 'Antuco' },
      { value: '233', provinciaId: '39', label: 'Cabrero' },
      { value: '234', provinciaId: '39', label: 'Laja' },
      { value: '235', provinciaId: '39', label: 'Mulchén' },
      { value: '236', provinciaId: '39', label: 'Nacimiento' },
      { value: '237', provinciaId: '39', label: 'Negrete' },
      { value: '238', provinciaId: '39', label: 'Quilaco' },
      { value: '239', provinciaId: '39', label: 'Quilleco' },
      { value: '240', provinciaId: '39', label: 'San Rosendo' },
      { value: '241', provinciaId: '39', label: 'Santa Bárbara' },
      { value: '242', provinciaId: '39', label: 'Tucapel' },
      { value: '243', provinciaId: '39', label: 'Yumbel' },
      { value: '244', provinciaId: '39', label: 'Alto Biobío' },
      
      // Provincia de Arauco (40)
      { value: '245', provinciaId: '40', label: 'Lebu' },
      { value: '246', provinciaId: '40', label: 'Arauco' },
      { value: '247', provinciaId: '40', label: 'Cañete' },
      { value: '248', provinciaId: '40', label: 'Contulmo' },
      { value: '249', provinciaId: '40', label: 'Curanilahue' },
      { value: '250', provinciaId: '40', label: 'Los Álamos' },
      { value: '251', provinciaId: '40', label: 'Tirúa' },
      
      // Otras comunas de ejemplo
      { value: '1', provinciaId: '1', label: 'Arica' },
      { value: '2', provinciaId: '1', label: 'Camarones' },
      { value: '83', provinciaId: '22', label: 'Santiago' },
      { value: '84', provinciaId: '22', label: 'Cerrillos' }
    ])

    // Datos para selects y opciones
    const estadosCiviles = [
      { value: '1', label: 'Soltero' },
      { value: '2', label: 'Casado' },
      { value: '3', label: 'Divorciado' },
      { value: '4', label: 'Viudo' },
      { value: '5', label: 'Unión Civil' }
    ]

    const tiposTelefono = [
      { value: 'movil', label: 'Móvil' },
      { value: 'casa', label: 'Casa' },
      { value: 'trabajo', label: 'Trabajo' }
    ]

    const zonas = [
      { value: '1', label: 'Zona Centro' },
      { value: '2', label: 'Zona Norte' },
      { value: '3', label: 'Zona Sur' },
      { value: '4', label: 'Zona Costa' }
    ]

    const distritos = [
      { value: '1', label: 'Distrito Centro' },
      { value: '2', label: 'Distrito Norte' },
      { value: '3', label: 'Distrito Sur' },
      { value: '4', label: 'Distrito Costa' }
    ]

    const grupos = [
      { value: '1', label: 'Grupo Scout 1 - Concepción' },
      { value: '2', label: 'Grupo Scout 2 - Talcahuano' },
      { value: '3', label: 'Grupo Scout 3 - Chiguayante' },
      { value: '4', label: 'Grupo Scout 4 - San Pedro' },
      { value: '5', label: 'Grupo Scout 5 - Los Ángeles' },
      { value: '6', label: 'Grupo Scout 6 - Cabrero' }
    ]

    const ramas = [
      { value: '1', label: 'Manada' },
      { value: '2', label: 'Tropa' },
      { value: '3', label: 'Comunidad' },
      { value: '4', label: 'Clan' }
    ]

    const roles = [
      { value: '1', label: 'Participante' },
      { value: '2', label: 'Formador' },
      { value: '3', label: 'Director' },
      { value: '4', label: 'Coordinador' },
      { value: '5', label: 'Apoyo' }
    ]

    const niveles = [
      { value: '0', label: 'N° Niveles' },
      { value: '1', label: 'Nivel Inicial' },
      { value: '2', label: 'Nivel Medio' },
      { value: '3', label: 'Nivel Avanzado' }
    ]

    const tiposAlimentacion = [
      { value: '1', label: 'Normal' },
      { value: '2', label: 'Vegetariano' },
      { value: '3', label: 'Vegano' },
      { value: '4', label: 'Celíaco' },
      { value: '5', label: 'Diabético' },
      { value: '6', label: 'Sin Restricciones' }
    ]

    const cursosDisponibles = [
      {
        id: 1,
        nombre: 'Curso Medio - Liderazgo Scout',
        fechas: '01-03 Feb 2024',
        ubicacion: 'Campamento Los Pinos, Concepción',
        cupoMaximo: 26,
        inscritos: 18,
        icono: '🏕️'
      },
      {
        id: 2,
        nombre: 'Primeros Auxilios en Terreno',
        fechas: '10-11 Feb 2024',
        ubicacion: 'Sede Scouts Talcahuano',
        cupoMaximo: 20,
        inscritos: 20,
        icono: '🩹'
      },
      {
        id: 3,
        nombre: 'Educación Ambiental Scout',
        fechas: '15-16 Feb 2024',
        ubicacion: 'Reserva Nacional Nonguén',
        cupoMaximo: 25,
        inscritos: 12,
        icono: '🌿'
      }
    ]

    // Computed properties para filtrar provincias y comunas
    const provinciasFiltradas = computed(() => {
      if (!formData.region) return []
      return provincias.value.filter(p => p.regionId === formData.region)
    })

    const comunasFiltradas = computed(() => {
      if (!formData.provincia) return []
      return comunas.value.filter(c => c.provinciaId === formData.provincia)
    })

    // CORRECCIÓN CRÍTICA: Validación por paso mejorada
    const isStepValid = (step) => {
      switch (step) {
        case 0: // Selección de Curso
          return !!formData.cursoId
        
        case 1: // Datos Personales
          return !!(
            formData.nombres?.trim() &&
            formData.apellidoPaterno?.trim() &&
            formData.rut?.trim() &&
            formData.fechaNacimiento &&
            formData.direccion?.trim() &&
            formData.region &&
            formData.provincia &&
            formData.comuna &&
            formData.email?.trim() &&
            formData.telefono?.trim()
          )
        
        case 2: // Información Asociación Scout
          return !!(
            formData.rama &&
            formData.rol &&
            formData.nivel
          )
        
        case 3: // Salud
          return !!(
            formData.alimentacion &&
            formData.contactoEmergenciaNombre?.trim() &&
            formData.contactoEmergenciaTelefono?.trim()
          )
        
        case 4: // Adicional - Todos los campos son opcionales
          return true
        
        case 5: // Confirmación
          return true
        
        default:
          return false
      }
    }

    const isFormValid = computed(() => {
      // Verificar que todos los pasos obligatorios estén completos
      return [0, 1, 2, 3].every(step => isStepValid(step))
    })

    // Methods 
    const actualizarProvincias = () => {
      formData.provincia = ''
      formData.comuna = ''
    }

    const actualizarComunas = () => {
      formData.comuna = ''
    }

    const actualizarPlaceholderTelefono = () => {
      switch (formData.tipoTelefono) {
        case 'movil':
          telefonoPlaceholder.value = '8 1234 5678' // MODIFICADO: Cambiado de 9 a 8
          break
        case 'casa':
          telefonoPlaceholder.value = '2 1234 5678'
          break
        case 'trabajo':
          telefonoPlaceholder.value = '2 1234 5678'
          break
        default:
          telefonoPlaceholder.value = '8 1234 5678' // MODIFICADO: Cambiado de 9 a 8
      }
    }

    const selectCurso = (curso) => {
      formData.cursoId = curso.id
    }

    const getCursoSeleccionado = () => {
      return cursosDisponibles.find(curso => curso.id === formData.cursoId) || {}
    }

    // NUEVO: Manejar Enter en el campo de observaciones
    const handleObservacionesEnter = (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        if (currentStep.value === 4) {
          nextStep()
        }
      }
    }

    // FUNCIONES para mostrar etiquetas en el resumen
    const getRegionLabel = (value) => {
      if (!value) return ''
      const region = regiones.value.find(r => r.value === value)
      return region ? region.label : value
    }

    const getProvinciaLabel = (value) => {
      if (!value) return ''
      const provincia = provincias.value.find(p => p.value === value)
      return provincia ? provincia.label : value
    }

    const getComunaLabel = (value) => {
      if (!value) return ''
      const comuna = comunas.value.find(c => c.value === value)
      return comuna ? comuna.label : value
    }

    const getRamaLabel = (value) => {
      if (!value) return ''
      const rama = ramas.find(r => r.value === value)
      return rama ? rama.label : value
    }

    const getRolLabel = (value) => {
      if (!value) return ''
      const rol = roles.find(r => r.value === value)
      return rol ? rol.label : value
    }

    const getNivelLabel = (value) => {
      if (!value) return ''
      const nivel = niveles.find(n => n.value === value)
      return nivel ? nivel.label : value
    }

    // Navegación CORREGIDA - Con protección contra navegación rápida
    const nextStep = async () => {
      if (isNavigating.value) return
      
      isNavigating.value = true
      
      try {
        if (isStepValid(currentStep.value)) {
          steps.value[currentStep.value].completed = true
          steps.value[currentStep.value].valid = true
          
          if (currentStep.value < steps.value.length - 1) {
            currentStep.value++
            // Esperar a que Vue actualice el DOM
            await nextTick()
            window.scrollTo({ top: 0, behavior: 'smooth' })
          }
        } else {
          console.log(`Paso ${currentStep.value} no válido`)
        }
      } finally {
        // Usar setTimeout para asegurar que la navegación se complete
        setTimeout(() => {
          isNavigating.value = false
        }, 100)
      }
    }

    const previousStep = async () => {
      if (isNavigating.value) return
      
      isNavigating.value = true
      
      try {
        if (currentStep.value > 0) {
          currentStep.value--
          // Esperar a que Vue actualice el DOM
          await nextTick()
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }
      } finally {
        // Usar setTimeout para asegurar que la navegación se complete
        setTimeout(() => {
          isNavigating.value = false
        }, 100)
      }
    }

    const submitForm = async () => {
      if (!isFormValid.value) {
        console.log('Formulario no válido')
        return
      }

      submitting.value = true

      try {
        // Simular envío
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Marcar todos los pasos como completados
        steps.value.forEach(step => {
          step.completed = true
          step.valid = true
        })
        
        showSuccessModal.value = true
        
      } catch (error) {
        console.error('Error en la pre-inscripción:', error)
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
        } else if (key === 'tipoTelefono') {
          formData[key] = 'movil'
        } else if (key === 'fotoParticipante' || key === 'fichaMedica') {
          formData[key] = null
        } else {
          formData[key] = ''
        }
      })
      
      // Resetear pasos
      steps.value.forEach(step => {
        step.completed = false
        step.valid = false
      })
      
      currentStep.value = 0
      telefonoPlaceholder.value = '8 1234 5678' // MODIFICADO: Cambiado de 9 a 8
      isNavigating.value = false
    }

    // Watchers para campos condicionales
    watch(() => formData.nivel, (newVal) => {
      // Mostrar número MMAA solo para niveles Medio (2) y Avanzado (3)
      mostrarCampoMMAA.value = (newVal === '2' || newVal === '3')
    })

    watch(() => formData.rol, (newVal) => {
      // Mostrar nivel de educación solo para el rol Formador (2)
      mostrarEducacionFormador.value = (newVal === '2')
    })

    onMounted(() => {
      console.log('Formulario de pre-inscripción Scouts Biobío montado')
    })

    return {
      currentStep,
      steps,
      formData,
      submitting,
      showSuccessModal,
      showFinalAlert,
      mostrarCampoMMAA,
      mostrarEducacionFormador,
      telefonoPlaceholder,
      isNavigating,
      estadosCiviles,
      tiposTelefono,
      regiones,
      provinciasFiltradas,
      comunasFiltradas,
      zonas,
      distritos,
      grupos,
      ramas,
      roles,
      niveles,
      tiposAlimentacion,
      cursosDisponibles,
      isStepValid,
      isFormValid,
      actualizarProvincias,
      actualizarComunas,
      actualizarPlaceholderTelefono,
      selectCurso,
      getCursoSeleccionado,
      getRegionLabel,
      getProvinciaLabel,
      getComunaLabel,
      getRamaLabel,
      getRolLabel,
      getNivelLabel,
      handleObservacionesEnter, // NUEVO: Exportar la función
      nextStep,
      previousStep,
      submitForm,
      handleModalClose
    }
  }
}
</script>

<style scoped>
/* Todos los estilos CSS permanecen iguales */
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

.intro-message {
  background: #e7f3ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
}

.intro-message p {
  margin: 0;
  color: #2c5aa0;
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

/* ========== ESTILOS EXPANDIDOS PARA CAMPOS MÁS GRANDES ========== */

/* Grid expandido para Información Básica y Dirección */
.form-grid-expanded {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row-expanded {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row-contacto-expanded {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

/* Campos expandidos */
.form-field-expanded {
  margin-bottom: 1.5rem;
  width: 100%;
}

/* Selectores expandidos */
.select-field-expanded {
  min-height: 44px;
}

.select-field-expanded :deep(select) {
  height: 44px;
  padding: 0.75rem;
  font-size: 1rem;
  width: 100%;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: white;
}

.select-field-expanded :deep(select):focus {
  border-color: #2c5aa0;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(44, 90, 160, 0.25);
}

/* Campos de texto grandes expandidos */
.textarea-field-expanded :deep(textarea) {
  min-height: 120px;
  resize: vertical;
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.textarea-field-expanded :deep(textarea):focus {
  border-color: #2c5aa0;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(44, 90, 160, 0.25);
}

/* NUEVO: Textareas EXTRA grandes para alergias, limitaciones y observaciones */
.extra-large-textarea :deep(textarea) {
  min-height: 200px;
  font-size: 1rem;
  line-height: 1.5;
  padding: 1rem;
}

/* NUEVO: Textarea SUPER grande para observaciones */
.super-large-textarea :deep(textarea) {
  min-height: 840px !important;
  font-size: 1rem;
  line-height: 1.5;
  padding: 1rem;
  resize: vertical;
}

.field-note {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
  font-style: italic;
}

/* GRUPO DE TELÉFONO EXPANDIDO */
.telefono-group-expanded {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
  align-items: end;
}

.telefono-select-expanded {
  margin-bottom: 0;
}

.telefono-input-container-expanded {
  margin-bottom: 0;
}

.input-label-expanded {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
}

.telefono-input-wrapper-expanded {
  display: flex;
  align-items: center;
  border: 1px solid #ced4da;
  border-radius: 4px;
  overflow: hidden;
  background: white;
  height: 44px;
}

.telefono-prefijo-expanded {
  padding: 0.75rem;
  background: #e9ecef;
  border-right: 1px solid #ced4da;
  color: #495057;
  font-weight: 500;
  font-size: 1rem;
  min-width: 60px;
  text-align: center;
}

.telefono-input-expanded {
  flex: 1;
  border: none;
  padding: 0.75rem;
  outline: none;
  font-size: 1rem;
  color: #495057;
  height: 100%;
  width: 100%;
}

.telefono-input-expanded::placeholder {
  color: #6c757d;
}

.telefono-input-expanded:focus {
  box-shadow: none;
}

/* Checkboxes expandidos */
.checkbox-group-expanded {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.checkbox-field-expanded {
  margin-bottom: 0;
}

/* Info de vehículo expandido */
.vehicle-info-expanded {
  margin-left: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #2c5aa0;
  margin-top: 0.5rem;
}

/* ========== ESTILOS PARA SELECCIÓN DE CURSOS EXPANDIDO ========== */
.courses-grid-uniform {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.course-option-uniform {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  position: relative;
  background: white;
}

.course-option-uniform:hover {
  border-color: #2c5aa0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.1);
}

.course-option-uniform.selected {
  border-color: #2c5aa0;
  background: linear-gradient(135deg, #f8fbff 0%, #e3f2fd 100%);
}

.course-icon-uniform {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.course-info-uniform {
  flex: 1;
}

.course-name-uniform {
  color: #2c5aa0;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.course-dates-uniform {
  color: #495057;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.course-location-uniform {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.course-meta-uniform {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-cupo-uniform {
  color: #495057;
  font-size: 0.9rem;
}

.selected-course-info-uniform {
  background: #e7f3ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-top: 1rem;
}

.selected-course-info-uniform h4 {
  color: #2c5aa0;
  margin-bottom: 0.5rem;
}

.no-course-selected-uniform {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-top: 1rem;
  color: #856404;
}

/* ========== ESTILOS PARA RESUMEN EXPANDIDO ========== */
.summary-container-expanded {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-section-expanded {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.summary-title-expanded {
  color: #2c5aa0;
  font-size: 1.3rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #2c5aa0;
  padding-bottom: 0.5rem;
}

.summary-grid-expanded {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1rem;
}

.summary-item-expanded {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #2c5aa0;
}

.summary-item-expanded strong {
  color: #495057;
}

/* Alerta final expandida */
.final-alert-expanded {
  margin-top: 2rem;
}

/* ========== NAVEGACIÓN EXPANDIDA ========== */
.form-navigation-expanded {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  gap: 1rem;
}

.nav-button-expanded {
  min-width: 160px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.submit-button-expanded {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  border: none;
}

.nav-spacer-expanded {
  flex: 1;
}

/* ========== MODAL DE ÉXITO EXPANDIDO ========== */
.success-modal-expanded {
  text-align: center;
  padding: 2rem;
}

.success-icon-expanded {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-modal-expanded h3 {
  color: #28a745;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.success-actions-expanded {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.action-button-expanded {
  min-width: 180px;
  height: 48px;
}

/* ========== RESPONSIVE PARA TODOS LOS DISPOSITIVOS ========== */
@media (max-width: 1200px) {
  .form-container {
    max-width: 100%;
    padding: 0 1.5rem;
  }
}

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
    padding: 1.5rem 1rem;
  }
  
  .courses-grid-uniform {
    grid-template-columns: 1fr;
  }
  
  .form-grid-expanded,
  .form-row-expanded,
  .form-row-contacto-expanded {
    grid-template-columns: 1fr;
  }
  
  .telefono-group-expanded {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .form-navigation-expanded {
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .nav-button-expanded {
    width: 100%;
  }
  
  .success-actions-expanded {
    flex-direction: column;
  }
  
  .action-button-expanded {
    width: 100%;
  }
  
  .vehicle-info-expanded {
    margin-left: 0;
  }
  
  .summary-grid-expanded {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .course-option-uniform {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .course-meta-uniform {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .summary-item-expanded {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .telefono-input-wrapper-expanded {
    height: 48px;
  }
  
  .form-grid-expanded {
    grid-template-columns: 1fr;
  }
  
  .step-title {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
  
  .success-modal-expanded {
    padding: 1rem;
  }
  
  .success-icon-expanded {
    font-size: 3rem;
  }
}

/* Estilos para estados de deshabilitado */
.select-field-expanded :deep(select):disabled {
  background-color: #e9ecef;
  opacity: 0.6;
  cursor: not-allowed;
}

/* Estilos para hover en todos los elementos interactivos */
.course-option-uniform:hover,
.form-field-expanded :deep(input):hover,
.form-field-expanded :deep(select):hover,
.form-field-expanded :deep(textarea):hover {
  border-color: #2c5aa0;
}

/* Transiciones suaves para todos los elementos */
.form-field-expanded :deep(*),
.course-option-uniform,
.nav-button-expanded {
  transition: all 0.2s ease-in-out;
}
</style>