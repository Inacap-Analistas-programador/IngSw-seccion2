<template>
  <div class="vista-pagos">
    <h1 class="titulo-vista">Gestión de Pagos</h1>

    <div class="layout-dos-columnas">

      <div class="columna-izquierda">
        <h2>Buscar Participante</h2>

        <div class="form-grupo">
          <label for="buscar-persona">Buscar por Persona (Nombre o RUT)</label>
          <input type="text" id="buscar-persona" placeholder="Ej: Juan Pérez..." class="input-grande">
        </div>
        <div class="form-grupo">
          <label for="buscar-grupo">Filtrar por Grupo</label>
          <select id="buscar-grupo"><option value="">Todos los grupos</option></select>
        </div>
        <div class="form-grupo">
          <label for="buscar-curso">Filtrar por Curso</label>
          <select id="buscar-curso"><option value="">Todos los cursos</option></select>
        </div>
        
        <div class="resultados-busqueda">
          <p>Resultados:</p>
          <ul>
            <li>
              <span>Macarena Rojas (Grupo 1) - Curso A</span>
              <div class="acciones-resultado">
                <button class="boton-accion ver">Ver</button>
                <button class="boton-accion modificar">Modificar</button>
                <button class="boton-accion eliminar">Eliminar</button>
              </div>
            </li>
            <li>
              <span>Juan Pérez (Grupo 2) - Curso B</span>
              <div class="acciones-resultado">
                <button class="boton-accion ver">Ver</button>
                <button class="boton-accion modificar">Modificar</button>
                <button class="boton-accion eliminar">Eliminar</button>
              </div>
            </li>
            </ul>
        </div>
        
        <div class="historico-simple">
          <h3>Histórico General</h3>
          <p>Mostrando los últimos 20 pagos registrados.</p>
          </div>
      </div>

      <div class="columna-derecha">
        <h2>Registrar Nuevo Pago</h2>
        <div class="form-grupo">
          <label for="grupo">Grupo</label>
          <select id="grupo" v-model="pago.grupo">
            <option value="">Seleccione un grupo</option>
            <option value="g1">Grupo 1</option>
            <option value="g2">Grupo 2</option>
          </select>
        </div>

        <div class="form-grupo">
          <label for="curso">Curso(s)</label>
          <select id="curso" v-model="pago.cursos" multiple>
            <option value="c1">Curso A</option>
            <option value="c2">Curso B</option>
            <option value="c3">Curso C</option>
          </select>
        </div>

        <div class="form-grupo">
          <label for="valor">Valor Pagado</label>
          <input type="number" id="valor" v-model="pago.valor" placeholder="Ej: 25000">
        </div>

        <div class="form-grupo">
          <label for="archivo">Comprobante de Pago</label>
          <input type="file" id="archivo">
        </div>

        <button class="boton-guardar">Guardar Pago</button>

        <hr class="divisor">

        <h2>Registro Masivo</h2>
        <p>
          Para activar el registro masivo, primero debe seleccionar un Grupo y al menos un Curso.
        </p>
        <button 
          class="boton-masivo" 
          :disabled="!pago.grupo || pago.cursos.length === 0">
          Cargar Archivo Masivo (Excel)
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Estado para el formulario de pago
const pago = ref({
  grupo: '',
  cursos: [],
  valor: null,
  archivo: null
});
</script>

<style scoped>
.vista-pagos {
  padding: 10px;
}
.titulo-vista {
  /* (Requisito 1: "más grande") */
  color: #1e3a8a;
  font-size: 2rem; /* 32px */
  font-weight: 600;
  margin-bottom: 20px;
}
.layout-dos-columnas {
  display: grid;
  /* (Requisito 1: "buscar izquierda") */
  grid-template-columns: 1.2fr 1fr; /* Columna izquierda más ancha */
  gap: 30px;
}
.columna-izquierda, .columna-derecha {
  background: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
h2 {
  font-size: 1.5rem; /* 24px */
  font-weight: 500;
  color: #1e3a8a;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
  margin-bottom: 20px;
}
.form-grupo {
  margin-bottom: 15px;
}
.form-grupo label {
  display: block;
  font-weight: 500;
  margin-bottom: 5px;
  color: #555;
}
.form-grupo input,
.form-grupo select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}
/* (Requisito 1: "más grande" para input de búsqueda) */
.input-grande {
  font-size: 1.15rem;
  padding: 12px;
}
.form-grupo select[multiple] {
  height: 100px;
}
.divisor {
  margin: 30px 0;
  border: 0;
  border-top: 1px solid #eee;
}
button {
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.boton-guardar {
  background: #2563eb;
  color: white;
}
.boton-guardar:hover {
  background: #1e3a8a;
}
.boton-masivo {
  background: #10b981;
  color: white;
}
.boton-masivo:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Columna Izquierda (Búsqueda) */
.resultados-busqueda {
  margin-top: 20px;
}
.resultados-busqueda ul {
  list-style: none;
  padding: 0;
  margin-top: 10px;
}
.resultados-busqueda li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

/* --- ESTILOS AÑADIDOS PARA LOS BOTONES --- */
.acciones-resultado {
  display: flex;
  gap: 5px;
}
.boton-accion {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 4px 8px; /* Más pequeños */
  border-radius: 4px;
}
.boton-accion.ver {
  background: #45af57; /* Gris */
  color: white;
}
.boton-accion.modificar {
  background: #f59e0b; /* Amarillo */
  color: white;
}
.boton-accion.eliminar {
  background: #dc2626; /* Rojo */
  color: white;
}
/* ------------------------------------------- */

.historico-simple {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px dashed #ccc;
}
</style>