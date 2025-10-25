<template>
  <div class="layout-root">
    <div class="layout-content">
      <main class="main">
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
              @click="handleCardClick(card.title)"
              style="cursor:pointer;"
            />
          </section>

          <!-- Modals (appear as overlays; close by clicking outside) -->
          <div class="collapsible-table" v-show="tablaVisible === 'clases'">
            <div class="table-box">
              <h2>Totales por Clases</h2>
              <table class="stats-table compact">
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
            </div>
          </div>

          <div class="collapsible-table" v-show="tablaVisible === 'ramas'">
            <div class="table-box">
              <h2>Totales por Ramas</h2>
              <table class="stats-table compact">
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
            </div>
          </div>

          <div class="collapsible-table" v-show="tablaVisible === 'pendientes'">
            <div class="table-box">
              <h2>Pendientes por Grupo o Individuo</h2>
              <table class="stats-table compact">
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
                      <span v-if="pendiente.tipo === 'Grupo'" class="grupo-link" @click.stop="verMiembrosGrupo(pendiente)">{{ pendiente.nombre }}</span>
                      <span v-else>{{ pendiente.nombre }}</span>
                    </td>
                    <td>{{ pendiente.cantidad }}</td>
                  </tr>
                </tbody>
              </table>

              <!-- Miembros del grupo -->
              <div v-if="grupoSeleccionado" class="miembros-modal">
                <h3>Miembros de {{ grupoSeleccionado.nombre }}</h3>
                <ul class="miembros-list">
                  <li v-for="miembro in grupoSeleccionado.miembros" :key="miembro">{{ miembro }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Cursos: botón que abre modal resumida -->
          <section class="list-row compact-list">
            <h2>Cursos Disponibles</h2>
            <button class="courses-btn" @click="toggleCursos">Ver cursos</button>
          </section>

          <!-- Cursos modal -->
          <div class="collapsible-table" v-show="cursosVisible">
            <div class="table-box">
              <h2>Cursos Disponibles</h2>
              <div class="courses-list">
                <table class="stats-table compact">
                  <thead>
                    <tr>
                      <th>Curso</th>
                      <th>Inscritos</th>
                      <th>Capacidad</th>
                      <th>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="curso in cursosList" :key="curso.title">
                      <td>{{ curso.title }}</td>
                      <td>{{ curso.inscritos }}</td>
                      <td>{{ curso.capacidad }}</td>
                      <td><span :class="['badge-dot', cursoAlert(curso)]" aria-hidden="true"></span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
const sidebarOpen = ref(true)
import { ref, onMounted, onUnmounted } from 'vue'
import DataCard from '@/components/Reutilizables/DataCard.vue'
// DataCardList removed: courses shown via modal button
const resumenCards = ref([
  { title: 'Total Inscripciones', value: 120, icon: 'mdi-account-multiple', color: '#3498db' },
  { title: 'Acreditados', value: 85, icon: 'mdi-check-circle', color: '#2ecc71' },
  { title: 'Pendientes', value: 35, icon: 'mdi-alert-circle', color: '#e67e22' }
])

const cursosList = ref([
  { title: 'Formación de Dirigentes', inscritos: 22, capacidad: 25, icon: 'mdi-school', color: '#2980b9' },
  { title: 'Curso de Especialidades', inscritos: 10, capacidad: 20, icon: 'mdi-star', color: '#8e44ad' },
  { title: 'Curso Básico Scout', inscritos: 28, capacidad: 30, icon: 'mdi-campfire', color: '#16a085' }
])

// Removed detailed inscripciones and DataRow: dashboard is summarized

// Cursos modal state
const cursosVisible = ref(false)
function toggleCursos() {
  cursosVisible.value = !cursosVisible.value
}

function handleCardClick(title) {
  if (title === 'Total Inscripciones') return mostrarTabla('clases')
  if (title === 'Acreditados') return mostrarTabla('ramas')
  if (title === 'Pendientes') {
    // Toggle the pendientes inline popup; allow closing by clicking outside
    if (tablaVisible.value === 'pendientes') {
      cerrarTabla()
    } else {
      mostrarTabla('pendientes')
    }
  }
}

function cursoAlert(curso) {
  if (curso.inscritos >= curso.capacidad) return 'full'
  if (curso.inscritos >= curso.capacidad * 0.7) return 'near'
  return 'ok'
}

// Removed combined totals to keep dashboard summarized

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
const modalContentRef = ref(null)

function mostrarTabla(tipo) {
  tablaVisible.value = tipo
  // lock scroll only for full-screen modals (clases, ramas)
  if (tipo === 'clases' || tipo === 'ramas') {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
  // next tick focus modal
  setTimeout(() => {
    if (modalContentRef.value) modalContentRef.value.focus()
  }, 0)
}
function cerrarTabla() {
  tablaVisible.value = null
  grupoSeleccionado.value = null
  cursosVisible.value = false
  document.body.style.overflow = ''
}

// Close on Escape
function onKeydown(e) {
  if (e.key === 'Escape') cerrarTabla()
}
onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  // Try to load real data from the API. If the API is not available or CORS blocks us,
  // the dashboard will keep the sample data defined above.
  const API_BASE = '/api/' // project urls.py registers ApiScouts under /api/

  async function safeFetchModel(modelName) {
    try {
      const res = await fetch(API_BASE + encodeURIComponent(modelName) + '/')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      return data
    } catch (err) {
      // silent fallback: return null so caller keeps sample data
      console.warn('Failed to fetch', modelName, err)
      return null
    }
  }

  ;(async () => {
    // Fetch Cursos
    const cursos = await safeFetchModel('Curso')
    if (cursos && Array.isArray(cursos)) {
      // Map minimal fields into cursosList shape used by the UI
      cursosList.value = cursos.map(c => ({
        title: c.CUR_DESCRIPCION || c.CUR_CODIGO || c.CURS_ID || 'Curso',
        inscritos: parseInt(c._inscritos_count || 0) || 0,
        capacidad: parseInt(c.CUR_COTA_CON_ALMUERZO || c.CUR_COTA_SIN_ALMUERZO || c.CUR_CANT_PARTICIPANTE || 0) || 0
      }))
    }

    // Fetch Curso_Seccion to derive ramas or capacities if available
    const secciones = await safeFetchModel('Curso_Seccion')
    if (secciones && Array.isArray(secciones) && secciones.length > 0) {
      // Try to compute inscritos per rama if persona-curso links are present
      // We'll fetch Persona_Curso to compute counts
      const perCurso = await safeFetchModel('Persona_Curso')
      if (perCurso && Array.isArray(perCurso)) {
        // Build counts by curso-seccion id
        const countsByCus = {}
        perCurso.forEach(pc => {
          const cus = pc.CUS_ID || pc.cus_id || null
          if (!cus) return
          countsByCus[cus] = (countsByCus[cus] || 0) + 1
        })

        // augment cursosList with counts if CURS_ID/CUS_ID mapping available
        cursosList.value = cursosList.value.map(c => {
          // try find matching section by description or id
          const match = secciones.find(s => (s.CUS_ID === c.title || s.CUR_ID === c.CUR_ID))
          const inscritos = match ? (countsByCus[match.CUS_ID] || 0) : c.inscritos
          return { ...c, inscritos }
        })
      }
    }

    // Fetch Rama and Grupo lists to power ramasStats and pendientes
    const ramas = await safeFetchModel('Rama')
    if (ramas && Array.isArray(ramas)) {
      // map to ramasStats if not already present
      ramasStats.value = ramas.map(r => ({ rama: r.RAM_DESCRIPCION || r.RAM_ID, inscritos: 0, acreditados: 0 }))
    }

    const grupos = await safeFetchModel('Grupo')
    if (grupos && Array.isArray(grupos)) {
      // map a pendientes groups
      const gruposPend = grupos.slice(0, 6).map(g => ({ tipo: 'Grupo', nombre: g.GRU_DESCRIPCION || g.GRU_ID, cantidad: 0, miembros: [] }))
      // Try fetch Persona_Grupo to get members
      const pg = await safeFetchModel('Persona_Grupo')
      if (pg && Array.isArray(pg)) {
        const membersByGroup = {}
        pg.forEach(item => {
          const gru = item.GRU_ID || item.gru_id || null
          const per = item.PER_ID || item.per_id || null
          if (!gru) return
          membersByGroup[gru] = membersByGroup[gru] || []
          membersByGroup[gru].push(per)
        })
        gruposPend.forEach(g => {
          // match group by id or description
          const match = grupos.find(x => x.GRU_DESCRIPCION === g.nombre || x.GRU_ID === g.nombre)
          if (match) {
            const id = match.GRU_ID
            g.miembros = (membersByGroup[id] || []).slice(0, 12)
            g.cantidad = (membersByGroup[id] || []).length
          }
        })
      }
      pendientesStats.value = gruposPend.concat(pendientesStats.value.filter(p => p.tipo !== 'Grupo'))
    }
  })()
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
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
  position: relative; /* anchor popups */
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

/* collapsible inline tables */
.collapsible-table { overflow: hidden; max-height: 0; transition: max-height 260ms ease, opacity 200ms ease; opacity: 0; }
.collapsible-table[style], .collapsible-table[aria-expanded='true'], .collapsible-table[v-cloak] { opacity: 1 }
.collapsible-table[style] { /* v-show adds inline style display:block; so this helps animate */ max-height: 1200px; }
.table-box { background: #fff; border-radius: 12px; padding: 1rem; width: 100%; box-shadow: 0 6px 18px rgba(0,0,0,0.04); }

/* Inline popups anchored to panel-container */
.panel-container { position: relative; }
.inline-popup {
  position: absolute;
  inset: auto 1.5rem auto 1.5rem;
  display: block;
  background: transparent;
  align-items: flex-start;
  justify-content: flex-start;
  /* allow clicks on overlay so clicking outside popup will close it */
  pointer-events: auto;
}
.inline-popup .modal-content.popup {
  pointer-events: auto;
  position: absolute;
  right: 1.5rem;
  top: 4.2rem;
  width: 420px;
  max-width: calc(100% - 3rem);
  transform-origin: top right;
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
  transition: transform 260ms cubic-bezier(.2,.9,.2,1), opacity 220ms ease;
  padding: 0.8rem;
}
.inline-popup .modal-content.popup {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.inline-popup .modal-content.popup::after {
  content: '';
  position: absolute;
  top: -8px;
  right: 18px;
  width: 12px;
  height: 12px;
  transform: rotate(45deg);
  background: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

/* small card hover/focus animation */
.cards-row .data-card { transition: transform 180ms ease, box-shadow 180ms ease; }
.cards-row .data-card:hover, .cards-row .data-card:focus { transform: translateY(-6px); box-shadow: 0 12px 26px rgba(0,0,0,0.08); }

/* badge pulse for near/full */
.badge { transition: transform 240ms ease, box-shadow 240ms ease; }
.badge.near { animation: pulse 2.4s infinite; }
.badge.full { animation: pulse-strong 2s infinite; }

/* badge-dot: small circular indicator (no text) */
.badge-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; }
.badge-dot.ok { background: #2ecc71; }
.badge-dot.near { background: #e67e22; box-shadow: 0 6px 18px rgba(230,126,34,0.08); animation: pulse 2.4s infinite; }
.badge-dot.full { background: #e74c3c; box-shadow: 0 8px 20px rgba(231,76,60,0.1); animation: pulse-strong 2s infinite; }

@keyframes pulse {
  0% { transform: scale(1); box-shadow: none }
  50% { transform: scale(1.04); box-shadow: 0 6px 18px rgba(230,126,34,0.12) }
  100% { transform: scale(1); box-shadow: none }
}
@keyframes pulse-strong {
  0% { transform: scale(1); box-shadow: none }
  50% { transform: scale(1.06); box-shadow: 0 8px 20px rgba(231,76,60,0.14) }
  100% { transform: scale(1); box-shadow: none }
}
.stats-table.compact th, .stats-table.compact td {
  padding: 0.4rem 0.6rem;
}
.miembros-modal {
  margin-top: 0.6rem;
  background: #fafafa;
  padding: 0.6rem;
  border-radius: 6px;
}

/* Courses modal */
.courses-btn {
  background: linear-gradient(90deg,#2980b9,#16a085);
  color: #fff;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}
.courses-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.course-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem;
  background: #fff;
  border: 1px solid #eef3f7;
  border-radius: 6px;
}
.badge {
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  color: #fff;
}
.badge.full { background: #e74c3c; }
.badge.near { background: #e67e22; }
.badge.ok { background: #2ecc71; }

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
