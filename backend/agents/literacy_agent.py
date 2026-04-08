"""Health Literacy Agent — simplifies medical text, explains terms, and generates patient education materials."""

import re
import math
from datetime import datetime, timezone


# Medical terminology dictionary: term -> {definition, analogy, category}
MEDICAL_TERMS = {
    "hypertension": {"definition": "High blood pressure — when the force of blood against artery walls is too high.", "analogy": "Like a garden hose with too much water pressure, which can damage the hose over time.", "category": "cardiovascular"},
    "hypotension": {"definition": "Low blood pressure — when blood pressure drops below normal levels.", "analogy": "Like a garden hose with very low water pressure — not enough flow to reach everything.", "category": "cardiovascular"},
    "tachycardia": {"definition": "A heart rate that is faster than normal, usually over 100 beats per minute at rest.", "analogy": "Your heart is like an engine running too fast when the car is parked.", "category": "cardiovascular"},
    "bradycardia": {"definition": "A heart rate that is slower than normal, usually under 60 beats per minute.", "analogy": "Your heart is beating more slowly than a ticking clock.", "category": "cardiovascular"},
    "arrhythmia": {"definition": "An irregular heartbeat — the heart may beat too fast, too slow, or with an uneven rhythm.", "analogy": "Like a drummer who keeps losing the beat and playing out of rhythm.", "category": "cardiovascular"},
    "atherosclerosis": {"definition": "A buildup of fatty deposits (plaque) inside the arteries that makes them narrow and stiff.", "analogy": "Like old pipes getting clogged with mineral buildup, reducing water flow.", "category": "cardiovascular"},
    "angina": {"definition": "Chest pain caused by reduced blood flow to the heart muscle.", "analogy": "Your heart muscle is not getting enough oxygen, like a cramp in your leg when you run too hard.", "category": "cardiovascular"},
    "myocardial infarction": {"definition": "A heart attack — when blood flow to part of the heart muscle is blocked.", "analogy": "A pipe to your heart gets completely blocked, and the area it feeds starts to get damaged.", "category": "cardiovascular"},
    "edema": {"definition": "Swelling caused by excess fluid trapped in body tissues.", "analogy": "Like a sponge soaking up too much water and puffing up.", "category": "general"},
    "inflammation": {"definition": "The body's response to injury or infection — causes redness, warmth, swelling, and pain.", "analogy": "Your body's alarm system responding to a problem — sending repair crews to the area.", "category": "general"},
    "benign": {"definition": "Not cancerous. A benign growth does not spread to other parts of the body.", "analogy": "A harmless bump that stays in one place and does not cause trouble.", "category": "oncology"},
    "malignant": {"definition": "Cancerous. A malignant tumor can invade nearby tissue and spread to other body parts.", "analogy": "A weed that spreads aggressively through the garden if not removed.", "category": "oncology"},
    "metastasis": {"definition": "The spread of cancer from where it started to other parts of the body.", "analogy": "Seeds from a dandelion blowing in the wind and taking root in new places.", "category": "oncology"},
    "biopsy": {"definition": "A procedure where a small sample of tissue is removed for testing under a microscope.", "analogy": "Taking a tiny core sample from the ground to see what is underneath the surface.", "category": "procedures"},
    "chronic": {"definition": "A condition that lasts a long time, usually more than 3 months, and may not go away.", "analogy": "Like a slow leak in your roof — it does not go away on its own and needs ongoing attention.", "category": "general"},
    "acute": {"definition": "A condition that comes on suddenly and is usually severe but short-lived.", "analogy": "Like a sudden thunderstorm — intense but usually passes relatively quickly.", "category": "general"},
    "prognosis": {"definition": "The likely course or outcome of a disease — what doctors expect will happen.", "analogy": "A weather forecast for your health — the doctor's best prediction of what comes next.", "category": "general"},
    "diagnosis": {"definition": "Identifying a disease or condition based on symptoms, tests, and examination.", "analogy": "Like a detective putting clues together to figure out what is causing the problem.", "category": "general"},
    "antibiotic": {"definition": "A medicine that kills bacteria or stops them from growing. Does not work against viruses.", "analogy": "A targeted weapon that fights only bacterial invaders, not viral ones.", "category": "pharmacology"},
    "analgesic": {"definition": "A pain-relieving medication like aspirin, ibuprofen, or acetaminophen.", "analogy": "A volume knob that turns down the pain signal your body is sending to your brain.", "category": "pharmacology"},
    "antipyretic": {"definition": "A medicine that reduces fever, such as acetaminophen or ibuprofen.", "analogy": "A thermostat that helps bring your body temperature back to normal.", "category": "pharmacology"},
    "immunosuppressant": {"definition": "A medicine that weakens the immune system, used to prevent organ rejection or treat autoimmune diseases.", "analogy": "Putting the brakes on your body's defense system so it stops attacking itself or a transplanted organ.", "category": "pharmacology"},
    "anemia": {"definition": "A condition where you do not have enough healthy red blood cells to carry oxygen.", "analogy": "Not having enough delivery trucks to bring oxygen packages to all parts of your body.", "category": "hematology"},
    "thrombosis": {"definition": "A blood clot that forms inside a blood vessel, blocking blood flow.", "analogy": "A traffic jam inside your blood vessels caused by a clump blocking the road.", "category": "hematology"},
    "embolism": {"definition": "A blood clot or other substance that travels through the bloodstream and blocks a vessel.", "analogy": "A piece of debris floating down a river and getting stuck under a bridge.", "category": "hematology"},
    "glucose": {"definition": "Blood sugar — the main source of energy for your body's cells.", "analogy": "The fuel that powers every cell in your body, like gasoline for a car.", "category": "endocrine"},
    "insulin": {"definition": "A hormone made by the pancreas that helps glucose enter cells for energy.", "analogy": "A key that unlocks cell doors so sugar can get inside and provide energy.", "category": "endocrine"},
    "hypothyroidism": {"definition": "An underactive thyroid gland that does not produce enough thyroid hormone.", "analogy": "Your body's thermostat is set too low, making everything run slower than normal.", "category": "endocrine"},
    "hyperthyroidism": {"definition": "An overactive thyroid gland that produces too much thyroid hormone.", "analogy": "Your body's thermostat is set too high, making everything run faster than it should.", "category": "endocrine"},
    "renal": {"definition": "Relating to the kidneys.", "analogy": "When doctors say 'renal,' they are talking about your kidneys — your body's filtration system.", "category": "renal"},
    "hepatic": {"definition": "Relating to the liver.", "analogy": "When doctors say 'hepatic,' they mean your liver — your body's chemical processing plant.", "category": "gastroenterology"},
    "pulmonary": {"definition": "Relating to the lungs.", "analogy": "When doctors say 'pulmonary,' they are talking about your lungs — your breathing organs.", "category": "pulmonology"},
    "cardiac": {"definition": "Relating to the heart.", "analogy": "When doctors say 'cardiac,' they mean your heart — the pump that circulates blood.", "category": "cardiovascular"},
    "cerebral": {"definition": "Relating to the brain.", "analogy": "When doctors say 'cerebral,' they mean your brain — your body's command center.", "category": "neurology"},
    "gastrointestinal": {"definition": "Relating to the stomach and intestines (the digestive tract).", "analogy": "The entire food processing pipeline — from stomach through intestines.", "category": "gastroenterology"},
    "subcutaneous": {"definition": "Under the skin.", "analogy": "Just beneath the surface of your skin, like planting a seed just below the soil.", "category": "general"},
    "intravenous": {"definition": "Into a vein — usually refers to medications or fluids given through a needle in a vein.", "analogy": "A direct delivery route into your bloodstream, like an express lane.", "category": "general"},
    "bilateral": {"definition": "On both sides of the body.", "analogy": "Affecting both the left and right side — like both ears or both knees.", "category": "general"},
    "contraindication": {"definition": "A reason why a particular treatment or medicine should NOT be used.", "analogy": "A warning sign saying 'do not enter' — this treatment could cause harm in your situation.", "category": "pharmacology"},
    "prophylaxis": {"definition": "Preventive treatment to stop a disease before it starts.", "analogy": "Like wearing a seatbelt — you use it to prevent injury, not to treat one.", "category": "general"},
    "sepsis": {"definition": "A life-threatening condition where the body's response to infection damages its own organs.", "analogy": "Your immune system goes into overdrive fighting an infection and accidentally damages your own body in the process.", "category": "emergency"},
    "dyspnea": {"definition": "Difficulty breathing or shortness of breath.", "analogy": "Feeling like you cannot get enough air, similar to breathing through a narrow straw.", "category": "pulmonology"},
    "neuropathy": {"definition": "Damage to nerves, often causing numbness, tingling, or pain, usually in hands and feet.", "analogy": "Like frayed electrical wires sending wrong signals — tingling, numbness, or pain.", "category": "neurology"},
    "hemoglobin": {"definition": "The protein in red blood cells that carries oxygen throughout the body.", "analogy": "Tiny oxygen taxis inside your red blood cells that pick up oxygen in the lungs and deliver it everywhere.", "category": "hematology"},
    "platelet": {"definition": "Tiny blood cells that help your body form clots to stop bleeding.", "analogy": "Your body's repair crew that rushes to plug holes when you get a cut.", "category": "hematology"},
    "serotonin": {"definition": "A chemical messenger in the brain that affects mood, sleep, and appetite.", "analogy": "A mood-regulating chemical — like a happiness signal that helps keep your emotions balanced.", "category": "neurology"},
    "cortisol": {"definition": "A stress hormone produced by the adrenal glands.", "analogy": "Your body's built-in alarm system hormone — it rises when you are stressed and helps you respond.", "category": "endocrine"},
    "bmi": {"definition": "Body Mass Index — a number calculated from height and weight used to screen for weight categories.", "analogy": "A simple ratio that compares your weight to your height to give a general picture of body size.", "category": "general"},
    "spirometry": {"definition": "A breathing test that measures how much air you can breathe in and out, and how fast.", "analogy": "Blowing into a special device to measure how strong your lungs are, like testing a balloon.", "category": "pulmonology"},
}

# Common medical jargon -> plain English replacements
SIMPLIFICATION_MAP = {
    "hypertension": "high blood pressure",
    "hypotension": "low blood pressure",
    "tachycardia": "fast heart rate",
    "bradycardia": "slow heart rate",
    "myocardial infarction": "heart attack",
    "cerebrovascular accident": "stroke",
    "dyspnea": "shortness of breath",
    "edema": "swelling",
    "pyrexia": "fever",
    "emesis": "vomiting",
    "cephalgia": "headache",
    "arthralgia": "joint pain",
    "myalgia": "muscle pain",
    "syncope": "fainting",
    "epistaxis": "nosebleed",
    "contusion": "bruise",
    "laceration": "cut",
    "pruritus": "itching",
    "erythema": "redness",
    "alopecia": "hair loss",
    "diaphoresis": "heavy sweating",
    "hematuria": "blood in urine",
    "dysuria": "painful urination",
    "polyuria": "frequent urination",
    "anorexia": "loss of appetite",
    "nausea": "feeling sick to your stomach",
    "vertigo": "dizziness or spinning sensation",
    "insomnia": "trouble sleeping",
    "fatigue": "extreme tiredness",
    "malaise": "general feeling of being unwell",
    "bilateral": "on both sides",
    "unilateral": "on one side",
    "proximal": "near the center of the body",
    "distal": "far from the center of the body",
    "acute": "sudden and short-term",
    "chronic": "long-lasting",
    "benign": "not cancerous",
    "malignant": "cancerous",
    "idiopathic": "of unknown cause",
    "etiology": "cause",
    "prognosis": "expected outcome",
    "contraindicated": "should not be used",
    "prophylactic": "preventive",
    "subcutaneous": "under the skin",
    "intravenous": "into a vein",
    "intramuscular": "into a muscle",
    "oral": "by mouth",
    "topical": "applied to the skin",
    "renal": "kidney",
    "hepatic": "liver",
    "pulmonary": "lung",
    "cardiac": "heart",
    "cerebral": "brain",
    "gastrointestinal": "stomach and intestines",
    "dermatological": "skin-related",
    "ophthalmic": "eye-related",
    "otic": "ear-related",
    "hemorrhage": "heavy bleeding",
    "thrombus": "blood clot",
    "emboli": "blood clots that travel",
    "lesion": "abnormal area of tissue",
    "neoplasm": "abnormal growth or tumor",
    "sepsis": "life-threatening infection response",
    "anemia": "low red blood cell count",
}


class HealthLiteracyAgent:
    """Simplifies medical text, explains terms, and generates patient education materials."""

    def simplify_text(self, medical_text: str, target_grade_level: int = 5) -> dict:
        """Rewrite medical text at a specified reading level."""
        simplified = medical_text
        replacements_made = []

        # Replace medical jargon with plain English
        for term, replacement in SIMPLIFICATION_MAP.items():
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            if pattern.search(simplified):
                simplified = pattern.sub(replacement, simplified)
                replacements_made.append({"original": term, "replacement": replacement})

        # Break long sentences (over 25 words) at conjunctions
        sentences = simplified.split(". ")
        shortened = []
        for sent in sentences:
            words = sent.split()
            if len(words) > 25:
                # Try to split at "and", "but", "which", "that"
                mid = len(words) // 2
                split_found = False
                for conj in ["and", "but", "which", "that", "because", "however"]:
                    for i in range(mid - 5, mid + 5):
                        if 0 <= i < len(words) and words[i].lower() == conj:
                            part1 = " ".join(words[:i])
                            part2 = " ".join(words[i+1:]) if conj in ("which", "that") else " ".join(words[i:])
                            shortened.append(part1)
                            shortened.append(part2)
                            split_found = True
                            break
                    if split_found:
                        break
                if not split_found:
                    shortened.append(sent)
            else:
                shortened.append(sent)

        simplified = ". ".join(shortened)

        # Assess both original and simplified
        original_score = self._flesch_kincaid_grade(medical_text)
        simplified_score = self._flesch_kincaid_grade(simplified)

        return {
            "original_text": medical_text,
            "simplified_text": simplified,
            "target_grade_level": target_grade_level,
            "original_grade_level": original_score,
            "simplified_grade_level": simplified_score,
            "replacements_made": replacements_made,
            "total_replacements": len(replacements_made),
            "improvement": round(original_score - simplified_score, 1),
        }

    def explain_term(self, medical_term: str) -> dict:
        """Return a plain English definition and analogy for a medical term."""
        key = medical_term.strip().lower()

        if key in MEDICAL_TERMS:
            info = MEDICAL_TERMS[key]
            return {
                "term": medical_term,
                "found": True,
                "definition": info["definition"],
                "analogy": info["analogy"],
                "category": info["category"],
            }

        # Check simplification map as fallback
        if key in SIMPLIFICATION_MAP:
            return {
                "term": medical_term,
                "found": True,
                "definition": f"{medical_term.title()} means {SIMPLIFICATION_MAP[key]}.",
                "analogy": None,
                "category": "general",
            }

        return {
            "term": medical_term,
            "found": False,
            "definition": None,
            "message": f"Term '{medical_term}' not found in dictionary. Please consult your healthcare provider for an explanation.",
        }

    def generate_patient_education(self, condition: str) -> dict:
        """Generate a structured patient education packet for a condition."""
        key = condition.strip().lower()

        education_db = {
            "hypertension": {
                "title": "Understanding High Blood Pressure",
                "what_it_is": "High blood pressure (hypertension) is when the force of blood pushing against your artery walls is consistently too high. Blood pressure is measured in two numbers: systolic (top) and diastolic (bottom). Normal is below 120/80 mmHg.",
                "symptoms": ["Often has NO symptoms (called 'the silent killer')", "Severe cases: headaches, shortness of breath, nosebleeds", "Dizziness or vision changes"],
                "causes": ["Family history", "Too much salt in diet", "Not enough physical activity", "Being overweight", "Smoking", "Stress", "Age (risk increases over 45)"],
                "treatment": ["Lifestyle changes: exercise 30 min/day, reduce salt, eat fruits and vegetables", "Medications: ACE inhibitors, beta-blockers, diuretics", "Monitor blood pressure at home regularly", "Limit alcohol and quit smoking"],
                "when_to_seek_help": ["Blood pressure over 180/120 (hypertensive crisis)", "Sudden severe headache with confusion", "Chest pain or difficulty breathing", "Vision changes or difficulty speaking"],
                "prevention_tips": ["Maintain a healthy weight", "Exercise regularly", "Eat a balanced, low-sodium diet (DASH diet)", "Limit alcohol", "Manage stress", "Get regular check-ups"],
            },
            "type 2 diabetes": {
                "title": "Understanding Type 2 Diabetes",
                "what_it_is": "Type 2 diabetes is a condition where your body cannot use insulin properly, causing blood sugar levels to be too high. Insulin is a hormone that helps sugar get into your cells for energy.",
                "symptoms": ["Increased thirst and frequent urination", "Unexplained weight loss", "Fatigue and weakness", "Blurred vision", "Slow-healing cuts or frequent infections", "Numbness or tingling in hands/feet"],
                "causes": ["Insulin resistance (body does not respond to insulin)", "Family history", "Being overweight, especially around the waist", "Lack of physical activity", "Age (risk increases over 45)", "History of gestational diabetes"],
                "treatment": ["Blood sugar monitoring", "Healthy eating plan", "Regular exercise (150 min/week)", "Medications (metformin is usually first choice)", "Insulin therapy if needed", "Regular eye, foot, and kidney check-ups"],
                "when_to_seek_help": ["Blood sugar over 300 mg/dL", "Symptoms of diabetic ketoacidosis: nausea, vomiting, fruity breath", "Signs of low blood sugar: shaking, sweating, confusion", "Any foot sore that does not heal"],
                "prevention_tips": ["Lose 5-7% of body weight if overweight", "Exercise at least 150 minutes per week", "Choose whole grains over refined carbs", "Eat plenty of fiber", "Get annual blood sugar screening if at risk"],
            },
            "asthma": {
                "title": "Understanding Asthma",
                "what_it_is": "Asthma is a chronic condition where the airways in your lungs become inflamed and narrow, making it hard to breathe. During an asthma attack, the muscles around the airways tighten and produce extra mucus.",
                "symptoms": ["Wheezing (whistling sound when breathing)", "Shortness of breath", "Chest tightness or pain", "Coughing, especially at night or early morning", "Difficulty sleeping due to breathing problems"],
                "causes": ["Allergens (pollen, dust mites, pet dander, mold)", "Respiratory infections", "Exercise (especially in cold air)", "Air pollution and smoke", "Strong emotions or stress", "Family history of asthma or allergies"],
                "treatment": ["Quick-relief inhaler (albuterol) for attacks", "Daily controller medications (inhaled corticosteroids)", "Avoid known triggers", "Asthma action plan with your doctor", "Peak flow monitoring at home"],
                "when_to_seek_help": ["Severe shortness of breath that does not improve with inhaler", "Cannot speak in full sentences", "Lips or fingernails turn blue", "Peak flow reading in the red zone", "Symptoms getting worse despite treatment"],
                "prevention_tips": ["Identify and avoid your triggers", "Take controller medications daily as prescribed", "Get flu and pneumonia vaccines", "Keep rescue inhaler accessible at all times", "Monitor air quality on high-pollution days"],
            },
            "depression": {
                "title": "Understanding Depression",
                "what_it_is": "Depression (major depressive disorder) is a common but serious mood disorder that affects how you feel, think, and handle daily activities. It is NOT a sign of weakness — it is a medical condition that can be treated.",
                "symptoms": ["Persistent sad, anxious, or empty feeling", "Loss of interest in activities you used to enjoy", "Changes in appetite or weight", "Difficulty sleeping or sleeping too much", "Fatigue and low energy", "Feelings of worthlessness or guilt", "Difficulty concentrating or making decisions", "Thoughts of death or suicide"],
                "causes": ["Brain chemistry imbalance", "Family history", "Traumatic or stressful life events", "Certain medical conditions", "Some medications", "Substance use"],
                "treatment": ["Talk therapy (cognitive behavioral therapy, CBT)", "Antidepressant medications (SSRIs are common first choice)", "Regular exercise", "Support groups", "Lifestyle changes: sleep, diet, social connection", "Combination of therapy and medication is often most effective"],
                "when_to_seek_help": ["Thoughts of suicide or self-harm — call 988 (Suicide & Crisis Lifeline)", "Unable to perform daily activities", "Symptoms lasting more than 2 weeks", "Using alcohol or drugs to cope", "Feeling hopeless or overwhelmed"],
                "prevention_tips": ["Stay connected with friends and family", "Exercise regularly", "Get enough sleep", "Manage stress with healthy coping strategies", "Seek help early — do not wait for it to get worse"],
            },
            "anxiety": {
                "title": "Understanding Anxiety Disorders",
                "what_it_is": "Anxiety disorders involve excessive worry or fear that interferes with daily life. While everyone feels anxious sometimes, anxiety disorders cause persistent, intense worry that is hard to control.",
                "symptoms": ["Excessive worrying that is hard to control", "Restlessness or feeling on edge", "Fatigue", "Difficulty concentrating", "Muscle tension", "Sleep problems", "Irritability", "Panic attacks: sudden intense fear with physical symptoms"],
                "causes": ["Brain chemistry and genetics", "Stressful or traumatic experiences", "Family history of anxiety", "Other medical conditions (thyroid problems, heart conditions)", "Caffeine or substance use"],
                "treatment": ["Cognitive behavioral therapy (CBT)", "Medications (SSRIs, SNRIs, buspirone)", "Relaxation techniques: deep breathing, progressive muscle relaxation", "Regular exercise", "Limiting caffeine and alcohol", "Mindfulness and meditation"],
                "when_to_seek_help": ["Anxiety interferes with work, school, or relationships", "Panic attacks", "Avoiding situations due to fear", "Physical symptoms: chest pain, dizziness, numbness", "Thoughts of self-harm"],
                "prevention_tips": ["Practice stress management daily", "Stay physically active", "Prioritize sleep", "Limit caffeine and alcohol", "Stay socially connected", "Learn and practice relaxation techniques"],
            },
        }

        packet = education_db.get(key)
        if packet:
            return {
                **packet,
                "condition": condition,
                "found": True,
                "reading_level": "5th grade",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

        # Generic fallback
        return {
            "condition": condition,
            "found": False,
            "title": f"About {condition.title()}",
            "what_it_is": f"Detailed patient education for {condition} is not yet in our database. Please ask your healthcare provider for information specific to your situation.",
            "symptoms": [],
            "causes": [],
            "treatment": ["Follow your doctor's treatment plan", "Take medications as prescribed", "Attend follow-up appointments"],
            "when_to_seek_help": ["Symptoms get worse", "New symptoms appear", "Side effects from medications", "Any emergency symptoms"],
            "prevention_tips": ["Maintain a healthy lifestyle", "Follow medical advice", "Get regular check-ups"],
            "reading_level": "5th grade",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def assess_readability(self, text: str) -> dict:
        """Assess text readability using Flesch-Kincaid metrics."""
        words = text.split()
        word_count = len(words)
        sentence_count = max(1, text.count(".") + text.count("!") + text.count("?"))
        syllable_count = sum(self._count_syllables(w) for w in words)
        complex_words = [w for w in words if self._count_syllables(w) >= 3]

        fk_grade = self._flesch_kincaid_grade(text)

        # Flesch Reading Ease
        if word_count > 0 and sentence_count > 0:
            fre = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
            fre = max(0, min(100, round(fre, 1)))
        else:
            fre = 0

        # Determine difficulty label
        if fk_grade <= 5:
            difficulty = "Easy (elementary school level)"
        elif fk_grade <= 8:
            difficulty = "Moderate (middle school level)"
        elif fk_grade <= 12:
            difficulty = "Difficult (high school level)"
        else:
            difficulty = "Very Difficult (college level or above)"

        return {
            "text_preview": text[:200] + "..." if len(text) > 200 else text,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "syllable_count": syllable_count,
            "complex_word_count": len(complex_words),
            "complex_words": complex_words[:20],  # limit output
            "flesch_kincaid_grade": fk_grade,
            "flesch_reading_ease": fre,
            "difficulty": difficulty,
            "avg_words_per_sentence": round(word_count / sentence_count, 1) if sentence_count > 0 else 0,
            "avg_syllables_per_word": round(syllable_count / word_count, 1) if word_count > 0 else 0,
        }

    def translate_medical_content(self, content: str, target_language: str) -> dict:
        """Mock translation of medical content to another language."""
        supported = {
            "es": "Spanish", "fr": "French", "de": "German", "zh": "Chinese (Simplified)",
            "ja": "Japanese", "ko": "Korean", "pt": "Portuguese", "ar": "Arabic",
            "hi": "Hindi", "ru": "Russian", "vi": "Vietnamese", "tl": "Tagalog",
        }

        lang_key = target_language.strip().lower()
        lang_name = supported.get(lang_key)
        if not lang_name:
            return {
                "error": f"Language '{target_language}' not supported. Supported: {', '.join(f'{k} ({v})' for k, v in supported.items())}",
            }

        return {
            "original_text": content,
            "target_language": lang_key,
            "language_name": lang_name,
            "translated_text": f"[{lang_name} translation of: {content[:100]}...]" if len(content) > 100 else f"[{lang_name} translation of: {content}]",
            "note": "This is a mock translation. In production, integrate with a certified medical translation service for accuracy.",
            "disclaimer": "Medical translations should be reviewed by a qualified bilingual healthcare professional.",
            "translated_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_visual_explainer(self, condition: str) -> dict:
        """Generate structured data for an infographic/visual explanation."""
        key = condition.strip().lower()

        explainers = {
            "hypertension": {
                "title": "High Blood Pressure at a Glance",
                "icon": "heart-pulse",
                "color_scheme": "red",
                "sections": [
                    {"heading": "What Is It?", "content": "Blood pushes too hard against artery walls", "icon": "info-circle"},
                    {"heading": "The Numbers", "content": "Normal: <120/80 | Elevated: 120-129/<80 | High: 130+/80+", "icon": "gauge"},
                    {"heading": "Risk Factors", "content": "Age, family history, obesity, high salt, low activity, smoking", "icon": "warning"},
                    {"heading": "What To Do", "content": "Exercise, eat less salt, take meds if prescribed, check BP regularly", "icon": "check-circle"},
                ],
                "key_stats": [
                    {"label": "Adults affected in US", "value": "47%"},
                    {"label": "Called 'silent killer'", "value": "Often no symptoms"},
                    {"label": "Increases risk of", "value": "Heart attack, stroke, kidney disease"},
                ],
                "key_facts": [
                    "1 in 2 adults has high blood pressure",
                    "Only about 1 in 4 has it under control",
                    "Lifestyle changes alone can lower BP by 10-15 points",
                ],
            },
            "type 2 diabetes": {
                "title": "Type 2 Diabetes at a Glance",
                "icon": "droplet",
                "color_scheme": "blue",
                "sections": [
                    {"heading": "What Is It?", "content": "Body cannot use insulin properly, so blood sugar stays high", "icon": "info-circle"},
                    {"heading": "The Numbers", "content": "Normal fasting: <100 | Pre-diabetes: 100-125 | Diabetes: 126+", "icon": "gauge"},
                    {"heading": "Warning Signs", "content": "Thirst, frequent urination, fatigue, blurred vision, slow healing", "icon": "warning"},
                    {"heading": "Management", "content": "Monitor blood sugar, eat well, exercise, take medication", "icon": "check-circle"},
                ],
                "key_stats": [
                    {"label": "Americans with diabetes", "value": "37 million"},
                    {"label": "Pre-diabetic adults", "value": "96 million"},
                    {"label": "Can be prevented/delayed by", "value": "Lifestyle changes"},
                ],
                "key_facts": [
                    "Type 2 accounts for 90-95% of all diabetes cases",
                    "Losing 5-7% body weight reduces risk by 58%",
                    "Regular exercise improves insulin sensitivity",
                ],
            },
            "asthma": {
                "title": "Asthma at a Glance",
                "icon": "lungs",
                "color_scheme": "teal",
                "sections": [
                    {"heading": "What Is It?", "content": "Airways swell and narrow, making breathing difficult", "icon": "info-circle"},
                    {"heading": "Triggers", "content": "Allergens, cold air, exercise, smoke, stress, infections", "icon": "warning"},
                    {"heading": "Symptoms", "content": "Wheezing, coughing, chest tightness, shortness of breath", "icon": "stethoscope"},
                    {"heading": "Treatment", "content": "Rescue inhaler for attacks, daily controller meds, avoid triggers", "icon": "check-circle"},
                ],
                "key_stats": [
                    {"label": "Americans with asthma", "value": "25 million"},
                    {"label": "Asthma attacks/year", "value": "~10 million"},
                    {"label": "Can be well-controlled with", "value": "Proper medication plan"},
                ],
                "key_facts": [
                    "Asthma cannot be cured but can be effectively managed",
                    "An asthma action plan reduces ER visits by 70%",
                    "Peak flow meters help monitor lung function at home",
                ],
            },
        }

        explainer = explainers.get(key)
        if explainer:
            return {
                **explainer,
                "condition": condition,
                "found": True,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

        return {
            "condition": condition,
            "found": False,
            "title": f"{condition.title()} at a Glance",
            "icon": "info-circle",
            "color_scheme": "gray",
            "sections": [
                {"heading": "About This Condition", "content": f"Visual explainer for {condition} is not yet available. Ask your doctor for educational materials.", "icon": "info-circle"},
            ],
            "key_stats": [],
            "key_facts": [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_terminology_database(self) -> dict:
        """Return the full terminology dictionary with stats."""
        categories = {}
        for term, info in MEDICAL_TERMS.items():
            cat = info["category"]
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

        return {
            "total_terms": len(MEDICAL_TERMS),
            "categories": categories,
            "terms": {
                term: {"definition": info["definition"], "category": info["category"]}
                for term, info in sorted(MEDICAL_TERMS.items())
            },
        }

    # ── Internal helpers ────────────────────────────────────────────

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for an English word."""
        word = word.lower().strip(".,!?;:\"'()-")
        if not word:
            return 0
        if len(word) <= 2:
            return 1
        vowels = "aeiouy"
        count = 0
        prev_vowel = False
        for char in word:
            if char in vowels:
                if not prev_vowel:
                    count += 1
                prev_vowel = True
            else:
                prev_vowel = False
        # Adjust for silent e
        if word.endswith("e") and count > 1:
            count -= 1
        return max(1, count)

    def _flesch_kincaid_grade(self, text: str) -> float:
        """Calculate Flesch-Kincaid grade level."""
        words = text.split()
        word_count = len(words)
        if word_count == 0:
            return 0.0
        sentence_count = max(1, text.count(".") + text.count("!") + text.count("?"))
        syllable_count = sum(self._count_syllables(w) for w in words)

        grade = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count / word_count) - 15.59
        return round(max(0, grade), 1)


# Singleton
_literacy_agent = None


def get_literacy_agent() -> HealthLiteracyAgent:
    global _literacy_agent
    if _literacy_agent is None:
        _literacy_agent = HealthLiteracyAgent()
    return _literacy_agent
