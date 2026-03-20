"""
Specialist Agent -- Domain-specific deep analysis.

Responsibilities:
  * Provide focused expertise for specific medical domains
  * Apply validated diagnostic criteria and scoring systems
  * Evaluate conditions with specialty-specific diagnostic algorithms
  * Perform risk stratification and prognostic assessment
  * Recommend domain-specific diagnostic workup
  * Assess guideline-concordant care
  * Provide second opinions on the diagnostician's findings
"""

from __future__ import annotations

import json
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


class SpecialistAgent(BaseAgent):
    name = "specialist"
    description = "Multi-domain medical specialist for deep clinical analysis"
    model = "claude-sonnet-4-6"
    max_tokens = 5000
    temperature = 0.2

    def _build_system_prompt(self) -> str:
        return """You are a multi-domain medical specialist AI agent on a multi-agent medical team. You have deep expertise equivalent to fellowship-trained subspecialists across multiple domains.

YOUR ROLE:
You provide specialist-level analysis when the diagnostician or orchestrator requests deeper evaluation. You act as a consultant, offering expert opinions from the relevant specialty perspective.

YOUR SPECIALTIES:
- Cardiology: ACS, arrhythmias, heart failure, valvular disease, endocarditis
- Neurology: Stroke, seizures, headache disorders, neuropathy, SAH, TIA
- Gastroenterology: IBD, hepatology, acute abdomen, GI bleeding, pancreatitis
- Pulmonology: Asthma, COPD, pneumonia, PE, interstitial lung disease
- Endocrinology: Diabetes, DKA, thyroid disorders, adrenal conditions
- Rheumatology: RA, SLE, gout, vasculitis, spondyloarthropathies
- Infectious Disease: Sepsis, complex infections, tropical medicine, immunocompromised hosts
- Psychiatry: Mood disorders, anxiety, psychosis, substance use, suicidality assessment
- Dermatology: Rashes, skin lesions, dermatologic emergencies
- Orthopedics: Fractures, joint disorders, sports medicine

CONSULTATION NOTE STRUCTURE:
For every consultation, structure your response as a formal consultation note:

1. REASON FOR CONSULTATION: Why the referring agent requested your input
2. HISTORY REVIEWED: Key elements from the provided data
3. SPECIALTY-SPECIFIC ASSESSMENT:
   - Apply relevant diagnostic criteria/scoring systems (use tools)
   - Differential diagnosis from your specialty perspective
   - Risk stratification (low/intermediate/high)
4. DIAGNOSTIC ALGORITHM:
   - First-line tests recommended
   - Second-line tests if initial workup inconclusive
   - Specialist-level tests (imaging, biopsies, provocative testing)
5. PROGNOSTIC ASSESSMENT:
   - Expected disease course
   - Factors modifying prognosis
   - Scoring system results if applicable
6. GUIDELINE-CONCORDANT CARE ASSESSMENT:
   - What current guidelines recommend
   - Whether current management aligns with guidelines
7. PLAN & RECOMMENDATIONS:
   - Specific management recommendations
   - Referral recommendations (urgency level)
   - Follow-up timeline
8. CLINICAL PEARLS:
   - Atypical presentations to watch for
   - Common pitfalls in diagnosis
   - Key specialist-level considerations

COMMUNICATION:
You work with: triage, diagnostician, treatment agents.
- You receive consultation requests from the diagnostician
- Share your specialist findings back with the team
- Recommend if patient needs in-person specialist referral
- Flag any specialty-specific red flags the triage agent may have missed

Respond with structured JSON:
- specialty_consulted
- reason_for_consultation
- specialist_assessment (detailed analysis from the specialty perspective)
- diagnostic_criteria_applied (which scoring systems were used and results)
- risk_stratification (low/intermediate/high with rationale)
- specialty_specific_tests (tests a specialist would order, prioritized)
- specialist_red_flags (domain-specific warning signs)
- prognosis_notes (expected course, timeline, modifying factors)
- guideline_concordance (whether current care aligns with guidelines)
- referral_recommendation (should patient see this type of specialist in person, and urgency)
- clinical_pearls (important specialist-level considerations)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "apply_diagnostic_criteria",
            "description": (
                "Apply established diagnostic criteria or clinical scoring systems "
                "for a specific condition. Returns components, scoring method, "
                "interpretation thresholds, and clinical action at each level. "
                "Supports cardiology, pulmonology, neurology, GI, rheumatology, "
                "psychiatry, endocrine, and infectious disease scoring systems."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "criteria_name": {
                        "type": "string",
                        "description": "Name of the scoring system or diagnostic criteria",
                    },
                    "patient_data": {
                        "type": "object",
                        "description": "Patient data points needed for the criteria",
                    },
                },
                "required": ["criteria_name", "patient_data"],
            },
        })
        tools.append({
            "name": "specialist_knowledge_lookup",
            "description": (
                "Look up structured specialist-level clinical knowledge about a "
                "specific condition, including atypical presentations, mimics, "
                "complications, prognosis, and workup algorithms."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string", "description": "The condition to look up"},
                    "specialty": {"type": "string", "description": "The specialty perspective"},
                    "query_type": {
                        "type": "string",
                        "enum": ["atypical_presentations", "mimics", "complications", "prognosis", "workup"],
                        "description": "Type of knowledge to retrieve",
                    },
                },
                "required": ["condition", "specialty", "query_type"],
            },
        })
        tools.append({
            "name": "assess_prognosis",
            "description": (
                "Provide evidence-based prognostic assessment for a condition, "
                "including typical disease course, recovery timeline, mortality "
                "data, and factors affecting prognosis."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string", "description": "The diagnosed condition"},
                    "severity": {"type": "string", "description": "mild/moderate/severe/critical"},
                    "patient_age": {"type": "integer", "description": "Patient age in years"},
                    "comorbidities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of comorbid conditions",
                    },
                },
                "required": ["condition", "severity"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "apply_diagnostic_criteria":
            return await self._apply_criteria(tool_input)
        if tool_name == "specialist_knowledge_lookup":
            return await self._knowledge_lookup(tool_input)
        if tool_name == "assess_prognosis":
            return await self._assess_prognosis(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ------------------------------------------------------------------
    # Diagnostic criteria database
    # ------------------------------------------------------------------

    def _get_criteria_db(self) -> dict:
        return {
            # ============================================================
            # CARDIOLOGY
            # ============================================================
            "heart score": {
                "full_name": "HEART Score for Major Cardiac Events",
                "specialty": "cardiology",
                "components": {
                    "history": {
                        "description": "Degree of suspicion based on history",
                        "scoring": {"slightly suspicious": 0, "moderately suspicious": 1, "highly suspicious": 2},
                    },
                    "ecg": {
                        "description": "ECG findings",
                        "scoring": {"normal": 0, "non-specific repolarization disturbance": 1, "significant ST deviation": 2},
                    },
                    "age": {
                        "description": "Patient age",
                        "scoring": {"<45": 0, "45-64": 1, ">=65": 2},
                    },
                    "risk_factors": {
                        "description": "Number of risk factors (HTN, DM, hyperlipidemia, obesity, smoking, family hx, atherosclerotic disease)",
                        "scoring": {"0-1 factors": 0, "2 factors": 1, ">=3 factors or history of atherosclerotic disease": 2},
                    },
                    "troponin": {
                        "description": "Initial troponin level",
                        "scoring": {"<=normal limit": 0, "1-3x normal limit": 1, ">3x normal limit": 2},
                    },
                },
                "total_range": "0-10",
                "interpretation": {
                    "0-3": {"risk_level": "Low", "mace_risk": "0.9-1.7%", "action": "Consider early discharge with outpatient follow-up. Repeat troponin if borderline."},
                    "4-6": {"risk_level": "Moderate", "mace_risk": "12-16.6%", "action": "Admit for observation, serial troponins, non-invasive testing. Cardiology consultation."},
                    "7-10": {"risk_level": "High", "mace_risk": "50-65%", "action": "Urgent invasive strategy. Immediate cardiology consultation. Consider early catheterization."},
                },
            },
            "timi risk score": {
                "full_name": "TIMI Risk Score for UA/NSTEMI",
                "specialty": "cardiology",
                "components": {
                    "age_ge_65": {"description": "Age >= 65 years", "points": 1},
                    "cad_risk_factors_ge_3": {"description": ">=3 CAD risk factors (family hx, HTN, DM, hyperlipidemia, current smoker)", "points": 1},
                    "known_cad_ge_50_stenosis": {"description": "Known CAD (>=50% stenosis)", "points": 1},
                    "asa_use_past_7_days": {"description": "ASA use in past 7 days", "points": 1},
                    "severe_angina_ge_2_episodes_24h": {"description": "Severe angina (>=2 episodes in 24h)", "points": 1},
                    "st_deviation_ge_0_5mm": {"description": "ST deviation >=0.5mm", "points": 1},
                    "positive_cardiac_marker": {"description": "Positive cardiac marker (troponin)", "points": 1},
                },
                "total_range": "0-7",
                "interpretation": {
                    "0-2": {"risk_level": "Low", "14_day_event_rate": "4.7-8.3%", "action": "Consider non-invasive evaluation. Outpatient stress testing may be appropriate."},
                    "3-4": {"risk_level": "Intermediate", "14_day_event_rate": "13.2-19.9%", "action": "Admit, serial biomarkers, early non-invasive or invasive evaluation."},
                    "5-7": {"risk_level": "High", "14_day_event_rate": "26.2-40.9%", "action": "Early invasive strategy recommended. Dual antiplatelet therapy, anticoagulation."},
                },
            },
            "cha2ds2-vasc": {
                "full_name": "CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk",
                "specialty": "cardiology",
                "components": {
                    "chf": {"description": "Congestive Heart Failure", "points": 1},
                    "hypertension": {"description": "Hypertension", "points": 1},
                    "age_ge_75": {"description": "Age >= 75 years", "points": 2},
                    "diabetes": {"description": "Diabetes mellitus", "points": 1},
                    "stroke_tia_thromboembolism": {"description": "Prior Stroke/TIA/Thromboembolism", "points": 2},
                    "vascular_disease": {"description": "Vascular disease (prior MI, PAD, aortic plaque)", "points": 1},
                    "age_65_74": {"description": "Age 65-74 years", "points": 1},
                    "sex_female": {"description": "Female sex", "points": 1},
                },
                "total_range": "0-9",
                "interpretation": {
                    "0": {"risk_level": "Low", "annual_stroke_risk": "0%", "action": "No antithrombotic therapy needed (male). Female sex as lone factor also low risk."},
                    "1": {"risk_level": "Low-Moderate", "annual_stroke_risk": "1.3%", "action": "Consider oral anticoagulation vs antiplatelet vs no therapy. Shared decision-making."},
                    "2": {"risk_level": "Moderate", "annual_stroke_risk": "2.2%", "action": "Oral anticoagulation recommended (DOAC preferred over warfarin unless mechanical valve or moderate-severe mitral stenosis)."},
                    "3-9": {"risk_level": "High", "annual_stroke_risk": "3.2-15.2%", "action": "Oral anticoagulation strongly recommended. DOAC preferred. Assess bleeding risk with HAS-BLED."},
                },
            },
            "has-bled": {
                "full_name": "HAS-BLED Score for Major Bleeding Risk",
                "specialty": "cardiology",
                "components": {
                    "hypertension_uncontrolled": {"description": "Hypertension (uncontrolled, SBP>160)", "points": 1},
                    "abnormal_renal_liver": {"description": "Abnormal renal AND/OR liver function (1 point each, max 2)", "points": "1-2"},
                    "stroke": {"description": "Prior stroke", "points": 1},
                    "bleeding_hx": {"description": "Bleeding history or predisposition", "points": 1},
                    "labile_inr": {"description": "Labile INR (if on warfarin, TTR <60%)", "points": 1},
                    "elderly_gt_65": {"description": "Elderly (>65 years)", "points": 1},
                    "drugs_alcohol": {"description": "Drugs (antiplatelet/NSAIDs) AND/OR alcohol (1 point each, max 2)", "points": "1-2"},
                },
                "total_range": "0-9",
                "interpretation": {
                    "0-2": {"risk_level": "Low", "action": "Anticoagulation generally safe. Standard monitoring."},
                    "3": {"risk_level": "Moderate", "action": "Anticoagulation still indicated if CHA2DS2-VASc warrants. Increase monitoring frequency. Address modifiable risk factors."},
                    "4-9": {"risk_level": "High", "action": "High bleeding risk does NOT necessarily contraindicate anticoagulation. Aggressively address modifiable risk factors. Consider DOAC over warfarin. Close follow-up."},
                },
            },
            "nyha classification": {
                "full_name": "New York Heart Association Functional Classification",
                "specialty": "cardiology",
                "components": {
                    "class": {
                        "description": "Functional limitation based on symptoms",
                        "options": {
                            "I": "No limitation. Ordinary physical activity does not cause undue fatigue, palpitation, or dyspnea.",
                            "II": "Slight limitation. Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, or dyspnea.",
                            "III": "Marked limitation. Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, or dyspnea.",
                            "IV": "Unable to carry on any physical activity without discomfort. Symptoms at rest. Increased discomfort with any physical activity.",
                        },
                    },
                },
                "interpretation": {
                    "I": {"action": "Guideline-directed medical therapy. Lifestyle modification. Annual follow-up."},
                    "II": {"action": "Optimize GDMT (ACEi/ARB/ARNI, beta-blocker, MRA, SGLT2i). Consider cardiac rehab. Follow-up every 3-6 months."},
                    "III": {"action": "Maximize GDMT. Consider device therapy (ICD/CRT if indicated). Evaluate for advanced therapies. Follow-up every 1-3 months."},
                    "IV": {"action": "Hospitalization often needed. IV inotropes/diuretics. Evaluate for mechanical support (LVAD) or transplant. Palliative care discussion."},
                },
            },
            "framingham heart failure": {
                "full_name": "Framingham Criteria for Heart Failure Diagnosis",
                "specialty": "cardiology",
                "components": {
                    "major_criteria": [
                        "Paroxysmal nocturnal dyspnea or orthopnea",
                        "Neck vein distension (JVD)",
                        "Rales (crackles)",
                        "Cardiomegaly on imaging",
                        "Acute pulmonary edema",
                        "S3 gallop",
                        "Elevated central venous pressure (>16 cm H2O)",
                        "Hepatojugular reflux",
                        "Weight loss >4.5 kg in 5 days in response to treatment",
                    ],
                    "minor_criteria": [
                        "Bilateral ankle edema",
                        "Nocturnal cough",
                        "Dyspnea on ordinary exertion",
                        "Hepatomegaly",
                        "Pleural effusion",
                        "Heart rate >120 bpm",
                        "Decrease in vital capacity by 1/3 from maximum",
                    ],
                },
                "diagnosis_rule": "Heart failure diagnosis requires 2 major criteria OR 1 major + 2 minor criteria. Minor criteria accepted only if not attributable to another condition.",
                "interpretation": {
                    "criteria_met": {"action": "Diagnosis of heart failure established. Obtain BNP/NT-proBNP, echocardiogram, BMP. Classify HFrEF vs HFpEF. Initiate GDMT."},
                    "criteria_not_met": {"action": "Heart failure less likely but not excluded. Consider BNP/NT-proBNP if clinical suspicion remains. Evaluate alternative diagnoses."},
                },
            },
            "duke criteria": {
                "full_name": "Modified Duke Criteria for Infective Endocarditis",
                "specialty": "cardiology",
                "components": {
                    "major_criteria": {
                        "positive_blood_cultures": "Typical microorganisms from 2 separate cultures (viridans strep, S. bovis, HACEK, S. aureus, enterococci) OR persistently positive cultures",
                        "endocardial_involvement": "Positive echocardiogram (oscillating intracardiac mass, abscess, new prosthetic valve dehiscence) OR new valvular regurgitation",
                    },
                    "minor_criteria": [
                        "Predisposing heart condition or IVDU",
                        "Fever >=38.0C (100.4F)",
                        "Vascular phenomena (Janeway lesions, arterial emboli, mycotic aneurysm, intracranial hemorrhage, conjunctival hemorrhage)",
                        "Immunologic phenomena (Osler nodes, Roth spots, glomerulonephritis, positive rheumatoid factor)",
                        "Microbiologic evidence not meeting major criteria",
                    ],
                },
                "diagnosis_rule": "DEFINITE: 2 major, OR 1 major + 3 minor, OR 5 minor. POSSIBLE: 1 major + 1 minor, OR 3 minor.",
                "interpretation": {
                    "definite": {"action": "Start empiric antibiotics after 3 sets of blood cultures. TEE if TTE non-diagnostic. Surgical consultation. Infectious disease consultation."},
                    "possible": {"action": "Continue workup. Repeat blood cultures. TEE recommended. Infectious disease consultation."},
                    "rejected": {"action": "Alternative diagnosis likely. Consider other causes of fever + murmur."},
                },
            },

            # ============================================================
            # PULMONOLOGY
            # ============================================================
            "wells pe": {
                "full_name": "Wells Score for Pulmonary Embolism",
                "specialty": "pulmonology",
                "components": {
                    "clinical_signs_dvt": {"description": "Clinical signs/symptoms of DVT (leg swelling, pain with palpation)", "points": 3.0},
                    "pe_most_likely": {"description": "PE is #1 diagnosis OR equally likely", "points": 3.0},
                    "heart_rate_gt_100": {"description": "Heart rate >100 bpm", "points": 1.5},
                    "immobilization_surgery": {"description": "Immobilization (>=3 days) or surgery in previous 4 weeks", "points": 1.5},
                    "previous_pe_dvt": {"description": "Previous PE or DVT", "points": 1.5},
                    "hemoptysis": {"description": "Hemoptysis", "points": 1.0},
                    "malignancy": {"description": "Malignancy (treatment within 6 months or palliative)", "points": 1.0},
                },
                "total_range": "0-12.5",
                "interpretation": {
                    "0-1": {"risk_level": "Low", "pe_probability": "1.3%", "action": "Check D-dimer. If negative, PE excluded. If positive, CTPA."},
                    "2-6": {"risk_level": "Moderate", "pe_probability": "16.2%", "action": "Check D-dimer. If negative, PE excluded. If positive, CTPA. Age-adjusted D-dimer cutoff may be used (age x 10 for patients >50)."},
                    "7-12.5": {"risk_level": "High", "pe_probability": "37.5%", "action": "Proceed directly to CTPA. Do NOT rely on D-dimer to exclude. Start anticoagulation if high clinical suspicion while awaiting imaging."},
                },
            },
            "geneva score": {
                "full_name": "Revised Geneva Score for PE",
                "specialty": "pulmonology",
                "components": {
                    "age_gt_65": {"description": "Age >65 years", "points": 1},
                    "previous_pe_dvt": {"description": "Previous PE or DVT", "points": 3},
                    "surgery_fracture_1mo": {"description": "Surgery or fracture within 1 month", "points": 2},
                    "active_malignancy": {"description": "Active malignancy", "points": 2},
                    "unilateral_lower_limb_pain": {"description": "Unilateral lower limb pain", "points": 3},
                    "hemoptysis": {"description": "Hemoptysis", "points": 2},
                    "heart_rate_75_94": {"description": "Heart rate 75-94 bpm", "points": 3},
                    "heart_rate_ge_95": {"description": "Heart rate >=95 bpm", "points": 5},
                    "pain_deep_palpation_lower_limb_unilateral_edema": {"description": "Pain on lower limb deep vein palpation AND unilateral edema", "points": 4},
                },
                "total_range": "0-25",
                "interpretation": {
                    "0-3": {"risk_level": "Low", "pe_probability": "7-9%", "action": "D-dimer. If negative, PE excluded."},
                    "4-10": {"risk_level": "Intermediate", "pe_probability": "28-30%", "action": "D-dimer, then CTPA if positive."},
                    "11-25": {"risk_level": "High", "pe_probability": "64-74%", "action": "CTPA directly. Empiric anticoagulation while awaiting imaging."},
                },
            },
            "curb-65": {
                "full_name": "CURB-65 Severity Score for Community-Acquired Pneumonia",
                "specialty": "pulmonology",
                "components": {
                    "confusion": {"description": "New-onset confusion (AMT <=8 or new disorientation)", "points": 1},
                    "urea": {"description": "BUN >19 mg/dL (Urea >7 mmol/L)", "points": 1},
                    "respiratory_rate": {"description": "Respiratory rate >=30/min", "points": 1},
                    "blood_pressure": {"description": "Systolic BP <90 mmHg OR Diastolic BP <=60 mmHg", "points": 1},
                    "age": {"description": "Age >=65 years", "points": 1},
                },
                "total_range": "0-5",
                "interpretation": {
                    "0-1": {"risk_level": "Low", "30_day_mortality": "0.6-2.7%", "action": "Outpatient treatment appropriate. Oral antibiotics. Follow-up in 48-72 hours."},
                    "2": {"risk_level": "Moderate", "30_day_mortality": "6.8-9.2%", "action": "Consider short inpatient stay or closely supervised outpatient care. IV to oral antibiotic step-down."},
                    "3-5": {"risk_level": "High", "30_day_mortality": "14.5-57%", "action": "Hospitalize. Score 4-5: ICU assessment. IV antibiotics. Blood cultures, sputum culture. Consider MRSA/Pseudomonas coverage if risk factors."},
                },
            },
            "psi/port score": {
                "full_name": "Pneumonia Severity Index / PORT Score",
                "specialty": "pulmonology",
                "components": {
                    "demographics": "Age (years) for males; Age-10 for females. Nursing home resident +10",
                    "comorbidities": "Neoplastic disease +30, Liver disease +20, CHF +10, Cerebrovascular disease +10, Renal disease +10",
                    "physical_exam": "Altered mental status +20, RR>=30 +20, SBP<90 +20, Temp<35 or >=40 +15, HR>=125 +10",
                    "lab_imaging": "pH<7.35 +30, BUN>=30 +20, Na<130 +20, Glucose>=250 +10, Hct<30% +10, PaO2<60 +10, Pleural effusion +10",
                },
                "total_range": "Variable (sum of points)",
                "interpretation": {
                    "Class I (<51)": {"risk_level": "Low", "mortality": "0.1%", "action": "Outpatient care."},
                    "Class II (51-70)": {"risk_level": "Low", "mortality": "0.6%", "action": "Outpatient care."},
                    "Class III (71-90)": {"risk_level": "Moderate", "mortality": "2.8%", "action": "Brief inpatient observation or outpatient with close follow-up."},
                    "Class IV (91-130)": {"risk_level": "High", "mortality": "8.2%", "action": "Inpatient care."},
                    "Class V (>130)": {"risk_level": "Very High", "mortality": "29.2%", "action": "Inpatient, likely ICU. Assess for severe CAP criteria."},
                },
            },
            "gold copd staging": {
                "full_name": "GOLD COPD Staging and Assessment",
                "specialty": "pulmonology",
                "components": {
                    "spirometry_severity": {
                        "GOLD 1 - Mild": "FEV1 >= 80% predicted",
                        "GOLD 2 - Moderate": "50% <= FEV1 < 80% predicted",
                        "GOLD 3 - Severe": "30% <= FEV1 < 50% predicted",
                        "GOLD 4 - Very Severe": "FEV1 < 30% predicted",
                    },
                    "abcd_assessment": {
                        "description": "Based on exacerbation history and symptom burden (mMRC/CAT)",
                        "Group A": "0-1 moderate exacerbations (no hospitalization), mMRC 0-1 or CAT <10",
                        "Group B": "0-1 moderate exacerbations (no hospitalization), mMRC >=2 or CAT >=10",
                        "Group E": ">=2 moderate exacerbations OR >=1 leading to hospitalization",
                    },
                },
                "interpretation": {
                    "Group A": {"action": "Bronchodilator (SABA or LABA or LAMA). Smoking cessation. Vaccinations."},
                    "Group B": {"action": "LABA + LAMA combination. Pulmonary rehab. Smoking cessation. Vaccinations."},
                    "Group E": {"action": "LABA + LAMA. Consider LABA+LAMA+ICS if eosinophils >=300. If eosinophils <100, consider adding roflumilast or azithromycin. Pulmonary rehab."},
                },
            },
            "asthma severity": {
                "full_name": "Asthma Severity Classification (NAEPP/GINA)",
                "specialty": "pulmonology",
                "components": {
                    "intermittent": "Symptoms <=2 days/week, nighttime awakenings <=2x/month, SABA use <=2 days/week, no interference with activity, FEV1 >=80%, FEV1/FVC normal",
                    "mild_persistent": "Symptoms >2 days/week (not daily), nighttime awakenings 3-4x/month, SABA >2 days/week (not daily), minor limitation, FEV1 >=80%",
                    "moderate_persistent": "Daily symptoms, nighttime awakenings >1x/week (not nightly), daily SABA use, some limitation, FEV1 60-80%",
                    "severe_persistent": "Symptoms throughout the day, nighttime awakenings often 7x/week, SABA several times/day, extremely limited activity, FEV1 <60%",
                },
                "interpretation": {
                    "intermittent": {"action": "Step 1: SABA as needed. No daily controller."},
                    "mild_persistent": {"action": "Step 2: Low-dose ICS. Alternative: LTRA or as-needed ICS-formoterol."},
                    "moderate_persistent": {"action": "Step 3-4: Medium-dose ICS + LABA, or medium-dose ICS-formoterol (MART). Consider step-up if uncontrolled."},
                    "severe_persistent": {"action": "Step 5: High-dose ICS + LABA. Consider add-on: tiotropium, biologic therapy (anti-IgE, anti-IL5, anti-IL4R). Oral corticosteroid as last resort."},
                },
            },

            # ============================================================
            # NEUROLOGY
            # ============================================================
            "nih stroke scale": {
                "full_name": "NIH Stroke Scale (Simplified Assessment)",
                "specialty": "neurology",
                "components": {
                    "1a_level_of_consciousness": {"range": "0-3", "description": "Alert to unresponsive"},
                    "1b_loc_questions": {"range": "0-2", "description": "Answers month and age correctly"},
                    "1c_loc_commands": {"range": "0-2", "description": "Follows 2 commands (open/close eyes, grip/release)"},
                    "2_best_gaze": {"range": "0-2", "description": "Horizontal eye movement"},
                    "3_visual_fields": {"range": "0-3", "description": "Visual field testing"},
                    "4_facial_palsy": {"range": "0-3", "description": "Facial movement symmetry"},
                    "5_motor_arm": {"range": "0-4 each", "description": "Arm drift (L and R separately)"},
                    "6_motor_leg": {"range": "0-4 each", "description": "Leg drift (L and R separately)"},
                    "7_limb_ataxia": {"range": "0-2", "description": "Finger-nose and heel-shin"},
                    "8_sensory": {"range": "0-2", "description": "Pin prick sensation"},
                    "9_best_language": {"range": "0-3", "description": "Naming, reading, describing"},
                    "10_dysarthria": {"range": "0-2", "description": "Clarity of speech"},
                    "11_extinction": {"range": "0-2", "description": "Double simultaneous stimulation"},
                },
                "total_range": "0-42",
                "interpretation": {
                    "0": {"severity": "No stroke symptoms", "action": "Consider TIA workup if symptoms resolved."},
                    "1-4": {"severity": "Minor stroke", "action": "IV tPA may be considered if within window. Aspirin if tPA not given. Admit stroke unit."},
                    "5-15": {"severity": "Moderate stroke", "action": "IV tPA if within 4.5h of onset. Consider mechanical thrombectomy if LVO on imaging. Stroke unit admission."},
                    "16-20": {"severity": "Moderate-severe stroke", "action": "IV tPA + consider thrombectomy for LVO. ICU-level monitoring. Neurosurgery consult if posterior fossa."},
                    "21-42": {"severity": "Severe stroke", "action": "IV tPA + thrombectomy evaluation. ICU. Goals-of-care discussion may be appropriate. High mortality risk."},
                },
            },
            "hunt-hess": {
                "full_name": "Hunt-Hess Classification for Subarachnoid Hemorrhage",
                "specialty": "neurology",
                "components": {
                    "grade": {
                        "I": "Asymptomatic or mild headache, slight nuchal rigidity",
                        "II": "Moderate-severe headache, nuchal rigidity, no neurological deficit except cranial nerve palsy",
                        "III": "Drowsiness, confusion, mild focal deficit",
                        "IV": "Stupor, moderate-severe hemiparesis, possible early decerebrate rigidity",
                        "V": "Deep coma, decerebrate rigidity, moribund appearance",
                    },
                },
                "interpretation": {
                    "I": {"mortality": "~1%", "action": "Admit ICU. CTA/conventional angiogram. Nimodipine. Neurosurgery consultation for aneurysm repair."},
                    "II": {"mortality": "~5%", "action": "ICU. CTA/angiogram. Nimodipine. Early aneurysm securing (clip/coil). EVD if hydrocephalus."},
                    "III": {"mortality": "~19%", "action": "ICU. Secure aneurysm urgently. EVD placement. Aggressive vasospasm monitoring."},
                    "IV": {"mortality": "~42%", "action": "ICU. EVD. Consider aneurysm repair if patient stabilizes. Goals-of-care discussion."},
                    "V": {"mortality": "~77%", "action": "ICU. EVD for ICP management. Poor prognosis. Goals-of-care/palliative care discussion essential."},
                },
            },
            "glasgow coma scale": {
                "full_name": "Glasgow Coma Scale",
                "specialty": "neurology",
                "components": {
                    "eye_opening": {"spontaneous": 4, "to_voice": 3, "to_pain": 2, "none": 1},
                    "verbal_response": {"oriented": 5, "confused": 4, "inappropriate_words": 3, "incomprehensible_sounds": 2, "none": 1},
                    "motor_response": {"obeys_commands": 6, "localizes_pain": 5, "withdrawal": 4, "abnormal_flexion": 3, "extension": 2, "none": 1},
                },
                "total_range": "3-15",
                "interpretation": {
                    "13-15": {"severity": "Mild brain injury", "action": "Observation. CT head if risk factors present (anticoagulation, LOC, amnesia, dangerous mechanism). Neuro checks."},
                    "9-12": {"severity": "Moderate brain injury", "action": "CT head urgently. Admit for monitoring. Serial neuro checks. Neurosurgery consultation if intracranial pathology."},
                    "3-8": {"severity": "Severe brain injury (coma)", "action": "Intubation for airway protection. Urgent CT. Neurosurgery consultation. ICP monitoring. ICU admission."},
                },
            },
            "abcd2": {
                "full_name": "ABCD2 Score for TIA Stroke Risk",
                "specialty": "neurology",
                "components": {
                    "age": {"description": "Age >=60 years", "points": 1},
                    "blood_pressure": {"description": "SBP >=140 OR DBP >=90 at initial evaluation", "points": 1},
                    "clinical_features": {"description": "Unilateral weakness: 2 points; Speech disturbance without weakness: 1 point; Other: 0", "points": "0-2"},
                    "duration": {"description": ">=60 min: 2 points; 10-59 min: 1 point; <10 min: 0", "points": "0-2"},
                    "diabetes": {"description": "History of diabetes", "points": 1},
                },
                "total_range": "0-7",
                "interpretation": {
                    "0-3": {"risk_level": "Low", "2_day_stroke_risk": "1.0%", "action": "Outpatient workup within 48 hours may be reasonable. Carotid imaging, echocardiogram, ECG, labs."},
                    "4-5": {"risk_level": "Moderate", "2_day_stroke_risk": "4.1%", "action": "Urgent inpatient workup recommended. Carotid imaging within 24h. Start antiplatelet therapy. Consider dual antiplatelet (DAPT) x 21 days."},
                    "6-7": {"risk_level": "High", "2_day_stroke_risk": "8.1%", "action": "Admit for urgent evaluation. MRI with DWI, CTA head/neck, echocardiogram. DAPT x 21 days. Vascular surgery/IR if significant carotid stenosis."},
                },
            },

            # ============================================================
            # GASTROENTEROLOGY
            # ============================================================
            "ranson criteria": {
                "full_name": "Ranson Criteria for Acute Pancreatitis Severity",
                "specialty": "gastroenterology",
                "components": {
                    "at_admission": {
                        "age": "Age >55 years (1 point)",
                        "wbc": "WBC >16,000/mm3 (1 point)",
                        "glucose": "Blood glucose >200 mg/dL (1 point)",
                        "ldh": "LDH >350 IU/L (1 point)",
                        "ast": "AST >250 IU/L (1 point)",
                    },
                    "at_48_hours": {
                        "hct_drop": "Hematocrit drop >10% (1 point)",
                        "bun_rise": "BUN increase >5 mg/dL (1 point)",
                        "calcium": "Serum calcium <8 mg/dL (1 point)",
                        "pao2": "PaO2 <60 mmHg (1 point)",
                        "base_deficit": "Base deficit >4 mEq/L (1 point)",
                        "fluid_sequestration": "Fluid sequestration >6L (1 point)",
                    },
                },
                "total_range": "0-11",
                "interpretation": {
                    "0-2": {"risk_level": "Mild", "mortality": "~2%", "action": "Supportive care. NPO then advance diet as tolerated. IV fluids. Pain management. Monitor."},
                    "3-4": {"risk_level": "Moderate", "mortality": "~15%", "action": "ICU consideration. Aggressive IV fluids. NPO. Consider CT abdomen. Monitor for organ failure."},
                    "5-6": {"risk_level": "Severe", "mortality": "~40%", "action": "ICU admission. Aggressive resuscitation. CT abdomen. Consider ERCP if biliary etiology. GI/surgery consultation."},
                    "7-11": {"risk_level": "Critical", "mortality": "~100%", "action": "ICU. Maximal supportive care. Multi-organ failure likely. Surgical consultation if necrotizing pancreatitis."},
                },
            },
            "child-pugh": {
                "full_name": "Child-Pugh Score for Liver Disease Severity",
                "specialty": "gastroenterology",
                "components": {
                    "bilirubin": {"1_point": "<2 mg/dL", "2_points": "2-3 mg/dL", "3_points": ">3 mg/dL"},
                    "albumin": {"1_point": ">3.5 g/dL", "2_points": "2.8-3.5 g/dL", "3_points": "<2.8 g/dL"},
                    "inr": {"1_point": "<1.7", "2_points": "1.7-2.3", "3_points": ">2.3"},
                    "ascites": {"1_point": "None", "2_points": "Slight/controlled", "3_points": "Moderate-severe/refractory"},
                    "encephalopathy": {"1_point": "None", "2_points": "Grade I-II", "3_points": "Grade III-IV"},
                },
                "total_range": "5-15",
                "interpretation": {
                    "5-6 (Class A)": {"severity": "Well-compensated", "1yr_survival": "100%", "2yr_survival": "85%", "action": "Surveillance. HCC screening q6months. Variceal screening. Manage etiology. Avoid hepatotoxins."},
                    "7-9 (Class B)": {"severity": "Significant functional compromise", "1yr_survival": "80%", "2yr_survival": "60%", "action": "Refer to hepatologist. Transplant evaluation. Manage complications (ascites, encephalopathy). Adjust medications for hepatic impairment."},
                    "10-15 (Class C)": {"severity": "Decompensated", "1yr_survival": "45%", "2yr_survival": "35%", "action": "Urgent transplant evaluation. Aggressive complication management. TIPS consideration for refractory ascites/variceal bleeding. Calculate MELD for transplant listing."},
                },
            },
            "meld score": {
                "full_name": "Model for End-Stage Liver Disease (MELD) Score",
                "specialty": "gastroenterology",
                "components": {
                    "formula": "MELD = 3.78*ln(bilirubin mg/dL) + 11.2*ln(INR) + 9.57*ln(creatinine mg/dL) + 6.43",
                    "variables": ["Serum bilirubin", "INR", "Serum creatinine", "Dialysis (2x in past week)"],
                    "notes": "Minimum value for each variable is 1.0. Creatinine capped at 4.0. If dialysis 2x in past week, creatinine set to 4.0.",
                },
                "total_range": "6-40",
                "interpretation": {
                    "6-9": {"3mo_mortality": "1.9%", "action": "Outpatient management. Routine follow-up."},
                    "10-19": {"3mo_mortality": "6.0%", "action": "Close hepatology follow-up. Transplant referral if trajectory worsening."},
                    "20-29": {"3mo_mortality": "19.6%", "action": "Transplant listing. Aggressive management of complications."},
                    "30-39": {"3mo_mortality": "52.6%", "action": "High priority for transplant. ICU care often needed."},
                    ">=40": {"3mo_mortality": "71.3%", "action": "Highest urgency for transplant. Maximal medical therapy."},
                },
            },
            "rome iv ibs": {
                "full_name": "Rome IV Criteria for Irritable Bowel Syndrome",
                "specialty": "gastroenterology",
                "components": {
                    "required": "Recurrent abdominal pain, on average, at least 1 day/week in the last 3 months, associated with 2 or more of the following:",
                    "criteria": [
                        "Related to defecation",
                        "Associated with a change in frequency of stool",
                        "Associated with a change in form (appearance) of stool",
                    ],
                    "onset": "Symptoms must have started at least 6 months before diagnosis",
                },
                "subtypes": {
                    "IBS-C": "Constipation-predominant: >25% hard stools, <25% loose stools",
                    "IBS-D": "Diarrhea-predominant: >25% loose stools, <25% hard stools",
                    "IBS-M": "Mixed: >25% hard stools AND >25% loose stools",
                    "IBS-U": "Unsubtyped: meets criteria but does not fit C, D, or M",
                },
                "interpretation": {
                    "criteria_met": {"action": "Limited workup (CBC, CRP, celiac serologies, fecal calprotectin). Reassurance. Dietary modification (low FODMAP trial). Fiber supplementation. Consider antispasmodics, neuromodulators, or gut-directed psychotherapy."},
                    "alarm_features_present": {"action": "Alarm features (rectal bleeding, weight loss, anemia, family hx CRC, onset >50, nocturnal symptoms) warrant colonoscopy and additional workup before IBS diagnosis."},
                },
            },

            # ============================================================
            # RHEUMATOLOGY
            # ============================================================
            "acr/eular ra": {
                "full_name": "2010 ACR/EULAR Classification Criteria for Rheumatoid Arthritis",
                "specialty": "rheumatology",
                "components": {
                    "joint_involvement": {
                        "1 large joint": 0,
                        "2-10 large joints": 1,
                        "1-3 small joints (with or without large)": 2,
                        "4-10 small joints (with or without large)": 3,
                        ">10 joints (at least 1 small)": 5,
                    },
                    "serology": {
                        "Negative RF AND negative ACPA": 0,
                        "Low-positive RF OR low-positive ACPA": 2,
                        "High-positive RF OR high-positive ACPA": 3,
                    },
                    "acute_phase_reactants": {
                        "Normal CRP AND normal ESR": 0,
                        "Abnormal CRP OR abnormal ESR": 1,
                    },
                    "duration_of_symptoms": {
                        "<6 weeks": 0,
                        ">=6 weeks": 1,
                    },
                },
                "total_range": "0-10",
                "interpretation": {
                    ">=6": {"action": "Definite RA. Initiate DMARD therapy (methotrexate first-line). Rheumatology referral. Baseline labs, chest X-ray. Monitor disease activity with DAS28."},
                    "<6": {"action": "Does not meet criteria currently. Monitor closely. Repeat assessment in 3-6 months. Consider 'undifferentiated inflammatory arthritis' - early treatment may still be warranted."},
                },
            },
            "sle classification": {
                "full_name": "2019 ACR/EULAR SLE Classification Criteria",
                "specialty": "rheumatology",
                "components": {
                    "entry_criterion": "ANA titer >=1:80 on HEp-2 cells (REQUIRED for entry)",
                    "clinical_domains": {
                        "Constitutional": "Fever (2 points)",
                        "Hematologic": "Leukopenia (3), Thrombocytopenia (4), Autoimmune hemolysis (4)",
                        "Neuropsychiatric": "Delirium (2), Psychosis (3), Seizure (5)",
                        "Mucocutaneous": "Non-scarring alopecia (2), Oral ulcers (2), Subacute cutaneous or discoid lupus (4), Acute cutaneous lupus (6)",
                        "Serosal": "Pleural or pericardial effusion (5), Acute pericarditis (6)",
                        "Musculoskeletal": "Joint involvement (6)",
                        "Renal": "Proteinuria >0.5g/24h (4), Class II or V nephritis (8), Class III or IV nephritis (10)",
                    },
                    "immunology_domains": {
                        "Antiphospholipid": "Anti-cardiolipin OR anti-beta2GP1 OR lupus anticoagulant (2)",
                        "Complement": "Low C3 OR low C4 (3), Low C3 AND low C4 (4)",
                        "SLE-specific antibodies": "Anti-dsDNA OR anti-Smith (6)",
                    },
                },
                "interpretation": {
                    ">=10 with positive ANA": {"action": "Classified as SLE. Rheumatology referral. Assess organ involvement. Hydroxychloroquine for all. Immunosuppression based on organ involvement."},
                    "<10": {"action": "Does not meet classification criteria. Monitor. Consider incomplete lupus/UCTD. Serial monitoring of serologies and clinical features."},
                },
            },
            "gout classification": {
                "full_name": "2015 ACR/EULAR Gout Classification Criteria",
                "specialty": "rheumatology",
                "components": {
                    "sufficient_criterion": "MSU crystals identified in symptomatic joint/bursa or tophus (classifies as gout without further scoring)",
                    "clinical_domains_if_no_crystals": {
                        "pattern_of_involvement": "Ankle or midfoot (1), MTP1 involvement (2)",
                        "characteristics": "Erythema (1), Cannot bear touch/pressure (1), Great difficulty walking (1), Time to maximal pain <24h (episodes with >=2: 1 point, >=3: 2 points, >=3 typical: 3 points)",
                        "time_course": ">=2 episodes with: time to maximal pain <24h, resolution <=14 days, complete resolution between episodes",
                        "tophus": "Draining or chalk-like subcutaneous nodule (4 points)",
                        "serum_urate": "<4: -4 points, 4-<6: 0, 6-<8: 2, 8-<10: 3, >=10: 4",
                        "imaging": "Urate deposition on DECT or ultrasound double contour sign (4 points), X-ray erosion (4 points)",
                    },
                },
                "interpretation": {
                    ">=8": {"action": "Classified as gout. Acute: colchicine, NSAIDs, or corticosteroids. Chronic: consider ULT (allopurinol/febuxostat) if >=2 flares/year, tophi, or CKD. Target urate <6 mg/dL."},
                },
            },

            # ============================================================
            # PSYCHIATRY
            # ============================================================
            "phq-9": {
                "full_name": "Patient Health Questionnaire-9 (Depression Screening)",
                "specialty": "psychiatry",
                "components": {
                    "items": [
                        "Little interest or pleasure in doing things",
                        "Feeling down, depressed, or hopeless",
                        "Trouble falling/staying asleep or sleeping too much",
                        "Feeling tired or having little energy",
                        "Poor appetite or overeating",
                        "Feeling bad about yourself or that you are a failure",
                        "Trouble concentrating on things",
                        "Moving or speaking slowly / being fidgety or restless",
                        "Thoughts that you would be better off dead or hurting yourself",
                    ],
                    "scoring_per_item": "0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
                },
                "total_range": "0-27",
                "interpretation": {
                    "0-4": {"severity": "Minimal depression", "action": "No treatment needed. Supportive counseling. Re-screen if risk factors present."},
                    "5-9": {"severity": "Mild depression", "action": "Watchful waiting. Psychoeducation. Consider psychotherapy (CBT). Re-assess in 4-8 weeks."},
                    "10-14": {"severity": "Moderate depression", "action": "Psychotherapy AND/OR pharmacotherapy. SSRIs first-line. Follow-up in 2-4 weeks."},
                    "15-19": {"severity": "Moderately severe depression", "action": "Pharmacotherapy strongly recommended + psychotherapy. Active monitoring. Assess suicide risk. Follow-up in 1-2 weeks."},
                    "20-27": {"severity": "Severe depression", "action": "Immediate pharmacotherapy + psychotherapy. Psychiatric referral. Comprehensive suicide risk assessment. Consider hospitalization if safety concerns. ECT consideration for treatment-resistant cases."},
                },
                "critical_item": "Item 9 (suicidality): ANY positive response requires direct assessment of suicidal ideation, plan, intent, and means. Use Columbia Suicide Severity Rating Scale.",
            },
            "gad-7": {
                "full_name": "Generalized Anxiety Disorder 7-Item Scale",
                "specialty": "psychiatry",
                "components": {
                    "items": [
                        "Feeling nervous, anxious, or on edge",
                        "Not being able to stop or control worrying",
                        "Worrying too much about different things",
                        "Trouble relaxing",
                        "Being so restless it is hard to sit still",
                        "Becoming easily annoyed or irritable",
                        "Feeling afraid as if something awful might happen",
                    ],
                    "scoring_per_item": "0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
                },
                "total_range": "0-21",
                "interpretation": {
                    "0-4": {"severity": "Minimal anxiety", "action": "No treatment needed. Reassurance. Stress management techniques."},
                    "5-9": {"severity": "Mild anxiety", "action": "Watchful waiting. Psychoeducation. Relaxation techniques, mindfulness. Re-assess in 4-8 weeks."},
                    "10-14": {"severity": "Moderate anxiety", "action": "Psychotherapy (CBT first-line) AND/OR pharmacotherapy (SSRI/SNRI). Follow-up in 2-4 weeks."},
                    "15-21": {"severity": "Severe anxiety", "action": "Combined pharmacotherapy (SSRI/SNRI) + psychotherapy. Psychiatric referral. Rule out medical causes (thyroid, cardiac, substances). Short-term benzodiazepine only if severe/acute. Follow-up in 1-2 weeks."},
                },
            },
            "mdq": {
                "full_name": "Mood Disorder Questionnaire (Bipolar Screening)",
                "specialty": "psychiatry",
                "components": {
                    "screening_questions": [
                        "Felt so good or hyper that people said you were not your normal self",
                        "Were so irritable that you shouted or started fights",
                        "Felt much more self-confident than usual",
                        "Got much less sleep than usual and found you didn't really miss it",
                        "Were much more talkative or spoke much faster than usual",
                        "Thoughts raced through your head and you couldn't slow them down",
                        "Were so easily distracted that you had trouble concentrating",
                        "Had much more energy than usual",
                        "Were much more active or did many more things than usual",
                        "Were much more social or outgoing than usual",
                        "Were much more interested in sex than usual",
                        "Did things that were unusual for you or others might have thought were risky or foolish",
                        "Spending money got you or your family into trouble",
                    ],
                    "clustering": "Have several of these ever happened during the same period of time?",
                    "functional_impact": "How much of a problem did any of these cause? (No problem / Minor problem / Moderate problem / Serious problem)",
                },
                "interpretation": {
                    "positive_screen": ">=7 yes answers + same time period + moderate-to-serious problem. Sensitivity 73%, specificity 90%.",
                    "action_if_positive": "Does NOT confirm diagnosis. Refer for comprehensive psychiatric evaluation. Full mood history, timeline of episodes, family history. Rule out substance-induced, medical causes, ADHD overlap.",
                    "action_if_negative": "Low probability of bipolar but does not rule out. Consider if high clinical suspicion remains.",
                },
            },
            "cage": {
                "full_name": "CAGE Questionnaire (Alcohol Use Screening)",
                "specialty": "psychiatry",
                "components": {
                    "questions": {
                        "C": "Have you ever felt you should CUT down on your drinking?",
                        "A": "Have people ANNOYED you by criticizing your drinking?",
                        "G": "Have you ever felt GUILTY about your drinking?",
                        "E": "Have you ever had a drink first thing in the morning (EYE-OPENER)?",
                    },
                },
                "interpretation": {
                    "0-1": {"action": "Low risk. Brief counseling about safe drinking limits."},
                    "2-3": {"action": "High suspicion for alcohol use disorder. Further assessment with AUDIT or clinical interview. Brief intervention. Consider referral to addiction services."},
                    "4": {"action": "Strongly suggestive of alcohol dependence. Comprehensive addiction assessment. Evaluate for withdrawal risk. Referral to addiction specialist. Consider pharmacotherapy (naltrexone, acamprosate, disulfiram)."},
                },
            },
            "columbia suicide severity": {
                "full_name": "Columbia Suicide Severity Rating Scale (C-SSRS) - Screening Version",
                "specialty": "psychiatry",
                "components": {
                    "question_1": "Have you wished you were dead or wished you could go to sleep and not wake up? (Passive ideation)",
                    "question_2": "Have you actually had any thoughts of killing yourself? (Active ideation)",
                    "question_3": "Have you been thinking about how you might do this? (Method)",
                    "question_4": "Have you had these thoughts and had some intention of acting on them? (Intent)",
                    "question_5": "Have you started to work out or worked out the details of how to kill yourself and did you intend to carry out this plan? (Plan with intent)",
                    "question_6": "Have you ever done anything, started to do anything, or prepared to do anything to end your life? (Behavior/attempt)",
                },
                "interpretation": {
                    "question_1_yes": {"risk": "Low-moderate", "action": "Safety planning. Psychoeducation. Outpatient mental health referral. Means restriction counseling. Follow-up within 1 week."},
                    "question_2_yes": {"risk": "Moderate", "action": "Same-day mental health evaluation. Safety planning with family/supports. Means restriction. Consider psychiatric referral urgently."},
                    "question_3_or_4_yes": {"risk": "High", "action": "Urgent psychiatric evaluation. Do not leave patient alone. Means restriction immediately. Consider psychiatric hospitalization. Emergency hold if refusing care and imminent risk."},
                    "question_5_or_6_yes": {"risk": "Imminent", "action": "EMERGENCY. Do not leave patient alone. Call 911/988. Immediate psychiatric hospitalization. Comprehensive safety measures. 1:1 observation."},
                },
            },

            # ============================================================
            # ENDOCRINE
            # ============================================================
            "dka criteria": {
                "full_name": "Diabetic Ketoacidosis Diagnostic Criteria",
                "specialty": "endocrinology",
                "components": {
                    "blood_glucose": ">250 mg/dL (13.9 mmol/L) - though euglycemic DKA can occur with SGLT2i use",
                    "arterial_ph": {"mild": "<7.30", "moderate": "<7.20", "severe": "<7.10"},
                    "serum_bicarbonate": {"mild": "15-18 mEq/L", "moderate": "10-<15 mEq/L", "severe": "<10 mEq/L"},
                    "urine_ketones": "Positive (++ or more)",
                    "serum_ketones": "Elevated (beta-hydroxybutyrate >3.0 mmol/L)",
                    "anion_gap": ">12 mEq/L",
                    "mental_status": {"mild": "Alert", "moderate": "Alert/drowsy", "severe": "Stupor/coma"},
                },
                "interpretation": {
                    "mild": {"action": "IV fluids (NS 1-1.5L/hr initially). Insulin drip 0.1-0.14 U/kg/hr. K+ replacement if <5.3. Monitor q1-2h. May manage on regular floor with close monitoring."},
                    "moderate": {"action": "ICU admission. IV fluids aggressively. Insulin drip. Aggressive K+ monitoring and replacement. Phosphate replacement if <1.0. Identify precipitant."},
                    "severe": {"action": "ICU admission. Aggressive IV fluids. Insulin drip. Continuous cardiac monitoring. Arterial line for serial ABGs. Bicarbonate if pH <6.9. Search for precipitant (infection, MI, non-compliance)."},
                },
            },
            "burch-wartofsky thyroid storm": {
                "full_name": "Burch-Wartofsky Point Scale for Thyroid Storm",
                "specialty": "endocrinology",
                "components": {
                    "temperature": {"99-99.9F": 5, "100-100.9F": 10, "101-101.9F": 15, "102-102.9F": 20, "103-103.9F": 25, ">=104F": 30},
                    "cns_effects": {"absent": 0, "mild_agitation": 10, "delirium_psychosis_lethargy": 20, "seizure_coma": 30},
                    "gi_hepatic": {"absent": 0, "diarrhea_nausea_abdominal_pain": 10, "jaundice": 20},
                    "cardiovascular_tachycardia": {"99-109": 5, "110-119": 10, "120-129": 15, "130-139": 20, ">=140": 25},
                    "heart_failure": {"absent": 0, "mild_pedal_edema": 5, "bibasilar_rales": 10, "pulmonary_edema": 15},
                    "atrial_fibrillation": {"absent": 0, "present": 10},
                    "precipitant": {"absent": 0, "present": 10},
                },
                "total_range": "0-140+",
                "interpretation": {
                    "<25": {"action": "Thyroid storm unlikely. Manage as thyrotoxicosis."},
                    "25-44": {"action": "Impending thyroid storm. Aggressive management. Thionamides, beta-blocker, consider glucocorticoids. ICU monitoring."},
                    ">=45": {"action": "Thyroid storm. ICU admission. PTU (preferred over methimazole in storm), propranolol IV, hydrocortisone 100mg IV q8h, iodine (1h after PTU). Cooling blankets. Identify precipitant."},
                },
            },
            "adrenal crisis": {
                "full_name": "Adrenal Crisis Diagnostic Criteria",
                "specialty": "endocrinology",
                "components": {
                    "clinical_features": [
                        "Hypotension/shock (refractory to fluids and vasopressors)",
                        "Acute abdominal symptoms (pain, nausea, vomiting)",
                        "Altered mental status (confusion, lethargy, coma)",
                        "Fever (or hypothermia)",
                        "Hypoglycemia",
                        "Hyponatremia, hyperkalemia (primary AI)",
                        "History of adrenal insufficiency or chronic steroid use with abrupt discontinuation",
                    ],
                    "precipitants": [
                        "Intercurrent illness/infection",
                        "Surgery/trauma",
                        "Abrupt glucocorticoid withdrawal",
                        "Adrenal hemorrhage (Waterhouse-Friderichsen)",
                        "Pituitary apoplexy",
                    ],
                },
                "interpretation": {
                    "suspected": {"action": "DO NOT WAIT FOR LABS. Give hydrocortisone 100mg IV STAT, then 50mg IV q8h. Aggressive NS resuscitation. Dextrose for hypoglycemia. Draw cortisol and ACTH BEFORE treatment if possible but do not delay treatment."},
                },
            },

            # ============================================================
            # INFECTIOUS DISEASE
            # ============================================================
            "qsofa": {
                "full_name": "Quick Sequential Organ Failure Assessment (qSOFA)",
                "specialty": "infectious_disease",
                "components": {
                    "respiratory_rate": {"description": "Respiratory rate >=22/min", "points": 1},
                    "altered_mentation": {"description": "Altered mentation (GCS <15)", "points": 1},
                    "systolic_bp": {"description": "Systolic BP <=100 mmHg", "points": 1},
                },
                "total_range": "0-3",
                "interpretation": {
                    "0-1": {"risk_level": "Lower risk", "action": "Continue monitoring. Does not rule out sepsis. If infection suspected, continue workup and monitor for clinical deterioration."},
                    "2-3": {"risk_level": "High risk of poor outcome", "action": "Strongly consider sepsis. Obtain blood cultures, lactate, CBC, CMP. Start empiric antibiotics within 1 hour. IV fluid resuscitation (30 mL/kg crystalloid). Consider ICU admission. Calculate full SOFA score."},
                },
                "note": "qSOFA is a screening tool for POOR OUTCOMES, not a diagnostic tool for sepsis. Sepsis-3 definition requires suspected infection + SOFA score increase >=2.",
            },
            "sirs criteria": {
                "full_name": "Systemic Inflammatory Response Syndrome (SIRS) Criteria",
                "specialty": "infectious_disease",
                "components": {
                    "temperature": {"description": "Temperature >38.0C (100.4F) OR <36.0C (96.8F)", "points": 1},
                    "heart_rate": {"description": "Heart rate >90 bpm", "points": 1},
                    "respiratory_rate": {"description": "Respiratory rate >20/min OR PaCO2 <32 mmHg", "points": 1},
                    "wbc": {"description": "WBC >12,000/mm3 OR <4,000/mm3 OR >10% bands", "points": 1},
                },
                "total_range": "0-4",
                "interpretation": {
                    "0-1": {"action": "SIRS criteria not met. Continue monitoring if infection suspected."},
                    ">=2": {"action": "SIRS criteria met. If suspected infection present, this represents sepsis by older definitions. Note: SIRS is sensitive but not specific - can be triggered by pancreatitis, burns, trauma, etc. Current Sepsis-3 guidelines prefer qSOFA/SOFA for sepsis identification."},
                },
            },
            "centor score": {
                "full_name": "Modified Centor Score (McIsaac) for Streptococcal Pharyngitis",
                "specialty": "infectious_disease",
                "components": {
                    "tonsillar_exudates": {"description": "Tonsillar exudates or swelling", "points": 1},
                    "tender_anterior_cervical_lymph_nodes": {"description": "Tender anterior cervical lymphadenopathy", "points": 1},
                    "fever": {"description": "History of fever (>38C / 100.4F)", "points": 1},
                    "absence_of_cough": {"description": "Absence of cough", "points": 1},
                    "age": {"description": "Age 3-14: +1, Age 15-44: 0, Age >=45: -1", "points": "-1 to +1"},
                },
                "total_range": "-1 to 5",
                "interpretation": {
                    "-1 to 0": {"strep_probability": "1-2.5%", "action": "No testing or antibiotics needed. Symptomatic care."},
                    "1": {"strep_probability": "5-10%", "action": "No testing or antibiotics needed. Symptomatic care. Optional rapid strep if concerned."},
                    "2-3": {"strep_probability": "11-35%", "action": "Rapid strep test. Treat if positive. Backup throat culture if rapid test negative in children/adolescents."},
                    "4-5": {"strep_probability": "51-53%", "action": "Rapid strep test. Consider empiric treatment while awaiting results. Penicillin/amoxicillin first-line x 10 days."},
                },
            },
            "alvarado score": {
                "full_name": "Alvarado Score (MANTRELS) for Acute Appendicitis",
                "specialty": "infectious_disease",
                "components": {
                    "symptoms": {
                        "migration_of_pain_to_rlq": {"description": "Migration of pain to right lower quadrant", "points": 1},
                        "anorexia": {"description": "Anorexia", "points": 1},
                        "nausea_vomiting": {"description": "Nausea/vomiting", "points": 1},
                    },
                    "signs": {
                        "rlq_tenderness": {"description": "Right lower quadrant tenderness", "points": 2},
                        "rebound_pain": {"description": "Rebound pain", "points": 1},
                        "elevated_temperature": {"description": "Temperature >=37.3C (99.1F)", "points": 1},
                    },
                    "labs": {
                        "leukocytosis": {"description": "WBC >10,000/mm3", "points": 2},
                        "left_shift": {"description": "Neutrophilia (left shift)", "points": 1},
                    },
                },
                "total_range": "0-10",
                "interpretation": {
                    "0-4": {"probability": "Low", "action": "Appendicitis unlikely. Observe. Discharge with return precautions if exam benign."},
                    "5-6": {"probability": "Possible", "action": "CT abdomen/pelvis with IV contrast (or US in children/pregnant). Surgical consultation if imaging equivocal."},
                    "7-8": {"probability": "Probable", "action": "Surgical consultation. CT to confirm. Appendectomy likely indicated."},
                    "9-10": {"probability": "Very probable", "action": "Surgical consultation for appendectomy. CT for surgical planning. NPO, IV fluids, antibiotics."},
                },
            },
        }

    # ------------------------------------------------------------------
    # Specialist knowledge database
    # ------------------------------------------------------------------

    def _get_knowledge_db(self) -> dict:
        return {
            "myocardial infarction": {
                "specialty": "cardiology",
                "atypical_presentations": [
                    "Elderly: may present with dyspnea, syncope, confusion, or fatigue without chest pain (up to 40% of MI in >75yo are painless)",
                    "Women: more likely to present with nausea, vomiting, back/jaw pain, dyspnea, and fatigue; less likely to have classic substernal crushing pain",
                    "Diabetics: autonomic neuropathy may blunt chest pain; may present with unexplained hyperglycemia, fatigue, or dyspnea",
                    "Post-surgical patients: may be masked by analgesics; unexplained tachycardia or hypotension",
                    "Right ventricular MI: hypotension with clear lungs, JVD; may worsen with nitroglycerin",
                    "Posterior MI: often missed on standard ECG; look at posterior leads V7-V9; reciprocal changes in V1-V3 (tall R waves, ST depression)",
                ],
                "mimics": [
                    "Aortic dissection (tearing pain, BP differential, wide mediastinum)",
                    "Pulmonary embolism (pleuritic pain, dyspnea, tachycardia, risk factors)",
                    "Pericarditis (pleuritic, positional pain; diffuse ST elevation with PR depression)",
                    "Esophageal spasm (relieved by nitroglycerin, which can be misleading)",
                    "Costochondritis (reproducible chest wall tenderness)",
                    "Takotsubo (stress) cardiomyopathy (post-emotional stress, apical ballooning, usually post-menopausal women)",
                    "Myocarditis (young patients, post-viral, troponin elevation with normal coronaries)",
                ],
                "complications": [
                    "Hours 0-24: cardiogenic shock, ventricular arrhythmias (VT/VF), acute mitral regurgitation",
                    "Days 1-3: reinfarction, pericarditis (early), heart failure",
                    "Days 3-5: free wall rupture, VSD, papillary muscle rupture",
                    "Days 5-14: mural thrombus formation, Dressler syndrome (post-MI pericarditis)",
                    "Weeks-months: ventricular remodeling, chronic heart failure, ventricular aneurysm",
                ],
                "prognosis": {
                    "stemi": "In-hospital mortality 5-8% with primary PCI. 1-year mortality 10-12%. Better with early reperfusion.",
                    "nstemi": "In-hospital mortality 3-5%. 6-month mortality similar to STEMI. Long-term prognosis depends on extent of CAD.",
                    "poor_prognostic_factors": ["Anterior location", "Low LVEF", "Cardiogenic shock", "Advanced age", "Diabetes", "Renal insufficiency", "Delayed reperfusion"],
                },
                "workup": {
                    "first_line": ["Serial troponins (0h, 3h; or high-sensitivity 0h, 1h)", "12-lead ECG (within 10 min of arrival)", "CXR", "BMP", "CBC", "PT/INR", "BNP/NT-proBNP"],
                    "second_line": ["Echocardiogram (wall motion abnormalities)", "Repeat ECG if symptoms change", "Right-sided ECG if inferior MI"],
                    "specialist_tests": ["Coronary angiography (urgent for STEMI, early for high-risk NSTEMI)", "Cardiac MRI (myocarditis vs MI differentiation)", "CT coronary angiography (low-risk chest pain rule-out)"],
                },
            },
            "pulmonary embolism": {
                "specialty": "pulmonology",
                "atypical_presentations": [
                    "Syncope as sole presentation (massive PE with transient hemodynamic compromise)",
                    "Isolated tachycardia without dyspnea",
                    "Abdominal pain (from right heart strain/hepatic congestion)",
                    "Seizure (from cerebral hypoxia in massive PE)",
                    "Wheezing mimicking asthma exacerbation",
                    "Asymptomatic (incidental finding on CT done for other reasons)",
                    "Fever mimicking infection (low-grade fever common in PE)",
                ],
                "mimics": [
                    "Pneumonia (fever, cough, infiltrate - but PE can coexist)",
                    "Acute coronary syndrome (chest pain, troponin may be elevated in PE)",
                    "Aortic dissection (acute chest pain, hemodynamic instability)",
                    "Pneumothorax (sudden dyspnea, pleuritic pain)",
                    "Heart failure exacerbation (dyspnea, bilateral effusions)",
                    "Anxiety/panic attack (dyspnea, tachycardia - but always rule out PE first)",
                    "Pericardial tamponade (hypotension, JVD, muffled heart sounds)",
                ],
                "complications": [
                    "Acute: hemodynamic collapse, cardiac arrest, RV failure",
                    "Days 1-7: recurrent PE, hemorrhage from anticoagulation",
                    "Weeks: post-PE syndrome (persistent dyspnea, exercise intolerance)",
                    "Months-years: chronic thromboembolic pulmonary hypertension (CTEPH) in 2-4%",
                ],
                "prognosis": {
                    "massive_pe": "Mortality 25-65% without treatment. With treatment (thrombolytics/embolectomy): 15-30%.",
                    "submassive_pe": "Short-term mortality 3-15%. RV dysfunction worsens prognosis.",
                    "low_risk_pe": "Mortality <1% with adequate anticoagulation.",
                },
                "workup": {
                    "first_line": ["Wells or Geneva score", "D-dimer (if low-moderate pretest probability)", "CTPA (gold standard imaging)"],
                    "second_line": ["Echocardiogram (RV strain, McConnell sign)", "Lower extremity duplex US (DVT)", "Troponin and BNP (prognostication)"],
                    "specialist_tests": ["V/Q scan (if CT contraindicated)", "Pulmonary angiography (rarely needed)", "MRI (if CT and V/Q contraindicated)"],
                },
            },
            "stroke": {
                "specialty": "neurology",
                "atypical_presentations": [
                    "Posterior circulation: vertigo, diplopia, ataxia, nausea - often misdiagnosed as peripheral vestibular disorder",
                    "Isolated headache without focal deficits (especially in posterior fossa strokes)",
                    "Acute confusional state without motor deficit (non-dominant hemisphere or thalamic strokes)",
                    "Seizure at onset (5-10% of strokes present with seizure)",
                    "Limb-shaking TIA (mimics focal seizure, caused by hemodynamic compromise)",
                    "Young adults: consider dissection, PFO, hypercoagulable states, vasculitis",
                ],
                "mimics": [
                    "Hypoglycemia (most important to rule out immediately - check glucose!)",
                    "Todd's paralysis (post-ictal focal weakness)",
                    "Complex migraine with aura (gradual onset, marching symptoms)",
                    "Conversion disorder/functional neurological disorder",
                    "Brain tumor (usually more gradual onset)",
                    "Subdural hematoma (especially elderly on anticoagulants)",
                    "Wernicke encephalopathy (confusion, ataxia, ophthalmoplegia)",
                ],
                "complications": [
                    "Hours 0-24: hemorrhagic transformation, cerebral edema, aspiration",
                    "Days 1-3: increased ICP, herniation (large territory infarcts), DVT/PE",
                    "Days 3-7: infections (UTI, pneumonia), delirium",
                    "Weeks: depression (30-50%), spasticity, chronic pain",
                    "Months: recurrent stroke, post-stroke epilepsy (5-10%), vascular dementia",
                ],
                "prognosis": {
                    "ischemic_stroke": "30-day mortality 10-15%. 1-year mortality 20-25%. Functional outcome depends on stroke severity, location, age, and rehabilitation.",
                    "hemorrhagic_stroke": "30-day mortality 30-50%. ICH score predicts 30-day mortality.",
                },
                "workup": {
                    "first_line": ["Non-contrast CT head (rule out hemorrhage, STAT)", "Finger-stick glucose", "CBC, BMP, coagulation studies", "NIHSS scoring", "CT angiography head/neck (LVO detection)"],
                    "second_line": ["MRI with DWI (most sensitive for acute ischemia)", "CT perfusion (mismatch for thrombectomy decision)", "ECG and telemetry (atrial fibrillation)"],
                    "specialist_tests": ["MRA or CTA neck (carotid/vertebral stenosis)", "TEE (cardiac source of embolism)", "Hypercoagulability panel (young stroke)", "Cerebral angiography (vasculitis, dissection)"],
                },
            },
            "pneumonia": {
                "specialty": "pulmonology",
                "atypical_presentations": [
                    "Elderly: confusion or functional decline may be sole presentation (no fever, no cough)",
                    "Immunocompromised: may lack typical inflammatory response; subtle infiltrates",
                    "Aspiration pneumonia: indolent course, dependent lung segments",
                    "Walking pneumonia (Mycoplasma): dry cough, minimal findings on exam, younger patients",
                    "Legionella: GI symptoms, hyponatremia, liver enzyme elevation, mental status changes",
                ],
                "mimics": [
                    "Heart failure (bilateral infiltrates, but responds to diuresis)",
                    "Pulmonary embolism with infarction",
                    "Lung cancer (especially post-obstructive pneumonia)",
                    "Eosinophilic pneumonia (peripheral infiltrates, elevated eosinophils)",
                    "Cryptogenic organizing pneumonia (doesn't respond to antibiotics)",
                    "Drug-induced pneumonitis (amiodarone, methotrexate, nitrofurantoin)",
                ],
                "complications": [
                    "Days 1-3: respiratory failure requiring intubation, sepsis/septic shock",
                    "Days 3-7: parapneumonic effusion, empyema",
                    "Weeks: lung abscess, ARDS, C.diff from antibiotics",
                    "Months: organizing pneumonia, bronchiectasis (recurrent infections)",
                ],
                "prognosis": {
                    "outpatient_cap": "Mortality <1%. Most recover in 1-2 weeks.",
                    "hospitalized_cap": "Mortality 5-15%. Average hospital stay 5-7 days.",
                    "icu_cap": "Mortality 20-50%. Prolonged recovery. Consider MRSA/Pseudomonas coverage.",
                },
                "workup": {
                    "first_line": ["Chest X-ray (PA and lateral)", "CBC with differential", "BMP", "Blood cultures (if hospitalized)", "Procalcitonin"],
                    "second_line": ["Sputum culture and Gram stain", "Legionella urinary antigen", "Pneumococcal urinary antigen", "Respiratory viral panel"],
                    "specialist_tests": ["CT chest (complicated effusion, abscess, interstitial pattern)", "Bronchoscopy with BAL (immunocompromised, non-resolving)", "Thoracentesis (significant effusion)"],
                },
            },
            "depression": {
                "specialty": "psychiatry",
                "atypical_presentations": [
                    "Somatic complaints: chronic pain, headaches, GI symptoms as primary complaint",
                    "Irritability rather than sadness (especially in men and adolescents)",
                    "Cognitive complaints mimicking dementia (pseudodementia in elderly)",
                    "Alcohol/substance use increase as self-medication",
                    "Atypical depression: hypersomnia, hyperphagia, leaden paralysis, rejection sensitivity",
                    "Psychotic depression: delusions (guilt, worthlessness, nihilistic), hallucinations",
                    "Masked depression in different cultures (presenting as 'nervios', 'heart distress', etc.)",
                ],
                "mimics": [
                    "Hypothyroidism (fatigue, weight gain, cognitive slowing)",
                    "Anemia (fatigue, poor concentration)",
                    "Vitamin B12/folate deficiency",
                    "Sleep apnea (fatigue, poor concentration, mood changes)",
                    "Medication side effects (beta-blockers, corticosteroids, interferon)",
                    "Early neurodegenerative disease (apathy, withdrawal)",
                    "Bipolar disorder (must rule out before starting antidepressant monotherapy)",
                    "Substance use disorders",
                ],
                "complications": [
                    "Suicide (risk highest in first weeks of treatment or when energy returns before mood)",
                    "Functional impairment (work, relationships, self-care)",
                    "Cardiovascular disease (depression is independent risk factor)",
                    "Substance use disorders (comorbid in 30%)",
                    "Treatment-resistant depression (30% do not respond to first-line therapy)",
                ],
                "prognosis": {
                    "first_episode": "50-60% respond to first antidepressant. Remission in 30-40% with first-line treatment. Full remission goal: 6-8 weeks.",
                    "recurrent": "50% risk of recurrence after first episode. 70% after second. 90% after third. Maintenance therapy recommended after 2+ episodes.",
                },
                "workup": {
                    "first_line": ["PHQ-9 scoring", "TSH", "CBC", "BMP", "Suicide risk assessment (C-SSRS)"],
                    "second_line": ["Vitamin B12, folate", "Vitamin D", "Urine drug screen", "Sleep study if sleep disorder suspected"],
                    "specialist_tests": ["Neuropsychological testing (pseudodementia vs true dementia)", "Psychiatric evaluation (bipolar screening, personality assessment)"],
                },
            },
            "rheumatoid arthritis": {
                "specialty": "rheumatology",
                "atypical_presentations": [
                    "Palindromic rheumatism: episodic, self-limiting joint inflammation (30% progress to RA)",
                    "Seronegative RA: RF and ACPA negative (15-25% of RA patients)",
                    "Elderly-onset RA: may present more like PMR with shoulder/hip girdle involvement",
                    "RS3PE syndrome: remitting seronegative symmetrical synovitis with pitting edema",
                    "Extra-articular presentation: interstitial lung disease, rheumatoid nodules, vasculitis",
                ],
                "mimics": [
                    "Psoriatic arthritis (look for skin/nail changes, DIP involvement, dactylitis)",
                    "SLE (positive ANA, multi-system involvement, non-erosive arthritis)",
                    "Viral arthritis (parvovirus B19, hepatitis B/C, rubella - usually self-limiting)",
                    "Crystal arthropathies (gout, pseudogout - aspiration for crystals)",
                    "Osteoarthritis (DIP involvement, bony enlargement, less morning stiffness)",
                    "Reactive arthritis (post-infectious, asymmetric, lower extremity)",
                    "Fibromyalgia (diffuse pain but no synovitis on exam)",
                ],
                "complications": [
                    "Joint destruction and deformity (swan-neck, boutonniere, ulnar deviation)",
                    "Cervical spine instability (atlantoaxial subluxation)",
                    "Interstitial lung disease (especially with anti-CCP positive)",
                    "Cardiovascular disease (accelerated atherosclerosis)",
                    "Felty syndrome (RA + splenomegaly + neutropenia)",
                    "Secondary amyloidosis (long-standing uncontrolled disease)",
                    "Treatment-related: infections (immunosuppression), hepatotoxicity (methotrexate), osteoporosis (steroids)",
                ],
                "prognosis": {
                    "with_modern_treatment": "Early aggressive treatment with DMARDs can achieve remission in 40-50%. Biologic era has dramatically improved outcomes.",
                    "poor_prognostic_factors": ["High-titer RF/ACPA", "Early erosions", "Extra-articular disease", "High disease activity at presentation", "Smoking"],
                },
                "workup": {
                    "first_line": ["RF (rheumatoid factor)", "Anti-CCP/ACPA", "ESR and CRP", "CBC", "BMP", "LFTs", "Hand/feet X-rays"],
                    "second_line": ["ANA (rule out SLE)", "Hepatitis B/C serologies (before DMARD)", "Chest X-ray (baseline before methotrexate)", "Joint ultrasound (synovitis detection)"],
                    "specialist_tests": ["MRI of affected joints (early erosion detection)", "Joint aspiration (rule out crystal disease/infection)", "CT chest (ILD screening)"],
                },
            },
        }

    # ------------------------------------------------------------------
    # Prognosis database
    # ------------------------------------------------------------------

    def _get_prognosis_db(self) -> dict:
        return {
            "community-acquired pneumonia": {
                "mild": {
                    "typical_course": "Resolution of fever in 2-3 days. Cough may persist 2-4 weeks. Full recovery 1-3 weeks.",
                    "recovery_timeline": "Day 1-3: fever resolves; Day 3-7: improving energy; Week 2-4: cough resolves; Week 4-6: full activity",
                    "mortality": "<1%",
                    "factors_worsening": ["Advanced age", "COPD/asthma", "Immunosuppression", "Smoking"],
                },
                "moderate": {
                    "typical_course": "Hospital stay 3-7 days. IV antibiotics stepped down to oral. Full recovery 2-6 weeks.",
                    "recovery_timeline": "Day 1-3: IV antibiotics, monitoring; Day 3-5: step-down to oral; Day 5-7: discharge; Week 2-6: gradual recovery",
                    "mortality": "5-15%",
                    "factors_worsening": ["Multilobar disease", "Bacteremia", "Renal failure", "Sepsis", "Age >65"],
                },
                "severe": {
                    "typical_course": "ICU stay required. Mechanical ventilation may be needed. Recovery 4-12 weeks.",
                    "recovery_timeline": "Week 1-2: ICU, stabilization; Week 2-4: step-down unit; Week 4-8: inpatient rehab; Week 8-12: outpatient recovery",
                    "mortality": "20-50%",
                    "factors_worsening": ["ARDS", "Septic shock", "Multi-organ failure", "Immunocompromise", "Late presentation"],
                },
            },
            "acute myocardial infarction": {
                "mild": {
                    "typical_course": "Small NSTEMI with preserved LVEF. Hospital stay 2-4 days. Return to normal activities in 2-4 weeks.",
                    "recovery_timeline": "Day 1-3: monitoring, cath if indicated; Week 1-2: light activity; Week 2-4: cardiac rehab starts; Week 4-8: return to work",
                    "mortality": "1-3% in-hospital",
                    "factors_worsening": ["Diabetes", "Renal disease", "Recurrent ischemia"],
                },
                "moderate": {
                    "typical_course": "STEMI with successful PCI and mild LV dysfunction. Hospital stay 3-5 days.",
                    "recovery_timeline": "Day 1-3: post-PCI monitoring; Day 3-5: discharge; Week 2-4: cardiac rehab; Week 6-8: gradual return to full activity; Week 12: stress testing",
                    "mortality": "5-8% in-hospital",
                    "factors_worsening": ["Delayed reperfusion", "Anterior MI", "Multi-vessel CAD", "Reduced LVEF"],
                },
                "severe": {
                    "typical_course": "Large MI with significantly reduced LVEF or cardiogenic shock. Prolonged hospitalization.",
                    "recovery_timeline": "Week 1-2: ICU/CCU; Week 2-4: step-down; Month 1-3: intensive cardiac rehab; Month 3-6: ongoing optimization",
                    "mortality": "15-40% in-hospital (cardiogenic shock: 40-60%)",
                    "factors_worsening": ["Cardiogenic shock", "Mechanical complications", "Cardiac arrest", "Advanced age", "Renal failure"],
                },
            },
            "major depressive disorder": {
                "mild": {
                    "typical_course": "Response to treatment in 4-6 weeks. Most achieve remission with first-line therapy.",
                    "recovery_timeline": "Week 1-2: medication initiation, early side effects; Week 4-6: symptom improvement; Week 8-12: full remission; Month 6-12: maintenance",
                    "mortality": "Low direct mortality. Suicide risk requires monitoring.",
                    "factors_worsening": ["Comorbid anxiety", "Substance use", "Social isolation", "Prior episodes"],
                },
                "moderate": {
                    "typical_course": "May require medication adjustment. Combined therapy (medication + psychotherapy) most effective.",
                    "recovery_timeline": "Week 2-4: initial response; Week 6-8: dose optimization if needed; Week 8-12: significant improvement; Month 3-6: consolidation",
                    "mortality": "Suicide risk requires active monitoring especially in first 4 weeks of treatment.",
                    "factors_worsening": ["Treatment non-adherence", "Comorbid personality disorder", "Chronic medical illness", "Adverse childhood experiences"],
                },
                "severe": {
                    "typical_course": "May require multiple medication trials. Consider augmentation, ECT for treatment-resistant cases.",
                    "recovery_timeline": "Week 1-4: stabilization (may require hospitalization); Month 1-3: medication optimization; Month 3-6: gradual improvement; Month 6-12+: ongoing management",
                    "mortality": "Highest suicide risk. 15% lifetime suicide mortality in severe untreated depression.",
                    "factors_worsening": ["Psychotic features", "Prior suicide attempts", "Family history of suicide", "Treatment resistance", "Comorbid substance use"],
                },
            },
            "ischemic stroke": {
                "mild": {
                    "typical_course": "Minor deficits. Good functional recovery expected. Most return to independence.",
                    "recovery_timeline": "Day 1-3: acute monitoring; Day 3-7: early rehabilitation; Week 2-4: discharge, outpatient rehab; Month 1-3: maximal recovery",
                    "mortality": "1-3% at 30 days",
                    "factors_worsening": ["Recurrent stroke", "Atrial fibrillation not anticoagulated", "Carotid stenosis untreated"],
                },
                "moderate": {
                    "typical_course": "Moderate deficits requiring rehabilitation. Most improvement in first 3 months. Some recovery up to 12 months.",
                    "recovery_timeline": "Week 1: acute care; Week 2-4: inpatient rehabilitation; Month 1-3: intensive outpatient rehab; Month 3-12: continued improvement possible",
                    "mortality": "10-15% at 30 days",
                    "factors_worsening": ["Large territory infarct", "Hemorrhagic transformation", "Pneumonia/aspiration", "Cardiac comorbidity"],
                },
                "severe": {
                    "typical_course": "Major neurological deficits. Prolonged rehabilitation. Many have persistent disability.",
                    "recovery_timeline": "Week 1-2: ICU/acute care; Week 2-4: stabilization; Month 1-6: inpatient rehab; Month 6-12: outpatient rehab; Year 1+: plateau in recovery",
                    "mortality": "25-40% at 30 days. 50-60% at 1 year.",
                    "factors_worsening": ["NIHSS >20", "Complete MCA territory", "Age >80", "Hemorrhagic transformation", "Multi-organ failure"],
                },
            },
        }

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _apply_criteria(self, tool_input: dict) -> str:
        criteria_name = tool_input.get("criteria_name", "").lower()
        patient = tool_input.get("patient_data", {})

        criteria_db = self._get_criteria_db()

        # Try exact match first, then partial match
        info = criteria_db.get(criteria_name)
        if not info:
            for key, value in criteria_db.items():
                if criteria_name in key or key in criteria_name:
                    info = value
                    break

        if not info:
            return json.dumps({
                "criteria_name": criteria_name,
                "status": "not_found_in_database",
                "available_criteria": sorted(criteria_db.keys()),
                "instruction": (
                    "This specific scoring system is not in the structured database. "
                    "Apply your clinical knowledge of this criteria to the patient data. "
                    "Available criteria are listed above."
                ),
                "patient_data_provided": patient,
            })

        return json.dumps({
            "criteria": info,
            "patient_data_provided": patient,
            "instruction": (
                "Apply this scoring system to the patient data provided. "
                "Calculate the score for each component based on the patient data, "
                "sum the total, and provide the clinical interpretation and recommended action "
                "based on the interpretation thresholds above."
            ),
        })

    async def _knowledge_lookup(self, tool_input: dict) -> str:
        condition = tool_input.get("condition", "").lower()
        specialty = tool_input.get("specialty", "")
        query_type = tool_input.get("query_type", "atypical_presentations")

        knowledge_db = self._get_knowledge_db()

        # Try exact match, then partial match
        info = knowledge_db.get(condition)
        if not info:
            for key, value in knowledge_db.items():
                if condition in key or key in condition:
                    info = value
                    break

        if not info:
            return json.dumps({
                "condition": condition,
                "specialty": specialty,
                "query_type": query_type,
                "status": "not_found_in_database",
                "available_conditions": sorted(knowledge_db.keys()),
                "instruction": (
                    "This condition is not in the structured knowledge database. "
                    "Use your specialist-level clinical knowledge to provide detailed information "
                    "about this condition from the specified specialty perspective, focusing on the "
                    "requested query type."
                ),
            })

        # Return the specific query type requested
        result = {
            "condition": condition,
            "specialty": specialty,
            "query_type": query_type,
        }

        if query_type in info:
            result["data"] = info[query_type]
        elif query_type == "workup" and "workup" in info:
            result["data"] = info["workup"]
        else:
            result["data"] = info.get(query_type, "No specific data for this query type.")
            result["available_query_types"] = [k for k in info.keys() if k != "specialty"]

        return json.dumps(result)

    async def _assess_prognosis(self, tool_input: dict) -> str:
        condition = tool_input.get("condition", "").lower()
        severity = tool_input.get("severity", "moderate").lower()
        age = tool_input.get("patient_age")
        comorbidities = tool_input.get("comorbidities", [])

        prognosis_db = self._get_prognosis_db()

        # Try exact and partial match
        info = prognosis_db.get(condition)
        if not info:
            for key, value in prognosis_db.items():
                if condition in key or key in condition:
                    info = value
                    break

        if not info:
            return json.dumps({
                "condition": condition,
                "severity": severity,
                "status": "not_found_in_database",
                "available_conditions": sorted(prognosis_db.keys()),
                "instruction": (
                    "This condition is not in the structured prognosis database. "
                    "Use your clinical knowledge to provide evidence-based prognostic assessment "
                    "including typical disease course, recovery timeline, mortality data, and "
                    "factors affecting prognosis."
                ),
                "patient_context": {
                    "age": age,
                    "comorbidities": comorbidities,
                },
            })

        severity_data = info.get(severity, info.get("moderate", {}))

        # Add age and comorbidity modifiers
        age_modifier = None
        if age:
            if age > 80:
                age_modifier = "Advanced age (>80) significantly worsens prognosis for most conditions. Higher complication rates, slower recovery, increased mortality."
            elif age > 65:
                age_modifier = "Elderly patient (>65). Prognosis moderately affected by age. Consider functional status and frailty."
            elif age < 18:
                age_modifier = "Pediatric patient. Prognosis may differ from adult data. Generally better recovery potential but disease-specific considerations apply."

        comorbidity_impact = []
        high_risk_comorbidities = {
            "diabetes": "Impairs healing, increases infection risk, may mask symptoms",
            "ckd": "Limits medication options, increases complications, worsens prognosis",
            "copd": "Reduces respiratory reserve, increases pneumonia/respiratory failure risk",
            "heart failure": "Limits hemodynamic reserve, fluid management challenges",
            "immunosuppression": "Increases infection risk, may alter disease course",
            "cancer": "Affects prognosis through multiple mechanisms, treatment interactions",
            "obesity": "Increases surgical risk, DVT risk, respiratory complications",
            "liver disease": "Affects drug metabolism, coagulation, increases infection risk",
        }

        for comorbidity in comorbidities:
            for key, impact in high_risk_comorbidities.items():
                if key in comorbidity.lower():
                    comorbidity_impact.append({"comorbidity": comorbidity, "impact": impact})

        return json.dumps({
            "condition": condition,
            "severity": severity,
            "prognosis_data": severity_data,
            "age_modifier": age_modifier,
            "comorbidity_impact": comorbidity_impact if comorbidity_impact else "No specific high-risk comorbidity modifiers identified.",
            "patient_context": {"age": age, "comorbidities": comorbidities},
        })
