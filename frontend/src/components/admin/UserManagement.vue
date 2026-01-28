<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
      <div class="flex items-center space-x-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search users..."
          class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        />
        <select
          v-model="roleFilter"
          class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
          <option value="">All Roles</option>
          <option value="patient">Patients</option>
          <option value="doctor">Doctors</option>
          <option value="admin">Admins</option>
        </select>
      </div>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Add User
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Joined</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-medium">
                  {{ getInitials(user.name) }}
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ user.name }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <span :class="getRoleBadgeClass(user.role)">{{ user.role }}</span>
            </td>
            <td class="px-6 py-4">
              <span :class="[
                'px-2 py-1 text-xs rounded-full',
                user.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]">
                {{ user.isActive ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
              {{ formatDate(user.createdAt) }}
            </td>
            <td class="px-6 py-4">
              <div class="flex space-x-2">
                <button @click="editUser(user)" class="text-blue-600 hover:text-blue-800">Edit</button>
                <button @click="toggleUserStatus(user)" class="text-yellow-600 hover:text-yellow-800">
                  {{ user.isActive ? 'Disable' : 'Enable' }}
                </button>
                <button @click="deleteUser(user)" class="text-red-600 hover:text-red-800">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-between items-center">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Showing {{ (page - 1) * pageSize + 1 }} to {{ Math.min(page * pageSize, totalUsers) }} of {{ totalUsers }} users
      </p>
      <div class="flex space-x-2">
        <button
          @click="page--"
          :disabled="page === 1"
          class="px-3 py-1 border rounded disabled:opacity-50 dark:border-gray-600 dark:text-white"
        >
          Previous
        </button>
        <button
          @click="page++"
          :disabled="page >= totalPages"
          class="px-3 py-1 border rounded disabled:opacity-50 dark:border-gray-600 dark:text-white"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const roleFilter = ref('')
const page = ref(1)
const pageSize = 10

const users = ref([
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'patient', isActive: true, createdAt: '2024-01-15' },
  { id: '2', name: 'Dr. Jane Smith', email: 'jane@example.com', role: 'doctor', isActive: true, createdAt: '2024-01-10' },
  { id: '3', name: 'Admin User', email: 'admin@example.com', role: 'admin', isActive: true, createdAt: '2024-01-01' }
])

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = !roleFilter.value || user.role === roleFilter.value
    return matchesSearch && matchesRole
  })
})

const totalUsers = computed(() => filteredUsers.value.length)
const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize))

function getInitials(name) {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function getRoleBadgeClass(role) {
  const classes = {
    admin: 'px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800',
    doctor: 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
    patient: 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
  }
  return classes[role] || classes.patient
}

function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

function editUser(user) {
  console.log('Edit user:', user)
}

function toggleUserStatus(user) {
  user.isActive = !user.isActive
}

function deleteUser(user) {
  if (confirm(`Delete user ${user.name}?`)) {
    users.value = users.value.filter(u => u.id !== user.id)
  }
}
</script>
