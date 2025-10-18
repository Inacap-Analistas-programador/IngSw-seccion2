<<<<<<< HEAD
<template>
  <div class="gestion-personas">
    <div class="header">
      <h2>Gestión de Personas - Módulo Centralizado</h2>
      <h3>Gestión Centralizada de Participantes</h3>
    </div>

    <!-- Barra de búsqueda y filtros -->
    <div class="filtros">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por nombre, RUT, email..."
      />
      <select v-model="selectedRole">
        <option value="">Todos los roles</option>
        <option value="PARTICIPANTE">Participante</option>
        <option value="DIRIGENTE">Dirigente</option>
        <option value="APOYO">Apoyo</option>
      </select>
      <select v-model="selectedRama">
        <option value="">Todas las ramas</option>
        <option value="CASTORES">Castores</option>
        <option value="LOBATOS">Lobatos</option>
        <option value="SCOUTS">Scouts</option>
        <option value="PIONEROS">Pioneros</option>
        <option value="ROVERS">Rovers</option>
      </select>
      <button class="buscar" @click="filtrar">Buscar</button>
      <button class="exportar" @click="exportarExcel">📊 Exportar</button>
    </div>

    <!-- Mensaje de filtro activo -->
    <div
      v-if="selectedRole"
      class="filtro-activo"
    >
      Filtro activo: Solo se muestran personas con rol "{{ selectedRole }}"
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
            <button class="editar" @click="seleccionar(p)">
              Ver/Editar
            </button>
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
export default {
  name: 'GestionPersonas',
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRama: '',
      personaSeleccionada: null,
      personas: [
        {
          nombre: 'JUAN PÉREZ GONZÁLEZ',
          rut: '12.345.678-9',
          email: 'juan.perez@email.com',
          telefono: '+56 9 1234 5678',
          profesion: 'INGENIERO',
          rol: 'PARTICIPANTE',
          rama: 'SCOUTS',
          grupo: 'GRUPO ARAUCO',
          zona: 'ZONA SUR',
          distrito: 'BIOBÍO',
          estado: 'Inscrito',
          inscripcion: 'Inscrito',
          pago: 'Confirmado',
          acreditacion: 'Pendiente'
        },
        {
          nombre: 'MARÍA GONZÁLEZ LÓPEZ',
          rut: '98.765.432-1',
          email: 'maria.gonzalez@email.com',
          telefono: '+56 9 2222 3333',
          profesion: 'DOCENTE',
          rol: 'PARTICIPANTE',
          rama: 'ROVERS',
          grupo: 'GRUPO LAUTARO',
          zona: 'ZONA SUR',
          distrito: 'BIOBÍO',
          estado: 'Preinscrito',
          inscripcion: 'Preinscrito',
          pago: 'Pendiente',
          acreditacion: 'Pendiente'
        },
        {
          nombre: 'CARLOS RAMÍREZ SOTO',
          rut: '11.222.333-4',
          email: 'carlos.ramirez@email.com',
          telefono: '+56 9 5555 6666',
          profesion: 'ESTUDIANTE',
          rol: 'PARTICIPANTE',
          rama: 'PIONEROS',
          grupo: 'GRUPO CAUPOLICÁN',
          zona: 'ZONA SUR',
          distrito: 'BIOBÍO',
          estado: 'Inscrito',
          inscripcion: 'Inscrito',
          pago: 'Confirmado',
          acreditacion: 'Pendiente'
        },
        {
          nombre: 'ANA TORRES RIVERA',
          rut: '15.987.654-2',
          email: 'ana.torres@email.com',
          telefono: '+56 9 7777 8888',
          profesion: 'MÉDICO',
          rol: 'DIRIGENTE',
          rama: 'SCOUTS',
          grupo: 'GRUPO LEBU',
          zona: 'ZONA SUR',
          distrito: 'BIOBÍO',
          estado: 'Inscrito',
          inscripcion: 'Inscrito',
          pago: 'Confirmado',
          acreditacion: 'Aprobada'
        }
      ]
    };
  },
  computed: {
    personasFiltradas() {
      return this.personas.filter((p) => {
        const coincideBusqueda =
          p.nombre.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          p.rut.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          p.email.toLowerCase().includes(this.searchQuery.toLowerCase());

        const coincideRol = this.selectedRole
          ? p.rol === this.selectedRole
          : true;
        const coincideRama = this.selectedRama
          ? p.rama === this.selectedRama
          : true;

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
  position: fixed;
  inset: 0; 
  box-sizing: border-box;
  margin: 0;
  padding: 18px 28px;
  background: #ffffff;
  color: #111; 
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-family: Arial, sans-serif;
  overflow: hidden; 
  z-index: 1000;
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
  .filtros input, .filtros select { width: 100%; }

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


=======
<script setup>
import NavBar from './components/Reutilizables/NavBar.vue'
</script>

<template>
		<div class="app-root">
			<NavBar />
			<main class="main-full">
				<router-view />
			</main>
		</div>
</template>

<style>
>>>>>>> fe3ca806e3592a744d4e2b2f7b27c752cbbeef0d
</style>
