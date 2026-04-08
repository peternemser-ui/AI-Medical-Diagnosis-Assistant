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
    chunkSizeWarningLimit: 700,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined
          const norm = id.replace(/\\/g, '/')
          const pkg = (name) => norm.includes(`/node_modules/${name}/`)
          if (pkg('vue') || pkg('vue-router') || pkg('@vue')) return 'vendor-vue'
          if (pkg('marked') || pkg('dompurify')) return 'vendor-markdown'
          if (pkg('html2pdf.js') || pkg('html2canvas')) return 'vendor-pdf'
          if (pkg('chart.js') || pkg('vue-chartjs') || pkg('chartjs-plugin-datalabels')) return 'vendor-charts'
          if (pkg('microsoft-cognitiveservices-speech-sdk')) return 'vendor-speech'
          if (pkg('lucide-vue-next')) return 'vendor-icons'
          if (pkg('@vueuse')) return 'vendor-vueuse'
          return 'vendor'
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  test: {
    exclude: ['e2e/**', 'node_modules/**', 'dist/**', '.{idea,git,cache,output,temp}/**', '**/*.{benchmark,bench}.?(c|m)[jt]s?(x)'],
    environment: 'jsdom',
  },
})