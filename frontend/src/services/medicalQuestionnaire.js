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

      // After the symptoms response, inject dynamic questions if needed
      if (questionId === 'symptoms' && this.dynamicQuestions.length === 0) {
        this.dynamicQuestions = this.getDynamicQuestions(response);
        if (this.dynamicQuestions.length > 0) {
          // Insert dynamic questions after 'symptoms' and before 'duration'
          // baseQuestions[0] = age, [1] = gender, [2] = symptoms
          this.questions = [
            this.baseQuestions[0], // age
            this.baseQuestions[1], // gender
            this.baseQuestions[2], // symptoms
            ...this.dynamicQuestions,
            ...this.baseQuestions.slice(3) // duration, severity, additional
          ];
        }
      }

      this.currentQuestionIndex++;
    }
  }

  // Generate dynamic follow-up questions based on symptom keywords
  getDynamicQuestions(symptomText) {
    const questions = [];
    const text = (symptomText || '').toLowerCase();
    if (text.includes('itch') || text.includes('rash') || text.includes('skin')) {
      questions.push({
        id: 'skin_location',
        text: 'Where exactly is the itching or rash located? Is it spreading?',
        type: 'open'
      });
      questions.push({
        id: 'skin_appearance',
        text: 'Can you describe any changes in the skin (redness, bumps, blisters, scaling, etc)?',
        type: 'open'
      });
      questions.push({
        id: 'hygiene',
        text: 'Have you changed soaps, detergents, or personal hygiene routines recently?',
        type: 'open'
      });
      questions.push({
        id: 'activities',
        text: 'Have you participated in any activities that may have exposed your skin to irritants (hiking, swimming, new clothing)?',
        type: 'open'
      });
    }
    // Add more symptom keyword logic here as needed
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
  }
}
