  <template>
  <section class="glass-section">
    <div id="seccion-2" class="anchor-offset"></div>
    <div class="section-header-modern">
      <AppIcons name="map" :size="24" />
      <h2>Información Asociación</h2>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="zona">Zona al que pertenece:</label>
        <FilterSelect 
          v-model="zonaSeleccionada" 
          :options="listaZonaApi" 
          valueKey="zon_id" 
          labelKey="zon_descripcion" 
          defaultLabel="Seleccione su zona" 
        />

        <div v-if="zonaSeleccionada === 'otro'" class="campo-adicional" style="margin-top: 12px;">
          <label for="otraZona">Ingrese el nombre de la zona:</label>
          <textarea
            id="otraZona"
            v-model="otraZona"
            placeholder="Escriba el nombre de la zona..."
            rows="2"
            maxlength="100"
          ></textarea>
        </div>
      </div>

      <div class="campo">
        <label for="distrito">Distrito:</label>
        <FilterSelect 
          v-model="distritoSeleccionado" 
          :disabled="!zonaSeleccionada" 
          :options="listaDistritoApi" 
          valueKey="dis_id" 
          labelKey="dis_descripcion" 
          defaultLabel="Seleccione su distrito" 
        />
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="grupoPertenece">Grupo al que pertenece:</label>
        <FilterSelect 
          v-model="grupoPertenece" 
          :disabled="!distritoSeleccionado" 
          :options="listaGrupoApi" 
          valueKey="gru_id" 
          labelKey="gru_descripcion" 
          defaultLabel="Seleccione su grupo" 
        />

        <transition name="desplegar">
          <div v-if="grupoPertenece === 'individual'" class="campo-adicional" style="margin-top: 12px;">
            <label for="cargo">Cargo en la Asociación:</label>
            <FilterSelect 
              v-model="cargoSeleccionado" 
              :options="listaCargoApi" 
              valueKey="car_id" 
              labelKey="car_descripcion" 
              defaultLabel="Seleccione su cargo" 
            />
          </div>
        </transition>
      </div>

      <div class="campo">
        <label for="rol">Rol en el curso:</label>
        <FilterSelect 
          v-model="rolSeleccionado" 
          :options="listaRolApi" 
          valueKey="rol_id" 
          labelKey="rol_descripcion" 
          defaultLabel="Seleccione su rol" 
        />

        <transition name="desplegar">
          <div v-if="rolSeleccionado === 'otro'" class="campo-adicional" style="margin-top: 12px;">
            <label for="rolOtro">Especifique su rol:</label>
            <textarea
              id="rolOtro"
              v-model="rolOtro"
              placeholder="Ingrese su rol aquí..."
              rows="2"
              maxlength="100"
            ></textarea>
          </div>
        </transition>
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="nivelFormacion">Nivel de formación:</label>
        <FilterSelect 
          v-model="nivelFormacion" 
          :options="listaNivelApi" 
          valueKey="niv_id" 
          labelKey="niv_descripcion" 
          defaultLabel="Seleccione su nivel" 
        />
      </div>
    </div>

    <transition name="desplegar">
      <div v-if="ordenActual > 1" class="niveles-container">
        <div class="niveles-grid">
          <div class="nivel-column" v-if="ordenActual >= 2">
            <h4 class="nivel-title">NIVEL MEDIO</h4>
            <div class="checkbox-list">
              <div v-for="rama in ramasMedio" :key="rama.value" class="checkbox-item">
                <input 
                  :id="'medio-' + rama.value" 
                  type="checkbox" 
                  class="custom-checkbox" 
                  :value="rama.value"
                  v-model="ramasMedioSeleccionadas"
                />
                <label :for="'medio-' + rama.value">{{ rama.label }}</label>
              </div>
            </div>
          </div>

          <div class="nivel-column" v-if="ordenActual >= 3">
            <h4 class="nivel-title">NIVEL AVANZADO</h4>
            <div class="checkbox-list">
              <div v-for="rama in ramasAvanzado" :key="rama.value" class="checkbox-item">
                <input 
                  :id="'avanzado-' + rama.value" 
                  type="checkbox" 
                  class="custom-checkbox" 
                  :value="rama.value"
                  v-model="ramasAvanzadoSeleccionadas"
                />
                <label :for="'avanzado-' + rama.value">{{ rama.label }}</label>
              </div>
            </div>
          </div>
        </div>

        <div v-if="ordenActual >= 2" class="mmaa-input-container">
          <label for="mmaaInput" class="mmaa-label">MMAA:</label>
          <input 
            id="mmaaInput" 
            v-model="mmaaValor" 
            type="text" 
            placeholder="Ingrese MMAA"
            maxlength="12"
            class="mmaa-input"
          />
        </div>
      </div>
    </transition>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { 
  zona as zonaApi, 
  distrito as distritoApi, 
  grupo as grupoApi, 
  rol as rolApi, 
  nivel as nivelApi,
  cargo as cargoApi 
} from '@/services/mantenedoresService';
import AppIcons from '@/components/icons/AppIcons.vue';
import FilterSelect from '@/components/common/FilterSelect.vue';

// Models
const zonaSeleccionada = defineModel('zonaSeleccionada');
const otraZona = defineModel('otraZona');
const distritoSeleccionado = defineModel('distritoSeleccionado');
const grupoPertenece = defineModel('grupoPertenece');
const cargoSeleccionado = defineModel('cargoSeleccionado');
const rolSeleccionado = defineModel('rolSeleccionado');
const rolOtro = defineModel('rolOtro');
const nivelFormacion = defineModel('nivelFormacion');
const ramasMedioSeleccionadas = defineModel('ramasMedioSeleccionadas');
const ramasAvanzadoSeleccionadas = defineModel('ramasAvanzadoSeleccionadas');
const mmaaValor = defineModel('mmaaValor');

// Local Data
const listaZonaApi = ref([]);
const listaDistritoApi = ref([]);
const listaGrupoApi = ref([]);
const listaCargoApi = ref([]);
const listaRolApi = ref([]);
const listaNivelApi = ref([]);
const listaRamas = ref([]);

// Computed Ramas e Information de Nivel
const nivelSeleccionado = computed(() => {
  return listaNivelApi.value.find(n => n.niv_id === nivelFormacion.value);
});

const ordenActual = computed(() => nivelSeleccionado.value?.niv_orden || 0);

const ramasMedio = computed(() => listaRamas.value.map(rama => ({ value: rama.ram_id, label: rama.ram_descripcion })));
const ramasAvanzado = computed(() => listaRamas.value.map(rama => ({ value: rama.ram_id, label: rama.ram_descripcion })));

// Watchers
watch(zonaSeleccionada, async (newVal) => {
  distritoSeleccionado.value = "";
  grupoPertenece.value = "";
  listaDistritoApi.value = [];
  listaGrupoApi.value = [];
  if (newVal === 'otro') otraZona.value = '';
  if (newVal && newVal !== 'otro') {
    try {
      const resp = await distritoApi.list({ zon_id: newVal, vigente: true });
      listaDistritoApi.value = resp.results || resp || [];
    } catch (e) { console.error(e); }
  }
});

watch(distritoSeleccionado, async (newVal) => {
  grupoPertenece.value = "";
  listaGrupoApi.value = [];
  if (newVal) {
    try {
      const resp = await grupoApi.list({ dis_id: newVal, vigente: true });
      const gruposDelDistrito = resp.results || resp || [];
      listaGrupoApi.value = [
        { gru_id: 'individual', gru_descripcion: 'Persona Individual' },
        ...gruposDelDistrito
      ];
    } catch (e) { console.error(e); }
  }
});

watch(ordenActual, (newVal) => {
  if (newVal < 3) {
    ramasAvanzadoSeleccionadas.value = [];
  }
  if (newVal < 2) {
    ramasMedioSeleccionadas.value = [];
    mmaaValor.value = '';
  }
});

onMounted(async () => {
    try {
        const [respZonas, respRoles, respNiveles, respRamas, respCargos] = await Promise.all([
            zonaApi.list({ page_size: 100, vigente: true }),
            rolApi.list({ vigente: true }),
            nivelApi.list({ vigente: true }),
            import('@/services/ramasService').then(m => m.ramas.list({ page_size: 200, vigente: true })),
            cargoApi.list({ page_size: 100, vigente: true })
        ]);
        
        const zonas = respZonas.results || respZonas || [];
        listaZonaApi.value = [...zonas, { zon_id: 'otro', zon_descripcion: 'Otro' }];
        
        const roles = respRoles.results || respRoles || [];
        listaRolApi.value = [...roles, { rol_id: 'otro', rol_descripcion: 'Otro' }];
        
        listaNivelApi.value = respNiveles.results || respNiveles || [];
        listaRamas.value = respRamas.results || respRamas || [];
        listaCargoApi.value = respCargos.results || respCargos || [];
    } catch (e) {
        console.error("Error loading association data", e);
    }
});
</script>

<style scoped>
.niveles-container {
  margin-top: 30px;
}

.nivel-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: #1e40af;
  text-align: center;
  padding: 12px;
  background: rgba(30, 64, 175, 0.05);
  border-bottom: 2px solid rgba(30, 64, 175, 0.1);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.niveles-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
  margin-bottom: 25px;
}

.nivel-column {
  flex: 1;
  min-width: 280px;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(30, 64, 175, 0.15);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.nivel-column:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.1);
  border-color: rgba(30, 64, 175, 0.3);
}

.checkbox-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background 0.2s;
}

.checkbox-item:hover {
  background: #f8fafc;
}

.mmaa-input-container {
  margin-top: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.mmaa-input {
  width: 140px;
  text-align: center;
}
</style>
