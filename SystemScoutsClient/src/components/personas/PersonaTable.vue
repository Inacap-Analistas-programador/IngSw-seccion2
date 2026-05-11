<template>
  <div class="table-section">
    <div class="table-container">
      <ModernMainScrollbar>
        <table class="data-table">
          <thead>
            <tr>
              <th class="text-left">Nombre</th>
              <th>RUT</th>
              <th>Email</th>
              <th class="text-left">Rol</th>
              <th>Teléfono</th>
              <th class="text-center">Estado</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in personas" :key="p.PER_ID">
              <td data-label="Nombre" class="text-left" :title="fullName(p)">
                <div class="nombre-container">
                  <div class="avatar-circle">
                    <img v-if="p.PER_FOTO" :src="getFotoUrl(p.PER_FOTO)" class="avatar-img" />
                    <div v-else class="avatar-placeholder">
                      {{ (p.PER_NOMBRES || '?')[0] }}
                    </div>
                  </div>
                  <span class="nombre-text truncate">{{ fullName(p) }}</span>
                </div>
              </td>
              <td data-label="RUT" class="rut-text">
                {{ p.PER_RUN }}-{{ p.PER_DV }}
              </td>
              <td data-label="Email" :title="p.PER_MAIL || 'Sin email'">
                <span class="truncate">{{ p.PER_MAIL || '---' }}</span>
              </td>
              <td data-label="Rol" class="text-left">
                <span class="role-badge">{{ p.PER_ROL || 'Sin rol' }}</span>
              </td>
              <td data-label="Teléfono">
                {{ p.PER_CEL || p.PER_FONO || '---' }}
              </td>
              <td data-label="Estado" class="text-center">
                <span :class="['status-badge', p.PER_VIGENTE ? 'status-active' : 'status-inactive']">
                  {{ p.PER_VIGENTE ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="text-center" data-label="Acciones">
                <div class="acciones-buttons">
                  <button class="action-btn btn-view" @click="$emit('view', p)" title="Ver Detalle">
                    <AppIcons name="eye" :size="16" />
                  </button>
                  <button v-if="canEdit" class="action-btn btn-edit" @click="$emit('edit', p)" title="Editar">
                    <AppIcons name="edit" :size="16" />
                  </button>
                  <button 
                    v-if="canDelete && p.PER_VIGENTE" 
                    class="action-btn btn-delete" 
                    @click="$emit('deactivate', p)" 
                    title="Anular"
                  >
                    <AppIcons name="trash" :size="16" />
                  </button>
                  <button 
                    v-if="canDelete && !p.PER_VIGENTE" 
                    class="action-btn btn-activate" 
                    @click="$emit('reactivate', p)" 
                    title="Reactivar"
                  >
                    <AppIcons name="check" :size="16" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!hasSearched && personas.length === 0">
              <td colspan="7" class="no-data-search">
                <div class="empty-state-content">
                  <AppIcons name="info" :size="32" class="empty-state-icon" />
                  <span class="empty-state-text">Ingrese al menos un filtro para buscar personas.</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="personas.length === 0">
              <td colspan="7" class="no-data">No se encontraron personas que coincidan con los filtros.</td>
            </tr>
          </tbody>
        </table>
      </ModernMainScrollbar>
    </div>
  </div>
</template>

<script setup>
import AppIcons from '@/components/icons/AppIcons.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'

const props = defineProps({
  personas: {
    type: Array,
    required: true,
    default: () => []
  },
  canEdit: Boolean,
  canDelete: Boolean,
  hasSearched: {
    type: Boolean,
    default: false
  }
})

defineEmits(['view', 'edit', 'deactivate', 'reactivate'])

const fullName = (p) => {
  return `${p.PER_NOMBRES || ''} ${p.PER_APELPTA || ''} ${p.PER_APELMAT || ''}`.trim()
}

const API_ROOT = (import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/?api\/?$/, '')

const getFotoUrl = (fotoPath) => {
  if (!fotoPath) return null
  if (fotoPath.startsWith('http') || fotoPath.startsWith('data:')) return fotoPath
  return `${API_ROOT}${fotoPath.startsWith('/') ? '' : '/'}${fotoPath}`
}
</script>

<style scoped>
.table-section { width: 100%; display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.table-container { flex: 1; overflow: hidden; border-radius: 8px; }

.data-table { width: 100%; min-width: 800px; border-collapse: collapse; }
.data-table th, .data-table td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #f0f0f0; }
.data-table th { background-color: #f8f9fa; color: #333; font-weight: 600; position: sticky; top: 0; z-index: 10; font-size: 0.85rem; text-transform: uppercase; }

.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

.truncate {
  max-width: 180px;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.nombre-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-circle { flex-shrink: 0; }
.avatar-img { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }
.avatar-placeholder {
  width: 32px; height: 32px; border-radius: 50%;
  background-color: #e0e7ff; color: #4f46e5;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.75rem;
}

.nombre-text { font-weight: 500; }

.role-badge {
  background: #eff6ff;
  color: #1d4ed8;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; }
.status-active { background-color: #e8f5e9; color: #2e7d32; }
.status-inactive { background-color: #ffebee; color: #c62828; }

.acciones-buttons { display: flex; gap: 8px; justify-content: center; }

.action-btn {
  background: none; border: none; cursor: pointer; padding: 6px; border-radius: 4px;
  transition: background 0.2s, color 0.2s; color: #555;
  display: flex; align-items: center; justify-content: center;
}

.action-btn:hover { background-color: #f0f0f0; }
.btn-view:hover { color: #1976d2; background-color: #e3f2fd; }
.btn-edit:hover { color: #f57c00; background-color: #fff3e0; }
.btn-delete:hover { color: #d32f2f; background-color: #ffebee; }
.btn-activate:hover { color: #388e3c; background-color: #e8f5e9; }

.no-data-search, .no-data {
  text-align: center;
  padding: 40px !important;
  color: #64748b;
  font-style: italic;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state-icon { color: #94a3b8; }

@media (max-width: 1024px) {
  .table-section { flex: none; overflow: visible; display: block; width: 100%; }
  .table-container { height: auto; overflow: visible; border: none; background: transparent; }
  
  .data-table { display: block; width: 100%; min-width: 0; background: transparent; }
  .data-table thead { display: none; }
  .data-table tbody { display: block; width: 100%; }
  
  .data-table tr { 
    display: block; width: 100%; background: white;
    border: 1px solid #e2e8f0; border-radius: 12px;
    margin-bottom: 20px; padding: 12px 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .data-table td { 
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 16px; border-bottom: 1px solid #f1f5f9; text-align: right;
  }
  
  .data-table td:last-child { border-bottom: none; }
  
  .data-table td::before { 
    content: attr(data-label); font-weight: 700; color: #64748b; 
    text-transform: uppercase; font-size: 0.75rem; text-align: left; 
    flex: 0 0 130px; margin-right: 8px;
  }

  .acciones-buttons { justify-content: flex-end; }
  .truncate { max-width: none; }
}
</style>
