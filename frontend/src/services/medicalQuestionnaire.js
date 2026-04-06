/**
 * Medical Questionnaire Manager
 * Handles the structured collection of medical information from users
 */
export class MedicalQuestionnaireManager {
  constructor() {
    this.baseQuestions = [
      {
        id: 'age',
        text: "To provide the best health assessment, I need some basic information. What is your age?",
        type: 'number'
      },
      {
        id: 'gender',
        text: "What is your gender? (male, female, non-binary, or prefer not to say)",
        type: 'text'
      },
      {
        id: 'symptoms',
        text: "Thank you. Now, please describe your main symptoms in detail. What are you experiencing?",
        type: 'open'
      },
      {
        id: 'duration',
        text: "Thank you for that information. How long have you been experiencing these symptoms?",
        type: 'duration',
        options: ['Just started', 'Few hours', '1-2 days', '3-7 days', '1-2 weeks', 'Few weeks', 'Months or longer']
      },
      {
        id: 'severity',
        text: "On a scale of 1-10, how severe would you rate your symptoms? (1 being mild, 10 being extremely severe)",
        type: 'scale'
      },
      {
        id: 'additional',
        text: "Are there any other symptoms or relevant medical history I should know about? Any medications you're currently taking?",
        type: 'open'
      }
    ];
    this.dynamicQuestions = [];
    this.questions = [...this.baseQuestions];
    this.currentQuestionIndex = 0;
    this.userResponses = {};
    this.isComplete = false;
    this.ageQuestionsInjected = false;
    this.severityQuestionsInjected = false;
  }

  getNextQuestion() {
    if (this.currentQuestionIndex < this.questions.length) {
      return this.questions[this.currentQuestionIndex].text
    }
    this.isComplete = true
    return null
  }

  addResponse(response) {
    if (this.currentQuestionIndex < this.questions.length) {
      const questionId = this.questions[this.currentQuestionIndex].id;
      this.userResponses[questionId] = response;

      // After age is captured, inject age-stratified questions
      if (questionId === 'age' && !this.ageQuestionsInjected) {
        this.addAgeStratifiedQuestions(response);
      }

      // After the symptoms response, inject dynamic questions if needed
      if (questionId === 'symptoms' && this.dynamicQuestions.length === 0) {
        this.dynamicQuestions = this.getDynamicQuestions(response);
        if (this.dynamicQuestions.length > 0) {
          const symptomsIdx = this.questions.findIndex(q => q.id === 'symptoms');
          const afterSymptoms = symptomsIdx + 1;
          // Insert dynamic questions after 'symptoms' and before 'duration'
          this.questions.splice(afterSymptoms, 0, ...this.dynamicQuestions);
        }
      }

      // After severity is captured, inject emergency screening if severity >= 8
      if (questionId === 'severity' && !this.severityQuestionsInjected) {
        this.addSeverityScreeningQuestions(response);
      }

      this.currentQuestionIndex++;
    }
  }

  /**
   * Inject age-specific screening questions after age is captured.
   */
  addAgeStratifiedQuestions(ageResponse) {
    if (this.ageQuestionsInjected) return;
    this.ageQuestionsInjected = true;

    const age = parseInt(ageResponse);
    if (isNaN(age)) return;

    const insertAt = this.currentQuestionIndex + 1; // After age, before gender
    const ageQuestions = [];

    if (age >= 65) {
      ageQuestions.push({
        id: 'elderly_screening',
        text: 'Do you have any issues with balance, memory, or frequent falls?',
        type: 'open'
      });
    } else if (age < 18) {
      ageQuestions.push({
        id: 'pediatric_screening',
        text: 'Is a parent or guardian present? Have you discussed this with a school nurse or pediatrician?',
        type: 'open'
      });
    }

    if (ageQuestions.length > 0) {
      this.questions.splice(insertAt, 0, ...ageQuestions);
    }
  }

  /**
   * Inject emergency screening questions when severity >= 8.
   */
  addSeverityScreeningQuestions(severityResponse) {
    if (this.severityQuestionsInjected) return;

    const severityMatch = (severityResponse || '').match(/\b(\d+)\b/);
    const severity = severityMatch ? parseInt(severityMatch[1]) : 0;
    if (severity < 8) return;

    this.severityQuestionsInjected = true;
    const insertAt = this.currentQuestionIndex + 1; // After severity, before additional
    const emergencyQuestions = [
      {
        id: 'emergency_breathing',
        text: 'Are you having difficulty breathing or chest pain right now?',
        type: 'open'
      },
      {
        id: 'emergency_consciousness',
        text: 'Have you lost consciousness, have severe bleeding, or feel you might faint?',
        type: 'open'
      }
    ];
    this.questions.splice(insertAt, 0, ...emergencyQuestions);
  }

  // Generate dynamic follow-up questions based on symptom keywords
  getDynamicQuestions(symptomText) {
    const questions = [];
    const text = (symptomText || '').toLowerCase();

    // Skin / rash / itch
    if (text.includes('itch') || text.includes('rash') || text.includes('skin')) {
      questions.push(
        { id: 'skin_location', text: 'Where exactly is the itching or rash located? Is it spreading?', type: 'open' },
        { id: 'skin_appearance', text: 'Can you describe any changes in the skin (redness, bumps, blisters, scaling, etc)?', type: 'open' },
        { id: 'hygiene', text: 'Have you changed soaps, detergents, or personal hygiene routines recently?', type: 'open' },
        { id: 'activities', text: 'Have you participated in any activities that may have exposed your skin to irritants (hiking, swimming, new clothing)?', type: 'open' },
      );
    }

    // Chest pain
    if (text.includes('chest') || text.includes('heart') || text.includes('cardiac')) {
      questions.push(
        { id: 'chest_exertion', text: 'Does the pain get worse with exertion or deep breaths?', type: 'open' },
        { id: 'chest_associated', text: 'Do you have shortness of breath, sweating, or nausea?', type: 'open' },
      );
    }

    // Headache
    if (text.includes('headache') || text.includes('head pain') || text.includes('migraine')) {
      questions.push(
        { id: 'headache_worst', text: 'Is this the worst headache of your life?', type: 'open' },
        { id: 'headache_redflags', text: 'Do you have neck stiffness, fever, or visual changes?', type: 'open' },
      );
    }

    // Abdominal pain
    if (text.includes('abdomin') || text.includes('stomach') || text.includes('belly') || text.includes('tummy')) {
      questions.push(
        { id: 'abdominal_location', text: 'Where is the pain — upper, lower, left, or right side?', type: 'open' },
        { id: 'abdominal_associated', text: 'Have you had changes in bowel habits, blood in stool, or vomiting?', type: 'open' },
      );
    }

    // Mental health
    if (text.includes('depress') || text.includes('anxiety') || text.includes('suicid') ||
        text.includes('self-harm') || text.includes('hopeless') || text.includes('panic')) {
      questions.push(
        { id: 'mental_safety', text: 'Have you had thoughts of harming yourself or others?', type: 'open' },
        { id: 'mental_sleep', text: 'How has your sleep and appetite been recently?', type: 'open' },
      );
    }

    // Breathing issues
    if (text.includes('breath') || text.includes('wheez') || text.includes('asthma') ||
        text.includes('suffocat') || text.includes('dyspnea')) {
      questions.push(
        { id: 'breathing_onset', text: 'How quickly did the breathing difficulty come on?', type: 'open' },
        { id: 'breathing_associated', text: 'Do you have chest pain, cough, or wheezing?', type: 'open' },
      );
    }

    // Medical history questions — always asked before diagnosis
    questions.push(
      { id: 'medications_detailed', text: 'Do you take any medications regularly? If so, what are they?', type: 'open' },
      { id: 'allergies_detailed', text: 'Do you have any known allergies, especially to medications?', type: 'open' },
      { id: 'family_history_detailed', text: 'Has anyone in your immediate family had serious medical conditions? (heart disease, cancer, diabetes, etc.)', type: 'open' },
    );

    return questions;
  }

  getAllResponses() {
    return Object.values(this.userResponses).join('\n\n')
  }

  getProgress() {
    return {
      current: this.currentQuestionIndex,
      total: this.questions.length,
      percentage: Math.round((this.currentQuestionIndex / this.questions.length) * 100)
    };
  }

  reset() {
    this.currentQuestionIndex = 0;
    this.userResponses = {};
    this.isComplete = false;
    this.questions = [...this.baseQuestions];
    this.dynamicQuestions = [];
    this.ageQuestionsInjected = false;
    this.severityQuestionsInjected = false;
  }
}
