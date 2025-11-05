import { ref, computed } from 'vue'

/**
 * Medical Questionnaire Composable
 * Manages the medical questionnaire flow and validation
 */
export function useQuestionnaire() {
  const isPetPatient = ref(false)
  const petType = ref('')

  const questions = [
    {
      id: 'age',
      text: "What is your age?",
      type: 'number',
      validation: (value) => {
        // Check if this is about a pet
        const petKeywords = ['dog', 'cat', 'pet', 'puppy', 'kitten', 'fish', 'bird', 'rabbit', 'hamster', 'guinea pig', 'ferret', 'reptile', 'snake', 'lizard', 'turtle', 'parrot', 'canary']
        const valueLower = value.toLowerCase()
        
        if (petKeywords.some(keyword => valueLower.includes(keyword))) {
          isPetPatient.value = true
          // Extract pet type
          for (const keyword of petKeywords) {
            if (valueLower.includes(keyword)) {
              petType.value = keyword
              break
            }
          }
          return { 
            valid: false, 
            error: `I appreciate you reaching out! However, I'm designed to provide health assessments for humans only. For your ${petType.value}, I strongly recommend consulting with a licensed veterinarian who can properly examine and treat your pet. Veterinary care is essential for accurate diagnosis and treatment of animals. 🐾` 
          }
        }

        const ageMatch = value.match(/\b(\d+)\b/)
        if (!ageMatch) {
          return { valid: false, error: 'Please provide your age as a number (e.g., 25).' }
        }
        const age = parseInt(ageMatch[1])
        if (age < 1 || age > 120) {
          return { valid: false, error: 'Please provide a valid age between 1 and 120.' }
        }
        return { valid: true }
      }
    },
    {
      id: 'gender',
      text: "What is your biological sex assigned at birth? (Male, Female, or prefer not to say)",
      type: 'open',
      validation: (value) => {
        // Check if this is about a pet
        const petKeywords = ['dog', 'cat', 'pet', 'puppy', 'kitten', 'fish', 'bird', 'rabbit', 'hamster', 'guinea pig', 'ferret', 'reptile', 'snake', 'lizard', 'turtle', 'parrot', 'canary']
        const valueLower = value.toLowerCase()
        
        if (petKeywords.some(keyword => valueLower.includes(keyword))) {
          isPetPatient.value = true
          for (const keyword of petKeywords) {
            if (valueLower.includes(keyword)) {
              petType.value = keyword
              break
            }
          }
          return { 
            valid: false, 
            error: `I appreciate you reaching out! However, I'm designed to provide health assessments for humans only. For your ${petType.value}, I strongly recommend consulting with a licensed veterinarian who can properly examine and treat your pet. Veterinary care is essential for accurate diagnosis and treatment of animals. 🐾` 
          }
        }

        const validGenders = ['male', 'female', 'man', 'woman', 'm', 'f', 'non-binary', 'nonbinary', 'other', 'prefer not to say', 'prefer not', 'rather not']
        const genderLower = value.toLowerCase().trim()
        const isValidGender = validGenders.some(g => genderLower.includes(g) || genderLower === g)
        if (!isValidGender && value.length < 2) {
          return { valid: false, error: 'Please specify your biological sex (e.g., male, female, or prefer not to say).' }
        }
        return { valid: true }
      }
    },
    {
      id: 'symptoms',
      text: "What brings you here today? Please describe your main symptoms or health concerns in as much detail as possible.",
      type: 'open',
      validation: (value) => {
        if (value.length < 5) {
          return { valid: false, error: 'Please provide more detail about your symptoms (at least 5 characters).' }
        }
        
        // Check if it's just gibberish or non-medical text
        if (/^[^a-zA-Z]*$/.test(value) || /^(.)\1+$/.test(value)) {
          return { valid: false, error: 'Please describe your symptoms using words.' }
        }

        // Check if this is about a pet with phrases like "my dog", "my cat", etc.
        const petPhrases = [
          /my (dog|cat|pet|puppy|kitten|fish|bird|rabbit|hamster|guinea pig|ferret|reptile|snake|lizard|turtle|parrot|canary)/i,
          /the (dog|cat|pet|puppy|kitten|fish|bird|rabbit|hamster|guinea pig|ferret|reptile|snake|lizard|turtle|parrot|canary)/i,
          /(dog|cat|pet|puppy|kitten|fish|bird|rabbit|hamster|guinea pig|ferret|reptile|snake|lizard|turtle|parrot|canary) (is|has|seems|appears|looks)/i,
          /(dog|cat|pet|puppy|kitten|fish|bird|rabbit|hamster|guinea pig|ferret|reptile|snake|lizard|turtle|parrot|canary)'s/i
        ]
        
        for (const pattern of petPhrases) {
          const match = value.match(pattern)
          if (match) {
            const detectedPet = match[1] || 'pet'
            isPetPatient.value = true
            petType.value = detectedPet
            return { 
              valid: false, 
              error: `I appreciate you reaching out about your ${detectedPet}! However, I'm designed to provide health assessments for humans only. For your ${detectedPet}, I strongly recommend consulting with a licensed veterinarian who can properly examine and treat your pet. Veterinary care is essential for accurate diagnosis and treatment of animals. 🐾\n\nIf you have personal health concerns, I'm here to help with those!` 
            }
          }
        }
        
        return { valid: true }
      }
    },
    {
      id: 'duration',
      text: "How long have you been experiencing these symptoms?",
      type: 'duration',
      options: ['Just started (less than 1 hour)', 'Few hours', '1-2 days', '3-7 days', '1-2 weeks', 'Several weeks', 'Months or longer'],
      validation: (value) => ({ valid: true }) // Accept any time description
    },
    {
      id: 'severity',
      text: "On a scale of 1-10, how severe are your symptoms? (1 = very mild, barely noticeable | 10 = extremely severe, unbearable)",
      type: 'scale',
      validation: (value) => {
        const severityMatch = value.match(/\b(\d+)\b/)
        if (!severityMatch) {
          return { valid: false, error: 'Please provide a number between 1 and 10 to rate the severity.' }
        }
        const severity = parseInt(severityMatch[1])
        if (severity < 1 || severity > 10) {
          return { valid: false, error: 'Please provide a severity rating between 1 and 10.' }
        }
        return { valid: true }
      }
    },
    {
      id: 'medical_history',
      text: "Do you have any relevant medical history, current medications, or allergies I should know about? Also, is there anything specific that triggered these symptoms or makes them better/worse?",
      type: 'open',
      validation: (value) => ({ valid: true }) // Accept any response
    }
  ]

  const currentQuestionIndex = ref(0)
  const userResponses = ref({})
  const isComplete = ref(false)

  const currentQuestion = computed(() => {
    if (currentQuestionIndex.value < questions.length) {
      return questions[currentQuestionIndex.value]
    }
    return null
  })

  const progress = computed(() => ({
    current: currentQuestionIndex.value,
    total: questions.length,
    percentage: Math.round((currentQuestionIndex.value / questions.length) * 100)
  }))

  /**
   * Get the next question text
   */
  function getNextQuestion() {
    if (currentQuestionIndex.value < questions.length) {
      return questions[currentQuestionIndex.value].text
    }
    isComplete.value = true
    return null
  }

  /**
   * Validate user response for current question
   */
  function validateResponse(response) {
    const trimmed = response.trim()

    if (!trimmed) {
      return { valid: false, error: 'Please provide a response.' }
    }

    const question = currentQuestion.value
    if (!question || !question.validation) {
      return { valid: true }
    }

    return question.validation(trimmed)
  }

  /**
   * Add user response and move to next question
   */
  function addResponse(response) {
    if (currentQuestionIndex.value < questions.length) {
      const questionId = questions[currentQuestionIndex.value].id
      userResponses.value[questionId] = response
      currentQuestionIndex.value++
    }
  }

  /**
   * Get all responses as formatted text
   */
  function getAllResponses() {
    return Object.values(userResponses.value).join('\n\n')
  }

  /**
   * Get structured responses object
   */
  function getStructuredResponses() {
    return { ...userResponses.value }
  }

  /**
   * Reset questionnaire to initial state
   */
  function reset() {
    currentQuestionIndex.value = 0
    userResponses.value = {}
    isComplete.value = false
  }

  /**
   * Go back to previous question
   */
  function goToPreviousQuestion() {
    if (currentQuestionIndex.value > 0) {
      currentQuestionIndex.value--
      isComplete.value = false
    }
  }

  /**
   * Skip current question
   */
  function skipQuestion() {
    if (currentQuestionIndex.value < questions.length) {
      const questionId = questions[currentQuestionIndex.value].id
      userResponses.value[questionId] = 'Not specified'
      currentQuestionIndex.value++
    }
  }

  return {
    // State
    currentQuestionIndex,
    userResponses,
    isComplete,
    isPetPatient,
    petType,

    // Computed
    currentQuestion,
    progress,

    // Methods
    getNextQuestion,
    validateResponse,
    addResponse,
    getAllResponses,
    getStructuredResponses,
    reset,
    goToPreviousQuestion,
    skipQuestion
  }
}
