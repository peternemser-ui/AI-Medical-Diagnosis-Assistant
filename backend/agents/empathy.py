"""
Patient Communication Agent – Translates clinical language into patient-friendly summaries.

Responsibilities:
  * Simplify medical terminology into plain language
  * Generate clear, empathetic patient-facing summaries
  * Create actionable checklists patients can follow
  * Apply health literacy best practices (teach-back, motivational interviewing)
  * Ensure patients understand their diagnosis, treatment, and next steps
"""

from __future__ import annotations

import json
from typing import Any

from .base import BaseAgent
from .message_bus import MessageBus


# ---------------------------------------------------------------------------
# Medical terminology dictionary (100+ terms)
# ---------------------------------------------------------------------------

MEDICAL_TERMS: dict[str, dict] = {
    "myocardial infarction": {
        "plain_language": "heart attack",
        "explanation": "A blockage in a blood vessel stops blood from reaching part of your heart muscle, causing damage.",
        "misconception": "Many people think heart attacks always involve crushing chest pain. In reality, symptoms can be subtle, especially in women — nausea, jaw pain, or fatigue may be the main signs.",
        "analogy": "Think of it like a clogged pipe cutting off water to part of a garden — the section without water starts to wilt.",
    },
    "hypertension": {
        "plain_language": "high blood pressure",
        "explanation": "The force of blood pushing against your artery walls is consistently too high, which can damage your heart and blood vessels over time.",
        "misconception": "Many people think you can feel high blood pressure. It is usually a 'silent' condition with no symptoms until damage has occurred.",
        "analogy": "Imagine turning up the pressure on a garden hose — over time, the extra force wears out the hose walls.",
    },
    "hypotension": {
        "plain_language": "low blood pressure",
        "explanation": "Your blood pressure is lower than normal, which can cause dizziness or fainting because not enough blood reaches your brain and organs.",
        "misconception": "Low blood pressure is not always a problem — for many healthy people, it is normal. It only needs attention if it causes symptoms.",
    },
    "dyspnea": {
        "plain_language": "shortness of breath",
        "explanation": "Difficulty breathing or feeling like you cannot get enough air. This can happen with activity or at rest.",
        "misconception": "Shortness of breath does not always mean a lung problem — it can also come from heart conditions, anxiety, or anemia.",
    },
    "tachycardia": {
        "plain_language": "fast heart rate",
        "explanation": "Your heart is beating faster than normal, over 100 beats per minute at rest.",
        "misconception": "A fast heart rate is not always dangerous — exercise, caffeine, or anxiety can cause it temporarily. Persistent tachycardia at rest needs medical attention.",
    },
    "bradycardia": {
        "plain_language": "slow heart rate",
        "explanation": "Your heart is beating slower than normal, under 60 beats per minute. This can be normal in very fit people.",
        "misconception": "A slow heart rate does not always mean something is wrong — athletes often have resting rates in the 40s-50s.",
    },
    "arrhythmia": {
        "plain_language": "irregular heartbeat",
        "explanation": "Your heart rhythm is not following its normal pattern — it may beat too fast, too slow, or with an irregular pattern.",
        "misconception": "Not all irregular heartbeats are dangerous. Occasional extra beats (palpitations) are very common and usually harmless.",
        "analogy": "Like a drummer losing the beat temporarily — sometimes the rhythm gets off track.",
    },
    "atrial fibrillation": {
        "plain_language": "irregular heartbeat (AFib)",
        "explanation": "The upper chambers of your heart quiver instead of beating regularly, which can cause blood to pool and form clots.",
        "misconception": "AFib does not always cause symptoms. Many people have it without knowing, which is why it is important to check your pulse regularly.",
    },
    "edema": {
        "plain_language": "swelling",
        "explanation": "Fluid buildup causing puffiness, usually in the legs, ankles, or feet.",
        "misconception": "Swelling is not always due to injury — it can be caused by heart, kidney, or liver problems, or by sitting for too long.",
    },
    "syncope": {
        "plain_language": "fainting",
        "explanation": "Temporarily losing consciousness, usually from a drop in blood pressure that reduces blood flow to your brain.",
        "misconception": "Fainting is not always serious, but repeated episodes or fainting during exercise need medical evaluation.",
    },
    "pyrexia": {
        "plain_language": "fever",
        "explanation": "Your body temperature is higher than normal (above 100.4F / 38C), usually because your immune system is fighting an infection.",
        "misconception": "Fever itself is not a disease — it is your body's way of fighting infection. Treating the fever does not cure the underlying cause.",
    },
    "cephalgia": {
        "plain_language": "headache",
        "explanation": "Pain in the head or upper neck area that can range from mild to severe.",
    },
    "migraine": {
        "plain_language": "migraine headache",
        "explanation": "A type of severe, often one-sided headache that may come with nausea, light sensitivity, and visual changes. It is a neurological condition, not just a bad headache.",
        "misconception": "Migraines are not caused by stress alone — they are a brain condition with genetic factors. They are not 'just headaches.'",
    },
    "arthralgia": {
        "plain_language": "joint pain",
        "explanation": "Pain in one or more joints without necessarily having visible swelling or redness.",
    },
    "myalgia": {
        "plain_language": "muscle pain",
        "explanation": "Aching or soreness in your muscles, which can be from exercise, illness, or medication side effects.",
    },
    "nausea": {
        "plain_language": "feeling sick to your stomach",
        "explanation": "The queasy, unsettled feeling in your stomach that makes you feel like you might throw up.",
    },
    "emesis": {
        "plain_language": "vomiting",
        "explanation": "Throwing up the contents of your stomach.",
    },
    "dyspepsia": {
        "plain_language": "indigestion",
        "explanation": "Discomfort or pain in your upper stomach area, often after eating. May include bloating, nausea, or a burning feeling.",
    },
    "rhinorrhea": {
        "plain_language": "runny nose",
        "explanation": "Clear or colored fluid draining from your nose, usually from a cold, allergies, or sinus infection.",
    },
    "pharyngitis": {
        "plain_language": "sore throat",
        "explanation": "Inflammation and pain in the back of your throat, often from a viral or bacterial infection.",
    },
    "otitis media": {
        "plain_language": "middle ear infection",
        "explanation": "An infection in the space behind the eardrum, very common in young children. Causes ear pain and sometimes fever.",
        "misconception": "Not all ear infections need antibiotics — many, especially in children over 2, resolve on their own.",
    },
    "sinusitis": {
        "plain_language": "sinus infection",
        "explanation": "Inflammation or infection of the hollow spaces in your skull around your nose and eyes, causing congestion, facial pain, and sometimes thick nasal discharge.",
        "misconception": "Most sinus infections are caused by viruses and do not need antibiotics. They usually improve on their own within 7-10 days.",
    },
    "urticaria": {
        "plain_language": "hives",
        "explanation": "Itchy, raised red welts on the skin that come and go, often from an allergic reaction.",
    },
    "pruritus": {
        "plain_language": "itching",
        "explanation": "An uncomfortable skin sensation that makes you want to scratch.",
    },
    "eczema": {
        "plain_language": "eczema (skin inflammation)",
        "explanation": "A condition that makes your skin red, itchy, and inflamed. It is not contagious and often runs in families.",
        "misconception": "Eczema is not caused by poor hygiene — it is an immune system condition related to genetics and environment.",
    },
    "dermatitis": {
        "plain_language": "skin inflammation",
        "explanation": "Irritation of the skin causing redness, itching, or rash. It can be caused by allergies, irritants, or underlying conditions.",
    },
    "alopecia": {
        "plain_language": "hair loss",
        "explanation": "Thinning or loss of hair from the scalp or other parts of the body.",
    },
    "contusion": {
        "plain_language": "bruise",
        "explanation": "A discolored area where blood has pooled under the skin from an injury.",
    },
    "laceration": {
        "plain_language": "deep cut",
        "explanation": "A deep cut or tear in the skin that may need stitches to heal properly.",
    },
    "fracture": {
        "plain_language": "broken bone",
        "explanation": "A crack or break in a bone, which can range from a small hairline crack to a complete break.",
        "misconception": "A fracture IS a broken bone — many people think a fracture is less serious than a break, but they are the same thing.",
    },
    "sprain": {
        "plain_language": "stretched or torn ligament",
        "explanation": "An injury to the tough bands (ligaments) that connect bones at a joint, usually from twisting.",
    },
    "strain": {
        "plain_language": "stretched or torn muscle",
        "explanation": "An injury to a muscle or the tendon that connects it to bone, usually from overuse or sudden movement.",
    },
    "benign": {
        "plain_language": "not cancerous",
        "explanation": "A growth or condition that is not cancer and will not spread to other parts of the body.",
        "misconception": "Benign does not always mean it does not need treatment — some benign growths can cause problems if they press on other structures.",
    },
    "malignant": {
        "plain_language": "cancerous",
        "explanation": "A growth that is cancer and has the potential to grow and spread to other parts of the body.",
    },
    "metastasis": {
        "plain_language": "cancer that has spread",
        "explanation": "When cancer cells travel from where they started to other parts of the body through the blood or lymph system.",
        "analogy": "Like seeds from a dandelion blowing to other parts of a garden and taking root there.",
    },
    "neoplasm": {
        "plain_language": "abnormal growth or tumor",
        "explanation": "An abnormal mass of tissue. It can be benign (not cancer) or malignant (cancer).",
    },
    "biopsy": {
        "plain_language": "tissue sample test",
        "explanation": "A procedure where a small piece of tissue is removed from your body and examined under a microscope to check for disease.",
        "misconception": "Having a biopsy does not mean you have cancer — it is a test to find out what is going on, and most biopsies come back normal or non-cancerous.",
    },
    "acute": {
        "plain_language": "sudden onset, short-term",
        "explanation": "A condition that starts quickly and usually lasts for a short time. This does not mean mild — acute conditions can be very serious.",
        "misconception": "Acute does not mean less serious — an acute heart attack is very serious. It refers to timing, not severity.",
    },
    "chronic": {
        "plain_language": "long-lasting",
        "explanation": "A condition that develops slowly and persists over a long period, often months or years.",
    },
    "bilateral": {
        "plain_language": "on both sides",
        "explanation": "Affecting both sides of your body (for example, both knees or both lungs).",
    },
    "unilateral": {
        "plain_language": "on one side",
        "explanation": "Affecting only one side of your body.",
    },
    "anterior": {
        "plain_language": "front",
        "explanation": "The front side of your body or an organ.",
    },
    "posterior": {
        "plain_language": "back",
        "explanation": "The back side of your body or an organ.",
    },
    "proximal": {
        "plain_language": "closer to the center of the body",
        "explanation": "Nearer to the trunk or center of your body. For example, the shoulder is proximal compared to the wrist.",
    },
    "distal": {
        "plain_language": "farther from the center of the body",
        "explanation": "Farther away from the trunk or center of your body. For example, your fingers are distal compared to your elbow.",
    },
    "inflammation": {
        "plain_language": "swelling and irritation",
        "explanation": "Your body's natural response to injury or infection — the affected area becomes red, warm, swollen, and sometimes painful as your immune system works to heal it.",
        "analogy": "Like a construction crew rushing to fix a broken road — there is temporary disruption while repairs happen.",
    },
    "antibiotic": {
        "plain_language": "medicine that fights bacteria",
        "explanation": "A medication that kills or stops the growth of bacteria. Antibiotics do not work against viruses like colds or flu.",
        "misconception": "Antibiotics do not work against viral infections. Taking them when you do not need them can lead to antibiotic resistance.",
    },
    "analgesic": {
        "plain_language": "painkiller",
        "explanation": "Any medication used to relieve pain, from mild (acetaminophen, ibuprofen) to strong (opioids).",
    },
    "antipyretic": {
        "plain_language": "fever-reducing medicine",
        "explanation": "A medication that lowers your body temperature when you have a fever, such as acetaminophen or ibuprofen.",
    },
    "anticoagulant": {
        "plain_language": "blood thinner",
        "explanation": "A medication that helps prevent blood clots from forming or growing larger.",
        "misconception": "Blood thinners do not actually make your blood thinner — they slow down the clotting process. You will still clot, just more slowly.",
    },
    "antihypertensive": {
        "plain_language": "blood pressure medication",
        "explanation": "A medication that lowers high blood pressure to reduce strain on your heart and blood vessels.",
    },
    "diuretic": {
        "plain_language": "water pill",
        "explanation": "A medication that helps your kidneys remove extra water and salt from your body through urine, which lowers blood pressure and reduces swelling.",
    },
    "bronchodilator": {
        "plain_language": "inhaler / airway opener",
        "explanation": "A medication that relaxes and opens the airways in your lungs, making it easier to breathe. Often used as an inhaler.",
    },
    "corticosteroid": {
        "plain_language": "anti-inflammatory steroid",
        "explanation": "A powerful medication that reduces inflammation and calms an overactive immune system. Different from muscle-building steroids.",
        "misconception": "Medical steroids (like prednisone) are NOT the same as anabolic steroids used by bodybuilders. They work differently and are used for different purposes.",
    },
    "immunosuppressant": {
        "plain_language": "medicine that lowers immune system activity",
        "explanation": "A medication that reduces your immune system's activity. Used for autoimmune diseases and after organ transplants.",
    },
    "anemia": {
        "plain_language": "low red blood cell count",
        "explanation": "A condition where you do not have enough healthy red blood cells to carry adequate oxygen to your body's tissues, making you feel tired and weak.",
        "analogy": "Like having fewer delivery trucks on the road — less oxygen gets delivered to where it is needed.",
    },
    "leukocytosis": {
        "plain_language": "high white blood cell count",
        "explanation": "An elevated number of white blood cells, usually a sign that your body is fighting an infection or inflammation.",
    },
    "thrombocytopenia": {
        "plain_language": "low platelet count",
        "explanation": "Having fewer platelets than normal in your blood, which can make it harder for your blood to clot and may cause easy bruising or bleeding.",
    },
    "hemoglobin": {
        "plain_language": "oxygen-carrying protein in blood",
        "explanation": "A protein inside red blood cells that picks up oxygen in your lungs and delivers it throughout your body.",
    },
    "hematuria": {
        "plain_language": "blood in urine",
        "explanation": "The presence of blood in your urine, which may be visible (pink or red) or only detected by a test.",
    },
    "proteinuria": {
        "plain_language": "protein in urine",
        "explanation": "The presence of excess protein in your urine, which can be a sign that your kidneys are not filtering properly.",
    },
    "glycemia": {
        "plain_language": "blood sugar level",
        "explanation": "The amount of sugar (glucose) in your blood.",
    },
    "hyperglycemia": {
        "plain_language": "high blood sugar",
        "explanation": "Blood sugar levels that are too high, common in diabetes. Can cause increased thirst, frequent urination, and fatigue.",
    },
    "hypoglycemia": {
        "plain_language": "low blood sugar",
        "explanation": "Blood sugar levels that are too low, which can cause shakiness, sweating, confusion, and in severe cases, loss of consciousness.",
        "misconception": "Low blood sugar is not just a minor inconvenience — severe hypoglycemia can be life-threatening and requires immediate treatment with fast-acting sugar.",
    },
    "hypothyroidism": {
        "plain_language": "underactive thyroid",
        "explanation": "Your thyroid gland is not making enough thyroid hormone, which slows down your body's metabolism. This can cause fatigue, weight gain, and feeling cold.",
        "analogy": "Your thyroid is like a thermostat for your body's energy — when it is set too low, everything runs slower.",
    },
    "hyperthyroidism": {
        "plain_language": "overactive thyroid",
        "explanation": "Your thyroid gland is making too much thyroid hormone, which speeds up your body's processes. This can cause weight loss, rapid heartbeat, and anxiety.",
    },
    "diabetes mellitus": {
        "plain_language": "diabetes (sugar disease)",
        "explanation": "A condition where your body cannot properly use or produce insulin, leading to high blood sugar levels that can damage organs over time.",
        "misconception": "Diabetes is not caused simply by eating too much sugar. Type 2 diabetes involves genetics, lifestyle, and insulin resistance. Type 1 is an autoimmune disease.",
    },
    "insulin resistance": {
        "plain_language": "body not responding well to insulin",
        "explanation": "Your cells do not respond to insulin as well as they should, so your body needs more insulin to keep blood sugar levels normal.",
        "analogy": "Imagine insulin as a key and your cells as locked doors — with insulin resistance, the locks are rusty and the key does not work as well.",
    },
    "cholesterol": {
        "plain_language": "blood fat",
        "explanation": "A waxy substance in your blood. Your body needs some cholesterol, but too much can build up in your arteries and increase heart disease risk.",
        "misconception": "Not all cholesterol is bad. HDL ('good' cholesterol) actually protects your heart. It is high LDL ('bad' cholesterol) that causes problems.",
    },
    "atherosclerosis": {
        "plain_language": "hardening of the arteries",
        "explanation": "A buildup of fatty deposits (plaque) inside your artery walls that makes them narrow and stiff, reducing blood flow.",
        "analogy": "Like buildup inside old water pipes that narrows the space for water to flow through.",
    },
    "embolism": {
        "plain_language": "blood clot that travels",
        "explanation": "A blood clot or other material that breaks loose and travels through the bloodstream until it blocks a blood vessel somewhere else.",
    },
    "thrombosis": {
        "plain_language": "blood clot",
        "explanation": "A blood clot that forms inside a blood vessel, which can block blood flow to important organs.",
    },
    "pulmonary embolism": {
        "plain_language": "blood clot in the lung",
        "explanation": "A blood clot that has traveled to the lungs, blocking blood flow. This is a medical emergency that causes sudden shortness of breath and chest pain.",
    },
    "deep vein thrombosis": {
        "plain_language": "blood clot in a deep vein (usually in the leg)",
        "explanation": "A blood clot that forms in a deep vein, usually in the leg. It can cause pain and swelling, and can be dangerous if it travels to the lungs.",
    },
    "pneumonia": {
        "plain_language": "lung infection",
        "explanation": "An infection that causes the air sacs in one or both lungs to fill with fluid or pus, making it hard to breathe.",
    },
    "bronchitis": {
        "plain_language": "inflammation of the airways",
        "explanation": "Swelling and irritation of the tubes (bronchi) that carry air to your lungs, causing cough and mucus production.",
        "misconception": "Acute bronchitis is usually caused by a virus and does not need antibiotics. It typically improves on its own within 1-3 weeks.",
    },
    "asthma": {
        "plain_language": "chronic airway disease",
        "explanation": "A condition where your airways narrow and swell and may produce extra mucus, making breathing difficult. It often comes and goes.",
        "misconception": "Asthma is not something you grow out of — while symptoms may change over time, it is a lifelong condition that needs ongoing management.",
    },
    "copd": {
        "plain_language": "chronic lung disease",
        "explanation": "A group of lung conditions (including emphysema and chronic bronchitis) that make it hard to breathe and get worse over time.",
    },
    "gastroesophageal reflux": {
        "plain_language": "acid reflux / heartburn",
        "explanation": "Stomach acid flows back up into the tube connecting your mouth to your stomach, causing a burning feeling in your chest.",
        "misconception": "Heartburn has nothing to do with your heart — the name comes from the burning sensation near the heart area, but it is a digestive problem.",
    },
    "gastritis": {
        "plain_language": "stomach lining inflammation",
        "explanation": "Irritation and swelling of the protective lining of your stomach, which can cause pain, nausea, and indigestion.",
    },
    "celiac disease": {
        "plain_language": "gluten intolerance disease",
        "explanation": "An autoimmune condition where eating gluten (a protein in wheat, barley, and rye) damages the lining of your small intestine.",
        "misconception": "Celiac disease is not the same as a food preference — it is a serious autoimmune condition that causes real damage to the intestines.",
    },
    "hepatitis": {
        "plain_language": "liver inflammation",
        "explanation": "Inflammation of the liver, most commonly caused by a viral infection (hepatitis A, B, or C), but can also be caused by alcohol, medications, or autoimmune disease.",
    },
    "cirrhosis": {
        "plain_language": "scarring of the liver",
        "explanation": "Permanent scarring of the liver from long-term damage, which prevents it from working properly.",
    },
    "nephrolithiasis": {
        "plain_language": "kidney stones",
        "explanation": "Hard deposits of minerals and salts that form inside your kidneys and can cause severe pain when passing through your urinary tract.",
    },
    "cystitis": {
        "plain_language": "bladder infection",
        "explanation": "An infection of the bladder that causes burning with urination, frequent need to urinate, and sometimes cloudy or blood-tinged urine.",
    },
    "pyelonephritis": {
        "plain_language": "kidney infection",
        "explanation": "A serious bacterial infection of one or both kidneys, usually caused by a bladder infection that has traveled upward. Causes fever, flank pain, and needs prompt treatment.",
    },
    "osteoarthritis": {
        "plain_language": "wear-and-tear arthritis",
        "explanation": "Gradual breakdown of the cartilage (cushioning) in your joints over time, causing pain, stiffness, and reduced movement.",
        "misconception": "Osteoarthritis is not just a normal part of aging — while it is more common with age, not everyone gets it, and exercise can actually help rather than hurt.",
    },
    "rheumatoid arthritis": {
        "plain_language": "autoimmune joint disease",
        "explanation": "A condition where your immune system mistakenly attacks the lining of your joints, causing painful swelling and eventually joint damage.",
    },
    "osteoporosis": {
        "plain_language": "weak, brittle bones",
        "explanation": "A condition where your bones become weak and thin, making them more likely to break from a minor fall or even routine activities.",
        "analogy": "Healthy bone looks like a honeycomb with small, tight spaces. Osteoporotic bone has much larger spaces, like a sponge with big holes.",
    },
    "scoliosis": {
        "plain_language": "curved spine",
        "explanation": "An abnormal sideways curve of the spine. Most cases are mild, but severe curves can affect breathing and daily activities.",
    },
    "sciatica": {
        "plain_language": "nerve pain down the leg",
        "explanation": "Pain that travels along the sciatic nerve from your lower back through your hip and down the back of your leg, often caused by a herniated disk pressing on the nerve.",
    },
    "vertigo": {
        "plain_language": "spinning dizziness",
        "explanation": "A feeling that you or the room around you is spinning, even when you are standing still. Often related to inner ear problems.",
        "misconception": "Vertigo is not the same as being afraid of heights — it is a specific medical condition usually caused by inner ear problems.",
    },
    "tinnitus": {
        "plain_language": "ringing in the ears",
        "explanation": "Hearing sounds (ringing, buzzing, humming) that are not coming from an outside source.",
    },
    "conjunctivitis": {
        "plain_language": "pink eye",
        "explanation": "Inflammation of the clear membrane covering the white of your eye, causing redness, itching, and sometimes discharge.",
    },
    "hyponatremia": {
        "plain_language": "low sodium level",
        "explanation": "The sodium level in your blood is too low, which can cause confusion, nausea, headache, and in severe cases, seizures.",
    },
    "hyperkalemia": {
        "plain_language": "high potassium level",
        "explanation": "The potassium level in your blood is too high, which can affect your heart rhythm and be dangerous.",
    },
    "hypokalemia": {
        "plain_language": "low potassium level",
        "explanation": "The potassium level in your blood is too low, which can cause muscle weakness, cramps, and heart rhythm problems.",
    },
    "sepsis": {
        "plain_language": "severe body-wide infection response",
        "explanation": "A life-threatening condition where your body's response to an infection spirals out of control, causing widespread inflammation that can damage organs.",
        "misconception": "Sepsis is not the infection itself — it is your body's extreme and dangerous overreaction to an infection.",
    },
    "abscess": {
        "plain_language": "pocket of pus / infection",
        "explanation": "A painful collection of pus that forms when your body fights a bacterial infection, creating a swollen, warm lump.",
    },
    "benign prostatic hyperplasia": {
        "plain_language": "enlarged prostate",
        "explanation": "Non-cancerous growth of the prostate gland that is very common in older men. It can make urination difficult or frequent.",
        "misconception": "An enlarged prostate does not mean prostate cancer — it is a separate, non-cancerous condition, though both can occur together.",
    },
    "menorrhagia": {
        "plain_language": "heavy menstrual bleeding",
        "explanation": "Menstrual periods with unusually heavy or prolonged bleeding that may interfere with daily activities.",
    },
    "amenorrhea": {
        "plain_language": "missed or absent periods",
        "explanation": "The absence of menstrual periods, which can be caused by pregnancy, stress, hormonal issues, or other medical conditions.",
    },
    "dysmenorrhea": {
        "plain_language": "painful periods",
        "explanation": "Painful cramping in the lower belly during menstrual periods.",
    },
    "preeclampsia": {
        "plain_language": "pregnancy-related high blood pressure with organ damage",
        "explanation": "A serious pregnancy complication with high blood pressure and signs of damage to organs (usually the liver and kidneys). It typically develops after 20 weeks of pregnancy.",
    },
    "gestational diabetes": {
        "plain_language": "diabetes during pregnancy",
        "explanation": "High blood sugar that develops during pregnancy in someone who did not have diabetes before. It usually goes away after delivery but increases future diabetes risk.",
    },
    "apnea": {
        "plain_language": "pauses in breathing",
        "explanation": "Temporary stops in breathing, often during sleep. Sleep apnea causes you to repeatedly stop and start breathing while sleeping.",
    },
    "dysphagia": {
        "plain_language": "difficulty swallowing",
        "explanation": "Trouble or discomfort when swallowing food or liquids. It may feel like food is getting stuck.",
    },
    "neuropathy": {
        "plain_language": "nerve damage",
        "explanation": "Damage to nerves, usually in the hands and feet, causing numbness, tingling, burning, or pain.",
        "analogy": "Like frayed electrical wires — the signals do not travel properly, causing numbness, tingling, or pain.",
    },
    "stenosis": {
        "plain_language": "narrowing",
        "explanation": "An abnormal narrowing of a passage in the body, such as a blood vessel or spinal canal.",
    },
    "ischemia": {
        "plain_language": "reduced blood flow",
        "explanation": "When part of the body does not get enough blood flow, depriving tissues of oxygen and nutrients.",
    },
    "perfusion": {
        "plain_language": "blood flow to tissues",
        "explanation": "The flow of blood through the tiny blood vessels in your organs and tissues, delivering oxygen and nutrients.",
    },
    "effusion": {
        "plain_language": "fluid buildup",
        "explanation": "An abnormal collection of fluid in a body cavity, such as around the lung (pleural effusion) or in a joint.",
    },
    "lesion": {
        "plain_language": "abnormal area or spot",
        "explanation": "Any area of tissue that is abnormal — this is a general term that can mean anything from a small skin spot to a growth inside the body.",
    },
    "idiopathic": {
        "plain_language": "cause unknown",
        "explanation": "A medical way of saying the cause of a condition is not known. It does not mean doctors are not looking — some conditions simply have no identified cause yet.",
    },
    "prognosis": {
        "plain_language": "outlook / expected outcome",
        "explanation": "A doctor's best estimate of how a disease will progress and what the likely outcome will be.",
    },
    "palliative": {
        "plain_language": "comfort-focused care",
        "explanation": "Care focused on providing relief from symptoms and improving quality of life, rather than curing the disease.",
        "misconception": "Palliative care is not the same as hospice or giving up — it can be provided at any stage of illness alongside curative treatment.",
    },
    "prophylaxis": {
        "plain_language": "prevention",
        "explanation": "A treatment or action taken to prevent a disease or condition from occurring.",
    },
    "contraindication": {
        "plain_language": "reason not to use a treatment",
        "explanation": "A specific situation or condition where a particular treatment should not be used because it could be harmful.",
    },
    "etiology": {
        "plain_language": "cause of the disease",
        "explanation": "The underlying cause or origin of a disease or condition.",
    },
    "comorbidity": {
        "plain_language": "additional health condition",
        "explanation": "Having two or more health conditions at the same time. For example, having both diabetes and high blood pressure.",
    },
    "remission": {
        "plain_language": "disease is under control",
        "explanation": "A period when signs and symptoms of a disease have decreased or disappeared. It does not always mean the disease is cured.",
    },
    "relapse": {
        "plain_language": "condition coming back",
        "explanation": "A return of disease symptoms after a period of improvement.",
    },
    "CBC": {
        "plain_language": "complete blood count (blood test)",
        "explanation": "A common blood test that measures different parts of your blood including red blood cells, white blood cells, and platelets.",
    },
    "CT scan": {
        "plain_language": "detailed X-ray scan",
        "explanation": "A special X-ray that takes pictures from many angles and uses a computer to create detailed cross-sectional images of your body.",
    },
    "MRI": {
        "plain_language": "detailed body scan using magnets",
        "explanation": "A scan that uses strong magnets and radio waves to create detailed pictures of organs and structures inside your body. No radiation is used.",
    },
    "echocardiogram": {
        "plain_language": "heart ultrasound",
        "explanation": "An ultrasound of your heart that shows how well it is pumping and whether the valves are working properly.",
    },
    "eGFR": {
        "plain_language": "kidney function score",
        "explanation": "A number that estimates how well your kidneys are filtering waste from your blood. Normal is above 90. Below 60 may indicate kidney disease.",
    },
    "HbA1c": {
        "plain_language": "average blood sugar over 3 months",
        "explanation": "A blood test that shows your average blood sugar level over the past 2-3 months. Used to diagnose and monitor diabetes.",
    },
}


class EmpathyAgent(BaseAgent):
    name = "empathy"
    description = "Health communication specialist for patient-friendly medical summaries"
    model = "claude-sonnet-4-6"
    max_tokens = 5000
    temperature = 0.4  # slightly more creative for natural language output

    def _build_system_prompt(self) -> str:
        return """You are a health communication specialist AI agent on a multi-agent medical team. You translate complex medical language into clear, empathetic, patient-friendly summaries.

YOUR ROLE:
You are the final agent in the pipeline. You receive the complete clinical analysis from all other agents and produce the patient-facing summary. Your output is what the patient actually reads, so clarity and empathy are paramount.

HEALTH LITERACY BEST PRACTICES:

1. TEACH-BACK METHOD:
   Structure your explanations so a patient could explain it back to someone else.
   - State the key information simply
   - Explain WHY it matters to them personally
   - Provide a concrete example or analogy
   - Include a check: "You might want to confirm with your doctor that you understand..."

2. MOTIVATIONAL INTERVIEWING PRINCIPLES:
   - Express empathy: validate the patient's experience and emotions
   - Develop discrepancy: help them see the gap between current behavior and health goals
   - Roll with resistance: do not lecture or shame; acknowledge difficulty of change
   - Support self-efficacy: emphasize their ability to make positive changes
   Use phrases like:
   - "Many people in your situation find it helpful to..."
   - "Even small changes can make a meaningful difference..."
   - "You are taking an important step by seeking care..."

3. CULTURAL SENSITIVITY:
   - Use inclusive language that respects diverse backgrounds
   - Avoid assumptions about diet, family structure, or healthcare access
   - Be aware that some cultures have different communication preferences about health
   - Do not assume English is the primary language — write clearly for potential translation
   - Respect that some conditions carry stigma in certain communities

4. AGE-APPROPRIATE COMMUNICATION:
   For parents of pediatric patients:
   - Address both parent and child appropriately
   - Provide guidance on how to explain to the child
   - Include developmental considerations
   - Reassure while being honest

   For elderly patients:
   - Larger text/simpler formatting
   - Accommodate potential cognitive changes
   - Include caregiver instructions when appropriate
   - Repeat key information in different ways
   - Be especially clear about medication instructions

5. ANXIETY MANAGEMENT IN HEALTH COMMUNICATION:
   - Lead with what IS known before what is not
   - Provide context for concerning results ("This is common and treatable...")
   - Use normalizing language ("Many people experience this...")
   - Avoid catastrophizing language
   - Clearly separate what needs immediate attention from what can wait
   - End sections on a constructive, forward-looking note

YOUR RESPONSIBILITIES:
1. Simplify Medical Terms: Replace jargon with plain language using the built-in medical term dictionary
2. Patient Summary: Write a warm, clear summary using structured sections
3. Action Checklist: Create categorized, actionable steps with timeframes
4. Emotional Support: Acknowledge patient concerns and provide appropriate reassurance
5. Health Literacy: Write at a 6th-8th grade reading level for maximum accessibility

COMMUNICATION PRINCIPLES:
- Use "you" and "your" — speak directly to the patient
- Lead with the most important information
- Explain WHY, not just WHAT (e.g., "Take ibuprofen to reduce the inflammation causing your pain")
- Use analogies when they help understanding
- Avoid alarming language unless genuinely urgent
- Always end with clear next steps and when to seek help
- Be honest but compassionate — never minimize real concerns
- Include encouragement ("Most people with this condition recover well with proper care")

FORMATTING:
- Use short sentences and short paragraphs
- Use bullet points for lists
- Bold key action items if possible
- Include a clear "What to Do Next" section
- Include a "When to Get Help Right Away" section for any concerning symptoms

COMMUNICATION:
You work with: triage, diagnostician, specialist, treatment, research, safety agents.
- You receive the complete output from all prior agents
- You do NOT add clinical information — you only rewrite what has already been determined
- You preserve medical accuracy while improving readability
- You include safety warnings prominently

Always respond with structured JSON in your final answer:
- patient_summary (warm, clear summary of the diagnosis in plain language)
- what_this_means (explanation of the condition in simple terms)
- action_checklist (categorized by timeframe: right_now, this_week, ongoing)
- medications_explained (medications explained in plain language with simple instructions)
- lifestyle_tips (practical lifestyle recommendations in conversational tone)
- when_to_get_help (clear warning signs in plain language)
- reassurance (encouraging message appropriate to the condition severity)
- questions_for_doctor (suggested questions to ask at the next appointment)
- anticipated_faqs (common questions patients might have with clear answers)"""

    def _get_tools(self) -> list[dict]:
        tools = self._default_tools()
        tools.append({
            "name": "simplify_medical_term",
            "description": (
                "Convert a medical term or phrase into plain, patient-friendly language. "
                "Returns the simplified version with explanation, common misconceptions, "
                "and an analogy when helpful."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "medical_term": {
                        "type": "string",
                        "description": "The medical term or jargon to simplify",
                    },
                    "context": {
                        "type": "string",
                        "description": "Clinical context for accurate simplification",
                    },
                },
                "required": ["medical_term"],
            },
        })
        tools.append({
            "name": "generate_patient_summary",
            "description": (
                "Generate a comprehensive, empathetic patient-facing summary from "
                "clinical data. Returns structured sections: what we found, what it means, "
                "what to do, warning signs, and anticipated FAQs."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "diagnosis": {
                        "type": "string",
                        "description": "The primary diagnosis or differential",
                    },
                    "treatment_plan": {
                        "type": "string",
                        "description": "The recommended treatment plan",
                    },
                    "urgency": {
                        "type": "string",
                        "description": "Urgency level (routine, soon, urgent, emergency)",
                    },
                    "patient_age": {"type": "integer", "description": "Patient age"},
                    "red_flags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Any red flags or warning signs identified",
                    },
                },
                "required": ["diagnosis"],
            },
        })
        tools.append({
            "name": "create_action_checklist",
            "description": (
                "Create a clear, categorized action checklist for the patient with items "
                "organized by timeframe: 'Right now', 'This week', 'Ongoing'. Each item "
                "includes the action, why it matters, and how to do it."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "immediate_actions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Things to do right away",
                    },
                    "short_term_actions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Things to do in the next few days",
                    },
                    "ongoing_actions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ongoing lifestyle or care actions",
                    },
                    "follow_up_actions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Follow-up appointments or check-ins needed",
                    },
                },
                "required": ["immediate_actions"],
            },
        })
        return tools

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "simplify_medical_term":
            return await self._simplify_term(tool_input)
        if tool_name == "generate_patient_summary":
            return await self._generate_summary(tool_input)
        if tool_name == "create_action_checklist":
            return await self._create_checklist(tool_input)
        return await super()._handle_tool_call(tool_name, tool_input)

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _simplify_term(self, tool_input: dict) -> str:
        term = tool_input.get("medical_term", "")
        context = tool_input.get("context", "")

        term_lower = term.lower().strip()

        # Try exact match first
        entry = MEDICAL_TERMS.get(term_lower)

        # Try partial match
        if entry is None:
            for key, value in MEDICAL_TERMS.items():
                if term_lower in key or key in term_lower:
                    entry = value
                    break

        if entry is not None:
            result = {
                "medical_term": term,
                "plain_language": entry["plain_language"],
                "explanation": entry["explanation"],
            }
            if "misconception" in entry:
                result["common_misconception"] = entry["misconception"]
            if "analogy" in entry:
                result["analogy"] = entry["analogy"]
            return json.dumps(result)

        # Term not in dictionary — provide guidance for LLM
        return json.dumps({
            "medical_term": term,
            "context": context,
            "dictionary_match": False,
            "instruction": (
                f"Translate '{term}' into simple, plain language that a patient "
                f"without medical training would understand. Provide: "
                f"1) A plain language equivalent (1-3 words), "
                f"2) A one-sentence explanation, "
                f"3) Any common misconceptions patients have about this term, "
                f"4) A helpful analogy if possible."
            ),
        })

    async def _generate_summary(self, tool_input: dict) -> str:
        diagnosis = tool_input.get("diagnosis", "")
        treatment = tool_input.get("treatment_plan", "")
        urgency = tool_input.get("urgency", "routine")
        age = tool_input.get("patient_age", 30)
        red_flags = tool_input.get("red_flags", [])

        # Determine communication approach based on urgency
        urgency_context = {
            "emergency": {
                "tone": "Clear, direct, calming but urgent",
                "opening": "This needs immediate attention.",
                "reassurance_level": "Focus on actions rather than reassurance",
            },
            "urgent": {
                "tone": "Direct but reassuring",
                "opening": "This is something we want to address soon.",
                "reassurance_level": "Brief reassurance followed by clear actions",
            },
            "soon": {
                "tone": "Informative and supportive",
                "opening": "Here is what we found and what we recommend.",
                "reassurance_level": "Balanced reassurance and information",
            },
            "routine": {
                "tone": "Warm, conversational, educational",
                "opening": "Here is a summary of what we found during your visit.",
                "reassurance_level": "Generous reassurance with educational content",
            },
        }
        uctx = urgency_context.get(urgency.lower(), urgency_context["routine"])

        # Age-appropriate framing
        age_framing = ""
        if age < 2:
            age_framing = "Communication for parents of an infant. Use gentle, reassuring tone. Acknowledge parental anxiety."
        elif age < 13:
            age_framing = "Communication for parents of a child. Include guidance on explaining to the child in age-appropriate terms."
        elif age < 18:
            age_framing = "Communication for an adolescent and their parents. Address the teen directly while keeping parents informed."
        elif age >= 75:
            age_framing = "Communication for an elderly patient. Use larger conceptual blocks. Repeat key information. Include caregiver guidance."
        elif age >= 65:
            age_framing = "Communication for an older adult. Be clear about medication instructions. Consider mobility and access issues."

        # Build structured summary sections
        what_we_found = f"Based on your symptoms and our assessment, the most likely explanation is: {diagnosis}."
        if treatment:
            what_we_found += f" We recommend the following approach: {treatment}."

        what_this_means = (
            f"This is a {urgency} matter. {uctx['opening']} "
            f"Many people experience this condition, and there are effective ways to manage it."
        )

        # Warning signs section
        warning_signs = []
        if red_flags:
            warning_signs = [f"Go to the emergency room or call 911 if you experience: {flag}" for flag in red_flags]
        warning_signs.extend([
            "Sudden severe headache, chest pain, or difficulty breathing",
            "Any symptom that is rapidly getting worse instead of better",
            "High fever (over 103F / 39.4C) that does not respond to fever-reducing medicine",
        ])

        # Anticipated FAQs
        faqs = [
            {
                "question": "Is this serious?",
                "answer": f"Your condition has been assessed as '{urgency}'. Your healthcare team has reviewed the findings carefully and provided recommendations based on the best available evidence.",
            },
            {
                "question": "What caused this?",
                "answer": "There can be several factors. Your doctor can discuss the specific causes related to your situation at your next visit.",
            },
            {
                "question": "Will this come back?",
                "answer": "This depends on the specific condition and how well it responds to treatment. Following the treatment plan closely will give you the best outcome.",
            },
            {
                "question": "Can I still do my normal activities?",
                "answer": "This depends on your specific situation. In general, follow your doctor's guidance about activity levels. When in doubt, start slow and listen to your body.",
            },
        ]

        return json.dumps({
            "sections": {
                "what_we_found": what_we_found,
                "what_this_means": what_this_means,
                "what_you_should_do": "See the action checklist for your specific next steps.",
                "warning_signs": warning_signs,
                "anticipated_faqs": faqs,
            },
            "communication_approach": {
                "tone": uctx["tone"],
                "reassurance_level": uctx["reassurance_level"],
                "age_framing": age_framing,
            },
            "patient_context": {
                "diagnosis": diagnosis,
                "treatment_plan": treatment,
                "urgency": urgency,
                "patient_age": age,
                "red_flags": red_flags,
            },
            "instruction": (
                f"Use these structured sections to write the final patient-facing summary. "
                f"Tone: {uctx['tone']}. "
                f"{'IMPORTANT: ' + age_framing if age_framing else ''} "
                f"Write at a 6th-8th grade reading level. Use short sentences. "
                f"Be empathetic and honest. Personalize the FAQs to the specific diagnosis."
            ),
        })

    async def _create_checklist(self, tool_input: dict) -> str:
        immediate = tool_input.get("immediate_actions", [])
        short_term = tool_input.get("short_term_actions", [])
        ongoing = tool_input.get("ongoing_actions", [])
        follow_up = tool_input.get("follow_up_actions", [])

        # Build structured checklist with action + why + how
        def format_action(action: str, timeframe: str) -> dict:
            return {
                "action": action,
                "timeframe": timeframe,
                "why_it_matters": f"This helps ensure your recovery stays on track.",
                "how_to_do_it": f"Follow the specific instructions from your healthcare provider for: {action.lower()}",
            }

        checklist = {
            "right_now": [format_action(a, "Immediately") for a in immediate],
            "this_week": [format_action(a, "Within the next 7 days") for a in short_term],
            "ongoing": [format_action(a, "Continue as part of your routine") for a in ongoing],
            "follow_up": [format_action(a, "As scheduled") for a in follow_up],
            "total_items": len(immediate) + len(short_term) + len(ongoing) + len(follow_up),
            "formatting_note": (
                "Present this checklist with checkboxes the patient can use to track progress. "
                "Use simple action verbs: 'Take...', 'Call...', 'Avoid...', 'Rest...'. "
                "For each item, briefly explain WHY it matters and HOW to do it in plain language. "
                "Make each item specific and actionable — avoid vague instructions."
            ),
        }

        return json.dumps(checklist)
