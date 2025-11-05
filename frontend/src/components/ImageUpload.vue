<template>
  <div class="image-upload-container">
    <!-- Upload Area -->
    <div 
      class="upload-zone"
      :class="{ 
        'drag-over': isDragging,
        'has-images': images.length > 0,
        'disabled': disabled || isUploading
      }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        multiple
        @change="handleFileSelect"
        style="display: none"
      />
      
      <div v-if="images.length === 0" class="upload-prompt">
        <MaterialIcon icon="add_photo_alternate" size="xxl" :fill="true" class="upload-icon" />
        <h3 class="text-lg font-semibold mb-2">Upload Symptom Photos</h3>
        <p class="text-sm text-gray-400 mb-3">
          Click to browse or drag & drop images here
        </p>
        <p class="text-xs text-gray-500">
          Supports: JPG, PNG, WebP (Max 10MB per image)
        </p>
      </div>
      
      <div v-else class="upload-prompt-mini">
        <MaterialIcon icon="add_photo_alternate" size="lg" />
        <span class="text-sm ml-2">Add more photos</span>
      </div>
    </div>

    <!-- Image Preview Grid -->
    <div v-if="images.length > 0" class="image-grid">
      <div 
        v-for="(image, index) in images" 
        :key="index"
        class="image-card"
      >
        <div class="image-wrapper">
          <img :src="image.preview" :alt="`Symptom photo ${index + 1}`" />
          
          <!-- Remove button -->
          <button
            @click.stop="removeImage(index)"
            class="remove-btn"
            :disabled="disabled || isUploading"
            title="Remove image"
          >
            <MaterialIcon icon="close" size="sm" />
          </button>
          
          <!-- Analysis status -->
          <div v-if="image.analyzing" class="analysis-overlay">
            <div class="spinner"></div>
            <span class="text-xs">Analyzing...</span>
          </div>
          
          <div v-else-if="image.analysis" class="analysis-badge">
            <MaterialIcon icon="check_circle" size="xs" />
            <span class="text-xs ml-1">Analyzed</span>
          </div>
        </div>
        
        <!-- Image info -->
        <div class="image-info">
          <p class="text-xs text-gray-400 truncate">{{ image.name }}</p>
          <p class="text-xs text-gray-500">{{ formatFileSize(image.size) }}</p>
        </div>
        
        <!-- Analysis result preview -->
        <div v-if="image.analysis" class="analysis-preview">
          <p class="text-xs text-gray-300">{{ image.analysis.substring(0, 100) }}...</p>
        </div>
      </div>
    </div>

    <!-- Upload Progress -->
    <div v-if="isUploading" class="upload-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
      </div>
      <p class="text-xs text-gray-400 mt-1">Uploading and analyzing images... {{ uploadProgress }}%</p>
    </div>

    <!-- Error message -->
    <div v-if="errorMessage" class="error-message">
      <MaterialIcon icon="error" size="sm" />
      <span class="text-sm ml-2">{{ errorMessage }}</span>
    </div>

    <!-- Action buttons -->
    <div v-if="images.length > 0 && !isUploading" class="action-buttons">
      <button
        @click="analyzeImages"
        :disabled="disabled || images.every(img => img.analysis)"
        class="btn-analyze"
      >
        <MaterialIcon icon="psychology" size="sm" />
        <span class="ml-2">Analyze Images</span>
      </button>
      
      <button
        @click="clearAll"
        :disabled="disabled"
        class="btn-clear"
      >
        <MaterialIcon icon="delete" size="sm" />
        <span class="ml-2">Clear All</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MaterialIcon from './MaterialIcon.vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  maxImages: {
    type: Number,
    default: 5
  },
  maxSizeBytes: {
    type: Number,
    default: 10 * 1024 * 1024 // 10MB
  }
})

const emit = defineEmits(['images-updated', 'analysis-complete'])

const fileInput = ref(null)
const images = ref([])
const isDragging = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const errorMessage = ref('')

const triggerFileInput = () => {
  if (!props.disabled && !isUploading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
  // Reset input so same file can be selected again
  event.target.value = ''
}

const handleDrop = (event) => {
  isDragging.value = false
  if (props.disabled || isUploading.value) return
  
  const files = Array.from(event.dataTransfer.files)
  addFiles(files)
}

const addFiles = (files) => {
  errorMessage.value = ''
  
  // Filter valid image files
  const validFiles = files.filter(file => {
    if (!file.type.startsWith('image/')) {
      errorMessage.value = 'Only image files are allowed'
      return false
    }
    if (file.size > props.maxSizeBytes) {
      errorMessage.value = `File ${file.name} is too large (max ${formatFileSize(props.maxSizeBytes)})`
      return false
    }
    return true
  })
  
  // Check max images limit
  if (images.value.length + validFiles.length > props.maxImages) {
    errorMessage.value = `Maximum ${props.maxImages} images allowed`
    return
  }
  
  // Process files
  validFiles.forEach(file => {
    const reader = new FileReader()
    
    reader.onload = (e) => {
      images.value.push({
        file,
        name: file.name,
        size: file.size,
        preview: e.target.result,
        analyzing: false,
        analysis: null
      })
      
      emit('images-updated', images.value)
    }
    
    reader.readAsDataURL(file)
  })
}

const removeImage = (index) => {
  images.value.splice(index, 1)
  emit('images-updated', images.value)
}

const clearAll = () => {
  images.value = []
  errorMessage.value = ''
  emit('images-updated', images.value)
}

const analyzeImages = async () => {
  if (images.value.length === 0) return
  
  isUploading.value = true
  uploadProgress.value = 0
  errorMessage.value = ''
  
  try {
    const unanalyzedImages = images.value.filter(img => !img.analysis)
    
    for (let i = 0; i < unanalyzedImages.length; i++) {
      const image = unanalyzedImages[i]
      image.analyzing = true
      
      // Send to backend for analysis
      const formData = new FormData()
      formData.append('image', image.file)
      
      const response = await fetch('/api/analyze-image', {
        method: 'POST',
        body: formData,
        headers: {
          'X-API-Key': localStorage.getItem('openai_api_key') || ''
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to analyze image')
      }
      
      const result = await response.json()
      image.analysis = result.analysis
      image.analyzing = false
      
      uploadProgress.value = Math.round(((i + 1) / unanalyzedImages.length) * 100)
    }
    
    emit('analysis-complete', images.value)
    
  } catch (error) {
    console.error('Image analysis error:', error)
    errorMessage.value = 'Failed to analyze images. Please try again.'
    
    // Reset analyzing state
    images.value.forEach(img => {
      img.analyzing = false
    })
  } finally {
    isUploading.value = false
    uploadProgress.value = 0
  }
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// Expose methods to parent
defineExpose({
  analyzeImages,
  clearAll,
  getImages: () => images.value
})
</script>

<style scoped>
.image-upload-container {
  width: 100%;
}

.upload-zone {
  border: 2px dashed #4B5563;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(31, 41, 55, 0.5);
}

.upload-zone:hover:not(.disabled) {
  border-color: #60A5FA;
  background: rgba(59, 130, 246, 0.1);
}

.upload-zone.drag-over {
  border-color: #3B82F6;
  background: rgba(59, 130, 246, 0.2);
  transform: scale(1.02);
}

.upload-zone.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-zone.has-images {
  padding: 1rem;
  margin-bottom: 1rem;
}

.upload-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  color: #60A5FA;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.upload-prompt-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #60A5FA;
  font-weight: 500;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.image-card {
  background: rgba(31, 41, 55, 0.8);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #374151;
}

.image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.8;
}

.remove-btn:hover:not(:disabled) {
  opacity: 1;
  transform: scale(1.1);
  background: rgba(239, 68, 68, 1);
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.analysis-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.analysis-badge {
  position: absolute;
  bottom: 0.5rem;
  left: 0.5rem;
  background: rgba(34, 197, 94, 0.9);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  font-size: 0.75rem;
}

.image-info {
  padding: 0.5rem;
  border-top: 1px solid #374151;
}

.analysis-preview {
  padding: 0.5rem;
  background: rgba(59, 130, 246, 0.1);
  border-top: 1px solid #374151;
}

.upload-progress {
  margin-top: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(75, 85, 99, 0.5);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3B82F6, #60A5FA);
  transition: width 0.3s ease;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #FCA5A5;
  display: flex;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn-analyze,
.btn-clear {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-analyze {
  background: linear-gradient(135deg, #3B82F6, #8B5CF6);
  color: white;
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-clear {
  background: rgba(239, 68, 68, 0.1);
  color: #FCA5A5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.btn-clear:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}
</style>
