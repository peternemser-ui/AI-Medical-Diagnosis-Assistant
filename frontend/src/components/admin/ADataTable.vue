<template>
  <div
    :class="[
      'rounded-2xl border overflow-hidden',
      isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200'
    ]"
  >
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <!-- Header -->
        <thead>
          <tr :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
            <th
              v-for="col in columns"
              :key="col.key"
              :class="[
                'sticky top-0 px-4 py-3 font-semibold whitespace-nowrap select-none',
                col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left',
                col.sortable ? 'cursor-pointer hover:opacity-80' : '',
                isDark ? 'text-slate-300 bg-slate-800/60' : 'text-slate-600 bg-slate-50'
              ]"
              @click="col.sortable && toggleSort(col.key)"
            >
              <span class="inline-flex items-center gap-1">
                {{ col.label }}
                <span v-if="col.sortable" class="inline-flex flex-col leading-none text-[10px] opacity-60">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-3 h-3"
                    :class="sortKey === col.key && sortDir === 'asc' ? 'opacity-100' : 'opacity-30'"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M5 12l5-5 5 5H5z" />
                  </svg>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-3 h-3 -mt-1"
                    :class="sortKey === col.key && sortDir === 'desc' ? 'opacity-100' : 'opacity-30'"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M5 8l5 5 5-5H5z" />
                  </svg>
                </span>
              </span>
            </th>
            <th
              v-if="$slots['row-actions']"
              :class="[
                'sticky top-0 px-4 py-3 text-right font-semibold',
                isDark ? 'text-slate-300 bg-slate-800/60' : 'text-slate-600 bg-slate-50'
              ]"
            >
              Actions
            </th>
          </tr>
        </thead>

        <!-- Loading skeleton -->
        <tbody v-if="loading">
          <tr v-for="r in 5" :key="'skel-' + r">
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-3"
            >
              <div
                :class="[
                  'h-4 rounded animate-pulse',
                  isDark ? 'bg-slate-700' : 'bg-slate-200'
                ]"
                :style="{ width: (50 + Math.random() * 40) + '%' }"
              />
            </td>
            <td v-if="$slots['row-actions']" class="px-4 py-3">
              <div
                :class="[
                  'h-4 w-16 rounded animate-pulse ml-auto',
                  isDark ? 'bg-slate-700' : 'bg-slate-200'
                ]"
              />
            </td>
          </tr>
        </tbody>

        <!-- Data rows -->
        <tbody v-else-if="sortedRows.length">
          <tr
            v-for="(row, idx) in sortedRows"
            :key="idx"
            :class="[
              'transition-colors',
              isDark
                ? 'hover:bg-slate-800/50 border-slate-800'
                : 'hover:bg-slate-50 border-slate-100',
              idx < sortedRows.length - 1 ? 'border-b' : ''
            ]"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-4 py-3',
                col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left',
                isDark ? 'text-slate-300' : 'text-slate-700'
              ]"
            >
              <slot :name="'cell-' + col.key" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
            <td
              v-if="$slots['row-actions']"
              :class="[
                'px-4 py-3 text-right',
                isDark ? 'text-slate-300' : 'text-slate-700'
              ]"
            >
              <slot name="row-actions" :row="row" />
            </td>
          </tr>
        </tbody>

        <!-- Empty state -->
        <tbody v-else>
          <tr>
            <td
              :colspan="columns.length + ($slots['row-actions'] ? 1 : 0)"
              :class="[
                'px-4 py-12 text-center',
                isDark ? 'text-slate-500' : 'text-slate-400'
              ]"
            >
              {{ emptyText }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyText: {
    type: String,
    default: 'No data available'
  }
})

const sortKey = ref(null)
const sortDir = ref(null) // 'asc' | 'desc' | null

function toggleSort(key) {
  if (sortKey.value !== key) {
    sortKey.value = key
    sortDir.value = 'asc'
  } else if (sortDir.value === 'asc') {
    sortDir.value = 'desc'
  } else {
    sortKey.value = null
    sortDir.value = null
  }
}

const sortedRows = computed(() => {
  if (!sortKey.value || !sortDir.value) return props.rows

  const key = sortKey.value
  const dir = sortDir.value === 'asc' ? 1 : -1

  return [...props.rows].sort((a, b) => {
    const aVal = a[key]
    const bVal = b[key]
    if (aVal == null && bVal == null) return 0
    if (aVal == null) return 1
    if (bVal == null) return -1
    if (typeof aVal === 'number' && typeof bVal === 'number') return (aVal - bVal) * dir
    return String(aVal).localeCompare(String(bVal)) * dir
  })
})
</script>
