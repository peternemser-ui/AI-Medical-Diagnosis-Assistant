export const HELP_CONTENT = `# MedDiagnose AI -- User Documentation

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Your Account](#2-your-account)
3. [Starting a Consultation](#3-starting-a-consultation)
4. [The Diagnosis Process](#4-the-diagnosis-process)
5. [Understanding Your Results](#5-understanding-your-results)
6. [Photo Upload & Annotation](#6-photo-upload--annotation)
7. [Voice Mode](#7-voice-mode)
8. [Your Health Profile](#8-your-health-profile)
9. [Reports & History](#9-reports--history)
10. [Medications](#10-medications)
11. [Settings & Preferences](#11-settings--preferences)
12. [Subscription Plans](#12-subscription-plans)
13. [Frequently Asked Questions](#13-frequently-asked-questions)
14. [Privacy & Security](#14-privacy--security)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Getting Started

### Creating an Account

1. Navigate to the MedDiagnose AI home page.
2. Click **Log In** in the top-right corner, then switch to the **Sign Up** tab.
3. Enter your full name, email address, and a password.
   - Your password must be at least **12 characters** and include an uppercase letter, a lowercase letter, a number, and a special character.
4. After signing up you will be directed to configure your AI provider and set up your profile.

### First-Time Setup

After creating your account, a guided setup modal walks you through getting started:

1. **Connect Your AI Provider** -- Choose between Anthropic (Claude), OpenAI (GPT), Google, or the free local Ollama option. The setup panel shows the full 7-agent diagnostic pipeline so you know what powers each consultation.
2. **Set Up Your Profile** -- Enter your basic health information (age, gender, allergies, medications). This lets the AI skip demographic questions during consultations and jump straight to symptoms.
3. **Start Your First Consultation** -- Click "Start Consultation" on the home page or navigate to the Consult page.

### Choosing an AI Model

MedDiagnose AI supports multiple AI providers. You can switch models at any time from the model selector in the consultation header or from Settings.

| Model | Provider | Quality | Speed | Est. Cost / Diagnosis |
|---|---|---|---|---|
| Claude Opus 4.6 | Anthropic | Highest | Slow | ~$1.50 |
| Claude Sonnet 4.6 | Anthropic | High | Fast | ~$0.50 |
| Claude Haiku 4.5 | Anthropic | Good | Fastest | ~$0.05 |
| GPT-4o | OpenAI | High | Fast | ~$0.08 |
| GPT-4o Mini | OpenAI | Good | Fast | ~$0.01 |
| Llama 3.1 (Ollama) | Local | Moderate | Varies | Free |

**Recommendation:** Auto mode uses Sonnet for clinical reasoning and Haiku for simpler tasks, providing the best balance of diagnostic quality and cost.

All cost estimates reflect raw API usage with your own key -- MedDiagnose AI adds no markup.

---

## 2. Your Account

### Logging In

The login page shows any previously saved accounts for quick one-click access. You can also enter your email and password manually. Sessions use JWT tokens that expire after 15 minutes, with automatic refresh in the background.

### Profile Information

Your profile helps the AI provide better diagnoses by pre-filling information it would otherwise need to ask during the interview. Profile fields include:

- **Basic Info**: Name, email, gender, date of birth
- **Location**: City, state, ZIP code (used to suggest nearby specialists)
- **Medical Info**: Blood type, allergies, current medications
- **Medical History**: Past conditions, surgeries, family history, social history
- **Emergency Contact**: Name and phone number

Completing your profile means the AI skips demographic questions and goes straight to asking about your symptoms.

### Changing Your Password

1. Go to **Settings** (accessible from the user menu in the top-right corner).
2. Scroll to the **Change Password** section.
3. Enter your current password, then your new password and confirm it.
4. The new password must meet the same strength requirements: 12+ characters with mixed case, numbers, and special characters.
5. Click **Update Password**.

### Logging Out

Click your avatar in the top-right corner of any page, then select **Log Out** from the dropdown menu.

---

## 3. Starting a Consultation

### Accessing the Consultation Page

- Click **Start Consultation** on the home page hero section.
- Use the symptom input box on the landing page to type your symptoms and be taken directly to the consultation.
- Navigate to \`/consult\` from any page via the navigation links.

You must be logged in and have an API key configured to access consultations. If either is missing, you will be redirected to the login or API setup page.

### Avatar Mode vs. Chat Mode

MedDiagnose AI offers two consultation interface modes, toggled from the bottom toolbar:

**Avatar Mode (Default)**
- Dr. Hopps, an animated AI assistant, guides the conversation.
- A large text display shows the current question prominently.
- The avatar's eyes follow your cursor and expressions react to your symptoms.
- Best for focused, step-by-step consultations.

**Chat Mode**
- A traditional chat interface with message bubbles and full conversation history visible.
- A progress sidebar shows interview steps completed and remaining.
- Best for detailed conversations and reviewing previous answers.

### The Interview Process

A typical consultation follows these steps:

1. **Demographics** -- The AI asks your age and gender (skipped if already in your profile).
2. **Chief Complaint** -- "What brings you here today?" Describe your primary symptoms.
3. **PA Interview** -- Dr. Hopps (acting as a physician's assistant) asks targeted follow-up questions about the location, duration, severity, and character of your symptoms.
4. **Specialist Handoff** -- If your symptoms fall into a specific domain (e.g., dermatology, cardiology), a named specialist takes over the questioning. For example, Dr. Amara Okafor, MD, FAAD may handle skin-related concerns.
5. **Specialist Questions** -- Domain-specific clinical questions to gather the detailed information needed for accurate diagnosis.
6. **Diagnosis** -- All 7 AI agents analyze your case simultaneously and produce a comprehensive clinical report.

### Quick Symptom Input

Multiple input methods are available from the bottom toolbar:

- **Type** your symptoms in the text input box.
- **Speak** using the microphone button for voice recognition.
- **Tap body regions** on the interactive body map to indicate affected areas.
- **Select symptom chips** from categorized quick-select options: Common, Pain, Skin, Mental Health, and Urgent.

### Selecting a Model Mid-Consultation

The consultation header includes a model selector dropdown. Click the current model badge to see all available models, their estimated cost per diagnosis, and which API keys you have configured. You can switch models between questions without restarting the consultation.

---

## 4. The Diagnosis Process

### The 7-Agent Pipeline

When you submit your symptoms for diagnosis, 7 specialized AI agents collaborate on your case:

1. **Triage Agent** -- Assesses urgency on the ESI 1-5 scale, identifies red flags, and classifies the clinical domain.
2. **Diagnostician Agent** -- Creates a differential diagnosis with confidence scores using Bayesian clinical reasoning and pattern matching.
3. **Research Agent** -- Retrieves evidence-based clinical guidelines, drug interaction data, disease prevalence, and relevant medical literature.
4. **Specialist Agent** -- Provides domain-specific deep analysis using established diagnostic criteria (e.g., HEART score for chest pain, Wells criteria for PE, CURB-65 for pneumonia, PHQ-9 for depression).
5. **Treatment Agent** -- Develops a treatment plan including medication recommendations, dosages, lifestyle modifications, and dietary suggestions.
6. **Safety Agent** -- Reviews the entire plan for patient safety, checking 50+ contraindication rules, drug interactions, dosage limits, allergy risks, and dangerous combinations.
7. **Empathy Agent** -- Translates all clinical findings into plain, patient-friendly language with clear action checklists and summaries.

The Diagnostician and Research agents run in parallel to reduce wait time. All agents communicate via an asynchronous message bus and can request consultations from each other.

### During Analysis

While the agents are working:

- A **pipeline progress indicator** shows which agent is currently active.
- **Educational health tips** appear to keep you informed while you wait.
- An **estimated time remaining** is displayed.
- The avatar shows a "thinking" expression in Avatar Mode.

### Streaming Results

Results stream in real-time as each agent completes its analysis. You do not need to wait for all 7 agents to finish before seeing initial findings.

---

## 5. Understanding Your Results

### The Clinical Assessment Dashboard

After diagnosis, you are taken to a comprehensive clinical report with two view modes:

- **Simple View** -- A clean, patient-friendly summary of findings.
- **Advanced View** -- Full clinical detail including agent timings, reasoning chains, and technical data.

Toggle between views using the **Simple / Advanced** button in the report header.

### Report Sections

**Patient Info Bar**
- Patient age and gender
- Report date
- Urgency badge: Routine, See Soon, Urgent, or Emergency

**Summary Section**
- Primary diagnosis with confidence percentage
- Medical illustration of the affected body system
- Urgency classification
- "Recommended Next Steps" action cards

**What to Tell Your Doctor**
- Key bullet points to bring to your appointment
- Suggested questions to ask your healthcare provider

**Differential Diagnoses**
- Multiple possible conditions ranked by probability
- Each entry shows: confidence percentage, urgency level, relevant specialty
- Expandable "View Clinical Reasoning" with supporting and opposing evidence for each diagnosis
- Must-not-miss diagnoses are flagged prominently

**Recommended Tests**
- Diagnostic tests suggested by the AI, prioritized by clinical importance

**Treatment & Medications**
- Medication recommendations with dosage, frequency, and warnings
- Lifestyle modifications
- Dietary recommendations

**Safety Review**
- Safety status: PASS, PASS WITH WARNINGS, CAUTION, or ALERT
- Contraindication check results
- Drug interaction warnings
- Allergy risk assessment

**Action Items**
- A prioritized checklist organized by timeframe: RIGHT NOW, THIS WEEK, ONGOING
- Option to set a 2-week follow-up reminder (downloads a calendar .ics file)
- Option to share the summary with a family member

### Sharing Your Report

The report header includes a **Share** button with multiple options:

- **Copy Report Text** -- Copies a text summary to your clipboard for pasting into messages or patient portals.
- **Email Report** -- Opens your email client with a pre-formatted summary ready to send to your doctor.
- **Print Report** -- Opens the browser print dialog for a paper copy.
- **Share via...** -- Uses your device's native sharing (available on mobile and supported desktop browsers).
- **Download PDF** -- Generates a full clinical report PDF with appropriate medical disclaimers.

---

## 6. Photo Upload & Annotation

### Uploading a Photo

Click the **camera button** in the consultation toolbar. You have three options:

- **Take Photo** -- Opens your device camera to capture an image in real-time.
- **Upload Image** -- Select an existing image from your files.
- **Drag & Drop** -- Drag an image file directly onto the chat area.

### Describing Your Photo

After uploading, a description modal guides you through providing context:

1. **Select Body Location** -- Choose from: Head/Face, Neck, Chest, Abdomen, Back, Arms, Hands, Legs, or Feet.
2. **Tag Symptoms** -- Select relevant descriptors: Red rash, Swelling, Bruise, Blisters, Burning, and more.
3. **Select Duration** -- Indicate how long the issue has been present: Today, Few days, 1-2 weeks, 1+ month, or Ongoing.
4. **Add Details** -- Free-text field for any additional description.

### Annotating Your Photo

An annotation toolbar appears above the uploaded image with the following tools:

- **Circle** -- Draw a circle to highlight areas of concern.
- **Arrow** -- Point to specific features.
- **Draw** -- Freehand sketching for custom annotations.
- **Text** -- Place labels such as "pain here" or "swelling started here."
- **Undo** -- Remove the last annotation.
- **Clear** -- Remove all annotations.

The annotated image is sent to the AI at full resolution for analysis.

### Image Quality Warnings

The system automatically checks image quality and warns you if:

- The image is too dark.
- The image is overexposed.
- The resolution is very low.

These warnings help ensure the AI can analyze your photo accurately.

---

## 7. Voice Mode

### Speech Input

1. Click the **microphone button** in the consultation toolbar to start recording.
2. A waveform visualization shows your audio level in real-time.
3. After approximately 3 seconds of silence, your speech is automatically transcribed and sent.
4. Click the microphone button again to stop recording manually.

### Text-to-Speech

- Toggle audio responses on or off using the **speaker button** in the toolbar.
- When enabled, Dr. Hopps speaks responses aloud.
- In Avatar Mode, the avatar's mouth animates in sync with the speech.
- You can adjust the speech rate in Settings (from 0.7x slow to 1.3x fast).

### Hands-Free Mode

- Click the **hands-free button** for continuous voice interaction.
- Speak naturally -- the system listens, processes your input, and responds audibly.
- The cycle continues automatically without needing to press any buttons.
- Ideal for when your hands are occupied or for accessibility.

---

## 8. Your Health Profile

Access your profile from the user menu dropdown (top-right) or by navigating to \`/profile\`. The profile page also serves as the login and signup page for new users.

### Basic Information

- **Name** -- Your full name, displayed in the consultation and on reports.
- **Email** -- Used for account login. Stored encrypted on the server.
- **Gender** -- Helps the AI consider gender-specific conditions.
- **Date of Birth** -- Used to calculate your age for clinical assessments.

### Location

- **City, State, ZIP** -- Used to suggest nearby specialists and urgent care facilities in your report.

### Medical Information

- **Blood Type** -- Relevant for certain diagnoses and emergency scenarios.
- **Allergies** -- Type an allergy and press Enter to add it as a tag. Multiple allergies can be added. The Safety Agent checks all medications against your allergy list.
- **Current Medications** -- Type a medication name and press Enter to add it as a tag. The Safety Agent uses this list for drug interaction checks.

### Medical History (Expandable Section)

- **Past Conditions** -- Toggle checkboxes for: Diabetes, Hypertension, Heart Disease, Asthma, Cancer, Stroke, Thyroid disorders, Kidney disease, Liver disease, Arthritis, Depression/Anxiety.
- **Surgical History** -- Add past surgeries with the year they occurred.
- **Family History** -- A grid of conditions crossed with family members (Mother, Father, Sibling, Grandparent). Check the relevant boxes.
- **Social History** -- Select your status for: Smoking, Alcohol use, Exercise level, and Drug use.

### Emergency Contact

- **Contact Name** and **Phone Number** -- Stored locally for your reference in urgent situations.

---

## 9. Reports & History

### Accessing Reports

Navigate to **Reports** from the navigation bar or user menu. This page shows all your past consultations.

### Summary Statistics

At the top of the Reports page, four summary cards display:

- **Total Consultations** -- How many diagnoses you have completed.
- **Average Confidence** -- The mean confidence score across all your diagnoses, color-coded green (70%+), amber (40-69%), or grey (<40%).
- **Routine Count** -- How many of your consultations were classified as routine urgency.
- **Health Score** -- An aggregate score reflecting your overall health trends.

### View Modes

- **List View** -- A flat, sortable list of all consultations.
- **Timeline View** -- Consultations grouped chronologically by month.

### Searching and Filtering

Use the search bar to filter consultations by symptoms, diagnosis, or any keyword. Results update in real-time as you type.

### Viewing a Past Consultation

Click any consultation in the list to open its full **Session Detail** page, which shows the complete clinical report from that session.

### Comparing Diagnoses

If you have 2 or more past consultations:

1. Click **Compare Diagnoses** in the top-right of the Reports page.
2. Select exactly 2 consultations by clicking on them.
3. Click **Compare Selected** when the button activates.
4. A side-by-side comparison panel shows: symptoms, diagnosis, confidence scores, and urgency for each.
5. Common findings and key differences are highlighted.

### Exporting Data

- **Export All as JSON** -- Downloads all your consultation data as a structured JSON file for your records or for importing into other tools.

---

## 10. Medications

Navigate to **Medications** from the profile page navigation bar. The medication management section is organized into several tabs:

### My Medications (\`/medications\`)

View and manage your current medication list. Each entry shows the medication name, dosage, and frequency. Add new medications or remove ones you are no longer taking.

### Drug Interactions (\`/medications/interactions\`)

Check for potential drug-drug interactions between your current medications. The system flags dangerous combinations and provides clinical context about the severity and mechanism of each interaction.

### Food Interactions (\`/medications/food\`)

Discover foods that may interact with your medications. Learn which foods to avoid or limit, and which may affect absorption or effectiveness.

### Side Effects (\`/medications/side-effects\`)

Track and review side effects associated with your medications. Report side effects you are experiencing to help inform future consultations.

### Medication Schedule (\`/medications/schedule\`)

View a daily timeline of when to take each medication. Helps you organize complex multi-medication regimens with clear timing guidance.

### Refills (\`/medications/refills\`)

Track refill dates for your prescriptions. Stay ahead of running out by monitoring when each medication needs to be renewed.

### Pill Identifier (\`/medications/identify\`)

Use your device camera to photograph an unknown pill. The system analyzes the pill's shape, color, and imprint markings to identify it.

### Scan Prescription (\`/medications/scan\`)

Photograph a paper prescription to create a digital record. The system extracts medication names, dosages, and instructions from the image.

---

## 11. Settings & Preferences

Access Settings from the user menu dropdown or by navigating to \`/settings\`.

### Profile

View your current name and email. Click **Edit Profile** to go to the full profile editor.

### Change Password

Enter your current password, new password, and confirmation. The new password must meet the same strength requirements as signup (12+ characters, mixed case, number, special character).

### Appearance

- **Theme** -- Toggle between dark mode and light mode.
- **Language** -- Choose from 12 supported languages:
  - English, Espanol, Francais, Deutsch, Italiano, Portugues, Chinese, Japanese, Korean, Hindi, Arabic, Russian
  - The AI will respond in your selected language.

### Voice & Audio

- **Voice Input** -- Enable or disable microphone recording in consultations.
- **Audio Responses** -- Enable or disable text-to-speech for AI responses.
- **Speech Rate** -- When audio responses are enabled, adjust the speaking speed from 0.7x (slow) to 1.3x (fast) using a slider.

### Interface

- **Auto-scroll Chat** -- Automatically scroll to new messages as they appear.
- **Sound Effects** -- Play notification sounds for events like diagnosis completion.

### API Keys

Manage API keys for each supported provider:

- **Anthropic** -- For Claude models (sk-ant-api03-...)
- **OpenAI** -- For GPT models (sk-proj-...)
- **Google** -- For Google AI models
- **Ollama** -- Free, local AI. No key required. The settings page auto-detects whether Ollama is running and shows installed models.

For each provider:
1. Select the provider tab.
2. Enter your API key.
3. Click **Save Key**.
4. Use **Validate All API Keys** to test that all your saved keys are working.

A status indicator (green dot = configured, red dot = not configured) shows which providers have valid keys.

### AI Model

Choose which AI model powers your diagnoses. Each option shows:
- Model name and provider
- Quality description
- Estimated cost per diagnosis
- Any special badges (e.g., "Recommended", "Free")

Select a model by clicking its radio button, and the preference is saved immediately.

### Data & Privacy

Three data management options, each requiring confirmation:

- **Export All Data as JSON** -- Downloads everything (profile, consultations, settings) as a JSON file.
- **Clear Consultation History** -- Removes all past consultations while keeping your profile and settings.
- **Clear All Data** -- Permanently deletes all local data including profile, consultations, settings, and encryption keys. This action cannot be undone.

---

## 12. Subscription Plans

MedDiagnose AI offers four tiers. Toggle between monthly and annual billing (annual saves 20%).

| Feature | Free | Plus ($9.99/mo) | Pro ($29.99/mo) | Family ($49.99/mo) |
|---|---|---|---|---|
| Diagnoses per month | 2 | 20 | Unlimited | Unlimited |
| AI Models | Ollama only | Claude + GPT | All models incl. Opus | All models |
| PDF Export | No | Yes | Yes | Yes |
| Photo Analysis | No | Yes | Yes | Yes |
| Specialist Routing | No | Yes | Yes | Yes |
| Health History | Basic | Full | Full | Full |
| Family Members | 0 | 0 | 0 | Up to 5 |
| Priority Support | No | No | Yes | Yes |
| API Access | No | No | Yes | Yes |

### Annual Billing

Switch to annual billing using the toggle on the Pricing page. Annual plans cost 20% less than the equivalent monthly rate.

### Current Plan Indicator

Your current plan is highlighted with a green badge on the Pricing page. Plans below your current tier show as downgrades; plans above show upgrade CTAs.

### Reaching Your Limit

When you exhaust your monthly diagnosis allowance, an upgrade prompt appears. You can:
- Upgrade to a higher tier for more diagnoses.
- Continue using Ollama (the free local model) regardless of your plan tier.

### Demo Mode

If Stripe payment processing is not configured for the instance, the Pricing page shows a "Demo Mode" badge and all upgrades take effect instantly without payment.

---

## 13. Frequently Asked Questions

### General

#### Is this a replacement for seeing a doctor?

**No. Absolutely not.** MedAssist AI is an informational and educational tool only. It does not constitute medical advice, diagnosis, or treatment. No doctor-patient relationship is created by using this service. The platform displays this disclaimer prominently on the home page, before every consultation, and in every report. Always consult a qualified healthcare professional for medical decisions.

#### How accurate is the AI?

The 7-agent system provides comprehensive analysis from multiple clinical perspectives, but AI cannot replace a physical examination, laboratory tests, or medical imaging. AI models can produce incorrect, incomplete, or misleading information. Use MedAssist AI as a well-informed starting point for understanding your symptoms before speaking with a doctor -- never as a final answer.

#### What should I do in a medical emergency?

**Call 911 (or your local emergency number) immediately.** Do not use MedAssist AI for emergency medical situations. If you or someone else is experiencing chest pain, difficulty breathing, severe bleeding, signs of stroke, allergic reactions, loss of consciousness, or any other life-threatening symptoms, seek emergency medical care right away.

#### Is MedAssist AI FDA-approved?

No. MedAssist AI is not a medical device and is not FDA-approved or cleared. It is a software tool that provides AI-generated health information for educational and informational purposes only. It has not been evaluated by the FDA or any regulatory body for clinical use.

#### Can I use MedAssist AI for my children?

MedAssist AI is not intended for users under 18 years of age without parental or guardian consent and supervision. If you are using the platform on behalf of a minor, you accept full responsibility for how the information is used. Pediatric symptoms can present differently than adult symptoms -- always consult a pediatrician for children's health concerns.

---

### Privacy & Data

#### Is my data private?

Yes. All medical data is encrypted with AES-256 and stored only on your device. The server stores only your email (encrypted), password hash (bcrypt, irreversible), and session tokens. No symptoms, diagnoses, photos, or health records are ever stored on MedAssist AI servers.

#### What data is sent to AI providers?

When you start a consultation, your symptoms and any uploaded images are sent to the selected AI provider (Anthropic Claude, OpenAI GPT, or Google Gemini) for processing. We do not include your name, email, or other personally identifiable information in these requests. Each AI provider has its own data handling and retention policies -- we recommend reviewing their respective privacy policies.

#### Is MedAssist AI HIPAA-compliant?

MedAssist AI follows HIPAA-aware design principles including encryption at rest and in transit, session timeouts, and minimal data collection. However, MedAssist AI is not a covered entity under HIPAA and does not claim full HIPAA compliance. For protected health information (PHI) management, consult your healthcare provider's patient portal.

#### Can I delete all my data?

Yes. Go to **Settings > Privacy & Data** and click **Clear All Data** to permanently remove all locally stored health data, consultation history, and preferences. You can also request full account deletion, which removes your server-side account within 30 days.

#### Does MedAssist AI use cookies or track me?

MedAssist AI uses localStorage (not cookies) for storing settings, session tokens, and encrypted health data. We do not use third-party tracking cookies, advertising pixels, or analytics services. Usage analytics are stored locally on your device and can be cleared at any time from Settings.

---

### AI & Technology

#### What AI models power MedAssist AI?

MedAssist AI supports multiple AI providers:
- **Anthropic Claude** (Sonnet, Haiku) -- recommended for best clinical reasoning
- **OpenAI GPT-4o** -- strong general-purpose medical knowledge
- **Google Gemini** -- good balance of speed and quality
- **Ollama** -- free, runs locally on your computer with no data leaving your device

You can select your preferred model in Settings or during API key setup.

#### What is the 7-agent pipeline?

Each consultation runs through 7 specialized AI agents:
1. **Triage Agent** -- Assesses urgency and identifies red flags
2. **Diagnostician Agent** -- Generates differential diagnoses using clinical reasoning
3. **Research Agent** -- Reviews medical literature and clinical guidelines
4. **Specialist Agent** -- Provides domain-specific deep analysis
5. **Treatment Agent** -- Suggests treatment approaches and lifestyle changes
6. **Safety Agent** -- Checks for contraindications, drug interactions, and safety concerns
7. **Empathy Agent** -- Translates clinical findings into clear, compassionate language

The Diagnostician and Research agents run in parallel for faster results.

#### Can I use it without an API key?

Yes. Select **Ollama (free, local model)** during setup or in Settings. Ollama runs entirely on your computer, requires no API key, and provides unlimited free consultations. Diagnostic quality may be lower than cloud-hosted models, however.

#### How much does each consultation cost?

Cost depends on your selected AI model. Approximate costs per consultation:
- **Claude Sonnet**: ~$0.02-0.08
- **GPT-4o**: ~$0.03-0.10
- **Gemini**: ~$0.01-0.05
- **Ollama (local)**: Free

Actual cost is shown after each consultation. Subscription plans (Plus, Pro, Family) include credits that reduce or eliminate per-consultation costs.

#### Can the AI analyze images?

Yes. You can upload photos of skin conditions, rashes, injuries, or other visible symptoms. The AI Image Agent analyzes the photo alongside your described symptoms. However, AI image analysis has significant limitations -- it cannot replace dermatoscopy, biopsy, or in-person examination. Always have a medical professional evaluate concerning skin changes or lesions.

---

### Using the Platform

#### How do I get the best results?

1. **Complete your health profile** -- age, gender, medications, allergies, and medical history help the AI provide more relevant analysis.
2. **Be specific about symptoms** -- describe location, duration, severity, triggers, and what makes it better or worse.
3. **Upload photos when relevant** -- annotate them to highlight areas of concern.
4. **Answer all follow-up questions thoroughly** -- the more detail the AI has, the better its analysis.
5. **Use Claude Sonnet or higher** -- higher-tier models produce more thorough clinical reasoning.
6. **Mention current medications** -- this helps the Safety Agent check for drug interactions.

#### What languages are supported?

The interface supports 12 languages: English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi, Arabic, and Russian. The AI responds in your selected language.

#### Can my doctor see my reports?

You can share reports with your doctor through several methods:
- **Download PDF** and email it or bring a printed copy to your appointment.
- **Email Report** generates an email-ready summary you can send directly.
- **Copy Report Text** for pasting into patient portals or messaging systems.
- **Print Report** for a physical copy.

Reports include a clear disclaimer noting they are AI-generated and for informational purposes only.

#### What is the Second Opinion feature?

Second Opinion lets you run the same symptoms through multiple AI models simultaneously and compare their analyses side by side. This helps identify areas of agreement (higher confidence) and disagreement (areas to discuss with your doctor). It is not a substitute for consulting multiple real physicians.

#### How does the Medication Tracker work?

The Medication Tracker lets you:
- Log your current medications with dosage and frequency
- Check for drug-drug interactions using the interaction matrix
- Review food and lifestyle interactions that may affect your medications
- Set up a daily medication schedule with reminders
- Track side effects and adherence

All medication data is stored locally and encrypted. The interaction checker is for reference only -- always verify with your pharmacist or prescribing physician.

#### Are the nutrition recommendations personalized?

The Nutrition Planner considers your health profile (conditions, allergies, dietary preferences) when generating meal plans and recommendations. However, these are general suggestions -- not medical nutrition therapy. If you have diabetes, kidney disease, food allergies, or other conditions requiring specialized diets, consult a registered dietitian.

#### How do the mental health assessments work?

MedAssist AI includes validated screening tools:
- **PHQ-9** for depression screening (9 questions)
- **GAD-7** for anxiety screening (7 questions)

These are widely used clinical screening instruments, but they are **screening tools only** -- they do not constitute a clinical diagnosis. Your results should be discussed with a licensed mental health professional who can provide proper evaluation and treatment.

---

### Account & Billing

#### What subscription plans are available?

| Plan | Price | Includes |
|------|-------|----------|
| **Free** | $0/month | 3 consultations/month, basic features |
| **Plus** | $9.99/month | 20 consultations/month, PDF reports, medication tracker |
| **Pro** | $19.99/month | Unlimited consultations, all features, priority processing |
| **Family** | $29.99/month | Up to 5 family members, all Pro features |

Annual billing saves 20%. All plans include a 7-day free trial for paid tiers.

#### How do I cancel my subscription?

Go to **Settings > Subscription** and click **Cancel Subscription**. Your access continues until the end of your current billing period. You can resubscribe at any time. Refunds are available within 7 days of purchase.

#### What happens to my data if I cancel?

Your locally stored data (consultations, medications, journal entries) remains on your device regardless of subscription status. Server-side account data is retained for 30 days after cancellation, then permanently deleted.

#### How do I change my AI model or API key?

Go to **Settings > API Configuration** to add, change, or remove API keys for different providers. You can switch between providers at any time. Your consultation history is not affected by changing providers.

---

### Troubleshooting

#### The AI gave me concerning results. What should I do?

If the AI flags something as urgent or suggests you seek immediate medical attention, take that seriously and **contact a healthcare professional right away**. However, remember that AI can also overestimate severity. A doctor can properly evaluate your symptoms with physical examination and appropriate tests.

#### My consultation seems stuck or incomplete.

This can happen if the AI provider is experiencing high traffic or if your internet connection is unstable. Try:
1. Wait 30 seconds -- the pipeline may still be processing.
2. Refresh the page and start a new consultation.
3. Switch to a different AI provider in Settings.
4. If using Ollama, ensure the Ollama server is running locally.

#### I forgot my password.

Click **Forgot Password?** on the login page to receive a password reset email. If you don't receive it within a few minutes, check your spam folder.

---

## 14. Privacy & Security

### Data Encryption

- **AES-256 encryption** protects all medical data stored locally on your device.
- **PBKDF2 key derivation** generates the encryption key from your password, meaning only you can decrypt your data.
- **Fernet symmetric encryption** protects server-side data (limited to email addresses for authentication).

### What Is NOT Stored on the Server

- No medical symptoms, diagnoses, or health records
- No consultation history
- No photos or images
- No API keys
- No profile health information (allergies, medications, conditions)

### What IS Stored on the Server

- Your **email address** (encrypted) for authentication purposes
- Your **password hash** (bcrypt with salt -- cannot be reversed to recover the password)
- **JWT session tokens** that expire after 15 minutes

### HIPAA Considerations

- **Field-level encryption** for all personally identifiable information
- **Automatic session timeout** after 15 minutes of inactivity
- **Audit trail** for data access events
- **No data sharing** with third parties
- **Local-only health data** means the server never has access to protected health information

### API Key Security

Your AI provider API keys are stored in your browser's localStorage, never transmitted to MedDiagnose AI servers. They are sent directly from your browser to the AI provider (Anthropic, OpenAI, or Google) during consultations.

### Deleting Your Data

You can delete all your data at any time from **Settings > Data & Privacy**:
- **Clear Consultation History** removes all past diagnoses.
- **Clear All Data** removes everything, including your profile and encryption keys.
- Clearing your browser data also removes all locally stored information permanently.

---

## 15. Troubleshooting

### "Invalid email or password"

- Verify your email address is typed correctly.
- Passwords are case-sensitive -- check your Caps Lock key.
- If you have forgotten your password, you will need to create a new account (passwords cannot be recovered because they derive the local encryption key).

### Diagnosis shows "Awaiting Analysis" or does not complete

- Your API key may not be configured correctly. Go to **Settings > API Keys** and click **Validate All API Keys**.
- If validation fails, re-enter your key and save it again.
- Try switching to **Ollama (free)** in Settings to test whether the issue is with your API key or the application.

### Slow diagnosis (more than 2 minutes)

- Check which model you are using in **Settings > AI Model**. Ollama (local) can be significantly slower than cloud models depending on your hardware.
- Larger models like Claude Opus are slower but more thorough. Claude Sonnet or Haiku are faster alternatives.
- Ensure your internet connection is stable for cloud-based models.

### Photo upload not working

- Check that your browser has **camera permissions** enabled for the site.
- Try **Upload Image** (file picker) instead of **Take Photo** (camera) to rule out camera access issues.
- Ensure the image file is under **10MB**.
- Supported formats: JPEG, PNG, WebP.

### Avatar not showing or not animated

- Refresh the page with Ctrl+Shift+R (hard refresh) to clear cached assets.
- Check the browser developer console (F12) for errors.
- Try clearing your browser cache if the issue persists.
- Ensure hardware acceleration is enabled in your browser settings.

### Voice input not working

- Verify your browser supports the Web Speech API (Chrome and Edge have the best support).
- Check that microphone permissions are granted for the site.
- Ensure **Voice Input** is enabled in **Settings > Voice & Audio**.
- Test your microphone in another application to rule out hardware issues.

### API keys keep disappearing

- This issue was resolved in a recent update. If you are still experiencing it:
  1. Go to **Settings > API Keys**.
  2. Re-enter your key for the affected provider.
  3. Click **Save Key** and wait for the "Saved!" confirmation.
  4. Refresh the page to verify the key persists.

### Cannot access the admin dashboard

- The admin dashboard requires an **admin role** assigned to your account. Standard users are redirected to the consultation page.
- If you believe you should have admin access, contact your system administrator.
- Try logging out and logging back in to refresh your session token.

### Consultation page redirects to login

- Your session may have expired (sessions last 15 minutes). Log in again.
- If you are immediately redirected after logging in, check that you have an API key configured. The consultation page requires both authentication and a configured API key.

### Data export produces an empty file

- You may not have any consultation data stored locally. Complete at least one diagnosis before exporting.
- If you recently cleared your browser data, all local consultation history has been permanently removed.

---

*MedDiagnose AI is an informational tool that provides AI-generated health assessments for educational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.*
`
