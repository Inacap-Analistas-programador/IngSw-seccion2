<template>
  <div class="dashboard-container">
    
    <!-- ==================== GRÁFICO DE RECAUDACIÓN ==================== -->
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <!-- ==================== LISTA DE CURSOS ==================== -->
    <div class="course-list">
      <h2>Listado de Cursos</h2>
      <div
        v-for="curso in cursos"
        :key="curso.id"
        class="course-item"
        :class="{
          'curso-ok': curso.porcentaje >= 49 && curso.encargado,
          'curso-error': curso.porcentaje < 49 || !curso.encargado
        }"
        @click="abrirPopup(curso)"
      >
        <div class="course-info">
          <h3>{{ curso.nombre }}</h3>
          <p>Recaudado: ${{ curso.recaudado.toLocaleString() }}</p>
          <p>Estimado: ${{ curso.estimado.toLocaleString() }}</p>
          <p>Encargado: {{ curso.encargado || 'No asignado' }}</p>
        </div>
      </div>
    </div>

    <!-- ==================== POPUP DETALLES ==================== -->
    <div v-if="mostrarPopup" class="popup-overlay" @click.self="cerrarPopup">
      <div class="popup-content">
        <h2>Detalles del Curso</h2>
        <p><strong>Nombre:</strong> {{ cursoSeleccionado.nombre }}</p>
        <p><strong>Encargado:</strong> {{ cursoSeleccionado.encargado || 'No asignado' }}</p>
        <p><strong>Recaudado:</strong> ${{ cursoSeleccionado.recaudado.toLocaleString() }}</p>
        <p><strong>Estimado:</strong> ${{ cursoSeleccionado.estimado.toLocaleString() }}</p>
        <p><strong>Lugar:</strong> {{ cursoSeleccionado.lugar }}</p>
        <p><strong>Participantes:</strong> {{ cursoSeleccionado.participantes }}</p>
        <button class="btn-cerrar" @click="cerrarPopup">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      cursos: [
        { id: 1, nombre: "Curso de Liderazgo Scout", recaudado: 250000, estimado: 400000, encargado: "Juan Pérez", lugar: "Sede Central", participantes: 25 },
        { id: 2, nombre: "Curso de Supervivencia", recaudado: 100000, estimado: 300000, encargado: null, lugar: "Parque Nacional", participantes: 18 },
        { id: 3, nombre: "Curso de Primeros Auxilios", recaudado: 280000, estimado: 280000, encargado: "María González", lugar: "Hospital Local", participantes: 22 },
        { id: 4, nombre: "Curso de Navegación", recaudado: 200000, estimado: 500000, encargado: "Pedro Ramírez", lugar: "Base Costera", participantes: 30 }
      ],
      mostrarPopup: false,
      cursoSeleccionado: {},
    };
  },
  mounted() {
    this.calcularPorcentajes();
    this.generarGrafico();
  },
  methods: {
    calcularPorcentajes() {
      this.cursos = this.cursos.map(c => ({
        ...c,
        porcentaje: (c.recaudado / c.estimado) * 100
      }));
    },
    generarGrafico() {
      const canvas = this.$refs.chartCanvas;
      const ctx = canvas.getContext("2d");

      const ancho = canvas.width = 800;
      const alto = canvas.height = 400;

      const maxValor = Math.max(...this.cursos.map(c => c.estimado)) * 1.2;
      const margen = 60;
      const espacioBarra = (ancho - margen * 2) / this.cursos.length;

      // Fondo
      ctx.fillStyle = "#fff";
      ctx.fillRect(0, 0, ancho, alto);

      // Ejes
      ctx.beginPath();
      ctx.moveTo(margen, margen);
      ctx.lineTo(margen, alto - margen);
      ctx.lineTo(ancho - margen, alto - margen);
      ctx.strokeStyle = "#000";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Eje Y
      ctx.font = "12px Arial";
      ctx.fillStyle = "#000";
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";

      const numLineas = 5;
      for (let i = 0; i <= numLineas; i++) {
        const valor = Math.round((maxValor / numLineas) * i);
        const y = alto - margen - (valor / maxValor) * (alto - margen * 2);
        ctx.fillText(`$${valor.toLocaleString()}`, margen - 10, y);
        ctx.beginPath();
        ctx.moveTo(margen, y);
        ctx.lineTo(ancho - margen, y);
        ctx.strokeStyle = "#ddd";
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Dibujar barras combinadas
      this.cursos.forEach((curso, index) => {
        const x = margen + index * espacioBarra + espacioBarra / 4;
        const anchoBarra = espacioBarra / 2;

        const alturaEstimado = (curso.estimado / maxValor) * (alto - margen * 2);
        const alturaRecaudado = (curso.recaudado / maxValor) * (alto - margen * 2);

        const yEstimado = alto - margen - alturaEstimado;
        const yRecaudado = alto - margen - alturaRecaudado;

        // Azul (estimado)
        ctx.fillStyle = "rgba(0, 100, 255, 0.4)";
        ctx.fillRect(x, yEstimado, anchoBarra, alturaEstimado);

        // Verde (recaudado encima)
        ctx.fillStyle = "rgba(0, 200, 0, 0.8)";
        ctx.fillRect(x, yRecaudado, anchoBarra, alturaRecaudado);

        // Nombre curso
        ctx.fillStyle = "#000";
        ctx.font = "12px Arial";
        ctx.textAlign = "center";
        ctx.fillText(curso.nombre, x + anchoBarra / 2, alto - margen + 20);
      });
    },
    abrirPopup(curso) {
      this.cursoSeleccionado = curso;
      this.mostrarPopup = true;
    },
    cerrarPopup() {
      this.mostrarPopup = false;
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  background-color: #f0f2f5;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.dashboard-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.chart-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.course-list {
  margin-top: 30px;
  background-color: #fff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  transition: background-color 0.3s;
  cursor: pointer;
}

.curso-ok {
  background-color: #e0f8e0;
}

.curso-error {
  background-color: #fbe4e6;
}

/* Popup */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 350px;
  max-width: 90%;
  text-align: left;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-cerrar {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  margin-top: 10px;
  cursor: pointer;
}

.btn-cerrar:hover {
  background-color: #b02a37;
}
</style>
