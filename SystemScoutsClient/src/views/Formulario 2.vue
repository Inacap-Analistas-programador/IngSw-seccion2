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
            
                <!-- Secciones anidadas dentro de la tarjeta cuando está seleccionada -->
                <div v-if="formData.cursoId === curso.id" style="margin-top: 18px;">
                  <div v-if="cargandoSecciones" class="info-message" style="padding: 8px; background:#eef6ff; border:1px solid #cde6ff; border-radius:6px; color:#23527c; margin-bottom:8px;">Cargando secciones desde SSB...</div>

                  <div v-else>
                    <div v-if="getSeccionesParaCurso(curso).length === 0" class="no-sections-message" style="padding: 8px; background:#fff3cd; border:1px solid #ffeeba; border-radius:6px; color:#856404; margin-bottom:8px;">No se encontraron secciones para esta opción en SSB.</div>

                    <div v-else style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:10px;">
                      <div
                        v-for="seccion in getSeccionesParaCurso(curso)"
                        :key="seccion.id"
                        :class="['seccion-card', { 'seccion-selected': formData.cusId === seccion.id }]"
                        @click.stop.prevent="selectSeccion(seccion)"
                        style="padding:10px; border:1px solid #ddd; border-radius:8px; cursor:pointer; background:white;"
                      >
                        <div style="font-weight:600; color:#2c5aa0;">{{ seccion.descripcion }}</div>
                        <div style="font-size:0.85rem; color:#6c757d">{{ seccion.cursoNombre ? ('Curso: ' + seccion.cursoNombre) : '' }}</div>
                        <div style="font-size:0.85rem; color:#6c757d">{{ seccion.fechaInicio ? ('Inicio: ' + seccion.fechaInicio) : '' }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
              message="Revise que toda la información sea correcta antes de confirmar la pre-inscripción en SSB."
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
            {{ submitting ? 'Enviando a SSB...' : '✅ Confirmar Pre-Inscripción en SSB' }}
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
        <h3>¡Pre-Inscripción Exitosa en SSB!</h3>
        <p>Su formulario ha sido registrado correctamente en la base de datos SSB Scouts Biobío.</p>
        
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
import authService from '@/services/authService'
import * as cursosService from '@/services/cursosService'
import { personas as personasApi, personaCursos as personaCursosApi, personaGrupos as personaGruposApi, personaNiveles as personaNivelesApi, personaIndividuales as personaIndividualesApi } from '@/services/personasService'
import { pagoPersona as pagoPersonaApi } from '@/services/pagosService'
import mantenedoresService from '@/services/mantenedoresService'

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
    const telefonoPlaceholder = ref('8 1234 5678')
    const isNavigating = ref(false)
    const seccionesDisponibles = ref([])
    const seccionSeleccionada = ref('')
    const cargandoSecciones = ref(false)

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
      // Paso 0 - Curso (primer paso)
      cursoId: '',
      cusId: '', // ID de la sección seleccionada
      
      // Paso 1 - Datos Personales (CON NUEVOS CAMPOS)
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

    // Datos para selects y opciones - CARGADOS DESDE API
    const estadosCiviles = ref([])
    const tiposTelefono = [
      { value: 'movil', label: 'Móvil' },
      { value: 'casa', label: 'Casa' },
      { value: 'trabajo', label: 'Trabajo' }
    ]
    const zonas = ref([])
    const distritos = ref([])
    const grupos = ref([])
    const ramas = ref([])
    const roles = ref([])
    const niveles = ref([])
    const tiposAlimentacion = ref([])

    const cursosDisponibles = ref([])

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
        case 0: // Selección de Curso y Sección
          return !!(formData.cursoId && formData.cusId)
        
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
          telefonoPlaceholder.value = '8 1234 5678'
          break
        case 'casa':
          telefonoPlaceholder.value = '2 1234 5678'
          break
        case 'trabajo':
          telefonoPlaceholder.value = '2 1234 5678'
          break
        default:
          telefonoPlaceholder.value = '8 1234 5678'
      }
    }

    const selectCurso = async (curso) => {
      formData.cursoId = Number(curso.id || curso.CUR_ID)
      formData.cusId = 0 // Resetear sección seleccionada a 0 (nulo)
      seccionSeleccionada.value = 0
      cargandoSecciones.value = true

      try {
        // Cargar secciones del curso seleccionado por su CUR_ID desde SSB
        const cursoId = Number(curso.id || curso.CUR_ID)
        console.log(`📚 Cargando secciones desde SSB para curso CUR_ID=${cursoId} (${curso.CUR_DESCRIPCION || curso.nombre})`)
        
        const raw = await cursosService.secciones.list({ curso_id: cursoId })
        const arr = Array.isArray(raw) ? raw : (Array.isArray(raw?.results) ? raw.results : [])
        
        seccionesDisponibles.value = arr.map(s => ({
          id: Number(s.CUS_ID || s.id),
          nombre: `${s.CUS_DESCRIPCION || s.descripcion || ''}`.trim(),
          descripcion: s.CUS_DESCRIPCION || s.descripcion || '',
          fechaInicio: s.CUS_FECHA_INICIO || s.fecha_inicio || '',
          fechaFin: s.CUS_FECHA_TERMINO || s.fecha_fin || '',
          cupo: s.CUS_CANT_PARTICIPANTE || s.cupo || 0,
          cursoId: cursoId,
          cursoNombre: curso.CUR_DESCRIPCION || curso.nombre || '',
          original: s
        }))
        
        console.log(`✅ ${seccionesDisponibles.value.length} secciones cargadas desde SSB para CUR_ID=${cursoId}`)
      } catch (e) {
        console.error('❌ Error cargando secciones desde SSB:', e?.message || e)
        seccionesDisponibles.value = []
      } finally {
        cargandoSecciones.value = false
      }
    }

    const selectSeccion = (seccion) => {
      // Guardar id como número para consistencia
      formData.cusId = Number(seccion.id)
      seccionSeleccionada.value = Number(seccion.id)
      console.log(`✅ Sección seleccionada desde SSB: ${seccion.descripcion} (id=${formData.cusId}, tipo=${typeof formData.cusId})`)
      console.log(`✅ Validación step 0: cursoId=${formData.cursoId}, cusId=${formData.cusId}, válido=${!!(formData.cursoId && formData.cusId)}`)
    }

    const getCursoSeleccionado = () => {
      return (cursosDisponibles.value || []).find(curso => curso.id === formData.cursoId) || {}
    }

    const getSeccionSeleccionada = () => {
      return seccionesDisponibles.value.find(seccion => seccion.id === formData.cusId) || {}
    }

    // Devuelve las secciones relevantes para una tarjeta de curso.
    const getSeccionesParaCurso = (curso) => {
      if (!Array.isArray(seccionesDisponibles.value)) return []
      const cursoId = Number(curso.id || curso.CUR_ID)
      return seccionesDisponibles.value.filter(s => Number(s.cursoId) === cursoId)
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
      const rama = ramas.value.find(r => r.value === value)
      return rama ? rama.label : value
    }

    const getRolLabel = (value) => {
      if (!value) return ''
      const rol = roles.value.find(r => r.value === value)
      return rol ? rol.label : value
    }

    const getNivelLabel = (value) => {
      if (!value) return ''
      const nivel = niveles.value.find(n => n.value === value)
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
        // Obtener usuario actual (si no viene, usar id=1 como fallback)
        let usuId = 1
        try {
          const currentUser = await authService.getCurrentUser()
          usuId = (currentUser && (currentUser.id || currentUser.USU_ID)) ? (currentUser.id || currentUser.USU_ID) : 1
        } catch (e) {
          console.warn('No se pudo obtener usuario actual, usando USU_ID=1', e && e.message)
        }

        // Preparar payload para crear Persona en SSB
        const rutRaw = (formData.rut || '').toString().trim()
        let perRun = rutRaw
        let perDv = ''
        if (rutRaw.includes('-')) {
          const parts = rutRaw.split('-')
          perRun = parts[0].replace(/[^0-9]/g, '')
          perDv = (parts[1] || '').toString().toUpperCase()
        }

        const tipoFono = (formData.tipoTelefono === 'movil') ? 2 : (formData.tipoTelefono === 'casa' ? 1 : 2)

        const datosPersona = {
          PER_NOMBRES: formData.nombres || '',
          PER_APELPTA: formData.apellidoPaterno || '',
          PER_APELMAT: formData.apellidoMaterno || '',
          PER_RUN: perRun || '',
          PER_DV: perDv || '',
          PER_MAIL: formData.email || '',
          PER_FECHA_NAC: formData.fechaNacimiento || null,
          PER_DIRECCION: formData.direccion || null,
          PER_TIPO_FONO: tipoFono,
          PER_FONO: formData.telefono ? ('+56' + formData.telefono.toString().replace(/[^0-9]/g, '').replace(/^56/, '')) : null,
          PER_APODO: formData.apodo || null,
          PER_PROFESION: formData.profesion || null,
          PER_NOM_EMERGENCIA: formData.contactoEmergenciaNombre || null,
          PER_FONO_EMERGENCIA: formData.contactoEmergenciaTelefono ? ('+56' + formData.contactoEmergenciaTelefono.toString().replace(/[^0-9]/g, '').replace(/^56/, '')) : null,
          PER_ALERGIA_ENFERMEDAD: formData.alergias || null,
          PER_LIMITACION: formData.limitaciones || null,
          PER_RELIGION: formData.religion || null,
          PER_NUM_MMA: formData.numeroMMAA || null,
          PER_OTROS: formData.observaciones || null,
          PER_APODO: formData.apodo || '',
          ESC_ID: formData.estadoCivil ? Number(formData.estadoCivil) : 1,
          COM_ID: formData.comuna ? Number(formData.comuna) : 1,
          USU_ID: usuId,
          PER_VIGENTE: true
        }

        console.log('📤 Creando persona en SSB con payload:', datosPersona)

        const personaCreada = await personasApi.create(datosPersona)
        const personaId = personaCreada.PER_ID || personaCreada.id || personaCreada.PER_ID_id
        console.log('✅ Persona creada en SSB:', personaCreada)

        // Crear inscripción (Persona_Curso) en SSB - Usar directamente la sección seleccionada
        const cusIdToUse = formData.cusId || null

        if (!cusIdToUse) {
          throw new Error('No hay sección de curso seleccionada en SSB')
        }

        const personaCursoPayload = {
          PER_ID: personaId,
          CUS_ID: cusIdToUse,
          ROL_ID: formData.rol ? Number(formData.rol) : null,
          ALI_ID: formData.alimentacion ? Number(formData.alimentacion) : null,
          NIV_ID: formData.nivel ? Number(formData.nivel) : null,
          PEC_OBSERVACION: formData.observaciones || null,
          PEC_REGISTRO: true,
          PEC_ACREDITACION: false,
          PEC_ENVIO_CORREO_QR: false
        }

        console.log('📤 Registrando pre-inscripción en SSB (Persona_Curso):', personaCursoPayload)
        const inscripcion = await personaCursosApi.create(personaCursoPayload)
        console.log('✅ Inscripción creada en SSB:', inscripcion)

        // GUARDAR EN TABLAS ADICIONALES DE SSB: Persona_Individual, Persona_Grupo, Persona_Nivel

        // 1. Guardar en Persona_Individual (ZON_ID, DIS_ID)
        if (formData.zona || formData.distrito) {
          try {
            const personaIndividualPayload = {
              PER_ID: personaId,
              ZON_ID: formData.zona ? Number(formData.zona) : null,
              DIS_ID: formData.distrito ? Number(formData.distrito) : null
            }
            console.log('📤 Registrando Persona_Individual en SSB:', personaIndividualPayload)
            await personaIndividualesApi.create(personaIndividualPayload)
            console.log('✅ Persona_Individual creada en SSB')
          } catch (e) {
            console.warn('⚠️ Error creando Persona_Individual en SSB:', e?.response?.data || e?.message)
          }
        }

        // 2. Guardar en Persona_Grupo (GRU_ID)
        if (formData.grupo) {
          try {
            const personaGrupoPayload = {
              PER_ID: personaId,
              GRU_ID: Number(formData.grupo)
            }
            console.log('📤 Registrando Persona_Grupo en SSB:', personaGrupoPayload)
            await personaGruposApi.create(personaGrupoPayload)
            console.log('✅ Persona_Grupo creada en SSB')
          } catch (e) {
            console.warn('⚠️ Error creando Persona_Grupo en SSB:', e?.response?.data || e?.message)
          }
        }

        // 3. Guardar en Persona_Nivel (RAM_ID, NIV_ID)
        if (formData.rama || formData.nivel) {
          try {
            const personaNivelPayload = {
              PER_ID: personaId,
              RAM_ID: formData.rama ? Number(formData.rama) : null,
              NIV_ID: formData.nivel ? Number(formData.nivel) : null
            }
            console.log('📤 Registrando Persona_Nivel en SSB:', personaNivelPayload)
            await personaNivelesApi.create(personaNivelPayload)
            console.log('✅ Persona_Nivel creada en SSB')
          } catch (e) {
            console.warn('⚠️ Error creando Persona_Nivel en SSB:', e?.response?.data || e?.message)
          }
        }

        // Marcar pasos como completados y mostrar modal de éxito
        steps.value.forEach(step => {
          step.completed = true
          step.valid = true
        })
        showSuccessModal.value = true

      } catch (error) {
        console.error('Error en la pre-inscripción en SSB (envío real):', error)
        // Mostrar alerta simple; podemos mejorar con mensajes detallados según error.response
        alert('Error al guardar la pre-inscripción en SSB. Revisa la consola para más detalles.')
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
      
      // Resetear secciones
      seccionesDisponibles.value = []
      seccionSeleccionada.value = ''
      cargandoSecciones.value = false
      
      // Resetear pasos
      steps.value.forEach(step => {
        step.completed = false
        step.valid = false
      })
      
      currentStep.value = 0
      telefonoPlaceholder.value = '8 1234 5678'
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

    onMounted(async () => {
      console.log('Formulario de pre-inscripción Scouts Biobío montado - Iniciando carga de datos desde SSB...')

      try {
        // 1. Cargar Estados Civiles desde SSB
        try {
          const estadosData = await mantenedoresService.estadoCivil.list()
          if (Array.isArray(estadosData) && estadosData.length) {
            estadosCiviles.value = estadosData.map(e => ({ value: String(e.ESC_ID), label: e.ESC_DESCRIPCION }))
            console.log(`✓ Estados civiles cargados desde SSB: ${estadosData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando estados civiles desde SSB:', e?.message)
        }

        // 2. Cargar Zonas desde SSB
        try {
          const zonasData = await mantenedoresService.zona.list()
          if (Array.isArray(zonasData) && zonasData.length) {
            zonas.value = zonasData.map(z => ({ value: String(z.ZON_ID), label: z.ZON_DESCRIPCION }))
            console.log(`✓ Zonas cargadas desde SSB: ${zonasData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando zonas desde SSB:', e?.message)
        }

        // 3. Cargar Distritos desde SSB
        try {
          const distritosData = await mantenedoresService.distrito.list()
          if (Array.isArray(distritosData) && distritosData.length) {
            distritos.value = distritosData.map(d => ({ value: String(d.DIS_ID), label: d.DIS_DESCRIPCION, zonaId: String(d.ZON_ID) }))
            console.log(`✓ Distritos cargados desde SSB: ${distritosData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando distritos desde SSB:', e?.message)
        }

        // 4. Cargar Grupos desde SSB
        try {
          const gruposData = await mantenedoresService.grupo.list()
          if (Array.isArray(gruposData) && gruposData.length) {
            grupos.value = gruposData.map(g => ({ value: String(g.GRU_ID), label: g.GRU_DESCRIPCION, distritoId: String(g.DIS_ID) }))
            console.log(`✓ Grupos cargados desde SSB: ${gruposData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando grupos desde SSB:', e?.message)
        }

        // 5. Cargar Ramas desde SSB
        try {
          const ramasData = await mantenedoresService.rama.list()
          if (Array.isArray(ramasData) && ramasData.length) {
            ramas.value = ramasData.map(r => ({ value: String(r.RAM_ID), label: r.RAM_DESCRIPCION }))
            console.log(`✓ Ramas cargadas desde SSB: ${ramasData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando ramas desde SSB:', e?.message)
        }

        // 6. Cargar Roles desde SSB
        try {
          const rolesData = await mantenedoresService.rol.list()
          if (Array.isArray(rolesData) && rolesData.length) {
            roles.value = rolesData.map(r => ({ value: String(r.ROL_ID), label: r.ROL_DESCRIPCION }))
            console.log(`✓ Roles cargados desde SSB: ${rolesData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando roles desde SSB:', e?.message)
        }

        // 7. Cargar Niveles desde SSB
        try {
          const nivelesData = await mantenedoresService.nivel.list()
          if (Array.isArray(nivelesData) && nivelesData.length) {
            niveles.value = nivelesData.map(n => ({ value: String(n.NIV_ID), label: n.NIV_DESCRIPCION }))
            console.log(`✓ Niveles cargados desde SSB: ${nivelesData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando niveles desde SSB:', e?.message)
        }

        // 8. Cargar Tipos de Alimentación desde SSB
        try {
          const alimentacionData = await mantenedoresService.alimentacion.list()
          if (Array.isArray(alimentacionData) && alimentacionData.length) {
            tiposAlimentacion.value = alimentacionData.map(a => ({ value: String(a.ALI_ID), label: a.ALI_DESCRIPCION }))
            console.log(`✓ Tipos de alimentación cargados desde SSB: ${alimentacionData.length}`)
          }
        } catch (e) {
          console.warn('⚠️ Error cargando tipos de alimentación desde SSB:', e?.message)
        }

        // 9. Cargar TODOS los cursos desde la API de SSB (sin predefinidas, SOLO de la base de datos SSB)
        try {
          console.log('🔄 Cargando cursos desde la API de SSB...')
          const rawCursos = await cursosService.cursos.list()
          const cursosArr = Array.isArray(rawCursos) ? rawCursos : (Array.isArray(rawCursos?.results) ? rawCursos.results : [])
          
          if (Array.isArray(cursosArr) && cursosArr.length) {
            // Mapear TODOS los cursos desde la BD SSB
            cursosDisponibles.value = cursosArr.map(c => ({
              id: Number(c.CUR_ID || c.id),
              CUR_ID: Number(c.CUR_ID || c.id),
              nombre: c.CUR_DESCRIPCION || c.nombre || (`Curso ${c.CUR_ID}`),
              CUR_DESCRIPCION: c.CUR_DESCRIPCION || '',
              ubicacion: c.CUR_LUGAR || '',
              CUR_LUGAR: c.CUR_LUGAR || '',
              fechas: c.CUR_FECHA ? String(c.CUR_FECHA) : 'Fechas por definir',
              cupoMaximo: c.CUR_CANT_PARTICIPANTE || 0,
              inscritos: c.CUR_INSCRITOS || 0,
              icono: '📚',
              estado: c.CUR_ESTADO || 0,
              CUR_ESTADO: c.CUR_ESTADO || 0
            }))
            console.log(`✅ ${cursosDisponibles.value.length} CURSOS CARGADOS DESDE LA BASE DE DATOS SSB`)
          } else {
            console.warn('⚠️ No se encontraron cursos en la base de datos SSB')
          }
        } catch (e) {
          console.error('❌ Error cargando cursos desde la base de datos SSB:', e?.message || e)
          cursosDisponibles.value = []
        }

        console.log('✓✓✓ Carga de todos los datos desde SSB completada ✓✓✓')
      } catch (e) {
        console.error('Error general en onMounted cargando desde SSB:', e)
      }
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
      seccionesDisponibles,
      cargandoSecciones,
      isStepValid,
      isFormValid,
      actualizarProvincias,
      actualizarComunas,
      actualizarPlaceholderTelefono,
      selectCurso,
      selectSeccion,
      getCursoSeleccionado,
      getSeccionSeleccionada,
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