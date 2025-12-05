[file name]: mantenedores.vue
[file content begin]
<template>
  <div class="mantenedores-scouts">
    <!-- Error Alert -->
    <div v-if="error" class="error-alert">
      <p>{{ error }}</p>
      <button @click="error = null">×</button>
    </div>

    <!-- Loading Indicator -->
    <div v-if="cargando" class="loading-indicator">
      <p>Cargando datos...</p>
    </div>

    <!-- Selector de Mantenedores Fijo -->
    <div class="mantenedor-selector-fixed">
      <div class="selector-container">
        <div class="selector-header">
          <h2>⚙️ Mantenedores</h2>
        </div>
        <div class="selector-dropdown" ref="dropdownContainer">
          <button 
            class="mantenedor-dropdown-toggle"
            :class="{ 'active': isDropdownOpen }"
            @click="toggleDropdown"
          >
            <span class="selected-option">
              {{ getSelectedTabInfo().icon }} {{ getSelectedTabInfo().label }}
            </span>
            <div class="dropdown-icon" :class="{ 'rotate': isDropdownOpen }">▼</div>
          </button>
          
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <div 
              v-for="tab in tabs" 
              :key="tab.id"
              class="dropdown-item"
              :class="{ 'active': activeTab === tab.id }"
              @click="selectTab(tab.id)"
            >
              <span class="dropdown-item-icon">{{ tab.icon }}</span>
              <span class="dropdown-item-text">{{ tab.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content-expanded">
      <!-- Header -->
      <div class="header-expanded">
        <h1>Módulo de Mantenedores</h1>
        <p>Gestión de Datos Maestros del Sistema Scout</p>
      </div>
      
      <!-- Zonas -->
      <div v-if="activeTab === 'zonas'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🗺️ Gestión de Zonas</h2>
          <button class="btn-primary" @click="abrirModalCrear('zona')">
            + Nueva Zona
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="BUSCAR ZONA POR DESCRIPCIÓN..."
            v-model="searchZonas"
            @input="searchZonas = searchZonas.toUpperCase()"
          >
          <button class="btn-primary" @click="buscarZonas">🔍 BUSCAR</button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>UNILATERAL</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="zona in filteredZonas" :key="zona.id">
                <td>{{ zona.descripcion }}</td>
                <td>{{ zona.unilateral ? 'SÍ' : 'NO' }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('zona', zona)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('zona', zona)">✏ EDITAR</button>
                  <button 
                    v-if="zona.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('zona', zona)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('zona', zona)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Distritos -->
      <div v-if="activeTab === 'distritos'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📍 Gestión de Distritos</h2>
          <button class="btn-primary" @click="abrirModalCrear('distrito')">
            + NUEVO DISTRITO
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="BUSCAR DISTRITO..."
            v-model="searchDistritos"
            @input="searchDistritos = searchDistritos.toUpperCase()"
          >
          <select class="select-filter" v-model="filtroZona">
            <option value="">TODAS LAS ZONAS</option>
            <option v-for="zona in zonas" :key="zona.id" :value="zona.descripcion">
              {{ zona.descripcion }}
            </option>
          </select>
          <button class="btn-primary" @click="buscarDistritos">🔍 BUSCAR</button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ZONA</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="distrito in filteredDistritos" :key="distrito.id">
                <td>{{ distrito.descripcion }}</td>
                <td>{{ getZonaNombre(distrito.zona_id) }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('distrito', distrito)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('distrito', distrito)">✏ EDITAR</button>
                  <button 
                    v-if="distrito.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('distrito', distrito)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('distrito', distrito)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Grupos -->
      <div v-if="activeTab === 'grupos'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>👥 Gestión de Grupos</h2>
          <button class="btn-primary" @click="abrirModalCrear('grupo')">
            + NUEVO GRUPO
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="BUSCAR GRUPO..."
            v-model="searchGrupos"
            @input="searchGrupos = searchGrupos.toUpperCase()"
          >
          <select class="select-filter" v-model="filtroDistrito">
            <option value="">TODOS LOS DISTRITOS</option>
            <option v-for="distrito in distritos" :key="distrito.id" :value="distrito.descripcion">
              {{ distrito.descripcion }}
            </option>
          </select>
          <button class="btn-primary" @click="buscarGrupos">🔍 BUSCAR</button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>DISTRITO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="grupo in filteredGrupos" :key="grupo.id">
                <td>{{ grupo.descripcion }}</td>
                <td>{{ getDistritoNombre(grupo.distrito_id) }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('grupo', grupo)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('grupo', grupo)">✏ EDITAR</button>
                  <button 
                    v-if="grupo.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('grupo', grupo)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('grupo', grupo)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Ramas -->
      <div v-if="activeTab === 'ramas'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🏕️ Gestión de Ramas</h2>
          <button class="btn-primary" @click="abrirModalCrear('rama')">
            + NUEVA RAMA
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rama in ramas" :key="rama.id">
                <td>{{ rama.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('rama', rama)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('rama', rama)">✏ EDITAR</button>
                  <button 
                    v-if="rama.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('rama', rama)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('rama', rama)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Tipos de Curso -->
      <div v-if="activeTab === 'tipos-curso'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📚 Gestión de Tipos de Curso</h2>
          <button class="btn-primary" @click="abrirModalCrear('tipoCurso')">
            + NUEVO TIPO
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>TIPO</th>
                <th>CANT. PARTICIPANTES</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoCurso in tiposCurso" :key="tipoCurso.id">
                <td>{{ tipoCurso.descripcion }}</td>
                <td>{{ tipoCurso.tipo }}</td>
                <td>{{ tipoCurso.cant_participante }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('tipoCurso', tipoCurso)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('tipoCurso', tipoCurso)">✏ EDITAR</button>
                  <button 
                    v-if="tipoCurso.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('tipoCurso', tipoCurso)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('tipoCurso', tipoCurso)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Cargos -->
      <div v-if="activeTab === 'cargos'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>👔 Gestión de Cargos</h2>
          <button class="btn-primary" @click="abrirModalCrear('cargo')">
            + NUEVO CARGO
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cargo in cargos" :key="cargo.id">
                <td>{{ cargo.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('cargo', cargo)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('cargo', cargo)">✏ EDITAR</button>
                  <button 
                    v-if="cargo.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('cargo', cargo)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('cargo', cargo)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Alimentación -->
      <div v-if="activeTab === 'alimentacion'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🍽️ Gestión de Alimentación</h2>
          <button class="btn-primary" @click="abrirModalCrear('alimentacion')">
            + NUEVA ALIMENTACIÓN
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>TIPO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="alimentacionItem in alimentacion" :key="alimentacionItem.id">
                <td>{{ alimentacionItem.descripcion }}</td>
                <td>{{ alimentacionItem.tipo }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('alimentacion', alimentacionItem)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('alimentacion', alimentacionItem)">✏ EDITAR</button>
                  <button 
                    v-if="alimentacionItem.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('alimentacion', alimentacionItem)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('alimentacion', alimentacionItem)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Comunas -->
      <div v-if="activeTab === 'comunas'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🏘️ Gestión de Comunas</h2>
          <button class="btn-primary" @click="abrirModalCrear('comuna')">
            + NUEVA COMUNA
          </button>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="BUSCAR COMUNA..."
            v-model="searchComunas"
            @input="searchComunas = searchComunas.toUpperCase()"
          >
          <button class="btn-primary" @click="buscarComunas">🔍 BUSCAR</button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>PROVINCIA</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comuna in comunas" :key="comuna.id">
                <td>{{ comuna.descripcion }}</td>
                <td>{{ getProvinciaNombre(comuna.provincia_id) }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('comuna', comuna)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('comuna', comuna)">✏ EDITAR</button>
                  <button 
                    v-if="comuna.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('comuna', comuna)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('comuna', comuna)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Provincias -->
      <div v-if="activeTab === 'provincias'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🏞️ Gestión de Provincias</h2>
          <button class="btn-primary" @click="abrirModalCrear('provincia')">
            + NUEVA PROVINCIA
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>REGIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="provincia in provincias" :key="provincia.id">
                <td>{{ provincia.descripcion }}</td>
                <td>{{ getRegionNombre(provincia.region_id) }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('provincia', provincia)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('provincia', provincia)">✏ EDITAR</button>
                  <button 
                    v-if="provincia.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('provincia', provincia)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('provincia', provincia)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Regiones -->
      <div v-if="activeTab === 'regiones'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>🗾 Gestión de Regiones</h2>
          <button class="btn-primary" @click="abrirModalCrear('region')">
            + NUEVA REGIÓN
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="region in regiones" :key="region.id">
                <td>{{ region.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('region', region)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('region', region)">✏ EDITAR</button>
                  <button 
                    v-if="region.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('region', region)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('region', region)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Niveles -->
      <div v-if="activeTab === 'niveles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📊 Gestión de Niveles</h2>
          <button class="btn-primary" @click="abrirModalCrear('nivel')">
            + NUEVO NIVEL
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="nivel in niveles" :key="nivel.id">
                <td>{{ nivel.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('nivel', nivel)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('nivel', nivel)">✏ EDITAR</button>
                  <button 
                    v-if="nivel.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('nivel', nivel)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('nivel', nivel)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Estado Civil -->
      <div v-if="activeTab === 'estados-civiles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>💑 Gestión de Estado Civil</h2>
          <button class="btn-primary" @click="abrirModalCrear('estadoCivil')">
            + NUEVO ESTADO CIVIL
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="estadoCivil in estadosCiviles" :key="estadoCivil.id">
                <td>{{ estadoCivil.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('estadoCivil', estadoCivil)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('estadoCivil', estadoCivil)">✏ EDITAR</button>
                  <button 
                    v-if="estadoCivil.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('estadoCivil', estadoCivil)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('estadoCivil', estadoCivil)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Roles -->
      <div v-if="activeTab === 'roles'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>👤 Gestión de Roles</h2>
          <button class="btn-primary" @click="abrirModalCrear('rol')">
            + NUEVO ROL
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rol in roles" :key="rol.id">
                <td>{{ rol.descripcion }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('rol', rol)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('rol', rol)">✏ EDITAR</button>
                  <button 
                    v-if="rol.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('rol', rol)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('rol', rol)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Conceptos Contables -->
      <div v-if="activeTab === 'conceptos-contables'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>💰 Gestión de Conceptos Contables</h2>
          <button class="btn-primary" @click="abrirModalCrear('conceptoContable')">
            + NUEVO CONCEPTO
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>TIPO</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="concepto in conceptosContables" :key="concepto.id">
                <td>{{ concepto.descripcion }}</td>
                <td>{{ concepto.tipo }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('conceptoContable', concepto)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('conceptoContable', concepto)">✏ EDITAR</button>
                  <button 
                    v-if="concepto.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('conceptoContable', concepto)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('conceptoContable', concepto)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tipos de Archivo -->
      <div v-if="activeTab === 'tipos-archivo'" class="mantenedor-section-expanded">
        <div class="mantenedor-header">
          <h2>📁 Gestión de Tipos de Archivo</h2>
          <button class="btn-primary" @click="abrirModalCrear('tipoArchivo')">
            + NUEVO TIPO
          </button>
        </div>
        
        <div class="table-container-expanded">
          <table class="data-table-expanded">
            <thead>
              <tr>
                <th>DESCRIPCIÓN</th>
                <th>EXTENSIÓN</th>
                <th>ACCIONES</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoArchivo in tiposArchivo" :key="tipoArchivo.id">
                <td>{{ tipoArchivo.descripcion }}</td>
                <td>{{ tipoArchivo.extension }}</td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('tipoArchivo', tipoArchivo)">👁 VER</button>
                  <button class="btn-action btn-edit" @click="editarElemento('tipoArchivo', tipoArchivo)">✏ EDITAR</button>
                  <button 
                    v-if="tipoArchivo.vigente" 
                    class="btn-action btn-anular" 
                    @click="anularElemento('tipoArchivo', tipoArchivo)"
                  >
                    🚫 ANULAR
                  </button>
                  <button 
                    v-else 
                    class="btn-action btn-habilitar" 
                    @click="habilitarElemento('tipoArchivo', tipoArchivo)"
                  >
                    ✅ ACTIVAR
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Visualización -->
    <div v-if="modalActivo === 'ver'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👁 VISUALIZAR {{ getTipoNombre(tipoElemento) }}</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">UNILATERAL:</label>
              <div class="view-value">{{ elementoSeleccionado.unilateral ? 'SÍ' : 'NO' }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">ESTADO:</label>
              <div class="view-value">
                <span class="status-badge" :class="elementoSeleccionado.vigente ? 'status-active' : 'status-inactive'">
                  {{ elementoSeleccionado.vigente ? 'ACTIVO' : 'INACTIVO' }}
                </span>
              </div>
            </div>

            <!-- Campos para otros tipos de elementos -->
            <div v-if="tipoElemento !== 'zona'" class="view-group">
              <label class="view-label">DESCRIPCIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="['distrito', 'grupo', 'comuna', 'provincia'].includes(tipoElemento)" class="view-group">
              <label class="view-label">{{ getRelacionNombre(tipoElemento) }}:</label>
              <div class="view-value">{{ getRelacionValor(tipoElemento) }}</div>
            </div>
            <div v-if="['tipoCurso', 'alimentacion', 'conceptoContable'].includes(tipoElemento)" class="view-group">
              <label class="view-label">TIPO:</label>
              <div class="view-value">{{ elementoSeleccionado.tipo }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoCurso'" class="view-group">
              <label class="view-label">CANT. PARTICIPANTES:</label>
              <div class="view-value">{{ elementoSeleccionado.cant_participante }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoArchivo'" class="view-group">
              <label class="view-label">EXTENSIÓN:</label>
              <div class="view-value">{{ elementoSeleccionado.extension }}</div>
            </div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="cerrarModal">CERRAR</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Zonas -->
    <div v-if="modalActivo === 'crear-zona' || modalActivo === 'editar-zona'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} ZONA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarZona">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formZona.descripcion"
                @input="formZona.descripcion = formZona.descripcion.toUpperCase()"
                placeholder="EJ: ZONA NORTE BIOBÍO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-checkbox">
                <input type="checkbox" v-model="formZona.unilateral">
                ZONA UNILATERAL
              </label>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Distritos -->
    <div v-if="modalActivo === 'crear-distrito' || modalActivo === 'editar-distrito'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} DISTRITO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarDistrito">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formDistrito.descripcion"
                @input="formDistrito.descripcion = formDistrito.descripcion.toUpperCase()"
                placeholder="EJ: DISTRITO CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">ZONA:</label>
              <select class="form-control" v-model="formDistrito.zona_id" required>
                <option value="">SELECCIONE UNA ZONA</option>
                <option v-for="zona in zonas" :key="zona.id" :value="zona.id">
                  {{ zona.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Grupos -->
    <div v-if="modalActivo === 'crear-grupo' || modalActivo === 'editar-grupo'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} GRUPO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarGrupo">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formGrupo.descripcion"
                @input="formGrupo.descripcion = formGrupo.descripcion.toUpperCase()"
                placeholder="EJ: GRUPO ARAUCO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">DISTRITO:</label>
              <select class="form-control" v-model="formGrupo.distrito_id" required>
                <option value="">SELECCIONE UN DISTRITO</option>
                <option v-for="distrito in distritos" :key="distrito.id" :value="distrito.id">
                  {{ distrito.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Ramas -->
    <div v-if="modalActivo === 'crear-rama' || modalActivo === 'editar-rama'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} RAMA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRama">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRama.descripcion"
                @input="formRama.descripcion = formRama.descripcion.toUpperCase()"
                placeholder="EJ: LOBATOS"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Tipos de Curso -->
    <div v-if="modalActivo === 'crear-tipoCurso' || modalActivo === 'editar-tipoCurso'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} TIPO DE CURSO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarTipoCurso">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoCurso.descripcion"
                @input="formTipoCurso.descripcion = formTipoCurso.descripcion.toUpperCase()"
                placeholder="EJ: CURSO BÁSICO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formTipoCurso.tipo" required>
                <option :value="1">INICIAL</option>
                <option :value="2">MEDIO</option>
                <option :value="3">AVANZADO</option>
                <option :value="4">HABILITACIÓN</option>
                <option :value="5">VERIFICACIÓN</option>
                <option :value="6">INSTITUCIONAL</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">CANT. PARTICIPANTES:</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formTipoCurso.cant_participante"
                placeholder="EJ: 30"
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Cargos -->
    <div v-if="modalActivo === 'crear-cargo' || modalActivo === 'editar-cargo'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} CARGO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarCargo">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formCargo.descripcion"
                @input="formCargo.descripcion = formCargo.descripcion.toUpperCase()"
                placeholder="EJ: JEFE DE GRUPO"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Alimentación -->
    <div v-if="modalActivo === 'crear-alimentacion' || modalActivo === 'editar-alimentacion'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} ALIMENTACIÓN</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarAlimentacion">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formAlimentacion.descripcion"
                @input="formAlimentacion.descripcion = formAlimentacion.descripcion.toUpperCase()"
                placeholder="EJ: DIETA REGULAR"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formAlimentacion.tipo" required>
                <option :value="1">CON ALMUERZO</option>
                <option :value="2">SIN ALMUERZO</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Comunas -->
    <div v-if="modalActivo === 'crear-comuna' || modalActivo === 'editar-comuna'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} COMUNA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarComuna">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formComuna.descripcion"
                @input="formComuna.descripcion = formComuna.descripcion.toUpperCase()"
                placeholder="EJ: CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">PROVINCIA:</label>
              <select class="form-control" v-model="formComuna.provincia_id" required>
                <option value="">SELECCIONE UNA PROVINCIA</option>
                <option v-for="provincia in provincias" :key="provincia.id" :value="provincia.id">
                  {{ provincia.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Provincias -->
    <div v-if="modalActivo === 'crear-provincia' || modalActivo === 'editar-provincia'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} PROVINCIA</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarProvincia">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formProvincia.descripcion"
                @input="formProvincia.descripcion = formProvincia.descripcion.toUpperCase()"
                placeholder="EJ: CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">REGIÓN:</label>
              <select class="form-control" v-model="formProvincia.region_id" required>
                <option value="">SELECCIONE UNA REGIÓN</option>
                <option v-for="region in regiones" :key="region.id" :value="region.id">
                  {{ region.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Regiones -->
    <div v-if="modalActivo === 'crear-region' || modalActivo === 'editar-region'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVA' }} REGIÓN</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRegion">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRegion.descripcion"
                @input="formRegion.descripcion = formRegion.descripcion.toUpperCase()"
                placeholder="EJ: REGIÓN DEL BIOBÍO"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Niveles -->
    <div v-if="modalActivo === 'crear-nivel' || modalActivo === 'editar-nivel'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} NIVEL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarNivel">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formNivel.descripcion"
                @input="formNivel.descripcion = formNivel.descripcion.toUpperCase()"
                placeholder="EJ: NIVEL BÁSICO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">ORDEN:</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formNivel.orden"
                placeholder="EJ: 1"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Estado Civil -->
    <div v-if="modalActivo === 'crear-estadoCivil' || modalActivo === 'editar-estadoCivil'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} ESTADO CIVIL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarEstadoCivil">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formEstadoCivil.descripcion"
                @input="formEstadoCivil.descripcion = formEstadoCivil.descripcion.toUpperCase()"
                placeholder="EJ: SOLTERO/A"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Roles -->
    <div v-if="modalActivo === 'crear-rol' || modalActivo === 'editar-rol'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} ROL</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRol">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRol.descripcion"
                @input="formRol.descripcion = formRol.descripcion.toUpperCase()"
                placeholder="EJ: ADMINISTRADOR"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formRol.tipo" required>
                <option :value="1">PARTICIPANTE</option>
                <option :value="2">FORMADORES</option>
                <option :value="3">APOYO FORMADORES</option>
                <option :value="4">ORGANIZACIÓN</option>
                <option :value="5">SERVICIO</option>
                <option :value="6">SALUD</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Conceptos Contables -->
    <div v-if="modalActivo === 'crear-conceptoContable' || modalActivo === 'editar-conceptoContable'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} CONCEPTO CONTABLE</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarConceptoContable">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formConceptoContable.descripcion"
                @input="formConceptoContable.descripcion = formConceptoContable.descripcion.toUpperCase()"
                placeholder="EJ: MATRÍCULA"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">TIPO:</label>
              <select class="form-control" v-model="formConceptoContable.tipo" required>
                <option value="">SELECCIONE UN TIPO</option>
                <option value="INGRESO">INGRESO</option>
                <option value="EGRESO">EGRESO</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Tipos de Archivo -->
    <div v-if="modalActivo === 'crear-tipoArchivo' || modalActivo === 'editar-tipoArchivo'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'EDITAR' : 'NUEVO' }} TIPO DE ARCHIVO</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarTipoArchivo">
            <div class="form-group">
              <label class="form-label">DESCRIPCIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoArchivo.descripcion"
                @input="formTipoArchivo.descripcion = formTipoArchivo.descripcion.toUpperCase()"
                placeholder="EJ: DOCUMENTO PDF"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">EXTENSIÓN:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formTipoArchivo.extension"
                placeholder="EJ: .PDF"
                required
              >
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">CANCELAR</button>
              <button type="submit" class="btn-primary">
                💾 {{ editando ? 'ACTUALIZAR' : 'GUARDAR' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import * as mantenedoresService from '@/services/mantenedoresService'

export default {
  name: 'MantenedoresScouts',
  setup() {
    // Estado reactivo
    const activeTab = ref('zonas')
    const modalActivo = ref('')
    const editando = ref(false)
    const tipoElemento = ref('')
    const elementoSeleccionado = ref(null)
    const isDropdownOpen = ref(false)
    const dropdownContainer = ref(null)
    const cargando = ref(false)
    const error = ref(null)
    
    // Estados de búsqueda
    const searchZonas = ref('')
    const searchDistritos = ref('')
    const searchGrupos = ref('')
    const searchComunas = ref('')
    const filtroZona = ref('')
    const filtroDistrito = ref('')

    // Tabs de navegación (sidebar)
    const tabs = [
      { id: 'zonas', label: 'Zonas', icon: '🗺️' },
      { id: 'distritos', label: 'Distritos', icon: '📍' },
      { id: 'grupos', label: 'Grupos', icon: '👥' },
      { id: 'ramas', label: 'Ramas', icon: '🏕️' },
      { id: 'tipos-curso', label: 'Tipos Curso', icon: '📚' },
      { id: 'cargos', label: 'Cargos', icon: '👔' },
      { id: 'alimentacion', label: 'Alimentación', icon: '🍽️' },
      { id: 'comunas', label: 'Comunas', icon: '🏘️' },
      { id: 'provincias', label: 'Provincias', icon: '🏞️' },
      { id: 'regiones', label: 'Regiones', icon: '🗾' },
      { id: 'niveles', label: 'Niveles', icon: '📊' },
      { id: 'estados-civiles', label: 'Estado Civil', icon: '💑' },
      { id: 'roles', label: 'Roles', icon: '👤' },
      { id: 'conceptos-contables', label: 'Conceptos Contables', icon: '💰' },
      { id: 'tipos-archivo', label: 'Tipos de Archivo', icon: '📁' }
    ]

    // Datos reactivos para todos los mantenedores (inicialmente vacíos, se llenan desde la API)
    const zonas = ref([])
    const distritos = ref([])
    const grupos = ref([])
    const ramas = ref([])
    const tiposCurso = ref([])
    const cargos = ref([])
    const alimentacion = ref([])
    const comunas = ref([])
    const provincias = ref([])
    const regiones = ref([])
    const niveles = ref([])
    const estadosCiviles = ref([])
    const roles = ref([])
    const conceptosContables = ref([])
    const tiposArchivo = ref([])

    // Carga inicial de todos los mantenedores
    const cargarDatos = async () => {
      cargando.value = true
      try {
        // Obtener raw desde API
        const rawZonas = await mantenedoresService.zona.list().catch(() => [])
        const rawDistritos = await mantenedoresService.distrito.list().catch(() => [])
        const rawGrupos = await mantenedoresService.grupo.list().catch(() => [])
        const rawRamas = await mantenedoresService.rama.list().catch(() => [])
        const rawTiposCurso = await mantenedoresService.tipoCursos.list().catch(() => [])
        const rawCargos = await mantenedoresService.cargo.list().catch(() => [])
        const rawAlimentacion = await mantenedoresService.alimentacion.list().catch(() => [])
        const rawComunas = await mantenedoresService.comuna.list().catch(() => [])
        const rawProvincias = await mantenedoresService.provincia.list().catch(() => [])
        const rawRegiones = await mantenedoresService.region.list().catch(() => [])
        const rawNiveles = await mantenedoresService.nivel.list().catch(() => [])
        const rawEstadosCiviles = await mantenedoresService.estadoCivil.list().catch(() => [])
        const rawRoles = await mantenedoresService.rol.list().catch(() => [])
        const rawConceptos = await mantenedoresService.conceptoContable.list().catch(() => [])
        const rawTiposArchivo = await mantenedoresService.tipoArchivos.list().catch(() => [])

        // Normalizar campos de la API (mayúsculas/DB) a forma usada en la UI
        zonas.value = (rawZonas || []).map(z => ({ id: z.ZON_ID ?? z.id, descripcion: z.ZON_DESCRIPCION ?? z.descripcion, unilateral: z.ZON_UNILATERAL ?? z.unilateral, vigente: z.ZON_VIGENTE ?? z.vigente }))
        distritos.value = (rawDistritos || []).map(d => ({ id: d.DIS_ID ?? d.id, descripcion: d.DIS_DESCRIPCION ?? d.descripcion, zona_id: (d.ZON_ID?.ZON_ID) ?? d.ZON_ID ?? d.zona_id, vigente: d.DIS_VIGENTE ?? d.vigente }))
        grupos.value = (rawGrupos || []).map(g => ({ id: g.GRU_ID ?? g.id, descripcion: g.GRU_DESCRIPCION ?? g.descripcion, distrito_id: (g.DIS_ID?.DIS_ID) ?? g.DIS_ID ?? g.distrito_id, vigente: g.GRU_VIGENTE ?? g.vigente }))
        ramas.value = (rawRamas || []).map(r => ({ id: r.RAM_ID ?? r.id, descripcion: r.RAM_DESCRIPCION ?? r.descripcion, vigente: r.RAM_VIGENTE ?? r.vigente }))
        tiposCurso.value = (rawTiposCurso || []).map(t => ({ id: t.TCU_ID ?? t.id, descripcion: t.TCU_DESCRIPCION ?? t.descripcion, tipo: t.TCU_TIPO ?? t.tipo, cant_participante: t.TCU_CANT_PARTICIPANTE ?? t.cant_participante, vigente: t.TCU_VIGENTE ?? t.vigente }))
        cargos.value = (rawCargos || []).map(c => ({ id: c.CAR_ID ?? c.id, descripcion: c.CAR_DESCRIPCION ?? c.descripcion, vigente: c.CAR_VIGENTE ?? c.vigente }))
        alimentacion.value = (rawAlimentacion || []).map(a => ({ id: a.ALI_ID ?? a.id, descripcion: a.ALI_DESCRIPCION ?? a.descripcion, tipo: a.ALI_TIPO ?? a.tipo, vigente: a.ALI_VIGENTE ?? a.vigente }))
        comunas.value = (rawComunas || []).map(c => ({ id: c.COM_ID ?? c.id, descripcion: c.COM_DESCRIPCION ?? c.descripcion, provincia_id: (c.PRO_ID?.PRO_ID) ?? c.PRO_ID ?? c.provincia_id, vigente: c.COM_VIGENTE ?? c.vigente }))
        provincias.value = (rawProvincias || []).map(p => ({ id: p.PRO_ID ?? p.id, descripcion: p.PRO_DESCRIPCION ?? p.descripcion, region_id: (p.REG_ID?.REG_ID) ?? p.REG_ID ?? p.region_id, vigente: p.PRO_VIGENTE ?? p.vigente }))
        regiones.value = (rawRegiones || []).map(rg => ({ id: rg.REG_ID ?? rg.id, descripcion: rg.REG_DESCRIPCION ?? rg.descripcion, vigente: rg.REG_VIGENTE ?? rg.vigente }))
        niveles.value = (rawNiveles || []).map(n => ({ id: n.NIV_ID ?? n.id, descripcion: n.NIV_DESCRIPCION ?? n.descripcion, orden: n.NIV_ORDEN ?? n.orden, vigente: n.NIV_VIGENTE ?? n.vigente }))
        estadosCiviles.value = (rawEstadosCiviles || []).map(e => ({ id: e.ESC_ID ?? e.id, descripcion: e.ESC_DESCRIPCION ?? e.descripcion, vigente: e.ESC_VIGENTE ?? e.vigente }))
        roles.value = (rawRoles || []).map(r => ({ id: r.ROL_ID ?? r.id, descripcion: r.ROL_DESCRIPCION ?? r.descripcion, tipo: r.ROL_TIPO ?? r.tipo, vigente: r.ROL_VIGENTE ?? r.vigente }))
        conceptosContables.value = (rawConceptos || []).map(c => ({ id: c.COC_ID ?? c.id, descripcion: c.COC_DESCRIPCION ?? c.descripcion, vigente: c.COC_VIGENTE ?? c.vigente }))
        tiposArchivo.value = (rawTiposArchivo || []).map(t => ({ id: t.TAR_ID ?? t.id, descripcion: t.TAR_DESCRIPCION ?? t.descripcion, extension: t.TAR_EXTENSION ?? t.extension, vigente: t.TAR_VIGENTE ?? t.vigente }))
      } catch (err) {
        error.value = 'Error al cargar datos: ' + err.message
      } finally {
        cargando.value = false
      }
    }

    onMounted(() => {
      cargarDatos()
      document.addEventListener('click', handleClickOutside)
    })

    // Recarga tras crear/editar/eliminar
    const recargar = cargarDatos

    // Formularios
    const formZona = reactive({
      id: null,
      descripcion: '',
      unilateral: false,
      vigente: true
    })

    const formDistrito = reactive({
      id: null,
      descripcion: '',
      zona_id: null,
      vigente: true
    })

    const formGrupo = reactive({
      id: null,
      descripcion: '',
      distrito_id: null,
      vigente: true
    })

    const formRama = reactive({
      id: null,
      descripcion: '',
      vigente: true
    })

    // Formularios adicionales para otros mantenedores
    const formTipoCurso = reactive({ id: null, descripcion: '', tipo: 1, cant_participante: null, vigente: true })
    const formCargo = reactive({ id: null, descripcion: '', vigente: true })
    const formAlimentacion = reactive({ id: null, descripcion: '', tipo: 1, vigente: true })
    const formComuna = reactive({ id: null, descripcion: '', provincia_id: null, vigente: true })
    const formProvincia = reactive({ id: null, descripcion: '', region_id: null, vigente: true })
    const formRegion = reactive({ id: null, descripcion: '', vigente: true })
    const formNivel = reactive({ id: null, descripcion: '', orden: 1, vigente: true })
    const formEstadoCivil = reactive({ id: null, descripcion: '', vigente: true })
    const formRol = reactive({ id: null, descripcion: '', tipo: 1, vigente: true })
    const formConceptoContable = reactive({ id: null, descripcion: '', tipo: '', vigente: true })
    const formTipoArchivo = reactive({ id: null, descripcion: '', extension: '', vigente: true })

    // Computed properties para filtros
    const filteredZonas = computed(() => {
      if (!searchZonas.value) return zonas.value
      return zonas.value.filter(zona => 
        zona.descripcion.toLowerCase().includes(searchZonas.value.toLowerCase())
      )
    })

    const filteredDistritos = computed(() => {
      let filtered = distritos.value
      
      if (searchDistritos.value) {
        filtered = filtered.filter(distrito => 
          distrito.descripcion.toLowerCase().includes(searchDistritos.value.toLowerCase())
        )
      }
      
      if (filtroZona.value) {
        const zona = zonas.value.find(z => z.descripcion === filtroZona.value)
        if (zona) {
          filtered = filtered.filter(distrito => distrito.zona_id === zona.id)
        }
      }
      
      return filtered
    })

    const filteredGrupos = computed(() => {
      let filtered = grupos.value
      
      if (searchGrupos.value) {
        filtered = filtered.filter(grupo => 
          grupo.descripcion.toLowerCase().includes(searchGrupos.value.toLowerCase())
        )
      }
      
      if (filtroDistrito.value) {
        const distrito = distritos.value.find(d => d.descripcion === filtroDistrito.value)
        if (distrito) {
          filtered = filtered.filter(grupo => grupo.distrito_id === distrito.id)
        }
      }
      
      return filtered
    })

    // Métodos de búsqueda activados por los botones "Buscar"
    const buscarZonas = () => {
      searchZonas.value = (searchZonas.value || '').trim()
    }

    const buscarDistritos = () => {
      searchDistritos.value = (searchDistritos.value || '').trim()
    }

    const buscarGrupos = () => {
      searchGrupos.value = (searchGrupos.value || '').trim()
    }

    const buscarComunas = () => {
      searchComunas.value = (searchComunas.value || '').trim()
    }

    // Métodos auxiliares
    const getZonaNombre = (zonaId) => {
      const zona = zonas.value.find(z => z.id === zonaId)
      return zona ? zona.descripcion : 'NO ENCONTRADA'
    }

    const getDistritoNombre = (distritoId) => {
      const distrito = distritos.value.find(d => d.id === distritoId)
      return distrito ? distrito.descripcion : 'NO ENCONTRADO'
    }

    const getProvinciaNombre = (provinciaId) => {
      const provincia = provincias.value.find(p => p.id === provinciaId)
      return provincia ? provincia.descripcion : 'NO ENCONTRADA'
    }

    const getRegionNombre = (regionId) => {
      const region = regiones.value.find(r => r.id === regionId)
      return region ? region.descripcion : 'NO ENCONTRADA'
    }

    const getTipoNombre = (tipo) => {
      const nombres = {
        'zona': 'ZONA',
        'distrito': 'DISTRITO',
        'grupo': 'GRUPO',
        'rama': 'RAMA',
        'tipoCurso': 'TIPO DE CURSO',
        'cargo': 'CARGO',
        'alimentacion': 'ALIMENTACIÓN',
        'comuna': 'COMUNA',
        'provincia': 'PROVINCIA',
        'region': 'REGIÓN',
        'nivel': 'NIVEL',
        'estadoCivil': 'ESTADO CIVIL',
        'rol': 'ROL',
        'conceptoContable': 'CONCEPTO CONTABLE',
        'tipoArchivo': 'TIPO DE ARCHIVO'
      }
      return nombres[tipo] || 'ELEMENTO'
    }

    const getRelacionNombre = (tipo) => {
      const relaciones = {
        'distrito': 'ZONA',
        'grupo': 'DISTRITO',
        'comuna': 'PROVINCIA',
        'provincia': 'REGIÓN'
      }
      return relaciones[tipo] || ''
    }

    const getRelacionValor = (tipo) => {
      switch (tipo) {
        case 'distrito':
          return getZonaNombre(elementoSeleccionado.value.zona_id)
        case 'grupo':
          return getDistritoNombre(elementoSeleccionado.value.distrito_id)
        case 'comuna':
          return getProvinciaNombre(elementoSeleccionado.value.provincia_id)
        case 'provincia':
          return getRegionNombre(elementoSeleccionado.value.region_id)
        default:
          return ''
      }
    }

    // Métodos para el dropdown personalizado
    const getSelectedTabInfo = () => {
      const tab = tabs.find(t => t.id === activeTab.value)
      return tab || tabs[0]
    }

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const selectTab = (tabId) => {
      activeTab.value = tabId
      isDropdownOpen.value = false // Cerrar dropdown después de seleccionar
    }

    // Cerrar dropdown al hacer clic fuera
    const handleClickOutside = (event) => {
      if (dropdownContainer.value && !dropdownContainer.value.contains(event.target)) {
        isDropdownOpen.value = false
      }
    }

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    // Métodos principales
    const abrirModalCrear = (tipo) => {
      modalActivo.value = `crear-${tipo}`
      editando.value = false
      tipoElemento.value = tipo
      elementoSeleccionado.value = null
      limpiarFormularios()
    }

    const verElemento = (tipo, elemento) => {
      modalActivo.value = 'ver'
      editando.value = false
      tipoElemento.value = tipo
      elementoSeleccionado.value = elemento
    }

    const editarElemento = (tipo, elemento) => {
      modalActivo.value = `editar-${tipo}`
      editando.value = true
      tipoElemento.value = tipo
      elementoSeleccionado.value = elemento
      cargarDatosFormulario(tipo, elemento)
    }

    // Nuevos métodos para anular y habilitar
    const anularElemento = async (tipo, elemento) => {
      if (!confirm('¿ESTÁ SEGURO QUE DESEA ANULAR ESTE REGISTRO? ESTA ACCIÓN NO SE PUEDE DESHACER.')) {
        return
      }
      
      try {
        const datosAPI = {
          ...elemento,
          vigente: false
        }
        
        switch (tipo) {
          case 'zona':
            await mantenedoresService.zona.update(elemento.id, datosAPI)
            break
          case 'distrito':
            await mantenedoresService.distrito.update(elemento.id, datosAPI)
            break
          case 'grupo':
            await mantenedoresService.grupo.update(elemento.id, datosAPI)
            break
          case 'rama':
            await mantenedoresService.rama.update(elemento.id, datosAPI)
            break
          case 'tipoCurso':
            await mantenedoresService.tipoCursos.update(elemento.id, datosAPI)
            break
          case 'cargo':
            await mantenedoresService.cargo.update(elemento.id, datosAPI)
            break
          case 'alimentacion':
            await mantenedoresService.alimentacion.update(elemento.id, datosAPI)
            break
          case 'comuna':
            await mantenedoresService.comuna.update(elemento.id, datosAPI)
            break
          case 'provincia':
            await mantenedoresService.provincia.update(elemento.id, datosAPI)
            break
          case 'region':
            await mantenedoresService.region.update(elemento.id, datosAPI)
            break
          case 'nivel':
            await mantenedoresService.nivel.update(elemento.id, datosAPI)
            break
          case 'estadoCivil':
            await mantenedoresService.estadoCivil.update(elemento.id, datosAPI)
            break
          case 'rol':
            await mantenedoresService.rol.update(elemento.id, datosAPI)
            break
          case 'conceptoContable':
            await mantenedoresService.conceptoContable.update(elemento.id, datosAPI)
            break
          case 'tipoArchivo':
            await mantenedoresService.tipoArchivos.update(elemento.id, datosAPI)
            break
        }
        
        await recargar()
      } catch (err) {
        error.value = 'ERROR AL ANULAR ELEMENTO: ' + err.message
      }
    }

    const habilitarElemento = async (tipo, elemento) => {
      try {
        const datosAPI = {
          ...elemento,
          vigente: true
        }
        
        switch (tipo) {
          case 'zona':
            await mantenedoresService.zona.update(elemento.id, datosAPI)
            break
          case 'distrito':
            await mantenedoresService.distrito.update(elemento.id, datosAPI)
            break
          case 'grupo':
            await mantenedoresService.grupo.update(elemento.id, datosAPI)
            break
          case 'rama':
            await mantenedoresService.rama.update(elemento.id, datosAPI)
            break
          case 'tipoCurso':
            await mantenedoresService.tipoCursos.update(elemento.id, datosAPI)
            break
          case 'cargo':
            await mantenedoresService.cargo.update(elemento.id, datosAPI)
            break
          case 'alimentacion':
            await mantenedoresService.alimentacion.update(elemento.id, datosAPI)
            break
          case 'comuna':
            await mantenedoresService.comuna.update(elemento.id, datosAPI)
            break
          case 'provincia':
            await mantenedoresService.provincia.update(elemento.id, datosAPI)
            break
          case 'region':
            await mantenedoresService.region.update(elemento.id, datosAPI)
            break
          case 'nivel':
            await mantenedoresService.nivel.update(elemento.id, datosAPI)
            break
          case 'estadoCivil':
            await mantenedoresService.estadoCivil.update(elemento.id, datosAPI)
            break
          case 'rol':
            await mantenedoresService.rol.update(elemento.id, datosAPI)
            break
          case 'conceptoContable':
            await mantenedoresService.conceptoContable.update(elemento.id, datosAPI)
            break
          case 'tipoArchivo':
            await mantenedoresService.tipoArchivos.update(elemento.id, datosAPI)
            break
        }
        
        await recargar()
      } catch (err) {
        error.value = 'ERROR AL HABILITAR ELEMENTO: ' + err.message
      }
    }

    const cargarDatosFormulario = (tipo, elemento) => {
      switch (tipo) {
        case 'zona':
          Object.assign(formZona, elemento)
          break
        case 'distrito':
          Object.assign(formDistrito, elemento)
          break
        case 'grupo':
          Object.assign(formGrupo, elemento)
          break
        case 'rama':
          Object.assign(formRama, elemento)
          break
        case 'tipoCurso':
          Object.assign(formTipoCurso, { id: elemento.id, descripcion: elemento.descripcion, tipo: elemento.tipo, cant_participante: elemento.cant_participante, vigente: elemento.vigente })
          break
        case 'cargo':
          Object.assign(formCargo, elemento)
          break
        case 'alimentacion':
          Object.assign(formAlimentacion, { id: elemento.id, descripcion: elemento.descripcion, tipo: elemento.tipo, vigente: elemento.vigente })
          break
        case 'comuna':
          Object.assign(formComuna, elemento)
          break
        case 'provincia':
          Object.assign(formProvincia, elemento)
          break
        case 'region':
          Object.assign(formRegion, elemento)
          break
        case 'nivel':
          Object.assign(formNivel, elemento)
          break
        case 'estadoCivil':
          Object.assign(formEstadoCivil, elemento)
          break
        case 'rol':
          Object.assign(formRol, { id: elemento.id, descripcion: elemento.descripcion, tipo: elemento.tipo, vigente: elemento.vigente })
          break
        case 'conceptoContable':
          Object.assign(formConceptoContable, elemento)
          break
        case 'tipoArchivo':
          Object.assign(formTipoArchivo, elemento)
          break
      }
    }

    const limpiarFormularios = () => {
      Object.assign(formZona, {
        id: null,
        descripcion: '',
        unilateral: false,
        vigente: true
      })
      Object.assign(formDistrito, {
        id: null,
        descripcion: '',
        zona_id: null,
        vigente: true
      })
      Object.assign(formGrupo, {
        id: null,
        descripcion: '',
        distrito_id: null,
        vigente: true
      })
      Object.assign(formRama, {
        id: null,
        descripcion: '',
        vigente: true
      })
      Object.assign(formTipoCurso, { id: null, descripcion: '', tipo: 1, cant_participante: null, vigente: true })
      Object.assign(formCargo, { id: null, descripcion: '', vigente: true })
      Object.assign(formAlimentacion, { id: null, descripcion: '', tipo: 1, vigente: true })
      Object.assign(formComuna, { id: null, descripcion: '', provincia_id: null, vigente: true })
      Object.assign(formProvincia, { id: null, descripcion: '', region_id: null, vigente: true })
      Object.assign(formRegion, { id: null, descripcion: '', vigente: true })
      Object.assign(formNivel, { id: null, descripcion: '', orden: 1, vigente: true })
      Object.assign(formEstadoCivil, { id: null, descripcion: '', vigente: true })
      Object.assign(formRol, { id: null, descripcion: '', tipo: 1, vigente: true })
      Object.assign(formConceptoContable, { id: null, descripcion: '', tipo: '', vigente: true })
      Object.assign(formTipoArchivo, { id: null, descripcion: '', extension: '', vigente: true })
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      editando.value = false
      tipoElemento.value = ''
      elementoSeleccionado.value = null
      limpiarFormularios()
    }

    // Métodos de guardado

    // Métodos CRUD para zonas, distritos, grupos, ramas
    const guardarZona = async () => {
      try {
        const payload = {
          ZON_DESCRIPCION: formZona.descripcion,
          ZON_UNILATERAL: !!formZona.unilateral,
          ZON_VIGENTE: !!formZona.vigente
        }
        if (editando.value) {
          await mantenedoresService.zona.update(formZona.id, payload)
        } else {
          await mantenedoresService.zona.create(payload)
        }
      } catch (err) {
        console.error('Error guardarZona:', err)
      } finally {
        cerrarModal()
        recargar()
      }
    }

    const guardarDistrito = async () => {
      try {
        const payload = {
          DIS_DESCRIPCION: formDistrito.descripcion,
          ZON_ID: formDistrito.zona_id,
          DIS_VIGENTE: !!formDistrito.vigente
        }
        if (editando.value) {
          await mantenedoresService.distrito.update(formDistrito.id, payload)
        } else {
          await mantenedoresService.distrito.create(payload)
        }
      } catch (err) {
        console.error('Error guardarDistrito:', err)
      } finally {
        cerrarModal()
        recargar()
      }
    }

    const guardarGrupo = async () => {
      try {
        const payload = {
          GRU_DESCRIPCION: formGrupo.descripcion,
          DIS_ID: formGrupo.distrito_id,
          GRU_VIGENTE: !!formGrupo.vigente
        }
        if (editando.value) {
          await mantenedoresService.grupo.update(formGrupo.id, payload)
        } else {
          await mantenedoresService.grupo.create(payload)
        }
      } catch (err) {
        console.error('Error guardarGrupo:', err)
      } finally {
        cerrarModal()
        recargar()
      }
    }

    const guardarRama = async () => {
      try {
        const payload = {
          RAM_DESCRIPCION: formRama.descripcion,
          RAM_VIGENTE: !!formRama.vigente
        }
        if (editando.value) {
          await mantenedoresService.rama.update(formRama.id, payload)
        } else {
          await mantenedoresService.rama.create(payload)
        }
      } catch (err) {
        console.error('Error guardarRama:', err)
      } finally {
        cerrarModal()
        recargar()
      }
    }

    // Guardar otros mantenedores
    const guardarTipoCurso = async () => {
      try {
        const payload = { TCU_DESCRIPCION: formTipoCurso.descripcion, TCU_TIPO: formTipoCurso.tipo, TCU_CANT_PARTICIPANTE: formTipoCurso.cant_participante, TCU_VIGENTE: !!formTipoCurso.vigente }
        if (editando.value) await mantenedoresService.tipoCursos.update(formTipoCurso.id, payload)
        else await mantenedoresService.tipoCursos.create(payload)
      } catch (err) { console.error('Error guardarTipoCurso', err) } finally { cerrarModal(); recargar() }
    }

    const guardarCargo = async () => {
      try { const payload = { CAR_DESCRIPCION: formCargo.descripcion, CAR_VIGENTE: !!formCargo.vigente }; if (editando.value) await mantenedoresService.cargo.update(formCargo.id, payload); else await mantenedoresService.cargo.create(payload) } catch (err) { console.error('Error guardarCargo', err) } finally { cerrarModal(); recargar() }
    }

    const guardarAlimentacion = async () => {
      try { const payload = { ALI_DESCRIPCION: formAlimentacion.descripcion, ALI_TIPO: formAlimentacion.tipo, ALI_VIGENTE: !!formAlimentacion.vigente }; if (editando.value) await mantenedoresService.alimentacion.update(formAlimentacion.id, payload); else await mantenedoresService.alimentacion.create(payload) } catch (err) { console.error('Error guardarAlimentacion', err) } finally { cerrarModal(); recargar() }
    }

    const guardarComuna = async () => {
      try { const payload = { COM_DESCRIPCION: formComuna.descripcion, PRO_ID: formComuna.provincia_id, COM_VIGENTE: !!formComuna.vigente }; if (editando.value) await mantenedoresService.comuna.update(formComuna.id, payload); else await mantenedoresService.comuna.create(payload) } catch (err) { console.error('Error guardarComuna', err) } finally { cerrarModal(); recargar() }
    }

    const guardarProvincia = async () => {
      try { const payload = { PRO_DESCRIPCION: formProvincia.descripcion, REG_ID: formProvincia.region_id, PRO_VIGENTE: !!formProvincia.vigente }; if (editando.value) await mantenedoresService.provincia.update(formProvincia.id, payload); else await mantenedoresService.provincia.create(payload) } catch (err) { console.error('Error guardarProvincia', err) } finally { cerrarModal(); recargar() }
    }

    const guardarRegion = async () => {
      try { const payload = { REG_DESCRIPCION: formRegion.descripcion, REG_VIGENTE: !!formRegion.vigente }; if (editando.value) await mantenedoresService.region.update(formRegion.id, payload); else await mantenedoresService.region.create(payload) } catch (err) { console.error('Error guardarRegion', err) } finally { cerrarModal(); recargar() }
    }

    const guardarNivel = async () => {
      try { const payload = { NIV_DESCRIPCION: formNivel.descripcion, NIV_ORDEN: formNivel.orden, NIV_VIGENTE: !!formNivel.vigente }; if (editando.value) await mantenedoresService.nivel.update(formNivel.id, payload); else await mantenedoresService.nivel.create(payload) } catch (err) { console.error('Error guardarNivel', err) } finally { cerrarModal(); recargar() }
    }

    const guardarEstadoCivil = async () => {
      try { const payload = { ESC_DESCRIPCION: formEstadoCivil.descripcion, ESC_VIGENTE: !!formEstadoCivil.vigente }; if (editando.value) await mantenedoresService.estadoCivil.update(formEstadoCivil.id, payload); else await mantenedoresService.estadoCivil.create(payload) } catch (err) { console.error('Error guardarEstadoCivil', err) } finally { cerrarModal(); recargar() }
    }

    const guardarRol = async () => {
      try { const payload = { ROL_DESCRIPCION: formRol.descripcion, ROL_TIPO: formRol.tipo, ROL_VIGENTE: !!formRol.vigente }; if (editando.value) await mantenedoresService.rol.update(formRol.id, payload); else await mantenedoresService.rol.create(payload) } catch (err) { console.error('Error guardarRol', err) } finally { cerrarModal(); recargar() }
    }

    const guardarConceptoContable = async () => {
      try { const payload = { COC_DESCRIPCION: formConceptoContable.descripcion, COC_VIGENTE: !!formConceptoContable.vigente }; if (editando.value) await mantenedoresService.conceptoContable.update(formConceptoContable.id, payload); else await mantenedoresService.conceptoContable.create(payload) } catch (err) { console.error('Error guardarConceptoContable', err) } finally { cerrarModal(); recargar() }
    }

    const guardarTipoArchivo = async () => {
      try { const payload = { TAR_DESCRIPCION: formTipoArchivo.descripcion, TAR_VIGENTE: !!formTipoArchivo.vigente }; if (editando.value) await mantenedoresService.tipoArchivos.update(formTipoArchivo.id, payload); else await mantenedoresService.tipoArchivos.create(payload) } catch (err) { console.error('Error guardarTipoArchivo', err) } finally { cerrarModal(); recargar() }
    }

    return {
      activeTab,
      modalActivo,
      editando,
      tipoElemento,
      elementoSeleccionado,
      isDropdownOpen,
      dropdownContainer,
      cargando,
      error,
      searchZonas,
      searchDistritos,
      searchGrupos,
      searchComunas,
      filtroZona,
      filtroDistrito,
      tabs,
      zonas,
      distritos,
      grupos,
      ramas,
      tiposCurso,
      cargos,
      alimentacion,
      comunas,
      provincias,
      regiones,
      niveles,
      estadosCiviles,
      roles,
      conceptosContables,
      tiposArchivo,
      formZona,
      formDistrito,
      formGrupo,
      formRama,
      formTipoCurso,
      formCargo,
      formAlimentacion,
      formComuna,
      formProvincia,
      formRegion,
      formNivel,
      formEstadoCivil,
      formRol,
      formConceptoContable,
      formTipoArchivo,
      filteredZonas,
      filteredDistritos,
      filteredGrupos,
      getZonaNombre,
      getDistritoNombre,
      getProvinciaNombre,
      getRegionNombre,
      getTipoNombre,
      getRelacionNombre,
      getRelacionValor,
      getSelectedTabInfo,
      toggleDropdown,
      selectTab,
      abrirModalCrear,
      verElemento,
      editarElemento,
      anularElemento,
      habilitarElemento,
      buscarZonas,
      buscarDistritos,
      buscarGrupos,
      buscarComunas,
      cerrarModal,
      guardarZona,
      guardarDistrito,
      guardarGrupo,
      guardarRama,
      guardarTipoCurso,
      guardarCargo,
      guardarAlimentacion,
      guardarComuna,
      guardarProvincia,
      guardarRegion,
      guardarNivel,
      guardarEstadoCivil,
      guardarRol,
      guardarConceptoContable,
      guardarTipoArchivo,
      recargar
    }
  }
} 
</script>

<style scoped>
.mantenedores-scouts {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(60,60,60,0.08);
  padding: 24px;
  margin-bottom: 24px;
  color: #111;
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
  width: 100%;
  height: 100%;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  min-height: calc(100vh - var(--navbar-height, 64px));
  margin-top: 0px;
  border-radius: 6px;
  overflow: hidden;
}

/* Error Alert */
.error-alert {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 15px 20px;
  margin: 10px 20px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-alert p {
  margin: 0;
}

.error-alert button {
  background: none;
  border: none;
  color: #721c24;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loading Indicator */
.loading-indicator {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
  padding: 15px 20px;
  margin: 10px 20px;
  border-radius: 8px;
  text-align: center;
}

/* Selector de Mantenedores Fijo - CORREGIDO */
.mantenedor-selector-fixed {
  background: #1a237e;
  color: white;
  padding: 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  width: 100%;
}

.selector-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  max-width: 100%;
  margin: 0 auto;
}

.selector-header {
  flex-shrink: 0;
}

.selector-header h2 {
  margin: 0;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
}

/* Nuevos estilos para el dropdown personalizado - MEJORADO */
.selector-dropdown {
  position: relative;
  max-width: 400px;
  width: 100%;
  margin-left: 20px;
}

.mantenedor-dropdown-toggle {
  width: 100%;
  padding: 12px 45px 12px 16px;
  border: 2px solid #3949ab;
  border-radius: 8px;
  background: white;
  color: #333;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 500;
}

.mantenedor-dropdown-toggle:hover {
  border-color: #ff6b35;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.2);
}

.mantenedor-dropdown-toggle.active {
  border-color: #ff6b35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.selected-option {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-weight: 500;
}

.dropdown-icon {
  color: #3949ab;
  transition: transform 0.3s ease;
  font-size: 0.9rem;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #3949ab;
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1001;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item.active {
  background: #e3f2fd;
  color: #3949ab;
  font-weight: 600;
}

.dropdown-item-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.dropdown-item-text {
  color: #333;
  font-weight: 500;
  flex: 1;
}

.dropdown-item.active .dropdown-item-text {
  color: #3949ab;
  font-weight: 600;
}

.dropdown-item:hover .dropdown-item-text {
  color: #1a237e;
}

/* Main Content Expandido */
.main-content-expanded {
  flex: 1;
  padding: 0;
  min-height: calc(100vh - var(--navbar-height, 64px) - 80px);
  width: 100%;
  margin: 0;
}

.header-expanded {
  background: #1a237e;
  color: white;
  padding: 30px 20px;
  margin: 0;
  width: 100%;
}

.header-expanded h1 {
  font-size: 1.8rem;
  margin-bottom: 8px;
  margin-top: 0;
}

.header-expanded p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.mantenedor-section-expanded {
  padding: 30px 20px;
  animation: fadeIn 0.5s ease;
  width: 100%;
  margin: 0;
  box-sizing: border-box;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 3px solid #3949ab;
  width: 100%;
  box-sizing: border-box;
}

.mantenedor-header h2 {
  color: #1a237e;
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.btn-primary {
  background: linear-gradient(180deg,#2b6cb0,#154c8c);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 14px;
  min-height: 44px;
  box-shadow: 0 6px 18px rgba(33,78,156,0.12);
}

.btn-primary:hover {
  background: linear-gradient(180deg,#1e40af,#1e3a8a);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(57, 73, 171, 0.3);
}

.search-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: flex-end;
  width: 100%;
  box-sizing: border-box;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #3949ab;
  box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
}

.select-filter {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 200px;
  box-sizing: border-box;
}

.table-container-expanded {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.data-table-expanded {
  width: 100%;
  border-collapse: collapse;
  box-sizing: border-box;
}

.data-table-expanded thead {
  background: #f8f9fa;
}

.data-table-expanded th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #1a237e;
  border-bottom: 2px solid #e1e5e9;
}

.data-table-expanded td {
  padding: 14px 12px;
  border-bottom: 1px solid #e1e5e9;
}

.data-table-expanded tr:hover {
  background: #f8f9fa;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-height: 32px;
}

.btn-view {
  background: #e3f2fd;
  color: #1565c0;
}

.btn-edit {
  background: #fff3cd;
  color: #856404;
}

.btn-anular {
  background: #f8d7da;
  color: #721c24;
}

.btn-habilitar {
  background: #d4edda;
  color: #155724;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 25px 30px 20px;
  border-bottom: 2px solid #3949ab;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #1a237e;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #1a237e;
}

.modal-body {
  padding: 25px 30px;
}

/* View Container Styles */
.view-container {
  margin-bottom: 20px;
}

.view-group {
  margin-bottom: 20px;
}

.view-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #39424b;
}

.view-value {
  padding: 12px 16px;
  background: #f8f9fa;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 14px;
  min-height: 44px;
}

.btn-secondary:hover {
  background: #5a6268;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #39424b;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3949ab;
  box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-checkbox input {
  width: 18px;
  height: 18px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 768px) {
  .selector-container {
    flex-direction: column;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .selector-dropdown {
    margin-left: 0;
    max-width: 100%;
  }
  
  .mantenedor-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .search-input, .select-filter {
    min-width: 100%;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .table-container-expanded {
    overflow-x: auto;
  }
  
  .data-table-expanded {
    min-width: 600px;
  }
  
  .dropdown-menu {
    max-height: 300px;
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Estilos adaptados de message.txt */
.btn-standard {
  min-width: 160px !important;
  padding: 10px 16px !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(40,92,168,0.08) !important;
  border: none !important;
  transition: all 0.3s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.btn-standard:hover {
  filter: brightness(0.95) !important;
  box-shadow: 0 4px 16px rgba(40,92,168,0.13) !important;
  transform: translateY(-1px) !important;
}

.estado { 
  padding: 6px 12px; 
  border-radius: 12px; 
  font-size: 12px; 
  white-space: nowrap;
  font-weight: 600;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.estado.activo { 
  background: #d1fae5; 
  color: #065f46;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.estado.inactivo { 
  background: #fee2e2; 
  color: #991b1b;
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.estado.vigente { background:#d1fae5; color:#065f46 }
.estado.no-vigente { background:#fbbf24; color:#1f2937 }
.estado.anulado { background:#e5e7eb; color:#374151; text-decoration: line-through; }

/* Mejoras responsivas adicionales */
@media (max-width: 480px) {
  .mantenedores-scouts {
    padding: 16px;
  }
  
  .mantenedor-section-expanded {
    padding: 20px 16px;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    justify-content: center;
  }
  
  .actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-action {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 1024px) {
  .mantenedores-scouts {
    margin: 12px;
    width: calc(100% - 24px);
  }
}
</style>
[file content end]