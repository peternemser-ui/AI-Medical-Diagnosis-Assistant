<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">
    <AppNav />

    <main class="max-w-3xl mx-auto px-4 py-8 pb-16">

      <!-- Page Header -->
      <div class="mb-10">
        <div class="inline-flex items-center gap-2 mb-4 px-3 py-1 rounded-full text-xs font-semibold border"
          :class="isDark ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' : 'bg-indigo-50 text-indigo-700 border-indigo-200'">
          Legal
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">Privacy Policy</h1>
        <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Last updated: April 2026 &nbsp;&middot;&nbsp; Effective: April 1, 2026
        </p>
        <p class="mt-4 text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
          MedAssist AI, Inc. ("we," "us," or "our") is committed to protecting your privacy. This Privacy Policy
          explains how we collect, use, store, and protect information when you use MedAssist AI (the "Service").
          Please read it carefully.
        </p>
      </div>

      <!-- Sections -->
      <div class="space-y-6">

        <!-- 1. Introduction -->
        <section :class="sectionClass">
          <h2 :class="headingClass">1. Introduction</h2>
          <div :class="bodyClass">
            <p>
              Your privacy — and especially the privacy of your health information — matters deeply to us. This
              Privacy Policy covers what information we collect, why we collect it, how we use it, how we protect it,
              and the choices you have regarding your information.
            </p>
            <p class="mt-3">
              This policy applies to all users of the MedAssist AI web application, including visitors who browse
              without an account and registered users who use the consultation and health tracking features.
            </p>
            <p class="mt-3">
              By using the Service, you agree to the collection and use of your information as described in this
              Privacy Policy. If you do not agree, please discontinue use of the Service.
            </p>
          </div>
        </section>

        <!-- 2. Information We Collect -->
        <section :class="sectionClass">
          <h2 :class="headingClass">2. Information We Collect</h2>
          <div :class="bodyClass">
            <p class="font-semibold mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
              We collect only the information necessary to provide and improve the Service:
            </p>

            <div class="space-y-4">
              <div>
                <h3 class="font-semibold text-sm mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  a) Account Information
                </h3>
                <p>
                  When you create an account, we collect your full name, email address, and a securely hashed version
                  of your password. We do not store your password in plain text. This information is stored on our
                  servers and is used to authenticate you and manage your account.
                </p>
              </div>

              <div>
                <h3 class="font-semibold text-sm mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  b) Health Profile Data
                </h3>
                <p>
                  If you choose to enter health profile information — such as age, biological sex, weight, known
                  medical conditions, medications, and allergies — this data is encrypted with AES-256 encryption and
                  stored locally on your device using your browser's local storage. This data is NOT transmitted to or
                  stored on our servers.
                </p>
              </div>

              <div>
                <h3 class="font-semibold text-sm mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  c) Consultation Data
                </h3>
                <p>
                  Symptom descriptions you enter for AI consultations, along with the AI-generated responses, are
                  stored locally on your device in encrypted form. Consultation queries are transmitted to our AI
                  provider partners (see Section 5) for processing, but we do not persistently store the full
                  contents of your consultations on our servers.
                </p>
              </div>

              <div>
                <h3 class="font-semibold text-sm mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  d) Usage Analytics
                </h3>
                <p>
                  We collect anonymized analytics data, such as which pages and features you visit and general
                  usage patterns. This data is used locally for service improvement purposes and is not shared with
                  external analytics platforms. We do not use third-party tracking cookies for advertising.
                </p>
              </div>

              <div>
                <h3 class="font-semibold text-sm mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  e) Technical Data
                </h3>
                <p>
                  We may collect basic technical data including your browser type, operating system, device type,
                  IP address, and approximate geographic region. This information is collected for security, fraud
                  prevention, and to optimize the Service for your device. It is not used to personally identify
                  you for advertising purposes.
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- 3. How We Use Information -->
        <section :class="sectionClass">
          <h2 :class="headingClass">3. How We Use Your Information</h2>
          <div :class="bodyClass">
            <p>We use the information we collect for the following purposes:</p>
            <ul class="mt-3 space-y-2 list-disc list-inside">
              <li>To create and manage your account and authenticate your identity.</li>
              <li>To provide AI-powered health information and consultation features.</li>
              <li>To process subscription payments and manage your billing relationship.</li>
              <li>To send transactional communications, such as account verification emails, billing receipts,
                and important service notices.</li>
              <li>To improve the quality, accuracy, and safety of the Service.</li>
              <li>To detect and prevent fraud, abuse, and security incidents.</li>
              <li>To comply with applicable legal obligations, court orders, or regulatory requirements.</li>
              <li>To enforce our Terms of Service.</li>
            </ul>
            <p class="mt-3">
              We do not sell your personal information to third parties. We do not use your health information for
              advertising, marketing profiling, or any purpose beyond what is described in this Privacy Policy.
            </p>
          </div>
        </section>

        <!-- 4. Data Storage & Security -->
        <section :class="sectionClass">
          <h2 :class="headingClass">4. Data Storage &amp; Security</h2>
          <div :class="bodyClass">
            <p>
              Protecting your data is a core part of how we design and operate the Service. Here is how we approach
              data storage and security:
            </p>
            <div class="mt-4 space-y-3">
              <div class="flex items-start gap-3 p-3 rounded-lg"
                :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                <div class="flex-shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center bg-emerald-500/15">
                  <svg class="w-3 h-3 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                    Local-First Health Data
                  </p>
                  <p class="text-sm mt-0.5">
                    Your health information is encrypted with AES-256 encryption and stored only on your device.
                    We cannot access, view, or recover this data.
                  </p>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 rounded-lg"
                :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                <div class="flex-shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center bg-emerald-500/15">
                  <svg class="w-3 h-3 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                    Minimal Server-Side Storage
                  </p>
                  <p class="text-sm mt-0.5">
                    Our servers store only your email address, hashed password (bcrypt), and subscription status.
                    No health content is stored server-side.
                  </p>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 rounded-lg"
                :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                <div class="flex-shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center bg-emerald-500/15">
                  <svg class="w-3 h-3 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                    API Key Encryption
                  </p>
                  <p class="text-sm mt-0.5">
                    If you store your AI provider API keys in the Service, they are encrypted using Fernet symmetric
                    encryption and stored in your device's local storage. They are never transmitted to our servers.
                  </p>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 rounded-lg"
                :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                <div class="flex-shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center bg-emerald-500/15">
                  <svg class="w-3 h-3 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                    HIPAA-Aware Design
                  </p>
                  <p class="text-sm mt-0.5">
                    Our system architecture follows HIPAA-aware design principles including access controls, data
                    minimization, and audit-ready logging. We do not sell or share health data with third parties.
                  </p>
                </div>
              </div>
            </div>
            <p class="mt-4">
              Despite our security measures, no method of electronic storage or transmission is 100% secure. We cannot
              guarantee absolute security of your information. In the event of a data breach affecting your account
              information, we will notify you as required by applicable law.
            </p>
          </div>
        </section>

        <!-- 5. Third-Party AI Providers -->
        <section :class="sectionClass">
          <h2 :class="headingClass">5. Third-Party AI Providers</h2>
          <div :class="bodyClass">
            <p>
              The AI features of MedAssist AI are powered by third-party large language model (LLM) providers.
              When you submit a consultation query, your symptom description and related context may be transmitted
              to one or more of the following providers for AI processing:
            </p>
            <ul class="mt-3 space-y-1 list-disc list-inside">
              <li><strong>Anthropic</strong> — Claude (claude.ai)</li>
              <li><strong>OpenAI</strong> — GPT models (openai.com)</li>
              <li><strong>Google</strong> — Gemini models (deepmind.google)</li>
            </ul>
            <p class="mt-3">
              These providers process queries subject to their own privacy policies and data handling practices,
              which may include using query data to improve their models unless you or we opt out of such use.
              We encourage you to review the privacy policies of these providers.
            </p>
            <p class="mt-3">
              We design our AI query pipeline to minimize the inclusion of personally identifiable information (PII).
              Specifically, we do not include your name, email address, or account identifiers in AI queries.
              However, any health information you include in your symptom description is transmitted as part of
              the query for processing.
            </p>
          </div>
        </section>

        <!-- 6. Data Retention -->
        <section :class="sectionClass">
          <h2 :class="headingClass">6. Data Retention</h2>
          <div :class="bodyClass">
            <ul class="space-y-3">
              <li>
                <strong class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Local device data
                </strong>
                — Health profiles, consultation history, and settings stored on your device persist until you
                explicitly clear them via your account settings, clear your browser's local storage, or delete
                your account.
              </li>
              <li>
                <strong class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Server account data
                </strong>
                — Your email address, hashed password, and subscription records are retained while your account
                is active and for up to 30 days after account deletion to allow for dispute resolution and
                legal compliance.
              </li>
              <li>
                <strong class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Payment records
                </strong>
                — Transaction and billing records are retained for 7 years to comply with applicable financial
                and tax regulations.
              </li>
              <li>
                <strong class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Security logs
                </strong>
                — Server-side access and security logs are retained for up to 90 days for fraud prevention and
                security purposes.
              </li>
            </ul>
          </div>
        </section>

        <!-- 7. Your Rights -->
        <section :class="sectionClass">
          <h2 :class="headingClass">7. Your Rights</h2>
          <div :class="bodyClass">
            <p>
              You have the following rights with respect to your personal information. To exercise any of these
              rights, contact us at
              <a href="mailto:privacy@medassist.ai" :class="linkClass">privacy@medassist.ai</a>:
            </p>
            <ul class="mt-4 space-y-3">
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">1</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Access:</span>
                  <span class="ml-1">You may request a copy of the personal information we hold about you.</span>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">2</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Correction:</span>
                  <span class="ml-1">You may request that we correct inaccurate or incomplete account information.</span>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">3</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Deletion:</span>
                  <span class="ml-1">You may request deletion of your account and associated server-side data. Local
                    device data can be cleared directly from your account settings.</span>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">4</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Data Export:</span>
                  <span class="ml-1">You may export your locally stored health data in JSON format from your account
                    settings at any time.</span>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">5</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Opt-Out of Analytics:</span>
                  <span class="ml-1">You may opt out of anonymized usage analytics through your account settings.</span>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-700'">6</div>
                <div>
                  <span class="font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Account Deletion:</span>
                  <span class="ml-1">You may request permanent deletion of your account and all associated server-side
                    data by emailing
                    <a href="mailto:privacy@medassist.ai" :class="linkClass">privacy@medassist.ai</a>.</span>
                </div>
              </li>
            </ul>
            <p class="mt-4">
              Depending on your jurisdiction, you may also have additional rights under applicable privacy laws
              such as the California Consumer Privacy Act (CCPA) or the General Data Protection Regulation (GDPR).
              We will honor all legally required rights requests within 30 days of receipt.
            </p>
          </div>
        </section>

        <!-- 8. Children's Privacy -->
        <section :class="sectionClass">
          <h2 :class="headingClass">8. Children's Privacy</h2>
          <div :class="bodyClass">
            <p>
              MedAssist AI is not intended for use by individuals under the age of 18 without verified parental or
              legal guardian consent. We do not knowingly collect personal or health information from minors under
              the age of 13. If you are a parent or guardian and believe your child has provided us with personal
              information without your consent, please contact us immediately at
              <a href="mailto:privacy@medassist.ai" :class="linkClass">privacy@medassist.ai</a> and we will take
              prompt steps to delete such information.
            </p>
            <p class="mt-3">
              Users between the ages of 13 and 17 may use the Service only with documented parental or legal guardian
              consent. If you are under 18, please have a parent or guardian review and agree to these terms and the
              Privacy Policy on your behalf before using the Service.
            </p>
          </div>
        </section>

        <!-- 9. Cookies & Local Storage -->
        <section :class="sectionClass">
          <h2 :class="headingClass">9. Cookies &amp; Local Storage</h2>
          <div :class="bodyClass">
            <p>
              MedAssist AI uses browser local storage (not traditional cookies) to persist settings and data
              on your device. We use local storage for the following purposes:
            </p>
            <ul class="mt-3 space-y-2 list-disc list-inside">
              <li>Authentication session tokens (to keep you logged in).</li>
              <li>Encrypted health profile and consultation history.</li>
              <li>User interface preferences, including theme (dark/light mode) and language settings.</li>
              <li>Encrypted API keys for AI provider access (if you choose to store them).</li>
            </ul>
            <p class="mt-3">
              We do not use third-party tracking cookies, advertising cookies, or cross-site tracking technologies.
              We do not integrate with Facebook Pixel, Google Analytics, or similar advertising platforms.
            </p>
            <p class="mt-3">
              You can clear your local storage at any time via your browser settings or via the "Clear All Data"
              option in your MedAssist AI account settings. Doing so will permanently remove your locally stored
              health data and session, logging you out of the Service.
            </p>
          </div>
        </section>

        <!-- 10. Changes to Policy -->
        <section :class="sectionClass">
          <h2 :class="headingClass">10. Changes to This Privacy Policy</h2>
          <div :class="bodyClass">
            <p>
              We may update this Privacy Policy from time to time to reflect changes in our practices, technology,
              legal requirements, or other factors. When we make material changes, we will notify you by:
            </p>
            <ul class="mt-3 space-y-1 list-disc list-inside">
              <li>Sending an email notification to the address associated with your account.</li>
              <li>Displaying a prominent notice within the Service.</li>
              <li>Updating the "Last updated" date at the top of this page.</li>
            </ul>
            <p class="mt-3">
              We encourage you to review this Privacy Policy periodically to stay informed about how we protect
              your information. Your continued use of the Service after the effective date of any changes constitutes
              your acceptance of the revised Privacy Policy.
            </p>
          </div>
        </section>

        <!-- 11. Contact -->
        <section :class="sectionClass">
          <h2 :class="headingClass">11. Contact Information</h2>
          <div :class="bodyClass">
            <p>
              If you have any questions, concerns, or requests regarding this Privacy Policy or how we handle
              your personal information, please contact our Privacy Team:
            </p>
            <div class="mt-4 p-4 rounded-lg" :class="isDark ? 'bg-slate-800/60' : 'bg-slate-100'">
              <p class="font-semibold text-sm">MedAssist AI, Inc.</p>
              <p class="text-sm mt-1">Privacy Team</p>
              <p class="text-sm mt-1">
                Email: <a href="mailto:privacy@medassist.ai" :class="linkClass">privacy@medassist.ai</a>
              </p>
            </div>
            <p class="mt-3">
              We will respond to all privacy-related requests within 30 days. For urgent concerns related to
              a potential data breach or unauthorized access to your account, please email
              <a href="mailto:security@medassist.ai" :class="linkClass">security@medassist.ai</a>.
            </p>
          </div>
        </section>

        <!-- 12. HIPAA Notice -->
        <section class="rounded-xl border p-6 sm:p-8"
          :class="isDark ? 'bg-amber-950/20 border-amber-500/30' : 'bg-amber-50 border-amber-200'">
          <h2 class="text-base font-bold mb-4" :class="isDark ? 'text-amber-300' : 'text-amber-800'">
            12. HIPAA Notice
          </h2>
          <div class="text-sm leading-relaxed" :class="isDark ? 'text-amber-200/80' : 'text-amber-900'">
            <p>
              While MedAssist AI is designed with HIPAA-aware principles — including data minimization, local
              encryption, access controls, and audit-ready architecture — <strong>MedAssist AI, Inc. is not a
              "covered entity" or "business associate" as defined under the Health Insurance Portability and
              Accountability Act (HIPAA)</strong>.
            </p>
            <p class="mt-3">
              The Service is a consumer-facing health information application, not a healthcare provider, health
              plan, or healthcare clearinghouse. Accordingly, HIPAA's privacy and security regulations do not
              apply to us as they would to a licensed medical provider or health insurer.
            </p>
            <p class="mt-3">
              If you require a formally HIPAA-compliant medical records system or telehealth platform, please
              use a service operated by a licensed healthcare provider. MedAssist AI is not a substitute for
              such services.
            </p>
          </div>
        </section>

      </div>

      <!-- Footer nav -->
      <div class="mt-12 pt-6 border-t flex flex-wrap gap-4 text-sm"
        :class="isDark ? 'border-slate-800 text-slate-500' : 'border-slate-200 text-slate-400'">
        <router-link to="/terms" :class="linkClass">Terms of Service</router-link>
        <router-link to="/" :class="linkClass">Back to Home</router-link>
      </div>

    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppNav from '@/components/AppNav.vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const sectionClass = computed(() => [
  'rounded-xl border p-6 sm:p-8',
  isDark.value ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm',
])

const headingClass = computed(() => [
  'text-base font-bold mb-4',
  isDark.value ? 'text-white' : 'text-slate-900',
])

const bodyClass = computed(() => [
  'text-sm leading-relaxed',
  isDark.value ? 'text-slate-400' : 'text-slate-600',
])

const linkClass = computed(() => [
  'underline underline-offset-2 transition-colors',
  isDark.value ? 'text-indigo-400 hover:text-indigo-300' : 'text-indigo-600 hover:text-indigo-800',
])
</script>
