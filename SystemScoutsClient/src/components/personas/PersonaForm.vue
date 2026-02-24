<template>
  <div class="persona-form">
    <header class="form-header">
      <div class="header-content">
        <h2>{{ isReadOnly ? 'Ver Persona' : (isEdit ? 'Editar Persona' : 'Nueva Persona') }}</h2>
        <p class="subtitle" v-if="formData.PER_NOMBRES">
          {{ formData.PER_NOMBRES }} {{ formData.PER_APELPTA }}
        </p>
      </div>
      <div class="header-actions">
        <BaseButton variant="secondary" @click="$emit('cancel')" :disabled="loading">
          <AppIcons name="x" :size="18" />
          {{ isReadOnly ? 'Cerrar' : 'Cancelar' }}
        </BaseButton>
        <BaseButton v-if="!isReadOnly" variant="primary" @click="handleSave" :disabled="loading">
          <AppIcons :name="loading ? 'refresh' : 'save'" :size="18" :class="{ 'spin': loading }" />
          {{ loading ? 'Guardando...' : 'Guardar' }}
        </BaseButton>
      </div>
    </header>

    <div class="form-tabs" v-if="isEdit || isReadOnly">
      <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">Información</button>
      <button :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'">Historial de Cursos</button>
    </div>

    <div class="form-scroll-area">
      <!-- TAB: INFO -->
      <div v-show="activeTab === 'info'" class="tab-content">
        <!-- Foto de Perfil -->
        <div class="photo-section glass-panel">
          <div class="photo-container">
            <div class="photo-preview">
              <img v-if="formData.PER_FOTO || fotoUrlDisplay" :src="fotoUrlDisplay || formData.PER_FOTO" class="avatar-large" />
              <div v-else class="avatar-placeholder">
                <AppIcons name="person" :size="64" />
                <span>Sin foto</span>
              </div>
            </div>
            <div v-if="!isReadOnly" class="photo-controls">
              <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" hidden />
              <BaseButton variant="primary" size="sm" @click="$refs.fileInput.click()">
                <AppIcons name="camera" :size="16" />
                {{ formData.PER_FOTO ? 'Cambiar' : 'Subir' }}
              </BaseButton>
              <BaseButton v-if="formData.PER_FOTO" variant="danger" size="sm" @click="removePhoto">
                <AppIcons name="trash" :size="16" />
              </BaseButton>
            </div>
          </div>
          <div class="photo-info">
            <p>Sube una foto de perfil clara (PNG/JPG, máx 5MB).</p>
          </div>
        </div>

        <div class="form-grid">
          <!-- Datos Personales -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="person" :size="18" /> Datos Personales</h3>
            <div class="fields-row">
              <div class="field">
                <label>Nombres *</label>
                <InputBase v-model="formData.PER_NOMBRES" :readonly="isReadOnly" required />
              </div>
              <div class="field">
                <label>Apellido Paterno *</label>
                <InputBase v-model="formData.PER_APELPTA" :readonly="isReadOnly" required />
              </div>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Apellido Materno</label>
                <InputBase v-model="formData.PER_APELMAT" :readonly="isReadOnly" />
              </div>
              <div class="field">
                <label>RUT *</label>
                <div class="rut-group">
                  <InputBase v-model="formData.PER_RUN" :readonly="isReadOnly" @input="onRutInput" required class="rut-main" />
                  <span class="sep">-</span>
                  <InputBase v-model="formData.PER_DV" :readonly="isReadOnly" maxlength="1" required class="rut-dv" />
                </div>
              </div>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Fecha Nacimiento *</label>
                <InputBase type="date" v-model="formData.PER_FECHA_NAC" :readonly="isReadOnly" required @input="limitDate" />
              </div>
              <div class="field">
                <label>Estado Civil *</label>
                <FilterSelect 
                  v-model="formData.ESC_ID" 
                  :options="options.estadoCivil" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                />
              </div>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Apodo</label>
                <InputBase v-model="formData.PER_APODO" :readonly="isReadOnly" />
              </div>
              <div class="field">
                <label>Religión</label>
                <InputBase v-model="formData.PER_RELIGION" :readonly="isReadOnly" />
              </div>
            </div>
          </section>

          <!-- Contacto y Ubicación -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="mail" :size="18" /> Contacto y Ubicación</h3>
            <div class="fields-row">
              <div class="field">
                <label>Email *</label>
                <InputBase type="email" v-model="formData.PER_MAIL" :readonly="isReadOnly" required />
              </div>
              <div class="field">
                <label>Celular/Fono *</label>
                <div class="phone-group">
                  <span class="prefix">+56</span>
                  <InputBase v-model="formData.PER_FONO" :readonly="isReadOnly" placeholder="912345678" />
                </div>
              </div>
            </div>
            <div class="field">
              <label>Dirección *</label>
              <InputBase v-model="formData.PER_DIRECCION" :readonly="isReadOnly" required />
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Región</label>
                <FilterSelect 
                  v-model="formData.REG_ID" 
                  :options="options.regiones" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                  @update:modelValue="onRegionChange"
                />
              </div>
              <div class="field">
                <label>Provincia</label>
                <FilterSelect 
                  v-model="formData.PRO_ID" 
                  :options="options.provincias" 
                  :disabled="isReadOnly || !formData.REG_ID"
                  value-key="value"
                  label-key="label"
                  @update:modelValue="onProvinciaChange"
                />
              </div>
            </div>
            <div class="field">
              <label>Comuna *</label>
              <FilterSelect 
                v-model="formData.COM_ID" 
                :options="options.comunas" 
                :disabled="isReadOnly || !formData.PRO_ID"
                value-key="value"
                label-key="label"
              />
            </div>
          </section>

          <!-- Organización -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="users" :size="18" /> Organización</h3>
            <div class="fields-row">
              <div class="field">
                <label>Rol Principal</label>
                <FilterSelect 
                  v-model="formData.PER_ROL" 
                  :options="options.roles" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                />
              </div>
              <div class="field">
                <label>Grupo Scout</label>
                <FilterSelect 
                  v-model="formData.GRU_ID" 
                  :options="options.grupos" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                />
              </div>
            </div>
            
            <!-- Niveles y Ramas Dinámicos -->
            <div class="dynamic-sub-section">
              <div class="sub-header">
                <h4>Niveles y Ramas</h4>
                <BaseButton v-if="!isReadOnly" variant="secondary" size="sm" @click="addRama">
                  <AppIcons name="plus" :size="14" /> Agregar
                </BaseButton>
              </div>
              <div v-for="(item, idx) in formData.ramas" :key="idx" class="dynamic-row">
                <div class="row-fields">
                  <FilterSelect 
                    v-model="item.NIV_ID" 
                    :options="options.niveles" 
                    :disabled="isReadOnly"
                    default-label="Nivel"
                    value-key="value"
                    label-key="label"
                  />
                  <FilterSelect 
                    v-model="item.RAM_ID_NIVEL" 
                    :options="options.ramas" 
                    :disabled="isReadOnly"
                    default-label="Rama"
                    value-key="value"
                    label-key="label"
                  />
                </div>
                <button v-if="!isReadOnly && formData.ramas.length > 1" class="btn-remove" @click="removeRama(idx)">
                  <AppIcons name="trash" :size="16" />
                </button>
              </div>
            </div>

            <div class="fields-row mt-4">
              <div class="field">
                <label>Número MMA</label>
                <InputBase type="number" v-model="formData.PER_NUM_MMA" :readonly="isReadOnly" />
              </div>
              <div class="field">
                <label>Profesión</label>
                <InputBase v-model="formData.PER_PROFESION" :readonly="isReadOnly" />
              </div>
            </div>
          </section>

          <!-- Salud y Vehículo -->
          <section class="form-section glass-panel">
            <h3 class="section-title"><AppIcons name="heart" :size="18" /> Salud y Logística</h3>
            <div class="fields-row">
              <div class="field">
                <label>Tipo Alimentación</label>
                <FilterSelect 
                  v-model="formData.ALI_ID" 
                  :options="options.alimentacion" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                />
              </div>
              <div class="field">
                <label>Vigente</label>
                <FilterSelect 
                  v-model="formData.PER_VIGENTE" 
                  :options="[{value: true, label: 'Activo'}, {value: false, label: 'Inactivo'}]" 
                  :disabled="isReadOnly"
                  value-key="value"
                  label-key="label"
                />
              </div>
            </div>
            <div class="field">
              <label>Alergias / Enfermedades</label>
              <InputBase v-model="formData.PER_ALERGIA_ENFERMEDAD" :readonly="isReadOnly" />
            </div>
            <div class="field">
              <label>Limitaciones</label>
              <InputBase v-model="formData.PER_LIMITACION" :readonly="isReadOnly" />
            </div>
            
            <div class="sub-header mt-4">
              <h4>Vehículo</h4>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Patente</label>
                <InputBase v-model="formData.PEV_PATENTE" :readonly="isReadOnly" placeholder="AAAA00" />
              </div>
              <div class="field">
                <label>Marca</label>
                <InputBase v-model="formData.PEV_MARCA" :readonly="isReadOnly" />
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- TAB: HISTORY -->
      <div v-show="activeTab === 'history'" class="tab-content history-tab">
        <div v-if="history.length === 0" class="no-history">
          <AppIcons name="calendar" :size="48" />
          <p>No hay cursos registrados para esta persona.</p>
        </div>
        <div v-else class="history-list">
          <div v-for="item in history" :key="item.PEC_ID" class="history-card glass-panel">
            <div class="card-info">
              <div class="card-title">
                <strong>{{ item.CUR_NOMBRE }}</strong>
                <span class="code">#{{ item.CUR_CODIGO }}</span>
              </div>
              <div class="card-meta">
                <span><AppIcons name="award" :size="14" /> {{ item.ROL_DESCRIPCION }}</span>
                <span v-if="item.ESTADO_APROBACION" :class="['status', item.ESTADO_APROBACION.aprobado ? 'ok' : 'pending']">
                  {{ item.ESTADO_APROBACION.texto }}
                </span>
              </div>
            </div>
            <div class="card-actions">
              <button class="btn-outline" @click="$emit('nav-course', item.CUS_ID)">Ver Curso</button>
              <button class="btn-outline" @click="$emit('nav-payments', item.CUS_ID)">Pagos</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import InputBase from '@/components/InputBase.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import BaseModal from '@/components/BaseModal.vue'
import { calcularDv } from '@/utils/formatters'

const props = defineProps({
  initialData: { type: Object, default: () => ({}) },
  options: { type: Object, default: () => ({}) },
  history: { type: Array, default: () => [] },
  isEdit: Boolean,
  isReadOnly: Boolean,
  loading: Boolean
})

const emit = defineEmits(['save', 'cancel', 'region-change', 'provincia-change', 'nav-course', 'nav-payments', 'show-alert'])

const activeTab = ref('info')
const formData = reactive({
  ramas: [{ NIV_ID: '', RAM_ID_NIVEL: '' }],
  ...props.initialData
})

const API_ROOT = (import.meta.env?.VITE_API_BASE || 'http://localhost:8000/api').replace(/\/?api\/?$/, '')

const fotoUrlDisplay = computed(() => {
  if (!formData.PER_FOTO) return null
  if (formData.PER_FOTO.startsWith('data:')) return formData.PER_FOTO
  if (formData.PER_FOTO.startsWith('http')) return formData.PER_FOTO
  return `${API_ROOT}${formData.PER_FOTO.startsWith('/') ? '' : '/'}${formData.PER_FOTO}`
})

/**
 * Comprime una imagen usando Canvas y aplica Center Crop a 400x400
 */
const comprimirImagen = (file, quality = 0.7, targetSize = 400) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = () => {
        const canvasComp = document.createElement('canvas');
        canvasComp.width = targetSize;
        canvasComp.height = targetSize;
        const ctx = canvasComp.getContext('2d');

        // Calcular recorte para mantener proporción y centrar (Center Crop)
        let sourceSize = Math.min(img.width, img.height);
        let sourceX = (img.width - sourceSize) / 2;
        let sourceY = (img.height - sourceSize) / 2;

        ctx.drawImage(
          img,
          sourceX, sourceY, sourceSize, sourceSize,
          0, 0, targetSize, targetSize
        );

        canvasComp.toBlob(
          (blob) => {
            if (blob) resolve(blob);
            else reject(new Error('Error al comprimir imagen'));
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = (err) => reject(err);
    };
    reader.onerror = (err) => reject(err);
  });
};

const onFileChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
    emit('show-alert', { text: 'Solo se permiten imágenes JPG o PNG', type: 'error' })
    return
  }
  
  try {
    const blobComprimido = await comprimirImagen(file, 0.7, 400)
    // Convert blob to base64
    const reader = new FileReader()
    reader.onloadend = () => {
      formData.PER_FOTO = reader.result
    }
    reader.readAsDataURL(blobComprimido)
  } catch (err) {
    console.error('Error al procesar/comprimir imagen:', err)
    emit('show-alert', { text: 'Error al procesar la imagen', type: 'error' })
  }
}



const removePhoto = () => { formData.PER_FOTO = null }

// Logic
const limitDate = (val) => {
  if (!val) return
  const year = val.split('-')[0]
  if (year && year.length > 4) {
    formData.PER_FECHA_NAC = val.slice(0, 4) + val.slice(5) // Not perfect logic but placeholder for refinement
  }
}

const onRutInput = (val) => {
  if (val) {
    formData.PER_RUN = val.replace(/[^0-9]/g, '')
    if (formData.PER_RUN.length >= 7) {
      formData.PER_DV = calcularDv(formData.PER_RUN)
    }
  }
}

const onRegionChange = (val) => { emit('region-change', val) }
const onProvinciaChange = (val) => { emit('provincia-change', val) }

const addRama = () => { formData.ramas.push({ NIV_ID: '', RAM_ID_NIVEL: '' }) }
const removeRama = (idx) => { formData.ramas.splice(idx, 1) }

const handleSave = () => {
  emit('save', { ...formData })
}
</script>

<style scoped>
.persona-form {
  display: flex;
  flex-direction: column;
  height: 90vh;
  max-height: 850px;
  background: #f8fafc;
  border-radius: 16px;
  overflow: hidden;
}

.form-header {
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 { margin: 0; font-size: 1.5rem; color: #1a237e; }
.header-content .subtitle { margin: 4px 0 0; color: #64748b; font-weight: 500; }
.header-actions { display: flex; gap: 12px; }

.form-tabs {
  display: flex;
  background: white;
  padding: 0 24px;
  border-bottom: 1px solid #e2e8f0;
  gap: 24px;
}

.form-tabs button {
  padding: 16px 4px;
  background: none;
  border: none;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.form-tabs button.active {
  color: #1a237e;
  border-bottom-color: #1a237e;
}

.form-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.tab-content { display: flex; flex-direction: column; gap: 24px; }

.glass-panel {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.photo-section {
  display: flex;
  align-items: center;
  gap: 32px;
}

.photo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 0.8rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-section { display: flex; flex-direction: column; gap: 16px; }
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
  font-size: 1.1rem;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 12px;
}

.fields-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 0.85rem; font-weight: 600; color: #64748b; }

.rut-group { display: flex; gap: 8px; align-items: center; }
.rut-main { flex: 1; }
.rut-dv { width: 45px; }

.phone-group { display: flex; gap: 0; align-items: center; border: 1px solid #d1d5db; border-radius: 6px; overflow: hidden; background: white; }
.phone-group .prefix { padding: 0 12px; background: #f8fafc; color: #64748b; font-weight: 600; font-size: 0.9rem; }
.phone-group :deep(input) { border: none !important; }

.dynamic-sub-section { border-top: 1px solid #f1f5f9; padding-top: 16px; }
.sub-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.sub-header h4 { margin: 0; font-size: 0.95rem; color: #475569; }

.dynamic-row { display: flex; gap: 12px; align-items: center; margin-bottom: 12px; }
.row-fields { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.btn-remove { background: none; border: none; color: #ef4444; border-radius: 6px; cursor: pointer; padding: 8px; transition: 0.2s; }
.btn-remove:hover { background: #fee2e2; }

.history-card { padding: 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.card-title { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.card-title .code { font-size: 0.8rem; color: #94a3b8; font-family: monospace; }
.card-meta { display: flex; gap: 16px; font-size: 0.85rem; color: #64748b; }
.status { font-weight: 600; }
.status.ok { color: #10b981; }
.card-actions { display: flex; gap: 8px; }
.btn-outline { background: white; border: 1px solid #e2e8f0; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }
.btn-outline:hover { background: #f8fafc; color: #1a237e; border-color: #1a237e; }

.cropper-wrap { padding: 20px; display: flex; flex-direction: column; gap: 16px; }
.cropper-stage { height: 300px; background: #000; overflow: hidden; position: relative; display: flex; align-items: center; justify-content: center; border-radius: 8px; }
.crop-img { max-width: 100%; transition: 0.1s; }
.crop-overlay { position: absolute; border: 2px solid rgba(255,255,255,0.8); border-radius: 50%; width: 200px; height: 200px; box-shadow: 0 0 0 9999px rgba(0,0,0,0.5); pointer-events: none; }
.cropper-controls { display: grid; gap: 12px; }
.ctrl { display: flex; flex-direction: column; gap: 4px; }
.cropper-actions { display: flex; justify-content: flex-end; gap: 12px; }

@media (max-width: 1024px) {
  .form-grid { grid-template-columns: 1fr; }
  .persona-form { height: 95vh; max-height: none; }
}

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>
