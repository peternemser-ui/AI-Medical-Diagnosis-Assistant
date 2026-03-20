"""
Patient Safety Agent – Reviews entire diagnosis pipeline for safety concerns.

Responsibilities:
  * Check for contraindications in recommended treatments
  * Verify medication dosage safety across age groups
  * Assess allergy and cross-reactivity risks
  * Flag dangerous drug combinations or treatment conflicts
  * Apply Swiss Cheese Model, Beers Criteria, STOPP/START criteria
  * Act as a "second pair of eyes" before final output
"""

from __future__ import annotations

import json
import re
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


# ---------------------------------------------------------------------------
# Contraindication database
# ---------------------------------------------------------------------------

CONTRAINDICATIONS: dict[str, list[dict]] = {
    # NSAIDs
    "ibuprofen": [
        {"condition": "gi bleed", "type": "absolute", "severity": "critical", "detail": "Active GI bleeding or history of NSAID-induced GI bleed", "alternative": "Acetaminophen, topical NSAIDs, or COX-2 selective inhibitor with PPI"},
        {"condition": "peptic ulcer", "type": "absolute", "severity": "critical", "detail": "Active peptic ulcer disease", "alternative": "Acetaminophen; if NSAID essential, use celecoxib + PPI"},
        {"condition": "ckd", "type": "relative", "severity": "high", "detail": "NSAIDs reduce renal blood flow via prostaglandin inhibition; may worsen CKD (avoid if eGFR < 30)", "alternative": "Acetaminophen, topical agents, non-pharmacologic pain management"},
        {"condition": "kidney", "type": "relative", "severity": "high", "detail": "NSAIDs may worsen renal function; avoid in advanced kidney disease", "alternative": "Acetaminophen, topical NSAIDs"},
        {"condition": "heart failure", "type": "relative", "severity": "high", "detail": "NSAIDs cause sodium and water retention, worsening heart failure; increase CV events", "alternative": "Acetaminophen; short-course topical NSAID if essential"},
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Contraindicated in third trimester (premature ductus arteriosus closure). Avoid throughout pregnancy if possible.", "alternative": "Acetaminophen"},
        {"condition": "asthma", "type": "relative", "severity": "high", "detail": "NSAID-exacerbated respiratory disease (Samter's triad) in ~10% of asthmatics", "alternative": "Acetaminophen (generally safe), COX-2 inhibitor with caution, desensitization if needed"},
        {"condition": "anticoagulant", "type": "relative", "severity": "high", "detail": "Additive bleeding risk with anticoagulants", "alternative": "Acetaminophen; if needed, use lowest dose shortest duration with PPI"},
    ],
    "naproxen": [
        {"condition": "gi bleed", "type": "absolute", "severity": "critical", "detail": "Active GI bleeding", "alternative": "Acetaminophen"},
        {"condition": "peptic ulcer", "type": "absolute", "severity": "critical", "detail": "Active peptic ulcer disease", "alternative": "Acetaminophen + PPI if needed"},
        {"condition": "ckd", "type": "relative", "severity": "high", "detail": "Nephrotoxic; avoid if eGFR < 30", "alternative": "Acetaminophen"},
        {"condition": "heart failure", "type": "relative", "severity": "high", "detail": "Fluid retention and CV risk", "alternative": "Acetaminophen"},
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Avoid especially in third trimester", "alternative": "Acetaminophen"},
    ],
    "diclofenac": [
        {"condition": "gi bleed", "type": "absolute", "severity": "critical", "detail": "Active GI bleeding", "alternative": "Acetaminophen, topical diclofenac (lower systemic absorption)"},
        {"condition": "cardiovascular", "type": "relative", "severity": "high", "detail": "Higher CV risk than other NSAIDs (similar to COX-2 inhibitors). Avoid in established CVD.", "alternative": "Naproxen (lowest CV risk among NSAIDs), acetaminophen"},
        {"condition": "ckd", "type": "relative", "severity": "high", "detail": "Nephrotoxic", "alternative": "Acetaminophen"},
        {"condition": "liver disease", "type": "relative", "severity": "high", "detail": "Hepatotoxicity risk; monitor LFTs", "alternative": "Acetaminophen (with dose adjustment), topical agents"},
    ],
    "aspirin": [
        {"condition": "child", "type": "absolute", "severity": "critical", "detail": "Contraindicated in children < 16 years — Reye syndrome risk (acute hepatic encephalopathy)", "alternative": "Acetaminophen or ibuprofen for pediatric pain/fever"},
        {"condition": "gi bleed", "type": "absolute", "severity": "critical", "detail": "Active GI bleeding", "alternative": "Acetaminophen"},
        {"condition": "bleeding disorder", "type": "absolute", "severity": "critical", "detail": "Hemophilia or severe thrombocytopenia", "alternative": "Acetaminophen"},
        {"condition": "gout", "type": "relative", "severity": "moderate", "detail": "Low-dose aspirin raises uric acid levels and may trigger gout flares", "alternative": "Acetaminophen for pain; if antiplatelet needed, monitor uric acid"},
    ],
    # ACE inhibitors
    "lisinopril": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Teratogenic — causes fetal renal dysgenesis, oligohydramnios, skull defects (2nd/3rd trimester)", "alternative": "Labetalol, nifedipine, or methyldopa for hypertension in pregnancy"},
        {"condition": "angioedema", "type": "absolute", "severity": "critical", "detail": "History of ACE inhibitor-induced angioedema", "alternative": "ARB (with caution, ~2% cross-reactivity) or CCB"},
        {"condition": "bilateral renal artery stenosis", "type": "absolute", "severity": "critical", "detail": "May precipitate acute renal failure", "alternative": "CCB (amlodipine)"},
        {"condition": "hyperkalemia", "type": "relative", "severity": "high", "detail": "K > 5.5 mEq/L — ACEi reduces potassium excretion", "alternative": "CCB, thiazide diuretic"},
        {"condition": "ckd", "type": "relative", "severity": "moderate", "detail": "Beneficial in CKD with proteinuria but requires monitoring; contraindicated if eGFR < 20 without specialist guidance", "alternative": "ARB if ACEi not tolerated; CCB for BP control alone"},
    ],
    "enalapril": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Teratogenic in all trimesters", "alternative": "Labetalol, nifedipine, methyldopa"},
        {"condition": "angioedema", "type": "absolute", "severity": "critical", "detail": "History of ACEi-induced angioedema", "alternative": "ARB or CCB"},
        {"condition": "hyperkalemia", "type": "relative", "severity": "high", "detail": "Risk of hyperkalemia", "alternative": "CCB"},
    ],
    "ramipril": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Teratogenic", "alternative": "Labetalol, nifedipine, methyldopa"},
        {"condition": "angioedema", "type": "absolute", "severity": "critical", "detail": "ACEi angioedema history", "alternative": "ARB or CCB"},
    ],
    # Beta-blockers
    "propranolol": [
        {"condition": "asthma", "type": "absolute", "severity": "critical", "detail": "Non-selective beta-blocker causes bronchospasm in asthma", "alternative": "Cardioselective beta-blocker (metoprolol, bisoprolol) with caution, or CCB"},
        {"condition": "copd", "type": "relative", "severity": "high", "detail": "Non-selective BB may worsen bronchospasm in severe COPD", "alternative": "Cardioselective BB (bisoprolol) generally safe in mild-moderate COPD"},
        {"condition": "bradycardia", "type": "absolute", "severity": "critical", "detail": "Heart rate < 50 bpm or sick sinus syndrome without pacemaker", "alternative": "CCB (if needed for rate control, use verapamil/diltiazem with caution)"},
        {"condition": "diabetes", "type": "relative", "severity": "moderate", "detail": "Masks hypoglycemia symptoms (tachycardia, tremor) and may prolong hypoglycemic episodes", "alternative": "Cardioselective BB (less masking effect) or alternative antihypertensive"},
        {"condition": "raynaud", "type": "relative", "severity": "moderate", "detail": "Worsens peripheral vasoconstriction", "alternative": "CCB (nifedipine, amlodipine)"},
    ],
    "metoprolol": [
        {"condition": "severe bradycardia", "type": "absolute", "severity": "critical", "detail": "Heart rate < 45 bpm or heart block > 1st degree without pacemaker", "alternative": "CCB, hydralazine"},
        {"condition": "cardiogenic shock", "type": "absolute", "severity": "critical", "detail": "Negative inotropic effect worsens cardiogenic shock", "alternative": "Hemodynamic support first, then consider BB when stable"},
        {"condition": "asthma", "type": "relative", "severity": "moderate", "detail": "Cardioselective but may still worsen severe asthma at higher doses", "alternative": "CCB for rate control or hypertension"},
    ],
    "atenolol": [
        {"condition": "asthma", "type": "relative", "severity": "moderate", "detail": "Cardioselective; generally safer but caution in severe asthma", "alternative": "CCB"},
        {"condition": "pregnancy", "type": "relative", "severity": "high", "detail": "Associated with IUGR; avoid in pregnancy", "alternative": "Labetalol"},
    ],
    # Statins
    "atorvastatin": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "All statins are Category X — teratogenic (cholesterol essential for fetal development)", "alternative": "Discontinue during pregnancy; bile acid sequestrants if LDL treatment essential"},
        {"condition": "liver disease", "type": "absolute", "severity": "critical", "detail": "Active liver disease or unexplained persistent transaminase elevation > 3x ULN", "alternative": "Ezetimibe, bile acid sequestrants, PCSK9 inhibitors"},
        {"condition": "rhabdomyolysis", "type": "absolute", "severity": "critical", "detail": "History of statin-induced rhabdomyolysis", "alternative": "Ezetimibe, PCSK9 inhibitor, bempedoic acid"},
        {"condition": "myopathy", "type": "relative", "severity": "moderate", "detail": "Muscle symptoms on prior statin — try dose reduction, alternate-day dosing, or different statin", "alternative": "Rosuvastatin (lower myopathy risk), pravastatin, or non-statin therapy"},
    ],
    "simvastatin": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Teratogenic (Category X)", "alternative": "Discontinue in pregnancy"},
        {"condition": "liver disease", "type": "absolute", "severity": "critical", "detail": "Active liver disease", "alternative": "Ezetimibe"},
        {"condition": "cyp3a4 inhibitor", "type": "absolute", "severity": "critical", "detail": "Contraindicated with strong CYP3A4 inhibitors (ketoconazole, itraconazole, HIV protease inhibitors) — rhabdomyolysis risk", "alternative": "Rosuvastatin or pravastatin (not CYP3A4 substrates)"},
    ],
    # Anticoagulants
    "warfarin": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Teratogenic (warfarin embryopathy — nasal hypoplasia, stippled epiphyses, CNS abnormalities). Especially weeks 6-12.", "alternative": "LMWH (enoxaparin) throughout pregnancy"},
        {"condition": "active bleeding", "type": "absolute", "severity": "critical", "detail": "Active hemorrhage or recent hemorrhagic stroke", "alternative": "Assess need for anticoagulation; mechanical valve may require heparin bridge"},
        {"condition": "severe liver disease", "type": "relative", "severity": "high", "detail": "Impaired clotting factor synthesis increases bleeding risk", "alternative": "Dose reduction with careful INR monitoring; DOAC may be preferred in mild-moderate liver disease"},
        {"condition": "falls risk", "type": "relative", "severity": "moderate", "detail": "Increased intracranial hemorrhage risk in elderly with frequent falls", "alternative": "DOAC (lower ICH risk than warfarin), assess fall prevention"},
    ],
    "rivaroxaban": [
        {"condition": "severe ckd", "type": "relative", "severity": "high", "detail": "Avoid if CrCl < 15 mL/min (no dialysis data). Dose adjust at CrCl 15-50.", "alternative": "Warfarin with INR monitoring, or apixaban (better renal safety data)"},
        {"condition": "active bleeding", "type": "absolute", "severity": "critical", "detail": "Active pathological bleeding", "alternative": "Assess anticoagulation need"},
        {"condition": "liver disease", "type": "absolute", "severity": "critical", "detail": "Avoid in Child-Pugh B/C with coagulopathy", "alternative": "Warfarin with careful monitoring"},
    ],
    "apixaban": [
        {"condition": "severe liver disease", "type": "absolute", "severity": "critical", "detail": "Avoid in Child-Pugh C", "alternative": "Warfarin with careful monitoring"},
        {"condition": "active bleeding", "type": "absolute", "severity": "critical", "detail": "Active pathological bleeding", "alternative": "Assess anticoagulation need"},
        {"condition": "mechanical valve", "type": "absolute", "severity": "critical", "detail": "DOACs contraindicated with mechanical heart valves (RE-ALIGN trial showed harm)", "alternative": "Warfarin is the only approved anticoagulant for mechanical valves"},
    ],
    # Opioids
    "morphine": [
        {"condition": "respiratory depression", "type": "absolute", "severity": "critical", "detail": "Severe respiratory depression or acute/severe asthma in unmonitored setting", "alternative": "Non-opioid analgesia; if opioid essential, use with monitoring and naloxone available"},
        {"condition": "paralytic ileus", "type": "absolute", "severity": "critical", "detail": "Known or suspected GI obstruction", "alternative": "Non-opioid analgesia"},
        {"condition": "head injury", "type": "relative", "severity": "high", "detail": "May mask neurological signs, raise ICP", "alternative": "Acetaminophen; if opioid needed, use with close neuro monitoring"},
        {"condition": "severe ckd", "type": "relative", "severity": "high", "detail": "Active metabolite (M6G) accumulates in renal failure, causing prolonged sedation", "alternative": "Fentanyl or hydromorphone (no active renal metabolites)"},
    ],
    "codeine": [
        {"condition": "child", "type": "absolute", "severity": "critical", "detail": "Contraindicated in children < 12 years and post-tonsillectomy in < 18 years (FDA black box). CYP2D6 ultra-rapid metabolizers at risk for fatal respiratory depression.", "alternative": "Acetaminophen, ibuprofen"},
        {"condition": "respiratory depression", "type": "absolute", "severity": "critical", "detail": "Severe respiratory insufficiency", "alternative": "Non-opioid analgesia"},
        {"condition": "breastfeeding", "type": "absolute", "severity": "critical", "detail": "Active metabolite (morphine) excreted in breast milk; fatal infant cases reported in ultra-rapid metabolizers", "alternative": "Acetaminophen, ibuprofen"},
    ],
    # Benzodiazepines
    "diazepam": [
        {"condition": "myasthenia gravis", "type": "absolute", "severity": "critical", "detail": "Worsens muscle weakness; may precipitate respiratory failure", "alternative": "Buspirone for anxiety; gabapentin for muscle spasm"},
        {"condition": "severe respiratory disease", "type": "relative", "severity": "high", "detail": "Risk of respiratory depression, especially with concurrent opioids", "alternative": "Buspirone, SSRI for anxiety; non-benzo muscle relaxant"},
        {"condition": "sleep apnea", "type": "relative", "severity": "high", "detail": "Worsens upper airway obstruction", "alternative": "Trazodone, melatonin for insomnia"},
        {"condition": "elderly", "type": "relative", "severity": "high", "detail": "Beers Criteria: avoid in elderly (falls, cognitive impairment, delirium, fractures). Long half-life especially problematic.", "alternative": "Buspirone, SSRI/SNRI, non-pharmacologic therapies"},
        {"condition": "liver disease", "type": "relative", "severity": "high", "detail": "Extensively hepatically metabolized; accumulation in cirrhosis", "alternative": "Lorazepam or oxazepam (conjugation only, safer in liver disease)"},
    ],
    "alprazolam": [
        {"condition": "elderly", "type": "relative", "severity": "high", "detail": "Beers Criteria: avoid in elderly; high fall and fracture risk", "alternative": "Buspirone, SSRI"},
        {"condition": "liver disease", "type": "relative", "severity": "high", "detail": "CYP3A4 metabolized; accumulation in hepatic impairment", "alternative": "Lorazepam, oxazepam"},
    ],
    # SSRIs
    "sertraline": [
        {"condition": "maoi", "type": "absolute", "severity": "critical", "detail": "Serotonin syndrome risk with MAOIs — potentially fatal. Requires 14-day washout.", "alternative": "Wait 14 days after MAOI discontinuation; or use non-serotonergic antidepressant (bupropion)"},
        {"condition": "qt prolongation", "type": "relative", "severity": "moderate", "detail": "Dose-dependent QTc prolongation, especially at higher doses", "alternative": "Escitalopram at low dose, or mirtazapine"},
        {"condition": "bleeding risk", "type": "relative", "severity": "moderate", "detail": "SSRIs impair platelet aggregation; increased bleeding with anticoagulants", "alternative": "Mirtazapine, bupropion (no significant serotonin reuptake inhibition)"},
    ],
    "fluoxetine": [
        {"condition": "maoi", "type": "absolute", "severity": "critical", "detail": "Serotonin syndrome. Fluoxetine requires 5-week washout due to long half-life of norfluoxetine.", "alternative": "5-week washout before MAOI"},
        {"condition": "tamoxifen", "type": "relative", "severity": "high", "detail": "Strong CYP2D6 inhibitor reduces tamoxifen activation (endoxifen)", "alternative": "Sertraline, citalopram, venlafaxine (weak CYP2D6 inhibitors)"},
    ],
    # Metformin
    "metformin": [
        {"condition": "severe ckd", "type": "absolute", "severity": "critical", "detail": "Contraindicated if eGFR < 30 mL/min (lactic acidosis risk). Dose reduction at eGFR 30-45.", "alternative": "SGLT2 inhibitor, DPP-4 inhibitor, insulin, GLP-1 RA"},
        {"condition": "liver failure", "type": "absolute", "severity": "critical", "detail": "Impaired lactate clearance increases lactic acidosis risk", "alternative": "Insulin, DPP-4 inhibitor"},
        {"condition": "alcoholism", "type": "relative", "severity": "high", "detail": "Chronic heavy alcohol use increases lactic acidosis risk", "alternative": "DPP-4 inhibitor, GLP-1 RA"},
        {"condition": "contrast", "type": "relative", "severity": "high", "detail": "Hold for 48h after iodinated contrast; restart after confirming stable renal function", "alternative": "Temporary insulin coverage if needed"},
    ],
    # Insulin
    "insulin": [
        {"condition": "hypoglycemia unawareness", "type": "relative", "severity": "high", "detail": "Loss of hypoglycemia warning symptoms increases risk of severe hypoglycemia", "alternative": "Relax glycemic targets (HbA1c < 8%), CGM, hypoglycemia awareness training"},
        {"condition": "insulinoma", "type": "absolute", "severity": "critical", "detail": "Exogenous insulin in insulinoma causes refractory hypoglycemia", "alternative": "Surgical resection of insulinoma"},
    ],
    # Corticosteroids
    "prednisone": [
        {"condition": "systemic fungal infection", "type": "absolute", "severity": "critical", "detail": "Immunosuppression worsens systemic fungal infections", "alternative": "Treat infection first; if steroid essential, ensure concurrent antifungal therapy"},
        {"condition": "diabetes", "type": "relative", "severity": "high", "detail": "Corticosteroids cause dose-dependent hyperglycemia; may require insulin initiation", "alternative": "Steroid-sparing agents; if steroid needed, monitor glucose and adjust diabetes medications"},
        {"condition": "osteoporosis", "type": "relative", "severity": "moderate", "detail": "Accelerates bone loss; fracture risk increases within 3 months of starting", "alternative": "Lowest effective dose, shortest duration. Start bisphosphonate + calcium + vitamin D if > 3 months predicted."},
        {"condition": "peptic ulcer", "type": "relative", "severity": "moderate", "detail": "Increased GI bleeding risk, especially with concurrent NSAIDs", "alternative": "PPI co-prescription if steroid essential"},
        {"condition": "psychosis", "type": "relative", "severity": "moderate", "detail": "Steroid-induced psychosis in 5-18% of patients at doses >= 40mg/day", "alternative": "Lowest effective dose; monitor mental status"},
    ],
    # Fluoroquinolones
    "ciprofloxacin": [
        {"condition": "myasthenia gravis", "type": "absolute", "severity": "critical", "detail": "Fluoroquinolones may exacerbate muscle weakness and cause respiratory failure in MG", "alternative": "Amoxicillin-clavulanate, TMP-SMX, or consult infectious disease"},
        {"condition": "tendon disorder", "type": "relative", "severity": "high", "detail": "FDA black box: tendinitis and tendon rupture risk, especially in elderly, corticosteroid users, and transplant recipients", "alternative": "Other antibiotic classes based on susceptibility"},
        {"condition": "qt prolongation", "type": "relative", "severity": "moderate", "detail": "QTc prolongation risk, especially with other QT-prolonging drugs", "alternative": "Amoxicillin-clavulanate, TMP-SMX, cephalosporins"},
        {"condition": "child", "type": "relative", "severity": "moderate", "detail": "FDA: use only when no alternative; concern for musculoskeletal toxicity in children", "alternative": "Amoxicillin-clavulanate, cephalosporins, azithromycin"},
    ],
    # Tetracyclines
    "doxycycline": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Tetracyclines cause permanent teeth discoloration and bone growth inhibition in fetus", "alternative": "Amoxicillin, azithromycin, cephalosporins depending on indication"},
        {"condition": "child", "type": "absolute", "severity": "critical", "detail": "Avoid in children < 8 years (permanent teeth staining)", "alternative": "Amoxicillin, azithromycin"},
        {"condition": "esophagitis", "type": "relative", "severity": "moderate", "detail": "Pill esophagitis risk — take with full glass of water, remain upright 30 min", "alternative": "Minocycline (less esophageal risk), or alternative antibiotic class"},
    ],
    # Methotrexate
    "methotrexate": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "Potent teratogen and abortifacient. Contraception required during and 3 months after treatment.", "alternative": "Azathioprine, sulfasalazine for rheumatologic conditions; certolizumab in pregnancy"},
        {"condition": "severe ckd", "type": "absolute", "severity": "critical", "detail": "Renal clearance; accumulation causes fatal pancytopenia and mucositis", "alternative": "Leflunomide, biologics"},
        {"condition": "liver disease", "type": "relative", "severity": "high", "detail": "Hepatotoxic; avoid in significant hepatic impairment or heavy alcohol use", "alternative": "Biologics, sulfasalazine"},
        {"condition": "immunodeficiency", "type": "relative", "severity": "high", "detail": "Severe immunosuppression risk; monitor CBC regularly", "alternative": "Biologics with different mechanism"},
    ],
    # Isotretinoin
    "isotretinoin": [
        {"condition": "pregnancy", "type": "absolute", "severity": "critical", "detail": "iPLEDGE program mandatory. Category X: causes craniofacial, cardiac, CNS birth defects. Two forms of contraception required.", "alternative": "Topical retinoids (less teratogenic but still avoid in pregnancy), antibiotics for acne"},
        {"condition": "liver disease", "type": "relative", "severity": "high", "detail": "Hepatotoxic; monitor LFTs monthly", "alternative": "Topical retinoids, oral antibiotics"},
        {"condition": "depression", "type": "relative", "severity": "moderate", "detail": "Controversial association with depression and suicidality; monitor mental health", "alternative": "Topical retinoids, hormonal therapy, antibiotics"},
    ],
}

# ---------------------------------------------------------------------------
# Dosage database
# ---------------------------------------------------------------------------

DOSAGE_DATABASE: dict[str, dict] = {
    "ibuprofen": {
        "standard_adult_dose": "200-400mg every 4-6 hours",
        "max_daily_dose": "1200mg OTC; 3200mg prescription",
        "pediatric_dose": "5-10 mg/kg every 6-8 hours (max 40 mg/kg/day)",
        "geriatric_adjustment": "Start at lowest effective dose; avoid if possible (Beers Criteria: increased GI bleed, AKI risk). Max 1200mg/day if used.",
        "renal_adjustment": {
            "eGFR_30_60": "Use with caution; lowest dose, shortest duration. Monitor creatinine.",
            "eGFR_15_30": "Generally avoid; use only if no alternative with close monitoring",
            "eGFR_below_15": "Contraindicated",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "Standard dose with monitoring",
            "child_pugh_B": "Reduce dose by 50%; monitor LFTs",
            "child_pugh_C": "Avoid",
        },
    },
    "acetaminophen": {
        "standard_adult_dose": "500-1000mg every 4-6 hours",
        "max_daily_dose": "3000mg (conservative) to 4000mg/day. Limit to 2000mg/day with liver disease or heavy alcohol use.",
        "pediatric_dose": "10-15 mg/kg every 4-6 hours (max 75 mg/kg/day, not to exceed 4000mg)",
        "geriatric_adjustment": "Max 2000-3000mg/day; hepatic metabolism declines with age",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment needed",
            "eGFR_15_30": "Extend interval to every 6-8 hours",
            "eGFR_below_15": "Extend interval to every 8 hours; max 2000mg/day",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "Max 2000mg/day",
            "child_pugh_B": "Max 2000mg/day with close monitoring",
            "child_pugh_C": "Avoid or max 1000mg/day with specialist guidance",
        },
    },
    "amoxicillin": {
        "standard_adult_dose": "250-500mg every 8 hours, or 500-875mg every 12 hours",
        "max_daily_dose": "3000mg/day (higher in some infections: 4000mg/day)",
        "pediatric_dose": "25-50 mg/kg/day divided every 8-12 hours. High-dose AOM: 80-90 mg/kg/day divided BID.",
        "geriatric_adjustment": "Adjust for renal function; otherwise standard dose",
        "renal_adjustment": {
            "eGFR_30_60": "No dose adjustment, consider extended interval",
            "eGFR_15_30": "250-500mg every 12 hours",
            "eGFR_below_15": "250-500mg every 24 hours",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "No adjustment",
            "child_pugh_C": "No adjustment (renally cleared)",
        },
    },
    "metformin": {
        "standard_adult_dose": "500mg BID with meals, titrate to 1000mg BID",
        "max_daily_dose": "2550mg/day (2000mg/day in many guidelines)",
        "pediatric_dose": "500mg daily, titrate to max 2000mg/day (age >= 10 years)",
        "geriatric_adjustment": "Conservative titration; use lowest effective dose; avoid if eGFR < 30",
        "renal_adjustment": {
            "eGFR_30_60": "eGFR 30-45: max 1000mg/day, do not initiate. eGFR 45-60: max 2000mg/day, may initiate with caution.",
            "eGFR_15_30": "Contraindicated",
            "eGFR_below_15": "Contraindicated",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "Use with caution",
            "child_pugh_B": "Avoid (impaired lactate clearance)",
            "child_pugh_C": "Contraindicated",
        },
    },
    "lisinopril": {
        "standard_adult_dose": "5-10mg daily initially; titrate to 20-40mg daily",
        "max_daily_dose": "80mg/day (heart failure target: 20-40mg/day)",
        "pediatric_dose": "0.07 mg/kg once daily (max 5mg); titrate to 0.6 mg/kg/day (max 40mg)",
        "geriatric_adjustment": "Start at 2.5-5mg daily; titrate slowly monitoring renal function and potassium",
        "renal_adjustment": {
            "eGFR_30_60": "Start 5mg daily; titrate with monitoring",
            "eGFR_15_30": "Start 2.5mg daily; max 40mg",
            "eGFR_below_15": "Start 2.5mg daily; use with specialist guidance",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment (renally cleared)",
            "child_pugh_B": "No adjustment",
            "child_pugh_C": "No adjustment",
        },
    },
    "amlodipine": {
        "standard_adult_dose": "5mg once daily; may increase to 10mg",
        "max_daily_dose": "10mg/day",
        "pediatric_dose": "2.5mg once daily (ages 6-17); max 5mg/day",
        "geriatric_adjustment": "Start 2.5mg daily (reduced clearance)",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment",
            "eGFR_below_15": "No adjustment (hepatically metabolized)",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Start 2.5mg daily",
            "child_pugh_C": "Start 2.5mg daily; titrate cautiously",
        },
    },
    "atorvastatin": {
        "standard_adult_dose": "10-20mg once daily; high-intensity: 40-80mg daily",
        "max_daily_dose": "80mg/day",
        "pediatric_dose": "10-20mg daily (ages 10-17); max 20mg/day",
        "geriatric_adjustment": "No specific dose adjustment; monitor for myopathy",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment (hepatically metabolized)",
            "eGFR_below_15": "No adjustment; but use cautiously",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "Use with caution",
            "child_pugh_B": "Contraindicated if ALT/AST > 3x ULN",
            "child_pugh_C": "Contraindicated",
        },
    },
    "metoprolol": {
        "standard_adult_dose": "Tartrate: 25-100mg BID. Succinate ER: 25-200mg daily.",
        "max_daily_dose": "Tartrate: 450mg/day. Succinate: 400mg/day. HF: start 12.5-25mg, target 200mg.",
        "pediatric_dose": "1-2 mg/kg/day divided BID (max 6 mg/kg/day, up to 200mg)",
        "geriatric_adjustment": "Start low (12.5-25mg); titrate slowly; monitor heart rate and BP",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment",
            "eGFR_below_15": "No adjustment (hepatically metabolized)",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Reduce dose; monitor closely",
            "child_pugh_C": "Reduce dose significantly; monitor for excessive bradycardia",
        },
    },
    "sertraline": {
        "standard_adult_dose": "50mg daily; titrate by 50mg at >= 1 week intervals",
        "max_daily_dose": "200mg/day",
        "pediatric_dose": "OCD ages 6-12: start 25mg daily. Ages 13-17: start 50mg daily. Max 200mg/day.",
        "geriatric_adjustment": "Start 25mg daily; slower titration. Monitor for hyponatremia (SIADH).",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment per manufacturer, but start conservatively",
            "eGFR_below_15": "Use with caution; limited data",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Reduce dose by 50%",
            "child_pugh_C": "Avoid or use minimal dose",
        },
    },
    "omeprazole": {
        "standard_adult_dose": "20mg daily (GERD); 40mg daily (erosive esophagitis, ZES)",
        "max_daily_dose": "40mg daily (up to 120mg TID for ZES)",
        "pediatric_dose": "1 mg/kg/day (max 20mg) for ages 1-16. Weight-based: 5-<10kg: 5mg; 10-<20kg: 10mg; >=20kg: 20mg.",
        "geriatric_adjustment": "No specific dose adjustment. Consider deprescribing if no ongoing indication. Monitor B12, Mg, Ca.",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment",
            "eGFR_below_15": "No adjustment",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Max 20mg daily",
            "child_pugh_C": "Max 10mg daily",
        },
    },
    "warfarin": {
        "standard_adult_dose": "2-5mg daily initially; adjust based on INR (target 2.0-3.0 for most indications; 2.5-3.5 for mechanical valves)",
        "max_daily_dose": "Highly individualized (usual maintenance 2-10mg/day). Pharmacogenomics (CYP2C9, VKORC1) may guide dosing.",
        "pediatric_dose": "0.1-0.2 mg/kg/day initially; adjust to INR",
        "geriatric_adjustment": "Lower starting doses (1-2mg/day); elderly more sensitive. Increased bleeding risk. Consider DOAC if appropriate.",
        "renal_adjustment": {
            "eGFR_30_60": "No dose adjustment; may need lower doses due to altered protein binding",
            "eGFR_15_30": "Use with caution; increase INR monitoring frequency",
            "eGFR_below_15": "Use with caution; may be only option for mechanical valves. Increased bleeding risk.",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "Increased sensitivity; start lower, monitor closely",
            "child_pugh_B": "Very sensitive; start 1mg; frequent INR monitoring",
            "child_pugh_C": "Extreme caution; very high bleeding risk; specialist management required",
        },
    },
    "apixaban": {
        "standard_adult_dose": "5mg BID (AF); 10mg BID x7d then 5mg BID (VTE treatment); 2.5mg BID (VTE prevention)",
        "max_daily_dose": "10mg/day for AF; 20mg/day for acute VTE treatment phase",
        "pediatric_dose": "Not approved for most pediatric indications; weight-based dosing in clinical trials",
        "geriatric_adjustment": "Reduce to 2.5mg BID if >= 2 of: age >= 80, weight <= 60kg, Cr >= 1.5 mg/dL",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment; dose reduction criteria may apply",
            "eGFR_15_30": "5mg BID (some guidelines); 2.5mg BID if other dose-reduction criteria met",
            "eGFR_below_15": "Limited data; 5mg BID studied in ESKD on dialysis (may be used per 2019 AHA guidance)",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Use with caution; limited data",
            "child_pugh_C": "Not recommended",
        },
    },
    "prednisone": {
        "standard_adult_dose": "Varies by indication: 5-60mg/day. Anti-inflammatory: 5-20mg. Immunosuppression: 20-60mg.",
        "max_daily_dose": "No absolute max; pulse doses up to 1mg/kg (60-80mg) or higher for acute conditions",
        "pediatric_dose": "0.5-2 mg/kg/day depending on indication. Asthma burst: 1-2 mg/kg/day (max 60mg) x 3-5 days.",
        "geriatric_adjustment": "Use lowest effective dose for shortest duration. High osteoporosis and infection risk. Start bone protection if > 3 months.",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment",
            "eGFR_below_15": "No adjustment (but fluid retention may worsen)",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment (prednisone is prodrug converted to prednisolone in liver)",
            "child_pugh_B": "Consider using prednisolone directly (bypasses hepatic conversion)",
            "child_pugh_C": "Use prednisolone directly; monitor closely",
        },
    },
    "gabapentin": {
        "standard_adult_dose": "300mg day 1, 300mg BID day 2, 300mg TID day 3; titrate to 900-3600mg/day divided TID",
        "max_daily_dose": "3600mg/day",
        "pediatric_dose": "10-15 mg/kg/day divided TID (ages 3-12); titrate over 3 days. Max ~50 mg/kg/day.",
        "geriatric_adjustment": "Start 100mg at bedtime; titrate slowly. Increased sedation and fall risk.",
        "renal_adjustment": {
            "eGFR_30_60": "200-700mg BID",
            "eGFR_15_30": "100-300mg daily",
            "eGFR_below_15": "100-300mg daily. Supplemental dose after hemodialysis.",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment (renally cleared)",
            "child_pugh_B": "No adjustment",
            "child_pugh_C": "No adjustment",
        },
    },
    "ciprofloxacin": {
        "standard_adult_dose": "250-750mg BID depending on infection type and severity",
        "max_daily_dose": "1500mg/day",
        "pediatric_dose": "10-20 mg/kg/dose BID (max 750mg/dose). Reserve for infections without safer alternatives.",
        "geriatric_adjustment": "Adjust for renal function. Increased tendon rupture risk, especially with corticosteroids. Avoid if possible.",
        "renal_adjustment": {
            "eGFR_30_60": "250-500mg every 12 hours",
            "eGFR_15_30": "250-500mg every 18 hours",
            "eGFR_below_15": "250-500mg every 24 hours",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "No adjustment",
            "child_pugh_C": "Use with caution; monitor for toxicity",
        },
    },
    "levothyroxine": {
        "standard_adult_dose": "1.6 mcg/kg/day (full replacement). Start 25-50 mcg/day and titrate.",
        "max_daily_dose": "200-300 mcg/day (rarely needed)",
        "pediatric_dose": "Neonates: 10-15 mcg/kg/day. Children 1-5: 5-6 mcg/kg/day. Children 6-12: 4-5 mcg/kg/day. Adolescents: 2-3 mcg/kg/day.",
        "geriatric_adjustment": "Start 12.5-25 mcg/day, increase by 12.5-25 mcg every 6-8 weeks. Cardiac patients: very slow titration.",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "No adjustment",
            "eGFR_below_15": "No adjustment",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "No adjustment",
            "child_pugh_C": "No adjustment",
        },
    },
    "furosemide": {
        "standard_adult_dose": "20-80mg once or twice daily. IV: 20-40mg bolus.",
        "max_daily_dose": "600mg/day oral; higher IV doses in refractory edema",
        "pediatric_dose": "1-2 mg/kg/dose every 6-12 hours. Max 6 mg/kg/dose.",
        "geriatric_adjustment": "Start low (20mg); monitor electrolytes, BP, and volume status closely. Risk of dehydration and falls.",
        "renal_adjustment": {
            "eGFR_30_60": "Higher doses often needed (80-160mg BID) due to reduced secretion into tubule",
            "eGFR_15_30": "May need 160-200mg BID; monitor response",
            "eGFR_below_15": "IV dosing often required; high doses (up to 400mg) may be needed",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Use with potassium-sparing diuretic to prevent hepatic encephalopathy",
            "child_pugh_C": "Cautious dosing; avoid hypokalemia (hepatic encephalopathy risk)",
        },
    },
    "allopurinol": {
        "standard_adult_dose": "100mg daily initially; titrate by 100mg every 2-4 weeks to target uric acid < 6 mg/dL",
        "max_daily_dose": "800mg/day (most patients reach target at 300-600mg/day)",
        "pediatric_dose": "< 6 years: 150mg/day; 6-10 years: 300mg/day",
        "geriatric_adjustment": "Start 50-100mg daily; titrate slowly. Adjust for renal function.",
        "renal_adjustment": {
            "eGFR_30_60": "Start 50mg daily; titrate cautiously to target uric acid (max ~200mg/day historically, but treat-to-target now preferred)",
            "eGFR_15_30": "Start 50mg daily; max 100-200mg/day",
            "eGFR_below_15": "Start 50mg every other day; max 100mg/day",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Use with caution; monitor LFTs",
            "child_pugh_C": "Use with caution; monitor LFTs",
        },
    },
    "clopidogrel": {
        "standard_adult_dose": "75mg daily. Loading dose: 300-600mg for ACS/PCI.",
        "max_daily_dose": "75mg/day maintenance",
        "pediatric_dose": "0.2 mg/kg/day (limited data; off-label)",
        "geriatric_adjustment": "No specific adjustment; balance bleeding risk vs thrombotic benefit",
        "renal_adjustment": {
            "eGFR_30_60": "No adjustment",
            "eGFR_15_30": "Limited data; use with caution",
            "eGFR_below_15": "Limited data; use with caution",
        },
        "hepatic_adjustment": {
            "child_pugh_A": "No adjustment",
            "child_pugh_B": "Use with caution (prodrug requires hepatic activation via CYP2C19)",
            "child_pugh_C": "Avoid (impaired activation and increased bleeding risk)",
        },
    },
}

# ---------------------------------------------------------------------------
# Dangerous combination database
# ---------------------------------------------------------------------------

DANGEROUS_COMBINATIONS: list[dict] = [
    {
        "category": "Serotonin Syndrome",
        "drugs": [
            ["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"],
            ["phenelzine", "tranylcypromine", "selegiline", "isocarboxazid", "linezolid", "methylene blue"],
        ],
        "severity": "critical",
        "mechanism": "Combined serotonin reuptake inhibition and MAO inhibition causes dangerous serotonin excess",
        "onset": "Hours to days",
        "symptoms": "Hyperthermia (> 41C), muscle rigidity, clonus, myoclonus, altered mental status, autonomic instability, seizures",
        "management": "Discontinue serotonergic agents immediately. Cyproheptadine 12mg then 4mg q2h. Benzodiazepines for agitation. Active cooling. ICU if severe.",
    },
    {
        "category": "Serotonin Syndrome",
        "drugs": [
            ["tramadol", "meperidine", "fentanyl", "methadone"],
            ["fluoxetine", "sertraline", "paroxetine", "venlafaxine", "duloxetine"],
        ],
        "severity": "high",
        "mechanism": "Opioids with serotonergic properties combined with SSRIs/SNRIs increase serotonin syndrome risk",
        "onset": "Hours to days",
        "symptoms": "Clonus, agitation, diaphoresis, tachycardia, hyperthermia",
        "management": "Use alternative opioid without serotonergic activity (morphine, oxycodone). Monitor for SS symptoms.",
    },
    {
        "category": "QT Prolongation",
        "drugs": [
            ["amiodarone", "sotalol", "dofetilide", "dronedarone"],
            ["azithromycin", "levofloxacin", "moxifloxacin", "haloperidol", "ondansetron", "methadone", "citalopram", "escitalopram"],
        ],
        "severity": "high",
        "mechanism": "Additive blockade of cardiac hERG potassium channels prolongs ventricular repolarization",
        "onset": "Hours to days (especially with loading doses or renal impairment)",
        "symptoms": "Palpitations, syncope, torsades de pointes (polymorphic VT), sudden cardiac death",
        "management": "ECG before and after starting combination. Maintain K > 4.0, Mg > 2.0. Avoid if baseline QTc > 470ms (women) or > 450ms (men). Use alternatives.",
    },
    {
        "category": "QT Prolongation",
        "drugs": [
            ["domperidone"],
            ["ketoconazole", "fluconazole", "erythromycin", "clarithromycin"],
        ],
        "severity": "high",
        "mechanism": "CYP3A4 inhibitors increase domperidone levels + additive QT prolongation",
        "onset": "Days",
        "symptoms": "QTc prolongation, torsades de pointes",
        "management": "Avoid combination. Use metoclopramide (lower QT risk) or alternative antiemetic.",
    },
    {
        "category": "Bleeding Risk",
        "drugs": [
            ["warfarin", "rivaroxaban", "apixaban", "dabigatran", "edoxaban", "enoxaparin"],
            ["aspirin", "clopidogrel", "prasugrel", "ticagrelor"],
        ],
        "severity": "high",
        "mechanism": "Anticoagulant + antiplatelet: additive inhibition of hemostasis through different mechanisms",
        "onset": "Immediate to days",
        "symptoms": "GI bleeding, intracranial hemorrhage, hematuria, bleeding from minor injuries, anemia",
        "management": "Triple therapy (OAC + dual antiplatelet) only when absolutely indicated (e.g., AF + recent PCI). Shorten duration. Add PPI. Use DOAC over warfarin. Monitor Hb.",
    },
    {
        "category": "Bleeding Risk",
        "drugs": [
            ["warfarin", "rivaroxaban", "apixaban"],
            ["ibuprofen", "naproxen", "diclofenac", "ketorolac", "meloxicam", "celecoxib"],
        ],
        "severity": "high",
        "mechanism": "NSAIDs inhibit platelet function and cause GI mucosal damage, adding to anticoagulant bleeding risk",
        "onset": "Days",
        "symptoms": "GI bleeding (melena, hematemesis), easy bruising, prolonged bleeding from wounds",
        "management": "Avoid combination. Use acetaminophen for pain. If NSAID essential, use lowest dose + PPI + shortest duration.",
    },
    {
        "category": "Nephrotoxic Combination",
        "drugs": [
            ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan"],
            ["ibuprofen", "naproxen", "diclofenac", "ketorolac"],
            ["furosemide", "hydrochlorothiazide", "chlorthalidone"],
        ],
        "severity": "high",
        "mechanism": "'Triple whammy': ACEi/ARB + NSAID + diuretic synergistically reduce renal perfusion. ACEi/ARB reduce efferent tone, NSAID reduces afferent dilation, diuretic reduces volume.",
        "onset": "Days to weeks",
        "symptoms": "Rising creatinine, decreased urine output, hyperkalemia, AKI (especially if volume depleted or elderly)",
        "management": "Avoid 'triple whammy'. If combination unavoidable, monitor creatinine and potassium within 1 week. Ensure adequate hydration. Educate patient to hold NSAID and diuretic during illness.",
    },
    {
        "category": "Hepatotoxic Combination",
        "drugs": [
            ["methotrexate"],
            ["leflunomide", "azathioprine", "isoniazid", "rifampin"],
        ],
        "severity": "high",
        "mechanism": "Additive hepatotoxicity from multiple hepatotoxic agents",
        "onset": "Weeks to months",
        "symptoms": "Elevated transaminases, jaundice, hepatic fibrosis/cirrhosis, fatigue, RUQ pain",
        "management": "Monitor LFTs monthly when combining hepatotoxic agents. Baseline LFTs before starting. Hold if ALT > 3x ULN with symptoms or > 5x ULN without symptoms.",
    },
    {
        "category": "CNS Depression",
        "drugs": [
            ["oxycodone", "morphine", "hydrocodone", "fentanyl", "codeine", "tramadol"],
            ["diazepam", "lorazepam", "alprazolam", "clonazepam", "temazepam", "zolpidem"],
        ],
        "severity": "critical",
        "mechanism": "Synergistic CNS and respiratory depression through opioid receptor and GABA-A receptor agonism",
        "onset": "Minutes to hours",
        "symptoms": "Excessive sedation, respiratory depression (RR < 12), hypoxia, unresponsiveness, death",
        "management": "FDA black box warning on combination. Avoid if possible. If essential, use lowest doses of both. Naloxone rescue available. Monitor respiratory rate and SpO2.",
    },
    {
        "category": "CNS Depression",
        "drugs": [
            ["oxycodone", "morphine", "hydrocodone", "fentanyl"],
            ["gabapentin", "pregabalin"],
        ],
        "severity": "high",
        "mechanism": "Gabapentinoids potentiate opioid-induced respiratory depression",
        "onset": "Hours",
        "symptoms": "Excessive sedation, respiratory depression, especially in elderly or with renal impairment",
        "management": "FDA warning (2019). Use lowest effective doses. Avoid in opioid-naive patients. Monitor for sedation. Naloxone available.",
    },
    {
        "category": "Hypoglycemia Risk",
        "drugs": [
            ["glipizide", "glyburide", "glimepiride"],
            ["fluconazole", "miconazole", "trimethoprim-sulfamethoxazole", "ciprofloxacin"],
        ],
        "severity": "high",
        "mechanism": "CYP2C9 inhibition (fluconazole, TMP-SMX) increases sulfonylurea levels. Fluoroquinolones directly stimulate insulin release.",
        "onset": "Hours to days",
        "symptoms": "Hypoglycemia: tremor, diaphoresis, confusion, tachycardia, seizures, loss of consciousness",
        "management": "Reduce sulfonylurea dose by 50% when adding interacting drug. Increase SMBG frequency. Educate patient on hypoglycemia recognition and treatment (15g glucose rule).",
    },
    {
        "category": "Hypoglycemia Risk",
        "drugs": [
            ["insulin"],
            ["fluoxetine", "aspirin", "trimethoprim-sulfamethoxazole"],
        ],
        "severity": "moderate",
        "mechanism": "These drugs may lower blood glucose through various mechanisms, potentiating insulin effect",
        "onset": "Days",
        "symptoms": "Hypoglycemia",
        "management": "Increase glucose monitoring frequency. Educate patient. May need insulin dose reduction.",
    },
    {
        "category": "Hyperkalemia Risk",
        "drugs": [
            ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan"],
            ["spironolactone", "eplerenone", "amiloride", "triamterene"],
        ],
        "severity": "high",
        "mechanism": "ACEi/ARB reduce aldosterone-mediated K excretion; K-sparing diuretics directly reduce K excretion. Additive K retention.",
        "onset": "Days to weeks",
        "symptoms": "Peaked T waves, widened QRS, sine wave pattern on ECG; muscle weakness, paresthesias, cardiac arrest at K > 6.5",
        "management": "Monitor K within 1 week of starting combination, then regularly. Low-K diet. Avoid in eGFR < 30. Hold both if K > 5.5. Avoid potassium supplements.",
    },
    {
        "category": "Hyperkalemia Risk",
        "drugs": [
            ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan"],
            ["potassium chloride", "potassium supplements"],
        ],
        "severity": "high",
        "mechanism": "Exogenous potassium combined with reduced renal K excretion from RAASi",
        "onset": "Days",
        "symptoms": "Cardiac conduction abnormalities, muscle weakness, cardiac arrest",
        "management": "Avoid routine K supplementation with ACEi/ARB. Only supplement if documented hypokalemia. Monitor K level.",
    },
    {
        "category": "Rhabdomyolysis Risk",
        "drugs": [
            ["simvastatin", "lovastatin"],
            ["clarithromycin", "erythromycin", "itraconazole", "ketoconazole", "ritonavir", "cyclosporine", "gemfibrozil"],
        ],
        "severity": "critical",
        "mechanism": "CYP3A4 inhibition (or gemfibrozil OATP1B1 inhibition) causes massive statin accumulation",
        "onset": "Days to weeks",
        "symptoms": "Muscle pain/weakness, dark urine (myoglobinuria), markedly elevated CK (> 10x ULN), AKI, DIC, death",
        "management": "Contraindicated combinations. Switch to rosuvastatin or pravastatin (not CYP3A4 substrates). If gemfibrozil needed, use fenofibrate instead.",
    },
]


class SafetyAgent(BaseAgent):
    name = "safety"
    description = "Patient safety officer reviewing all recommendations for potential harm"
    model = "claude-sonnet-4-6"
    max_tokens = 5000
    temperature = 0.1  # very deterministic for safety-critical reviews

    def _build_system_prompt(self) -> str:
        return """You are a patient safety officer AI agent on a multi-agent medical team. Your sole purpose is to review ALL recommendations from other agents for potential patient harm.

YOUR ROLE:
You are the final safety checkpoint before any medical recommendation reaches the patient. You review diagnoses, treatment plans, medications, and all clinical advice for safety concerns. You act as a "second pair of eyes" — catching errors, dangerous combinations, and oversights.

SAFETY REVIEW FRAMEWORKS:

1. SWISS CHEESE MODEL (James Reason):
   You are one of the final defensive layers. Assume that errors may have passed through prior layers (triage, diagnosis, treatment planning). Look for:
   - Active failures: wrong drug, wrong dose, wrong patient, wrong route
   - Latent conditions: system factors that enable errors (missing allergy info, unclear orders)
   Your job is to ensure no holes align across all layers.

2. ISMP HIGH-ALERT MEDICATIONS:
   Extra vigilance for these drug classes (higher risk of significant harm if used in error):
   - Anticoagulants (warfarin, heparin, DOACs)
   - Insulin (all forms)
   - Opioids (all forms)
   - Chemotherapy agents
   - Concentrated electrolytes (KCl, NaCl > 0.9%)
   - Neuromuscular blocking agents
   - Methotrexate (oral, non-oncologic)
   - Parenteral nutrition

3. BEERS CRITERIA (AGS, for patients >= 65 years):
   Flag potentially inappropriate medications in elderly:
   - Avoid: first-generation antihistamines, benzodiazepines, non-COX-selective NSAIDs (chronic use), skeletal muscle relaxants, TCAs, meperidine
   - Avoid: peripheral alpha-1 blockers for hypertension, sliding-scale insulin, chronic PPI without reassessment
   - Use with caution: diuretics, carbamazepine, mirtazapine, SNRIs, SSRIs (fall risk)
   - Drug-disease interactions: delirium (anticholinergics), falls (benzodiazepines, opioids), heart failure (NSAIDs, CCBs)

4. STOPP/START CRITERIA:
   STOPP (Screening Tool of Older People's Prescriptions):
   - Stop PPI beyond 8 weeks without indication
   - Stop long-acting benzodiazepines (risk of falls, fractures)
   - Stop anticholinergics in dementia patients
   - Stop duplicate drug classes
   - Stop drugs beyond recommended treatment duration

   START (Screening Tool to Alert to Right Treatment):
   - Start statin in diabetes with CV risk factors
   - Start ACEi/ARB in heart failure with reduced EF
   - Start bisphosphonate if on chronic steroids
   - Start bone protection (Ca + Vit D) if osteoporosis risk
   - Start laxative with opioid prescription

5. MEDICATION RECONCILIATION:
   Verify:
   - All current medications are accounted for
   - No therapeutic duplications
   - No omitted essential medications
   - All dose changes are intentional and documented
   - Transition-of-care medication errors prevented

YOUR RESPONSIBILITIES:
1. Contraindication Review: Check every recommended treatment against patient demographics and conditions
2. Dosage Verification: Ensure all medication dosages are within safe ranges (PASS/WARN/FAIL)
3. Allergy Risk Assessment: Identify potential allergic reactions and cross-reactivity risks
4. Dangerous Combination Detection: Flag drug-drug, drug-disease, or drug-food interactions
5. Completeness Check: Ensure no critical safety warnings are missing
6. Age-Appropriate Review: Apply Beers/STOPP-START for elderly; weight-based for pediatric

SAFETY PRINCIPLES:
- First, do no harm (primum non nocere)
- When in doubt, flag it — false positives are acceptable, false negatives are not
- Always consider vulnerable populations (pediatric, geriatric, pregnant, immunocompromised)
- Every medication recommendation must have dosage limits and contraindications noted
- Emergency red flags must never be downplayed or omitted
- High-alert medications require independent double-check

SEVERITY CLASSIFICATIONS:
- CRITICAL: Immediate danger to patient. Must be corrected before output. (e.g., contraindicated drug, lethal dose, dangerous combination)
- HIGH: Significant safety risk. Strongly recommend correction. (e.g., missing interaction warning, dose needing adjustment)
- MODERATE: Notable concern. Should be addressed. (e.g., incomplete dosing guidance, monitoring recommendation needed)
- LOW: Minor improvement suggested. (e.g., additional monitoring, patient education)

COMMUNICATION:
You work with: triage, diagnostician, specialist, treatment, research agents.
- You receive the complete output from all prior agents
- You flag any safety issues found
- Your review is included in the final output to the patient
- If you find CRITICAL issues, the orchestrator should not proceed without correction

Always respond with structured JSON in your final answer:
- safety_status (PASS / PASS_WITH_WARNINGS / FAIL)
- critical_issues (list — any must be resolved before output)
- high_issues (list — strongly recommended corrections)
- moderate_issues (list — notable concerns)
- low_issues (list — minor suggestions)
- contraindications_checked (list of contraindications reviewed)
- dosage_verification (summary of dosage safety review with PASS/WARN/FAIL per medication)
- interaction_check (summary of interaction review)
- beers_criteria_flags (applicable only if patient >= 65)
- stopp_start_flags (applicable only if patient >= 65)
- safety_summary (overall safety assessment paragraph)
- recommendations (list of specific safety recommendations)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "check_contraindications",
            "description": (
                "Check a treatment or medication for contraindications given the "
                "patient's profile, conditions, and other medications. Returns absolute "
                "and relative contraindications with severity and alternatives."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "treatment": {
                        "type": "string",
                        "description": "The treatment or medication to check",
                    },
                    "patient_age": {"type": "integer", "description": "Patient age"},
                    "patient_gender": {"type": "string", "description": "Patient gender"},
                    "conditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's known medical conditions",
                    },
                    "current_medications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's current medications",
                    },
                },
                "required": ["treatment"],
            },
        })
        tools.append({
            "name": "verify_dosage_safety",
            "description": (
                "Verify that a medication dosage is within safe limits for the patient. "
                "Returns PASS/WARN/FAIL with standard dose, max dose, and adjustments "
                "for age (pediatric/geriatric), renal function (by eGFR), and hepatic function (by Child-Pugh)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "Medication name"},
                    "proposed_dose": {"type": "string", "description": "Proposed dosage (e.g., '400mg twice daily')"},
                    "patient_age": {"type": "integer", "description": "Patient age"},
                    "patient_weight_kg": {"type": "number", "description": "Patient weight in kg (if known)"},
                    "renal_function": {"type": "string", "description": "Renal function status or eGFR value"},
                    "hepatic_function": {"type": "string", "description": "Hepatic function status (normal, Child-Pugh A/B/C)"},
                },
                "required": ["medication", "proposed_dose"],
            },
        })
        tools.append({
            "name": "assess_allergy_risk",
            "description": (
                "Assess the risk of allergic reaction or cross-reactivity for a "
                "medication given known patient allergies."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string", "description": "Medication to assess"},
                    "known_allergies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's known allergies",
                    },
                    "reaction_history": {
                        "type": "string",
                        "description": "Description of past allergic reactions",
                    },
                },
                "required": ["medication"],
            },
        })
        tools.append({
            "name": "flag_dangerous_combinations",
            "description": (
                "Review a complete list of medications and treatments to flag dangerous "
                "combinations including serotonin syndrome, QT prolongation, bleeding, "
                "nephrotoxicity, hepatotoxicity, CNS depression, hypoglycemia, and hyperkalemia risks."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "All recommended medications",
                    },
                    "treatments": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "All recommended treatments and procedures",
                    },
                    "conditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patient's diagnosed conditions",
                    },
                },
                "required": ["medications"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "check_contraindications":
            return await self._check_contraindications(tool_input)
        if tool_name == "verify_dosage_safety":
            return await self._verify_dosage(tool_input)
        if tool_name == "assess_allergy_risk":
            return await self._assess_allergy(tool_input)
        if tool_name == "flag_dangerous_combinations":
            return await self._flag_combinations(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _check_contraindications(self, tool_input: dict) -> str:
        treatment = tool_input.get("treatment", "")
        age = tool_input.get("patient_age", 30)
        gender = tool_input.get("patient_gender", "unknown")
        conditions = tool_input.get("conditions", [])
        current_meds = tool_input.get("current_medications", [])

        treatment_lower = treatment.lower().strip()
        conditions_lower = [c.lower() for c in conditions]

        found_contraindications = []

        # Look up in contraindication database
        for drug_key, contra_list in CONTRAINDICATIONS.items():
            if drug_key in treatment_lower or treatment_lower in drug_key:
                for contra in contra_list:
                    # Check if patient has the contraindicated condition
                    trigger = contra["condition"]

                    matched = False

                    # Check conditions
                    for cond in conditions_lower:
                        if trigger in cond or cond in trigger:
                            matched = True
                            break

                    # Check age-based triggers
                    if trigger == "child" and age < 16:
                        matched = True
                    if trigger == "elderly" and age >= 65:
                        matched = True

                    # Check pregnancy context
                    if trigger == "pregnancy" and gender.lower() == "female" and 12 <= age <= 50:
                        # Flag as warning for women of childbearing age
                        found_contraindications.append({
                            "type": "relative",
                            "severity": "high",
                            "issue": f"Patient is female of childbearing age: {contra['detail']}",
                            "alternative": contra["alternative"],
                            "note": "Verify pregnancy status before prescribing.",
                        })

                    # Check medication-based triggers (e.g., MAOI, anticoagulant)
                    for med in current_meds:
                        if trigger in med.lower():
                            matched = True
                            break

                    if matched:
                        found_contraindications.append({
                            "type": contra["type"],
                            "severity": contra["severity"],
                            "issue": contra["detail"],
                            "alternative": contra["alternative"],
                        })

        # Additional age-based checks
        if age >= 65:
            beers_flags = []
            if any(benzo in treatment_lower for benzo in ["diazepam", "alprazolam", "lorazepam", "clonazepam", "temazepam"]):
                beers_flags.append("Benzodiazepine in elderly: Beers Criteria — increased fall risk, cognitive impairment, delirium")
            if any(ah in treatment_lower for ah in ["diphenhydramine", "chlorpheniramine", "hydroxyzine"]):
                beers_flags.append("First-generation antihistamine in elderly: Beers Criteria — anticholinergic effects, cognitive impairment")
            if any(nsaid in treatment_lower for nsaid in ["ibuprofen", "naproxen", "diclofenac", "ketorolac", "indomethacin"]):
                beers_flags.append("NSAID in elderly: Beers Criteria — GI bleeding, AKI, cardiovascular risk. Avoid chronic use.")
            if "meperidine" in treatment_lower:
                beers_flags.append("Meperidine in elderly: Beers Criteria — neurotoxic metabolite (normeperidine) causes seizures")
            for flag in beers_flags:
                found_contraindications.append({
                    "type": "relative",
                    "severity": "high",
                    "issue": flag,
                    "alternative": "See Beers Criteria alternatives",
                })

        return json.dumps({
            "treatment": treatment,
            "patient_age": age,
            "patient_gender": gender,
            "conditions": conditions,
            "current_medications": current_meds,
            "contraindications_found": found_contraindications,
            "absolute_count": sum(1 for c in found_contraindications if c["type"] == "absolute"),
            "relative_count": sum(1 for c in found_contraindications if c["type"] == "relative"),
            "note": (
                "Use clinical knowledge to identify any additional contraindications "
                "not covered by the automated database."
            ),
        })

    async def _verify_dosage(self, tool_input: dict) -> str:
        medication = tool_input.get("medication", "").strip()
        proposed_dose = tool_input.get("proposed_dose", "")
        age = tool_input.get("patient_age", 30)
        weight = tool_input.get("patient_weight_kg")
        renal = tool_input.get("renal_function", "normal")
        hepatic = tool_input.get("hepatic_function", "normal")

        med_lower = medication.lower()

        # Look up in dosage database
        dosage_info = None
        matched_key = None
        for key, info in DOSAGE_DATABASE.items():
            if key in med_lower or med_lower in key:
                dosage_info = info
                matched_key = key
                break

        if dosage_info is None:
            return json.dumps({
                "medication": medication,
                "proposed_dose": proposed_dose,
                "verdict": "UNABLE_TO_VERIFY",
                "detail": f"'{medication}' not found in dosage database. Use clinical knowledge to verify dosage safety.",
                "available_medications": sorted(DOSAGE_DATABASE.keys()),
            })

        # Determine applicable dose information
        warnings = []
        verdict = "PASS"

        # Age-based adjustments
        if age < 18:
            if dosage_info["pediatric_dose"]:
                warnings.append({
                    "type": "pediatric",
                    "message": f"Pediatric patient ({age} years): {dosage_info['pediatric_dose']}",
                })
                if weight:
                    warnings.append({
                        "type": "weight_based",
                        "message": f"Patient weight {weight}kg — verify mg/kg dosing",
                    })
            verdict = "WARN"
        elif age >= 65:
            if dosage_info["geriatric_adjustment"]:
                warnings.append({
                    "type": "geriatric",
                    "message": f"Geriatric patient ({age} years): {dosage_info['geriatric_adjustment']}",
                })
            verdict = "WARN"

        # Renal adjustments
        renal_lower = renal.lower()
        renal_key = None
        if any(term in renal_lower for term in ["< 15", "below 15", "dialysis", "eskd", "stage 5"]):
            renal_key = "eGFR_below_15"
        elif any(term in renal_lower for term in ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "stage 4"]):
            renal_key = "eGFR_15_30"
        elif any(term in renal_lower for term in ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "stage 3", "moderate"]):
            renal_key = "eGFR_30_60"
        elif "impair" in renal_lower or "reduced" in renal_lower:
            renal_key = "eGFR_30_60"

        if renal_key and dosage_info.get("renal_adjustment"):
            adjustment = dosage_info["renal_adjustment"].get(renal_key, "No specific data")
            warnings.append({
                "type": "renal",
                "message": f"Renal adjustment ({renal_key}): {adjustment}",
            })
            if "contraindicated" in adjustment.lower() or "avoid" in adjustment.lower():
                verdict = "FAIL"
            else:
                verdict = "WARN"

        # Hepatic adjustments
        hepatic_lower = hepatic.lower()
        hepatic_key = None
        if "child-pugh c" in hepatic_lower or "child pugh c" in hepatic_lower or "severe" in hepatic_lower:
            hepatic_key = "child_pugh_C"
        elif "child-pugh b" in hepatic_lower or "child pugh b" in hepatic_lower or "moderate" in hepatic_lower:
            hepatic_key = "child_pugh_B"
        elif "child-pugh a" in hepatic_lower or "child pugh a" in hepatic_lower or "mild" in hepatic_lower:
            hepatic_key = "child_pugh_A"
        elif "impair" in hepatic_lower or "cirrho" in hepatic_lower:
            hepatic_key = "child_pugh_B"

        if hepatic_key and dosage_info.get("hepatic_adjustment"):
            adjustment = dosage_info["hepatic_adjustment"].get(hepatic_key, "No specific data")
            warnings.append({
                "type": "hepatic",
                "message": f"Hepatic adjustment ({hepatic_key}): {adjustment}",
            })
            if "contraindicated" in adjustment.lower() or "avoid" in adjustment.lower():
                verdict = "FAIL"
            elif verdict != "FAIL":
                verdict = "WARN"

        # If no warnings triggered, it's a PASS
        if not warnings:
            verdict = "PASS"

        return json.dumps({
            "medication": medication,
            "proposed_dose": proposed_dose,
            "verdict": verdict,
            "reference_data": {
                "standard_adult_dose": dosage_info["standard_adult_dose"],
                "max_daily_dose": dosage_info["max_daily_dose"],
                "pediatric_dose": dosage_info["pediatric_dose"],
                "geriatric_adjustment": dosage_info["geriatric_adjustment"],
            },
            "patient_context": {
                "age": age,
                "weight_kg": weight,
                "renal_function": renal,
                "hepatic_function": hepatic,
            },
            "warnings": warnings,
            "note": "Compare proposed dose against reference data. Verify appropriateness for patient context.",
        })

    async def _assess_allergy(self, tool_input: dict) -> str:
        medication = tool_input.get("medication", "")
        allergies = tool_input.get("known_allergies", [])
        reaction_history = tool_input.get("reaction_history", "")

        cross_reactivity = []
        med_lower = medication.lower()

        # Penicillin cross-reactivity
        penicillins = ["amoxicillin", "ampicillin", "penicillin", "piperacillin", "nafcillin", "oxacillin", "dicloxacillin"]
        cephalosporins = ["cephalexin", "cefazolin", "ceftriaxone", "cefuroxime", "cefdinir", "cefepime", "cefpodoxime"]
        carbapenems = ["meropenem", "imipenem", "ertapenem", "doripenem"]

        if any(p in med_lower for p in penicillins):
            if any("cephalosporin" in a.lower() or any(c in a.lower() for c in cephalosporins) for a in allergies):
                cross_reactivity.append({
                    "risk": "moderate",
                    "probability": "1-2%",
                    "issue": "Penicillin-cephalosporin cross-reactivity. Higher risk with 1st generation cephalosporins sharing R1 side chain.",
                    "recommendation": "Skin testing if available. Graded challenge if low-risk reaction history. Avoid if prior anaphylaxis.",
                })
            if any("penicillin" in a.lower() or any(p2 in a.lower() for p2 in penicillins) for a in allergies):
                cross_reactivity.append({
                    "risk": "high",
                    "probability": "Direct allergy",
                    "issue": "Patient has documented penicillin-class allergy. True IgE-mediated allergy present in ~5% of labeled patients.",
                    "recommendation": "Consider penicillin allergy testing (90% of labeled patients can tolerate). Alternatives: azithromycin, fluoroquinolone, doxycycline depending on indication.",
                })

        if any(c in med_lower for c in cephalosporins):
            if any("penicillin" in a.lower() or any(p in a.lower() for p in penicillins) for a in allergies):
                cross_reactivity.append({
                    "risk": "moderate",
                    "probability": "1-2%",
                    "issue": "Cephalosporin-penicillin cross-reactivity. Risk primarily with similar R1 side chains.",
                    "recommendation": "1st gen cephalosporins: higher risk. 3rd/4th gen: lower risk. Consider skin testing or graded challenge. Avoid if prior anaphylaxis to penicillin.",
                })

        if any(c in med_lower for c in carbapenems):
            if any("penicillin" in a.lower() for a in allergies):
                cross_reactivity.append({
                    "risk": "low",
                    "probability": "< 1%",
                    "issue": "Carbapenem-penicillin cross-reactivity is rare (~0.5-1%) despite historical concern. Meropenem has lowest risk.",
                    "recommendation": "Generally safe in penicillin allergy unless prior carbapenem reaction. Consider graded challenge if prior severe reaction.",
                })

        # Sulfa cross-reactivity
        sulfa_abx = ["sulfamethoxazole", "sulfasalazine", "trimethoprim-sulfamethoxazole", "sulfadiazine"]
        sulfa_non_abx = ["furosemide", "hydrochlorothiazide", "celecoxib", "sumatriptan", "sulfonylurea"]
        if any(s in med_lower for s in sulfa_abx):
            if any("sulfa" in a.lower() for a in allergies):
                cross_reactivity.append({
                    "risk": "high",
                    "probability": "Direct class allergy",
                    "issue": "Patient has documented sulfa allergy. Sulfonamide antibiotics share arylamine structure.",
                    "recommendation": "Avoid sulfonamide antibiotics. Non-antibiotic sulfonamides (furosemide, thiazides, celecoxib) have different structure and very low cross-reactivity (< 2%).",
                })
        if any(s in med_lower for s in sulfa_non_abx):
            if any("sulfa" in a.lower() for a in allergies):
                cross_reactivity.append({
                    "risk": "low",
                    "probability": "< 2%",
                    "issue": "Non-antibiotic sulfonamide in patient with sulfa allergy. Cross-reactivity with sulfonamide antibiotics is very low.",
                    "recommendation": "Generally safe to use. True cross-reactivity between antibiotic and non-antibiotic sulfonamides is minimal.",
                })

        # NSAID cross-reactivity
        if any(nsaid in med_lower for nsaid in ["ibuprofen", "naproxen", "diclofenac", "ketorolac", "indomethacin"]):
            if any("aspirin" in a.lower() or "nsaid" in a.lower() for a in allergies):
                cross_reactivity.append({
                    "risk": "high",
                    "probability": "Cross-intolerance in ~50% of aspirin-intolerant patients",
                    "issue": "NSAIDs share COX-1 inhibition mechanism with aspirin. High cross-reactivity in aspirin-exacerbated respiratory disease.",
                    "recommendation": "Avoid NSAIDs in aspirin allergy. Consider acetaminophen (safe in most) or COX-2 selective inhibitor (celecoxib) with supervised challenge.",
                })

        return json.dumps({
            "medication": medication,
            "known_allergies": allergies,
            "reaction_history": reaction_history,
            "cross_reactivity_risks": cross_reactivity,
            "count": len(cross_reactivity),
            "note": (
                "Use clinical knowledge to identify any additional allergy or "
                "cross-reactivity risks. Consider the severity of prior reactions "
                "(urticaria vs anaphylaxis) when assessing risk."
            ),
        })

    async def _flag_combinations(self, tool_input: dict) -> str:
        medications = tool_input.get("medications", [])
        treatments = tool_input.get("treatments", [])
        conditions = tool_input.get("conditions", [])

        med_lower = [m.lower().strip() for m in medications]
        flagged = []

        for combo in DANGEROUS_COMBINATIONS:
            drug_groups = combo["drugs"]

            if len(drug_groups) == 2:
                group_a, group_b = drug_groups
                matched_a = [m for m in med_lower if any(d in m or m in d for d in group_a)]
                matched_b = [m for m in med_lower if any(d in m or m in d for d in group_b)]

                if matched_a and matched_b:
                    flagged.append({
                        "category": combo["category"],
                        "severity": combo["severity"],
                        "drugs_involved": list(set(matched_a + matched_b)),
                        "mechanism": combo["mechanism"],
                        "onset": combo["onset"],
                        "symptoms_to_watch": combo["symptoms"],
                        "management": combo["management"],
                    })
            elif len(drug_groups) == 3:
                # Triple combination (e.g., triple whammy)
                matched_groups = []
                for group in drug_groups:
                    matches = [m for m in med_lower if any(d in m or m in d for d in group)]
                    matched_groups.append(matches)

                if all(matched_groups):
                    all_matched = []
                    for mg in matched_groups:
                        all_matched.extend(mg)
                    flagged.append({
                        "category": combo["category"],
                        "severity": combo["severity"],
                        "drugs_involved": list(set(all_matched)),
                        "mechanism": combo["mechanism"],
                        "onset": combo["onset"],
                        "symptoms_to_watch": combo["symptoms"],
                        "management": combo["management"],
                    })

        return json.dumps({
            "medications_reviewed": medications,
            "treatments_reviewed": treatments,
            "conditions": conditions,
            "dangerous_combinations": flagged,
            "count": len(flagged),
            "severity_summary": {
                "critical": sum(1 for f in flagged if f["severity"] == "critical"),
                "high": sum(1 for f in flagged if f["severity"] == "high"),
                "moderate": sum(1 for f in flagged if f["severity"] == "moderate"),
            },
            "note": (
                "Use clinical knowledge to identify any additional dangerous "
                "combinations not covered by the automated check. Consider "
                "patient-specific factors (age, renal function, other conditions)."
            ),
        })
