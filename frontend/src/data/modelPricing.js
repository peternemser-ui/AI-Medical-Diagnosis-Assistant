/**
 * Per-model pricing displayed to users.
 * Prices are per-diagnosis estimates based on average token usage (~2K input, ~2K output).
 *
 * Multi-agent pipeline uses ~7 calls per diagnosis.
 * Single-model (OpenAI) uses 1 call.
 */

export const MODEL_PRICING = {
  'auto': {
    label: 'Auto (Recommended)',
    description: 'Best balance of quality and speed',
    estimatedCost: '~$0.50',
    perDiagnosis: 0.50,
    provider: 'auto',
    badge: 'default',
  },
  'opus': {
    label: 'Claude Opus 4.6',
    description: 'Highest quality. Most thorough clinical reasoning.',
    estimatedCost: '~$2.50',
    perDiagnosis: 2.50,
    provider: 'anthropic',
    badge: 'best quality',
  },
  'sonnet': {
    label: 'Claude Sonnet 4.6',
    description: 'Fast and capable. Good quality for most cases.',
    estimatedCost: '~$0.50',
    perDiagnosis: 0.50,
    provider: 'anthropic',
    badge: 'fast',
  },
  'haiku': {
    label: 'Claude Haiku 4.5',
    description: 'Fastest Anthropic model. Good for simple symptom checks.',
    estimatedCost: '~$0.10',
    perDiagnosis: 0.10,
    provider: 'anthropic',
    badge: 'budget',
  },
  'gpt-4o': {
    label: 'GPT-4o',
    description: 'OpenAI flagship. Strong general reasoning.',
    estimatedCost: '~$0.40',
    perDiagnosis: 0.40,
    provider: 'openai',
    badge: 'OpenAI',
  },
  'gpt-4o-mini': {
    label: 'GPT-4o Mini',
    description: 'Lower cost, good for routine cases.',
    estimatedCost: '~$0.06',
    perDiagnosis: 0.06,
    provider: 'openai',
    badge: 'OpenAI',
  },
  'o3': {
    label: 'OpenAI o3',
    description: 'Advanced reasoning. Excellent for complex cases.',
    estimatedCost: '~$0.30',
    perDiagnosis: 0.30,
    provider: 'openai',
    badge: 'OpenAI',
  },
  'gemini-2.5-pro': {
    label: 'Gemini 2.5 Pro',
    description: 'Google flagship. Strong medical knowledge.',
    estimatedCost: '~$0.35',
    perDiagnosis: 0.35,
    provider: 'google',
    badge: 'Google',
  },
  'gemini-2.5-flash': {
    label: 'Gemini 2.5 Flash',
    description: 'Fast Google model. Good balance of speed and quality.',
    estimatedCost: '~$0.05',
    perDiagnosis: 0.05,
    provider: 'google',
    badge: 'Google',
  },
  'llama3.1:8b': {
    label: 'Llama 3.1 8B (Ollama)',
    description: 'Runs locally. Free, no API key needed.',
    estimatedCost: 'Free',
    perDiagnosis: 0,
    provider: 'ollama',
    badge: 'free',
  },
  'qwen2.5:7b': {
    label: 'Qwen 2.5 7B (Ollama)',
    description: 'Local model with strong multilingual support. Free.',
    estimatedCost: 'Free',
    perDiagnosis: 0,
    provider: 'ollama',
    badge: 'free',
  },
  'gemma2:2b': {
    label: 'Gemma 2 2B (Ollama)',
    description: 'Smallest and fastest local model. Free.',
    estimatedCost: 'Free',
    perDiagnosis: 0,
    provider: 'ollama',
    badge: 'fast + free',
  },
}

export function getModelPrice(modelId) {
  return MODEL_PRICING[modelId] || MODEL_PRICING['auto']
}

export function formatModelCost(modelId) {
  const info = getModelPrice(modelId)
  return info.estimatedCost || 'Free'
}
