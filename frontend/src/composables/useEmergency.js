import { ref } from 'vue'

/**
 * Emergency Detection Composable
 * Detects critical symptoms that require immediate medical attention
 */
export function useEmergency() {
  const showEmergency = ref(false)
  const emergencyType = ref('')
  const emergencyMessage = ref('')
  const emergencyCategory = ref('')

  /**
   * Emergency keywords database
   */
  const emergencyKeywords = {
    cardiac: {
      keywords: [
        'chest pain', 'heart attack', 'crushing chest', 'chest pressure',
        'chest tightness', 'arm pain radiating', 'jaw pain with chest',
        'heart racing severely', 'irregular heartbeat severe'
      ],
      type: 'CARDIAC EMERGENCY',
      message: '🚨 You may be experiencing a CARDIAC EMERGENCY. Call 911 immediately if you have chest pain, especially with arm/jaw pain, shortness of breath, or sweating.',
      priority: 1
    },
    respiratory: {
      keywords: [
        'can\'t breathe', 'cannot breathe', 'difficulty breathing severe',
        'shortness of breath severe', 'choking', 'suffocating',
        'turning blue', 'gasping for air', 'lips blue', 'face blue'
      ],
      type: 'RESPIRATORY EMERGENCY',
      message: '🚨 SEVERE BREATHING DIFFICULTY detected. Call 911 immediately if you cannot breathe properly, are gasping for air, or have blue lips/face.',
      priority: 1
    },
    stroke: {
      keywords: [
        'stroke', 'face drooping', 'arm weakness sudden', 'speech difficulty sudden',
        'slurred speech sudden', 'sudden confusion', 'sudden severe headache',
        'vision loss sudden', 'numbness one side', 'paralysis one side',
        'can\'t move arm', 'can\'t move leg', 'facial droop'
      ],
      type: 'POSSIBLE STROKE',
      message: '🚨 STROKE WARNING SIGNS detected (F.A.S.T.: Face drooping, Arm weakness, Speech difficulty, Time to call 911). Stroke is time-critical - call 911 NOW.',
      priority: 1
    },
    bleeding: {
      keywords: [
        'severe bleeding', 'won\'t stop bleeding', 'bleeding heavily',
        'bleeding profusely', 'blood gushing', 'spurting blood',
        'uncontrollable bleeding', 'hemorrhaging'
      ],
      type: 'SEVERE BLEEDING',
      message: '🚨 SEVERE BLEEDING detected. Apply direct pressure and call 911 immediately. Do not remove objects embedded in wounds.',
      priority: 1
    },
    trauma: {
      keywords: [
        'severe injury', 'head injury severe', 'unconscious', 'unresponsive',
        'seizure', 'convulsing', 'fell from height', 'car accident',
        'motorcycle accident', 'major trauma', 'broken neck', 'spinal injury'
      ],
      type: 'SEVERE TRAUMA',
      message: '🚨 SEVERE INJURY/TRAUMA detected. Call 911 immediately. Do not move the person unless in immediate danger.',
      priority: 1
    },
    poisoning: {
      keywords: [
        'overdose', 'poisoned', 'ingested poison', 'chemical exposure',
        'swallowed bleach', 'carbon monoxide', 'drug overdose',
        'too many pills', 'accidental ingestion'
      ],
      type: 'POISONING/OVERDOSE',
      message: '🚨 POISONING/OVERDOSE detected. Call 911 and Poison Control (1-800-222-1222) immediately. Do not induce vomiting unless instructed.',
      priority: 1
    },
    allergic: {
      keywords: [
        'anaphylaxis', 'throat closing', 'swelling throat', 'severe allergic reaction',
        'epipen', 'can\'t swallow', 'tongue swelling', 'throat swelling',
        'airway closing', 'allergic shock'
      ],
      type: 'ANAPHYLAXIS',
      message: '🚨 SEVERE ALLERGIC REACTION (Anaphylaxis) detected. Use EpiPen if available and call 911 immediately. This is life-threatening.',
      priority: 1
    },
    abdominal: {
      keywords: [
        'severe abdominal pain', 'stomach pain severe', 'vomiting blood',
        'blood in vomit', 'black tarry stool', 'rectal bleeding severe',
        'appendix burst', 'stabbing abdominal pain'
      ],
      type: 'SEVERE ABDOMINAL EMERGENCY',
      message: '🚨 SEVERE ABDOMINAL EMERGENCY detected. Call 911 if you have severe pain, vomiting blood, or signs of internal bleeding.',
      priority: 2
    },
    neurological: {
      keywords: [
        'worst headache of life', 'thunderclap headache', 'sudden blindness',
        'double vision sudden', 'loss of consciousness', 'altered mental state',
        'extreme confusion', 'hallucinations severe'
      ],
      type: 'NEUROLOGICAL EMERGENCY',
      message: '🚨 NEUROLOGICAL EMERGENCY detected. Call 911 if experiencing sudden severe headache, vision changes, or altered consciousness.',
      priority: 2
    },
    pregnancy: {
      keywords: [
        'pregnant bleeding', 'pregnancy bleeding severe', 'severe pregnancy pain',
        'baby not moving', 'contractions severe early', 'water broke early',
        'preeclampsia', 'pregnancy emergency'
      ],
      type: 'PREGNANCY EMERGENCY',
      message: '🚨 PREGNANCY EMERGENCY detected. Call 911 or go to emergency room immediately for severe pregnancy complications.',
      priority: 1
    }
  }

  /**
   * Detect emergency conditions in user message
   */
  function detectEmergency(message) {
    if (!message || typeof message !== 'string') {
      return null
    }

    const msg = message.toLowerCase()
    let detectedEmergency = null
    let highestPriority = Infinity

    // Check each emergency category
    for (const [category, data] of Object.entries(emergencyKeywords)) {
      for (const keyword of data.keywords) {
        if (msg.includes(keyword)) {
          // Use highest priority (lowest number) emergency
          if (data.priority < highestPriority) {
            highestPriority = data.priority
            detectedEmergency = {
              type: data.type,
              message: data.message,
              category,
              priority: data.priority
            }
          }

          console.log('🚨 EMERGENCY DETECTED:', category, keyword)
        }
      }
    }

    return detectedEmergency
  }

  /**
   * Show emergency alert
   */
  function showAlert(emergency) {
    if (!emergency) return

    emergencyType.value = emergency.type
    emergencyMessage.value = emergency.message
    emergencyCategory.value = emergency.category
    showEmergency.value = true

    console.log('🚨 Emergency alert displayed:', emergency.type)

    return emergency
  }

  /**
   * Dismiss emergency alert
   */
  function dismissAlert() {
    showEmergency.value = false
    console.log('✅ Emergency alert dismissed')
  }

  /**
   * Reset emergency state
   */
  function reset() {
    showEmergency.value = false
    emergencyType.value = ''
    emergencyMessage.value = ''
    emergencyCategory.value = ''
  }

  /**
   * Check if message contains emergency keywords
   */
  function hasEmergencyKeywords(message) {
    const emergency = detectEmergency(message)
    return emergency !== null
  }

  /**
   * Get emergency priority level (1 = highest, 3 = lowest)
   */
  function getEmergencyPriority(message) {
    const emergency = detectEmergency(message)
    return emergency?.priority || null
  }

  /**
   * Add custom emergency keyword
   */
  function addCustomKeyword(category, keyword, data) {
    if (!emergencyKeywords[category]) {
      emergencyKeywords[category] = {
        keywords: [],
        type: data.type || 'EMERGENCY',
        message: data.message || 'Emergency detected. Seek immediate medical attention.',
        priority: data.priority || 3
      }
    }

    emergencyKeywords[category].keywords.push(keyword)
    console.log(`✅ Added custom emergency keyword: ${keyword} to ${category}`)
  }

  return {
    // State
    showEmergency,
    emergencyType,
    emergencyMessage,
    emergencyCategory,

    // Methods
    detectEmergency,
    showAlert,
    dismissAlert,
    reset,
    hasEmergencyKeywords,
    getEmergencyPriority,
    addCustomKeyword
  }
}
