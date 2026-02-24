<template>
  <div class="persona-modals">
    <!-- Modal: RUT Search (Premium Design) -->
    <Teleport to="body">
        <div v-if="rutModalVisible" class="modal-overlay-glass" @mousedown.self="rutModalVisible = false">
          <div class="modal-content-premium rut-modal-box" role="dialog" aria-modal="true">
            <div class="modal-header-premium">
              <div class="header-title">
                <AppIcons name="user" :size="24" />
                <h3>Ingresar RUT</h3>
              </div>
              <button type="button" class="modal-close-btn" @click="rutModalVisible = false">✕</button>
            </div>
            <div class="modal-body-premium">
              <p class="mb-4 text-slate-600">Ingresa el RUT de la persona para verificar si ya existe en el sistema antes de crear un nuevo registro.</p>
              <div class="rut-row">
                <InputBase 
                  v-model="rutSearch.run" 
                  placeholder="12345678" 
                  maxlength="8"
                  @update:modelValue="onRutSearchInput"
                  class="rut-input"
                />
                <span class="sep text-slate-400 font-bold">-</span>
                <InputBase 
                  v-model="rutSearch.dv" 
                  maxlength="1" 
                  @update:modelValue="onDvSearchInput"
                  class="rut-dv"
                />
              </div>
              <p v-if="rutError" class="error-msg-premium">
                <AppIcons name="alert-circle" :size="16" /> {{ rutError }}
              </p>
            </div>
            <div class="modal-footer-premium">
              <BaseButton variant="secondary" @click="rutModalVisible = false" class="btn-large">Cancelar</BaseButton>
              <BaseButton variant="primary" @click="$emit('rut-check', rutSearch)" :disabled="!rutSearch.run" class="btn-large">
                <AppIcons name="search" :size="20" style="margin-right: 8px;" />
                Verificar
              </BaseButton>
            </div>
          </div>
        </div>
    </Teleport>

    <!-- Modal: Importar Excel -->
    <BaseModal v-model="importModalVisible" title="Importar Personas desde Excel" class="modal-large">
      <div class="import-content">
        <div class="import-instructions glass-panel">
          <h3>Instrucciones</h3>
          <ul>
            <li>Descarga la plantilla oficial para asegurar el formato correcto.</li>
            <li>El RUT y Nombre son campos obligatorios.</li>
            <li>Si la persona ya existe, se actualizarán sus datos básicos.</li>
          </ul>
          <BaseButton variant="secondary" size="sm" @click="$emit('download-template')">
            <AppIcons name="download" :size="16" /> Descargar Plantilla
          </BaseButton>
        </div>

        <div class="file-upload-area">
          <input type="file" ref="excelInput" accept=".xlsx, .xls" @change="onFileChange" hidden />
          <div class="upload-zone" @click="$refs.excelInput.click()">
            <AppIcons name="upload" :size="48" />
            <p v-if="!selectedFile">Haz clic para seleccionar un archivo Excel</p>
            <p v-else class="file-selected">Archivo: {{ selectedFile.name }}</p>
          </div>
        </div>

        <div v-if="importPreview.length > 0" class="import-preview overflow-auto">
          <h4>Vista Previa ({{ importPreview.length }} filas)</h4>
          <table class="preview-table">
            <thead>
              <tr>
                <th v-for="col in previewCols" :key="col">{{ col }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in importPreview.slice(0, 5)" :key="idx">
                <td v-for="col in previewCols" :key="col">{{ row[col] }}</td>
              </tr>
            </tbody>
          </table>
          <p v-if="importPreview.length > 5" class="text-sm italic">...y {{ importPreview.length - 5 }} filas más.</p>
        </div>
        
        <div class="modal-actions mt-6">
          <BaseButton variant="secondary" @click="importModalVisible = false">Cerrar</BaseButton>
          <BaseButton variant="primary" @click="$emit('import-execute')" :disabled="!selectedFile || importing">
            <AppIcons :name="importing ? 'refresh' : 'check'" :size="18" :class="{ 'spin': importing }" />
            {{ importing ? 'Importando...' : 'Iniciar Importación' }}
          </BaseButton>
        </div>
      </div>
    </BaseModal>

    <!-- Modal: Exportar -->
    <BaseModal v-model="exportModalVisible" title="Exportar Datos" class="modal-medium">
      <div class="export-content">
        <p>Selecciona el formato de exportación para las personas filtradas actualmente.</p>
        <div class="export-options">
          <button class="export-card" @click="$emit('export-excel')">
            <AppIcons name="grid" :size="32" />
            <span>Excel (.xlsx)</span>
            <small>Formato completo con todos los campos</small>
          </button>
          <button class="export-card" @click="$emit('export-emails')">
            <AppIcons name="mail" :size="32" />
            <span>Lista de Emails</span>
            <small>Copia todos los correos al portapapeles</small>
          </button>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseButton from '@/components/BaseButton.vue'
import InputBase from '@/components/InputBase.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import { calcularDv } from '@/utils/formatters'

const props = defineProps({
  importing: Boolean,
  importPreview: { type: Array, default: () => [] }
})

const emit = defineEmits([
  'rut-check', 
  'download-template', 
  'file-selected', 
  'import-execute', 
  'export-excel', 
  'export-emails'
])

const rutModalVisible = defineModel('rutModalVisible')
const importModalVisible = defineModel('importModalVisible')
const exportModalVisible = defineModel('exportModalVisible')

const rutSearch = reactive({ run: '', dv: '' })
const rutError = ref('')
const selectedFile = ref(null)

const previewCols = ['RUT', 'DV', 'Nombres', 'Apellido Paterno', 'Email']

const onRutSearchInput = (val) => {
  if (val !== null && val !== undefined && val !== '') {
    const strVal = String(val)
    rutSearch.run = strVal.replace(/[^0-9]/g, '').slice(0, 8)
    if (rutSearch.run.length >= 7) {
      rutSearch.dv = calcularDv(rutSearch.run)
    } else {
      rutSearch.dv = ''
    }
  } else {
    rutSearch.run = ''
    rutSearch.dv = ''
  }
}

const onDvSearchInput = (val) => {
  if (val !== null && val !== undefined && val !== '') {
    const strVal = String(val)
    rutSearch.dv = strVal.replace(/[^0-9kK]/g, '').toUpperCase()
  } else {
    rutSearch.dv = ''
  }
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

watch(importModalVisible, (val) => {
  if (!val) {
    selectedFile.value = null
  }
})
</script>

<style scoped>
.rut-row { 
  display: flex; gap: 12px; align-items: center; margin-top: 16px; 
  background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;
}
.rut-input { flex: 1; }
.rut-dv { width: 60px; text-align: center; }
.error-msg-premium { 
  color: #ef4444; font-size: 0.85rem; margin-top: 12px; 
  display: flex; align-items: center; gap: 6px; font-weight: 500;
}

/* Modal Premium Styles */
.modal-overlay-glass {
  position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 20px;
}
.modal-content-premium {
  background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 24px;
  width: 100%; max-width: 500px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); overflow: hidden;
}
.modal-header-premium {
  padding: 24px; display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
.header-title { display: flex; align-items: center; gap: 12px; color: #1e293b; }
.header-title h3 { margin: 0; font-size: 1.25rem; font-weight: 700; }
.modal-close-btn {
  background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; cursor: pointer; color: #64748b; transition: all 0.2s;
}
.modal-close-btn:hover { background: #e2e8f0; color: #0f172a; transform: rotate(90deg); }
.modal-body-premium { padding: 32px 24px; }
.modal-footer-premium {
  padding: 20px 24px; background: rgba(248, 250, 252, 0.5);
  display: flex; justify-content: flex-end; gap: 12px; border-top: 1px solid #e2e8f0;
}
.btn-large { padding: 12px 24px !important; font-weight: 600 !important; border-radius: 12px !important; }



.import-content { display: flex; flex-direction: column; gap: 20px; }
.glass-panel { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; }
.import-instructions h3 { margin: 0 0 12px; font-size: 1rem; color: #1e293b; }
.import-instructions ul { padding-left: 20px; margin-bottom: 16px; color: #64748b; font-size: 0.9rem; }

.file-upload-area { border: 2px dashed #cbd5e1; border-radius: 12px; cursor: pointer; transition: 0.2s; }
.file-upload-area:hover { border-color: #1a237e; background: #eff6ff; }
.upload-zone { padding: 40px; display: flex; flex-direction: column; align-items: center; gap: 12px; color: #94a3b8; }
.file-selected { color: #10b981; font-weight: 600; }

.preview-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; margin-top: 12px; }
.preview-table th, .preview-table td { border: 1px solid #e2e8f0; padding: 8px; text-align: left; }
.preview-table th { background: #f1f5f9; }

.export-options { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }
.export-card { 
  display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 24px;
  background: white; border: 1px solid #e2e8f0; border-radius: 12px; cursor: pointer; transition: 0.2s;
}
.export-card:hover { border-color: #1a237e; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.export-card span { font-weight: 600; color: #1e293b; }
.export-card small { color: #94a3b8; font-size: 0.75rem; text-align: center; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.modal-actions { display: flex; justify-content: flex-end; gap: 12px; }
</style>
