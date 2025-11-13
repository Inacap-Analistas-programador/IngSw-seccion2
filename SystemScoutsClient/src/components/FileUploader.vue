<template>
  <div class="file-uploader">
    <label v-if="label" class="upload-label">{{ label }}</label>
    
    <div 
      class="file-upload-area"
      :class="{ 
        'has-file': modelValue, 
        'is-dragging': isDragging,
        'is-invalid': hasError
      }"
      @click="triggerFileInput"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
    >
      <div class="upload-content">
        <div class="upload-icon">📷</div>
        
        <div v-if="!modelValue" class="upload-placeholder">
          <p class="upload-text">Haga clic o arrastre una foto aquí</p>
          <p class="upload-formats">Formatos aceptados: {{ acceptFormats }}</p>
        </div>
        
        <div v-else class="file-info">
          <div class="file-preview" v-if="isImage">
            <img :src="previewUrl" alt="Vista previa" class="preview-image" />
          </div>
          <div class="file-details">
            <p class="file-name">{{ fileName }}</p>
            <p class="file-size">{{ fileSize }}</p>
            <button type="button" class="remove-button" @click.stop="removeFile">
              ❌ Eliminar
            </button>
          </div>
        </div>
      </div>
      
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :required="required"
        @change="handleFileSelect"
        class="file-input"
      />
    </div>
    
    <div v-if="hasError" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'FileUploader',
  props: {
    modelValue: {
      type: [File, null],
      default: null
    },
    label: {
      type: String,
      default: ''
    },
    accept: {
      type: String,
      default: 'image/jpeg,image/png,image/jpg'
    },
    required: {
      type: Boolean,
      default: false
    },
    maxSize: {
      type: Number,
      default: 5 * 1024 * 1024 // 5MB por defecto
    }
  },
  emits: ['update:modelValue', 'upload'],
  setup(props, { emit }) {
    const fileInput = ref(null)
    const isDragging = ref(false)
    const previewUrl = ref('')
    const hasError = ref(false)
    const errorMessage = ref('')

    // Computed properties
    const acceptFormats = computed(() => {
      return props.accept.split(',').map(format => {
        if (format === 'image/jpeg') return 'JPEG'
        if (format === 'image/png') return 'PNG'
        if (format === 'image/jpg') return 'JPG'
        return format
      }).join(', ')
    })

    const fileName = computed(() => {
      return props.modelValue ? props.modelValue.name : ''
    })

    const fileSize = computed(() => {
      if (!props.modelValue) return ''
      const size = props.modelValue.size
      if (size < 1024) return `${size} B`
      if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
      return `${(size / (1024 * 1024)).toFixed(1)} MB`
    })

    const isImage = computed(() => {
      return props.modelValue && props.modelValue.type.startsWith('image/')
    })

    // Methods
    const triggerFileInput = () => {
      fileInput.value?.click()
    }

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        validateAndSetFile(file)
      }
    }

    const handleDragOver = (event) => {
      event.preventDefault()
      isDragging.value = true
    }

    const handleDragLeave = (event) => {
      event.preventDefault()
      isDragging.value = false
    }

    const handleDrop = (event) => {
      event.preventDefault()
      isDragging.value = false
      
      const files = event.dataTransfer.files
      if (files.length > 0) {
        validateAndSetFile(files[0])
      }
    }

    const validateAndSetFile = (file) => {
      hasError.value = false
      errorMessage.value = ''

      // Validar tipo de archivo
      const acceptedTypes = props.accept.split(',')
      if (!acceptedTypes.includes(file.type)) {
        hasError.value = true
        errorMessage.value = `Formato no válido. Formatos aceptados: ${acceptFormats.value}`
        return
      }

      // Validar tamaño
      if (file.size > props.maxSize) {
        hasError.value = true
        errorMessage.value = `El archivo es demasiado grande. Tamaño máximo: ${(props.maxSize / (1024 * 1024)).toFixed(0)}MB`
        return
      }

      // Crear URL para vista previa si es imagen
      if (file.type.startsWith('image/')) {
        if (previewUrl.value) {
          URL.revokeObjectURL(previewUrl.value)
        }
        previewUrl.value = URL.createObjectURL(file)
      }

      // Emitir el archivo
      emit('update:modelValue', file)
      emit('upload', file)
    }

    const removeFile = () => {
      if (previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value)
        previewUrl.value = ''
      }
      emit('update:modelValue', null)
      
      // Limpiar el input file
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    // Cleanup al desmontar el componente
    watch(() => props.modelValue, (newValue) => {
      if (!newValue && previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value)
        previewUrl.value = ''
      }
    })

    return {
      fileInput,
      isDragging,
      previewUrl,
      hasError,
      errorMessage,
      acceptFormats,
      fileName,
      fileSize,
      isImage,
      triggerFileInput,
      handleFileSelect,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      removeFile
    }
  }
}
</script>

<style scoped>
.file-uploader {
  margin-bottom: 1rem;
}

.upload-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #495057;
  font-size: 0.9rem;
}

.file-upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
  position: relative;
}

.file-upload-area:hover {
  border-color: #2c5aa0;
  background: #e7f3ff;
}

.file-upload-area.has-file {
  border-color: #28a745;
  background: #f8fff8;
}

.file-upload-area.is-dragging {
  border-color: #2c5aa0;
  background: #e3f2fd;
  transform: scale(1.02);
}

.file-upload-area.is-invalid {
  border-color: #dc3545;
  background: #f8f8f8;
}

.file-input {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 2.5rem;
}

.upload-text {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.25rem;
}

.upload-formats {
  font-size: 0.85rem;
  color: #6c757d;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.file-preview {
  flex-shrink: 0;
}

.preview-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  border: 2px solid #e9ecef;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.25rem;
  word-break: break-word;
}

.file-size {
  color: #6c757d;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.remove-button {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.remove-button:hover {
  background: #c82333;
}

.error-message {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .file-upload-area {
    padding: 1.5rem;
  }
  
  .file-info {
    flex-direction: column;
    text-align: center;
  }
  
  .file-details {
    text-align: center;
  }
}
</style>