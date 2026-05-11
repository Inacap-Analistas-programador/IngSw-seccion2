<template>
  <section class="table-section">
    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead>
            <tr>
              <th class="text-left">DESCRIPCIÓN</th>
              <th>CÓDIGO</th>
              <th class="text-left">TIPO</th>
              <th>FECHAS</th>
              <th class="text-left">RESPONSABLE</th>
              <th class="text-center">ESTADO</th>
              <th class="text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in cursos" :key="c.CUR_ID">
              <td data-label="DESCRIPCIÓN" class="text-left">
                <span class="truncate" :title="c.CUR_DESCRIPCION">{{ c.CUR_DESCRIPCION || '-' }}</span>
              </td>
              <td data-label="CÓDIGO">{{ c.CUR_CODIGO || '-' }}</td>
              <td data-label="TIPO" class="text-left">{{ getTipoCursoName(c.TCU_ID) }}</td>
              <td data-label="FECHAS">{{ formatDates(c) }}</td>
              <td data-label="RESPONSABLE" class="text-left">
                <div>{{ getPersonaName(c.PER_ID_RESPONSABLE) }}</div>
                <div v-if="c.CAR_ID_RESPONSABLE" class="responsable-cargo">{{ getCargoName(c.CAR_ID_RESPONSABLE) }}</div>
              </td>
              <td class="text-center" data-label="ESTADO">
                <span :class="['status-badge', getEstadoClass(c.CUR_ESTADO)]">
                  {{ getEstadoText(c.CUR_ESTADO) }}
                </span>
              </td>
              <td class="text-center" data-label="ACCIONES">
                <div class="acciones-buttons">
              <button class="action-btn btn-view" title="Ver" @click="$emit('ver', c)">
                <AppIcons name="eye" :size="16" />
              </button>
              <button class="action-btn btn-edit" title="Editar" @click="$emit('editar', c)">
                <AppIcons name="edit" :size="16" />
              </button>
              <button 
                class="action-btn" 
                :class="c.CUR_ESTADO == 1 ? 'btn-delete' : 'btn-activate'"
                :title="c.CUR_ESTADO == 1 ? 'Anular' : 'Activar (Vigente)'" 
                @click="$emit('cambioEstado', c)"
              >
                <AppIcons :name="c.CUR_ESTADO == 1 ? 'trash' : 'check'" :size="16" />
              </button>
              <button class="action-btn btn-dashboard" title="Dashboard" @click="$emit('dashboard', c)">
                <AppIcons name="bar-chart" :size="16" />
              </button>
            </div>
              </td>
            </tr>
            <tr v-if="!hasAnyFilter && cursos.length === 0">
              <td colspan="7" class="no-data-search">
                <div class="empty-state-content">
                  <AppIcons name="info" :size="32" class="empty-state-icon" />
                  <span class="empty-state-text">Ingrese al menos un filtro para buscar cursos.</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="cursos.length === 0">
              <td colspan="7" class="no-data">No se encontraron cursos que coincidan con los filtros.</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>
  </section>
</template>

<script setup>
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

defineProps({
  cursos: Array,
  hasAnyFilter: Boolean,
  getTipoCursoName: Function,
  formatDates: Function,
  getPersonaName: Function,
  getCargoName: Function,
  getEstadoClass: Function,
  getEstadoText: Function
})

defineEmits(['ver', 'editar', 'cambioEstado', 'dashboard'])
</script>

<style scoped>
.table-section { width: 100%; display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.table-container { flex: 1; overflow: hidden; border-radius: 8px; }

.data-table { width: 100%; min-width: 800px; border-collapse: collapse; }
.data-table th, .data-table td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #f0f0f0; }
.data-table th { background-color: #f8f9fa; color: #333; font-weight: 600; position: sticky; top: 0; z-index: 10; font-size: 0.85rem; text-transform: uppercase; }

.text-left {
  text-align: left !important;
}

.responsable-cargo {
  font-size: 0.85em; 
  color: #666;
}

.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; }
.status-active { background-color: #e8f5e9; color: #2e7d32; }
.badge-warning { background-color: #fef3c7; color: #92400e; }
.status-inactive { background-color: #ffebee; color: #c62828; }
.status-info { background-color: #e0f2fe; color: #0369a1; }

.acciones-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: background 0.2s;
  color: #555;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background-color: #f0f0f0;
}

.btn-view:hover { color: #1976d2; background-color: #e3f2fd; }
.btn-edit:hover { color: #f57c00; background-color: #fff3e0; }
.btn-delete:hover { color: #d32f2f; background-color: #ffebee; }
.btn-activate:hover { color: #388e3c; background-color: #e8f5e9; }
.btn-dashboard:hover { color: #6a1b9a; background-color: #f3e5f5; }

.no-data-search, .no-data {
  padding: 40px;
  color: #64748b;
  font-style: italic;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state-icon {
  color: #94a3b8;
}

@media (max-width: 768px) {
  .table-section {
    flex: none !important;
    overflow: visible !important;
    display: block;
    width: 100%;
  }
  .table-container { 
    height: auto !important;
    overflow: visible !important;
    border: none;
    background: transparent;
  }
  
  /* Transformation into cards */
  .data-table { 
    display: block !important;
    width: 100% !important;
    min-width: 0 !important; 
    background: transparent;
  }
  .data-table thead { display: none !important; }
  .data-table tbody { display: block !important; width: 100% !important; }
  
  .data-table tr { 
    display: block !important;
    width: 100% !important;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-bottom: 20px;
    padding: 12px 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .data-table td { 
    display: flex !important;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid #f1f5f9;
    text-align: right;
  }
  
  .data-table td:last-child { border-bottom: none; }
  
  .data-table td::before { 
    content: attr(data-label); 
    font-weight: 700; 
    color: #64748b; 
    text-transform: uppercase; 
    font-size: 0.75rem; 
    text-align: left; 
    flex: 0 0 130px; 
    margin-right: 8px;
  }

  .acciones-buttons {
    justify-content: flex-end;
  }
}
</style>
