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
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">Terms of Service</h1>
        <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Last updated: April 2026 &nbsp;&middot;&nbsp; Effective: April 1, 2026
        </p>
        <p class="mt-4 text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
          These Terms of Service govern your access to and use of MedAssist AI, operated by MedAssist AI, Inc.
          Please read them carefully before using the service.
        </p>
      </div>

      <!-- Sections -->
      <div class="space-y-6">

        <!-- 1. Acceptance of Terms -->
        <section :class="sectionClass">
          <h2 :class="headingClass">1. Acceptance of Terms</h2>
          <div :class="bodyClass">
            <p>
              By accessing or using MedAssist AI (the "Service"), you agree to be bound by these Terms of Service
              ("Terms"), our Privacy Policy, and all applicable laws and regulations. If you do not agree to any part
              of these Terms, you may not access or use the Service.
            </p>
            <p class="mt-3">
              These Terms constitute a legally binding agreement between you and MedAssist AI, Inc. ("Company," "we,"
              "us," or "our"). Your continued use of the Service after any modification to these Terms constitutes
              your acceptance of those modifications.
            </p>
            <p class="mt-3">
              If you are using the Service on behalf of an organization, you represent and warrant that you have the
              authority to bind that organization to these Terms.
            </p>
          </div>
        </section>

        <!-- 2. Description of Service -->
        <section :class="sectionClass">
          <h2 :class="headingClass">2. Description of Service</h2>
          <div :class="bodyClass">
            <p>
              MedAssist AI is an AI-powered health information platform that uses multiple specialized AI agents to
              analyze reported symptoms and provide informational health content. The Service is designed solely for
              educational and informational purposes.
            </p>
            <p class="mt-3">
              The Service includes features such as symptom analysis, differential information, medication interaction
              references, nutritional guidance, mental health screening instruments, and symptom journaling. These
              features are powered by large language model AI technology, including models provided by third-party AI
              providers.
            </p>
            <p class="mt-3">
              The Service is provided on a subscription basis with a limited free tier, as described in Section 8
              (Subscription &amp; Payments).
            </p>
          </div>
        </section>

        <!-- 3. Medical Disclaimer — CRITICAL -->
        <section class="rounded-xl border-2 p-6 sm:p-8"
          :class="isDark ? 'bg-red-950/20 border-red-500/40' : 'bg-red-50 border-red-300'">
          <div class="flex items-start gap-3 mb-4">
            <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
              :class="isDark ? 'bg-red-500/20' : 'bg-red-100'">
              <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 class="text-lg font-bold text-red-600 dark:text-red-400">3. Medical Disclaimer</h2>
          </div>
          <div class="space-y-3 text-sm leading-relaxed" :class="isDark ? 'text-red-200' : 'text-red-900'">
            <p class="font-semibold">
              PLEASE READ THIS SECTION CAREFULLY. IT CONTAINS CRITICAL LIMITATIONS ON THE USE OF THIS SERVICE.
            </p>
            <ul class="space-y-2 list-none">
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>Not a Medical Device:</strong> MedAssist AI is NOT a medical device as defined by the
                  U.S. Food and Drug Administration (FDA) or any equivalent regulatory body. It has not been reviewed,
                  cleared, or approved by the FDA or any other regulatory authority.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>Not a Medical Diagnosis:</strong> The AI-generated content produced by this Service does
                  NOT constitute a medical diagnosis, clinical opinion, or professional medical advice of any kind.
                  The term "diagnosis" used within the platform interface refers exclusively to the AI's information
                  output and NOT to any clinical diagnostic determination.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>Informational and Educational Use Only:</strong> All content generated by MedAssist AI,
                  including but not limited to symptom analyses, condition descriptions, medication references, and
                  treatment information, is provided for informational and educational purposes ONLY.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>Consult a Healthcare Professional:</strong> You MUST ALWAYS consult a qualified,
                  licensed healthcare professional before making any medical decision, including decisions about
                  diagnosis, treatment, medication, or changes to your health regimen. Do not rely solely on this
                  Service for any health-related decision.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>Emergency Situations:</strong> IF YOU ARE EXPERIENCING A MEDICAL EMERGENCY, CALL 911
                  OR YOUR LOCAL EMERGENCY SERVICES IMMEDIATELY. DO NOT USE THIS SERVICE IN PLACE OF EMERGENCY MEDICAL
                  CARE. MedAssist AI is not equipped to handle medical emergencies.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>No Doctor-Patient Relationship:</strong> Your use of the Service does not create a
                  doctor-patient relationship, therapist-patient relationship, or any other professional healthcare
                  relationship between you and MedAssist AI, Inc. or any of its employees, contractors, or AI
                  systems.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>No Self-Diagnosis or Self-Treatment:</strong> AI suggestions provided by this Service
                  should NEVER be used to self-diagnose a medical condition, self-prescribe medications, self-treat
                  an illness or injury, or delay, avoid, or substitute for seeking qualified professional medical
                  care.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="font-bold flex-shrink-0">&#9679;</span>
                <span><strong>AI Limitations:</strong> AI-generated health content may be inaccurate, incomplete,
                  outdated, or inappropriate for your specific health circumstances. The AI does not know your full
                  medical history and cannot physically examine you.</span>
              </li>
            </ul>
          </div>
        </section>

        <!-- 4. User Accounts -->
        <section :class="sectionClass">
          <h2 :class="headingClass">4. User Accounts</h2>
          <div :class="bodyClass">
            <p>
              To access certain features of the Service, you must create an account by providing accurate, complete,
              and current information, including your name and email address. You agree to update your account
              information promptly if it changes.
            </p>
            <p class="mt-3">
              You are solely responsible for maintaining the confidentiality of your account credentials and for all
              activity that occurs under your account. You agree to immediately notify us at
              <a href="mailto:support@medassist.ai" :class="linkClass">support@medassist.ai</a> of any unauthorized
              access or use of your account.
            </p>
            <p class="mt-3">
              You may not share your account with or transfer your account to another person. You may not create
              accounts using automated means or under false pretenses. We reserve the right to suspend or terminate
              accounts that violate these Terms.
            </p>
          </div>
        </section>

        <!-- 5. Health Information & Privacy -->
        <section :class="sectionClass">
          <h2 :class="headingClass">5. Health Information &amp; Privacy</h2>
          <div :class="bodyClass">
            <p>
              We take the privacy of your health information seriously. Health profile data you enter — including age,
              gender, medical history, and symptoms — is encrypted using AES-256 encryption and stored locally on
              your device. We maintain minimal server-side data, limited to your email address, hashed password, and
              subscription status.
            </p>
            <p class="mt-3">
              The Service is designed with HIPAA-aware principles, including data minimization, access controls, and
              audit-ready logging. However, MedAssist AI, Inc. is not a "covered entity" as defined under the Health
              Insurance Portability and Accountability Act (HIPAA), and the Service is not a HIPAA-compliant medical
              records system.
            </p>
            <p class="mt-3">
              Your use of the Service is also governed by our
              <router-link to="/privacy" :class="linkClass">Privacy Policy</router-link>, which is incorporated into
              these Terms by reference. By using the Service, you consent to the data practices described in the
              Privacy Policy.
            </p>
          </div>
        </section>

        <!-- 6. AI Technology Disclosure -->
        <section :class="sectionClass">
          <h2 :class="headingClass">6. AI Technology Disclosure</h2>
          <div :class="bodyClass">
            <p>
              MedAssist AI uses third-party large language model (LLM) providers to power its AI agents. These
              providers may include Anthropic (Claude), OpenAI (GPT), and Google (Gemini). By using the Service, you
              acknowledge and consent to your queries being transmitted to one or more of these third-party AI
              providers for processing.
            </p>
            <p class="mt-3">
              AI-generated responses may contain errors, hallucinations, omissions, or outdated information. The AI
              has no awareness of your complete medical history, cannot physically examine you, and cannot account
              for all individual variables that a licensed clinician would consider. AI technology has inherent
              limitations that make it unsuitable as a replacement for professional medical judgment.
            </p>
            <p class="mt-3">
              We continuously work to improve the accuracy and safety of AI outputs, but we make no representation
              or warranty regarding the accuracy, completeness, or fitness for any particular purpose of
              AI-generated content.
            </p>
          </div>
        </section>

        <!-- 7. Acceptable Use -->
        <section :class="sectionClass">
          <h2 :class="headingClass">7. Acceptable Use</h2>
          <div :class="bodyClass">
            <p>You agree to use the Service only for lawful purposes and in accordance with these Terms. You agree NOT to use the Service:</p>
            <ul class="mt-3 space-y-2 list-none">
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>In emergency medical situations where immediate professional care is required.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>To prescribe, recommend, or obtain prescription medications.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>For users under the age of 18 without verified parental or guardian consent. The Service is not
                  intended for minors, and we do not knowingly collect health information from users under 18 without
                  appropriate parental consent.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>To upload or transmit content that is unlawful, harmful, defamatory, or infringes on the
                  intellectual property rights of others.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>To reverse-engineer, decompile, or attempt to extract source code from the Service.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>To use automated tools, bots, or scripts to access or scrape the Service.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 mt-0.5 text-red-500 font-bold">&#10005;</span>
                <span>To interfere with or disrupt the integrity or performance of the Service or its infrastructure.</span>
              </li>
            </ul>
          </div>
        </section>

        <!-- 8. Subscription & Payments -->
        <section :class="sectionClass">
          <h2 :class="headingClass">8. Subscription &amp; Payments</h2>
          <div :class="bodyClass">
            <p>
              The Service offers a limited free tier and paid subscription tiers. Paid subscriptions are billed on a
              recurring monthly or annual basis and are processed through Stripe, our third-party payment processor.
              By subscribing to a paid plan, you authorize MedAssist AI, Inc. to charge your designated payment
              method on a recurring basis at the applicable subscription rate.
            </p>
            <p class="mt-3">
              <strong>Cancellation:</strong> You may cancel your subscription at any time through your account
              settings or by contacting us at
              <a href="mailto:billing@medassist.ai" :class="linkClass">billing@medassist.ai</a>. Cancellation will
              take effect at the end of the current billing period. You will retain access to paid features until the
              end of the billing period for which you have already paid.
            </p>
            <p class="mt-3">
              <strong>Refund Policy:</strong> We offer a 7-day money-back guarantee on new paid subscriptions. If
              you are not satisfied with the Service, you may request a full refund within 7 days of your initial
              subscription charge by contacting
              <a href="mailto:billing@medassist.ai" :class="linkClass">billing@medassist.ai</a>. Refunds are not
              available after the 7-day window or for subsequent billing cycles.
            </p>
            <p class="mt-3">
              We reserve the right to change subscription pricing with at least 30 days' written notice. Continued
              use of the Service after a price change constitutes your acceptance of the new pricing.
            </p>
          </div>
        </section>

        <!-- 9. Limitation of Liability -->
        <section :class="sectionClass">
          <h2 :class="headingClass">9. Limitation of Liability</h2>
          <div :class="bodyClass">
            <p>
              THE SERVICE IS PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS WITHOUT WARRANTIES OF ANY KIND, EITHER
              EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
              PARTICULAR PURPOSE, ACCURACY, RELIABILITY, OR NON-INFRINGEMENT.
            </p>
            <p class="mt-3">
              TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, MEDASSIST AI, INC. AND ITS DIRECTORS, EMPLOYEES,
              AGENTS, PARTNERS, AND LICENSORS SHALL NOT BE LIABLE FOR:
            </p>
            <ul class="mt-3 space-y-2 list-disc list-inside">
              <li>Any health outcomes, injuries, or damages arising from reliance on AI-generated content.</li>
              <li>Any indirect, incidental, special, consequential, or punitive damages.</li>
              <li>Any loss of data, revenue, profits, or business opportunities.</li>
              <li>Any interruption, suspension, or termination of the Service.</li>
              <li>Any errors, inaccuracies, or omissions in AI-generated content.</li>
            </ul>
            <p class="mt-3">
              IN NO EVENT SHALL OUR TOTAL LIABILITY TO YOU FOR ALL CLAIMS ARISING OUT OF OR RELATED TO THESE TERMS
              OR THE SERVICE EXCEED THE TOTAL AMOUNT OF SUBSCRIPTION FEES YOU HAVE PAID TO US IN THE TWELVE (12)
              MONTHS PRECEDING THE CLAIM, OR ONE HUNDRED DOLLARS ($100), WHICHEVER IS GREATER.
            </p>
            <p class="mt-3">
              Some jurisdictions do not allow the exclusion of implied warranties or limitation of liability for
              incidental or consequential damages, so the above limitations may not apply to you in full.
            </p>
          </div>
        </section>

        <!-- 10. Indemnification -->
        <section :class="sectionClass">
          <h2 :class="headingClass">10. Indemnification</h2>
          <div :class="bodyClass">
            <p>
              You agree to indemnify, defend, and hold harmless MedAssist AI, Inc. and its officers, directors,
              employees, agents, and licensors from and against any claims, liabilities, damages, losses, costs, and
              expenses (including reasonable attorneys' fees) arising out of or related to:
            </p>
            <ul class="mt-3 space-y-1 list-disc list-inside">
              <li>Your use of or reliance on the Service or AI-generated content.</li>
              <li>Your violation of these Terms.</li>
              <li>Your violation of any applicable law or third-party rights.</li>
              <li>Any content you submit, post, or transmit through the Service.</li>
            </ul>
          </div>
        </section>

        <!-- 11. Intellectual Property -->
        <section :class="sectionClass">
          <h2 :class="headingClass">11. Intellectual Property</h2>
          <div :class="bodyClass">
            <p>
              All content, features, functionality, branding, logos, user interface design, and technology comprising
              the Service — including the multi-agent AI pipeline architecture — are owned by MedAssist AI, Inc. or
              its licensors and are protected by applicable intellectual property laws, including copyright, trademark,
              and trade secret laws.
            </p>
            <p class="mt-3">
              You are granted a limited, non-exclusive, non-transferable, revocable license to access and use the
              Service for your personal, non-commercial purposes in accordance with these Terms. You may not copy,
              modify, distribute, sell, or create derivative works from any portion of the Service without our express
              written consent.
            </p>
          </div>
        </section>

        <!-- 12. Termination -->
        <section :class="sectionClass">
          <h2 :class="headingClass">12. Termination</h2>
          <div :class="bodyClass">
            <p>
              We reserve the right to suspend or permanently terminate your access to the Service at our sole
              discretion, with or without notice, for conduct that we determine violates these Terms, is harmful
              to other users or third parties, or is contrary to applicable law.
            </p>
            <p class="mt-3">
              You may terminate your account at any time by contacting us at
              <a href="mailto:support@medassist.ai" :class="linkClass">support@medassist.ai</a> or through your
              account settings. Upon termination, your right to access the Service will immediately cease.
            </p>
            <p class="mt-3">
              Provisions of these Terms that by their nature should survive termination — including but not limited to
              the Medical Disclaimer, Limitation of Liability, Indemnification, and Intellectual Property sections —
              shall survive termination.
            </p>
          </div>
        </section>

        <!-- 13. Changes to Terms -->
        <section :class="sectionClass">
          <h2 :class="headingClass">13. Changes to Terms</h2>
          <div :class="bodyClass">
            <p>
              We may update or modify these Terms at any time. When we make material changes, we will provide notice
              via email to the address associated with your account and/or by posting a prominent notice within the
              Service at least 14 days before the changes take effect.
            </p>
            <p class="mt-3">
              Your continued use of the Service after the effective date of any changes constitutes your acceptance
              of the revised Terms. If you do not agree to the revised Terms, you must discontinue your use of the
              Service before the effective date.
            </p>
          </div>
        </section>

        <!-- 14. Governing Law -->
        <section :class="sectionClass">
          <h2 :class="headingClass">14. Governing Law &amp; Dispute Resolution</h2>
          <div :class="bodyClass">
            <p>
              These Terms shall be governed by and construed in accordance with the laws of the State of Delaware,
              without regard to its conflict of law principles. You agree to submit to the exclusive personal
              jurisdiction of the courts located in Delaware for resolution of any disputes arising under these Terms.
            </p>
            <p class="mt-3">
              Any dispute, claim, or controversy arising out of or relating to these Terms or your use of the Service
              that cannot be resolved informally shall be resolved through binding arbitration under the rules of the
              American Arbitration Association (AAA), conducted in English, in the State of Delaware. The arbitrator's
              decision shall be final and binding and may be entered as a judgment in any court of competent
              jurisdiction. You waive any right to bring claims as a plaintiff or class member in any class action
              proceeding.
            </p>
          </div>
        </section>

        <!-- 15. Contact -->
        <section :class="sectionClass">
          <h2 :class="headingClass">15. Contact Information</h2>
          <div :class="bodyClass">
            <p>
              If you have any questions, concerns, or requests regarding these Terms of Service, please contact us:
            </p>
            <div class="mt-4 p-4 rounded-lg" :class="isDark ? 'bg-slate-800/60' : 'bg-slate-100'">
              <p class="font-semibold text-sm">MedAssist AI, Inc.</p>
              <p class="text-sm mt-1">Legal Department</p>
              <p class="text-sm mt-1">
                Email: <a href="mailto:legal@medassist.ai" :class="linkClass">legal@medassist.ai</a>
              </p>
            </div>
          </div>
        </section>

      </div>

      <!-- Footer nav -->
      <div class="mt-12 pt-6 border-t flex flex-wrap gap-4 text-sm"
        :class="isDark ? 'border-slate-800 text-slate-500' : 'border-slate-200 text-slate-400'">
        <router-link to="/privacy" :class="linkClass">Privacy Policy</router-link>
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
