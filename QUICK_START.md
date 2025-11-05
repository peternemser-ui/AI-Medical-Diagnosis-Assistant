# Quick Start Guide - AI Medical Diagnosis Assistant v2.0

## 🚀 What's New?

Your application has been comprehensively improved with **professional-grade enhancements**:

- ✅ **9 Reusable Composables** - Clean, organized code
- ✅ **Security Features** - Input sanitization & API key encryption
- ✅ **Error Handling** - Automatic retry with exponential backoff
- ✅ **Accessibility** - ARIA labels, focus management, screen reader support
- ✅ **Export Features** - Save conversations as PDF, JSON, HTML, or Text
- ✅ **Loading States** - Professional loading skeletons
- ✅ **Backend Middleware** - Rate limiting, validation, security headers
- ✅ **Offline Support** - Graceful degradation when offline

---

## 📁 New File Structure

```
frontend/src/
├── composables/           ⭐ NEW
│   ├── useQuestionnaire.js
│   ├── useVoice.js
│   ├── useEmergency.js
│   ├── useChat.js
│   ├── useApiStatus.js
│   ├── useRetry.js
│   ├── useOffline.js
│   └── useTheme.js
├── lib/                   ⭐ NEW
│   ├── sanitization.js
│   ├── encryption.js
│   ├── focusManagement.js
│   └── exportConversation.js
└── components/
    ├── LoadingSkeleton.vue  ⭐ NEW
    └── ErrorBoundary.vue    ⭐ NEW

backend/
├── middleware.py          ⭐ NEW
└── validators.py          ⭐ NEW
```

---

## 🎯 Quick Examples

### 1. Use Chat Composable

**Before:**
```vue
<script setup>
const messages = ref([])
const addMessage = (text) => {
  messages.value.push({ text, timestamp: new Date() })
}
</script>
```

**After:**
```vue
<script setup>
import { useChat } from '@/composables/useChat'

const { messages, addUserMessage, addAssistantMessage, exportAsJSON } = useChat()

// Add messages easily
addUserMessage('Hello')
addAssistantMessage('Hi! How can I help?')

// Export conversation
exportAsJSON() // Downloads JSON file
</script>
```

### 2. Show Loading Skeleton

```vue
<template>
  <LoadingSkeleton v-if="loading" variant="message" :count="3" />
  <ChatArea v-else :messages="messages" />
</template>

<script setup>
import LoadingSkeleton from '@/components/LoadingSkeleton.vue'
</script>
```

### 3. Add Error Boundary

```vue
<template>
  <ErrorBoundary
    title="Oops!"
    :on-retry="reload"
    :show-details="true"
  >
    <YourComponent />
  </ErrorBoundary>
</template>

<script setup>
import ErrorBoundary from '@/components/ErrorBoundary.vue'

function reload() {
  // Reload logic
}
</script>
```

### 4. Export Conversation

```vue
<script setup>
import { exportConversation } from '@/lib/exportConversation'

async function exportAsPDF() {
  await exportConversation(messages.value, 'pdf', {
    patientInfo: {
      'Age': 35,
      'Gender': 'Female',
      'Date': new Date().toLocaleDateString()
    }
  })
}
</script>
```

### 5. Sanitize User Input

```vue
<script setup>
import { sanitizeMedicalInput, validateInput } from '@/lib/sanitization'

function handleInput(rawInput) {
  // Validate
  const { valid, error } = validateInput(rawInput, {
    minLength: 5,
    maxLength: 10000,
    checkXss: true
  })

  if (!valid) {
    console.error(error)
    return
  }

  // Sanitize
  const clean = sanitizeMedicalInput(rawInput)

  // Use clean input
  processSymptoms(clean)
}
</script>
```

### 6. Encrypt API Key

```vue
<script setup>
import { storeApiKey, retrieveApiKey } from '@/lib/encryption'

async function saveApiKey(key) {
  // Automatically encrypted
  await storeApiKey(key)
  console.log('✅ API key encrypted and stored')
}

async function loadApiKey() {
  // Automatically decrypted
  const key = await retrieveApiKey()
  return key
}
</script>
```

---

## 🔧 Backend Usage

### 1. Add Middleware to main.py

```python
from middleware import (
    RateLimitMiddleware,
    LoggingMiddleware,
    ValidationMiddleware,
    SecurityHeadersMiddleware
)

# Add middleware in order
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ValidationMiddleware)
```

### 2. Use Validators

```python
from validators import DiagnosisRequest

@app.post("/api/diagnose")
async def diagnose(request: DiagnosisRequest):
    # request is automatically validated!
    age = request.age           # Validated: 0-150
    gender = request.gender     # Validated: not empty
    symptoms = request.symptoms # Validated: 5-10000 chars

    # Process safely...
```

### 3. Use Cache

```python
from middleware import cache

# Get from cache
result = cache.get(f"diagnosis:{user_id}")
if result:
    return result

# Compute and cache
diagnosis = expensive_ai_call()
cache.set(f"diagnosis:{user_id}", diagnosis)
```

---

## 🎨 Component Examples

### LoadingSkeleton Variants

```vue
<!-- Text lines -->
<LoadingSkeleton variant="text" width="80%" />

<!-- Circle (avatar) -->
<LoadingSkeleton variant="circle" width="48px" />

<!-- Card -->
<LoadingSkeleton variant="card" />

<!-- Message -->
<LoadingSkeleton variant="message" :count="3" />

<!-- List -->
<LoadingSkeleton variant="list" :count="5" />

<!-- Dark mode -->
<LoadingSkeleton variant="card" :dark="true" />

<!-- Custom animation -->
<LoadingSkeleton variant="text" animation="pulse" />
```

---

## 📚 Composable Cheat Sheet

### useQuestionnaire

```javascript
const {
  currentQuestion,      // Current question object
  progress,            // { current, total, percentage }
  validateResponse,    // Validate user answer
  addResponse,         // Add answer and move next
  getAllResponses,     // Get all answers
  reset                // Start over
} = useQuestionnaire()
```

### useVoice

```javascript
const {
  isRecording,         // Is currently recording
  soundEnabled,        // Is sound on
  startRecording,      // Start voice input
  stopRecording,       // Stop recording
  speak,              // Text-to-speech
  toggleSound         // Toggle sound on/off
} = useVoice()
```

### useEmergency

```javascript
const {
  showEmergency,       // Should show alert
  emergencyType,       // Emergency category
  emergencyMessage,    // Alert message
  detectEmergency,     // Check for emergencies
  showAlert,          // Display alert
  dismissAlert        // Hide alert
} = useEmergency()
```

### useApiStatus

```javascript
const {
  apiStatus,           // true/false/null
  isEnhancedMode,      // Has API key and connected
  statusMessage,       // User-friendly status
  statusColor,         // green/yellow/red
  checkHealth,        // Check API health
  refresh             // Force status refresh
} = useApiStatus()
```

### useOffline

```javascript
const {
  isOnline,            // Connection status
  wasOffline,          // Was previously offline
  checkConnectivity,   // Manual connection check
  getOfflineDuration   // How long offline (seconds)
} = useOffline()
```

---

## 🔒 Security Features

### 1. **Input Sanitization**
- ✅ XSS prevention
- ✅ SQL injection detection
- ✅ HTML stripping
- ✅ Length validation

### 2. **API Key Encryption**
- ✅ AES-256-GCM encryption
- ✅ Device-specific keys
- ✅ Automatic migration
- ✅ Secure deletion

### 3. **Rate Limiting**
- ✅ Frontend: 20 req/min
- ✅ Backend: 60 req/min
- ✅ Clear error messages
- ✅ Automatic reset

### 4. **Security Headers**
- ✅ X-Content-Type-Options: nosniff
- ✅ X-Frame-Options: DENY
- ✅ X-XSS-Protection: 1
- ✅ Strict-Transport-Security
- ✅ Content-Security-Policy

---

## 📊 Export Formats

### Available Formats

| Format | Extension | Best For |
|--------|-----------|----------|
| **PDF** | `.pdf` | Printing, official records |
| **JSON** | `.json` | Data backup, processing |
| **HTML** | `.html` | Sharing, web viewing |
| **Text** | `.txt` | Simple viewing, email |

### Usage

```javascript
import { exportConversation } from '@/lib/exportConversation'

// Export as PDF
await exportConversation(messages, 'pdf', metadata)

// Export as JSON
await exportConversation(messages, 'json', metadata)

// Export as HTML
await exportConversation(messages, 'html', metadata)

// Export as Text
await exportConversation(messages, 'text', metadata)
```

---

## 🐛 Error Handling

### API Errors

```javascript
import { diagnose, ApiError } from '@/services/api'

try {
  const result = await diagnose(data)
} catch (error) {
  if (error instanceof ApiError) {
    if (error.status === 429) {
      // Rate limited
      alert(`Too many requests. Wait ${error.details.resetTime}ms`)
    } else if (error.isRetryable) {
      // Can retry
      alert('Temporary error. Please try again.')
    } else {
      // Permanent error
      alert(error.message)
    }
  }
}
```

### Component Errors

```vue
<ErrorBoundary
  :on-retry="handleRetry"
  :on-reset="handleReset"
  :show-details="isDevelopment"
>
  <MyComponent />
</ErrorBoundary>
```

---

## 🎯 Best Practices

### 1. **Always Sanitize User Input**

```javascript
import { sanitizeMedicalInput } from '@/lib/sanitization'

// ✅ Good
const clean = sanitizeMedicalInput(userInput)
await diagnose({ symptoms: clean })

// ❌ Bad
await diagnose({ symptoms: userInput })
```

### 2. **Use Composables for Logic**

```javascript
// ✅ Good
import { useChat } from '@/composables/useChat'
const { messages, addMessage } = useChat()

// ❌ Bad
const messages = ref([])
// ... duplicate logic in every component
```

### 3. **Show Loading States**

```vue
<!-- ✅ Good -->
<LoadingSkeleton v-if="loading" variant="message" />
<Content v-else />

<!-- ❌ Bad -->
<div v-if="loading">Loading...</div>
```

### 4. **Handle Errors Gracefully**

```vue
<!-- ✅ Good -->
<ErrorBoundary :on-retry="reload">
  <DiagnosisView />
</ErrorBoundary>

<!-- ❌ Bad -->
<DiagnosisView /> <!-- No error handling -->
```

---

## 📈 Performance Tips

1. **Lazy Load Heavy Components**
```javascript
const Dashboard = defineAsyncComponent(() =>
  import('@/components/DiagnosisDashboard.vue')
)
```

2. **Use Loading Skeletons**
```vue
<LoadingSkeleton variant="card" />
```

3. **Enable Caching (Backend)**
```python
result = cache.get(key) or expensive_operation()
```

4. **Monitor Rate Limits**
```javascript
const { remaining } = getRateLimitStatus()
if (remaining < 5) {
  console.warn('Approaching rate limit')
}
```

---

## 🆘 Troubleshooting

### Issue: "Rate limit exceeded"
**Solution:** Wait 60 seconds or use `resetRateLimit()` in development

### Issue: "API key not found"
**Solution:** Run `await migrateApiKey()` to migrate old keys

### Issue: "Request timeout"
**Solution:** Check backend is running. Automatic retry will handle temporary issues.

### Issue: "XSS detected in input"
**Solution:** Input contains HTML/scripts. Sanitize with `sanitizeMedicalInput()`

---

## 📞 Support

- **Full Documentation:** See `IMPROVEMENTS.md`
- **Code Examples:** Check `src/composables/` directory
- **Issues:** [GitHub Issues](https://github.com/anthropics/claude-code/issues)

---

## ✅ Checklist for Using New Features

- [ ] Import composables instead of duplicating logic
- [ ] Use `LoadingSkeleton` for loading states
- [ ] Wrap components in `ErrorBoundary`
- [ ] Sanitize all user input
- [ ] Encrypt sensitive data
- [ ] Add ARIA labels for accessibility
- [ ] Export conversations for users
- [ ] Add backend middleware
- [ ] Use Pydantic validators
- [ ] Enable caching for performance

---

**Happy Coding! 🚀**
