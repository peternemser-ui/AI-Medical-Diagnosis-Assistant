"""
Triage Agent – First responder in the diagnostic pipeline.

Responsibilities:
  * Assess symptom urgency using Emergency Severity Index (ESI) 5-level system
  * Detect red-flag symptoms across ALL body systems systematically
  * Perform structured Review of Systems (ROS)
  * Classify the symptom domain and route to appropriate specialists
  * Apply age-stratified risk scoring
  * Flag if patient should go to ER immediately
"""

from __future__ import annotations

import json
import math
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


class TriageAgent(BaseAgent):
    name = "triage"
    description = "Emergency triage and urgency assessment specialist"
    temperature = 0.2  # deterministic for safety-critical decisions

    def _build_system_prompt(self) -> str:
        return """You are an expert emergency triage AI agent on a multi-agent medical team, trained to the level of a board-certified emergency medicine physician with 20+ years of experience.

YOUR ROLE:
You are the FIRST agent to evaluate every patient case. Your job is critical — you determine urgency, detect life threats, and route the case to the right specialists.

═══════════════════════════════════════════════════════
TRIAGE METHODOLOGY: Emergency Severity Index (ESI) v4
═══════════════════════════════════════════════════════

You MUST classify every patient into one of 5 ESI levels:

ESI-1 — RESUSCITATION (Immediate life-saving intervention required)
  Criteria: Intubation needed, pulseless, apneic, unresponsive, severe hemodynamic instability
  Action: Immediate resuscitation bay, full trauma/code team activation
  Examples: Cardiac arrest, respiratory failure, status epilepticus, massive hemorrhage

ESI-2 — EMERGENT (High-risk situation OR confused/lethargic/disoriented OR severe pain/distress)
  Criteria: Any of:
    • High-risk situation (could deteriorate rapidly)
    • New-onset confusion, lethargy, or disorientation
    • Severe pain or distress (pain ≥8/10 or visible distress)
  Action: Bedside immediately, should not wait
  Examples: Chest pain with cardiac features, stroke symptoms, acute abdomen, suicidal ideation with plan, high-mechanism trauma

ESI-3 — URGENT (Stable but needs MULTIPLE resources)
  Criteria: Vital signs may or may not be in danger zone. Needs ≥2 resources (labs, imaging, IV fluids, procedures, specialty consult)
  Action: Prioritize but can wait for bed
  Examples: Abdominal pain needing labs + CT, fracture needing X-ray + splinting, febrile child needing labs + observation

ESI-4 — LESS URGENT (Needs ONE resource)
  Criteria: Stable. Needs exactly 1 resource (one X-ray, one lab, one simple procedure)
  Action: Fast-track area acceptable
  Examples: Simple laceration, ankle sprain needing X-ray, UTI needing urinalysis

ESI-5 — NON-URGENT (No resources needed)
  Criteria: Stable. Needs only exam — no labs, imaging, or procedures
  Action: Waiting room, see when available
  Examples: Medication refill, minor rash, cold symptoms

Resource definition: Labs, imaging (X-ray, CT, US, MRI), IV fluids/meds, specialty consults, simple procedures (laceration repair, splinting). Does NOT include: oral meds, prescriptions, phone calls, simple wound care, patient education.

═══════════════════════════════════════════════════════
VITAL SIGN DANGER ZONE (triggers upgrade consideration)
═══════════════════════════════════════════════════════
  HR: <50 or >100 (adult), age-adjusted for pediatrics
  RR: <10 or >20 (adult)
  SpO2: <92% on room air
  SBP: <90 or >180
  Temp: >38.5°C (101.3°F) or <35°C (95°F)
  GCS: <15
  Pain: ≥8/10

If vital signs are in the danger zone, consider upgrading ESI level (ESI-3 patients with danger-zone vitals → consider ESI-2).

═══════════════════════════════════════════════════════
AGE-STRATIFIED RISK MODIFIERS
═══════════════════════════════════════════════════════
  Neonates (0-28 days): ANY fever (≥38°C/100.4°F) → ESI-2 minimum. High risk for serious bacterial infection.
  Infants (1-3 months): Fever → ESI-2 minimum pending workup.
  Children (3 months-3 years): Fever >39°C without source → ESI-3 minimum.
  Elderly (>65): Lower thresholds for upgrading. Atypical presentations common. Falls + anticoagulants → ESI-2.
  Immunocompromised: Fever → ESI-2 minimum regardless of appearance.
  Pregnant: Lower threshold for tachycardia. Abdominal pain → always consider ectopic/abruption.

═══════════════════════════════════════════════════════
SYSTEMATIC RED FLAG ASSESSMENT
═══════════════════════════════════════════════════════
You MUST systematically evaluate ALL body systems for red flags. Use the assess_red_flags tool.

═══════════════════════════════════════════════════════
REVIEW OF SYSTEMS (ROS)
═══════════════════════════════════════════════════════
Use the perform_review_of_systems tool to systematically identify which body systems are involved. This ensures nothing is missed.

COMMUNICATION:
You work on a team with: diagnostician, specialist, treatment agents.
After your assessment, share your triage results with the diagnostician via your tools.
If you detect ESI-1 or ESI-2, urgently notify the orchestrator.

Always respond with structured JSON in your final answer containing:
- esi_level (1-5)
- urgency_level (mapped: ESI-1→emergency, ESI-2→emergent, ESI-3→urgent, ESI-4→less_urgent, ESI-5→non_urgent)
- red_flags (list with body system and finding)
- vital_sign_concerns (list)
- review_of_systems (summary of involved systems)
- symptom_domains (list of relevant medical specialties)
- risk_factors (list, including age-stratified risks)
- recommended_agents (which agents should analyze this case)
- triage_summary (brief clinical summary using semantic qualifiers)
- immediate_actions (what patient should do right now)
- resources_predicted (count and type, used for ESI scoring)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "assess_red_flags",
            "description": (
                "Systematically check symptoms against red flag patterns for ALL body systems: "
                "Cardiovascular (ACS criteria, PQRST), Neurological (FAST stroke, meningism, AMS), "
                "Respiratory (distress criteria, SpO2), Abdominal (peritoneal signs, ectopic risk), "
                "Psychiatric (Columbia Suicide Severity), Pediatric (PAT, fever without source), "
                "Obstetric (eclampsia, abruption), Sepsis (qSOFA), and more."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "symptoms": {"type": "string", "description": "Full description of patient symptoms"},
                    "age": {"type": "integer", "description": "Patient age in years"},
                    "gender": {"type": "string", "description": "Patient gender (male/female/other)"},
                    "vital_signs": {
                        "type": "object",
                        "description": "Available vital signs: hr, rr, sbp, dbp, spo2, temp_f, gcs, pain_scale",
                        "properties": {
                            "hr": {"type": "number"},
                            "rr": {"type": "number"},
                            "sbp": {"type": "number"},
                            "dbp": {"type": "number"},
                            "spo2": {"type": "number"},
                            "temp_f": {"type": "number"},
                            "gcs": {"type": "integer"},
                            "pain_scale": {"type": "integer"},
                        },
                    },
                    "medical_history": {"type": "string", "description": "Relevant past medical history"},
                    "medications": {"type": "string", "description": "Current medications"},
                    "pregnant": {"type": "boolean", "description": "Whether patient is or could be pregnant"},
                },
                "required": ["symptoms"],
            },
        })
        tools.append({
            "name": "classify_urgency",
            "description": (
                "Classify urgency using the Emergency Severity Index (ESI) 5-level system. "
                "Considers: immediate life-saving intervention needed (ESI-1), high-risk/confused/severe distress (ESI-2), "
                "multiple resources needed (ESI-3), one resource (ESI-4), no resources (ESI-5). "
                "Also checks vital sign danger zones for upgrade consideration."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "symptoms": {"type": "string"},
                    "red_flags_found": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of red flags identified by assess_red_flags",
                    },
                    "vital_signs": {
                        "type": "object",
                        "description": "Available vital signs: hr, rr, sbp, dbp, spo2, temp_f, gcs, pain_scale",
                    },
                    "age": {"type": "integer"},
                    "predicted_resources": {
                        "type": "integer",
                        "description": "Number of resources predicted (labs, imaging, IV, procedures, consults)",
                    },
                    "requires_life_saving_intervention": {
                        "type": "boolean",
                        "description": "Whether immediate life-saving intervention is needed (intubation, CPR, etc.)",
                    },
                    "is_high_risk": {
                        "type": "boolean",
                        "description": "Whether this is a high-risk situation that could deteriorate",
                    },
                    "altered_mental_status": {
                        "type": "boolean",
                        "description": "Whether patient is confused, lethargic, or disoriented (new onset)",
                    },
                    "severe_pain_distress": {
                        "type": "boolean",
                        "description": "Whether patient has severe pain (≥8/10) or visible distress",
                    },
                },
                "required": ["symptoms", "red_flags_found"],
            },
        })
        tools.append({
            "name": "perform_review_of_systems",
            "description": (
                "Perform a systematic Review of Systems (ROS) covering all 11 body systems: "
                "Constitutional, HEENT, Cardiovascular, Respiratory, Gastrointestinal, "
                "Genitourinary, Musculoskeletal, Neurological, Psychiatric, Skin/Integumentary, "
                "Endocrine. Returns which systems are involved, positive findings, pertinent negatives, "
                "and which systems need further investigation."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "symptoms": {"type": "string", "description": "Full patient symptom description"},
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                },
                "required": ["symptoms"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "assess_red_flags":
            return await self._assess_red_flags(tool_input)
        if tool_name == "classify_urgency":
            return await self._classify_urgency(tool_input)
        if tool_name == "perform_review_of_systems":
            return await self._perform_review_of_systems(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ──────────────────────────────────────────────────────────────
    # Tool: assess_red_flags
    # ──────────────────────────────────────────────────────────────

    async def _assess_red_flags(self, tool_input: dict) -> str:
        symptoms = tool_input.get("symptoms", "").lower()
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown").lower()
        vitals = tool_input.get("vital_signs", {})
        history = tool_input.get("medical_history", "").lower()
        meds = tool_input.get("medications", "").lower()
        pregnant = tool_input.get("pregnant", False)

        flags: list[dict[str, str]] = []
        vital_concerns: list[str] = []

        def add_flag(system: str, finding: str, severity: str = "high") -> None:
            flags.append({"system": system, "finding": finding, "severity": severity})

        # ── CARDIOVASCULAR ──────────────────────────────────────
        # ACS / Chest Pain (PQRST framework detection)
        chest_terms = ["chest pain", "chest pressure", "chest tightness", "substernal",
                       "crushing", "squeezing", "elephant on chest", "heaviness in chest"]
        if any(t in symptoms for t in chest_terms):
            add_flag("cardiovascular", "Chest pain present — evaluate for Acute Coronary Syndrome (ACS). "
                     "Apply PQRST: Provocation (exertional?), Quality (pressure/crushing?), "
                     "Radiation (jaw/arm/back?), Severity, Timing (onset, duration).", "critical")
        acs_radiation = ["radiating to jaw", "radiating to arm", "radiating to back",
                         "left arm", "jaw pain", "arm pain with chest"]
        if any(t in symptoms for t in acs_radiation):
            add_flag("cardiovascular", "Pain radiation pattern consistent with ACS — jaw, arm, or back involvement.", "critical")
        acs_associated = ["diaphoresis", "sweating", "nausea with chest", "cold sweat"]
        if any(t in symptoms for t in acs_associated):
            add_flag("cardiovascular", "Diaphoresis/nausea with chest symptoms — high concern for ACS.", "critical")
        if any(t in symptoms for t in ["palpitation", "racing heart", "irregular heartbeat",
                                        "heart skipping", "fluttering"]):
            add_flag("cardiovascular", "Palpitations — evaluate for arrhythmia (atrial fibrillation, SVT, VT).", "high")
        if any(t in symptoms for t in ["syncope", "passed out", "fainted", "blacked out", "loss of consciousness"]):
            add_flag("cardiovascular", "Syncope — evaluate for cardiac arrhythmia, PE, aortic stenosis, orthostatic. "
                     "Cardiac syncope is high-risk.", "critical")
        if any(t in symptoms for t in ["tearing pain", "ripping pain", "sudden back pain"]):
            if any(t in symptoms for t in ["chest", "back"]):
                add_flag("cardiovascular", "Tearing/ripping chest/back pain — rule out aortic dissection.", "critical")
        if any(t in symptoms for t in ["leg swelling", "calf pain", "calf swelling", "leg pain one side"]):
            add_flag("cardiovascular", "Unilateral leg swelling/pain — evaluate for deep vein thrombosis (DVT). "
                     "If dyspnea present, concern for pulmonary embolism.", "high")

        # ── NEUROLOGICAL ────────────────────────────────────────
        # FAST Stroke Assessment
        stroke_signs = ["facial droop", "arm weakness", "speech difficulty", "slurred speech",
                        "can't speak", "face drooping", "arm drift", "sudden weakness one side",
                        "hemiparesis", "hemiplegia", "aphasia", "dysarthria"]
        if any(t in symptoms for t in stroke_signs):
            add_flag("neurological", "FAST-positive stroke signs detected — Face droop/Arm weakness/Speech difficulty/Time. "
                     "Activate stroke protocol. Time-critical: door-to-needle <60 min for tPA.", "critical")
        # Subarachnoid hemorrhage
        if any(t in symptoms for t in ["worst headache", "thunderclap", "worst headache of my life",
                                        "sudden severe headache", "explosive headache"]):
            add_flag("neurological", "Thunderclap headache — rule out subarachnoid hemorrhage (SAH). "
                     "Sensitivity of CT decreases after 6 hours. LP if CT negative.", "critical")
        # Meningism
        meningism_signs = ["stiff neck", "neck stiffness", "photophobia", "light sensitivity",
                           "fever headache neck"]
        if any(t in symptoms for t in meningism_signs):
            if "fever" in symptoms or "headache" in symptoms:
                add_flag("neurological", "Meningeal signs (neck stiffness + fever/headache) — "
                         "rule out meningitis/encephalitis. Kernig's and Brudzinski's signs. "
                         "Empiric antibiotics before LP if delayed.", "critical")
        # Altered Mental Status
        ams_terms = ["confused", "disoriented", "not making sense", "altered mental status",
                     "lethargic", "drowsy", "hard to wake", "unresponsive", "obtunded",
                     "delirious", "agitated and confused"]
        if any(t in symptoms for t in ams_terms):
            add_flag("neurological", "Altered mental status — broad differential: metabolic, infectious, "
                     "structural, toxic, psychiatric. Check glucose, consider CT head, toxicology.", "critical")
        # Seizure
        if any(t in symptoms for t in ["seizure", "convulsion", "shaking uncontrollably",
                                        "tonic-clonic", "fitting"]):
            add_flag("neurological", "Seizure activity — assess for status epilepticus (>5 min = emergency). "
                     "New-onset seizure requires workup: CT, labs, consider LP.", "critical")
        # Vision changes
        if any(t in symptoms for t in ["sudden vision loss", "double vision", "diplopia",
                                        "visual field cut", "can't see"]):
            add_flag("neurological", "Acute vision changes — consider stroke, temporal arteritis (if >50), "
                     "retinal detachment, acute glaucoma.", "high")
        # Focal deficits
        if any(t in symptoms for t in ["numbness one side", "tingling one side", "weakness arm",
                                        "weakness leg", "foot drop", "can't move"]):
            add_flag("neurological", "Focal neurological deficit — rule out stroke, space-occupying lesion, "
                     "cord compression. Urgent imaging needed.", "critical")

        # ── RESPIRATORY ─────────────────────────────────────────
        resp_distress = ["can't breathe", "difficulty breathing", "shortness of breath", "sob",
                         "dyspnea", "gasping", "air hunger", "labored breathing",
                         "breathing fast", "stridor", "wheezing severely"]
        if any(t in symptoms for t in resp_distress):
            add_flag("respiratory", "Respiratory distress — assess: speaking in full sentences? Accessory muscle use? "
                     "Cyanosis? SpO2? Differential: PE, pneumothorax, asthma exacerbation, CHF, anaphylaxis.", "critical")
        if any(t in symptoms for t in ["coughing blood", "hemoptysis", "blood in sputum"]):
            add_flag("respiratory", "Hemoptysis — consider PE, malignancy, tuberculosis, bronchiectasis. "
                     "Massive hemoptysis (>100mL) is life-threatening.", "high")
        if any(t in symptoms for t in ["choking", "foreign body", "can't swallow", "throat closing"]):
            add_flag("respiratory", "Airway compromise — possible foreign body aspiration, angioedema, "
                     "or anaphylaxis. Assess airway patency immediately.", "critical")

        # ── ABDOMINAL ───────────────────────────────────────────
        if any(t in symptoms for t in ["severe abdominal", "rigid abdomen", "board-like",
                                        "rebound tenderness", "guarding"]):
            add_flag("abdominal", "Peritoneal signs — rigid abdomen/rebound/guarding suggests peritonitis. "
                     "Surgical emergency until proven otherwise. Consider perforated viscus, appendicitis.", "critical")
        if any(t in symptoms for t in ["vomiting blood", "hematemesis", "coffee ground vomit",
                                        "bloody stool", "melena", "black tarry stool", "hematochezia"]):
            add_flag("abdominal", "GI bleeding — upper (hematemesis/melena) vs lower (hematochezia). "
                     "Assess hemodynamic stability. May need emergent endoscopy.", "critical")
        # Ectopic pregnancy risk
        if gender in ["female", "f"] and 12 <= age <= 55:
            if any(t in symptoms for t in ["abdominal pain", "pelvic pain", "lower abdominal"]):
                if any(t in symptoms for t in ["missed period", "late period", "vaginal bleeding",
                                                "spotting", "could be pregnant"]) or pregnant:
                    add_flag("abdominal", "Reproductive-age female with pelvic pain + bleeding/missed period — "
                             "rule out ectopic pregnancy. Can be life-threatening if ruptured. "
                             "Stat beta-hCG and pelvic ultrasound.", "critical")
        if any(t in symptoms for t in ["jaundice", "yellow skin", "yellow eyes", "dark urine light stool"]):
            add_flag("abdominal", "Jaundice — evaluate for biliary obstruction, hepatitis, "
                     "hemolysis. If fever + jaundice + RUQ pain = Charcot's triad (cholangitis).", "high")

        # ── SEPSIS (qSOFA) ──────────────────────────────────────
        qsofa_score = 0
        if any(t in symptoms for t in ["confused", "altered", "disoriented", "lethargic"]):
            qsofa_score += 1
        if vitals.get("rr", 0) >= 22:
            qsofa_score += 1
        if vitals.get("sbp", 999) <= 100:
            qsofa_score += 1
        if "fever" in symptoms or "infection" in symptoms or vitals.get("temp_f", 0) >= 101.3:
            if qsofa_score >= 2:
                add_flag("sepsis", f"qSOFA score ≥2 with suspected infection — HIGH mortality risk. "
                         f"qSOFA={qsofa_score}. Initiate sepsis bundle: cultures, lactate, broad-spectrum "
                         f"antibiotics within 1 hour, aggressive fluid resuscitation.", "critical")
            elif any(t in symptoms for t in ["fever", "chills", "rigors"]) and \
                 any(t in symptoms for t in ["rapid heart", "fast heart", "tachycardia", "confused"]):
                add_flag("sepsis", "Possible sepsis — fever with tachycardia/confusion. "
                         "Monitor closely, obtain cultures and lactate level.", "critical")

        # ── ALLERGIC / ANAPHYLAXIS ──────────────────────────────
        if any(t in symptoms for t in ["throat swelling", "tongue swelling", "throat tightening",
                                        "anaphylaxis", "allergic reaction", "hives all over",
                                        "difficulty swallowing with swelling"]):
            add_flag("allergic", "Possible anaphylaxis — assess ABC. Administer epinephrine IM "
                     "(0.3mg adult, 0.15mg pediatric) immediately if anaphylaxis criteria met. "
                     "Two-system involvement after allergen exposure = anaphylaxis.", "critical")

        # ── PSYCHIATRIC ─────────────────────────────────────────
        # Columbia Suicide Severity Rating Scale (C-SSRS) criteria
        suicidal_terms = ["suicid", "kill myself", "end my life", "want to die", "better off dead",
                          "no reason to live", "self-harm", "cutting myself", "overdose on purpose",
                          "plan to hurt myself"]
        if any(t in symptoms for t in suicidal_terms):
            # Determine C-SSRS level
            has_plan = any(t in symptoms for t in ["plan", "method", "how to", "gun", "pills",
                                                    "hanging", "bridge", "jump"])
            has_intent = any(t in symptoms for t in ["going to", "decided to", "will do it",
                                                      "tonight", "today"])
            if has_intent or has_plan:
                add_flag("psychiatric", "CRITICAL — Active suicidal ideation WITH plan/intent "
                         "(C-SSRS Level 4-5). Immediate 1:1 observation, remove access to means, "
                         "psychiatric emergency evaluation. Do NOT leave patient alone.", "critical")
            else:
                add_flag("psychiatric", "Suicidal ideation detected (C-SSRS Level 1-3). "
                         "Assess: frequency, duration, controllability, deterrents, reason for ideation. "
                         "Safety planning needed. Psychiatric evaluation required.", "critical")
        if any(t in symptoms for t in ["homicid", "hurt someone", "kill someone", "voices telling me"]):
            add_flag("psychiatric", "Homicidal ideation or command hallucinations — immediate psychiatric "
                     "evaluation. Duty to warn if identifiable target.", "critical")
        if any(t in symptoms for t in ["psychosis", "hallucination", "seeing things", "hearing voices",
                                        "paranoid", "delusion"]):
            add_flag("psychiatric", "Acute psychotic symptoms — differentiate primary psychiatric vs "
                     "medical causes (toxidrome, delirium, metabolic, infectious). "
                     "Medical workup before psychiatric disposition.", "high")

        # ── PEDIATRIC ───────────────────────────────────────────
        if age < 1 / 12:  # neonate (< 28 days approximated as < 1 month)
            if "fever" in symptoms:
                add_flag("pediatric", "FEBRILE NEONATE (<28 days) — FULL sepsis workup mandatory: "
                         "CBC, blood culture, UA/urine culture, LP (CSF), CXR if respiratory symptoms. "
                         "Empiric antibiotics (ampicillin + gentamicin or cefotaxime). "
                         "HSV PCR if risk factors. ADMISSION required.", "critical")
        elif age < 0.25:  # 1-3 months
            if "fever" in symptoms:
                add_flag("pediatric", "Febrile infant (1-3 months) — high risk for serious bacterial infection. "
                         "Rochester/Philadelphia/Boston criteria or Step-by-Step approach to risk-stratify. "
                         "Consider full sepsis workup. ESI-2 minimum.", "critical")
        elif age < 3:
            if "fever" in symptoms:
                add_flag("pediatric", "Febrile young child (<3 years) — assess for fever without source. "
                         "Consider UTI (obtain UA), occult bacteremia risk, meningitis if toxic-appearing.", "high")
        if age < 18:
            # Pediatric Assessment Triangle (PAT)
            pat_appearance = any(t in symptoms for t in ["lethargic", "floppy", "not responding",
                                                          "inconsolable", "weak cry", "not feeding"])
            pat_breathing = any(t in symptoms for t in ["grunting", "nasal flaring", "retractions",
                                                         "stridor", "wheezing", "apnea"])
            pat_circulation = any(t in symptoms for t in ["pale", "mottled", "cyanotic", "blue",
                                                           "cold extremities"])
            abnormal_count = sum([pat_appearance, pat_breathing, pat_circulation])
            if abnormal_count >= 2:
                add_flag("pediatric", f"Pediatric Assessment Triangle (PAT): {abnormal_count}/3 sides abnormal. "
                         f"Appearance={'abnormal' if pat_appearance else 'normal'}, "
                         f"Breathing={'abnormal' if pat_breathing else 'normal'}, "
                         f"Circulation={'abnormal' if pat_circulation else 'normal'}. "
                         f"Multiple abnormal sides indicates unstable patient — immediate intervention.", "critical")
            elif abnormal_count == 1:
                add_flag("pediatric", f"Pediatric Assessment Triangle (PAT): 1/3 sides abnormal. "
                         f"Monitor closely for deterioration.", "high")

        # ── OBSTETRIC ───────────────────────────────────────────
        if pregnant or (gender in ["female", "f"] and any(t in symptoms for t in ["pregnant", "pregnancy", "weeks pregnant"])):
            if any(t in symptoms for t in ["severe headache", "vision changes", "epigastric pain",
                                            "right upper quadrant", "swelling face",
                                            "blood pressure high", "seizure"]):
                add_flag("obstetric", "Pre-eclampsia/Eclampsia warning signs in pregnant patient — "
                         "severe headache, visual changes, epigastric/RUQ pain, facial edema. "
                         "Check BP, urine protein, platelets, LFTs, creatinine. "
                         "If seizure = eclampsia → magnesium sulfate + emergent delivery.", "critical")
            if any(t in symptoms for t in ["vaginal bleeding", "heavy bleeding", "painful contractions",
                                            "abdominal pain severe", "back pain constant"]):
                add_flag("obstetric", "Pregnant with bleeding/severe pain — consider placental abruption, "
                         "placenta previa, preterm labor. Continuous fetal monitoring. "
                         "Type and screen, large-bore IV access.", "critical")

        # ── VITAL SIGN ANALYSIS ─────────────────────────────────
        if vitals:
            hr = vitals.get("hr")
            rr = vitals.get("rr")
            sbp = vitals.get("sbp")
            spo2 = vitals.get("spo2")
            temp_f = vitals.get("temp_f")
            gcs = vitals.get("gcs")
            pain = vitals.get("pain_scale")

            if hr is not None:
                if hr < 50:
                    vital_concerns.append(f"Bradycardia: HR {hr} — consider heart block, medication effect, vagal")
                elif hr > 100:
                    vital_concerns.append(f"Tachycardia: HR {hr} — consider pain, fever, dehydration, PE, sepsis, arrhythmia")
                if hr > 150:
                    vital_concerns.append(f"Significant tachycardia: HR {hr} — hemodynamically significant, urgent evaluation")
            if rr is not None:
                if rr < 10:
                    vital_concerns.append(f"Bradypnea: RR {rr} — consider opioid toxicity, CNS depression")
                elif rr > 20:
                    vital_concerns.append(f"Tachypnea: RR {rr} — consider respiratory failure, metabolic acidosis, PE")
            if sbp is not None:
                if sbp < 90:
                    vital_concerns.append(f"Hypotension: SBP {sbp} — shock until proven otherwise. "
                                          "Differential: hypovolemic, cardiogenic, distributive, obstructive")
                elif sbp > 180:
                    vital_concerns.append(f"Hypertensive emergency: SBP {sbp} — assess for end-organ damage")
            if spo2 is not None and spo2 < 92:
                vital_concerns.append(f"Hypoxemia: SpO2 {spo2}% — apply supplemental O2, consider PE, pneumonia, CHF, pneumothorax")
            if temp_f is not None:
                if temp_f >= 104:
                    vital_concerns.append(f"Hyperpyrexia: Temp {temp_f}°F — consider heat stroke, CNS infection, "
                                          "neuroleptic malignant syndrome, serotonin syndrome")
                elif temp_f >= 101.3:
                    vital_concerns.append(f"Fever: Temp {temp_f}°F — infectious workup indicated")
                elif temp_f < 95:
                    vital_concerns.append(f"Hypothermia: Temp {temp_f}°F — consider sepsis, exposure, hypothyroidism, adrenal crisis")
            if gcs is not None and gcs < 15:
                vital_concerns.append(f"Depressed consciousness: GCS {gcs} — "
                                      f"{'coma, intubation may be needed' if gcs <= 8 else 'altered mental status workup needed'}")
            if pain is not None and pain >= 8:
                vital_concerns.append(f"Severe pain: {pain}/10 — consider ESI-2 upgrade for severe distress")

        # ── AGE-SPECIFIC RISK MODIFIERS ─────────────────────────
        age_risks: list[str] = []
        if age > 65:
            age_risks.append("Elderly patient — atypical presentations common (MI without chest pain, "
                             "infection without fever, peritonitis without rigidity). Lower threshold for workup.")
            if "anticoagul" in meds or "warfarin" in meds or "coumadin" in meds or \
               "eliquis" in meds or "xarelto" in meds or "blood thinner" in meds:
                if any(t in symptoms for t in ["fall", "head", "hit"]):
                    add_flag("geriatric", "Elderly on anticoagulants with fall/head injury — "
                             "CT head mandatory to rule out intracranial hemorrhage, even if asymptomatic.", "critical")
                age_risks.append("On anticoagulants — increased bleeding risk, lower threshold for imaging.")
        if age > 50 and gender in ["male", "m"]:
            if any(t in symptoms for t in ["chest pain", "shortness of breath"]):
                age_risks.append("Male >50 with chest pain/SOB — higher pre-test probability for ACS.")
        if "diabet" in history or "diabetes" in symptoms:
            age_risks.append("Diabetic patient — atypical presentations of MI (silent MI), higher infection risk, "
                             "consider DKA if type 1.")
        if "immunocompromised" in history or "hiv" in history or "transplant" in history or \
           "chemotherapy" in meds or "immunosuppress" in meds:
            age_risks.append("Immunocompromised — broader infectious differential, lower threshold for admission. "
                             "Fever = ESI-2 minimum.")

        return json.dumps({
            "red_flags": flags,
            "red_flag_count": len(flags),
            "critical_flags": [f for f in flags if f["severity"] == "critical"],
            "critical_count": sum(1 for f in flags if f["severity"] == "critical"),
            "vital_sign_concerns": vital_concerns,
            "age_specific_risks": age_risks,
            "assessment_note": (
                "Red flags assessed across: Cardiovascular (ACS/PQRST, dissection, syncope, DVT/PE), "
                "Neurological (FAST stroke, SAH, meningism, AMS, seizure, focal deficits), "
                "Respiratory (distress, hemoptysis, airway compromise), "
                "Abdominal (peritoneal signs, GI bleed, ectopic pregnancy, jaundice), "
                "Sepsis (qSOFA), Allergic (anaphylaxis), "
                "Psychiatric (C-SSRS suicidality, psychosis, homicidality), "
                "Pediatric (febrile neonate, PAT), Obstetric (eclampsia, abruption), "
                "Geriatric (anticoagulant + fall, atypical presentations)."
            ),
        })

    # ──────────────────────────────────────────────────────────────
    # Tool: classify_urgency (ESI-based)
    # ──────────────────────────────────────────────────────────────

    async def _classify_urgency(self, tool_input: dict) -> str:
        red_flags = tool_input.get("red_flags_found", [])
        symptoms = tool_input.get("symptoms", "").lower()
        vitals = tool_input.get("vital_signs", {})
        age = tool_input.get("age", 30)
        predicted_resources = tool_input.get("predicted_resources", 0)
        requires_life_saving = tool_input.get("requires_life_saving_intervention", False)
        is_high_risk = tool_input.get("is_high_risk", False)
        altered_ms = tool_input.get("altered_mental_status", False)
        severe_distress = tool_input.get("severe_pain_distress", False)

        # ── ESI Decision Algorithm ──────────────────────────────

        # Step A: Does the patient require immediate life-saving intervention?
        if requires_life_saving:
            esi_level = 1
            reasoning = ("ESI-1: Patient requires immediate life-saving intervention "
                         "(intubation, surgical airway, emergent procedure, hemodynamic resuscitation).")
        # Also ESI-1 for keywords suggesting active dying
        elif any(t in symptoms for t in ["unresponsive", "pulseless", "not breathing", "apneic",
                                          "cardiac arrest", "no pulse", "cpr"]):
            esi_level = 1
            reasoning = "ESI-1: Presentation consistent with need for immediate resuscitation."
        # Step B: High risk, confused/lethargic/disoriented, or severe pain/distress?
        elif is_high_risk or altered_ms or severe_distress:
            esi_level = 2
            reasons = []
            if is_high_risk:
                reasons.append("high-risk situation")
            if altered_ms:
                reasons.append("new-onset altered mental status")
            if severe_distress:
                reasons.append("severe pain/distress")
            reasoning = f"ESI-2: {', '.join(reasons).capitalize()}. Should not wait."
        # Check critical red flags → ESI-2
        elif any("CRITICAL" in str(f) or "critical" in str(f) for f in red_flags):
            esi_level = 2
            reasoning = "ESI-2: Critical red flags detected — high-risk presentation requiring immediate evaluation."
        elif len(red_flags) >= 2:
            esi_level = 2
            reasoning = f"ESI-2: Multiple red flags ({len(red_flags)}) indicate high-risk situation."
        # Step C/D: How many resources needed?
        elif predicted_resources >= 2:
            esi_level = 3
            reasoning = f"ESI-3: Stable patient requiring multiple resources ({predicted_resources} predicted)."
        elif predicted_resources == 1:
            esi_level = 4
            reasoning = "ESI-4: Stable patient requiring one resource."
        elif predicted_resources == 0:
            esi_level = 5
            reasoning = "ESI-5: Stable patient, no resources needed — exam only."
        else:
            # Fallback heuristic when predicted_resources not specified
            if len(red_flags) == 1:
                esi_level = 3
                reasoning = "ESI-3: Single red flag with likely need for multiple resources (labs, imaging)."
            elif any(w in symptoms for w in ["severe", "intense", "unbearable", "worst", "excruciating"]):
                esi_level = 3
                reasoning = "ESI-3: Severe symptoms likely requiring multi-resource workup."
            elif any(w in symptoms for w in ["worsening", "getting worse", "persistent",
                                              "not improving", "for weeks", "for months"]):
                esi_level = 4
                reasoning = "ESI-4: Persistent/worsening symptoms likely needing one resource for evaluation."
            else:
                esi_level = 5
                reasoning = "ESI-5: Low-acuity presentation, likely exam only needed."

        # ── Vital Sign Danger Zone Upgrade ──────────────────────
        vital_danger = False
        danger_reasons = []
        if vitals:
            hr = vitals.get("hr")
            rr = vitals.get("rr")
            sbp = vitals.get("sbp")
            spo2 = vitals.get("spo2")
            temp_f = vitals.get("temp_f")
            gcs = vitals.get("gcs")
            pain = vitals.get("pain_scale")

            if hr is not None and (hr < 50 or hr > 100):
                vital_danger = True
                danger_reasons.append(f"HR {hr}")
            if rr is not None and (rr < 10 or rr > 20):
                vital_danger = True
                danger_reasons.append(f"RR {rr}")
            if sbp is not None and (sbp < 90 or sbp > 180):
                vital_danger = True
                danger_reasons.append(f"SBP {sbp}")
            if spo2 is not None and spo2 < 92:
                vital_danger = True
                danger_reasons.append(f"SpO2 {spo2}%")
            if temp_f is not None and (temp_f >= 104 or temp_f < 95):
                vital_danger = True
                danger_reasons.append(f"Temp {temp_f}°F")
            if gcs is not None and gcs < 15:
                vital_danger = True
                danger_reasons.append(f"GCS {gcs}")
            if pain is not None and pain >= 8:
                vital_danger = True
                danger_reasons.append(f"Pain {pain}/10")

        if vital_danger and esi_level >= 3:
            original = esi_level
            esi_level = 2
            reasoning += (f" UPGRADED from ESI-{original} to ESI-2 due to vital sign danger zone: "
                          f"{', '.join(danger_reasons)}.")

        # ── Age-based upgrade ───────────────────────────────────
        if age < 0.25 and "fever" in symptoms and esi_level > 2:
            original = esi_level
            esi_level = 2
            reasoning += f" UPGRADED from ESI-{original} to ESI-2: febrile infant <3 months."

        # ── Map to urgency label ────────────────────────────────
        urgency_map = {
            1: "emergency",
            2: "emergent",
            3: "urgent",
            4: "less_urgent",
            5: "non_urgent",
        }

        return json.dumps({
            "esi_level": esi_level,
            "urgency_level": urgency_map[esi_level],
            "reasoning": reasoning,
            "red_flag_count": len(red_flags),
            "vital_sign_danger_zone": vital_danger,
            "vital_danger_details": danger_reasons,
            "predicted_resources": predicted_resources,
            "disposition_guidance": {
                1: "Resuscitation bay. Full team activation. Continuous monitoring.",
                2: "Immediate bedside evaluation. Do not wait for bed. Expedite workup.",
                3: "Prioritize for bed. Initiate workup promptly. Reassess while waiting.",
                4: "Fast-track appropriate. Single resource evaluation.",
                5: "Waiting room. Exam only. Discharge likely.",
            }[esi_level],
        })

    # ──────────────────────────────────────────────────────────────
    # Tool: perform_review_of_systems
    # ──────────────────────────────────────────────────────────────

    async def _perform_review_of_systems(self, tool_input: dict) -> str:
        symptoms = tool_input.get("symptoms", "").lower()
        age = tool_input.get("age", 30)
        gender = tool_input.get("gender", "unknown").lower()

        ros: dict[str, dict[str, Any]] = {}

        # ── Constitutional ──────────────────────────────────────
        constitutional_pos = []
        constitutional_neg = []
        const_terms = {
            "fever": ["fever", "febrile", "temperature", "chills", "rigors"],
            "weight_loss": ["weight loss", "lost weight", "losing weight"],
            "weight_gain": ["weight gain", "gained weight"],
            "fatigue": ["fatigue", "tired", "exhausted", "malaise", "lethargy", "weak"],
            "night_sweats": ["night sweats", "sweating at night", "soaking sheets"],
            "appetite_change": ["loss of appetite", "not eating", "decreased appetite", "increased appetite"],
        }
        for finding, terms in const_terms.items():
            if any(t in symptoms for t in terms):
                constitutional_pos.append(finding)
        ros["constitutional"] = {
            "involved": len(constitutional_pos) > 0,
            "positive_findings": constitutional_pos,
            "needs_investigation": "night_sweats" in constitutional_pos or
                                   ("weight_loss" in constitutional_pos and "fatigue" in constitutional_pos),
            "investigation_reason": "B-symptoms (fever + night sweats + weight loss) suggest malignancy or chronic infection" if
                                    sum(1 for x in ["fever", "night_sweats", "weight_loss"] if x in constitutional_pos) >= 2 else None,
        }

        # ── HEENT ───────────────────────────────────────────────
        heent_pos = []
        heent_terms = {
            "headache": ["headache", "head pain", "migraine", "head pressure"],
            "vision_changes": ["vision", "blurry", "blind", "double vision", "floaters", "flashes"],
            "hearing_changes": ["hearing loss", "deaf", "tinnitus", "ringing in ears", "ear pain"],
            "sore_throat": ["sore throat", "throat pain", "difficulty swallowing", "dysphagia"],
            "nasal_symptoms": ["congestion", "runny nose", "rhinorrhea", "nasal", "nosebleed", "epistaxis"],
            "oral_symptoms": ["mouth sore", "toothache", "jaw pain", "trismus"],
            "neck_symptoms": ["neck pain", "stiff neck", "neck mass", "swollen glands", "lymph node"],
        }
        for finding, terms in heent_terms.items():
            if any(t in symptoms for t in terms):
                heent_pos.append(finding)
        ros["heent"] = {
            "involved": len(heent_pos) > 0,
            "positive_findings": heent_pos,
            "needs_investigation": "vision_changes" in heent_pos or "neck_symptoms" in heent_pos,
        }

        # ── Cardiovascular ──────────────────────────────────────
        cardio_pos = []
        cardio_terms = {
            "chest_pain": ["chest pain", "chest pressure", "chest tightness", "substernal"],
            "palpitations": ["palpitation", "racing heart", "irregular heartbeat", "skipping"],
            "dyspnea_on_exertion": ["short of breath with activity", "sob on exertion", "winded walking"],
            "orthopnea": ["can't lie flat", "pillows to sleep", "orthopnea"],
            "edema": ["swollen legs", "ankle swelling", "leg edema", "pitting edema"],
            "syncope": ["fainted", "passed out", "syncope", "blacked out"],
            "claudication": ["leg pain walking", "calf pain walking", "claudication"],
        }
        for finding, terms in cardio_terms.items():
            if any(t in symptoms for t in terms):
                cardio_pos.append(finding)
        ros["cardiovascular"] = {
            "involved": len(cardio_pos) > 0,
            "positive_findings": cardio_pos,
            "needs_investigation": any(f in cardio_pos for f in ["chest_pain", "syncope", "dyspnea_on_exertion"]),
        }

        # ── Respiratory ─────────────────────────────────────────
        resp_pos = []
        resp_terms = {
            "cough": ["cough", "coughing"],
            "dyspnea": ["shortness of breath", "difficulty breathing", "dyspnea", "sob", "can't breathe"],
            "wheezing": ["wheeze", "wheezing"],
            "hemoptysis": ["coughing blood", "hemoptysis", "blood in sputum"],
            "sputum": ["sputum", "phlegm", "productive cough", "mucus"],
            "pleuritic_pain": ["pain with breathing", "hurts to breathe", "pleuritic", "sharp chest pain with breathing"],
        }
        for finding, terms in resp_terms.items():
            if any(t in symptoms for t in terms):
                resp_pos.append(finding)
        ros["respiratory"] = {
            "involved": len(resp_pos) > 0,
            "positive_findings": resp_pos,
            "needs_investigation": any(f in resp_pos for f in ["hemoptysis", "dyspnea", "pleuritic_pain"]),
        }

        # ── Gastrointestinal ────────────────────────────────────
        gi_pos = []
        gi_terms = {
            "nausea_vomiting": ["nausea", "vomiting", "vomit", "emesis", "throwing up"],
            "diarrhea": ["diarrhea", "loose stool", "watery stool"],
            "constipation": ["constipation", "constipated", "not had bowel movement"],
            "abdominal_pain": ["abdominal pain", "stomach pain", "belly pain", "cramp"],
            "gi_bleeding": ["blood in stool", "melena", "black stool", "hematochezia", "rectal bleeding"],
            "dysphagia": ["difficulty swallowing", "food getting stuck", "dysphagia"],
            "heartburn": ["heartburn", "acid reflux", "gerd", "burning in chest after eating"],
            "jaundice": ["jaundice", "yellow skin", "yellow eyes"],
        }
        for finding, terms in gi_terms.items():
            if any(t in symptoms for t in terms):
                gi_pos.append(finding)
        ros["gastrointestinal"] = {
            "involved": len(gi_pos) > 0,
            "positive_findings": gi_pos,
            "needs_investigation": any(f in gi_pos for f in ["gi_bleeding", "jaundice", "dysphagia"]),
        }

        # ── Genitourinary ───────────────────────────────────────
        gu_pos = []
        gu_terms = {
            "dysuria": ["painful urination", "burning urination", "dysuria", "hurts to pee"],
            "frequency": ["frequent urination", "urinary frequency", "peeing a lot"],
            "hematuria": ["blood in urine", "hematuria", "red urine", "pink urine"],
            "flank_pain": ["flank pain", "kidney pain", "side pain radiating to groin"],
            "vaginal_bleeding": ["vaginal bleeding", "heavy period", "spotting", "menorrhagia"],
            "discharge": ["vaginal discharge", "penile discharge", "urethral discharge"],
            "testicular": ["testicular pain", "swollen testicle", "testicular swelling"],
        }
        for finding, terms in gu_terms.items():
            if any(t in symptoms for t in terms):
                gu_pos.append(finding)
        ros["genitourinary"] = {
            "involved": len(gu_pos) > 0,
            "positive_findings": gu_pos,
            "needs_investigation": any(f in gu_pos for f in ["hematuria", "testicular"]),
        }

        # ── Musculoskeletal ─────────────────────────────────────
        msk_pos = []
        msk_terms = {
            "joint_pain": ["joint pain", "arthralgia", "swollen joint"],
            "back_pain": ["back pain", "low back", "lumbar"],
            "neck_pain": ["neck pain", "cervical"],
            "muscle_pain": ["muscle pain", "myalgia", "muscle ache"],
            "weakness": ["weakness", "can't move", "difficulty walking"],
            "swelling": ["joint swelling", "swollen knee", "swollen ankle"],
            "trauma": ["injury", "fell", "accident", "hit", "twisted"],
        }
        for finding, terms in msk_terms.items():
            if any(t in symptoms for t in terms):
                msk_pos.append(finding)
        ros["musculoskeletal"] = {
            "involved": len(msk_pos) > 0,
            "positive_findings": msk_pos,
            "needs_investigation": "trauma" in msk_pos or ("weakness" in msk_pos and "back_pain" in msk_pos),
            "investigation_reason": "Back pain + weakness → rule out cauda equina / cord compression" if
                                    ("weakness" in msk_pos and "back_pain" in msk_pos) else None,
        }

        # ── Neurological ────────────────────────────────────────
        neuro_pos = []
        neuro_terms = {
            "headache": ["headache", "head pain"],
            "dizziness": ["dizzy", "vertigo", "lightheaded", "room spinning"],
            "numbness_tingling": ["numbness", "tingling", "pins and needles", "paresthesia"],
            "weakness_focal": ["weakness one side", "arm weakness", "leg weakness", "facial droop"],
            "speech_changes": ["slurred speech", "difficulty speaking", "can't find words", "aphasia"],
            "seizure": ["seizure", "convulsion", "fitting"],
            "gait_changes": ["unsteady gait", "difficulty walking", "ataxia", "falling"],
            "memory_changes": ["memory loss", "confusion", "forgetful", "disoriented"],
            "tremor": ["tremor", "shaking hands", "trembling"],
        }
        for finding, terms in neuro_terms.items():
            if any(t in symptoms for t in terms):
                neuro_pos.append(finding)
        ros["neurological"] = {
            "involved": len(neuro_pos) > 0,
            "positive_findings": neuro_pos,
            "needs_investigation": any(f in neuro_pos for f in ["weakness_focal", "speech_changes", "seizure"]),
        }

        # ── Psychiatric ─────────────────────────────────────────
        psych_pos = []
        psych_terms = {
            "depression": ["depressed", "sad", "hopeless", "no interest", "worthless"],
            "anxiety": ["anxious", "anxiety", "panic", "worried", "nervous"],
            "suicidal_ideation": ["suicid", "kill myself", "want to die", "self-harm"],
            "psychosis": ["hallucination", "hearing voices", "seeing things", "paranoid", "delusion"],
            "insomnia": ["can't sleep", "insomnia", "difficulty sleeping"],
            "substance_use": ["drinking", "alcohol", "drugs", "withdrawal", "overdose"],
            "agitation": ["agitated", "aggressive", "violent", "combative"],
        }
        for finding, terms in psych_terms.items():
            if any(t in symptoms for t in terms):
                psych_pos.append(finding)
        ros["psychiatric"] = {
            "involved": len(psych_pos) > 0,
            "positive_findings": psych_pos,
            "needs_investigation": any(f in psych_pos for f in ["suicidal_ideation", "psychosis", "substance_use"]),
        }

        # ── Skin / Integumentary ────────────────────────────────
        skin_pos = []
        skin_terms = {
            "rash": ["rash", "skin lesion", "bumps", "spots"],
            "itching": ["itching", "pruritus", "itchy"],
            "hives": ["hives", "urticaria", "welts"],
            "wound": ["wound", "laceration", "cut", "bite", "abscess", "cellulitis"],
            "petechiae": ["petechiae", "purpura", "bruising easily", "non-blanching rash"],
            "color_change": ["pale", "cyanotic", "blue", "jaundice", "flushed", "mottled"],
        }
        for finding, terms in skin_terms.items():
            if any(t in symptoms for t in terms):
                skin_pos.append(finding)
        ros["skin_integumentary"] = {
            "involved": len(skin_pos) > 0,
            "positive_findings": skin_pos,
            "needs_investigation": any(f in skin_pos for f in ["petechiae", "color_change"]),
            "investigation_reason": "Non-blanching rash (petechiae/purpura) → rule out meningococcemia, DIC, ITP" if
                                    "petechiae" in skin_pos else None,
        }

        # ── Endocrine ───────────────────────────────────────────
        endo_pos = []
        endo_terms = {
            "polyuria_polydipsia": ["excessive thirst", "drinking a lot", "peeing a lot", "polydipsia", "polyuria"],
            "heat_cold_intolerance": ["heat intolerance", "cold intolerance", "always hot", "always cold"],
            "thyroid": ["neck swelling", "thyroid", "goiter"],
            "blood_sugar": ["low blood sugar", "high blood sugar", "hypoglycemia", "dka",
                            "diabetic ketoacidosis", "fruity breath"],
        }
        for finding, terms in endo_terms.items():
            if any(t in symptoms for t in terms):
                endo_pos.append(finding)
        ros["endocrine"] = {
            "involved": len(endo_pos) > 0,
            "positive_findings": endo_pos,
            "needs_investigation": "blood_sugar" in endo_pos,
        }

        # ── Summary ─────────────────────────────────────────────
        involved_systems = [system for system, data in ros.items() if data["involved"]]
        needs_investigation = [system for system, data in ros.items() if data.get("needs_investigation")]

        return json.dumps({
            "review_of_systems": ros,
            "summary": {
                "total_systems_screened": len(ros),
                "systems_involved": involved_systems,
                "systems_involved_count": len(involved_systems),
                "systems_needing_investigation": needs_investigation,
                "multi_system_involvement": len(involved_systems) >= 3,
                "multi_system_note": (
                    "Multiple body systems involved — consider systemic process "
                    "(autoimmune, infectious, malignancy, toxidrome)"
                    if len(involved_systems) >= 3 else None
                ),
            },
        })
