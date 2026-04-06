import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const backendUrl = process.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: true,
    open: true,
    cors: true,
    proxy: {
      '/api': {
        target: backendUrl,
        changeOrigin: true,
        timeout: 600000,
        proxyTimeout: 600000,
      },
      '/health': {
        target: backendUrl,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: process.env.NODE_ENV !== 'production',
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-vue': ['vue', 'vue-router'],
          'vendor-marked': ['marked'],
          'vendor-dompurify': ['dompurify'],
          'vendor-html2pdf': ['html2pdf.js'],
          'vendor-html2canvas': ['html2canvas'],
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})