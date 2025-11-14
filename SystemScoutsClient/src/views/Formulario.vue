<template>
  <div class="formulario"> 
    <div class="form-outer">
      <form class="form-inner">
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Datos Personales         ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  
  <!--::::::::::::::::::::::::::::::::::CURSO DE PARTICIPACIÓN::::::::::::::::::::::::::::::::::::::::-->
  <section>
    <div class="seleccioneCurso"></div> <!-- Titulo Eleccion de Cursos-->
          <h2>Seleccione Curso</h2>

    <div class="curso-container">
      <div class="campos-curso-seccion">
        <div class="campo-curso">
          <label for="curso">¿En qué curso participará?</label>
          <select id="curso" v-model="cursoSeleccionado" required @change="handleCursoChange">
            <option value="">Seleccione un curso</option>
            <option value="liderazgoJuvenil">Curso de Liderazgo Juvenil</option>
            <option value="primerosAuxilios">Curso de Primeros Auxilios en Campamento</option>
            <option value="gestionAmbiental">Curso de Gestión Ambiental Scout</option>
          </select>
        </div>

        <transition name="desplegar">
          <div v-if="cursoSeleccionado" class="campo-seccion">
            <label for="seccionCurso">Selecciona la Sección del Curso: <span style="color: red;">*</span></label>
            <select
              id="seccionCurso"
              v-model="seccionCurso"
              required
              @change="handleSeccionChange"
            >
              <option value="">Seleccione una sección</option>
              <option value="mañana">Mañana</option>
              <option value="tarde">Tarde</option>
              <option value="vespertino">Vespertino</option>
            </select>
          </div>
        </transition>
      </div>

      <div class="boton-descarga-container">
        <img src="/favicon.ico" alt="Logo Scout" class="logo-descarga" />
        <label class="label-descarga">Descarga y rellena tu ficha médica, te la pediremos más adelante!</label>
        <a href="/Ficha Medica.docx" download class="btn-download">
          <div class="svg-wrapper-1">
            <div class="svg-wrapper">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="24"
                height="24"
              >
                <path fill="none" d="M0 0h24v24H0z"></path>
                <path
                  fill="currentColor"
                  d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"
                ></path>
              </svg>
            </div>
          </div>
          <span>Descargar Ficha</span>
        </a>
      </div>
    </div>

  </section>
<!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <transition name="fade">
    <div v-if="cursoSeleccionado && seccionCurso" class="resto-formulario">
      <section>
              <div class="section-header">
                <h2>Datos Personales</h2>
                <div class="section-subtitle"></div>
              </div>
  <!-- :::::::::::::::::: INPUTS BÁSICOS ::::::::::::::::::::::::: -->
        <div class="section-grid">
          <div class="campo">
            <label for="nombre">Nombres:</label>
            <input id="nombre" v-model="nombre" type="text" placeholder="PRIMER Y SEGUNDO NOMBRE" />
          </div>
          <div class="campo">
            <label for="apellidoPaterno">Apellido Paterno:</label>
            <input id="apellidoPaterno" v-model="apellidoPaterno" type="text" placeholder="APELLIDO PATERNO" />
          </div>
        </div>

        <div class="section-grid">
          <div class="campo">
            <label for="apellidoMaterno">Apellido Materno:</label>
            <input id="apellidoMaterno" v-model="apellidoMaterno" type="text" placeholder="APELLIDO MATERNO" />
          </div>

          <div class="campo">
            <label for="rut">RUT (sin puntos ni guion):</label>
            <input id="rut" type="text" v-model="rut" maxlength="9" placeholder="Ej: 123456789" @input="rut = rut.replace(/[^0-9]/g, '')"
              :class="{ invalido: rut.length > 0 && rut.length < 7 }" required
            />
          </div>
        </div>

        <div class="section-grid">
          <div class="campo">
            <label for="fechaNacimiento">Fecha de Nacimiento:</label>
            <input id="fechaNacimiento" v-model="fechaNacimiento" type="date" />
          </div>
          <div class="campo">
            <label for="email">Correo Electrónico:</label>
            <input id="email" v-model="email" type="email" placeholder="INGRESE EMAIL" />
          </div>
        </div>

  <!--::::::::::::::::::: NÚMEROS DE CONTACTO :::::::::::::::::::::::::-->
      <div class="section-header">
        <!-- empty spacer to keep alignment if needed -->
      </div>
              <!-- Selector único de teléfono: el usuario elige qué tipo de teléfono ingresará y se muestra un solo input con prefijo +56 -->
              <!-- Número de contacto eliminado por solicitud del usuario -->

<!-- :::::::::::::::::: SELECTOR DE REGIONES Y DIRECCIÓN (agrupados) ::::::::::::::::::::::::: -->
<div class="section-grid">
  <div class="campo">
    <label for="Provincia">Provincia:</label>
    <select id="Provincia" v-model="regionSeleccionada">
      <option disabled value="">Seleccione una región</option>
      <option v-for="region in Object.keys(comunasPorRegion)" :key="region" :value="region">
        {{ region }}
      </option>
    </select>
  </div>

  <div class="campo">
    <label for="direccion">Dirección:</label>
    <input id="direccion" v-model="direccion" type="text" placeholder="INGRESE DIRECCIÓN" />
  </div>
</div>

<!-- Agrupamos Ciudad / Comuna / Distrito en una fila de 3 columnas -->
<transition name="desplegar">
  <div v-if="regionSeleccionada" class="section-grid-3" :key="regionSeleccionada">
    <div class="campo">
      <label for="ciudad">Ciudad:</label>
      <select id="ciudad" v-model="ciudadSeleccionada">
        <option disabled value="">Seleccione una ciudad</option>
        <option v-for="ciudad in Object.keys(ciudadesDisponibles)" :key="ciudad" :value="ciudad">
          {{ ciudad }}
        </option>
      </select>
    </div>

    <div class="campo">
      <label for="comuna">Comuna:</label>
      <select id="comuna" v-model="comunaSeleccionada">
        <option disabled value="">Seleccione una comuna</option>
        <option v-for="comuna in comunasDisponibles" :key="comuna" :value="comuna">
          {{ comuna }}
        </option>
      </select>
    </div>

    <div class="campo">
      <label for="distrito">Distrito:</label>
      <select id="distrito" v-model="distritoSeleccionado">
        <option disabled value="">Seleccione su distrito</option>
        <option value="Concepcion">Concepción</option>
        <option value="Talcahuano - Hualpen">Talcahuano - Hualpén</option>
        <option value="Rio Andalien">Río Andalién</option>
        <option value="BioBio">Biobío</option>
        <option value="Nahuelbuta">Nahuelbuta</option>
        <option value="Equipo Distrital">Equipo Distrital</option>
        <option value="Equipo Zonal">Equipo Zonal</option>
        <option value="Equipo Nacional">Equipo Nacional</option>
        <option value="Zona Ñuble">Zona Ñuble</option>
        <option value="Zona Los Lagos">Zona Los Lagos</option>
        <option value="Zona La Frontera">Zona La Frontera</option>
        <option value="Zona de los Rios">Zona de los Ríos</option>
        <option value="Otro">Otro</option>
      </select>
    </div>
  </div>
</transition>


  <!-- (Dirección ahora está agrupada con Provincia en la sección superior) -->

  <!-- :::::::::::::::::: SELECTOR DE ESTADO CIVIL ::::::::::::::::::::::::: -->
      <div class="section-grid">
        <div class="campo">
          <label for="estadoCivil">Estado Civil:</label>
          <select id="estadoCivil" v-model="estadoCivil">
            <option disabled value="">Seleccione su estado civil</option>
            <option value="soltero">Soltero/a</option>
            <option value="casado">Casado/a</option>
            <option value="divorciado">Divorciado/a</option>
            <option value="viudo">Viudo/a</option>
            <option value="conviviente_civil">Conviviente Civil</option>
          </select>
        </div>

        <div class="campo">
          <label for="profesion">Apodo para Credencial:</label>
          <input
            id="apodoCredencial"
            v-model="apodoCredencial"
            type="text"
            placeholder="INGRESE SU APODO O NOMBRE PARA CREDENCIAL"
            maxlength="50"
            @input="profesion = profesion.toUpperCase()"
          />
        </div>
      </div>

      <div class="section-grid">
        <div class="campo">
          <label for="tipoContacto">Tipo de contacto:</label>
          <select id="tipoContacto" v-model="tipoContactoSeleccionado">
            <option disabled value="">Seleccione una opción</option>
            <option value="telefono_fijo">Teléfono Fijo</option>
            <option value="celular">Celular</option>
            <option value="celular_whatsapp">Celular con WhatsApp</option>
            <option value="whatsapp">WhatsApp</option>
          </select>
          
          <!-- Input de número de teléfono que aparece debajo del select -->
          <transition name="desplegar">
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
          </transition>
        </div>
        
        <div class="campo">
          <label for="religion">Religión:</label>
          <input id="religion" v-model="religion" type="text" placeholder="INGRESE SU RELIGIÓN" />
        </div>
      </div>

  <!-- ::::::::::::::::::::: FOTO (Selfie o Subida) ::::::::::::::::::::: -->
<!-- Input para subir archivo oculto y botones de captura agrupados -->
<div class="section-grid file-row">
  <div class="campo" style="display: none;">
    <input
      type="file"
      id="foto"
      accept="image/png, image/jpeg"
      :disabled="camaraActiva || fotoUrl"
      @change="procesarFoto"
      ref="inputFoto"
    />
  </div>

  <div class="campo botones-inline">
    <label class="label-foto">¿Deseas subir una foto o tomar una foto?</label>
    <div class="botones-grupo">
      <button
        type="button"
        class="btn-subir-foto"
        @click="$refs.inputFoto.click()"
        :disabled="camaraActiva || fotoUrl"
      >
        📁 Subir foto
      </button>

      <button
        type="button"
        class="btn-capturar"
        @click="abrirCamara"
        :disabled="fotoSubida || fotoUrl"
      >
        📷 Tomar foto
      </button>

      <!-- Mostrar botón eliminar junto al tomar foto si ya hay foto -->
      <button
        v-if="fotoUrl"
        type="button"
        class="btn-eliminar"
        @click="eliminarFoto"
      >
        🗑️ Eliminar foto
      </button>
    </div>
  </div>
</div>

<!-- Vista previa -->
<div v-if="fotoUrl" class="preview">
  <img :src="fotoUrl" alt="Vista previa de la foto" />
</div>

<!-- Contenedor de cámara como overlay centrado -->
<div v-if="mostrarCamara" class="camara-overlay" @keydown.esc="cerrarCamara">
  <div class="camara-container" role="dialog" aria-modal="true">
    <button type="button" class="close-camera-btn" @click="cerrarCamara" aria-label="Cerrar cámara">✕</button>
    <video ref="video" autoplay playsinline></video>
    <div class="camara-actions">
      <button type="button" class="btn-foto" @click="capturarFoto">Capturar</button>
    </div>
    <canvas ref="canvas" style="display: none;"></canvas>
  </div>
</div>

<!-- ::::::::::::::::::::::::: RELIGIÓN ::::::::::::::::::::::::: -->
<!-- (Religión eliminado según solicitud del usuario) -->

<!-- ::::::::::::::::::: FORMADOR ::::::::::::::::::: -->
<section class="bloque-formador">
  <!-- Opción A: etiqueta tradicional arriba del select -->
  <div class="campo">
    <label for="formador">¿Eres Formador?</label>
    <select id="formador" v-model="esFormador" class="selector-formador">
      <option value="">Seleccione una opción</option>
      <option value="si">Sí</option>
      <option value="no">No</option>
    </select>
  </div>

  <!-- ::::::::::::::::::: CAMPOS ADICIONALES ::::::::::::::::::: -->
  <transition name="desplegar">
    <div v-if="esFormador === 'si'" class="campos-formador">
      <!-- Reorganizado: dos columnas dentro de formador -->
      <div class="formador-grid">
        <!-- Columna izquierda: label + textarea -->
        <div class="campo columna-izquierda">
          <label for="historialFormador">Historial de Formador:</label>
          <textarea
            id="historialFormador"
            v-model="historialFormador"
            placeholder="Describe tu experiencia o historial como formador"
            rows="6"
            maxlength="500"
          ></textarea>
        </div>

        <!-- Columna derecha: habilitaciones 1 y 2 (apiladas) -->
        <div class="campo columna-derecha">
          <div class="habilitaciones-vertical">
            <div class="checkbox-list">
              <div>
                <input id="habilitacion1" type="checkbox" class="custom-checkbox" v-model="habilidad1" true-value="si" false-value="no" />
                <label for="habilitacion1">Habilitación 1</label>
              </div>

              <div>
                <input id="habilitacion2" type="checkbox" class="custom-checkbox" v-model="habilidad2" true-value="si" false-value="no" />
                <label for="habilitacion2">Habilitación 2</label>
              </div>

              <div>
                <input id="verificado" type="checkbox" class="custom-checkbox" v-model="verificado" true-value="si" false-value="no" />
                <label for="verificado">Verificado</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</section>





</section>

<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--:::::::::::::::::::::::::          INFORMACION ASOCIACION       ::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <section>
    <div class="datosScout"></div> <!-- TITULO iNFORMACVION ACOCIACION-->
          <div class="section-header">
            <h2>Informacion Asociacion</h2>
            <div class="section-subtitle"></div>
          </div>


  <!-- :::::::::::::::::: SELECTOR DE ROL EN EL CURSO ::::::::::::::::::::::::: -->
      <label for="rol">Rol en el curso:</label>
      <select id="rol" v-model="rolSeleccionado">
        <option disabled value="">Seleccione su rol</option>
        <option value="participante">Participante</option>
        <option value="apoyo_formadores">Apoyo a formadores</option>
        <option value="formador">Formador(a)</option>
        <option value="equipo_servicio">Equipo de servicio</option>
        <option value="equipo_organizador">Equipo organizador</option>
        <option value="equipo_salud">Equipo de salud</option>
        <option value="otro">Otro</option>
      </select>

  <!-- TEXTAREA BLOQUEADO POR DEFECTO, SE HABILITA SI ELIGE "OTRO" -->
                    <Transition name="desplegar">
                      <div v-if="rolSeleccionado === 'otro'" class="campo">
                      <label for="rolOtro">Especifique su rol:</label>
                      <textarea
                        id="rolOtro"
                        v-model="rolOtro"
                        placeholder="INGRESE SU ROL AQUÍ..."
                        rows="3"
                        maxlength="100"
                        :disabled="rolSeleccionado !== 'otro'"
                      ></textarea>
                      </div>
                    </Transition>

  <!-- :::::::::::::::::: SELECTOR DE ZONA ::::::::::::::::::::::::: -->
        <label for="grupo">Zona al que pertenece:</label>
        <select id="grupo" v-model="zonaSeleccionada" @change="handleZonaChange">
          <option disabled value="">Seleccione su zona</option>
          <option value="Alcatipay">Alcatipay</option>
          <option value="Alfa Cruz">Alfa Cruz</option>
          <option value="Alpha y Omega">Alpha y Omega</option>
          <option value="Andalien">Andalien</option>
          <option value="Axis Mundi">Axis Mundi</option>
          <option value="Baden Powell - Tome">Baden Powell - Tomé</option>
          <option value="Buen Pastor">Buen Pastor</option>
          <option value="Buena Aventura">Buena Aventura</option>
          <option value="Callaqui">Callaqui</option>
          <option value="Catiray">Catiray</option>
          <option value="Elcan Mapu">Elcan Mapu</option>
          <option value="Enrique Valdebenito">Enrique Valdebenito</option>
          <option value="Equipo Zonal">Equipo Zonal</option>
          <option value="Espíritu Santo">Espíritu Santo</option>
          <option value="Fresia Müller Ruiz">Fresia Müller Ruiz</option>
          <option value="Halcones Negros">Halcones Negros</option>
          <option value="Helen Keller">Helen Keller</option>
          <option value="Huilliche">Huilliche</option>
          <option value="Inmaculada Concepción de Talcahuano">Inmaculada Concepción de Talcahuano</option>
          <option value="Kutral Üinkelen">Kutral Üinkelen</option>
          <option value="La Ascensión">La Ascensión</option>
          <option value="La Asunción">La Asunción</option>
          <option value="Lafkenche">Lafkenche</option>
          <option value="Lemu Inalaf">Lemu Inalaf</option>
          <option value="Liceo Alemán del Verbo Divino">Liceo Alemán del Verbo Divino</option>
          <option value="Mahuidanche">Mahuidanche</option>
          <option value="Manutara">Manutara</option>
          <option value="Mapu Antu">Mapu Antu</option>
          <option value="Mapu Ñuke">Mapu Ñuke</option>
          <option value="Monte Kenya">Monte Kenya</option>
          <option value="Namuncura">Namuncura</option>
          <option value="Pehuen">Pehuen</option>
          <option value="Pellu Wellang - Arauco">Pellu Wellang - Arauco</option>
          <option value="Peulla">Peulla</option>
          <option value="Rañileufu">Rañileufu</option>
          <option value="Rosa de los Vientos">Rosa de los Vientos</option>
          <option value="Rucapeñihue">Rucapeñihue</option>
          <option value="Sagrada Familia">Sagrada Familia</option>
          <option value="Sagrados Corazones">Sagrados Corazones</option>
          <option value="Salesiano">Salesiano</option>
          <option value="Salesianos Concepción">Salesianos Concepción</option>
          <option value="San Ignacio de Loyola">San Ignacio de Loyola</option>
          <option value="San Pablo">San Pablo</option>
          <option value="San Rafael">San Rafael</option>
          <option value="San Sebastian">San Sebastián</option>
          <option value="Santa Bárbara">Santa Bárbara</option>
          <option value="Santa Cecilia">Santa Cecilia</option>
          <option value="Santa María">Santa María</option>
          <option value="Tricolor Chileno">Tricolor Chileno</option>
          <option value="Wetripantu">Wetripantu</option>
          <option value="otro">Otro</option>
        </select>

    <!--:::::::::::::: TEXTAREA QUE SE HABILITA SOLO AL ELEGIR "OTRO"::::::::::::::::::::: -->
                          <Transition name="desplegar">
                            <div v-if="zonaSeleccionada === 'otro'" class="campo">
                            <label for="otraZona">Ingrese el nombre de la zona:</label>
                            <textarea
                              id="otraZona"
                              v-model="otraZona"
                              placeholder="ESCRIBA EL NOMBRE DE LA ZONA..."
                              rows="3"
                              maxlength="100"
                            ></textarea>
                            </div>
                          </Transition>
      <!-- :::::::::::::::::: GRUPO AL QUE PERTENECE ::::::::::::::::::::::::: -->
      <label for="rama">Grupo al que pertenece:</label>
      <select id="rama" v-model="grupoPertenece">
        <option disabled value="">Seleccione su grupo</option>
        <option value="Lobatos">Lobatos</option>
        <option value="Golondrinas">Golondrinas</option>
        <option value="Guias">Guías</option>
        <option value="Scouts">Scouts</option>
        <option value="Pioneros">Pioneros</option>
        <option value="Caminantes">Caminantes</option>
      </select>
    
<!--::::::::::::::::::::::SELECTOR NIVEL:::::::::::::::::::::::::::::::::::::::::::::::-->
    <label for="nivel">¿Qué nivel tienes?</label>
    <select id="nivel" v-model="nivelSeleccionado" required>
      <option disabled value="">Seleccione su nivel</option>
      <option value="Inicial">Inicial</option>
      <option value="Medio">Medio</option>
      <option value="Avanzado">Avanzado</option>
      <option value="Ninguno">Ninguno</option>
    </select>

<!--::::::::::::::::::::::SELECTOR RAMA PARA NIVEL MEDIO:::::::::::::::::::::::::::::::::::::::::::::::-->
                      <transition name="desplegar">
                        <div v-if="nivelSeleccionado === 'Medio'" class="campo">
                          <label for="ramaMedio">¿En qué rama tienes ese nivel?</label>
                          <select id="ramaMedio" v-model="ramaMedioSeleccionada">
                            <option disabled value="">Seleccione la rama</option>
                            <option value="Lobatos">Lobatos</option>
                            <option value="Golondrinas">Golondrinas</option>
                            <option value="Guías">Guías</option>
                            <option value="Scouts">Scouts</option>
                            <option value="Pioneros">Pioneros</option>
                            <option value="Caminantes">Caminantes</option>
                            <option value="Ninguno">Ninguno</option>
                          </select>
                        </div>
                      </transition>

  <!--::::::::::::::::::::::SELECTOR RAMA PARA NIVEL AVANZADO:::::::::::::::::::::::::::::::::::::::::::::::-->
                      <transition name="desplegar">
                        <div v-if="nivelSeleccionado === 'Avanzado'" class="campo">
                          <label for="ramaAvanzado">¿En qué rama tienes ese nivel?</label>
                          <select id="ramaAvanzado" v-model="ramaAvanzadoSeleccionada">
                            <option disabled value="">Seleccione la rama</option>
                            <option value="Lobatos">Lobatos</option>
                            <option value="Golondrinas">Golondrinas</option>
                            <option value="Guías">Guías</option>
                            <option value="Scouts">Scouts</option>
                            <option value="Pioneros">Pioneros</option>
                            <option value="Caminantes">Caminantes</option>
                            <option value="Ninguno">Ninguno</option>
                          </select>
                        </div>
                      </transition>

  </section>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Salud y Logistica        ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <section>
      <div class="saludLogistica"></div> <!-- Salud y Logistica-->
          <div class="section-header">
            <h2>Salud y Logistica</h2>
            <div class="section-subtitle"></div>
          </div>
  
  <div class="section-grid">
    <!--::::::::::::::::::: INPUT DE ALERGIAS/ENFERMEDADES ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="salud">¿Tiene alergias,enfermedad a considerar?</label>
      <select id="salud" v-model="tieneAlergiaEnfermedad">
        <option disabled value="">Seleccione una opción</option>
        <option value="Si">Sí</option>
        <option value="No">No</option>
      </select>

      <!--:::::::::::::::: TEXT AREA BLOQUEADO POR DEFECTO, SE HABILITA AL SELECCIONAR "si" :::::::::::::::::::::::::::::::::-->
      <transition name="desplegar">
        <div v-if="tieneAlergiaEnfermedad === 'Si'" style="margin-top: 12px;">
          <label for="detalleSalud">Detalle alergias,enfermedad o limitacion:</label>
          <textarea
            id="detalleSalud"
            v-model="detalleAlergiaEnfermedad"
            placeholder="INGRESE LA ALERGIAS,ENFERMEDAD O LIMITACION"
            rows="4"
            maxlength="255"
            :disabled="tieneAlergiaEnfermedad !== 'Si'"
          ></textarea>
        </div>
      </transition>
    </div>

    <!--::::::::::::::::::: INPUT DE LIMITACIONES ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="limitacion">¿Tiene alguna limitación?</label>
      <select id="limitacion" v-model="tieneLimitacion">
        <option disabled value="">Seleccione una opción</option>
        <option value="Si">Sí</option>
        <option value="No">No</option>
      </select>

      <!--:::::::::::::::: TEXT AREA BLOQUEADO POR DEFECTO, SE HABILITA AL SELECCIONAR "si" :::::::::::::::::::::::::::::::::-->
      <transition name="desplegar">
        <div v-if="tieneLimitacion === 'Si'" style="margin-top: 12px;">
          <label for="detalleLimitacion">Detalle de la limitación:</label>
          <textarea
            id="detalleLimitacion"
            v-model="detalleLimitacion"
            placeholder="INGRESE LA LIMITACION"
            rows="4"
            maxlength="255"
            :disabled="tieneLimitacion !== 'Si'"
          ></textarea>
        </div>
      </transition>
    </div>
  </div>

  <!--::::::::::::::::::::::CONTACTO DE EMERGENCIA:::::::::::::::::::::::::::::::::::::::::::::::-->
      <div class="section-grid">
        <div class="campo">
          <label for="nombreEmergencia">Nombre de contacto de emergencia:</label>
          <input id="nombreEmergencia" v-model="nombreEmergencia" type="text" placeholder="Ej: ALAN DAVE" />
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

<!--:::::::::::::::::::::: VEHÍCULO PROPIO Y ALIMENTACIÓN :::::::::::::::::::::::::::::::::::::::::::::::::::-->
<div class="section-grid">
  <div class="campo">
    <label for="vehiculoPropio">¿Viene en vehículo propio?</label>
    <select id="vehiculoPropio" v-model="vehiculoPropio" required>
      <option disabled value="">Seleccione una opción</option>
      <option value="si">Sí</option>
      <option value="no">No</option>
    </select>
  </div>

  <!-- :::::::::::::::::: SELECTOR DE TIPO DE ALIMENTACIÓN ::::::::::::::::::::::::: -->
  <div class="campo">
    <label for="alimentacion">Tipo de alimentación:</label>
    <select id="alimentacion" v-model="tipoAlimentacion">
      <option disabled value="">Seleccione su tipo de alimentación</option>

      <!-- Alimentación común -->
      <option value="omnivora">Omnívora</option>
      <option value="vegetariana">Vegetariana</option>
      <option value="vegana">Vegana</option>
      <option value="pescetariana">Pescetariana</option>
      <option value="flexitariana">Flexitariana</option>

      <!-- Dietas especiales por enfermedades -->
      <option value="diabetica">Dieta para diabetes</option>
      <option value="hipertension">Dieta para hipertensión</option>
      <option value="celiaca">Dieta sin gluten (celíaca)</option>
      <option value="baja_sodio">Dieta baja en sodio</option>
      <option value="baja_lipidos">Dieta baja en lípidos/colesterol</option>
      <option value="renal">Dieta renal</option>
      <option value="intolerancia_lactosa">Dieta sin lactosa</option>
      <option value="ninguna">Ninguna</option>
    </select>
  </div>
</div>

<!--:::::::::::::::::::::: CAMPOS SOLO SI SELECCIONA "SI" :::::::::::::::::::::::::::::::::::::::::::::::::::-->
              <transition name="desplegar">
                <div v-if="vehiculoPropio === 'si'" class="campo">
                  <div class="section-grid-3">
                    <div class="campo">
                      <label for="patentePropia">Patente del vehículo (formato: ABCD12)</label>
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
                      <label for="marcaPropia">Marca del vehículo:</label>
                      <input
                        id="marcaPropia"
                        v-model="marcaPropia"
                        type="text"
                        placeholder="Ej: Toyota"
                      />
                    </div>

                    <div class="campo">
                      <label for="modeloPropio">Modelo del vehículo:</label>
                      <input
                        id="modeloPropio"
                        v-model="modeloPropio"
                        type="text"
                        placeholder="Ej: Yaris"
                      />
                    </div>
                  </div>
                </div>
              </transition>

  <!-- Botón para subir ficha médica -->
  <div class="contenedor-boton-subir">
    <a href="#" @click.prevent="abrirSelectorArchivo" class="btn-subir-ficha">
      <div class="svg-wrapper-1">
        <div class="svg-wrapper">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="24"
            height="24"
          >
            <path fill="none" d="M0 0h24v24H0z"></path>
            <path
              fill="currentColor"
              d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"
            ></path>
          </svg>
        </div>
      </div>
      <span>Subir Ficha Médica</span>
    </a>
    <input 
      type="file" 
      ref="fichaMedicaInput" 
      @change="handleFichaMedicaUpload" 
      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
      style="display: none;"
    />
    <p v-if="fichaMedicaNombre" class="archivo-seleccionado">
      Archivo seleccionado: {{ fichaMedicaNombre }}
    </p>
  </div>

  </section>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::          Informacion Adicional      ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <section>
      <div class="informacionAdicional"></div> <!-- Titulo Informacion Adicional-->
          <div class="section-header">
            <h2>Informacion Adicional</h2>
            <div class="section-subtitle"></div>
          </div>
    
    <div class="section-grid">
      <!-- :::::::::::::::::: INPUT OBSERVACIONES DEL CURSO ::::::::::::::::::::::::: -->
      <div class="campo">
        <label for="observacionesCurso">Observaciones de curso:</label>
        <textarea
          id="observacionesCurso"
          v-model="observacionesCurso"
          placeholder="INGRESE CUALQUIER COMENTARIO O CONSIDERACIÓN"
          rows="4"
          maxlength="200"
        ></textarea>
      </div>

      <!-- :::::::::::::::::: INPUT TEXT AREA DE OTROS ::::::::::::::::::::::::: -->
      <div class="campo">
        <label for="consideraciones">Otros:</label>
        <textarea
          id="consideraciones"
          v-model="consideraciones"
          placeholder="INGRESE CUALQUIER COMENTARIO O CONSIDERACIÓN"
          rows="4"
          maxlength="200"
        ></textarea>
      </div>
    </div>

  <div class="section-grid">
    <!--::::::::::::::::::::::EXPERIENCIA CON NIÑOS:::::::::::::::::::::::::::::::::::::::::::::::-->
    <div class="campo">
      <label for="trabajoNinos">¿Ha trabajado con niños?</label>
      <select id="trabajoNinos" v-model="haTrabajadoConNinos" required>
        <option disabled value="">Seleccione una opción</option>
        <option value="si">Sí</option>
        <option value="no">No</option>
      </select>
      
      <transition name="desplegar">
        <div v-if="haTrabajadoConNinos === 'si'" style="margin-top: 12px;">
          <label for="tiempoTrabajoNinos">¿Cuánto tiempo?</label>
          <div style="display: flex; gap: 10px; align-items: center;">
            <!-- AÑOS -->
            <select id="añosTrabajadoNinos" v-model="añosTrabajoNinos" style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;">
              <option disabled value="">Años</option>
              <option v-for="n in 20" :key="n" :value="n">{{ n }} año{{ n > 1 ? 's' : '' }}</option>
            </select>

            <!-- MESES -->
            <select id="mesesTrabajadoNinos" v-model="mesesTrabajoNinos" style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;">
              <option disabled value="">Meses</option>
              <option v-for="m in 11" :key="m" :value="m">{{ m }} mes{{ m > 1 ? 'es' : '' }}</option>
            </select>
          </div>
        </div>
      </transition>
    </div>

    <!-- ::::::::::::::::: BENEFICIARIO ::::::::::::::::: -->
    <div class="campo">
      <label for="beneficiario">¿Estuviste de niño en el movimiento?</label>
      <select id="beneficiario" v-model="esBeneficiario" required>
        <option disabled value="">Seleccione una opción</option>
        <option value="si">Sí</option>
        <option value="no">No</option>
      </select>

      <!-- ::::::::::::::::: CAMPO DESPLEGABLE ::::::::::::::::: -->
      <transition name="desplegar">
        <div v-if="esBeneficiario === 'si'" style="margin-top: 12px;">
          <label for="tiempoBeneficiario">¿Cuánto tiempo?</label>
          <div style="display: flex; gap: 10px; align-items: center;">
            
            <!-- AÑOS -->
            <select
              id="añosTiempoBeneficiario"
              v-model="añosTiempoBeneficiario"
              style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;"
            >
              <option disabled value="">Años</option>
              <option v-for="n in 20" :key="n" :value="n">
                {{ n }} año{{ n > 1 ? 's' : '' }}
              </option>
            </select>

            <!-- MESES -->
            <select
              id="mesesTiempoBeneficiario"
              v-model="mesesTiempoBeneficiario"
              style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;"
            >
              <option disabled value="">Meses</option>
              <option v-for="m in 11" :key="m" :value="m">
                {{ m }} mes{{ m > 1 ? 'es' : '' }}
              </option>
            </select>
          </div>
        </div>
      </transition>
    </div>
  </div>

  <div class="section-grid">
    <!-- :::::::::::::::::: INPUT DE PROFESIÓN ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="profesion">Profesión:</label>
      <input
        id="profesion"
        v-model="profesion"
        type="text"
        placeholder="INGRESE SU PROFESIÓN"
        maxlength="50"
        @input="profesion = profesion.toUpperCase()"
      />
    </div>

    <!--:::::::::::::::::::::: ALOJAMIENTO :::::::::::::::::::::::::::::::::::::::::::::::::::-->
    <div class="campo">
      <div style="display: flex; align-items: center; gap: 0.6rem; margin-top: 33px; margin-left: 1px;">
        <input
          id="alojamiento"
          type="checkbox"
          class="custom-checkbox"
          v-model="necesitaAlojamiento"
          true-value="si"
          false-value="no"
        />
        <label for="alojamiento" style="cursor: pointer;">¿Necesita alojamiento?</label>
      </div>
    </div>
  </div>

  </section>
    </div>
  </transition>

  <!--:::::::::::::::::::::: BOTONES DE ACCIÓN ::::::::::::::::::::::::::::::::::-->
        <div class="botones-formulario" style="display: flex; justify-content: center; align-items: center; gap: 20px; width: 100%;">
          <button type="button" class="btn-vaciar" @click="limpiarFormulario">VACIAR</button>
          <button type="submit" class="btn-enviar" @click.prevent="enviarFormulario">ENVIAR</button>
        </div>
    
      </form>
    </div>
  </div>

</template>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::        SCRIPST  JS    :::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->

<script setup>
// :::::::::::::::::: IMPORTS Y WEAS :::::::::::::::::::::::::
import { ref, computed } from 'vue';

// :::::::::::::::::: MANEJO DE SELECCIÓN DE CURSO Y SECCIÓN :::::::::::::::::::::::::
const handleCursoChange = () => {
  if (!cursoSeleccionado.value) {
    // Cuando se selecciona "Seleccione un curso", limpiamos el formulario
    limpiarFormulario();
    seccionCurso.value = ""; // Reset sección when course changes
  }
};

const handleSeccionChange = () => {
  if (!seccionCurso.value) {
    // Si se deselecciona la sección, limpiamos el formulario
    limpiarFormulario();
  }
};

// Handler para el cambio de zona
const handleZonaChange = () => {
  if (zonaSeleccionada.value !== 'otro') {
    otraZona.value = ''; // Limpiamos el valor cuando no es "otro"
  }
};

// :::::::::::::::::: VARIABLES PARA CAPTURAR VALORES :::::::::::::::::::::::::
const tieneLimitacion = ref("");
const detalleLimitacion = ref("");
const zonaSeleccionada = ref("");
const otraZona = ref("");
const grupoPertenece = ref("");
const nombre = ref("");
const apellidoPaterno = ref("");
const apellidoMaterno = ref("");
const rut = ref("");
const fechaNacimiento = ref("");
const email = ref("");
const religion = ref("");
const tipoContactoSeleccionado = ref("");
const numeroContacto = ref("");
const estadoCivil = ref("");
const direccion = ref("");
const edad = ref(null);
const consideraciones = ref("");
const necesitaAlojamiento = ref("");
const profesion = ref("");
const apodoCredencial = ref("");
const tieneAlergiaEnfermedad = ref("");
const detalleAlergiaEnfermedad = ref("");
const tipoAlimentacion = ref("");
const rolSeleccionado = ref("");
const rolOtro = ref("");
const grupoSeleccionado = ref("");
const grupoOtro = ref("");
const ramaSeleccionada = ref("");
const opcionCargo = ref("");
const cargoTexto = ref("");
const añosUnidad = ref("");
const mesesUnidad = ref("");
const distritoSeleccionado = ref("");
const distritoOtro = ref("");
const nivelSeleccionado = ref("");
const ramaMedioSeleccionada = ref("");
const ramaAvanzadoSeleccionada = ref("");
const nombreEmergencia = ref("");
const numeroEmergencia = ref("");
const tieneNumeroFijo = ref("");
const numeroFijoEmergencia = ref("");
const haTrabajadoConNinos = ref("");
const añosTrabajoNinos = ref("");
const mesesTrabajoNinos = ref("");
const esBeneficiario = ref("");
const tiempoBeneficiario = ref("");
const esMiembroActivo = ref("");
const patenteVehiculo = ref("");
const vehiculoPropio = ref("");
const patentePropia = ref("");
const marcaPropia = ref("");
const modeloPropio = ref("");
const cursoSeleccionado = ref("");
const seccionCurso = ref("");
const añosTiempoBeneficiario = ref("");
const mesesTiempoBeneficiario = ref("");

const regionSeleccionada = ref("");
const ciudadSeleccionada = ref("");
const comunaSeleccionada = ref("");

// (campo de teléfono principal eliminado)

// Handler para el select de Dirección: si escoge una opción distinta de 'Otra',
// copiamos el valor a `direccion` (para que el payload siga usando `direccion`).
// onDireccionSelect removed — la dirección ahora se ingresa directamente en el campo `direccion`

// Variables para el formador
const esFormador = ref("");
const historialFormador = ref("");
const habilidad1 = ref("");
const habilidad2 = ref("");
const verificado = ref("");

// Variables para manejo de ficha médica
const fichaMedicaInput = ref(null);
const fichaMedicaNombre = ref("");
const fichaMedicaArchivo = ref(null);

// Función para abrir el selector de archivo
const abrirSelectorArchivo = () => {
  fichaMedicaInput.value.click();
};

// Función para manejar la carga del archivo
const handleFichaMedicaUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    fichaMedicaNombre.value = file.name;
    fichaMedicaArchivo.value = file;
  }
};

//:::::::::::::::::::::::::::::FUNCION LIMPIAR FORMULARIO (BOTON):::::::::::::::::::::::::::::::::::::::::::::::

function limpiarFormulario() {
  nombre.value = "";
  apellidoPaterno.value = "";
  apellidoMaterno.value = "";
  necesitaAlojamiento.value = "";
  rut.value = "";
  fechaNacimiento.value = "";
  email.value = "";
  religion.value = "";
  tipoContactoSeleccionado.value = "";
  numeroContacto.value = "";
  estadoCivil.value = "";
  direccion.value = "";
  edad.value = null;
  consideraciones.value = "";
  profesion.value = "";
  apodoCredencial.value = "";
  tieneAlergiaEnfermedad.value = "";
  detalleAlergiaEnfermedad.value = "";
  tipoAlimentacion.value = "";
  rolSeleccionado.value = "";
  rolOtro.value = "";
  grupoSeleccionado.value = "";
  grupoOtro.value = "";
  ramaSeleccionada.value = "";
  opcionCargo.value = "";
  cargoTexto.value = "";
  añosUnidad.value = "";
  mesesUnidad.value = "";
  distritoSeleccionado.value = "";
  distritoOtro.value = "";
  nivelSeleccionado.value = "";
  ramaMedioSeleccionada.value = "";
  ramaAvanzadoSeleccionada.value = "";
  nombreEmergencia.value = "";
  numeroEmergencia.value = "";
  tieneNumeroFijo.value = "";
  numeroFijoEmergencia.value = "";
  haTrabajadoConNinos.value = "";
  esBeneficiario.value = "";
  tiempoBeneficiario.value = "";
  esMiembroActivo.value = "";
  patenteVehiculo.value = "";
  vehiculoPropio.value = "";
  patentePropia.value = "";
  marcaPropia.value = "";
  modeloPropio.value = "";
  cursoSeleccionado.value = "";
  regionSeleccionada.value = "";
  ciudadSeleccionada.value = "";
  comunaSeleccionada.value = "";
  añosTiempoBeneficiario.value = "";
  mesesTiempoBeneficiario.value = "";

  
  // Limpia también los demás campos que tengas
  alert("Formulario vaciado correctamente.");
}

// Validación del formato de patente chilena (ej: AB-CD-12)
function validarPatentePropia() {
  // Permite formato: AA-BB-11 o AB-CD-12 o similar
  const formato = /^[A-Z]{2}-[A-Z]{2}-\d{2}$/;
  if (patenteVehiculo.value && !formato.test(patenteVehiculo.value.toUpperCase())) {
    patenteVehiculo.value = patenteVehiculo.value
      .toUpperCase()
      .replace(/[^A-Z0-9-]/g, ""); // limpia caracteres no válidos
  }
}

const fotoUrl = ref(null)
const mostrarCamara = ref(false)
const video = ref(null)
const canvas = ref(null)
const camaraActiva = ref(false)
const fotoSubida = ref(false)
const fotoFinal = ref(null)

let stream = null

function procesarFoto(event) {
  const file = event.target.files[0]
  if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
    if (file.size <= 50 * 1024 * 1024) {
      fotoUrl.value = URL.createObjectURL(file)
      fotoSubida.value = true
      fotoFinal.value = file
    } else {
      alert('La imagen excede el tamaño máximo de 50MB.')
    }
  } else {
    alert('Solo se permiten imágenes en formato JPG o PNG.')
  }
}

async function abrirCamara() {
  try {
    mostrarCamara.value = true
    camaraActiva.value = true
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream
  } catch (error) {
    alert('No se pudo acceder a la cámara. Verifica permisos o hardware disponible.')
  }
}

function capturarFoto() {
  const context = canvas.value.getContext('2d')
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)

  const dataUrl = canvas.value.toDataURL('image/png')
  fotoUrl.value = dataUrl
  fotoFinal.value = dataUrl
  cerrarCamara()
}

function cerrarCamara() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  mostrarCamara.value = false
  camaraActiva.value = false
}

//::::::::::::::::::Nueva función: eliminar la foto actual:::::::::::::::::::::::::
function eliminarFoto() {
  fotoUrl.value = null
  fotoFinal.value = null
  fotoSubida.value = false
  camaraActiva.value = false
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  mostrarCamara.value = false
  // Limpia el input file por si el usuario subió un archivo
  const input = document.getElementById('foto')
  if (input) input.value = ''
}



// :::::::::::::::::: LISTA DE REGIONES, CIUDADES Y COMUNAS ::::::::::::::::::::::::: 
const comunasPorRegion = {
  "Arica y Parinacota": {
    "Arica": ["Arica"],
    "Putre": ["Putre"],
    "General Lagos": ["General Lagos"],
    "Camarones": ["Camarones"]
  },
  "Tarapacá": {
    "Iquique": ["Iquique", "Alto Hospicio"],
    "Tamarugal": ["Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]
  },
  "Antofagasta": {
    "Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal"],
    "El Loa": ["Calama", "Ollagüe", "San Pedro de Atacama"],
    "Tocopilla": ["Tocopilla", "María Elena"]
  },
  "Atacama": {
    "Copiapó": ["Copiapó", "Caldera", "Tierra Amarilla"],
    "Chañaral": ["Chañaral", "Diego de Almagro"],
    "Huasco": ["Vallenar", "Alto del Carmen", "Freirina", "Huasco"]
  },
  "Coquimbo": {
    "Elqui": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña"],
    "Limarí": ["Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
    "Choapa": ["Illapel", "Canela", "Los Vilos", "Salamanca"]
  },
  "Valparaíso": {
    "Valparaíso": ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví"],
    "Isla de Pascua": ["Isla de Pascua"],
    "Los Andes": ["Los Andes", "Calle Larga", "Rinconada", "San Esteban"],
    "Petorca": ["La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar"],
    "Quillota": ["Quillota", "La Calera", "Hijuelas", "La Cruz", "Nogales"],
    "San Antonio": ["San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo"],
    "San Felipe de Aconcagua": ["San Felipe", "Catemu", "Llay-Llay", "Panquehue", "Putaendo", "Santa María"],
    "Marga Marga": ["Quilpué", "Limache", "Olmué", "Villa Alemana"]
  },
  "Metropolitana de Santiago": {
    "Santiago": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Puente Alto", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura"],
    "Cordillera": ["San José de Maipo"],
    "Chacabuco": ["Colina", "Lampa", "Tiltil"],
    "Maipo": ["San Bernardo", "Buin", "Calera de Tango", "Paine"],
    "Talagante": ["Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"],
    "Melipilla": ["Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro"]
  },
  "Libertador General Bernardo O'Higgins": {
    "Cachapoal": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente"],
    "Cardenal Caro": ["Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones"],
    "Colchagua": ["San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"]
  },
  "Maule": {
    "Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
    "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"],
    "Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
    "Linares": ["Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"]
  },
  "Ñuble": {
    "Diguillín": ["Bulnes", "Chillán", "Chillán Viejo", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay"],
    "Itata": ["Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Quirihue", "Ránquil", "Treguaco"],
    "Punilla": ["Coihueco", "Ñiquén", "San Carlos", "San Fabián", "San Nicolás"]
  },
  "Biobío": {
    "Concepción": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén"],
    "Arauco": ["Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa"],
    "Biobío": ["Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"]
  },
  "La Araucanía": {
    "Cautín": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica"],
    "Malleco": ["Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Purén", "Renaico", "Traiguén", "Victoria"]
  },
  "Los Ríos": {
    "Valdivia": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli"],
    "Ranco": ["La Unión", "Futrono", "Lago Ranco", "Río Bueno"]
  },
  "Los Lagos": {
    "Llanquihue": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Llanquihue", "Los Muermos", "Maullín", "Puerto Varas"],
    "Chiloé": ["Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao"],
    "Osorno": ["Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo"]
  },
  "Aysén del General Carlos Ibáñez del Campo": {
    "Coyhaique": ["Coyhaique", "Lago Verde"],
    "Aysén": ["Aysén", "Cisnes", "Guaitecas"],
    "General Carrera": ["Cochrane", "O'Higgins"],
    "Capitán Prat": ["Tortel"]
  },
  "Magallanes y de la Antártica Chilena": {
    "Magallanes": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio"],
    "Antártica": ["Cabo de Hornos", "Antártica"],
    "Tierra del Fuego": ["Porvenir", "Primavera", "Timaukel"],
    "Última Esperanza": ["Puerto Natales", "Torres del Paine"]
  }
};

// :::::::::::::::::: LOGICA FILTRO DE LISTA DE CUIDADES Y COMUNAS :::::::::::::::::::::::::

// Ciudades disponibles según la región elegida
const ciudadesDisponibles = computed(() => {
  return regionSeleccionada.value ? comunasPorRegion[regionSeleccionada.value] : {};
});

// Comunas disponibles según la ciudad elegida
const comunasDisponibles = computed(() => {
  if (regionSeleccionada.value && ciudadSeleccionada.value) {
    return comunasPorRegion[regionSeleccionada.value][ciudadSeleccionada.value] || [];
  }
  return [];
});
</script>


  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::        STYLES CSS     :::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->

<style scoped>


/* :::::::::: ANIMACIÓN DESPLEGABLE :::::::::: */
.desplegar-enter-active, .desplegar-leave-active {
  transition: all 0.4s ease;
  overflow: hidden;
}

.desplegar-enter-from, .desplegar-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.desplegar-enter-to, .desplegar-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Smooth horizontal deploy for phone input (fade + slide + simulated width)
   Smoother animation: longer duration, eased cubic-bezier and subtle shadow at end */
.phone-desplegar-enter-active,
.phone-desplegar-leave-active {
  /* separate timings: opacity+transform for feel, max-width slightly longer to avoid clipping */
  transition: opacity 380ms cubic-bezier(.2,.8,.2,1),
              transform 380ms cubic-bezier(.2,.8,.2,1),
              max-width 440ms cubic-bezier(.2,.8,.2,1);
  overflow: hidden;
  will-change: opacity, transform, max-width;
}
.phone-desplegar-enter-from,
.phone-desplegar-leave-to {
  opacity: 0;
  transform: translateX(18px) scale(.995);
  max-width: 0;
}
.phone-desplegar-enter-to,
.phone-desplegar-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
  max-width: 1000px; /* allow expansion to available space inside flex */
  box-shadow: 0 6px 18px rgba(16,24,40,0.06); /* subtle depth on reveal */
  border-radius: 6px; /* match input rounded corners when revealed */
}

/* ======================================================
======================================================
*/
.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;             /* consistent horizontal/vertical spacing */
  align-items: start;
  margin-bottom: 12px;   /* spacing between stacked sections */
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;              /* label to control spacing */
}

.campo label {
  display: block;
  margin: 0;
  font-size: 14px;
  color: #334155;       /* slightly dark, accessible */
  font-weight: 600;
}

/* Unified control styles for inputs, selects and textarea - uiverse.io inspired */
input[type="text"],
input[type="email"],
input[type="tel"],
input[type="date"],
select,
textarea,
.selector-formador {
  width: 100%;
  padding: 12px 16px !important;
  border: 2px solid #e8e8e8 !important;
  border-radius: 10px !important;
  background: #fff !important;
  box-sizing: border-box;
  font-size: 15px !important;
  color: #0d0c22 !important;
  font-weight: 500 !important;
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1) !important;
  box-shadow: 0px 0px 20px -18px !important;
}

input:hover,
select:hover,
textarea:hover,
.selector-formador:hover {
  border: 2px solid #2f2c45 !important;
  box-shadow: 0px 0px 20px -17px !important;
}

input:focus,
select:focus,
textarea:focus,
.selector-formador:focus {
  outline: none !important;
  border: 2px solid #2f2c45 !important;
  box-shadow: 0px 0px 20px -17px !important;
}

input:active,
select:active,
textarea:active {
  transform: scale(0.995);
}

/* Make select arrows visually consistent and leave space for them */
select.selector-formador {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  padding-right: 40px;
  background-image: linear-gradient(45deg,#0000 50%,#000 50%), linear-gradient(135deg,#0000 50%,#000 50%);
  background-position: calc(100% - 18px) calc(1em + 2px), calc(100% - 13px) calc(1em + 2px);
  background-size: 6px 6px, 6px 6px;
  background-repeat: no-repeat;
}

/* Phone row: keep phone type select fixed size and input flexible */
.phone-row {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.phone-row .phone-select {
  flex: 0 0 320px; /* matches Provincia width target */
}
.phone-row .phone-input {
  flex: 1 1 auto;
}

/* Prefix in phone inputs */
.phone-input-row { display:flex; gap:8px; align-items:center; }
.phone-input-row .prefix { background:transparent; color:#0f172a; padding:8px 6px; }

/* Responsive: stack columns on narrow screens */
@media (max-width: 760px) {
  .section-grid { grid-template-columns: 1fr; }
  .phone-row { flex-direction: column; }
  .phone-row .phone-select { flex: none; width: 100%; }
}

/* ::::::::::::::::::: FORMADOR ::::::::::::::::::: */
.bloque-formador {
  margin-top: 25px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  text-align: center;
}

/* Alinea las etiquetas dentro del bloque de formador encima y a la izquierda */
.bloque-formador .campo label {
  display: block;
  text-align: left; /* fuerza la alineación a la izquierda */
  width: 100%;
  margin-bottom: 8px; /* separa la label del textarea */
  color: #333;
  font-weight: 600;
}

/* Asegura que el textarea del formador ocupe el ancho disponible y quede alineado a la izquierda */
.bloque-formador .campo textarea {
  width: 100%;
  max-width: 700px; /* conserva un límite razonable */
  box-sizing: border-box;
  margin: 0; /* elimina centrado por márgenes previos */
}

/* Grid específico para la sección de formador: textarea a la izquierda, habilitaciones a la derecha */
.formador-grid {
  display: grid;
  grid-template-columns: 1fr 320px; /* izquierda flexible, derecha columna fija más estrecha */
  gap: 18px;
  align-items: start;
}

.bloque-formador .columna-izquierda label {
  display: block;
  text-align: left;
  width: 100%;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
}

.bloque-formador .columna-izquierda textarea {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.habilitaciones-vertical .campo { margin-bottom: 12px; }

/* Ajuste vertical: bajar la columna derecha para alinear con el inicio del textarea */
.bloque-formador .columna-derecha {
  margin-top: 26px; /* baja la columna para que los checkboxes queden alineados con el textarea */
}

/* Custom checkbox based on uiverse example (calm-wasp-75) */
.bloque-formador {
  --_clr-primary: #333;
  --_clr-checked: #127acf;
}
.bloque-formador .checkbox-list > div {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-block-start: 0.4rem;
}
.bloque-formador label[for] {
  cursor: pointer;
  color: var(--_clr-primary);
  user-select: none;
}
.bloque-formador input[type="checkbox"].custom-checkbox {
  appearance: none;
  -webkit-appearance: none;
  outline: none;
  width: 1.5rem;
  height: 1.5rem;
  aspect-ratio: 1;
  padding: 0.12rem;
  background: transparent;
  border: 1px solid var(--_clr-primary);
  border-radius: 4px;
  display: grid;
  place-content: center;
  cursor: pointer;
  transition: all 140ms ease-in-out;
}
.bloque-formador input[type="checkbox"].custom-checkbox::after {
  content: '';
  color: #fff;
  font-weight: 700;
  transform: scale(0);
  transition: transform 120ms ease-in-out;
}
.bloque-formador input[type="checkbox"].custom-checkbox:checked {
  background: var(--_clr-checked);
  border-color: var(--_clr-checked);
}
.bloque-formador input[type="checkbox"].custom-checkbox:checked::after {
  content: '✓';
  transform: scale(1);
  font-size: 0.95rem;
}

@media (max-width: 900px) {
  .formador-grid { grid-template-columns: 1fr; }
}

@media (max-width: 900px) {
  /* En pantallas pequeñas volvemos a la normalidad y removemos el offset */
  .bloque-formador .columna-derecha { margin-top: 12px; }
}

@media (max-width: 900px) {
  .formador-grid { grid-template-columns: 1fr; }
}

/* Estilos para checkbox de alojamiento (mismo estilo que habilidades) */
input[type="checkbox"].custom-checkbox {
  appearance: none;
  -webkit-appearance: none;
  outline: none;
  width: 1.5rem;
  height: 1.5rem;
  aspect-ratio: 1;
  padding: 0.12rem;
  background: transparent;
  border: 1px solid #333;
  border-radius: 4px;
  display: grid;
  place-content: center;
  cursor: pointer;
  transition: all 140ms ease-in-out;
}

input[type="checkbox"].custom-checkbox::after {
  content: '';
  color: #fff;
  font-weight: 700;
  transform: scale(0);
  transition: transform 120ms ease-in-out;
}

input[type="checkbox"].custom-checkbox:checked {
  background: #127acf;
  border-color: #127acf;
}

input[type="checkbox"].custom-checkbox:checked::after {
  content: '✓';
  transform: scale(1);
  font-size: 0.95rem;
}

.titulo-bloque {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.selector-formador,
.selector-habilidad {
  width: 90%;
  max-width: 300px;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
  color: #333;
  background-color: white;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.selector-formador:focus,

/* Estilo específico para el selector de tipo de teléfono: coherente con otros selects */
/* Removed .phone-type-select so the phone-type select uses the standard .campo + .selector-formador styles */
.selector-habilidad:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}
.campo > select#tipoTelefono.selector-formador {
  /* Layout: poner select y campo de número en la misma fila */
  display: flex;
  gap: 16px;
  align-items: flex-end; /* labels encima, inputs alineados */
  flex-wrap: wrap;
}
.phone-select {
  flex: 0 0 auto; /* mantiene su ancho natural (controlado por .selector-formador) */
}
.phone-input {
  flex: 1 1 320px; /* input ocupará el espacio restante pero no menos de 320px */
  min-width: 0; /* allow flex children to shrink properly */
  overflow: hidden; /* required so max-width animation clips content during the deploy */
}
.phone-input .phone-input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

@media (max-width: 700px) {
  /* En pantallas pequeñas apilamos verticalmente */
  .phone-row { flex-direction: column; align-items: stretch; }
  .phone-input { flex: 1 1 auto; }
}

/* Asegura que la etiqueta del selector de teléfono quede encima del select y comparta la estética */
.campo > label[for="tipoTelefono"] {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
}
.campo > select#tipoTelefono.selector-formador {
  width: 90%;
  max-width: 300px;
}

/* Centrar la etiqueta y el select del campo '¿Eres Formador?' */
.bloque-formador .campo label[for="formador"] {
  text-align: center;
  display: block;
  width: 100%;
  margin-bottom: 8px;
}
.bloque-formador .campo select#formador,
.bloque-formador .selector-formador {
  margin-left: auto;
  margin-right: auto;
  display: block;
}

/* Estilos para el selector de tipo de teléfono (botones segmentados) */
.phone-type-buttons .segmented-btn {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
.phone-type-buttons .segmented-btn.active {
  background: #127acf;
  color: white;
  border-color: #127acf;
}
.phone-type-buttons .segmented-btn:focus {
  outline: 2px solid rgba(18,124,207,0.18);
}

.prefix { font-weight: 700; }

/* Floating label pattern for specific fields (used by the formador select) */
.floating-field {
  position: relative;
  width: 90%;
  max-width: 320px;
  margin-bottom: 12px;
}
.floating-field .selector-formador {
  width: 100%;
  /* add top padding so the label can sit inside the select before floating */
  padding: 18px 10px 10px;
  box-sizing: border-box;
}
.floating-label {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  transition: all 0.18s ease;
  pointer-events: none;
  background: #f8fafc; /* match bloque-formador background to avoid overlap */
  padding: 0 6px;
  color: #666;
  font-size: 14px;
  font-weight: 600;
}
.floating-field.is-filled .floating-label,
.floating-field:focus-within .floating-label {
  top: -8px;
  transform: translateY(0);
  font-size: 12px;
  color: var(--_clr-checked, #127acf);
}

.campos-formador {
  margin-top: 20px;
}

.habilidades {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

textarea {
  width: 90%;
  max-width: 500px;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
  resize: none;
  outline: none;
  transition: border-color 0.3s;
}

textarea:focus {
  border-color: #3b82f6;
}

/* Transición suave al aparecer */
.desplegar-enter-active,
.desplegar-leave-active {
  transition: all 0.4s ease;
}
.desplegar-enter-from,
.desplegar-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}


/* :::::::::::::::::::: CHECKBOX MODERNO Y CENTRADO :::::::::::::::::::: */
.campo-checkbox {
  display: flex;
  justify-content: center;      /* Centra horizontalmente */
  padding: 15px 10px;              /* Espaciado vertical */
}

.campo-checkbox label {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #333;
  background-color: #f9f9f9;    /* Fondo suave */
  padding: 10px 20px;           /* Padding interno */
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1); /* Suaviza el bloque */
  transition: all 0.3s ease;
}

.campo-checkbox label:hover {
  background-color: #f0f8ff;    /* Azul muy claro al pasar el mouse */
  transform: translateY(-2px);
}

.campo-checkbox input[type="checkbox"] {
  accent-color: #2196f3;        /* Azul moderno */
  width: 20px;
  height: 20px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.campo-checkbox input[type="checkbox"]:hover {
  transform: scale(1.1);
}


.invalido {
  border: 2px solid #e74c3c; /* rojo para indicar error */
}

/* Estilos para la transición del formulario */
.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
  max-height: 9999px;
  opacity: 1;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

.resto-formulario {
  transition: all 1s ease;
}

* { font-family: "Calibri", sans-serif; } 

/*:::::::::::::BOTON DE FOTO STYLES::::::::::::::::*/
/* :::::::::::::::::::: PREVISUALIZACIÓN DE FOTO :::::::::::::::::::: */
.preview {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}

.preview img {
  width: 180px;        /* Tamaño fijo para mantener proporción uniforme */
  height: 180px;
  object-fit: cover;   /* Recorta y centra sin deformar */
  border-radius: 10px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
}

/* :::::::::::::::::::: BOTONES DE FOTO :::::::::::::::::::: */
.botones-foto {
  display: flex;
  justify-content: center; /* Centra los botones horizontalmente */
  gap: 10px;
  margin-top: 15px;
}

.btn-capturar,
.btn-eliminar,
.btn-subir-foto {
  padding: 10px 15px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-subir-foto {
  background-color: #28a745;
  color: white;
}

.btn-subir-foto:hover {
  background-color: #218838;
}

.label-foto {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  margin-right: 15px;
  white-space: nowrap;
}

.btn-capturar {
  background-color: #007bff;
  color: white;
}

.btn-capturar:hover {
  background-color: #0056b3;
}

.btn-eliminar {
  background-color: #dc3545;
  color: white;
}

.btn-eliminar:hover {
  background-color: #b02a37;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* :::::::::::::::::::: BOTÓN DE CAPTURA :::::::::::::::::::: */
.btn-foto {
  background: linear-gradient(135deg, #2196f3, #1e88e5);
  color: white;
  font-weight: 600;
  font-size: 16px;
  padding: 12px 25px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(30, 136, 229, 0.4);
  margin-top: 10px;
}

.btn-foto:hover {
  background: linear-gradient(135deg, #42a5f5, #1976d2);
  box-shadow: 0 6px 12px rgba(25, 118, 210, 0.45);
  transform: translateY(-2px);
}

.btn-foto:active {
  transform: scale(0.97);
  box-shadow: 0 3px 8px rgba(25, 118, 210, 0.3);
}

.btn-foto::before {
  content: "📸 ";
}

.file-row {
  display: flex;
  gap: 12px;
  align-items: center; /* centra verticalmente el input y los botones */
}

.botones-inline {
  display: flex !important;
  flex-direction: column !important;
  align-items: center;
  gap: 5px;
  margin-left: 0;
  margin-top: 0;
}

.botones-inline .botones-grupo {
  display: flex;
  gap: 12px;
  align-items: center;
}
.botones-inline .btn-capturar,
.botones-inline .btn-subir-foto,
.botones-inline .btn-eliminar {
  margin-bottom: 0; /* eliminar offsets verticales forzados */
  margin-top: 10px; /* bajar ambos botones 10px */
  transform: none; /* evitar transformaciones que muevan el botón fuera del flujo */
}

/* Limitar el ancho del primer campo (input de archivo) para dejar espacio al botón
   y posicionar el botón cerca del input (el usuario pidió colocarlo en el recuadro rojo). */
.file-row > .campo:first-child {
  flex: 1 1 60%;
  min-width: 180px;
}
.file-row > .campo.botones-inline {
  flex: 0 0 auto;
}

@media (max-width: 900px) {
  .botones-inline { align-items: center; }
  .botones-inline .btn-capturar { margin-bottom: 0; transform: none; }
}

/* Ajuste para la fila de archivo/foto: alinear items al inicio para que la celda de botones pueda bajar */


/* :::::::::::::::::::: CONTENEDOR DE CÁMARA :::::::::::::::::::: */
.camara-container {
  display: flex;
  flex-direction: column;
  align-items: center;         /* Centra horizontalmente */
  justify-content: center;     /* Centra verticalmente */
  gap: 10px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 640px;            /* Aumentado para vista centrada */
  box-sizing: border-box;
}

/* :::::::::::::::::::: VIDEO DE CÁMARA :::::::::::::::::::: */
.camara-container video {
  width: 100%;
  height: 360px;
  max-width: 600px;
  border-radius: 10px;
  border: 2px solid #2196f3;
  object-fit: cover;           /* Evita deformación */
  background-color: #000;      /* Fondo oscuro mientras carga */
}

/* Fullscreen overlay that centers the camera container */
.camara-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.45);
  z-index: 2000;
  padding: 24px;
}

.close-camera-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.camara-actions { margin-top: 8px; }


.formulario { 
    display: flex; 
    flex-direction: column; 
    justify-content: flex-start; /* Cambiado a flex-start para alinear al inicio */ 
    align-items: center; /* Centra horizontalmente */ 
    min-height: 100vh; /* Ocupa todo el alto de la ventana */
    padding-top: 30px; /* Ajusta este valor para mover el formulario más arriba o abajo */
    background: linear-gradient(135deg, #2c5cdd, #2563eb, #3b82f6);
} 

textarea { 
    resize: none; /* desactiva el cambio de tamaño con el mouse */ 
    height: 100px; /* ||alto fijo (puedes ajustar a tu gusto) */ 
    width: 100%; /* asegura que ocupe todo el ancho del contenedor */ 
    box-sizing: border-box; /* evita desbordes por padding */ 
} 

h2 { 
    font-size: 20px; /* tamaño de los sub titulos */ 
    color: #333; 
    font-weight: 600; 
    text-align: center; 
    margin: 1.5rem 0 1rem 0; 
    border-bottom: 2px solid #428ce1; 
    padding-bottom: 6px; 
} 

section {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border: #7d787834 1px solid;
}

.formulario :deep(input), .formulario :deep(select), .formulario :deep(textarea) { 
    padding: 5px 5px; 
    border: 1px solid #ccc; 
    border-radius: 6px; 
    font-size: 16px; /* Tamaño de fuente legible dentro de los inputs */ 
    background-color: #f9f9f9; 
    color: #333; 
    transition: all 0.2s ease; 
    width: 100%; 
    box-sizing: border-box; 
} 

.formulario :deep(input:focus), .formulario :deep(select:focus), .formulario :deep(textarea:focus) { /*border-color: #3079f0;*/ 
    box-shadow: 0 0 4px rgba(2, 145, 255, 0.925); 
    outline: none; 
} 
    
.formulario :deep(label) { 
    font-weight: 600; color: #444; 
    margin-bottom: 5px; 
    display: inline-block; 
} 

/* OUTER FORM LAYOUT: central card that fills the red-box area in the mockup */
.form-outer {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 32px 24px;
  box-sizing: border-box;
}

.form-inner {
  width: 100%;
  max-width: 1100px; /* occupy central wide area */
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.98));
  padding: 34px;
  border-radius: 14px;
  box-shadow: 0 18px 40px rgba(16, 24, 40, 0.12);
  box-sizing: border-box;
}

/* Section card inside the main white container to mimic the example */
section {
  background: #ffffff;
  border-radius: 10px;
  padding: 22px 20px;
  margin-bottom: 18px;
  box-shadow: 0 6px 18px rgba(11, 34, 92, 0.04);
  border: 1px solid rgba(15, 23, 42, 0.04);
}

.section-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}

.section-header h2 {
  font-size: 18px;
  margin: 0;
  color: #1f2937; /* darker heading */
  font-weight: 700;
}

.section-subtitle {
  height: 2px;
  background: linear-gradient(90deg, rgba(59,130,246,0.15), rgba(59,130,246,0.25));
  width: 100%;
  border-radius: 2px;
}

/* grid helper to layout fields in two columns like the example */
.section-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* three-column helper for compact rows (city / zip / state) */
.section-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  align-items: end;
  margin-top: 8px;
}

/* Responsive: stack on small screens */
@media (max-width: 900px) {
  .section-grid { grid-template-columns: 1fr; }
  .section-grid-3 { grid-template-columns: 1fr; }
}

/* make smaller input groups occupy full width when needed */
.full-width {
  grid-column: 1 / -1;
}

/* Reduce the default input background inside cards */
/* .form-inner :deep(input), .form-inner :deep(select), .form-inner :deep(textarea) {
  background-color: #fbfdff;
} */

/* Override: for rows that also have .file-row we need flex layout (overrides .section-grid)
This forces the file input and the buttons to sit side-by-side and allows shifting
   the botones-inline block left so the blue button sits inside the empty area. */
.section-grid.file-row {
  display: flex !important;
  gap: 12px !important;
  align-items: center !important;
}
.section-grid.file-row .botones-inline {
  /* reduce left shift to move buttons to the right */
  margin-left: -1px !important;
}

h1 {
  font-family: "Segoe UI", "Calibri", sans-serif;
  font-weight: 700;
  font-size: 2.2rem;
  text-align: center;
  color: #ffffff;
  background-color: #1e3b728c; /* azul profundo */
  background-image: linear-gradient(135deg, #2a5298, #1e3c72);
  opacity: 70%;
  padding: 20px;
  border-radius: 10px 10px 0 0; /* redondea solo arriba */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
  letter-spacing: 8px;
  text-transform: capitalize;
  width: 70%; /* Aumentado para coincidir con el nuevo ancho del formulario */
  margin-bottom: 20px;
  box-sizing: border-box;
}



input, select, textarea { 
    padding: 10px; 
    border-radius: 6px; 
    border: 1px solid #ccc; 
    width: 100%; 
    box-sizing: border-box; /* Asegura que padding no rompa el ancho */ 
    font-size: 14px; 
    font-weight: 500; 
    color: #333; 
    transition: all 0.2s ease; 
} 
/* Efecto al enfocar (hover o focus) */ 
input:focus, select:focus, textarea:focus { 
    border-color: #4CAF50; /* Verde suave */ 
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.3); 
    outline: none; 
} 
/* Placeholder más suave */ 
::placeholder { 
    color: #999; 
} 
/* :::::::::::::::::::: EFECTO DESPLEGABLE :::::::::::::::::::: */ 
.desplegar-enter-active, .desplegar-leave-active { 
  transition: all 0.5s ease;
} 
.desplegar-enter-from, .desplegar-leave-to { 
    opacity: 0; 
    transform: translateY(-10px); 
} 
.desplegar-enter-to, .desplegar-leave-from { 
    max-height: 200px; 
    opacity: 1; 
    transform: translateY(0); 
} 
/* :::::::::::::::::::: CAMPO :::::::::::::::::::: */ 
.campo { 
    width: 100%; 
    transition: all 0.3s ease; 
} 

/* :::::::::::::::::::: CONTENEDOR CURSO + BOTÓN DESCARGA :::::::::::::::::::: */
.curso-container {
  display: grid;
  grid-template-columns: auto auto;
  gap: 50px;
  align-items: start;
  margin-bottom: 10px;
  justify-content: start;
  margin-left: 140px;
}

.campos-curso-seccion {
  width: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: flex-start;
  margin-left: 20px;
  margin-top: 30px;
}

.campo-curso {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.campo-curso label {
  text-align: left;
  width: 100%;
}

.campo-seccion {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.campo-seccion label {
  text-align: left;
  width: 100%;
}

.boton-descarga-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding-top: 0px;
}

.logo-descarga {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.label-descarga {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
  text-align: center;
  line-height: 1.4;
  max-width: 200px;
}

/* :::::::::::::::::::: BOTÓN DE DESCARGA (uiverse.io) :::::::::::::::::::: */
.btn-download {
  font-family: inherit;
  font-size: 15px;
  background: linear-gradient(to bottom, #4dc7d9 0%, #66a6ff 100%);
  color: white;
  padding: 0.8em 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 25px;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s;
  text-decoration: none;
  cursor: pointer;
}

.btn-download:hover {
  transform: translateY(-3px);
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
}

.btn-download:active {
  transform: scale(0.95);
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.btn-download span {
  display: block;
  margin-left: 0.4em;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-download svg {
  width: 18px;
  height: 18px;
  fill: white;
  transition: all 0.3s;
  transform: rotate(45deg);
}

.btn-download .svg-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  margin-right: 0.5em;
  transition: all 0.3s;
}

.btn-download:hover .svg-wrapper {
  background-color: #4ba0f4;
}

.btn-download:hover svg {
  transform: rotate(135deg);
  fill: white;
}

/* :::::::::::::::::::: BOTÓN SUBIR FICHA MÉDICA :::::::::::::::::::: */
.contenedor-boton-subir {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 30px;
  margin-bottom: 20px;
}

.btn-subir-ficha {
  font-family: inherit;
  font-size: 15px;
  background: linear-gradient(to bottom, #4dc7d9 0%, #66a6ff 100%);
  color: white;
  padding: 0.8em 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 25px;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s;
  text-decoration: none;
  cursor: pointer;
}

.btn-subir-ficha:hover {
  transform: translateY(-3px);
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
}

.btn-subir-ficha:active {
  transform: scale(0.95);
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.btn-subir-ficha span {
  display: block;
  margin-left: 0.4em;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-subir-ficha svg {
  width: 18px;
  height: 18px;
  fill: white;
  transition: all 0.3s;
  transform: rotate(45deg); /* Inicialmente apunta hacia la derecha (al texto) */
}

.btn-subir-ficha .svg-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  margin-right: 0.5em;
  transition: all 0.3s;
}

.btn-subir-ficha:hover .svg-wrapper {
  background-color: #4ba0f4;
}

.btn-subir-ficha:hover svg {
  transform: rotate(-45deg); /* Al hacer hover gira hacia arriba */
  fill: white;
}

.archivo-seleccionado {
  font-size: 13px;
  color: #4ade80;
  font-weight: 500;
  text-align: center;
  margin-top: 5px;
}

/* :::::::::::::::::::: BOTONES :::::::::::::::::::: */ 
  .btn-enviar {
    margin-top: 20px;
    position: relative;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-width: 140px;
    padding: 15px 30px;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1;
    color: #fff;
    text-decoration: none;
    background-color: #4facfe;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    box-shadow: 0 10px 20px rgba(79, 172, 254, 0.4);
  }

  .btn-enviar::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50px;
    padding: 3px;
    background: linear-gradient(135deg, #00f5ff, #4facfe, #00a4ff);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.3s;
  }

  .btn-enviar:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(79, 172, 254, 0.6);
    background-color: #00a4ff;
  }

  .btn-enviar:hover::before {
    opacity: 1;
  }

  .btn-enviar:active {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.5);
  } 
/*:::::::::::::::::::::::::::::::::::::::::::::::::::::::*/
  .btn-vaciar {
    margin-top: 20px;
    position: relative;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-width: 140px;
    padding: 15px 30px;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1;
    color: #fff;
    text-decoration: none;
    background-color: #10b981;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4);
  }

  .btn-vaciar::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50px;
    padding: 3px;
    background: linear-gradient(135deg, #34d399, #10b981, #059669);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.3s;
  }

  .btn-vaciar:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(16, 185, 129, 0.6);
    background-color: #059669;
  }

  .btn-vaciar:hover::before {
    opacity: 1;
  }

  .btn-vaciar:active {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 5px 15px rgba(16, 185, 129, 0.5);
  }

/* Religión styles removed */

/* :::::::::: RADIO / CHECKBOX :::::::::: */
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin: 15px 0 25px;
  perspective: 1000px;
}

.checkbox-group label {
  font-weight: 500;
  background-color: #fff;
  padding: 10px 16px;
  border-radius: 10px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  user-select: none;
}

.checkbox-group input[type="radio"] {
  margin-right: 8px;
  transform: scale(1.1);
  accent-color: #3b82f6;
  transition: transform 0.2s ease;
}

.checkbox-group label:hover {
  background-color: #f1f5f9;
  border-color: #3b82f6;
  transform: translateY(-2px) rotateX(5deg);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.15);
}

.checkbox-group input[type="radio"]:checked + label {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #1e40af;
  transform: scale(1.02);
}

/* :::::::::: TRANSICIÓN :::::::::: */
.desplegar-enter-active {
  animation: slide-fade-in 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.desplegar-leave-active {
  animation: slide-fade-out 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slide-fade-in {
  from {
    opacity: 0;
    transform: translateY(-15px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes slide-fade-out {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-15px) scale(0.95);
  }
}




</style>





