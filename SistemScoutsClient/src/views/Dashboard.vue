<template>
  <div class="panel-container">
    <header class="panel-header">
      <h1>Panel de Control<br><span class="panel-sub">Segmentado por Curso</span></h1>
    </header>

    <!-- Tarjetas resumen -->
    <section class="cards-row">
      <DataCard
        v-for="card in resumenCards"
        :key="card.title"
        :title="card.title"
        :value="card.value"
        :icon="card.icon"
        :color="card.color"
        @click="card.title === 'Total Inscripciones' ? mostrarTabla('clases') : card.title === 'Acreditados' ? mostrarTabla('ramas') : card.title === 'Pendientes' ? mostrarTabla('pendientes') : null"
        style="cursor:pointer;"
      />
    </section>

    <!-- Tabla de Clases -->
    <section v-if="tablaVisible === 'clases'" class="stats-row">
      <div class="tabla-header">
        <h2>Totales por Clases</h2>
        <button @click="cerrarTabla" class="close-btn">Cerrar</button>
      </div>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Clase</th>
            <th>Inscritos</th>
            <th>Acreditados</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="clase in clasesStats" :key="clase.clase">
            <td>{{ clase.clase }}</td>
            <td>{{ clase.inscritos }}</td>
            <td>{{ clase.acreditados }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Tabla de Ramas -->
    <section v-if="tablaVisible === 'ramas'" class="stats-row">
      <div class="tabla-header">
        <h2>Totales por Ramas</h2>
        <button @click="cerrarTabla" class="close-btn">Cerrar</button>
      </div>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Rama</th>
            <th>Inscritos</th>
                  <th>Acreditados</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="rama in ramasStats" :key="rama.rama">
                  <td>{{ rama.rama }}</td>
                  <td>{{ rama.inscritos }}</td>
                  <td>{{ rama.acreditados }}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <!-- Tabla de Pendientes -->
          <section v-if="tablaVisible === 'pendientes'" class="stats-row">
            <div class="tabla-header">
              <h2>Pendientes por Grupo o Individuo</h2>
              <button @click="cerrarTabla" class="close-btn">Cerrar</button>
            </div>
            <table class="stats-table">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Nombre</th>
                  <th>Cantidad</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pendiente in pendientesStats" :key="pendiente.tipo + '-' + pendiente.nombre">
                  <td>{{ pendiente.tipo }}</td>
                  <td>
                    <span v-if="pendiente.tipo === 'Grupo'" class="grupo-link" @click="verMiembrosGrupo(pendiente)">{{ pendiente.nombre }}</span>
                    <span v-else>{{ pendiente.nombre }}</span>
                  </td>
                  <td>{{ pendiente.cantidad }}</td>
                </tr>
              </tbody>
            </table>

            <!-- Miembros del grupo -->
            <div v-if="grupoSeleccionado" class="miembros-modal">
              <div class="tabla-header">
                <h3>Miembros de {{ grupoSeleccionado.nombre }}</h3>
                <button @click="cerrarMiembrosGrupo" class="close-btn">Cerrar</button>
              </div>
              <ul class="miembros-list">
                <li v-for="miembro in grupoSeleccionado.miembros" :key="miembro">{{ miembro }}</li>
              </ul>
            </div>
          </section>

          <!-- Lista de cursos -->
          <section class="list-row">
            <h2>Cursos Disponibles</h2>
            <DataCardList :items="cursosList" />
          </section>

          <!-- Fila de datos (DataRow) -->
          <section class="datarow-row">
            <h2>Detalle Seleccionado</h2>
            <table style="width:100%">
              <tbody>
                <DataRow :rowData="dataRowObject" :fields="['Usuario','Curso','Estado']" />
              </tbody>
            </table>
          </section>

          <!-- Tabla de inscripciones -->
          <section class="table-row wide-table-row">
            <h2>Últimas Inscripciones</h2>
            <DataTable :columns="tableColumns" :rows="inscripciones" />
          </section>
        </div>
      
</template>

<script setup>
import { ref, onMounted } from 'vue'
const sidebarOpen = ref(true)
import DataCard from '@/components/Reutilizables/DataCard.vue'
import DataCardList from '@/components/Reutilizables/DataCardList.vue'
import DataTable from '@/components/Reutilizables/DataTable.vue'
import DataRow from '@/components/Reutilizables/DataRow.vue'
const resumenCards = ref([
  { title: 'Total Inscripciones', value: 120, icon: 'mdi-account-multiple', color: '#3498db' },
  { title: 'Acreditados', value: 85, icon: 'mdi-check-circle', color: '#2ecc71' },
  { title: 'Pendientes', value: 35, icon: 'mdi-alert-circle', color: '#e67e22' }
])

const cursosList = ref([
  { title: 'Formación de Dirigentes', description: 'Curso para líderes scouts', icon: 'mdi-school', color: '#2980b9' },
  { title: 'Curso de Especialidades', description: 'Especialidades scouts', icon: 'mdi-star', color: '#8e44ad' },
  { title: 'Curso Básico Scout', description: 'Curso inicial para scouts', icon: 'mdi-campfire', color: '#16a085' }
])

const tableColumns = [
  { label: 'FechaHora', field: 'fecha' },
  { label: 'Nombre', field: 'nombre' },
  { label: 'Curso', field: 'curso' },
  { label: 'Estado', field: 'estado' }
]

const inscripciones = ref([])

// Ejemplo de datos para DataRow
const dataRowObject = ref({
  Usuario: 'JUAN PÉREZ GONZÁLEZ',
  Curso: 'SCOUTS',
})

// Simula llamada a API
async function fetchInscripciones() {
  // Aquí iría la llamada real a la API
  await new Promise(resolve => setTimeout(resolve, 500))
  inscripciones.value = [
    { fecha: '26/09/2015 12:55', nombre: 'JUAN PÉREZ GONZÁLEZ', curso: 'SCOUTS', estado: 'Acreditado' },
    { fecha: '26/09/2015 12:52', nombre: 'MARÍA RAMÍREZ LÓPEZ', curso: 'ROVERS', estado: 'Pendiente' },
    { fecha: '26/09/2015 12:50', nombre: 'CARLOS RAMÍREZ SOTO', curso: 'PIONEROS', estado: 'Acreditado' }
  ]
}

onMounted(() => {
  fetchInscripciones()
})

// Totales combinados por clase y rama (ejemplo básico)
const totalesCombinados = ref([
  { clase: 'Clase 1', rama: 'Rama Lobatos', inscritos: 15, acreditados: 10 },
  { clase: 'Clase 1', rama: 'Rama Scouts', inscritos: 15, acreditados: 12 },
  { clase: 'Clase 1', rama: 'Rama Rovers', inscritos: 10, acreditados: 8 },
  { clase: 'Clase 2', rama: 'Rama Lobatos', inscritos: 10, acreditados: 8 },
  { clase: 'Clase 2', rama: 'Rama Scouts', inscritos: 25, acreditados: 20 },
  { clase: 'Clase 2', rama: 'Rama Rovers', inscritos: 15, acreditados: 12 },
  { clase: 'Clase 3', rama: 'Rama Lobatos', inscritos: 5, acreditados: 4 },
  { clase: 'Clase 3', rama: 'Rama Scouts', inscritos: 15, acreditados: 13 },
  { clase: 'Clase 3', rama: 'Rama Rovers', inscritos: 10, acreditados: 8 }
])

const clasesStats = ref([
  { clase: 'Clase 1', inscritos: 40, acreditados: 30 },
  { clase: 'Clase 2', inscritos: 50, acreditados: 40 },
  { clase: 'Clase 3', inscritos: 30, acreditados: 15 }
])

const ramasStats = ref([
  { rama: 'Rama Lobatos', inscritos: 25, acreditados: 20 },
  { rama: 'Rama Scouts', inscritos: 55, acreditados: 45 },
  { rama: 'Rama Rovers', inscritos: 40, acreditados: 20 }
])

const pendientesStats = ref([
  { tipo: 'Grupo', nombre: 'Grupo Scout A', cantidad: 12, miembros: ['Pedro González', 'Ana López', 'Luis Soto', 'María Ramírez', 'Carlos Soto', 'Juan Pérez', 'Sofía Torres', 'Miguel Díaz', 'Lucía Gómez', 'Andrés Fuentes', 'Valentina Ríos', 'Jorge Herrera'] },
  { tipo: 'Grupo', nombre: 'Grupo Scout B', cantidad: 8, miembros: ['Martín Silva', 'Paula Castro', 'Diego Paredes', 'Camila Ruiz', 'Esteban Bravo', 'Isabel Soto', 'Tomás Vidal', 'Gabriela Muñoz'] },
  { tipo: 'Individuo', nombre: 'Pedro González', cantidad: 1 },
  { tipo: 'Individuo', nombre: 'Ana López', cantidad: 2 },
  { tipo: 'Individuo', nombre: 'Luis Soto', cantidad: 12 }
])

const grupoSeleccionado = ref(null)
function verMiembrosGrupo(grupo) {
  grupoSeleccionado.value = grupo
}
function cerrarMiembrosGrupo() {
  grupoSeleccionado.value = null
}

const tablaVisible = ref(null) // 'clases' | 'ramas' | null
function mostrarTabla(tipo) {
  tablaVisible.value = tipo
}
function cerrarTabla() {
  tablaVisible.value = null
}
</script>

<style scoped>
.sidebar-toggle {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 100;
  background: #223046;
  border: none;
  border-radius: 4px;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.hamburger {
  display: block;
  width: 24px;
  height: 3px;
  background: #fff;
  position: relative;
}
.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  left: 0;
  width: 24px;
  height: 3px;
  background: #fff;
  transition: 0.3s;
}
.hamburger::before {
  top: -8px;
}
.hamburger::after {
  top: 8px;
}
.SideBar {
  transition: transform 0.3s, width 0.3s;
}
.SideBar:not(.open) {
  transform: translateX(-100%);
}
.main.sidebar-closed {
  margin-left: 0;
  width: 100%;
}
@media (max-width: 900px) {
  .sidebar-toggle {
    display: flex;
  }
  .SideBar {
    width: 220px;
    min-width: 180px;
    max-width: 220px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 10;
    box-shadow: 1px 0px 6px 0px rgba(0,0,0,0.07);
    transition: transform 0.3s, width 0.3s;
  }
  .SideBar:not(.open) {
    transform: translateX(-100%);
  }
  .main {
    margin-left: 0;
    width: 100vw;
  }
  .main.sidebar-closed {
    margin-left: 0;
    width: 100vw;
  }
}
.layout-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: #f0f2f5;
  overflow-x: hidden;
}

.layout-content {
  display: flex;
  flex-direction: row;
  flex: 1;
  width: 100%;
  min-height: 0;
  height: 100vh;
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem 0;
  min-height: 0;
  margin-left: 0;
  width: 100%;
  transition: margin-left 0.3s, width 0.3s;
}

.panel-container {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  max-width: 900px;
  width: 100%;
  padding: 2rem 2rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

/* Ensure readable text inside the white panel even if global theme sets light text */
.panel-container, .panel-container * {
  color: #222 !important;
}


.SideBar {
  width: 260px;
  min-width: 220px;
  max-width: 260px;
  height: 100vh;
  background: #223046;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 2;
  flex-shrink: 0;
  box-shadow: 1px 0px 6px 0px rgba(0,0,0,0.07);
  transition: width 0.3s;
}

.panel-header {
  width: 100%;
  text-align: center;
  margin-bottom: 0.5rem;
}

.panel-header h1 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.2rem;
  letter-spacing: 1px;
}

.panel-sub {
  font-size: 0.9rem;
  color: #34495e;
  font-weight: 400;
}



.cards-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.7rem;
  width: 100%;
  justify-content: center;
}



.list-row {
  margin-bottom: 0.7rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 0.5rem 0 0.5rem 0;
}



.datarow-row {
  margin-bottom: 0.7rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 0.5rem 0 0.5rem 0;
}




.table-row {
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 0.5rem 0.2rem;
  width: 100%;
  max-width: 350px;
  margin: 0 auto;
}


.wide-table-row {
  max-width: 900px;
  width: 100%;
}



h2 {
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
  text-align: left;
  width: 100%;
  color: #34495e;
  font-weight: 600;
}




.tabla-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.close-btn {
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.3rem 0.7rem;
  cursor: pointer;
  font-size: 0.9rem;
}

@media (max-width: 900px) {
  .main {
    padding: 1rem 0;
  }
  .panel-container {
    max-width: 98vw;
    width: 98vw;
    padding: 1rem 0.5rem;
    margin: 0 auto;
    gap: 1rem;
  }
  .SideBar {
    width: 60px;
    min-width: 60px;
    max-width: 60px;
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
  }
  .main {
    margin-left: 60px;
    width: calc(100% - 60px);
  }
  .wide-table-row {
    max-width: 99vw;
  }
}

@media (max-width: 600px) {
  .layout-content {
    flex-direction: column;
    height: auto;
  }
  .SideBar {
    position: relative;
    width: 100vw;
    min-width: 0;
    max-width: 100vw;
    height: 56px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    display: flex;
    align-items: center;
    justify-content: flex-start;
    top: 0;
    left: 0;
    z-index: 2;
  }
  .main {
    margin-left: 0;
    width: 100vw;
    padding: 1rem 0.2rem;
  }
  .panel-container {
    max-width: 99vw;
    padding: 0.5rem 0.2rem;
    gap: 0.5rem;
  }
  .cards-row {
    flex-direction: column;
    gap: 0.2rem;
    align-items: center;
  }
  .panel-header h1 {
    font-size: 0.8rem;
  }
  h2 {
    font-size: 0.7rem;
  }
}

@media (max-width: 600px) {
  .main {
    padding: 0.5rem 0;
  }
  .panel-container {
    max-width: 99vw;
    width: 99vw;
    padding: 0.5rem 0.2rem;
    gap: 0.5rem;
    margin: 0 auto;
  }
  .cards-row {
    flex-direction: column;
    gap: 0.2rem;
    align-items: center;
  }
  .panel-header h1 {
    font-size: 0.8rem;
  }
  h2 {
    font-size: 0.7rem;
  }
}

.grupo-link {
  color: #2980b9;
  text-decoration: underline;
  cursor: pointer;
}
.miembros-modal {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 1rem;
  margin-top: 1rem;
  width: 100%;
  max-width: 400px;
}
.miembros-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}
.miembros-list li {
  padding: 0.3rem 0;
  border-bottom: 1px solid #e0e0e0;
}
.miembros-list li:last-child {
  border-bottom: none;
}
</style>