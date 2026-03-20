"""
Diagnostician Agent – Core differential diagnosis engine.

Responsibilities:
  * Perform structured differential diagnosis using VINDICATE framework
  * Apply Bayesian reasoning with likelihood ratios
  * Match illness scripts with full clinical detail
  * Check for anchoring bias and cognitive errors
  * Rank conditions by clinical likelihood with transparent reasoning
  * Always include must-not-miss diagnoses
  * Generate high-yield follow-up questions
"""

from __future__ import annotations

import json
import math
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


class DiagnosticianAgent(BaseAgent):
    name = "diagnostician"
    description = "Differential diagnosis and clinical reasoning specialist"
    model = "claude-sonnet-4-6"
    max_tokens = 4096
    temperature = 0.2

    def _build_system_prompt(self) -> str:
        return """You are an expert diagnostician AI agent on a multi-agent medical team, equivalent to a board-certified internal medicine physician with fellowship training in diagnostic medicine and 25+ years of clinical experience. You think like a master clinician.

YOUR ROLE:
You receive triaged cases and perform comprehensive differential diagnosis. You are the analytical core of the team — accuracy is paramount.

═══════════════════════════════════════════════════════
CLINICAL REASONING METHODOLOGY
═══════════════════════════════════════════════════════

You MUST follow this structured approach for EVERY case:

────────────────────────────────────────────────────
STEP 1: PROBLEM REPRESENTATION
────────────────────────────────────────────────────
Distill the case into ONE sentence using semantic qualifiers:
  "[Age] [gender] with [acute/subacute/chronic] [qualifying descriptors] presenting with [key findings]"

Example: "65-year-old male with acute-onset substernal crushing chest pain radiating to left arm with diaphoresis and dyspnea"

Good semantic qualifiers: acute/chronic, unilateral/bilateral, constant/intermittent, sharp/dull, migratory/fixed, exertional/rest, proximal/distal, inflammatory/mechanical

────────────────────────────────────────────────────
STEP 2: DIFFERENTIAL GENERATION — VINDICATE FRAMEWORK
────────────────────────────────────────────────────
For the affected body system(s), systematically consider ALL disease categories:

  V = Vascular (thrombosis, embolism, hemorrhage, infarction, vasculitis, aneurysm)
  I = Infectious (bacterial, viral, fungal, parasitic, TB, STI, opportunistic)
  N = Neoplastic (primary, metastatic, paraneoplastic, benign tumors)
  D = Degenerative / Deficiency (osteoarthritis, vitamin deficiency, wear-and-tear, nutritional)
  I = Iatrogenic / Intoxication (drug side effects, drug interactions, poisoning, radiation, post-procedural)
  C = Congenital (genetic, developmental, inherited metabolic)
  A = Autoimmune / Allergic (SLE, RA, vasculitis, anaphylaxis, hypersensitivity, sarcoid)
  T = Traumatic (blunt, penetrating, overuse, repetitive strain, post-surgical)
  E = Endocrine / Metabolic (thyroid, adrenal, glucose, electrolyte, acid-base, inborn errors)

Use the apply_vindicate_framework tool to ensure systematic coverage.

IMPORTANT: Do NOT skip categories. Even if a category seems unlikely, briefly state why it was excluded. This prevents premature closure.

────────────────────────────────────────────────────
STEP 3: ILLNESS SCRIPT MATCHING
────────────────────────────────────────────────────
For each candidate diagnosis in your differential, evaluate using illness scripts:

  1. EPIDEMIOLOGY: Who gets this? (age, gender, race, geography, occupation, exposures)
  2. PATHOPHYSIOLOGY: How does this disease cause THESE specific symptoms?
  3. TIME COURSE: Does the timeline fit? (hyperacute/acute/subacute/chronic, progressive/relapsing)
  4. KEY FEATURES: Are the discriminating features present?
     - Pathognomonic findings (virtually diagnostic)
     - Highly specific findings (strongly supportive)
     - Sensitive findings (expected to be present; absence argues against)
  5. EXPECTED FINDINGS: What SHOULD be present if this diagnosis is correct?
     - Are there expected findings that are ABSENT? (argues against)
     - Are there findings present that are UNEXPECTED? (argues against)
  6. RED HERRINGS: What findings do NOT fit this diagnosis?

Use the clinical_pattern_match tool for structured illness script data.

────────────────────────────────────────────────────
STEP 4: BAYESIAN REASONING
────────────────────────────────────────────────────
For your top differential diagnoses, apply formal Bayesian updating:

  1. Estimate PRE-TEST PROBABILITY based on:
     - Disease prevalence (age + gender + geography adjusted)
     - Clinical setting (primary care vs ED vs ICU)
     - Risk factors present

  2. For each clinical feature, apply LIKELIHOOD RATIOS:
     - LR+ = sensitivity / (1 - specificity)
     - LR- = (1 - sensitivity) / specificity
     - LR > 10: Strong evidence FOR
     - LR 5-10: Moderate evidence FOR
     - LR 2-5: Weak evidence FOR
     - LR 0.5-2: No meaningful change
     - LR 0.2-0.5: Weak evidence AGAINST
     - LR 0.1-0.2: Moderate evidence AGAINST
     - LR < 0.1: Strong evidence AGAINST

  3. Calculate POST-TEST PROBABILITY:
     post_odds = pre_test_odds × LR1 × LR2 × LR3 ...
     post_test_probability = post_odds / (1 + post_odds)

Use the calculate_diagnostic_probability tool for formal calculations.

────────────────────────────────────────────────────
STEP 5: ANCHORING BIAS CHECK
────────────────────────────────────────────────────
BEFORE finalizing your differential, EXPLICITLY ask:
  1. What am I anchoring on? What was my first impression?
  2. What symptoms does my top diagnosis NOT explain?
  3. What alternative diagnoses would explain those unexplained symptoms?
  4. Am I being influenced by availability bias (recent similar case)?
  5. Is there a unifying diagnosis that explains MORE of the findings?
  6. Have I considered an atypical presentation of a common disease?

Use the check_anchoring_bias tool to systematically challenge your leading diagnosis.

────────────────────────────────────────────────────
STEP 6: MUST-NOT-MISS DIAGNOSES
────────────────────────────────────────────────────
ALWAYS include diagnoses that are:
  - Life-threatening if missed (even if low probability)
  - Time-sensitive (outcomes worsen with delay)
  - Treatable (missing them leads to preventable harm)

Common must-not-miss by presentation:
  Chest pain: ACS, PE, aortic dissection, tension pneumothorax, esophageal rupture, cardiac tamponade
  Headache: SAH, meningitis, temporal arteritis, brain tumor, cavernous sinus thrombosis
  Abdominal pain: Appendicitis, ectopic pregnancy, AAA, mesenteric ischemia, bowel obstruction, perforation
  SOB: PE, pneumothorax, acute CHF, anaphylaxis, foreign body
  Fever: Meningitis, necrotizing fasciitis, endocarditis, epidural abscess
  Back pain: Cauda equina, epidural abscess, AAA, aortic dissection
  Weakness: Stroke, GBS, myasthenia crisis, cord compression, hypokalemia
  Syncope: Cardiac arrhythmia, PE, AAA, ectopic pregnancy, SAH

────────────────────────────────────────────────────
DIAGNOSTIC CONFIDENCE SCORING
────────────────────────────────────────────────────
  90-100%: Pathognomonic features present, classic textbook presentation
  70-89%: Strong clinical match, most illness script features present, high LR+ features
  50-69%: Moderate match, some key features present, needs confirmatory testing
  30-49%: Possible but atypical, or common condition with few specific features
  10-29%: Low probability but included for clinical importance (must-not-miss)
  <10%: Remote possibility, included only if catastrophic if missed

COMMUNICATION:
You work on a team with: triage, specialist, treatment agents.
- Review triage findings (ESI level, red flags, ROS) before starting
- Request specialist consultation for complex or ambiguous cases
- Share your differential with treatment agent for planning
- Generate questions that most efficiently narrow the differential (highest information gain)

Always produce structured JSON in your final answer:
- problem_representation (one-sentence case summary with semantic qualifiers)
- differential_diagnosis (list of conditions with: condition, confidence_pct, bayesian_reasoning, illness_script_fit, supporting_features, opposing_features, must_not_miss flag, urgency, recommended_specialty)
- vindicate_analysis (summary of which disease categories were considered/excluded)
- must_not_miss (dangerous diagnoses to rule out, with brief reasoning and recommended tests)
- anchoring_bias_check (what was considered, what doesn't fit, alternatives)
- discriminating_features (what tests/findings would most change the differential, with expected LR+/LR-)
- recommended_tests (ordered by diagnostic yield, with what each test confirms/excludes)
- follow_up_questions (3-5 questions that would most change the differential, with which diagnosis each targets)
- clinical_reasoning_summary (paragraph explaining the diagnostic thought process)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "clinical_pattern_match",
            "description": (
                "Match patient symptoms against comprehensive clinical illness scripts. "
                "Returns full illness scripts with: classic presentation, key discriminating features, "
                "expected timeline, associated symptoms, risk factors, and red herring symptoms. "
                "Covers domains: Respiratory, GI, Neurological, Cardiovascular, MSK, Dermatological, "
                "Psychiatric, Infectious, Endocrine, Hematologic, Renal/Urologic, Allergic/Immunologic."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "symptoms": {"type": "string", "description": "Patient symptoms"},
                    "age": {"type": "integer", "description": "Patient age"},
                    "gender": {"type": "string", "description": "Patient gender"},
                    "duration": {"type": "string", "description": "Symptom duration"},
                    "severity": {"type": "integer", "description": "1-10 scale"},
                    "affected_systems": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Body systems involved (from ROS)",
                    },
                },
                "required": ["symptoms"],
            },
        })
        tools.append({
            "name": "calculate_diagnostic_probability",
            "description": (
                "Apply formal Bayesian reasoning to calculate post-test probability of a condition. "
                "Uses pre-test probability (prevalence-based, age/gender/geography adjusted), "
                "positive and negative likelihood ratios for each clinical feature, and sequential "
                "LR application. Returns full calculation chain: pre-test% → each LR applied → post-test%."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string", "description": "The condition to evaluate"},
                    "pre_test_probability_pct": {
                        "type": "number",
                        "description": "Estimated pre-test probability as percentage (0-100), based on prevalence adjusted for age/gender/geography",
                    },
                    "features_with_lr": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "feature": {"type": "string", "description": "Clinical feature or test finding"},
                                "present": {"type": "boolean", "description": "Whether the feature is present"},
                                "lr_positive": {"type": "number", "description": "Positive likelihood ratio (LR+) when feature is present"},
                                "lr_negative": {"type": "number", "description": "Negative likelihood ratio (LR-) when feature is absent"},
                                "sensitivity": {"type": "number", "description": "Estimated sensitivity (0-1)"},
                                "specificity": {"type": "number", "description": "Estimated specificity (0-1)"},
                                "source": {"type": "string", "description": "Source or reasoning for LR estimate"},
                            },
                            "required": ["feature", "present"],
                        },
                        "description": "Clinical features with their likelihood ratios",
                    },
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                },
                "required": ["condition", "pre_test_probability_pct", "features_with_lr"],
            },
        })
        tools.append({
            "name": "apply_vindicate_framework",
            "description": (
                "Systematically generate differential diagnoses using the VINDICATE mnemonic: "
                "Vascular, Infectious, Neoplastic, Degenerative/Deficiency, Iatrogenic/Intoxication, "
                "Congenital, Autoimmune/Allergic, Traumatic, Endocrine/Metabolic. "
                "For each category, returns plausible conditions with brief reasoning. "
                "Ensures no category of disease is overlooked."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "symptoms": {"type": "string", "description": "Patient symptoms"},
                    "age": {"type": "integer", "description": "Patient age"},
                    "gender": {"type": "string", "description": "Patient gender"},
                    "affected_system": {
                        "type": "string",
                        "description": "Primary affected body system (e.g., cardiovascular, neurological, respiratory)",
                    },
                    "duration": {"type": "string", "description": "Symptom duration"},
                },
                "required": ["symptoms", "affected_system"],
            },
        })
        tools.append({
            "name": "check_anchoring_bias",
            "description": (
                "Cognitive debiasing tool. Given the current leading diagnosis and all symptoms, "
                "identifies unexplained symptoms and suggests alternative diagnoses that better "
                "account for the full clinical picture. Forces consideration of what doesn't fit."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "current_top_diagnosis": {
                        "type": "string",
                        "description": "The current leading diagnosis being considered",
                    },
                    "all_symptoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Complete list of all patient symptoms and findings",
                    },
                    "explained_symptoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Symptoms that ARE explained by the top diagnosis",
                    },
                    "unexplained_symptoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Symptoms that are NOT explained by the top diagnosis",
                    },
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                },
                "required": ["current_top_diagnosis", "all_symptoms", "unexplained_symptoms"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "clinical_pattern_match":
            return await self._clinical_pattern_match(tool_input)
        if tool_name == "calculate_diagnostic_probability":
            return await self._calculate_probability(tool_input)
        if tool_name == "apply_vindicate_framework":
            return await self._apply_vindicate(tool_input)
        if tool_name == "check_anchoring_bias":
            return await self._check_anchoring_bias(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ──────────────────────────────────────────────────────────────
    # Tool: clinical_pattern_match
    # ──────────────────────────────────────────────────────────────

    async def _clinical_pattern_match(self, tool_input: dict) -> str:
        """Provide comprehensive illness scripts for the LLM to reason over."""
        symptoms = tool_input.get("symptoms", "").lower()
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown").lower()
        duration = tool_input.get("duration", "unknown")
        severity = tool_input.get("severity", 5)

        patterns = []

        # ── RESPIRATORY ─────────────────────────────────────────
        if any(w in symptoms for w in ["cough", "fever", "sore throat", "congestion", "runny nose",
                                        "shortness of breath", "wheezing", "chest cold"]):
            patterns.append({
                "domain": "respiratory",
                "illness_scripts": [
                    {
                        "condition": "Upper Respiratory Infection (URI/Common Cold)",
                        "classic_presentation": "Gradual onset rhinorrhea, nasal congestion, sore throat, mild cough. Low-grade or no fever. Mild malaise.",
                        "key_discriminating_features": ["Rhinorrhea predominant", "Self-limited (7-10 days)", "No significant dyspnea", "Multiple URI symptoms together"],
                        "expected_timeline": "Onset over 1-2 days, peak at 2-3 days, resolution in 7-10 days. Cough may linger 2-3 weeks.",
                        "associated_symptoms": ["Sneezing", "Mild headache", "Watery eyes", "Mild body aches"],
                        "risk_factors": ["Exposure to sick contacts", "Season (fall/winter)", "Daycare/school-age children"],
                        "red_herrings": ["High fever >102F suggests NOT simple URI", "Dyspnea suggests lower respiratory process", "Focal findings suggest pneumonia"],
                    },
                    {
                        "condition": "Influenza",
                        "classic_presentation": "Abrupt onset high fever (102-104F), severe myalgias, headache, dry cough, profound fatigue. Respiratory symptoms may be initially mild.",
                        "key_discriminating_features": ["ABRUPT onset (can often name the hour)", "Severe myalgias (legs and back)", "High fever", "Profound fatigue out of proportion to other symptoms"],
                        "expected_timeline": "Abrupt onset, fever 3-5 days, fatigue/cough may persist 2+ weeks. Biphasic fever possible.",
                        "associated_symptoms": ["Sore throat", "Rhinorrhea", "Eye pain/photophobia", "GI symptoms more common in children"],
                        "risk_factors": ["Flu season (Oct-Mar)", "Unvaccinated", "Exposure", "Age >65 or <5", "Immunocompromised", "Pregnancy"],
                        "red_herrings": ["Gradual onset argues against", "Prominent rhinorrhea early suggests URI more than flu"],
                    },
                    {
                        "condition": "COVID-19",
                        "classic_presentation": "Variable: fever, cough, fatigue, myalgias, loss of taste/smell, sore throat, dyspnea (if lower respiratory involvement).",
                        "key_discriminating_features": ["Anosmia/ageusia highly specific", "Hypoxia may be 'silent' (happy hypoxia)", "Highly variable presentation", "Longer incubation (2-14 days)"],
                        "expected_timeline": "Incubation 2-14 days (median 5). Mild illness 1-2 weeks. Respiratory deterioration typically day 7-10 if occurring.",
                        "associated_symptoms": ["Diarrhea", "Headache", "Conjunctivitis", "Skin changes", "Dysgeusia"],
                        "risk_factors": ["Exposure to known case", "Unvaccinated", "Crowded settings", "Age >60", "Obesity", "Comorbidities"],
                        "red_herrings": ["Normal SpO2 does not exclude — check with exertion"],
                    },
                    {
                        "condition": "Community-Acquired Pneumonia (CAP)",
                        "classic_presentation": "Productive cough, fever/chills, dyspnea, pleuritic chest pain. Focal crackles on exam. May have dullness to percussion.",
                        "key_discriminating_features": ["Productive cough with purulent sputum", "Focal lung findings (crackles, egophony, bronchial breath sounds)", "Fever with rigors", "Dyspnea/tachypnea"],
                        "expected_timeline": "Develops over 1-3 days. Without treatment, progressive. Atypical pneumonia may have more gradual onset (days to weeks).",
                        "associated_symptoms": ["Rigors", "Tachycardia", "Confusion (elderly)", "Pleuritic chest pain"],
                        "risk_factors": ["Age >65", "COPD/asthma", "Smoking", "Immunocompromised", "Aspiration risk", "Recent viral URI"],
                        "red_herrings": ["Normal WBC does not exclude (especially elderly/immunocompromised)", "Absence of fever does not exclude in elderly"],
                    },
                    {
                        "condition": "Pulmonary Embolism (PE)",
                        "classic_presentation": "Acute dyspnea, pleuritic chest pain, tachycardia. May have cough, hemoptysis, leg swelling. Often post-immobilization or surgery.",
                        "key_discriminating_features": ["Acute onset dyspnea without clear cause", "Pleuritic chest pain", "Tachycardia out of proportion", "Risk factors for VTE", "Hypoxia", "Clear lungs on exam (dyspnea with clear lungs = PE until proven otherwise)"],
                        "expected_timeline": "Acute onset (seconds to minutes). Progressive without treatment.",
                        "associated_symptoms": ["Hemoptysis (late)", "Syncope (massive PE)", "Leg swelling/pain (DVT source)", "Anxiety"],
                        "risk_factors": ["Recent surgery/immobilization", "Malignancy", "OCP/HRT", "Pregnancy/postpartum", "Prior VTE", "Thrombophilia", "Long travel"],
                        "red_herrings": ["Normal D-dimer in low-probability patient excludes PE", "But D-dimer is nonspecific — elevated in many conditions"],
                    },
                    {
                        "condition": "Acute Asthma Exacerbation",
                        "classic_presentation": "Wheezing, dyspnea, cough, chest tightness. Often triggered by allergens, infection, cold air, exercise. History of asthma.",
                        "key_discriminating_features": ["Diffuse bilateral wheezing", "Known asthma history", "Response to bronchodilators", "Trigger identifiable"],
                        "expected_timeline": "Develops over hours. Can be rapid if severe trigger. Resolves with treatment.",
                        "associated_symptoms": ["Chest tightness", "Inability to complete sentences (severe)", "Use of accessory muscles (severe)"],
                        "risk_factors": ["Prior asthma diagnosis", "Allergies/atopy", "Recent URI", "Allergen exposure", "Medication non-compliance"],
                        "red_herrings": ["Absence of wheezing in severe attack ('silent chest') indicates critical obstruction, not improvement"],
                    },
                ],
            })

        # ── GASTROINTESTINAL ────────────────────────────────────
        if any(w in symptoms for w in ["nausea", "vomit", "diarrhea", "stomach", "abdominal",
                                        "belly", "heartburn", "bloating"]):
            patterns.append({
                "domain": "gastrointestinal",
                "illness_scripts": [
                    {
                        "condition": "Acute Gastroenteritis",
                        "classic_presentation": "Acute onset nausea, vomiting, watery diarrhea, cramping abdominal pain. May have low-grade fever. Usually self-limited.",
                        "key_discriminating_features": ["Acute onset", "Nausea/vomiting + diarrhea together", "Cramping/colicky pain", "Sick contacts or food exposure", "Self-limited course"],
                        "expected_timeline": "Viral: 1-3 days. Bacterial: 1-7 days. Onset within hours (toxin-mediated) to days (infectious).",
                        "associated_symptoms": ["Myalgias", "Low-grade fever", "Abdominal cramps", "Dehydration signs"],
                        "risk_factors": ["Food exposure", "Sick contacts", "Travel", "Daycare", "Cruise ship", "Contaminated water"],
                        "red_herrings": ["Bloody diarrhea → consider invasive bacterial (Shigella, Salmonella, E. coli O157:H7, C. diff)", "High fever → consider invasive pathogen", "Duration >7 days → consider non-infectious cause"],
                    },
                    {
                        "condition": "Appendicitis",
                        "classic_presentation": "Periumbilical pain migrating to RLQ over 12-24 hours, anorexia, nausea/vomiting (after pain onset), low-grade fever. McBurney's point tenderness.",
                        "key_discriminating_features": ["Pain migration (periumbilical → RLQ)", "Anorexia (almost always present)", "Nausea/vomiting AFTER pain onset (not before)", "Rebound tenderness", "RLQ tenderness", "Psoas sign, obturator sign, Rovsing sign"],
                        "expected_timeline": "Progressive over 12-48 hours. If untreated, perforation risk increases after 36-72 hours.",
                        "associated_symptoms": ["Anorexia", "Low-grade fever (typically <101F early)", "Guarding"],
                        "risk_factors": ["Age 10-30 (peak)", "Male > female slightly", "Family history"],
                        "red_herrings": ["Vomiting BEFORE pain onset suggests gastroenteritis, not appendicitis", "Diarrhea can occur (retrocecal or pelvic appendix) — does not exclude", "Elderly/immunocompromised: may lack classic signs"],
                    },
                    {
                        "condition": "GERD (Gastroesophageal Reflux Disease)",
                        "classic_presentation": "Burning substernal chest pain/heartburn, worse after meals and when lying down, acid regurgitation, chronic cough.",
                        "key_discriminating_features": ["Postprandial worsening", "Positional (worse supine)", "Relief with antacids", "Retrosternal burning quality", "No exertional component"],
                        "expected_timeline": "Chronic/recurrent. Episodic over weeks to months.",
                        "associated_symptoms": ["Sour taste", "Dysphagia (if stricture)", "Chronic cough", "Hoarseness", "Globus sensation"],
                        "risk_factors": ["Obesity", "Hiatal hernia", "Pregnancy", "Smoking", "Spicy/fatty foods", "Caffeine", "Alcohol", "NSAIDs"],
                        "red_herrings": ["Can mimic cardiac chest pain — ALWAYS rule out ACS first in appropriate patients", "Dysphagia suggests complication or alternative diagnosis"],
                    },
                    {
                        "condition": "Peptic Ulcer Disease",
                        "classic_presentation": "Epigastric burning/gnawing pain, may be related to meals (worse with meals for gastric, better for duodenal), nausea. H. pylori or NSAID use.",
                        "key_discriminating_features": ["Epigastric location", "Meal relationship (gastric: worse with food; duodenal: better with food, worse 2-3h later)", "NSAID or H. pylori association", "Nocturnal pain (duodenal)"],
                        "expected_timeline": "Chronic/recurring over weeks to months. Acute perforation is sudden.",
                        "associated_symptoms": ["Nausea", "Early satiety", "Weight loss (gastric)", "Melena or hematemesis if bleeding"],
                        "risk_factors": ["H. pylori infection", "NSAID use", "Smoking", "Alcohol", "Stress", "Age >60"],
                        "red_herrings": ["Perforation presents with sudden severe pain and rigid abdomen — surgical emergency", "Bleeding ulcer may present with hematemesis or melena without prior pain"],
                    },
                    {
                        "condition": "Cholecystitis / Biliary Colic",
                        "classic_presentation": "RUQ or epigastric pain, often postprandial (fatty meal), nausea/vomiting, Murphy's sign positive. Constant pain lasting >4-6 hours suggests cholecystitis vs colic.",
                        "key_discriminating_features": ["RUQ pain", "Postprandial (especially fatty food)", "Murphy's sign", "Constant (not colicky despite name)", "Fever suggests cholecystitis vs simple colic"],
                        "expected_timeline": "Biliary colic: 30 min to 6 hours, then resolves. Cholecystitis: >6 hours, progressive, with fever.",
                        "associated_symptoms": ["Nausea/vomiting", "Referred pain to right scapula", "Fever/chills (cholecystitis)", "Jaundice (if CBD obstruction)"],
                        "risk_factors": ["Female", "Age >40", "Obesity", "Multiparity", "Rapid weight loss", "Family history", "Native American heritage"],
                        "red_herrings": ["Charcot's triad (fever + jaundice + RUQ pain) = cholangitis — more serious", "Reynolds pentad adds AMS + shock = toxic cholangitis"],
                    },
                    {
                        "condition": "Mesenteric Ischemia",
                        "classic_presentation": "Severe periumbilical pain out of proportion to physical exam findings. Often elderly with atrial fibrillation or vascular disease. 'Pain out of proportion to exam' is classic.",
                        "key_discriminating_features": ["Pain out of proportion to exam (early)", "Elderly with AF/vascular disease", "Postprandial pain (chronic type — 'intestinal angina')", "Bloody diarrhea (late — indicates bowel necrosis)"],
                        "expected_timeline": "Acute: sudden onset, rapidly progressive. Chronic: postprandial pain over weeks/months with food fear and weight loss.",
                        "associated_symptoms": ["Nausea/vomiting", "Diarrhea (may be bloody late)", "Abdominal distension (late)", "Hemodynamic instability (late)"],
                        "risk_factors": ["Age >60", "Atrial fibrillation", "CHF", "Peripheral vascular disease", "Hypercoagulable states", "Recent cardiac catheterization"],
                        "red_herrings": ["Normal lactate early does not exclude", "CT may be normal early — CTA is needed", "Peritoneal signs are LATE and indicate necrosis"],
                    },
                ],
            })

        # ── NEUROLOGICAL ────────────────────────────────────────
        if any(w in symptoms for w in ["headache", "dizzy", "numb", "tingling", "vision",
                                        "weakness", "seizure", "confusion", "memory"]):
            patterns.append({
                "domain": "neurological",
                "illness_scripts": [
                    {
                        "condition": "Migraine",
                        "classic_presentation": "Unilateral pulsating headache, moderate-severe, with nausea/vomiting, photophobia, phonophobia. May have aura (visual, sensory, speech). Lasts 4-72 hours.",
                        "key_discriminating_features": ["Unilateral", "Pulsating/throbbing quality", "Photophobia AND phonophobia", "Nausea/vomiting", "Aura (present in ~30%)", "Disability (want to lie in dark quiet room)", "Prior similar episodes"],
                        "expected_timeline": "Aura: 5-60 min. Headache: 4-72 hours. Prodrome hours-days before. Postdrome hours-days after.",
                        "associated_symptoms": ["Visual aura (scintillating scotoma, zigzag lines)", "Sensory aura (tingling)", "Allodynia", "Neck stiffness"],
                        "risk_factors": ["Female (3:1)", "Age 15-55", "Family history", "Hormonal changes (menstrual)", "Triggers: stress, foods, sleep changes, weather"],
                        "red_herrings": ["First or worst headache needs SAH workup", "Headache with fever needs meningitis workup", "Headache with neurological deficit needs stroke/mass workup", "Bilateral headache does NOT exclude migraine"],
                    },
                    {
                        "condition": "Ischemic Stroke",
                        "classic_presentation": "Acute onset focal neurological deficit: unilateral weakness, numbness, speech difficulty, vision loss, ataxia. Maximal at onset or rapidly progressive.",
                        "key_discriminating_features": ["SUDDEN onset (seconds to minutes)", "Focal deficits following vascular territory", "FAST positive: Face droop, Arm weakness, Speech difficulty", "Risk factors for cerebrovascular disease"],
                        "expected_timeline": "Maximal deficit at onset or progressive over minutes-hours. TIA resolves within 24 hours (usually <1 hour).",
                        "associated_symptoms": ["Headache (more common in hemorrhagic)", "Confusion", "Visual field cut", "Neglect", "Vertigo/ataxia (posterior circulation)"],
                        "risk_factors": ["Age >55", "Hypertension", "Diabetes", "Atrial fibrillation", "Smoking", "Prior TIA/stroke", "Hyperlipidemia", "Carotid stenosis"],
                        "red_herrings": ["Normal CT does not exclude ischemic stroke (CT may be negative early)", "MRI with DWI is gold standard for early detection", "Posterior circulation strokes may present with isolated vertigo — mimics benign conditions"],
                    },
                    {
                        "condition": "Subarachnoid Hemorrhage (SAH)",
                        "classic_presentation": "Sudden-onset 'worst headache of life' reaching peak intensity in seconds, often occipital. May have brief LOC, nausea/vomiting, neck stiffness, photophobia.",
                        "key_discriminating_features": ["Thunderclap onset (maximal in <1 minute)", "'Worst headache of life'", "Neck stiffness (meningismus)", "May have sentinel headache (1-2 weeks prior in 30-50%)", "Altered consciousness"],
                        "expected_timeline": "Instantaneous onset. CT sensitivity ~98% in first 6 hours, decreases to ~90% at 24 hours, ~50% at 5 days.",
                        "associated_symptoms": ["Vomiting", "Photophobia", "Seizure", "Focal deficits (if mass effect)", "Retinal hemorrhages"],
                        "risk_factors": ["Hypertension", "Smoking", "Family history (first-degree)", "Polycystic kidney disease", "Connective tissue disorders (Ehlers-Danlos)", "Cocaine use"],
                        "red_herrings": ["'Worst headache' in someone with no prior headaches is MORE concerning", "Normal neuro exam does not exclude SAH", "Negative CT requires LP if clinical suspicion remains"],
                    },
                    {
                        "condition": "Benign Paroxysmal Positional Vertigo (BPPV)",
                        "classic_presentation": "Brief episodes (seconds) of rotational vertigo triggered by head position changes (rolling in bed, looking up, bending forward). No hearing loss or neurological deficits.",
                        "key_discriminating_features": ["Positional trigger (head movement)", "Brief episodes (<1 minute)", "No hearing loss", "No focal neurological deficits", "Positive Dix-Hallpike test", "Fatigable nystagmus"],
                        "expected_timeline": "Episodes last seconds. Condition may last weeks-months, then resolves. Often recurrent.",
                        "associated_symptoms": ["Nausea with episodes", "Imbalance between episodes", "No tinnitus (unlike Meniere's)"],
                        "risk_factors": ["Age >50", "Female", "Head trauma", "Prolonged bed rest", "Vitamin D deficiency"],
                        "red_herrings": ["Continuous vertigo (not episodic) suggests different diagnosis", "Hearing loss suggests Meniere's", "Focal deficits → stroke until proven otherwise"],
                    },
                    {
                        "condition": "Meningitis",
                        "classic_presentation": "Fever, severe headache, neck stiffness (classic triad). May have photophobia, altered mental status, petechial rash (meningococcal). Rapid progression.",
                        "key_discriminating_features": ["Classic triad: fever + headache + neck stiffness (present in ~44%)", "Kernig sign, Brudzinski sign", "Photophobia", "Rapid deterioration", "Petechial/purpuric rash (meningococcal)"],
                        "expected_timeline": "Bacterial: hours to 1-2 days (rapid). Viral: gradual onset over days, milder course. TB/fungal: weeks.",
                        "associated_symptoms": ["Nausea/vomiting", "Seizures", "Altered mental status", "Rash (petechial → purpuric in meningococcal)"],
                        "risk_factors": ["Age <5 or >60", "Immunocompromised", "Crowded living (military, dorms)", "Recent neurosurgery or LP", "CSF leak/basilar skull fracture"],
                        "red_herrings": ["Absence of ALL triad components has high NPV — but absence of one does not exclude", "Elderly may lack neck stiffness", "Immunocompromised may lack fever"],
                    },
                ],
            })

        # ── CARDIOVASCULAR ──────────────────────────────────────
        if any(w in symptoms for w in ["chest", "heart", "palpitation", "shortness of breath",
                                        "syncope", "edema", "swelling legs"]):
            patterns.append({
                "domain": "cardiovascular",
                "illness_scripts": [
                    {
                        "condition": "Acute Coronary Syndrome (STEMI/NSTEMI/Unstable Angina)",
                        "classic_presentation": "Substernal pressure/heaviness radiating to left arm/jaw, with diaphoresis, dyspnea, nausea. Exertional or at rest. Lasts >20 minutes (unlike stable angina).",
                        "key_discriminating_features": ["Substernal pressure/heaviness/squeezing (NOT sharp/pleuritic)", "Radiation to arm, jaw, back", "Diaphoresis (LR+ 2.0)", "Exertional component", "Duration >20 min", "Similar to prior angina but worse", "Relief with nitroglycerin"],
                        "expected_timeline": "Unstable angina: crescendo pattern. NSTEMI/STEMI: acute onset lasting >20 minutes, not relieved by rest.",
                        "associated_symptoms": ["Diaphoresis", "Dyspnea", "Nausea/vomiting", "Lightheadedness", "Sense of doom"],
                        "risk_factors": ["Age (M>45, F>55)", "Hypertension", "Diabetes", "Hyperlipidemia", "Smoking", "Family history premature CAD", "Obesity", "Cocaine use (any age)"],
                        "red_herrings": ["Sharp, pleuritic, positional pain is less likely ACS (but does NOT exclude)", "Normal ECG does not exclude NSTEMI", "Atypical presentation in women, elderly, diabetics (may have dyspnea only, fatigue, nausea without chest pain)"],
                    },
                    {
                        "condition": "Aortic Dissection",
                        "classic_presentation": "Sudden-onset severe 'tearing/ripping' chest or back pain. May have blood pressure differential between arms, aortic regurgitation murmur, pulse deficit.",
                        "key_discriminating_features": ["Sudden onset at maximal intensity", "Tearing/ripping quality", "Radiates to back (descending) or anterior (ascending)", "BP differential >20mmHg between arms", "Pulse deficit", "Aortic regurgitation murmur (ascending)"],
                        "expected_timeline": "Instantaneous onset at maximal severity. This is key — ACS builds up, dissection is maximal immediately.",
                        "associated_symptoms": ["Syncope", "Stroke symptoms (carotid involvement)", "Limb ischemia", "Abdominal pain (mesenteric involvement)", "Heart failure (acute AR)"],
                        "risk_factors": ["Hypertension (most common)", "Connective tissue disorder (Marfan, Ehlers-Danlos)", "Bicuspid aortic valve", "Prior cardiac surgery", "Cocaine use", "Age >60"],
                        "red_herrings": ["Normal CXR does not exclude (mediastinal widening sensitivity only ~60%)", "Normal D-dimer may help rule OUT but still emergent if high clinical suspicion"],
                    },
                    {
                        "condition": "Heart Failure (Acute Decompensation)",
                        "classic_presentation": "Progressive dyspnea (orthopnea, PND), peripheral edema, fatigue, weight gain. Exam: JVD, crackles, S3, peripheral edema.",
                        "key_discriminating_features": ["Orthopnea (LR+ 2.2)", "PND (LR+ 2.6)", "JVD (LR+ 5.1)", "S3 gallop (LR+ 11)", "Bilateral crackles", "Peripheral edema", "BNP/NT-proBNP elevation"],
                        "expected_timeline": "Chronic with acute exacerbations. Triggers: medication non-compliance, dietary indiscretion, arrhythmia, infection, ischemia.",
                        "associated_symptoms": ["Weight gain (fluid)", "Exercise intolerance", "Cough (especially supine)", "Nocturia", "Hepatomegaly"],
                        "risk_factors": ["Prior MI", "Hypertension", "Valvular disease", "Diabetes", "Obesity", "Alcohol use", "Cardiotoxic drugs"],
                        "red_herrings": ["Normal BNP (<100) effectively rules out CHF (high NPV)", "Wheezing may mimic asthma ('cardiac asthma')"],
                    },
                    {
                        "condition": "Atrial Fibrillation",
                        "classic_presentation": "Palpitations (rapid irregular heartbeat), may have dyspnea, lightheadedness, fatigue. Irregularly irregular pulse.",
                        "key_discriminating_features": ["Irregularly irregular rhythm", "Absence of P waves on ECG", "Variable R-R intervals", "Rapid ventricular rate often 110-160"],
                        "expected_timeline": "Paroxysmal (self-terminating <7 days), persistent (>7 days), permanent. New-onset may present acutely.",
                        "associated_symptoms": ["Exercise intolerance", "Dyspnea", "Chest pressure", "Polyuria (ANP release)"],
                        "risk_factors": ["Age >65", "Hypertension", "CHF", "Valvular disease", "Thyroid disease", "Obesity", "OSA", "Alcohol ('holiday heart')"],
                        "red_herrings": ["Rate control vs rhythm control debate", "Must assess stroke risk (CHA2DS2-VASc)", "Look for underlying cause: thyroid, PE, sepsis"],
                    },
                ],
            })

        # ── MUSCULOSKELETAL ─────────────────────────────────────
        if any(w in symptoms for w in ["pain", "ache", "joint", "muscle", "back", "neck",
                                        "knee", "shoulder", "hip", "stiffness"]):
            patterns.append({
                "domain": "musculoskeletal",
                "illness_scripts": [
                    {
                        "condition": "Mechanical Low Back Pain",
                        "classic_presentation": "Lumbar pain worsened by movement, improved with rest. No radiation below knee, no red flags. Often related to lifting or prolonged positioning.",
                        "key_discriminating_features": ["Mechanical pattern (worse with movement, better with rest)", "No neurological deficits", "No radiation below knee", "Paraspinal muscle tenderness", "Age 20-55"],
                        "expected_timeline": "Acute episodes resolve in 4-6 weeks in 90% of cases. May recur.",
                        "associated_symptoms": ["Muscle spasm", "Limited ROM", "Paraspinal tenderness"],
                        "risk_factors": ["Sedentary lifestyle", "Heavy lifting", "Obesity", "Prior episodes", "Psychosocial factors"],
                        "red_herrings": ["Red flags requiring urgent workup: saddle anesthesia, urinary retention (cauda equina), fever (infection), weight loss (malignancy), age >50 first episode, worst pain supine at night, IV drug use"],
                    },
                    {
                        "condition": "Cauda Equina Syndrome",
                        "classic_presentation": "Low back pain with bilateral leg pain/weakness, saddle anesthesia (perineal numbness), urinary retention/incontinence, bowel incontinence. Surgical emergency.",
                        "key_discriminating_features": ["Saddle anesthesia (LR+ 6.0)", "Urinary retention (LR+ 4.2)", "Bilateral leg symptoms", "Decreased anal sphincter tone", "Progressive neurological deficit"],
                        "expected_timeline": "Can be acute (disc herniation) or progressive (tumor, abscess). Outcome directly related to time to decompression.",
                        "associated_symptoms": ["Bilateral sciatica", "Sexual dysfunction", "Lower extremity weakness (bilateral)"],
                        "risk_factors": ["Large disc herniation", "Spinal stenosis", "Spinal tumor", "Epidural abscess", "Post-spinal procedure"],
                        "red_herrings": ["Unilateral symptoms more likely radiculopathy than cauda equina", "Must ask about urinary symptoms — patients may not volunteer"],
                    },
                    {
                        "condition": "Septic Arthritis",
                        "classic_presentation": "Acute monoarticular joint pain with warmth, swelling, erythema, severely limited ROM. Fever. Most commonly knee. Unable to bear weight.",
                        "key_discriminating_features": ["Monoarticular (usually)", "Hot, swollen, erythematous joint", "Severe pain with any ROM", "Fever", "Unable to bear weight", "Synovial WBC >50,000"],
                        "expected_timeline": "Acute onset over hours to days. Progressive without treatment. Joint destruction can occur in 24-48 hours.",
                        "associated_symptoms": ["Fever/chills", "Malaise", "Joint effusion"],
                        "risk_factors": ["Prosthetic joint", "RA/immunosuppression", "IV drug use", "Recent joint procedure", "Skin infection/cellulitis", "Diabetes"],
                        "red_herrings": ["Gout and pseudogout can look identical — arthrocentesis with crystal analysis is essential", "Polyarticular septic arthritis occurs but is less common (consider gonococcal)"],
                    },
                ],
            })

        # ── DERMATOLOGICAL ──────────────────────────────────────
        if any(w in symptoms for w in ["rash", "itch", "skin", "bump", "lesion", "hives",
                                        "wound", "bruise"]):
            patterns.append({
                "domain": "dermatological",
                "illness_scripts": [
                    {
                        "condition": "Cellulitis",
                        "classic_presentation": "Expanding area of erythema, warmth, swelling, tenderness. Usually unilateral lower extremity. May have fever. Clear border but not sharply demarcated (unlike erysipelas).",
                        "key_discriminating_features": ["Unilateral", "Expanding erythema with warmth/tenderness", "Indistinct borders (vs erysipelas = sharply demarcated)", "Portal of entry often identifiable"],
                        "expected_timeline": "Develops over 1-3 days. Spreads progressively without treatment.",
                        "associated_symptoms": ["Fever", "Lymphangitis (red streaking)", "Regional lymphadenopathy"],
                        "risk_factors": ["Skin break/wound", "Lymphedema", "Obesity", "Diabetes", "Peripheral vascular disease", "Prior cellulitis", "Tinea pedis"],
                        "red_herrings": ["Bilateral 'cellulitis' is almost never bilateral — consider stasis dermatitis, DVT", "Pain out of proportion with crepitus → necrotizing fasciitis (surgical emergency)", "Rapidly progressive with systemic toxicity → necrotizing fasciitis"],
                    },
                    {
                        "condition": "Contact Dermatitis",
                        "classic_presentation": "Pruritic, erythematous, vesicular rash in distribution matching exposure pattern. Well-demarcated borders. Linear streaks suggest plant exposure.",
                        "key_discriminating_features": ["Distribution matches exposure", "Well-demarcated borders", "Pruritus prominent", "Vesicles/bullae in acute phase", "History of exposure"],
                        "expected_timeline": "Allergic: 24-72 hours after exposure. Irritant: hours after exposure. Resolves 2-3 weeks after exposure removed.",
                        "associated_symptoms": ["Intense pruritus", "Vesicles/bullae", "Weeping/crusting"],
                        "risk_factors": ["Occupational exposures", "Nickel allergy", "Cosmetics/fragrances", "Plants (poison ivy/oak)"],
                        "red_herrings": ["Widespread involvement without clear exposure pattern → consider drug eruption or systemic cause"],
                    },
                    {
                        "condition": "Urticaria (Hives) / Angioedema",
                        "classic_presentation": "Raised, erythematous, pruritic wheals (hives) that are transient (individual lesions last <24 hours). Angioedema: deeper swelling of lips, eyelids, tongue.",
                        "key_discriminating_features": ["Individual lesions last <24 hours (key feature)", "Blanchable", "Pruritic", "Migratory (new lesions appear as old ones resolve)", "Angioedema: non-pruritic swelling"],
                        "expected_timeline": "Acute: <6 weeks (usually identifiable trigger). Chronic: >6 weeks (usually idiopathic).",
                        "associated_symptoms": ["Angioedema", "Pruritus", "If anaphylaxis: dyspnea, hypotension, GI symptoms"],
                        "risk_factors": ["Drug exposure (NSAIDs, antibiotics, ACE inhibitors for angioedema)", "Food allergy", "Infection", "Stress"],
                        "red_herrings": ["Individual lesions lasting >24 hours or leaving bruising → urticarial vasculitis, not simple urticaria", "Angioedema without urticaria + on ACE inhibitor → bradykinin-mediated, will not respond to antihistamines"],
                    },
                ],
            })

        # ── PSYCHIATRIC ─────────────────────────────────────────
        if any(w in symptoms for w in ["anxiety", "depress", "insomnia", "stress", "panic",
                                        "mood", "suicid", "hallucin", "psychosis"]):
            patterns.append({
                "domain": "psychiatric",
                "illness_scripts": [
                    {
                        "condition": "Major Depressive Disorder",
                        "classic_presentation": "Depressed mood OR anhedonia (at least one required) plus ≥4 of: sleep changes, guilt/worthlessness, energy loss, concentration difficulty, appetite/weight changes, psychomotor changes, suicidal ideation. Duration ≥2 weeks.",
                        "key_discriminating_features": ["SIG E CAPS mnemonic: Sleep, Interest, Guilt, Energy, Concentration, Appetite, Psychomotor, Suicidality", "Duration ≥2 weeks", "Functional impairment", "Depressed mood OR anhedonia must be present"],
                        "expected_timeline": "Episodes last 6-12 months if untreated. Recurrent in majority. First episode often triggered by stressor.",
                        "associated_symptoms": ["Anxiety (70% comorbid)", "Somatic symptoms (headache, back pain, GI)", "Cognitive symptoms (difficulty concentrating, indecisiveness)"],
                        "risk_factors": ["Family history", "Prior episodes", "Female (2:1)", "Chronic illness", "Substance use", "Childhood adversity", "Social isolation"],
                        "red_herrings": ["Always rule out: hypothyroidism, anemia, sleep apnea, substance use, medication effects, B12 deficiency", "Bipolar disorder: ask about manic episodes before treating with antidepressants alone"],
                    },
                    {
                        "condition": "Generalized Anxiety Disorder",
                        "classic_presentation": "Excessive worry about multiple life domains (not just one), difficulty controlling worry, with ≥3 of: restlessness, fatigue, concentration difficulty, irritability, muscle tension, sleep disturbance. Duration ≥6 months.",
                        "key_discriminating_features": ["Excessive worry across MULTIPLE domains", "Difficulty controlling the worry", "Duration ≥6 months", "Physical symptoms of tension", "Not explained by another psychiatric disorder"],
                        "expected_timeline": "Chronic, waxing and waning. Often begins in adolescence/early adulthood.",
                        "associated_symptoms": ["Muscle tension", "GI symptoms (IBS-like)", "Headache", "Insomnia", "Palpitations"],
                        "risk_factors": ["Family history", "Female (2:1)", "Comorbid depression", "Childhood adversity", "Temperament (neuroticism)"],
                        "red_herrings": ["Rule out: hyperthyroidism, pheochromocytoma, caffeine excess, medication effects, substance withdrawal", "Panic disorder: discrete episodes vs GAD: persistent worry"],
                    },
                    {
                        "condition": "Panic Disorder",
                        "classic_presentation": "Recurrent unexpected panic attacks: sudden surge of intense fear peaking in minutes with ≥4 of: palpitations, sweating, trembling, SOB, choking, chest pain, nausea, dizziness, derealization, paresthesias, chills/hot flashes, fear of dying/losing control.",
                        "key_discriminating_features": ["Discrete episodes (not continuous)", "Peak in minutes", "≥4 symptoms from list", "At least one followed by ≥1 month of worry about additional attacks or avoidant behavior", "Often present to ED thinking cardiac event"],
                        "expected_timeline": "Attacks last 10-30 minutes. Disorder is chronic with recurrent attacks. Anticipatory anxiety between attacks.",
                        "associated_symptoms": ["Agoraphobia (30-50% comorbid)", "Depression", "Substance use (self-medication)"],
                        "risk_factors": ["Family history", "Female (2:1)", "Childhood separation anxiety", "Stressful life events"],
                        "red_herrings": ["MUST rule out cardiac causes, PE, thyroid disease, pheochromocytoma on first presentation", "Chest pain in panic attacks is often sharp/localized vs ACS pressure/diffuse"],
                    },
                ],
            })

        # ── INFECTIOUS ──────────────────────────────────────────
        if any(w in symptoms for w in ["fever", "chills", "infection", "swollen glands",
                                        "night sweats", "body aches"]):
            patterns.append({
                "domain": "infectious",
                "illness_scripts": [
                    {
                        "condition": "Urinary Tract Infection (UTI)",
                        "classic_presentation": "Dysuria, frequency, urgency, suprapubic pain. Cloudy or malodorous urine. No systemic symptoms in uncomplicated cystitis.",
                        "key_discriminating_features": ["Dysuria + frequency + urgency = high probability", "Suprapubic tenderness", "Positive UA (leukocyte esterase, nitrites)", "No fever/flank pain (uncomplicated)"],
                        "expected_timeline": "Acute onset over 1-2 days. If untreated, may progress to pyelonephritis.",
                        "associated_symptoms": ["Hematuria", "Suprapubic discomfort", "Urgency"],
                        "risk_factors": ["Female (short urethra)", "Sexual activity", "Diaphragm/spermicide", "Post-menopausal", "Catheterization", "Diabetes", "Urinary retention"],
                        "red_herrings": ["Fever + flank pain = pyelonephritis (not simple cystitis)", "Elderly may present with AMS only, without urinary symptoms", "Asymptomatic bacteriuria in elderly does NOT require treatment"],
                    },
                    {
                        "condition": "Infective Endocarditis",
                        "classic_presentation": "Prolonged fever with new or changing heart murmur, risk factors (IVDU, prosthetic valve, poor dentition). Duke criteria for diagnosis.",
                        "key_discriminating_features": ["Persistent fever + new murmur", "Multiple positive blood cultures", "Vegetations on echo", "Peripheral embolic phenomena (Osler nodes, Janeway lesions, splinter hemorrhages, Roth spots)", "Duke criteria (2 major, or 1 major + 3 minor, or 5 minor)"],
                        "expected_timeline": "Acute (S. aureus): days to weeks, rapidly destructive. Subacute (viridans strep): weeks to months, insidious.",
                        "associated_symptoms": ["Night sweats", "Weight loss", "Embolic events (stroke, renal infarct, splenic infarct)", "Back pain (vertebral osteomyelitis)", "Splenomegaly"],
                        "risk_factors": ["IV drug use (right-sided, S. aureus)", "Prosthetic valve", "Poor dentition/recent dental procedure", "Congenital heart disease", "Hemodialysis"],
                        "red_herrings": ["Blood cultures may be negative if prior antibiotics or fastidious organisms (HACEK group)", "TTE sensitivity only ~60-75% — TEE needed if clinical suspicion persists"],
                    },
                    {
                        "condition": "Mononucleosis (EBV)",
                        "classic_presentation": "Adolescent/young adult with prolonged sore throat, fatigue, fever, posterior cervical lymphadenopathy, splenomegaly. May have exudative pharyngitis.",
                        "key_discriminating_features": ["Age 15-25", "Posterior cervical lymphadenopathy (anterior less specific)", "Fatigue out of proportion", "Splenomegaly", "Palatal petechiae", "Maculopapular rash after amoxicillin"],
                        "expected_timeline": "Incubation 4-6 weeks. Acute illness 2-4 weeks. Fatigue may persist months.",
                        "associated_symptoms": ["Hepatosplenomegaly", "Periorbital edema", "Palatal petechiae", "Atypical lymphocytes on smear"],
                        "risk_factors": ["Adolescent/young adult", "Close contact (kissing, shared utensils)"],
                        "red_herrings": ["Can look like strep pharyngitis — rapid strep positive does not exclude mono (5-30% co-colonized)", "Ampicillin/amoxicillin causes rash in mono — does NOT mean penicillin allergy"],
                    },
                ],
            })

        # ── ENDOCRINE ───────────────────────────────────────────
        if any(w in symptoms for w in ["fatigue", "weight", "thirst", "sweating", "heat",
                                        "cold intolerance", "tremor", "hair loss"]):
            patterns.append({
                "domain": "endocrine",
                "illness_scripts": [
                    {
                        "condition": "Hypothyroidism",
                        "classic_presentation": "Fatigue, weight gain, cold intolerance, constipation, dry skin, hair loss, depression, menstrual irregularity. Insidious onset.",
                        "key_discriminating_features": ["Cold intolerance", "Weight gain despite reduced appetite", "Constipation", "Dry skin/coarse hair", "Delayed relaxation of deep tendon reflexes", "Elevated TSH"],
                        "expected_timeline": "Gradual onset over months to years. May be precipitated by postpartum period or medication (lithium, amiodarone).",
                        "associated_symptoms": ["Periorbital edema", "Bradycardia", "Macroglossia", "Carpal tunnel syndrome", "Hyperlipidemia"],
                        "risk_factors": ["Female (5-8:1)", "Age >60", "Family history", "Autoimmune disease (Hashimoto's)", "Prior thyroid surgery/radiation", "Medications (lithium, amiodarone)"],
                        "red_herrings": ["Myxedema coma: severe hypothyroidism with AMS, hypothermia, bradycardia — rare but life-threatening", "Subclinical hypothyroidism (elevated TSH, normal T4) may not need treatment"],
                    },
                    {
                        "condition": "Type 2 Diabetes Mellitus / DKA / HHS",
                        "classic_presentation": "T2DM: polyuria, polydipsia, blurred vision, fatigue, weight loss, recurrent infections. DKA: nausea, vomiting, abdominal pain, Kussmaul breathing, fruity breath. HHS: profound dehydration, AMS.",
                        "key_discriminating_features": ["Polyuria + polydipsia + weight loss", "Random glucose >200 with symptoms", "DKA: pH<7.3, bicarb<18, ketones, AG>12", "HHS: glucose>600, osmolality>320, minimal ketones"],
                        "expected_timeline": "T2DM: insidious over months/years. DKA: hours to days. HHS: days to weeks.",
                        "associated_symptoms": ["Recurrent infections (candidal, UTI)", "Acanthosis nigricans", "Blurred vision", "Peripheral neuropathy", "Slow wound healing"],
                        "risk_factors": ["Obesity", "Family history", "Sedentary", "Gestational diabetes", "PCOS", "Ethnicity (African American, Hispanic, Native American)"],
                        "red_herrings": ["DKA can present with abdominal pain mimicking surgical abdomen", "DKA more common in T1DM but occurs in T2DM (ketosis-prone T2DM)", "HHS has higher mortality than DKA"],
                    },
                ],
            })

        # ── HEMATOLOGIC ─────────────────────────────────────────
        if any(w in symptoms for w in ["bruising", "bleeding", "fatigue", "pallor", "pale",
                                        "swollen lymph", "petechiae"]):
            patterns.append({
                "domain": "hematologic",
                "illness_scripts": [
                    {
                        "condition": "Iron Deficiency Anemia",
                        "classic_presentation": "Gradual fatigue, exertional dyspnea, pallor, pica (pagophagia — ice craving), koilonychia. Microcytic hypochromic anemia.",
                        "key_discriminating_features": ["Microcytic hypochromic anemia", "Low ferritin (most specific)", "Low serum iron, high TIBC", "Response to iron supplementation", "Pica/pagophagia"],
                        "expected_timeline": "Gradual onset over months. Must identify and treat underlying cause.",
                        "associated_symptoms": ["Pallor", "Tachycardia", "Glossitis", "Angular cheilitis", "Restless leg syndrome"],
                        "risk_factors": ["Premenopausal women (menstrual blood loss)", "GI blood loss (most common in men and postmenopausal women)", "Pregnancy", "Poor diet", "Malabsorption (celiac)"],
                        "red_herrings": ["In men and postmenopausal women, iron deficiency = GI blood loss until proven otherwise — needs endoscopy to rule out malignancy"],
                    },
                ],
            })

        # ── RENAL / UROLOGIC ────────────────────────────────────
        if any(w in symptoms for w in ["flank pain", "blood in urine", "kidney", "urinary",
                                        "peeing", "urine"]):
            patterns.append({
                "domain": "renal_urologic",
                "illness_scripts": [
                    {
                        "condition": "Nephrolithiasis (Kidney Stones)",
                        "classic_presentation": "Sudden-onset severe colicky flank pain radiating to groin, with nausea/vomiting, hematuria. Patient unable to find comfortable position (writhing — unlike peritonitis where patient lies still).",
                        "key_discriminating_features": ["Colicky (waxing/waning) flank-to-groin pain", "Restlessness (can't get comfortable — vs peritonitis where patient lies still)", "Hematuria (90%, but absence does not exclude)", "CVA tenderness"],
                        "expected_timeline": "Acute onset. Pain comes in waves (ureteral peristalsis). Stones <5mm usually pass spontaneously in 1-2 weeks.",
                        "associated_symptoms": ["Nausea/vomiting (vagal stimulation)", "Hematuria", "Urinary urgency/frequency (distal ureteral stone)"],
                        "risk_factors": ["Male (2-3:1)", "Age 20-50", "Dehydration", "Family history", "Prior stones (50% recurrence in 5 years)", "Hot climate", "High oxalate/sodium/protein diet"],
                        "red_herrings": ["Infected/obstructing stone = urological emergency (fever + stone + hydronephrosis)", "AAA can mimic renal colic in elderly — consider CT if >50 with first episode"],
                    },
                ],
            })

        # ── ALLERGIC / IMMUNOLOGIC ──────────────────────────────
        if any(w in symptoms for w in ["allergy", "hives", "swelling", "reaction", "itch",
                                        "anaphylaxis"]):
            patterns.append({
                "domain": "allergic_immunologic",
                "illness_scripts": [
                    {
                        "condition": "Anaphylaxis",
                        "classic_presentation": "Rapid onset (minutes to hours) after exposure: urticaria/angioedema + respiratory compromise (wheeze, stridor, dyspnea) + hypotension/syncope. GI symptoms common.",
                        "key_discriminating_features": ["Rapid onset after known/suspected allergen", "Two or more organ systems involved", "Skin (hives, flushing) + respiratory OR cardiovascular", "Hypotension after known allergen exposure alone is sufficient"],
                        "expected_timeline": "Minutes to hours after exposure. Biphasic reaction in 5-20% (recurrence 1-72 hours later).",
                        "associated_symptoms": ["Pruritus", "Flushing", "Throat tightness", "Dyspnea/wheeze", "Abdominal cramps/vomiting", "Dizziness/syncope"],
                        "risk_factors": ["Prior anaphylaxis", "Known allergy", "Asthma (risk for severe)", "Mast cell disorders"],
                        "red_herrings": ["Can occur without urticaria (especially drug-induced)", "Biphasic reaction — must observe 4-6+ hours", "Late-onset anaphylaxis (alpha-gal syndrome) occurs 3-6 hours after red meat"],
                    },
                ],
            })

        # Fallback for unmatched symptoms
        if not patterns:
            patterns.append({
                "domain": "general",
                "illness_scripts": [
                    {
                        "condition": "Viral Syndrome",
                        "classic_presentation": "Nonspecific symptoms: fatigue, malaise, low-grade fever, myalgias, headache. Usually self-limited.",
                        "key_discriminating_features": ["Nonspecific constellation", "Self-limited course", "No focal findings", "Often in context of community outbreak"],
                        "expected_timeline": "3-7 days for most viral illnesses.",
                        "associated_symptoms": ["Myalgias", "Mild headache", "Anorexia"],
                        "risk_factors": ["Exposure to sick contacts", "Season"],
                        "red_herrings": ["'Viral syndrome' is a diagnosis of exclusion — ensure serious conditions have been considered"],
                    },
                ],
            })

        return json.dumps({
            "matched_patterns": patterns,
            "patient_profile": {"age": age, "gender": gender, "duration": duration, "severity": severity},
            "instructions": (
                "Use these illness scripts as structured starting points. For each potential diagnosis: "
                "(1) Check if epidemiology fits this patient, "
                "(2) Verify the timeline matches, "
                "(3) Look for key discriminating features, "
                "(4) Note any red herrings that argue against, "
                "(5) Consider what expected findings are absent."
            ),
        })

    # ──────────────────────────────────────────────────────────────
    # Tool: calculate_diagnostic_probability (Bayesian)
    # ──────────────────────────────────────────────────────────────

    async def _calculate_probability(self, tool_input: dict) -> str:
        condition = tool_input.get("condition", "Unknown")
        pre_test_pct = tool_input.get("pre_test_probability_pct", 50.0)
        features = tool_input.get("features_with_lr", [])
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown")

        # Clamp pre-test probability to valid range
        pre_test_pct = max(0.1, min(99.9, pre_test_pct))

        # Convert to odds
        pre_test_odds = pre_test_pct / (100 - pre_test_pct)

        # Apply likelihood ratios sequentially
        calculation_chain = []
        current_odds = pre_test_odds
        current_pct = pre_test_pct

        calculation_chain.append({
            "step": "Pre-test",
            "description": f"Base prevalence (age/gender adjusted) for {condition}",
            "probability_pct": round(current_pct, 2),
            "odds": round(current_odds, 4),
        })

        for i, feature_data in enumerate(features):
            feature_name = feature_data.get("feature", f"Feature {i+1}")
            present = feature_data.get("present", True)
            lr_pos = feature_data.get("lr_positive")
            lr_neg = feature_data.get("lr_negative")
            sensitivity = feature_data.get("sensitivity")
            specificity = feature_data.get("specificity")
            source = feature_data.get("source", "clinical estimate")

            # Calculate LR from sensitivity/specificity if not provided
            if lr_pos is None and sensitivity is not None and specificity is not None:
                lr_pos = sensitivity / (1 - specificity) if specificity < 1 else float('inf')
            if lr_neg is None and sensitivity is not None and specificity is not None:
                lr_neg = (1 - sensitivity) / specificity if specificity > 0 else 0

            # Use appropriate LR based on presence/absence
            if present:
                lr = lr_pos if lr_pos is not None else 1.0
                lr_type = "LR+"
            else:
                lr = lr_neg if lr_neg is not None else 1.0
                lr_type = "LR-"

            # Clamp LR to reasonable range to avoid extreme results
            lr = max(0.001, min(1000, lr))

            # Apply LR
            current_odds *= lr
            current_pct = (current_odds / (1 + current_odds)) * 100

            # Interpret the LR strength
            if lr > 10:
                strength = "STRONG evidence for"
            elif lr > 5:
                strength = "Moderate evidence for"
            elif lr > 2:
                strength = "Weak evidence for"
            elif lr > 0.5:
                strength = "Minimal change"
            elif lr > 0.2:
                strength = "Weak evidence against"
            elif lr > 0.1:
                strength = "Moderate evidence against"
            else:
                strength = "STRONG evidence against"

            step_data = {
                "step": f"Feature {i+1}",
                "feature": feature_name,
                "present": present,
                "lr_type": lr_type,
                "lr_value": round(lr, 3),
                "interpretation": strength,
                "probability_after_pct": round(current_pct, 2),
                "odds_after": round(current_odds, 4),
                "source": source,
            }
            if sensitivity is not None:
                step_data["sensitivity"] = round(sensitivity, 3)
            if specificity is not None:
                step_data["specificity"] = round(specificity, 3)

            calculation_chain.append(step_data)

        # Final result
        post_test_pct = max(0.1, min(99.9, current_pct))

        # Confidence classification
        if post_test_pct >= 90:
            confidence = "Very high — classic presentation, strong diagnostic probability"
        elif post_test_pct >= 70:
            confidence = "High — strong clinical match, most features support"
        elif post_test_pct >= 50:
            confidence = "Moderate — reasonable probability, confirmatory testing recommended"
        elif post_test_pct >= 30:
            confidence = "Low-moderate — possible but consider alternatives"
        elif post_test_pct >= 10:
            confidence = "Low — atypical or must-not-miss consideration"
        else:
            confidence = "Very low — unlikely but included for completeness"

        return json.dumps({
            "condition": condition,
            "pre_test_probability_pct": round(pre_test_pct, 2),
            "post_test_probability_pct": round(post_test_pct, 2),
            "probability_change": round(post_test_pct - pre_test_pct, 2),
            "confidence_level": confidence,
            "calculation_chain": calculation_chain,
            "features_analyzed": len(features),
            "methodology": (
                "Sequential Bayesian updating: pre-test odds × LR1 × LR2 × ... = post-test odds, "
                "then converted back to probability. LR+ applied when feature present, LR- when absent. "
                "Independence assumption: LRs are applied independently (may overestimate confidence "
                "when features are correlated)."
            ),
            "caveats": [
                "LR estimates are approximate and based on published literature or clinical judgment",
                "Independence assumption may not hold for correlated features",
                "Pre-test probability is estimated, not precisely measured",
                "Clinical judgment should always supplement quantitative reasoning",
            ],
        })

    # ──────────────────────────────────────────────────────────────
    # Tool: apply_vindicate_framework
    # ──────────────────────────────────────────────────────────────

    async def _apply_vindicate(self, tool_input: dict) -> str:
        symptoms = tool_input.get("symptoms", "").lower()
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown").lower()
        system = tool_input.get("affected_system", "general").lower()
        duration = tool_input.get("duration", "unknown")

        # Build comprehensive VINDICATE analysis based on affected system
        vindicate: dict[str, dict[str, Any]] = {}

        # The framework provides structured prompts per category, seeded with
        # relevant conditions based on the affected system. The LLM uses these
        # as a systematic checklist to ensure no category is missed.

        system_conditions = self._get_vindicate_conditions(system, symptoms, age, gender)

        for category, data in system_conditions.items():
            vindicate[category] = {
                "category_full_name": data["full_name"],
                "plausible_conditions": data["conditions"],
                "reasoning_prompt": data["reasoning"],
            }

        return json.dumps({
            "vindicate_framework": vindicate,
            "affected_system": system,
            "patient_profile": {"age": age, "gender": gender, "duration": duration},
            "instructions": (
                "Review each VINDICATE category. For each listed condition: "
                "(1) Is it epidemiologically plausible for this patient? "
                "(2) Does the timeline fit? "
                "(3) Are key features present or absent? "
                "Even if a category seems unlikely, briefly note why it was excluded — "
                "this prevents premature closure."
            ),
        })

    def _get_vindicate_conditions(self, system: str, symptoms: str, age: int, gender: str) -> dict:
        """Return VINDICATE conditions organized by affected body system."""

        # Base structure — this covers general conditions.
        # System-specific conditions are added/substituted below.
        conditions: dict[str, dict[str, Any]] = {
            "V_vascular": {
                "full_name": "Vascular (thrombosis, embolism, hemorrhage, infarction, vasculitis)",
                "conditions": [],
                "reasoning": "Consider: Is there ischemia, thrombosis, embolism, hemorrhage, or vasculitis?",
            },
            "I_infectious": {
                "full_name": "Infectious (bacterial, viral, fungal, parasitic, TB)",
                "conditions": [],
                "reasoning": "Consider: Is there fever? Exposure? Immunocompromised? Endemic area?",
            },
            "N_neoplastic": {
                "full_name": "Neoplastic (primary, metastatic, paraneoplastic)",
                "conditions": [],
                "reasoning": "Consider: Age-appropriate malignancy? Constitutional symptoms (weight loss, night sweats)? Mass effect?",
            },
            "D_degenerative_deficiency": {
                "full_name": "Degenerative / Deficiency (wear-and-tear, nutritional, vitamin)",
                "conditions": [],
                "reasoning": "Consider: Chronic wear-and-tear? Nutritional deficiency? Age-related degeneration?",
            },
            "I_iatrogenic_intoxication": {
                "full_name": "Iatrogenic / Intoxication (drug effects, poisoning, post-procedural)",
                "conditions": [],
                "reasoning": "Consider: Any new medications? Drug interactions? Substance use? Recent procedure?",
            },
            "C_congenital": {
                "full_name": "Congenital (genetic, developmental, inherited metabolic)",
                "conditions": [],
                "reasoning": "Consider: Family history? Onset in childhood? Known genetic condition?",
            },
            "A_autoimmune_allergic": {
                "full_name": "Autoimmune / Allergic (autoimmune, hypersensitivity, sarcoidosis)",
                "conditions": [],
                "reasoning": "Consider: Multisystem involvement? Young female? Family history of autoimmune disease? Exposure/allergen?",
            },
            "T_traumatic": {
                "full_name": "Traumatic (blunt, penetrating, overuse, post-surgical)",
                "conditions": [],
                "reasoning": "Consider: Any recent injury? Repetitive strain? Prior surgery? Mechanism of injury?",
            },
            "E_endocrine_metabolic": {
                "full_name": "Endocrine / Metabolic (hormonal, electrolyte, acid-base)",
                "conditions": [],
                "reasoning": "Consider: Thyroid? Adrenal? Glucose? Electrolyte abnormality? Acid-base disturbance?",
            },
        }

        # Populate based on system
        if "cardio" in system or "heart" in system or "chest" in system:
            conditions["V_vascular"]["conditions"] = [
                {"condition": "Acute coronary syndrome (STEMI/NSTEMI)", "brief": "Coronary thrombosis → myocardial ischemia/infarction"},
                {"condition": "Pulmonary embolism", "brief": "Venous thromboembolism → pulmonary vascular obstruction"},
                {"condition": "Aortic dissection", "brief": "Intimal tear → aortic wall separation"},
                {"condition": "Peripheral arterial disease", "brief": "Atherosclerotic stenosis → limb ischemia"},
                {"condition": "Mesenteric ischemia", "brief": "Arterial occlusion → bowel ischemia"},
            ]
            conditions["I_infectious"]["conditions"] = [
                {"condition": "Endocarditis", "brief": "Valve infection → vegetation, emboli, valvular dysfunction"},
                {"condition": "Myocarditis", "brief": "Viral/inflammatory → myocardial inflammation and dysfunction"},
                {"condition": "Pericarditis", "brief": "Pericardial infection/inflammation → chest pain, friction rub"},
            ]
            conditions["N_neoplastic"]["conditions"] = [
                {"condition": "Cardiac myxoma", "brief": "Benign cardiac tumor → obstruction, emboli"},
                {"condition": "Metastatic pericardial disease", "brief": "Pericardial metastases → effusion, tamponade"},
            ]
            conditions["D_degenerative_deficiency"]["conditions"] = [
                {"condition": "Degenerative valvular disease", "brief": "Calcific aortic stenosis, mitral annular calcification"},
                {"condition": "Thiamine deficiency (wet beriberi)", "brief": "B1 deficiency → high-output heart failure"},
            ]
            conditions["I_iatrogenic_intoxication"]["conditions"] = [
                {"condition": "Drug-induced cardiomyopathy", "brief": "Anthracyclines, trastuzumab, alcohol → myocardial damage"},
                {"condition": "Cocaine/stimulant-induced", "brief": "Coronary vasospasm, hypertensive crisis, arrhythmia"},
                {"condition": "Medication-induced QT prolongation", "brief": "Drug effect → torsades de pointes"},
            ]
            conditions["C_congenital"]["conditions"] = [
                {"condition": "Bicuspid aortic valve", "brief": "Congenital → stenosis/regurgitation, aortic root dilation"},
                {"condition": "Hypertrophic cardiomyopathy (HCM)", "brief": "Genetic → asymmetric septal hypertrophy, outflow obstruction"},
                {"condition": "Long QT syndrome", "brief": "Channelopathy → arrhythmia, syncope, sudden death"},
            ]
            conditions["A_autoimmune_allergic"]["conditions"] = [
                {"condition": "Lupus pericarditis/myocarditis", "brief": "SLE → pericardial/myocardial inflammation"},
                {"condition": "Rheumatic heart disease", "brief": "Post-streptococcal autoimmune → valvular damage"},
                {"condition": "Kounis syndrome", "brief": "Allergic → coronary vasospasm during anaphylaxis"},
            ]
            conditions["T_traumatic"]["conditions"] = [
                {"condition": "Cardiac contusion", "brief": "Blunt chest trauma → myocardial bruising, arrhythmia"},
                {"condition": "Traumatic aortic injury", "brief": "Deceleration injury → aortic tear"},
                {"condition": "Costochondritis", "brief": "Chest wall strain → localized reproducible pain"},
            ]
            conditions["E_endocrine_metabolic"]["conditions"] = [
                {"condition": "Thyrotoxicosis", "brief": "Excess thyroid hormone → tachycardia, AF, high-output failure"},
                {"condition": "Pheochromocytoma", "brief": "Catecholamine excess → paroxysmal hypertension, palpitations"},
                {"condition": "Electrolyte abnormality", "brief": "Hypo/hyperkalemia, hypomagnesemia → arrhythmia"},
            ]

        elif "neuro" in system or "brain" in system or "head" in system:
            conditions["V_vascular"]["conditions"] = [
                {"condition": "Ischemic stroke", "brief": "Cerebral artery occlusion → focal deficit"},
                {"condition": "Hemorrhagic stroke (ICH)", "brief": "Intracerebral hemorrhage → focal deficit + headache"},
                {"condition": "Subarachnoid hemorrhage", "brief": "Aneurysm rupture → thunderclap headache"},
                {"condition": "Cerebral venous thrombosis", "brief": "Dural sinus thrombosis → headache, seizure, focal deficits"},
                {"condition": "Temporal arteritis (GCA)", "brief": "Large vessel vasculitis → headache, jaw claudication, vision loss in >50y"},
            ]
            conditions["I_infectious"]["conditions"] = [
                {"condition": "Bacterial meningitis", "brief": "CSF infection → fever, headache, neck stiffness, AMS"},
                {"condition": "Viral encephalitis (HSV)", "brief": "Temporal lobe predilection → fever, AMS, seizures, personality change"},
                {"condition": "Brain abscess", "brief": "Focal infection → headache, fever, focal deficits"},
                {"condition": "Neurocysticercosis", "brief": "Parasitic → seizures, headache (endemic areas)"},
            ]
            conditions["N_neoplastic"]["conditions"] = [
                {"condition": "Brain tumor (primary or metastatic)", "brief": "Mass effect → progressive headache, focal deficits, seizure"},
                {"condition": "Leptomeningeal carcinomatosis", "brief": "Meningeal metastases → cranial neuropathies, headache"},
            ]
            conditions["D_degenerative_deficiency"]["conditions"] = [
                {"condition": "Alzheimer's disease", "brief": "Progressive cortical degeneration → memory loss, cognitive decline"},
                {"condition": "Parkinson's disease", "brief": "Dopaminergic degeneration → tremor, rigidity, bradykinesia"},
                {"condition": "B12 deficiency", "brief": "Subacute combined degeneration → paresthesias, ataxia, cognitive changes"},
                {"condition": "Normal pressure hydrocephalus", "brief": "Triad: gait apraxia, urinary incontinence, dementia"},
            ]
            conditions["I_iatrogenic_intoxication"]["conditions"] = [
                {"condition": "Serotonin syndrome", "brief": "Serotonergic drug excess → AMS, clonus, hyperthermia, autonomic instability"},
                {"condition": "Neuroleptic malignant syndrome", "brief": "Dopamine blockade → rigidity, hyperthermia, AMS"},
                {"condition": "Drug-induced headache (MOH)", "brief": "Analgesic overuse → chronic daily headache"},
                {"condition": "Carbon monoxide poisoning", "brief": "CO exposure → headache, confusion, cherry-red skin"},
            ]
            conditions["C_congenital"]["conditions"] = [
                {"condition": "Arteriovenous malformation (AVM)", "brief": "Congenital vascular → hemorrhage, seizure"},
                {"condition": "Chiari malformation", "brief": "Cerebellar tonsillar herniation → headache with Valsalva, ataxia"},
            ]
            conditions["A_autoimmune_allergic"]["conditions"] = [
                {"condition": "Multiple sclerosis", "brief": "CNS demyelination → disseminated neurological deficits in time and space"},
                {"condition": "CNS vasculitis", "brief": "Cerebral vessel inflammation → multifocal deficits, headache"},
                {"condition": "Autoimmune encephalitis (anti-NMDA-R)", "brief": "Antibody-mediated → psychiatric symptoms, seizures, movement disorder"},
                {"condition": "Guillain-Barré syndrome", "brief": "Post-infectious autoimmune → ascending weakness, areflexia"},
            ]
            conditions["T_traumatic"]["conditions"] = [
                {"condition": "Concussion / post-concussive syndrome", "brief": "Head injury → headache, cognitive symptoms, dizziness"},
                {"condition": "Subdural hematoma", "brief": "Bridging vein tear → progressive headache, AMS (especially elderly on anticoagulants)"},
                {"condition": "Epidural hematoma", "brief": "Temporal bone fracture → lucid interval then rapid decline"},
            ]
            conditions["E_endocrine_metabolic"]["conditions"] = [
                {"condition": "Hypoglycemia", "brief": "Low glucose → confusion, tremor, diaphoresis, seizure"},
                {"condition": "Hyponatremia", "brief": "Low sodium → confusion, seizure, cerebral edema"},
                {"condition": "Hepatic encephalopathy", "brief": "Ammonia → asterixis, confusion, personality change"},
                {"condition": "Uremic encephalopathy", "brief": "Renal failure → AMS, seizure, myoclonus"},
                {"condition": "Thyroid storm", "brief": "Severe thyrotoxicosis → AMS, fever, tachycardia"},
            ]

        elif "resp" in system or "pulm" in system or "lung" in system:
            conditions["V_vascular"]["conditions"] = [
                {"condition": "Pulmonary embolism", "brief": "VTE → acute dyspnea, pleuritic pain, hypoxia"},
                {"condition": "Pulmonary hypertension", "brief": "Elevated PA pressure → progressive dyspnea, RV failure"},
                {"condition": "Pulmonary hemorrhage / DAH", "brief": "Alveolar hemorrhage → hemoptysis, dyspnea, anemia"},
            ]
            conditions["I_infectious"]["conditions"] = [
                {"condition": "Community-acquired pneumonia", "brief": "Lung parenchymal infection → cough, fever, dyspnea, consolidation"},
                {"condition": "Tuberculosis", "brief": "Mycobacterial → chronic cough, hemoptysis, night sweats, weight loss"},
                {"condition": "COVID-19 pneumonia", "brief": "SARS-CoV-2 → bilateral GGO, hypoxia, ARDS"},
                {"condition": "Lung abscess", "brief": "Necrotizing infection → foul sputum, fever"},
                {"condition": "Empyema", "brief": "Infected pleural fluid → persistent fever despite antibiotics"},
            ]
            conditions["N_neoplastic"]["conditions"] = [
                {"condition": "Lung cancer (primary)", "brief": "Bronchogenic carcinoma → cough, hemoptysis, weight loss, smoking history"},
                {"condition": "Pulmonary metastases", "brief": "Hematogenous spread → multiple nodules, dyspnea"},
                {"condition": "Lymphoma (mediastinal)", "brief": "Mediastinal mass → cough, SVC syndrome"},
            ]
            conditions["D_degenerative_deficiency"]["conditions"] = [
                {"condition": "COPD exacerbation", "brief": "Progressive airflow limitation → dyspnea, productive cough, wheezing"},
                {"condition": "Idiopathic pulmonary fibrosis", "brief": "Progressive fibrosis → dry cough, exertional dyspnea, bibasilar crackles"},
            ]
            conditions["I_iatrogenic_intoxication"]["conditions"] = [
                {"condition": "Drug-induced pneumonitis", "brief": "Amiodarone, methotrexate, nitrofurantoin → cough, dyspnea, GGO"},
                {"condition": "Aspiration pneumonia/pneumonitis", "brief": "Aspiration event → cough, fever, infiltrate in dependent segment"},
                {"condition": "Opioid-induced respiratory depression", "brief": "CNS depression → bradypnea, hypoxia, somnolence"},
            ]
            conditions["C_congenital"]["conditions"] = [
                {"condition": "Cystic fibrosis", "brief": "CFTR mutation → chronic productive cough, bronchiectasis, malabsorption"},
                {"condition": "Alpha-1 antitrypsin deficiency", "brief": "Genetic → early-onset emphysema, liver disease"},
            ]
            conditions["A_autoimmune_allergic"]["conditions"] = [
                {"condition": "Asthma", "brief": "Airway hyperreactivity → episodic wheezing, cough, dyspnea, trigger-related"},
                {"condition": "Eosinophilic granulomatosis (Churg-Strauss)", "brief": "Vasculitis → asthma, eosinophilia, multisystem"},
                {"condition": "Hypersensitivity pneumonitis", "brief": "Antigen exposure → cough, dyspnea, GGO"},
                {"condition": "Sarcoidosis", "brief": "Non-caseating granulomas → bilateral hilar lymphadenopathy, cough"},
            ]
            conditions["T_traumatic"]["conditions"] = [
                {"condition": "Pneumothorax", "brief": "Air in pleural space → sudden dyspnea, pleuritic pain, decreased breath sounds"},
                {"condition": "Rib fracture", "brief": "Chest wall injury → localized pain, splinting, risk of pneumothorax"},
                {"condition": "Pulmonary contusion", "brief": "Blunt trauma → hemorrhage into parenchyma → hypoxia"},
            ]
            conditions["E_endocrine_metabolic"]["conditions"] = [
                {"condition": "Metabolic acidosis (Kussmaul breathing)", "brief": "DKA, uremia, toxin → deep rapid breathing as compensation"},
                {"condition": "Obesity hypoventilation syndrome", "brief": "Obesity → chronic hypoventilation, hypoxia, hypercapnia"},
            ]

        else:
            # General / GI / MSK / other — provide broadly applicable conditions
            conditions["V_vascular"]["conditions"] = [
                {"condition": "Thromboembolic event", "brief": "Arterial or venous thrombosis in affected territory"},
                {"condition": "Vasculitis", "brief": "Inflammatory vessel damage → ischemia in affected organ"},
            ]
            conditions["I_infectious"]["conditions"] = [
                {"condition": "Bacterial infection", "brief": "Organ-specific bacterial infection"},
                {"condition": "Viral infection", "brief": "Common viral syndrome or organ-specific viral illness"},
                {"condition": "Opportunistic infection", "brief": "If immunocompromised — broader differential"},
            ]
            conditions["N_neoplastic"]["conditions"] = [
                {"condition": "Age-appropriate malignancy", "brief": "Screen based on age, gender, risk factors, constitutional symptoms"},
                {"condition": "Paraneoplastic syndrome", "brief": "Remote effects of malignancy — can affect any system"},
            ]
            conditions["D_degenerative_deficiency"]["conditions"] = [
                {"condition": "Nutritional deficiency", "brief": "B12, folate, iron, vitamin D — consider based on symptoms"},
                {"condition": "Degenerative condition", "brief": "Age-related wear and degeneration"},
            ]
            conditions["I_iatrogenic_intoxication"]["conditions"] = [
                {"condition": "Medication side effect", "brief": "Review ALL current medications for temporal correlation"},
                {"condition": "Drug-drug interaction", "brief": "Check for pharmacokinetic/pharmacodynamic interactions"},
                {"condition": "Substance use/withdrawal", "brief": "Alcohol, drugs, supplements — ask specifically"},
            ]
            conditions["C_congenital"]["conditions"] = [
                {"condition": "Genetic/inherited condition", "brief": "Family history? Onset in youth? Consanguinity?"},
            ]
            conditions["A_autoimmune_allergic"]["conditions"] = [
                {"condition": "Systemic autoimmune disease", "brief": "SLE, RA, vasculitis — multisystem involvement, young female"},
                {"condition": "Allergic/hypersensitivity reaction", "brief": "New exposure? Medication? Environmental?"},
            ]
            conditions["T_traumatic"]["conditions"] = [
                {"condition": "Traumatic injury", "brief": "Recent injury, overuse, repetitive strain, post-procedural"},
            ]
            conditions["E_endocrine_metabolic"]["conditions"] = [
                {"condition": "Thyroid disorder", "brief": "Hypo/hyperthyroidism — fatigue, weight change, temperature intolerance"},
                {"condition": "Diabetes/glucose disorder", "brief": "DM, DKA, HHS, hypoglycemia, reactive hypoglycemia"},
                {"condition": "Electrolyte abnormality", "brief": "Na, K, Ca, Mg — check if symptoms fit"},
                {"condition": "Adrenal disorder", "brief": "Addison's (fatigue, hypotension, hyperpigmentation) or Cushing's"},
            ]

        return conditions

    # ──────────────────────────────────────────────────────────────
    # Tool: check_anchoring_bias
    # ──────────────────────────────────────────────────────────────

    async def _check_anchoring_bias(self, tool_input: dict) -> str:
        top_dx = tool_input.get("current_top_diagnosis", "Unknown")
        all_symptoms = tool_input.get("all_symptoms", [])
        explained = tool_input.get("explained_symptoms", [])
        unexplained = tool_input.get("unexplained_symptoms", [])
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown").lower()

        analysis = {
            "current_leading_diagnosis": top_dx,
            "total_symptoms": len(all_symptoms),
            "explained_symptoms": {
                "count": len(explained),
                "symptoms": explained,
            },
            "unexplained_symptoms": {
                "count": len(unexplained),
                "symptoms": unexplained,
                "concern_level": (
                    "HIGH — multiple unexplained symptoms suggest the leading diagnosis may be incomplete or wrong"
                    if len(unexplained) >= 3
                    else "MODERATE — some unexplained symptoms warrant consideration of alternatives"
                    if len(unexplained) >= 1
                    else "LOW — leading diagnosis appears to explain the clinical picture well"
                ),
            },
            "explanation_coverage": (
                f"{len(explained)}/{len(all_symptoms)} symptoms explained "
                f"({round(len(explained) / max(len(all_symptoms), 1) * 100)}%)"
            ),
        }

        # Generate alternative considerations based on unexplained symptoms
        alternatives = []
        unexplained_lower = " ".join(unexplained).lower()

        # Check for symptom patterns that suggest specific alternative diagnoses
        alternative_patterns = [
            {
                "triggers": ["weight loss", "night sweats", "fatigue"],
                "alternatives": ["Malignancy (lymphoma, solid tumor)", "Chronic infection (TB, endocarditis, HIV)", "Hyperthyroidism"],
                "reasoning": "Constitutional B-symptoms suggest systemic disease",
            },
            {
                "triggers": ["rash", "joint pain", "fatigue"],
                "alternatives": ["Systemic lupus erythematosus", "Viral syndrome (parvovirus, hepatitis)", "Drug reaction", "Reactive arthritis"],
                "reasoning": "Multi-system involvement suggests autoimmune or systemic infectious process",
            },
            {
                "triggers": ["fever", "weight loss", "sweats"],
                "alternatives": ["Malignancy", "Endocarditis", "Tuberculosis", "HIV", "Abscess"],
                "reasoning": "Fever of unknown origin differential — consider the 'Big 3': infection, malignancy, autoimmune",
            },
            {
                "triggers": ["numbness", "tingling", "weakness"],
                "alternatives": ["Multiple sclerosis", "B12 deficiency", "Guillain-Barré", "Peripheral neuropathy (DM)", "Cervical/lumbar radiculopathy"],
                "reasoning": "Neurological symptoms unexplained by current diagnosis suggest primary neurological process",
            },
            {
                "triggers": ["anxiety", "palpitations", "weight loss", "tremor"],
                "alternatives": ["Hyperthyroidism", "Pheochromocytoma", "Substance use/withdrawal", "Cardiac arrhythmia"],
                "reasoning": "Sympathetic activation symptoms could be endocrine or cardiac rather than psychiatric",
            },
            {
                "triggers": ["fatigue", "weight gain", "constipation", "cold"],
                "alternatives": ["Hypothyroidism", "Depression", "Anemia", "Sleep disorder"],
                "reasoning": "Hypometabolic symptoms suggest endocrine etiology",
            },
            {
                "triggers": ["dry eyes", "dry mouth", "joint pain"],
                "alternatives": ["Sjögren's syndrome", "Rheumatoid arthritis", "Sarcoidosis", "IgG4-related disease"],
                "reasoning": "Sicca symptoms with arthralgia suggest autoimmune exocrinopathy",
            },
        ]

        for pattern in alternative_patterns:
            trigger_match = sum(1 for t in pattern["triggers"] if any(t in s.lower() for s in unexplained))
            if trigger_match >= 2:
                alternatives.append({
                    "matching_unexplained_pattern": [t for t in pattern["triggers"] if any(t in s.lower() for s in unexplained)],
                    "alternative_diagnoses": pattern["alternatives"],
                    "reasoning": pattern["reasoning"],
                })

        analysis["alternative_considerations"] = alternatives

        # Cognitive bias warnings
        bias_warnings = []
        if len(unexplained) >= 2:
            bias_warnings.append(
                "PREMATURE CLOSURE WARNING: Multiple unexplained symptoms. Have you stopped "
                "searching too early? Consider: Is there a single unifying diagnosis that "
                "explains ALL symptoms better?"
            )
        if len(all_symptoms) <= 2:
            bias_warnings.append(
                "INSUFFICIENT DATA WARNING: Very few symptoms documented. Consider: Are there "
                "additional symptoms the patient hasn't mentioned? Use Review of Systems to screen."
            )

        # Always include these prompts
        bias_warnings.append(
            f"REPRESENTATION ERROR CHECK: Is {top_dx} truly the best fit, or did you anchor on "
            f"the first diagnosis that came to mind? What would a colleague suggest?"
        )
        bias_warnings.append(
            "ATYPICAL PRESENTATION CHECK: Could this be an atypical presentation of a common disease? "
            "Women, elderly, diabetics, and immunocompromised patients often present atypically."
        )
        bias_warnings.append(
            "DUAL PATHOLOGY CHECK: Could the patient have TWO conditions simultaneously? "
            "Not all symptoms must be explained by a single diagnosis."
        )

        analysis["cognitive_bias_warnings"] = bias_warnings

        # Structured debiasing questions
        analysis["debiasing_questions"] = [
            f"If {top_dx} is wrong, what is the most dangerous alternative?",
            f"What single test would most change your confidence in {top_dx}?",
            "If you had to argue AGAINST your leading diagnosis, what would you say?",
            "What would a specialist in the most relevant field consider first?",
            "Is there a common condition you might be overlooking because it seems 'too simple'?",
        ]

        return json.dumps(analysis)
