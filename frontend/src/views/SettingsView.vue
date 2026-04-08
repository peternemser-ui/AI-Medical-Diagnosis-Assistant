<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <AppNav currentPage="settings" />

    <!-- Main content -->
    <div class="flex justify-center px-4 py-8">
      <div class="max-w-2xl w-full space-y-5">

        <!-- Page header -->
        <div class="pt-2 pb-1">
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Settings</h1>
          <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Manage your account, preferences, and API keys</p>
        </div>

        <!-- ── Profile Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-indigo-500/15' : 'bg-indigo-50'">
              <svg class="w-3.5 h-3.5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Profile</h2>
          </div>
          <div class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-sm font-bold text-white flex-shrink-0">
                  {{ profile.name ? profile.name.trim().split(/\s+/).map(w => w[0]).join('').toUpperCase().slice(0,2) : '?' }}
                </div>
                <div>
                  <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ profile.name || 'No name set' }}</p>
                  <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ profile.email || 'No email set' }}</p>
                </div>
              </div>
              <router-link to="/profile"
                class="px-4 py-2 text-sm font-medium rounded-lg border transition-colors"
                :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white' : 'border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
                Edit Profile
              </router-link>
            </div>
          </div>
        </section>

        <!-- ── Appearance Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-purple-500/15' : 'bg-purple-50'">
              <svg class="w-3.5 h-3.5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Appearance</h2>
          </div>
          <div class="px-6 py-5 space-y-5">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Theme</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ isDark ? 'Dark mode enabled' : 'Light mode enabled' }}</p>
              </div>
              <button @click="toggleTheme"
                class="relative w-12 h-6 rounded-full transition-colors duration-200"
                :class="isDark ? 'bg-indigo-600' : 'bg-slate-300'">
                <span class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-200"
                  :class="isDark ? 'translate-x-6' : 'translate-x-0'"></span>
              </button>
            </div>
            <div class="h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'"></div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Language</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ currentLanguage.name }}</p>
              </div>
              <select @change="setLang($event.target.value)" :value="lang"
                class="rounded-lg px-3 py-1.5 text-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'">
                <option v-for="l in languages" :key="l.code" :value="l.code">{{ l.flag }} {{ l.name }}</option>
              </select>
            </div>
          </div>
        </section>

        <!-- ── Voice & Audio Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-blue-500/15' : 'bg-blue-50'">
              <svg class="w-3.5 h-3.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Voice & Audio</h2>
          </div>
          <div class="px-6 py-5 space-y-5">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Voice Input</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Enable microphone for voice recording</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.voiceInput" @change="saveSetting('voiceInput', settings.voiceInput)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <div class="h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'"></div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Audio Responses</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Play AI responses as audio</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.audioResponses" @change="saveSetting('audioResponses', settings.audioResponses)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <div v-if="settings.audioResponses">
              <div class="h-px mb-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'"></div>
              <p class="text-sm font-medium mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Speech Rate</p>
              <div class="flex items-center gap-4">
                <span class="text-xs w-8" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Slow</span>
                <input type="range" v-model.number="settings.speechRate" @input="saveSetting('speechRate', settings.speechRate)"
                  min="0.7" max="1.3" step="0.05"
                  class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-200'" />
                <span class="text-xs w-8 text-right" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Fast</span>
              </div>
              <p class="text-xs mt-2" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Rate: {{ settings.speechRate.toFixed(2) }}x</p>
            </div>
          </div>
        </section>

        <!-- ── Interface Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-emerald-500/15' : 'bg-emerald-50'">
              <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Interface</h2>
          </div>
          <div class="px-6 py-5 space-y-5">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Auto-scroll Chat</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Automatically scroll to new messages</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.autoScroll" @change="saveSetting('autoScroll', settings.autoScroll)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
            <div class="h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'"></div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">Sound Effects</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Play sounds for notifications</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="settings.soundEffects" @change="saveSetting('soundEffects', settings.soundEffects)" class="sr-only peer">
                <div class="w-11 h-6 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
              </label>
            </div>
          </div>
        </section>

        <!-- ── API Configuration Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-amber-500/15' : 'bg-amber-50'">
              <svg class="w-3.5 h-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">API Configuration</h2>
          </div>
          <div class="px-6 py-5 space-y-4">
            <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Add keys for the AI providers you want to use.</p>
            <!-- Provider tabs -->
            <div class="flex gap-2">
              <button v-for="p in providers" :key="p.id" @click="apiProvider = p.id; loadProviderKey()"
                class="flex-1 py-2 text-xs font-medium rounded-lg border transition-colors text-center"
                :class="apiProvider === p.id
                  ? (isDark ? 'bg-indigo-500/15 border-indigo-500/40 text-indigo-400' : 'bg-indigo-50 border-indigo-300 text-indigo-700')
                  : (isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-200 text-slate-500 hover:border-slate-300')">
                {{ p.name }}
                <span v-if="hasKey(p.id)" class="ml-1 text-emerald-400">&#10003;</span>
              </button>
            </div>

            <!-- Ollama status -->
            <div v-if="apiProvider === 'ollama'" class="space-y-3">
              <div v-if="ollamaChecking" class="flex items-center gap-2 py-3">
                <svg class="w-4 h-4 animate-spin text-orange-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <span class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Detecting Ollama...</span>
              </div>
              <div v-else-if="ollamaAvailable" class="space-y-3">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
                  <span class="text-sm font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Ollama is running</span>
                </div>
                <div class="p-3 rounded-lg border" :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <div class="text-xs uppercase font-semibold mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Installed Models</div>
                  <div v-for="model in ollamaModels" :key="model" class="flex items-center gap-2 py-1 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <svg class="w-3.5 h-3.5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    {{ model }}
                  </div>
                </div>
                <div class="p-3 rounded-lg" :class="isDark ? 'bg-emerald-500/10 border border-emerald-500/15' : 'bg-emerald-50 border border-emerald-200'">
                  <p class="text-xs" :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">No API key needed. Runs 100% locally, free and unlimited.</p>
                </div>
                <button @click="activateOllama" class="px-5 py-2.5 bg-orange-600 hover:bg-orange-500 text-white font-medium rounded-lg text-sm transition-all">
                  Use Ollama
                </button>
              </div>
              <div v-else class="space-y-3 py-2">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                  <span class="text-sm font-medium" :class="isDark ? 'text-red-400' : 'text-red-500'">Ollama not detected</span>
                </div>
                <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Install from ollama.com, then run: <code class="px-1.5 py-0.5 rounded text-orange-400" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">ollama pull llama3.1:8b</code></p>
                <button @click="checkOllamaStatus" class="text-xs text-orange-400 hover:text-orange-300 underline underline-offset-2">Retry Detection</button>
              </div>
            </div>

            <!-- API Key Input -->
            <div v-else>
              <label class="text-sm font-medium mb-1.5 block" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                {{ currentProviderLabel }} API Key
              </label>
              <div class="relative">
                <input v-model="apiKey" :type="showApiKey ? 'text' : 'password'"
                  :placeholder="apiProvider === 'anthropic' ? 'sk-ant-api03-...' : 'sk-proj-...'"
                  class="w-full rounded-lg px-3.5 py-2.5 text-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all pr-10"
                  :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'" />
                <button @click="showApiKey = !showApiKey"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">
                  <svg v-if="showApiKey" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/></svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.543 7-1.275 4.057-5.065 7-9.543 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                </button>
              </div>
            </div>

            <!-- Save Key -->
            <div v-if="apiProvider !== 'ollama'" class="flex items-center gap-3">
              <button @click="saveApiKeyFn" :disabled="!apiKey.trim()"
                class="px-5 py-2.5 bg-indigo-700 hover:bg-indigo-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg text-sm transition-all">
                Save Key
              </button>
              <span v-if="apiKeySaved" class="text-xs text-emerald-400 font-medium">Saved!</span>
            </div>

            <!-- Validate All Keys -->
            <div v-if="apiProvider !== 'ollama'" class="pt-3 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
              <button @click="validateKeys" :disabled="isValidating"
                class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-colors border"
                :class="isDark ? 'border-slate-700 bg-slate-800/50 text-slate-300 hover:bg-slate-700' : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'">
                <svg v-if="isValidating" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                {{ isValidating ? 'Validating...' : 'Validate All API Keys' }}
              </button>
              <div v-if="validationResults" class="mt-3 space-y-2">
                <div v-for="(result, vendor) in validationResults.results" :key="vendor"
                  class="flex items-center justify-between px-3 py-2 rounded-lg text-xs"
                  :class="result.valid
                    ? (isDark ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-emerald-50 border border-emerald-200')
                    : (result.message === 'No key provided'
                      ? (isDark ? 'bg-slate-800/50 border border-slate-700/30' : 'bg-slate-50 border border-slate-200')
                      : (isDark ? 'bg-red-500/10 border border-red-500/20' : 'bg-red-50 border border-red-200'))">
                  <div class="flex items-center gap-2">
                    <span v-if="result.valid" class="text-emerald-400">&#10003;</span>
                    <span v-else-if="result.message === 'No key provided'" class="text-slate-500">&#8212;</span>
                    <span v-else class="text-red-400">&#10007;</span>
                    <span class="capitalize font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ vendor }}</span>
                  </div>
                  <span :class="result.valid ? 'text-emerald-400' : (result.message === 'No key provided' ? (isDark ? 'text-slate-500' : 'text-slate-400') : 'text-red-400')">{{ result.message }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- ── AI Model Selection Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-cyan-500/15' : 'bg-cyan-50'">
              <svg class="w-3.5 h-3.5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            </div>
            <div>
              <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">AI Model</h2>
            </div>
          </div>
          <div class="px-6 py-5">
            <p class="text-sm mb-4" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              Choose which AI model powers your diagnosis. Higher-tier models provide more thorough analysis.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <label v-for="m in modelOptions" :key="m.id"
                class="flex items-start gap-3 p-4 rounded-xl border cursor-pointer transition-all"
                :class="modelPreference === m.id
                  ? (isDark ? 'bg-indigo-500/10 border-indigo-500/40 ring-1 ring-indigo-500/30' : 'bg-indigo-50 border-indigo-300 ring-1 ring-indigo-200')
                  : (isDark ? 'border-slate-700 hover:border-slate-600 hover:bg-slate-800/40' : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50')">
                <input type="radio" :value="m.id" v-model="modelPreference" @change="saveModelPreference" class="mt-1 text-indigo-600">
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ m.name }}</div>
                  <div class="text-xs mt-0.5 leading-relaxed" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ m.desc }}</div>
                  <div class="flex items-center gap-2 mt-2 flex-wrap">
                    <span v-if="m.badge" class="text-xs px-2 py-0.5 rounded-full font-medium" :class="m.badgeClass">{{ m.badge }}</span>
                    <span class="text-xs font-mono px-2 py-0.5 rounded-full" :class="m.free ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-600')">
                      {{ m.free ? 'Free — local' : m.price + ' / diagnosis' }}
                    </span>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </section>

        <!-- ── App Usage Analytics Section ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b flex items-center gap-2.5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-teal-500/15' : 'bg-teal-50'">
              <svg class="w-3.5 h-3.5 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">App Usage</h2>
          </div>
          <div class="px-6 py-5 space-y-4">
            <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              Local usage statistics — stored only on this device, never shared.
            </p>
            <div class="grid grid-cols-2 gap-3">
              <div class="rounded-xl p-4 text-center"
                :class="isDark ? 'bg-slate-800 border border-slate-700' : 'bg-slate-50 border border-slate-200'">
                <div class="text-2xl font-bold tabular-nums text-teal-500">{{ analyticsSummary.totalPageViews }}</div>
                <div class="text-xs mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Page Views</div>
              </div>
              <div class="rounded-xl p-4 text-center"
                :class="isDark ? 'bg-slate-800 border border-slate-700' : 'bg-slate-50 border border-slate-200'">
                <div class="text-2xl font-bold tabular-nums text-indigo-500">{{ analyticsSummary.totalEvents }}</div>
                <div class="text-xs mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Features Used</div>
              </div>
            </div>
            <div v-if="analyticsSummary.topPages.length > 0">
              <div class="text-xs font-semibold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Most Visited</div>
              <div class="space-y-1.5">
                <div v-for="page in analyticsSummary.topPages" :key="page.path"
                  class="flex items-center justify-between px-3 py-2 rounded-lg text-sm"
                  :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                  <span class="font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ page.name }}</span>
                  <span class="tabular-nums text-xs px-2 py-0.5 rounded-full font-semibold"
                    :class="isDark ? 'bg-teal-500/15 text-teal-400' : 'bg-teal-50 text-teal-700'">
                    {{ page.count }}x
                  </span>
                </div>
              </div>
            </div>
            <div v-if="analyticsSummary.recentEvents.length > 0">
              <div class="text-xs font-semibold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Feature Usage</div>
              <div class="space-y-1.5">
                <div v-for="evt in analyticsSummary.recentEvents" :key="evt.key"
                  class="flex items-center justify-between px-3 py-2 rounded-lg text-sm"
                  :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                  <span class="capitalize" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ evt.category }} — {{ evt.action }}</span>
                  <span class="tabular-nums text-xs px-2 py-0.5 rounded-full font-semibold"
                    :class="isDark ? 'bg-indigo-500/15 text-indigo-400' : 'bg-indigo-50 text-indigo-700'">{{ evt.count }}x</span>
                </div>
              </div>
            </div>
            <div v-if="analyticsSummary.totalPageViews === 0 && analyticsSummary.totalEvents === 0" class="text-center py-4">
              <p class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">No usage data yet — it will appear as you use the app.</p>
            </div>
            <div v-if="analyticsSummary.startedAt" class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
              Tracking since {{ new Date(analyticsSummary.startedAt).toLocaleDateString() }}
            </div>
            <button @click="handleClearAnalytics"
              class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-colors border"
              :class="isDark ? 'border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200' : 'border-slate-200 text-slate-500 hover:bg-slate-100 hover:text-slate-700'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              Clear Analytics
            </button>
          </div>
        </section>

        <!-- ── Danger Zone ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden border-l-4 border-l-red-500"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="flex items-center gap-2.5">
              <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
              <h2 class="text-base font-semibold text-red-500">Danger Zone</h2>
            </div>
          </div>
          <div class="px-6 py-5 space-y-4">
            <!-- Change Password -->
            <div class="pb-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
              <h3 class="text-sm font-semibold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Change Password</h3>
              <div class="space-y-3">
                <div>
                  <label class="text-sm font-medium mb-1.5 block" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Current Password</label>
                  <input v-model="currentPassword" type="password" placeholder="Enter current password"
                    class="w-full rounded-lg px-3.5 py-2.5 text-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                    :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-300 text-slate-900'" />
                </div>
                <div>
                  <label class="text-sm font-medium mb-1.5 block" :class="isDark ? 'text-slate-300' : 'text-slate-700'">New Password</label>
                  <input v-model="newPassword" type="password" placeholder="Min 12 chars, uppercase, number, special"
                    class="w-full rounded-lg px-3.5 py-2.5 text-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                    :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-300 text-slate-900'" />
                </div>
                <div>
                  <label class="text-sm font-medium mb-1.5 block" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Confirm New Password</label>
                  <input v-model="confirmPassword" type="password" placeholder="Repeat new password"
                    class="w-full rounded-lg px-3.5 py-2.5 text-sm border focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                    :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-300 text-slate-900'" />
                </div>
                <div v-if="passwordError" class="text-xs text-red-400 font-medium">{{ passwordError }}</div>
                <div v-if="passwordSuccess" class="text-xs text-emerald-400 font-medium">{{ passwordSuccess }}</div>
                <button @click="changePassword" :disabled="!currentPassword || !newPassword || !confirmPassword || changingPassword"
                  class="px-5 py-2.5 bg-indigo-700 hover:bg-indigo-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg text-sm transition-all">
                  {{ changingPassword ? 'Changing...' : 'Update Password' }}
                </button>
              </div>
            </div>

            <!-- Privacy & Data actions -->
            <div>
              <h3 class="text-sm font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Privacy & Data</h3>
              <p class="text-xs mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">All data is stored locally on your device. Nothing is sent to external servers.</p>
              <div class="space-y-2">
                <button @click="handleExportData"
                  class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-colors border"
                  :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white' : 'border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                  Export All Data as JSON
                </button>
                <button @click="handleClearHistory"
                  class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-colors border"
                  :class="isDark ? 'border-red-800/50 text-red-400 hover:bg-red-500/10' : 'border-red-200 text-red-500 hover:bg-red-50'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                  Clear Consultation History
                </button>
                <button @click="handleClearAll"
                  class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium bg-red-600 hover:bg-red-700 text-white transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
                  Clear All Data
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- ── Help ── -->
        <section class="rounded-xl border shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
          <div class="px-6 py-6 flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-indigo-500/15' : 'bg-indigo-50'">
              <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Need Help?</h3>
              <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Browse documentation for consultations, reports, voice mode, and more.</p>
            </div>
            <router-link to="/help"
              class="px-4 py-2 text-sm font-medium rounded-lg bg-indigo-700 hover:bg-indigo-800 text-white transition-colors flex-shrink-0">
              Help Center
            </router-link>
          </div>
        </section>

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
import AppNav from '@/components/AppNav.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { getProfile, getPreferences, savePreference, exportAllData, clearUserData } from '@/services/userService.js'
import { clearAllEncryptedDataIncludingKeys } from '@/services/encryptedStorage.js'
import { clearHistory as clearHistoryFn } from '@/services/historyService.js'
import { validateApiKeys, API_BASE_URL } from '@/services/api.js'
import { MODEL_PRICING, getModelPrice } from '@/data/modelPricing.js'
import { getAnalyticsSummary, clearAnalytics } from '@/composables/useAnalytics.js'

const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const { lang, currentLanguage, setLang, languages } = useI18n()

const profile = ref({})
const showUserMenu = ref(false)
const apiProvider = ref('anthropic')
const apiKey = ref('')
const showApiKey = ref(false)
const apiKeySaved = ref(false)

// Change password state
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')
const changingPassword = ref(false)

async function changePassword() {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'New passwords do not match.'
    return
  }
  if (newPassword.value.length < 12) {
    passwordError.value = 'Password must be at least 12 characters.'
    return
  }

  changingPassword.value = true
  try {
    const { getAccessToken } = await import('@/services/authService.js')
    const token = getAccessToken()
    const res = await fetch(`${API_BASE_URL}/api/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        old_password: currentPassword.value,
        new_password: newPassword.value,
      }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      passwordError.value = err.detail || 'Failed to change password.'
      return
    }
    passwordSuccess.value = 'Password changed successfully!'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    setTimeout(() => { passwordSuccess.value = '' }, 3000)
  } catch (e) {
    passwordError.value = e.message || 'Network error.'
  } finally {
    changingPassword.value = false
  }
}

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
  // Keep API keys in storage as fallback — don't delete them
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
const settingsBadgeClassMap = {
  'default': 'bg-blue-500/20 text-blue-400',
  'best quality': 'bg-purple-500/20 text-purple-400',
  'fast': 'bg-emerald-500/20 text-emerald-400',
  'budget': 'bg-amber-500/20 text-amber-400',
  'OpenAI': 'bg-green-500/20 text-green-400',
  'Google': 'bg-sky-500/20 text-sky-400',
  'free': 'bg-orange-500/20 text-orange-400',
  'fast + free': 'bg-orange-500/20 text-orange-400',
}

const modelOptions = Object.entries(MODEL_PRICING).map(([id, m]) => ({
  id,
  name: m.label,
  desc: m.description,
  badge: m.badge,
  badgeClass: settingsBadgeClassMap[m.badge] || 'bg-slate-500/20 text-slate-400',
  price: m.estimatedCost,
  perDiagnosis: m.perDiagnosis,
  free: m.perDiagnosis === 0,
}))

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

// ── Analytics ────────────────────────────────────────────────────────────────
const analyticsSummary = ref(getAnalyticsSummary())

function handleClearAnalytics() {
  confirmDialog.message = 'Clear all local usage statistics? This cannot be undone.'
  confirmDialog.action = () => {
    clearAnalytics()
    analyticsSummary.value = getAnalyticsSummary()
  }
  confirmDialog.show = true
}

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

  // Refresh analytics summary (pick up the page-view that was just tracked for /settings)
  analyticsSummary.value = getAnalyticsSummary()
})

function saveSetting(key, value) {
  savePreference(key, value)
}

function saveApiKeyFn() {
  const key = apiKey.value.trim()
  if (!key) return

  // Save key for the active provider (keep other providers' keys intact for fallback)
  const p = providers.find(p => p.id === apiProvider.value)
  if (p) {
    localStorage.setItem(p.storageKey, key)
  }
  localStorage.setItem('ai_provider', apiProvider.value)
  localStorage.setItem('api_key_configured', 'true')
  apiKeySaved.value = true
  setTimeout(() => { apiKeySaved.value = false }, 2000)
}

async function handleExportData() {
  const data = await exportAllData()
  if (data.error) {
    console.warn('Export failed:', data.error)
    return
  }
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
    clearAllEncryptedDataIncludingKeys()  // Nuclear: wipe ALL encrypted data including API keys
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
