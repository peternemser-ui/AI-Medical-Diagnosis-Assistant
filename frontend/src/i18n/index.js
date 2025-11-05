import { createI18n } from 'vue-i18n'

// Translation messages
const messages = {
  en: {
    app: {
      title: '🩺 AI Health Assistant',
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
      title: '💊 Drug Information',
      subtitle: 'Search medications and check interactions',
      searchPlaceholder: 'Search for a medication (e.g., \'aspirin\', \'lisinopril\')...',
      searchButton: '🔍 Search Drug Database',
      searching: 'Searching RxNorm Database...',
      found: 'Found {count} medication(s)',
      noResults: 'No medications found for "{query}"',
      tryAgain: 'Try searching for the generic name or brand name',
      selectedMeds: 'Selected Medications',
      checkInteractions: '⚠️ Check Drug Interactions',
      checking: 'Checking interactions...',
      interactionsFound: '⚠️ {count} Drug Interaction(s) Found',
      interactionsWarning: 'The selected medications may interact with each other. Consult your doctor or pharmacist.',
      noInteractions: '✅ No Known Interactions',
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
    dashboard: {
      title: 'Diagnosis Dashboard',
      patientInfo: 'Patient Information',
      diagnoses: 'Differential Diagnoses',
      confidence: 'Confidence',
      treatment: 'Treatment Recommendations',
      followUp: 'Follow-up',
      export: 'Export Report'
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
    }
  },
  es: {
    app: {
      title: '🩺 Asistente de Salud IA',
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
      title: '💊 Información de Medicamentos',
      subtitle: 'Busca medicamentos y verifica interacciones',
      searchPlaceholder: 'Buscar un medicamento (ej: \'aspirina\', \'lisinopril\')...',
      searchButton: '🔍 Buscar en Base de Datos',
      searching: 'Buscando en Base de Datos RxNorm...',
      found: 'Se encontraron {count} medicamento(s)',
      noResults: 'No se encontraron medicamentos para "{query}"',
      tryAgain: 'Intenta buscar por el nombre genérico o de marca',
      selectedMeds: 'Medicamentos Seleccionados',
      checkInteractions: '⚠️ Verificar Interacciones',
      checking: 'Verificando interacciones...',
      interactionsFound: '⚠️ {count} Interacción(es) Encontrada(s)',
      interactionsWarning: 'Los medicamentos seleccionados pueden interactuar entre sí. Consulta a tu médico o farmacéutico.',
      noInteractions: '✅ Sin Interacciones Conocidas',
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
    dashboard: {
      title: 'Panel de Diagnóstico',
      patientInfo: 'Información del Paciente',
      diagnoses: 'Diagnósticos Diferenciales',
      confidence: 'Confianza',
      treatment: 'Recomendaciones de Tratamiento',
      followUp: 'Seguimiento',
      export: 'Exportar Informe'
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
    }
  },
  fr: {
    app: {
      title: '🩺 Assistant Santé IA',
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
      title: '💊 Information sur les Médicaments',
      subtitle: 'Rechercher médicaments et vérifier interactions',
      searchPlaceholder: 'Rechercher un médicament (ex: \'aspirine\', \'lisinopril\')...',
      searchButton: '🔍 Rechercher dans la Base',
      searching: 'Recherche dans RxNorm...',
      found: '{count} médicament(s) trouvé(s)',
      noResults: 'Aucun médicament trouvé pour "{query}"',
      tryAgain: 'Essayez de rechercher par nom générique ou de marque',
      selectedMeds: 'Médicaments Sélectionnés',
      checkInteractions: '⚠️ Vérifier les Interactions',
      checking: 'Vérification des interactions...',
      interactionsFound: '⚠️ {count} Interaction(s) Trouvée(s)',
      interactionsWarning: 'Les médicaments sélectionnés peuvent interagir. Consultez votre médecin ou pharmacien.',
      noInteractions: '✅ Aucune Interaction Connue',
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
    dashboard: {
      title: 'Tableau de Bord Diagnostic',
      patientInfo: 'Informations Patient',
      diagnoses: 'Diagnostics Différentiels',
      confidence: 'Confiance',
      treatment: 'Recommandations de Traitement',
      followUp: 'Suivi',
      export: 'Exporter le Rapport'
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
    }
  },
  zh: {
    app: {
      title: '🩺 AI健康助手',
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
      title: '💊 药物信息',
      subtitle: '搜索药物并检查相互作用',
      searchPlaceholder: '搜索药物（例如：\'阿司匹林\'、\'赖诺普利\'）...',
      searchButton: '🔍 搜索药物数据库',
      searching: '正在搜索RxNorm数据库...',
      found: '找到{count}种药物',
      noResults: '未找到"{query}"的药物',
      tryAgain: '尝试搜索通用名称或品牌名称',
      selectedMeds: '已选药物',
      checkInteractions: '⚠️ 检查药物相互作用',
      checking: '正在检查相互作用...',
      interactionsFound: '⚠️ 发现{count}个药物相互作用',
      interactionsWarning: '所选药物可能相互作用。请咨询您的医生或药剂师。',
      noInteractions: '✅ 无已知相互作用',
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
    dashboard: {
      title: '诊断仪表板',
      patientInfo: '患者信息',
      diagnoses: '鉴别诊断',
      confidence: '置信度',
      treatment: '治疗建议',
      followUp: '随访',
      export: '导出报告'
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
