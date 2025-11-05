<template>
  <div class="h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white text-center p-4 md:p-6">
    <div class="w-full max-w-lg mx-auto flex flex-col justify-center h-full py-8">
      <!-- Header Section -->
      <div class="flex-shrink-0 mb-8">
        <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-blue-700 leading-tight mb-4">
          {{ $t('home.welcome') }}
        </h1>

        <p class="text-sm sm:text-base lg:text-lg text-gray-700 leading-relaxed px-2">
          {{ $t('home.subtitle') }}
        </p>
      </div>

      <!-- Main Action Buttons -->
      <div class="flex-1 flex flex-col justify-center">
        <div class="flex flex-col gap-3 sm:gap-4 w-full max-w-md mx-auto">
          <router-link
            to="/voice-diagnosis"
            class="bg-blue-600 text-white text-sm sm:text-base lg:text-lg font-semibold py-3 sm:py-4 px-6 rounded-lg shadow-lg hover:bg-blue-700 transition duration-200 transform hover:scale-105 hover:shadow-xl"
          >
            {{ $t('home.startAssessment') }}
          </router-link>

          <router-link
            to="/dashboard"
            class="bg-green-600 text-white text-sm sm:text-base lg:text-lg font-semibold py-3 sm:py-4 px-6 rounded-lg shadow-lg hover:bg-green-700 transition duration-200 transform hover:scale-105 hover:shadow-xl"
          >
            {{ $t('home.viewDashboard') }} 📊
          </router-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex-shrink-0 mt-6">
        <div class="text-xs sm:text-sm text-gray-500">
          {{ $t('home.disclaimer') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// This view is static — no script needed
</script>
y are 