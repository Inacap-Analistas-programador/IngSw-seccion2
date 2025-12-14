<template>
  <div class="formulario">
    <div class="form-outer">
      <form class="form-inner">
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Datos Personales         ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  
    <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::CURSO DE PARTICIPACIÓN::::::::::::::::::::::::::::::::::::::::-->
  <section>
    <div class="seleccioneCurso"></div> <!-- Titulo Eleccion de Cursos-->
          <h2 class="titulo-seleccion-curso">Selección de Curso</h2>

    <div class="curso-root-container">
      <!-- Left Column: Inputs -->
      <div class="curso-inputs-column">
        <div class="campo" style="margin-bottom: 20px;">
          <label for="curso">¿En qué curso participará?</label>
          <select id="curso" v-model="cursoSeleccionado" required @change="handleCursoChange">
            <option value="" disabled selected hidden>Seleccione un curso</option>
            <option v-for="curso in listaCursosApi" :key="curso.cur_id" :value="curso.cur_id">
              {{ curso.cur_descripcion }}
            </option>
          </select>
        </div>

        <transition name="desplegar">
          <div v-if="cursoSeleccionado" class="campo">
            <label for="seccionCurso">Selecciona sección <span style="color: red;">*</span></label>
            <select
              id="seccionCurso"
              v-model="seccionCurso"
              required
              @change="handleSeccionChange"
            >
              <option value="" disabled selected hidden>Seleccione una sección</option>
              <option v-for="seccion in listaSeccionesApi" :key="seccion.cus_id" :value="seccion.cus_id">
                {{ seccion.sec_descripcion }}
              </option>
            </select>
          </div>
        </transition>
      </div>

      <!-- Right Column: Download -->
      <div class="boton-descarga-container">
        <img src="/favicon.ico" alt="Logo Scout" class="logo-descarga" />
        <div class="label-descarga">
          <p class="label-principal">Descarga y rellena tu ficha médica</p>
          <p class="label-secundario">¡Te la pediremos más adelante!</p>
        </div>
        <BaseButton 
          variant="primary" 
          @click="descargarFicha"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Descargar Ficha
        </BaseButton>
      </div>
    </div>

  </section>


<!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <transition name="fade">
    <div v-if="cursoSeleccionado && seccionCurso" class="resto-formulario">
      
      <!-- Navegación flotante -->
      <nav class="nav-flotante">
        <a href="#top-formulario" class="nav-item nav-logo" @click.prevent="scrollToTop">
            <img src="/favicon.ico" alt="Logo Scout" class="nav-logo-img" />
        </a>
        <a href="#seccion-1" class="nav-item" @click.prevent="scrollToSection(1)">
          <span class="nav-numero">1</span>
        </a>
        <a href="#seccion-2" class="nav-item" @click.prevent="scrollToSection(2)">
          <span class="nav-numero">2</span>
        </a>
        <a href="#seccion-3" class="nav-item" @click.prevent="scrollToSection(3)">
          <span class="nav-numero">3</span>
        </a>
        <a href="#seccion-4" class="nav-item" @click.prevent="scrollToSection(4)">
          <span class="nav-numero">4</span>
        </a>
      </nav>

      <div id="seccion-1" class="inicio-linea-verde">
        <span class="numero-seccion">1</span>
      </div>
      <section>
              <div class="section-header">
                <h2>Datos Personales</h2>
                <div class="section-subtitle"></div>
              </div>
  <!-- :::::::::::::::::: INPUTS BÁSICOS ::::::::::::::::::::::::: -->
        <div class="section-grid">
          <div class="campo">
            <label for="nombre">Nombres:</label>
            <input id="nombre" v-model="nombre" type="text" placeholder="Primer y segundo nombre" />
          </div>
          <div class="campo">
            <label for="apellidoPaterno">Apellido Paterno:</label>
            <input id="apellidoPaterno" v-model="apellidoPaterno" type="text" placeholder="Apellido paterno" />
          </div>
        </div>

        <div class="section-grid">
          <div class="campo">
            <label for="apellidoMaterno">Apellido Materno:</label>
            <input id="apellidoMaterno" v-model="apellidoMaterno" type="text" placeholder="Apellido materno" />
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
            <input id="email" v-model="email" type="email" placeholder="Ingrese email" />
          </div>
        </div>

<!-- :::::::::::::::::: SELECTOR DE REGIONES Y DIRECCIÓN (agrupados) ::::::::::::::::::::::::: -->
<div class="section-grid">
  <div class="campo">
    <label for="Region">Región:</label>
    <select id="Region" v-model="regionSeleccionada">
      <option disabled value="">Seleccione una región</option>
      <option v-for="reg in listaRegionApi" :key="reg.reg_id" :value="reg.reg_id">
        {{ reg.reg_descripcion }}
      </option>
    </select>
  </div>
</div>
<div class="section-grid">
  <div class="campo">
    <label for="Provincia">Provincia:</label>
    <select id="Provincia" v-model="provinciaSeleccionada" :disabled="!regionSeleccionada">
      <option disabled value="">Seleccione una provincia</option>
      <option v-for="prov in listaProvinciaApi" :key="prov.pro_id" :value="prov.pro_id">
        {{ prov.pro_descripcion }}
      </option>
    </select>
  </div>

  <div class="campo">
    <label for="direccion">Dirección:</label>
    <input id="direccion" v-model="direccion" type="text" placeholder="Ingrese dirección" />
  </div>
</div>

<!-- Agrupamos Ciudad / Comuna / Distrito en una fila de 3 columnas -->
<transition name="desplegar">
  <div v-if="provinciaSeleccionada" class="section-grid-3" :key="provinciaSeleccionada">


    <div class="campo">
      <label for="comuna">Comuna:</label>
      <select id="comuna" v-model="comunaSeleccionada" :disabled="!provinciaSeleccionada">
        <option disabled value="">Seleccione una comuna</option>
        <option v-for="comuna in listaComunaApi" :key="comuna.com_id" :value="comuna.com_id">
          {{ comuna.com_descripcion }}
        </option>
      </select>
    </div>


  </div>
</transition>

<!-- :::::::::::::::::: SELECTOR DE ESTADO CIVIL Y APODO ::::::::::::::::::::::::: -->
      <div class="section-grid">
        <div class="campo">
          <label for="estadoCivil">Estado Civil:</label>
          <select id="estadoCivil" v-model="estadoCivil">
            <option disabled value="">Seleccione su estado civil</option>
            <option v-for="item in listaEstadoCivilApi" :key="item.esc_id" :value="item.esc_id">
              {{ item.esc_descripcion }}
            </option>
          </select>
        </div>

        <div class="campo">
          <label for="profesion">Apodo para Credencial:</label>
          <input
            id="apodoCredencial"
            v-model="apodoCredencial"
            type="text"
            placeholder="Ingrese su apodo o nombre para credencial"
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
          <input id="religion" v-model="religion" type="text" placeholder="Ingrese su religión" />
        </div>
      </div>

  <!-- ::::::::::::::::::::: FOTO (Selfie o Subida) ::::::::::::::::::::: -->
<!-- Input para subir archivo oculto y botones de captura agrupados -->
<div class="foto-section-centered">
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

<!-- ::::::::::::::::::: FORMADOR ::::::::::::::::::: -->
<div class="bloque-formador">
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
      <!-- Checkboxes en horizontal centrados -->
      <div class="checkbox-list-horizontal">
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
  </transition>
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

</section>

<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--:::::::::::::::::::::::::          INFORMACION ASOCIACION       ::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
<!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <div id="seccion-2" class="inicio-linea-verde">
    <span class="numero-seccion">2</span>
  </div>
  <section>
    <div class="datosScout"></div> <!-- TITULO iNFORMACVION ACOCIACION-->
          <div class="section-header">
            <h2>Informacion Asociacion</h2>
            <div class="section-subtitle"></div>
          </div>

  <div class="section-grid">
  <!-- :::::::::::::::::: SELECTOR DE ZONA ::::::::::::::::::::::::: -->
    <div class="campo">
        <label for="grupo">Zona al que pertenece:</label>
        <select id="grupo" v-model="zonaSeleccionada" @change="handleZonaChange">
          <option disabled value="">Seleccione su zona</option>
          <option v-for="zona in listaZonaApi" :key="zona.zon_id" :value="zona.zon_id">
              {{ zona.zon_descripcion }}
          </option>
        </select>

    <!--:::::::::::::: TEXTAREA QUE SE HABILITA SOLO AL ELEGIR "OTRO"::::::::::::::::::::: -->
                          <Transition name="desplegar">
                            <div v-if="zonaSeleccionada === 'otro'" class="campo">
                            <label for="otraZona">Ingrese el nombre de la zona:</label>
                            <textarea
                              id="otraZona"
                              v-model="otraZona"
                              placeholder="Escriba el nombre de la zona..."
                              rows="3"
                              maxlength="100"
                            ></textarea>
                            </div>
                          </Transition>
    </div>

      <!-- :::::::::::::::::: DISTRITO ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="distrito">Distrito:</label>
        <select id="distrito" v-model="distritoSeleccionado" :disabled="!zonaSeleccionada">
          <option disabled value="">Seleccione su distrito</option>
          <option v-for="dist in listaDistritoApi" :key="dist.dis_id" :value="dist.dis_id">
            {{ dist.dis_descripcion }}
          </option>
        </select>
    </div>

      <!-- :::::::::::::::::: GRUPO AL QUE PERTENECE ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="rama">Grupo al que pertenece:</label>
      <select id="rama" v-model="grupoPertenece" :disabled="!distritoSeleccionado">
        <option disabled value="">Seleccione su grupo</option>
        <option v-for="grupo in listaGrupoApi" :key="grupo.gru_id" :value="grupo.gru_id">
          {{ grupo.gru_descripcion }}
        </option>
      </select>
    </div>
  </div>

  <div class="section-grid">
  <!-- :::::::::::::::::: SELECTOR DE ROL EN EL CURSO ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="rol">Rol en el curso:</label>
      <select id="rol" v-model="rolSeleccionado">
        <option disabled value="">Seleccione su rol</option>
        <option v-for="rol in listaRolApi" :key="rol.rol_id" :value="rol.rol_id">
            {{ rol.rol_descripcion }}
        </option>
      </select>

  <!-- TEXTAREA BLOQUEADO POR DEFECTO, SE HABILITA SI ELIGE "OTRO" -->
                    <Transition name="desplegar">
                      <div v-if="rolSeleccionado === 'otro'" class="campo">
                      <label for="rolOtro">Especifique su rol:</label>
                      <textarea
                        id="rolOtro"
                        v-model="rolOtro"
                        placeholder="Ingrese su rol aquí..."
                        rows="3"
                        maxlength="100"
                        :disabled="rolSeleccionado !== 'otro'"
                      ></textarea>
                      </div>
                    </Transition>
    </div>

  <!-- :::::::::::::::::: SELECTOR DE NIVEL ::::::::::::::::::::::::: -->
    <div class="campo">
      <label for="nivelFormacion">Nivel de formación:</label>
      <select id="nivelFormacion" v-model="nivelFormacion">
        <option disabled value="">Seleccione su nivel</option>
        <option v-for="nivel in listaNivelApi" :key="nivel.niv_id" :value="nivel.niv_id">
           {{ nivel.niv_descripcion }}
        </option>
      </select>
    </div>
  </div>

  <!-- :::::::::::::::::: CHECKBOXES DE NIVELES (Mayor a Inicial) ::::::::::::::::::::::::: -->
  <transition name="desplegar">
    <div v-if="nivelFormacion > 1" class="niveles-container">
      <div class="section-grid">
        <!-- Columna izquierda: Medio -->
        <div class="nivel-column">
          <h4 class="nivel-title">Medio</h4>
          <div class="checkbox-list">
            <div v-for="rama in ramasMedio" :key="rama.value" class="checkbox-item">
              <input 
                :id="'medio-' + rama.value" 
                type="checkbox" 
                class="custom-checkbox" 
                :value="rama.value"
                v-model="ramasMedioSeleccionadas"
              />
              <label :for="'medio-' + rama.value">{{ rama.label }}</label>
            </div>
          </div>
        </div>

        <!-- Columna derecha: Avanzado -->
        <div class="nivel-column">
          <h4 class="nivel-title">Avanzado</h4>
          <div class="checkbox-list">
            <div v-for="rama in ramasAvanzado" :key="rama.value" class="checkbox-item">
              <input 
                :id="'avanzado-' + rama.value" 
                type="checkbox" 
                class="custom-checkbox" 
                :value="rama.value"
                v-model="ramasAvanzadoSeleccionadas"
              />
              <label :for="'avanzado-' + rama.value">{{ rama.label }}</label>
            </div>
          </div>
        </div>
      </div>

      <!-- Input MMAA fuera del grid, debajo de las columnas -->
      <div class="mmaa-input-container">
        <label for="mmaaInput" class="mmaa-label">MMAA:</label>
        <input 
          id="mmaaInput" 
          v-model="mmaaValor" 
          type="text" 
          placeholder="Ingrese MMAA"
          maxlength="4"
          class="mmaa-input"
        />
      </div>
    </div>
  </transition>

  </section>

  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--:::::::::::::::::::::::::            Salud y Logistica        ::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <div id="seccion-3" class="inicio-linea-verde">
    <span class="numero-seccion">3</span>
  </div>
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
            placeholder="Ingrese las alergias, enfermedad o limitación"
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
            placeholder="Ingrese la limitación"
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
          <input id="nombreEmergencia" v-model="nombreEmergencia" type="text" placeholder="Ej: Alan Dave" />
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
      <option v-for="alim in listaAlimentacionApi" :key="alim.ali_id" :value="alim.ali_id">
          {{ alim.ali_descripcion }}
      </option>
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
                        placeholder="Ej: Abcd12"
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
    <BaseButton 
      variant="primary" 
      @click.prevent="abrirSelectorArchivo"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
      Subir Ficha Médica
    </BaseButton>
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
  <div id="seccion-4" class="inicio-linea-verde">
    <span class="numero-seccion">4</span>
  </div>
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
          placeholder="Ingrese cualquier comentario o consideración"
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
          placeholder="Ingrese cualquier comentario o consideración"
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
        placeholder="Ingrese su profesión"
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
        <div class="botones-formulario botones-acciones">
          <BaseButton type="button" variant="outline" size="xl" @click="limpiarFormulario">VACIAR</BaseButton>
          <BaseButton type="submit" variant="primary" size="xl" :loading="false" @click.prevent="enviarFormulario">ENVIAR</BaseButton>
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
import { regionApi } from '../services/regionService';
import BaseButton from '@/components/BaseButton.vue';
const listaRegionApi = ref([]);
import { watch } from 'vue';
// :::::::::::::::::: IMPORTS Y WEAS :::::::::::::::::::::::::
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
// Lista de ramas para mostrar el nombre
const listaRamas = ref([]);

// Devuelve la descripción de la rama por su ID
const obtenerDescripcionRama = (ramaId) => {
  const rama = listaRamas.value.find(r => r.ram_id === ramaId);
  return rama ? rama.ram_descripcion : ramaId;
};

import { cursos as cursosApi, secciones as seccionesApi } from '../services/cursosService';
import { estadoCivilApi } from '../services/estadoCivilService';
import { provinciaApi } from '../services/provinciaService';
import { comunaApi } from '../services/comunaService';
import { 
    zona as zonaApi, 
    distrito as distritoApi, 
    grupo as grupoApi, 
    rol as rolApi, 
    nivel as nivelApi, 
    alimentacion as alimentacionApi 
} from '../services/mantenedoresService';

// :::::::::::::::::: MANEJO DE SELECCIÓN DE CURSO Y SECCIÓN :::::::::::::::::::::::::
// :::::::::::::::::: CURSOS DESDE API :::::::::::::::::::::::::
const listaCursosApi = ref([]);
// Lista vacía para secciones, igual que cursos
const listaSeccionesApi = ref([]);
// Lista de comunas para el selector
const listaComunaApi = ref([]);
// Estado civil desde API
const listaEstadoCivilApi = ref([]);
const listaProvinciaApi = ref([]);

// Nuevas listas para mantenedores
const listaZonaApi = ref([]);
const listaDistritoApi = ref([]);
const listaGrupoApi = ref([]);
const listaRolApi = ref([]);
const listaNivelApi = ref([]);
const listaAlimentacionApi = ref([]);

// :::::::::::::::::: VARIABLES PARA CAPTURAR VALORES (Movidas al inicio) :::::::::::::::::::::::::
const observacionesCurso = ref("");
const tieneLimitacion = ref("");
const detalleLimitacion = ref("");
const zonaSeleccionada = ref("");
const otraZona = ref("");
const grupoPertenece = ref("");

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
const nivelFormacion = ref("");
const ramasMedioSeleccionadas = ref([]);
const ramasAvanzadoSeleccionadas = ref([]);
const mmaaValor = ref("");
const grupoSeleccionado = ref("");
const grupoOtro = ref("");
const ramaSeleccionada = ref("");

// Datos para los checkboxes de ramas (se pueden conectar a una API)
// Ramas computadas desde la API en lugar de hardcodeadas
const ramasMedio = computed(() => {
  return listaRamas.value.map(rama => ({
    value: rama.ram_id,
    label: rama.ram_descripcion
  }));
});

// Asumimos que las mismas ramas están disponibles para avanzado, 
// o si hay lógica diferente, se puede filtrar aquí.
const ramasAvanzado = computed(() => {
  return listaRamas.value.map(rama => ({
    value: rama.ram_id,
    label: rama.ram_descripcion
  }));
});
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
const provinciaSeleccionada = ref("");



const descargarFicha = () => {
  const link = document.createElement('a');
  link.href = '/Ficha Medica.docx';
  link.setAttribute('download', 'Ficha Medica.docx');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

onMounted(async () => {
  // Cargar ramas
  try {
    const respRamas = await import('../services/ramasService');
    const ramasApi = respRamas.ramas;
    const ramasResp = await ramasApi.list({ page_size: 200 });
    listaRamas.value = ramasResp.results || ramasResp || [];
  } catch {
    listaRamas.value = [];
  }
      // Región
      try {
        const regionResp = await regionApi.list();
        listaRegionApi.value = regionResp.results || regionResp || [];
      } catch {
        listaRegionApi.value = [];
      }


    // Cuando cambia la Región: Cargar Provincias
    watch(regionSeleccionada, async (newVal) => {
      provinciaSeleccionada.value = "";
      comunaSeleccionada.value = "";
      listaProvinciaApi.value = [];
      listaComunaApi.value = [];

      if (newVal) {
        try {
          // Filtramos provincias por region_id
          const resp = await provinciaApi.list({ region_id: newVal });
          listaProvinciaApi.value = resp.results || resp || [];
        } catch (e) {
          console.error('Error fetching provinces:', e);
          listaProvinciaApi.value = [];
        }
      }
    });


    // Cuando cambia la Provincia: Cargar Comunas
    watch(provinciaSeleccionada, async (newVal) => {
      comunaSeleccionada.value = "";
      listaComunaApi.value = [];

      if (newVal) {
        try {
          // Filtramos comunas por provincia_id
          const resp = await comunaApi.list({ provincia_id: newVal });
          listaComunaApi.value = resp.results || resp || [];
        } catch (e) {
            console.error('Error fetching comunas:', e);
            listaComunaApi.value = [];
        }
      }
    });

    // Cargar distritos cuando cambia la zona seleccionada
    watch(zonaSeleccionada, async (newVal) => {
      distritoSeleccionado.value = "";
      grupoSeleccionado.value = "";
      listaDistritoApi.value = [];
      listaGrupoApi.value = [];

      if (newVal) {
        try {
          const distResp = await distritoApi.list({ zon_id: newVal });
          listaDistritoApi.value = distResp.results || distResp || [];
        } catch {
          listaDistritoApi.value = [];
        }
      }
    });

    // Cargar grupos cuando cambia el distrito seleccionado
    watch(distritoSeleccionado, async (newVal) => {
        grupoSeleccionado.value = "";
        listaGrupoApi.value = [];
        
      if (newVal) {
        try {
          const grupoResp = await grupoApi.list({ dis_id: newVal });
          listaGrupoApi.value = grupoResp.results || grupoResp || [];
        } catch {
          listaGrupoApi.value = [];
        }
      }
    });

  try {
    // Solicita todos los cursos con un page_size grande
    const respuesta = await cursosApi.list({ page_size: 2000 });
    listaCursosApi.value = (respuesta.results || respuesta || [])
      .map(curso => ({ ...curso }))
      .sort((a, b) => a.cur_id - b.cur_id);
  } catch (error) {
    console.error('Error al obtener cursos:', error);
  }
    // Estado civil
  try {
    const estadoCivilResp = await estadoCivilApi.list();
    listaEstadoCivilApi.value = estadoCivilResp.results || estadoCivilResp || [];
  } catch {
    listaEstadoCivilApi.value = [];
  }
  
  // NOTE: Ya no cargamos provincias ni comunas inicialmente, dependen de la selección cascada

  // Cargar mantenedores generales
  try {
      console.log('Loading mantenedores...');
      const [zonaResp, rolResp, nivelResp, alimResp] = await Promise.all([
          zonaApi.list({ page_size: 100 }),
          rolApi.list(),
          nivelApi.list(),
          alimentacionApi.list()
      ]);
      console.log('Zona response:', zonaResp);
      
      const zonas = zonaResp.results || zonaResp || [];
      console.log('Zonas parsed:', zonas);
      listaZonaApi.value = [...zonas, { zon_id: 'otro', zon_descripcion: 'Otro' }];
      
      const roles = rolResp.results || rolResp || [];
      listaRolApi.value = [...roles, { rol_id: 'otro', rol_descripcion: 'Otro' }];
      
      const niveles = nivelResp.results || nivelResp || [];
      listaNivelApi.value = niveles;
      
      const alims = alimResp.results || alimResp || [];
      listaAlimentacionApi.value = alims; // Alimentacion usually has 'Ninguna' or specific, maybe add 'Otro' if requested but DB had 'Ninguna'

  } catch (e) {
      console.error("Error cargando mantenedores", e);
  }
});

const handleCursoChange = async () => {
  seccionCurso.value = "";
  listaSeccionesApi.value = [];

  if (!cursoSeleccionado.value) {
    return;
  }

  try {
    // La API espera el parámetro cur_id
    const respuestaSecciones = await seccionesApi.list({ cur_id: cursoSeleccionado.value });
    listaSeccionesApi.value = respuestaSecciones.results || respuestaSecciones || [];
    console.log('Secciones obtenidas para el curso:', listaSeccionesApi.value);
  } catch (error) {
    console.error('Error al obtener las secciones del curso:', error);
    listaSeccionesApi.value = [];
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

// :::::::::::::::::: FUNCIÓN DE NAVEGACIÓN FLOTANTE :::::::::::::::::::::::::
const scrollToSection = (sectionNumber) => {
  const element = document.getElementById(`seccion-${sectionNumber}`);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    updateActiveNavItem(sectionNumber);
  }
};

// Scroll al h1 del formulario
const scrollToTop = () => {
  const h1 = document.querySelector('.titulo-pre-registro');
  if (h1) {
    h1.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

// Actualizar el botón activo
const updateActiveNavItem = (sectionNumber) => {
  document.querySelectorAll('.nav-item').forEach((item, index) => {
    item.classList.toggle('active', index === sectionNumber - 1);
  });
};

// Detectar scroll y actualizar navegación automáticamente
// let intersectionObserver = null; // Unused for now

onMounted(() => {
  // Función para detectar qué sección está en el centro de la pantalla
  const checkActiveSection = () => {
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
        
        // Si esta sección está más cerca del centro de la pantalla
        if (distance < minDistance && rect.top < viewportCenter && rect.bottom > 0) {
          minDistance = distance;
          closestSection = num;
        }
      }
    });
    
    updateActiveNavItem(closestSection);
  };
  
  // Listener de scroll con throttle
  let scrollTimeout;
  const handleScroll = () => {
    if (scrollTimeout) {
      clearTimeout(scrollTimeout);
    }
    scrollTimeout = setTimeout(() => {
      checkActiveSection();
    }, 100);
  };
  
  window.addEventListener('scroll', handleScroll);
  
  // Verificar sección activa al cargar
  setTimeout(() => {
    checkActiveSection();
  }, 500);
  
  // Limpiar listener al desmontar
  onBeforeUnmount(() => {
    window.removeEventListener('scroll', handleScroll);
    if (scrollTimeout) {
      clearTimeout(scrollTimeout);
    }
  });
});

// (Moved to top)
// const provinciaSeleccionadaValor = computed(() => {
//   return listaProvinciaApi.value.find(p => p.PRO_ID === provinciaSeleccionada.value) || null;
// });
const ciudadSeleccionada = ref("");
const comunaSeleccionada = ref("");

// (campo de teléfono principal eliminado)

// Handler para el select de Dirección: si escoge una opción distinta de 'Otra',
// copiamos el valor a `direccion` (para que el payload siga usando `direccion`).
//
// onDireccionSelect removed — la dirección ahora se ingresa directamente en el campo `direccion`

// Variables para el formador
const esFormador = ref("");
// const historialFormador = ref(""); // Unused for now
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
// function validarPatentePropia() {
//   // Permite formato: AA-BB-11 o AB-CD-12 o similar
//   const formato = /^[A-Z]{2}-[A-Z]{2}-\d{2}$/;
//   if (patenteVehiculo.value && !formato.test(patenteVehiculo.value.toUpperCase())) {
//     patenteVehiculo.value = patenteVehiculo.value
//       .toUpperCase()
//       .replace(/[^A-Z0-9-]/g, ""); // limpia caracteres no válidos
//   }
// }

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
  } catch {
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




// const comunasDisponibles = computed(() => {
//   if (regionSeleccionada.value && ciudadSeleccionada.value) {
//     return comunasPorRegion[regionSeleccionada.value][ciudadSeleccionada.value] || [];
//   }
//   return [];
// });
import authService from '../services/authService';

// ... (existing code)

const enviarFormulario = async () => {
  try {
    // 0. Validar usuario logueado
    const currentUser = await authService.getCurrentUser();
    if (!currentUser || !currentUser.id) {
      alert("Error: No se pudo identificar al usuario actual. Por favor inicie sesión nuevamente.");
      return;
    }

    // 1. Validaciones básicas
    if (!rut.value || !nombres.value || !apellidoPaterno.value || !email.value) {
      alert("Por favor complete los campos obligatorios del postulante.");
      return;
    }
    if (!seccionCurso.value || !rolSeleccionado.value) {
      alert("Por favor seleccione Curso y Cargo/Rol.");
      return;
    }

    // 2. Preparar datos de Persona
    const [run, dv] = rut.value.split('-');
    
    // Mapeo de campos según persona_model.py
    const personaData = {
      usu_id: currentUser.id, // ID del usuario que crea el registro
      per_run: run,
      per_dv: dv || '', // Manejar caso sin guion si rut viene limpio
      per_nombres: nombres.value,
      per_apelpta: apellidoPaterno.value,
      per_apelmat: apellidoMaterno.value || '',
      per_email: email.value,
      per_fecha_nac: fechaNacimiento.value, // Asegurar formato YYYY-MM-DD
      per_direccion: direccion.value,
      com_id: comunaSeleccionada.value,
      esc_id: estadoCivil.value,
      per_tipo_fono: tipoTelefono.value,
      per_fono: telefono.value,
      per_nom_emergencia: nombreEmergencia.value,
      per_fono_emergencia: telefonoEmergencia.value,
      per_alergia_enfermedad: alergias.value || '',
      per_limitacion: limitaciones.value || '', // Verificar si existe este input
      per_profesion: profesion.value || '',
      per_religion: religion.value || '',
      per_apodo: apodoCredencial.value || '',
      // per_foto: fotoUrl.value, // Pendiente: Manejo de subida de archivo
      per_otros: consideraciones.value || '',
      // per_num_mmaa: mmaaValor.value // Si existe input
      // Valores por defecto
      per_vigente: true
    };
    
    // Agregar campos opcionales solo si tienen valor
    if (anosTrabajoNinos.value) personaData.per_tiempo_nnaj = anosTrabajoNinos.value;
    // if (anosTiempoBeneficiario.value) personaData.per_tiempo_adulto = ...;


    // 3. Preparar datos de Curso (Persona_Curso)
    const cursoData = {
      cus_id: seccionCurso.value,
      rol_id: rolSeleccionado.value,
      ali_id: tipoAlimentacion.value,
      niv_id: nivelFormacion.value
    };

    // 4. Preparar datos de Vehículo (Persona_Vehiculo)
    let vehiculoData = null;
    if (vehiculoPropio.value === 'si') {
      vehiculoData = {
        pev_patente: patentePropia.value,
        pev_marca: marcaPropia.value, 
        pev_modelo: modeloPropio.value
      };
    }

    // 5. Preparar datos de Formador (Persona_Formador)
    let formadorData = null;
    if (habilidad1.value || habilidad2.value || verificado.value) {
      formadorData = {
        pef_hab_1: habilidad1.value === 'si' || habilidad1.value === true, // Ensure boolean
        pef_hab_2: habilidad2.value === 'si' || habilidad2.value === true,
        pef_verif: verificado.value === 'si' || verificado.value === true,
        pef_historial: ''
      };
    }

    // 6. Preparar datos de Ramas (Persona_Nivel)
    let ramasData = [];
    
    const getNivelId = (nombre) => {
      const nivel = listaNivelApi.value.find(n => n.niv_descripcion && n.niv_descripcion.toLowerCase().includes(nombre.toLowerCase()));
      return nivel ? nivel.niv_id : null;
    };

    const idMedio = getNivelId('Medio') || 2; 
    const idAvanzado = getNivelId('Avanzado') || 3; 

    if (ramasMedioSeleccionadas.value.length > 0) {
      ramasMedioSeleccionadas.value.forEach(rId => {
        ramasData.push({ niv_id: idMedio, ram_id: rId });
      });
    }
    if (ramasAvanzadoSeleccionadas.value.length > 0) {
      ramasAvanzadoSeleccionadas.value.forEach(rId => {
        ramasData.push({ niv_id: idAvanzado, ram_id: rId });
      });
    }

    // 7. Preparar datos de Grupo (Persona_Grupo)
    let grupoData = null;
    if (grupoPertenece.value) {
      grupoData = {
        gru_id: grupoPertenece.value,
        peg_vigente: true
      };
    }

    // 8. Enviar al Backend
    console.log("Enviando formulario:", { personaData, cursoData, vehiculoData, formadorData, ramasData, grupoData });
    const result = await personasService.createPersonaWithCourseAndVehicle({
      personaData,
      cursoData,
      vehiculoData,
      formadorData,
      ramasData,
      grupoData
    });

    console.log("Resultado envío:", result);
    alert("Formulario enviado exitosamente y todos los datos registrados!");
    limpiarFormulario();

  } catch (error) {
    console.error("Error al enviar formulario:", error);
    alert("Error al enviar el formulario: " + (error.message || "Error desconocido"));
  }
};
</script>


  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::        STYLES CSS     :::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
  <!--::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&family=Montserrat:wght@700&family=Poppins:wght@400&display=swap');

/* :::::::::::::::::::: H1 PRE-REGISTRO :::::::::::::::::::: */
/* :::::::::::::::::::: H1 PRE-REGISTRO :::::::::::::::::::: */
.titulo-pre-registro {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #3b82f6);
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  animation: expandLine 1s ease-out 0.3s forwards;
  width: 0;
}

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
  position: relative;    /* For custom arrow positioning */
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
  padding: 8px 12px !important;
  border: 2px solid #e8e8e8 !important;
  border-radius: 8px !important;
  background: #fff !important;
  box-sizing: border-box;
  font-size: 14px !important;
  color: #333 !important;
  font-weight: 500 !important;
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1) !important;
  box-shadow: 0px 0px 20px -18px !important;
}

/* Hide default select arrow */
select,
.selector-formador {
  -webkit-appearance: none !important;
  -moz-appearance: none !important;
  appearance: none !important;
  padding-right: 40px !important;
 
  cursor: pointer;
}

/* Placeholder color for unselected state */
select:invalid {
  color: #999 !important;
}

select option {
  color: #333 !important;
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
  border: 2px solid #007bff !important;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25) !important;
}

input:active,
select:active,
textarea:active {
  transform: scale(0.995);
}

/* Custom arrow for select elements */
.campo:has(select)::after,
.campo:has(.selector-formador)::after {
  content: '';
  position: absolute;
  top: calc(50% + 12px);
  right: 15px;
  transform: translateY(-50%) rotate(45deg);
  width: 8px;
  height: 8px;
  border-bottom: 2px solid #888;
  border-right: 2px solid #888;
  pointer-events: none;
  transition: border-color 0.2s, transform 0.2s;
}

/* Arrow color change on hover */
.campo:has(select:hover)::after,
.campo:has(.selector-formador:hover)::after {
  border-color: #007bff;
}

/* Arrow color and rotation on focus */
.campo:has(select:focus)::after,
.campo:has(.selector-formador:focus)::after {
  border-color: #007bff;
  transform: translateY(-50%) rotate(225deg);
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

/* Checkboxes en horizontal centrados */
.checkbox-list-horizontal {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 0.5rem;
}

.checkbox-list-horizontal > div {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* Custom checkbox based on uiverse example (calm-wasp-75) */
.bloque-formador {
  --_clr-primary: #333;
  --_clr-checked: #127acf;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 900px;
  margin: 50 auto;
  padding: 15px 15px 15px 0;
  box-sizing: border-box;
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
  .checkbox-list-horizontal {
    flex-direction: column;
    gap: 1rem;
  }
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

/* Estilos para las columnas de nivel */
.niveles-container {
  margin-top: 20px;
  width: 100%;
}

.nivel-column {
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  min-height: 250px;
  display: flex;
  flex-direction: column;
}

.nivel-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 15px 0;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #10b981;
}

.nivel-column .checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-grow: 0;
}

.nivel-column .checkbox-list > div {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nivel-column .checkbox-list label {
  cursor: pointer;
  color: #333;
  user-select: none;
  font-size: 14px;
}

/* Input MMAA minimalista - posicionado debajo de ambas columnas */
.mmaa-input-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  justify-content: flex-start;
  padding-left: 0;
}

.mmaa-label {
  font-size: 12px !important;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.mmaa-input {
  width: 130px !important;
  padding: 4px 8px !important;
  font-size: 12px !important;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  text-align: center;
  transition: all 0.2s ease;
}

.mmaa-input:focus {
  border-color: #10b981;
  outline: none;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.mmaa-input::placeholder {
  color: #9ca3af;
  font-size: 12px;
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

/* Centrar la sección completa de '¿Eres Formador?' */
.bloque-formador .campo {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.bloque-formador .campo label[for="formador"] {
  text-align: center;
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.bloque-formador .campo select#formador,
.bloque-formador .selector-formador {
  max-width: 400px;
  width: 100%;
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


/* :::::::::::::::::::: ESTILOS PARA CAJAS DE RAMAS :::::::::::::::::::: */
.niveles-container {
  margin-top: 30px;
  width: 100%;
}

.nivel-column {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  height: 100%;
}

.nivel-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  text-align: center;
  padding: 15px 0;
  background-color: #fff;
  border-bottom: 3px solid #10b981; /* Green line separator */
}

/* Grid layout for checkboxes inside the card */
.nivel-column .checkbox-list {
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.checkbox-item:hover {
  background-color: #f8fafc;
}

.checkbox-item label {
  cursor: pointer;
  color: #334155;
  font-weight: 500;
  font-size: 15px;
  user-select: none;
  margin: 0;
}

/* Custom checkbox styling */
.custom-checkbox {
  appearance: none;
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid #cbd5e1;
  border-radius: 4px;
  background-color: white;
  display: grid;
  place-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.custom-checkbox::after {
  content: "✓";
  font-size: 14px;
  color: white;
  transform: scale(0);
  transition: transform 0.2s ease;
  font-weight: bold;
}

.custom-checkbox:checked {
  background-color: #10b981; /* Green active color */
  border-color: #10b981;
}

.custom-checkbox:checked::after {
  transform: scale(1);
}

/* Input MMAA minimalista - posicionado debajo de ambas columnas */
.mmaa-input-container {
  margin-top: 25px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Center align */
  gap: 8px;
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
    padding-top: 10px; /* Ajusta este valor para mover el formulario más arriba o abajo */
    background: linear-gradient(to bottom, #E0F2F7, #F0F8FF);
} 

textarea { 
    resize: none; /* desactiva el cambio de tamaño con el mouse */ 
    height: 100px; /* ||alto fijo (puedes ajustar a tu gusto) */ 
    width: 100%; /* asegura que ocupe todo el ancho del contenedor */ 
    box-sizing: border-box; /* evita desbordes por padding */ 
} 

h2 { 
    font-size: 1.8rem; /* tamaño de los sub titulos aumentado */ 
    color: #1e293b; 
    font-weight: 700; 
    text-align: left; 
    margin: 1.5rem 0 1rem 0; 
    padding-bottom: 10px;
    padding-left: 40px;
    position: relative;
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
  max-width: 1100px;
  display: flex;
  justify-content: center;
  padding: 0 24px 32px 24px;
  box-sizing: border-box;
}

.form-inner {
  width: 100%;
  max-width: 1100px; /* occupy central wide area */
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.98));
  padding: 34px;
  border-radius: 25px;
  box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.1);
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
  position: relative;
  margin-left: 50px;
}

/* Línea vertical verde conectando las secciones (solo dentro de resto-formulario) */
.resto-formulario section::before {
  content: '';
  position: absolute;
  left: -34px;
  top: 48px;
  bottom: -18px;
  width: 3px;
  background: #2563eb;
  z-index: 1;
}

/* Eliminar línea verde de la sección "¿Eres Formador?" */
.resto-formulario section.bloque-formador::before {
  display: none;
}

.resto-formulario section:first-of-type::before {
  top: 16px;
}

.resto-formulario section:last-of-type::before {
  content: '';
  position: absolute;
  left: -34px;
  top: 48px;
  bottom: -18px;
  width: 3px;
  background: #2563eb;
  z-index: 1;
  display: block;
}

.section-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
  margin-top: -50px;
}

.section-header h2 {
  font-size: 18px;
  margin: 0;
  margin-left: -10px;
  padding-left: 10px;
  padding-right: 80px;
  color: #1f2937; /* darker heading */
  font-weight: 700;
  font-family: 'Poppins', 'Montserrat', 'Roboto', sans-serif;
  font-weight: 400;
  display: inline-block;
  align-items: center;
  gap: 12px;
  padding-bottom: 6px;
  border-bottom: 3px solid #2563eb;
  max-width: 100%;
}

.numero-seccion {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: #2563eb;
  color: #ffffff;
  border-radius: 50%;
  font-size: 20px;
  font-weight: 700;
  flex-shrink: 0;
  position: relative;
  z-index: 2;
  box-shadow: 0 0 0 4px #ffffff;
}

/* Círculo inicial en el extremo superior de la línea verde */
.inicio-linea-verde {
  position: relative;
  margin-left: -4px;
  padding-left: 0px;
  z-index: 3;
}

/* Primer círculo (número 1) mantiene posición original */
.inicio-linea-verde:first-of-type {
  margin-bottom: -16px;
}

/* Círculos 2, 3, 4 - posición ajustada más abajo */
.inicio-linea-verde:not(:first-of-type) {
  margin-top: -10px;
  margin-bottom: -8px;
}

.inicio-linea-verde .numero-seccion {
  display: inline-flex;
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
/* Centrar toda la sección de foto */
.foto-section-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 20px 0;
}

.foto-section-centered .botones-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.foto-section-centered .label-foto {
  text-align: center;
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.foto-section-centered .botones-grupo {
  display: flex;
  gap: 12px;
  justify-content: center;
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

/* :::::::::::::::::::: TÍTULO SELECCIONE CURSO :::::::::::::::::::: */
.titulo-seleccion-curso {
  font-size: 2.2em;
  font-weight: 700;
  font-family: 'Roboto', 'Segoe UI', sans-serif;
  text-align: center;
  color: #1e3a8a;
  margin: 30px auto 15px auto;
  padding: 0;
  text-transform: uppercase;
  letter-spacing: 4px;
  display: inline-block;
  width: 100%;
}




/* :::::::::::::::::::: LAYOUT CURSO + DESCARGA :::::::::::::::::::: */
.curso-root-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center; /* Align vertically centered */
  justify-content: center; /* Center the group on page */
  gap: 60px; /* Separation between inputs and download button */
  margin-top: 20px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.curso-inputs-column {
  flex: 0 1 400px; /* Flex-basis 400px (standard grid width), allows shrink */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Ensure inputs fill the column width (standard "fill" behavior) */
.curso-inputs-column .campo {
  width: 100%;
}

@media (max-width: 768px) {
  .curso-root-container {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
  .curso-inputs-column {
    flex: 1 1 auto;
    width: 100%;
    max-width: 100%;
  }
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
  font-family: 'Segoe UI', 'Roboto', 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  text-align: center;
  max-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-descarga p {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.4 !important;
}

.label-principal {
  font-size: 14px !important;
  color: #334155 !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px !important;
}

.label-secundario {
  font-size: 13px !important;
  color: #64748b !important;
  font-weight: 500 !important;
  letter-spacing: 0.2px !important;
  font-style: italic !important;
}

/* :::::::::::::::::::: BOTÓN DE DESCARGA (BaseButton used) :::::::::::::::::::: */
/* Styles removed as we use BaseButton component */

/* :::::::::::::::::::: BOTONES ACCIONES (Vaciar / Enviar) :::::::::::::::::::: */
.botones-acciones {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 100%;
  margin-top: 20px;
}

@media (max-width: 600px) {
  .botones-acciones {
    flex-direction: column;
    gap: 15px;
  }
  .botones-acciones > * {
    width: 100% !important; 
    /* Force full width on mobile for better touch targets */
  }
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

.archivo-seleccionado {
  font-size: 13px;
  color: #4ade80;
  font-weight: 500;
  text-align: center;
  margin-top: 5px;
}



/* :::::::::::::::::::: NAVEGACIÓN FLOTANTE :::::::::::::::::::: */
.nav-flotante {
  position: fixed;
  right: 60px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 1000;
  animation: slideInRight 0.6s ease-out;
}

.nav-item.nav-logo {
  background: linear-gradient(135deg, #fff 0%, #e0f2f1 100%);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.12);
  border: 2px solid #10b981;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-bottom: 0;
  margin-top: 0;
}
.nav-logo-img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.18);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px) translateY(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0) translateY(-50%);
  }
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  border-radius: 50%;
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  cursor: pointer;
}

.nav-item::before {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 20px;
  background: linear-gradient(to bottom, #10b981, transparent);
}

.nav-item:last-child::before {
  display: none;
}

.nav-numero {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
  position: relative;
  z-index: 1;
}

.nav-item:hover {
  transform: scale(1.15);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
}

.nav-item.active {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  box-shadow: 0 8px 30px rgba(5, 150, 105, 0.6);
  transform: scale(1.2);
}

.nav-item.active::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  border: 2px solid #10b981;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

/* Responsive: ocultar en pantallas pequeñas */
@media (max-width: 768px) {
  .nav-flotante {
    display: none;
  }
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





