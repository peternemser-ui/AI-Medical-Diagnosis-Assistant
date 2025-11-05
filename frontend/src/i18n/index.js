import { createI18n } from 'vue-i18n'

// Translation messages - Comprehensive coverage for all components
const messages = {
  en: {
    app: {
      title: 'AI Health Assistant',
      subtitle: 'Professional health guidance powered by AI',
      online: 'Online',
      aiActive: 'AI Active',
      basicMode: 'Basic Mode',
      estimatedCost: 'Estimated Cost'
    },
    nav: {
      home: 'Home',
      diagnosis: 'Diagnosis',
      dashboard: 'Dashboard',
      apiSetup: 'API Setup'
    },
    diagnosis: {
      start: 'Start Diagnosis',
      startMessage: 'Hello! I\'m your AI Health Assistant. I\'m here to help you understand your symptoms and provide professional health guidance.',
      askQuestion: 'What brings you here today?',
      typeMessage: 'Type your message here...',
      send: 'Send',
      restart: 'Start Over',
      viewDashboard: 'View Detailed Dashboard',
      exportPdf: 'Export as PDF',
      analyzing: 'AI Doctor is analyzing...',
      thinking: 'AI is thinking...'
    },
    dashboard: {
      title: 'AI Medical Assessment Dashboard',
      subtitle: 'Comprehensive diagnosis analysis with clinical insights',
      exportReport: 'Export Report',
      exportFormats: {
        pdf: 'Export as PDF',
        pdfDesc: 'Printable medical report',
        html: 'Export as HTML',
        htmlDesc: 'Web page format',
        json: 'Export as JSON',
        jsonDesc: 'Data format',
        text: 'Export as Text',
        textDesc: 'Plain text transcript'
      },
      patientInfo: {
        title: 'Patient Information',
        age: 'Age',
        gender: 'Gender',
        duration: 'Duration',
        severity: 'Severity',
        chiefComplaint: 'Chief Complaint'
      },
      differentialDiagnoses: {
        title: 'Differential Diagnoses',
        symptomMap: 'Symptom Map',
        areas: 'area | areas',
        affectedAreas: 'Affected Areas',
        noLocations: 'No symptom locations recorded',
        noData: 'No differential diagnoses available.',
        urgency: 'urgency',
        learnMore: 'Learn More',
        askQuestions: 'Ask Questions',
        findSpecialist: 'Find Specialist',
        likelihood: {
          veryHigh: 'Very High Likelihood',
          high: 'High Likelihood',
          moderate: 'Moderate Likelihood',
          low: 'Low Likelihood',
          veryLow: 'Very Low Likelihood'
        }
      },
      treatment: {
        title: 'Medical Treatment Plan',
        noData: 'No specific treatment recommendations available.'
      },
      holistic: {
        title: 'Holistic & Alternative Therapies',
        noData: 'No holistic recommendations available.'
      },
      conversation: {
        title: 'Conversation',
        you: 'You',
        assistant: 'Assistant',
        noMessages: 'No conversation history.'
      },
      followUp: {
        title: 'AI Follow-up Questions',
        subtitle: 'Help me understand your symptoms better',
        inputPlaceholder: 'Type your response...',
        send: 'Send',
        askQuestion: 'Ask a Question',
        noData: 'No follow-up questions at this time.'
      },
      redFlags: {
        title: 'Medical Red Flags',
        warning: 'Important Warning Signs',
        seekCare: 'Seek Medical Care Immediately',
        noData: 'No critical warning signs identified.'
      },
      lifestyle: {
        title: 'Lifestyle & Prevention',
        noData: 'No lifestyle recommendations available.'
      },
      tests: {
        title: 'Recommended Medical Tests',
        noData: 'No specific tests recommended at this time.'
      },
      prognosis: {
        title: 'Prognosis & Timeline',
        noData: 'Prognosis information not available.'
      }
    },
    questionnaire: {
      age: 'What is your age?',
      gender: 'What is your biological sex/gender? (Male, Female, or Other)',
      symptoms: 'What brings you here today? Please describe your main symptoms or health concerns in as much detail as possible.',
      duration: 'How long have you been experiencing these symptoms?',
      severity: 'On a scale of 1-10, how severe would you rate your symptoms?',
      medicalHistory: 'Do you have any relevant medical history, current medications, or allergies I should know about?'
    },
    severity: {
      title: 'Rate Your Symptom Severity',
      mild: 'Mild',
      moderate: 'Moderate',
      significant: 'Significant',
      severe: 'Severe',
      critical: 'Critical',
      submit: 'Submit Rating'
    },
    bodyDiagram: {
      title: 'Select Symptom Locations',
      subtitle: 'Click on body areas where you experience symptoms',
      front: 'Front',
      back: 'Back',
      submit: 'Submit Selected Areas',
      selected: 'Selected Areas'
    },
    imageUpload: {
      title: 'Upload Symptom Photos',
      subtitle: 'Upload images for AI visual analysis',
      dragDrop: 'Drag and drop images here, or click to browse',
      analyzing: 'Analyzing images with AI...',
      maxFiles: 'Maximum 5 images',
      maxSize: '10MB per image'
    },
    drugLookup: {
      title: 'Drug Information',
      subtitle: 'Search medications and check interactions',
      searchPlaceholder: 'Search for a medication (e.g., \'aspirin\', \'lisinopril\')...',
      searchButton: 'Search Drug Database',
      searching: 'Searching RxNorm Database...',
      found: 'Found {count} medication(s)',
      noResults: 'No medications found for "{query}"',
      tryAgain: 'Try searching for the generic name or brand name',
      selectedMeds: 'Selected Medications',
      checkInteractions: 'Check Drug Interactions',
      checking: 'Checking interactions...',
      interactionsFound: '{count} Drug Interaction(s) Found',
      interactionsWarning: 'The selected medications may interact with each other. Consult your doctor or pharmacist.',
      noInteractions: 'No Known Interactions',
      noInteractionsDesc: 'No major drug-drug interactions found between the selected medications.',
      aboutTitle: 'About This Tool',
      aboutText: 'Drug information is sourced from RxNorm, a standardized nomenclature for clinical drugs maintained by the U.S. National Library of Medicine. Always consult your healthcare provider before starting or stopping any medication.',
      severity: {
        high: 'HIGH',
        moderate: 'MODERATE',
        low: 'LOW'
      }
    },
    emergency: {
      cardiac: 'CARDIAC EMERGENCY',
      respiratory: 'RESPIRATORY EMERGENCY',
      stroke: 'POSSIBLE STROKE',
      bleeding: 'SEVERE BLEEDING',
      trauma: 'SEVERE TRAUMA',
      poisoning: 'POISONING/OVERDOSE',
      allergic: 'ANAPHYLAXIS',
      abdominal: 'SEVERE ABDOMINAL EMERGENCY',
      call911: 'CALL 911 NOW',
      understand: 'I understand (dismiss)'
    },
    settings: {
      title: 'Settings',
      language: 'Language',
      theme: 'Theme',
      voice: 'Voice Enabled',
      sound: 'Sound Effects',
      autoScroll: 'Auto Scroll',
      apiKey: 'API Key Configuration'
    },
    errors: {
      generic: 'An error occurred. Please try again.',
      network: 'Network error. Please check your connection.',
      apiKey: 'Invalid API key. Please check your settings.'
    },
    common: {
      close: 'Close',
      cancel: 'Cancel',
      confirm: 'Confirm',
      save: 'Save',
      loading: 'Loading...',
      yes: 'Yes',
      no: 'No',
      back: 'Back',
      next: 'Next'
    },
    home: {
      welcome: 'Welcome to Your AI Health Checker',
      subtitle: 'Get personalized health guidance through our intelligent AI system. Start with a comprehensive health assessment using voice or text input.',
      startAssessment: 'Start Health Assessment',
      viewDashboard: 'View Sample Dashboard',
      disclaimer: 'AI-powered health assessment for informational purposes only'
    },
    apiSetup: {
      title: 'AI Medical Diagnosis Assistant',
      subtitle: 'Configure your AI service to get started',
      configTitle: 'OpenAI API Configuration',
      configSubtitle: 'Enter your OpenAI API key to enable AI-powered medical diagnosis assistance.',
      apiKeyLabel: 'OpenAI API Key',
      apiKeyPlaceholder: 'sk-...',
      saveAndContinue: 'Save & Continue',
      validating: 'Validating...',
      skipForNow: 'Skip for Now',
      needKeyTitle: 'Need an API Key?',
      needKeySubtitle: 'Get your OpenAI API key from the OpenAI platform:',
      steps: {
        step1: 'Visit platform.openai.com/api-keys',
        step2: 'Sign in to your OpenAI account',
        step3: 'Click "Create new secret key"',
        step4: 'Copy the key and paste it above'
      },
      securityNote: 'Your API key is stored locally and never sent to our servers.',
      footer: 'Secure • Private • HIPAA-Compliant Design',
      errors: {
        required: 'API key is required',
        invalidFormat: 'Invalid API key format. OpenAI keys start with "sk-"',
        tooShort: 'API key appears to be too short',
        saveFailed: 'Failed to save API key. Please try again.'
      },
      success: 'API key saved successfully!'
    }
  },
  es: {
    app: {
      title: 'Asistente de Salud IA',
      subtitle: 'Orientación médica profesional con IA',
      online: 'En línea',
      aiActive: 'IA Activa',
      basicMode: 'Modo Básico',
      estimatedCost: 'Costo Estimado'
    },
    nav: {
      home: 'Inicio',
      diagnosis: 'Diagnóstico',
      dashboard: 'Panel',
      apiSetup: 'Config. API'
    },
    diagnosis: {
      start: 'Iniciar Diagnóstico',
      startMessage: '¡Hola! Soy tu Asistente de Salud IA. Estoy aquí para ayudarte a entender tus síntomas y brindarte orientación médica profesional.',
      askQuestion: '¿Qué te trae por aquí hoy?',
      typeMessage: 'Escribe tu mensaje aquí...',
      send: 'Enviar',
      restart: 'Comenzar de Nuevo',
      viewDashboard: 'Ver Panel Detallado',
      exportPdf: 'Exportar como PDF',
      analyzing: 'El médico IA está analizando...',
      thinking: 'La IA está pensando...'
    },
    dashboard: {
      title: 'Panel de Evaluación Médica IA',
      subtitle: 'Análisis de diagnóstico integral con información clínica',
      exportReport: 'Exportar Informe',
      exportFormats: {
        pdf: 'Exportar como PDF',
        pdfDesc: 'Informe médico imprimible',
        html: 'Exportar como HTML',
        htmlDesc: 'Formato de página web',
        json: 'Exportar como JSON',
        jsonDesc: 'Formato de datos',
        text: 'Exportar como Texto',
        textDesc: 'Transcripción de texto plano'
      },
      patientInfo: {
        title: 'Información del Paciente',
        age: 'Edad',
        gender: 'Género',
        duration: 'Duración',
        severity: 'Gravedad',
        chiefComplaint: 'Queja Principal'
      },
      differentialDiagnoses: {
        title: 'Diagnósticos Diferenciales',
        symptomMap: 'Mapa de Síntomas',
        areas: 'área | áreas',
        affectedAreas: 'Áreas Afectadas',
        noLocations: 'No hay ubicaciones de síntomas registradas',
        noData: 'No hay diagnósticos diferenciales disponibles.',
        urgency: 'urgencia',
        learnMore: 'Más Información',
        askQuestions: 'Hacer Preguntas',
        findSpecialist: 'Buscar Especialista',
        likelihood: {
          veryHigh: 'Probabilidad Muy Alta',
          high: 'Probabilidad Alta',
          moderate: 'Probabilidad Moderada',
          low: 'Probabilidad Baja',
          veryLow: 'Probabilidad Muy Baja'
        }
      },
      treatment: {
        title: 'Plan de Tratamiento Médico',
        noData: 'No hay recomendaciones de tratamiento específicas disponibles.'
      },
      holistic: {
        title: 'Terapias Holísticas y Alternativas',
        noData: 'No hay recomendaciones holísticas disponibles.'
      },
      conversation: {
        title: 'Conversación',
        you: 'Tú',
        assistant: 'Asistente',
        noMessages: 'No hay historial de conversación.'
      },
      followUp: {
        title: 'Preguntas de Seguimiento de IA',
        subtitle: 'Ayúdame a entender mejor tus síntomas',
        inputPlaceholder: 'Escribe tu respuesta...',
        send: 'Enviar',
        askQuestion: 'Hacer una Pregunta',
        noData: 'No hay preguntas de seguimiento en este momento.'
      },
      redFlags: {
        title: 'Señales de Alerta Médicas',
        warning: 'Señales de Advertencia Importantes',
        seekCare: 'Buscar Atención Médica Inmediatamente',
        noData: 'No se identificaron señales de advertencia críticas.'
      },
      lifestyle: {
        title: 'Estilo de Vida y Prevención',
        noData: 'No hay recomendaciones de estilo de vida disponibles.'
      },
      tests: {
        title: 'Pruebas Médicas Recomendadas',
        noData: 'No se recomiendan pruebas específicas en este momento.'
      },
      prognosis: {
        title: 'Pronóstico y Cronología',
        noData: 'Información de pronóstico no disponible.'
      }
    },
    questionnaire: {
      age: '¿Cuál es tu edad?',
      gender: '¿Cuál es tu sexo biológico/género? (Masculino, Femenino u Otro)',
      symptoms: '¿Qué te trae por aquí hoy? Por favor describe tus síntomas principales o preocupaciones de salud con el mayor detalle posible.',
      duration: '¿Cuánto tiempo has estado experimentando estos síntomas?',
      severity: 'En una escala del 1 al 10, ¿qué tan graves calificarías tus síntomas?',
      medicalHistory: '¿Tienes algún historial médico relevante, medicamentos actuales o alergias que deba conocer?'
    },
    severity: {
      title: 'Califica la Gravedad de tus Síntomas',
      mild: 'Leve',
      moderate: 'Moderado',
      significant: 'Significativo',
      severe: 'Grave',
      critical: 'Crítico',
      submit: 'Enviar Calificación'
    },
    bodyDiagram: {
      title: 'Selecciona Ubicaciones de Síntomas',
      subtitle: 'Haz clic en las áreas del cuerpo donde experimentas síntomas',
      front: 'Frente',
      back: 'Espalda',
      submit: 'Enviar Áreas Seleccionadas',
      selected: 'Áreas Seleccionadas'
    },
    imageUpload: {
      title: 'Subir Fotos de Síntomas',
      subtitle: 'Sube imágenes para análisis visual con IA',
      dragDrop: 'Arrastra y suelta imágenes aquí, o haz clic para explorar',
      analyzing: 'Analizando imágenes con IA...',
      maxFiles: 'Máximo 5 imágenes',
      maxSize: '10MB por imagen'
    },
    drugLookup: {
      title: 'Información de Medicamentos',
      subtitle: 'Busca medicamentos y verifica interacciones',
      searchPlaceholder: 'Buscar un medicamento (ej: \'aspirina\', \'lisinopril\')...',
      searchButton: 'Buscar en Base de Datos',
      searching: 'Buscando en Base de Datos RxNorm...',
      found: 'Se encontraron {count} medicamento(s)',
      noResults: 'No se encontraron medicamentos para "{query}"',
      tryAgain: 'Intenta buscar por el nombre genérico o de marca',
      selectedMeds: 'Medicamentos Seleccionados',
      checkInteractions: 'Verificar Interacciones',
      checking: 'Verificando interacciones...',
      interactionsFound: '{count} Interacción(es) Encontrada(s)',
      interactionsWarning: 'Los medicamentos seleccionados pueden interactuar entre sí. Consulta a tu médico o farmacéutico.',
      noInteractions: 'Sin Interacciones Conocidas',
      noInteractionsDesc: 'No se encontraron interacciones importantes entre los medicamentos seleccionados.',
      aboutTitle: 'Acerca de Esta Herramienta',
      aboutText: 'La información de medicamentos proviene de RxNorm, una nomenclatura estandarizada mantenida por la Biblioteca Nacional de Medicina de EE.UU. Siempre consulta a tu proveedor de salud antes de iniciar o detener cualquier medicamento.',
      severity: {
        high: 'ALTA',
        moderate: 'MODERADA',
        low: 'BAJA'
      }
    },
    emergency: {
      cardiac: 'EMERGENCIA CARDÍACA',
      respiratory: 'EMERGENCIA RESPIRATORIA',
      stroke: 'POSIBLE DERRAME CEREBRAL',
      bleeding: 'SANGRADO SEVERO',
      trauma: 'TRAUMA SEVERO',
      poisoning: 'ENVENENAMIENTO/SOBREDOSIS',
      allergic: 'ANAFILAXIA',
      abdominal: 'EMERGENCIA ABDOMINAL SEVERA',
      call911: 'LLAMA AL 911 AHORA',
      understand: 'Entiendo (descartar)'
    },
    settings: {
      title: 'Configuración',
      language: 'Idioma',
      theme: 'Tema',
      voice: 'Voz Habilitada',
      sound: 'Efectos de Sonido',
      autoScroll: 'Desplazamiento Automático',
      apiKey: 'Configuración de Clave API'
    },
    errors: {
      generic: 'Ocurrió un error. Por favor intenta de nuevo.',
      network: 'Error de red. Por favor verifica tu conexión.',
      apiKey: 'Clave API inválida. Por favor verifica tu configuración.'
    },
    common: {
      close: 'Cerrar',
      cancel: 'Cancelar',
      confirm: 'Confirmar',
      save: 'Guardar',
      loading: 'Cargando...',
      yes: 'Sí',
      no: 'No',
      back: 'Atrás',
      next: 'Siguiente'
    },
    home: {
      welcome: 'Bienvenido a Tu Verificador de Salud IA',
      subtitle: 'Obtén orientación de salud personalizada a través de nuestro sistema inteligente de IA. Comienza con una evaluación de salud integral usando entrada de voz o texto.',
      startAssessment: 'Iniciar Evaluación de Salud',
      viewDashboard: 'Ver Panel de Muestra',
      disclaimer: 'Evaluación de salud impulsada por IA solo con fines informativos'
    },
    apiSetup: {
      title: 'Asistente de Diagnóstico Médico IA',
      subtitle: 'Configura tu servicio de IA para comenzar',
      configTitle: 'Configuración de API de OpenAI',
      configSubtitle: 'Ingresa tu clave API de OpenAI para habilitar asistencia de diagnóstico médico impulsada por IA.',
      apiKeyLabel: 'Clave API de OpenAI',
      apiKeyPlaceholder: 'sk-...',
      saveAndContinue: 'Guardar y Continuar',
      validating: 'Validando...',
      skipForNow: 'Omitir por Ahora',
      needKeyTitle: '¿Necesitas una Clave API?',
      needKeySubtitle: 'Obtén tu clave API de OpenAI desde la plataforma de OpenAI:',
      steps: {
        step1: 'Visita platform.openai.com/api-keys',
        step2: 'Inicia sesión en tu cuenta de OpenAI',
        step3: 'Haz clic en "Crear nueva clave secreta"',
        step4: 'Copia la clave y pégala arriba'
      },
      securityNote: 'Tu clave API se almacena localmente y nunca se envía a nuestros servidores.',
      footer: 'Seguro • Privado • Diseño Compatible con HIPAA',
      errors: {
        required: 'Se requiere clave API',
        invalidFormat: 'Formato de clave API inválido. Las claves de OpenAI comienzan con "sk-"',
        tooShort: 'La clave API parece ser demasiado corta',
        saveFailed: 'Error al guardar la clave API. Por favor intenta de nuevo.'
      },
      success: '¡Clave API guardada exitosamente!'
    }
  },
  fr: {
    app: {
      title: 'Assistant Santé IA',
      subtitle: 'Conseils médicaux professionnels avec IA',
      online: 'En ligne',
      aiActive: 'IA Active',
      basicMode: 'Mode Basique',
      estimatedCost: 'Coût Estimé'
    },
    nav: {
      home: 'Accueil',
      diagnosis: 'Diagnostic',
      dashboard: 'Tableau de bord',
      apiSetup: 'Config. API'
    },
    diagnosis: {
      start: 'Démarrer le Diagnostic',
      startMessage: 'Bonjour! Je suis votre Assistant Santé IA. Je suis là pour vous aider à comprendre vos symptômes et vous fournir des conseils médicaux professionnels.',
      askQuestion: 'Qu\'est-ce qui vous amène aujourd\'hui?',
      typeMessage: 'Tapez votre message ici...',
      send: 'Envoyer',
      restart: 'Recommencer',
      viewDashboard: 'Voir le Tableau Détaillé',
      exportPdf: 'Exporter en PDF',
      analyzing: 'Le médecin IA analyse...',
      thinking: 'L\'IA réfléchit...'
    },
    dashboard: {
      title: 'Tableau de Bord Évaluation Médicale IA',
      subtitle: 'Analyse diagnostique complète avec informations cliniques',
      exportReport: 'Exporter le Rapport',
      exportFormats: {
        pdf: 'Exporter en PDF',
        pdfDesc: 'Rapport médical imprimable',
        html: 'Exporter en HTML',
        htmlDesc: 'Format de page web',
        json: 'Exporter en JSON',
        jsonDesc: 'Format de données',
        text: 'Exporter en Texte',
        textDesc: 'Transcription texte brut'
      },
      patientInfo: {
        title: 'Informations Patient',
        age: 'Âge',
        gender: 'Genre',
        duration: 'Durée',
        severity: 'Gravité',
        chiefComplaint: 'Plainte Principale'
      },
      differentialDiagnoses: {
        title: 'Diagnostics Différentiels',
        symptomMap: 'Carte des Symptômes',
        areas: 'zone | zones',
        affectedAreas: 'Zones Affectées',
        noLocations: 'Aucune localisation de symptômes enregistrée',
        noData: 'Aucun diagnostic différentiel disponible.',
        urgency: 'urgence',
        learnMore: 'En Savoir Plus',
        askQuestions: 'Poser des Questions',
        findSpecialist: 'Trouver un Spécialiste',
        likelihood: {
          veryHigh: 'Probabilité Très Élevée',
          high: 'Probabilité Élevée',
          moderate: 'Probabilité Modérée',
          low: 'Probabilité Faible',
          veryLow: 'Probabilité Très Faible'
        }
      },
      treatment: {
        title: 'Plan de Traitement Médical',
        noData: 'Aucune recommandation de traitement spécifique disponible.'
      },
      holistic: {
        title: 'Thérapies Holistiques et Alternatives',
        noData: 'Aucune recommandation holistique disponible.'
      },
      conversation: {
        title: 'Conversation',
        you: 'Vous',
        assistant: 'Assistant',
        noMessages: 'Aucun historique de conversation.'
      },
      followUp: {
        title: 'Questions de Suivi IA',
        subtitle: 'Aidez-moi à mieux comprendre vos symptômes',
        inputPlaceholder: 'Tapez votre réponse...',
        send: 'Envoyer',
        askQuestion: 'Poser une Question',
        noData: 'Aucune question de suivi pour le moment.'
      },
      redFlags: {
        title: 'Signaux d\'Alerte Médicaux',
        warning: 'Signes d\'Avertissement Importants',
        seekCare: 'Consulter Immédiatement un Médecin',
        noData: 'Aucun signe d\'avertissement critique identifié.'
      },
      lifestyle: {
        title: 'Mode de Vie et Prévention',
        noData: 'Aucune recommandation de mode de vie disponible.'
      },
      tests: {
        title: 'Tests Médicaux Recommandés',
        noData: 'Aucun test spécifique recommandé pour le moment.'
      },
      prognosis: {
        title: 'Pronostic et Chronologie',
        noData: 'Informations de pronostic non disponibles.'
      }
    },
    questionnaire: {
      age: 'Quel est votre âge?',
      gender: 'Quel est votre sexe biologique/genre? (Homme, Femme ou Autre)',
      symptoms: 'Qu\'est-ce qui vous amène aujourd\'hui? Veuillez décrire vos principaux symptômes ou préoccupations de santé aussi détaillés que possible.',
      duration: 'Depuis combien de temps ressentez-vous ces symptômes?',
      severity: 'Sur une échelle de 1 à 10, comment évalueriez-vous la gravité de vos symptômes?',
      medicalHistory: 'Avez-vous des antécédents médicaux pertinents, des médicaments actuels ou des allergies que je devrais connaître?'
    },
    severity: {
      title: 'Évaluez la Gravité de Vos Symptômes',
      mild: 'Léger',
      moderate: 'Modéré',
      significant: 'Significatif',
      severe: 'Grave',
      critical: 'Critique',
      submit: 'Soumettre l\'Évaluation'
    },
    bodyDiagram: {
      title: 'Sélectionner les Zones de Symptômes',
      subtitle: 'Cliquez sur les zones du corps où vous ressentez des symptômes',
      front: 'Avant',
      back: 'Arrière',
      submit: 'Soumettre les Zones Sélectionnées',
      selected: 'Zones Sélectionnées'
    },
    imageUpload: {
      title: 'Télécharger Photos de Symptômes',
      subtitle: 'Téléchargez des images pour analyse visuelle IA',
      dragDrop: 'Glissez-déposez les images ici ou cliquez pour parcourir',
      analyzing: 'Analyse des images avec IA...',
      maxFiles: 'Maximum 5 images',
      maxSize: '10MB par image'
    },
    drugLookup: {
      title: 'Information sur les Médicaments',
      subtitle: 'Rechercher médicaments et vérifier interactions',
      searchPlaceholder: 'Rechercher un médicament (ex: \'aspirine\', \'lisinopril\')...',
      searchButton: 'Rechercher dans la Base',
      searching: 'Recherche dans RxNorm...',
      found: '{count} médicament(s) trouvé(s)',
      noResults: 'Aucun médicament trouvé pour "{query}"',
      tryAgain: 'Essayez de rechercher par nom générique ou de marque',
      selectedMeds: 'Médicaments Sélectionnés',
      checkInteractions: 'Vérifier les Interactions',
      checking: 'Vérification des interactions...',
      interactionsFound: '{count} Interaction(s) Trouvée(s)',
      interactionsWarning: 'Les médicaments sélectionnés peuvent interagir. Consultez votre médecin ou pharmacien.',
      noInteractions: 'Aucune Interaction Connue',
      noInteractionsDesc: 'Aucune interaction majeure trouvée entre les médicaments sélectionnés.',
      aboutTitle: 'À Propos de Cet Outil',
      aboutText: 'Les informations proviennent de RxNorm, une nomenclature standardisée maintenue par la Bibliothèque Nationale de Médecine des États-Unis. Consultez toujours votre professionnel de santé avant de commencer ou d\'arrêter un médicament.',
      severity: {
        high: 'HAUTE',
        moderate: 'MODÉRÉE',
        low: 'BASSE'
      }
    },
    emergency: {
      cardiac: 'URGENCE CARDIAQUE',
      respiratory: 'URGENCE RESPIRATOIRE',
      stroke: 'AVC POSSIBLE',
      bleeding: 'SAIGNEMENT SÉVÈRE',
      trauma: 'TRAUMATISME SÉVÈRE',
      poisoning: 'EMPOISONNEMENT/SURDOSE',
      allergic: 'ANAPHYLAXIE',
      abdominal: 'URGENCE ABDOMINALE SÉVÈRE',
      call911: 'APPELEZ LE 911 MAINTENANT',
      understand: 'Je comprends (fermer)'
    },
    settings: {
      title: 'Paramètres',
      language: 'Langue',
      theme: 'Thème',
      voice: 'Voix Activée',
      sound: 'Effets Sonores',
      autoScroll: 'Défilement Auto',
      apiKey: 'Configuration Clé API'
    },
    errors: {
      generic: 'Une erreur s\'est produite. Veuillez réessayer.',
      network: 'Erreur réseau. Veuillez vérifier votre connexion.',
      apiKey: 'Clé API invalide. Veuillez vérifier vos paramètres.'
    },
    common: {
      close: 'Fermer',
      cancel: 'Annuler',
      confirm: 'Confirmer',
      save: 'Enregistrer',
      loading: 'Chargement...',
      yes: 'Oui',
      no: 'Non',
      back: 'Retour',
      next: 'Suivant'
    },
    home: {
      welcome: 'Bienvenue dans Votre Vérificateur de Santé IA',
      subtitle: 'Obtenez des conseils de santé personnalisés grâce à notre système intelligent IA. Commencez par une évaluation de santé complète utilisant la voix ou le texte.',
      startAssessment: 'Démarrer l\'Évaluation de Santé',
      viewDashboard: 'Voir le Tableau de Bord Exemple',
      disclaimer: 'Évaluation de santé propulsée par IA à des fins informatives uniquement'
    },
    apiSetup: {
      title: 'Assistant de Diagnostic Médical IA',
      subtitle: 'Configurez votre service IA pour commencer',
      configTitle: 'Configuration de l\'API OpenAI',
      configSubtitle: 'Entrez votre clé API OpenAI pour activer l\'assistance de diagnostic médical propulsée par IA.',
      apiKeyLabel: 'Clé API OpenAI',
      apiKeyPlaceholder: 'sk-...',
      saveAndContinue: 'Enregistrer et Continuer',
      validating: 'Validation...',
      skipForNow: 'Ignorer pour le Moment',
      needKeyTitle: 'Besoin d\'une Clé API?',
      needKeySubtitle: 'Obtenez votre clé API OpenAI depuis la plateforme OpenAI:',
      steps: {
        step1: 'Visitez platform.openai.com/api-keys',
        step2: 'Connectez-vous à votre compte OpenAI',
        step3: 'Cliquez sur "Créer une nouvelle clé secrète"',
        step4: 'Copiez la clé et collez-la ci-dessus'
      },
      securityNote: 'Votre clé API est stockée localement et n\'est jamais envoyée à nos serveurs.',
      footer: 'Sécurisé • Privé • Conforme HIPAA',
      errors: {
        required: 'Clé API requise',
        invalidFormat: 'Format de clé API invalide. Les clés OpenAI commencent par "sk-"',
        tooShort: 'La clé API semble trop courte',
        saveFailed: 'Échec de l\'enregistrement de la clé API. Veuillez réessayer.'
      },
      success: 'Clé API enregistrée avec succès!'
    }
  },
  zh: {
    app: {
      title: 'AI健康助手',
      subtitle: 'AI驱动的专业健康指导',
      online: '在线',
      aiActive: 'AI已激活',
      basicMode: '基础模式',
      estimatedCost: '预估费用'
    },
    nav: {
      home: '首页',
      diagnosis: '诊断',
      dashboard: '仪表板',
      apiSetup: 'API设置'
    },
    diagnosis: {
      start: '开始诊断',
      startMessage: '您好！我是您的AI健康助手。我在这里帮助您了解症状并提供专业的健康指导。',
      askQuestion: '今天什么带您来这里？',
      typeMessage: '在此输入您的消息...',
      send: '发送',
      restart: '重新开始',
      viewDashboard: '查看详细仪表板',
      exportPdf: '导出为PDF',
      analyzing: 'AI医生正在分析...',
      thinking: 'AI正在思考...'
    },
    dashboard: {
      title: 'AI医疗评估仪表板',
      subtitle: '全面的诊断分析与临床见解',
      exportReport: '导出报告',
      exportFormats: {
        pdf: '导出为PDF',
        pdfDesc: '可打印医疗报告',
        html: '导出为HTML',
        htmlDesc: '网页格式',
        json: '导出为JSON',
        jsonDesc: '数据格式',
        text: '导出为文本',
        textDesc: '纯文本转录'
      },
      patientInfo: {
        title: '患者信息',
        age: '年龄',
        gender: '性别',
        duration: '持续时间',
        severity: '严重程度',
        chiefComplaint: '主诉'
      },
      differentialDiagnoses: {
        title: '鉴别诊断',
        symptomMap: '症状图',
        areas: '区域',
        affectedAreas: '受影响区域',
        noLocations: '未记录症状位置',
        noData: '无可用的鉴别诊断。',
        urgency: '紧急程度',
        learnMore: '了解更多',
        askQuestions: '提问',
        findSpecialist: '查找专科医生',
        likelihood: {
          veryHigh: '可能性极高',
          high: '可能性高',
          moderate: '可能性中等',
          low: '可能性低',
          veryLow: '可能性极低'
        }
      },
      treatment: {
        title: '医疗治疗计划',
        noData: '没有特定的治疗建议。'
      },
      holistic: {
        title: '整体和替代疗法',
        noData: '没有整体建议。'
      },
      conversation: {
        title: '对话',
        you: '您',
        assistant: '助手',
        noMessages: '无对话历史。'
      },
      followUp: {
        title: 'AI后续问题',
        subtitle: '帮助我更好地了解您的症状',
        inputPlaceholder: '输入您的回复...',
        send: '发送',
        askQuestion: '提问',
        noData: '目前没有后续问题。'
      },
      redFlags: {
        title: '医疗警示信号',
        warning: '重要警告信号',
        seekCare: '立即就医',
        noData: '未发现关键警告信号。'
      },
      lifestyle: {
        title: '生活方式和预防',
        noData: '无可用的生活方式建议。'
      },
      tests: {
        title: '推荐医疗检查',
        noData: '目前没有推荐特定检查。'
      },
      prognosis: {
        title: '预后和时间线',
        noData: '预后信息不可用。'
      }
    },
    questionnaire: {
      age: '您的年龄是多少？',
      gender: '您的生理性别/性别是什么？（男性、女性或其他）',
      symptoms: '今天什么带您来这里？请尽可能详细地描述您的主要症状或健康问题。',
      duration: '您出现这些症状多长时间了？',
      severity: '在1-10的等级中，您如何评价症状的严重程度？',
      medicalHistory: '您是否有相关病史、目前使用的药物或我应该知道的过敏史？'
    },
    severity: {
      title: '评估症状严重程度',
      mild: '轻度',
      moderate: '中度',
      significant: '显著',
      severe: '严重',
      critical: '危急',
      submit: '提交评级'
    },
    bodyDiagram: {
      title: '选择症状位置',
      subtitle: '点击您出现症状的身体部位',
      front: '正面',
      back: '背面',
      submit: '提交选定区域',
      selected: '已选区域'
    },
    imageUpload: {
      title: '上传症状照片',
      subtitle: '上传图片进行AI视觉分析',
      dragDrop: '将图片拖放到此处，或点击浏览',
      analyzing: '正在使用AI分析图片...',
      maxFiles: '最多5张图片',
      maxSize: '每张图片10MB'
    },
    drugLookup: {
      title: '药物信息',
      subtitle: '搜索药物并检查相互作用',
      searchPlaceholder: '搜索药物（例如：\'阿司匹林\'、\'赖诺普利\'）...',
      searchButton: '搜索药物数据库',
      searching: '正在搜索RxNorm数据库...',
      found: '找到{count}种药物',
      noResults: '未找到"{query}"的药物',
      tryAgain: '尝试搜索通用名称或品牌名称',
      selectedMeds: '已选药物',
      checkInteractions: '检查药物相互作用',
      checking: '正在检查相互作用...',
      interactionsFound: '发现{count}个药物相互作用',
      interactionsWarning: '所选药物可能相互作用。请咨询您的医生或药剂师。',
      noInteractions: '无已知相互作用',
      noInteractionsDesc: '所选药物之间未发现重大相互作用。',
      aboutTitle: '关于此工具',
      aboutText: '药物信息来源于RxNorm，这是由美国国家医学图书馆维护的标准化临床药物命名法。在开始或停止任何药物之前，请务必咨询您的医疗保健提供者。',
      severity: {
        high: '高',
        moderate: '中',
        low: '低'
      }
    },
    emergency: {
      cardiac: '心脏紧急情况',
      respiratory: '呼吸紧急情况',
      stroke: '可能中风',
      bleeding: '严重出血',
      trauma: '严重创伤',
      poisoning: '中毒/过量',
      allergic: '过敏性休克',
      abdominal: '严重腹部紧急情况',
      call911: '立即拨打911',
      understand: '我明白（关闭）'
    },
    settings: {
      title: '设置',
      language: '语言',
      theme: '主题',
      voice: '启用语音',
      sound: '音效',
      autoScroll: '自动滚动',
      apiKey: 'API密钥配置'
    },
    errors: {
      generic: '发生错误。请重试。',
      network: '网络错误。请检查您的连接。',
      apiKey: 'API密钥无效。请检查您的设置。'
    },
    common: {
      close: '关闭',
      cancel: '取消',
      confirm: '确认',
      save: '保存',
      loading: '加载中...',
      yes: '是',
      no: '否',
      back: '返回',
      next: '下一步'
    },
    home: {
      welcome: '欢迎使用AI健康检查器',
      subtitle: '通过我们的智能AI系统获得个性化的健康指导。使用语音或文本输入开始全面的健康评估。',
      startAssessment: '开始健康评估',
      viewDashboard: '查看示例仪表板',
      disclaimer: 'AI驱动的健康评估仅供参考'
    },
    apiSetup: {
      title: 'AI医疗诊断助手',
      subtitle: '配置您的AI服务以开始使用',
      configTitle: 'OpenAI API配置',
      configSubtitle: '输入您的OpenAI API密钥以启用AI驱动的医疗诊断辅助。',
      apiKeyLabel: 'OpenAI API密钥',
      apiKeyPlaceholder: 'sk-...',
      saveAndContinue: '保存并继续',
      validating: '验证中...',
      skipForNow: '暂时跳过',
      needKeyTitle: '需要API密钥？',
      needKeySubtitle: '从OpenAI平台获取您的OpenAI API密钥：',
      steps: {
        step1: '访问 platform.openai.com/api-keys',
        step2: '登录您的OpenAI账户',
        step3: '点击"创建新密钥"',
        step4: '复制密钥并粘贴到上面'
      },
      securityNote: '您的API密钥存储在本地，永远不会发送到我们的服务器。',
      footer: '安全 • 私密 • 符合HIPAA的设计',
      errors: {
        required: '需要API密钥',
        invalidFormat: 'API密钥格式无效。OpenAI密钥以"sk-"开头',
        tooShort: 'API密钥似乎太短',
        saveFailed: '保存API密钥失败。请重试。'
      },
      success: 'API密钥保存成功！'
    }
  }
}

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: localStorage.getItem('app-language') || 'en', // Get from localStorage or default to English
  fallbackLocale: 'en',
  messages,
  globalInjection: true // Enable global $t
})

export default i18n
