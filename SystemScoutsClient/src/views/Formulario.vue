<template>
  <div class="formulario"> 
    <form>
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Datos Personales         ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  
  <!--::::::::::::::::::::::::::::::::::CURSO DE PARTICIPACIÓN::::::::::::::::::::::::::::::::::::::::-->
  <section>
    <div class="seleccioneCurso"></div> <!-- Titulo Eleccion de Cursos-->
          <h2>Seleccione Curso</h2>

    <label for="curso">¿En qué curso participará?</label>
    <select id="curso" v-model="cursoSeleccionado" required @change="handleCursoChange">
      <option value="">Seleccione un curso</option>
      <option value="liderazgoJuvenil">Curso de Liderazgo Juvenil</option>
      <option value="primerosAuxilios">Curso de Primeros Auxilios en Campamento</option>
      <option value="gestionAmbiental">Curso de Gestión Ambiental Scout</option>
    </select>

    <transition name="desplegar">
              <div v-if="cursoSeleccionado" class="campo">
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

  </section>
<!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <transition name="fade">
    <div v-if="cursoSeleccionado && seccionCurso" class="resto-formulario">
      <section>
              <h2>Datos Personales</h2>
  <!-- :::::::::::::::::: INPUTS BÁSICOS ::::::::::::::::::::::::: -->
        <InputBase v-model="nombre" label="Nombres:" type="text" placeholder="PRIMER Y SEGUNDO NOMBRE" />
        <InputBase v-model="apellidoMaterno" label="Apellido Materno:" type="text" placeholder="APELLIDO MATERNO" />
        <InputBase v-model="apellidoPaterno" label="Apellido Paterno:" type="text" placeholder="APELLIDO PATERNO" />
        <label for="rut">RUT (sin puntos ni guion):</label>
        <input id="rut" type="text" v-model="rut" maxlength="9" placeholder="Ej: 123456789" @input="rut = rut.replace(/[^0-9]/g, '')"
              :class="{ invalido: rut.length > 0 && rut.length < 7 }" required
          />

        <InputBase v-model="fechaNacimiento" label="Fecha de Nacimiento:" type="date" />
        <InputBase v-model="email" label="Correo Electrónico:" type="email" placeholder="INGRESE EMAIL" />

  <!--::::::::::::::::::: NÚMEROS DE CONTACTO :::::::::::::::::::::::::-->
              <!-- TELÉFONO FIJO -->
              <label for="telefonoFijo">Teléfono Fijo:</label>
              <div style="display: flex; align-items: center; gap: 6px;">
                <input
                  id="telefonoFijo"
                  v-model="telefonoFijo"
                  type="tel"
                  placeholder="412345678"
                  maxlength="9"
                />
              </div>

              <!-- NÚMERO DE CELULAR -->
              <label for="numeroCelular">Número de Celular:</label>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+56</span>
                <input
                  id="numeroCelular"
                  v-model="numeroCelular"
                  type="tel"
                  placeholder="976432101"
                  maxlength="9"
                  required
                />
              </div>

              <!-- CELULAR CON WHATSAPP -->
              <label for="celularWhatsapp">Número de Celular con WhatsApp:</label>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+56</span>
                <input
                  id="celularWhatsapp"
                  v-model="celularWhatsapp"
                  type="tel"
                  placeholder="976432101"
                  maxlength="9"
                />
              </div>

              <!-- WHATSAPP ADICIONAL -->
              <label for="whatsappAdicional">WhatsApp adicional (si tiene):</label>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+56</span>
                <input
                  id="whatsappAdicional"
                  v-model="whatsappAdicional"
                  type="tel"
                  placeholder="976432101"
                  maxlength="9"
                />
              </div>

<!-- :::::::::::::::::: SELECTOR DE REGIONES ::::::::::::::::::::::::: -->
<label for="Provincia">Provincia:</label>
<select id="Provincia" v-model="regionSeleccionada">
  <option disabled value="">Seleccione una región</option>
  <option v-for="region in Object.keys(comunasPorRegion)" :key="region" :value="region">
    {{ region }}
  </option>
</select>

<!-- :::::::::::::::::: SELECTOR DE CIUDADES ::::::::::::::::::::::::: -->
<transition name="desplegar">
  <!-- SOLO se renderiza si regionSeleccionada tiene valor -->
  <div v-if="regionSeleccionada" class="campo" :key="regionSeleccionada">
    <label for="ciudad">Ciudad:</label>
    <select id="ciudad" v-model="ciudadSeleccionada">
      <option disabled value="">Seleccione una ciudad</option>
      <option v-for="ciudad in Object.keys(ciudadesDisponibles)" :key="ciudad" :value="ciudad">
        {{ ciudad }}
      </option>
    </select>
  </div>
</transition>

<!-- :::::::::::::::::: SELECTOR DE COMUNAS ::::::::::::::::::::::::: -->
<transition name="desplegar">
  <!-- SOLO se renderiza si ciudadSeleccionada tiene valor -->
  <div v-if="ciudadSeleccionada" class="campo" :key="ciudadSeleccionada">
    <label for="comuna">Comuna:</label>
    <select id="comuna" v-model="comunaSeleccionada">
      <option disabled value="">Seleccione una comuna</option>
      <option v-for="comuna in comunasDisponibles" :key="comuna" :value="comuna">
        {{ comuna }}
      </option>
    </select>
  </div>
</transition>


  <!-- :::::::::::::::::: INPUT DIRECCION ::::::::::::::::::::::::: -->
  <InputBase v-model="direccion" label="Dirección:" type="text" placeholder="INGRESE DIRECCIÓN" />

  <!-- :::::::::::::::::: SELECTOR DE ESTADO CIVIL ::::::::::::::::::::::::: -->
      <label for="estadoCivil">Estado Civil:</label>
      <select id="estadoCivil" v-model="estadoCivil">
        <option disabled value="">Seleccione su estado civil</option>
        <option value="soltero">Soltero/a</option>
        <option value="casado">Casado/a</option>
        <option value="divorciado">Divorciado/a</option>
        <option value="viudo">Viudo/a</option>
        <option value="conviviente_civil">Conviviente Civil</option>
      </select>

    <!-- :::::::::::::::::: INPUT APODO CREDENCIAL ::::::::::::::::::::::::: -->
      <label for="profesion">Apodo para Credencial:</label>
      <input
        id="apodoCredencial"
        v-model="apodoCredencial"
        type="text"
        placeholder="INGRESE SU APODO O NOMBRE PARA CREDENCIAL"
        maxlength="50"
        @input="profesion = profesion.toUpperCase()"
      />

  <!-- ::::::::::::::::::::: FOTO (Selfie o Subida) ::::::::::::::::::::: -->
<label for="foto">Sube o toma tu foto (selfie):</label>

<!-- Input para subir archivo -->
<input
  type="file"
  id="foto"
  accept="image/png, image/jpeg"
  :disabled="camaraActiva || fotoUrl"   
  @change="procesarFoto"
/>

<!-- Vista previa -->
<div v-if="fotoUrl" class="preview">
  <img :src="fotoUrl" alt="Vista previa de la foto" />
</div>

<!-- Botones -->
<div class="botones-foto">
  <button
    type="button"
    class="btn-capturar"
    @click="abrirCamara"
    :disabled="fotoSubida || fotoUrl"     
  >
    📷 Tomar foto ahora
  </button>

  <button
    v-if="fotoUrl"
    type="button"
    class="btn-eliminar"
    @click="eliminarFoto"
  >
    🗑️ Eliminar foto
  </button>
</div>

<!-- Contenedor de cámara -->
<div v-if="mostrarCamara" class="camara-container">
  
  <video ref="video" autoplay></video>
  <button type="button" class="btn-foto" @click="capturarFoto">Capturar</button>
  <canvas ref="canvas" style="display: none;"></canvas>
</div>

<!-- ::::::::::::::::::: FORMADOR ::::::::::::::::::: -->
<section class="bloque-formador">
  <label class="titulo-bloque">¿Eres Formador?</label>
  <select id="formador" v-model="esFormador" class="selector-formador">
    <option value="">Seleccione una opción</option>
    <option value="si">Sí</option>
    <option value="no">No</option>
  </select>

  <!-- ::::::::::::::::::: CAMPOS ADICIONALES ::::::::::::::::::: -->
  <transition name="desplegar">
    <div v-if="esFormador === 'si'" class="campos-formador">
      <!-- ::::::::::::::::::: TEXT AREA ::::::::::::::::::: -->
      <div class="campo">
        <label for="historialFormador">Historial de Formador:</label>
        <textarea
          id="historialFormador"
          v-model="historialFormador"
          placeholder="Describe tu experiencia o historial como formador"
          rows="5"
          maxlength="500"
        ></textarea>
      </div>

      <!-- ::::::::::::::::::: HABILIDADES ::::::::::::::::::: -->
      <div class="habilidades">
        <div class="campo">
          <label class="titulo-bloque">Habilidad 1</label>
          <select v-model="habilidad1" class="selector-habilidad">
            <option value="">Seleccione una opción</option>
            <option value="si">Sí</option>
            <option value="no">No</option>
          </select>
        </div>

        <div class="campo">
          <label class="titulo-bloque">Habilidad 2</label>
          <select v-model="habilidad2" class="selector-habilidad">
            <option value="">Seleccione una opción</option>
            <option value="si">Sí</option>
            <option value="no">No</option>
          </select>
        </div>

        <div class="campo">
          <label class="titulo-bloque">Verificado</label>
          <select v-model="verificado" class="selector-habilidad">
            <option value="">Seleccione una opción</option>
            <option value="si">Sí</option>
            <option value="no">No</option>
          </select>
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
          <h2>Informacion Asociacion</h2>


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
    <!--::::::::::::::::::::::SELECTOR DISTRITO:::::::::::::::::::::::::::::::::::::::::::::::-->
      <label for="distrito">Distrito al que pertenece:</label>
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

                      <!-- TEXTAREA QUE SE HABILITA SOLO AL ELEGIR "OTRO" -->
                    <Transition name="desplegar">
                      <div v-if="distritoSeleccionado === 'Otro'" class="campo">
                      <label for="distritoOtro">Ingrese el nombre del Distrito:</label>
                      <textarea
                        id="distritoOtro"
                        v-model="distritoOtro"
                        placeholder="ESCRIBA EL NOMBRE DE SU DISTRITO..."
                        rows="3"
                        maxlength="100"
                        :disabled="distritoSeleccionado !== 'Otro'"
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
          <h2>Salud y Logistica</h2>
  <!--::::::::::::::::::: INPUT DE ALERGIAS/ENFERMEDADES ::::::::::::::::::::::::: -->
      <label for="salud">¿Tiene alergias,enfermedad o limitacion considerar?</label>
      <select id="salud" v-model="tieneAlergiaEnfermedad">
        <option disabled value="">Seleccione una opción</option>
        <option value="Si">Sí</option>
        <option value="No">No</option>
      </select>

  <!--:::::::::::::::: TEXT AREA BLOQUEADO POR DEFECTO, SE HABILITA AL SELECCIONAR "si" :::::::::::::::::::::::::::::::::-->
                        <transition name="desplegar">
                          <div v-if="tieneAlergiaEnfermedad === 'Si'" class="campo">
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
  <!-- :::::::::::::::::: SELECTOR DE TIPO DE ALIMENTACIÓN ::::::::::::::::::::::::: -->
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

  <!--::::::::::::::::::::::CONTACTO DE EMERGENCIA:::::::::::::::::::::::::::::::::::::::::::::::-->
      <label for="nombreEmergencia">Nombre de contacto de emergencia:</label>
      <InputBase
        id="nombreEmergencia"
        v-model="nombreEmergencia"
        type="text"
        placeholder="Ej: ALAN DAVE"
      />

      <label for="numeroEmergencia">Número de celular de emergencia:</label>
      <div style="display: flex; align-items: center; gap: 6px;">
        <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+56</span>
        <input
          id="numeroEmergencia"
          v-model="numeroEmergencia"
          type="tel"
          placeholder="974643210"
          maxlength="9"
          required
        />
      </div>

      <label for="tieneNumeroFijo">¿Desea agregar un teléfono fijo de emergencia?</label>
      <select id="tieneNumeroFijo" v-model="tieneNumeroFijo">
        <option disabled value="">Seleccione una opción</option>
        <option value="si">Sí</option>
        <option value="no">No</option>
      </select>

      <transition name="desplegar">
        <div v-if="tieneNumeroFijo === 'si'" class="campo">
          <label for="numeroFijoEmergencia">Número fijo de emergencia:</label>
          <div style="display: flex; align-items: center; gap: 6px;">
            <input
              id="numeroFijoEmergencia"
              v-model="numeroFijoEmergencia"
              type="tel"
              placeholder="412345678"
              maxlength="9"
            />
          </div>
        </div>
      </transition>

<!--:::::::::::::::::::::: VEHÍCULO PROPIO :::::::::::::::::::::::::::::::::::::::::::::::::::-->
<label for="vehiculoPropio">¿Viene en vehículo propio?</label>
<select id="vehiculoPropio" v-model="vehiculoPropio" required>
  <option disabled value="">Seleccione una opción</option>
  <option value="si">Sí</option>
  <option value="no">No</option>
</select>

<!--:::::::::::::::::::::: CAMPOS SOLO SI SELECCIONA "SI" :::::::::::::::::::::::::::::::::::::::::::::::::::-->
              <transition name="desplegar">
                <div v-if="vehiculoPropio === 'si'" class="campo">
                  <label for="patentePropia">Patente del vehículo (formato: AB-CD-12)</label>
                  <input
                    id="patentePropia"
                    v-model="patentePropia"
                    type="text"
                    placeholder="Ej: AB-CD-12"
                    maxlength="8"
                    @input="validarPatentePropia"
                  />

                  <label for="marcaPropia">Marca del vehículo:</label>
                  <input
                    id="marcaPropia"
                    v-model="marcaPropia"
                    type="text"
                    placeholder="Ej: Toyota"
                  />

                  <label for="modeloPropio">Modelo del vehículo:</label>
                  <input
                    id="modeloPropio"
                    v-model="modeloPropio"
                    type="text"
                    placeholder="Ej: Yaris"
                  />
                </div>
              </transition>

  <!--:::::::::::::::::::::: ALOJAMIENTO :::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <div class="campo campo-checkbox">
  <label>
    ¿Necesita alojamiento?
    <input
      type="checkbox"
      v-model="necesitaAlojamiento"
      true-value="si"
      false-value="no"
    /> 
  </label>
  </div>
  </section>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::          Informacion Adicional      ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <section>
      <div class="informacionAdicional"></div> <!-- Titulo Informacion Adicional-->
          <h2>Informacion Adicional</h2>
  <!-- :::::::::::::::::: INPUT TEXT AREA DE OTROS ::::::::::::::::::::::::: -->
        <label for="consideraciones">Otros:</label>
        <textarea            id="consideraciones"
          v-model="consideraciones"
          placeholder="INGRESE CUALQUIER COMENTARIO O CONSIDERACIÓN"
          rows="4"
          maxlength="200"
        ></textarea>

  <!-- :::::::::::::::::: INPUT DE PROFESIÓN ::::::::::::::::::::::::: -->
      <label for="profesion">Profesión:</label>
      <input
        id="profesion"
        v-model="profesion"
        type="text"
        placeholder="INGRESE SU PROFESIÓN"
        maxlength="50"
        @input="profesion = profesion.toUpperCase()"
      />
  <!--::::::::::::::::::::::EXPERIENCIA CON NIÑOS:::::::::::::::::::::::::::::::::::::::::::::::-->
    <label for="trabajoNinos">¿Ha trabajado con niños?</label>
    <select id="trabajoNinos" v-model="haTrabajadoConNinos" required>
      <option disabled value="">Seleccione una opción</option>
      <option value="si">Sí</option>
      <option value="no">No</option>
    </select>
                <transition name="desplegar">
                  <div v-if="haTrabajadoConNinos === 'si'" class="campo">
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




<!-- ::::::::::::::::: BENEFICIARIO ::::::::::::::::: -->
<label for="beneficiario">¿Eres o fuiste beneficiario?</label>
<select id="beneficiario" v-model="esBeneficiario" required>
  <option disabled value="">Seleccione una opción</option>
  <option value="si">Sí</option>
  <option value="no">No</option>
</select>

<!-- ::::::::::::::::: CAMPO DESPLEGABLE ::::::::::::::::: -->
<transition name="desplegar">
  <div v-if="esBeneficiario === 'si'" class="campo">
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



  </section>
    </div>
  </transition>

  <!--:::::::::::::::::::::: BOTONES DE ACCIÓN ::::::::::::::::::::::::::::::::::-->
        <div class="botones-formulario" style="display: flex; justify-content: center; align-items: center; gap: 20px; width: 100%;">
          <button type="button" class="btn-vaciar" @click="limpiarFormulario">VACIAR</button>
          <button type="submit" class="btn-enviar" @click.prevent="enviarFormulario">ENVIAR</button>
        </div>
    
  <!--:::::::::::::::::::::: BOTON FLOTANTE ::::::::::::::::::::::::::::::::::-->
  <button class="btn-volver" @click="scrollArriba" title="Volver al inicio">↑</button>
</form>
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
import InputBase from '@/components/InputBase.vue';

// :::::::::::::::::: LOGICA BOTON FLOTANTE :::::::::::::::::::::::::
function scrollArriba(){
  const main = document.querySelector('main');
  main.scrollTo({
    top: 0,
    behavior: 'smooth'
  });

}



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
const zonaSeleccionada = ref("");
const otraZona = ref("");
const grupoPertenece = ref("");
const nombre = ref("");
const apellidoPaterno = ref("");
const apellidoMaterno = ref("");
const rut = ref("");
const fechaNacimiento = ref("");
const telefonoFijo = ref("");
const numeroCelular = ref("");
const celularWhatsapp = ref("");
const whatsappAdicional = ref("");
const email = ref("");
const estadoCivil = ref("");
const direccion = ref("");
const edad = ref(null);
const religion = ref("");
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

// Variables para el formador
const esFormador = ref("");
const historialFormador = ref("");
const habilidad1 = ref("");
const habilidad2 = ref("");
const verificado = ref("");



//:::::::::::::::::::::::::::::FUNCION LIMPIAR FORMULARIO (BOTON):::::::::::::::::::::::::::::::::::::::::::::::

function limpiarFormulario() {
  nombre.value = "";
  apellidoPaterno.value = "";
  apellidoMaterno.value = "";
  necesitaAlojamiento.value = "";
  rut.value = "";
  fechaNacimiento.value = "";
  telefonoFijo.value = "";
  numeroCelular.value = "";
  celularWhatsapp.value = "";
  whatsappAdicional.value = "";
  email.value = "";
  estadoCivil.value = "";
  direccion.value = "";
  edad.value = null;
  religion.value = "";
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
/* ::::::::::::::::::: FORMADOR ::::::::::::::::::: */
.bloque-formador {
  margin-top: 25px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  text-align: center;
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
.selector-habilidad:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
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

  /* Estilos para el botón flotante que en template tiene la clase `btn-volver` */
  .btn-volver {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background: linear-gradient(135deg, #8e04e9);
    color: #fff;
    border: none;
    border-radius: 50%;
    width: 55px;
    height: 55px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(21, 101, 192, 0.4);
    transition: all 0.3s ease;
    z-index: 9999;
    scroll-padding-top: 29px;
  }

  .btn-volver:hover {
    background: linear-gradient(135deg, #1e88e5, #42a5f5);
    transform: translateY(-4px);
    box-shadow: 0 6px 14px rgba(30, 136, 229, 0.5);
  }

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
.btn-eliminar {
  padding: 10px 15px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
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

/* :::::::::::::::::::: CONTENEDOR DE CÁMARA :::::::::::::::::::: */
.camara-container {
  display: flex;
  flex-direction: column;
  align-items: center;         /* Centra horizontalmente */
  justify-content: center;     /* Centra verticalmente */
  margin-top: 20px;
  gap: 10px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;            /* Mantiene proporción del formulario */
  box-sizing: border-box;
}

/* :::::::::::::::::::: VIDEO DE CÁMARA :::::::::::::::::::: */
.camara-container video {
  width: 100%;
  height: 280px;
  max-width: 350px;
  border-radius: 10px;
  border: 2px solid #2196f3;
  object-fit: cover;           /* Evita deformación */
  background-color: #000;      /* Fondo oscuro mientras carga */
}


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

form { 
    display: flex; 
    flex-direction: column; 
    gap: 10px; 
    width: 100%; 
    max-width: 600px; /* Aumentado el ancho máximo del formulario */ 
    background: rgb(255, 255, 255); /* Opcional: fondo blanco */ 
    padding: 70px; 
    border-radius: 10px; 
    box-shadow: 0 0 10px rgba(34, 24, 232, 0.1); 
    border: 2px solid #1135a1; /* Borde azul claro */ 
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
/* :::::::::::::::::::: BOTONES :::::::::::::::::::: */ 
  .btn-enviar {
  margin-top: 20px;
  display: inline-block;
  justify-content: center;
  align-items: center;
  width: 180px;
  height: 45px;
  border-radius: 10px;
  border: 1px solid black;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease-in;
  z-index: 1;
  font-weight: bold;
  
  }

  .btn-enviar::before,
  .btn-enviar::after {
  content: '';
  position: absolute;
  top: 0;
  width: 0;
  height: 100%;
  transform: skew(15deg);
  transition: all 0.5s;
  overflow: hidden;
  z-index: -1;
  }

  .btn-enviar::before {
  left: -10px;
  background: #0ca5e6;
  }

  .btn-enviar::after {
  right: -10px;
  background: #0ca5e6;
  }

  .btn-enviar:hover::before,
  .btn-enviar:hover::after {
  width: 58%;
  }
/*:::::::::::::::::::::::::::::::::::::::::::::::::::::::*/
  .btn-vaciar {
  margin-top: 20px;
  display: inline-block;
  justify-content: center;
  align-items: center;
  width: 180px;
  height: 45px;
  border-radius: 10px;
  border: 1px solid black;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease-in;
  z-index: 1;
  font-weight: bold;
  }

  .btn-vaciar::before,
  .btn-vaciar::after {
  content: '';
  position: absolute;
  top: 0;
  width: 0;
  height: 100%;
  transform: skew(15deg);
  transition: all 0.5s;
  overflow: hidden;
  z-index: -1;
  }

  .btn-vaciar::before {
  left: -10px;
  background: #5ac392;
  }

  .btn-vaciar::after {
  right: -10px;
  background: #5ac392;
  }

  .btn-vaciar:hover::before,
  .btn-vaciar:hover::after {
  width: 58%;
  }



</style>





