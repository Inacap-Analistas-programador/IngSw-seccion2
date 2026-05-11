<template>
  <section class="glass-section">
    <div id="seccion-4" class="anchor-offset"></div>
    <div class="section-header-modern">
      <AppIcons name="clipboard" :size="24" />
      <h2>Información Adicional</h2>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="trabajoNinos">¿Ha trabajado o trabajado actualmente con Niños, Niñas, Adolescentes o Jóvenes (NNAJ)?</label>
        <FilterSelect 
          v-model="haTrabajadoConNinos" 
          :options="opcionesSiNoMin" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />
        
        <transition name="desplegar">
          <div v-if="haTrabajadoConNinos === 'si'" style="margin-top: 12px;">
            <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 8px;">Indique tiempo total (años y meses):</p>
            <div style="display: flex; gap: 10px; align-items: center;">
              <input v-model="añosTrabajoNinos" type="number" placeholder="Años" style="width: 80px;" min="0" />
              <span>Años</span>
              <input v-model="mesesTrabajoNinos" type="number" placeholder="Meses" style="width: 80px;" min="0" max="11" />
              <span>Meses</span>
            </div>
          </div>
        </transition>
      </div>

      <div class="campo">
        <label for="beneficiario">¿Es o fue beneficiario de la Asociación?</label>
        <FilterSelect 
          v-model="esBeneficiario" 
          :options="opcionesSiNoMin" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />

        <transition name="desplegar">
          <div v-if="esBeneficiario === 'si'" style="margin-top: 12px;">
            <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 8px;">Indique tiempo total como beneficiario:</p>
            <div style="display: flex; gap: 10px; align-items: center;">
              <input v-model="añosTiempoBeneficiario" type="number" placeholder="Años" style="width: 80px;" min="0" />
              <span>Años</span>
              <input v-model="mesesTiempoBeneficiario" type="number" placeholder="Meses" style="width: 80px;" min="0" max="11" />
              <span>Meses</span>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="profesion">Profesión u oficio:</label>
        <input id="profesion" v-model="profesion" type="text" placeholder="Ej: Ingeniero, Estudiante, etc." />
      </div>

      <div class="campo">
        <label for="miembroActivo">¿Es miembro activo?</label>
        <FilterSelect 
          v-model="esMiembroActivo" 
          :options="opcionesSiNoMin" 
          valueKey="value" 
          labelKey="label" 
          defaultLabel="Seleccione una opción" 
        />
      </div>
    </div>

    <div class="section-grid">
      <div class="campo">
        <label for="consideraciones">Observaciones o consideraciones adicionales (Opcional):</label>
        <textarea
          id="consideraciones"
          v-model="consideraciones"
          placeholder="Cualquier información que consideres relevante..."
          rows="4"
        ></textarea>
      </div>

      <div class="campo">
        <label for="alojamiento">¿Necesita alojamiento?</label>
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-top: 10px;">
          <input id="alojamiento" type="checkbox" class="custom-checkbox" v-model="necesitaAlojamiento" true-value="si" false-value="no" />
          <span>Indique si requiere alojamiento durante el curso</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import AppIcons from '@/components/icons/AppIcons.vue';
import FilterSelect from '@/components/common/FilterSelect.vue';

const opcionesSiNoMin = [
  { value: 'si', label: 'Sí' },
  { value: 'no', label: 'No' }
];

// Models
const haTrabajadoConNinos = defineModel('haTrabajadoConNinos');
const añosTrabajoNinos = defineModel('añosTrabajoNinos');
const mesesTrabajoNinos = defineModel('mesesTrabajoNinos');
const esBeneficiario = defineModel('esBeneficiario');
const añosTiempoBeneficiario = defineModel('añosTiempoBeneficiario');
const mesesTiempoBeneficiario = defineModel('mesesTiempoBeneficiario');
const esMiembroActivo = defineModel('esMiembroActivo');
const necesitaAlojamiento = defineModel('necesitaAlojamiento');
const consideraciones = defineModel('consideraciones');
const profesion = defineModel('profesion');
</script>

<style scoped>
</style>
