<template>
  <div class="mantenedores-scouts">
    <!-- Main Content (sidebar propia removida; se usa la barra lateral global) -->
      <div class="main-content">
      <!-- Header eliminado a petición: se muestra directamente el contenido -->
      
      <!-- Zonas -->
      <div v-if="activeTab === 'zonas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Zonas</h2>
          <button class="btn-primary" @click="abrirModalCrear('zona')">
            + Nueva Zona
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las zonas son agrupaciones geográficas de distritos scouts.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar zona por descripción..."
            v-model="searchZonas"
          >
          <button class="btn-primary">Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Unilateral</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="zona in filteredZonas" :key="zona.id">
                <td>{{ zona.descripcion }}</td>
                <td>{{ zona.unilateral ? 'Sí' : 'No' }}</td>
                <td>
                  <span class="status-badge" :class="zona.vigente ? 'status-active' : 'status-inactive'">
                    {{ zona.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('zona', zona)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('zona', zona)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('zona', zona)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Distritos -->
      <div v-if="activeTab === 'distritos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Distritos</h2>
          <button class="btn-primary" @click="abrirModalCrear('distrito')">
            + Nuevo Distrito
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los distritos agrupan varios grupos scouts dentro de una zona específica.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar distrito..."
            v-model="searchDistritos"
          >
          <select class="select-filter" v-model="filtroZona">
            <option value="">Todas las zonas</option>
            <option v-for="zona in zonas" :key="zona.id" :value="zona.descripcion">
              {{ zona.descripcion }}
            </option>
          </select>
          <button class="btn-primary">Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Zona</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="distrito in filteredDistritos" :key="distrito.id">
                <td>{{ distrito.descripcion }}</td>
                <td>{{ getZonaNombre(distrito.zona_id) }}</td>
                <td>
                  <span class="status-badge" :class="distrito.vigente ? 'status-active' : 'status-inactive'">
                    {{ distrito.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('distrito', distrito)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('distrito', distrito)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('distrito', distrito)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Grupos Scout -->
      <div v-if="activeTab === 'grupos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Grupos Scout</h2>
          <button class="btn-primary" @click="abrirModalCrear('grupo')">
            + Nuevo Grupo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los grupos scout son las unidades operativas donde se desarrollan las actividades con los jóvenes.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar grupo..."
            v-model="searchGrupos"
          >
          <select class="select-filter" v-model="filtroDistrito">
            <option value="">Todos los distritos</option>
            <option v-for="distrito in distritos" :key="distrito.id" :value="distrito.descripcion">
              {{ distrito.descripcion }}
            </option>
          </select>
          <button class="btn-primary">Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Distrito</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="grupo in filteredGrupos" :key="grupo.id">
                <td>{{ grupo.descripcion }}</td>
                <td>{{ getDistritoNombre(grupo.distrito_id) }}</td>
                <td>
                  <span class="status-badge" :class="grupo.vigente ? 'status-active' : 'status-inactive'">
                    {{ grupo.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('grupo', grupo)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('grupo', grupo)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('grupo', grupo)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Ramas -->
      <div v-if="activeTab === 'ramas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Ramas</h2>
          <button class="btn-primary" @click="abrirModalCrear('rama')">
            + Nueva Rama
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las ramas definen las divisiones por edad dentro del movimiento scout.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rama in ramas" :key="rama.id">
                <td>{{ rama.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="rama.vigente ? 'status-active' : 'status-inactive'">
                    {{ rama.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('rama', rama)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('rama', rama)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('rama', rama)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Tipos de Curso -->
      <div v-if="activeTab === 'tipos-curso'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Tipos de Curso</h2>
          <button class="btn-primary" @click="abrirModalCrear('tipoCurso')">
            + Nuevo Tipo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los tipos de curso definen las categorías de formación disponibles en el sistema.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Tipo</th>
                <th>Cant. Participantes</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoCurso in tiposCurso" :key="tipoCurso.id">
                <td>{{ tipoCurso.descripcion }}</td>
                <td>{{ tipoCurso.tipo }}</td>
                <td>{{ tipoCurso.cant_participante }}</td>
                <td>
                  <span class="status-badge" :class="tipoCurso.vigente ? 'status-active' : 'status-inactive'">
                    {{ tipoCurso.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('tipoCurso', tipoCurso)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('tipoCurso', tipoCurso)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('tipoCurso', tipoCurso)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Cargos -->
      <div v-if="activeTab === 'cargos'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Cargos</h2>
          <button class="btn-primary" @click="abrirModalCrear('cargo')">
            + Nuevo Cargo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los cargos definen las responsabilidades dentro de la organización scout.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cargo in cargos" :key="cargo.id">
                <td>{{ cargo.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="cargo.vigente ? 'status-active' : 'status-inactive'">
                    {{ cargo.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('cargo', cargo)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('cargo', cargo)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('cargo', cargo)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Alimentación -->
      <div v-if="activeTab === 'alimentacion'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Alimentación</h2>
          <button class="btn-primary" @click="abrirModalCrear('alimentacion')">
            + Nueva Alimentación
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Tipos de alimentación disponibles para los participantes de cursos.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="alimentacionItem in alimentacion" :key="alimentacionItem.id">
                <td>{{ alimentacionItem.descripcion }}</td>
                <td>{{ alimentacionItem.tipo }}</td>
                <td>
                  <span class="status-badge" :class="alimentacionItem.vigente ? 'status-active' : 'status-inactive'">
                    {{ alimentacionItem.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('alimentacion', alimentacionItem)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('alimentacion', alimentacionItem)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('alimentacion', alimentacionItem)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Comunas -->
      <div v-if="activeTab === 'comunas'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Comunas</h2>
          <button class="btn-primary" @click="abrirModalCrear('comuna')">
            + Nueva Comuna
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las comunas son divisiones administrativas dentro de las provincias.
          </div>
        </div>
        
        <div class="search-bar">
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar comuna..."
            v-model="searchComunas"
          >
          <button class="btn-primary">Buscar</button>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Provincia</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comuna in comunas" :key="comuna.id">
                <td>{{ comuna.descripcion }}</td>
                <td>{{ getProvinciaNombre(comuna.provincia_id) }}</td>
                <td>
                  <span class="status-badge" :class="comuna.vigente ? 'status-active' : 'status-inactive'">
                    {{ comuna.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('comuna', comuna)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('comuna', comuna)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('comuna', comuna)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Provincias -->
      <div v-if="activeTab === 'provincias'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Provincias</h2>
          <button class="btn-primary" @click="abrirModalCrear('provincia')">
            + Nueva Provincia
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las provincias son divisiones administrativas dentro de las regiones.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Región</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="provincia in provincias" :key="provincia.id">
                <td>{{ provincia.descripcion }}</td>
                <td>{{ getRegionNombre(provincia.region_id) }}</td>
                <td>
                  <span class="status-badge" :class="provincia.vigente ? 'status-active' : 'status-inactive'">
                    {{ provincia.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('provincia', provincia)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('provincia', provincia)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('provincia', provincia)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Regiones -->
      <div v-if="activeTab === 'regiones'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Regiones</h2>
          <button class="btn-primary" @click="abrirModalCrear('region')">
            + Nueva Región
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Las regiones son las principales divisiones territoriales del país.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="region in regiones" :key="region.id">
                <td>{{ region.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="region.vigente ? 'status-active' : 'status-inactive'">
                    {{ region.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('region', region)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('region', region)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('region', region)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Niveles -->
      <div v-if="activeTab === 'niveles'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Niveles</h2>
          <button class="btn-primary" @click="abrirModalCrear('nivel')">
            + Nuevo Nivel
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los niveles definen escalas o rangos dentro de la organización.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="nivel in niveles" :key="nivel.id">
                <td>{{ nivel.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="nivel.vigente ? 'status-active' : 'status-inactive'">
                    {{ nivel.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('nivel', nivel)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('nivel', nivel)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('nivel', nivel)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Estados Civiles -->
      <div v-if="activeTab === 'estados-civiles'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Estados Civiles</h2>
          <button class="btn-primary" @click="abrirModalCrear('estadoCivil')">
            + Nuevo Estado Civil
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los estados civiles definen las situaciones personales de los miembros.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="estadoCivil in estadosCiviles" :key="estadoCivil.id">
                <td>{{ estadoCivil.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="estadoCivil.vigente ? 'status-active' : 'status-inactive'">
                    {{ estadoCivil.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('estadoCivil', estadoCivil)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('estadoCivil', estadoCivil)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('estadoCivil', estadoCivil)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Roles -->
      <div v-if="activeTab === 'roles'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Roles</h2>
          <button class="btn-primary" @click="abrirModalCrear('rol')">
            + Nuevo Rol
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los roles definen las funciones y permisos dentro del sistema.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rol in roles" :key="rol.id">
                <td>{{ rol.descripcion }}</td>
                <td>
                  <span class="status-badge" :class="rol.vigente ? 'status-active' : 'status-inactive'">
                    {{ rol.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('rol', rol)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('rol', rol)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('rol', rol)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Conceptos Contables -->
      <div v-if="activeTab === 'conceptos-contables'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Conceptos Contables</h2>
          <button class="btn-primary" @click="abrirModalCrear('conceptoContable')">
            + Nuevo Concepto
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los conceptos contables definen las clasificaciones financieras.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="concepto in conceptosContables" :key="concepto.id">
                <td>{{ concepto.descripcion }}</td>
                <td>{{ concepto.tipo }}</td>
                <td>
                  <span class="status-badge" :class="concepto.vigente ? 'status-active' : 'status-inactive'">
                    {{ concepto.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('conceptoContable', concepto)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('conceptoContable', concepto)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('conceptoContable', concepto)">Anular</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tipos de Archivo -->
      <div v-if="activeTab === 'tipos-archivo'" class="mantenedor-section">
        <div class="mantenedor-header">
          <h2>Gestión de Tipos de Archivo</h2>
          <button class="btn-primary" @click="abrirModalCrear('tipoArchivo')">
            + Nuevo Tipo
          </button>
        </div>
        
        <div class="alert">
          <span class="alert-icon">ℹ️</span>
          <div>
            <strong>Información:</strong> Los tipos de archivo definen los formatos de documento aceptados en el sistema.
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Extensión</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tipoArchivo in tiposArchivo" :key="tipoArchivo.id">
                <td>{{ tipoArchivo.descripcion }}</td>
                <td>{{ tipoArchivo.extension }}</td>
                <td>
                  <span class="status-badge" :class="tipoArchivo.vigente ? 'status-active' : 'status-inactive'">
                    {{ tipoArchivo.vigente ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="actions">
                  <button class="btn-action btn-view" @click="verElemento('tipoArchivo', tipoArchivo)">Ver</button>
                  <button class="btn-action btn-edit" @click="editarElemento('tipoArchivo', tipoArchivo)">Editar</button>
                  <button class="btn-action btn-anular" @click="solicitarAnular('tipoArchivo', tipoArchivo)">Anular</button>
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
          <h3>Visualizar {{ getTipoNombre(tipoElemento) }}</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="view-container">
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">Descripción:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">Unilateral:</label>
              <div class="view-value">{{ elementoSeleccionado.unilateral ? 'Sí' : 'No' }}</div>
            </div>
            <div v-if="tipoElemento === 'zona'" class="view-group">
              <label class="view-label">Estado:</label>
              <div class="view-value">
                <span class="status-badge" :class="elementoSeleccionado.vigente ? 'status-active' : 'status-inactive'">
                  {{ elementoSeleccionado.vigente ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
            </div>

            <!-- Campos para otros tipos de elementos -->
            <div v-if="tipoElemento !== 'zona'" class="view-group">
              <label class="view-label">Descripción:</label>
              <div class="view-value">{{ elementoSeleccionado.descripcion }}</div>
            </div>
            <div v-if="['distrito', 'grupo', 'comuna', 'provincia'].includes(tipoElemento)" class="view-group">
              <label class="view-label">{{ getRelacionNombre(tipoElemento) }}:</label>
              <div class="view-value">{{ getRelacionValor(tipoElemento) }}</div>
            </div>
            <div v-if="['tipoCurso', 'alimentacion', 'conceptoContable'].includes(tipoElemento)" class="view-group">
              <label class="view-label">Tipo:</label>
              <div class="view-value">{{ elementoSeleccionado.tipo }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoCurso'" class="view-group">
              <label class="view-label">Cant. Participantes:</label>
              <div class="view-value">{{ elementoSeleccionado.cant_participante }}</div>
            </div>
            <div v-if="tipoElemento === 'tipoArchivo'" class="view-group">
              <label class="view-label">Extensión:</label>
              <div class="view-value">{{ elementoSeleccionado.extension }}</div>
            </div>
            <div class="view-group">
              <label class="view-label">Estado:</label>
              <div class="view-value">
                <span class="status-badge" :class="elementoSeleccionado.vigente ? 'status-active' : 'status-inactive'">
                  {{ elementoSeleccionado.vigente ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
            </div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="cerrarModal">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmación de Anulación -->
    <div v-if="modalActivo === 'confirmar-anular'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Anulación</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <div class="confirmation-message">
            <p>¿Está seguro que desea anular el siguiente elemento?</p>
            <div class="elemento-info">
              <strong>{{ getTipoNombre(tipoElemento) }}:</strong> {{ elementoSeleccionado.descripcion }}
            </div>
            <p class="warning-text">Esta acción no se puede deshacer.</p>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn-danger" @click="confirmarAnular">
              🚫 Confirmar Anulación
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edición/Creación para Zonas -->
    <div v-if="modalActivo === 'crear-zona' || modalActivo === 'editar-zona'" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editando ? 'Editar' : 'Nueva' }} Zona</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarZona">
            <div class="form-group">
              <label class="form-label">Descripción:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formZona.descripcion"
                placeholder="Ej: ZONA NORTE BIOBÍO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-checkbox">
                <input type="checkbox" v-model="formZona.unilateral">
                Zona Unilateral
              </label>
            </div>
            <div class="form-group">
              <label class="form-label">Estado:</label>
              <select class="form-control" v-model="formZona.vigente" required>
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn-primary">
                {{ editando ? 'Actualizar' : 'Guardar' }}
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
          <h3>{{ editando ? 'Editar' : 'Nuevo' }} Distrito</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarDistrito">
            <div class="form-group">
              <label class="form-label">Descripción:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formDistrito.descripcion"
                placeholder="Ej: DISTRITO CONCEPCIÓN"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">Zona:</label>
              <select class="form-control" v-model="formDistrito.zona_id" required>
                <option value="">Seleccione una zona</option>
                <option v-for="zona in zonas" :key="zona.id" :value="zona.id">
                  {{ zona.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Estado:</label>
              <select class="form-control" v-model="formDistrito.vigente" required>
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn-primary">
                {{ editando ? 'Actualizar' : 'Guardar' }}
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
          <h3>{{ editando ? 'Editar' : 'Nuevo' }} Grupo Scout</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarGrupo">
            <div class="form-group">
              <label class="form-label">Descripción:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formGrupo.descripcion"
                placeholder="Ej: GRUPO ARAUCO"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">Distrito:</label>
              <select class="form-control" v-model="formGrupo.distrito_id" required>
                <option value="">Seleccione un distrito</option>
                <option v-for="distrito in distritos" :key="distrito.id" :value="distrito.id">
                  {{ distrito.descripcion }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Estado:</label>
              <select class="form-control" v-model="formGrupo.vigente" required>
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn-primary">
                {{ editando ? 'Actualizar' : 'Guardar' }}
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
          <h3>{{ editando ? 'Editar' : 'Nueva' }} Rama</h3>
          <button class="modal-close" @click="cerrarModal">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRama">
            <div class="form-group">
              <label class="form-label">Descripción:</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formRama.descripcion"
                placeholder="Ej: LOBATOS"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">Estado:</label>
              <select class="form-control" v-model="formRama.vigente" required>
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModal">Cancelar</button>
              <button type="submit" class="btn-primary">
                {{ editando ? 'Actualizar' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modales para los nuevos mantenedores (estructura similar) -->
    <!-- Se pueden expandir siguiendo el mismo patrón -->

  </div>
</template>

<script>
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import mantenedoresService from '@/services/mantenedoresService.js'

export default {
  name: 'MantenedoresScouts',
  setup() {
    // Estado reactivo / sincronización de pestaña con la URL
      const route = useRoute()
      const router = useRouter()

      const VALID_TABS = [
        'zonas','distritos','grupos','ramas','tipos-curso','cargos','alimentacion',
        'comunas','provincias','regiones','niveles','estados-civiles','roles',
        'conceptos-contables','tipos-archivo'
      ]

  const activeTab = ref('zonas')

      // Inicializar desde la URL
      onMounted(() => {
        const initial = typeof route.params.tab === 'string' ? route.params.tab : ''
        activeTab.value = VALID_TABS.includes(initial) ? initial : 'zonas'
      })

      // Sincronizar cuando cambia la URL
      watch(() => route.params.tab, (val) => {
        if (typeof val === 'string' && VALID_TABS.includes(val)) {
          activeTab.value = val
        }
      })

      // Empujar a la URL cuando cambia la pestaña desde el contenido
      watch(activeTab, (val) => {
        if (!VALID_TABS.includes(val)) return
        if (route.params.tab !== val) {
          router.replace({ name: 'mantenedores', params: { tab: val } })
        }
      })
    const modalActivo = ref('')
    const editando = ref(false)
    const tipoElemento = ref('')
    const elementoSeleccionado = ref(null)
    
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
      { id: 'grupos', label: 'Grupos Scout', icon: '👥' },
      { id: 'ramas', label: 'Ramas', icon: '🏕️' },
      { id: 'tipos-curso', label: 'Tipos Curso', icon: '📚' },
      { id: 'cargos', label: 'Cargos', icon: '👔' },
      { id: 'alimentacion', label: 'Alimentación', icon: '🍽️' },
      { id: 'comunas', label: 'Comunas', icon: '🏘️' },
      { id: 'provincias', label: 'Provincias', icon: '🏞️' },
      { id: 'regiones', label: 'Regiones', icon: '🗾' },
      { id: 'niveles', label: 'Niveles', icon: '📊' },
      { id: 'estados-civiles', label: 'Estados Civiles', icon: '💑' },
      { id: 'roles', label: 'Roles', icon: '👤' },
      { id: 'conceptos-contables', label: 'Conceptos Contables', icon: '💰' },
      { id: 'tipos-archivo', label: 'Tipos de Archivo', icon: '📁' }
    ]

    // Datos cargados desde API
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

    // Carga inicial desde endpoints
    onMounted(async () => {
      try {
        const [
          _zonas,
          _distritos,
          _grupos,
          _ramas,
          _tiposCurso,
          _cargos,
          _alimentacion,
          _regiones,
          _provincias,
          _comunas,
          _niveles,
          _estados,
          _roles,
          _conceptos,
          _tiposArchivo
        ] = await Promise.all([
          mantenedoresService.listarZonas(),
          mantenedoresService.listarDistritos(),
          mantenedoresService.listarGrupos(),
          mantenedoresService.listarRamas(),
          mantenedoresService.listarTiposCurso(),
          mantenedoresService.listarCargos(),
          mantenedoresService.listarAlimentacion(),
          mantenedoresService.listarRegiones(),
          mantenedoresService.listarProvincias(),
          mantenedoresService.listarComunas(),
          mantenedoresService.listarNiveles(),
          mantenedoresService.listarEstadosCiviles(),
          mantenedoresService.listarRoles(),
          mantenedoresService.listarConceptosContables(),
          mantenedoresService.listarTiposArchivo(),
        ])
        zonas.value = _zonas
        distritos.value = _distritos
        grupos.value = _grupos
        ramas.value = _ramas
        tiposCurso.value = _tiposCurso
        cargos.value = _cargos
        alimentacion.value = _alimentacion
        regiones.value = _regiones
        provincias.value = _provincias
        comunas.value = _comunas
        niveles.value = _niveles
        estadosCiviles.value = _estados
        roles.value = _roles
        conceptosContables.value = _conceptos
        tiposArchivo.value = _tiposArchivo
      } catch (e) {
        console.warn('No se pudieron cargar algunos mantenedores desde la API', e)
      }
    })

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

    // Métodos auxiliares
    const getZonaNombre = (zonaId) => {
      const zona = zonas.value.find(z => z.id === zonaId)
      return zona ? zona.descripcion : 'No encontrada'
    }

    const getDistritoNombre = (distritoId) => {
      const distrito = distritos.value.find(d => d.id === distritoId)
      return distrito ? distrito.descripcion : 'No encontrado'
    }

    const getProvinciaNombre = (provinciaId) => {
      const provincia = provincias.value.find(p => p.id === provinciaId)
      return provincia ? provincia.descripcion : 'No encontrada'
    }

    const getRegionNombre = (regionId) => {
      const region = regiones.value.find(r => r.id === regionId)
      return region ? region.descripcion : 'No encontrada'
    }

    const getTipoNombre = (tipo) => {
      const nombres = {
        'zona': 'Zona',
        'distrito': 'Distrito',
        'grupo': 'Grupo Scout',
        'rama': 'Rama',
        'tipoCurso': 'Tipo de Curso',
        'cargo': 'Cargo',
        'alimentacion': 'Alimentación',
        'comuna': 'Comuna',
        'provincia': 'Provincia',
        'region': 'Región',
        'nivel': 'Nivel',
        'estadoCivil': 'Estado Civil',
        'rol': 'Rol',
        'conceptoContable': 'Concepto Contable',
        'tipoArchivo': 'Tipo de Archivo'
      }
      return nombres[tipo] || 'Elemento'
    }

    const getRelacionNombre = (tipo) => {
      const relaciones = {
        'distrito': 'Zona',
        'grupo': 'Distrito',
        'comuna': 'Provincia',
        'provincia': 'Región'
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

    const solicitarAnular = (tipo, elemento) => {
      modalActivo.value = 'confirmar-anular'
      editando.value = false
      tipoElemento.value = tipo
      elementoSeleccionado.value = elemento
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
        // Agregar casos para otros tipos
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
    }

    const cerrarModal = () => {
      modalActivo.value = ''
      editando.value = false
      tipoElemento.value = ''
      elementoSeleccionado.value = null
      limpiarFormularios()
    }

    const confirmarAnular = () => {
      if (elementoSeleccionado.value) {
        const index = getArrayByTipo(tipoElemento.value).findIndex(item => item.id === elementoSeleccionado.value.id)
        if (index !== -1) {
          getArrayByTipo(tipoElemento.value)[index].vigente = false
        }
      }
      cerrarModal()
    }

    const getArrayByTipo = (tipo) => {
      const arrays = {
        'zona': zonas,
        'distrito': distritos,
        'grupo': grupos,
        'rama': ramas,
        'tipoCurso': tiposCurso,
        'cargo': cargos,
        'alimentacion': alimentacion,
        'comuna': comunas,
        'provincia': provincias,
        'region': regiones,
        'nivel': niveles,
        'estadoCivil': estadosCiviles,
        'rol': roles,
        'conceptoContable': conceptosContables,
        'tipoArchivo': tiposArchivo
      }
      return arrays[tipo] || zonas
    }

    // Métodos de guardado
    const guardarZona = () => {
      if (editando.value) {
        const index = zonas.value.findIndex(z => z.id === formZona.id)
        if (index !== -1) {
          zonas.value[index] = { ...formZona }
        }
      } else {
        const nuevaZona = {
          id: Math.max(...zonas.value.map(z => z.id)) + 1,
          ...formZona
        }
        zonas.value.push(nuevaZona)
      }
      cerrarModal()
    }

    const guardarDistrito = () => {
      if (editando.value) {
        const index = distritos.value.findIndex(d => d.id === formDistrito.id)
        if (index !== -1) {
          distritos.value[index] = { ...formDistrito }
        }
      } else {
        const nuevoDistrito = {
          id: Math.max(...distritos.value.map(d => d.id)) + 1,
          ...formDistrito
        }
        distritos.value.push(nuevoDistrito)
      }
      cerrarModal()
    }

    const guardarGrupo = () => {
      if (editando.value) {
        const index = grupos.value.findIndex(g => g.id === formGrupo.id)
        if (index !== -1) {
          grupos.value[index] = { ...formGrupo }
        }
      } else {
        const nuevoGrupo = {
          id: Math.max(...grupos.value.map(g => g.id)) + 1,
          ...formGrupo
        }
        grupos.value.push(nuevoGrupo)
      }
      cerrarModal()
    }

    const guardarRama = () => {
      if (editando.value) {
        const index = ramas.value.findIndex(r => r.id === formRama.id)
        if (index !== -1) {
          ramas.value[index] = { ...formRama }
        }
      } else {
        const nuevaRama = {
          id: Math.max(...ramas.value.map(r => r.id)) + 1,
          ...formRama
        }
        ramas.value.push(nuevaRama)
      }
      cerrarModal()
    }

    return {
      activeTab,
      modalActivo,
      editando,
      tipoElemento,
      elementoSeleccionado,
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
      abrirModalCrear,
      verElemento,
      editarElemento,
      solicitarAnular,
      cerrarModal,
      confirmarAnular,
      guardarZona,
      guardarDistrito,
      guardarGrupo,
      guardarRama
    }
  }
}
</script>

<style scoped>
.mantenedores-scouts {
  display: block;
  min-height: 100vh;
  background: #f5f5f5;
}

/* Main Content Styles (a pantalla completa) */
.main-content {
  padding: 0;
  min-height: 100vh;
  margin-left: 0; /* sin sidebar interna */
  width: 100%;
}



.mantenedor-section {
  padding: 30px;
  animation: fadeIn 0.5s ease;
}

.mantenedor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 3px solid #2c5aa0;
}

.mantenedor-header h2 {
  color: #2c5aa0;
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.btn-primary {
  background: #2c5aa0;
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
}

.btn-primary:hover {
  background: #1e3d73;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
}

.alert {
  background: #e3f2fd;
  border: 1px solid #bbdefb;
  color: #1565c0;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 25px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.alert-icon { display: none; }

.search-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.select-filter {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  min-width: 200px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f8f9fa;
}

.data-table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c5aa0;
  border-bottom: 2px solid #e1e5e9;
}

.data-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #e1e5e9;
}

.data-table tr:hover {
  background: #f8f9fa;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-active {
  background: #d4edda;
  color: #155724;
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
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
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
  z-index: 1000;
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
  border-bottom: 2px solid #2c5aa0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #2c5aa0;
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
  color: #2c5aa0;
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

/* Confirmation Message */
.confirmation-message {
  text-align: center;
  margin-bottom: 25px;
}

.elemento-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin: 15px 0;
  border-left: 4px solid #2c5aa0;
}

.warning-text {
  color: #dc3545;
  font-weight: 600;
}

.btn-danger {
  background: #dc3545;
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
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
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
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
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

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .main-content {
    margin-left: 0;
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
  
  .table-container {
    overflow-x: auto;
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
</style>
