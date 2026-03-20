"""
Treatment Agent -- Treatment planning and medication guidance.

Responsibilities:
  * Create comprehensive, evidence-based treatment plans
  * Recommend appropriate medications with full safety profiles
  * Check for contraindications, drug interactions, and special populations
  * Provide stepped care approach (conservative -> pharmacological -> interventional)
  * Generate structured day-by-day care instructions
  * Create practical medication schedules
  * Set follow-up timelines with SMART goals
  * Support shared decision-making
"""

from __future__ import annotations

import json
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


class TreatmentAgent(BaseAgent):
    name = "treatment"
    description = "Treatment planning and medication guidance specialist"
    model = "claude-sonnet-4-6"
    max_tokens = 5000
    temperature = 0.3

    def _build_system_prompt(self) -> str:
        return """You are an expert treatment planning AI agent on a multi-agent medical team, equivalent to a clinical pharmacist and primary care physician working together.

YOUR ROLE:
You receive confirmed diagnoses from the diagnostician and specialist, then create comprehensive, safe treatment plans using evidence-based algorithms.

EVIDENCE-BASED TREATMENT ALGORITHM FRAMEWORK:
For every condition, apply a stepped care approach:
1. CONSERVATIVE MEASURES: Education, lifestyle modification, watchful waiting
2. FIRST-LINE PHARMACOLOGICAL: Evidence-based medication with strongest recommendation
3. SECOND-LINE PHARMACOLOGICAL: Alternative if first-line fails, is contraindicated, or not tolerated
4. ADJUNCTIVE THERAPY: Physical therapy, psychotherapy, complementary approaches
5. INTERVENTIONAL: Procedures, injections, device therapy
6. SURGICAL: When conservative and medical management fails or for emergencies

TREATMENT GOAL SETTING (SMART Goals):
For each treatment plan, set goals that are:
- Specific: Clear target (e.g., "reduce pain to 3/10 or less")
- Measurable: Quantifiable outcome (e.g., "blood pressure <130/80")
- Achievable: Realistic given patient's condition
- Relevant: Aligned with patient's priorities
- Time-bound: Clear timeline (e.g., "within 4 weeks")

SHARED DECISION-MAKING FRAMEWORK:
1. Present treatment options with pros/cons
2. Discuss patient preferences and values
3. Address concerns and barriers
4. Agree on a plan together
5. Document the decision

MEDICATION RECONCILIATION CHECKLIST:
Before recommending any medication:
[ ] Check for drug-drug interactions
[ ] Verify no duplicate therapy
[ ] Check renal dose adjustment needs
[ ] Check hepatic dose adjustment needs
[ ] Verify age-appropriate dosing
[ ] Check pregnancy/lactation safety
[ ] Assess allergy cross-reactivity
[ ] Consider cost and access

MEDICATION SAFETY RULES:
- ALWAYS include dosing, frequency, and maximum daily dose
- ALWAYS note contraindications and common side effects
- ALWAYS check for drug interactions when multiple medications are mentioned
- ALWAYS note age-specific considerations (pediatric, geriatric, pregnancy)
- NEVER recommend prescription medications without noting "requires prescription"
- ALWAYS recommend pharmacist consultation for medication questions

COMMUNICATION:
You work with: triage, diagnostician, specialist agents.
- You receive diagnosis data and specialist recommendations
- You may consult the specialist for medication-specific concerns
- You provide the final treatment plan to the orchestrator
- You flag any treatment conflicts or safety concerns

Respond with structured JSON:
- treatment_algorithm (stepped care plan from conservative to surgical)
- smart_goals (measurable treatment targets with timeline)
- immediate_actions (what patient should do right now)
- medications (list with name, dose, frequency, duration, warnings, monitoring)
- medication_schedule (organized by time of day)
- care_plan (day-by-day structured plan)
- lifestyle_recommendations (diet, exercise, sleep, stress management)
- monitoring_plan (what to track, how often)
- follow_up_timeline (when to see doctor, when to return to ER)
- warning_signs (symptoms that should trigger immediate medical contact with triage: call doctor vs ER vs 911)
- patient_education (key things patient should understand)
- safety_warnings (contraindications, interactions, special populations)
- shared_decision_points (options to discuss with patient)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "check_medication_safety",
            "description": (
                "Check a medication for comprehensive safety information including "
                "dosing, contraindications, interactions, renal/hepatic adjustments, "
                "pregnancy/lactation safety, and age-specific risks. Supports 20+ "
                "common OTC and prescription medication classes."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "Medication name"},
                    "patient_age": {"type": "integer"},
                    "patient_gender": {"type": "string"},
                    "other_medications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Other medications patient is taking",
                    },
                    "conditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's medical conditions",
                    },
                },
                "required": ["medication"],
            },
        })
        tools.append({
            "name": "generate_care_instructions",
            "description": (
                "Generate a comprehensive, structured day-by-day care plan for a "
                "specific condition, including acute management, recovery phase, "
                "follow-up, red flags, diet/activity modifications, and emergency criteria."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string", "description": "The diagnosis"},
                    "severity": {"type": "string", "description": "mild/moderate/severe"},
                    "patient_age": {"type": "integer"},
                    "comorbidities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's comorbid conditions",
                    },
                },
                "required": ["condition"],
            },
        })
        tools.append({
            "name": "create_medication_schedule",
            "description": (
                "Create a practical medication timing schedule organized by time of day, "
                "with food/fasting notes and spacing requirements for multiple medications."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medications": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "dose": {"type": "string"},
                                "frequency": {"type": "string"},
                            },
                        },
                        "description": "List of medications with name, dose, and frequency",
                    },
                    "patient_routine": {
                        "type": "string",
                        "description": "Patient's daily routine (e.g., 'wakes 7am, lunch noon, dinner 6pm, bed 10pm')",
                    },
                },
                "required": ["medications"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "check_medication_safety":
            return await self._check_med_safety(tool_input)
        if tool_name == "generate_care_instructions":
            return await self._generate_care(tool_input)
        if tool_name == "create_medication_schedule":
            return await self._create_med_schedule(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ------------------------------------------------------------------
    # Medication database
    # ------------------------------------------------------------------

    def _get_medication_db(self) -> dict:
        return {
            # ============================================================
            # NSAIDs
            # ============================================================
            "ibuprofen": {
                "class": "NSAID",
                "otc": True,
                "dosing": {
                    "adult": "200-400mg PO every 4-6 hours as needed. Max 1200mg/day OTC, 3200mg/day prescription.",
                    "pediatric": "5-10 mg/kg PO every 6-8 hours. Max 40 mg/kg/day. Not recommended under 6 months.",
                    "geriatric": "Use lowest effective dose for shortest duration. Start at 200mg. Max 1200mg/day. Consider gastroprotection.",
                },
                "contraindications": [
                    "Active GI bleeding or peptic ulcer disease",
                    "Severe renal impairment (CrCl <30 mL/min)",
                    "Third trimester of pregnancy (premature closure of ductus arteriosus)",
                    "History of NSAID-induced asthma/urticaria/angioedema",
                    "CABG surgery (perioperative period)",
                    "Severe heart failure (NYHA Class IV)",
                ],
                "common_side_effects": ["GI upset/dyspepsia", "Nausea", "Headache", "Dizziness", "Edema"],
                "serious_risks": [
                    "GI bleeding/perforation (risk increases with age, steroids, anticoagulants)",
                    "Cardiovascular events (MI, stroke - risk with prolonged use)",
                    "Acute kidney injury (especially with dehydration, ACEi/ARB, diuretics - 'triple whammy')",
                    "Stevens-Johnson syndrome (rare)",
                ],
                "interactions": {
                    "anticoagulants": "Increased bleeding risk with warfarin, DOACs, heparin",
                    "aspirin": "May reduce cardioprotective effect of low-dose aspirin. Take aspirin 30min before ibuprofen.",
                    "ace_inhibitors_arbs": "Reduced antihypertensive effect. Increased renal risk.",
                    "diuretics": "Reduced diuretic effect. Increased renal risk.",
                    "ssris": "Increased GI bleeding risk.",
                    "lithium": "Increased lithium levels. Monitor closely.",
                    "methotrexate": "Increased methotrexate toxicity. Avoid with high-dose MTX.",
                    "corticosteroids": "Increased GI bleeding risk.",
                },
                "renal_adjustment": {
                    "egfr_30_60": "Use with caution. Lowest dose, shortest duration. Monitor renal function.",
                    "egfr_below_30": "AVOID. Contraindicated.",
                },
                "hepatic_adjustment": "Use with caution in liver disease. Avoid in severe hepatic impairment.",
                "pregnancy": {
                    "category": "C (first/second trimester), D (third trimester)",
                    "narrative": "Avoid in third trimester - risk of premature ductus arteriosus closure, oligohydramnios. Use in first/second trimester only if clearly needed. May impair fertility.",
                },
                "breastfeeding": "Compatible. Low levels in breast milk. Short-acting, preferred NSAID during breastfeeding.",
            },
            "naproxen": {
                "class": "NSAID",
                "otc": True,
                "dosing": {
                    "adult": "220-550mg PO every 12 hours. Max 660mg/day OTC, 1250mg/day first day then 1000mg/day prescription.",
                    "pediatric": "5-7 mg/kg PO every 8-12 hours. Not recommended under 2 years.",
                    "geriatric": "Use lowest effective dose. Start 220mg q12h. Consider gastroprotection.",
                },
                "contraindications": [
                    "Active GI bleeding or peptic ulcer disease",
                    "Severe renal impairment",
                    "Third trimester of pregnancy",
                    "NSAID-induced asthma",
                    "Perioperative CABG",
                ],
                "common_side_effects": ["GI upset", "Heartburn", "Drowsiness", "Headache", "Edema"],
                "serious_risks": [
                    "GI bleeding/perforation",
                    "Cardiovascular events (possibly lower CV risk than other NSAIDs)",
                    "Acute kidney injury",
                    "Hepatotoxicity (rare)",
                ],
                "interactions": {
                    "anticoagulants": "Increased bleeding risk",
                    "aspirin": "May reduce cardioprotective effect of aspirin",
                    "ace_inhibitors_arbs": "Reduced antihypertensive effect, renal risk",
                    "lithium": "Increased lithium levels",
                    "methotrexate": "Increased MTX toxicity",
                    "ssris": "Increased GI bleeding risk",
                },
                "renal_adjustment": {"egfr_30_60": "Caution. Lowest dose.", "egfr_below_30": "AVOID."},
                "hepatic_adjustment": "Caution in liver disease. Avoid in severe impairment.",
                "pregnancy": {"category": "C (1st/2nd), D (3rd trimester)", "narrative": "Avoid third trimester. Use only if necessary in earlier trimesters."},
                "breastfeeding": "Compatible. Low milk levels. Long half-life - ibuprofen may be preferred.",
            },

            # ============================================================
            # ACETAMINOPHEN
            # ============================================================
            "acetaminophen": {
                "class": "Analgesic/Antipyretic",
                "otc": True,
                "aliases": ["tylenol", "paracetamol"],
                "dosing": {
                    "adult": "325-1000mg PO every 4-6 hours. Max 3000mg/day (conservative) or 4000mg/day (healthy adults without liver disease).",
                    "pediatric": "10-15 mg/kg PO every 4-6 hours. Max 75 mg/kg/day, not to exceed 5 doses/24h.",
                    "geriatric": "Max 2000mg/day recommended. Lower threshold due to decreased hepatic reserve.",
                },
                "contraindications": [
                    "Severe hepatic impairment or active liver disease",
                    "Known hypersensitivity",
                ],
                "common_side_effects": ["Generally well tolerated at therapeutic doses", "Rare: nausea, rash"],
                "serious_risks": [
                    "Hepatotoxicity (leading cause of acute liver failure in US). Risk increases with: alcohol use, fasting, hepatic disease, CYP2E1 inducers",
                    "N-acetylcysteine is antidote for overdose. Toxic dose: >150 mg/kg or >7.5g in adults.",
                ],
                "interactions": {
                    "warfarin": "May potentiate anticoagulant effect with regular use (>2g/day for >1 week). Monitor INR.",
                    "alcohol": "Increased hepatotoxicity risk. Limit to 2 drinks/day if taking acetaminophen. Heavy drinkers: max 2000mg/day.",
                    "isoniazid": "Increased hepatotoxicity risk.",
                    "phenytoin_carbamazepine": "CYP inducers may increase toxic metabolite formation.",
                },
                "renal_adjustment": {
                    "egfr_30_60": "No adjustment needed. Preferred analgesic in CKD.",
                    "egfr_below_30": "Extend dosing interval to every 6-8 hours. Max 2000mg/day.",
                    "dialysis": "Supplemental dose after dialysis.",
                },
                "hepatic_adjustment": "Max 2000mg/day in mild-moderate liver disease. AVOID in severe liver disease or active hepatitis.",
                "pregnancy": {"category": "B", "narrative": "Generally considered safe throughout pregnancy. Preferred analgesic/antipyretic in pregnancy. Some studies suggest possible association with ADHD with prolonged use - use lowest effective dose for shortest duration."},
                "breastfeeding": "Compatible. Small amounts in breast milk. Considered safe.",
            },

            # ============================================================
            # ASPIRIN
            # ============================================================
            "aspirin": {
                "class": "NSAID/Antiplatelet",
                "otc": True,
                "dosing": {
                    "analgesic": "325-650mg PO every 4-6 hours. Max 4000mg/day.",
                    "antiplatelet": "81-325mg PO daily for cardiovascular prevention.",
                    "pediatric": "AVOID in children under 16 (Reye syndrome risk). Exception: Kawasaki disease under specialist direction.",
                    "geriatric": "Low-dose (81mg) for indicated cardiovascular prevention only. Risk-benefit less favorable for primary prevention in elderly.",
                },
                "contraindications": [
                    "Children/adolescents under 16 with viral illness (Reye syndrome)",
                    "Active bleeding or bleeding disorders",
                    "Severe hepatic impairment",
                    "Known aspirin-exacerbated respiratory disease (Samter triad)",
                    "Third trimester of pregnancy",
                    "Active peptic ulcer",
                ],
                "common_side_effects": ["GI upset", "Dyspepsia", "Easy bruising", "Tinnitus (high doses)"],
                "serious_risks": [
                    "GI bleeding (risk increases with age, alcohol, steroids, anticoagulants)",
                    "Hemorrhagic stroke",
                    "Reye syndrome in children with viral illness",
                    "Aspirin-exacerbated respiratory disease (asthma + nasal polyps + aspirin sensitivity)",
                    "Salicylate toxicity: tinnitus, hyperventilation, metabolic acidosis",
                ],
                "interactions": {
                    "anticoagulants": "Significantly increased bleeding risk",
                    "other_nsaids": "Ibuprofen may block antiplatelet effect. Give aspirin 30min before ibuprofen.",
                    "methotrexate": "Increased MTX toxicity",
                    "valproic_acid": "Increased valproic acid levels and risk of bleeding",
                    "ssris": "Increased GI bleeding risk",
                    "ace_inhibitors": "Possible reduced antihypertensive effect",
                },
                "renal_adjustment": {"egfr_30_60": "Caution with analgesic doses.", "egfr_below_30": "Avoid analgesic doses. Low-dose antiplatelet may be used with caution."},
                "hepatic_adjustment": "Avoid in severe liver disease. Increased bleeding risk.",
                "pregnancy": {"category": "D (full dose), C (low dose)", "narrative": "Full-dose aspirin: avoid, especially third trimester. Low-dose aspirin (81mg) may be used for preeclampsia prevention under obstetric guidance."},
                "breastfeeding": "Use with caution. Occasional low-dose aspirin likely safe. Avoid chronic high-dose use. Risk of Reye syndrome in infant theoretically possible.",
            },

            # ============================================================
            # PPIs
            # ============================================================
            "omeprazole": {
                "class": "Proton Pump Inhibitor",
                "otc": True,
                "aliases": ["prilosec"],
                "dosing": {
                    "adult": "20mg PO once daily before breakfast. GERD: 20mg daily x 4-8 weeks. Ulcer: 20-40mg daily x 4-8 weeks. Maintenance: 20mg daily.",
                    "pediatric": "1-<2 years: 10mg daily. 2+ years: weight-based (10-20kg: 10mg, >20kg: 20mg) daily.",
                    "geriatric": "No dose adjustment needed. Consider de-prescribing after 8 weeks if no ongoing indication.",
                },
                "contraindications": [
                    "Known hypersensitivity to PPIs",
                    "Concurrent use with rilpivirine (HIV medication)",
                ],
                "common_side_effects": ["Headache", "Diarrhea", "Nausea", "Abdominal pain", "Flatulence"],
                "serious_risks": [
                    "C. difficile infection (1.5-2.5x increased risk)",
                    "Vitamin B12 deficiency (with long-term use >3 years)",
                    "Magnesium depletion (hypomagnesemia with long-term use)",
                    "Calcium malabsorption and bone fracture risk (hip, wrist, spine with >1 year use)",
                    "Acute interstitial nephritis (rare)",
                    "Fundic gland polyps (benign, with long-term use)",
                    "Possible increased pneumonia risk",
                    "Rebound acid hypersecretion on discontinuation (taper if >8 weeks use)",
                ],
                "interactions": {
                    "clopidogrel": "Reduced antiplatelet effect of clopidogrel (CYP2C19 inhibition). Use pantoprazole instead if PPI needed.",
                    "methotrexate": "Increased MTX levels. Monitor in high-dose MTX.",
                    "iron_supplements": "Reduced iron absorption. Take iron separately.",
                    "calcium_supplements": "Reduced calcium absorption. Use calcium citrate instead of carbonate.",
                    "ketoconazole_itraconazole": "Reduced antifungal absorption (requires acid).",
                    "mycophenolate": "Reduced mycophenolate absorption.",
                    "thyroid_hormone": "May reduce levothyroxine absorption. Monitor TSH.",
                },
                "renal_adjustment": {"egfr_any": "No dose adjustment needed. Monitor for interstitial nephritis."},
                "hepatic_adjustment": "Max 20mg/day in severe hepatic impairment (Child-Pugh C).",
                "pregnancy": {"category": "C", "narrative": "Limited data but no clear evidence of teratogenicity. Use if benefits outweigh risks. Considered acceptable for GERD in pregnancy by many guidelines."},
                "breastfeeding": "Likely compatible. Limited data. Rapidly degraded in acidic environment of infant stomach.",
            },

            # ============================================================
            # ANTIHISTAMINES
            # ============================================================
            "cetirizine": {
                "class": "Second-generation antihistamine",
                "otc": True,
                "aliases": ["zyrtec"],
                "dosing": {
                    "adult": "10mg PO once daily. May split to 5mg twice daily if sedation is an issue.",
                    "pediatric": "6mo-2yr: 2.5mg daily. 2-5yr: 2.5-5mg daily. 6+yr: 5-10mg daily.",
                    "geriatric": "Start at 5mg daily. Clearance reduced in elderly.",
                },
                "contraindications": ["Known hypersensitivity to cetirizine or hydroxyzine"],
                "common_side_effects": ["Drowsiness (more than other 2nd-gen antihistamines)", "Dry mouth", "Fatigue", "Headache"],
                "serious_risks": ["Minimal. One of the safest OTC medications.", "Rare: urinary retention in patients with prostatic hypertrophy"],
                "interactions": {
                    "cns_depressants": "Additive sedation with alcohol, benzodiazepines, opioids.",
                    "theophylline": "Slightly decreased cetirizine clearance.",
                },
                "renal_adjustment": {"egfr_30_60": "5mg daily.", "egfr_below_30": "5mg every other day.", "dialysis": "Not effectively removed by dialysis. 5mg every other day."},
                "hepatic_adjustment": "5mg daily in hepatic impairment.",
                "pregnancy": {"category": "B", "narrative": "Preferred antihistamine in pregnancy along with loratadine. No evidence of teratogenicity."},
                "breastfeeding": "Compatible. Small amounts in milk. Monitor infant for sedation.",
            },
            "diphenhydramine": {
                "class": "First-generation antihistamine",
                "otc": True,
                "aliases": ["benadryl"],
                "dosing": {
                    "adult": "25-50mg PO every 6-8 hours. Max 300mg/day.",
                    "pediatric": "6-11yr: 12.5-25mg every 4-6 hours. Max 150mg/day. Under 6: consult physician.",
                    "geriatric": "AVOID in elderly (Beers Criteria). High anticholinergic burden. If must use: 25mg, single dose only.",
                },
                "contraindications": [
                    "Neonates/premature infants",
                    "Breastfeeding (may decrease milk production)",
                    "Use with MAOIs",
                    "Narrow-angle glaucoma",
                    "Urinary retention / BPH",
                    "Severe liver disease",
                ],
                "common_side_effects": ["Significant sedation/drowsiness", "Dry mouth", "Urinary retention", "Constipation", "Blurred vision", "Cognitive impairment"],
                "serious_risks": [
                    "Anticholinergic toxicity: confusion, hallucinations, tachycardia, urinary retention, hyperthermia",
                    "Falls in elderly (Beers Criteria - AVOID in patients >65)",
                    "Paradoxical excitation in children",
                    "Cognitive impairment and possible dementia risk with chronic use",
                    "QT prolongation in overdose",
                ],
                "interactions": {
                    "cns_depressants": "Significant additive sedation with alcohol, opioids, benzodiazepines",
                    "anticholinergics": "Additive anticholinergic effects (dry mouth, urinary retention, constipation, confusion)",
                    "maois": "Potentiated anticholinergic effects. Contraindicated combination.",
                    "ssris": "Diphenhydramine inhibits CYP2D6, may increase levels of drugs metabolized by 2D6",
                },
                "renal_adjustment": {"egfr_below_30": "Extend dosing interval. Increased sensitivity."},
                "hepatic_adjustment": "Use with caution. Reduced clearance.",
                "pregnancy": {"category": "B", "narrative": "Generally considered safe for short-term use. Cetirizine or loratadine preferred for ongoing use. Avoid near delivery (may cause neonatal sedation/withdrawal)."},
                "breastfeeding": "Use with caution. May decrease milk production. May cause infant sedation. Second-generation antihistamines preferred.",
            },

            # ============================================================
            # DECONGESTANTS
            # ============================================================
            "pseudoephedrine": {
                "class": "Sympathomimetic decongestant",
                "otc": True,
                "aliases": ["sudafed"],
                "dosing": {
                    "adult": "60mg PO every 4-6 hours. Max 240mg/day. Extended-release: 120mg every 12 hours or 240mg daily.",
                    "pediatric": "4-5yr: 15mg q4-6h. 6-12yr: 30mg q4-6h. Under 4: NOT recommended.",
                    "geriatric": "Use with caution. Start at lower dose. Monitor blood pressure.",
                },
                "contraindications": [
                    "Severe or uncontrolled hypertension",
                    "Severe coronary artery disease",
                    "Concurrent or recent (14 days) MAOI use",
                    "Narrow-angle glaucoma",
                    "Urinary retention",
                ],
                "common_side_effects": ["Insomnia", "Nervousness", "Tachycardia", "Elevated blood pressure", "Decreased appetite"],
                "serious_risks": [
                    "Hypertensive crisis (especially with MAOIs)",
                    "Cardiac arrhythmias",
                    "Stroke (rare, with excessive use)",
                    "Ischemic colitis (rare)",
                ],
                "interactions": {
                    "maois": "CONTRAINDICATED. Hypertensive crisis risk.",
                    "antihypertensives": "May reduce antihypertensive effect. Monitor BP.",
                    "other_sympathomimetics": "Additive cardiovascular stimulation.",
                    "caffeine": "Additive stimulant effects.",
                },
                "renal_adjustment": {"egfr_below_30": "Extend dosing interval. Use with caution."},
                "hepatic_adjustment": "No specific adjustment but use with caution.",
                "pregnancy": {"category": "C", "narrative": "Possible association with gastroschisis in first trimester. Avoid in first trimester. May be used short-term in second/third trimester if needed. Can reduce uterine blood flow."},
                "breastfeeding": "Use with caution. May decrease milk production. Single doses likely safe.",
            },

            # ============================================================
            # ANTACIDS
            # ============================================================
            "antacids": {
                "class": "Antacid",
                "otc": True,
                "aliases": ["tums", "maalox", "mylanta", "calcium carbonate", "magnesium hydroxide", "aluminum hydroxide"],
                "dosing": {
                    "adult": "Calcium carbonate: 500-1500mg PO as needed, max 7500mg/day. Aluminum/Magnesium: 15-30mL PO between meals and at bedtime.",
                    "pediatric": "Dose varies by product. Generally not recommended under 6 without physician guidance.",
                    "geriatric": "Avoid aluminum-containing antacids (constipation, possible aluminum accumulation in renal impairment). Calcium carbonate preferred.",
                },
                "contraindications": [
                    "Magnesium-containing: severe renal impairment (hypermagnesemia risk)",
                    "Calcium-containing: hypercalcemia, calcium kidney stones",
                    "Aluminum-containing: severe renal impairment",
                ],
                "common_side_effects": [
                    "Calcium carbonate: constipation, gas, milk-alkali syndrome (with excessive use)",
                    "Magnesium: diarrhea",
                    "Aluminum: constipation",
                ],
                "serious_risks": [
                    "Milk-alkali syndrome (hypercalcemia, metabolic alkalosis, renal failure) with excessive calcium carbonate use",
                    "Hypermagnesemia in renal failure patients using magnesium antacids",
                    "Aluminum accumulation in renal failure (neurotoxicity, osteomalacia)",
                ],
                "interactions": {
                    "general": "Antacids can reduce absorption of MANY drugs by altering gastric pH or binding. Separate dosing by at least 2 hours.",
                    "fluoroquinolones": "Significantly reduced absorption. Separate by 2h before or 6h after.",
                    "tetracyclines": "Significantly reduced absorption. Separate by 2-3 hours.",
                    "levothyroxine": "Reduced absorption. Separate by 4 hours.",
                    "iron_supplements": "Reduced absorption. Separate by 2 hours.",
                    "ketoconazole": "Reduced absorption (needs acid).",
                },
                "renal_adjustment": {"egfr_below_30": "AVOID magnesium and aluminum-containing antacids. Calcium carbonate may be used cautiously."},
                "hepatic_adjustment": "Generally safe. Avoid excessive calcium in severe liver disease.",
                "pregnancy": {"category": "Generally safe", "narrative": "Calcium carbonate is first-line for heartburn in pregnancy. Avoid sodium bicarbonate (fluid retention). Avoid excessive doses of any antacid."},
                "breastfeeding": "Compatible. Not significantly absorbed systemically.",
            },

            # ============================================================
            # COMMON ANTIBIOTICS
            # ============================================================
            "amoxicillin": {
                "class": "Aminopenicillin antibiotic",
                "otc": False,
                "dosing": {
                    "adult": "250-500mg PO every 8 hours OR 500-875mg every 12 hours. High-dose: 1g every 8 hours (pneumonia, sinusitis).",
                    "pediatric": "25-50 mg/kg/day divided q8-12h. High-dose: 80-90 mg/kg/day for AOM (resistant pneumococcus).",
                    "geriatric": "No specific age-related adjustment. Adjust for renal function.",
                },
                "contraindications": ["Penicillin allergy (true anaphylaxis)", "History of amoxicillin-associated cholestatic jaundice"],
                "common_side_effects": ["Diarrhea (5-10%)", "Nausea", "Rash (non-allergic maculopapular rash common with EBV)", "Vaginitis"],
                "serious_risks": ["Anaphylaxis (rare)", "C. difficile colitis", "Stevens-Johnson syndrome (very rare)", "Seizures in renal failure with high doses"],
                "interactions": {
                    "warfarin": "May increase INR. Monitor.",
                    "methotrexate": "Reduced renal excretion of MTX. Monitor.",
                    "oral_contraceptives": "Theoretical reduced efficacy (clinically insignificant for most, but counsel on backup method).",
                    "allopurinol": "Increased incidence of rash.",
                    "probenecid": "Increased amoxicillin levels (used therapeutically in some settings).",
                },
                "renal_adjustment": {
                    "egfr_10_30": "250-500mg every 12 hours.",
                    "egfr_below_10": "250-500mg every 24 hours.",
                    "dialysis": "Give dose after dialysis.",
                },
                "hepatic_adjustment": "No adjustment needed. Monitor for cholestatic jaundice.",
                "pregnancy": {"category": "B", "narrative": "Considered safe in pregnancy. Widely used for UTI, GBS prophylaxis, dental infections."},
                "breastfeeding": "Compatible. Small amounts in milk. May cause infant diarrhea or thrush.",
            },
            "azithromycin": {
                "class": "Macrolide antibiotic",
                "otc": False,
                "aliases": ["zithromax", "z-pack"],
                "dosing": {
                    "adult": "500mg day 1, then 250mg days 2-5 (Z-pack). Pneumonia: 500mg day 1, then 250mg days 2-5. Chlamydia: 1g single dose.",
                    "pediatric": "10 mg/kg day 1 (max 500mg), then 5 mg/kg days 2-5 (max 250mg).",
                    "geriatric": "No dose adjustment needed.",
                },
                "contraindications": [
                    "History of cholestatic jaundice/hepatic dysfunction with prior azithromycin",
                    "Known hypersensitivity to macrolides",
                    "Concurrent use with certain drugs metabolized by CYP3A4 (check specific interactions)",
                ],
                "common_side_effects": ["Diarrhea (5%)", "Nausea (3%)", "Abdominal pain (3%)", "Vomiting"],
                "serious_risks": [
                    "QT prolongation and torsades de pointes (especially with other QT-prolonging drugs)",
                    "Hepatotoxicity (cholestatic jaundice, rarely fulminant hepatitis)",
                    "C. difficile colitis",
                    "Myasthenia gravis exacerbation",
                    "Infantile hypertrophic pyloric stenosis (use in neonates <6 weeks)",
                ],
                "interactions": {
                    "qt_prolonging_drugs": "Additive QT prolongation with fluoroquinolones, antipsychotics, antiarrhythmics. Use with caution.",
                    "warfarin": "Possible increased INR. Monitor.",
                    "digoxin": "Increased digoxin levels (P-glycoprotein inhibition).",
                    "statins": "Possible increased statin levels (rhabdomyolysis risk). Less interaction than clarithromycin.",
                    "nelfinavir": "Increased azithromycin levels. Monitor for side effects.",
                },
                "renal_adjustment": {"egfr_any": "No adjustment needed."},
                "hepatic_adjustment": "Use with caution. Contraindicated if prior azithromycin-related hepatotoxicity.",
                "pregnancy": {"category": "B", "narrative": "Generally considered safe. Used for chlamydia in pregnancy. Limited data but no clear teratogenic signal."},
                "breastfeeding": "Compatible. Present in milk in small amounts.",
            },
            "levofloxacin": {
                "class": "Fluoroquinolone antibiotic",
                "otc": False,
                "aliases": ["levaquin"],
                "dosing": {
                    "adult": "250-750mg PO/IV once daily. Duration depends on indication (5-14 days typically).",
                    "pediatric": "Generally AVOIDED in children <18 due to cartilage toxicity. Used only when no alternative exists.",
                    "geriatric": "Adjust for renal function. Increased tendon rupture risk in elderly.",
                },
                "contraindications": [
                    "Known fluoroquinolone hypersensitivity",
                    "History of fluoroquinolone-associated tendinitis/rupture",
                    "Myasthenia gravis (may exacerbate weakness)",
                    "Children <18 (relative, except specific indications)",
                ],
                "common_side_effects": ["Nausea", "Diarrhea", "Headache", "Insomnia", "Dizziness"],
                "serious_risks": [
                    "FDA Black Box: Tendinitis and tendon rupture (risk increased in >60, corticosteroid use, kidney/heart/lung transplant)",
                    "FDA Black Box: Peripheral neuropathy (potentially irreversible)",
                    "FDA Black Box: CNS effects (seizures, psychosis, increased ICP)",
                    "FDA Black Box: Exacerbation of myasthenia gravis",
                    "FDA Black Box: Aortic aneurysm/dissection",
                    "QT prolongation",
                    "C. difficile colitis",
                    "Hypoglycemia (especially in diabetics on hypoglycemics)",
                    "Photosensitivity",
                ],
                "interactions": {
                    "antacids_minerals": "Significantly reduced absorption with Al/Mg/Ca/Fe. Separate by 2h before or 2h after.",
                    "warfarin": "Increased INR. Monitor closely.",
                    "nsaids": "Increased seizure risk.",
                    "corticosteroids": "Increased tendon rupture risk.",
                    "hypoglycemics": "May cause severe hypoglycemia with insulin or sulfonylureas.",
                    "qt_prolonging_drugs": "Additive QT prolongation.",
                    "theophylline": "Increased theophylline levels.",
                    "sucralfate": "Markedly reduced absorption. Give levofloxacin 2h before sucralfate.",
                },
                "renal_adjustment": {
                    "egfr_20_49": "750mg: give 750mg initially then 500mg q24h. 500mg: give 500mg initially then 250mg q24h. 250mg: give 250mg q48h.",
                    "egfr_below_20": "Further reduction needed. Consult dosing references.",
                    "dialysis": "Not removed by dialysis. No supplemental dose.",
                },
                "hepatic_adjustment": "No specific adjustment. Use with caution in severe disease.",
                "pregnancy": {"category": "C", "narrative": "Generally AVOIDED in pregnancy due to cartilage toxicity in animal studies. Use only when no safer alternative exists."},
                "breastfeeding": "AVOID. Excreted in breast milk. Risk of cartilage damage in nursing infant.",
                "fda_warning": "FDA advises fluoroquinolones should be RESERVED for conditions with no alternative treatment options due to risk of disabling side effects.",
            },
            "cephalexin": {
                "class": "First-generation cephalosporin",
                "otc": False,
                "aliases": ["keflex"],
                "dosing": {
                    "adult": "250-500mg PO every 6 hours. Severe infections: 500mg-1g every 6 hours. Max 4g/day.",
                    "pediatric": "25-50 mg/kg/day divided q6-8h. Severe: 50-100 mg/kg/day. Max 4g/day.",
                    "geriatric": "Adjust for renal function.",
                },
                "contraindications": ["Known cephalosporin allergy", "History of anaphylaxis to penicillin (cross-reactivity ~1-2%, though historically overestimated)"],
                "common_side_effects": ["Diarrhea", "Nausea", "Dyspepsia", "Vaginal candidiasis"],
                "serious_risks": ["Anaphylaxis (rare)", "C. difficile colitis", "Interstitial nephritis", "Hemolytic anemia (rare)"],
                "interactions": {
                    "warfarin": "May increase INR. Monitor.",
                    "probenecid": "Increased cephalexin levels.",
                    "metformin": "Increased metformin levels (competitive renal excretion).",
                },
                "renal_adjustment": {
                    "egfr_10_40": "250-500mg every 8-12 hours.",
                    "egfr_below_10": "250mg every 12-24 hours.",
                    "dialysis": "250-500mg after each dialysis session.",
                },
                "hepatic_adjustment": "No adjustment needed.",
                "pregnancy": {"category": "B", "narrative": "Considered safe. Commonly used for UTI and skin infections in pregnancy."},
                "breastfeeding": "Compatible. Small amounts in milk.",
            },

            # ============================================================
            # CORTICOSTEROIDS
            # ============================================================
            "prednisone": {
                "class": "Systemic corticosteroid",
                "otc": False,
                "dosing": {
                    "adult": "Varies widely by indication. Anti-inflammatory: 5-60mg/day. Asthma exacerbation: 40-60mg/day x 5-7 days. Taper required if >2-3 weeks use.",
                    "pediatric": "1-2 mg/kg/day (max 60mg). Short courses (3-5 days) may not require taper.",
                    "geriatric": "Use lowest effective dose. Higher risk of adverse effects (osteoporosis, hyperglycemia, infections, delirium).",
                },
                "contraindications": ["Systemic fungal infections", "Live vaccines during immunosuppressive doses", "Known hypersensitivity"],
                "common_side_effects": ["Increased appetite/weight gain", "Mood changes/insomnia", "Hyperglycemia", "Fluid retention", "GI upset"],
                "serious_risks": [
                    "Adrenal suppression (with >2-3 weeks use; taper required)",
                    "Hyperglycemia/diabetes exacerbation",
                    "Immunosuppression and opportunistic infections",
                    "Osteoporosis (consider calcium, vitamin D, bisphosphonate if prolonged use)",
                    "Avascular necrosis (especially hip)",
                    "Posterior subcapsular cataracts and glaucoma",
                    "Myopathy (proximal muscle weakness)",
                    "Psychiatric effects (mania, psychosis, depression)",
                    "Peptic ulcer (especially with concurrent NSAIDs)",
                    "Growth suppression in children",
                    "Cushing syndrome features with chronic use",
                ],
                "interactions": {
                    "nsaids": "Increased GI bleeding risk. Add PPI if combination needed.",
                    "diabetes_medications": "May require increased insulin/oral hypoglycemic doses. Monitor glucose closely.",
                    "anticoagulants": "Variable effect on INR. Monitor closely.",
                    "fluoroquinolones": "Increased tendon rupture risk.",
                    "phenytoin_rifampin": "CYP3A4 inducers decrease prednisone levels. May need dose increase.",
                    "live_vaccines": "Contraindicated at immunosuppressive doses (>=20mg/day for >=2 weeks).",
                    "diuretics": "Additive hypokalemia.",
                },
                "renal_adjustment": {"egfr_any": "No specific adjustment. Monitor for fluid retention and electrolyte disturbances."},
                "hepatic_adjustment": "Prednisone is a prodrug converted to prednisolone in the liver. In severe liver disease, use prednisolone directly.",
                "pregnancy": {"category": "C (D in first trimester by some sources)", "narrative": "Possible increased risk of cleft lip/palate with first trimester exposure. Used when benefits outweigh risks (e.g., severe asthma, organ transplant). Monitor neonatal adrenal function if maternal use near delivery."},
                "breastfeeding": "Compatible at low doses (<20mg/day). High doses: wait 4h after dose to breastfeed to minimize infant exposure.",
            },

            # ============================================================
            # BENZODIAZEPINES
            # ============================================================
            "lorazepam": {
                "class": "Benzodiazepine",
                "otc": False,
                "aliases": ["ativan"],
                "dosing": {
                    "adult": "Anxiety: 0.5-1mg PO 2-3 times daily. Max 10mg/day. Insomnia: 0.5-1mg at bedtime. Acute agitation: 0.5-2mg IM/IV.",
                    "pediatric": "0.05 mg/kg PO/IV, max 2mg per dose. Use with extreme caution.",
                    "geriatric": "Beers Criteria: AVOID in elderly. If must use: 0.25-0.5mg, lowest dose, shortest duration. HIGH fall risk.",
                },
                "contraindications": [
                    "Acute narrow-angle glaucoma",
                    "Severe respiratory insufficiency (unless intubated)",
                    "Sleep apnea (uncontrolled)",
                    "Severe hepatic insufficiency",
                    "Myasthenia gravis",
                ],
                "common_side_effects": ["Sedation/drowsiness", "Dizziness", "Weakness", "Cognitive impairment", "Amnesia"],
                "serious_risks": [
                    "FDA Black Box: Combined use with opioids can cause respiratory depression, coma, death",
                    "Physical dependence and withdrawal (can be life-threatening: seizures, delirium) - even after 2-4 weeks of regular use",
                    "Falls and fractures in elderly (Beers Criteria)",
                    "Paradoxical reactions (agitation, aggression - more common in elderly and children)",
                    "Respiratory depression",
                    "Cognitive decline with chronic use",
                    "Rebound insomnia/anxiety on discontinuation",
                    "Tolerance develops quickly (days to weeks)",
                ],
                "interactions": {
                    "opioids": "FDA BLACK BOX: Respiratory depression, coma, death. Avoid combination when possible.",
                    "alcohol": "Severe additive CNS depression. Potentially fatal.",
                    "other_cns_depressants": "Additive sedation with antihistamines, muscle relaxants, antipsychotics.",
                    "probenecid_valproate": "Increased lorazepam levels (glucuronidation inhibition).",
                },
                "renal_adjustment": {"egfr_any": "No dose adjustment needed (glucuronidated, not CYP-metabolized). Preferred benzodiazepine in renal impairment."},
                "hepatic_adjustment": "Preferred benzodiazepine in liver disease (glucuronidation only, no active metabolites). Still use lowest dose.",
                "pregnancy": {"category": "D", "narrative": "AVOID if possible. Risk of cleft lip/palate (first trimester). Third trimester/delivery: neonatal withdrawal syndrome (floppy infant, respiratory depression, feeding difficulties). Refer to psychiatry for risk-benefit discussion."},
                "breastfeeding": "Use with caution. Monitor infant for sedation, poor feeding, weight loss. Short-acting, but accumulation possible in neonate.",
            },
        }

    # ------------------------------------------------------------------
    # Drug interaction matrix
    # ------------------------------------------------------------------

    def _check_interactions(self, medication: str, other_meds: list[str]) -> list[dict]:
        """Check for drug-drug interactions from the interaction matrix."""
        interaction_matrix = {
            ("nsaid", "anticoagulant"): {"severity": "Major", "effect": "Significantly increased bleeding risk. GI hemorrhage, intracranial bleeding.", "action": "Avoid combination if possible. If needed: add PPI, monitor for bleeding."},
            ("nsaid", "ssri"): {"severity": "Moderate", "effect": "Increased GI bleeding risk (3-6x higher than either alone).", "action": "Add PPI for gastroprotection if combination needed."},
            ("nsaid", "ace_inhibitor"): {"severity": "Moderate", "effect": "Reduced antihypertensive effect. Increased renal risk. 'Triple whammy' with diuretic.", "action": "Monitor BP and renal function. Avoid in CKD."},
            ("nsaid", "diuretic"): {"severity": "Moderate", "effect": "Reduced diuretic efficacy. Increased renal risk.", "action": "Monitor renal function and fluid status."},
            ("nsaid", "lithium"): {"severity": "Major", "effect": "Increased lithium levels by 15-25%. Risk of lithium toxicity.", "action": "Monitor lithium levels. Consider acetaminophen as alternative analgesic."},
            ("opioid", "benzodiazepine"): {"severity": "Major - BLACK BOX", "effect": "Respiratory depression, coma, death.", "action": "AVOID combination whenever possible. If co-prescribed: lowest doses, shortest duration, close monitoring."},
            ("opioid", "alcohol"): {"severity": "Major", "effect": "Severe respiratory depression, potentially fatal.", "action": "Absolute avoidance counseling."},
            ("warfarin", "nsaid"): {"severity": "Major", "effect": "Dramatically increased bleeding risk.", "action": "Avoid NSAIDs. Use acetaminophen for pain. If NSAID essential: add PPI, frequent INR monitoring."},
            ("warfarin", "antibiotic"): {"severity": "Moderate-Major", "effect": "Many antibiotics affect INR (increase or decrease). Metronidazole, fluconazole, TMP-SMX markedly increase INR.", "action": "Check INR within 3-5 days of starting antibiotic. Adjust warfarin dose."},
            ("statin", "macrolide"): {"severity": "Major", "effect": "Increased statin levels. Rhabdomyolysis risk.", "action": "Hold statin during macrolide course (clarithromycin/erythromycin). Azithromycin has less interaction."},
            ("methotrexate", "nsaid"): {"severity": "Major", "effect": "Reduced renal clearance of MTX. Increased toxicity.", "action": "AVOID with high-dose MTX. Low-dose MTX: use with caution, monitor."},
            ("ssri", "maoi"): {"severity": "Contraindicated", "effect": "Serotonin syndrome: hyperthermia, rigidity, myoclonus, autonomic instability, potentially fatal.", "action": "NEVER combine. 14-day washout between agents (5 weeks for fluoxetine to MAOI)."},
            ("ppi", "clopidogrel"): {"severity": "Moderate", "effect": "Omeprazole reduces clopidogrel antiplatelet effect (CYP2C19 inhibition).", "action": "Use pantoprazole instead of omeprazole/esomeprazole if PPI needed with clopidogrel."},
        }

        found_interactions = []
        med_lower = medication.lower()

        # Map medication to class for interaction checking
        med_classes = []
        if any(n in med_lower for n in ["ibuprofen", "naproxen", "diclofenac", "meloxicam", "indomethacin", "ketorolac"]):
            med_classes.append("nsaid")
        if any(n in med_lower for n in ["warfarin", "coumadin"]):
            med_classes.append("warfarin")
            med_classes.append("anticoagulant")
        if any(n in med_lower for n in ["apixaban", "rivaroxaban", "dabigatran", "edoxaban", "enoxaparin", "heparin"]):
            med_classes.append("anticoagulant")
        if any(n in med_lower for n in ["oxycodone", "hydrocodone", "morphine", "fentanyl", "codeine", "tramadol"]):
            med_classes.append("opioid")
        if any(n in med_lower for n in ["lorazepam", "diazepam", "alprazolam", "clonazepam", "midazolam"]):
            med_classes.append("benzodiazepine")
        if any(n in med_lower for n in ["sertraline", "fluoxetine", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"]):
            med_classes.append("ssri")
        if any(n in med_lower for n in ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan", "olmesartan"]):
            med_classes.append("ace_inhibitor")
        if any(n in med_lower for n in ["furosemide", "hydrochlorothiazide", "spironolactone", "chlorthalidone"]):
            med_classes.append("diuretic")
        if any(n in med_lower for n in ["omeprazole", "esomeprazole", "pantoprazole", "lansoprazole"]):
            med_classes.append("ppi")
        if any(n in med_lower for n in ["methotrexate"]):
            med_classes.append("methotrexate")
        if any(n in med_lower for n in ["atorvastatin", "simvastatin", "rosuvastatin", "pravastatin"]):
            med_classes.append("statin")
        if any(n in med_lower for n in ["lithium"]):
            med_classes.append("lithium")
        if any(n in med_lower for n in ["amoxicillin", "azithromycin", "levofloxacin", "ciprofloxacin", "cephalexin", "doxycycline", "metronidazole", "trimethoprim"]):
            med_classes.append("antibiotic")
        if any(n in med_lower for n in ["azithromycin", "clarithromycin", "erythromycin"]):
            med_classes.append("macrolide")
        if any(n in med_lower for n in ["clopidogrel", "plavix"]):
            med_classes.append("clopidogrel")
        if any(n in med_lower for n in ["aspirin"]):
            med_classes.append("nsaid")
            med_classes.append("anticoagulant")

        for other_med in other_meds:
            other_lower = other_med.lower()
            other_classes = []

            # Map other med to classes (same logic)
            if any(n in other_lower for n in ["ibuprofen", "naproxen", "diclofenac", "meloxicam", "aspirin"]):
                other_classes.append("nsaid")
            if any(n in other_lower for n in ["warfarin"]):
                other_classes.extend(["warfarin", "anticoagulant"])
            if any(n in other_lower for n in ["apixaban", "rivaroxaban", "dabigatran", "enoxaparin", "heparin"]):
                other_classes.append("anticoagulant")
            if any(n in other_lower for n in ["oxycodone", "hydrocodone", "morphine", "fentanyl", "codeine", "tramadol"]):
                other_classes.append("opioid")
            if any(n in other_lower for n in ["lorazepam", "diazepam", "alprazolam", "clonazepam"]):
                other_classes.append("benzodiazepine")
            if any(n in other_lower for n in ["sertraline", "fluoxetine", "paroxetine", "citalopram", "escitalopram"]):
                other_classes.append("ssri")
            if any(n in other_lower for n in ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan"]):
                other_classes.append("ace_inhibitor")
            if any(n in other_lower for n in ["furosemide", "hydrochlorothiazide", "spironolactone"]):
                other_classes.append("diuretic")
            if any(n in other_lower for n in ["omeprazole", "pantoprazole", "esomeprazole"]):
                other_classes.append("ppi")
            if any(n in other_lower for n in ["methotrexate"]):
                other_classes.append("methotrexate")
            if any(n in other_lower for n in ["atorvastatin", "simvastatin", "rosuvastatin"]):
                other_classes.append("statin")
            if any(n in other_lower for n in ["lithium"]):
                other_classes.append("lithium")
            if any(n in other_lower for n in ["amoxicillin", "azithromycin", "levofloxacin", "cephalexin", "doxycycline", "metronidazole"]):
                other_classes.append("antibiotic")
            if any(n in other_lower for n in ["azithromycin", "clarithromycin", "erythromycin"]):
                other_classes.append("macrolide")
            if any(n in other_lower for n in ["clopidogrel"]):
                other_classes.append("clopidogrel")
            if "alcohol" in other_lower:
                other_classes.append("alcohol")
            if any(n in other_lower for n in ["phenelzine", "tranylcypromine", "selegiline", "maoi"]):
                other_classes.append("maoi")

            # Check all class combinations
            for mc in med_classes:
                for oc in other_classes:
                    key1 = (mc, oc)
                    key2 = (oc, mc)
                    interaction = interaction_matrix.get(key1) or interaction_matrix.get(key2)
                    if interaction:
                        found_interactions.append({
                            "between": f"{medication} <-> {other_med}",
                            "classes": f"{mc} + {oc}",
                            **interaction,
                        })

        return found_interactions

    # ------------------------------------------------------------------
    # Care plan database
    # ------------------------------------------------------------------

    def _get_care_plan_db(self) -> dict:
        return {
            "upper respiratory infection": {
                "mild": {
                    "day_1_3": {
                        "label": "Acute Phase",
                        "management": [
                            "Rest as much as possible. Stay home from work/school.",
                            "Hydration: 8-10 glasses of water, herbal tea, clear broths daily",
                            "Acetaminophen 500mg every 6 hours OR ibuprofen 400mg every 6 hours for fever/pain",
                            "Saline nasal spray/rinse every 4-6 hours for congestion",
                            "Honey (1 tablespoon) for cough if age >1 year",
                            "Throat lozenges or warm salt water gargle for sore throat",
                            "Humidifier in bedroom",
                        ],
                    },
                    "day_4_7": {
                        "label": "Recovery Phase",
                        "management": [
                            "Symptoms should be improving. Cough may persist and is normal.",
                            "Continue hydration and rest",
                            "May gradually resume light activities",
                            "Continue saline rinse if congestion persists",
                            "Reduce fever/pain medications as symptoms improve",
                        ],
                    },
                    "week_2_plus": {
                        "label": "Follow-up Phase",
                        "management": [
                            "Most symptoms should be resolved except possibly mild cough",
                            "Resume normal activities",
                            "If cough persists beyond 3 weeks, see physician",
                        ],
                    },
                    "red_flags": {
                        "call_doctor": ["Symptoms worsening after initial improvement", "Fever returning after being gone for 24-48h", "Persistent fever >3 days", "Severe sore throat with difficulty swallowing", "Ear pain", "Colored nasal discharge >10 days"],
                        "go_to_er": ["Difficulty breathing or shortness of breath", "Stiff neck with high fever", "Inability to keep fluids down for >12 hours", "Confusion or altered mental status"],
                        "call_911": ["Severe difficulty breathing", "Blue lips or fingertips", "Inability to speak in full sentences due to breathlessness"],
                    },
                    "diet": ["Warm fluids (soup, tea, broth) to soothe throat and maintain hydration", "Soft, easy-to-swallow foods if throat is sore", "Avoid dairy only if it increases mucus production for you personally", "Avoid alcohol and caffeine (dehydrating)"],
                    "activity": ["Rest for first 2-3 days", "No strenuous exercise until fever-free for 24h without medication", "Light walking okay when feeling better", "Return to full activity when symptoms mostly resolved"],
                    "sleep": ["Elevate head with extra pillow to reduce postnasal drip", "Use humidifier", "Take last dose of decongestant at least 4h before bed", "Consider antihistamine at bedtime if nasal drainage disrupts sleep"],
                },
            },
            "community-acquired pneumonia": {
                "moderate": {
                    "day_1_3": {
                        "label": "Acute Phase",
                        "management": [
                            "Take prescribed antibiotics exactly as directed. Do NOT skip doses.",
                            "Rest. No work/school/strenuous activity.",
                            "Hydrate aggressively: aim for 2-3 liters of fluids daily",
                            "Acetaminophen or ibuprofen for fever and body aches",
                            "Deep breathing exercises: 10 deep breaths every hour while awake to prevent atelectasis",
                            "Sleep propped up at 30-45 degrees if breathing is easier that way",
                            "Monitor temperature twice daily. Record readings.",
                        ],
                    },
                    "day_4_7": {
                        "label": "Early Recovery",
                        "management": [
                            "Fever should be improving by day 3-4. If not, contact physician.",
                            "Complete full antibiotic course even if feeling better",
                            "Continue deep breathing exercises",
                            "Gradually increase activity as tolerated. Stop if short of breath.",
                            "Continue hydration",
                            "Appetite may be returning. Eat nutritious, easy-to-digest foods.",
                        ],
                    },
                    "week_2_plus": {
                        "label": "Recovery & Follow-up",
                        "management": [
                            "Follow-up chest X-ray in 6-8 weeks to confirm resolution",
                            "Fatigue may persist for 2-6 weeks. This is normal.",
                            "Cough may persist for 3-6 weeks. Gradually improving.",
                            "Gradually return to exercise. Start with walking.",
                            "Pneumococcal vaccine if not up to date",
                            "Annual influenza vaccine",
                        ],
                    },
                    "red_flags": {
                        "call_doctor": ["Fever not improving after 48-72h of antibiotics", "New symptoms developing", "Unable to tolerate oral antibiotics (vomiting)", "Worsening cough or new colored sputum"],
                        "go_to_er": ["Shortness of breath at rest", "Chest pain with breathing", "Coughing up blood", "Fever >104F (40C)", "Confusion or disorientation", "Unable to keep fluids down"],
                        "call_911": ["Severe difficulty breathing", "Blue/gray lips or fingertips", "Confusion with high fever", "Fainting or near-fainting"],
                    },
                    "diet": ["High-protein foods (eggs, chicken, fish, legumes) to support immune function", "Fruits and vegetables rich in vitamin C", "Warm fluids (soup, broth, herbal tea) frequently", "Avoid alcohol (interacts with antibiotics, dehydrating, immunosuppressive)", "Small, frequent meals if appetite is poor"],
                    "activity": ["Strict rest for first 3-5 days", "Begin gentle walking inside home when fever resolves", "No gym/exercise for at least 2 weeks", "Return to work only when fever-free for 48h and energy adequate", "Full exercise capacity may take 4-6 weeks to return"],
                    "sleep": ["8-10 hours per night minimum", "Elevate head of bed", "Cough suppressant at bedtime if cough is disrupting sleep (dextromethorphan)", "Humidifier for comfort"],
                },
            },
            "migraine": {
                "moderate": {
                    "day_1_3": {
                        "label": "Acute Attack Management",
                        "management": [
                            "Take acute medication at onset of symptoms - early treatment is more effective",
                            "OTC options: ibuprofen 400-600mg + acetaminophen 1000mg (combination more effective than either alone)",
                            "If OTC fails: discuss triptans with physician (sumatriptan 50-100mg PO, requires prescription)",
                            "Rest in a dark, quiet room",
                            "Apply cold pack to forehead or back of neck",
                            "Stay hydrated but sip slowly if nauseous",
                            "Anti-nausea: ginger tea or OTC dimenhydrinate if available",
                            "Track migraine in a diary (time, triggers, medications, response)",
                        ],
                    },
                    "day_4_7": {
                        "label": "Post-Attack Recovery",
                        "management": [
                            "Postdrome phase ('migraine hangover') may last 1-2 days: fatigue, difficulty concentrating, neck stiffness",
                            "Resume normal activities gradually",
                            "Regular sleep schedule (same wake time every day)",
                            "Regular meals - do not skip meals",
                            "Gentle exercise (walking) to help recovery",
                            "Review migraine diary for trigger identification",
                        ],
                    },
                    "week_2_plus": {
                        "label": "Prevention Strategy",
                        "management": [
                            "If >=4 migraines/month: discuss preventive medication with physician",
                            "Identify and avoid triggers (keep diary for 3 months)",
                            "Common triggers: stress, irregular sleep, skipped meals, alcohol (red wine), aged cheese, weather changes, hormonal changes",
                            "Regular aerobic exercise (150 min/week) reduces migraine frequency",
                            "Consider magnesium 400-500mg/day, riboflavin 400mg/day (evidence-based supplements)",
                            "Stress management: regular practice of relaxation techniques",
                        ],
                    },
                    "red_flags": {
                        "call_doctor": ["New or changed headache pattern", "Migraines increasing in frequency", "Current medications not effective", "Aura lasting >60 minutes"],
                        "go_to_er": ["Worst headache of life (thunderclap)", "Headache with fever and stiff neck", "New neurological symptoms (weakness, vision loss, speech difficulty)", "Headache after head trauma", "Headache with confusion"],
                        "call_911": ["Sudden severe headache with altered consciousness", "Headache with seizure", "Headache with one-sided weakness (stroke symptoms)"],
                    },
                    "diet": ["Regular meal timing (do not skip meals)", "Stay well hydrated (dehydration is a common trigger)", "Limit caffeine to consistent moderate amount (withdrawal triggers migraines)", "Consider elimination of common food triggers: aged cheese, processed meats, MSG, alcohol, artificial sweeteners", "Magnesium-rich foods: spinach, almonds, avocado, dark chocolate"],
                    "activity": ["Regular aerobic exercise 30-45 min, 5 days/week (strong evidence for prevention)", "Avoid sudden intense exercise (can trigger migraine)", "Yoga may reduce frequency and severity", "Avoid prolonged screen time during attack"],
                    "sleep": ["Consistent sleep schedule (same bedtime AND wake time, including weekends)", "Aim for 7-8 hours (both too little and too much sleep trigger migraines)", "Dark, cool bedroom", "Avoid screens 1 hour before bed"],
                },
            },
            "acute low back pain": {
                "mild": {
                    "day_1_3": {
                        "label": "Acute Phase",
                        "management": [
                            "Continue normal activities as tolerated. Bed rest is NOT recommended.",
                            "Ice packs 15-20 min every 2-3 hours for first 48-72 hours",
                            "Acetaminophen 500-1000mg every 6 hours AND/OR ibuprofen 400mg every 6 hours",
                            "Gentle walking as tolerated (short walks, gradually increase)",
                            "Avoid heavy lifting, bending, and twisting",
                            "Sleep with pillow between knees (side) or under knees (back)",
                        ],
                    },
                    "day_4_7": {
                        "label": "Active Recovery",
                        "management": [
                            "Switch from ice to heat (heating pad 15-20 min, several times daily)",
                            "Begin gentle stretching: cat-cow, knee-to-chest, pelvic tilts",
                            "Gradually increase walking distance and duration",
                            "Reduce pain medications as tolerated",
                            "Maintain good posture. Use lumbar support if sitting for long periods.",
                        ],
                    },
                    "week_2_plus": {
                        "label": "Rehabilitation & Prevention",
                        "management": [
                            "Most acute low back pain resolves within 4-6 weeks",
                            "Core strengthening exercises (planks, bridges, bird-dogs)",
                            "Regular walking, swimming, or cycling",
                            "If not improving by 4-6 weeks, see physician for further evaluation",
                            "Ergonomic assessment of workstation if desk job",
                            "Weight management if applicable",
                        ],
                    },
                    "red_flags": {
                        "call_doctor": ["Pain not improving after 4-6 weeks of self-care", "Pain radiating below the knee (sciatica)", "Numbness or tingling in legs", "History of cancer with new back pain", "Unexplained weight loss with back pain", "Pain worse at night or at rest"],
                        "go_to_er": ["Loss of bladder or bowel control (cauda equina syndrome - EMERGENCY)", "Progressive leg weakness", "Back pain after significant trauma", "Fever with back pain", "Saddle anesthesia (numbness in groin/inner thighs)"],
                        "call_911": ["Loss of bladder/bowel control with leg weakness (cauda equina)"],
                    },
                    "diet": ["Anti-inflammatory diet: omega-3 fatty acids (fish, flaxseed, walnuts)", "Adequate calcium and vitamin D for bone health", "Maintain hydration for disc health", "Avoid excess alcohol (increases inflammation)"],
                    "activity": ["Walking is the BEST activity for acute back pain", "Avoid prolonged sitting (stand/stretch every 30-45 min)", "No heavy lifting >10 lbs for first 2 weeks", "Swimming/water exercises excellent for recovery", "Avoid high-impact activities until pain resolves"],
                    "sleep": ["Firm (not hard) mattress", "Side sleeping with pillow between knees", "Or back sleeping with pillow under knees", "Avoid stomach sleeping"],
                },
            },
            "type 2 diabetes": {
                "moderate": {
                    "day_1_3": {
                        "label": "Initial Management",
                        "management": [
                            "Begin glucose monitoring: check fasting and 2h post-meal (or per physician instruction)",
                            "Start or continue prescribed medications as directed",
                            "Dietary assessment: begin tracking carbohydrate intake",
                            "Target blood glucose: fasting 80-130 mg/dL, 2h post-meal <180 mg/dL",
                            "Learn hypoglycemia symptoms and treatment (15g fast-acting carbs rule)",
                            "Schedule diabetes education class if available",
                        ],
                    },
                    "day_4_7": {
                        "label": "Establishing Routine",
                        "management": [
                            "Establish consistent meal timing and portions",
                            "Begin regular exercise: 10-15 min walks after meals",
                            "Record blood glucose readings in log",
                            "Review medication side effects with pharmacist",
                            "Begin foot care routine: inspect feet daily",
                        ],
                    },
                    "week_2_plus": {
                        "label": "Ongoing Management",
                        "management": [
                            "Target HbA1c <7% (individualized based on patient factors)",
                            "Exercise: 150 min/week moderate activity + 2 sessions resistance training",
                            "Annual: eye exam, foot exam, urine albumin, lipid panel",
                            "Every 3-6 months: HbA1c",
                            "Blood pressure target: <130/80",
                            "Statin therapy if age >40 with risk factors",
                            "ACEi/ARB if albuminuria detected",
                            "Pneumococcal and annual flu vaccination",
                        ],
                    },
                    "red_flags": {
                        "call_doctor": ["Blood glucose consistently >250 mg/dL", "Recurrent hypoglycemia (<70 mg/dL)", "Numbness/tingling in feet (neuropathy)", "Vision changes", "Persistent foot wound or sore", "Medication side effects"],
                        "go_to_er": ["Blood glucose >400 mg/dL", "Symptoms of DKA: nausea, vomiting, abdominal pain, fruity breath, confusion", "Severe hypoglycemia (unable to self-treat, confusion, seizure)", "Chest pain or shortness of breath", "Signs of stroke"],
                        "call_911": ["Loss of consciousness from hypoglycemia (glucagon if available)", "Chest pain suggesting MI", "Stroke symptoms"],
                    },
                    "diet": ["Carbohydrate counting: 45-60g per meal (individualized)", "Plate method: 1/2 non-starchy vegetables, 1/4 lean protein, 1/4 whole grains", "Limit added sugars and refined carbohydrates", "Increase fiber intake (25-30g/day)", "Choose whole grains over refined", "Healthy fats: olive oil, nuts, avocado", "Limit sodium to <2300mg/day"],
                    "activity": ["150 min/week moderate aerobic exercise (brisk walking, cycling, swimming)", "Resistance training 2-3x/week (improves insulin sensitivity)", "Reduce sedentary time: move every 30 minutes", "Check blood glucose before and after exercise", "Carry fast-acting glucose during exercise", "Avoid exercise if blood glucose >250 with ketones"],
                    "sleep": ["Aim for 7-8 hours per night (poor sleep worsens glucose control)", "Screen for sleep apnea (common in type 2 diabetes)", "Consistent sleep schedule", "Avoid heavy meals close to bedtime"],
                },
            },
        }

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _check_med_safety(self, tool_input: dict) -> str:
        medication = tool_input.get("medication", "").lower()
        age = tool_input.get("patient_age", 30)
        gender = tool_input.get("patient_gender", "unknown")
        other_meds = tool_input.get("other_medications", [])
        conditions = tool_input.get("conditions", [])

        med_db = self._get_medication_db()

        # Find the medication in the database (exact or alias match)
        med_info = None
        matched_name = None
        for name, info in med_db.items():
            aliases = info.get("aliases", [])
            if medication in name or name in medication or any(a in medication or medication in a for a in aliases):
                med_info = info
                matched_name = name
                break

        if not med_info:
            # Build safety info from interaction checking even without a profile
            interactions = self._check_interactions(medication, other_meds)
            return json.dumps({
                "medication": medication,
                "status": "not_in_database",
                "available_medications": sorted(med_db.keys()),
                "interactions_found": interactions,
                "instruction": (
                    "This medication is not in the structured safety database. "
                    "Use your clinical pharmacology knowledge to assess safety. "
                    "The available medications in the database are listed above. "
                    "Any interactions detected with other medications are included."
                ),
                "general_checks": {
                    "patient_age": age,
                    "patient_gender": gender,
                    "other_medications": other_meds,
                    "conditions": conditions,
                },
            })

        # Build comprehensive safety report
        safety_report = {
            "medication": matched_name,
            "class": med_info.get("class"),
            "otc": med_info.get("otc"),
            "dosing": med_info.get("dosing", {}),
            "contraindications": med_info.get("contraindications", []),
            "common_side_effects": med_info.get("common_side_effects", []),
            "serious_risks": med_info.get("serious_risks", []),
            "age_specific_concerns": [],
            "condition_specific_concerns": [],
            "interaction_alerts": [],
            "renal_hepatic_notes": [],
            "pregnancy_lactation": {},
        }

        # Age-specific concerns
        if age < 2:
            safety_report["age_specific_concerns"].append("INFANT: Consult pediatrician before any medication. Use weight-based dosing only.")
            if "dosing" in med_info and "pediatric" in med_info["dosing"]:
                safety_report["age_specific_concerns"].append(f"Pediatric dosing: {med_info['dosing']['pediatric']}")
        elif age < 12:
            safety_report["age_specific_concerns"].append("CHILD: Use pediatric formulation and weight-based dosing.")
            if "dosing" in med_info and "pediatric" in med_info["dosing"]:
                safety_report["age_specific_concerns"].append(f"Pediatric dosing: {med_info['dosing']['pediatric']}")
        elif age < 18:
            if "aspirin" in matched_name:
                safety_report["age_specific_concerns"].append("CONTRAINDICATED: Risk of Reye syndrome in adolescents with viral illness.")
            if "dosing" in med_info and "pediatric" in med_info["dosing"]:
                safety_report["age_specific_concerns"].append(f"Pediatric dosing: {med_info['dosing']['pediatric']}")
        elif age >= 65:
            safety_report["age_specific_concerns"].append("ELDERLY: Use lowest effective dose for shortest duration.")
            if "dosing" in med_info and "geriatric" in med_info["dosing"]:
                safety_report["age_specific_concerns"].append(f"Geriatric dosing: {med_info['dosing']['geriatric']}")
            if any(kw in matched_name for kw in ["diphenhydramine", "lorazepam"]):
                safety_report["age_specific_concerns"].append("Beers Criteria: This medication should generally be AVOIDED in patients >= 65 years due to high risk of falls, cognitive impairment, and adverse effects.")

        # Condition-specific concerns
        conditions_lower = [c.lower() for c in conditions]
        for condition in conditions_lower:
            if "kidney" in condition or "renal" in condition or "ckd" in condition:
                renal = med_info.get("renal_adjustment", {})
                if renal:
                    safety_report["renal_hepatic_notes"].append({"type": "renal", "details": renal})
            if "liver" in condition or "hepat" in condition or "cirrhosis" in condition:
                hepatic = med_info.get("hepatic_adjustment")
                if hepatic:
                    safety_report["renal_hepatic_notes"].append({"type": "hepatic", "details": hepatic})
            if "asthma" in condition and any(kw in matched_name for kw in ["aspirin", "ibuprofen", "naproxen"]):
                safety_report["condition_specific_concerns"].append("NSAIDs/Aspirin can trigger bronchospasm in aspirin-sensitive asthma (Samter triad). Use with extreme caution.")
            if "ulcer" in condition or "gi bleed" in condition:
                if any(kw in matched_name for kw in ["ibuprofen", "naproxen", "aspirin"]):
                    safety_report["condition_specific_concerns"].append("CONTRAINDICATED: Active or recent GI ulcer/bleeding. Use acetaminophen instead.")
            if "heart failure" in condition:
                if any(kw in matched_name for kw in ["ibuprofen", "naproxen"]):
                    safety_report["condition_specific_concerns"].append("NSAIDs can worsen heart failure (fluid retention, reduced renal perfusion). Avoid if possible.")
            if "alcohol" in condition:
                if "acetaminophen" in matched_name:
                    safety_report["condition_specific_concerns"].append("CAUTION: Alcohol use increases hepatotoxicity risk. Maximum 2000mg/day. Avoid if heavy alcohol use.")

        # Pregnancy/lactation
        if gender and gender.lower() == "female" and 12 <= age <= 55:
            preg = med_info.get("pregnancy", {})
            lact = med_info.get("breastfeeding", "")
            safety_report["pregnancy_lactation"] = {
                "note": "Patient is of childbearing age. Verify pregnancy/lactation status.",
                "pregnancy": preg,
                "breastfeeding": lact,
            }

        # Drug-drug interactions from matrix
        matrix_interactions = self._check_interactions(medication, other_meds)
        if matrix_interactions:
            safety_report["interaction_alerts"].extend(matrix_interactions)

        # Also check the medication's own interaction list
        med_interactions = med_info.get("interactions", {})
        for other_med in other_meds:
            other_lower = other_med.lower()
            for key, detail in med_interactions.items():
                if any(word in other_lower for word in key.split("_")):
                    safety_report["interaction_alerts"].append({
                        "between": f"{matched_name} <-> {other_med}",
                        "category": key,
                        "detail": detail,
                    })

        # Prescription reminder
        if not med_info.get("otc", False):
            safety_report["prescription_required"] = "This medication REQUIRES a prescription. Patient must see a physician."

        return json.dumps(safety_report)

    async def _generate_care(self, tool_input: dict) -> str:
        condition = tool_input.get("condition", "").lower()
        severity = tool_input.get("severity", "moderate").lower()
        age = tool_input.get("patient_age", 30)
        comorbidities = tool_input.get("comorbidities", [])

        care_db = self._get_care_plan_db()

        # Find matching care plan
        care_plan = None
        matched_condition = None
        for key, plans in care_db.items():
            if condition in key or key in condition:
                care_plan = plans
                matched_condition = key
                break

        if not care_plan:
            return json.dumps({
                "condition": condition,
                "severity": severity,
                "status": "not_in_database",
                "available_conditions": sorted(care_db.keys()),
                "instruction": (
                    "This condition is not in the structured care plan database. "
                    "Generate a comprehensive day-by-day care plan using your clinical knowledge. "
                    "Structure it as: Day 1-3 (acute), Day 4-7 (recovery), Week 2+ (follow-up). "
                    "Include red flags (call doctor vs ER vs 911), diet, activity, and sleep recommendations."
                ),
                "patient_context": {"age": age, "comorbidities": comorbidities},
            })

        # Get the severity-matched plan, or the closest available
        plan = care_plan.get(severity)
        if not plan:
            available_severities = list(care_plan.keys())
            plan = care_plan.get(available_severities[0], {})

        # Add age-specific modifications
        age_modifications = []
        if age < 2:
            age_modifications.append("INFANT: All medications require pediatric formulations and weight-based dosing. Consult pediatrician for all medication decisions.")
            age_modifications.append("Monitor for dehydration: wet diapers <6/day, sunken fontanelle, no tears when crying.")
        elif age < 12:
            age_modifications.append("CHILD: Use pediatric dosing. Avoid aspirin (Reye syndrome). Make instructions accessible to caregiver.")
        elif age >= 75:
            age_modifications.append("ELDERLY: Higher fall risk. Avoid sedating medications. Lower medication doses. Ensure caregiver support available.")
            age_modifications.append("Monitor for delirium/confusion with any illness.")

        # Add comorbidity modifications
        comorbidity_notes = []
        for comorbidity in comorbidities:
            cl = comorbidity.lower()
            if "diabetes" in cl:
                comorbidity_notes.append("DIABETES: Monitor blood glucose more frequently during illness. Illness can raise blood glucose. Adjust insulin if needed. Stay hydrated. Sick-day rules apply.")
            if "heart failure" in cl:
                comorbidity_notes.append("HEART FAILURE: Monitor daily weights. Avoid excess fluid and sodium. Report weight gain >2 lbs in a day or 5 lbs in a week.")
            if "copd" in cl or "asthma" in cl:
                comorbidity_notes.append("RESPIRATORY: Lower threshold for seeking emergency care. Continue inhalers. Avoid NSAIDs if aspirin-sensitive asthma.")
            if "kidney" in cl or "ckd" in cl:
                comorbidity_notes.append("KIDNEY DISEASE: Avoid NSAIDs. Adjust medication doses. Monitor fluid intake. Report decreased urine output.")
            if "immunosuppressed" in cl or "transplant" in cl or "hiv" in cl:
                comorbidity_notes.append("IMMUNOCOMPROMISED: Lower threshold for medical evaluation. Infections may progress rapidly. Contact physician early.")

        result = {
            "condition": matched_condition,
            "severity": severity,
            "care_plan": plan,
            "age_modifications": age_modifications if age_modifications else "Standard adult care plan applies.",
            "comorbidity_modifications": comorbidity_notes if comorbidity_notes else "No specific comorbidity modifications.",
            "patient_context": {"age": age, "comorbidities": comorbidities},
        }

        return json.dumps(result)

    async def _create_med_schedule(self, tool_input: dict) -> str:
        medications = tool_input.get("medications", [])
        routine = tool_input.get("patient_routine", "wakes 7am, lunch noon, dinner 6pm, bed 10pm")

        # Parse routine for approximate times
        times = {
            "morning": "7:00 AM",
            "midmorning": "10:00 AM",
            "noon": "12:00 PM",
            "afternoon": "3:00 PM",
            "evening": "6:00 PM",
            "bedtime": "10:00 PM",
        }

        # Medication timing knowledge
        timing_rules = {
            "omeprazole": {"timing": "morning", "food": "Take 30 minutes BEFORE breakfast on empty stomach", "note": "Best absorbed on empty stomach before first meal"},
            "pantoprazole": {"timing": "morning", "food": "Take 30 minutes BEFORE breakfast on empty stomach", "note": "Best absorbed on empty stomach"},
            "levothyroxine": {"timing": "morning", "food": "Take on empty stomach, 30-60 min before breakfast. Separate from calcium, iron by 4 hours.", "note": "Take first thing in the morning with water only"},
            "metformin": {"timing": "with meals", "food": "Take WITH meals to reduce GI side effects", "note": "Usually twice daily with breakfast and dinner"},
            "lisinopril": {"timing": "morning", "food": "Can take with or without food", "note": "Once daily, consistent timing"},
            "amlodipine": {"timing": "morning", "food": "Can take with or without food", "note": "Once daily"},
            "atorvastatin": {"timing": "evening", "food": "Can take with or without food", "note": "Can be taken any time of day. Evening traditionally preferred but not required."},
            "simvastatin": {"timing": "evening", "food": "Take in the evening", "note": "MUST be taken in evening for optimal effect"},
            "metoprolol": {"timing": "with meals", "food": "Take with or immediately following meals", "note": "Usually twice daily. Do not abruptly discontinue."},
            "furosemide": {"timing": "morning", "food": "Take in morning to avoid nighttime urination", "note": "Second dose, if needed, take by early afternoon (2 PM)"},
            "prednisone": {"timing": "morning", "food": "Take WITH food to reduce GI upset", "note": "Morning dosing mimics natural cortisol rhythm. Take with breakfast."},
            "iron_supplement": {"timing": "morning", "food": "Take on empty stomach with vitamin C (orange juice) for best absorption. Separate from calcium, antacids, PPIs by 2 hours.", "note": "May cause constipation and dark stools"},
            "calcium": {"timing": "with meals", "food": "Take WITH meals for absorption (carbonate form). Citrate can be taken with or without food.", "note": "Max 500-600mg per dose. Split if taking >600mg/day. Separate from iron and thyroid meds by 2-4 hours."},
            "aspirin": {"timing": "morning", "food": "Take with food to reduce GI upset", "note": "If also taking ibuprofen, take aspirin 30 min before ibuprofen."},
            "ibuprofen": {"timing": "as needed", "food": "Take WITH food", "note": "Every 6-8 hours as needed. Max 1200mg/day OTC."},
            "acetaminophen": {"timing": "as needed", "food": "Can take with or without food", "note": "Every 4-6 hours as needed. Max 3000mg/day."},
            "cetirizine": {"timing": "bedtime", "food": "Can take with or without food", "note": "Once daily. Bedtime if causes drowsiness."},
            "loratadine": {"timing": "morning", "food": "Can take with or without food", "note": "Once daily. Non-sedating."},
            "melatonin": {"timing": "bedtime", "food": "Take 30-60 minutes before desired bedtime", "note": "Start with 0.5-1mg. Do not exceed 5mg."},
        }

        schedule = {
            "morning_on_waking": {"time": times["morning"], "medications": [], "notes": []},
            "morning_with_breakfast": {"time": f"~30 min after waking", "medications": [], "notes": []},
            "midmorning": {"time": times["midmorning"], "medications": [], "notes": []},
            "noon_with_lunch": {"time": times["noon"], "medications": [], "notes": []},
            "afternoon": {"time": times["afternoon"], "medications": [], "notes": []},
            "evening_with_dinner": {"time": times["evening"], "medications": [], "notes": []},
            "bedtime": {"time": times["bedtime"], "medications": [], "notes": []},
            "as_needed": {"medications": [], "notes": []},
        }

        spacing_warnings = []

        for med in medications:
            med_name = med.get("name", "").lower()
            dose = med.get("dose", "as prescribed")
            frequency = med.get("frequency", "once daily").lower()

            # Find timing rules
            rule = None
            for key, val in timing_rules.items():
                if key in med_name:
                    rule = val
                    break

            med_entry = {"name": med.get("name", med_name), "dose": dose}

            if rule:
                timing = rule["timing"]
                med_entry["food_instruction"] = rule["food"]
                med_entry["note"] = rule["note"]

                if timing == "morning" and "empty stomach" in rule.get("food", "").lower():
                    schedule["morning_on_waking"]["medications"].append(med_entry)
                elif timing == "morning":
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
                elif timing == "evening":
                    schedule["evening_with_dinner"]["medications"].append(med_entry)
                elif timing == "bedtime":
                    schedule["bedtime"]["medications"].append(med_entry)
                elif timing == "with meals":
                    if "twice" in frequency or "bid" in frequency:
                        schedule["morning_with_breakfast"]["medications"].append(med_entry)
                        schedule["evening_with_dinner"]["medications"].append({**med_entry, "note": "Second dose"})
                    elif "three" in frequency or "tid" in frequency:
                        schedule["morning_with_breakfast"]["medications"].append(med_entry)
                        schedule["noon_with_lunch"]["medications"].append({**med_entry, "note": "Second dose"})
                        schedule["evening_with_dinner"]["medications"].append({**med_entry, "note": "Third dose"})
                    else:
                        schedule["morning_with_breakfast"]["medications"].append(med_entry)
                elif timing == "as needed":
                    schedule["as_needed"]["medications"].append(med_entry)
                else:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
            else:
                # Default scheduling based on frequency
                med_entry["food_instruction"] = "Take with food unless otherwise directed"
                if "once" in frequency or "daily" in frequency or "qd" in frequency:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
                elif "twice" in frequency or "bid" in frequency:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
                    schedule["evening_with_dinner"]["medications"].append({**med_entry, "note": "Second dose"})
                elif "three" in frequency or "tid" in frequency:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
                    schedule["noon_with_lunch"]["medications"].append({**med_entry, "note": "Second dose"})
                    schedule["evening_with_dinner"]["medications"].append({**med_entry, "note": "Third dose"})
                elif "four" in frequency or "qid" in frequency:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)
                    schedule["midmorning"]["medications"].append({**med_entry, "note": "Second dose"})
                    schedule["afternoon"]["medications"].append({**med_entry, "note": "Third dose"})
                    schedule["bedtime"]["medications"].append({**med_entry, "note": "Fourth dose"})
                elif "as needed" in frequency or "prn" in frequency:
                    schedule["as_needed"]["medications"].append(med_entry)
                else:
                    schedule["morning_with_breakfast"]["medications"].append(med_entry)

        # Check for spacing conflicts
        med_names = [m.get("name", "").lower() for m in medications]
        if any("iron" in m for m in med_names) and any(kw in m for m in med_names for kw in ["calcium", "antacid", "omeprazole", "pantoprazole"]):
            spacing_warnings.append("IRON: Separate iron supplements from calcium, antacids, and PPIs by at least 2 hours for proper absorption.")
        if any("levothyroxine" in m for m in med_names) and any(kw in m for m in med_names for kw in ["calcium", "iron", "antacid"]):
            spacing_warnings.append("THYROID: Separate levothyroxine from calcium, iron, and antacids by at least 4 hours.")
        if any("fluoroquinolone" in m or "levofloxacin" in m or "ciprofloxacin" in m for m in med_names) and any(kw in m for m in med_names for kw in ["antacid", "calcium", "iron", "magnesium"]):
            spacing_warnings.append("ANTIBIOTIC: Separate fluoroquinolones from antacids, calcium, iron, and magnesium by 2 hours before or 6 hours after.")

        # Remove empty time slots
        clean_schedule = {}
        for time_slot, data in schedule.items():
            if data.get("medications"):
                clean_schedule[time_slot] = data

        return json.dumps({
            "medication_schedule": clean_schedule,
            "spacing_warnings": spacing_warnings if spacing_warnings else "No specific spacing conflicts detected.",
            "general_instructions": [
                "Take medications at the same time each day for consistency.",
                "Set phone alarms or use a pill organizer to help remember.",
                "Do NOT crush or split extended-release or enteric-coated medications.",
                "If you miss a dose, take it as soon as you remember unless it's almost time for the next dose. Never double up.",
                "Keep an updated medication list in your wallet and share with all healthcare providers.",
                "Contact your pharmacist with any questions about your medication schedule.",
            ],
            "patient_routine": routine,
        })
