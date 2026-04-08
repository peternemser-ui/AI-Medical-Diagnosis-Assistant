/**
 * Common medications database with enriched clinical data.
 * Used to augment the simple medication names stored in user profiles
 * with dosage, category, food interactions, and lifestyle information.
 */

export const MEDICATION_DATABASE = {
  'lisinopril': {
    name: 'Lisinopril',
    category: 'ACE Inhibitor',
    commonDosages: ['5mg', '10mg', '20mg', '40mg'],
    defaultDosage: '10mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['High-potassium foods (bananas, oranges, potatoes) in excess', 'Salt substitutes containing potassium'],
      helpful: ['Low-sodium diet improves effectiveness', 'Balanced potassium from varied sources'],
      mealTiming: 'Can be taken with or without food. Take at the same time each day.',
      alcohol: 'Limit alcohol. It can lower blood pressure further, causing dizziness.',
      supplements: ['Potassium supplements (risk of hyperkalemia)', 'NSAIDs like ibuprofen (reduce effectiveness)'],
      lifestyle: ['Rise slowly from sitting to avoid dizziness', 'Stay hydrated, especially in hot weather', 'Report persistent cough to doctor']
    }
  },
  'metformin': {
    name: 'Metformin',
    category: 'Biguanide (Antidiabetic)',
    commonDosages: ['500mg', '850mg', '1000mg'],
    defaultDosage: '500mg',
    defaultFrequency: 'Twice daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Excessive sugar and refined carbohydrates', 'Heavy meals high in fat (slows absorption)'],
      helpful: ['High-fiber foods help blood sugar control', 'Balanced meals with protein and complex carbs'],
      mealTiming: 'Take with meals to reduce stomach upset. Best taken with the largest meals.',
      alcohol: 'Avoid or strictly limit alcohol. Increases risk of lactic acidosis.',
      supplements: ['Vitamin B12 absorption may be reduced (monitor levels)', 'Chromium supplements (unpredictable glucose effects)'],
      lifestyle: ['Maintain regular exercise routine', 'Monitor blood sugar regularly', 'Stay well hydrated']
    }
  },
  'atorvastatin': {
    name: 'Atorvastatin',
    category: 'Statin (HMG-CoA Reductase Inhibitor)',
    commonDosages: ['10mg', '20mg', '40mg', '80mg'],
    defaultDosage: '20mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 21,
    foodInteractions: {
      avoid: ['Grapefruit and grapefruit juice (increases drug levels)', 'Excessive alcohol (liver strain)'],
      helpful: ['Oat bran and soluble fiber (complement cholesterol reduction)', 'Fish rich in omega-3 fatty acids'],
      mealTiming: 'Take at bedtime for best effectiveness. Can be taken with or without food.',
      alcohol: 'Limit to moderate amounts. Heavy drinking increases liver damage risk.',
      supplements: ['St. John\'s Wort (reduces effectiveness)', 'Red yeast rice (contains natural statins, additive risk)'],
      lifestyle: ['Report any unexplained muscle pain or weakness immediately', 'Regular liver function tests recommended', 'Maintain heart-healthy diet and exercise']
    }
  },
  'albuterol': {
    name: 'Albuterol',
    category: 'Beta-2 Agonist (Bronchodilator)',
    commonDosages: ['90mcg/puff', '2.5mg/3ml nebulizer'],
    defaultDosage: '90mcg',
    defaultFrequency: 'As needed',
    defaultRoute: 'Inhaled',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Caffeine in excess (may increase heart rate)', 'Foods that trigger your asthma/allergies'],
      helpful: ['Anti-inflammatory foods (berries, leafy greens, fatty fish)', 'Adequate hydration thins mucus'],
      mealTiming: 'Use as needed. No specific meal timing requirements.',
      alcohol: 'Moderate alcohol is usually fine. Avoid if it triggers breathing issues.',
      supplements: ['Ephedra / ma huang (additive stimulant effects)', 'High-dose caffeine supplements'],
      lifestyle: ['Rinse mouth after use to prevent irritation', 'Track triggers and avoid them', 'Keep rescue inhaler accessible at all times']
    }
  },
  'omeprazole': {
    name: 'Omeprazole',
    category: 'Proton Pump Inhibitor',
    commonDosages: ['10mg', '20mg', '40mg'],
    defaultDosage: '20mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 7,
    foodInteractions: {
      avoid: ['Spicy and acidic foods (worsen reflux symptoms)', 'Carbonated beverages', 'Chocolate and peppermint (relax lower esophageal sphincter)'],
      helpful: ['Non-citrus fruits and vegetables', 'Lean proteins', 'Whole grains'],
      mealTiming: 'Take 30-60 minutes before breakfast on an empty stomach for best absorption.',
      alcohol: 'Avoid or limit alcohol. It increases stomach acid production.',
      supplements: ['Magnesium levels may be affected with long-term use', 'Calcium absorption may decrease (consider calcium citrate)'],
      lifestyle: ['Do not crush or chew capsules', 'Avoid lying down within 2-3 hours after eating', 'Elevate head of bed if nighttime reflux is an issue']
    }
  },
  'amlodipine': {
    name: 'Amlodipine',
    category: 'Calcium Channel Blocker',
    commonDosages: ['2.5mg', '5mg', '10mg'],
    defaultDosage: '5mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Grapefruit and grapefruit juice (increases drug levels)', 'High-sodium foods'],
      helpful: ['Potassium-rich fruits and vegetables', 'DASH diet supports blood pressure control'],
      mealTiming: 'Can be taken with or without food. Take at the same time each day.',
      alcohol: 'Limit alcohol. May enhance blood pressure lowering and cause dizziness.',
      supplements: ['St. John\'s Wort (may reduce effectiveness)', 'Simvastatin doses above 20mg (increased side effect risk)'],
      lifestyle: ['Monitor blood pressure regularly', 'Report swelling in ankles or feet', 'Avoid sudden position changes']
    }
  },
  'levothyroxine': {
    name: 'Levothyroxine',
    category: 'Thyroid Hormone',
    commonDosages: ['25mcg', '50mcg', '75mcg', '100mcg', '125mcg', '150mcg'],
    defaultDosage: '75mcg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 6,
    foodInteractions: {
      avoid: ['Soy products within 4 hours (interfere with absorption)', 'High-fiber foods at same time (reduce absorption)', 'Walnuts, cottonseed meal, dietary fiber'],
      helpful: ['Consistent diet helps maintain stable levels', 'Selenium-rich foods (Brazil nuts, fish) support thyroid function'],
      mealTiming: 'Take on an empty stomach, 30-60 minutes before breakfast. Or take at bedtime, 3+ hours after last meal.',
      alcohol: 'Moderate alcohol is generally acceptable. Heavy use may affect thyroid function.',
      supplements: ['Calcium supplements (take 4+ hours apart)', 'Iron supplements (take 4+ hours apart)', 'Antacids (take 4+ hours apart)'],
      lifestyle: ['Take at the same time every day for consistent levels', 'Regular thyroid function tests (TSH) are essential', 'Report palpitations, weight changes, or mood changes']
    }
  },
  'losartan': {
    name: 'Losartan',
    category: 'Angiotensin II Receptor Blocker (ARB)',
    commonDosages: ['25mg', '50mg', '100mg'],
    defaultDosage: '50mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['High-potassium foods in excess (bananas, oranges, potatoes)', 'Salt substitutes with potassium'],
      helpful: ['Low-sodium diet enhances effectiveness', 'Heart-healthy Mediterranean diet'],
      mealTiming: 'Can be taken with or without food. Take at the same time each day.',
      alcohol: 'Limit alcohol. May enhance blood pressure lowering effect.',
      supplements: ['Potassium supplements (risk of hyperkalemia)', 'NSAIDs may reduce effectiveness and harm kidneys'],
      lifestyle: ['Monitor blood pressure regularly', 'Stay hydrated', 'Report dizziness or lightheadedness']
    }
  },
  'gabapentin': {
    name: 'Gabapentin',
    category: 'Anticonvulsant / Neuropathic Pain Agent',
    commonDosages: ['100mg', '300mg', '400mg', '600mg', '800mg'],
    defaultDosage: '300mg',
    defaultFrequency: 'Three times daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Antacids containing aluminum or magnesium (take 2 hours apart)', 'High-fat meals may increase absorption unpredictably'],
      helpful: ['Consistent meal timing helps maintain stable levels', 'Balanced diet with adequate hydration'],
      mealTiming: 'Can be taken with or without food. Take doses at evenly spaced intervals.',
      alcohol: 'Avoid alcohol. Both cause CNS depression; combination increases drowsiness and dizziness risk.',
      supplements: ['Morphine and opioids (increased gabapentin levels)', 'CNS depressants (additive sedation)'],
      lifestyle: ['Do not stop abruptly — taper under medical supervision', 'May cause drowsiness; avoid driving until you know how it affects you', 'Report mood changes or suicidal thoughts immediately']
    }
  },
  'sertraline': {
    name: 'Sertraline',
    category: 'SSRI (Antidepressant)',
    commonDosages: ['25mg', '50mg', '100mg', '150mg', '200mg'],
    defaultDosage: '50mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Grapefruit juice (may increase drug levels)', 'Tyramine-rich foods in large quantities (aged cheese, cured meats)'],
      helpful: ['Omega-3 rich foods (salmon, walnuts) may complement mood benefits', 'Regular balanced meals maintain stable blood sugar and mood'],
      mealTiming: 'Can be taken with or without food. Taking with food may reduce nausea.',
      alcohol: 'Avoid alcohol. Both affect the brain; combination worsens side effects and depression.',
      supplements: ['St. John\'s Wort (risk of serotonin syndrome)', 'Tryptophan supplements (risk of serotonin syndrome)', 'MAOIs (dangerous interaction)'],
      lifestyle: ['May take 4-6 weeks for full effect', 'Do not stop abruptly — taper under medical guidance', 'Report worsening depression or suicidal thoughts immediately']
    }
  },
  'metoprolol': {
    name: 'Metoprolol',
    category: 'Beta Blocker',
    commonDosages: ['25mg', '50mg', '100mg', '200mg'],
    defaultDosage: '50mg',
    defaultFrequency: 'Twice daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Grapefruit juice (may increase drug levels with extended-release)', 'High-sodium foods'],
      helpful: ['Heart-healthy diet low in saturated fat', 'Potassium-rich foods in moderation'],
      mealTiming: 'Take with or immediately after meals. Food enhances absorption.',
      alcohol: 'Limit alcohol. Can enhance blood pressure lowering and increase dizziness.',
      supplements: ['Calcium channel blockers (additive heart rate reduction)', 'Clonidine (risk of rebound hypertension if stopped)'],
      lifestyle: ['Do not stop abruptly — must taper gradually', 'Check pulse regularly; report if below 60 bpm', 'May mask symptoms of low blood sugar in diabetics']
    }
  },
  'amoxicillin': {
    name: 'Amoxicillin',
    category: 'Penicillin Antibiotic',
    commonDosages: ['250mg', '500mg', '875mg'],
    defaultDosage: '500mg',
    defaultFrequency: 'Three times daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Acidic foods/drinks may degrade the medication', 'Dairy may slightly reduce absorption (minor effect)'],
      helpful: ['Probiotic-rich foods (yogurt, kefir) help maintain gut flora', 'Adequate water intake aids absorption'],
      mealTiming: 'Can be taken with or without food. Taking with food may reduce stomach upset.',
      alcohol: 'Avoid or limit alcohol while on antibiotics. May worsen side effects.',
      supplements: ['Probiotics (take 2+ hours apart from antibiotic)', 'May reduce effectiveness of oral contraceptives'],
      lifestyle: ['Complete the full course even if feeling better', 'Take doses at evenly spaced intervals', 'Report any rash or allergic reaction immediately']
    }
  },
  'ibuprofen': {
    name: 'Ibuprofen',
    category: 'NSAID (Anti-inflammatory)',
    commonDosages: ['200mg', '400mg', '600mg', '800mg'],
    defaultDosage: '400mg',
    defaultFrequency: 'As needed',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Alcohol (increases stomach bleeding risk)', 'Spicy foods if you have stomach sensitivity'],
      helpful: ['Take with food or milk to reduce stomach irritation', 'Adequate hydration protects kidneys'],
      mealTiming: 'Take with food or a full glass of water to minimize stomach upset.',
      alcohol: 'Avoid alcohol. Significantly increases risk of stomach bleeding.',
      supplements: ['Aspirin (may reduce aspirin\'s heart-protective effects if taken together)', 'Blood thinners (increased bleeding risk)', 'ACE inhibitors/ARBs (reduced effectiveness, kidney risk)'],
      lifestyle: ['Use the lowest effective dose for the shortest time', 'Do not exceed recommended daily maximum', 'Report black stools or stomach pain immediately']
    }
  },
  'acetaminophen': {
    name: 'Acetaminophen',
    category: 'Analgesic / Antipyretic',
    commonDosages: ['325mg', '500mg', '650mg', '1000mg'],
    defaultDosage: '500mg',
    defaultFrequency: 'As needed',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Alcohol (greatly increases liver damage risk)', 'Fasting/starvation (increases liver toxicity risk)'],
      helpful: ['Adequate hydration', 'Regular balanced meals support liver health'],
      mealTiming: 'Can be taken with or without food. Food may slow but not reduce absorption.',
      alcohol: 'Strictly avoid alcohol. Combination dramatically increases liver damage risk.',
      supplements: ['Check all other medications for hidden acetaminophen (cold/flu meds, pain combos)', 'Warfarin (may increase bleeding risk with regular use)'],
      lifestyle: ['Do not exceed 3000-4000mg per day (including all sources)', 'Check all OTC medications for acetaminophen content', 'Seek emergency help if overdose is suspected']
    }
  },
  'aspirin': {
    name: 'Aspirin',
    category: 'NSAID / Antiplatelet',
    commonDosages: ['81mg', '325mg', '500mg'],
    defaultDosage: '81mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Alcohol (increases bleeding and stomach ulcer risk)', 'Ibuprofen timing (take aspirin first, then wait 30 minutes)'],
      helpful: ['Take with food to reduce stomach irritation', 'Adequate hydration'],
      mealTiming: 'Low-dose aspirin can be taken with or without food. Take with food if stomach upset occurs.',
      alcohol: 'Avoid or limit alcohol. Increases risk of stomach bleeding.',
      supplements: ['Fish oil/omega-3 (additive blood-thinning effect)', 'Ginkgo biloba (increased bleeding risk)', 'Other NSAIDs (increased GI bleeding risk)'],
      lifestyle: ['Inform all doctors and dentists you take aspirin', 'Do not stop low-dose aspirin without doctor approval', 'Report unusual bruising or bleeding']
    }
  },
  'prednisone': {
    name: 'Prednisone',
    category: 'Corticosteroid',
    commonDosages: ['5mg', '10mg', '20mg', '40mg', '60mg'],
    defaultDosage: '10mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['High-sodium foods (prednisone causes fluid retention)', 'Sugary foods (raises blood sugar)', 'Grapefruit juice (may increase drug levels)'],
      helpful: ['Calcium and vitamin D rich foods (protects bones)', 'High-protein foods (counteracts muscle wasting)', 'Potassium-rich foods (prednisone depletes potassium)'],
      mealTiming: 'Take with food or milk to prevent stomach irritation. Best taken in the morning.',
      alcohol: 'Avoid or limit alcohol. Both irritate the stomach lining.',
      supplements: ['Calcium and vitamin D (bone protection during long-term use)', 'NSAIDs (increased GI bleeding risk)', 'Live vaccines (avoid during treatment)'],
      lifestyle: ['Do not stop abruptly — must taper gradually', 'Monitor blood sugar if diabetic', 'Report signs of infection (immune suppression)']
    }
  },
  'fluoxetine': {
    name: 'Fluoxetine',
    category: 'SSRI (Antidepressant)',
    commonDosages: ['10mg', '20mg', '40mg', '60mg'],
    defaultDosage: '20mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Grapefruit juice (may increase drug levels)', 'Tyramine-rich foods in excess (aged cheese, cured meats)'],
      helpful: ['Omega-3 fatty acids support mental health', 'Regular balanced meals help stabilize mood and energy'],
      mealTiming: 'Can be taken with or without food. Taking in the morning is common to avoid insomnia.',
      alcohol: 'Avoid alcohol. Both affect the brain; combination worsens side effects.',
      supplements: ['St. John\'s Wort (risk of serotonin syndrome)', 'MAOIs (dangerous interaction — allow 5-week washout)', 'Tryptophan (serotonin syndrome risk)'],
      lifestyle: ['May take 4-6 weeks for full therapeutic effect', 'Do not stop abruptly — taper under medical guidance', 'Report worsening mood or suicidal thoughts immediately']
    }
  },
  'warfarin': {
    name: 'Warfarin',
    category: 'Anticoagulant (Blood Thinner)',
    commonDosages: ['1mg', '2mg', '2.5mg', '5mg', '7.5mg', '10mg'],
    defaultDosage: '5mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 18,
    foodInteractions: {
      avoid: ['Large amounts of vitamin K-rich foods (kale, spinach, broccoli) — keep intake CONSISTENT, not zero', 'Cranberry juice in large quantities (increases warfarin effect)'],
      helpful: ['Maintain a CONSISTENT diet — do not suddenly increase or decrease vitamin K foods', 'Regular balanced meals'],
      mealTiming: 'Take at the same time every day, with or without food. Evening dosing is common.',
      alcohol: 'Avoid or strictly limit alcohol. Alcohol affects how the liver processes warfarin.',
      supplements: ['Vitamin E (increased bleeding risk)', 'Fish oil (increased bleeding risk)', 'St. John\'s Wort (reduces effectiveness)', 'Garlic supplements (increased bleeding)'],
      lifestyle: ['Regular INR blood tests are essential', 'Inform ALL healthcare providers you take warfarin', 'Report any unusual bruising, bleeding, or dark stools immediately', 'Wear a medical alert bracelet']
    }
  },
  'clopidogrel': {
    name: 'Clopidogrel',
    category: 'Antiplatelet Agent',
    commonDosages: ['75mg'],
    defaultDosage: '75mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 8,
    foodInteractions: {
      avoid: ['Grapefruit and grapefruit juice (may affect drug metabolism)', 'Omega-3 supplements in high doses (additive bleeding risk)'],
      helpful: ['Consistent balanced diet', 'Adequate hydration'],
      mealTiming: 'Can be taken with or without food. Take at the same time each day.',
      alcohol: 'Limit alcohol. Increases risk of stomach bleeding.',
      supplements: ['Omeprazole/esomeprazole (may reduce effectiveness — use pantoprazole instead)', 'NSAIDs (increased bleeding risk)', 'Fish oil in high doses (additive bleeding)'],
      lifestyle: ['Do not stop without doctor approval (risk of blood clots)', 'Inform dentists and surgeons', 'Report unusual bruising or prolonged bleeding']
    }
  },
  'pantoprazole': {
    name: 'Pantoprazole',
    category: 'Proton Pump Inhibitor',
    commonDosages: ['20mg', '40mg'],
    defaultDosage: '40mg',
    defaultFrequency: 'Once daily',
    defaultRoute: 'Oral',
    scheduleHour: 7,
    foodInteractions: {
      avoid: ['Spicy and acidic foods (worsen reflux)', 'Carbonated beverages', 'Caffeine in excess'],
      helpful: ['Non-citrus fruits and vegetables', 'Lean proteins and whole grains', 'Smaller, more frequent meals'],
      mealTiming: 'Take 30 minutes before a meal, preferably before breakfast. Swallow whole, do not crush.',
      alcohol: 'Avoid or limit alcohol. Increases stomach acid production.',
      supplements: ['Magnesium levels may drop with long-term use', 'Iron and B12 absorption may be reduced', 'Calcium absorption may decrease — consider calcium citrate form'],
      lifestyle: ['Do not use long-term without doctor guidance', 'Avoid lying down within 2-3 hours after eating', 'Elevate head of bed for nighttime symptoms']
    }
  }
}

/**
 * Enrich a simple medication name string with full clinical data.
 * Falls back gracefully for unknown medications.
 *
 * @param {string} name - Medication name from user profile
 * @returns {object} Enriched medication object
 */
export function enrichMedication(name) {
  const key = name.toLowerCase().trim()
  const data = MEDICATION_DATABASE[key]
  if (data) {
    return {
      ...data,
      dosage: data.defaultDosage,
      frequency: data.defaultFrequency,
      route: data.defaultRoute,
      fromProfile: true
    }
  }
  // Unknown medication — return basic info
  return {
    name: name,
    category: 'Other',
    commonDosages: [],
    defaultDosage: '',
    defaultFrequency: 'As directed',
    defaultRoute: 'Oral',
    dosage: '',
    frequency: 'As directed',
    route: 'Oral',
    scheduleHour: 8,
    foodInteractions: null,
    fromProfile: true,
    unknown: true
  }
}

/**
 * Get all known medication names (for autocomplete / suggestions)
 */
export function getAllMedicationNames() {
  return Object.values(MEDICATION_DATABASE).map(m => m.name)
}

/**
 * Known drug-drug interactions.
 * Each key is a lowercase medication name; values are arrays of
 * { drug, severity, description } objects.
 */
export const DRUG_INTERACTIONS = {
  'warfarin': [
    { drug: 'ibuprofen', severity: 'high', description: 'Increased bleeding risk. NSAIDs inhibit platelet function and may cause GI bleeding.' },
    { drug: 'aspirin', severity: 'high', description: 'Significantly increased bleeding risk. Dual antiplatelet/anticoagulant effect.' },
    { drug: 'clopidogrel', severity: 'high', description: 'Increased bleeding risk with dual antithrombotic therapy.' },
    { drug: 'sertraline', severity: 'moderate', description: 'SSRIs may increase bleeding risk when combined with warfarin.' },
    { drug: 'fluoxetine', severity: 'moderate', description: 'SSRIs may increase bleeding risk and affect warfarin metabolism.' },
    { drug: 'omeprazole', severity: 'moderate', description: 'May alter warfarin metabolism. Monitor INR closely.' },
  ],
  'lisinopril': [
    { drug: 'ibuprofen', severity: 'moderate', description: 'NSAIDs reduce the effectiveness of ACE inhibitors and increase kidney risk.' },
    { drug: 'losartan', severity: 'high', description: 'Dual RAAS blockade increases risk of hypotension, hyperkalemia, and renal failure.' },
  ],
  'losartan': [
    { drug: 'ibuprofen', severity: 'moderate', description: 'NSAIDs reduce the effectiveness of ARBs and increase kidney risk.' },
    { drug: 'lisinopril', severity: 'high', description: 'Dual RAAS blockade increases risk of hypotension, hyperkalemia, and renal failure.' },
  ],
  'metformin': [
    { drug: 'prednisone', severity: 'moderate', description: 'Corticosteroids raise blood sugar and may counteract metformin.' },
  ],
  'sertraline': [
    { drug: 'fluoxetine', severity: 'high', description: 'Do not combine two SSRIs. Risk of serotonin syndrome.' },
    { drug: 'warfarin', severity: 'moderate', description: 'SSRIs may increase bleeding risk when combined with warfarin.' },
    { drug: 'ibuprofen', severity: 'moderate', description: 'SSRIs combined with NSAIDs increase GI bleeding risk.' },
  ],
  'fluoxetine': [
    { drug: 'sertraline', severity: 'high', description: 'Do not combine two SSRIs. Risk of serotonin syndrome.' },
    { drug: 'warfarin', severity: 'moderate', description: 'SSRIs may increase bleeding risk and affect warfarin metabolism.' },
    { drug: 'ibuprofen', severity: 'moderate', description: 'SSRIs combined with NSAIDs increase GI bleeding risk.' },
  ],
  'ibuprofen': [
    { drug: 'aspirin', severity: 'moderate', description: 'Ibuprofen may reduce the cardioprotective effect of low-dose aspirin.' },
    { drug: 'warfarin', severity: 'high', description: 'Increased bleeding risk. NSAIDs inhibit platelet function.' },
    { drug: 'lisinopril', severity: 'moderate', description: 'NSAIDs reduce ACE inhibitor effectiveness and increase kidney risk.' },
    { drug: 'losartan', severity: 'moderate', description: 'NSAIDs reduce ARB effectiveness and increase kidney risk.' },
    { drug: 'clopidogrel', severity: 'high', description: 'Increased GI bleeding risk with combined antiplatelet and NSAID therapy.' },
  ],
  'aspirin': [
    { drug: 'warfarin', severity: 'high', description: 'Significantly increased bleeding risk.' },
    { drug: 'ibuprofen', severity: 'moderate', description: 'Ibuprofen may reduce the cardioprotective effect of low-dose aspirin.' },
    { drug: 'clopidogrel', severity: 'moderate', description: 'Increased bleeding risk with dual antiplatelet therapy.' },
  ],
  'clopidogrel': [
    { drug: 'omeprazole', severity: 'moderate', description: 'Omeprazole reduces clopidogrel effectiveness. Use pantoprazole instead.' },
    { drug: 'warfarin', severity: 'high', description: 'Increased bleeding risk with dual antithrombotic therapy.' },
    { drug: 'ibuprofen', severity: 'high', description: 'Increased GI bleeding risk.' },
    { drug: 'aspirin', severity: 'moderate', description: 'Increased bleeding risk with dual antiplatelet therapy.' },
  ],
  'omeprazole': [
    { drug: 'clopidogrel', severity: 'moderate', description: 'Omeprazole reduces clopidogrel effectiveness. Use pantoprazole instead.' },
  ],
  'metoprolol': [
    { drug: 'amlodipine', severity: 'moderate', description: 'Combined use may cause excessive blood pressure lowering or bradycardia.' },
  ],
  'amlodipine': [
    { drug: 'metoprolol', severity: 'moderate', description: 'Combined use may cause excessive blood pressure lowering or bradycardia.' },
  ],
  'prednisone': [
    { drug: 'ibuprofen', severity: 'moderate', description: 'Increased risk of GI ulceration and bleeding.' },
    { drug: 'metformin', severity: 'moderate', description: 'Corticosteroids raise blood sugar and counteract metformin.' },
    { drug: 'warfarin', severity: 'moderate', description: 'Corticosteroids may alter warfarin response. Monitor INR.' },
  ],
}

/**
 * Check a medication against a list of existing medications for interactions.
 * @param {string} newMedName - Name of the new medication being added
 * @param {Array} existingMeds - Array of medication objects with a `name` property
 * @returns {Array} Array of { existingMed, severity, description } interaction warnings
 */
export function checkDrugInteractions(newMedName, existingMeds) {
  const key = newMedName.toLowerCase().trim()
  const interactions = DRUG_INTERACTIONS[key]
  if (!interactions) return []

  const warnings = []
  for (const med of existingMeds) {
    const existingKey = med.name.toLowerCase().trim()
    const match = interactions.find(i => i.drug === existingKey)
    if (match) {
      warnings.push({
        existingMed: med.name,
        severity: match.severity,
        description: match.description,
      })
    }
  }
  return warnings
}
