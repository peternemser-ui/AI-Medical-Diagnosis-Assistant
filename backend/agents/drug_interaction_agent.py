"""Drug Interaction Agent — checks medication interactions, allergies, contraindications, and dosage safety."""

from datetime import datetime, timezone


# Built-in interaction database: (drug_a, drug_b) -> interaction info
INTERACTION_DB = {
    ("warfarin", "ibuprofen"): {"severity": "major", "description": "Increased risk of gastrointestinal bleeding and prolonged INR", "recommendation": "Avoid combination. Use acetaminophen for pain if anticoagulated."},
    ("warfarin", "aspirin"): {"severity": "major", "description": "Significantly increased bleeding risk due to combined anticoagulant and antiplatelet effects", "recommendation": "Avoid unless specifically prescribed by cardiologist. Monitor INR closely."},
    ("warfarin", "naproxen"): {"severity": "major", "description": "NSAIDs increase bleeding risk and may displace warfarin from protein binding", "recommendation": "Avoid combination. Consider acetaminophen as alternative analgesic."},
    ("lisinopril", "potassium"): {"severity": "major", "description": "ACE inhibitors reduce potassium excretion; supplemental potassium may cause hyperkalemia", "recommendation": "Avoid potassium supplements unless serum K+ is monitored. Check levels within 1 week."},
    ("enalapril", "potassium"): {"severity": "major", "description": "ACE inhibitors reduce potassium excretion; risk of life-threatening hyperkalemia", "recommendation": "Monitor serum potassium closely. Avoid potassium-sparing diuretics."},
    ("fluoxetine", "phenelzine"): {"severity": "major", "description": "SSRI + MAOI combination can cause serotonin syndrome — potentially fatal", "recommendation": "Contraindicated. Allow 5-week washout when switching from fluoxetine to MAOI."},
    ("sertraline", "phenelzine"): {"severity": "major", "description": "Risk of serotonin syndrome: hyperthermia, rigidity, myoclonus, autonomic instability", "recommendation": "Contraindicated. Allow 2-week washout between SSRI and MAOI."},
    ("fluoxetine", "tramadol"): {"severity": "major", "description": "Increased risk of serotonin syndrome and seizures", "recommendation": "Avoid combination. If necessary, use lowest doses and monitor for serotonin toxicity signs."},
    ("methotrexate", "ibuprofen"): {"severity": "major", "description": "NSAIDs reduce renal clearance of methotrexate, increasing toxicity risk", "recommendation": "Avoid NSAIDs during methotrexate therapy. Use acetaminophen for pain."},
    ("digoxin", "amiodarone"): {"severity": "major", "description": "Amiodarone increases digoxin levels by 70-100%, risk of toxicity", "recommendation": "Reduce digoxin dose by 50% when starting amiodarone. Monitor digoxin levels."},
    ("clopidogrel", "omeprazole"): {"severity": "major", "description": "Omeprazole inhibits CYP2C19, reducing clopidogrel activation and antiplatelet effect", "recommendation": "Use pantoprazole instead of omeprazole. Avoid esomeprazole as well."},
    ("simvastatin", "grapefruit"): {"severity": "moderate", "description": "Grapefruit inhibits CYP3A4, increasing statin blood levels and risk of rhabdomyolysis", "recommendation": "Avoid grapefruit juice. Consider switching to rosuvastatin (not CYP3A4 dependent)."},
    ("atorvastatin", "grapefruit"): {"severity": "moderate", "description": "Grapefruit increases statin exposure via CYP3A4 inhibition", "recommendation": "Limit grapefruit intake to small amounts. Monitor for muscle pain."},
    ("metformin", "alcohol"): {"severity": "moderate", "description": "Alcohol increases risk of lactic acidosis with metformin and impairs gluconeogenesis", "recommendation": "Limit alcohol to moderate intake. Avoid binge drinking. Monitor blood glucose."},
    ("lisinopril", "spironolactone"): {"severity": "moderate", "description": "Both agents increase potassium retention; combined use increases hyperkalemia risk", "recommendation": "Monitor serum potassium within 1 week of initiation and periodically thereafter."},
    ("ciprofloxacin", "antacids"): {"severity": "moderate", "description": "Antacids containing aluminum/magnesium chelate ciprofloxacin, reducing absorption by 90%", "recommendation": "Take ciprofloxacin 2 hours before or 6 hours after antacids."},
    ("levothyroxine", "calcium"): {"severity": "moderate", "description": "Calcium supplements reduce levothyroxine absorption", "recommendation": "Separate administration by at least 4 hours."},
    ("levothyroxine", "iron"): {"severity": "moderate", "description": "Iron supplements reduce levothyroxine absorption by forming insoluble complexes", "recommendation": "Separate administration by at least 4 hours. Take levothyroxine on empty stomach."},
    ("metronidazole", "alcohol"): {"severity": "moderate", "description": "Disulfiram-like reaction: nausea, vomiting, flushing, headache, tachycardia", "recommendation": "Avoid alcohol during treatment and for 48 hours after completing metronidazole."},
    ("sildenafil", "nitrates"): {"severity": "major", "description": "Severe hypotension risk — can be fatal. Both agents cause vasodilation", "recommendation": "Absolutely contraindicated. Do not use within 24 hours of nitrate administration."},
    ("lithium", "ibuprofen"): {"severity": "major", "description": "NSAIDs reduce renal lithium clearance, increasing levels and toxicity risk", "recommendation": "Avoid NSAIDs. If required, monitor lithium levels closely and reduce dose."},
    ("ssri", "nsaid"): {"severity": "moderate", "description": "SSRIs impair platelet function; combined with NSAIDs increases GI bleeding risk 3-fold", "recommendation": "Consider gastroprotective agent (PPI) if combination is necessary."},
    ("amoxicillin", "methotrexate"): {"severity": "moderate", "description": "Penicillins may reduce renal clearance of methotrexate", "recommendation": "Monitor methotrexate levels and renal function if used concurrently."},
    ("prednisone", "nsaid"): {"severity": "moderate", "description": "Increased risk of GI ulceration and bleeding with corticosteroid + NSAID combination", "recommendation": "Use gastroprotective agent. Monitor for GI symptoms."},
}

# NSAID list for group matching
NSAIDS = {"ibuprofen", "naproxen", "aspirin", "diclofenac", "celecoxib", "meloxicam", "indomethacin", "ketorolac"}
SSRIS = {"fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"}
MAOIS = {"phenelzine", "tranylcypromine", "isocarboxazid", "selegiline"}
ACE_INHIBITORS = {"lisinopril", "enalapril", "ramipril", "benazepril", "captopril", "fosinopril", "quinapril"}
STATINS = {"simvastatin", "atorvastatin", "rosuvastatin", "pravastatin", "lovastatin", "fluvastatin"}

# Allergy cross-reactivity database
ALLERGY_CROSS_REACTIVITY = {
    "penicillin": {"amoxicillin", "ampicillin", "piperacillin", "nafcillin", "dicloxacillin"},
    "sulfa": {"sulfamethoxazole", "sulfasalazine", "sulfadiazine"},
    "nsaid": NSAIDS,
    "cephalosporin": {"cephalexin", "cefazolin", "ceftriaxone", "cefdinir", "cefuroxime"},
    "aspirin": {"aspirin"} | {"ibuprofen", "naproxen"},  # cross-reactive in aspirin-sensitive patients
}

# Contraindication database: medication -> set of conditions
CONTRAINDICATION_DB = {
    "metformin": {"severe renal impairment", "metabolic acidosis", "diabetic ketoacidosis", "severe liver disease"},
    "ibuprofen": {"active gi bleeding", "severe renal impairment", "third trimester pregnancy", "aspirin-sensitive asthma"},
    "lisinopril": {"angioedema", "bilateral renal artery stenosis", "pregnancy", "hyperkalemia"},
    "warfarin": {"active bleeding", "severe liver disease", "recent surgery", "uncontrolled hypertension"},
    "methotrexate": {"pregnancy", "severe liver disease", "severe renal impairment", "immunodeficiency", "bone marrow hypoplasia"},
    "simvastatin": {"active liver disease", "pregnancy", "breastfeeding"},
    "lithium": {"severe renal impairment", "severe cardiovascular disease", "addison disease", "dehydration"},
    "ciprofloxacin": {"myasthenia gravis", "tendon disorders", "qt prolongation"},
    "sildenafil": {"concurrent nitrate use", "severe hepatic impairment", "hypotension", "recent stroke"},
    "prednisone": {"systemic fungal infection", "live vaccine administration"},
}

# Dosage reference: medication -> {unit, adult_min, adult_max, pediatric_factor, max_daily, renal_adjust}
DOSAGE_DB = {
    "ibuprofen": {"unit": "mg", "adult_min": 200, "adult_max": 800, "max_daily": 3200, "frequency": "every 6-8 hours", "pediatric_mg_per_kg": 10, "renal_adjust": True},
    "amoxicillin": {"unit": "mg", "adult_min": 250, "adult_max": 500, "max_daily": 3000, "frequency": "every 8 hours", "pediatric_mg_per_kg": 25, "renal_adjust": True},
    "metformin": {"unit": "mg", "adult_min": 500, "adult_max": 1000, "max_daily": 2550, "frequency": "twice daily", "pediatric_mg_per_kg": None, "renal_adjust": True},
    "lisinopril": {"unit": "mg", "adult_min": 5, "adult_max": 40, "max_daily": 80, "frequency": "once daily", "pediatric_mg_per_kg": 0.07, "renal_adjust": True},
    "atorvastatin": {"unit": "mg", "adult_min": 10, "adult_max": 80, "max_daily": 80, "frequency": "once daily", "pediatric_mg_per_kg": None, "renal_adjust": False},
    "sertraline": {"unit": "mg", "adult_min": 25, "adult_max": 200, "max_daily": 200, "frequency": "once daily", "pediatric_mg_per_kg": None, "renal_adjust": False},
    "omeprazole": {"unit": "mg", "adult_min": 20, "adult_max": 40, "max_daily": 40, "frequency": "once daily", "pediatric_mg_per_kg": 1, "renal_adjust": False},
    "prednisone": {"unit": "mg", "adult_min": 5, "adult_max": 60, "max_daily": 80, "frequency": "once daily or divided", "pediatric_mg_per_kg": 1, "renal_adjust": False},
    "warfarin": {"unit": "mg", "adult_min": 2, "adult_max": 10, "max_daily": 10, "frequency": "once daily", "pediatric_mg_per_kg": 0.2, "renal_adjust": False},
    "methotrexate": {"unit": "mg", "adult_min": 7.5, "adult_max": 25, "max_daily": 25, "frequency": "once weekly", "pediatric_mg_per_kg": 0.3, "renal_adjust": True},
}


class DrugInteractionAgent:
    """Checks medication interactions, allergies, contraindications, and dosage safety."""

    def _normalize(self, name: str) -> str:
        return name.strip().lower().replace("-", " ")

    def _expand_groups(self, drug: str) -> set[str]:
        """Expand a drug name to include its class group keys for lookup."""
        names = {drug}
        if drug in NSAIDS:
            names.add("nsaid")
        if drug in SSRIS:
            names.add("ssri")
        if drug in MAOIS:
            names.add("maoi")
        if drug in ACE_INHIBITORS:
            names.add("lisinopril")
            names.add("enalapril")
        if drug in STATINS:
            names.add("simvastatin")
            names.add("atorvastatin")
        return names

    def check_interactions(self, medications: list[str]) -> dict:
        """Check a list of medications for pairwise interactions."""
        meds = [self._normalize(m) for m in medications]
        interactions = []
        checked_pairs = set()

        for i, med_a in enumerate(meds):
            for j, med_b in enumerate(meds):
                if i >= j:
                    continue
                pair_key = tuple(sorted([med_a, med_b]))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                # Try direct lookup and expanded group lookup
                found = None
                names_a = self._expand_groups(med_a)
                names_b = self._expand_groups(med_b)

                for na in names_a:
                    for nb in names_b:
                        key1 = (na, nb)
                        key2 = (nb, na)
                        if key1 in INTERACTION_DB:
                            found = INTERACTION_DB[key1]
                            break
                        if key2 in INTERACTION_DB:
                            found = INTERACTION_DB[key2]
                            break
                    if found:
                        break

                if found:
                    interactions.append({
                        "drug_a": med_a,
                        "drug_b": med_b,
                        **found,
                    })

        major = [i for i in interactions if i["severity"] == "major"]
        moderate = [i for i in interactions if i["severity"] == "moderate"]
        minor = [i for i in interactions if i["severity"] == "minor"]

        return {
            "medications_checked": meds,
            "total_interactions": len(interactions),
            "summary": {
                "major": len(major),
                "moderate": len(moderate),
                "minor": len(minor),
            },
            "interactions": interactions,
            "safe": len(major) == 0,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    def check_allergies(self, medications: list[str], known_allergies: list[str]) -> dict:
        """Cross-reference medications against patient's known allergies."""
        meds = [self._normalize(m) for m in medications]
        allergies = [self._normalize(a) for a in known_allergies]
        alerts = []

        for med in meds:
            for allergy in allergies:
                # Direct match
                if med == allergy:
                    alerts.append({
                        "medication": med,
                        "allergy": allergy,
                        "type": "direct",
                        "risk": "high",
                        "message": f"Patient is allergic to {allergy}. {med} is contraindicated.",
                    })
                    continue

                # Cross-reactivity check
                for allergy_class, members in ALLERGY_CROSS_REACTIVITY.items():
                    if allergy in members or allergy == allergy_class:
                        if med in members:
                            alerts.append({
                                "medication": med,
                                "allergy": allergy,
                                "type": "cross_reactivity",
                                "risk": "moderate",
                                "class": allergy_class,
                                "message": f"{med} may cross-react with {allergy} allergy ({allergy_class} class).",
                            })

        return {
            "medications_checked": meds,
            "known_allergies": allergies,
            "total_alerts": len(alerts),
            "alerts": alerts,
            "safe": len(alerts) == 0,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_contraindications(self, medication: str, conditions: list[str]) -> dict:
        """Check a medication against a list of patient conditions."""
        med = self._normalize(medication)
        conds = [self._normalize(c) for c in conditions]
        contraindications = []

        med_contras = CONTRAINDICATION_DB.get(med, set())
        for cond in conds:
            for contra in med_contras:
                if cond in contra or contra in cond:
                    contraindications.append({
                        "medication": med,
                        "condition": cond,
                        "contraindication": contra,
                        "severity": "absolute",
                        "message": f"{med.title()} is contraindicated in patients with {contra}.",
                    })

        return {
            "medication": med,
            "conditions_checked": conds,
            "total_contraindications": len(contraindications),
            "contraindications": contraindications,
            "safe": len(contraindications) == 0,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_medication_guide(self, medication: str) -> dict:
        """Generate a patient-friendly medication guide."""
        med = self._normalize(medication)

        guides = {
            "ibuprofen": {
                "generic_name": "Ibuprofen",
                "brand_names": ["Advil", "Motrin"],
                "drug_class": "NSAID (Non-Steroidal Anti-Inflammatory Drug)",
                "purpose": "Reduces pain, fever, and inflammation",
                "how_it_works": "Blocks enzymes (COX-1 and COX-2) that produce prostaglandins, chemicals that cause pain and swelling.",
                "common_dosage": "200-400 mg every 4-6 hours as needed (max 1200 mg/day OTC)",
                "side_effects": {
                    "common": ["Stomach upset", "Nausea", "Dizziness", "Headache"],
                    "serious": ["GI bleeding", "Kidney problems", "Heart attack or stroke (long-term use)", "Severe allergic reaction"],
                },
                "warnings": ["Do not take on empty stomach", "Avoid if you have kidney disease", "Do not combine with other NSAIDs", "Avoid in third trimester of pregnancy"],
                "food_interactions": ["Take with food or milk to reduce stomach upset", "Avoid alcohol (increases bleeding risk)"],
            },
            "metformin": {
                "generic_name": "Metformin",
                "brand_names": ["Glucophage", "Fortamet"],
                "drug_class": "Biguanide (Antidiabetic)",
                "purpose": "Lowers blood sugar levels in type 2 diabetes",
                "how_it_works": "Decreases glucose production by the liver and improves insulin sensitivity in muscle tissue.",
                "common_dosage": "500 mg twice daily, titrated up to 2000 mg/day",
                "side_effects": {
                    "common": ["Nausea", "Diarrhea", "Stomach cramps", "Metallic taste"],
                    "serious": ["Lactic acidosis (rare but serious)", "Vitamin B12 deficiency (long-term)"],
                },
                "warnings": ["Take with meals", "Stay hydrated", "Stop before contrast dye procedures", "Avoid excessive alcohol"],
                "food_interactions": ["Take with food to reduce GI side effects", "Limit alcohol consumption"],
            },
            "lisinopril": {
                "generic_name": "Lisinopril",
                "brand_names": ["Prinivil", "Zestril"],
                "drug_class": "ACE Inhibitor (Antihypertensive)",
                "purpose": "Lowers blood pressure and protects the heart and kidneys",
                "how_it_works": "Blocks the enzyme that produces angiotensin II, a hormone that narrows blood vessels.",
                "common_dosage": "10-40 mg once daily",
                "side_effects": {
                    "common": ["Dry cough", "Dizziness", "Headache", "Fatigue"],
                    "serious": ["Angioedema (swelling of face/throat)", "Hyperkalemia", "Kidney impairment", "Low blood pressure"],
                },
                "warnings": ["Do not use during pregnancy", "Avoid potassium supplements unless directed", "Report any swelling of face or throat immediately"],
                "food_interactions": ["Avoid potassium-rich salt substitutes", "Limit high-potassium foods if directed"],
            },
            "atorvastatin": {
                "generic_name": "Atorvastatin",
                "brand_names": ["Lipitor"],
                "drug_class": "HMG-CoA Reductase Inhibitor (Statin)",
                "purpose": "Lowers cholesterol and reduces risk of heart disease",
                "how_it_works": "Blocks an enzyme in the liver that produces cholesterol, lowering LDL and total cholesterol.",
                "common_dosage": "10-80 mg once daily, usually at bedtime",
                "side_effects": {
                    "common": ["Muscle aches", "Joint pain", "Diarrhea", "Nausea"],
                    "serious": ["Rhabdomyolysis (muscle breakdown)", "Liver damage", "Memory problems"],
                },
                "warnings": ["Report unexplained muscle pain immediately", "Regular liver function tests needed", "Do not use during pregnancy"],
                "food_interactions": ["Avoid large quantities of grapefruit juice", "Can be taken with or without food"],
            },
            "sertraline": {
                "generic_name": "Sertraline",
                "brand_names": ["Zoloft"],
                "drug_class": "SSRI (Selective Serotonin Reuptake Inhibitor)",
                "purpose": "Treats depression, anxiety, PTSD, OCD, and panic disorder",
                "how_it_works": "Increases serotonin levels in the brain by blocking its reabsorption, improving mood and reducing anxiety.",
                "common_dosage": "50-200 mg once daily",
                "side_effects": {
                    "common": ["Nausea", "Insomnia", "Diarrhea", "Dry mouth", "Dizziness"],
                    "serious": ["Serotonin syndrome", "Suicidal thoughts (especially in young adults)", "Bleeding risk", "Hyponatremia"],
                },
                "warnings": ["Do not combine with MAOIs", "May take 4-6 weeks for full effect", "Do not stop abruptly — taper gradually"],
                "food_interactions": ["Avoid alcohol", "Can be taken with or without food"],
            },
            "amoxicillin": {
                "generic_name": "Amoxicillin",
                "brand_names": ["Amoxil", "Trimox"],
                "drug_class": "Penicillin Antibiotic",
                "purpose": "Treats bacterial infections (ear, throat, urinary, skin, respiratory)",
                "how_it_works": "Kills bacteria by preventing them from building their cell walls.",
                "common_dosage": "250-500 mg every 8 hours for 7-14 days",
                "side_effects": {
                    "common": ["Diarrhea", "Nausea", "Rash", "Vomiting"],
                    "serious": ["Severe allergic reaction (anaphylaxis)", "C. difficile diarrhea", "Stevens-Johnson syndrome"],
                },
                "warnings": ["Complete the full course even if you feel better", "Tell your doctor if you are allergic to penicillin", "May reduce effectiveness of oral contraceptives"],
                "food_interactions": ["Can be taken with or without food", "Take with food if stomach upset occurs"],
            },
            "omeprazole": {
                "generic_name": "Omeprazole",
                "brand_names": ["Prilosec", "Losec"],
                "drug_class": "Proton Pump Inhibitor (PPI)",
                "purpose": "Reduces stomach acid production; treats GERD, ulcers, and acid reflux",
                "how_it_works": "Blocks the proton pump in stomach lining cells, significantly reducing acid secretion.",
                "common_dosage": "20-40 mg once daily, taken 30 minutes before breakfast",
                "side_effects": {
                    "common": ["Headache", "Nausea", "Diarrhea", "Stomach pain", "Flatulence"],
                    "serious": ["C. difficile infection", "Bone fractures (long-term)", "Magnesium deficiency", "Vitamin B12 deficiency"],
                },
                "warnings": ["Not intended for immediate heartburn relief", "Long-term use may increase fracture risk", "Take before meals"],
                "food_interactions": ["Take 30-60 minutes before eating", "Swallow capsules whole — do not crush or chew"],
            },
            "warfarin": {
                "generic_name": "Warfarin",
                "brand_names": ["Coumadin", "Jantoven"],
                "drug_class": "Anticoagulant (Blood Thinner)",
                "purpose": "Prevents blood clots in conditions like atrial fibrillation, DVT, and pulmonary embolism",
                "how_it_works": "Inhibits vitamin K-dependent clotting factors, slowing the blood clotting process.",
                "common_dosage": "Individualized — typically 2-10 mg once daily based on INR",
                "side_effects": {
                    "common": ["Easy bruising", "Minor bleeding from cuts"],
                    "serious": ["Major hemorrhage", "GI bleeding", "Intracranial bleeding", "Skin necrosis"],
                },
                "warnings": ["Requires regular INR monitoring", "Many drug and food interactions", "Avoid contact sports", "Carry a medical alert card"],
                "food_interactions": ["Maintain consistent vitamin K intake", "Avoid large changes in leafy green consumption", "Avoid alcohol or limit to small amounts", "Cranberry juice may increase effect"],
            },
        }

        guide = guides.get(med)
        if guide:
            return {**guide, "found": True, "generated_at": datetime.now(timezone.utc).isoformat()}

        # Generic fallback
        return {
            "found": False,
            "generic_name": medication.title(),
            "brand_names": [],
            "drug_class": "Unknown",
            "purpose": "Information not available in local database. Please consult a pharmacist.",
            "how_it_works": "Mechanism information not available.",
            "common_dosage": "Consult your prescribing physician.",
            "side_effects": {"common": [], "serious": []},
            "warnings": ["Always take as prescribed", "Do not stop without consulting your doctor"],
            "food_interactions": [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_interaction_database_stats(self) -> dict:
        """Return database size, coverage, and metadata."""
        severities = {"major": 0, "moderate": 0, "minor": 0}
        for info in INTERACTION_DB.values():
            severities[info["severity"]] = severities.get(info["severity"], 0) + 1

        return {
            "total_interactions": len(INTERACTION_DB),
            "severity_breakdown": severities,
            "drug_classes_covered": [
                "NSAIDs", "SSRIs", "MAOIs", "ACE Inhibitors", "Statins",
                "Anticoagulants", "Antibiotics", "Antidiabetics", "PDE5 Inhibitors",
                "Proton Pump Inhibitors", "Corticosteroids", "Antiarrhythmics",
            ],
            "allergy_classes_tracked": list(ALLERGY_CROSS_REACTIVITY.keys()),
            "contraindication_medications": list(CONTRAINDICATION_DB.keys()),
            "dosage_reference_medications": list(DOSAGE_DB.keys()),
            "last_updated": "2026-03-15",
            "version": "1.0.0",
            "disclaimer": "This database is for educational purposes only. Always consult a licensed pharmacist or physician.",
        }

    def check_dosage_safety(self, medication: str, dose: float, patient_age: int, patient_weight: float | None = None) -> dict:
        """Validate dosage for a given patient profile."""
        med = self._normalize(medication)
        ref = DOSAGE_DB.get(med)

        if not ref:
            return {
                "medication": med,
                "found": False,
                "message": f"Dosage reference not available for {medication}. Consult prescribing information.",
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }

        warnings = []
        is_pediatric = patient_age < 18
        is_elderly = patient_age >= 65
        status = "safe"

        # Determine expected range
        if is_pediatric and ref["pediatric_mg_per_kg"] and patient_weight:
            expected_dose = ref["pediatric_mg_per_kg"] * patient_weight
            dose_label = f"{ref['pediatric_mg_per_kg']} mg/kg"
            if dose > expected_dose * 1.5:
                status = "excessive"
                warnings.append(f"Dose {dose} {ref['unit']} exceeds pediatric recommendation of ~{expected_dose:.0f} {ref['unit']} for {patient_weight}kg patient.")
            elif dose > expected_dose * 1.2:
                status = "high"
                warnings.append(f"Dose is on the high end for a pediatric patient weighing {patient_weight}kg.")
        elif is_pediatric and not ref["pediatric_mg_per_kg"]:
            warnings.append(f"{med.title()} may not be recommended for pediatric use (age {patient_age}).")
            status = "caution"
        else:
            if dose > ref["adult_max"]:
                status = "excessive"
                warnings.append(f"Dose {dose} {ref['unit']} exceeds maximum adult dose of {ref['adult_max']} {ref['unit']}.")
            elif dose > ref["adult_max"] * 0.8 and is_elderly:
                status = "high"
                warnings.append(f"Consider lower dose for elderly patient (age {patient_age}). Current dose is near maximum.")

        if dose > ref["max_daily"]:
            status = "excessive"
            warnings.append(f"Dose {dose} {ref['unit']} exceeds maximum daily limit of {ref['max_daily']} {ref['unit']}.")

        if is_elderly and ref.get("renal_adjust"):
            warnings.append("Renal dose adjustment may be needed for elderly patients. Check renal function.")

        if dose < ref["adult_min"] and not is_pediatric:
            warnings.append(f"Dose {dose} {ref['unit']} is below typical starting dose of {ref['adult_min']} {ref['unit']}. May be sub-therapeutic.")

        return {
            "medication": med,
            "found": True,
            "dose": dose,
            "unit": ref["unit"],
            "patient_age": patient_age,
            "patient_weight": patient_weight,
            "status": status,  # safe, caution, high, excessive
            "reference": {
                "adult_range": f"{ref['adult_min']}-{ref['adult_max']} {ref['unit']}",
                "max_daily": f"{ref['max_daily']} {ref['unit']}",
                "frequency": ref["frequency"],
            },
            "warnings": warnings,
            "safe": status in ("safe", "caution"),
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }


# Singleton
_drug_agent = None


def get_drug_interaction_agent() -> DrugInteractionAgent:
    global _drug_agent
    if _drug_agent is None:
        _drug_agent = DrugInteractionAgent()
    return _drug_agent
