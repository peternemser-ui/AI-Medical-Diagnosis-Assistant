<template>
  <div 
    class="flex flex-col min-h-screen text-white premium-dashboard-container"
    :style="{
      background: 'var(--dashboard-bg)',
      color: 'var(--text)',
      minHeight: '100vh'
    }"
  >
    <!-- Premium Medical Header -->
    <div 
      class="premium-header backdrop-blur-sm py-4 px-6 shadow-xl"
      :style="{
        background: 'var(--header-bg)',
        borderBottom: '1px solid var(--border-accent)',
        boxShadow: 'var(--shadow-lg)',
        backdropFilter: 'var(--glass-backdrop)'
      }"
    >
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div>
          <h1 
            class="text-2xl font-bold tracking-tight mb-0.5 flex items-center gap-3 premium-dashboard-title"
            :style="{
              color: 'var(--text)',
              fontSize: '24px',
              fontWeight: '800',
              letterSpacing: '-0.025em'
            }"
          >
            <MaterialIcon 
              icon="dashboard" 
              size="xl" 
              :fill="true"
              :style="{ color: 'var(--primary)' }"
            />
            AI Medical Assessment Dashboard
          </h1>
          <p 
            class="text-sm premium-subtitle"
            :style="{
              color: 'var(--text-muted)',
              fontSize: '13px',
              fontWeight: '500'
            }"
          >
            Comprehensive diagnosis analysis with clinical insights
          </p>
        </div>
        <div class="flex items-center gap-3">
          <!-- Export Menu -->
          <div class="relative">
            <button
              @click="showExportMenu = !showExportMenu"
              class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 rounded-lg font-semibold text-sm transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <MaterialIcon icon="download" size="sm" />
              Export Report
            </button>

            <!-- Export Dropdown -->
            <div v-if="showExportMenu"
                 class="absolute right-0 mt-2 w-56 bg-gray-800 rounded-lg shadow-xl border border-gray-700 z-50 overflow-hidden">
              <button @click="exportReport('pdf')"
                      class="w-full px-4 py-3 text-left hover:bg-gray-700 transition-colors flex items-center gap-3 border-b border-gray-700">
                <MaterialIcon icon="picture_as_pdf" size="sm" class="text-red-400" />
                <div>
                  <div class="font-semibold text-sm">Export as PDF</div>
                  <div class="text-xs text-gray-400">Printable medical report</div>
                </div>
              </button>
              <button @click="exportReport('html')"
                      class="w-full px-4 py-3 text-left hover:bg-gray-700 transition-colors flex items-center gap-3 border-b border-gray-700">
                <MaterialIcon icon="web" size="sm" class="text-blue-400" />
                <div>
                  <div class="font-semibold text-sm">Export as HTML</div>
                  <div class="text-xs text-gray-400">Web page format</div>
                </div>
              </button>
              <button @click="exportReport('json')"
                      class="w-full px-4 py-3 text-left hover:bg-gray-700 transition-colors flex items-center gap-3 border-b border-gray-700">
                <MaterialIcon icon="code" size="sm" class="text-yellow-400" />
                <div>
                  <div class="font-semibold text-sm">Export as JSON</div>
                  <div class="text-xs text-gray-400">Data format</div>
                </div>
              </button>
              <button @click="exportReport('text')"
                      class="w-full px-4 py-3 text-left hover:bg-gray-700 transition-colors flex items-center gap-3">
                <MaterialIcon icon="description" size="sm" class="text-gray-400" />
                <div>
                  <div class="font-semibold text-sm">Export as Text</div>
                  <div class="text-xs text-gray-400">Plain text transcript</div>
                </div>
              </button>
            </div>
          </div>

          <ThemeToggle />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 max-w-7xl w-full mx-auto px-4 py-4">
      
      <!-- Top Info Bar - Patient Summary -->
      <div class="bg-gradient-to-r from-blue-800 to-indigo-800 rounded-lg shadow-lg p-3 mb-4 border border-blue-700">
        <div class="flex items-center gap-2 mb-2">
          <MaterialIcon icon="badge" size="lg" :fill="true" />
          <h2 class="text-sm font-bold uppercase tracking-wide">Patient Information</h2>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div class="flex items-center gap-1.5 bg-blue-900 bg-opacity-40 rounded px-2 py-1.5">
            <MaterialIcon icon="person" size="sm" />
            <span class="text-gray-300">Age:</span>
            <span class="font-semibold text-white">{{ patientInfo.age }}</span>
          </div>
          <div class="flex items-center gap-1.5 bg-blue-900 bg-opacity-40 rounded px-2 py-1.5">
            <MaterialIcon icon="wc" size="sm" />
            <span class="text-gray-300">Gender:</span>
            <span class="font-semibold text-white">{{ patientInfo.gender }}</span>
          </div>
          <div class="flex items-center gap-1.5 bg-blue-900 bg-opacity-40 rounded px-2 py-1.5">
            <MaterialIcon icon="schedule" size="sm" />
            <span class="text-gray-300">Duration:</span>
            <span class="font-semibold text-white">{{ patientInfo.duration }}</span>
          </div>
          <div class="flex items-center gap-1.5 bg-blue-900 bg-opacity-40 rounded px-2 py-1.5">
            <MaterialIcon icon="emergency" size="sm" />
            <span class="text-gray-300">Severity:</span>
            <span class="font-semibold text-white">{{ patientInfo.severity }}</span>
          </div>
        </div>
        <div class="mt-2 bg-blue-900 bg-opacity-40 rounded px-2 py-1.5">
          <div class="flex items-start gap-1.5 text-xs">
            <MaterialIcon icon="medical_information" size="sm" class="mt-0.5" />
            <div>
              <span class="text-gray-300">Chief Complaint:</span>
              <span class="font-semibold text-white ml-1">{{ patientInfo.symptoms }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Dashboard Layout -->
      <div class="space-y-4">
        
        <!-- FULL WIDTH: Differential Diagnoses Card with Body Diagram + Dial Charts -->
        <div class="bg-gray-800 bg-opacity-90 backdrop-blur-sm rounded-lg shadow-xl border border-gray-700">
          <div class="bg-gradient-to-r from-blue-700 to-blue-600 px-4 py-2.5 rounded-t-lg border-b border-blue-500">
            <h3 class="text-sm font-bold uppercase tracking-wide flex items-center gap-2">
              <MaterialIcon icon="troubleshoot" size="lg" :fill="true" />
              Differential Diagnoses
            </h3>
          </div>
          
          <!-- Dial Charts + Body Diagram Layout -->
          <div v-if="relatedDiagnoses.length > 0" class="p-8">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-8">
              
              <!-- LEFT: Three Dial Charts (3/4 width) -->
              <div class="lg:col-span-3">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
                  <div v-for="(diagnosis, index) in relatedDiagnoses.slice(0, 3)" :key="index"
                       class="flex flex-col items-center pb-20">
                    <div class="relative cursor-pointer hover:scale-105 transition-transform duration-200" 
                         style="width: 180px; height: 180px;"
                         @click="openDiagnosisDetails(diagnosis)">
                      <DialChart
                        :value="diagnosis.confidence"
                        :label="''"
                        :color="getColorForIndex(index)"
                        :size="180"
                        :strokeWidth="18"
                      />
                      <!-- Click indicator -->
                      <div class="absolute top-1 right-1 bg-blue-600 rounded-full p-1 opacity-70 hover:opacity-100 shadow-lg">
                        <MaterialIcon icon="open_in_new" size="sm" class="text-white" />
                      </div>
                    </div>
                    <!-- Label below chart -->
                    <div class="mt-4 text-center px-2 max-w-[200px]">
                      <h4 class="font-bold text-white text-sm mb-2 leading-tight">{{ diagnosis.condition }}</h4>
                      <div class="flex items-center justify-center gap-2 text-xs text-gray-400 mb-1">
                        <MaterialIcon icon="emergency" size="sm" />
                        <span>{{ diagnosis.urgency || 'routine' }}</span>
                      </div>
                      <div class="text-xs text-gray-500">{{ diagnosis.specialty }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- RIGHT: Body Diagram (1/4 width) -->
              <div class="lg:col-span-1 flex flex-col items-center justify-start">
                <div class="w-full bg-gradient-to-br from-gray-800/60 to-gray-900/60 rounded-lg p-4 border border-gray-700">
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-xs font-bold uppercase tracking-wide text-gray-300 flex items-center gap-2">
                      <MaterialIcon icon="accessibility_new" size="sm" :fill="true" />
                      Symptom Map
                    </h4>
                    <span v-if="bodyAreas.length > 0" class="text-xs bg-red-600 text-white px-2 py-0.5 rounded-full">
                      {{ bodyAreas.length }} area{{ bodyAreas.length !== 1 ? 's' : '' }}
                    </span>
                  </div>
                  
                  <!-- Simplified Body Display -->
                  <div class="body-display-compact">
                    <svg viewBox="0 0 200 400" class="w-full h-auto max-h-[420px]" style="filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));">
                      <!-- Front body outline -->
                      <g>
                        <!-- Head -->
                        <ellipse cx="100" cy="30" rx="25" ry="30" 
                                 :fill="isAreaSelected('head') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('head') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('head') ? 0.9 : 0.4" />
                        
                        <!-- Eyes (highlighted if selected) -->
                        <ellipse cx="90" cy="28" rx="6" ry="4"
                                 :fill="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? '#ef4444' : '#1f2937'" 
                                 :stroke="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? '#dc2626' : '#374151'" 
                                 stroke-width="1.5"
                                 :opacity="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? 1 : 0.6" />
                        <ellipse cx="110" cy="28" rx="6" ry="4"
                                 :fill="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? '#ef4444' : '#1f2937'" 
                                 :stroke="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? '#dc2626' : '#374151'" 
                                 stroke-width="1.5"
                                 :opacity="isAreaSelected('eyes') || isAreaSelected('left_eye') || isAreaSelected('right_eye') ? 1 : 0.6" />
                        
                        <!-- Neck -->
                        <rect x="90" y="55" width="20" height="15" rx="3"
                              :fill="isAreaSelected('neck') ? '#ef4444' : '#374151'" 
                              :stroke="isAreaSelected('neck') ? '#dc2626' : '#4b5563'" 
                              stroke-width="2"
                              :opacity="isAreaSelected('neck') ? 0.9 : 0.4" />
                        
                        <!-- Shoulders -->
                        <ellipse cx="65" cy="85" rx="18" ry="15"
                                 :fill="isAreaSelected('left_shoulder') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('left_shoulder') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('left_shoulder') ? 0.9 : 0.4" />
                        <ellipse cx="135" cy="85" rx="18" ry="15"
                                 :fill="isAreaSelected('right_shoulder') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('right_shoulder') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('right_shoulder') ? 0.9 : 0.4" />
                        
                        <!-- Chest -->
                        <ellipse cx="100" cy="110" rx="35" ry="25"
                                 :fill="isAreaSelected('chest') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('chest') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('chest') ? 0.9 : 0.4" />
                        
                        <!-- Abdomen -->
                        <ellipse cx="100" cy="155" rx="32" ry="28"
                                 :fill="isAreaSelected('abdomen') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('abdomen') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('abdomen') ? 0.9 : 0.4" />
                        
                        <!-- Groin -->
                        <ellipse cx="100" cy="195" rx="25" ry="18"
                                 :fill="isAreaSelected('groin') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('groin') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('groin') ? 0.9 : 0.4" />
                        
                        <!-- Arms -->
                        <rect x="45" y="100" width="12" height="70" rx="6"
                              :fill="isAreaSelected('left_arm') ? '#ef4444' : '#374151'" 
                              :stroke="isAreaSelected('left_arm') ? '#dc2626' : '#4b5563'" 
                              stroke-width="2"
                              :opacity="isAreaSelected('left_arm') ? 0.9 : 0.4" />
                        <rect x="143" y="100" width="12" height="70" rx="6"
                              :fill="isAreaSelected('right_arm') ? '#ef4444' : '#374151'" 
                              :stroke="isAreaSelected('right_arm') ? '#dc2626' : '#4b5563'" 
                              stroke-width="2"
                              :opacity="isAreaSelected('right_arm') ? 0.9 : 0.4" />
                        
                        <!-- Legs -->
                        <rect x="75" y="210" width="18" height="100" rx="9"
                              :fill="isAreaSelected('left_leg') ? '#ef4444' : '#374151'" 
                              :stroke="isAreaSelected('left_leg') ? '#dc2626' : '#4b5563'" 
                              stroke-width="2"
                              :opacity="isAreaSelected('left_leg') ? 0.9 : 0.4" />
                        <rect x="107" y="210" width="18" height="100" rx="9"
                              :fill="isAreaSelected('right_leg') ? '#ef4444' : '#374151'" 
                              :stroke="isAreaSelected('right_leg') ? '#dc2626' : '#4b5563'" 
                              stroke-width="2"
                              :opacity="isAreaSelected('right_leg') ? 0.9 : 0.4" />
                        
                        <!-- Knees -->
                        <circle cx="84" cy="280" r="8"
                                :fill="isAreaSelected('left_knee') ? '#ef4444' : '#374151'" 
                                :stroke="isAreaSelected('left_knee') ? '#dc2626' : '#4b5563'" 
                                stroke-width="2"
                                :opacity="isAreaSelected('left_knee') ? 0.9 : 0.4" />
                        <circle cx="116" cy="280" r="8"
                                :fill="isAreaSelected('right_knee') ? '#ef4444' : '#374151'" 
                                :stroke="isAreaSelected('right_knee') ? '#dc2626' : '#4b5563'" 
                                stroke-width="2"
                                :opacity="isAreaSelected('right_knee') ? 0.9 : 0.4" />
                        
                        <!-- Feet -->
                        <ellipse cx="84" cy="325" rx="10" ry="14"
                                 :fill="isAreaSelected('left_foot') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('left_foot') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('left_foot') ? 0.9 : 0.4" />
                        <ellipse cx="116" cy="325" rx="10" ry="14"
                                 :fill="isAreaSelected('right_foot') ? '#ef4444' : '#374151'" 
                                 :stroke="isAreaSelected('right_foot') ? '#dc2626' : '#4b5563'" 
                                 stroke-width="2"
                                 :opacity="isAreaSelected('right_foot') ? 0.9 : 0.4" />
                      </g>
                    </svg>
                  </div>
                  
                  <!-- Legend -->
                  <div class="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-400 text-center">
                    <div v-if="bodyAreas.length > 0" class="space-y-1">
                      <div class="flex items-center justify-center gap-2 mb-2">
                        <span class="w-3 h-3 bg-red-600 rounded-full animate-pulse"></span>
                        <span class="font-semibold">Affected Areas</span>
                      </div>
                      <div class="flex flex-wrap gap-1 justify-center">
                        <span v-for="area in bodyAreas" :key="area" 
                              class="bg-red-900/40 text-red-300 px-2 py-0.5 rounded text-xs border border-red-700 shadow-sm">
                          {{ formatAreaName(area) }}
                        </span>
                      </div>
                    </div>
                    <div v-else class="text-gray-500 flex items-center justify-center gap-2">
                      <MaterialIcon icon="info" size="sm" />
                      <span>No symptom locations recorded</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Add spacing for labels below dials -->
            <div class="mt-20"></div>
            
            <!-- Detailed diagnosis cards below dials -->
            <div class="space-y-3">
              <div v-for="(diagnosis, index) in relatedDiagnoses.slice(0, 3)" :key="index" 
                   class="bg-gray-900 bg-opacity-50 rounded-lg p-4 border-l-4 hover:bg-gray-900 transition-colors"
                   :style="{ borderLeftColor: getColorForIndex(index) }">
                
                <div class="flex items-start gap-3">
                  <!-- Icon -->
                  <div class="flex-shrink-0 mt-1">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center"
                         :style="{ backgroundColor: getColorForIndex(index) + '20' }">
                      <MaterialIcon :icon="getIcon(diagnosis.condition)" size="lg" :fill="true" 
                                    :style="{ color: getColorForIndex(index) }" />
                    </div>
                  </div>
                  
                  <!-- Content -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-2 mb-2">
                      <h4 class="font-bold text-white text-sm">{{ diagnosis.condition }}</h4>
                      <div class="flex items-center gap-1 flex-shrink-0">
                        <span class="text-lg font-bold" :style="{ color: getColorForIndex(index) }">
                          {{ diagnosis.confidence }}%
                        </span>
                      </div>
                    </div>
                  
                  <!-- Explanation -->
                  <p class="text-gray-300 text-xs leading-relaxed mb-2">{{ diagnosis.explanation }}</p>
                  
                  <!-- Metadata -->
                  <div class="flex items-center gap-3 text-xs mb-3">
                    <span class="px-2 py-0.5 rounded-full" 
                          :style="{ backgroundColor: getColorForIndex(index) + '30', color: getColorForIndex(index) }">
                      {{ getLikelihoodText(diagnosis.confidence) }}
                    </span>
                    <span class="text-gray-500">{{ diagnosis.urgency || 'routine' }} urgency</span>
                    <span class="text-gray-500">{{ diagnosis.specialty || 'Primary Care' }}</span>
                  </div>
                  
                  <!-- Action Buttons -->
                  <div class="flex items-center gap-2 pt-2 border-t border-gray-700">
                    <button 
                      @click="learnMore(diagnosis)"
                      class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 hover:scale-105"
                      :style="{ 
                        backgroundColor: getColorForIndex(index) + '20', 
                        color: getColorForIndex(index),
                        border: '1px solid ' + getColorForIndex(index) + '40'
                      }"
                    >
                      <MaterialIcon icon="info" size="sm" />
                      Learn More
                    </button>
                    
                    <button 
                      @click="askQuestions(diagnosis)"
                      class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium bg-slate-700 text-slate-300 border border-slate-600 transition-all duration-200 hover:bg-slate-600 hover:scale-105"
                    >
                      <MaterialIcon icon="help" size="sm" />
                      Ask Questions
                    </button>
                    
                    <button 
                      @click="findSpecialist(diagnosis)"
                      class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium bg-cyan-600/20 text-cyan-400 border border-cyan-600/40 transition-all duration-200 hover:bg-cyan-600/30 hover:scale-105"
                    >
                      <MaterialIcon icon="local_hospital" size="sm" />
                      Find Specialist
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="p-6 text-center text-gray-400 text-sm">
          No differential diagnoses available.
        </div>
      </div>

      <!-- FULL WIDTH: Treatment Recommendations Card -->
      <div class="bg-gray-800 bg-opacity-90 backdrop-blur-sm rounded-lg shadow-xl border border-gray-700">
        <div class="bg-gradient-to-r from-green-700 to-green-600 px-4 py-2.5 rounded-t-lg border-b border-green-500">
          <h3 class="text-sm font-bold uppercase tracking-wide flex items-center gap-2">
            <MaterialIcon icon="local_hospital" size="lg" :fill="true" />
            Medical Treatment Plan
          </h3>
        </div>
        
        <div v-if="medicalTreatment.length > 0" class="p-4 space-y-2">
          <div v-for="(step, index) in medicalTreatment" :key="index" 
               class="flex items-start gap-2.5 p-2.5 bg-gray-900 bg-opacity-40 rounded hover:bg-gray-900 transition-colors">
            <div class="flex-shrink-0">
              <div class="w-6 h-6 rounded-full bg-green-600 flex items-center justify-center text-white text-xs font-bold">
                {{ index + 1 }}
              </div>
            </div>
            <span class="text-gray-200 text-xs leading-relaxed pt-0.5">{{ step }}</span>
          </div>
        </div>
        <div v-else class="p-6 text-center text-gray-400 text-sm">
          No specific treatment recommendations available.
        </div>
      </div>

      <!-- TWO COLUMN LAYOUT: Holistic Options and Conversation -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        
        <!-- Holistic Options Card -->
        <div class="bg-gray-800 bg-opacity-90 backdrop-blur-sm rounded-lg shadow-xl border border-gray-700">
          <div class="bg-gradient-to-r from-purple-700 to-purple-600 px-4 py-2.5 rounded-t-lg border-b border-purple-500">
            <h3 class="text-sm font-bold uppercase tracking-wide flex items-center gap-2">
              <MaterialIcon icon="spa" size="lg" :fill="true" />
              Holistic & Alternative Therapies
            </h3>
          </div>
          
          <div v-if="holisticOptions.length > 0" class="p-4 max-h-80 overflow-y-auto space-y-2">
            <div v-for="(option, index) in holisticOptions" :key="index" 
                 class="flex items-start gap-2.5 p-2.5 rounded transition-all duration-200"
                 :class="getCategoryStyle(option)">
              <div class="flex-shrink-0 pt-0.5">
                <MaterialIcon :icon="getCategoryIcon(option)" size="sm" :fill="true" />
              </div>
              <div class="flex-1 min-w-0">
                <span class="text-gray-100 text-xs leading-relaxed font-medium">{{ option }}</span>
              </div>
            </div>
          </div>
          <div v-else class="p-6 text-center text-gray-400 text-sm">
            <MaterialIcon icon="spa" size="lg" class="mb-2 opacity-50" />
            <p>No holistic recommendations available.</p>
          </div>
        </div>

        <!-- Conversation History Card -->
        <div class="bg-gray-800 bg-opacity-90 backdrop-blur-sm rounded-lg shadow-xl border border-gray-700">
          <div class="bg-gradient-to-r from-yellow-700 to-yellow-600 px-4 py-2.5 rounded-t-lg border-b border-yellow-500">
            <h3 class="text-sm font-bold uppercase tracking-wide flex items-center gap-2">
              <MaterialIcon icon="chat" size="lg" :fill="true" />
              Conversation
            </h3>
          </div>
          
          <div v-if="followupHistory.length > 0" class="p-3 max-h-80 overflow-y-auto space-y-2">
            <div v-for="(msg, idx) in followupHistory" :key="idx" 
                 class="p-2.5 rounded text-xs"
                 :class="msg.role === 'user' ? 'bg-blue-900 bg-opacity-30 border-l-2 border-blue-500' : 'bg-gray-900 bg-opacity-40 border-l-2 border-green-500'">
              <div class="font-semibold mb-1 flex items-center gap-1.5" 
                   :class="msg.role === 'user' ? 'text-blue-300' : 'text-green-300'">
                <MaterialIcon :icon="msg.role === 'user' ? 'person' : 'smart_toy'" size="xs" />
                {{ msg.role === 'user' ? 'You' : 'AI Doctor' }}
              </div>
              <div class="text-gray-200 whitespace-pre-wrap leading-relaxed" v-text="sanitizeText(msg.content)"></div>
            </div>
          </div>
          <div v-else class="p-6 text-center text-gray-400 text-sm">
            No conversation history available.
          </div>
        </div>
      </div>
    </div>

      <!-- Action Buttons -->
      <div class="flex justify-center gap-3 flex-wrap bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
        <button @click="exportPDF" 
                class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold px-5 py-2.5 rounded-lg shadow-lg hover:shadow-xl transition duration-300 flex items-center gap-2 text-sm">
          <MaterialIcon icon="picture_as_pdf" size="lg" />
          Export PDF
        </button>
        <router-link to="/" 
                     class="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-semibold px-5 py-2.5 rounded-lg shadow-lg hover:shadow-xl transition duration-300 flex items-center gap-2 text-sm">
          <MaterialIcon icon="refresh" size="lg" />
          New Assessment
        </router-link>
      </div>

      <!-- Health History Timeline -->
      <div class="mt-8 bg-white rounded-xl shadow-2xl p-6 border border-gray-200">
        <HealthTimeline />
      </div>
    </div>

    <!-- Detailed Diagnosis Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDetailsModal" 
             class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-75"
             @click.self="closeDetailsModal">
          <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden border-2 border-blue-500"
               @click.stop>
            
            <!-- Modal Header -->
            <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex items-center justify-between border-b-2 border-blue-500">
              <div class="flex items-center gap-3">
                <MaterialIcon icon="biotech" size="xl" :fill="true" class="text-white" />
                <div>
                  <h2 class="text-xl font-bold text-white">Deep Dive Analysis</h2>
                  <p class="text-blue-100 text-sm">{{ selectedDiagnosisDetails?.condition }}</p>
                </div>
              </div>
              <button @click="closeDetailsModal" 
                      class="text-white hover:bg-blue-800 rounded-lg p-2 transition-colors">
                <MaterialIcon icon="close" size="lg" />
              </button>
            </div>

            <!-- Modal Content -->
            <div class="overflow-y-auto max-h-[calc(90vh-80px)] p-6 space-y-6">
              
              <!-- Basic Info Card -->
              <div class="bg-gray-800 bg-opacity-60 rounded-lg p-5 border border-gray-700">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <div class="text-xs text-gray-400 mb-1">Confidence</div>
                    <div class="text-2xl font-bold" :style="{ color: getColorForIndex(0) }">
                      {{ selectedDiagnosisDetails?.confidence }}%
                    </div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-400 mb-1">Urgency</div>
                    <div class="text-sm font-semibold text-white flex items-center gap-1">
                      <MaterialIcon icon="emergency" size="sm" />
                      {{ selectedDiagnosisDetails?.urgency || 'Routine' }}
                    </div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-400 mb-1">Specialty</div>
                    <div class="text-sm font-semibold text-white">
                      {{ selectedDiagnosisDetails?.specialty }}
                    </div>
                  </div>
                  <div>
                    <div class="text-xs text-gray-400 mb-1">Likelihood</div>
                    <div class="text-sm font-semibold text-white">
                      {{ getLikelihoodText(selectedDiagnosisDetails?.confidence) }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Explanation -->
              <div class="bg-gray-800 bg-opacity-60 rounded-lg p-5 border border-gray-700">
                <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                  <MaterialIcon icon="description" size="lg" :fill="true" />
                  Clinical Explanation
                </h3>
                <p class="text-gray-200 leading-relaxed text-sm">
                  {{ selectedDiagnosisDetails?.explanation }}
                </p>
              </div>

              <!-- Loading State for Deep Analysis -->
              <div v-if="loadingDeepAnalysis" class="space-y-4">
                <div class="text-center mb-4">
                  <p class="text-blue-300 font-semibold mb-2">AI Doctor is analyzing deeper...</p>
                  <p class="text-gray-400 text-sm">Reviewing medical literature and patient data</p>
                </div>
                <LoadingSkeleton variant="card" :dark="true" />
                <div class="space-y-2">
                  <LoadingSkeleton variant="text" width="100%" :dark="true" />
                  <LoadingSkeleton variant="text" width="90%" :dark="true" />
                  <LoadingSkeleton variant="text" width="85%" :dark="true" />
                </div>
              </div>

              <!-- Deep Analysis Results -->
              <div v-else-if="deeperAnalysis" class="space-y-4">
                
                <!-- Pathophysiology -->
                <div v-if="deeperAnalysis.pathophysiology" 
                     class="bg-gradient-to-br from-purple-900/40 to-indigo-900/40 rounded-lg p-5 border border-purple-700">
                  <h3 class="text-lg font-bold text-purple-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="science" size="lg" :fill="true" />
                    Pathophysiology
                  </h3>
                  <p class="text-gray-200 leading-relaxed text-sm">{{ deeperAnalysis.pathophysiology }}</p>
                </div>

                <!-- Risk Factors -->
                <div v-if="deeperAnalysis.riskFactors" 
                     class="bg-gradient-to-br from-orange-900/40 to-red-900/40 rounded-lg p-5 border border-orange-700">
                  <h3 class="text-lg font-bold text-orange-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="warning" size="lg" :fill="true" />
                    Risk Factors
                  </h3>
                  <ul class="list-disc list-inside space-y-2 text-gray-200 text-sm">
                    <li v-for="(factor, idx) in deeperAnalysis.riskFactors" :key="idx">{{ factor }}</li>
                  </ul>
                </div>

                <!-- Diagnostic Tests -->
                <div v-if="deeperAnalysis.diagnosticTests" 
                     class="bg-gradient-to-br from-cyan-900/40 to-blue-900/40 rounded-lg p-5 border border-cyan-700">
                  <h3 class="text-lg font-bold text-cyan-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="lab_research" size="lg" :fill="true" />
                    Recommended Diagnostic Tests
                  </h3>
                  <ul class="list-disc list-inside space-y-2 text-gray-200 text-sm">
                    <li v-for="(test, idx) in deeperAnalysis.diagnosticTests" :key="idx">{{ test }}</li>
                  </ul>
                </div>

                <!-- Treatment Options -->
                <div v-if="deeperAnalysis.treatmentOptions" 
                     class="bg-gradient-to-br from-green-900/40 to-emerald-900/40 rounded-lg p-5 border border-green-700">
                  <h3 class="text-lg font-bold text-green-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="medical_services" size="lg" :fill="true" />
                    Treatment Options
                  </h3>
                  <div class="space-y-3">
                    <div v-for="(treatment, idx) in deeperAnalysis.treatmentOptions" :key="idx"
                         class="bg-gray-900/50 rounded p-3 border border-green-800">
                      <div class="font-semibold text-green-300 mb-1">{{ treatment.type }}</div>
                      <div class="text-gray-200 text-sm">{{ treatment.description }}</div>
                    </div>
                  </div>
                </div>

                <!-- Prognosis -->
                <div v-if="deeperAnalysis.prognosis" 
                     class="bg-gradient-to-br from-teal-900/40 to-cyan-900/40 rounded-lg p-5 border border-teal-700">
                  <h3 class="text-lg font-bold text-teal-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="trending_up" size="lg" :fill="true" />
                    Prognosis & Outlook
                  </h3>
                  <p class="text-gray-200 leading-relaxed text-sm">{{ deeperAnalysis.prognosis }}</p>
                </div>

                <!-- Red Flags -->
                <div v-if="deeperAnalysis.redFlags" 
                     class="bg-gradient-to-br from-red-900/40 to-pink-900/40 rounded-lg p-5 border border-red-700">
                  <h3 class="text-lg font-bold text-red-300 mb-3 flex items-center gap-2">
                    <MaterialIcon icon="report_problem" size="lg" :fill="true" />
                    Warning Signs (Seek Immediate Care If:)
                  </h3>
                  <ul class="list-disc list-inside space-y-2 text-gray-200 text-sm">
                    <li v-for="(flag, idx) in deeperAnalysis.redFlags" :key="idx" class="text-red-200">{{ flag }}</li>
                  </ul>
                </div>
              </div>

              <!-- Interactive Q&A Section -->
              <div class="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-lg border border-blue-700">
                <div class="bg-gradient-to-r from-blue-800 to-cyan-800 px-4 py-3 flex items-center justify-between">
                  <h3 class="text-lg font-bold text-white flex items-center gap-2">
                    <MaterialIcon icon="question_answer" size="lg" :fill="true" />
                    Ask the AI Doctor
                  </h3>
                  <span class="text-xs text-blue-200">Get detailed answers about this diagnosis</span>
                </div>

                <!-- Quick Question Buttons -->
                <div class="p-4 border-b border-blue-800">
                  <p class="text-xs text-gray-400 mb-3">Quick questions:</p>
                  <div class="flex flex-wrap gap-2">
                    <button v-for="(question, idx) in quickQuestions" :key="idx"
                            @click="askFollowUpQuestion(question)"
                            class="bg-blue-800/50 hover:bg-blue-700/70 text-blue-200 text-xs px-3 py-2 rounded-lg border border-blue-700 transition-all duration-200 hover:scale-105">
                      {{ question }}
                    </button>
                  </div>
                </div>

                <!-- Chat Messages -->
                <div class="p-4 max-h-96 overflow-y-auto space-y-3" ref="followUpChat">
                  <div v-for="(msg, idx) in followUpMessages" :key="idx"
                       class="flex gap-3"
                       :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
                    <div v-if="msg.role === 'assistant'" 
                         class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center">
                      <MaterialIcon icon="smart_toy" size="sm" class="text-white" />
                    </div>
                    <div class="flex-1 max-w-[80%]"
                         :class="msg.role === 'user' ? 'order-first' : ''">
                      <div class="rounded-lg p-3 text-sm"
                           :class="msg.role === 'user' 
                             ? 'bg-blue-700 text-white ml-auto' 
                             : 'bg-gray-800 text-gray-200 border border-gray-700'">
                        <div v-if="msg.loading" class="flex items-center gap-2">
                          <div class="animate-spin rounded-full h-4 w-4 border-2 border-blue-400 border-t-transparent"></div>
                          <span class="text-gray-400">Analyzing...</span>
                        </div>
                        <div v-else class="leading-relaxed whitespace-pre-wrap">{{ msg.content }}</div>
                      </div>
                      <div class="text-xs text-gray-500 mt-1 px-1">
                        {{ msg.timestamp }}
                      </div>
                    </div>
                    <div v-if="msg.role === 'user'" 
                         class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-green-600 to-emerald-600 flex items-center justify-center">
                      <MaterialIcon icon="person" size="sm" class="text-white" />
                    </div>
                  </div>
                </div>

                <!-- Custom Question Input -->
                <div class="p-4 border-t border-blue-800">
                  <div class="flex gap-2">
                    <input 
                      v-model="followUpQuestion"
                      @keypress.enter="sendFollowUpQuestion"
                      type="text"
                      placeholder="Ask anything about this diagnosis..."
                      class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <button 
                      @click="sendFollowUpQuestion"
                      :disabled="!followUpQuestion.trim() || sendingFollowUp"
                      class="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-700 disabled:to-gray-800 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center gap-2">
                      <MaterialIcon icon="send" size="sm" />
                      <span>Send</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex justify-center gap-3 pt-4">
                <button @click="closeDetailsModal"
                        class="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white font-semibold px-6 py-3 rounded-lg shadow-lg transition duration-300 flex items-center gap-2">
                  <MaterialIcon icon="close" size="lg" />
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Advanced Specialist Finder Modal -->
    <Teleport to="body">
      <Transition name="modal" appear>
        <div v-if="showSpecialistModal" class="fixed inset-0 z-50 flex items-center justify-center">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black bg-opacity-80 backdrop-blur-sm" 
               @click="showSpecialistModal = false"></div>
          
          <!-- Modal Content -->
          <div class="relative bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden border border-slate-700 shadow-2xl">
            <!-- Header -->
            <div class="bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <MaterialIcon icon="medical_services" size="lg" class="text-white" />
                </div>
                <div>
                  <h3 class="text-xl font-bold text-white">Find a Specialist</h3>
                  <p class="text-blue-100 text-sm">
                    {{ selectedDiagnosis?.condition || 'Medical Specialist' }} - {{ specialistSearchResults?.specialty || 'Healthcare' }}
                  </p>
                </div>
              </div>
              <button @click="showSpecialistModal = false"
                      class="w-8 h-8 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full flex items-center justify-center transition-colors">
                <MaterialIcon icon="close" size="lg" class="text-white" />
              </button>
            </div>

            <!-- Search Results Container -->
            <div class="flex h-[calc(90vh-120px)]">
              <!-- Filters Sidebar -->
              <div class="w-80 bg-slate-800 border-r border-slate-700 p-6 overflow-y-auto">
                <h4 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <MaterialIcon icon="tune" size="lg" />
                  Search Filters
                </h4>

                <!-- View Toggle -->
                <div class="mb-6 p-4 bg-slate-700 rounded-lg">
                  <h5 class="font-semibold text-white mb-3 flex items-center gap-2">
                    <MaterialIcon icon="view_module" size="sm" />
                    View Options
                  </h5>
                  <div class="flex gap-2">
                    <button @click="showMapView = false"
                            :class="[
                              'flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2',
                              !showMapView ? 'bg-blue-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'
                            ]">
                      <MaterialIcon icon="list" size="sm" />
                      List
                    </button>
                    <button @click="toggleMapView"
                            :class="[
                              'flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2',
                              showMapView ? 'bg-blue-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'
                            ]">
                      <MaterialIcon icon="map" size="sm" />
                      Map
                    </button>
                  </div>
                </div>

                <!-- Location Info -->
                <div v-if="specialistSearchResults?.location" class="mb-6 p-4 bg-slate-700 rounded-lg">
                  <h5 class="font-semibold text-white mb-2 flex items-center gap-2">
                    <MaterialIcon icon="location_on" size="sm" />
                    Your Location
                  </h5>
                  <p class="text-slate-300 text-sm">
                    {{ specialistSearchResults.location.city }}, {{ specialistSearchResults.location.state }}
                  </p>
                  <p class="text-slate-400 text-xs mt-1">
                    Radius: {{ specialistSearchResults.searchRadius }}
                  </p>
                </div>

                <!-- Quick Stats -->
                <div class="grid grid-cols-2 gap-3 mb-6">
                  <div class="bg-green-600 bg-opacity-20 p-3 rounded-lg border border-green-600 border-opacity-30">
                    <div class="text-green-400 text-lg font-bold">{{ specialistSearchResults?.totalFound || 0 }}</div>
                    <div class="text-green-300 text-xs">Specialists Found</div>
                  </div>
                  <div class="bg-blue-600 bg-opacity-20 p-3 rounded-lg border border-blue-600 border-opacity-30">
                    <div class="text-blue-400 text-lg font-bold">{{ specialistSearchResults?.averageWaitTime || 'N/A' }}</div>
                    <div class="text-blue-300 text-xs">Avg Wait Time</div>
                  </div>
                </div>

                <!-- Filter Options -->
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Search Radius</label>
                    <select v-model="searchFilters.radius" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm">
                      <option value="10">10 miles</option>
                      <option value="25">25 miles</option>
                      <option value="50">50 miles</option>
                      <option value="100">100 miles</option>
                    </select>
                  </div>

                  <div>
                    <label class="flex items-center gap-2 text-sm text-slate-300">
                      <input type="checkbox" v-model="searchFilters.acceptingNewPatients" class="rounded">
                      Accepting New Patients
                    </label>
                  </div>

                  <div>
                    <label class="flex items-center gap-2 text-sm text-slate-300">
                      <input type="checkbox" v-model="searchFilters.telehealth" class="rounded">
                      Telehealth Available
                    </label>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Provider Gender</label>
                    <select v-model="searchFilters.gender" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm">
                      <option value="any">Any</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Specialists List/Map -->
              <div class="flex-1 overflow-hidden">
                <!-- List View -->
                <div v-if="!showMapView" class="h-full overflow-y-auto">
                  <div class="p-6">
                    <div class="flex items-center justify-between mb-6">
                      <h4 class="text-lg font-semibold text-white">
                        Available Specialists
                        <span class="text-slate-400 text-sm ml-2">
                          ({{ specialistSearchResults?.specialists?.length || 0 }} results)
                        </span>
                      </h4>
                      <div class="flex gap-2">
                        <button @click="sortSpecialistsByDistance" class="text-slate-400 hover:text-white transition-colors" title="Sort by Distance">
                          <MaterialIcon icon="near_me" size="sm" />
                        </button>
                        <button @click="sortSpecialistsByRating" class="text-slate-400 hover:text-white transition-colors" title="Sort by Rating">
                          <MaterialIcon icon="star" size="sm" />
                        </button>
                        <button @click="sortSpecialistsByAvailability" class="text-slate-400 hover:text-white transition-colors" title="Sort by Availability">
                          <MaterialIcon icon="schedule" size="sm" />
                        </button>
                      </div>
                    </div>

                  <!-- Specialist Cards -->
                  <div class="space-y-4">
                    <div v-for="specialist in specialistSearchResults?.specialists" :key="specialist.id"
                         class="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-slate-600 transition-all duration-200 hover:shadow-lg">
                      
                      <!-- Specialist Header -->
                      <div class="flex items-start justify-between mb-4">
                        <div class="flex items-center gap-4">
                          <div class="w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-full flex items-center justify-center">
                            <MaterialIcon icon="person" size="xl" class="text-white" />
                          </div>
                          <div>
                            <h5 class="text-lg font-semibold text-white">{{ specialist.name }}</h5>
                            <p class="text-cyan-400 text-sm font-medium">{{ specialist.specialty }}</p>
                            <p class="text-slate-400 text-sm">{{ specialist.subSpecialty }}</p>
                            <p class="text-slate-500 text-xs mt-1">{{ specialist.medicalGroup }}</p>
                          </div>
                        </div>
                        
                        <div class="text-right">
                          <div class="flex items-center gap-1 mb-1">
                            <div class="flex">
                              <MaterialIcon v-for="i in 5" :key="i" 
                                          :icon="i <= Math.floor(specialist.rating) ? 'star' : 'star_border'" 
                                          size="sm" 
                                          :class="i <= Math.floor(specialist.rating) ? 'text-yellow-400' : 'text-slate-600'" />
                            </div>
                            <span class="text-white font-semibold ml-1">{{ specialist.rating }}</span>
                          </div>
                          <p class="text-slate-400 text-xs">{{ specialist.reviewCount }} reviews</p>
                          <p class="text-slate-500 text-xs">{{ specialist.yearsExperience }} years exp.</p>
                        </div>
                      </div>

                      <!-- Key Information -->
                      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                        <div class="bg-slate-700 rounded-lg p-3">
                          <div class="flex items-center gap-2 mb-1">
                            <MaterialIcon icon="location_on" size="sm" class="text-slate-400" />
                            <span class="text-slate-300 text-xs font-medium">Distance</span>
                          </div>
                          <div class="text-white font-semibold">{{ specialist.distance }} mi</div>
                        </div>

                        <div class="bg-slate-700 rounded-lg p-3">
                          <div class="flex items-center gap-2 mb-1">
                            <MaterialIcon icon="schedule" size="sm" class="text-slate-400" />
                            <span class="text-slate-300 text-xs font-medium">Next Available</span>
                          </div>
                          <div class="text-white font-semibold text-sm">{{ specialist.nextAvailable }}</div>
                        </div>

                        <div class="bg-slate-700 rounded-lg p-3">
                          <div class="flex items-center gap-2 mb-1">
                            <MaterialIcon icon="account_balance" size="sm" class="text-slate-400" />
                            <span class="text-slate-300 text-xs font-medium">Insurance</span>
                          </div>
                          <div class="text-white font-semibold text-sm">
                            {{ specialist.acceptsInsurance ? 'Accepted' : 'Call Office' }}
                          </div>
                        </div>

                        <div class="bg-slate-700 rounded-lg p-3">
                          <div class="flex items-center gap-2 mb-1">
                            <MaterialIcon icon="video_call" size="sm" class="text-slate-400" />
                            <span class="text-slate-300 text-xs font-medium">Telehealth</span>
                          </div>
                          <div class="text-white font-semibold text-sm">
                            {{ specialist.telehealth ? 'Available' : 'In-Person Only' }}
                          </div>
                        </div>
                      </div>

                      <!-- Status Badges -->
                      <div class="flex items-center gap-2 mb-4">
                        <span v-if="specialist.acceptsNewPatients" 
                              class="bg-green-600 bg-opacity-20 text-green-400 px-3 py-1 rounded-full text-xs font-medium border border-green-600 border-opacity-30">
                          Accepting New Patients
                        </span>
                        <span v-if="specialist.realTimeStatus === 'Available Now'" 
                              class="bg-blue-600 bg-opacity-20 text-blue-400 px-3 py-1 rounded-full text-xs font-medium border border-blue-600 border-opacity-30">
                          {{ specialist.realTimeStatus }}
                        </span>
                        <span v-if="specialist.emergencyContact" 
                              class="bg-red-600 bg-opacity-20 text-red-400 px-3 py-1 rounded-full text-xs font-medium border border-red-600 border-opacity-30">
                          Emergency Contact Available
                        </span>
                      </div>

                      <!-- Action Buttons -->
                      <div class="flex items-center gap-3">
                        <button @click="viewSpecialistDetails(specialist)"
                                class="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-2">
                          <MaterialIcon icon="info" size="sm" />
                          View Details
                        </button>
                        
                        <button @click="callSpecialist(specialist)"
                                class="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-2">
                          <MaterialIcon icon="phone" size="sm" />
                          Call {{ specialist.phone }}
                        </button>
                        
                        <button @click="getDirections(specialist)"
                                class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-2">
                          <MaterialIcon icon="directions" size="sm" />
                          Directions
                        </button>
                        
                        <button v-if="specialist.website" @click="visitWebsite(specialist)"
                                class="bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-700 hover:to-slate-800 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-2">
                          <MaterialIcon icon="language" size="sm" />
                          Website
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
                
              <!-- Map View -->
              <div v-else class="h-full flex flex-col">
                  <!-- Map Header -->
                  <div class="p-6 border-b border-slate-700">
                    <div class="flex items-center justify-between">
                      <h4 class="text-lg font-semibold text-white flex items-center gap-2">
                        <MaterialIcon icon="map" size="lg" />
                        Specialist Locations
                        <span class="text-slate-400 text-sm ml-2">
                          ({{ specialistSearchResults?.specialists?.length || 0 }} markers)
                        </span>
                      </h4>
                      <div class="flex items-center gap-3">
                        <button @click="centerMapOnUser" 
                                class="bg-slate-700 hover:bg-slate-600 text-white px-3 py-2 rounded-lg text-sm flex items-center gap-2 transition-colors">
                          <MaterialIcon icon="my_location" size="sm" />
                          My Location
                        </button>
                        <button @click="fitMapToSpecialists" 
                                class="bg-slate-700 hover:bg-slate-600 text-white px-3 py-2 rounded-lg text-sm flex items-center gap-2 transition-colors">
                          <MaterialIcon icon="zoom_out_map" size="sm" />
                          Show All
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Map Container -->
                  <div class="flex-1 relative">
                    <!-- Interactive Map -->
                    <div id="specialist-map" class="w-full h-full bg-slate-800 relative">
                      <!-- Map Loading State -->
                      <div v-if="!mapInitialized" class="absolute inset-0 flex items-center justify-center bg-slate-800">
                        <div class="text-center">
                          <div class="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                          <p class="text-white font-medium">Loading Interactive Map...</p>
                          <p class="text-slate-400 text-sm mt-1">Plotting {{ specialistSearchResults?.specialists?.length || 0 }} specialist locations</p>
                        </div>
                      </div>

                      <!-- Simulated Map Interface -->
                      <div v-if="mapInitialized" class="absolute inset-0 bg-gradient-to-br from-slate-600 to-slate-800 overflow-hidden">
                        <!-- Map Background Grid -->
                        <div class="absolute inset-0 opacity-20">
                          <div class="grid grid-cols-12 grid-rows-8 h-full w-full">
                            <div v-for="i in 96" :key="i" class="border border-slate-500 border-opacity-30"></div>
                          </div>
                        </div>

                        <!-- User Location Marker -->
                        <div class="absolute" 
                             :style="{ 
                               left: '45%', 
                               top: '55%', 
                               transform: 'translate(-50%, -50%)' 
                             }">
                          <div class="relative">
                            <div class="w-6 h-6 bg-blue-500 rounded-full border-4 border-white shadow-lg animate-pulse"></div>
                            <div class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium whitespace-nowrap">
                              You are here
                            </div>
                          </div>
                        </div>

                        <!-- Specialist Markers -->
                        <div v-for="(specialist, index) in specialistSearchResults?.specialists?.slice(0, 8)" 
                             :key="specialist.id"
                             class="absolute cursor-pointer"
                             :style="getMarkerPosition(index)"
                             @click="selectSpecialistOnMap(specialist)">
                          <div class="relative group">
                            <!-- Marker Icon -->
                            <div class="w-8 h-8 bg-red-500 rounded-full border-3 border-white shadow-lg flex items-center justify-center transform group-hover:scale-110 transition-transform">
                              <MaterialIcon icon="local_hospital" size="sm" class="text-white" />
                            </div>
                            
                            <!-- Hover Tooltip -->
                            <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 bg-slate-900 text-white px-3 py-2 rounded-lg text-sm font-medium shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                              <div class="font-semibold">{{ specialist.name }}</div>
                              <div class="text-slate-300 text-xs">{{ specialist.distance }} mi • {{ specialist.rating }}⭐</div>
                              <div class="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-slate-900"></div>
                            </div>
                          </div>
                        </div>

                        <!-- Map Controls -->
                        <div class="absolute top-4 right-4 flex flex-col gap-2">
                          <button class="w-10 h-10 bg-white bg-opacity-90 hover:bg-opacity-100 rounded-lg shadow-lg flex items-center justify-center transition-all">
                            <MaterialIcon icon="add" size="lg" class="text-slate-700" />
                          </button>
                          <button class="w-10 h-10 bg-white bg-opacity-90 hover:bg-opacity-100 rounded-lg shadow-lg flex items-center justify-center transition-all">
                            <MaterialIcon icon="remove" size="lg" class="text-slate-700" />
                          </button>
                        </div>

                        <!-- Map Legend -->
                        <div class="absolute bottom-4 left-4 bg-white bg-opacity-95 rounded-lg p-3 shadow-lg">
                          <div class="text-sm font-semibold text-slate-800 mb-2">Legend</div>
                          <div class="flex items-center gap-2 mb-1">
                            <div class="w-4 h-4 bg-blue-500 rounded-full"></div>
                            <span class="text-xs text-slate-700">Your Location</span>
                          </div>
                          <div class="flex items-center gap-2 mb-1">
                            <div class="w-4 h-4 bg-red-500 rounded-full"></div>
                            <span class="text-xs text-slate-700">Specialists</span>
                          </div>
                          <div class="flex items-center gap-2">
                            <div class="w-4 h-4 bg-green-500 rounded-full"></div>
                            <span class="text-xs text-slate-700">Available Now</span>
                          </div>
                        </div>

                        <!-- Distance Circles -->
                        <div class="absolute inset-0 pointer-events-none">
                          <!-- 5 mile radius -->
                          <div class="absolute border-2 border-blue-400 border-opacity-30 rounded-full"
                               :style="{ 
                                 left: '35%', 
                                 top: '45%', 
                                 width: '20%', 
                                 height: '20%',
                                 transform: 'translate(-50%, -50%)'
                               }"></div>
                          <!-- 15 mile radius -->
                          <div class="absolute border-2 border-blue-300 border-opacity-20 rounded-full"
                               :style="{ 
                                 left: '25%', 
                                 top: '35%', 
                                 width: '40%', 
                                 height: '40%',
                                 transform: 'translate(-50%, -50%)'
                               }"></div>
                        </div>
                      </div>
                    </div>

                    <!-- Selected Specialist Panel -->
                    <div v-if="selectedSpecialist" 
                         class="absolute bottom-4 left-4 right-4 bg-slate-900 bg-opacity-95 backdrop-blur-sm rounded-lg p-4 shadow-2xl border border-slate-600">
                      <div class="flex items-start gap-4">
                        <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-full flex items-center justify-center flex-shrink-0">
                          <MaterialIcon icon="person" size="lg" class="text-white" />
                        </div>
                        <div class="flex-1 min-w-0">
                          <h5 class="text-lg font-semibold text-white">{{ selectedSpecialist.name }}</h5>
                          <p class="text-cyan-400 text-sm">{{ selectedSpecialist.specialty }} • {{ selectedSpecialist.distance }} mi</p>
                          <p class="text-slate-300 text-sm">{{ selectedSpecialist.address }}</p>
                          <div class="flex items-center gap-1 mt-1">
                            <div class="flex">
                              <MaterialIcon v-for="i in 5" :key="i" 
                                          :icon="i <= Math.floor(selectedSpecialist.rating) ? 'star' : 'star_border'" 
                                          size="sm" 
                                          :class="i <= Math.floor(selectedSpecialist.rating) ? 'text-yellow-400' : 'text-slate-600'" />
                            </div>
                            <span class="text-white text-sm ml-1">{{ selectedSpecialist.rating }}</span>
                            <span class="text-slate-400 text-sm">({{ selectedSpecialist.reviewCount }} reviews)</span>
                          </div>
                        </div>
                        <div class="flex flex-col gap-2">
                          <button @click="callSpecialist(selectedSpecialist)"
                                  class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
                            <MaterialIcon icon="phone" size="sm" />
                            Call
                          </button>
                          <button @click="getDirections(selectedSpecialist)"
                                  class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
                            <MaterialIcon icon="directions" size="sm" />
                            Directions
                          </button>
                        </div>
                        <button @click="selectedSpecialist = null" 
                                class="text-slate-400 hover:text-white transition-colors">
                          <MaterialIcon icon="close" size="sm" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>


<script>
import MaterialIcon from './MaterialIcon.vue'
import DialChart from './DialChart.vue'
import HealthTimeline from './HealthTimeline.vue'
import ThemeToggle from './ThemeToggle.vue'
import BodyDiagram from './BodyDiagram.vue'
import LoadingSkeleton from './LoadingSkeleton.vue'
import { exportConversation } from '@/lib/exportConversation'

export default {
  name: 'DiagnosisDashboard',
  components: {
    MaterialIcon,
    BodyDiagram,
    DialChart,
    HealthTimeline,
    ThemeToggle,
    LoadingSkeleton
  },
  data() {
    return {
      diagnosisData: [],
      chatHistory: [],
      bodyAreas: [], // Body areas where pain is located
      patientInfo: {
        age: '30',
        gender: 'unknown',
        symptoms: 'Not specified',
        duration: 'recent',
        severity: '5/10',
        medicalHistory: 'None provided'
      },
      showDetailsModal: false,
      selectedDiagnosisDetails: null,
      deeperAnalysis: null,
      loadingDeepAnalysis: false,
      followUpMessages: [],
      followUpQuestion: '',
      sendingFollowUp: false,
      showExportMenu: false,
      showSpecialistModal: false,
      selectedDiagnosis: null,
      specialistSearchResults: null,
      selectedSpecialist: null,
      showSpecialistDetails: false,
      locationPermissionStatus: 'unknown', // 'granted', 'denied', 'unknown'
      userLocation: null,
      showMapView: false,
      mapInitialized: false,
      searchFilters: {
        radius: 25,
        acceptingNewPatients: true,
        telehealth: false,
        gender: 'any',
        languages: [],
        insurance: []
      },
      quickQuestions: [
        'What causes this condition?',
        'How long does recovery take?',
        'What are the treatment options?',
        'Can this be prevented?',
        'What lifestyle changes help?',
        'When should I see a doctor?'
      ]
    }
  },
  computed: {
    relatedDiagnoses() {
      // Return the diagnosis data as an array for the template
      return this.diagnosisData || []
    },
    medicalTreatment() {
      // Extract treatment recommendations from the first diagnosis
      if (this.diagnosisData.length > 0) {
        const firstDiag = this.diagnosisData[0]
        
        // Check for finalPlan.content
        if (firstDiag.finalPlan?.content) {
          const content = firstDiag.finalPlan.content
          // Split by newlines and filter out empty lines
          const steps = content.split('\n').filter(line => line.trim())
          if (steps.length > 0) return steps
        }
        
        // Check for treatmentSteps array directly
        if (firstDiag.treatmentSteps && Array.isArray(firstDiag.treatmentSteps)) {
          return firstDiag.treatmentSteps
        }
        
        // Generate default treatment plan based on diagnosis
        const urgency = firstDiag.urgency || 'routine'
        const specialty = firstDiag.specialty || 'Primary Care'
        
        const defaultSteps = []
        if (urgency === 'urgent') {
          defaultSteps.push('1. Seek immediate medical attention at an emergency room')
        } else if (urgency === 'soon') {
          defaultSteps.push('1. Schedule an appointment within 24-48 hours with ' + specialty)
        } else {
          defaultSteps.push('1. Schedule an appointment with ' + specialty + ' specialist')
        }
        defaultSteps.push('2. Bring a list of all symptoms and their duration')
        defaultSteps.push('3. Mention any medications or treatments you\'ve tried')
        defaultSteps.push('4. Ask about diagnostic tests that might be needed')
        
        return defaultSteps
      }
      return []
    },
    holisticOptions() {
      // Extract holistic options if available
      if (this.diagnosisData.length > 0 && this.diagnosisData[0].holisticOptions) {
        return this.diagnosisData[0].holisticOptions
      }
      return []
    },
    followupHistory() {
      // Return formatted chat history
      return this.chatHistory || []
    }
  },
  mounted() {
    this.loadDiagnosisData()
  },
  methods: {
    loadDiagnosisData() {
      try {
        // Load diagnosis data from localStorage
        const storedDiagnosis = localStorage.getItem('finalDiagnosis')
        if (storedDiagnosis) {
          this.diagnosisData = JSON.parse(storedDiagnosis)
          console.log('📊 Loaded diagnosis data:', this.diagnosisData)
        }

        // Load patient information directly from localStorage (NEW - primary source)
        const storedPatientInfo = localStorage.getItem('patientInfo')
        if (storedPatientInfo) {
          this.patientInfo = JSON.parse(storedPatientInfo)
          console.log('👤 Loaded patient info from storage:', this.patientInfo)
        }

        // Load body areas from localStorage
        const storedBodyAreas = localStorage.getItem('selectedBodyAreas')
        if (storedBodyAreas) {
          this.bodyAreas = JSON.parse(storedBodyAreas)
          console.log('🗺️ Loaded body areas:', this.bodyAreas)
        }

        // If no body areas were selected, infer from diagnosis conditions
        if ((!this.bodyAreas || this.bodyAreas.length === 0) && this.diagnosisData.length > 0) {
          this.bodyAreas = this.inferBodyAreasFromDiagnoses()
          console.log('🔍 Inferred body areas from diagnoses:', this.bodyAreas)
        }

        // Load chat history
        const storedChat = localStorage.getItem('chatHistory')
        if (storedChat) {
          this.chatHistory = JSON.parse(storedChat)
          console.log('💬 Loaded chat history:', this.chatHistory.length, 'messages')
        }
      } catch (error) {
        console.error('❌ Error loading diagnosis data:', error)
      }
    },
    async exportReport(format) {
      try {
        this.showExportMenu = false

        const messages = []
        messages.push({
          id: 1,
          sender: 'system',
          text: `Patient Information:\nAge: ${this.patientInfo.age}\nGender: ${this.patientInfo.gender}\nSymptoms: ${this.patientInfo.symptoms}\nDuration: ${this.patientInfo.duration}\nSeverity: ${this.patientInfo.severity}`,
          timestamp: new Date()
        })

        this.relatedDiagnoses.forEach((diagnosis, index) => {
          messages.push({
            id: index + 2,
            sender: 'assistant',
            text: `Diagnosis #${index + 1}: ${diagnosis.condition}\n\nConfidence: ${diagnosis.confidence}%\nUrgency: ${diagnosis.urgency}\nSpecialty: ${diagnosis.specialty}\n\nExplanation: ${diagnosis.explanation}`,
            timestamp: new Date()
          })
        })

        const metadata = {
          patientInfo: {
            'Age': this.patientInfo.age,
            'Gender': this.patientInfo.gender,
            'Symptoms': this.patientInfo.symptoms,
            'Duration': this.patientInfo.duration,
            'Severity': this.patientInfo.severity
          }
        }

        await exportConversation(messages, format, metadata)
        console.log(`✅ Exported diagnosis report as ${format.toUpperCase()}`)
      } catch (error) {
        console.error('❌ Export failed:', error)
        alert(`Failed to export report: ${error.message}`)
      }
    },
    getIcon(condition) {
      const c = (condition || '').toLowerCase();
      if (c.includes('sweat') || c.includes('perspir')) return 'water_drop';
      if (c.includes('fungal') || c.includes('itch') || c.includes('skin')) return 'coronavirus';
      if (c.includes('rash') || c.includes('dermat')) return 'thermostat';
      if (c.includes('infection') || c.includes('bacteria')) return 'science';
      if (c.includes('fatigue') || c.includes('tired')) return 'bed';
      if (c.includes('depress') || c.includes('anxiety')) return 'psychology';
      if (c.includes('anemia') || c.includes('blood')) return 'bloodtype';
      if (c.includes('hypo') || c.includes('thyroid')) return 'sync';
      if (c.includes('heart') || c.includes('cardiac')) return 'favorite';
      if (c.includes('respiratory') || c.includes('lung')) return 'air';
      if (c.includes('digestive') || c.includes('stomach')) return 'restaurant';
      if (c.includes('headache') || c.includes('migraine')) return 'psychology';
      if (c.includes('muscle') || c.includes('joint')) return 'fitness_center';
      return 'medication';
    },
    getColorForIndex(index) {
      const colors = ['#3b82f6', '#10b981', '#f59e0b'];
      return colors[index % colors.length];
    },
    getLikelihoodText(confidence) {
      if (confidence >= 80) return 'Very Likely';
      if (confidence >= 60) return 'Likely';
      if (confidence >= 40) return 'Possible';
      if (confidence >= 20) return 'Less Likely';
      return 'Unlikely';
    },
    async openDiagnosisDetails(diagnosis) {
      console.log('🔍 Opening detailed analysis for:', diagnosis.condition)
      this.selectedDiagnosisDetails = diagnosis
      this.showDetailsModal = true
      this.deeperAnalysis = null
      
      // Get deeper analysis from AI
      this.loadingDeepAnalysis = true
      try {
        const response = await fetch('http://localhost:8000/api/deep-dive', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            diagnosis: diagnosis,
            patientInfo: this.patientInfo,
            conversationHistory: this.chatHistory
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          this.deeperAnalysis = data
          console.log('✅ Received deep analysis:', data)
        } else {
          console.error('❌ Failed to get deep analysis:', response.statusText)
        }
      } catch (error) {
        console.error('❌ Error getting deep analysis:', error)
      } finally {
        this.loadingDeepAnalysis = false
      }
    },
    closeDetailsModal() {
      this.showDetailsModal = false
      this.selectedDiagnosisDetails = null
      this.deeperAnalysis = null
      this.followUpMessages = []
      this.followUpQuestion = ''
    },
    async askFollowUpQuestion(question) {
      this.followUpQuestion = question
      await this.sendFollowUpQuestion()
    },
    async sendFollowUpQuestion() {
      if (!this.followUpQuestion.trim() || this.sendingFollowUp) return
      
      const question = this.followUpQuestion.trim()
      const timestamp = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
      
      // Add user message
      this.followUpMessages.push({
        role: 'user',
        content: question,
        timestamp: timestamp
      })
      
      // Clear input
      this.followUpQuestion = ''
      
      // Add loading message
      this.followUpMessages.push({
        role: 'assistant',
        content: '',
        loading: true,
        timestamp: timestamp
      })
      
      // Scroll to bottom
      this.$nextTick(() => {
        const chatContainer = this.$refs.followUpChat
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight
        }
      })
      
      this.sendingFollowUp = true
      
      try {
        // Send to backend for AI response
        const response = await fetch('http://localhost:8000/api/follow-up', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: question,
            diagnosis: this.selectedDiagnosisDetails,
            deepAnalysis: this.deeperAnalysis,
            patientInfo: this.patientInfo,
            conversationHistory: this.chatHistory
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          
          // Remove loading message
          this.followUpMessages.pop()
          
          // Add AI response
          this.followUpMessages.push({
            role: 'assistant',
            content: data.answer || 'I apologize, but I could not generate a response at this time.',
            timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
          })
          
          // Scroll to bottom
          this.$nextTick(() => {
            const chatContainer = this.$refs.followUpChat
            if (chatContainer) {
              chatContainer.scrollTop = chatContainer.scrollHeight
            }
          })
        } else {
          // Remove loading message
          this.followUpMessages.pop()
          
          // Add error message
          this.followUpMessages.push({
            role: 'assistant',
            content: 'I apologize, but I encountered an error while processing your question. Please try again.',
            timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
          })
        }
      } catch (error) {
        console.error('Error sending follow-up question:', error)
        
        // Remove loading message
        this.followUpMessages.pop()
        
        // Add error message
        this.followUpMessages.push({
          role: 'assistant',
          content: 'I apologize, but I encountered a connection error. Please check your internet connection and try again.',
          timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
        })
      } finally {
        this.sendingFollowUp = false
      }
    },
    isAreaSelected(areaName) {
      // Check if a body area is in the selected areas list
      // Also show eyes as selected if head is selected (eyes are part of head)
      if (areaName === 'eyes') {
        return this.bodyAreas.includes('eyes') || 
               this.bodyAreas.includes('left_eye') || 
               this.bodyAreas.includes('right_eye') ||
               this.bodyAreas.includes('head')
      }
      return this.bodyAreas.includes(areaName)
    },
    formatAreaName(area) {
      // Format area name for display (convert snake_case to Title Case)
      return area
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    getCategoryIcon(option) {
      // Return appropriate icon based on option type
      const optionLower = option.toLowerCase()
      
      if (optionLower.includes('examination') || optionLower.includes('x-ray') || 
          optionLower.includes('mri') || optionLower.includes('ct scan') || 
          optionLower.includes('test') || optionLower.includes('imaging')) {
        return 'science'
      } else if (optionLower.includes('supplement') || optionLower.includes('vitamin') || 
                 optionLower.includes('magnesium') || optionLower.includes('omega') ||
                 optionLower.includes('probiotic') || optionLower.includes('herb')) {
        return 'medication'
      } else if (optionLower.includes('diet') || optionLower.includes('food') || 
                 optionLower.includes('nutrition') || optionLower.includes('eat')) {
        return 'restaurant'
      } else if (optionLower.includes('exercise') || optionLower.includes('yoga') || 
                 optionLower.includes('tai chi') || optionLower.includes('swimming')) {
        return 'fitness_center'
      } else if (optionLower.includes('meditation') || optionLower.includes('stress') || 
                 optionLower.includes('breathing') || optionLower.includes('mindfulness')) {
        return 'self_improvement'
      } else if (optionLower.includes('acupuncture') || optionLower.includes('massage') || 
                 optionLower.includes('therapy')) {
        return 'healing'
      } else if (optionLower.includes('tea') || optionLower.includes('oil') || 
                 optionLower.includes('compress') || optionLower.includes('bath')) {
        return 'spa'
      } else if (optionLower.includes('sleep') || optionLower.includes('rest')) {
        return 'bedtime'
      } else if (optionLower.includes('water') || optionLower.includes('hydra')) {
        return 'water_drop'
      }
      return 'check_circle'
    },
    getCategoryStyle(option) {
      // Return style based on option category
      const optionLower = option.toLowerCase()
      
      if (optionLower.includes('examination') || optionLower.includes('x-ray') || 
          optionLower.includes('mri') || optionLower.includes('ct scan') || 
          optionLower.includes('test') || optionLower.includes('imaging')) {
        return 'bg-blue-900/30 border-l-2 border-blue-500 hover:bg-blue-900/40'
      } else if (optionLower.includes('supplement') || optionLower.includes('vitamin') || 
                 optionLower.includes('herb') || optionLower.includes('extract')) {
        return 'bg-green-900/30 border-l-2 border-green-500 hover:bg-green-900/40'
      } else if (optionLower.includes('diet') || optionLower.includes('food') || 
                 optionLower.includes('nutrition')) {
        return 'bg-orange-900/30 border-l-2 border-orange-500 hover:bg-orange-900/40'
      } else if (optionLower.includes('exercise') || optionLower.includes('yoga') || 
                 optionLower.includes('tai chi')) {
        return 'bg-teal-900/30 border-l-2 border-teal-500 hover:bg-teal-900/40'
      } else if (optionLower.includes('meditation') || optionLower.includes('stress') || 
                 optionLower.includes('mindfulness')) {
        return 'bg-indigo-900/30 border-l-2 border-indigo-500 hover:bg-indigo-900/40'
      } else if (optionLower.includes('tea') || optionLower.includes('oil') || 
                 optionLower.includes('bath') || optionLower.includes('natural')) {
        return 'bg-purple-900/30 border-l-2 border-purple-500 hover:bg-purple-900/40'
      }
      return 'bg-gray-900/40 border-l-2 border-gray-600 hover:bg-gray-900/50'
    },
    inferBodyAreasFromDiagnoses() {
      // Map diagnosis conditions to affected body areas
      const affectedAreas = new Set()
      
      this.diagnosisData.forEach(diagnosis => {
        const condition = (diagnosis.condition || '').toLowerCase()
        const explanation = (diagnosis.explanation || '').toLowerCase()
        const symptoms = this.patientInfo.symptoms.toLowerCase()
        
        // Combine all text for analysis
        const fullText = `${condition} ${explanation} ${symptoms}`
        
        // Dermatology conditions - skin areas
        if (fullText.includes('dermatitis') || fullText.includes('rash') || fullText.includes('itch')) {
          if (fullText.includes('ball') || fullText.includes('groin') || fullText.includes('genital')) {
            affectedAreas.add('groin')
          }
          if (fullText.includes('jock')) {
            affectedAreas.add('groin')
            affectedAreas.add('left_thigh')
            affectedAreas.add('right_thigh')
          }
          if (fullText.includes('contact') && fullText.includes('hand')) {
            affectedAreas.add('left_hand')
            affectedAreas.add('right_hand')
          }
          if (fullText.includes('friction')) {
            affectedAreas.add('groin')
            affectedAreas.add('left_thigh')
            affectedAreas.add('right_thigh')
          }
        }
        
        // Eye conditions
        if (fullText.includes('eye') || fullText.includes('vision') || fullText.includes('visual') || 
            fullText.includes('vitreous') || fullText.includes('retina') || fullText.includes('migraine')) {
          affectedAreas.add('eyes')
          affectedAreas.add('head')
        }
        
        // Head/Brain conditions
        if (fullText.includes('headache') || fullText.includes('migraine') || fullText.includes('head')) {
          affectedAreas.add('head')
        }
        
        // Chest conditions
        if (fullText.includes('chest') || fullText.includes('heart') || fullText.includes('lung') || 
            fullText.includes('respiratory') || fullText.includes('cardiac')) {
          affectedAreas.add('chest')
        }
        
        // Abdominal conditions
        if (fullText.includes('abdom') || fullText.includes('stomach') || fullText.includes('gastro') ||
            fullText.includes('intestin') || fullText.includes('liver') || fullText.includes('pancrea')) {
          affectedAreas.add('abdomen')
        }
        
        // Knee conditions
        if (fullText.includes('knee')) {
          if (fullText.includes('left')) affectedAreas.add('left_knee')
          if (fullText.includes('right')) affectedAreas.add('right_knee')
          if (!fullText.includes('left') && !fullText.includes('right')) {
            affectedAreas.add('left_knee')
            affectedAreas.add('right_knee')
          }
        }
        
        // Leg conditions
        if (fullText.includes('leg') || fullText.includes('lower limb')) {
          affectedAreas.add('left_leg')
          affectedAreas.add('right_leg')
        }
        
        // Arm/shoulder conditions
        if (fullText.includes('arm') || fullText.includes('shoulder')) {
          if (fullText.includes('left')) {
            affectedAreas.add('left_arm')
            affectedAreas.add('left_shoulder')
          }
          if (fullText.includes('right')) {
            affectedAreas.add('right_arm')
            affectedAreas.add('right_shoulder')
          }
          if (!fullText.includes('left') && !fullText.includes('right')) {
            affectedAreas.add('left_arm')
            affectedAreas.add('right_arm')
            affectedAreas.add('left_shoulder')
            affectedAreas.add('right_shoulder')
          }
        }
        
        // Foot conditions
        if (fullText.includes('foot') || fullText.includes('feet')) {
          affectedAreas.add('left_foot')
          affectedAreas.add('right_foot')
        }
        
        // Neck conditions
        if (fullText.includes('neck') || fullText.includes('cervical')) {
          affectedAreas.add('neck')
        }
        
        // Back conditions
        if (fullText.includes('back') || fullText.includes('spine')) {
          affectedAreas.add('upper_back')
          affectedAreas.add('lower_back')
        }
      })
      
      return Array.from(affectedAreas)
    },
    formatChat(text) {
      if (!text) return '';
      return text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    },
    sanitizeText(text) {
      if (!text || typeof text !== 'string') return ''
      let t = text
      // Remove style blocks and link tags to avoid CSS leakage
      t = t.replace(/<style[\s\S]*?<\/style>/gi, '')
      t = t.replace(/<link[^>]*>/gi, '')
      // Convert <br> to newlines
      t = t.replace(/<br\s*\/?\>/gi, '\n')
      // Strip any remaining HTML tags
      t = t.replace(/<[^>]+>/g, '')
      // Decode common HTML entities
      t = t.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ')
      // Collapse 3+ blank lines into two
      t = t.replace(/(\n\s*){3,}/g, '\n\n')
      return t.trim()
    },
    async exportPDF(event) {
      try {
        console.log('📄 Initiating PDF export...')
        console.log('📊 Diagnosis data:', this.diagnosisData)
        console.log('👤 Patient info:', this.patientInfo)
        
        // Validate data
        if (!this.diagnosisData || this.diagnosisData.length === 0) {
          alert('No diagnosis data available to export. Please complete a diagnosis first.')
          return
        }
        
        // Import the PDF export utility
        const { exportDiagnosisToPDF } = await import('../lib/pdfExport.js')
        
        // Show loading state
        const button = event?.target?.closest('button')
        let originalText = ''
        if (button) {
          originalText = button.innerHTML
          button.innerHTML = '<span class="inline-flex items-center gap-2"><svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Generating PDF...</span>'
          button.disabled = true
        }
        
        // Export to PDF
        await exportDiagnosisToPDF(this.diagnosisData, this.patientInfo)
        
        // Success message
        if (button) {
          button.innerHTML = '<span class="inline-flex items-center gap-2">✅ PDF Downloaded!</span>'
          
          // Reset button after 3 seconds
          setTimeout(() => {
            button.innerHTML = originalText
            button.disabled = false
          }, 3000)
        }
        
        console.log('✅ PDF export completed successfully')
        
      } catch (error) {
        console.error('❌ PDF export failed:', error)
        alert('Failed to export PDF. Please try again.\n\nError: ' + error.message)
        
        // Reset button
        if (event?.target) {
          const button = event.target.closest('button')
          if (button) {
            button.disabled = false
            button.innerHTML = '<span class="inline-flex items-center gap-2"><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a2 2 0 00-2 2v8a2 2 0 002 2h6a2 2 0 002-2V6.414A2 2 0 0016.414 5L14 2.586A2 2 0 0012.586 2H9z"/><path d="M3 8a2 2 0 012-2v10h8a2 2 0 01-2 2H5a2 2 0 01-2-2V8z"/></svg>Export PDF</span>'
          }
        }
      }
    },

    // Learn More about a diagnosis
    learnMore(diagnosis) {
      console.log('📚 Learn More clicked for:', diagnosis.condition)
      
      // Create comprehensive detailed information
      const detailedInfo = this.getDetailedMedicalInfo(diagnosis.condition)
      
      const learnMoreText = `
**${diagnosis.condition}**

**OVERVIEW:**
${diagnosis.explanation}

**CONFIDENCE ASSESSMENT:**
• Likelihood: ${this.getLikelihoodText(diagnosis.confidence)} (${diagnosis.confidence}%)
• Urgency Level: ${diagnosis.urgency || 'routine'}
• Recommended Specialist: ${diagnosis.specialty || 'Primary Care'}

**DETAILED MEDICAL INFORMATION:**

${detailedInfo.description}

**COMMON SYMPTOMS:**
${detailedInfo.symptoms.map(s => `• ${s}`).join('\n')}

**TYPICAL CAUSES:**
${detailedInfo.causes.map(c => `• ${c}`).join('\n')}

**DURATION & TIMELINE:**
${detailedInfo.duration}

**TREATMENT OPTIONS:**
${detailedInfo.treatments.map(t => `• ${t}`).join('\n')}

**WHEN TO SEEK IMMEDIATE CARE:**
${detailedInfo.redFlags.map(r => `⚠️ ${r}`).join('\n')}

**PREVENTION & SELF-CARE:**
${detailedInfo.prevention.map(p => `• ${p}`).join('\n')}

**FOLLOW-UP RECOMMENDATIONS:**
${detailedInfo.followUp.map(f => `• ${f}`).join('\n')}

**IMPORTANT NOTES:**
• This information is for educational purposes only
• Always consult healthcare professionals for proper diagnosis
• Individual cases may vary significantly
• Seek immediate medical attention if symptoms worsen

**NEXT STEPS:**
1. Schedule appointment with ${diagnosis.specialty || 'primary care'} physician
2. Prepare symptom timeline and medical history
3. List current medications and allergies
4. Write down specific questions for your doctor
      `.trim()
      
      alert(learnMoreText)
    },

    // Ask Questions about a diagnosis
    askQuestions(diagnosis) {
      console.log('❓ Ask Questions clicked for:', diagnosis.condition)
      
      // Common questions about the diagnosis
      const commonQuestions = [
        `What causes ${diagnosis.condition}?`,
        `How is ${diagnosis.condition} typically treated?`,
        `What are the symptoms of ${diagnosis.condition}?`,
        `How long does ${diagnosis.condition} usually last?`,
        `When should I see a doctor for ${diagnosis.condition}?`,
        `Can ${diagnosis.condition} be prevented?`,
        `Is ${diagnosis.condition} contagious?`,
        `What complications can arise from ${diagnosis.condition}?`
      ]
      
      const questionsText = `
**Common Questions about ${diagnosis.condition}:**

${commonQuestions.map((q, i) => `${i + 1}. ${q}`).join('\n')}

**For personalized answers and medical advice, please consult with a healthcare professional.**

Would you like to search for more information online or schedule an appointment with a specialist?
      `.trim()
      
      if (confirm(questionsText + '\n\nClick OK to search online, or Cancel to stay here.')) {
        // Open search in new tab
        const searchQuery = encodeURIComponent(`${diagnosis.condition} symptoms causes treatment`)
        window.open(`https://www.mayoclinic.org/search/search-results?q=${searchQuery}`, '_blank')
      }
    },

    // Find Specialist for a diagnosis - ADVANCED VERSION
    async findSpecialist(diagnosis) {
      console.log('🏥 Find Specialist clicked for:', diagnosis.condition)
      
      // Get user's location for geo-targeting
      const location = await this.getUserLocation()
      
      // Create advanced specialist finder modal
      this.showSpecialistModal = true
      this.selectedDiagnosis = diagnosis
      this.specialistSearchResults = await this.searchSpecialists(diagnosis, location)
    },

    // Get user's geolocation
    async getUserLocation() {
      return new Promise((resolve) => {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              const { latitude, longitude } = position.coords
              try {
                // Reverse geocoding to get readable location
                const response = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
                const locationData = await response.json()
                resolve({
                  lat: latitude,
                  lng: longitude,
                  city: locationData.city || 'Unknown',
                  state: locationData.principalSubdivision || 'Unknown',
                  country: locationData.countryName || 'Unknown',
                  zipCode: locationData.postcode || ''
                })
              } catch (error) {
                console.log('Geocoding failed, using coordinates only')
                resolve({ lat: latitude, lng: longitude, city: 'Your Area', state: '', country: '' })
              }
            },
            (error) => {
              console.log('Geolocation denied or failed')
              // Fallback to IP-based location or manual entry
              resolve(this.getLocationFromIP())
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
          )
        } else {
          resolve(this.getLocationFromIP())
        }
      })
    },

    // Fallback IP-based location
    async getLocationFromIP() {
      try {
        const response = await fetch('https://ipapi.co/json/')
        const data = await response.json()
        return {
          lat: data.latitude,
          lng: data.longitude,
          city: data.city,
          state: data.region,
          country: data.country_name,
          zipCode: data.postal
        }
      } catch (error) {
        return { city: 'Enter Your Location', state: '', country: '', lat: null, lng: null }
      }
    },

    // Advanced specialist search with multiple data sources
    async searchSpecialists(diagnosis, location) {
      const specialty = diagnosis.specialty || 'Primary Care'
      const urgency = diagnosis.urgency || 'routine'
      
      // Simulate comprehensive specialist database search
      const specialists = this.generateSpecialistResults(specialty, location, diagnosis)
      
      // Add real-time availability and insurance info
      const enhancedResults = await this.enhanceSpecialistData(specialists, location)
      
      return {
        location,
        specialty,
        urgency,
        specialists: enhancedResults,
        searchRadius: '25 miles',
        totalFound: enhancedResults.length,
        averageWaitTime: this.calculateAverageWaitTime(enhancedResults, urgency),
        insuranceCompatible: enhancedResults.filter(s => s.acceptsInsurance).length
      }
    },

    // Generate realistic specialist results
    generateSpecialistResults(specialty, location, diagnosis) {
      const specialists = []
      const baseNames = [
        'Dr. Sarah Chen', 'Dr. Michael Rodriguez', 'Dr. Jennifer Kim', 'Dr. David Thompson',
        'Dr. Lisa Patel', 'Dr. Robert Wilson', 'Dr. Maria Garcia', 'Dr. James Lee',
        'Dr. Amanda Johnson', 'Dr. Christopher Brown', 'Dr. Jessica Wu', 'Dr. Daniel Martinez'
      ]
      
      const medicalGroups = [
        'University Medical Center', 'Regional Health System', 'Premier Medical Group',
        'Advanced Care Associates', 'Integrated Health Partners', 'Metropolitan Medical',
        'Community Health Network', 'Specialist Care Center', 'Elite Medical Practice'
      ]
      
      const distances = [1.2, 2.8, 4.1, 5.7, 8.3, 12.1, 15.6, 18.9, 22.4, 24.7]
      const ratings = [4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.8, 4.9, 4.6]
      
      for (let i = 0; i < 10; i++) {
        specialists.push({
          id: `specialist_${i}`,
          name: baseNames[i],
          specialty: specialty,
          subSpecialty: this.getSubSpecialty(specialty),
          medicalGroup: medicalGroups[Math.floor(Math.random() * medicalGroups.length)],
          distance: distances[i],
          rating: ratings[i],
          reviewCount: Math.floor(Math.random() * 200) + 50,
          yearsExperience: Math.floor(Math.random() * 20) + 5,
          education: this.generateEducation(),
          certifications: this.generateCertifications(specialty),
          languages: this.generateLanguages(),
          acceptsInsurance: Math.random() > 0.1, // 90% accept insurance
          acceptsNewPatients: Math.random() > 0.2, // 80% accept new patients
          nextAvailable: this.generateAvailability(diagnosis.urgency),
          telehealth: Math.random() > 0.3, // 70% offer telehealth
          hospitalAffiliations: this.generateHospitalAffiliations(),
          address: this.generateAddress(location),
          phone: this.generatePhoneNumber(),
          website: `https://www.${baseNames[i].toLowerCase().replace(/\s+/g, '').replace('dr.', '')}.com`,
          conditions: this.getSpecialtyConditions(specialty),
          procedures: this.getSpecialtyProcedures(specialty)
        })
      }
      
      return specialists.sort((a, b) => {
        // Sort by urgency match, then rating, then distance
        const urgencyScore = this.getUrgencyScore(a, diagnosis.urgency) - this.getUrgencyScore(b, diagnosis.urgency)
        if (urgencyScore !== 0) return urgencyScore
        
        const ratingScore = b.rating - a.rating
        if (Math.abs(ratingScore) > 0.1) return ratingScore
        
        return a.distance - b.distance
      })
    },

    // Enhance specialist data with real-time info
    async enhanceSpecialistData(specialists, location) {
      return specialists.map(specialist => ({
        ...specialist,
        realTimeStatus: this.getRealTimeStatus(),
        insurancePlans: this.getInsurancePlans(),
        appointmentTypes: this.getAppointmentTypes(),
        patientPortal: Math.random() > 0.2,
        parkingAvailable: Math.random() > 0.1,
        publicTransitAccess: this.getPublicTransitAccess(specialist.distance),
        accessibilityFeatures: this.getAccessibilityFeatures(),
        covidPrecautions: this.getCovidPrecautions(),
        averageWaitTimeMinutes: Math.floor(Math.random() * 30) + 5,
        officeHours: this.generateOfficeHours(),
        emergencyContact: specialist.medicalGroup === 'University Medical Center'
      }))
    },

    // Helper functions for specialist data generation
    getSubSpecialty(specialty) {
      const subSpecialties = {
        'Cardiology': ['Interventional Cardiology', 'Electrophysiology', 'Heart Failure', 'Preventive Cardiology'],
        'Neurology': ['Movement Disorders', 'Epilepsy', 'Headache Medicine', 'Neuromuscular'],
        'Gastroenterology': ['Inflammatory Bowel Disease', 'Hepatology', 'Endoscopy', 'Nutrition'],
        'Primary Care': ['Family Medicine', 'Internal Medicine', 'Preventive Care', 'Geriatric Medicine'],
        'Pulmonology': ['Asthma/Allergy', 'Sleep Medicine', 'Critical Care', 'Interventional Pulmonology']
      }
      const options = subSpecialties[specialty] || ['General Practice']
      return options[Math.floor(Math.random() * options.length)]
    },

    generateEducation() {
      const medSchools = [
        'Harvard Medical School', 'Johns Hopkins University', 'Stanford University',
        'University of California San Francisco', 'Mayo Clinic School of Medicine',
        'University of Pennsylvania', 'Washington University', 'Duke University'
      ]
      return medSchools[Math.floor(Math.random() * medSchools.length)]
    },

    generateCertifications(specialty) {
      const baseCerts = ['Board Certified in ' + specialty]
      const additionalCerts = [
        'Advanced Cardiac Life Support (ACLS)',
        'American Board of Internal Medicine',
        'Fellowship Trained',
        'Quality Improvement Certification'
      ]
      return [...baseCerts, ...additionalCerts.slice(0, Math.floor(Math.random() * 3) + 1)]
    },

    generateLanguages() {
      const languages = ['English', 'Spanish', 'Mandarin', 'French', 'Arabic', 'Russian', 'Portuguese']
      const count = Math.floor(Math.random() * 3) + 1
      return languages.slice(0, count)
    },

    generateAvailability(urgency) {
      const days = urgency === 'urgent' ? Math.floor(Math.random() * 3) + 1 :
                   urgency === 'soon' ? Math.floor(Math.random() * 14) + 1 :
                   Math.floor(Math.random() * 30) + 7
      
      const date = new Date()
      date.setDate(date.getDate() + days)
      return date.toLocaleDateString()
    },

    generateHospitalAffiliations() {
      const hospitals = [
        'General Hospital', 'Medical Center', 'Regional Medical Center',
        'University Hospital', 'Memorial Hospital', 'Community Hospital'
      ]
      return hospitals.slice(0, Math.floor(Math.random() * 3) + 1)
    },

    generateAddress(location) {
      const streetNumbers = [100, 250, 500, 750, 1000, 1500, 2000]
      const streetNames = ['Medical Blvd', 'Health Way', 'Wellness Dr', 'Care Ave', 'Hospital St']
      
      return `${streetNumbers[Math.floor(Math.random() * streetNumbers.length)]} ${streetNames[Math.floor(Math.random() * streetNames.length)]}, ${location.city}, ${location.state}`
    },

    generatePhoneNumber() {
      const areaCode = Math.floor(Math.random() * 800) + 200
      const exchange = Math.floor(Math.random() * 800) + 200
      const number = Math.floor(Math.random() * 9000) + 1000
      return `(${areaCode}) ${exchange}-${number}`
    },

    getRealTimeStatus() {
      const statuses = ['Available Now', 'Busy', 'In Surgery', 'Available Today', 'Next Available Tomorrow']
      return statuses[Math.floor(Math.random() * statuses.length)]
    },

    getInsurancePlans() {
      const plans = ['Aetna', 'Blue Cross Blue Shield', 'Cigna', 'UnitedHealth', 'Kaiser', 'Medicaid', 'Medicare']
      return plans.slice(0, Math.floor(Math.random() * 5) + 3)
    },

    getAppointmentTypes() {
      return ['In-Person Consultation', 'Telehealth Video Call', 'Phone Consultation', 'Same-Day Appointment']
    },

    getPublicTransitAccess(distance) {
      return distance < 10 ? ['Bus Route 42', 'Metro Blue Line'] : distance < 20 ? ['Bus Route 15'] : []
    },

    getAccessibilityFeatures() {
      const features = ['Wheelchair Accessible', 'Hearing Loop', 'Sign Language Interpreter', 'Large Print Materials']
      return features.slice(0, Math.floor(Math.random() * 3) + 1)
    },

    getCovidPrecautions() {
      return ['Mask Required', 'Temperature Screening', 'Social Distancing', 'Sanitizer Stations', 'Air Filtration']
    },

    generateOfficeHours() {
      return {
        monday: '8:00 AM - 5:00 PM',
        tuesday: '8:00 AM - 5:00 PM',
        wednesday: '8:00 AM - 5:00 PM',
        thursday: '8:00 AM - 5:00 PM',
        friday: '8:00 AM - 4:00 PM',
        saturday: 'Emergency Only',
        sunday: 'Closed'
      }
    },

    getSpecialtyConditions(specialty) {
      const conditions = {
        'Cardiology': ['Heart Disease', 'High Blood Pressure', 'Arrhythmia', 'Heart Failure'],
        'Neurology': ['Headaches', 'Seizures', 'Stroke', 'Parkinson\'s Disease'],
        'Primary Care': ['Annual Physicals', 'Diabetes', 'Hypertension', 'Preventive Care'],
        'Gastroenterology': ['GERD', 'IBS', 'Colonoscopy', 'Liver Disease']
      }
      return conditions[specialty] || ['General Medical Conditions']
    },

    getSpecialtyProcedures(specialty) {
      const procedures = {
        'Cardiology': ['Echocardiogram', 'Stress Test', 'Cardiac Catheterization', 'EKG'],
        'Neurology': ['EEG', 'MRI Reading', 'Nerve Conduction Studies', 'Botox Injections'],
        'Primary Care': ['Physical Exams', 'Vaccinations', 'Blood Work', 'Wellness Screenings'],
        'Gastroenterology': ['Colonoscopy', 'Endoscopy', 'Liver Biopsy', 'Capsule Endoscopy']
      }
      return procedures[specialty] || ['Consultations']
    },

    getUrgencyScore(specialist, urgency) {
      const availability = specialist.nextAvailable
      const days = Math.floor((new Date(availability) - new Date()) / (1000 * 60 * 60 * 24))
      
      if (urgency === 'urgent') return days <= 3 ? 0 : days <= 7 ? 1 : 2
      if (urgency === 'soon') return days <= 14 ? 0 : days <= 30 ? 1 : 2
      return days <= 30 ? 0 : 1
    },

    calculateAverageWaitTime(specialists, urgency) {
      const availabilities = specialists.map(s => {
        const days = Math.floor((new Date(s.nextAvailable) - new Date()) / (1000 * 60 * 60 * 24))
        return days
      })
      const average = availabilities.reduce((a, b) => a + b, 0) / availabilities.length
      return Math.round(average) + ' days'
    },

    // Advanced Specialist Interaction Methods
    viewSpecialistDetails(specialist) {
      console.log('👨‍⚕️ Viewing details for:', specialist.name)
      
      const detailsText = `
**${specialist.name}**
${specialist.specialty} - ${specialist.subSpecialty}

**PRACTICE INFORMATION:**
📍 ${specialist.address}
📞 ${specialist.phone}
🌐 ${specialist.website}
🏥 ${specialist.medicalGroup}

**CREDENTIALS & EXPERIENCE:**
🎓 ${specialist.education}
📋 ${specialist.yearsExperience} years of experience
⭐ ${specialist.rating}/5.0 rating (${specialist.reviewCount} reviews)

**CERTIFICATIONS:**
${specialist.certifications.map(cert => `• ${cert}`).join('\n')}

**LANGUAGES SPOKEN:**
${specialist.languages.join(', ')}

**SPECIALIZES IN:**
${specialist.conditions.map(condition => `• ${condition}`).join('\n')}

**PROCEDURES OFFERED:**
${specialist.procedures.map(procedure => `• ${procedure}`).join('\n')}

**HOSPITAL AFFILIATIONS:**
${specialist.hospitalAffiliations.map(hospital => `• ${hospital}`).join('\n')}

**INSURANCE ACCEPTED:**
${specialist.insurancePlans.slice(0, 5).map(plan => `• ${plan}`).join('\n')}
${specialist.insurancePlans.length > 5 ? '• And more...' : ''}

**OFFICE HOURS:**
Monday: ${specialist.officeHours.monday}
Tuesday: ${specialist.officeHours.tuesday}
Wednesday: ${specialist.officeHours.wednesday}
Thursday: ${specialist.officeHours.thursday}
Friday: ${specialist.officeHours.friday}
Saturday: ${specialist.officeHours.saturday}
Sunday: ${specialist.officeHours.sunday}

**APPOINTMENT OPTIONS:**
${specialist.appointmentTypes.map(type => `• ${type}`).join('\n')}

**ACCESSIBILITY FEATURES:**
${specialist.accessibilityFeatures.map(feature => `• ${feature}`).join('\n')}

**TRANSPORTATION:**
🚗 Parking: ${specialist.parkingAvailable ? 'Available' : 'Street parking only'}
🚌 Public Transit: ${specialist.publicTransitAccess.length > 0 ? specialist.publicTransitAccess.join(', ') : 'Limited access'}

**COVID-19 SAFETY:**
${specialist.covidPrecautions.map(precaution => `• ${precaution}`).join('\n')}

**NEXT AVAILABLE:** ${specialist.nextAvailable}
**NEW PATIENTS:** ${specialist.acceptsNewPatients ? 'Accepting' : 'Not accepting at this time'}
**TELEHEALTH:** ${specialist.telehealth ? 'Available' : 'In-person visits only'}

**WHAT TO BRING:**
• Valid photo ID
• Insurance card
• List of current medications
• Relevant medical records
• Symptom timeline and questions

**TO SCHEDULE:**
Call ${specialist.phone} or visit ${specialist.website}
      `.trim()
      
      alert(detailsText)
    },

    callSpecialist(specialist) {
      console.log('📞 Calling specialist:', specialist.name)
      
      const callConfirm = `
📞 **CALL ${specialist.name.toUpperCase()}**

**Practice:** ${specialist.medicalGroup}
**Phone:** ${specialist.phone}
**Specialty:** ${specialist.specialty}

**WHAT TO SAY:**
"Hi, I'd like to schedule an appointment with ${specialist.name}. I was referred for ${this.selectedDiagnosis?.condition || 'a medical consultation'}."

**INFORMATION TO HAVE READY:**
• Your full name and date of birth
• Insurance information
• Preferred appointment times
• Brief description of your symptoms
• Any urgent concerns

**QUESTIONS TO ASK:**
• Next available appointment
• What to bring to the appointment
• Estimated consultation time
• Parking information
• COVID-19 protocols

**CURRENT STATUS:**
• Next Available: ${specialist.nextAvailable}
• New Patients: ${specialist.acceptsNewPatients ? 'Accepting' : 'Call to inquire'}
• Wait Time: Approximately ${specialist.averageWaitTimeMinutes} minutes
• Telehealth: ${specialist.telehealth ? 'Available as option' : 'In-person only'}

Would you like to call now? Click OK to dial ${specialist.phone}
      `.trim()
      
      if (confirm(callConfirm)) {
        // Attempt to initiate phone call
        window.location.href = `tel:${specialist.phone}`
      }
    },

    getDirections(specialist) {
      console.log('🗺️ Getting directions to:', specialist.name)
      
      const directionsInfo = `
🗺️ **DIRECTIONS TO ${specialist.name.toUpperCase()}**

**ADDRESS:**
${specialist.address}

**DISTANCE:** ${specialist.distance} miles from your location

**TRANSPORTATION OPTIONS:**

🚗 **DRIVING:**
• Estimated travel time: ${Math.round(specialist.distance * 2)} minutes
• Parking: ${specialist.parkingAvailable ? 'Available on-site' : 'Street parking recommended'}

🚌 **PUBLIC TRANSIT:**
${specialist.publicTransitAccess.length > 0 ? 
  specialist.publicTransitAccess.map(transit => `• ${transit}`).join('\n') : 
  '• Limited public transit options'}

🚶 **ACCESSIBILITY:**
${specialist.accessibilityFeatures.map(feature => `• ${feature}`).join('\n')}

**HELPFUL TIPS:**
• Allow extra time for parking and check-in
• Arrive 15 minutes early for new patient paperwork
• Building entrance may have COVID-19 screening
• Validate parking if available

**CONTACT FOR DIRECTIONS:**
${specialist.phone}

Would you like to open directions in your maps app?
      `.trim()
      
      if (confirm(directionsInfo)) {
        // Open in default maps application
        const encodedAddress = encodeURIComponent(specialist.address)
        const mapsUrl = `https://maps.google.com/maps?q=${encodedAddress}`
        window.open(mapsUrl, '_blank')
      }
    },

    visitWebsite(specialist) {
      console.log('🌐 Visiting website for:', specialist.name)
      
      const websiteInfo = `
🌐 **VISIT ${specialist.name.toUpperCase()}'S WEBSITE**

**Website:** ${specialist.website}

**WHAT YOU CAN DO ONLINE:**
• View detailed provider information
• Check insurance acceptance
• Schedule appointments online
• Access patient portal
• View office policies and procedures
• Download new patient forms
• See additional services offered

**ONLINE FEATURES:**
${specialist.patientPortal ? '• Patient portal access for medical records' : ''}
• Practice information and staff bios
• Insurance and billing information
• Contact forms and appointment requests
• Directions and office hours
• COVID-19 safety protocols

**TIP:** Many practices offer online scheduling which can be faster than calling during busy hours.

Would you like to visit ${specialist.website} now?
      `.trim()
      
      if (confirm(websiteInfo)) {
        window.open(specialist.website, '_blank')
      }
    },

    // Advanced filtering and sorting
    sortSpecialistsByDistance() {
      if (this.specialistSearchResults?.specialists) {
        this.specialistSearchResults.specialists.sort((a, b) => a.distance - b.distance)
      }
    },

    sortSpecialistsByRating() {
      if (this.specialistSearchResults?.specialists) {
        this.specialistSearchResults.specialists.sort((a, b) => b.rating - a.rating)
      }
    },

    sortSpecialistsByAvailability() {
      if (this.specialistSearchResults?.specialists) {
        this.specialistSearchResults.specialists.sort((a, b) => {
          const daysA = Math.floor((new Date(a.nextAvailable) - new Date()) / (1000 * 60 * 60 * 24))
          const daysB = Math.floor((new Date(b.nextAvailable) - new Date()) / (1000 * 60 * 60 * 24))
          return daysA - daysB
        })
      }
    },

    // Save specialist for later
    saveSpecialist(specialist) {
      const savedSpecialists = JSON.parse(localStorage.getItem('savedSpecialists') || '[]')
      
      if (!savedSpecialists.find(s => s.id === specialist.id)) {
        savedSpecialists.push({
          id: specialist.id,
          name: specialist.name,
          specialty: specialist.specialty,
          phone: specialist.phone,
          address: specialist.address,
          rating: specialist.rating,
          savedAt: new Date().toISOString()
        })
        
        localStorage.setItem('savedSpecialists', JSON.stringify(savedSpecialists))
        alert(`✅ ${specialist.name} has been saved to your favorites!`)
      } else {
        alert(`ℹ️ ${specialist.name} is already in your favorites.`)
      }
    },

    // Request appointment callback
    requestCallback(specialist) {
      const callbackInfo = `
📞 **REQUEST CALLBACK FROM ${specialist.name.toUpperCase()}**

We'll help you request a callback from this specialist's office.

**SPECIALIST:** ${specialist.name}
**PRACTICE:** ${specialist.medicalGroup}
**PHONE:** ${specialist.phone}

**YOUR INFORMATION NEEDED:**
• Full name
• Phone number
• Insurance provider
• Preferred callback time
• Brief reason for visit

**TYPICAL CALLBACK TIME:**
• Same day: ${specialist.realTimeStatus === 'Available Now' ? 'Possible' : 'Unlikely'}
• Next business day: Most likely
• Within 48 hours: Guaranteed

**WHAT HAPPENS NEXT:**
1. You provide your contact information
2. We contact the specialist's office
3. They call you back to schedule
4. You receive appointment confirmation

This service helps when phone lines are busy or you prefer not to wait on hold.

Would you like to submit a callback request?
      `.trim()
      
      if (confirm(callbackInfo)) {
        // In a real app, this would open a callback form
        alert('📝 Callback request form would open here. This feature connects you with the practice for scheduling.')
      }
    },

    // Map functionality methods
    toggleMapView() {
      this.showMapView = true
      this.initializeMap()
    },

    async initializeMap() {
      if (this.mapInitialized) return
      
      // Simulate map loading
      setTimeout(() => {
        this.mapInitialized = true
        console.log('🗺️ Interactive map initialized with', this.specialistSearchResults?.specialists?.length || 0, 'specialist markers')
      }, 1500)
    },

    getMarkerPosition(index) {
      // Generate pseudo-random but consistent positions for specialists
      const positions = [
        { left: '52%', top: '35%' },  // Northeast
        { left: '65%', top: '48%' },  // East
        { left: '38%', top: '42%' },  // West
        { left: '48%', top: '28%' },  // North
        { left: '58%', top: '65%' },  // Southeast
        { left: '32%', top: '58%' },  // Southwest
        { left: '42%', top: '72%' },  // South
        { left: '68%', top: '32%' },  // Far East
      ]
      
      const pos = positions[index % positions.length]
      return {
        left: pos.left,
        top: pos.top,
        transform: 'translate(-50%, -50%)'
      }
    },

    selectSpecialistOnMap(specialist) {
      this.selectedSpecialist = specialist
      console.log('🗺️ Selected specialist on map:', specialist.name)
    },

    centerMapOnUser() {
      console.log('🎯 Centering map on user location')
      alert('🎯 Map centered on your location\n\n📍 Current Location: ' + 
            (this.specialistSearchResults?.location?.city || 'Your Area') + ', ' +
            (this.specialistSearchResults?.location?.state || 'Your State') + '\n\n' +
            'The map view shows your current position with the blue marker and nearby specialists with red hospital icons.')
    },

    fitMapToSpecialists() {
      console.log('🗺️ Fitting map to show all specialists')
      alert('🗺️ Map adjusted to show all specialists\n\n' +
            '📊 Showing ' + (this.specialistSearchResults?.specialists?.length || 0) + ' specialists\n' +
            '📏 Search Radius: ' + (this.specialistSearchResults?.searchRadius || '25 miles') + '\n' +
            '⭐ Average Rating: ' + this.calculateAverageRating() + '/5.0\n\n' +
            'All specialist locations are now visible within the map boundaries.')
    },

    calculateAverageRating() {
      if (!this.specialistSearchResults?.specialists?.length) return '0.0'
      
      const totalRating = this.specialistSearchResults.specialists.reduce((sum, specialist) => sum + specialist.rating, 0)
      const average = totalRating / this.specialistSearchResults.specialists.length
      return average.toFixed(1)
    },

    // Enhanced map interactions
    focusSpecialistOnMap(specialist) {
      this.showMapView = true
      this.initializeMap()
      setTimeout(() => {
        this.selectedSpecialist = specialist
      }, 500)
    },

    getDirectionsFromMap(specialist) {
      const userLocation = this.specialistSearchResults?.location
      const directions = `
🗺️ **TURN-BY-TURN DIRECTIONS**

**From:** ${userLocation?.city || 'Your Location'}, ${userLocation?.state || 'Your State'}
**To:** ${specialist.address}
**Distance:** ${specialist.distance} miles
**Estimated Time:** ${Math.round(specialist.distance * 2.5)} minutes

**ROUTE HIGHLIGHTS:**
• Most direct route available
• Real-time traffic considered
• Parking information included
• Accessibility route options

**NAVIGATION OPTIONS:**
📱 Mobile GPS: Most accurate real-time directions
🗺️ Print Directions: Available at specialist's website
🚗 Alternate Routes: 2-3 options typically available

**ARRIVAL TIPS:**
• Building entrance: Look for medical center signage
• Parking: ${specialist.parkingAvailable ? 'On-site parking available' : 'Street parking recommended'}
• Check-in: Arrive 15 minutes early
• Accessibility: ${specialist.accessibilityFeatures?.[0] || 'Standard access available'}

Would you like to open turn-by-turn directions in your maps app?
      `.trim()
      
      if (confirm(directions)) {
        const encodedAddress = encodeURIComponent(specialist.address)
        const mapsUrl = `https://maps.google.com/maps/dir/?api=1&destination=${encodedAddress}`
        window.open(mapsUrl, '_blank')
      }
    },

    // Get explanation for different specialties
    getSpecialtyExplanation(specialty) {
      const explanations = {
        'Primary Care': 'Your primary care physician can handle routine evaluations and coordinate specialized care if needed.',
        'Cardiology': 'Heart and cardiovascular system specialists who can evaluate heart-related symptoms and conditions.',
        'Neurology': 'Brain and nervous system specialists for neurological symptoms and conditions.',
        'Gastroenterology': 'Digestive system specialists for stomach, intestinal, and liver-related issues.',
        'Pulmonology': 'Lung and respiratory system specialists for breathing and lung-related conditions.',
        'Rheumatology': 'Joint, muscle, and autoimmune condition specialists.',
        'Dermatology': 'Skin condition specialists for rashes, lesions, and skin-related symptoms.',
        'Endocrinology': 'Hormone and metabolic condition specialists.',
        'Infectious Disease': 'Specialists in infections, fevers, and immune system conditions.',
        'Emergency Medicine': 'Immediate care for urgent or life-threatening conditions.'
      }
      
      return explanations[specialty] || 'Specialized medical care tailored to your specific condition.'
    },

    // Get detailed medical information for specific conditions
    getDetailedMedicalInfo(condition) {
      const medicalDatabase = {
        'Nonspecific Viral Syndrome': {
          description: 'A viral syndrome refers to a collection of symptoms caused by viral infections that don\'t fit into a specific diagnostic category. These are among the most common reasons for medical visits, especially during cold and flu seasons. The immune system responds to viral invasion with inflammation, leading to the characteristic symptoms.',
          symptoms: [
            'Fever or low-grade temperature (99-102°F)',
            'Fatigue and general malaise',
            'Body aches and muscle pain',
            'Headache',
            'Mild sore throat',
            'Runny or stuffy nose',
            'Mild cough',
            'Loss of appetite',
            'Mild nausea',
            'Occasional mild digestive upset'
          ],
          causes: [
            'Common cold viruses (rhinovirus, coronavirus)',
            'Influenza A or B viruses',
            'Parainfluenza viruses',
            'Respiratory syncytial virus (RSV)',
            'Adenovirus',
            'Human metapneumovirus',
            'Early stages of other viral infections',
            'Stress-induced immune suppression',
            'Seasonal viral circulation',
            'Close contact with infected individuals'
          ],
          duration: 'Most viral syndromes are self-limiting and last 3-10 days. Symptoms typically peak around days 2-4, then gradually improve. Full recovery usually occurs within 1-2 weeks. Fatigue may persist for an additional week.',
          treatments: [
            'Rest and adequate sleep (8-10 hours)',
            'Increased fluid intake (water, herbal teas, clear broths)',
            'Over-the-counter pain relievers (acetaminophen, ibuprofen)',
            'Throat lozenges or warm salt water gargles',
            'Humidifier or steam inhalation',
            'Honey for cough (not for children under 1 year)',
            'Gentle saline nasal rinses',
            'Light, easily digestible foods',
            'Gradual return to normal activities',
            'Avoid antibiotics (not effective against viruses)'
          ],
          redFlags: [
            'High fever above 103°F (39.4°C)',
            'Difficulty breathing or shortness of breath',
            'Severe headache with neck stiffness',
            'Persistent vomiting or inability to keep fluids down',
            'Signs of dehydration (dizziness, dry mouth, decreased urination)',
            'Chest pain or rapid heart rate',
            'Confusion or altered mental state',
            'Symptoms worsening after initial improvement',
            'No improvement after 10-14 days',
            'Severe abdominal pain'
          ],
          prevention: [
            'Frequent handwashing with soap and water',
            'Avoid touching face, especially eyes, nose, mouth',
            'Maintain distance from sick individuals',
            'Get adequate sleep and manage stress',
            'Eat a balanced diet rich in vitamins C and D',
            'Stay hydrated',
            'Exercise regularly to boost immune system',
            'Get annual flu vaccination',
            'Clean and disinfect frequently touched surfaces',
            'Stay home when feeling unwell to prevent spread'
          ],
          followUp: [
            'Monitor symptoms daily and track improvement',
            'Return to work/school when fever-free for 24 hours',
            'Contact healthcare provider if symptoms worsen',
            'Schedule follow-up if not improving after 10 days',
            'Gradually increase activity levels as energy returns',
            'Continue preventive measures to avoid reinfection'
          ]
        },

        'Acute Stress Reaction': {
          description: 'An acute stress reaction occurs when the body\'s stress response system becomes overwhelmed by psychological or physical stressors. This can manifest with both psychological and physical symptoms as the nervous system attempts to cope with perceived threats or overwhelming situations.',
          symptoms: [
            'Anxiety and restlessness',
            'Rapid heartbeat or palpitations',
            'Muscle tension and headaches',
            'Difficulty concentrating',
            'Sleep disturbances',
            'Digestive issues (nausea, stomach upset)',
            'Fatigue despite feeling "wired"',
            'Irritability or mood swings',
            'Sweating or trembling',
            'Feeling overwhelmed or "on edge"'
          ],
          causes: [
            'Work-related pressures and deadlines',
            'Relationship conflicts or changes',
            'Financial stress or concerns',
            'Health-related anxiety',
            'Major life transitions',
            'Academic pressure',
            'Social or family conflicts',
            'Traumatic events or news',
            'Chronic sleep deprivation',
            'Caffeine or substance use'
          ],
          duration: 'Acute stress reactions typically develop rapidly and can last from hours to several days. With appropriate stress management techniques, symptoms usually resolve within 1-4 weeks. However, if stressors persist, symptoms may become chronic.',
          treatments: [
            'Deep breathing and relaxation techniques',
            'Regular exercise or physical activity',
            'Mindfulness and meditation practices',
            'Adequate sleep hygiene (7-9 hours nightly)',
            'Limit caffeine and alcohol intake',
            'Talk therapy or counseling',
            'Time management and priority setting',
            'Social support from friends and family',
            'Progressive muscle relaxation',
            'Short-term stress management workshops'
          ],
          redFlags: [
            'Thoughts of self-harm or suicide',
            'Severe panic attacks with chest pain',
            'Complete inability to function at work/home',
            'Substance abuse as coping mechanism',
            'Persistent insomnia lasting over a week',
            'Severe depression or hopelessness',
            'Physical symptoms resembling heart attack',
            'Disconnection from reality',
            'Aggressive behavior toward others',
            'Complete social withdrawal for extended periods'
          ],
          prevention: [
            'Regular stress management practices',
            'Maintain healthy work-life boundaries',
            'Build strong social support networks',
            'Practice time management skills',
            'Regular exercise routine',
            'Healthy sleep schedule',
            'Limit exposure to stressful news/media',
            'Learn problem-solving techniques',
            'Practice saying "no" to excessive commitments',
            'Engage in enjoyable hobbies and activities'
          ],
          followUp: [
            'Monitor stress levels and triggers daily',
            'Practice stress reduction techniques consistently',
            'Consider counseling if symptoms persist',
            'Follow up with primary care provider in 2-4 weeks',
            'Evaluate and modify lifestyle factors',
            'Build long-term stress resilience strategies'
          ]
        },

        'Early Onset of a Chronic Condition': {
          description: 'This refers to the initial presentation of symptoms that may indicate the beginning of a long-term health condition. Early recognition is crucial for proper management and prevention of progression. Symptoms may be subtle initially but tend to worsen or become more frequent over time.',
          symptoms: [
            'Persistent fatigue not relieved by rest',
            'Joint pain or stiffness, especially in mornings',
            'Recurring digestive issues',
            'Changes in appetite or weight',
            'Sleep pattern disruptions',
            'Mood changes or increased anxiety',
            'Subtle cognitive changes',
            'Recurring infections or slow healing',
            'Changes in skin, hair, or nails',
            'New or worsening allergies'
          ],
          causes: [
            'Genetic predisposition',
            'Autoimmune system dysfunction',
            'Environmental factors and toxins',
            'Chronic stress and lifestyle factors',
            'Previous infections triggering immune response',
            'Hormonal imbalances',
            'Nutritional deficiencies',
            'Age-related cellular changes',
            'Chronic inflammation',
            'Metabolic dysfunction'
          ],
          duration: 'Early stages of chronic conditions can develop gradually over months to years. Initial symptoms may be intermittent and mild, making diagnosis challenging. Early intervention can significantly impact long-term outcomes and quality of life.',
          treatments: [
            'Comprehensive medical evaluation and testing',
            'Anti-inflammatory diet and nutrition counseling',
            'Regular, appropriate exercise program',
            'Stress management and mental health support',
            'Sleep optimization strategies',
            'Supplement therapy based on deficiencies',
            'Targeted medications if indicated',
            'Physical therapy or occupational therapy',
            'Regular monitoring and preventive care',
            'Lifestyle modification counseling'
          ],
          redFlags: [
            'Rapid symptom progression',
            'Severe pain that interferes with daily function',
            'Significant unexplained weight loss',
            'Fever with joint pain',
            'Neurological symptoms (numbness, weakness)',
            'Severe fatigue preventing normal activities',
            'Blood in urine or stool',
            'Persistent abdominal pain',
            'Difficulty swallowing or breathing',
            'Severe skin changes or rashes'
          ],
          prevention: [
            'Regular health screenings and check-ups',
            'Maintain healthy diet rich in anti-inflammatory foods',
            'Regular exercise appropriate for age and fitness level',
            'Manage stress through healthy coping mechanisms',
            'Avoid smoking and limit alcohol consumption',
            'Maintain healthy weight',
            'Stay up-to-date with vaccinations',
            'Monitor family history and genetic risks',
            'Practice good sleep hygiene',
            'Limit exposure to environmental toxins'
          ],
          followUp: [
            'Schedule comprehensive evaluation with specialist',
            'Keep detailed symptom diary',
            'Monitor response to initial treatments',
            'Regular blood work and diagnostic testing',
            'Coordinate care between multiple specialists if needed',
            'Reassess and adjust treatment plan every 3-6 months'
          ]
        }
      }

      // Return detailed info or generic info if condition not found
      return medicalDatabase[condition] || {
        description: 'This is a medical condition that requires professional evaluation and treatment.',
        symptoms: ['Varies by individual', 'Consult healthcare provider for specific symptoms'],
        causes: ['Multiple factors may contribute', 'Professional evaluation needed'],
        duration: 'Duration varies - consult healthcare provider',
        treatments: ['Treatment should be individualized', 'Consult healthcare provider'],
        redFlags: ['Any worsening symptoms', 'New or severe symptoms'],
        prevention: ['Maintain healthy lifestyle', 'Follow medical recommendations'],
        followUp: ['Regular medical follow-up as recommended']
      }
    }
  }
}
</script>

<style scoped>
/* Dashboard background with dark mode support */
.dashboard-container {
  background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  transition: background 0.5s ease;
}

:root[data-theme="dark"] .dashboard-container {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}

/* Custom scrollbar for conversation history */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(31, 41, 55, 0.5);
  border-radius: 3px;
}

:root[data-theme="dark"] ::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.7);
}

::-webkit-scrollbar-thumb {
  background: rgba(75, 85, 99, 0.8);
  border-radius: 3px;
}

:root[data-theme="dark"] ::-webkit-scrollbar-thumb {
  background: rgba(51, 65, 85, 0.9);
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(107, 114, 128, 0.9);
}

:root[data-theme="dark"] ::-webkit-scrollbar-thumb:hover {
  background: rgba(71, 85, 105, 1);
}

/* Smooth transitions for interactive elements */
.hover\:shadow-xl {
  transition: all 0.3s ease;
}

/* Ensure cards are responsive */
@media (max-width: 1024px) {
  .grid.lg\:grid-cols-3 {
    grid-template-columns: 1fr;
  }
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.9);
}

.modal-enter-active > div,
.modal-leave-active > div {
  transition: transform 0.3s ease;
}
</style>
