<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-purple-600/5' : 'bg-purple-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b backdrop-blur-xl"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-4">
        <button @click="goBack" class="p-1.5 rounded-lg transition-colors"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <h1 class="text-lg font-bold text-[var(--text-primary)]">Settings</h1>
      </div>
      <ThemeLangControls />
    </nav>

    <!-- Main content -->
    <div class="relative z-10 flex justify-center px-4 py-8">
      <div class="max-w-2xl w-full space-y-6">

        <!-- Profile Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Profile
            </h2>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-[var(--text-primary)]">
                  {{ profile.name || 'No name set' }}
                </p>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                  {{ profile.email || 'No email set' }}
                </p>
              </div>
              <router-link to="/profile"
                class="px-4 py-2 text-xs font-medium rounded-lg transition-colors"
                :class="isDark
                  ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'">
                Edit Profile
              </router-link>
            </div>
          </div>
        </section>

        <!-- Appearance Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
              </svg>
              Appearance
            </h2>
          </div>
          <div class="p-6 space-y-5">
            <!-- Theme -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Theme</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Switch between light and dark mode</p>
              </div>
              <button @click="toggleTheme"
                class="relative w-14 h-7 rounded-full transition-colors duration-200"
                :class="isDark ? 'bg-blue-600' : 'bg-slate-300'">
                <span class="absolute top-0.5 left-0.5 w-6 h-6 bg-white rounded-full shadow transition-transform duration-200"
                  :class="isDark ? 'translate-x-7' : 'translate-x-0'"></span>
              </button>
            </div>
            <!-- Language -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Language</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ currentLanguage.name }}</p>
              </div>
              <select @change="setLang($event.target.value)" :value="lang"
                class="rounded-lg px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                :class="isDark
                  ? 'bg-slate-800 border border-slate-700 text-white'
                  : 'bg-slate-50 border border-slate-200 text-slate-900'">
                <option v-for="l in languages" :key="l.code" :value="l.code">{{ l.flag }} {{ l.name }}</option>
              </select>
            </div>
          </div>
        </section>

        <!-- Voice & Audio Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              </svg>
              Voice & Audio
            </h2>
          </div>
          <div class="p-6 space-y-5">
            <!-- Voice Input -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Voice Input</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Enable microphone for voice recording</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.voiceInput" @change="saveSetting('voiceInput', settings.voiceInput)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <!-- Audio Responses -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Audio Responses</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Play AI responses as audio</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.audioResponses" @change="saveSetting('audioResponses', settings.audioResponses)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <!-- Speech Rate -->
            <div v-if="settings.audioResponses">
              <label class="text-sm font-medium block mb-2 text-[var(--text-primary)]">Speech Rate</label>
              <div class="flex items-center gap-4">
                <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Slow</span>
                <input
                  type="range"
                  v-model.number="settings.speechRate"
                  @input="saveSetting('speechRate', settings.speechRate)"
                  min="0.7" max="1.3" step="0.05"
                  class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"
                />
                <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Fast</span>
              </div>
              <p class="text-xs mt-1" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Current: {{ settings.speechRate.toFixed(2) }}x</p>
            </div>
          </div>
        </section>

        <!-- Interface Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              Interface
            </h2>
          </div>
          <div class="p-6 space-y-5">
            <!-- Auto-scroll -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Auto-scroll Chat</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Automatically scroll to new messages</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.autoScroll" @change="saveSetting('autoScroll', settings.autoScroll)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <!-- Sound Effects -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-[var(--text-primary)]">Sound Effects</label>
                <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Play sounds for notifications</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.soundEffects" @change="saveSetting('soundEffects', settings.soundEffects)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
          </div>
        </section>

        <!-- API Keys Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
              API Keys
            </h2>
          </div>
          <div class="p-6 space-y-5">
            <!-- Provider tabs -->
            <div>
              <label class="text-xs font-medium mb-2 block text-[var(--text-secondary)]">API Keys (add keys for the vendors you want to use)</label>
              <div class="flex gap-2">
                <button v-for="p in providers" :key="p.id" @click="apiProvider = p.id; loadProviderKey()"
                  class="flex-1 py-2 text-xs font-medium rounded-lg border transition-colors text-center"
                  :class="apiProvider === p.id
                    ? (isDark ? 'bg-blue-500/15 border-blue-500/30 text-blue-400' : 'bg-blue-50 border-blue-300 text-blue-600')
                    : (isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-200 text-slate-500 hover:border-slate-300')">
                  {{ p.name }}
                  <span v-if="hasKey(p.id)" class="ml-1 text-emerald-400">&#10003;</span>
                </button>
              </div>
            </div>
            <!-- Ollama status (no key needed) -->
            <div v-if="apiProvider === 'ollama'" class="space-y-3">
              <div v-if="ollamaChecking" class="flex items-center gap-2 py-3">
                <svg class="w-4 h-4 animate-spin text-orange-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <span class="text-xs text-[var(--text-secondary)]">Detecting Ollama...</span>
              </div>
              <div v-else-if="ollamaAvailable" class="space-y-3">
                <div class="flex items-center gap-2 py-1">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
                  <span class="text-sm font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Ollama is running</span>
                </div>
                <div class="p-3 rounded-xl border" :class="isDark ? 'bg-slate-800/60 border-slate-700/30' : 'bg-slate-50 border-slate-200'">
                  <div class="text-detail uppercase font-semibold mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Installed Models</div>
                  <div v-for="model in ollamaModels" :key="model" class="flex items-center gap-2 py-1 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <svg class="w-3.5 h-3.5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    {{ model }}
                  </div>
                </div>
                <div class="p-3 rounded-lg" :class="isDark ? 'bg-emerald-500/10 border border-emerald-500/15' : 'bg-emerald-50 border border-emerald-200'">
                  <p class="text-xs" :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">No API key needed. Runs 100% locally, free and unlimited.</p>
                </div>
                <button @click="activateOllama" class="px-5 py-2.5 bg-orange-600 hover:bg-orange-500 text-white font-medium rounded-xl text-sm transition-all">
                  Use Ollama
                </button>
              </div>
              <div v-else class="space-y-3 py-2">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                  <span class="text-sm font-medium" :class="isDark ? 'text-red-400' : 'text-red-500'">Ollama not detected</span>
                </div>
                <p class="text-xs text-[var(--text-secondary)]">Install Ollama from ollama.com, run it, then pull a model with: <code class="px-1.5 py-0.5 rounded text-orange-400" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">ollama pull llama3.1:8b</code></p>
                <button @click="checkOllamaStatus" class="text-xs text-orange-400 hover:text-orange-300 underline underline-offset-2">Retry Detection</button>
              </div>
            </div>

            <!-- API Key Input (non-Ollama providers) -->
            <div v-else>
              <label class="text-xs font-medium mb-1.5 block text-[var(--text-secondary)]">
                {{ currentProviderLabel }} API Key
              </label>
              <div class="relative">
                <input
                  v-model="apiKey"
                  :type="showApiKey ? 'text' : 'password'"
                  :placeholder="apiProvider === 'anthropic' ? 'sk-ant-api03-...' : 'sk-proj-...'"
                  class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all pr-10"
                  :class="isDark
                    ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                    : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                />
                <button @click="showApiKey = !showApiKey"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">
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
            <!-- Save Key -->
            <div v-if="apiProvider !== 'ollama'" class="flex items-center gap-3">
              <button @click="saveApiKeyFn"
                :disabled="!apiKey.trim()"
                class="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed text-white font-medium rounded-xl text-sm transition-all">
                Save Key
              </button>
              <span v-if="apiKeySaved" class="text-xs text-emerald-400">Saved!</span>
            </div>

            <!-- Validate All Keys -->
            <div v-if="apiProvider !== 'ollama'" class="pt-3 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
              <button @click="validateKeys" :disabled="isValidating"
                class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-colors"
                :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                <svg v-if="isValidating" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                {{ isValidating ? 'Validating...' : 'Validate All API Keys' }}
              </button>
              <!-- Validation results -->
              <div v-if="validationResults" class="mt-3 space-y-2">
                <div v-for="(result, vendor) in validationResults.results" :key="vendor"
                  class="flex items-center justify-between px-3 py-2 rounded-lg text-xs"
                  :class="result.valid
                    ? (isDark ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-emerald-50 border border-emerald-200')
                    : (result.message === 'No key provided'
                      ? (isDark ? 'bg-slate-800/50 border border-slate-700/30' : 'bg-slate-50 border border-slate-200')
                      : (isDark ? 'bg-red-500/10 border border-red-500/20' : 'bg-red-50 border border-red-200'))">
                  <div class="flex items-center gap-2">
                    <span v-if="result.valid" class="text-emerald-400 text-sm">&#10003;</span>
                    <span v-else-if="result.message === 'No key provided'" class="text-slate-500 text-sm">&#8212;</span>
                    <span v-else class="text-red-400 text-sm">&#10007;</span>
                    <span class="capitalize font-medium text-[var(--text-primary)]">{{ vendor }}</span>
                  </div>
                  <span :class="result.valid ? 'text-emerald-400' : (result.message === 'No key provided' ? (isDark ? 'text-slate-500' : 'text-slate-400') : 'text-red-400')">
                    {{ result.message }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- AI Model Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-[var(--text-primary)]">
              <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              AI Model
            </h2>
          </div>
          <div class="p-6 space-y-3">
            <p class="text-xs mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Choose which AI model powers your diagnosis. Higher-tier models provide more thorough analysis but may be slower.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <label v-for="m in modelOptions" :key="m.id"
                class="flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition-all"
                :class="modelPreference === m.id
                  ? (isDark ? 'bg-blue-500/10 border-blue-500/30' : 'bg-blue-50 border-blue-300')
                  : (isDark ? 'border-slate-700 hover:border-slate-600' : 'border-slate-200 hover:border-slate-300')">
                <input type="radio" :value="m.id" v-model="modelPreference" @change="saveModelPreference" class="mt-1 text-blue-600">
                <div>
                  <div class="text-sm font-medium text-[var(--text-primary)]">{{ m.name }}</div>
                  <div class="text-detail mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ m.desc }}</div>
                  <span v-if="m.badge" class="inline-block mt-1 text-tiny px-1.5 py-0.5 rounded-full" :class="m.badgeClass">{{ m.badge }}</span>
                </div>
              </label>
            </div>
          </div>
        </section>

        <!-- Data & Privacy Section -->
        <section class="backdrop-blur-xl rounded-2xl border shadow-lg overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-red-900/30' : 'bg-white/80 border-red-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-red-900/30' : 'border-red-200'">
            <h2 class="text-sm font-semibold flex items-center gap-2 text-red-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
              Data & Privacy
            </h2>
          </div>
          <div class="p-6 space-y-4">
            <p class="text-xs mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              All data is stored locally on your device. Nothing is sent to external servers.
            </p>
            <!-- Export Data -->
            <button @click="handleExportData"
              class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-colors"
              :class="isDark
                ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Export All Data as JSON
            </button>
            <!-- Clear History -->
            <button @click="handleClearHistory"
              class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-colors border"
              :class="isDark
                ? 'border-red-800/50 text-red-400 hover:bg-red-500/10'
                : 'border-red-200 text-red-500 hover:bg-red-50'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              Clear Consultation History
            </button>
            <!-- Clear All Data -->
            <button @click="handleClearAll"
              class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium bg-red-600 hover:bg-red-700 text-white transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
              Clear All Data
            </button>
          </div>
        </section>

        <!-- Spacer at bottom -->
        <div class="h-8"></div>
      </div>
    </div>

    <!-- Confirm Dialog -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="confirmDialog.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
        <div class="rounded-2xl border shadow-2xl max-w-sm w-full p-6"
          :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
          <p class="text-sm mb-5 text-[var(--text-primary)]">{{ confirmDialog.message }}</p>
          <div class="flex gap-3 justify-end">
            <button @click="confirmDialog.show = false"
              class="px-4 py-2 text-xs rounded-lg transition-colors"
              :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
              Cancel
            </button>
            <button @click="confirmDialog.action(); confirmDialog.show = false"
              class="px-4 py-2 text-xs text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors">
              Confirm
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { getProfile, getPreferences, savePreference, exportAllData, clearUserData } from '@/services/userService.js'
import { clearHistory as clearHistoryFn } from '@/services/historyService.js'
import { validateApiKeys, API_BASE_URL } from '@/services/api.js'

const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const { lang, currentLanguage, setLang, languages } = useI18n()

const profile = ref({})
const apiProvider = ref('anthropic')
const apiKey = ref('')
const showApiKey = ref(false)
const apiKeySaved = ref(false)

const providers = [
  { id: 'anthropic', name: 'Anthropic', keyPrefix: 'sk-ant-', storageKey: 'anthropic_api_key' },
  { id: 'openai', name: 'OpenAI', keyPrefix: 'sk-', storageKey: 'openai_api_key' },
  { id: 'google', name: 'Google', keyPrefix: 'AIza', storageKey: 'google_api_key' },
  { id: 'ollama', name: 'Ollama (Free)', keyPrefix: '', storageKey: '' },
]

// Ollama detection
const ollamaChecking = ref(false)
const ollamaAvailable = ref(false)
const ollamaModels = ref([])

async function checkOllamaStatus() {
  ollamaChecking.value = true
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

function activateOllama() {
  localStorage.setItem('ai_provider', 'ollama')
  localStorage.removeItem('anthropic_api_key')
  localStorage.removeItem('openai_api_key')
  localStorage.removeItem('google_api_key')
  localStorage.setItem('api_key_configured', 'true')
  localStorage.setItem('model_preference', 'llama3.1:8b')
  modelPreference.value = 'llama3.1:8b'
  apiKeySaved.value = true
  setTimeout(() => { apiKeySaved.value = false }, 2000)
}

const currentProviderLabel = computed(() => {
  const p = providers.find(p => p.id === apiProvider.value)
  return p ? p.name : 'API'
})

function hasKey(providerId) {
  const p = providers.find(p => p.id === providerId)
  return p && !!localStorage.getItem(p.storageKey)
}

function loadProviderKey() {
  if (apiProvider.value === 'ollama') {
    checkOllamaStatus()
    return
  }
  const p = providers.find(p => p.id === apiProvider.value)
  apiKey.value = p ? (localStorage.getItem(p.storageKey) || '') : ''
  apiKeySaved.value = false
}

// Model preference
const modelPreference = ref(localStorage.getItem('model_preference') || 'auto')
const modelOptions = [
  // Auto
  { id: 'auto', name: 'Auto (Recommended)', desc: 'Opus for diagnostician, Sonnet for other agents. Best balance of quality and speed.', badge: 'default', badgeClass: 'bg-blue-500/20 text-blue-400' },
  // Anthropic
  { id: 'opus', name: 'Claude Opus 4.6', desc: 'Highest quality. Most thorough clinical reasoning across all 7 agents.', badge: 'best quality', badgeClass: 'bg-purple-500/20 text-purple-400' },
  { id: 'sonnet', name: 'Claude Sonnet 4.6', desc: 'Fast and capable. Good quality for most cases.', badge: 'fast', badgeClass: 'bg-emerald-500/20 text-emerald-400' },
  { id: 'haiku', name: 'Claude Haiku 4.5', desc: 'Fastest Anthropic model. Good for simple symptom checks.', badge: 'budget', badgeClass: 'bg-amber-500/20 text-amber-400' },
  // OpenAI
  { id: 'gpt-4o', name: 'GPT-4o', desc: 'OpenAI flagship. Strong general reasoning. Requires OpenAI API key.', badge: 'OpenAI', badgeClass: 'bg-green-500/20 text-green-400' },
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', desc: 'Faster OpenAI model. Lower cost, good for routine cases.', badge: 'OpenAI', badgeClass: 'bg-green-500/20 text-green-400' },
  { id: 'o3', name: 'OpenAI o3', desc: 'Advanced reasoning model. Excellent for complex differential diagnosis.', badge: 'OpenAI', badgeClass: 'bg-green-500/20 text-green-400' },
  // Google
  { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', desc: 'Google flagship. Strong medical knowledge. Requires Google API key.', badge: 'Google', badgeClass: 'bg-sky-500/20 text-sky-400' },
  { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', desc: 'Fast Google model. Good balance of speed and quality.', badge: 'Google', badgeClass: 'bg-sky-500/20 text-sky-400' },
  // Ollama (local)
  { id: 'llama3.1:8b', name: 'Llama 3.1 8B (Ollama)', desc: 'Runs locally on your machine. Free, no API key needed. Good for development.', badge: 'free', badgeClass: 'bg-orange-500/20 text-orange-400' },
  { id: 'qwen2.5:7b', name: 'Qwen 2.5 7B (Ollama)', desc: 'Local model with strong multilingual support. Free, no API key.', badge: 'free', badgeClass: 'bg-orange-500/20 text-orange-400' },
  { id: 'gemma2:2b', name: 'Gemma 2 2B (Ollama)', desc: 'Smallest and fastest local model. Good for quick tests.', badge: 'fast + free', badgeClass: 'bg-orange-500/20 text-orange-400' },
]

function saveModelPreference() {
  localStorage.setItem('model_preference', modelPreference.value)
}

// Key validation
const isValidating = ref(false)
const validationResults = ref(null)

async function validateKeys() {
  isValidating.value = true
  validationResults.value = null
  try {
    validationResults.value = await validateApiKeys()
  } catch (e) {
    validationResults.value = {
      results: {
        anthropic: { valid: false, message: 'Backend unreachable' },
        openai: { valid: false, message: 'Backend unreachable' },
        google: { valid: false, message: 'Backend unreachable' },
      },
      any_valid: false
    }
  } finally {
    isValidating.value = false
  }
}

const settings = reactive({
  voiceInput: true,
  audioResponses: false,
  speechRate: 0.95,
  autoScroll: true,
  soundEffects: true,
})

const confirmDialog = reactive({
  show: false,
  message: '',
  action: () => {},
})

onMounted(() => {
  profile.value = getProfile()
  const prefs = getPreferences()
  settings.voiceInput = prefs.voiceInput ?? true
  settings.audioResponses = prefs.audioResponses ?? false
  settings.speechRate = prefs.speechRate ?? 0.95
  settings.autoScroll = prefs.autoScroll ?? true
  settings.soundEffects = prefs.soundEffects ?? true

  // Load existing API key for current provider
  loadProviderKey()
})

function saveSetting(key, value) {
  savePreference(key, value)
}

function saveApiKeyFn() {
  const key = apiKey.value.trim()
  if (!key) return

  // Clear ALL vendor keys first, then set only the active one
  localStorage.removeItem('anthropic_api_key')
  localStorage.removeItem('openai_api_key')
  localStorage.removeItem('google_api_key')

  const p = providers.find(p => p.id === apiProvider.value)
  if (p) {
    localStorage.setItem(p.storageKey, key)
  }
  localStorage.setItem('ai_provider', apiProvider.value)
  localStorage.setItem('api_key_configured', 'true')
  apiKeySaved.value = true
  setTimeout(() => { apiKeySaved.value = false }, 2000)
}

function handleExportData() {
  const data = exportAllData()
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `medical-ai-data-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}

function handleClearHistory() {
  confirmDialog.message = 'Are you sure you want to clear all consultation history? This cannot be undone.'
  confirmDialog.action = () => { clearHistoryFn() }
  confirmDialog.show = true
}

function handleClearAll() {
  confirmDialog.message = 'Are you sure you want to clear ALL data including your profile, preferences, API keys, and consultation history? This cannot be undone.'
  confirmDialog.action = () => {
    clearUserData()
    clearHistoryFn()
    localStorage.removeItem('anthropic_api_key')
    localStorage.removeItem('openai_api_key')
    localStorage.removeItem('google_api_key')
    localStorage.removeItem('ai_provider')
    localStorage.removeItem('api_key_configured')
    profile.value = {}
    apiKey.value = ''
  }
  confirmDialog.show = true
}

function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 18px;
  width: 18px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.slider::-webkit-slider-track {
  height: 8px;
  -webkit-appearance: none;
  border-radius: 4px;
}
.slider::-moz-range-thumb {
  height: 18px;
  width: 18px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.slider::-moz-range-track {
  height: 8px;
  border-radius: 4px;
  border: none;
}
</style>
