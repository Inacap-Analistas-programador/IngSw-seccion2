<template>
  <section class="glass-section">
    <div class="section-header-modern">
      <AppIcons name="map" :size="24" />
      <h2>Selección de Curso</h2>
    </div>

    <div class="curso-root-container">
      <div class="curso-inputs-column">
        <div class="campo">
          <FilterSelect 
            v-model="cursoSeleccionado"
            :options="cursosParaSelect"
            default-label="¿En qué curso participará?"
            @update:model-value="handleCursoChange"
          />
        </div>

        <!-- Seccion selector removed because it is now auto-selected -->
      </div>

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
          <AppIcons name="download" :size="20" style="margin-right: 8px;" />
          Descargar Ficha
        </BaseButton>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { cursos as cursosApi, secciones as seccionesApi } from '@/services/cursosService';
import BaseButton from '@/components/BaseButton.vue';
import AppIcons from '@/components/icons/AppIcons.vue';
import FilterSelect from '@/components/common/FilterSelect.vue';

const cursoSeleccionado = defineModel('cursoSeleccionado');
const seccionCurso = defineModel('seccionCurso');

const listaCursosApi = ref([]);
const listaSeccionesApi = ref([]);

const cursosParaSelect = computed(() => {
  return listaCursosApi.value.map(curso => ({
    id: curso.cur_id,
    descripcion: curso.cur_descripcion
  }));
});

const emit = defineEmits(['seccion-change']);

const handleCursoChange = async (val) => {
  // El valor ya viene actualizado por defineModel/v-model, 
  // pero lo recibimos aquí para disparar la carga de secciones
  seccionCurso.value = "";
  listaSeccionesApi.value = [];

  if (!val) {
    return;
  }

  try {
    const respuestaSecciones = await seccionesApi.list({ cur_id: cursoSeleccionado.value });
    const secciones = respuestaSecciones.results || respuestaSecciones || [];
    listaSeccionesApi.value = secciones;

    // Pre-seleccionar la primera sección por defecto
    if (secciones.length > 0) {
      seccionCurso.value = secciones[0].cus_id;
      emitSeccionChange();
    }
  } catch (error) {
    console.error('Error al obtener las secciones del curso:', error);
    listaSeccionesApi.value = [];
  }
};

const emitSeccionChange = () => {
  emit('seccion-change', seccionCurso.value);
};

const descargarFicha = () => {
  // Usamos una ruta absoluta desde la raíz para evitar problemas en sub-rutas de hosting
  const fileName = 'Ficha Medica.docx';
  const fileUrl = `${window.location.origin}/${fileName}`;
  
  const link = document.createElement('a');
  link.href = fileUrl;
  link.download = fileName;
  link.target = '_blank'; // Abrir en nueva pestaña si el navegador no fuerza la descarga
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

onMounted(async () => {
  try {
    // Solo traer cursos Vigentes (cur_estado = 1)
    const respuesta = await cursosApi.list({ cur_estado: 1, page_size: 2000 });
    const todosLosCursos = respuesta.results || respuesta || [];
    
    // Filtrar solo los que tengan al menos una sección
    listaCursosApi.value = todosLosCursos
      .filter(curso => curso.secciones && curso.secciones.length > 0)
      .map(curso => ({ ...curso }))
      .sort((a, b) => a.cur_id - b.cur_id);
  } catch (error) {
    console.error('Error al obtener cursos:', error);
  }
});
</script>

<style scoped>
.curso-root-container {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.curso-inputs-column {
  flex: 1 1 250px; /* Reduced min-width to prevent overflow on very small screens */
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.boton-descarga-container {
  flex: 1 1 300px; /* Allow it to grow and shrink, better balance on desktop */
  max-width: 400px; /* Prevent it from getting too wide on large screens */
  background: rgba(255, 255, 255, 0.5);
  border: 1px dashed var(--color-primary);
  border-radius: 15px;
  padding: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 15px;
}

.logo-descarga {
  width: 50px;
  height: 50px;
}

.label-descarga {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label-principal {
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.label-secundario {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

@media (max-width: 768px) {
  .boton-descarga-container {
    flex: 1 1 100%;
  }
}
</style>
