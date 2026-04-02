/**
 * Specialist Doctor Registry
 *
 * Each specialist has a distinct identity, visual style, and
 * domain-specific follow-up questions. Used during the PA → Specialist
 * handoff to create a cinematic referral experience.
 */

export const SPECIALIST_DOCTORS = {
  cardiology: {
    name: 'Dr. Sarah Chen',
    title: 'Board-Certified Cardiologist',
    credentials: 'MD, FACC',
    emoji: '❤️',
    accentColor: 'red',
    accentHex: '#ef4444',
    bgClass: 'from-red-500 to-rose-600',
    greeting: "Hello, I'm Dr. Sarah Chen, a cardiologist. {paName} has shared your case notes with me. I specialize in heart and cardiovascular conditions — let me ask a couple of focused questions before we proceed with the full analysis.",
    questions: [
      "Do you notice these symptoms more during physical exertion, at rest, or when lying down?",
      "Have you ever been told you have high blood pressure, high cholesterol, or a heart murmur?",
    ],
    farewell: "Thank you. I now have a clear cardiovascular picture. Let me coordinate with our diagnostic team for a thorough analysis.",
  },

  dermatology: {
    name: 'Dr. Amara Okafor',
    title: 'Board-Certified Dermatologist',
    credentials: 'MD, FAAD',
    emoji: '🌸',
    accentColor: 'rose',
    accentHex: '#f43f5e',
    bgClass: 'from-rose-500 to-pink-600',
    greeting: "Hi there, I'm Dr. Amara Okafor, a dermatologist. I've reviewed the notes from {paName}. Skin conditions often reveal a lot through their history — let me ask a couple of targeted questions.",
    questions: [
      "Has the affected area changed in size, color, or texture since you first noticed it?",
      "Have you had significant sun exposure, used any new skincare products, or noticed similar issues elsewhere on your body?",
    ],
    farewell: "Thank you for those details. I have a good clinical picture now. Let me run this through our diagnostic team.",
  },

  neurology: {
    name: 'Dr. James Patel',
    title: 'Board-Certified Neurologist',
    credentials: 'MD, PhD',
    emoji: '🧠',
    accentColor: 'purple',
    accentHex: '#a855f7',
    bgClass: 'from-purple-500 to-violet-600',
    greeting: "Hello, I'm Dr. James Patel, a neurologist. {paName} briefed me on your symptoms. Neurological conditions can be nuanced, so I'd like to understand a few specifics.",
    questions: [
      "Are your symptoms constant, or do they come and go? If episodic, how long does each episode last?",
      "Have you noticed any changes in vision, speech, balance, or coordination alongside these symptoms?",
    ],
    farewell: "Thank you. These details are very helpful for a neurological assessment. Let me coordinate the full diagnostic analysis.",
  },

  gastroenterology: {
    name: 'Dr. Maria Santos',
    title: 'Board-Certified Gastroenterologist',
    credentials: 'MD, FACG',
    emoji: '🫁',
    accentColor: 'amber',
    accentHex: '#f59e0b',
    bgClass: 'from-amber-500 to-orange-600',
    greeting: "Hi, I'm Dr. Maria Santos, a gastroenterologist. I've been briefed by {paName} on your case. Digestive symptoms often have dietary or lifestyle connections — let me dig a bit deeper.",
    questions: [
      "Is there any pattern to when your symptoms occur — after eating, on an empty stomach, at night, or after specific foods?",
      "Have you noticed any changes in your bowel habits, appetite, or unintended weight changes recently?",
    ],
    farewell: "Thank you. I have a solid understanding of your GI picture. Let me get the diagnostic team working on this.",
  },

  psychiatry: {
    name: 'Dr. David Kim',
    title: 'Board-Certified Psychiatrist',
    credentials: 'MD, DFAPA',
    emoji: '🧘',
    accentColor: 'indigo',
    accentHex: '#6366f1',
    bgClass: 'from-indigo-500 to-blue-600',
    greeting: "Hello, I'm Dr. David Kim, a psychiatrist. {paName} mentioned some concerns that fall within my area. I want you to know this is a safe, confidential space. Let me understand a bit more about what you're experiencing.",
    questions: [
      "How long have you been experiencing these feelings, and have they affected your daily activities, work, or relationships?",
      "Have you tried any coping strategies, therapy, or medications for these symptoms before?",
    ],
    farewell: "Thank you for sharing that with me. Your openness helps us provide the best guidance. Let me run a comprehensive assessment.",
  },

  pulmonology: {
    name: 'Dr. Rachel Nguyen',
    title: 'Board-Certified Pulmonologist',
    credentials: 'MD, FCCP',
    emoji: '🫁',
    accentColor: 'cyan',
    accentHex: '#06b6d4',
    bgClass: 'from-cyan-500 to-teal-600',
    greeting: "Hi, I'm Dr. Rachel Nguyen, a pulmonologist. {paName} flagged some respiratory concerns in your case. Let me ask a couple of questions specific to lung and breathing health.",
    questions: [
      "Does your breathing difficulty occur at rest, with exertion, or when lying flat? Does it wake you up at night?",
      "Have you been exposed to smoke, dust, chemicals, or allergens recently? Any history of asthma or lung conditions?",
    ],
    farewell: "Thank you. I have a clear respiratory picture now. Let me coordinate with the diagnostic team.",
  },

  endocrinology: {
    name: 'Dr. Michael Torres',
    title: 'Board-Certified Endocrinologist',
    credentials: 'MD, FACE',
    emoji: '⚗️',
    accentColor: 'teal',
    accentHex: '#14b8a6',
    bgClass: 'from-teal-500 to-emerald-600',
    greeting: "Hello, I'm Dr. Michael Torres, an endocrinologist. {paName} shared your case with me. Hormonal and metabolic conditions can affect many body systems — let me ask a couple of focused questions.",
    questions: [
      "Have you noticed any unexplained weight changes, changes in energy levels, or temperature sensitivity (feeling too hot or too cold)?",
      "Do you have a personal or family history of diabetes, thyroid conditions, or other hormonal disorders?",
    ],
    farewell: "Thank you. These details are crucial for an endocrine assessment. Let me run the full analysis.",
  },

  orthopedics: {
    name: 'Dr. Lisa Park',
    title: 'Board-Certified Orthopedic Surgeon',
    credentials: 'MD, FAAOS',
    emoji: '🦴',
    accentColor: 'slate',
    accentHex: '#64748b',
    bgClass: 'from-slate-500 to-gray-600',
    greeting: "Hi, I'm Dr. Lisa Park, an orthopedic specialist. {paName} noted some musculoskeletal concerns. Let me understand the biomechanics of your situation better.",
    questions: [
      "Can you pinpoint exactly where the pain or discomfort is located? Does it radiate to other areas?",
      "Did this start after an injury or activity, or did it develop gradually? Does movement make it better or worse?",
    ],
    farewell: "Thank you. I have a clear picture of the musculoskeletal presentation. Let me get the diagnostic team on this.",
  },

  general_medicine: {
    name: 'Dr. Emily Wright',
    title: 'Board-Certified Internist',
    credentials: 'MD, FACP',
    emoji: '🩺',
    accentColor: 'blue',
    accentHex: '#3b82f6',
    bgClass: 'from-blue-500 to-indigo-600',
    greeting: "Hello, I'm Dr. Emily Wright, an internist. {paName} has shared your case notes with me. As a generalist, I look at the whole picture — let me ask a couple more questions to round out my understanding.",
    questions: [
      "Are you currently taking any medications, supplements, or herbal remedies — even over-the-counter ones?",
      "Have you traveled recently, been around anyone who's ill, or had any significant life changes or stressors?",
    ],
    farewell: "Thank you. I have a comprehensive picture now. Let me coordinate with our diagnostic team for a thorough analysis.",
  },
}

/**
 * Get specialist doctor by specialty key.
 * Falls back to general_medicine for unknown specialties.
 */
export function getSpecialist(specialty) {
  const key = specialty?.toLowerCase().replace(/[\s-]/g, '_') || 'general_medicine'
  return SPECIALIST_DOCTORS[key] || SPECIALIST_DOCTORS.general_medicine
}

/**
 * Map PA character type to emoji for the handoff card.
 */
export const PA_EMOJIS = {
  bunny: '🐰',
  cat: '🐱',
  dog: '🐶',
  human: '👨‍⚕️',
}
