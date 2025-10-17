<template>
  <div class="app-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <ul>
        <li v-for="item in menuItems" :key="item.id">
          <button 
            class="sidebar-link" 
            :class="{ active: activeMenu === item.id }"
            @click="setActiveMenu(item.id)"
          >
            <span class="icon">{{ item.icon }}</span>
            <span class="label">{{ item.label }}</span>
          </button>
        </li>
      </ul>
    </aside>

    <!-- Contenido principal -->
    <main class="main-content">
      <!-- Navbar -->
      <nav class="navbar">
        <div class="navbar-left">
          <img :src="logo" alt="Logo Scouts" class="logo" />
          <span class="title">Sistema Scouts Región del Biobío</span>
        </div>

        <ul :class="['navbar-links', { active: mobileMenuOpen }]">
          <li v-for="link in navbarLinks" :key="link.text">
            <a :href="link.href">{{ link.text }}</a>
          </li>
        </ul>

        <button 
          class="navbar-menu" 
          @click="toggleMobileMenu"
          aria-label="Alternar menú"
        >
          ☰
        </button>
      </nav>

      <!-- Formulario de Pre-inscripción -->
      <div class="form-container">
        <h1 class="form-title">Formulario de Pre-inscripción - Curso Medio</h1>
        
        <!-- Alerta informativa -->
        <div class="alert alert-info">
          <span class="alert-icon">ℹ️</span>
          <span>Complete todos los campos obligatorios (*) para realizar la pre-inscripción. Los datos serán verificados antes de la confirmación final.</span>
        </div>

        <div v-if="showErrorAlert" class="alert alert-error">
          <span class="alert-icon">⚠️</span>
          <span>Por favor, corrija los errores en el formulario antes de enviarlo.</span>
        </div>
        
        <!-- Selección de Curso -->
        <div class="form-section">
          <h2 class="section-title">
            <span class="icon">📚</span>
            Selección de Curso
          </h2>
          
          <div class="form-group">
            <label for="curso" class="form-label required">¿A qué curso se va a inscribir?</label>
            <select 
              id="curso" 
              v-model="formData.curso"
              class="form-select" 
              required
              @blur="validateField('curso')"
            >
              <option value="">Seleccione un curso</option>
              <option value="curso-inicial">Curso Inicial</option>
              <option value="curso-medio">Curso Medio</option>
              <option value="curso-avanzado">Curso Avanzado</option>
            </select>
            <span class="form-error">{{ errors.curso }}</span>
          </div>
        </div>
        
        <!-- Información Personal -->
        <div class="form-section">
          <h2 class="section-title">
            <span class="icon">👤</span>
            Información Personal
          </h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="nombres" class="form-label required">Nombres</label>
              <input 
                type="text" 
                id="nombres" 
                v-model="formData.nombres"
                class="form-input" 
                placeholder="INGRESE SUS NOMBRES" 
                required 
                @blur="validateField('nombres')"
                style="text-transform: uppercase;"
              >
              <span class="form-error">{{ errors.nombres }}</span>
            </div>
            
            <div class="form-group">
              <label for="apellidos" class="form-label required">Apellidos</label>
              <input 
                type="text" 
                id="apellidos" 
                v-model="formData.apellidos"
                class="form-input" 
                placeholder="INGRESE SUS APELLIDOS" 
                required 
                @blur="validateField('apellidos')"
                style="text-transform: uppercase;"
              >
              <span class="form-error">{{ errors.apellidos }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="rut" class="form-label required">RUT</label>
              <input 
                type="text" 
                id="rut" 
                v-model="formData.rut"
                class="form-input" 
                placeholder="EJ: 12.345.678-9" 
                required 
                @blur="validateRUT"
              >
              <span class="form-error">{{ errors.rut }}</span>
            </div>
            
            <div class="form-group">
              <label for="fecha-nacimiento" class="form-label required">Fecha de Nacimiento</label>
              <input 
                type="date" 
                id="fecha-nacimiento" 
                v-model="formData.fechaNacimiento"
                class="form-input" 
                required 
                @blur="validateField('fechaNacimiento')"
              >
              <span class="form-error">{{ errors.fechaNacimiento }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="genero" class="form-label required">Género</label>
              <select 
                id="genero" 
                v-model="formData.genero"
                class="form-select" 
                required 
                @blur="validateField('genero')"
              >
                <option value="">Seleccione una opción</option>
                <option value="masculino">Masculino</option>
                <option value="femenino">Femenino</option>
                <option value="otro">Otro</option>
                <option value="prefiero-no-decir">Prefiero no decir</option>
              </select>
              <span class="form-error">{{ errors.genero }}</span>
            </div>
            
            <div class="form-group">
              <label for="nacionalidad" class="form-label required">Nacionalidad</label>
              <input 
                type="text" 
                id="nacionalidad" 
                v-model="formData.nacionalidad"
                class="form-input" 
                placeholder="EJ: CHILENA" 
                required 
                @blur="validateField('nacionalidad')"
                style="text-transform: uppercase;"
              >
              <span class="form-error">{{ errors.nacionalidad }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="estado-civil" class="form-label">Estado Civil</label>
              <select 
                id="estado-civil" 
                v-model="formData.estadoCivil"
                class="form-select"
              >
                <option value="">Seleccione una opción</option>
                <option value="soltero">Soltero/a</option>
                <option value="casado">Casado/a</option>
                <option value="divorciado">Divorciado/a</option>
                <option value="viudo">Viudo/a</option>
                <option value="union-civil">Unión Civil</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="profesion" class="form-label">Profesión</label>
              <input 
                type="text" 
                id="profesion" 
                v-model="formData.profesion"
                class="form-input" 
                placeholder="EJ: PROFESOR, INGENIERO, ETC." 
                style="text-transform: uppercase;"
              >
            </div>
          </div>
          
          <div class="form-group">
            <label for="apodo" class="form-label">Apodo para credencial</label>
            <input 
              type="text" 
              id="apodo" 
              v-model="formData.apodo"
              class="form-input" 
              placeholder="APODO QUE APARECERÁ EN SU CREDENCIAL"
            >
          </div>
        </div>
        
        <!-- Información de Contacto -->
        <div class="form-section">
          <h2 class="section-title">
            <span class="icon">📞</span>
            Información de Contacto
          </h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="email" class="form-label required">Correo Electrónico</label>
              <input 
                type="email" 
                id="email" 
                v-model="formData.email"
                class="form-input" 
                placeholder="ejemplo@correo.com" 
                required 
                @blur="validateEmail"
              >
              <span class="form-error">{{ errors.email }}</span>
            </div>
            
            <div class="form-group">
              <label for="telefono" class="form-label required">Teléfono Celular</label>
              <input 
                type="tel" 
                id="telefono" 
                v-model="formData.telefono"
                class="form-input" 
                placeholder="+56 9 1234 5678" 
                required 
                @blur="validateField('telefono')"
              >
              <span class="form-error">{{ errors.telefono }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="telefono-casa" class="form-label">Teléfono Casa</label>
              <input 
                type="tel" 
                id="telefono-casa" 
                v-model="formData.telefonoCasa"
                class="form-input" 
                placeholder="+56 41 234 5678"
              >
            </div>
            
            <div class="form-group">
              <label for="telefono-trabajo" class="form-label">Teléfono Trabajo</label>
              <input 
                type="tel" 
                id="telefono-trabajo" 
                v-model="formData.telefonoTrabajo"
                class="form-input" 
                placeholder="+56 41 345 6789"
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="direccion" class="form-label required">Dirección</label>
              <input 
                type="text" 
                id="direccion" 
                v-model="formData.direccion"
                class="form-input" 
                placeholder="CALLE, NÚMERO, DEPARTAMENTO" 
                required 
                @blur="validateField('direccion')"
                style="text-transform: uppercase;"
              >
              <span class="form-error">{{ errors.direccion }}</span>
            </div>
            
            <div class="form-group">
              <label for="comuna" class="form-label required">Comuna</label>
              <select 
                id="comuna" 
                v-model="formData.comuna"
                class="form-select" 
                required 
                @blur="validateField('comuna')"
              >
                <option value="">Seleccione una comuna</option>
                <option value="concepcion">Concepción</option>
                <option value="talcahuano">Talcahuano</option>
                <option value="chiguayante">Chiguayante</option>
                <option value="san-pedro">San Pedro de la Paz</option>
                <option value="hualpen">Hualpén</option>
                <option value="coronel">Coronel</option>
                <option value="lota">Lota</option>
                <option value="penco">Penco</option>
                <option value="tome">Tomé</option>
                <option value="arauco">Arauco</option>
                <option value="lebu">Lebu</option>
                <option value="cañete">Cañete</option>
                <option value="los-alamos">Los Álamos</option>
                <option value="curanilahue">Curanilahue</option>
              </select>
              <span class="form-error">{{ errors.comuna }}</span>
            </div>
          </div>
        </div>
        
        <!-- Información del Scout -->
        <div class="form-section">
          <h2 class="section-title">
            <span class="icon">🏕️</span>
            Información del Scout
          </h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="rol" class="form-label required">Rol dentro del curso</label>
              <select 
                id="rol" 
                v-model="formData.rol"
                class="form-select" 
                required 
                @blur="validateField('rol')"
              >
                <option value="">Seleccione su rol</option>
                <option value="participante">Participante</option>
                <option value="apoyo-formadores">Apoyo a Formadores</option>
                <option value="formador">Formador</option>
                <option value="director">Director</option>
                <option value="coordinador">Coordinador</option>
                <option value="administrativo">Personal Administrativo</option>
                <option value="logistica">Personal de Logística</option>
                <option value="salud">Personal de Salud</option>
              </select>
              <span class="form-error">{{ errors.rol }}</span>
            </div>
            
            <div class="form-group">
              <label for="grupo-scout" class="form-label required">Grupo Scout</label>
              <select 
                id="grupo-scout" 
                v-model="formData.grupoScout"
                class="form-select" 
                required 
                @blur="validateField('grupoScout')"
              >
                <option value="">Seleccione su grupo scout</option>
                <option v-for="grupo in gruposScout" :key="grupo" :value="grupo">{{ grupo }}</option>
              </select>
              <span class="form-error">{{ errors.grupoScout }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="distrito" class="form-label required">Distrito</label>
              <select 
                id="distrito" 
                v-model="formData.distrito"
                class="form-select" 
                required 
                @blur="validateField('distrito')"
              >
                <option value="">Seleccione su distrito</option>
                <option value="distrito-1">Distrito 1</option>
                <option value="distrito-2">Distrito 2</option>
                <option value="distrito-3">Distrito 3</option>
                <option value="distrito-4">Distrito 4</option>
                <option value="distrito-5">Distrito 5</option>
                <option value="distrito-6">Distrito 6</option>
              </select>
              <span class="form-error">{{ errors.distrito }}</span>
            </div>
            
            <div class="form-group">
              <label for="rama" class="form-label required">Rama</label>
              <select 
                id="rama" 
                v-model="formData.rama"
                class="form-select" 
                required 
                @blur="validateField('rama')"
              >
                <option value="">Seleccione su rama</option>
                <option value="manada">Manada (7-10 años)</option>
                <option value="tropa">Tropa (11-14 años)</option>
                <option value="comunidad">Comunidad (15-17 años)</option>
                <option value="clan">Clan (18-20 años)</option>
                <option value="dirigente">Dirigente</option>
              </select>
              <span class="form-error">{{ errors.rama }}</span>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="nivel" class="form-label required">Nivel de Formación</label>
              <select 
                id="nivel" 
                v-model="formData.nivel"
                class="form-select" 
                required 
                @blur="validateField('nivel')"
              >
                <option value="">Seleccione su nivel</option>
                <option value="inicial">Inicial</option>
                <option value="medio">Medio</option>
                <option value="avanzado">Avanzado</option>
                <option value="ninguno">Ninguno</option>
              </select>
              <span class="form-error">{{ errors.nivel }}</span>
            </div>
            
            <div class="form-group">
              <label for="cargo" class="form-label">Cargo en la Unidad/Asociación</label>
              <input 
                type="text" 
                id="cargo" 
                v-model="formData.cargo"
                class="form-input" 
                placeholder="EJ: GUÍA DE PATRULLA, SUBJEFE, ETC." 
                style="text-transform: uppercase;"
              >
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="fecha-ingreso" class="form-label">Fecha de Ingreso al Movimiento Scout</label>
              <input 
                type="date" 
                id="fecha-ingreso" 
                v-model="formData.fechaIngreso"
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label for="miembro-activo" class="form-label">Número de Miembro Activo (MMAA)</label>
              <input 
                type="text" 
                id="miembro-activo" 
                v-model="formData.miembroActivo"
                class="form-input" 
                placeholder="EJ: 5208"
              >
            </div>
          </div>
        </div>
        
        <!-- Información de Salud -->
        <div class="form-section">
          <h2 class="section-title">
            <span class="icon">🏥</span>
            Información de Salud
          </h2>
          
          <div class="form-group">
            <label for="alergias" class="form-label">Alergias (medicamentos, alimentos, etc.)</label>
            <textarea 
              id="alergias" 
              v-model="formData.alergias"
              class="form-textarea" 
              placeholder="DESCRIBA SUS ALERGIAS, SI NO TIENE ESCRIBA 'NINGUNA'"
              rows="3"
              style="text-transform: uppercase;"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="condiciones-medicas" class="form-label">Condiciones Médicas (asma, diabetes, epilepsia, etc.)</label>
            <textarea 
              id="condiciones-medicas" 
              v-model="formData.condicionesMedicas"
              class="form-textarea" 
              placeholder="DESCRIBA SUS CONDICIONES MÉDICAS, SI NO TIENE ESCRIBA 'NINGUNA'"
              rows="3"
              style="text-transform: uppercase;"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="medicamentos" class="form-label">Medicamentos que toma regularmente</label>
            <textarea 
              id="medicamentos" 
              v-model="formData.medicamentos"
              class="form-textarea" 
              placeholder="DESCRIBA LOS MEDICAMENTOS QUE TOMA, SI NO TOMA ESCRIBA 'NINGUNO'"
              rows="3"
              style="text-transform: uppercase;"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="seguro-medico" class="form-label">Seguro Médico</label>
            <select 
              id="seguro-medico" 
              v-model="formData.seguroMedico"
              class="form-select"
            >
              <option value="">Seleccione una opción</option>
              <option value="fonasa">FONASA</option>
              <option value="isapre">ISAPRE</option>
              <option value="particular">Particular</option>
              <option value="ninguno">Ninguno</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="contacto-emergencia" class="form-label required">Nombre de Contacto de Emergencia</label>
            <input 
              type="text" 
              id="contacto-emergencia" 
              v-model="formData.contactoEmergencia"
              class="form-input" 
              placeholder="NOMBRE COMPLETO" 
              required 
              @blur="validateField('contactoEmergencia')"
              style="text-transform: uppercase;"
            >
            <span class="form-error">{{ errors.contactoEmergencia }}</span>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="telefono-emergencia" class="form-label required">Teléfono de Emergencia</label>
              <input 
                type="tel" 
                id="telefono-emergencia" 
                v-model="formData.telefonoEmergencia"
                class="form-input" 
                placeholder="+56 9 1234 5678" 
                required 
                @blur="validateField('telefonoEmergencia')"
              >
              <span class="form-error">{{ errors.telefonoEmergencia }}</span>
            </div>
            
            <div class="form-group">
              <label for="parentesco-emergencia" class="form-label required">Parentesco</label>
              <input 
                type="text" 
                id="parentesco-emergencia" 
                v-model="formData.parentescoEmergencia"
                class="form-input" 
                placeholder="EJ: MADRE, PADRE, HERMANO/A, ETC." 
                required 
                @blur="validateField('parentescoEmergencia')"
                style="text-transform: uppercase;"
              >
              <span class="form-error">{{ errors.parentescoEmergencia }}</span>
            </div>
          </div>
        </div>
        
        <!-- Botones de acción -->
        <div class="form-actions">
          <button 
            type="button" 
            class="btn btn-secondary"
            @click="resetForm"
          >
            Limpiar Formulario
          </button>
          
          <button 
            type="button" 
            class="btn btn-primary"
            @click="submitForm"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Enviando...' : 'Enviar Pre-inscripción' }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'FormularioPreinscripcion',
  data() {
    return {
      activeMenu: 4,
      mobileMenuOpen: false,
      isSubmitting: false,
      showErrorAlert: false,
      logo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiByeD0iMzAiIGZpbGw9IiMyQzVBQTAiLz4KPHBhdGggZD0iTTMwIDQwQzM1LjUyMjggNDAgNDAgMzUuNTIyOCA0MCAzMEM0MCAyNC40NzcyIDM1LjUyMjggMjAgMzAgMjBDMjQuNDc3MiAyMCAyMCAyNC40NzcyIDIwIDMwQzIwIDM1LjUyMjggMjQuNDc3MiA0MCAzMCA0MFoiIGZpbGw9IiNGRkNDMDAiLz4KPHBhdGggZD0iTTMwIDM0QzMyLjIwOTEgMzQgMzQgMzIuMjA5MSAzNCAzMEMzNCAyNy43OTA5IDMyLjIwOTEgMjYgMzAgMjZDMjcuNzkwOSAyNiAyNiAyNy43OTA5IDI2IDMwQzI2IDMyLjIwOTEgMjcuNzkwOSAzNCAzMCAzNFoiIGZpbGw9IiMyQzVBQTAiLz4KPC9zdmc+',
      menuItems: [
        { id: 1, label: "Dashboard", icon: "📊" },
        { id: 2, label: "Usuarios", icon: "👥" },
        { id: 3, label: "Cursos", icon: "📚" },
        { id: 4, label: "Inscripción", icon: "📝" },
        { id: 5, label: "Personas", icon: "👤" },
        { id: 6, label: "Habilitación", icon: "✅" },
        { id: 7, label: "Pagos", icon: "💰" },
        { id: 8, label: "Gestión", icon: "⚙️" },
        { id: 9, label: "Correos", icon: "📧" },
        { id: 10, label: "Acreditación", icon: "🎟️" }
      ],
      navbarLinks: [
        { text: "Inicio", href: "#" },
        { text: "Panel de Control", href: "#" },
        { text: "Usuarios y Roles", href: "#" },
        { text: "Cursos y Capacitaciones", href: "#" },
        { text: "Inscripciones", href: "#" },
        { text: "Gestión de Personas", href: "#" },
        { text: "Pagos", href: "#" },
        { text: "Envío de Correos", href: "#" },
        { text: "Reportes", href: "#" },
        { text: "Acreditación QR", href: "#" }
      ],
      gruposScout: [
        "Grupo Scout Andalien",
        "Grupo Scout Ainil",
        "Grupo Scout Lautaro",
        "Grupo Scout Quinchamalí",
        "Grupo Scout Galvarino",
        "Grupo Scout Calafquén",
        "Grupo Scout Alerce",
        "Grupo Scout Araucanía",
        "Grupo Scout Pucón",
        "Grupo Scout Villarrica",
        "Grupo Scout Temuco",
        "Grupo Scout Padre Hurtado",
        "Grupo Scout San Francisco",
        "Grupo Scout Santa Rosa",
        "Grupo Scout San José",
        "Grupo Scout San Juan",
        "Grupo Scout San Pedro",
        "Grupo Scout San Mateo",
        "Grupo Scout San Lucas",
        "Grupo Scout San Marcos"
      ],
      formData: {
        curso: '',
        nombres: '',
        apellidos: '',
        rut: '',
        fechaNacimiento: '',
        genero: '',
        nacionalidad: '',
        estadoCivil: '',
        profesion: '',
        apodo: '',
        email: '',
        telefono: '',
        telefonoCasa: '',
        telefonoTrabajo: '',
        direccion: '',
        comuna: '',
        rol: '',
        grupoScout: '',
        distrito: '',
        rama: '',
        nivel: '',
        cargo: '',
        fechaIngreso: '',
        miembroActivo: '',
        alergias: '',
        condicionesMedicas: '',
        medicamentos: '',
        seguroMedico: '',
        contactoEmergencia: '',
        telefonoEmergencia: '',
        parentescoEmergencia: ''
      },
      errors: {}
    }
  },
  methods: {
    setActiveMenu(menuId) {
      this.activeMenu = menuId
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    validateField(field) {
      if (!this.formData[field]) {
        this.errors[field] = 'Este campo es obligatorio'
      } else {
        delete this.errors[field]
      }
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.formData.email) {
        this.errors.email = 'Este campo es obligatorio'
      } else if (!emailRegex.test(this.formData.email)) {
        this.errors.email = 'Ingrese un correo electrónico válido'
      } else {
        delete this.errors.email
      }
    },
    validateRUT() {
      if (!this.formData.rut) {
        this.errors.rut = 'Este campo es obligatorio'
        return
      }
      
      // Validación básica de formato RUT chileno
      const rutRegex = /^[0-9]{1,2}\.?[0-9]{3}\.?[0-9]{3}-[0-9kK]{1}$/
      if (!rutRegex.test(this.formData.rut)) {
        this.errors.rut = 'Formato de RUT inválido (ej: 12.345.678-9)'
      } else {
        delete this.errors.rut
      }
    },
    validateForm() {
      // Validar todos los campos obligatorios
      const requiredFields = [
        'curso', 'nombres', 'apellidos', 'rut', 'fechaNacimiento',
        'genero', 'nacionalidad', 'email', 'telefono', 'direccion',
        'comuna', 'rol', 'grupoScout', 'distrito', 'rama', 'nivel',
        'contactoEmergencia', 'telefonoEmergencia', 'parentescoEmergencia'
      ]
      
      requiredFields.forEach(field => {
        this.validateField(field)
      })
      
      this.validateEmail()
      this.validateRUT()
      
      return Object.keys(this.errors).length === 0
    },
    async submitForm() {
      if (!this.validateForm()) {
        this.showErrorAlert = true
        // Scroll al primer error
        const firstErrorField = Object.keys(this.errors)[0]
        const element = document.getElementById(firstErrorField)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
        return
      }
      
      this.showErrorAlert = false
      this.isSubmitting = true
      
      try {
        // Simular envío de datos
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Mostrar mensaje de éxito
        alert('¡Pre-inscripción enviada exitosamente! Recibirá un correo de confirmación en breve.')
        
        // Resetear formulario
        this.resetForm()
        
      } catch (error) {
        alert('Error al enviar el formulario. Por favor, intente nuevamente.')
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      if (confirm('¿Está seguro de que desea limpiar todo el formulario? Se perderán todos los datos ingresados.')) {
        Object.keys(this.formData).forEach(key => {
          this.formData[key] = ''
        })
        this.errors = {}
        this.showErrorAlert = false
      }
    }
  }
}
</script>

<style scoped>
/* Estilos generales - Reutilizados del Dashboard */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Segoe UI", Arial, sans-serif;
}

body {
  background-color: #f5f7fa;
  color: #333;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: #2c3e50;
  padding: 10px 0;
  height: 100vh;
  position: fixed;
  overflow-y: auto;
  z-index: 100;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  width: 100%;
  background: none;
  border: none;
  color: #ecf0f1;
  padding: 12px 15px;
  cursor: pointer;
  text-align: left;
}

.sidebar-link:hover {
  background: #34495e;
}

.sidebar-link.active {
  background: #1abc9c;
}

.icon {
  margin-right: 10px;
}

/* Contenido principal */
.main-content {
  flex: 1;
  margin-left: 220px;
  padding: 20px;
}

/* Navbar */
.navbar {
  background: #2c5aa0;
  color: white;
  padding: 14px 26px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-bottom: 20px;
  z-index: 10;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 18px;
}

.logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid #ffcc00;
  background: white;
  object-fit: cover;
  box-shadow: 0 3px 6px rgba(0,0,0,0.18);
}

.title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 0.6px;
}

.navbar-links {
  display: flex;
  gap: 26px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar-links a {
  font-weight: 600;
  text-decoration: none;
  color: white;
  transition: color 0.3s, border-bottom 0.3s;
  border-bottom: 2px solid transparent;
}

.navbar-links a:hover {
  color: #ffcc00;
  border-bottom: 2px solid #ffcc00;
}

.navbar-menu {
  display: none;
  background: #ffcc00;
  color: #2c5aa0;
  font-size: 1.6rem;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  margin-left: 14px;
}

/* Contenedor del formulario */
.form-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 30px;
}

.form-title {
  color: #2c5aa0;
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.8rem;
}

/* Alertas */
.alert {
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
}

.alert-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-icon {
  margin-right: 10px;
  font-size: 18px;
}

/* Secciones del formulario */
.form-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8f9fa;
}

.section-title {
  color: #2c5aa0;
  margin-bottom: 20px;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Grupos de formulario */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.form-label.required::after {
  content: " *";
  color: #e74c3c;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 2px rgba(44, 90, 160, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-error {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
  display: block;
}

/* Botones */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #2c5aa0;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1e3d73;
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 15px 20px;
  }
  
  .navbar-links {
    flex-direction: column;
    gap: 10px;
    width: 100%;
    display: none;
    margin-top: 12px;
  }
  
  .navbar-links.active {
    display: flex;
  }
  
  .navbar-menu {
    display: block;
    align-self: flex-end;
  }
  
  .form-container {
    padding: 15px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>