<template>
  <div
    :class="[
      'border-2 border-dashed rounded-lg p-6 text-center transition-colors',
      isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600',
      'hover:border-blue-400'
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <input ref="fileInput" type="file" :accept="accept" :multiple="multiple" class="hidden" @change="handleFileSelect" />
    <svg class="mx-auto w-12 h-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
    <p class="text-gray-600 dark:text-gray-400 mb-2">
      <button type="button" @click="$refs.fileInput.click()" class="text-blue-600 hover:text-blue-700 font-medium">
        Click to upload
      </button>
      or drag and drop
    </p>
    <p class="text-xs text-gray-500">{{ hint }}</p>

    <div v-if="files.length > 0" class="mt-4 space-y-2">
      <div v-for="(file, index) in files" :key="index" class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
        <span class="text-sm text-gray-700 dark:text-gray-300 truncate">{{ file.name }}</span>
        <button @click="removeFile(index)" class="text-red-500 hover:text-red-600">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  accept: { type: String, default: 'image/*' },
  multiple: { type: Boolean, default: false },
  maxSize: { type: Number, default: 5 * 1024 * 1024 },
  hint: { type: String, default: 'PNG, JPG up to 5MB' }
})

const emit = defineEmits(['update:files', 'error'])

const files = ref([])
const isDragging = ref(false)

const handleFileSelect = (e) => processFiles(e.target.files)
const handleDrop = (e) => {
  isDragging.value = false
  processFiles(e.dataTransfer.files)
}

const processFiles = (fileList) => {
  const newFiles = Array.from(fileList).filter(file => {
    if (file.size > props.maxSize) {
      emit('error', `File ${file.name} is too large`)
      return false
    }
    return true
  })
  files.value = props.multiple ? [...files.value, ...newFiles] : newFiles
  emit('update:files', files.value)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
  emit('update:files', files.value)
}
</script>
