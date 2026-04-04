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
    <nav class="relative z-20 flex items-center justify-between px-4 sm:px-6 py-3 border-b backdrop-blur-xl"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline text-[var(--text-primary)]">MedDiagnose AI</span>
        </router-link>
        <div class="w-px h-5 hidden sm:block" style="background: var(--clinical-border)"></div>
        <router-link to="/consult" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors"
          :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          <span class="hidden sm:inline">Consult</span>
        </router-link>
        <router-link to="/reports" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors"
          :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          <span class="hidden sm:inline">Reports</span>
        </router-link>
        <router-link to="/medications" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors"
          :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
          <span class="hidden sm:inline">Medications</span>
        </router-link>
      </div>
      <div class="flex items-center gap-2">
        <ThemeLangControls />
      </div>
    </nav>

    <!-- Main content -->
    <div class="relative z-10 flex justify-center px-4 py-10">
      <div class="max-w-lg w-full space-y-6">
        <!-- Title -->
        <div class="text-center">
          <div class="inline-flex p-3 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-xl shadow-blue-500/20 mb-5">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ isEditing ? 'Edit Profile' : (mode === 'login' ? 'Welcome Back' : 'Create Account') }}</h1>
          <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ isEditing ? 'Update your profile information' : (mode === 'login' ? 'Log in to your account' : 'Set up your profile for a personalized experience') }}</p>
        </div>

        <!-- Login / Sign Up Toggle (hidden when editing existing profile) -->
        <div v-if="!isEditing" class="flex rounded-xl p-1 gap-1" :class="isDark ? 'bg-slate-800/60' : 'bg-slate-100'">
          <button @click="mode = 'login'" class="flex-1 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
            :class="mode === 'login'
              ? (isDark ? 'bg-slate-700 text-white shadow-md' : 'bg-white text-slate-900 shadow-md')
              : (isDark ? 'text-slate-400 hover:text-slate-300' : 'text-slate-500 hover:text-slate-700')">
            Log In
          </button>
          <button @click="mode = 'signup'" class="flex-1 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
            :class="mode === 'signup'
              ? (isDark ? 'bg-slate-700 text-white shadow-md' : 'bg-white text-slate-900 shadow-md')
              : (isDark ? 'text-slate-400 hover:text-slate-300' : 'text-slate-500 hover:text-slate-700')">
            Sign Up
          </button>
        </div>

        <!-- Security & Privacy Info -->
        <div class="rounded-2xl border overflow-hidden"
          :class="isDark ? 'bg-slate-900/60 border-slate-800/60' : 'bg-white/60 border-slate-200'">
          <div class="p-5 space-y-3">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-emerald-500/15' : 'bg-emerald-50'">
                <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-white' : 'text-slate-900'">Encrypted & Private</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Your medical data is encrypted (AES-256) and stored only on your device. Your login works across browsers, but health data stays local.</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-blue-500/15' : 'bg-blue-50'">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-white' : 'text-slate-900'">HIPAA Compliant</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Your password derives the encryption key for local health data. Log in from any browser — your account syncs, your medical data is per-device.</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" :class="isDark ? 'bg-purple-500/15' : 'bg-purple-50'">
                <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-white' : 'text-slate-900'">You're in Control</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Export or delete your data anytime from Settings. Clearing your browser data removes everything permanently.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- ═══ LOGIN MODE ═══ -->
        <div v-if="mode === 'login'" class="backdrop-blur-xl rounded-2xl border shadow-2xl overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="p-6 space-y-5">
            <!-- Saved accounts -->
            <div v-if="savedAccounts.length > 0">
              <h3 class="text-xs uppercase tracking-wider font-semibold mb-3"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">Saved Accounts</h3>
              <div class="space-y-2">
                <button v-for="account in savedAccounts" :key="account.email"
                  @click="loginWithAccount(account)"
                  class="w-full flex items-center gap-3 p-3 rounded-xl border transition-all text-left group"
                  :class="isDark
                    ? 'border-slate-700/50 hover:border-blue-500/40 hover:bg-slate-800/60'
                    : 'border-slate-200 hover:border-blue-300 hover:bg-blue-50/50'">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
                    {{ account.name ? account.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) : '?' }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ account.name }}</div>
                    <div class="text-xs truncate" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ account.email }}</div>
                  </div>
                  <svg class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" :class="isDark ? 'text-blue-400' : 'text-blue-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
              <div class="flex items-center gap-3 my-4">
                <div class="flex-1 h-px" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-200'"></div>
                <span class="text-detail uppercase tracking-wider" :class="isDark ? 'text-slate-600' : 'text-slate-400'">or enter email</span>
                <div class="flex-1 h-px" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-200'"></div>
              </div>
            </div>

            <!-- Email login -->
            <div>
              <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Email Address</label>
              <input
                v-model="loginEmail"
                type="email"
                placeholder="your@email.com"
                @keyup.enter="handleLogin"
                class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                :class="isDark
                  ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                  : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
              />
            </div>

            <!-- Error -->
            <div v-if="loginError" class="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
              <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <div>
                <p class="text-red-300 text-xs">{{ loginError }}</p>
                <button @click="mode = 'signup'" class="text-blue-400 hover:text-blue-300 text-xs mt-1 underline underline-offset-2">Create a new account instead</button>
              </div>
            </div>

            <!-- Login Button -->
            <button
              @click="handleLogin"
              :disabled="!loginEmail.trim()"
              class="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl text-sm transition-all duration-200 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
              </svg>
              Log In
            </button>

            <p class="text-center text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Don't have an account? <button @click="mode = 'signup'" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">Sign up</button>
            </p>
          </div>
        </div>

        <!-- ═══ SIGN UP MODE ═══ -->
        <div v-else class="backdrop-blur-xl rounded-2xl border shadow-2xl overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="p-6 space-y-6">

            <!-- Basic Info Section -->
            <div>
              <h3 class="text-xs uppercase tracking-wider font-semibold mb-4"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">Basic Information</h3>
              <div class="space-y-4">
                <!-- Name -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Name <span class="text-red-400">*</span>
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    placeholder="Your full name"
                    @blur="nameBlurred = true"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="[
                      isDark ? 'bg-slate-800/80 border text-white placeholder-slate-600' : 'bg-slate-50 border text-slate-900 placeholder-slate-400',
                      nameBlurred && !form.name.trim() ? 'border-red-500/50 ring-1 ring-red-500/20' : (isDark ? 'border-slate-700/50' : 'border-slate-200')
                    ]"
                  />
                  <p v-if="nameBlurred && !form.name.trim()" class="text-caption text-red-400 mt-1">Name is required</p>
                </div>
                <!-- Email -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Email <span class="text-red-400">*</span>
                  </label>
                  <input
                    v-model="form.email"
                    type="email"
                    placeholder="your@email.com"
                    @blur="emailBlurred = true"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="[
                      isDark ? 'bg-slate-800/80 border text-white placeholder-slate-600' : 'bg-slate-50 border text-slate-900 placeholder-slate-400',
                      emailBlurred && form.email && !isValidEmail(form.email) ? 'border-amber-500/50 ring-1 ring-amber-500/20' : (isDark ? 'border-slate-700/50' : 'border-slate-200')
                    ]"
                  />
                  <p v-if="emailBlurred && form.email && !isValidEmail(form.email)" class="text-caption text-amber-400 mt-1">Please enter a valid email address</p>
                </div>
                <!-- Gender -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Gender</label>
                  <select
                    v-model="form.gender"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  >
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer_not_to_say">Prefer not to say</option>
                  </select>
                </div>
                <!-- Date of Birth -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Date of Birth</label>
                  <input
                    v-model="form.dateOfBirth"
                    type="date"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  />
                </div>
                <!-- Location -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Location <span class="text-detail font-normal" :class="isDark ? 'text-slate-600' : 'text-slate-400'">(helps find nearby specialists)</span>
                  </label>
                  <div class="grid grid-cols-2 gap-3">
                    <input
                      v-model="form.city"
                      type="text"
                      placeholder="City or town"
                      class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                      :class="isDark
                        ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                        : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                    />
                    <input
                      v-model="form.stateRegion"
                      type="text"
                      placeholder="State / Region"
                      class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                      :class="isDark
                        ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                        : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                    />
                  </div>
                  <input
                    v-model="form.zipCode"
                    type="text"
                    placeholder="Zip / Postal code"
                    class="w-full rounded-xl px-4 py-3 text-sm mt-3 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
              </div>
            </div>

            <!-- Medical Info Section -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xs uppercase tracking-wider font-semibold"
                  :class="isDark ? 'text-slate-500' : 'text-slate-400'">Medical Information</h3>
                <span class="text-detail px-2 py-0.5 rounded-full"
                  :class="isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'">Optional</span>
              </div>
              <div class="space-y-4">
                <!-- Blood Type -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Blood Type</label>
                  <select
                    v-model="form.bloodType"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  >
                    <option value="">Select blood type</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
                <!-- Allergies (chip/tag input) -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Allergies <span class="text-detail font-normal" :class="isDark ? 'text-slate-600' : 'text-slate-400'">(type + Enter to add)</span>
                  </label>
                  <div class="flex flex-wrap gap-2 mb-2" v-if="allergyChips.length">
                    <span v-for="(chip, i) in allergyChips" :key="'allergy-'+i"
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium"
                      :class="isDark ? 'bg-red-500/15 text-red-300 border border-red-500/20' : 'bg-red-50 text-red-700 border border-red-200'">
                      {{ chip }}
                      <button @click="allergyChips.splice(i, 1)" class="ml-0.5 hover:opacity-70" type="button">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                      </button>
                    </span>
                  </div>
                  <input
                    v-model="allergyInput"
                    type="text"
                    placeholder="e.g. Penicillin, Peanuts, Latex"
                    @keydown.enter.prevent="addAllergyChip"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
                <!-- Current Medications (chip/tag input) -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Current Medications <span class="text-detail font-normal" :class="isDark ? 'text-slate-600' : 'text-slate-400'">(type + Enter to add)</span>
                  </label>
                  <div class="flex flex-wrap gap-2 mb-2" v-if="medicationChips.length">
                    <span v-for="(chip, i) in medicationChips" :key="'med-'+i"
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium"
                      :class="isDark ? 'bg-blue-500/15 text-blue-300 border border-blue-500/20' : 'bg-blue-50 text-blue-700 border border-blue-200'">
                      {{ chip }}
                      <button @click="medicationChips.splice(i, 1)" class="ml-0.5 hover:opacity-70" type="button">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                      </button>
                    </span>
                  </div>
                  <input
                    v-model="medicationInput"
                    type="text"
                    placeholder="e.g. Lisinopril, Metformin"
                    @keydown.enter.prevent="addMedicationChip"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
              </div>
            </div>

            <!-- ═══ MEDICAL HISTORY (collapsible) ═══ -->
            <div>
              <button @click="medHistoryExpanded = !medHistoryExpanded" type="button"
                class="w-full flex items-center justify-between py-3 group">
                <div class="flex items-center gap-2">
                  <h3 class="text-xs uppercase tracking-wider font-semibold"
                    :class="isDark ? 'text-slate-500' : 'text-slate-400'">Medical History</h3>
                  <span class="text-detail px-2 py-0.5 rounded-full"
                    :class="isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'">Optional</span>
                </div>
                <svg class="w-4 h-4 transition-transform duration-200" :class="[medHistoryExpanded ? 'rotate-180' : '', isDark ? 'text-slate-500' : 'text-slate-400']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>

              <div v-show="medHistoryExpanded" class="space-y-6 pt-2">

                <!-- 1. Past Medical Conditions -->
                <div>
                  <label class="text-xs font-medium mb-2.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Past Medical Conditions</label>
                  <div class="grid grid-cols-2 gap-2">
                    <label v-for="cond in pastConditionOptions" :key="cond"
                      class="flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors"
                      :class="isDark ? 'hover:bg-slate-800/60' : 'hover:bg-slate-50'">
                      <input type="checkbox" :value="cond" v-model="form.pastConditions"
                        class="w-4 h-4 rounded border-slate-600 text-blue-500 focus:ring-blue-500/30 bg-transparent" />
                      <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ cond }}</span>
                    </label>
                  </div>
                  <div v-if="form.pastConditions.includes('Cancer (specify)') || form.pastConditions.includes('Other')" class="mt-2">
                    <input v-model="form.pastConditionsOther" type="text"
                      :placeholder="form.pastConditions.includes('Cancer (specify)') ? 'Specify cancer type or other condition...' : 'Specify other condition...'"
                      class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                      :class="isDark
                        ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                        : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'" />
                  </div>
                </div>

                <!-- 2. Surgical History -->
                <div>
                  <label class="text-xs font-medium mb-2.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Surgical History</label>
                  <div class="space-y-2">
                    <div v-for="(surgery, i) in form.surgeries" :key="'surg-'+i" class="flex gap-2 items-center">
                      <input v-model="surgery.name" type="text" placeholder="Surgery name"
                        class="flex-1 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark
                          ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                          : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'" />
                      <input v-model="surgery.year" type="text" placeholder="Year" maxlength="4"
                        class="w-20 rounded-xl px-3 py-2.5 text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark
                          ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                          : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'" />
                      <button @click="form.surgeries.splice(i, 1)" type="button"
                        class="p-1.5 rounded-lg transition-colors"
                        :class="isDark ? 'text-slate-500 hover:text-red-400 hover:bg-slate-800' : 'text-slate-400 hover:text-red-500 hover:bg-slate-100'">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                      </button>
                    </div>
                    <button @click="form.surgeries.push({ name: '', year: '' })" type="button"
                      class="flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg transition-colors"
                      :class="isDark ? 'text-blue-400 hover:bg-slate-800/60' : 'text-blue-600 hover:bg-blue-50'">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                      Add Surgery
                    </button>
                  </div>
                </div>

                <!-- 3. Family History (grid) -->
                <div>
                  <label class="text-xs font-medium mb-2.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Family History</label>
                  <div class="overflow-x-auto rounded-xl border" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
                    <table class="w-full text-xs">
                      <thead>
                        <tr :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                          <th class="text-left px-3 py-2 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Condition</th>
                          <th v-for="member in familyMembers" :key="member" class="px-2 py-2 font-medium text-center" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ member }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="cond in familyConditions" :key="cond"
                          class="border-t" :class="isDark ? 'border-slate-700/30' : 'border-slate-100'">
                          <td class="px-3 py-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ cond }}</td>
                          <td v-for="member in familyMembers" :key="cond+'-'+member" class="px-2 py-2 text-center">
                            <input type="checkbox"
                              :checked="(form.familyHistory[cond] || []).includes(member)"
                              @change="toggleFamilyHistory(cond, member)"
                              class="w-4 h-4 rounded border-slate-600 text-blue-500 focus:ring-blue-500/30 bg-transparent cursor-pointer" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- 4. Social History -->
                <div>
                  <label class="text-xs font-medium mb-2.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Social History</label>
                  <div class="space-y-3">
                    <!-- Smoking -->
                    <div class="flex items-center gap-3">
                      <label class="text-sm w-20 flex-shrink-0" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Smoking</label>
                      <select v-model="form.socialHistory.smoking"
                        class="flex-1 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark ? 'bg-slate-800/80 border border-slate-700/50 text-white' : 'bg-slate-50 border border-slate-200 text-slate-900'">
                        <option value="">Select...</option>
                        <option value="never">Never</option>
                        <option value="former">Former</option>
                        <option value="current">Current (packs/day)</option>
                      </select>
                    </div>
                    <!-- Alcohol -->
                    <div class="flex items-center gap-3">
                      <label class="text-sm w-20 flex-shrink-0" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Alcohol</label>
                      <select v-model="form.socialHistory.alcohol"
                        class="flex-1 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark ? 'bg-slate-800/80 border border-slate-700/50 text-white' : 'bg-slate-50 border border-slate-200 text-slate-900'">
                        <option value="">Select...</option>
                        <option value="none">None</option>
                        <option value="occasional">Occasional</option>
                        <option value="moderate">Moderate</option>
                        <option value="heavy">Heavy</option>
                      </select>
                    </div>
                    <!-- Exercise -->
                    <div class="flex items-center gap-3">
                      <label class="text-sm w-20 flex-shrink-0" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Exercise</label>
                      <select v-model="form.socialHistory.exercise"
                        class="flex-1 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark ? 'bg-slate-800/80 border border-slate-700/50 text-white' : 'bg-slate-50 border border-slate-200 text-slate-900'">
                        <option value="">Select...</option>
                        <option value="sedentary">Sedentary</option>
                        <option value="light">Light</option>
                        <option value="moderate">Moderate</option>
                        <option value="active">Active</option>
                      </select>
                    </div>
                    <!-- Drug Use -->
                    <div class="flex items-center gap-3">
                      <label class="text-sm w-20 flex-shrink-0" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Drug Use</label>
                      <select v-model="form.socialHistory.drugUse"
                        class="flex-1 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                        :class="isDark ? 'bg-slate-800/80 border border-slate-700/50 text-white' : 'bg-slate-50 border border-slate-200 text-slate-900'">
                        <option value="">Select...</option>
                        <option value="none">None</option>
                        <option value="cannabis">Cannabis</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <!-- Emergency Contact Section -->
            <div>
              <h3 class="text-xs uppercase tracking-wider font-semibold mb-4"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">Emergency Contact</h3>
              <div class="space-y-4">
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Contact Name</label>
                  <input
                    v-model="form.emergencyContactName"
                    type="text"
                    placeholder="Emergency contact name"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Contact Phone</label>
                  <input
                    v-model="form.emergencyContactPhone"
                    type="tel"
                    placeholder="+1 (555) 000-0000"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
              </div>
            </div>

            <!-- Error message -->
            <div v-if="error" class="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
              <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <p class="text-red-300 text-xs">{{ error }}</p>
            </div>

            <!-- Save Button -->
            <button
              @click="handleSave"
              :disabled="saving || !form.name.trim() || !form.email.trim() || !isValidEmail(form.email)"
              class="w-full btn-blue py-3 rounded-xl text-sm"
            >
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              <svg v-else-if="!isEditing" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              {{ saving ? 'Saving...' : (isEditing ? 'Save Profile' : 'Create Account') }}
            </button>

            <p v-if="!isEditing" class="text-center text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Already have an account? <button @click="handleLogin" class="text-blue-400 hover:text-blue-300 underline underline-offset-2">Log in</button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { useUser } from '@/composables/useUser.js'
import { getProfile, saveProfile } from '@/services/userService.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

export default {
  name: 'ProfileSetup',
  components: { ThemeLangControls },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const { isDark } = useTheme()
    const { profile: userProfile, updateProfile } = useUser()
    const error = ref('')
    const saving = ref(false)
    const nameBlurred = ref(false)
    const emailBlurred = ref(false)

    // Doctor avatar for nav icon
    const defaultAvatar = {
      bgColor: '#1e3a5f', skinTone: '#F5CBA7', hairColor: '#3d2b1f',
      coatColor: '#f0f0f0', lipColor: '#c9877a', glasses: true,
    }
    const navAvatar = JSON.parse(localStorage.getItem('doctor_avatar') || JSON.stringify(defaultAvatar))

    // Mode: 'login' or 'signup' — default to login if not already logged in
    const isEditing = ref(false)
    const mode = ref('login')

    // Login state
    const loginEmail = ref('')
    const loginError = ref('')
    const savedAccounts = ref([]) // No longer populated — auth goes through backend

    function isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    }

    const form = ref({
      name: '',
      email: '',
      gender: '',
      dateOfBirth: '',
      city: '',
      stateRegion: '',
      zipCode: '',
      bloodType: '',
      emergencyContactName: '',
      emergencyContactPhone: '',
      pastConditions: [],
      pastConditionsOther: '',
      surgeries: [],
      familyHistory: {},
      socialHistory: { smoking: '', alcohol: '', exercise: '', drugUse: '' },
    })

    // Chip/tag inputs for allergies and medications
    const allergyChips = ref([])
    const allergyInput = ref('')
    const medicationChips = ref([])
    const medicationInput = ref('')

    function addAllergyChip() {
      const val = allergyInput.value.trim()
      if (val && !allergyChips.value.includes(val)) {
        allergyChips.value.push(val)
      }
      allergyInput.value = ''
    }
    function addMedicationChip() {
      const val = medicationInput.value.trim()
      if (val && !medicationChips.value.includes(val)) {
        medicationChips.value.push(val)
      }
      medicationInput.value = ''
    }

    // Medical history collapsible
    const medHistoryExpanded = ref(false)

    // Options for past conditions checkboxes
    const pastConditionOptions = [
      'Diabetes', 'Hypertension', 'Heart Disease', 'Asthma/COPD',
      'Cancer (specify)', 'Stroke', 'Thyroid Disease', 'Kidney Disease',
      'Liver Disease', 'Arthritis', 'Depression/Anxiety', 'Other'
    ]

    // Family history grid data
    const familyConditions = ['Heart Disease', 'Diabetes', 'Cancer', 'Stroke', 'High Blood Pressure', 'Mental Health']
    const familyMembers = ['Mother', 'Father', 'Sibling', 'Grandparent']

    function toggleFamilyHistory(condition, member) {
      if (!form.value.familyHistory[condition]) {
        form.value.familyHistory[condition] = []
      }
      const arr = form.value.familyHistory[condition]
      const idx = arr.indexOf(member)
      if (idx >= 0) {
        arr.splice(idx, 1)
      } else {
        arr.push(member)
      }
    }

    // Legacy compat
    const allergiesText = ref('')
    const medicationsText = ref('')

    onMounted(() => {
      const profile = getProfile()
      // If user already has a profile, they're editing — go straight to signup form
      if (profile.name && profile.name.trim()) {
        isEditing.value = true
        mode.value = 'signup'
      } else {
        // Default to login if there are saved accounts, otherwise signup
        mode.value = 'signup'
      }
      form.value.name = profile.name || ''
      form.value.email = profile.email || ''
      form.value.gender = profile.gender || ''
      form.value.dateOfBirth = profile.dateOfBirth || ''
      form.value.city = profile.city || ''
      form.value.stateRegion = profile.stateRegion || ''
      form.value.zipCode = profile.zipCode || ''
      form.value.bloodType = profile.bloodType || ''
      form.value.emergencyContactName = profile.emergencyContactName || ''
      form.value.emergencyContactPhone = profile.emergencyContactPhone || ''
      // Chip inputs (load from array or legacy comma-separated)
      allergyChips.value = Array.isArray(profile.allergies) ? [...profile.allergies] : []
      medicationChips.value = Array.isArray(profile.medications) ? [...profile.medications] : []
      allergiesText.value = (profile.allergies || []).join(', ')
      medicationsText.value = (profile.medications || []).join(', ')
      // Medical history fields
      form.value.pastConditions = Array.isArray(profile.pastConditions) ? [...profile.pastConditions] : []
      form.value.pastConditionsOther = profile.pastConditionsOther || ''
      form.value.surgeries = Array.isArray(profile.surgeries) ? profile.surgeries.map(s => ({ ...s })) : []
      form.value.familyHistory = profile.familyHistory ? JSON.parse(JSON.stringify(profile.familyHistory)) : {}
      form.value.socialHistory = profile.socialHistory ? { ...{ smoking: '', alcohol: '', exercise: '', drugUse: '' }, ...profile.socialHistory } : { smoking: '', alcohol: '', exercise: '', drugUse: '' }
      // Auto-expand if any medical history data exists
      if (form.value.pastConditions.length || form.value.surgeries.length || Object.keys(form.value.familyHistory).length || form.value.socialHistory.smoking || form.value.socialHistory.alcohol) {
        medHistoryExpanded.value = true
      }
    })

    function parseCommaSeparated(text) {
      if (!text.trim()) return []
      return text.split(',').map(s => s.trim()).filter(Boolean)
    }

    function handleLogin() {
      // Redirect to proper backend auth
      router.push('/login')
    }

    function loginWithAccount() {
      // Redirect to proper backend auth
      router.push('/login')
    }

    async function handleSave() {
      error.value = ''
      if (!form.value.name.trim()) {
        error.value = 'Name is required.'
        return
      }
      if (!form.value.email.trim() || !isValidEmail(form.value.email)) {
        error.value = 'A valid email is required.'
        return
      }

      saving.value = true
      const data = {
        ...form.value,
        allergies: allergyChips.value.length ? [...allergyChips.value] : parseCommaSeparated(allergiesText.value),
        medications: medicationChips.value.length ? [...medicationChips.value] : parseCommaSeparated(medicationsText.value),
        surgeries: form.value.surgeries.filter(s => s.name.trim()),
        emergencyContact: form.value.emergencyContactName
          ? `${form.value.emergencyContactName}${form.value.emergencyContactPhone ? ' - ' + form.value.emergencyContactPhone : ''}`
          : '',
      }

      try {
        await saveProfile(data)
        updateProfile(data)
        // Verify save worked
        const verify = localStorage.getItem('user_profile')
        if (!verify) {
          // Direct write as last resort
          localStorage.setItem('user_profile', JSON.stringify(data))
        }
        router.push(isEditing.value ? '/consult' : '/')
      } catch (e) {
        error.value = e.message || 'Failed to save profile. Please try again.'
      } finally {
        saving.value = false
      }
    }

    return {
      isDark,
      mode,
      isEditing,
      form,
      allergiesText,
      medicationsText,
      allergyChips,
      allergyInput,
      addAllergyChip,
      medicationChips,
      medicationInput,
      addMedicationChip,
      medHistoryExpanded,
      pastConditionOptions,
      familyConditions,
      familyMembers,
      toggleFamilyHistory,
      error,
      saving,
      nameBlurred,
      emailBlurred,
      isValidEmail,
      handleSave,
      loginEmail,
      loginError,
      savedAccounts,
      handleLogin,
      loginWithAccount,
      navAvatar,
    }
  }
}
</script>
