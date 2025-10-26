<template>
  <div class="formulario">  
    <h1>FORMULARIO DE REGISTRO</h1>

    <form>
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Datos Personales         ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->

  <!--::::::::::::::::::::::::::::::::::CURSO DE PARTICIPACIÓN::::::::::::::::::::::::::::::::::::::::-->
    <div class="seleccioneCurso"></div> <!-- Titulo Eleccion de Cursos-->
          <h2>Seleccione Curso</h2>

    <label for="curso">¿En qué curso participará?</label>
    <select id="curso" v-model="cursoSeleccionado" required>
      <option disabled value="">Seleccione un curso</option>
      <option value="liderazgoJuvenil">Curso de Liderazgo Juvenil</option>
      <option value="primerosAuxilios">Curso de Primeros Auxilios en Campamento</option>
      <option value="gestionAmbiental">Curso de Gestión Ambiental Scout</option>
    </select>

      <div class="datosPersonales"></div> <!-- titulo Datos Personales-->
          <h2>Datos Personales</h2>
  <!-- :::::::::::::::::: INPUTS BÁSICOS ::::::::::::::::::::::::: -->
        <InputBase v-model="nombre" label="Nombre Completo:" type="text" placeholder="nombre completo" />
        <InputBase v-model="rut" label="RUT:" type="text" placeholder="XXXXXXXX-X" rules="rut" />
        <InputBase v-model="fechaNacimiento" label="Fecha de Nacimiento:" type="date" />
  <!--::::::::::::::::::: NUMERO DE CELULAR CON +569:::::::::::::::::::::::::-->
              <label for="numeroCelular">Número de Celular:</label>
      <div style="display: flex; align-items: center; gap: 6px;">
        <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+569</span>
        <input
          id="numeroCelular"
          v-model="numeroCelular"
          type="tel"
          placeholder="97643210"
          maxlength="8"
        />
      </div>
        <InputBase v-model="email" label="Correo Electrónico:" type="email" placeholder="Ingrese EMAIL" />
        <InputBase v-model="edad" label="Edad" type="number" placeholder="Ingrese su edad" min="0" max="120"/>

<!-- :::::::::::::::::: SELECTOR DE REGIONES ::::::::::::::::::::::::: -->
<label for="region">Región:</label>
<select id="region" v-model="regionSeleccionada">
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
      <InputBase v-model="direccion" label="Dirección:" type="text" placeholder="Ingrese Dirección" />

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

  <!-- :::::::::::::::::: SELECTOR DE RELIGIÓN ::::::::::::::::::::::::: --> 
        <label for="religion">Religión:</label>
        <select id="religion" v-model="religion">
          <option disabled value="">Seleccione su religión</option>
          <option value="catolica">Católica</option>
          <option value="evangelica">Evangélica / Protestante</option>
          <option value="testigos_de_jehova">Testigos de Jehová</option>
          <option value="mormona">Iglesia de Jesucristo de los Santos de los Últimos Días (Mormona)</option>
          <option value="adventista">Adventista del Séptimo Día</option>
          <option value="judia">Judía</option>
          <option value="islamica">Islámica</option>
          <option value="budista">Budista</option>
          <option value="agnostica">Agnóstica</option>
          <option value="atea">Atea</option>
          <option value="otra">Otra</option>
        </select>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::              Datos Scout            ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
    <div class="datosScout"></div> <!-- titulo Datos Scout-->
          <h2>Datos Scout</h2>
  <!-- :::::::::::::::::: INPUT APODO CREDENCIAL ::::::::::::::::::::::::: -->
      <label for="profesion">Apodo para Credencial:</label>
      <input
        id="apodoCredencial"
        v-model="apodoCredencial"
        type="text"
        placeholder="Ingrese su apodo o nombre para credencial"
        maxlength="50"
        @input="profesion = profesion.toUpperCase()"
      />

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
                      <label for="rolOtro">Especifique su rol:</label>
                      <textarea
                        id="rolOtro"
                        v-model="rolOtro"
                        placeholder="Ingrese su rol aquí..."
                        rows="3"
                        maxlength="100"
                        :disabled="rolSeleccionado !== 'otro'"
                      ></textarea>

  <!-- :::::::::::::::::: SELECTOR DE GRUPO ::::::::::::::::::::::::: -->
        <label for="grupo">Grupo al que pertenece:</label>
        <select id="grupo" v-model="grupoSeleccionado">
          <option disabled value="">Seleccione su grupo</option>
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
                            <label for="grupoOtro">Ingrese el nombre del grupo:</label>
                            <textarea
                              id="grupoOtro"
                              v-model="grupoOtro"
                              placeholder="Escriba el nombre de su grupo..."
                              rows="3"
                              maxlength="100"
                              :disabled="grupoSeleccionado !== 'otro'"
                            ></textarea>

      <!-- :::::::::::::::::: SELECTOR DE RAMA / SECCIÓN ::::::::::::::::::::::::: -->
      <label for="rama">Rama o sección a la que pertenece:</label>
      <select id="rama" v-model="ramaSeleccionada">
        <option disabled value="">Seleccione su rama</option>
        <option value="Lobatos">Lobatos</option>
        <option value="Golondrinas">Golondrinas</option>
        <option value="Guias">Guías</option>
        <option value="Scouts">Scouts</option>
        <option value="Pioneros">Pioneros</option>
        <option value="Caminantes">Caminantes</option>
      </select>

    <!-- :::::::::::::::::: INPUT DE CARGO EN LA UNIDAD ::::::::::::::::::::::::: -->
      <label for="cargo">¿Qué cargo tienes en tu Unidad?</label>
      <select id="cargo" v-model="opcionCargo">
        <option disabled value="">Seleccione una opción</option>
        <option value="escribir">Sí</option>
        <option value="ninguno">No</option>
      </select>

      <label for="cargoTexto">Escriba su cargo:</label>
      <input
        id="cargoTexto"
        type="text"
        v-model="cargoTexto"
        placeholder="Ingrese su cargo..."
        maxlength="50"
        :disabled="opcionCargo !== 'escribir'"
      />

  <!-- :::::::::::::::::: INPUT TIEMPO EN LA UNIDAD ::::::::::::::::::::::::: -->
    <label for="tiempoUnidad">¿Cuánto tiempo lleva en su unidad?</label>
    <div style="display: flex; gap: 10px; align-items: center;">
      <!-- AÑOS -->
      <select id="años" v-model="añosUnidad" style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;">
        <option disabled value="">Años</option>
        <option v-for="n in 20" :key="n" :value="n">{{ n }} año{{ n > 1 ? 's' : '' }}</option>
      </select>

      <!-- MESES -->
      <select id="meses" v-model="mesesUnidad" style="padding: 8px; border-radius: 6px; border: 1px solid #ccc;">
        <option disabled value="">Meses</option>
        <option v-for="m in 11" :key="m" :value="m">{{ m }} mes{{ m > 1 ? 'es' : '' }}</option>
      </select>
    </div>

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
                      <label for="distritoOtro">Ingrese el nombre del Distrito:</label>
                      <textarea
                        id="distritoOtro"
                        v-model="distritoOtro"
                        placeholder="Escriba el nombre de su Distrito..."
                        rows="3"
                        maxlength="100"
                        :disabled="distritoSeleccionado !== 'Otro'"
                      ></textarea>
  
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
      <label for="ramaMedio">¿En qué rama tienes ese nivel? (solo si tu nivel es Medio)</label>
      <select
        id="ramaMedio"
        v-model="ramaMedioSeleccionada"
        :disabled="nivelSeleccionado !== 'Medio'"
      >
        <option disabled value="">Seleccione la rama</option>
        <option value="Lobatos">Lobatos</option>
        <option value="Golondrinas">Golondrinas</option>
        <option value="Guías">Guías</option>
        <option value="Scouts">Scouts</option>
        <option value="Pioneros">Pioneros</option>
        <option value="Caminantes">Caminantes</option>
        <option value="Ninguno">Ninguno</option>
      </select>

  <!--::::::::::::::::::::::SELECTOR RAMA PARA NIVEL AVANZADO:::::::::::::::::::::::::::::::::::::::::::::::-->
      <label for="ramaAvanzado">¿En qué rama tienes ese nivel? (solo si tu nivel es Avanzado)</label>
      <select
        id="ramaAvanzado"
        v-model="ramaAvanzadoSeleccionada"
        :disabled="nivelSeleccionado !== 'Avanzado'"
      >
        <option disabled value="">Seleccione la rama</option>
        <option value="Lobatos">Lobatos</option>
        <option value="Golondrinas">Golondrinas</option>
        <option value="Guías">Guías</option>
        <option value="Scouts">Scouts</option>
        <option value="Pioneros">Pioneros</option>
        <option value="Caminantes">Caminantes</option>
        <option value="Ninguno">Ninguno</option>
      </select>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Salud y Logistica        ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
      <div class="saludLogistica"></div> <!-- Salud y Logistica-->
          <h2>Salud y Logistica</h2>
  <!--::::::::::::::::::: INPUT DE ALERGIAS/ENFERMEDADES ::::::::::::::::::::::::: -->
      <label for="salud">¿Tiene alergias o alguna enfermedad a considerar?</label>
      <select id="salud" v-model="tieneAlergiaEnfermedad">
        <option disabled value="">Seleccione una opción</option>
        <option value="si">Sí</option>
        <option value="no">No</option>
      </select>

  <!--:::::::::::::::: TEXT AREA BLOQUEADO POR DEFECTO, SE HABILITA AL SELECCIONAR "si" :::::::::::::::::::::::::::::::::-->
                            <label for="detalleSalud">Detalle de alergias o enfermedades:</label>
                            <textarea
                                id="detalleSalud"
                                v-model="detalleAlergiaEnfermedad"
                                placeholder="Ingrese la alergia o enfermedad"
                                rows="4"
                                maxlength="200"
                              :disabled="tieneAlergiaEnfermedad !== 'si'"
                            ></textarea>

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

      <label for="numeroEmergencia">Número de contacto de emergencia:</label>
      <div style="display: flex; align-items: center; gap: 6px;">
        <span style="background-color: #f2f2f2; padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px;">+569</span>
        <input
          id="numeroEmergencia"
          v-model="numeroEmergencia"
          type="tel"
          placeholder="97643210"
          maxlength="8"
        />
      </div>

  <!--::::::::::::::::::::::VEHÍCULO PROPIO:::::::::::::::::::::::::::::::::::::::::::::::-->
    <label for="vehiculoPropio">¿Viene en vehículo propio?</label>
    <select id="vehiculoPropio" v-model="vehiculoPropio" required>
      <option disabled value="">Seleccione una opción</option>
      <option value="si">Sí</option>
      <option value="no">No</option>
    </select>
  <!--::::::::::::::::::::::CAMPOS SOLO SI SELECCIONA "SI" AL VAHICULO PROPIO:::::::::::::::::::::::::::::::::::::::::::::::-->
                              <label for="patentePropia">Patente del vehículo (formato: AB-CD-12)</label>
                              <input
                                id="patentePropia"
                                v-model="patentePropia"
                                type="text"
                                placeholder="Ej: AB-CD-12"
                                maxlength="8"
                                @input="validarPatentePropia"
                                :disabled="vehiculoPropio !== 'si'"
                              />

                              <label for="marcaPropia">Marca del vehículo:</label>
                              <input
                                id="marcaPropia"
                                v-model="marcaPropia"
                                type="text"
                                placeholder="Ej: Toyota"
                                :disabled="vehiculoPropio !== 'si'"
                              />

                              <label for="modeloPropio">Modelo del vehículo:</label>
                              <input
                                id="modeloPropio"
                                v-model="modeloPropio"
                                type="text"
                                placeholder="Ej: Yaris"
                                :disabled="vehiculoPropio !== 'si'"
                              />

  <!-- :::::::::::::::::: SELECTOR DE ALOJAMIENTO ::::::::::::::::::::::::: -->
            <label for="alojamiento">¿Necesita alojamiento?</label>
            <select id="alojamiento" v-model="necesitaAlojamiento">
              <option disabled value="">Seleccione una opción</option>
              <option value="si">Sí</option>
              <option value="no">No</option>
            </select>
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::          Informacion Adicional      ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
      <div class="informacionAdicional"></div> <!-- Titulo Informacion Adicional-->
          <h2>Informacion Adicional</h2>
  <!-- :::::::::::::::::: INPUT TEXT AREA DE CONSIDERACIONES ::::::::::::::::::::::::: -->
        <label for="consideraciones">Consideraciones:</label>
        <textarea            id="consideraciones"
          v-model="consideraciones"
          placeholder="Ingrese cualquier comentario o consideración"
          rows="4"
          maxlength="200"
        ></textarea>

  <!-- :::::::::::::::::: INPUT DE PROFESIÓN ::::::::::::::::::::::::: -->
      <label for="profesion">Profesión:</label>
      <input
        id="profesion"
        v-model="profesion"
        type="text"
        placeholder="Ingrese su profesión"
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

  <!--::::::::::::::::::::::BENEFICIARIO:::::::::::::::::::::::::::::::::::::::::::::::-->
    <label for="beneficiario">¿Eres o fuiste beneficiario?</label>
    <select id="beneficiario" v-model="esBeneficiario" required>
      <option disabled value="">Seleccione una opción</option>
      <option value="si">Sí</option>
      <option value="no">No</option>
    </select>

                      <!-- Input para el tiempo si selecciona "Sí" -->
                      <label for="tiempoBeneficiario">¿Por cuánto tiempo?</label>
                      <input
                        id="tiempoBeneficiario"
                        v-model="tiempoBeneficiario"
                        type="text"
                        placeholder="Ingrese el tiempo"
                        :disabled="esBeneficiario !== 'si'"
                      />
  
  <!--::::::::::::::::::::::MIEMBRO ACTIVO:::::::::::::::::::::::::::::::::::::::::::::::-->
      <label for="miembroActivo">¿Es un miembro activo?</label>
      <select id="miembroActivo" v-model="esMiembroActivo" required>
        <option disabled value="">Seleccione una opción</option>
        <option value="si">Sí</option>
        <option value="no">No</option>
      </select>



    </form>
  </div>
</template>



<script setup>
import { ref, computed } from 'vue';
import InputBase from '@/components/Reutilizables/InputBase.vue';


// :::::::::::::::::: VARIABLES PARA CAPTURAR VALORES :::::::::::::::::::::::::

const nombre = ref("");
const rut = ref("");
const fechaNacimiento = ref("");
const numeroCelular = ref("");
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
const haTrabajadoConNinos = ref("");
const esBeneficiario = ref("");
const tiempoBeneficiario = ref("");
const esMiembroActivo = ref("");
const patenteVehiculo = ref("");
const vehiculoPropio = ref("");
const patentePropia = ref("");
const marcaPropia = ref("");
const modeloPropio = ref("");
const cursoSeleccionado = ref("");


// REGION / CIUDAD / COMUNA
const regionSeleccionada = ref("");
const ciudadSeleccionada = ref("");
const comunaSeleccionada = ref("");

// Validación del formato de patente chilena (ej: AB-CD-12)
function validarPatente() {
  // Permite formato: AA-BB-11 o AB-CD-12 o similar
  const formato = /^[A-Z]{2}-[A-Z]{2}-\d{2}$/;
  if (patenteVehiculo.value && !formato.test(patenteVehiculo.value.toUpperCase())) {
    patenteVehiculo.value = patenteVehiculo.value
      .toUpperCase()
      .replace(/[^A-Z0-9-]/g, ""); // limpia caracteres no válidos
  }
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




<style scoped>

* {
  font-family: "Calibri", sans-serif;
}



.formulario {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centra verticalmente */
  align-items: center;     /* Centra horizontalmente */
  min-height: 100vh;       /* Ocupa todo el alto de la ventana */
  background-color: #f5f5f5; /* (Opcional) fondo suave */
}

textarea {
  resize: none;           /* desactiva el cambio de tamaño con el mouse */
  height: 100px;          /* ||alto fijo (puedes ajustar a tu gusto) */
  width: 100%;            /* asegura que ocupe todo el ancho del contenedor */
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

.formulario :deep(input),
.formulario :deep(select),
.formulario :deep(textarea) {
  padding: 10px 5px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;   /* Tamaño de fuente legible dentro de los inputs */
  background-color: #f9f9f9;
  color: #333;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.formulario :deep(input:focus),
.formulario :deep(select:focus),
.formulario :deep(textarea:focus) {
  /*border-color: #3079f0;*/

  box-shadow: 0 0 4px rgba(2, 145, 255, 0.925);
  outline: none;
}

.formulario :deep(label) {
  font-weight: 600;
  color: #444;
  margin-bottom: 5px;
  display: inline-block;
}


form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 400px;          /* Controla el ancho del formulario */
  background: rgb(255, 255, 255);         /* Opcional: fondo blanco */
  padding: 50px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(34, 24, 232, 0.1);
  border: 2px solid #ffffff;   /* Borde azul claro */
}

h1 {
text-align: left; 
font-family: "Calibri", sans-serif; 
font-weight: bold; font-size: 30px; 
background: #202020; 
-webkit-background-clip: text; 
-moz-background-clip: text; 
background-clip: text; 
color: transparent; 
}

input, select, textarea {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 100%;
  box-sizing: border-box;  /* Asegura que padding no rompa el ancho */
  font-size: 14px;
  font-weight: 500;
  color: #333;
  transition: all 0.2s ease;
}

/* Efecto al enfocar (hover o focus) */
input:focus, select:focus, textarea:focus {
  border-color: #4CAF50;         /* Verde suave */
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
  outline: none;
}

/* Placeholder más suave */
::placeholder {
  color: #999;
}

/* :::::::::::::::::::: EFECTO DESPLEGABLE :::::::::::::::::::: */
.desplegar-enter-active,
.desplegar-leave-active {
  transition: all 0.4s ease;
  overflow: hidden;
}

.desplegar-enter-from,
.desplegar-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.desplegar-enter-to,
.desplegar-leave-from {
  max-height: 200px;
  opacity: 1;
  transform: translateY(0);
}

/* :::::::::::::::::::: CAMPO :::::::::::::::::::: */
.campo {
  width: 100%;
  transition: all 0.3s ease;
}




</style>
