<template>
  <div class="gestion-personas">
  <!-- Vista: la NavBar se renderiza globalmente en App.vue, no incluirla aquí -->

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <InputBase v-model="searchQuery" placeholder="Buscar por nombre, RUT, email..." />
      <BaseSelect v-model="selectedRole" :options="roleOptions" placeholder="Todos los roles" />
      <BaseSelect v-model="selectedRama" :options="ramaOptions" placeholder="Todas las ramas" />
      <BaseButton variant="primary" @click="filtrar">Buscar</BaseButton>
      <BaseButton variant="secondary" @click="exportarExcel">📊 Exportar</BaseButton>
    </div>

    <!-- Mensaje de filtro activo (estilo mockup) -->
    <div v-if="selectedRole" class="filtro-activo" role="status" aria-live="polite">
      {{ filtroMensaje }}
    </div>

    <!-- Contenedor principal: tabla + detallet (scroll interno) -->
    <div class="main-area">
      <!-- Tabla de participantes -->
      <div class="table-wrapper">
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
            <BaseButton class="editar" variant="secondary" @click="seleccionar(p)">Ver/Editar</BaseButton>
          </td>
        </tr>
        <!-- Placeholder...-->
        <tr v-if="personasFiltradas.length === 0" class="placeholder-row">
          <td data-label="Nombre" colspan="8">No hay participantes para mostrar</td>
        </tr>
      </tbody>
      </table>
    </div>
      
      <!-- Detalle de persona seleccionada -->
      <div v-if="personaSeleccionada" class="detalle">
        <div class="detalle-header">
          <h4>Detalle Completo - {{ personaSeleccionada.nombre }}</h4>
          <button class="cerrar-detalle" @click="cerrarDetalle" aria-label="Cerrar detalle">✕</button>
        </div>
        <div class="detalle-body">
          <div class="detalle-contenido">
        <div class="col">
          <h5>Datos Personales</h5>
          <p><strong>RUT:</strong> {{ personaSeleccionada.rut }}</p>
          <p><strong>Email:</strong> {{ personaSeleccionada.email }}</p>
          <p><strong>Teléfono:</strong> {{ personaSeleccionada.telefono }}</p>
          <p><strong>Profesión:</strong> {{ personaSeleccionada.profesion }}</p>
        </div>
        <div class="col">
          <h5>Datos Scout</h5>
          <p><strong>Zona:</strong> {{ personaSeleccionada.zona }}</p>
          <p><strong>Distrito:</strong> {{ personaSeleccionada.distrito }}</p>
          <p><strong>Grupo:</strong> {{ personaSeleccionada.grupo }}</p>
          <p><strong>Rama:</strong> {{ personaSeleccionada.rama }}</p>
        </div>
        <div class="col">
          <h5>Estados</h5>
          <p>
            <strong>Inscripción:</strong>
            <span :class="['estado', (personaSeleccionada.inscripcion || '').toLowerCase()]">{{ personaSeleccionada.inscripcion }}</span>
          </p>
          <p>
            <strong>Pago:</strong>
            <span :class="['estado', (personaSeleccionada.pago || '').toLowerCase()]">{{ personaSeleccionada.pago }}</span>
          </p>
          <p>
            <strong>Acreditación:</strong>
            <span :class="['estado', (personaSeleccionada.acreditacion || '').toLowerCase()]">{{ personaSeleccionada.acreditacion }}</span>
          </p>
        </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

      <!-- Datos ejemplo para pruebas -->

<script>
import InputBase from '@/components/Reutilizables/InputBase.vue'
import BaseSelect from '@/components/Reutilizables/BaseSelect.vue'
import BaseButton from '@/components/Reutilizables/BaseButton.vue'
import BaseAlert from '@/components/Reutilizables/BaseAlert.vue'

export default {
  name: 'GestionPersonas',
  components: { InputBase, BaseSelect, BaseButton, BaseAlert },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRama: '',
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
  personaSeleccionada: null,
      personas: [
        { nombre: 'JUAN PÉREZ GONZÁLEZ', rut: '12.345.678-9', email: 'juan.perez@email.com', telefono: '+56 9 1234 5678', profesion: 'INGENIERO', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO ARAUCO', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente' },
        { nombre: 'MARÍA GONZÁLEZ LÓPEZ', rut: '98.765.432-1', email: 'maria.gonzalez@email.com', telefono: '+56 9 2222 3333', profesion: 'DOCENTE', rol: 'PARTICIPANTE', rama: 'ROVERS', grupo: 'GRUPO LAUTARO', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'CARLOS RAMÍREZ SOTO', rut: '11.222.333-4', email: 'carlos.ramirez@email.com', telefono: '+56 9 5555 6666', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'PIONEROS', grupo: 'GRUPO CAUPOLICÁN', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente' },
        { nombre: 'ANA TORRES RIVERA', rut: '15.987.654-2', email: 'ana.torres@email.com', telefono: '+56 9 7777 8888', profesion: 'MÉDICO', rol: 'DIRIGENTE', rama: 'SCOUTS', grupo: 'GRUPO LEBU', zona: 'ZONA SUR', distrito: 'BIOBÍO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'PABLO MENDEZ', rut: '20.111.222-3', email: 'pablo.mendez@email.com', telefono: '+56 9 3333 4444', profesion: 'ARQUITECTO', rol: 'APOYO', rama: 'CASTORES', grupo: 'GRUPO CASTOR', zona: 'ZONA NORTE', distrito: 'SANTIAGO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'LAURA VEGA', rut: '21.222.333-4', email: 'laura.vega@email.com', telefono: '+56 9 4444 5555', profesion: 'ENFERMERA', rol: 'DIRIGENTE', rama: 'LOBATOS', grupo: 'GRUPO LOBITOS', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'MARIO LOPEZ', rut: '22.333.444-5', email: 'mario.lopez@email.com', telefono: '+56 9 6666 7777', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO SUR', zona: 'ZONA SUR', distrito: 'SANTIAGO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'SUSANA RIVERA', rut: '23.444.555-6', email: 'susana.rivera@email.com', telefono: '+56 9 8888 9999', profesion: 'DOCENTE', rol: 'APOYO', rama: 'PIONEROS', grupo: 'GRUPO PION', zona: 'ZONA NORTE', distrito: 'VALPARAÍSO', estado: 'Pendiente', inscripcion: 'Pendiente', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'RODRIGO CAMPOS', rut: '24.555.666-7', email: 'rodrigo.campos@email.com', telefono: '+56 9 1010 1111', profesion: 'INGENIERO', rol: 'DIRIGENTE', rama: 'ROVERS', grupo: 'GRUPO ROVER', zona: 'ZONA CENTRO', distrito: 'VALPARAÍSO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'ELENA FERNANDEZ', rut: '25.666.777-8', email: 'elena.fernandez@email.com', telefono: '+56 9 1212 1313', profesion: 'ABOGADA', rol: 'PARTICIPANTE', rama: 'CASTORES', grupo: 'GRUPO CASTOR 2', zona: 'ZONA NORTE', distrito: 'ANTOFAGASTA', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'ANDRES GOMEZ', rut: '26.777.888-9', email: 'andres.gomez@email.com', telefono: '+56 9 1414 1515', profesion: 'PROFESOR', rol: 'PARTICIPANTE', rama: 'LOBATOS', grupo: 'GRUPO LOBOS', zona: 'ZONA CENTRO', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente' },
        { nombre: 'VERONICA SALAS', rut: '27.888.999-0', email: 'veronica.salas@email.com', telefono: '+56 9 1616 1717', profesion: 'ENFERMERA', rol: 'APOYO', rama: 'SCOUTS', grupo: 'GRUPO SUR 2', zona: 'ZONA SUR', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'RICARDO PENA', rut: '28.999.000-1', email: 'ricardo.pena@email.com', telefono: '+56 9 1818 1919', profesion: 'TÉCNICO', rol: 'DIRIGENTE', rama: 'PIONEROS', grupo: 'GRUPO PION 2', zona: 'ZONA NORTE', distrito: 'IQUIQUE', estado: 'Pendiente', inscripcion: 'Pendiente', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'MARTA LOZANO', rut: '29.000.111-2', email: 'marta.lozano@email.com', telefono: '+56 9 2020 2121', profesion: 'ESTILISTA', rol: 'PARTICIPANTE', rama: 'ROVERS', grupo: 'GRUPO ROVER 2', zona: 'ZONA SUR', distrito: 'VALPARAÍSO', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'HUGO SANCHEZ', rut: '30.111.222-3', email: 'hugo.sanchez@email.com', telefono: '+56 9 2223 2324', profesion: 'MUSICO', rol: 'APOYO', rama: 'CASTORES', grupo: 'GRUPO CASTOR 3', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente' },
        { nombre: 'CAMILA RIOS', rut: '31.222.333-4', email: 'camila.rios@email.com', telefono: '+56 9 2425 2627', profesion: 'INGENIERA', rol: 'DIRIGENTE', rama: 'LOBATOS', grupo: 'GRUPO LOBOS 2', zona: 'ZONA SUR', distrito: 'CONCEPCIÓN', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'OSCAR NAVARRO', rut: '32.333.444-5', email: 'oscar.navarro@email.com', telefono: '+56 9 2728 2929', profesion: 'ESTUDIANTE', rol: 'PARTICIPANTE', rama: 'SCOUTS', grupo: 'GRUPO SUR 3', zona: 'ZONA SUR', distrito: 'TALCA', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Pendiente' },
        { nombre: 'LUIS FARIAS', rut: '33.444.555-6', email: 'luis.farias@email.com', telefono: '+56 9 3031 3233', profesion: 'AGRICULTOR', rol: 'APOYO', rama: 'PIONEROS', grupo: 'GRUPO PION 3', zona: 'ZONA NORTE', distrito: 'IQUIQUE', estado: 'Inscrito', inscripcion: 'Inscrito', pago: 'Confirmado', acreditacion: 'Aprobada' },
        { nombre: 'NICOLE MORA', rut: '34.555.666-7', email: 'nicole.mora@email.com', telefono: '+56 9 3334 3536', profesion: 'DOCTORA', rol: 'DIRIGENTE', rama: 'ROVERS', grupo: 'GRUPO ROVER 3', zona: 'ZONA CENTRO', distrito: 'SANTIAGO', estado: 'Preinscrito', inscripcion: 'Preinscrito', pago: 'Pendiente', acreditacion: 'Pendiente' }
      ]
    };
  },
  computed: {
    filtroMensaje() {
      return `Filtro activo: Solo se muestran personas con rol "${this.selectedRole}"`
    },
    personasFiltradas() {
      const q = (this.searchQuery || '').toLowerCase().trim();
      const selectedRoleNorm = (this.selectedRole || '').toString().trim().toUpperCase();
      const selectedRamaNorm = (this.selectedRama || '').toString().trim().toUpperCase();

      return this.personas.filter((p) => {
        const nombre = (p.nombre || '').toLowerCase();
        const rut = (p.rut || '').toLowerCase();
        const email = (p.email || '').toLowerCase();

        const coincideBusqueda =
          nombre.includes(q) ||
          rut.includes(q) ||
          email.includes(q);

        const pRolNorm = (p.rol || '').toString().trim().toUpperCase();
        const pRamaNorm = (p.rama || '').toString().trim().toUpperCase();

        const coincideRol = selectedRoleNorm ? pRolNorm === selectedRoleNorm : true;
        const coincideRama = selectedRamaNorm ? pRamaNorm === selectedRamaNorm : true;

        return coincideBusqueda && coincideRol && coincideRama;
      });
    }
  },
  methods: {
    seleccionar(persona) {
      this.personaSeleccionada = persona;
    },
    cerrarDetalle() {
      this.personaSeleccionada = null;
    },
    filtrar() {
      // Para se mantiene por compatibilidad
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
      // Exportar como CSV, No final 
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
  }
};
</script>

<style>
.gestion-personas {
  box-sizing: border-box;
  margin: 18px auto;
  padding: 18px 28px;
  background: #ffffff;
  color: #111;
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-family: Arial, sans-serif;
  max-width: 1100px;
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
}

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
  flex: 1 1 480px; 
  min-width: 260px;
  max-width: 900px;
  margin-bottom: 0; 
}
.filtros .base-input .base-field {
  padding: 10px 12px;
  font-size: 14px;
}
.filtros .base-select {
  flex: 0 0 180px; 
  min-width: 140px;
  max-width: 260px;
  margin-bottom: 0;
}
.filtros .base-select .base-select__element {
  padding: 8px 10px;
  font-size: 14px;
}
.filtros button {
  flex: 0 0 auto;
}

.buscar, .exportar {
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.buscar { background: #1e60af; color: #fff; }
.exportar { background: #22c55e; color: #fff; }

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
  -webkit-overflow-scrolling: touch;
}

.main-area {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  overflow: hidden; 
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  min-width: 0; 
}

th, td {
  padding: 18px 14px;
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
  .filtros input, .filtros select, .filtros .base-input, .filtros .base-select { width: 100%; }

  thead { display: none; }
  tr { display: block; margin-bottom: 12px; box-shadow: none; }
  td { display: flex; justify-content: space-between; border-bottom: 0; padding: 8px 6px; }
  .table-wrapper { overflow:auto; }
  td[data-label]::before { content: attr(data-label) ": "; font-weight:600; margin-right:6px; color:#333; }
}

@media (min-width: 1100px) {
  .main-area {
    flex-direction: column;
  }
  .list-area {
    flex: 1 1 auto;
  }
  .detail-panel {
    width: 100%;
    flex: 0 0 auto;
    border-left: none;
  }
  .table-wrapper { max-height: calc(100vh - 300px); }
  .detail-panel .detalle { padding: 18px 20px; }
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
