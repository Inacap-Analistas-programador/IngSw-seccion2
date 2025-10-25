<template>
  <div class="gestion-personas">
  <!-- Vista: la NavBar se renderiza globalmente en App.vue, no incluirla aquí -->

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <div class="filtros-left">
        <InputBase v-model="searchQuery" placeholder="Buscar por nombre, RUT, email..." @keydown.enter="filtrar" />
        <BaseSelect v-model="selectedRole" :options="roleOptions" placeholder="Todos los roles" />
        <BaseSelect v-model="selectedCourse" :options="courseOptions" placeholder="Todos los cursos" />
        <BaseSelect v-model="selectedRama" :options="ramaOptions" placeholder="Todas las ramas" />
      </div>
      <div class="filtros-right">
        <BaseButton class="btn-search" variant="primary" @click="filtrar">🔎 Buscar</BaseButton>
        <BaseButton class="btn-export" variant="secondary" @click="exportarExcel">📊 Exportar</BaseButton>
      </div>
    </div>

    <!-- Mensaje de filtro activo -->
    <div v-if="selectedRole" class="filtro-activo" role="status" aria-live="polite">
      {{ filtroMensaje }}
    </div>

    <!-- Contenedor principal: tabla + detallet (scroll interno) -->
    <div class="main-area">
      <!-- Tabla de participantes (se muestra solo tras filtrar) -->
      <div v-if="filtroAplicado" class="table-wrapper">
      <table>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>RUT</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Rama</th>
          <th>Grupo</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in personasFiltradas" :key="p.rut">
          <td data-label="Nombre">{{ p.nombre }}</td>
          <td data-label="RUT">{{ p.rut }}</td>
          <td data-label="Email">{{ p.email }}</td>
          <td data-label="Rol">{{ p.rol }}</td>
          <td data-label="Rama">{{ p.rama }}</td>
          <td data-label="Grupo">{{ p.grupo }}</td>
          <td data-label="Estado">
            <span
              :class="['estado', p.estado.toLowerCase()]"
            >
              {{ p.estado }}
            </span>
          </td>
          <td>
            <BaseButton class="editar btn-edit" variant="secondary" @click="abrirModal(p)">✏️ Ver / Editar</BaseButton>
          </td>
        </tr>
        <tr v-if="personasFiltradas.length === 0" class="placeholder-row">
          <td data-label="Nombre" colspan="8">No hay participantes para mostrar</td>
        </tr>
      </tbody>
      </table>
    </div>

      <!-- Si aún no se filtra, mostrar mensaje instructivo -->
      <div v-else class="no-filtro" style="padding:32px; text-align:center; color:#666;">
        Aplica filtros y presiona "Buscar" para ver la lista de personas.
      </div>

  <!-- Ver/Editar persona -->
  <BaseModal v-model="editModalVisible" @close="cancelarEdicion">
        <template #default>
          <div class="modal-edit">
                <header class="modal-header">
                  <h3>Ver / Editar - {{ personaEditada?.nombre || '' }}</h3>
                  <div class="header-actions">
                    <BaseButton v-if="!pendingSave" class="btn-save" type="button" variant="primary" @click="prepararGuardado">💾 Guardar</BaseButton>
                    <BaseButton v-else class="btn-confirm" type="button" variant="success" @click="guardarEdicion">✅ Confirmar</BaseButton>
                  </div>
                </header>

                <div class="modal-tabs">
                  <button :class="{active: modalTab === 'info'}" @click="modalTab='info'">Info</button>
                  <button :class="{active: modalTab === 'hist'}" @click="modalTab='hist'">Historial</button>
                </div>

                <form v-if="modalTab==='info'" @submit.prevent="guardarEdicion" class="modal-form">
                  <div class="row">
                    <label>Nombre</label>
                    <input v-model="personaEditada.nombre" required />
                  </div>
                  <div class="row">
                    <label>RUT</label>
                    <input v-model="personaEditada.rut" required />
                  </div>
                  <div class="row">
                    <label>Email</label>
                    <input v-model="personaEditada.email" type="email" />
                  </div>
                  <div class="row">
                    <label>Teléfono</label>
                    <input v-model="personaEditada.telefono" />
                  </div>
                  <div class="row">
                    <label>Profesión</label>
                    <input v-model="personaEditada.profesion" />
                  </div>
                  <div class="row">
                    <label>Fecha Nac.</label>
                    <input v-model="personaEditada.fecha_nac" type="date" />
                  </div>
                  <div class="row">
                    <label>Dirección</label>
                    <input v-model="personaEditada.direccion" />
                  </div>
                  <div class="row">
                    <label>Contacto Emerg.</label>
                    <input v-model="personaEditada.contacto_emergencia" />
                  </div>
                  <div class="row">
                    <label>Tel. Emerg.</label>
                    <input v-model="personaEditada.telefono_emergencia" />
                  </div>
                  <div class="row">
                    <label>Alergias</label>
                    <input v-model="personaEditada.alergias" />
                  </div>
                  <div class="row">
                    <label>Limitación</label>
                    <input v-model="personaEditada.limitacion" />
                  </div>
                  <div class="row">
                    <label>Apodo</label>
                    <input v-model="personaEditada.apodo" />
                  </div>
                  <div class="row">
                    <label>Religión</label>
                    <input v-model="personaEditada.religion" />
                  </div>
                  <div class="row">
                    <label>Tiempo NNAJ</label>
                    <input v-model="personaEditada.tiempo_nnaj" />
                  </div>
                  <div class="row">
                    <label>Tiempo Adulto</label>
                    <input v-model="personaEditada.tiempo_adulto" />
                  </div>
                  <div class="row">
                    <label>Vigente</label>
                    <select v-model="personaEditada.vigente">
                      <option :value="true">Si</option>
                      <option :value="false">No</option>
                    </select>
                  </div>
                  <div class="row">
                    <label>Rol</label>
                    <BaseSelect v-model="personaEditada.rol" :options="roleOptions" />
                  </div>
                  <div class="row">
                    <label>Rama</label>
                    <BaseSelect v-model="personaEditada.rama" :options="ramaOptions" />
                  </div>
                </form>

                <div v-else class="historial-panel">
                  <div class="hist-list">
                    <div v-if="(personaEditada.historial || []).length === 0">No hay participaciones previas.</div>
                    <ul>
                      <li v-for="(h, idx) in (personaEditada.historial || [])" :key="idx">
                        <strong>{{ h.fecha }}</strong>: {{ h.descripcion }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
        </template>
      </BaseModal>
    </div>
  </div>
</template>

      <!-- Datos ejemplo para pruebas/Remover después de las pruebas -->

<script>
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'
import BaseModal from '@/components/Reutilizables/BaseModal.vue'

export default {
  name: 'GestionPersonas',
  components: { InputBase, BaseSelect, BaseButton, BaseAlert, BaseModal },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRama: '',
  selectedCourse: '',
      roleOptions: [
        { value: '', label: 'Todos los roles' },
        { value: 'PARTICIPANTE', label: 'Participante' },
        { value: 'DIRIGENTE', label: 'Dirigente' },
        { value: 'APOYO', label: 'Apoyo' }
      ],
      ramaOptions: [
        { value: '', label: 'Todas las ramas' },
        { value: 'CASTORES', label: 'Castores' },
        { value: 'LOBATOS', label: 'Lobatos' },
        { value: 'SCOUTS', label: 'Scouts' },
        { value: 'PIONEROS', label: 'Pioneros' },
        { value: 'ROVERS', label: 'Rovers' }
      ],
      courseOptions: [
        { value: '', label: 'Todos los cursos' },
        { value: 'PRIMEROS_AUXILIOS', label: 'Primeros Auxilios (RCP y Soporte Vital)' },
        { value: 'ORIENTACION_NAV', label: 'Orientación y Navegación' },
        { value: 'CAMPAMENTOS', label: 'Campamentos y Técnicas de Campo' },
        { value: 'LIDERAZGO_SCOUT', label: 'Liderazgo Scout' },
        { value: 'FORMACION_DIRIGENTES', label: 'Formación de Dirigentes' }
      ],
  personaSeleccionada: null,
  editModalVisible: false,
  personaEditada: null,
  modalTab: 'info',
  pendingSave: false,
    filtroAplicado: false,
    filteredPersonas: [],
      personas: [
  { nombre: 'JUAN PÉREZ GONZÁLEZ', rut: '12.345.678-9', email: 'juan.perez@email.com', telefono: '+56 9 1234 5678', profesion: 'INGENIERO', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO ARAUCO', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente', cursos: ['PRIMEROS_AUXILIOS','CAMPAMENTOS'], historial: [ { fecha: '2024-01-10', descripcion: 'Campamento regional' }, { fecha: '2023-11-05', descripcion: 'Taller de primeros auxilios' } ], fecha_nac: '1990-05-10', direccion: 'Av. Libertad 123, Concepción', contacto_emergencia: 'MARIA GONZÁLEZ', telefono_emergencia: '+56 9 4444 5555', alergias: '', limitacion: '', num_mmaa: 0, tiempo_nnaj: '3 años', tiempo_adulto: '2 años', religion: 'Católica', apodo: 'Juanca', foto: null, vigente: true, otros: '' },
  { nombre: 'MARÍA GONZÁLEZ LÓPEZ', rut: '98.765.432-1', email: 'maria.gonzalez@email.com', telefono: '+56 9 2222 3333', profesion: 'DOCENTE', rol: 'PARTICIPANTE', rama: 'ROVERS', grupo: 'GRUPO LAUTARO', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['ORIENTACION_NAV'], historial: [ { fecha: '2023-08-20', descripcion: 'Actividad de voluntariado' } ], fecha_nac: '1992-03-22', direccion: 'Calle Los Pinos 45, Talcahuano', contacto_emergencia: 'JOSÉ LÓPEZ', telefono_emergencia: '+56 9 1010 2020', alergias: 'Penicilina', limitacion: '', num_mmaa: 0, tiempo_nnaj: '1 año', tiempo_adulto: '4 años', religion: 'Evangelica', apodo: 'Maru', foto: null, vigente: true, otros: '' },
  { nombre: 'CARLOS RAMÍREZ SOTO', rut: '11.222.333-4', email: 'carlos.ramirez@email.com', telefono: '+56 9 5555 6666', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'PIONEROS', grupo: 'GRUPO CAUPOLICÁN', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente', cursos: ['CAMPAMENTOS'], historial: [], fecha_nac: '2004-09-10', direccion: 'Pasaje Los Aromos 7, Concepción', contacto_emergencia: 'LAURA SOTO', telefono_emergencia: '+56 9 5555 0000', alergias: 'Ninguna', limitacion: '', num_mmaa: 0, tiempo_nnaj: '2 años', tiempo_adulto: '0 años', religion: 'Sin religión', apodo: 'Carlitos', foto: null, vigente: true, otros: '' },
  { nombre: 'ANA TORRES RIVERA', rut: '15.987.654-2', email: 'ana.torres@email.com', telefono: '+56 9 7777 8888', profesion: 'MÉDICO', rol: 'DIRIGENTE', rama: 'SCOUTS', grupo: 'GRUPO LEBU', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['FORMACION_DIRIGENTES'], historial: [ { fecha: '2022-10-12', descripcion: 'Líder regional' } ], fecha_nac: '1981-12-02', direccion: 'Av. Argentina 200, Concepción', contacto_emergencia: 'CARLOS TORRES', telefono_emergencia: '+56 9 7777 1111', alergias: '', limitacion: '', num_mmaa: 0, tiempo_nnaj: '0 años', tiempo_adulto: '10 años', religion: 'Católica', apodo: 'Ana', foto: null, vigente: true, otros: '' },
  { nombre: 'PABLO MENDEZ', rut: '20.111.222-3', email: 'pablo.mendez@email.com', telefono: '+56 9 3333 4444', profesion: 'ARQUITECTO', rol: 'APOYO', rama: 'CASTORES', grupo: 'GRUPO CASTOR', zona: 'ZONA NORTE', distrito: 'SANTIAGO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['PRIMEROS_AUXILIOS'], historial: [ { fecha: '2021-03-05', descripcion: 'Voluntariado en campo' } ], fecha_nac: '1979-04-14', direccion: 'Calle Larga 555, Santiago', contacto_emergencia: 'SOFIA MENDEZ', telefono_emergencia: '+56 9 6666 7777', alergias: 'Polen', limitacion: '', num_mmaa: 0, tiempo_nnaj: '0 años', tiempo_adulto: '6 años', religion: 'Católica', apodo: '', foto: null, vigente: true, otros: '' },
  { nombre: 'LAURA VEGA', rut: '21.222.333-4', email: 'laura.vega@email.com', telefono: '+56 9 4444 5555', profesion: 'ENFERMERA', rol: 'DIRIGENTE', rama: 'LOBATOS', grupo: 'GRUPO LOBITOS', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['PRIMEROS_AUXILIOS'], historial: [ { fecha: '2020-07-18', descripcion: 'Atención sanitaria en campamento' } ], fecha_nac: '1987-11-30', direccion: 'Av. Providencia 321, Santiago', contacto_emergencia: 'MARTA VEGA', telefono_emergencia: '+56 9 8888 0000', alergias: '', limitacion: '', num_mmaa: 0, tiempo_nnaj: '0 años', tiempo_adulto: '8 años', religion: 'Católica', apodo: 'Lau', foto: null, vigente: true, otros: '' },
  { nombre: 'MARIO LOPEZ', rut: '22.333.444-5', email: 'mario.lopez@email.com', telefono: '+56 9 6666 7777', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO SUR', zona: 'ZONA SUR', distrito: 'SANTIAGO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['CAMPAMENTOS'], historial: [ { fecha: '2024-02-01', descripcion: 'Competencia regional' } ] },
  { nombre: 'SUSANA RIVERA', rut: '23.444.555-6', email: 'susana.rivera@email.com', telefono: '+56 9 8888 9999', profesion: 'DOCENTE', rol: 'APOYO', rama: 'PIONEROS', grupo: 'GRUPO PION', zona: 'ZONA NORTE', distrito: 'VALPARAÍSO', estado: 'Pendiente', inscripcion: 'Pendiente', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['FORMACION_DIRIGENTES'], historial: [ { fecha: '2019-06-12', descripcion: 'Capacitación docente' } ] },
  { nombre: 'RODRIGO CAMPOS', rut: '24.555.666-7', email: 'rodrigo.campos@email.com', telefono: '+56 9 1010 1111', profesion: 'INGENIERO', rol: 'DIRIGENTE', rama: 'ROVERS', grupo: 'GRUPO ROVER', zona: 'ZONA CENTRO', distrito: 'VALPARAÍSO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['LIDERAZGO_SCOUT'], historial: [ { fecha: '2022-12-01', descripcion: 'Organizador de actividad' } ] },
  { nombre: 'ELENA FERNANDEZ', rut: '25.666.777-8', email: 'elena.fernandez@email.com', telefono: '+56 9 1212 1313', profesion: 'ABOGADA', rol: 'PARTICIPANTE', rama: 'CASTORES', grupo: 'GRUPO CASTOR 2', zona: 'ZONA NORTE', distrito: 'ANTOFAGASTA', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['ORIENTACION_NAV'], historial: [ { fecha: '2021-09-09', descripcion: 'Participación en taller legal' } ] },
  { nombre: 'ANDRES GOMEZ', rut: '26.777.888-9', email: 'andres.gomez@email.com', telefono: '+56 9 1414 1515', profesion: 'PROFESOR', rol: 'PARTICIPANTE', rama: 'LOBATOS', grupo: 'GRUPO LOBOS', zona: 'ZONA CENTRO', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente', cursos: ['CAMPAMENTOS'], historial: [ { fecha: '2023-04-11', descripcion: 'Taller educativo' } ] },
  { nombre: 'VERONICA SALAS', rut: '27.888.999-0', email: 'veronica.salas@email.com', telefono: '+56 9 1616 1717', profesion: 'ENFERMERA', rol: 'APOYO', rama: 'SCOUTS', grupo: 'GRUPO SUR 2', zona: 'ZONA SUR', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['PRIMEROS_AUXILIOS'], historial: [ { fecha: '2020-02-14', descripcion: 'Campaña de salud' } ] },
  { nombre: 'RICARDO PENA', rut: '28.999.000-1', email: 'ricardo.pena@email.com', telefono: '+56 9 1818 1919', profesion: 'TÉCNICO', rol: 'DIRIGENTE', rama: 'PIONEROS', grupo: 'GRUPO PION 2', zona: 'ZONA NORTE', distrito: 'IQUIQUE', estado: 'Pendiente', inscripcion: 'Pendiente', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['FORMACION_DIRIGENTES'], historial: [ { fecha: '2018-05-30', descripcion: 'Formación técnica' } ] },
  { nombre: 'MARTA LOZANO', rut: '29.000.111-2', email: 'marta.lozano@email.com', telefono: '+56 9 2020 2121', profesion: 'ESTILISTA', rol: 'PARTICIPANTE', rama: 'ROVERS', grupo: 'GRUPO ROVER 2', zona: 'ZONA SUR', distrito: 'VALPARAÍSO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['LIDERAZGO_SCOUT'], historial: [ { fecha: '2022-01-20', descripcion: 'Organización de evento' } ] },
  { nombre: 'HUGO SANCHEZ', rut: '30.111.222-3', email: 'hugo.sanchez@email.com', telefono: '+56 9 2223 2324', profesion: 'MUSICO', rol: 'APOYO', rama: 'CASTORES', grupo: 'GRUPO CASTOR 3', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['ORIENTACION_NAV'], historial: [ { fecha: '2019-11-02', descripcion: 'Actividad cultural' } ] },
  { nombre: 'CAMILA RIOS', rut: '31.222.333-4', email: 'camila.rios@email.com', telefono: '+56 9 2425 2627', profesion: 'INGENIERA', rol: 'DIRIGENTE', rama: 'LOBATOS', grupo: 'GRUPO LOBOS 2', zona: 'ZONA SUR', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['FORMACION_DIRIGENTES'], historial: [ { fecha: '2021-06-15', descripcion: 'Coordinación de campamento' } ] },
  { nombre: 'OSCAR NAVARRO', rut: '32.333.444-5', email: 'oscar.navarro@email.com', telefono: '+56 9 2728 2929', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO SUR 3', zona: 'ZONA SUR', distrito: 'TALCA', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente', cursos: ['CAMPAMENTOS'], historial: [ { fecha: '2023-09-05', descripcion: 'Competencia local' } ] },
  { nombre: 'LUIS FARIAS', rut: '33.444.555-6', email: 'luis.farias@email.com', telefono: '+56 9 3031 3233', profesion: 'AGRICULTOR', rol: 'APOYO', rama: 'PIONEROS', grupo: 'GRUPO PION 3', zona: 'ZONA NORTE', distrito: 'IQUIQUE', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada', cursos: ['PRIMEROS_AUXILIOS'], historial: [ { fecha: '2022-08-10', descripcion: 'Apoyo logístico' } ] },
  { nombre: 'NICOLE MORA', rut: '34.555.666-7', email: 'nicole.mora@email.com', telefono: '+56 9 3334 3536', profesion: 'DOCTORA', rol: 'DIRIGENTE', rama: 'ROVERS', grupo: 'GRUPO ROVER 3', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente', cursos: ['FORMACION_DIRIGENTES','PRIMEROS_AUXILIOS'], historial: [ { fecha: '2017-04-22', descripcion: 'Atención médica en evento' } ] }
      ]
    };
  },
  created() {
    // enriquecer personas con campos tipo BD al crear
    this.enrichPersonas();
  },
  computed: {
    filtroMensaje() {
      return `Filtro activo: Solo se muestran personas con rol "${this.selectedRole}"`
    },
    // Mostrar la instantánea de personas filtradas. Vacío hasta presionar Buscar.
    personasFiltradas() {
      return this.filteredPersonas || [];
    }
  },
  methods: {
    seleccionar(persona) {
      // mantener compatibilidad - también abrir modal para editar
      this.abrirModal(persona);
    },
    abrirModal(persona) {
      // clon profundo para que historial y objetos anidados queden aislados hasta guardar
      this.personaEditada = JSON.parse(JSON.stringify(persona || {}));
      if (!this.personaEditada.historial) this.personaEditada.historial = [];
      this.newHistEntry = { fecha: '', descripcion: '' };
      this.modalTab = 'info';
      this.editModalVisible = true;
      // también mantener referencia al elemento original para la lógica de guardado
      this.personaSeleccionada = persona;
  this.pendingSave = false;
    },
    cancelarEdicion() {
      // cerrar modal usando la propiedad reactiva
      this.editModalVisible = false;
      this.personaEditada = null;
      this.personaSeleccionada = null;
      this.pendingSave = false;
    },
    cerrarDetalle() {
      this.personaSeleccionada = null;
    },
    filtrar() {
      // Marcar que el usuario aplicó el filtro para mostrar la lista
      this.filtroAplicado = true;
      // cerrar detalle si estaba abierto
      this.personaSeleccionada = null;

  // Calcular la instantánea filtrada una vez (no actualizar reactivamente mientras se escribe)
      const q = (this.searchQuery || '').toLowerCase().trim();
  const selectedRoleNorm = (this.selectedRole || '').toString().trim().toUpperCase();
  const selectedRamaNorm = (this.selectedRama || '').toString().trim().toUpperCase();
  const selectedCourseNorm = (this.selectedCourse || '').toString().trim().toUpperCase();

      this.filteredPersonas = this.personas.filter((p) => {
        const nombre = (p.nombre || '').toLowerCase();
        const rut = (p.rut || '').toLowerCase();
        const email = (p.email || '').toLowerCase();

        const coincideBusqueda = nombre.includes(q) || rut.includes(q) || email.includes(q);

        const pRolNorm = (p.rol || '').toString().trim().toUpperCase();
        const pRamaNorm = (p.rama || '').toString().trim().toUpperCase();
        const pCursos = (p.cursos || []).map((c) => ('' + c).toString().trim().toUpperCase());

        const coincideRol = selectedRoleNorm ? pRolNorm === selectedRoleNorm : true;
        const coincideRama = selectedRamaNorm ? pRamaNorm === selectedRamaNorm : true;
        const coincideCurso = selectedCourseNorm ? pCursos.includes(selectedCourseNorm) : true;

        return coincideBusqueda && coincideRol && coincideRama && coincideCurso;
      });

      // pequeño comportamiento UX: scrollear la tabla hacia la vista
      this.$nextTick(() => {
        const el = document.querySelector('.table-wrapper');
        if (el && typeof el.scrollIntoView === 'function') el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    },
    // enriquecer objetos persona con campos adicionales tipo BD
    enrichPersonas() {
      const now = new Date().toISOString();
      this.personas = (this.personas || []).map((p, idx) => {
        const rawRut = (p.rut || '').toString().trim();
        let per_run = null;
        let per_dv = '';
        const m = rawRut.match(/([0-9\.]+)-?([0-9kK])/);
        if (m) {
          per_run = Number(m[1].replace(/\./g, '')) || null;
          per_dv = m[2] || '';
        }

  // dividir nombre en apellidos / nombres
        const nameParts = (p.nombre || '').toString().trim().split(/\s+/);
        let apelpat = '';
        let apelmat = '';
        let nombres = p.nombre || '';
        if (nameParts.length >= 2) {
          apelpat = nameParts[nameParts.length - 2] || '';
          apelmat = nameParts[nameParts.length - 1] || '';
          nombres = nameParts.slice(0, nameParts.length - 2).join(' ') || nombres;
          }

        const enriched = Object.assign({}, p, {
          PER_ID: idx + 1,
          ESC_ID: null,
          COM_ID: null,
          USU_ID: null,
          PER_FECHA_HORA: now,
          PER_RUN: per_run,
          PER_DV: per_dv,
          PER_APELPAT: apelpat,
          PER_APELMAT: apelmat,
          PER_NOMBRES: nombres || p.nombre,
          PER_EMAIL: p.email || '',
          PER_FECHA_NAC: p.fecha_nac || '1990-01-01',
          PER_DIRECCION: p.direccion || '',
          PER_TIPO_FONO: 'Móvil',
          PER_FONO: p.telefono || '',
          PER_ALERGIA_ENFERMEDAD: p.alergias || '',
          PER_LIMITACION: p.limitacion || '',
          PER_NOM_EMERGENCIA: p.contacto_emergencia || '',
          PER_FONO_EMERGENCIA: p.telefono_emergencia || '',
          PER_OTROS: p.otros || '',
          PER_NUM_MMAA: p.num_mmaa || 0,
          PER_PROFESION: p.profesion || '',
          PER_TIEMPO_NNAJ: p.tiempo_nnaj || '',
          PER_TIEMPO_ADULTO: p.tiempo_adulto || '',
          PER_RELIGION: p.religion || '',
          PER_APODO: p.apodo || '',
          PER_FOTO: p.foto || null,
          PER_VIGENTE: p.vigente === undefined ? true : !!p.vigente,
          cursos: p.cursos || [],
          historial: p.historial || []
        });

        return enriched;
      });
    },
    exportarExcel() {
      const datos = this.personasFiltradas.map((p) => ({
        Nombre: p.nombre,
        RUT: p.rut,
        Email: p.email,
        Rol: p.rol,
        Rama: p.rama,
        Grupo: p.grupo,
        Estado: p.estado
      }));
  // Exportar como CSV
      const keys = datos.length ? Object.keys(datos[0]) : ['Nombre','RUT','Email','Rol','Rama','Grupo','Estado'];
      const rows = [];
      rows.push(keys.join(','));

      for (const item of datos) {
        const values = keys.map((k) => {
          const v = item[k] ?? '';
          const safe = String(v).replace(/"/g, '""');
          return `"${safe}"`;
        });
        rows.push(values.join(','));
      }

      const csv = rows.join('\r\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });

  // Crear enlace de descarga
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.setAttribute('download', 'GestionPersonas.csv');
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    ,
    guardarEdicion() {
      if (!this.personaEditada || !this.personaEditada.rut || !this.personaEditada.nombre) {
        // validación mínima
        alert('Nombre y RUT son obligatorios');
        return;
      }

      if (this.personaEditada) {
        this.personaEditada.PER_FECHA_NAC = this.personaEditada.fecha_nac || this.personaEditada.PER_FECHA_NAC || '';
        this.personaEditada.PER_DIRECCION = this.personaEditada.direccion || this.personaEditada.PER_DIRECCION || '';
        this.personaEditada.PER_NOM_EMERGENCIA = this.personaEditada.contacto_emergencia || this.personaEditada.PER_NOM_EMERGENCIA || '';
        this.personaEditada.PER_FONO_EMERGENCIA = this.personaEditada.telefono_emergencia || this.personaEditada.PER_FONO_EMERGENCIA || '';
        this.personaEditada.PER_ALERGIA_ENFERMEDAD = this.personaEditada.alergias || this.personaEditada.PER_ALERGIA_ENFERMEDAD || '';
        this.personaEditada.PER_LIMITACION = this.personaEditada.limitacion || this.personaEditada.PER_LIMITACION || '';
        this.personaEditada.PER_APODO = this.personaEditada.apodo || this.personaEditada.PER_APODO || '';
        this.personaEditada.PER_RELIGION = this.personaEditada.religion || this.personaEditada.PER_RELIGION || '';
        this.personaEditada.PER_TIEMPO_NNAJ = this.personaEditada.tiempo_nnaj || this.personaEditada.PER_TIEMPO_NNAJ || '';
        this.personaEditada.PER_TIEMPO_ADULTO = this.personaEditada.tiempo_adulto || this.personaEditada.PER_TIEMPO_ADULTO || '';
        this.personaEditada.PER_VIGENTE = this.personaEditada.vigente === undefined ? (this.personaEditada.PER_VIGENTE ?? true) : !!this.personaEditada.vigente;
      }

      // buscar índice en el array principal personas por rut (único)
      const idx = this.personas.findIndex((p) => p.rut === this.personaEditada.rut);
      if (idx !== -1) {
        // reemplazar el objeto en el array principal (preservar reactividad)
        this.$set ? this.$set(this.personas, idx, Object.assign({}, this.personaEditada)) : (this.personas.splice(idx, 1, Object.assign({}, this.personaEditada)));
      } else {
        // si RUT cambió y no se encontró, intentar emparejar por el rut original seleccionado
        const originalRut = this.personaSeleccionada && this.personaSeleccionada.rut;
        const idx2 = this.personas.findIndex((p) => p.rut === originalRut);
        if (idx2 !== -1) this.personas.splice(idx2, 1, Object.assign({}, this.personaEditada));
      }

      // actualizar la instantánea filtrada si está presente
      if (this.filteredPersonas && this.filteredPersonas.length) {
        const fidx = this.filteredPersonas.findIndex((p) => p.rut === this.personaEditada.rut);
        if (fidx !== -1) this.filteredPersonas.splice(fidx, 1, Object.assign({}, this.personaEditada));
        else {
          // además, si el RUT cambió, intentar encontrar por el original
          const orig = this.personaSeleccionada && this.personaSeleccionada.rut;
          const fidx2 = this.filteredPersonas.findIndex((p) => p.rut === orig);
          if (fidx2 !== -1) this.filteredPersonas.splice(fidx2, 1, Object.assign({}, this.personaEditada));
        }
      }

      // cerrar modal mediante la propiedad reactiva
      this.editModalVisible = false;
      this.personaSeleccionada = null;
      this.personaEditada = null;
      this.pendingSave = false;
    },
    prepararGuardado() {
      // Marcar pendingSave para que el usuario confirme al guardar
      this.pendingSave = true;
      this.$nextTick(() => {
        const m = document.querySelector('.modal-edit');
        if (m && typeof m.scrollIntoView === 'function') m.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
      },
      addHistEntry() {
      if (!this.personaEditada) return;
      const fecha = (this.newHistEntry.fecha || '').trim();
      const descripcion = (this.newHistEntry.descripcion || '').trim();
      if (!fecha || !descripcion) {
        alert('Fecha y descripción son obligatorias para agregar al historial');
        return;
      }
      this.personaEditada.historial = this.personaEditada.historial || [];
      this.personaEditada.historial.unshift({ fecha, descripcion });
      this.newHistEntry = { fecha: '', descripcion: '' };
    }
  }
};
</script>

<style>
.gestion-personas {
  box-sizing: border-box;
  margin: 20px auto;
  padding: 16px 40px; 
  background: #ffffff;
  color: #111;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: Arial, sans-serif;
  width: 1100px;                
  max-width: calc(100% - 48px);
  height: auto;
  max-height: calc(100vh - 48px);
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(16,24,40,0.08);
  overflow: hidden;            
}

.main-area { 
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header h2 {
  background-color: #214e9c;
  color: #fff;
  padding: 14px 18px;
  border-radius: 6px;
  margin: 0 0 4px 0;
}

.header h3 {
  margin: 6px 0 0 0;
  color: #444;
  font-weight: 500;
}

.filtros {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 0 0 auto;
  padding: 12px 0;
  min-height: 56px;
  flex-wrap: wrap; 
  box-sizing: border-box;
  padding-right: 8px;
}

.filtros-left { display:flex; gap:12px; align-items:center; flex: 1 1 auto; min-width: 0 }
.filtros-right { display:flex; gap:10px; align-items:center; justify-content:flex-end; flex: 0 0 auto }

.filtros input,
.filtros select {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  color: #222;
  background: #fff;
}

.filtros input {
  flex: 1 1 0;
}
.filtros select {
  flex: 0 0 160px;
}


.filtros .base-input {
  flex: 1 1 420px; 
  min-width: 180px;
  max-width: 720px;
  margin-bottom: 0; 
}
.filtros .base-input .base-field {
  padding: 10px 12px;
  font-size: 14px;
}
.filtros .base-select {
  flex: 0 0 160px; 
  min-width: 120px;
  max-width: 220px;
  margin-bottom: 0;
}
.filtros .base-select .base-select__element {
  padding: 8px 10px;
  font-size: 14px;
}
.filtros button {
  flex: 0 0 auto;
  flex-shrink: 0; 
}

.buscar, .exportar {
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-search, .buscar { background: linear-gradient(180deg,#2b6cb0,#154c8c); color: #fff; box-shadow: 0 6px 18px rgba(33,78,156,0.12); border: none; }
.btn-export, .exportar { background: linear-gradient(180deg,#16a34a,#15803d); color: #fff; box-shadow: 0 6px 18px rgba(16,185,129,0.08); border: none; }

.btn-edit { background: linear-gradient(180deg,#facc15,#f59e0b); color: #111; box-shadow: 0 6px 18px rgba(250,204,21,0.08); }
.btn-save { background: linear-gradient(180deg,#2563eb,#1e40af); color:#fff; box-shadow: 0 8px 24px rgba(37,99,235,0.12); }
.btn-confirm { background: linear-gradient(180deg,#059669,#047857); color:#fff; box-shadow: 0 8px 24px rgba(5,150,105,0.12); }

.btn-search, .btn-export, .btn-edit, .btn-save, .btn-confirm {
  padding: 8px 14px;
  border-radius: 8px;
  font-weight:700;
  transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
}
.btn-search:hover, .btn-export:hover, .btn-edit:hover, .btn-save:hover, .btn-confirm:hover { transform: translateY(-2px); }
.btn-search:active, .btn-export:active, .btn-edit:active, .btn-save:active, .btn-confirm:active { transform: translateY(0); }
.btn-search:focus, .btn-export:focus, .btn-edit:focus, .btn-save:focus, .btn-confirm:focus { outline: 3px solid rgba(33,78,156,0.12); }

.editar { padding: 6px 10px; }

.filtro-activo {
  background-color: #f4faf5;
  color: #115e26;
  padding: 8px;
  margin-bottom: 6px;
  border-radius: 4px;
}

.table-wrapper {
  flex: 1 1 auto;
  overflow: auto;
  padding-right: 12px; 
  -webkit-overflow-scrolling: touch;
  min-height: 0; 
}

.main-area {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  overflow: hidden; 
  min-height: 0; 
}

table {
  width: 100%;
  box-sizing: border-box;
  border-collapse: collapse;
  background-color: #fff;
  min-width: 0; 
  font-size: 14px;
}

th, td {
  padding: 14px 12px;
  border-bottom: 1px solid #ececec;
  text-align: left;
  color: #222; 
  opacity: 1;
}

th {
  background-color: #f7f7f7;
  color: #222;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 2;
}

.editar {
  background-color: #facc15;
  color: #111;
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
}

.estado { padding: 4px 8px; border-radius: 12px; font-size: 12px; }
.estado.inscrito { background:#d1fae5; color:#065f46 }
.estado.preinscrito { background:#fff4db; color:#8f5b00 }
.estado.confirmado { background:#d1fae5; color:#065f46 }
.estado.aprobada { background:#d1fae5; color:#065f46 }
.estado.pendiente { background:#fff4db; color:#8f5b00 }

.detail-panel .detalle { flex: 0 0 auto; margin-top: 18px; padding: 14px 18px; background: #f6f7f9; border-radius: 6px; }
.detail-panel .detalle h4 { margin: 0 0 10px 0; color:#1e3a8a; font-size: 20px; font-weight:700 }

.placeholder-row td {
  text-align: center;
  color: #666;
  padding: 48px 10px;
  background: linear-gradient(180deg,#fff,#fbfbfb);
}

@media (max-width: 960px) {
  .filtros { flex-wrap: wrap; }
}

@media (max-width: 520px) {
  .gestion-personas { padding: 12px; }
  .filtros { flex-direction: column; align-items: stretch; }
  .filtros-left, .filtros-right { width: 100%; justify-content: space-between }
  .filtros input, .filtros select, .filtros .base-input, .filtros .base-select { width: 100%; }

  thead { display: none; }
  tr { display: block; margin-bottom: 12px; box-shadow: none; }
  td { display: flex; justify-content: space-between; border-bottom: 0; padding: 8px 6px; }
  .table-wrapper { overflow:auto; }
  td[data-label]::before { content: attr(data-label) ": "; font-weight:600; margin-right:6px; color:#333; }
}

@media (max-width: 1100px) {
  .gestion-personas {
    width: calc(100% - 32px);
    height: auto;
    margin: 12px auto;
    border-radius: 6px;
  }
}

@media (min-width: 1100px) {
  .main-area {
    flex-direction: row;
    align-items: flex-start;
    gap: 24px;
  }
  .table-wrapper {
    flex: 1 1 auto;
    max-height: calc(820px - 240px); 
    overflow: auto;
  }
  .detalle {
    flex: 0 0 420px;
    max-width: 420px;
  }
  .detail-panel .detalle { padding: 20px; }
}

.detail-panel .detalle {
  background: #f2f5f9; 
  border-radius: 6px;
  padding: 18px 18px 16px 18px;
  border: 1px solid rgba(33,78,156,0.08);
  color: #222;
  font-size: 15px;
  line-height: 1.4;
}
.detalle { box-shadow: 0 6px 20px rgba(16,24,40,0.06); }
.detail-panel .detalle h4 {
  background: transparent;
  color: #214e9c; 
  padding: 0;
  margin: 0 0 10px 0;
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
}
.detalle-contenido {
  display: flex;
  gap: 48px;
  align-items: flex-start;
  justify-content: space-between;
  border-top: 2px solid #214e9c; 
  padding-top: 14px;
  margin-top: 10px;
}


.detalle-header {
  background: #214e9c;
  color: #fff;
  padding: 12px 16px;
  border-radius: 6px 6px 0 0;
  margin-bottom: 12px;
  position: relative;
}
.detalle-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}
.cerrar-detalle {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  line-height: 1;
  padding: 6px 8px;
  border-radius: 4px;
}
.cerrar-detalle:hover { background: rgba(255,255,255,0.06); }
.detalle-body {
  background: #fff;
  border-radius: 0 0 6px 6px;
  padding: 18px;
  border: 1px solid #eef2f6;
}
.detalle-contenido .col {
  flex: 1 1 0;
  padding: 6px 8px;
}
.detalle-contenido .col:nth-child(1) { max-width: 420px; }
.detalle-contenido .col:nth-child(2) { max-width: 380px; }
.detalle-contenido .col:nth-child(3) { max-width: 260px; }
.detalle h5 { margin: 6px 0 8px 0; font-size: 15px; color: #111; font-weight: 700; line-height:1.2; display:block; text-transform: none; }
.detalle p { margin: 6px 0; color: #222; }
.detalle strong { display: inline-block; min-width: 110px; font-weight: 700; color: #111; }


td[data-label="Nombre"] { text-transform: uppercase; font-weight:600; }


</style>

<style scoped>
.modal-edit {
  width: 720px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 96px);
  overflow: auto;
  box-sizing: border-box;
  padding: 12px 14px;
}
.modal-header { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:12px; }
.modal-header h3 { margin:0; font-size:18px; color:#214e9c }
.modal-close { background:transparent; border:none; font-size:18px; cursor:pointer }
.modal-header .header-actions { display:flex; gap:8px; align-items:center }
.modal-header .header-actions .base-button { padding:6px 10px }

@media (max-width: 520px) {
  .modal-header { flex-direction: column; align-items: stretch; gap:8px }
  .modal-header .header-actions { justify-content: flex-end }
  .modal-header .header-actions .base-button { padding:8px 12px }
}
.modal-form {
  display:flex;
  flex-direction:column;
  gap:10px;
  max-height: calc(100vh - 240px);
  overflow: auto;
  padding-right: 8px;
}
.modal-form .row { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.modal-form .row label { width:120px; min-width:100px; font-weight:700; color:#222 }
.modal-form .row input, .modal-form .row select { flex:1; min-width:140px; padding:8px 10px; border:1px solid #e6e6e6; border-radius:6px }
.modal-form .actions { justify-content:flex-end; margin-top:12px }
.modal-form .actions .base-button { margin-left:8px }
</style>

<style scoped>
.modal-tabs { display:flex; gap:8px; margin-bottom:12px }
.modal-tabs button { padding:8px 12px; border-radius:6px; border:1px solid #e6e6e6; background:#fff; cursor:pointer }
.modal-tabs button.active { background:#214e9c; color:#fff; border-color:#214e9c }
.historial-panel { display:flex; gap:20px; align-items:flex-start }
.historial-panel { max-height: calc(100vh - 260px); overflow: auto; }
.hist-list { flex:1; overflow:auto; }
.hist-list ul { list-style:none; padding:0; margin:0 }
.hist-list li { padding:8px 10px; border-bottom:1px solid #eee }
.hist-add { width:320px; border-left:1px solid #f0f0f0; padding-left:16px }
</style>
