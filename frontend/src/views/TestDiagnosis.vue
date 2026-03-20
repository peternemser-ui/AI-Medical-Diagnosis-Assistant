<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 text-white flex flex-col">
    <div class="p-8">
      <h1 class="text-3xl font-bold mb-4">🚀 TEST COMPONENT LOADED SUCCESSFULLY</h1>
      <div class="bg-gray-800 p-4 rounded">
        <h2 class="text-xl mb-2">AI Health Assistant</h2>
        <p class="mb-4">Hello! I'm your AI health assistant. What brings you here today?</p>
        <p class="text-sm text-gray-300">This is a test component to verify Vue is working.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
console.log('✅ TEST COMPONENT LOADED - Vue is working!')
console.log('🌍 Current location:', window.location.href)
</script>
