<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center p-4">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/5 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/5 rounded-full blur-[120px]"></div>
    </div>

    <div class="relative z-10 max-w-md w-full space-y-6">
      <!-- Logo + Title -->
      <div class="text-center">
        <div class="inline-flex p-3 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-xl shadow-blue-500/20 mb-5">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">Medical Diagnosis AI</h1>
        <p class="text-sm text-slate-400 mt-1">Connect your AI provider to get started</p>
      </div>

      <!-- Main Card -->
      <div class="bg-slate-900/80 backdrop-blur-xl rounded-2xl border border-slate-800 shadow-2xl overflow-hidden">
        <!-- Provider Tabs -->
        <div class="flex border-b border-slate-800">
          <button
            @click="provider = 'anthropic'"
            class="flex-1 py-3.5 text-sm font-medium transition-all relative"
            :class="provider === 'anthropic' ? 'text-white' : 'text-slate-500 hover:text-slate-300'"
          >
            Anthropic
            <span v-if="provider === 'anthropic'" class="absolute bottom-0 left-4 right-4 h-0.5 bg-blue-500 rounded-full"></span>
            <span v-if="provider === 'anthropic'" class="ml-1.5 text-[9px] bg-blue-500/20 text-blue-400 px-1.5 py-0.5 rounded-full">recommended</span>
          </button>
          <button
            @click="provider = 'openai'"
            class="flex-1 py-3.5 text-sm font-medium transition-all relative"
            :class="provider === 'openai' ? 'text-white' : 'text-slate-500 hover:text-slate-300'"
          >
            OpenAI
            <span v-if="provider === 'openai'" class="absolute bottom-0 left-4 right-4 h-0.5 bg-emerald-500 rounded-full"></span>
          </button>
          <button
            @click="provider = 'ollama'; checkOllama()"
            class="flex-1 py-3.5 text-sm font-medium transition-all relative"
            :class="provider === 'ollama' ? 'text-white' : 'text-slate-500 hover:text-slate-300'"
          >
            Ollama
            <span v-if="provider === 'ollama'" class="absolute bottom-0 left-4 right-4 h-0.5 bg-orange-500 rounded-full"></span>
            <span v-if="provider !== 'ollama'" class="ml-1 text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded-full">free</span>
          </button>
        </div>

        <div class="p-6 space-y-5">
          <!-- Ollama Mode -->
          <template v-if="provider === 'ollama'">
            <div class="text-center space-y-3">
              <!-- Status indicator -->
              <div v-if="ollamaChecking" class="flex items-center justify-center gap-2 py-4">
                <svg class="w-4 h-4 animate-spin text-orange-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <span class="text-sm text-slate-400">Detecting Ollama...</span>
              </div>
              <div v-else-if="ollamaAvailable" class="space-y-4">
                <div class="flex items-center justify-center gap-2 py-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
                  <span class="text-sm text-emerald-400 font-medium">Ollama is running</span>
                </div>
                <div class="p-3 rounded-xl bg-slate-800/60 border border-slate-700/30 text-left">
                  <div class="text-[10px] text-slate-500 uppercase font-semibold mb-2">Available Models</div>
                  <div v-for="model in ollamaModels" :key="model" class="flex items-center gap-2 py-1">
                    <svg class="w-3.5 h-3.5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    <span class="text-xs text-slate-300">{{ model }}</span>
                  </div>
                </div>
                <div class="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/15">
                  <p class="text-xs text-emerald-300/80">Runs 100% locally on your machine. No API key needed, no usage costs, unlimited consultations.</p>
                </div>
              </div>
              <div v-else class="space-y-3 py-2">
                <div class="flex items-center justify-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                  <span class="text-sm text-red-400 font-medium">Ollama not detected</span>
                </div>
                <div class="p-3 rounded-lg bg-slate-800/60 border border-slate-700/30 text-left">
                  <p class="text-xs text-slate-400 mb-2">To use Ollama (free local AI):</p>
                  <ol class="text-xs text-slate-500 space-y-1.5 list-decimal ml-4">
                    <li>Download from <span class="text-orange-400">ollama.com</span></li>
                    <li>Install and run it</li>
                    <li>Open a terminal and run: <code class="text-orange-400 bg-slate-800 px-1.5 py-0.5 rounded">ollama pull llama3.1:8b</code></li>
                    <li>Come back here and click "Retry Detection"</li>
                  </ol>
                </div>
                <button @click="checkOllama" class="text-xs text-orange-400 hover:text-orange-300 underline underline-offset-2">Retry Detection</button>
              </div>
            </div>
          </template>

          <!-- API Key Input (Anthropic/OpenAI) -->
          <template v-else>
            <div>
              <label class="text-xs text-slate-400 font-medium mb-1.5 block">
                {{ provider === 'anthropic' ? 'Anthropic API Key' : 'OpenAI API Key' }}
              </label>
              <div class="relative">
                <input
                  v-model="apiKey"
                  :type="showApiKey ? 'text' : 'password'"
                  :placeholder="provider === 'anthropic' ? 'sk-ant-api03-...' : 'sk-proj-...'"
                  class="w-full bg-slate-800/80 border border-slate-700/50 rounded-xl px-4 py-3 text-white text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                  @keyup.enter="saveAndContinue"
                />
                <button
                  @click="showApiKey = !showApiKey"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-500 hover:text-slate-300"
                >
                  <svg v-if="showApiKey" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.543 7-1.275 4.057-5.065 7-9.543 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>
          </template>

          <!-- Status messages -->
          <div v-if="error" class="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
            <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <p class="text-red-300 text-xs">{{ error }}</p>
          </div>
          <div v-if="success" class="flex items-start gap-2 p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
            <svg class="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <p class="text-emerald-300 text-xs">{{ success }}</p>
          </div>

          <!-- Buttons -->
          <div class="flex gap-3">
            <button
              @click="saveAndContinue"
              :disabled="(provider !== 'ollama' && !apiKey.trim()) || (provider === 'ollama' && !ollamaAvailable) || isLoading"
              class="flex-1 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl text-sm transition-all duration-200 flex items-center justify-center gap-2"
            >
              <svg v-if="isLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              {{ isLoading ? 'Connecting...' : provider === 'ollama' ? 'Use Ollama & Start' : 'Connect & Start' }}
            </button>
            <button
              @click="skipSetup"
              class="px-5 py-3 text-slate-400 hover:text-white text-sm font-medium rounded-xl hover:bg-slate-800 transition-all"
            >
              Skip
            </button>
          </div>
          <p class="text-[10px] text-slate-600 text-center">{{ provider === 'ollama' ? 'Ollama runs locally — no API key or costs needed.' : 'Skip uses basic mode without AI agents. You can add a key later in Settings.' }}</p>
        </div>
      </div>

      <!-- Agent Pipeline Preview -->
      <div class="bg-slate-900/60 backdrop-blur rounded-xl border border-slate-800/50 p-4">
        <div class="text-[10px] text-slate-500 uppercase tracking-wider font-semibold mb-3">7-Agent Pipeline</div>
        <div class="flex items-center gap-1 overflow-x-auto no-scrollbar">
          <div v-for="(agent, i) in agents" :key="agent.name" class="flex items-center gap-1">
            <div class="flex items-center gap-1.5 bg-slate-800/70 rounded-lg px-2.5 py-1.5 flex-shrink-0">
              <span class="text-xs">{{ agent.icon }}</span>
              <div>
                <div class="text-[10px] font-medium text-slate-300">{{ agent.name }}</div>
                <div class="text-[8px] text-slate-600">{{ agent.desc }}</div>
              </div>
            </div>
            <svg v-if="i < agents.length - 1" class="w-3 h-3 text-slate-700 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- Help link -->
      <div class="text-center space-y-2">
        <button @click="showHelp = !showHelp" class="text-xs text-slate-500 hover:text-slate-300 transition-colors">
          {{ showHelp ? 'Hide instructions' : 'How to get an API key?' }}
        </button>
        <div v-if="showHelp" class="bg-slate-900/60 rounded-xl border border-slate-800/50 p-4 text-left">
          <div v-if="provider === 'anthropic'">
            <ol class="text-xs text-slate-400 space-y-1.5 list-decimal ml-4">
              <li>Go to <a href="https://console.anthropic.com/settings/keys" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">console.anthropic.com</a></li>
              <li>Sign in or create an account</li>
              <li>Navigate to API Keys</li>
              <li>Create a new key and paste it above</li>
            </ol>
          </div>
          <div v-else>
            <ol class="text-xs text-slate-400 space-y-1.5 list-decimal ml-4">
              <li>Go to <a href="https://platform.openai.com/api-keys" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">platform.openai.com/api-keys</a></li>
              <li>Sign in or create an account</li>
              <li>Click "Create new secret key"</li>
              <li>Copy and paste it above</li>
            </ol>
          </div>
          <p class="text-[10px] text-slate-600 mt-3">Your key is stored locally and never sent to our servers.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ApiKeySetup',
  setup() {
    const router = useRouter()
    const provider = ref(localStorage.getItem('ai_provider') || 'anthropic')
    const apiKey = ref(localStorage.getItem('anthropic_api_key') || localStorage.getItem('openai_api_key') || '')
    const showApiKey = ref(false)
    const showHelp = ref(false)
    const isLoading = ref(false)
    const error = ref('')
    const success = ref('')

    // Ollama state
    const ollamaChecking = ref(false)
    const ollamaAvailable = ref(false)
    const ollamaModels = ref([])

    const agents = [
      { name: 'Triage', icon: '🚨', desc: 'Urgency' },
      { name: 'Diagnosis', icon: '🔬', desc: 'DDx' },
      { name: 'Research', icon: '📚', desc: 'Evidence' },
      { name: 'Specialist', icon: '🏥', desc: 'Deep analysis' },
      { name: 'Treatment', icon: '💊', desc: 'Care plan' },
      { name: 'Safety', icon: '🛡️', desc: 'Review' },
      { name: 'Summary', icon: '💬', desc: 'Plain language' },
    ]

    const checkOllama = async () => {
      ollamaChecking.value = true
      error.value = ''
      try {
        const resp = await fetch('http://localhost:8000/health')
        const data = await resp.json()
        ollamaAvailable.value = data.ollama_available || false
        ollamaModels.value = data.ollama_models || []
      } catch {
        ollamaAvailable.value = false
        ollamaModels.value = []
      } finally {
        ollamaChecking.value = false
      }
    }

    const validateApiKey = (key) => {
      if (provider.value === 'ollama') return null
      if (!key.trim()) return 'API key is required'
      if (provider.value === 'anthropic' && !key.startsWith('sk-ant-'))
        return 'Anthropic keys start with "sk-ant-"'
      if (provider.value === 'openai' && !key.startsWith('sk-'))
        return 'OpenAI keys start with "sk-"'
      if (key.length < 20) return 'Key appears too short'
      return null
    }

    const saveAndContinue = async () => {
      error.value = ''
      success.value = ''

      // Ollama path — no API key needed
      if (provider.value === 'ollama') {
        if (!ollamaAvailable.value) {
          error.value = 'Ollama is not running. Please start it first.'
          return
        }
        isLoading.value = true
        localStorage.setItem('ai_provider', 'ollama')
        localStorage.removeItem('anthropic_api_key')
        localStorage.removeItem('openai_api_key')
        localStorage.setItem('api_key_configured', 'true')
        success.value = 'Connected to Ollama! Redirecting...'
        setTimeout(() => router.push('/consult'), 800)
        isLoading.value = false
        return
      }

      const err = validateApiKey(apiKey.value)
      if (err) { error.value = err; return }

      isLoading.value = true
      try {
        const key = apiKey.value.trim()
        localStorage.setItem('ai_provider', provider.value)
        if (provider.value === 'anthropic') {
          localStorage.setItem('anthropic_api_key', key)
        } else {
          localStorage.setItem('openai_api_key', key)
        }
        localStorage.setItem('api_key_configured', 'true')

        // Validate the key by making a test API call
        success.value = 'Validating key...'
        try {
          const { validateApiKeys } = await import('@/services/api.js')
          const result = await validateApiKeys()
          const vendorResult = result.results[provider.value]
          if (vendorResult && vendorResult.valid) {
            success.value = `Key validated! ${vendorResult.message}. Redirecting...`
            setTimeout(() => router.push('/consult'), 1000)
          } else if (vendorResult) {
            error.value = `Key validation failed: ${vendorResult.message}`
            success.value = ''
          } else {
            success.value = 'Key saved! Redirecting...'
            setTimeout(() => router.push('/consult'), 800)
          }
        } catch (validationErr) {
          success.value = 'Key saved (validation unavailable). Redirecting...'
          setTimeout(() => router.push('/consult'), 800)
        }
      } catch (e) {
        error.value = 'Failed to save. Please try again.'
      } finally {
        isLoading.value = false
      }
    }

    const skipSetup = () => {
      localStorage.setItem('api_key_configured', 'skipped')
      router.push('/consult')
    }

    return { provider, apiKey, showApiKey, showHelp, isLoading, error, success, agents, saveAndContinue, skipSetup, ollamaChecking, ollamaAvailable, ollamaModels, checkOllama }
  }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
