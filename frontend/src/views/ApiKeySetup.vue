<template>
  <div class="overflow-hidden">
    <!-- Backdrop overlay -->
    <Transition name="modal-backdrop">
      <div class="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm"></div>
    </Transition>

    <!-- Modal dialog -->
    <Transition name="modal">
      <div class="fixed inset-0 z-50 flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-label="API Key Setup">

        <!-- Modal card -->
        <div class="relative max-w-[1050px] w-[95vw] max-h-[82vh] grid grid-cols-1 lg:grid-cols-[38%_1fr] rounded-2xl shadow-2xl shadow-black/60 border border-slate-700/50 overflow-hidden">

          <!-- Close button -->
          <button
            @click="skipSetup"
            class="absolute top-4 right-4 z-10 p-1.5 rounded-lg text-slate-500 hover:text-white hover:bg-slate-800 transition-all"
            aria-label="Close"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>

          <!-- Left branding panel (hidden on mobile) -->
          <div class="hidden lg:flex relative items-center justify-center p-6 bg-slate-950 rounded-l-2xl">
            <div class="relative z-10 max-w-sm">
              <div class="inline-flex p-4 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-2xl shadow-emerald-500/25 mb-8">
                <svg class="w-12 h-12 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
                </svg>
              </div>
              <h1 class="text-4xl font-extrabold text-white tracking-tight leading-tight">Medical<br/>Diagnosis AI</h1>
              <p class="text-slate-400 mt-4 text-base leading-relaxed">Multi-agent clinical analysis powered by 7 specialized AI agents working together to provide comprehensive diagnostic insights.</p>

              <!-- Pipeline preview -->
              <div class="mt-10 space-y-3">
                <div class="text-detail text-slate-500 uppercase tracking-widest font-bold">Diagnostic Pipeline</div>
                <div class="grid grid-cols-2 gap-2">
                  <div v-for="agent in agents" :key="agent.name" class="flex items-center gap-2.5 bg-slate-800/40 rounded-lg px-3 py-2 border border-slate-800/60">
                    <span class="text-sm">{{ agent.icon }}</span>
                    <div>
                      <div class="text-caption font-semibold text-slate-300">{{ agent.name }}</div>
                      <div class="text-tiny text-slate-600">{{ agent.desc }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Trust signals -->
              <div class="mt-8 flex items-center gap-4 text-detail text-slate-600">
                <div class="flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                  Keys stored locally
                </div>
                <div class="flex items-center gap-1.5">
                  <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                  HIPAA-aware design
                </div>
              </div>
            </div>
          </div>

          <!-- Right config panel -->
          <div class="overflow-y-auto bg-slate-900 rounded-2xl lg:rounded-l-none lg:rounded-r-2xl scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
            <div class="p-6 space-y-4">

              <!-- Mobile logo (hidden on desktop) -->
              <div class="lg:hidden text-center mb-2">
                <div class="inline-flex p-3 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-xl shadow-emerald-500/20 mb-4">
                  <svg class="w-9 h-9 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
                  </svg>
                </div>
                <h1 class="text-2xl font-bold text-white">Medical Diagnosis AI</h1>
                <p class="text-sm text-slate-400 mt-1">Connect your AI provider to get started</p>
              </div>

              <!-- Desktop heading -->
              <div class="hidden lg:block">
                <h2 class="text-xl font-bold text-white">Connect your AI provider</h2>
                <p class="text-sm text-slate-400 mt-1">Choose a provider and enter your API key to begin</p>
              </div>

              <!-- Provider Tabs (segmented control) -->
              <div class="grid grid-cols-4 bg-slate-800 rounded-xl p-1 gap-1">
                <button
                  @click="provider = 'anthropic'"
                  class="py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all text-center"
                  :class="provider === 'anthropic' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'"
                >
                  Anthropic
                </button>
                <button
                  @click="provider = 'openai'"
                  class="py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all text-center"
                  :class="provider === 'openai' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'"
                >
                  OpenAI
                </button>
                <button
                  @click="provider = 'google'"
                  class="py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all text-center"
                  :class="provider === 'google' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'"
                >
                  Google
                </button>
                <button
                  @click="provider = 'ollama'; checkOllama()"
                  class="py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all text-center"
                  :class="provider === 'ollama' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'"
                >
                  Ollama
                </button>
              </div>

              <!-- Provider badge row -->
              <div>
                <div v-if="provider === 'anthropic'" class="flex items-center gap-2">
                  <span class="text-tiny font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-blue-500/15 text-blue-400 border border-blue-500/20">Recommended</span>
                  <span class="text-detail text-slate-500">Claude Sonnet 4.6 &middot; 7 agents &middot; ~$0.50/diagnosis</span>
                </div>
                <div v-else-if="provider === 'openai'" class="flex items-center gap-2">
                  <span class="text-tiny font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/20">Supported</span>
                  <span class="text-detail text-slate-500">GPT-4o &middot; Single model &middot; ~$0.40/diagnosis</span>
                </div>
                <div v-else-if="provider === 'google'" class="flex items-center gap-2">
                  <span class="text-tiny font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-violet-500/15 text-violet-400 border border-violet-500/20">Supported</span>
                  <span class="text-detail text-slate-500">Gemini 2.5 &middot; Multi-agent &middot; ~$0.35/diagnosis</span>
                </div>
                <div v-else class="flex items-center gap-2">
                  <span class="text-tiny font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">Free</span>
                  <span class="text-detail text-slate-500">Local models &middot; No API key needed &middot; Unlimited</span>
                </div>
              </div>

              <!-- Form content area -->
              <div class="space-y-4">
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
                        <div class="text-detail text-slate-500 uppercase font-semibold mb-2">Available Models</div>
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

                <!-- API Key Input (Anthropic/OpenAI/Google) -->
                <template v-else>
                  <div>
                    <label class="text-xs text-slate-400 font-medium mb-1.5 block">
                      {{ provider === 'anthropic' ? 'Anthropic API Key' : provider === 'google' ? 'Google AI API Key' : 'OpenAI API Key' }}
                    </label>
                    <div class="relative">
                      <input
                        v-model="apiKey"
                        :type="showApiKey ? 'text' : 'password'"
                        :placeholder="provider === 'anthropic' ? 'sk-ant-api03-...' : provider === 'google' ? 'AIza...' : 'sk-proj-...'"
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

                <!-- Test API Key button -->
                <button v-if="provider !== 'ollama' && apiKey.trim()"
                  @click="testApiKey"
                  :disabled="isTesting"
                  class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-medium border transition-all"
                  :class="testResult === 'valid'
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    : testResult === 'invalid'
                      ? 'bg-red-500/10 border-red-500/30 text-red-400'
                      : 'bg-slate-800/60 border-slate-700/50 text-slate-300 hover:bg-slate-700/60 hover:border-slate-600'"
                >
                  <svg v-if="isTesting" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                  <svg v-else-if="testResult === 'valid'" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                  <svg v-else-if="testResult === 'invalid'" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                  <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                  {{ isTesting ? 'Testing...' : testResult === 'valid' ? 'Key is valid!' : testResult === 'invalid' ? testMessage : 'Test API Key' }}
                </button>

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
                <div class="flex gap-2">
                  <!-- Save Only (doesn't redirect) -->
                  <button
                    v-if="provider !== 'ollama' && apiKey.trim()"
                    @click="saveKeyOnly"
                    :disabled="isLoading"
                    class="px-4 py-3 rounded-xl text-sm font-medium border transition-all flex items-center gap-1.5"
                    :class="keySaved ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-slate-800 border-slate-700/50 text-slate-300 hover:bg-slate-700 hover:border-slate-600'"
                  >
                    <svg v-if="keySaved" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                    {{ keySaved ? 'Saved!' : 'Save' }}
                  </button>
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
                <p class="text-detail text-slate-600 text-center">{{ provider === 'ollama' ? 'Ollama runs locally — no API key or costs needed.' : 'Skip uses basic mode without AI agents. You can add a key later in Settings.' }}</p>

                <!-- Active API Keys Overview -->
                <div class="mt-2 p-3 rounded-xl bg-slate-800/40 border border-slate-700/30">
                  <div class="text-detail text-slate-500 uppercase font-bold tracking-wider mb-2">Configured Keys</div>
                  <div class="space-y-1.5">
                    <div v-for="k in savedKeys" :key="k.provider" class="flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <div class="w-1.5 h-1.5 rounded-full" :class="k.active ? 'bg-emerald-500' : 'bg-slate-600'"></div>
                        <span class="text-xs font-medium" :class="k.active ? 'text-emerald-400' : 'text-slate-500'">{{ k.label }}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <span class="text-detail font-mono" :class="k.active ? 'text-slate-400' : 'text-slate-600'">{{ k.maskedKey }}</span>
                        <button v-if="k.active" @click="removeKey(k.provider)" class="text-detail text-red-500/60 hover:text-red-400 transition-colors">Remove</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Help link -->
              <div class="text-center space-y-2">
                <button @click="showHelp = !showHelp" class="text-xs text-slate-500 hover:text-slate-300 transition-colors flex items-center gap-1.5 mx-auto">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  {{ showHelp ? 'Hide instructions' : 'How to get an API key?' }}
                </button>
                <div v-if="showHelp" class="bg-slate-800/60 rounded-xl border border-slate-700/40 p-4 text-left">
                  <div v-if="provider === 'anthropic'">
                    <ol class="text-xs text-slate-400 space-y-1.5 list-decimal ml-4">
                      <li>Go to <a href="https://console.anthropic.com/settings/keys" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">console.anthropic.com</a></li>
                      <li>Sign in or create an account</li>
                      <li>Navigate to API Keys</li>
                      <li>Create a new key and paste it above</li>
                    </ol>
                  </div>
                  <div v-else-if="provider === 'google'">
                    <ol class="text-xs text-slate-400 space-y-1.5 list-decimal ml-4">
                      <li>Go to <a href="https://aistudio.google.com/apikey" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">aistudio.google.com/apikey</a></li>
                      <li>Sign in with your Google account</li>
                      <li>Click "Create API key"</li>
                      <li>Copy and paste it above</li>
                    </ol>
                  </div>
                  <div v-else-if="provider === 'openai'">
                    <ol class="text-xs text-slate-400 space-y-1.5 list-decimal ml-4">
                      <li>Go to <a href="https://platform.openai.com/api-keys" target="_blank" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">platform.openai.com/api-keys</a></li>
                      <li>Sign in or create an account</li>
                      <li>Click "Create new secret key"</li>
                      <li>Copy and paste it above</li>
                    </ol>
                  </div>
                  <p class="text-detail text-slate-600 mt-3">Your key is stored locally and never sent to our servers.</p>
                </div>
              </div>

              <!-- Mobile pipeline preview -->
              <div class="lg:hidden bg-slate-800/40 rounded-xl border border-slate-700/40 p-3">
                <div class="text-detail text-slate-500 uppercase tracking-wider font-semibold mb-2">7-Agent Pipeline</div>
                <div class="flex items-center gap-1 overflow-x-auto no-scrollbar">
                  <div v-for="(agent, i) in agents" :key="'m-'+agent.name" class="flex items-center gap-1">
                    <div class="flex items-center gap-1.5 bg-slate-800/70 rounded-lg px-2 py-1.5 flex-shrink-0">
                      <span class="text-xs">{{ agent.icon }}</span>
                      <span class="text-detail font-medium text-slate-300">{{ agent.name }}</span>
                    </div>
                    <svg v-if="i < agents.length - 1" class="w-2.5 h-2.5 text-slate-700 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE_URL } from '@/services/api.js'

// Map provider id to its localStorage key name
const providerStorageKeys = {
  anthropic: 'anthropic_api_key',
  openai: 'openai_api_key',
  google: 'google_api_key',
}

function getKeyForProvider(providerId) {
  const storageKey = providerStorageKeys[providerId]
  return storageKey ? (localStorage.getItem(storageKey) || '') : ''
}

export default {
  name: 'ApiKeySetup',
  setup() {
    const router = useRouter()
    const provider = ref(localStorage.getItem('ai_provider') || 'anthropic')
    const apiKey = ref(getKeyForProvider(provider.value))
    const showApiKey = ref(false)
    const showHelp = ref(false)
    const isLoading = ref(false)
    const error = ref('')
    const success = ref('')
    const isTesting = ref(false)
    const testResult = ref('') // '', 'valid', 'invalid'
    const testMessage = ref('')

    const testApiKey = async () => {
      if (!apiKey.value.trim()) return

      // Validate format before hitting the backend
      const formatErr = validateApiKey(apiKey.value)
      if (formatErr) {
        testResult.value = 'invalid'
        testMessage.value = formatErr
        setTimeout(() => { if (testResult.value) testResult.value = '' }, 8000)
        return
      }

      isTesting.value = true
      testResult.value = ''
      testMessage.value = ''
      error.value = ''

      try {
        const headers = { 'Content-Type': 'application/json' }
        if (provider.value === 'anthropic') {
          headers['X-Anthropic-API-Key'] = apiKey.value.trim()
        } else if (provider.value === 'google') {
          headers['X-Google-API-Key'] = apiKey.value.trim()
        } else {
          headers['X-OpenAI-API-Key'] = apiKey.value.trim()
        }

        const resp = await fetch(`${API_BASE_URL}/api/validate-key`, {
          method: 'POST',
          headers,
        })
        const data = await resp.json()
        const vendorResult = data.results?.[provider.value]

        if (vendorResult && vendorResult.valid) {
          testResult.value = 'valid'
          testMessage.value = vendorResult.message || 'Key is valid'
        } else {
          testResult.value = 'invalid'
          testMessage.value = vendorResult?.message || 'Key validation failed'
        }
      } catch (e) {
        testResult.value = 'invalid'
        testMessage.value = 'Could not reach server to validate'
      } finally {
        isTesting.value = false
        // Reset after 8 seconds
        setTimeout(() => { if (testResult.value) testResult.value = '' }, 8000)
      }
    }

    // When provider tab changes, load the correct saved key for that provider
    watch(provider, (newProvider) => {
      apiKey.value = getKeyForProvider(newProvider)
      testResult.value = ''
      testMessage.value = ''
      error.value = ''
      success.value = ''
    })

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
        const resp = await fetch(`${API_BASE_URL}/health`)
        if (!resp.ok) throw new Error(`Health check returned ${resp.status}`)
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
      if (provider.value === 'google' && !key.startsWith('AIza'))
        return 'Google AI keys start with "AIza"'
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

        const storageKey = providerStorageKeys[provider.value]
        if (storageKey) localStorage.setItem(storageKey, key)

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

    const keySaved = ref(false)

    // Save key without redirecting
    const saveKeyOnly = () => {
      const storageKey = providerStorageKeys[provider.value]
      if (storageKey && apiKey.value.trim()) {
        localStorage.setItem(storageKey, apiKey.value.trim())
        localStorage.setItem('ai_provider', provider.value)
        localStorage.setItem('api_key_configured', 'true')
        keySaved.value = true
        success.value = `${provider.value.charAt(0).toUpperCase() + provider.value.slice(1)} key saved!`
        setTimeout(() => { keySaved.value = false; success.value = '' }, 2000)
      }
    }

    // Overview of all saved keys
    const savedKeys = ref([])
    const refreshSavedKeys = () => {
      const keys = [
        { provider: 'anthropic', label: 'Anthropic', storageKey: 'anthropic_api_key' },
        { provider: 'openai', label: 'OpenAI', storageKey: 'openai_api_key' },
        { provider: 'google', label: 'Google', storageKey: 'google_api_key' },
        { provider: 'ollama', label: 'Ollama (Local)', storageKey: null },
      ]
      savedKeys.value = keys.map(k => {
        if (k.provider === 'ollama') {
          return { ...k, active: ollamaAvailable.value, maskedKey: ollamaAvailable.value ? 'localhost:11434' : 'Not running' }
        }
        const raw = k.storageKey ? localStorage.getItem(k.storageKey) : null
        return {
          ...k,
          active: !!raw,
          maskedKey: raw ? raw.slice(0, 7) + '...' + raw.slice(-4) : 'Not set'
        }
      })
    }
    refreshSavedKeys()

    // Re-check saved keys when provider/key changes
    watch([provider, apiKey], () => refreshSavedKeys())

    const removeKey = (providerId) => {
      const storageKey = providerStorageKeys[providerId]
      if (storageKey) {
        localStorage.removeItem(storageKey)
        if (provider.value === providerId) apiKey.value = ''
        refreshSavedKeys()
      }
    }

    return { provider, apiKey, showApiKey, showHelp, isLoading, error, success, agents, saveAndContinue, skipSetup, ollamaChecking, ollamaAvailable, ollamaModels, checkOllama, isTesting, testResult, testMessage, testApiKey, keySaved, saveKeyOnly, savedKeys, removeKey }
  }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

/* Modal entrance animation */
.modal-enter-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.modal-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.modal-enter-from {
  opacity: 0;
  transform: scale(0.95);
}
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Backdrop animation */
.modal-backdrop-enter-active {
  transition: opacity 0.3s ease;
}
.modal-backdrop-leave-active {
  transition: opacity 0.2s ease;
}
.modal-backdrop-enter-from,
.modal-backdrop-leave-to {
  opacity: 0;
}

/* Smooth scrollbar for right panel */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgb(51 65 85 / 0.5);
  border-radius: 3px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background-color: rgb(71 85 105 / 0.7);
}
</style>
