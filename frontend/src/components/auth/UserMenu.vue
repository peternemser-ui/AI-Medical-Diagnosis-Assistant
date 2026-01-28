<template>
  <div class="relative" ref="menuRef">
    <button
      @click="isOpen = !isOpen"
      class="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
    >
      <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-medium">
        {{ userInitials }}
      </div>
      <span class="hidden md:block text-gray-700 dark:text-gray-300">{{ userName }}</span>
      <ChevronDown class="w-4 h-4 text-gray-500" :class="{ 'rotate-180': isOpen }" />
    </button>

    <!-- Dropdown menu -->
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50"
      >
        <!-- User info -->
        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <p class="text-sm font-medium text-gray-900 dark:text-white">{{ userName }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ userEmail }}</p>
        </div>

        <!-- Menu items -->
        <div class="py-1">
          <button
            @click="navigateTo('profile')"
            class="w-full flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <User class="w-4 h-4 mr-3" />
            {{ $t('auth.profile') || 'Profile' }}
          </button>

          <button
            @click="navigateTo('settings')"
            class="w-full flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Settings class="w-4 h-4 mr-3" />
            {{ $t('auth.settings') || 'Settings' }}
          </button>

          <button
            @click="navigateTo('history')"
            class="w-full flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <History class="w-4 h-4 mr-3" />
            {{ $t('auth.diagnosisHistory') || 'Diagnosis History' }}
          </button>

          <div v-if="isAdmin" class="border-t border-gray-200 dark:border-gray-700 my-1"></div>

          <button
            v-if="isAdmin"
            @click="navigateTo('admin')"
            class="w-full flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Shield class="w-4 h-4 mr-3" />
            {{ $t('auth.adminPanel') || 'Admin Panel' }}
          </button>
        </div>

        <!-- Logout -->
        <div class="border-t border-gray-200 dark:border-gray-700 py-1">
          <button
            @click="handleLogout"
            class="w-full flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
          >
            <LogOut class="w-4 h-4 mr-3" />
            {{ $t('auth.logout') || 'Logout' }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, User, Settings, History, Shield, LogOut } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { userName, userEmail, isAdmin, logout } = useAuth()

const isOpen = ref(false)
const menuRef = ref(null)

const userInitials = computed(() => {
  if (!userName.value) return '?'
  return userName.value
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

function navigateTo(route) {
  isOpen.value = false
  router.push(`/${route}`)
}

async function handleLogout() {
  isOpen.value = false
  await logout()
  router.push('/login')
}

function handleClickOutside(event) {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
