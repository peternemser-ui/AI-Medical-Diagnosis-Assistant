"""
Medical Research Agent – Evidence-based medical literature context.

Responsibilities:
  * Search clinical guidelines for relevant treatment protocols
  * Check drug interactions across medication combinations
  * Look up disease prevalence and epidemiological data
  * Provide evidence-based context using GRADE framework and PICO methodology
"""

from __future__ import annotations

import json
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


# ---------------------------------------------------------------------------
# Clinical guidelines database
# ---------------------------------------------------------------------------

CLINICAL_GUIDELINES: dict[str, dict] = {
    "hypertension": {
        "sources": ["AHA/ACC 2017", "JNC 8", "NICE CG136", "ESC/ESH 2018"],
        "screening": "Screen all adults >= 18 years at every healthcare encounter. Confirm with ambulatory or home BP monitoring.",
        "diagnostic_criteria": "Stage 1: >= 130/80 mmHg; Stage 2: >= 140/90 mmHg (AHA/ACC). NICE uses >= 140/90 clinic, >= 135/85 ambulatory.",
        "first_line_treatment": [
            {"therapy": "ACE inhibitor or ARB", "evidence_grade": "A", "population": "General, especially with diabetes or CKD"},
            {"therapy": "Thiazide diuretic (chlorthalidone preferred)", "evidence_grade": "A", "population": "General, especially Black patients"},
            {"therapy": "Calcium channel blocker (amlodipine)", "evidence_grade": "A", "population": "General, especially Black patients or elderly"},
        ],
        "treatment_targets": "< 130/80 mmHg for most adults (AHA/ACC); < 140/90 for most, < 150/90 if >= 80 years (NICE).",
        "referral_criteria": "Resistant hypertension (uncontrolled on 3 drugs including diuretic), suspected secondary cause, hypertensive emergency.",
        "key_recommendations": [
            {"recommendation": "Lifestyle modifications for all patients: DASH diet, sodium < 1500mg/day, exercise 150 min/week, weight loss, limit alcohol", "grade": "A"},
            {"recommendation": "Start pharmacotherapy if BP >= 140/90 or >= 130/80 with ASCVD risk >= 10%", "grade": "A"},
            {"recommendation": "Dual therapy for Stage 2 hypertension", "grade": "B"},
            {"recommendation": "Monitor potassium and creatinine within 2-4 weeks of starting ACEi/ARB", "grade": "B"},
        ],
    },
    "type_2_diabetes": {
        "sources": ["ADA Standards of Care 2024", "NICE NG28", "EASD/ADA Consensus 2022", "WHO"],
        "screening": "Screen adults 35-70 with BMI >= 25 (USPSTF Grade B). Earlier if risk factors present.",
        "diagnostic_criteria": "HbA1c >= 6.5%, FPG >= 126 mg/dL, 2h OGTT >= 200 mg/dL, or random glucose >= 200 with symptoms.",
        "first_line_treatment": [
            {"therapy": "Metformin + lifestyle modification", "evidence_grade": "A", "population": "All patients without contraindications"},
            {"therapy": "SGLT2 inhibitor (empagliflozin, dapagliflozin)", "evidence_grade": "A", "population": "With established CVD, HF, or CKD"},
            {"therapy": "GLP-1 receptor agonist (semaglutide, liraglutide)", "evidence_grade": "A", "population": "With established CVD or high CV risk, or obesity"},
        ],
        "treatment_targets": "HbA1c < 7% for most adults; < 8% for elderly/frail; < 6.5% if achievable without hypoglycemia.",
        "referral_criteria": "Type 1 suspected, DKA, persistent hyperglycemia despite triple therapy, advanced complications.",
        "key_recommendations": [
            {"recommendation": "Metformin remains first-line unless contraindicated", "grade": "A"},
            {"recommendation": "Add SGLT2i or GLP-1 RA early if CVD, HF, or CKD present regardless of HbA1c", "grade": "A"},
            {"recommendation": "Annual screening: retinopathy, nephropathy (uACR + eGFR), neuropathy, foot exam", "grade": "B"},
            {"recommendation": "Statin therapy for all patients 40-75 years", "grade": "A"},
            {"recommendation": "BP target < 130/80 mmHg", "grade": "A"},
        ],
    },
    "coronary_artery_disease": {
        "sources": ["AHA/ACC 2023 Chronic Coronary Disease", "ESC 2019", "NICE CG126"],
        "screening": "Risk assessment with Pooled Cohort Equations for adults 40-75 years without known ASCVD.",
        "diagnostic_criteria": "Stress testing (exercise or pharmacologic), coronary CTA, or invasive angiography based on pre-test probability.",
        "first_line_treatment": [
            {"therapy": "Aspirin 75-100mg daily", "evidence_grade": "A", "population": "Established CAD"},
            {"therapy": "High-intensity statin (atorvastatin 40-80mg or rosuvastatin 20-40mg)", "evidence_grade": "A", "population": "All CAD patients"},
            {"therapy": "Beta-blocker", "evidence_grade": "A", "population": "Post-MI or with LV dysfunction"},
            {"therapy": "ACE inhibitor or ARB", "evidence_grade": "A", "population": "With LV dysfunction, DM, HTN, or CKD"},
        ],
        "treatment_targets": "LDL < 70 mg/dL (< 55 mg/dL ESC for very high risk); BP < 130/80.",
        "referral_criteria": "Acute coronary syndrome, refractory angina, left main or multivessel disease, reduced EF.",
        "key_recommendations": [
            {"recommendation": "Dual antiplatelet therapy (DAPT) for 12 months after ACS or PCI", "grade": "A"},
            {"recommendation": "Cardiac rehabilitation referral for all CAD patients", "grade": "A"},
            {"recommendation": "Sublingual nitroglycerin for acute angina", "grade": "A"},
            {"recommendation": "Consider PCSK9 inhibitor if LDL not at goal on max statin + ezetimibe", "grade": "A"},
        ],
    },
    "asthma": {
        "sources": ["GINA 2024", "NAEPP EPR-4", "NICE NG80", "BTS/SIGN"],
        "screening": "Spirometry for all suspected cases. Peak flow monitoring for ongoing assessment.",
        "diagnostic_criteria": "Variable expiratory airflow limitation: FEV1/FVC < 0.75-0.80 in adults with bronchodilator reversibility >= 12% and >= 200mL.",
        "first_line_treatment": [
            {"therapy": "Low-dose ICS (budesonide, fluticasone)", "evidence_grade": "A", "population": "All persistent asthma"},
            {"therapy": "ICS-formoterol as needed (MART)", "evidence_grade": "A", "population": "Mild asthma (GINA preferred track)"},
            {"therapy": "SABA as needed", "evidence_grade": "A", "population": "Intermittent asthma (alternative track)"},
        ],
        "treatment_targets": "Well-controlled: daytime symptoms <= 2/week, no nighttime waking, no activity limitation, SABA use <= 2/week.",
        "referral_criteria": "Severe/uncontrolled asthma despite Step 4 therapy, diagnostic uncertainty, occupational asthma.",
        "key_recommendations": [
            {"recommendation": "ICS are the cornerstone of asthma management at all severity levels", "grade": "A"},
            {"recommendation": "Step-up therapy based on symptom control and risk assessment", "grade": "A"},
            {"recommendation": "Written asthma action plan for all patients", "grade": "A"},
            {"recommendation": "Assess inhaler technique at every visit", "grade": "B"},
            {"recommendation": "Consider biologic therapy (anti-IgE, anti-IL5) for severe eosinophilic asthma", "grade": "A"},
        ],
    },
    "depression": {
        "sources": ["APA Practice Guidelines 2023", "NICE CG90/CG91", "CANMAT 2023", "WHO mhGAP"],
        "screening": "PHQ-2 then PHQ-9. USPSTF recommends screening all adults (Grade B).",
        "diagnostic_criteria": "DSM-5: >= 5 symptoms over 2 weeks including depressed mood or anhedonia. Must cause significant distress/impairment.",
        "first_line_treatment": [
            {"therapy": "SSRI (sertraline, escitalopram)", "evidence_grade": "A", "population": "Moderate-severe MDD"},
            {"therapy": "CBT or behavioral activation", "evidence_grade": "A", "population": "Mild-moderate MDD"},
            {"therapy": "Combined SSRI + CBT", "evidence_grade": "A", "population": "Severe MDD, better outcomes than either alone"},
        ],
        "treatment_targets": "Full remission (PHQ-9 < 5). Minimum 4-6 week adequate trial before switching.",
        "referral_criteria": "Suicidal ideation with plan/intent, psychotic features, bipolar suspected, treatment-resistant (failed 2+ adequate trials).",
        "key_recommendations": [
            {"recommendation": "SSRIs and SNRIs are first-line pharmacotherapy with comparable efficacy", "grade": "A"},
            {"recommendation": "Continue antidepressant for >= 6-12 months after remission to prevent relapse", "grade": "A"},
            {"recommendation": "Screen for bipolar disorder before starting antidepressant", "grade": "B"},
            {"recommendation": "Assess suicide risk at every visit during treatment", "grade": "A"},
            {"recommendation": "Exercise as adjunctive therapy (150 min/week moderate intensity)", "grade": "B"},
        ],
    },
    "copd": {
        "sources": ["GOLD 2024", "NICE NG115", "ATS/ERS"],
        "screening": "Spirometry in symptomatic adults with risk factors (smoking, occupational exposure).",
        "diagnostic_criteria": "Post-bronchodilator FEV1/FVC < 0.70. Severity: GOLD 1 (>= 80%), GOLD 2 (50-79%), GOLD 3 (30-49%), GOLD 4 (< 30%).",
        "first_line_treatment": [
            {"therapy": "LAMA (tiotropium)", "evidence_grade": "A", "population": "Group B-E"},
            {"therapy": "LABA + LAMA combination", "evidence_grade": "A", "population": "Group E or persistent dyspnea on monotherapy"},
            {"therapy": "ICS + LABA + LAMA triple therapy", "evidence_grade": "A", "population": "Group E with eosinophils >= 300, or frequent exacerbations"},
        ],
        "treatment_targets": "Reduce symptoms (mMRC/CAT), prevent exacerbations, slow disease progression.",
        "referral_criteria": "Diagnostic uncertainty, rapid decline, frequent severe exacerbations, surgical evaluation (LVRS, transplant).",
        "key_recommendations": [
            {"recommendation": "Smoking cessation is the single most effective intervention", "grade": "A"},
            {"recommendation": "Pulmonary rehabilitation for all symptomatic patients", "grade": "A"},
            {"recommendation": "Annual influenza + pneumococcal + COVID vaccination", "grade": "A"},
            {"recommendation": "Supplemental oxygen if PaO2 <= 55 mmHg or SpO2 <= 88%", "grade": "A"},
        ],
    },
    "heart_failure": {
        "sources": ["AHA/ACC/HFSA 2022", "ESC 2021", "NICE NG106"],
        "screening": "BNP or NT-proBNP for suspected HF. Echocardiography for confirmed cases.",
        "diagnostic_criteria": "Signs and symptoms of HF with structural/functional cardiac abnormality. HFrEF: LVEF <= 40%; HFpEF: LVEF >= 50% with diastolic dysfunction.",
        "first_line_treatment": [
            {"therapy": "ACEi/ARB/ARNI (sacubitril-valsartan preferred)", "evidence_grade": "A", "population": "HFrEF"},
            {"therapy": "Beta-blocker (carvedilol, metoprolol succinate, bisoprolol)", "evidence_grade": "A", "population": "HFrEF, stable patients"},
            {"therapy": "MRA (spironolactone, eplerenone)", "evidence_grade": "A", "population": "HFrEF with NYHA II-IV"},
            {"therapy": "SGLT2 inhibitor (dapagliflozin, empagliflozin)", "evidence_grade": "A", "population": "HFrEF and HFpEF"},
        ],
        "treatment_targets": "Optimize GDMT to target doses. NYHA class improvement. Reduce hospitalization.",
        "referral_criteria": "NYHA III-IV, consider device therapy (ICD/CRT), transplant evaluation, mechanical support.",
        "key_recommendations": [
            {"recommendation": "Initiate all four pillars of GDMT as soon as possible (ARNI + BB + MRA + SGLT2i)", "grade": "A"},
            {"recommendation": "Sodium restriction < 1500mg/day and fluid restriction if hyponatremic", "grade": "B"},
            {"recommendation": "ICD for primary prevention if LVEF <= 35% on optimal therapy >= 3 months", "grade": "A"},
            {"recommendation": "Diuretics for volume management (not mortality benefit)", "grade": "B"},
        ],
    },
    "atrial_fibrillation": {
        "sources": ["AHA/ACC/HRS 2023", "ESC 2020", "NICE NG196", "CCS 2020"],
        "screening": "Opportunistic pulse palpation. ECG for confirmation.",
        "diagnostic_criteria": "ECG showing irregularly irregular rhythm with absence of P waves. Duration: paroxysmal (< 7 days), persistent (> 7 days), permanent.",
        "first_line_treatment": [
            {"therapy": "Anticoagulation: DOAC preferred (apixaban, rivaroxaban, edoxaban, dabigatran)", "evidence_grade": "A", "population": "CHA2DS2-VASc >= 2 (men) or >= 3 (women)"},
            {"therapy": "Rate control: beta-blocker or non-DHP CCB (diltiazem, verapamil)", "evidence_grade": "A", "population": "Most AF patients"},
            {"therapy": "Rhythm control: flecainide, amiodarone, or catheter ablation", "evidence_grade": "A", "population": "Symptomatic AF, especially early AF"},
        ],
        "treatment_targets": "Resting HR < 110 bpm (lenient) or < 80 bpm (strict). Stroke prevention per CHA2DS2-VASc.",
        "referral_criteria": "Symptomatic despite rate control, candidate for ablation, WPW + AF, HCM + AF.",
        "key_recommendations": [
            {"recommendation": "Assess stroke risk with CHA2DS2-VASc and bleeding risk with HAS-BLED at every visit", "grade": "A"},
            {"recommendation": "DOACs preferred over warfarin in non-valvular AF", "grade": "A"},
            {"recommendation": "Early rhythm control improves outcomes in recently diagnosed AF (EAST-AFNET 4 trial)", "grade": "A"},
            {"recommendation": "Screen for and treat modifiable risk factors: obesity, OSA, alcohol, HTN", "grade": "B"},
        ],
    },
    "pneumonia": {
        "sources": ["ATS/IDSA 2019 CAP Guidelines", "NICE CG191", "BTS 2015"],
        "screening": "Chest X-ray for suspected cases. CURB-65 or PSI for severity assessment.",
        "diagnostic_criteria": "New infiltrate on chest imaging + signs/symptoms (cough, fever, dyspnea, crackles).",
        "first_line_treatment": [
            {"therapy": "Amoxicillin 500mg TID (outpatient, no comorbidities)", "evidence_grade": "A", "population": "Healthy outpatient CAP"},
            {"therapy": "Amoxicillin-clavulanate + macrolide OR respiratory fluoroquinolone", "evidence_grade": "A", "population": "Outpatient with comorbidities"},
            {"therapy": "Beta-lactam + macrolide OR respiratory fluoroquinolone (inpatient)", "evidence_grade": "A", "population": "Non-ICU inpatient CAP"},
            {"therapy": "Beta-lactam + macrolide + consider MRSA/Pseudomonas coverage", "evidence_grade": "A", "population": "ICU CAP"},
        ],
        "treatment_targets": "Clinical stability (afebrile, HR < 100, RR < 24, SpO2 > 90%, able to eat) within 48-72h.",
        "referral_criteria": "CURB-65 >= 3, need for ICU, empyema, failure to improve on antibiotics.",
        "key_recommendations": [
            {"recommendation": "Obtain sputum and blood cultures before antibiotics in hospitalized patients", "grade": "B"},
            {"recommendation": "Start antibiotics within 4 hours of presentation for inpatients", "grade": "B"},
            {"recommendation": "5-day antibiotic course sufficient if clinically stable by day 3-5", "grade": "A"},
            {"recommendation": "Corticosteroids for severe CAP (prednisone 40mg x 5 days, CAPE COD trial)", "grade": "A"},
        ],
    },
    "urinary_tract_infection": {
        "sources": ["IDSA 2011 Uncomplicated UTI", "AUA/CUA/SUFU 2019", "NICE NG109", "EAU 2023"],
        "screening": "Urinalysis and urine culture. Do not screen or treat asymptomatic bacteriuria (except pregnancy).",
        "diagnostic_criteria": "Symptoms (dysuria, frequency, urgency) + pyuria/bacteriuria. >= 10^3 CFU/mL in symptomatic women; >= 10^5 in men or catheter.",
        "first_line_treatment": [
            {"therapy": "Nitrofurantoin 100mg BID x 5 days", "evidence_grade": "A", "population": "Uncomplicated cystitis"},
            {"therapy": "TMP-SMX 160/800mg BID x 3 days", "evidence_grade": "A", "population": "Uncomplicated cystitis (if resistance < 20%)"},
            {"therapy": "Fosfomycin 3g single dose", "evidence_grade": "A", "population": "Uncomplicated cystitis"},
            {"therapy": "Fluoroquinolone", "evidence_grade": "A", "population": "Complicated UTI or pyelonephritis"},
        ],
        "treatment_targets": "Symptom resolution within 48-72h. Repeat culture only if persistent symptoms.",
        "referral_criteria": "Recurrent UTI (>= 3/year), structural abnormality, male UTI, pyelonephritis not responding to oral therapy.",
        "key_recommendations": [
            {"recommendation": "Avoid fluoroquinolones for uncomplicated cystitis (reserve for complicated infections)", "grade": "A"},
            {"recommendation": "Do not treat asymptomatic bacteriuria except in pregnancy", "grade": "A"},
            {"recommendation": "Consider vaginal estrogen for recurrent UTI in postmenopausal women", "grade": "B"},
            {"recommendation": "Obtain urine culture in complicated UTI, male UTI, treatment failure, or pyelonephritis", "grade": "B"},
        ],
    },
    "osteoarthritis": {
        "sources": ["ACR/AF 2019", "OARSI 2019", "NICE NG226", "EULAR 2019"],
        "screening": "Clinical diagnosis based on history and exam. Imaging when diagnosis uncertain.",
        "diagnostic_criteria": "Joint pain with use, morning stiffness < 30 min, crepitus, bony enlargement, no warmth. X-ray: joint space narrowing, osteophytes.",
        "first_line_treatment": [
            {"therapy": "Exercise and weight management", "evidence_grade": "A", "population": "All OA patients"},
            {"therapy": "Topical NSAIDs (diclofenac gel)", "evidence_grade": "A", "population": "Knee and hand OA"},
            {"therapy": "Oral NSAIDs (lowest effective dose, shortest duration)", "evidence_grade": "A", "population": "Moderate-severe symptoms"},
            {"therapy": "Duloxetine", "evidence_grade": "A", "population": "Knee OA with inadequate response to NSAIDs"},
        ],
        "treatment_targets": "Pain reduction, functional improvement, quality of life. No disease-modifying therapy available.",
        "referral_criteria": "Severe functional limitation despite conservative management, candidate for joint replacement.",
        "key_recommendations": [
            {"recommendation": "Exercise is strongly recommended regardless of severity, age, or comorbidity", "grade": "A"},
            {"recommendation": "Intra-articular corticosteroid injections for acute flares (limit frequency)", "grade": "B"},
            {"recommendation": "Acetaminophen no longer recommended as first-line due to limited efficacy", "grade": "A"},
            {"recommendation": "Glucosamine and chondroitin not recommended (insufficient evidence)", "grade": "B"},
        ],
    },
    "anxiety_disorders": {
        "sources": ["APA 2023", "NICE CG113", "CANMAT 2023", "BAP 2014"],
        "screening": "GAD-7 screening tool. USPSTF recommends screening all adults (Grade B, 2023).",
        "diagnostic_criteria": "DSM-5: Excessive anxiety/worry occurring more days than not for >= 6 months with >= 3 associated symptoms.",
        "first_line_treatment": [
            {"therapy": "SSRI (sertraline, escitalopram, paroxetine)", "evidence_grade": "A", "population": "GAD, SAD, PD"},
            {"therapy": "SNRI (venlafaxine, duloxetine)", "evidence_grade": "A", "population": "GAD"},
            {"therapy": "CBT", "evidence_grade": "A", "population": "All anxiety disorders"},
        ],
        "treatment_targets": "GAD-7 < 5. Functional improvement. Response typically takes 4-8 weeks for medications.",
        "referral_criteria": "Treatment-resistant, comorbid substance use, severe functional impairment, suicidality.",
        "key_recommendations": [
            {"recommendation": "CBT is first-line and has durable effects after discontinuation", "grade": "A"},
            {"recommendation": "Benzodiazepines only for short-term acute management (< 4 weeks), not first-line", "grade": "A"},
            {"recommendation": "Start SSRI/SNRI at low dose and titrate slowly to minimize initial anxiety worsening", "grade": "B"},
            {"recommendation": "Buspirone as augmentation or alternative in GAD", "grade": "B"},
        ],
    },
    "chronic_kidney_disease": {
        "sources": ["KDIGO 2024", "NICE NG203", "ACP 2023"],
        "screening": "eGFR and uACR in high-risk populations (diabetes, hypertension, family history).",
        "diagnostic_criteria": "eGFR < 60 mL/min/1.73m2 or albuminuria >= 30 mg/g for >= 3 months. Staging: G1-G5 by eGFR; A1-A3 by albuminuria.",
        "first_line_treatment": [
            {"therapy": "ACEi or ARB (maximally tolerated dose)", "evidence_grade": "A", "population": "CKD with albuminuria"},
            {"therapy": "SGLT2 inhibitor (dapagliflozin, empagliflozin)", "evidence_grade": "A", "population": "CKD G2-G4 with albuminuria"},
            {"therapy": "Finerenone (non-steroidal MRA)", "evidence_grade": "A", "population": "DKD with persistent albuminuria on ACEi/ARB"},
        ],
        "treatment_targets": "BP < 120 systolic (SPRINT), slow eGFR decline, reduce albuminuria.",
        "referral_criteria": "eGFR < 30, rapid decline (> 5 mL/min/year), refractory hypertension, suspected glomerulonephritis.",
        "key_recommendations": [
            {"recommendation": "SGLT2 inhibitors provide kidney protection independent of diabetes status (DAPA-CKD, EMPA-KIDNEY trials)", "grade": "A"},
            {"recommendation": "Monitor potassium closely with ACEi/ARB + MRA", "grade": "A"},
            {"recommendation": "Adjust drug dosing for eGFR (especially metformin, DOACs, gabapentin)", "grade": "A"},
            {"recommendation": "Avoid NSAIDs in CKD", "grade": "A"},
        ],
    },
    "obesity": {
        "sources": ["AGA 2022", "Endocrine Society 2023", "NICE CG189", "ACC/AHA/TOS 2013"],
        "screening": "BMI at every visit. Waist circumference for BMI 25-34.9.",
        "diagnostic_criteria": "BMI >= 30 kg/m2 (obesity). BMI 25-29.9 (overweight). Consider waist circumference and comorbidities.",
        "first_line_treatment": [
            {"therapy": "Intensive behavioral intervention (>= 14 sessions in 6 months)", "evidence_grade": "A", "population": "All patients with obesity"},
            {"therapy": "GLP-1 receptor agonist (semaglutide 2.4mg weekly)", "evidence_grade": "A", "population": "BMI >= 30 or >= 27 with comorbidity"},
            {"therapy": "Tirzepatide (GIP/GLP-1 agonist)", "evidence_grade": "A", "population": "BMI >= 30 or >= 27 with comorbidity"},
        ],
        "treatment_targets": ">= 5-10% weight loss for metabolic benefit. >= 15% with pharmacotherapy. >= 25-30% with bariatric surgery.",
        "referral_criteria": "BMI >= 40 or >= 35 with comorbidities for bariatric surgery evaluation.",
        "key_recommendations": [
            {"recommendation": "GLP-1 RAs produce 15-20% weight loss (STEP trials); tirzepatide up to 22% (SURMOUNT)", "grade": "A"},
            {"recommendation": "Bariatric surgery remains most effective intervention for severe obesity", "grade": "A"},
            {"recommendation": "Treat obesity as a chronic disease requiring long-term management", "grade": "A"},
            {"recommendation": "Screen for and treat associated conditions: T2DM, HTN, OSA, NAFLD, GERD", "grade": "B"},
        ],
    },
    "migraine": {
        "sources": ["AHS 2021", "AAN 2021", "NICE CG150", "EHF 2022"],
        "screening": "ID Migraine screener (3 questions). Neuroimaging not routine; only if red flags present.",
        "diagnostic_criteria": "ICHD-3: >= 5 attacks lasting 4-72h with >= 2 of: unilateral, pulsating, moderate-severe, aggravated by activity; plus >= 1: nausea/vomiting, photo+phonophobia.",
        "first_line_treatment": [
            {"therapy": "Acute: NSAID (ibuprofen 400-600mg) or triptan (sumatriptan 50-100mg)", "evidence_grade": "A", "population": "Moderate-severe attacks"},
            {"therapy": "Preventive: propranolol, topiramate, or amitriptyline", "evidence_grade": "A", "population": ">= 4 headache days/month"},
            {"therapy": "Preventive: CGRP mAb (erenumab, fremanezumab, galcanezumab)", "evidence_grade": "A", "population": "Episodic or chronic migraine, failed oral preventives"},
        ],
        "treatment_targets": ">= 50% reduction in headache days. Reduced disability (MIDAS/HIT-6).",
        "referral_criteria": "Diagnostic uncertainty, thunderclap headache, new daily persistent headache, medication overuse headache, failed >= 2 preventives.",
        "key_recommendations": [
            {"recommendation": "Treat early in the attack for best efficacy", "grade": "A"},
            {"recommendation": "Limit acute medication use to < 10-15 days/month to prevent MOH", "grade": "A"},
            {"recommendation": "CGRP monoclonal antibodies are effective with favorable side-effect profile", "grade": "A"},
            {"recommendation": "Gepants (ubrogepant, rimegepant) as alternative acute therapy for triptan non-responders", "grade": "A"},
        ],
    },
    "hypothyroidism": {
        "sources": ["ATA 2014", "ETA 2013", "NICE NG145", "AACE/ATA 2012"],
        "screening": "TSH is the primary screening test. Not universally recommended; screen high-risk groups.",
        "diagnostic_criteria": "Elevated TSH with low free T4 (overt). Elevated TSH with normal free T4 (subclinical).",
        "first_line_treatment": [
            {"therapy": "Levothyroxine (1.6 mcg/kg/day starting dose for young healthy adults)", "evidence_grade": "A", "population": "Overt hypothyroidism"},
            {"therapy": "Levothyroxine (lower starting dose 25-50 mcg/day)", "evidence_grade": "A", "population": "Elderly or cardiac disease"},
        ],
        "treatment_targets": "TSH in normal range (0.4-4.0 mIU/L); lower half of range for most symptomatic patients.",
        "referral_criteria": "Suspected central hypothyroidism, thyroid nodule, pregnancy with thyroid disease, poor response to levothyroxine.",
        "key_recommendations": [
            {"recommendation": "Take levothyroxine on empty stomach 30-60 min before breakfast", "grade": "B"},
            {"recommendation": "Recheck TSH 6-8 weeks after dose change", "grade": "B"},
            {"recommendation": "Subclinical hypothyroidism: treat if TSH > 10 or symptoms present with TSH 5-10", "grade": "B"},
            {"recommendation": "Separate levothyroxine from calcium, iron, PPI by >= 4 hours", "grade": "B"},
        ],
    },
    "iron_deficiency_anemia": {
        "sources": ["ASH 2020", "BSH 2021", "NICE NG24", "WHO"],
        "screening": "CBC with iron studies (ferritin, serum iron, TIBC, transferrin saturation).",
        "diagnostic_criteria": "Hb < 13 g/dL (men), < 12 g/dL (women) with ferritin < 30 ng/mL (< 100 in CKD/inflammation).",
        "first_line_treatment": [
            {"therapy": "Oral iron (ferrous sulfate 325mg = 65mg elemental iron, 1-3x daily)", "evidence_grade": "A", "population": "Mild-moderate anemia"},
            {"therapy": "IV iron (ferric carboxymaltose, iron sucrose)", "evidence_grade": "A", "population": "Intolerance/failure of oral iron, malabsorption, CKD, HF, IBD"},
        ],
        "treatment_targets": "Hb normalization (usually within 6-8 weeks). Ferritin > 100 ng/mL for repletion.",
        "referral_criteria": "GI blood loss suspected (endoscopy), unexplained IDA in men or postmenopausal women, refractory to iron therapy.",
        "key_recommendations": [
            {"recommendation": "Always investigate the cause of iron deficiency, especially in men and postmenopausal women (rule out GI malignancy)", "grade": "A"},
            {"recommendation": "Alternate-day dosing of oral iron improves absorption (fractional absorption better with 48h intervals)", "grade": "B"},
            {"recommendation": "Vitamin C 200mg with oral iron enhances absorption", "grade": "B"},
            {"recommendation": "Continue iron supplementation 3-6 months after Hb normalization to replenish stores", "grade": "B"},
        ],
    },
    "gerd": {
        "sources": ["ACG 2022", "AGA 2020", "NICE NG124", "Lyon Consensus 2018"],
        "screening": "Clinical diagnosis based on typical symptoms. Endoscopy for alarm features or refractory symptoms.",
        "diagnostic_criteria": "Typical symptoms (heartburn, regurgitation) responding to PPI trial. Confirmed with pH monitoring + impedance if diagnostic uncertainty.",
        "first_line_treatment": [
            {"therapy": "PPI (omeprazole 20mg, pantoprazole 40mg) once daily 30-60 min before meal", "evidence_grade": "A", "population": "Erosive and non-erosive GERD"},
            {"therapy": "H2RA (famotidine 20-40mg) for mild/intermittent symptoms", "evidence_grade": "B", "population": "Mild GERD"},
            {"therapy": "Lifestyle: weight loss, head-of-bed elevation, avoid late meals", "evidence_grade": "B", "population": "All GERD patients"},
        ],
        "treatment_targets": "Symptom resolution. Healing of erosive esophagitis (8-week PPI course).",
        "referral_criteria": "Alarm features (dysphagia, weight loss, GI bleeding), Barrett's esophagus, refractory to PPI, > 10 year history.",
        "key_recommendations": [
            {"recommendation": "8-week PPI trial is standard initial therapy", "grade": "A"},
            {"recommendation": "Step down to lowest effective PPI dose or H2RA for maintenance", "grade": "B"},
            {"recommendation": "Endoscopy for patients with alarm symptoms, long-standing GERD, or Barrett's screening", "grade": "B"},
            {"recommendation": "Avoid long-term PPI without indication reassessment (discuss risks: C. diff, fracture, hypomagnesemia)", "grade": "B"},
        ],
    },
    "low_back_pain": {
        "sources": ["ACP 2017", "NICE NG59", "ACS Appropriateness Criteria", "VA/DoD 2022"],
        "screening": "Red flag assessment for all acute low back pain. Imaging not recommended < 6 weeks without red flags.",
        "diagnostic_criteria": "Clinical diagnosis. Mechanical (90%+). Red flags: cauda equina syndrome, fracture, malignancy, infection.",
        "first_line_treatment": [
            {"therapy": "NSAIDs (ibuprofen, naproxen) for acute pain", "evidence_grade": "A", "population": "Acute non-specific LBP"},
            {"therapy": "Skeletal muscle relaxants (cyclobenzaprine) for acute pain", "evidence_grade": "B", "population": "Acute LBP with muscle spasm"},
            {"therapy": "Physical therapy and exercise", "evidence_grade": "A", "population": "Subacute and chronic LBP"},
            {"therapy": "Duloxetine", "evidence_grade": "A", "population": "Chronic LBP"},
        ],
        "treatment_targets": "Functional improvement. Return to normal activities. Pain reduction.",
        "referral_criteria": "Red flags, progressive neurological deficit, cauda equina syndrome, failure to improve after 6 weeks.",
        "key_recommendations": [
            {"recommendation": "Avoid imaging for acute non-specific LBP without red flags", "grade": "A"},
            {"recommendation": "Encourage staying active; bed rest worsens outcomes", "grade": "A"},
            {"recommendation": "Opioids are not first-line and should be avoided when possible", "grade": "A"},
            {"recommendation": "CBT for chronic LBP with psychosocial risk factors (yellow flags)", "grade": "A"},
        ],
    },
    "hyperlipidemia": {
        "sources": ["ACC/AHA 2018 Cholesterol Guidelines", "ESC/EAS 2019", "NICE CG181"],
        "screening": "Lipid panel every 4-6 years for adults 20+. More frequently with risk factors. USPSTF Grade B for 40-75.",
        "diagnostic_criteria": "Total cholesterol, LDL, HDL, triglycerides. Risk-based approach using ASCVD risk calculator.",
        "first_line_treatment": [
            {"therapy": "High-intensity statin (atorvastatin 40-80mg or rosuvastatin 20-40mg)", "evidence_grade": "A", "population": "Clinical ASCVD, LDL >= 190, or DM 40-75 years"},
            {"therapy": "Moderate-intensity statin", "evidence_grade": "A", "population": "10-year ASCVD risk 7.5-20% with risk enhancers"},
            {"therapy": "Ezetimibe add-on", "evidence_grade": "A", "population": "Not at LDL goal on maximal statin"},
            {"therapy": "PCSK9 inhibitor (evolocumab, alirocumab)", "evidence_grade": "A", "population": "Very high risk not at goal on statin + ezetimibe"},
        ],
        "treatment_targets": "LDL >= 50% reduction from baseline. Very high risk: LDL < 70 (ACC/AHA) or < 55 (ESC).",
        "referral_criteria": "Familial hypercholesterolemia suspected, statin intolerance, complex lipid disorders.",
        "key_recommendations": [
            {"recommendation": "Statin therapy is the foundation of ASCVD risk reduction", "grade": "A"},
            {"recommendation": "Use ASCVD risk calculator to guide therapy in primary prevention", "grade": "A"},
            {"recommendation": "CAC scoring can reclassify borderline risk patients", "grade": "B"},
            {"recommendation": "Bempedoic acid as alternative for statin-intolerant patients", "grade": "A"},
        ],
    },
    "celiac_disease": {
        "sources": ["ACG 2023", "BSG 2019", "NICE NG20", "ESPGHAN 2020"],
        "screening": "IgA-tTG antibody. Total IgA to rule out IgA deficiency. Screen first-degree relatives.",
        "diagnostic_criteria": "Positive serology (IgA-tTG >= 10x ULN + positive EMA in pediatrics). Duodenal biopsy (Marsh 3) for confirmation in adults.",
        "first_line_treatment": [
            {"therapy": "Strict lifelong gluten-free diet", "evidence_grade": "A", "population": "All confirmed celiac disease"},
        ],
        "treatment_targets": "Symptom resolution, antibody normalization (6-12 months), mucosal healing (1-2 years).",
        "referral_criteria": "Non-responsive celiac, refractory celiac disease, concern for enteropathy-associated T-cell lymphoma.",
        "key_recommendations": [
            {"recommendation": "Referral to experienced dietitian for GFD education is essential", "grade": "A"},
            {"recommendation": "Screen for nutritional deficiencies: iron, folate, B12, vitamin D, calcium, zinc", "grade": "B"},
            {"recommendation": "Repeat antibodies and consider follow-up biopsy at 1-2 years to confirm healing", "grade": "B"},
            {"recommendation": "DEXA scan for bone density assessment at diagnosis", "grade": "B"},
        ],
    },
    "stroke": {
        "sources": ["AHA/ASA 2019", "ESO 2021", "NICE NG128"],
        "screening": "BP management and AF screening for prevention. FAST for acute recognition.",
        "diagnostic_criteria": "CT head to exclude hemorrhage. MRI with DWI for ischemic stroke confirmation. NIHSS for severity.",
        "first_line_treatment": [
            {"therapy": "IV alteplase (0.9mg/kg, max 90mg) within 4.5 hours of onset", "evidence_grade": "A", "population": "Acute ischemic stroke within window"},
            {"therapy": "Mechanical thrombectomy within 24 hours for large vessel occlusion", "evidence_grade": "A", "population": "LVO with salvageable tissue on imaging"},
            {"therapy": "Aspirin 160-325mg within 24-48h (not within 24h of thrombolysis)", "evidence_grade": "A", "population": "Acute ischemic stroke"},
        ],
        "treatment_targets": "Time-critical: door-to-needle < 60 min, door-to-groin < 90 min. Secondary prevention of recurrence.",
        "referral_criteria": "All acute stroke to stroke unit. Neurosurgery for hemorrhagic stroke or malignant edema.",
        "key_recommendations": [
            {"recommendation": "Time is brain: every minute of delay loses 1.9 million neurons", "grade": "A"},
            {"recommendation": "Extended thrombolysis window to 4.5h and thrombectomy to 24h with imaging selection", "grade": "A"},
            {"recommendation": "Secondary prevention: antiplatelet + statin + BP control + lifestyle modification", "grade": "A"},
            {"recommendation": "Dual antiplatelet (aspirin + clopidogrel) for 21 days after minor stroke/TIA", "grade": "A"},
        ],
    },
    "breast_cancer_screening": {
        "sources": ["USPSTF 2024", "ACS 2023", "NCCN 2024", "ACR"],
        "screening": "Mammography. Risk assessment to determine need for MRI.",
        "diagnostic_criteria": "BI-RADS classification on imaging. Tissue diagnosis by core needle biopsy.",
        "first_line_treatment": [
            {"therapy": "Surgery (lumpectomy + radiation or mastectomy)", "evidence_grade": "A", "population": "Early-stage breast cancer"},
            {"therapy": "Endocrine therapy (tamoxifen, aromatase inhibitors) for ER+ disease", "evidence_grade": "A", "population": "ER/PR-positive breast cancer"},
        ],
        "treatment_targets": "Complete excision with clear margins. Adjuvant therapy per molecular subtype.",
        "referral_criteria": "Any suspicious finding on screening, genetic counseling for high-risk.",
        "key_recommendations": [
            {"recommendation": "Biennial screening mammography for average-risk women 40-74 (USPSTF 2024 updated to age 40 start)", "grade": "B"},
            {"recommendation": "Risk assessment by age 30 to determine need for enhanced screening", "grade": "B"},
            {"recommendation": "MRI screening in addition to mammography for lifetime risk >= 20%", "grade": "B"},
            {"recommendation": "Genetic testing referral for strong family history or Ashkenazi Jewish heritage", "grade": "B"},
        ],
    },
    "colorectal_cancer_screening": {
        "sources": ["USPSTF 2021", "ACS 2018", "ACG 2021", "NCCN 2024"],
        "screening": "Begin at age 45 for average risk. Earlier if family history or other risk factors.",
        "diagnostic_criteria": "Colonoscopy with biopsy. FIT annually as alternative. Cologuard every 3 years.",
        "first_line_treatment": [
            {"therapy": "Colonoscopic polypectomy for precancerous polyps", "evidence_grade": "A", "population": "Adenomatous polyps"},
            {"therapy": "Surgical resection for localized CRC", "evidence_grade": "A", "population": "Stage I-III CRC"},
        ],
        "treatment_targets": "Detection and removal of precancerous polyps. Early-stage cancer detection.",
        "referral_criteria": "Positive screening test, family history of CRC < 60 or adenoma, Lynch syndrome suspected.",
        "key_recommendations": [
            {"recommendation": "Screening starting at age 45 for average-risk adults (USPSTF Grade A for 50-75, B for 45-49)", "grade": "A"},
            {"recommendation": "Colonoscopy every 10 years OR annual FIT are both acceptable options", "grade": "A"},
            {"recommendation": "Earlier and more frequent screening with family history of CRC or advanced adenoma", "grade": "B"},
            {"recommendation": "Shared decision-making for screening in ages 76-85", "grade": "C"},
        ],
    },
    "osteoporosis": {
        "sources": ["NOF 2022", "AACE/ACE 2020", "NICE TA464", "USPSTF 2018"],
        "screening": "DEXA scan for women >= 65, men >= 70, or younger with risk factors. FRAX for 10-year fracture risk.",
        "diagnostic_criteria": "T-score <= -2.5 at hip or spine (DEXA). Osteopenia: T-score -1.0 to -2.5. Or fragility fracture.",
        "first_line_treatment": [
            {"therapy": "Oral bisphosphonate (alendronate 70mg weekly, risedronate 35mg weekly)", "evidence_grade": "A", "population": "Postmenopausal women and men >= 50 with osteoporosis"},
            {"therapy": "IV zoledronic acid 5mg annually", "evidence_grade": "A", "population": "Alternative if oral bisphosphonate not tolerated"},
            {"therapy": "Denosumab 60mg SC every 6 months", "evidence_grade": "A", "population": "Alternative to bisphosphonates, especially with renal impairment"},
        ],
        "treatment_targets": "Fracture prevention. T-score improvement. Maintain therapy for 3-5 years then reassess.",
        "referral_criteria": "Fracture on therapy, very low T-score (< -3.0), consideration for anabolic therapy.",
        "key_recommendations": [
            {"recommendation": "Calcium 1000-1200mg/day and Vitamin D 800-1000 IU/day for all patients", "grade": "A"},
            {"recommendation": "Bisphosphonate drug holiday after 3-5 years in moderate risk; continue in high risk", "grade": "B"},
            {"recommendation": "Anabolic therapy (teriparatide, romosozumab) for very high fracture risk", "grade": "A"},
            {"recommendation": "Fall prevention program as integral part of fracture prevention", "grade": "A"},
        ],
    },
    "allergic_rhinitis": {
        "sources": ["ARIA 2020", "AAO-HNS 2015", "NICE CG57", "BSACI 2017"],
        "screening": "Clinical diagnosis based on symptoms. Skin prick testing or specific IgE for allergen identification.",
        "diagnostic_criteria": "Nasal congestion, rhinorrhea, sneezing, itching triggered by allergen exposure. Intermittent (< 4 days/week) vs persistent.",
        "first_line_treatment": [
            {"therapy": "Intranasal corticosteroid (fluticasone, mometasone)", "evidence_grade": "A", "population": "Moderate-severe or persistent symptoms"},
            {"therapy": "Second-generation oral antihistamine (cetirizine, loratadine, fexofenadine)", "evidence_grade": "A", "population": "Mild-moderate symptoms"},
            {"therapy": "Allergen immunotherapy (SCIT or SLIT)", "evidence_grade": "A", "population": "Inadequate response to pharmacotherapy, known allergen trigger"},
        ],
        "treatment_targets": "Symptom control, quality of life improvement, minimize side effects.",
        "referral_criteria": "Inadequate response to optimal pharmacotherapy, consider immunotherapy, complications (sinusitis, OME).",
        "key_recommendations": [
            {"recommendation": "Intranasal corticosteroids are the most effective monotherapy", "grade": "A"},
            {"recommendation": "Avoid first-generation antihistamines (diphenhydramine) due to sedation and anticholinergic effects", "grade": "A"},
            {"recommendation": "Allergen avoidance measures when specific triggers identified", "grade": "B"},
            {"recommendation": "Combination intranasal corticosteroid + antihistamine (e.g., Dymista) for refractory symptoms", "grade": "A"},
        ],
    },
    "dvt_pe": {
        "sources": ["ASH 2020", "ACCP/CHEST 2021", "NICE NG158", "ESC 2019"],
        "screening": "Wells score for pre-test probability. D-dimer for low-probability patients.",
        "diagnostic_criteria": "DVT: compression ultrasound. PE: CTPA or V/Q scan. Age-adjusted D-dimer (age x 10 for > 50 years).",
        "first_line_treatment": [
            {"therapy": "DOAC (apixaban or rivaroxaban) as monotherapy", "evidence_grade": "A", "population": "Most DVT/PE without cancer"},
            {"therapy": "LMWH + warfarin (overlap until INR therapeutic)", "evidence_grade": "A", "population": "Alternative if DOAC contraindicated"},
            {"therapy": "LMWH monotherapy", "evidence_grade": "A", "population": "Cancer-associated VTE"},
        ],
        "treatment_targets": "3 months minimum for provoked VTE. Extended/indefinite for unprovoked or recurrent.",
        "referral_criteria": "Massive PE (hemodynamic instability), IVC filter consideration, recurrent VTE on anticoagulation.",
        "key_recommendations": [
            {"recommendation": "DOACs preferred over warfarin for non-cancer VTE (fewer bleeding events, no monitoring)", "grade": "A"},
            {"recommendation": "Systemic thrombolysis for massive PE with hemodynamic compromise", "grade": "A"},
            {"recommendation": "Extended anticoagulation for unprovoked VTE if bleeding risk acceptable", "grade": "A"},
            {"recommendation": "LMWH or DOAC (edoxaban, rivaroxaban) for cancer-associated VTE", "grade": "A"},
        ],
    },
    "pregnancy_prenatal": {
        "sources": ["ACOG 2023", "NICE CG62", "WHO Antenatal Care 2016", "SMFM"],
        "screening": "First visit: CBC, blood type, Rh, rubella, HIV, hepatitis B/C, syphilis, urinalysis, urine culture, Pap, GDM screening 24-28 weeks, GBS 36 weeks.",
        "diagnostic_criteria": "Positive pregnancy test (hCG). Dating ultrasound in first trimester.",
        "first_line_treatment": [
            {"therapy": "Prenatal vitamins with folic acid 400-800 mcg daily", "evidence_grade": "A", "population": "All pregnant women"},
            {"therapy": "Low-dose aspirin 81mg daily from 12-28 weeks", "evidence_grade": "A", "population": "High risk for preeclampsia"},
        ],
        "treatment_targets": "Healthy pregnancy outcomes. Screening at appropriate gestational ages.",
        "referral_criteria": "High-risk pregnancy (multiple gestation, pre-existing conditions, prior preterm birth), abnormal screening results.",
        "key_recommendations": [
            {"recommendation": "Folic acid supplementation before conception and through first trimester prevents neural tube defects", "grade": "A"},
            {"recommendation": "Screen for gestational diabetes at 24-28 weeks with GCT or OGTT", "grade": "A"},
            {"recommendation": "Low-dose aspirin for preeclampsia prevention in high-risk women", "grade": "A"},
            {"recommendation": "Avoid: ACE inhibitors, warfarin, isotretinoin, methotrexate, statins, valproic acid in pregnancy", "grade": "A"},
        ],
    },
    "otitis_media": {
        "sources": ["AAP 2013", "NICE CG69", "AAFP"],
        "screening": "Otoscopic examination. Pneumatic otoscopy or tympanometry for confirmation.",
        "diagnostic_criteria": "Moderate-severe bulging TM, new otorrhea not from otitis externa, or mild bulging with < 48h ear pain or intense erythema.",
        "first_line_treatment": [
            {"therapy": "Amoxicillin 80-90mg/kg/day divided BID for 10 days (< 2 years) or 5-7 days (>= 2 years)", "evidence_grade": "A", "population": "AOM requiring antibiotics"},
            {"therapy": "Observation with follow-up in 48-72h", "evidence_grade": "A", "population": "Non-severe AOM in children >= 2 years with unilateral disease"},
        ],
        "treatment_targets": "Symptom resolution within 48-72h. Follow-up if no improvement.",
        "referral_criteria": "Recurrent AOM (>= 3 in 6 months or >= 4 in 12 months), chronic OME, hearing loss concerns.",
        "key_recommendations": [
            {"recommendation": "Watchful waiting is appropriate for non-severe unilateral AOM in children >= 2 years", "grade": "A"},
            {"recommendation": "Adequate pain management is essential (ibuprofen or acetaminophen)", "grade": "A"},
            {"recommendation": "Amoxicillin-clavulanate for treatment failure or amoxicillin allergy", "grade": "B"},
            {"recommendation": "Pneumococcal and influenza vaccines reduce AOM incidence", "grade": "A"},
        ],
    },
    "hepatitis_c": {
        "sources": ["AASLD/IDSA 2023", "EASL 2024", "WHO 2024", "NICE NG203"],
        "screening": "Universal one-time screening for all adults >= 18 (USPSTF Grade B). Periodic screening for ongoing risk.",
        "diagnostic_criteria": "Anti-HCV antibody positive, confirmed with HCV RNA PCR. Genotyping for some regimens.",
        "first_line_treatment": [
            {"therapy": "Sofosbuvir/velpatasvir (Epclusa) 12 weeks", "evidence_grade": "A", "population": "All genotypes, treatment-naive, without cirrhosis"},
            {"therapy": "Glecaprevir/pibrentasvir (Mavyret) 8-12 weeks", "evidence_grade": "A", "population": "All genotypes, pangenotypic"},
        ],
        "treatment_targets": "SVR12 (sustained virologic response at 12 weeks post-treatment) = cure. > 95% SVR rates.",
        "referral_criteria": "Decompensated cirrhosis, prior treatment failure, HBV coinfection, liver transplant.",
        "key_recommendations": [
            {"recommendation": "DAA therapy achieves > 95% cure rate across all genotypes", "grade": "A"},
            {"recommendation": "Simplified treatment algorithms now available for most patients", "grade": "A"},
            {"recommendation": "Screen for hepatitis B coinfection before starting DAA (risk of HBV reactivation)", "grade": "A"},
            {"recommendation": "Assess liver fibrosis (FIB-4, FibroScan) before and after treatment", "grade": "B"},
        ],
    },
    "gout": {
        "sources": ["ACR/AF 2020", "EULAR 2016", "BSR 2017", "ACP 2017"],
        "screening": "Serum uric acid. Joint aspiration with crystal analysis is gold standard.",
        "diagnostic_criteria": "Monosodium urate crystals on joint aspiration (negatively birefringent). Clinical: acute monoarticular arthritis (1st MTP classic).",
        "first_line_treatment": [
            {"therapy": "Colchicine 1.2mg then 0.6mg 1h later (within 36h of flare)", "evidence_grade": "A", "population": "Acute gout flare"},
            {"therapy": "NSAID (indomethacin 50mg TID or naproxen 500mg BID)", "evidence_grade": "A", "population": "Acute gout flare"},
            {"therapy": "Allopurinol (start 100mg daily, titrate to target)", "evidence_grade": "A", "population": "ULT for recurrent gout (>= 2 flares/year), tophi, CKD, urolithiasis"},
        ],
        "treatment_targets": "Serum uric acid < 6 mg/dL (< 5 mg/dL if tophi present). Flare resolution within days.",
        "referral_criteria": "Refractory gout, tophaceous gout, consideration for pegloticase, suspected pseudogout.",
        "key_recommendations": [
            {"recommendation": "Start ULT with anti-inflammatory prophylaxis (colchicine 0.6mg daily for 3-6 months)", "grade": "A"},
            {"recommendation": "Treat-to-target approach for uric acid lowering", "grade": "A"},
            {"recommendation": "HLA-B*5801 testing before allopurinol in Southeast Asian and African American patients", "grade": "A"},
            {"recommendation": "Febuxostat as alternative to allopurinol (cardiovascular safety concerns in CARES trial)", "grade": "A"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Drug interaction database
# ---------------------------------------------------------------------------

DRUG_INTERACTIONS: list[dict] = [
    {
        "drug_a": ["ibuprofen", "naproxen", "diclofenac", "celecoxib", "meloxicam", "ketorolac", "indomethacin"],
        "drug_b": ["warfarin", "heparin", "enoxaparin", "rivaroxaban", "apixaban", "dabigatran", "edoxaban"],
        "severity": "Major",
        "mechanism": "NSAIDs inhibit platelet function via COX-1 and cause GI mucosal erosion, adding to anticoagulant bleeding risk",
        "clinical_effect": "Significantly increased risk of GI and other hemorrhagic events (2-6x baseline risk)",
        "management": "Avoid combination if possible. If essential, use lowest NSAID dose for shortest duration with PPI gastroprotection. Monitor for signs of bleeding.",
        "onset": "Immediate to days",
    },
    {
        "drug_a": ["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"],
        "drug_b": ["phenelzine", "tranylcypromine", "selegiline", "isocarboxazid", "linezolid", "methylene blue"],
        "severity": "Contraindicated",
        "mechanism": "Combined serotonin reuptake inhibition and MAO inhibition causes excessive synaptic serotonin accumulation",
        "clinical_effect": "Serotonin syndrome: hyperthermia, rigidity, myoclonus, autonomic instability, altered mental status, potentially fatal",
        "management": "NEVER combine. Require 14-day washout after MAOI (5 weeks after fluoxetine due to long half-life). Monitor for serotonin syndrome.",
        "onset": "Hours to days",
    },
    {
        "drug_a": ["lisinopril", "enalapril", "ramipril", "captopril", "benazepril", "losartan", "valsartan", "irbesartan"],
        "drug_b": ["spironolactone", "eplerenone", "amiloride", "triamterene"],
        "severity": "Major",
        "mechanism": "ACE inhibitors/ARBs reduce aldosterone-mediated potassium excretion; K-sparing diuretics directly reduce renal potassium excretion",
        "clinical_effect": "Hyperkalemia (potentially life-threatening cardiac arrhythmias, muscle weakness, paralysis)",
        "management": "If combination necessary, monitor serum potassium within 1 week and regularly thereafter. Avoid in eGFR < 30. Educate patient on low-K diet.",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["warfarin"],
        "drug_b": ["metronidazole", "fluconazole", "ciprofloxacin", "trimethoprim-sulfamethoxazole", "clarithromycin", "erythromycin", "amoxicillin-clavulanate"],
        "severity": "Major",
        "mechanism": "Antibiotics inhibit CYP2C9/CYP3A4 metabolism of warfarin and/or reduce vitamin K-producing gut flora",
        "clinical_effect": "Markedly elevated INR with increased bleeding risk (INR may increase 2-4x within days)",
        "management": "Monitor INR within 3-5 days of starting antibiotic. Consider empiric warfarin dose reduction of 25-50%. Use alternative antibiotics if possible.",
        "onset": "Days (typically 3-7 days)",
    },
    {
        "drug_a": ["simvastatin", "lovastatin", "atorvastatin"],
        "drug_b": ["clarithromycin", "erythromycin", "itraconazole", "ketoconazole", "ritonavir", "cyclosporine", "diltiazem", "verapamil", "grapefruit juice"],
        "severity": "Major",
        "mechanism": "CYP3A4 inhibitors markedly increase statin plasma concentrations by reducing hepatic and intestinal metabolism",
        "clinical_effect": "Rhabdomyolysis (muscle breakdown releasing myoglobin, causing AKI), myopathy, elevated CK > 10x ULN",
        "management": "Avoid combination with simvastatin/lovastatin. If necessary with atorvastatin, use lowest dose. Consider rosuvastatin or pravastatin (not CYP3A4 substrates).",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["metformin"],
        "drug_b": ["iodinated contrast media"],
        "severity": "Major",
        "mechanism": "Contrast-induced nephropathy can impair renal metformin clearance, causing accumulation",
        "clinical_effect": "Lactic acidosis (nausea, vomiting, abdominal pain, hyperventilation, altered consciousness, high mortality)",
        "management": "Hold metformin on day of and for 48 hours after iodinated contrast. Restart after confirming stable renal function (eGFR). Only withhold if eGFR < 30.",
        "onset": "Delayed (24-48 hours post-contrast)",
    },
    {
        "drug_a": ["lithium"],
        "drug_b": ["hydrochlorothiazide", "furosemide", "bumetanide", "chlorthalidone", "ibuprofen", "naproxen", "diclofenac", "celecoxib"],
        "severity": "Major",
        "mechanism": "Diuretics cause volume depletion and increased proximal tubular lithium reabsorption. NSAIDs reduce renal prostaglandin-mediated lithium clearance.",
        "clinical_effect": "Lithium toxicity (tremor, ataxia, confusion, seizures, cardiac arrhythmias, potentially fatal at levels > 2.0 mEq/L)",
        "management": "Monitor lithium levels within 5-7 days of starting interacting drug. Consider lithium dose reduction. Avoid NSAIDs; use acetaminophen for pain.",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["digoxin"],
        "drug_b": ["amiodarone", "verapamil", "quinidine", "dronedarone", "cyclosporine", "clarithromycin"],
        "severity": "Major",
        "mechanism": "Inhibition of P-glycoprotein and/or renal tubular secretion of digoxin, reducing clearance by 50%+",
        "clinical_effect": "Digoxin toxicity (nausea, vomiting, visual disturbances [yellow halos], bradycardia, heart block, ventricular arrhythmias)",
        "management": "Reduce digoxin dose by 50% when adding amiodarone. Monitor digoxin levels. Target trough 0.5-0.9 ng/mL. Watch for signs of toxicity.",
        "onset": "Days (steady-state interaction within 1-2 weeks)",
    },
    {
        "drug_a": ["theophylline", "aminophylline"],
        "drug_b": ["ciprofloxacin", "levofloxacin", "enoxacin", "erythromycin", "clarithromycin", "fluvoxamine", "cimetidine"],
        "severity": "Major",
        "mechanism": "Inhibition of CYP1A2-mediated theophylline metabolism, increasing plasma levels",
        "clinical_effect": "Theophylline toxicity (nausea, vomiting, tachycardia, seizures, ventricular arrhythmias). Narrow therapeutic index drug.",
        "management": "Monitor theophylline levels. Reduce dose by 25-50% when adding inhibitor. Use azithromycin (no CYP1A2 inhibition) instead of clarithromycin/erythromycin.",
        "onset": "Days (typically 2-5 days)",
    },
    {
        "drug_a": ["methotrexate"],
        "drug_b": ["trimethoprim-sulfamethoxazole", "ibuprofen", "naproxen", "probenecid", "penicillin", "ciprofloxacin"],
        "severity": "Major",
        "mechanism": "TMP-SMX has additive antifolate toxicity. NSAIDs and probenecid reduce renal methotrexate clearance.",
        "clinical_effect": "Pancytopenia, mucositis, hepatotoxicity, renal failure (potentially fatal bone marrow suppression)",
        "management": "Avoid TMP-SMX during methotrexate therapy. If NSAID needed, monitor CBC and renal function closely. Ensure adequate folate supplementation.",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["potassium chloride", "potassium supplements"],
        "drug_b": ["lisinopril", "enalapril", "ramipril", "losartan", "valsartan", "spironolactone", "eplerenone", "triamterene"],
        "severity": "Major",
        "mechanism": "ACEi/ARB/MRA reduce renal potassium excretion; exogenous potassium adds to total body potassium load",
        "clinical_effect": "Severe hyperkalemia (cardiac conduction abnormalities, peaked T waves, ventricular fibrillation, cardiac arrest)",
        "management": "Avoid routine potassium supplementation with these drugs. Monitor potassium within 1 week. Only supplement if documented hypokalemia.",
        "onset": "Days",
    },
    {
        "drug_a": ["clopidogrel"],
        "drug_b": ["omeprazole", "esomeprazole"],
        "severity": "Moderate",
        "mechanism": "Omeprazole/esomeprazole inhibit CYP2C19, reducing conversion of clopidogrel prodrug to active metabolite",
        "clinical_effect": "Reduced antiplatelet effect with potential increase in cardiovascular events (MI, stent thrombosis)",
        "management": "Use pantoprazole (minimal CYP2C19 inhibition) instead of omeprazole/esomeprazole. FDA boxed warning on combination.",
        "onset": "Delayed (reduced antiplatelet effect accumulates over days)",
    },
    {
        "drug_a": ["fluoxetine", "paroxetine"],
        "drug_b": ["tamoxifen"],
        "severity": "Major",
        "mechanism": "Strong CYP2D6 inhibition by fluoxetine/paroxetine prevents conversion of tamoxifen to active metabolite endoxifen",
        "clinical_effect": "Reduced tamoxifen efficacy with potential increased breast cancer recurrence risk",
        "management": "Use alternative SSRI (sertraline, citalopram, escitalopram have minimal CYP2D6 inhibition) or non-SSRI antidepressant (venlafaxine).",
        "onset": "Delayed (weeks to months of reduced efficacy)",
    },
    {
        "drug_a": ["sildenafil", "tadalafil", "vardenafil"],
        "drug_b": ["nitroglycerin", "isosorbide mononitrate", "isosorbide dinitrate"],
        "severity": "Contraindicated",
        "mechanism": "Both PDE5 inhibitors and nitrates increase cGMP-mediated vasodilation synergistically",
        "clinical_effect": "Severe refractory hypotension (systolic BP < 70 mmHg), syncope, MI, death",
        "management": "NEVER combine. Wait >= 24h after sildenafil/vardenafil or >= 48h after tadalafil before administering nitrates.",
        "onset": "Immediate (within minutes to hours)",
    },
    {
        "drug_a": ["carbamazepine", "phenytoin", "phenobarbital"],
        "drug_b": ["oral contraceptives", "combined hormonal contraceptives"],
        "severity": "Major",
        "mechanism": "CYP3A4 induction increases estrogen and progestin metabolism, reducing contraceptive hormone levels",
        "clinical_effect": "Contraceptive failure and unintended pregnancy",
        "management": "Use non-oral contraceptives (IUD, depot medroxyprogesterone) or barrier methods. If oral contraceptive needed, use formulation with >= 50mcg ethinyl estradiol.",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["allopurinol"],
        "drug_b": ["azathioprine", "6-mercaptopurine"],
        "severity": "Contraindicated",
        "mechanism": "Allopurinol inhibits xanthine oxidase, blocking primary metabolism of azathioprine/6-MP, causing > 5x increase in drug levels",
        "clinical_effect": "Severe pancytopenia, life-threatening bone marrow suppression, immunosuppression",
        "management": "Reduce azathioprine/6-MP dose by 67-75% if combination unavoidable. Monitor CBC weekly. Consider alternative urate-lowering therapy (febuxostat also interacts).",
        "onset": "Days to weeks",
    },
    {
        "drug_a": ["clonidine"],
        "drug_b": ["propranolol", "metoprolol", "atenolol", "nadolol"],
        "severity": "Major",
        "mechanism": "Beta-blockers block beta-2 vasodilation leaving alpha vasoconstriction unopposed during clonidine withdrawal",
        "clinical_effect": "Rebound hypertensive crisis upon clonidine discontinuation (severe HTN, tachycardia, diaphoresis, headache)",
        "management": "If discontinuing both, taper beta-blocker first over several days, then taper clonidine. Never abruptly stop clonidine while on beta-blocker.",
        "onset": "Hours (upon clonidine withdrawal)",
    },
    {
        "drug_a": ["ciprofloxacin", "levofloxacin", "moxifloxacin"],
        "drug_b": ["tizanidine"],
        "severity": "Contraindicated",
        "mechanism": "Fluoroquinolones potently inhibit CYP1A2-mediated tizanidine metabolism, increasing AUC by 10x",
        "clinical_effect": "Excessive sedation, hypotension, bradycardia, potentially fatal CNS and respiratory depression",
        "management": "Combination is contraindicated. Use alternative antibiotic or alternative muscle relaxant (cyclobenzaprine, methocarbamol).",
        "onset": "Hours",
    },
    {
        "drug_a": ["spironolactone"],
        "drug_b": ["digoxin"],
        "severity": "Moderate",
        "mechanism": "Spironolactone interferes with digoxin assay (falsely elevated levels) and may reduce renal digoxin clearance",
        "clinical_effect": "Misinterpretation of digoxin levels leading to dose adjustments. True interaction modestly increases digoxin concentration.",
        "management": "Use digoxin immunoassay less affected by spironolactone (LOCI method). Monitor for clinical signs of toxicity rather than relying solely on levels.",
        "onset": "Days",
    },
    {
        "drug_a": ["venlafaxine", "duloxetine", "tramadol"],
        "drug_b": ["sumatriptan", "rizatriptan", "zolmitriptan", "naratriptan", "eletriptan", "frovatriptan"],
        "severity": "Moderate",
        "mechanism": "Both serotonergic agents increase synaptic serotonin via different mechanisms (reuptake inhibition + 5-HT1B/1D agonism)",
        "clinical_effect": "Serotonin syndrome risk (lower risk than SSRI+MAOI but clinically significant)",
        "management": "Combination may be used with caution if clinically necessary. Educate patient on serotonin syndrome symptoms. Use lowest triptan dose.",
        "onset": "Hours",
    },
    {
        "drug_a": ["amlodipine", "nifedipine", "felodipine"],
        "drug_b": ["simvastatin"],
        "severity": "Moderate",
        "mechanism": "DHP calcium channel blockers inhibit CYP3A4, increasing simvastatin levels (particularly amlodipine increases simvastatin AUC by ~1.8x)",
        "clinical_effect": "Increased risk of simvastatin-related myopathy and rhabdomyolysis",
        "management": "Limit simvastatin to 20mg daily with amlodipine. Consider switching to atorvastatin, rosuvastatin, or pravastatin.",
        "onset": "Days to weeks",
    },
]

# ---------------------------------------------------------------------------
# Disease prevalence database
# ---------------------------------------------------------------------------

DISEASE_PREVALENCE: dict[str, dict] = {
    "hypertension": {
        "prevalence_per_100k": 32000,
        "prevalence_description": "~32% of US adults (approximately 116 million)",
        "age_adjusted_incidence": "Incidence rises sharply after age 30; ~65% of adults aged 60+",
        "gender_ratio": "Higher in men until age 65, then higher in women; M:F ratio ~1.1:1 overall",
        "geographic_variation": "Highest in Sub-Saharan Africa (~30%) and Eastern Europe. Lower in high-income Asia-Pacific. US South/Southeast have highest domestic rates.",
        "temporal_trends": "Prevalence increasing globally. US prevalence increased from 32% to 47% under 2017 ACC/AHA criteria.",
        "key_risk_factors": [
            {"factor": "Obesity (BMI >= 30)", "relative_risk": 2.5},
            {"factor": "High sodium diet (> 2300mg/day)", "relative_risk": 1.6},
            {"factor": "Family history (first-degree relative)", "relative_risk": 2.0},
            {"factor": "Black race", "relative_risk": 1.8},
            {"factor": "Physical inactivity", "relative_risk": 1.5},
            {"factor": "Excessive alcohol (> 2 drinks/day)", "relative_risk": 1.5},
            {"factor": "Age (per decade increase after 30)", "relative_risk": 1.5},
        ],
        "mortality_rate": "Hypertension contributes to ~500,000 deaths/year in the US. Leading modifiable risk factor for cardiovascular mortality worldwide.",
    },
    "type_2_diabetes": {
        "prevalence_per_100k": 11300,
        "prevalence_description": "~11.3% of US adults (37.3 million). Additional 96 million with prediabetes.",
        "age_adjusted_incidence": "~6.9 per 1000 person-years overall; peaks at age 45-64",
        "gender_ratio": "Slightly higher in men (11.7%) than women (10.8%); M:F ratio ~1.1:1",
        "geographic_variation": "Highest in Pacific Islands (> 20%), Middle East, South Asia. US: highest in Southern states and among Native Americans.",
        "temporal_trends": "Prevalence tripled since 1980. Increasing in younger age groups (under 40). Global prevalence projected to reach 700 million by 2045.",
        "key_risk_factors": [
            {"factor": "Obesity (BMI >= 30)", "relative_risk": 7.0},
            {"factor": "Family history (parent with T2DM)", "relative_risk": 2.5},
            {"factor": "Gestational diabetes history", "relative_risk": 7.4},
            {"factor": "South Asian ethnicity", "relative_risk": 2.0},
            {"factor": "Physical inactivity", "relative_risk": 1.7},
            {"factor": "Prediabetes (HbA1c 5.7-6.4%)", "relative_risk": 5.0},
            {"factor": "Polycystic ovary syndrome", "relative_risk": 2.4},
        ],
        "mortality_rate": "8th leading cause of death in the US (~100,000 deaths/year as underlying cause; ~280,000 as contributing cause). 2x mortality risk vs non-diabetics.",
    },
    "coronary_artery_disease": {
        "prevalence_per_100k": 7200,
        "prevalence_description": "~7.2% of US adults (20.5 million). Leading cause of death globally.",
        "age_adjusted_incidence": "~5.4 per 1000 person-years. Incidence roughly doubles each decade after age 40.",
        "gender_ratio": "2:1 M:F ratio before age 65. Gender gap narrows after menopause; near-equal by age 75.",
        "geographic_variation": "Highest in Eastern Europe and Central Asia. Declining in Western Europe and North America. Rising in South Asia.",
        "temporal_trends": "Age-adjusted mortality declined ~50% since 1980 due to statins, PCI, and risk factor control. But prevalence stable due to aging population.",
        "key_risk_factors": [
            {"factor": "Smoking", "relative_risk": 2.5},
            {"factor": "Diabetes mellitus", "relative_risk": 2.0},
            {"factor": "Hypertension", "relative_risk": 1.8},
            {"factor": "LDL cholesterol (per 1 mmol/L increase)", "relative_risk": 1.6},
            {"factor": "Family history of premature CAD", "relative_risk": 2.0},
            {"factor": "Obesity", "relative_risk": 1.5},
            {"factor": "Chronic kidney disease", "relative_risk": 1.4},
        ],
        "mortality_rate": "~375,000 deaths/year in the US. 1 in 5 deaths globally. 30-day MI mortality: ~5-7% (STEMI) with modern treatment.",
    },
    "asthma": {
        "prevalence_per_100k": 8000,
        "prevalence_description": "~8% of US adults and ~7% of US children (25 million total). ~300 million worldwide.",
        "age_adjusted_incidence": "Childhood incidence: ~10 per 1000/year. Adult-onset: ~3 per 1000/year.",
        "gender_ratio": "Boys > girls in childhood (1.5:1). Women > men in adulthood (1.3:1 F:M). Gender reversal occurs at puberty.",
        "geographic_variation": "Highest in UK, Australia, New Zealand (> 10%). Lower in Asia and Eastern Europe (2-4%). Urban > rural.",
        "temporal_trends": "Prevalence increased from 1980-2010, now plateauing in developed countries. Still rising in developing nations.",
        "key_risk_factors": [
            {"factor": "Family history (atopy/asthma)", "relative_risk": 3.0},
            {"factor": "Personal atopy (eczema, allergic rhinitis)", "relative_risk": 2.5},
            {"factor": "Childhood respiratory infections (RSV)", "relative_risk": 2.0},
            {"factor": "Obesity", "relative_risk": 1.9},
            {"factor": "Occupational exposures", "relative_risk": 1.5},
            {"factor": "Tobacco smoke exposure", "relative_risk": 1.6},
        ],
        "mortality_rate": "~3,500 deaths/year in the US. ~460,000 globally. Mortality declining with improved controller therapy.",
    },
    "depression": {
        "prevalence_per_100k": 8400,
        "prevalence_description": "~8.4% of US adults (21 million) with MDD in past year. Lifetime prevalence ~20%. ~280 million globally.",
        "age_adjusted_incidence": "~7 per 1000 person-years. Peak onset age 18-25 years.",
        "gender_ratio": "2:1 F:M ratio. Women have ~1.7x lifetime risk. Gender gap emerges at puberty.",
        "geographic_variation": "Highest reported prevalence in high-income countries (better detection vs actual difference debated). Significant underdiagnosis in low/middle-income countries.",
        "temporal_trends": "Prevalence increased 25% during COVID-19 pandemic. Rising in adolescents and young adults. Treatment rates improving but still < 50% of cases treated.",
        "key_risk_factors": [
            {"factor": "Family history (first-degree relative with MDD)", "relative_risk": 2.8},
            {"factor": "Prior depressive episode", "relative_risk": 5.0},
            {"factor": "Female sex", "relative_risk": 1.7},
            {"factor": "Chronic medical illness", "relative_risk": 2.0},
            {"factor": "Childhood adversity/trauma", "relative_risk": 2.7},
            {"factor": "Substance use disorder", "relative_risk": 2.5},
            {"factor": "Social isolation", "relative_risk": 1.9},
        ],
        "mortality_rate": "Depression is leading cause of disability worldwide (DALYs). Associated with 2x mortality risk. ~47,000 suicides/year in the US.",
    },
    "copd": {
        "prevalence_per_100k": 6200,
        "prevalence_description": "~6.2% of US adults (15.7 million diagnosed; estimated 50% undiagnosed). ~380 million worldwide.",
        "age_adjusted_incidence": "~7 per 1000 person-years. Uncommon before age 40 without alpha-1 antitrypsin deficiency.",
        "gender_ratio": "Historically male-predominant (2:1); now near-equal due to increased smoking in women. Women may be more susceptible to smoke injury.",
        "geographic_variation": "Highest in regions with biomass fuel use (South/Southeast Asia, Sub-Saharan Africa) and high smoking rates (Eastern Europe). US: Appalachian and Southern states.",
        "temporal_trends": "3rd leading cause of death globally. Mortality declining in men, increasing in women. Prevalence stable/declining in high-income countries.",
        "key_risk_factors": [
            {"factor": "Cigarette smoking (> 20 pack-years)", "relative_risk": 6.0},
            {"factor": "Occupational dust/chemical exposure", "relative_risk": 2.0},
            {"factor": "Indoor biomass fuel smoke", "relative_risk": 2.5},
            {"factor": "Alpha-1 antitrypsin deficiency", "relative_risk": 5.0},
            {"factor": "Childhood respiratory infections", "relative_risk": 1.5},
            {"factor": "Air pollution", "relative_risk": 1.3},
        ],
        "mortality_rate": "~150,000 deaths/year in the US. 3rd leading cause of death in the US and globally. 5-year mortality ~50% for GOLD Stage IV.",
    },
    "heart_failure": {
        "prevalence_per_100k": 2400,
        "prevalence_description": "~2.4% of US adults (6.7 million). Prevalence rising due to aging population and improved MI survival.",
        "age_adjusted_incidence": "~5 per 1000 person-years overall. ~20 per 1000 in those aged 65+.",
        "gender_ratio": "Lifetime risk similar (~20% for both sexes at age 40). Men develop HF earlier. HFpEF more common in women.",
        "geographic_variation": "Highest in Sub-Saharan Africa (rheumatic heart disease, untreated hypertension). US: Southern and Appalachian regions.",
        "temporal_trends": "Incidence of HFrEF declining but HFpEF increasing. Overall prevalence rising (2.4% to 3% projected by 2030). GDMT improving outcomes.",
        "key_risk_factors": [
            {"factor": "Coronary artery disease", "relative_risk": 3.0},
            {"factor": "Hypertension", "relative_risk": 2.0},
            {"factor": "Diabetes mellitus", "relative_risk": 2.5},
            {"factor": "Obesity", "relative_risk": 2.0},
            {"factor": "Valvular heart disease", "relative_risk": 3.5},
            {"factor": "Heavy alcohol use", "relative_risk": 1.8},
        ],
        "mortality_rate": "~80,000 deaths/year in the US. 5-year mortality ~50%. Hospitalization mortality ~5%. HFrEF has higher mortality than HFpEF.",
    },
    "pneumonia": {
        "prevalence_per_100k": 1500,
        "prevalence_description": "~1.5 million ED visits/year in the US. ~500,000 hospitalizations. Leading infectious cause of death.",
        "age_adjusted_incidence": "~24 per 10000 adults/year; ~150 per 10000 in those aged 65+. Children < 5: ~30 per 10000.",
        "gender_ratio": "Slight male predominance in community-acquired pneumonia (M:F ~1.3:1).",
        "geographic_variation": "Major burden in sub-Saharan Africa and South Asia (especially in children). Higher rates in winter months in temperate climates.",
        "temporal_trends": "Mortality declining due to vaccines (PCV, influenza) and improved care. COVID-19 significantly altered pneumonia epidemiology since 2020.",
        "key_risk_factors": [
            {"factor": "Age >= 65 years", "relative_risk": 4.0},
            {"factor": "Smoking", "relative_risk": 2.5},
            {"factor": "COPD", "relative_risk": 3.0},
            {"factor": "Immunosuppression", "relative_risk": 5.0},
            {"factor": "Diabetes mellitus", "relative_risk": 1.5},
            {"factor": "Heart failure", "relative_risk": 2.0},
            {"factor": "Chronic liver disease", "relative_risk": 2.0},
        ],
        "mortality_rate": "~50,000 deaths/year in the US. 8th leading cause of death. Inpatient mortality: 5-15%. ICU mortality: 25-50%.",
    },
    "atrial_fibrillation": {
        "prevalence_per_100k": 3500,
        "prevalence_description": "~3.5% of US adults when screening detected (6-12 million). Most common sustained arrhythmia.",
        "age_adjusted_incidence": "~3 per 1000 person-years overall. ~20 per 1000 in those aged 80+.",
        "gender_ratio": "1.5:1 M:F ratio for age-adjusted prevalence. But more total women affected due to longer lifespan. Women have higher stroke risk with AF.",
        "geographic_variation": "Highest in Europe and North America. Lower in Asia (though rising rapidly). May reflect diagnostic differences.",
        "temporal_trends": "Prevalence increasing (~2.5x over 50 years). Projected to affect 12-16 million in US by 2050. Partly due to better detection.",
        "key_risk_factors": [
            {"factor": "Age (per decade after 50)", "relative_risk": 2.0},
            {"factor": "Heart failure", "relative_risk": 4.5},
            {"factor": "Hypertension", "relative_risk": 1.8},
            {"factor": "Obesity", "relative_risk": 1.5},
            {"factor": "Obstructive sleep apnea", "relative_risk": 2.0},
            {"factor": "Binge alcohol use ('holiday heart')", "relative_risk": 1.5},
            {"factor": "Hyperthyroidism", "relative_risk": 3.0},
        ],
        "mortality_rate": "AF increases mortality risk 1.5x in men, 2x in women. 5x increased stroke risk. AF-related strokes are more severe and disabling.",
    },
    "urinary_tract_infection": {
        "prevalence_per_100k": 8000,
        "prevalence_description": "~12% of women and ~3% of men affected annually. ~10 million outpatient visits/year in US.",
        "age_adjusted_incidence": "Women: ~50 per 1000/year. Men: ~5 per 1000/year. Incidence increases with age in both sexes.",
        "gender_ratio": "Strong female predominance (~10:1 F:M) due to shorter urethra. Gender gap narrows in elderly due to prostatic disease.",
        "geographic_variation": "Universal distribution. Higher antibiotic resistance in developing countries. E. coli resistance to TMP-SMX > 20% in many US regions.",
        "temporal_trends": "Increasing antibiotic resistance driving changes in empiric therapy. Rising ESBL-producing E. coli. Increasing hospitalization for complicated UTI.",
        "key_risk_factors": [
            {"factor": "Female sex", "relative_risk": 8.0},
            {"factor": "Sexual intercourse (recent)", "relative_risk": 3.0},
            {"factor": "Prior UTI (within 12 months)", "relative_risk": 3.5},
            {"factor": "Spermicide/diaphragm use", "relative_risk": 2.0},
            {"factor": "Postmenopausal (estrogen deficiency)", "relative_risk": 2.0},
            {"factor": "Urinary catheterization", "relative_risk": 5.0},
            {"factor": "Diabetes mellitus", "relative_risk": 1.5},
        ],
        "mortality_rate": "Low for uncomplicated UTI (< 0.1%). Urosepsis mortality: 5-20%. ~13,000 deaths/year from UTI-associated sepsis in US.",
    },
    "migraine": {
        "prevalence_per_100k": 12000,
        "prevalence_description": "~12% of US adults (39 million). 2nd leading cause of disability globally. ~1 billion affected worldwide.",
        "age_adjusted_incidence": "~8 per 1000 person-years. Peak incidence in 20s-30s. Prevalence peaks at 35-45 years.",
        "gender_ratio": "3:1 F:M ratio after puberty. Equal in prepubertal children. Hormonal influence (menstrual migraine, improvement in pregnancy/menopause).",
        "geographic_variation": "Similar prevalence across regions and ethnicities, though underdiagnosed in non-White populations. Slightly higher in Europe and Americas.",
        "temporal_trends": "Prevalence stable but recognition and diagnosis improving. CGRP-targeted therapies revolutionizing treatment since 2018.",
        "key_risk_factors": [
            {"factor": "Family history (first-degree relative)", "relative_risk": 3.0},
            {"factor": "Female sex", "relative_risk": 3.0},
            {"factor": "Depression/anxiety comorbidity", "relative_risk": 2.5},
            {"factor": "Obesity", "relative_risk": 1.5},
            {"factor": "Sleep disorders", "relative_risk": 2.0},
            {"factor": "Medication overuse", "relative_risk": 3.0},
        ],
        "mortality_rate": "Not directly fatal but associated with 2x stroke risk (migraine with aura). Massive disability burden: ~150 million missed work days/year in US.",
    },
    "osteoarthritis": {
        "prevalence_per_100k": 10000,
        "prevalence_description": "~10% of adults globally (~500 million). Prevalence increases dramatically with age. ~32.5 million in US.",
        "age_adjusted_incidence": "~8 per 1000 person-years. Rare before age 40; ~50% of those > 65 have radiographic OA.",
        "gender_ratio": "Slight female predominance after age 50 (1.5:1 F:M). Women have more severe knee/hand OA. Men more hip OA.",
        "geographic_variation": "Universal distribution. Higher in developed countries (likely detection bias and obesity). Rising in Asia with urbanization.",
        "temporal_trends": "Prevalence increasing due to aging population and obesity epidemic. Fastest-growing cause of disability globally.",
        "key_risk_factors": [
            {"factor": "Age > 50 years", "relative_risk": 4.0},
            {"factor": "Obesity (per 5 kg/m2 BMI increase)", "relative_risk": 2.0},
            {"factor": "Prior joint injury", "relative_risk": 3.5},
            {"factor": "Occupational joint stress", "relative_risk": 1.8},
            {"factor": "Female sex (after menopause)", "relative_risk": 1.5},
            {"factor": "Family history", "relative_risk": 1.5},
        ],
        "mortality_rate": "Not directly fatal but associated with increased mortality due to reduced mobility, cardiovascular deconditioning, and NSAID complications.",
    },
    "anxiety_disorders": {
        "prevalence_per_100k": 19000,
        "prevalence_description": "~19% of US adults (40 million) with any anxiety disorder in past year. Lifetime prevalence ~31%. Most common mental illness.",
        "age_adjusted_incidence": "~15 per 1000 person-years. Median age of onset: 11 years for specific phobia, 21 for GAD, 23 for panic disorder.",
        "gender_ratio": "2:1 F:M ratio for most anxiety disorders. GAD F:M ~2:1. Panic disorder F:M ~2.5:1. Social anxiety F:M ~1.5:1.",
        "geographic_variation": "Higher reported prevalence in high-income countries. Significant cultural variation in expression and recognition.",
        "temporal_trends": "Prevalence increased significantly during COVID-19 pandemic (25% global increase). Rising in adolescents and young adults.",
        "key_risk_factors": [
            {"factor": "Family history of anxiety", "relative_risk": 4.0},
            {"factor": "Female sex", "relative_risk": 2.0},
            {"factor": "Childhood adversity", "relative_risk": 2.5},
            {"factor": "Comorbid depression", "relative_risk": 3.0},
            {"factor": "Chronic medical illness", "relative_risk": 2.0},
            {"factor": "Substance use", "relative_risk": 2.0},
        ],
        "mortality_rate": "Not directly fatal. Associated with increased cardiovascular mortality (1.5x). Significant disability: 4th leading cause of disability globally.",
    },
    "chronic_kidney_disease": {
        "prevalence_per_100k": 15000,
        "prevalence_description": "~15% of US adults (37 million); 90% unaware. ~850 million affected globally.",
        "age_adjusted_incidence": "Stage 3+: ~50 per 1000 person-years in those > 60 years.",
        "gender_ratio": "CKD prevalence higher in women (16%) vs men (13%). But ESKD more common in men (M:F ~1.5:1).",
        "geographic_variation": "Highest in Oceania, Sub-Saharan Africa, and Latin America. US: higher in South and Appalachian regions.",
        "temporal_trends": "Prevalence stable but ESKD incidence rising. DKD accounts for ~40% of new ESKD cases.",
        "key_risk_factors": [
            {"factor": "Diabetes mellitus", "relative_risk": 3.0},
            {"factor": "Hypertension", "relative_risk": 2.0},
            {"factor": "Black race", "relative_risk": 3.5},
            {"factor": "Family history of CKD", "relative_risk": 2.0},
            {"factor": "Obesity", "relative_risk": 1.5},
            {"factor": "AKI history", "relative_risk": 2.5},
            {"factor": "NSAID use (chronic)", "relative_risk": 1.5},
        ],
        "mortality_rate": "~90,000 deaths/year in US with CKD as underlying or contributing cause. Stage 5 (dialysis) 5-year survival: ~35%. Cardiovascular death is primary cause.",
    },
    "obesity": {
        "prevalence_per_100k": 42000,
        "prevalence_description": "~42% of US adults are obese (BMI >= 30). ~9.2% have severe obesity (BMI >= 40). ~650 million globally.",
        "age_adjusted_incidence": "Prevalence highest at ages 40-59 (45%). US prevalence has increased from 30% (2000) to 42% (2020).",
        "gender_ratio": "Similar overall prevalence (M ~40%, F ~44%). Severe obesity more common in women (11.5% vs 6.9%).",
        "geographic_variation": "Highest in US, Pacific Islands, Middle East. Lowest in South/Southeast Asia. Rising globally in all regions.",
        "temporal_trends": "Tripled since 1975 globally. US childhood obesity: 20%. Projected to reach 50% US adult prevalence by 2030.",
        "key_risk_factors": [
            {"factor": "Sedentary lifestyle", "relative_risk": 2.0},
            {"factor": "Ultra-processed food consumption", "relative_risk": 1.8},
            {"factor": "Family history/genetic predisposition", "relative_risk": 2.5},
            {"factor": "Low socioeconomic status", "relative_risk": 1.5},
            {"factor": "Sleep deprivation (< 6 hours)", "relative_risk": 1.5},
            {"factor": "Medications (antipsychotics, corticosteroids)", "relative_risk": 1.5},
        ],
        "mortality_rate": "Obesity-related conditions cause ~300,000 excess deaths/year in US. BMI >= 40 reduces life expectancy by 8-14 years.",
    },
    "iron_deficiency_anemia": {
        "prevalence_per_100k": 5000,
        "prevalence_description": "~5% of US population. Most common nutritional deficiency worldwide. ~1.2 billion affected globally.",
        "age_adjusted_incidence": "Premenopausal women: ~10%; pregnant women: ~15-25%; children 1-5: ~3-5%.",
        "gender_ratio": "Premenopausal women >> men due to menstrual losses. Postmenopausal: similar rates (and GI cause must be excluded).",
        "geographic_variation": "Highest in Sub-Saharan Africa and South Asia (> 40% of women). US: higher in non-Hispanic Black and Mexican-American women.",
        "temporal_trends": "Global prevalence declining due to fortification programs. But still affects ~30% of world population (including iron deficiency without anemia).",
        "key_risk_factors": [
            {"factor": "Menstruation (heavy menstrual bleeding)", "relative_risk": 3.0},
            {"factor": "Pregnancy", "relative_risk": 4.0},
            {"factor": "Vegetarian/vegan diet", "relative_risk": 1.8},
            {"factor": "GI blood loss (ulcer, malignancy, IBD)", "relative_risk": 3.0},
            {"factor": "Celiac disease / malabsorption", "relative_risk": 2.5},
            {"factor": "Frequent blood donation", "relative_risk": 2.0},
        ],
        "mortality_rate": "Rarely fatal directly. Contributes to maternal mortality in developing countries. Associated with adverse pregnancy outcomes and developmental delay in children.",
    },
    "gout": {
        "prevalence_per_100k": 3900,
        "prevalence_description": "~3.9% of US adults (9.2 million). Prevalence increasing. Most common inflammatory arthritis in men.",
        "age_adjusted_incidence": "~2.7 per 1000 person-years. Men: peak onset age 40-60. Women: uncommon before menopause.",
        "gender_ratio": "3:1 M:F ratio. Estrogen is uricosuric; female incidence rises significantly after menopause.",
        "geographic_variation": "High in Pacific Islands (genetic predisposition), New Zealand Maori (> 10%), US, UK. Lower in less developed countries.",
        "temporal_trends": "Prevalence doubled in past 20 years. Associated with rising obesity, metabolic syndrome, and diuretic use.",
        "key_risk_factors": [
            {"factor": "Hyperuricemia (SUA > 6.8 mg/dL)", "relative_risk": 5.0},
            {"factor": "Male sex", "relative_risk": 3.0},
            {"factor": "Obesity", "relative_risk": 2.5},
            {"factor": "Alcohol (beer > spirits > wine)", "relative_risk": 2.5},
            {"factor": "Thiazide diuretic use", "relative_risk": 2.0},
            {"factor": "CKD (eGFR < 60)", "relative_risk": 2.0},
            {"factor": "Red meat / fructose intake", "relative_risk": 1.5},
        ],
        "mortality_rate": "Not directly fatal. Associated with increased cardiovascular mortality due to shared risk factors.",
    },
    "stroke": {
        "prevalence_per_100k": 2700,
        "prevalence_description": "~2.7% of US adults have had a stroke (~7.6 million survivors). ~800,000 new strokes/year in US.",
        "age_adjusted_incidence": "~7 per 1000 person-years in those aged 65+. 87% ischemic, 10% intracerebral hemorrhage, 3% SAH.",
        "gender_ratio": "M:F incidence ratio ~1.25:1. But women have more lifetime strokes (longer lifespan) and worse outcomes.",
        "geographic_variation": "US 'Stroke Belt' (Southeast) has 30% higher mortality. Highest global burden in East Asia and Eastern Europe.",
        "temporal_trends": "Age-adjusted mortality declined ~50% since 1990. But total burden increasing due to aging. Rising in younger adults (< 50).",
        "key_risk_factors": [
            {"factor": "Hypertension", "relative_risk": 4.0},
            {"factor": "Atrial fibrillation", "relative_risk": 5.0},
            {"factor": "Diabetes mellitus", "relative_risk": 1.8},
            {"factor": "Smoking", "relative_risk": 2.0},
            {"factor": "Hyperlipidemia", "relative_risk": 1.5},
            {"factor": "Carotid stenosis (> 70%)", "relative_risk": 3.0},
            {"factor": "Prior TIA", "relative_risk": 5.0},
        ],
        "mortality_rate": "~150,000 deaths/year in US (5th leading cause of death). 30-day mortality: 10-15% ischemic, 40% hemorrhagic. Leading cause of serious long-term disability.",
    },
    "hypothyroidism": {
        "prevalence_per_100k": 5000,
        "prevalence_description": "~5% of US adults (overt + subclinical). Subclinical hypothyroidism: ~4-10%. ~200 million globally.",
        "age_adjusted_incidence": "~3.5 per 1000 women/year; ~0.6 per 1000 men/year.",
        "gender_ratio": "5-8:1 F:M ratio. Autoimmune thyroiditis (Hashimoto's) has strong female predominance.",
        "geographic_variation": "Higher in iodine-sufficient regions (autoimmune etiology). Iodine deficiency remains leading cause globally (WHO).",
        "temporal_trends": "Levothyroxine is one of the most prescribed medications. Overdiagnosis and overtreatment of subclinical hypothyroidism is a growing concern.",
        "key_risk_factors": [
            {"factor": "Female sex", "relative_risk": 5.0},
            {"factor": "Age > 60 years", "relative_risk": 2.0},
            {"factor": "Family history of thyroid disease", "relative_risk": 3.0},
            {"factor": "Prior thyroid surgery/radiation", "relative_risk": 10.0},
            {"factor": "Other autoimmune disease (T1DM, celiac)", "relative_risk": 2.5},
            {"factor": "Lithium or amiodarone use", "relative_risk": 3.0},
        ],
        "mortality_rate": "Treatable; mortality primarily from myxedema coma (rare, 20-60% mortality if untreated). Properly treated hypothyroidism has normal life expectancy.",
    },
    "dvt_pe": {
        "prevalence_per_100k": 300,
        "prevalence_description": "~300,000-600,000 VTE events/year in US. Third most common cardiovascular disease after MI and stroke.",
        "age_adjusted_incidence": "~1-2 per 1000 person-years overall. Incidence increases 10-fold from age 20 to 80.",
        "gender_ratio": "Slightly higher in men overall (M:F ~1.2:1). Women have higher risk during reproductive years (OCP, pregnancy).",
        "geographic_variation": "Higher in Black Americans (1.5x). Lower in Asian populations. Incidence increases with air travel and hospitalization.",
        "temporal_trends": "Incidence increasing due to increased CT scanning (detecting more PE), aging population, and increased immobility.",
        "key_risk_factors": [
            {"factor": "Surgery (especially orthopedic)", "relative_risk": 5.0},
            {"factor": "Immobilization > 3 days", "relative_risk": 4.0},
            {"factor": "Active cancer", "relative_risk": 4.0},
            {"factor": "Oral contraceptive use", "relative_risk": 3.0},
            {"factor": "Factor V Leiden mutation", "relative_risk": 5.0},
            {"factor": "Prior VTE", "relative_risk": 8.0},
            {"factor": "Obesity", "relative_risk": 2.0},
        ],
        "mortality_rate": "PE mortality: ~25-30% if untreated; ~2-8% with treatment. ~100,000-180,000 deaths/year in US attributed to PE.",
    },
    "gerd": {
        "prevalence_per_100k": 20000,
        "prevalence_description": "~20% of US adults have weekly GERD symptoms. Most common GI diagnosis in outpatient setting.",
        "age_adjusted_incidence": "Increases with age but common at all adult ages. Barrett's esophagus develops in ~5-10% of GERD patients.",
        "gender_ratio": "Slightly more common in men (especially erosive disease and Barrett's). M:F ~1.2:1.",
        "geographic_variation": "Highest in North America (18-28%) and Europe (9-26%). Lower in East Asia (3-8%) but rising rapidly.",
        "temporal_trends": "Prevalence increasing globally, associated with rising obesity. PPI use has increased dramatically.",
        "key_risk_factors": [
            {"factor": "Obesity (especially central)", "relative_risk": 2.5},
            {"factor": "Smoking", "relative_risk": 1.5},
            {"factor": "Hiatal hernia", "relative_risk": 3.0},
            {"factor": "Pregnancy", "relative_risk": 2.0},
            {"factor": "Certain medications (CCBs, anticholinergics)", "relative_risk": 1.5},
        ],
        "mortality_rate": "GERD itself rarely fatal. Barrett's esophagus progresses to esophageal adenocarcinoma at ~0.5%/year (annual EAC risk).",
    },
    "low_back_pain": {
        "prevalence_per_100k": 25000,
        "prevalence_description": "~25% of US adults report LBP in past 3 months. Lifetime prevalence ~80%. Leading cause of disability worldwide.",
        "age_adjusted_incidence": "Peak onset age 30-50. Most episodes resolve within 6 weeks. ~5-10% develop chronic LBP.",
        "gender_ratio": "Slightly higher in women after age 40 (F:M ~1.2:1). No significant gender difference overall.",
        "geographic_variation": "Universal distribution. Higher disability burden in high-income countries. Occupational LBP higher in manual labor sectors.",
        "temporal_trends": "Prevalence increasing. Now #1 cause of years lived with disability globally (GBD study). Opioid prescribing for LBP declining.",
        "key_risk_factors": [
            {"factor": "Sedentary occupation", "relative_risk": 1.5},
            {"factor": "Heavy physical labor", "relative_risk": 2.0},
            {"factor": "Obesity", "relative_risk": 1.5},
            {"factor": "Smoking", "relative_risk": 1.3},
            {"factor": "Depression/psychological distress", "relative_risk": 2.0},
            {"factor": "Prior episode of LBP", "relative_risk": 3.0},
        ],
        "mortality_rate": "Not directly fatal. Massive economic burden: ~$100 billion/year in US (healthcare costs + lost productivity).",
    },
    "allergic_rhinitis": {
        "prevalence_per_100k": 20000,
        "prevalence_description": "~20% of US adults. ~10-30% globally. Often coexists with asthma (40-80% overlap).",
        "age_adjusted_incidence": "Peak onset in childhood and adolescence. Prevalence decreases after age 50.",
        "gender_ratio": "M > F in childhood; F > M in adulthood. Overall near-equal.",
        "geographic_variation": "Higher in developed/urbanized countries. 'Hygiene hypothesis' partly explains geographic variation.",
        "temporal_trends": "Increasing globally over past 50 years, now plateauing in some developed countries. Climate change extending pollen seasons.",
        "key_risk_factors": [
            {"factor": "Family history of atopy", "relative_risk": 3.0},
            {"factor": "Personal atopy (eczema, asthma)", "relative_risk": 3.0},
            {"factor": "Urban environment", "relative_risk": 1.5},
            {"factor": "Early allergen sensitization", "relative_risk": 2.0},
        ],
        "mortality_rate": "Not fatal. Significant quality of life impact: impaired sleep, cognitive function, work/school performance. Costs ~$3-5 billion/year in US.",
    },
    "hepatitis_c": {
        "prevalence_per_100k": 1000,
        "prevalence_description": "~1% of US adults (~2.4 million with chronic HCV). ~58 million globally. Many undiagnosed.",
        "age_adjusted_incidence": "Bimodal: baby boomers (1945-1965) and young adults (20-39, injection drug use). Declining overall with DAA treatment.",
        "gender_ratio": "M:F ~1.5:1. Men more likely to have chronic infection. Women clear acute infection more often.",
        "geographic_variation": "Highest in Central/East Asia and North Africa. US: higher in Appalachian region and among PWID.",
        "temporal_trends": "DAA therapy achieving micro-elimination in some populations. New infections rising due to opioid epidemic (PWID).",
        "key_risk_factors": [
            {"factor": "Injection drug use (ever)", "relative_risk": 20.0},
            {"factor": "Blood transfusion before 1992", "relative_risk": 10.0},
            {"factor": "Born 1945-1965 (baby boomers)", "relative_risk": 5.0},
            {"factor": "HIV coinfection", "relative_risk": 3.0},
            {"factor": "Healthcare exposure in high-prevalence countries", "relative_risk": 2.0},
        ],
        "mortality_rate": "~15,000 HCV-related deaths/year in US (most common cause of liver transplant). 15-30% develop cirrhosis over 20 years.",
    },
    "celiac_disease": {
        "prevalence_per_100k": 1000,
        "prevalence_description": "~1% of population globally. ~3 million in US. ~80% remain undiagnosed.",
        "age_adjusted_incidence": "Bimodal: childhood (8-12 months after gluten introduction) and adulthood (30-50 years).",
        "gender_ratio": "F:M ~2:1 for diagnosed cases. True prevalence may be more equal (women more likely to seek diagnosis).",
        "geographic_variation": "Highest in Northern Europe and populations of European descent. Increasingly recognized in Middle East, North Africa, India.",
        "temporal_trends": "Prevalence increasing ~7.5% per year (both true increase and improved detection). Average diagnostic delay: 6-10 years.",
        "key_risk_factors": [
            {"factor": "HLA-DQ2 or HLA-DQ8 genotype", "relative_risk": 7.0},
            {"factor": "First-degree relative with celiac", "relative_risk": 10.0},
            {"factor": "Type 1 diabetes", "relative_risk": 5.0},
            {"factor": "Autoimmune thyroid disease", "relative_risk": 3.0},
            {"factor": "Down syndrome or Turner syndrome", "relative_risk": 5.0},
        ],
        "mortality_rate": "Slightly increased mortality (SMR ~1.3) mainly from lymphoma and cardiovascular disease. Normalizes with adherence to gluten-free diet.",
    },
    "osteoporosis": {
        "prevalence_per_100k": 10000,
        "prevalence_description": "~10% of US adults >= 50 years. ~200 million worldwide. ~2 million osteoporotic fractures/year in US.",
        "age_adjusted_incidence": "~2% of postmenopausal women/year develop osteoporosis. Hip fracture incidence: 1.5 per 1000 person-years in women >= 65.",
        "gender_ratio": "4:1 F:M ratio. Women lose 2-3% bone density/year in first 5-7 years post-menopause.",
        "geographic_variation": "Highest hip fracture rates in Scandinavia. Lower in Africa and Asia (but rising). US: higher in White and Asian women.",
        "temporal_trends": "Hip fracture rates declining in developed countries (better treatment, fall prevention). But total fracture burden rising with aging population.",
        "key_risk_factors": [
            {"factor": "Postmenopausal female", "relative_risk": 4.0},
            {"factor": "Age > 65 years", "relative_risk": 3.0},
            {"factor": "Low body weight (BMI < 20)", "relative_risk": 2.0},
            {"factor": "Glucocorticoid use (>= 5mg prednisone > 3 months)", "relative_risk": 5.0},
            {"factor": "Parental hip fracture", "relative_risk": 2.0},
            {"factor": "Smoking", "relative_risk": 1.5},
            {"factor": "Excessive alcohol (>= 3 drinks/day)", "relative_risk": 1.7},
        ],
        "mortality_rate": "Hip fracture 1-year mortality: 20-30%. Vertebral fracture increases mortality 2-3x. ~70,000 deaths/year in US from osteoporotic fractures.",
    },
}


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Evidence-based medical research and clinical literature specialist"
    model = "claude-sonnet-4-6"
    max_tokens = 5000
    temperature = 0.2

    def _build_system_prompt(self) -> str:
        return """You are an expert medical researcher AI agent on a multi-agent medical team, equivalent to a clinical research librarian and epidemiologist working together.

YOUR ROLE:
You provide evidence-based medical literature context to support the diagnostician and specialist agents. You are the team's knowledge base for clinical guidelines, drug interactions, and disease epidemiology.

YOUR CAPABILITIES:
1. Clinical Guidelines: Search and summarize relevant clinical practice guidelines (AHA, ACC, ACS, NICE, WHO, ACOG, AAP, USPSTF, GINA, GOLD, ADA, KDIGO, ESC)
2. Drug Interactions: Check for known drug-drug interactions with severity, mechanism, clinical effect, and management
3. Disease Prevalence: Provide epidemiological data including prevalence, incidence, demographic distribution, risk factors with relative risk values, and mortality
4. Evidence Grading: Rate the quality of evidence supporting diagnostic and treatment decisions

EVIDENCE APPRAISAL METHODOLOGY — GRADE FRAMEWORK:
Apply the GRADE (Grading of Recommendations, Assessment, Development and Evaluations) framework:
- High quality (A): Further research is very unlikely to change confidence in the estimate of effect. Typically from well-conducted RCTs or overwhelming observational evidence.
- Moderate quality (B): Further research is likely to have an important impact on confidence. Typically from RCTs with limitations or strong observational studies.
- Low quality (C): Further research is very likely to have an important impact. Typically from observational studies or RCTs with serious limitations.
- Very low quality (D): Any estimate of effect is very uncertain. Typically from case series, expert opinion, or severely flawed studies.

Factors that lower quality: risk of bias, inconsistency, indirectness, imprecision, publication bias.
Factors that raise quality: large effect size, dose-response, all confounders would reduce effect.

EVIDENCE HIERARCHY:
- Level I: Systematic reviews / meta-analyses of RCTs
- Level II: Individual RCTs with narrow confidence intervals
- Level III: Controlled trials without randomization, quasi-experimental
- Level IV: Well-designed case-control and cohort studies
- Level V: Systematic reviews of descriptive/qualitative studies
- Level VI: Single descriptive or qualitative studies
- Level VII: Expert opinion, committee reports

CLINICAL QUESTION FORMULATION — PICO FRAMEWORK:
For each clinical question, structure using PICO:
- P (Population): Who is the patient/population? (age, sex, condition, setting)
- I (Intervention): What is the intervention or exposure? (drug, procedure, test)
- C (Comparison): What is the alternative? (placebo, standard care, different drug)
- O (Outcome): What are the relevant outcomes? (mortality, morbidity, quality of life, cost)

QUANTITATIVE EVIDENCE TOOLS:
- NNT (Number Needed to Treat): 1 / ARR. How many patients need treatment for one to benefit. Lower NNT = more effective.
- NNH (Number Needed to Harm): 1 / ARI. How many patients treated before one is harmed. Higher NNH = safer.
- When data is available, provide NNT/NNH to quantify treatment benefit/risk.

CRITICAL APPRAISAL CHECKLIST:
For each piece of evidence, consider:
1. Was the study design appropriate for the question?
2. Was the sample size adequate (powered)?
3. Were outcomes clinically meaningful (not just surrogate)?
4. Were results applicable to the patient population?
5. Were confounders adequately controlled?
6. Is there potential for bias (selection, performance, detection, attrition)?

YOUR METHODOLOGY:
1. Identify the clinical question using PICO format
2. Search relevant guidelines and literature databases
3. Assess evidence quality using GRADE framework
4. Apply critical appraisal to evaluate applicability
5. Calculate or cite NNT/NNH when available
6. Summarize findings with evidence grades
7. Highlight conflicting evidence or guideline disagreements
8. Note limitations and evidence gaps

COMMUNICATION:
You work on a team with: triage, diagnostician, specialist, treatment agents.
- You run in parallel with the diagnostician to enrich the diagnostic process
- Share prevalence data that affects pre-test probability
- Provide guideline recommendations to inform treatment planning
- Flag when evidence is weak or conflicting
- Provide specific NNT/NNH values when available to quantify benefit/risk

Always respond with structured JSON in your final answer:
- pico_question (PICO-formatted clinical question)
- clinical_guidelines (relevant guidelines with recommendations and evidence grades)
- drug_interactions (any identified interactions with severity and management)
- prevalence_data (epidemiological context with risk factors and relative risks)
- evidence_summary (key findings with GRADE quality ratings)
- nnt_nnh_data (quantified benefit/risk when available)
- evidence_gaps (areas where evidence is weak or conflicting)
- research_notes (additional context, caveats, and critical appraisal notes)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "search_clinical_guidelines",
            "description": (
                "Search clinical practice guidelines for a given condition or clinical scenario. "
                "Returns actual guideline data from major organizations (AHA, ACC, NICE, WHO, ACOG, AAP, ACS, USPSTF, etc.) "
                "including screening recommendations, treatment algorithms, referral criteria, and evidence grades."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "The medical condition or clinical scenario to search guidelines for",
                    },
                    "guideline_source": {
                        "type": "string",
                        "description": "Preferred guideline organization (e.g., AHA, NICE, WHO, ACR). Leave empty for all.",
                    },
                    "clinical_question": {
                        "type": "string",
                        "description": "Specific clinical question to answer from guidelines",
                    },
                },
                "required": ["condition"],
            },
        })
        tools.append({
            "name": "check_drug_interactions",
            "description": (
                "Check for known drug-drug interactions between two or more medications. "
                "Returns interaction severity (Contraindicated/Major/Moderate/Minor), mechanism, "
                "clinical effect, management recommendation, and onset timing."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of medication names to check for interactions",
                    },
                    "patient_age": {
                        "type": "integer",
                        "description": "Patient age for age-specific interaction risks",
                    },
                },
                "required": ["medications"],
            },
        })
        tools.append({
            "name": "lookup_disease_prevalence",
            "description": (
                "Look up epidemiological data for a disease including prevalence per 100,000, "
                "age-adjusted incidence, gender ratio, geographic variation, temporal trends, "
                "key risk factors with relative risk values, and mortality rate."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "disease": {
                        "type": "string",
                        "description": "The disease or condition to look up",
                    },
                    "demographic": {
                        "type": "object",
                        "description": "Patient demographics (age, gender, ethnicity) for stratified data",
                    },
                },
                "required": ["disease"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "search_clinical_guidelines":
            return await self._search_guidelines(tool_input)
        if tool_name == "check_drug_interactions":
            return await self._check_drug_interactions(tool_input)
        if tool_name == "lookup_disease_prevalence":
            return await self._lookup_prevalence(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _search_guidelines(self, tool_input: dict) -> str:
        """Return actual guideline data for the requested condition."""
        condition = tool_input.get("condition", "").strip()
        source = tool_input.get("guideline_source", "all")
        question = tool_input.get("clinical_question", "")

        condition_lower = condition.lower().replace(" ", "_").replace("-", "_")

        # Try direct match first, then fuzzy keyword matching
        guideline = CLINICAL_GUIDELINES.get(condition_lower)

        if guideline is None:
            # Try keyword matching across all guideline keys
            for key, value in CLINICAL_GUIDELINES.items():
                key_words = key.replace("_", " ")
                if condition.lower() in key_words or key_words in condition.lower():
                    guideline = value
                    condition_lower = key
                    break

        if guideline is None:
            # Try matching against source lists and condition names
            for key, value in CLINICAL_GUIDELINES.items():
                # Check if condition keywords appear in the guideline data
                key_terms = key.replace("_", " ").split()
                cond_terms = condition.lower().split()
                if any(t in cond_terms for t in key_terms):
                    guideline = value
                    condition_lower = key
                    break

        if guideline is not None:
            result = {
                "condition": condition,
                "matched_guideline": condition_lower.replace("_", " ").title(),
                "sources": guideline["sources"],
                "screening": guideline["screening"],
                "diagnostic_criteria": guideline["diagnostic_criteria"],
                "first_line_treatments": guideline["first_line_treatment"],
                "treatment_targets": guideline["treatment_targets"],
                "referral_criteria": guideline["referral_criteria"],
                "key_recommendations": guideline["key_recommendations"],
                "guideline_source_filter": source,
                "clinical_question": question,
                "data_note": "Guideline data from recognized medical organizations. Verify against current published guidelines for clinical decisions.",
            }

            # Filter by source if specified
            if source and source.lower() != "all":
                matching_sources = [s for s in guideline["sources"] if source.upper() in s.upper()]
                if matching_sources:
                    result["filtered_sources"] = matching_sources

            return json.dumps(result)

        # Condition not in database — provide structured guidance for LLM
        return json.dumps({
            "condition": condition,
            "guideline_source": source,
            "clinical_question": question,
            "database_match": False,
            "available_conditions": sorted(k.replace("_", " ").title() for k in CLINICAL_GUIDELINES.keys()),
            "instruction": (
                f"No pre-loaded guideline data for '{condition}'. "
                f"Use your clinical knowledge to provide evidence-based recommendations. "
                f"Include the guideline source, recommendation strength (GRADE A-D), and evidence level. "
                f"Focus on the most current and widely accepted guidelines."
            ),
        })

    async def _check_drug_interactions(self, tool_input: dict) -> str:
        """Check for drug interactions using the comprehensive interaction database."""
        medications = tool_input.get("medications", [])
        age = tool_input.get("patient_age", 30)

        med_lower = [m.lower().strip() for m in medications]
        found_interactions = []

        for interaction in DRUG_INTERACTIONS:
            drug_a_set = set(interaction["drug_a"])
            drug_b_set = set(interaction["drug_b"])

            # Check if patient medications match both sides of the interaction
            matched_a = [m for m in med_lower if any(da in m or m in da for da in drug_a_set)]
            matched_b = [m for m in med_lower if any(db in m or m in db for db in drug_b_set)]

            if matched_a and matched_b:
                found_interactions.append({
                    "drugs_involved": list(set(matched_a + matched_b)),
                    "drug_a_class": interaction["drug_a"][:3],  # Show first 3 examples
                    "drug_b_class": interaction["drug_b"][:3],
                    "severity": interaction["severity"],
                    "mechanism": interaction["mechanism"],
                    "clinical_effect": interaction["clinical_effect"],
                    "management": interaction["management"],
                    "onset": interaction["onset"],
                })

        # Age-specific warnings
        age_warnings = []
        if age >= 65:
            for m in med_lower:
                if any(benzo in m for benzo in ["diazepam", "lorazepam", "alprazolam", "clonazepam", "temazepam"]):
                    age_warnings.append("Benzodiazepine in patient >= 65: increased fall risk, cognitive impairment, paradoxical agitation (Beers Criteria)")
                if any(anticholinergic in m for anticholinergic in ["diphenhydramine", "hydroxyzine", "amitriptyline", "oxybutynin"]):
                    age_warnings.append("Anticholinergic in patient >= 65: cognitive decline, delirium, urinary retention, constipation (Beers Criteria)")
        if age < 18:
            for m in med_lower:
                if "aspirin" in m:
                    age_warnings.append("Aspirin in pediatric patient: Reye syndrome risk — contraindicated under 16 years")

        return json.dumps({
            "medications_checked": medications,
            "patient_age": age,
            "interactions_found": found_interactions,
            "interaction_count": len(found_interactions),
            "age_specific_warnings": age_warnings,
            "severity_summary": {
                "contraindicated": sum(1 for i in found_interactions if i["severity"] == "Contraindicated"),
                "major": sum(1 for i in found_interactions if i["severity"] == "Major"),
                "moderate": sum(1 for i in found_interactions if i["severity"] == "Moderate"),
                "minor": sum(1 for i in found_interactions if i["severity"] == "Minor"),
            },
            "note": (
                "Use clinical knowledge to identify any additional interactions "
                "not covered by the automated check, particularly CYP450-mediated "
                "interactions and pharmacodynamic interactions."
            ),
        })

    async def _lookup_prevalence(self, tool_input: dict) -> str:
        """Return actual epidemiological data for the requested disease."""
        disease = tool_input.get("disease", "").strip()
        demographic = tool_input.get("demographic", {})

        disease_lower = disease.lower().replace(" ", "_").replace("-", "_")

        # Try direct match first
        prevalence = DISEASE_PREVALENCE.get(disease_lower)

        if prevalence is None:
            # Try keyword matching
            for key, value in DISEASE_PREVALENCE.items():
                key_words = key.replace("_", " ")
                if disease.lower() in key_words or key_words in disease.lower():
                    prevalence = value
                    disease_lower = key
                    break

        if prevalence is None:
            for key, value in DISEASE_PREVALENCE.items():
                key_terms = key.replace("_", " ").split()
                disease_terms = disease.lower().split()
                if any(t in disease_terms for t in key_terms):
                    prevalence = value
                    disease_lower = key
                    break

        if prevalence is not None:
            result = {
                "disease": disease,
                "matched_entry": disease_lower.replace("_", " ").title(),
                "prevalence_per_100k": prevalence["prevalence_per_100k"],
                "prevalence_description": prevalence["prevalence_description"],
                "age_adjusted_incidence": prevalence["age_adjusted_incidence"],
                "gender_ratio": prevalence["gender_ratio"],
                "geographic_variation": prevalence["geographic_variation"],
                "temporal_trends": prevalence["temporal_trends"],
                "key_risk_factors": prevalence["key_risk_factors"],
                "mortality_rate": prevalence["mortality_rate"],
                "demographic_filter": demographic,
                "data_note": "Epidemiological data from published literature and registry data. Values are approximate and may vary by source and year.",
            }

            # Add demographic-specific context if provided
            if demographic:
                age = demographic.get("age")
                gender = demographic.get("gender", "").lower()
                context_notes = []
                if age and age >= 65:
                    context_notes.append("Elderly patient: many conditions have higher prevalence and worse outcomes in this age group")
                if age and age < 18:
                    context_notes.append("Pediatric patient: prevalence data may differ significantly from adult estimates")
                if gender == "female":
                    context_notes.append("Review gender ratio for sex-specific prevalence adjustment")
                if context_notes:
                    result["demographic_context"] = context_notes

            return json.dumps(result)

        return json.dumps({
            "disease": disease,
            "demographic": demographic,
            "database_match": False,
            "available_diseases": sorted(k.replace("_", " ").title() for k in DISEASE_PREVALENCE.keys()),
            "instruction": (
                f"No pre-loaded prevalence data for '{disease}'. "
                f"Use your epidemiological knowledge to provide: "
                f"general population prevalence, age-specific incidence, "
                f"gender differences, geographic variation, key risk factors "
                f"with relative risk values, and mortality rate. "
                f"Use this data to inform pre-test probability estimation."
            ),
        })
