"""
Medication Management API — comprehensive medication tracking, interaction checking,
adherence logging, side effect reporting, and Claude-powered features.

All data is stored in-memory (keyed by user_id). Claude is used for advanced features
like food interaction analysis, prescription scanning, pill identification, and
side effect pattern analysis.
"""

from __future__ import annotations

import os
import json
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Header, Query
from pydantic import BaseModel, Field

from agents.drug_interaction_agent import get_drug_interaction_agent, INTERACTION_DB

logger = logging.getLogger(__name__)

# ── Router ────────────────────────────────────────────────────────────

medication_router = APIRouter(prefix="/api/medications", tags=["medications"])


# ══════════════════════════════════════════════════════════════════════
# Pydantic Models
# ══════════════════════════════════════════════════════════════════════

class MedicationCreate(BaseModel):
    name: str
    dosage: str = ""
    frequency: str = ""
    time_of_day: list[str] = Field(default_factory=list)
    prescriber: str = ""
    purpose: str = ""
    start_date: str = ""
    end_date: str = ""
    refill_date: str = ""
    pills_remaining: Optional[int] = None
    notes: str = ""
    active: bool = True


class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time_of_day: Optional[list[str]] = None
    prescriber: Optional[str] = None
    purpose: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    refill_date: Optional[str] = None
    pills_remaining: Optional[int] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class InteractionCheckRequest(BaseModel):
    medications: list[str]
    allergies: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)


class FoodInteractionRequest(BaseModel):
    medications: list[str]


class AdherenceLog(BaseModel):
    medication_id: str
    status: str  # "taken", "skipped", "late"
    scheduled_time: str = ""
    actual_time: str = ""
    notes: str = ""


class SideEffectReport(BaseModel):
    medication_id: str
    medication_name: str = ""
    symptom: str
    severity: str = "mild"  # mild, moderate, severe
    onset: str = ""
    duration: str = ""
    notes: str = ""


class SideEffectAnalysisRequest(BaseModel):
    medication_names: list[str] = Field(default_factory=list)


class ReminderCreate(BaseModel):
    medication_id: str
    medication_name: str = ""
    time: str  # HH:MM
    days: list[str] = Field(default_factory=lambda: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    enabled: bool = True
    notes: str = ""


class PrescriptionScanRequest(BaseModel):
    image_base64: str
    media_type: str = "image/jpeg"


class PillIdentifyRequest(BaseModel):
    image_base64: str
    media_type: str = "image/jpeg"
    description: str = ""


# ══════════════════════════════════════════════════════════════════════
# In-Memory Storage
# ══════════════════════════════════════════════════════════════════════

# All keyed by user_id
_medications: dict[str, dict[str, dict]] = {}  # user_id -> {med_id -> med}
_adherence: dict[str, list[dict]] = {}          # user_id -> [log entries]
_side_effects: dict[str, list[dict]] = {}       # user_id -> [reports]
_reminders: dict[str, dict[str, dict]] = {}     # user_id -> {reminder_id -> reminder}


def _get_user_id(request: Request) -> str:
    return request.headers.get("x-user-id", "default")


def _get_anthropic_key(request: Request) -> Optional[str]:
    return (
        request.headers.get("x-anthropic-api-key")
        or os.getenv("ANTHROPIC_API_KEY")
    )


async def _call_claude(api_key: str, system: str, user_content, model: str = "claude-sonnet-4-6", max_tokens: int = 4096) -> Optional[str]:
    """Make a single Claude API call and return the text response."""
    try:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=api_key)

        # user_content can be a string or list (for multimodal)
        messages = [{"role": "user", "content": user_content}]

        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=0.2,
            system=system,
            messages=messages,
        )

        text_parts = [b.text for b in response.content if hasattr(b, "text") and b.type == "text"]
        return "\n".join(text_parts)
    except Exception as e:
        logger.error("Claude API call failed: %s", e)
        return None


# ══════════════════════════════════════════════════════════════════════
# Food-Drug Interaction Database (30+ entries)
# ══════════════════════════════════════════════════════════════════════

FOOD_INTERACTION_DB: dict[str, list[dict]] = {
    "warfarin": [
        {"food": "Vitamin K-rich foods (kale, spinach, broccoli)", "severity": "major",
         "description": "Vitamin K counteracts warfarin's anticoagulant effect, reducing INR and increasing clot risk.",
         "recommendation": "Maintain consistent daily vitamin K intake. Do not suddenly increase or decrease leafy green consumption."},
        {"food": "Cranberry juice", "severity": "moderate",
         "description": "Cranberry may inhibit CYP2C9, increasing warfarin levels and bleeding risk.",
         "recommendation": "Limit cranberry juice to small amounts. Monitor INR if consuming regularly."},
        {"food": "Alcohol", "severity": "major",
         "description": "Acute alcohol intake increases warfarin effect; chronic heavy use decreases it. Both patterns destabilize INR.",
         "recommendation": "Avoid alcohol or limit to 1 drink/day. Avoid binge drinking entirely."},
        {"food": "Green tea", "severity": "moderate",
         "description": "Green tea contains vitamin K which can reduce warfarin effectiveness.",
         "recommendation": "Moderate consumption. Keep intake consistent day to day."},
    ],
    "simvastatin": [
        {"food": "Grapefruit / grapefruit juice", "severity": "major",
         "description": "Grapefruit inhibits intestinal CYP3A4, dramatically increasing statin blood levels and risk of rhabdomyolysis.",
         "recommendation": "Avoid grapefruit and grapefruit juice entirely while taking simvastatin."},
    ],
    "atorvastatin": [
        {"food": "Grapefruit / grapefruit juice", "severity": "moderate",
         "description": "Grapefruit increases atorvastatin exposure via CYP3A4 inhibition, though less than with simvastatin.",
         "recommendation": "Limit grapefruit to small occasional amounts. Report muscle pain promptly."},
    ],
    "lovastatin": [
        {"food": "Grapefruit / grapefruit juice", "severity": "major",
         "description": "Lovastatin is highly susceptible to CYP3A4 inhibition by grapefruit, greatly increasing toxicity risk.",
         "recommendation": "Avoid grapefruit entirely."},
    ],
    "metformin": [
        {"food": "Alcohol", "severity": "major",
         "description": "Alcohol increases the risk of lactic acidosis with metformin and impairs hepatic gluconeogenesis.",
         "recommendation": "Limit alcohol to moderate intake. Never binge drink. Monitor blood glucose closely."},
    ],
    "metronidazole": [
        {"food": "Alcohol", "severity": "major",
         "description": "Disulfiram-like reaction: severe nausea, vomiting, flushing, headache, tachycardia, abdominal cramps.",
         "recommendation": "Avoid ALL alcohol during treatment and for 48-72 hours after completing the course."},
    ],
    "tetracycline": [
        {"food": "Dairy products (milk, cheese, yogurt)", "severity": "major",
         "description": "Calcium in dairy chelates tetracycline, reducing absorption by up to 65%.",
         "recommendation": "Take tetracycline 1 hour before or 2 hours after dairy products."},
        {"food": "Iron-fortified foods / supplements", "severity": "moderate",
         "description": "Iron forms insoluble complexes with tetracycline, reducing absorption.",
         "recommendation": "Separate tetracycline and iron by at least 2-3 hours."},
    ],
    "doxycycline": [
        {"food": "Dairy products", "severity": "moderate",
         "description": "Calcium in dairy can reduce doxycycline absorption, though less than with tetracycline.",
         "recommendation": "Separate from dairy by 1-2 hours for optimal absorption."},
    ],
    "ciprofloxacin": [
        {"food": "Dairy products", "severity": "moderate",
         "description": "Calcium chelates ciprofloxacin, reducing absorption by up to 40%.",
         "recommendation": "Take ciprofloxacin 2 hours before or 6 hours after dairy."},
        {"food": "Calcium-fortified juice", "severity": "moderate",
         "description": "Fortified juices contain enough calcium to significantly reduce fluoroquinolone absorption.",
         "recommendation": "Avoid calcium-fortified beverages near dosing time."},
    ],
    "levothyroxine": [
        {"food": "Soy products", "severity": "moderate",
         "description": "Soy can decrease levothyroxine absorption and may require dose adjustment.",
         "recommendation": "If consuming soy regularly, maintain consistent intake and have TSH monitored."},
        {"food": "High-fiber foods", "severity": "moderate",
         "description": "Dietary fiber can bind levothyroxine and reduce absorption.",
         "recommendation": "Take levothyroxine on an empty stomach, 30-60 minutes before breakfast."},
        {"food": "Coffee", "severity": "mild",
         "description": "Coffee can reduce levothyroxine absorption if taken simultaneously.",
         "recommendation": "Wait at least 30 minutes after taking levothyroxine before drinking coffee."},
        {"food": "Calcium-rich foods", "severity": "moderate",
         "description": "Calcium impairs levothyroxine absorption by forming insoluble complexes.",
         "recommendation": "Separate from calcium-rich foods and supplements by at least 4 hours."},
    ],
    "phenelzine": [
        {"food": "Tyramine-rich foods (aged cheese, cured meats, fermented foods, soy sauce, tap beer)", "severity": "major",
         "description": "MAOIs prevent tyramine breakdown, causing hypertensive crisis: severe headache, rapid heart rate, potential stroke.",
         "recommendation": "STRICTLY avoid all tyramine-rich foods. Follow MAOI dietary restrictions carefully."},
    ],
    "tranylcypromine": [
        {"food": "Tyramine-rich foods (aged cheese, cured meats, fermented foods, soy sauce, tap beer)", "severity": "major",
         "description": "Same tyramine-MAOI interaction — risk of hypertensive crisis.",
         "recommendation": "STRICTLY avoid all tyramine-rich foods. Carry emergency information."},
    ],
    "isocarboxazid": [
        {"food": "Tyramine-rich foods", "severity": "major",
         "description": "MAO inhibition causes dangerous tyramine accumulation — hypertensive emergency.",
         "recommendation": "STRICTLY avoid tyramine-rich foods throughout treatment and for 2 weeks after stopping."},
    ],
    "lithium": [
        {"food": "Caffeine", "severity": "moderate",
         "description": "Caffeine increases renal lithium clearance, potentially lowering therapeutic levels.",
         "recommendation": "Maintain consistent caffeine intake. Sudden changes can alter lithium levels."},
        {"food": "Salt / sodium", "severity": "moderate",
         "description": "Low sodium intake increases lithium retention and toxicity risk; high sodium increases excretion.",
         "recommendation": "Maintain a consistent salt intake. Stay well hydrated. Avoid sudden dietary changes."},
    ],
    "digoxin": [
        {"food": "High-fiber foods", "severity": "moderate",
         "description": "Dietary fiber can reduce digoxin absorption.",
         "recommendation": "Take digoxin separately from high-fiber meals. Maintain consistent fiber intake."},
        {"food": "St. John's Wort", "severity": "major",
         "description": "St. John's Wort induces P-glycoprotein, substantially reducing digoxin levels.",
         "recommendation": "Avoid St. John's Wort entirely while taking digoxin."},
    ],
    "theophylline": [
        {"food": "Caffeine", "severity": "moderate",
         "description": "Both caffeine and theophylline are xanthine derivatives. Caffeine can increase theophylline side effects.",
         "recommendation": "Limit caffeine intake. Monitor for increased jitteriness, palpitations, or insomnia."},
        {"food": "Charcoal-broiled foods", "severity": "moderate",
         "description": "Polycyclic aromatic hydrocarbons in charcoal-grilled food induce CYP1A2, decreasing theophylline levels.",
         "recommendation": "Be aware that heavy intake of grilled/smoked foods may reduce drug effectiveness."},
    ],
    "spironolactone": [
        {"food": "Potassium-rich foods (bananas, oranges, potatoes, salt substitutes)", "severity": "moderate",
         "description": "Spironolactone is potassium-sparing; excess potassium intake can cause dangerous hyperkalemia.",
         "recommendation": "Avoid potassium supplements and salt substitutes. Moderate potassium-rich food intake."},
    ],
    "lisinopril": [
        {"food": "Potassium-rich foods / salt substitutes", "severity": "moderate",
         "description": "ACE inhibitors reduce potassium excretion. Excess potassium intake raises hyperkalemia risk.",
         "recommendation": "Avoid potassium-based salt substitutes. Moderate high-potassium food intake."},
    ],
    "alendronate": [
        {"food": "Any food (especially calcium and dairy)", "severity": "major",
         "description": "Food dramatically reduces alendronate absorption — bioavailability drops to near zero.",
         "recommendation": "Take on empty stomach with plain water, at least 30 minutes before any food or drink."},
    ],
    "isoniazid": [
        {"food": "Tyramine-rich foods", "severity": "moderate",
         "description": "Isoniazid has mild MAO inhibitory activity; tyramine-rich foods may cause headache and hypertension.",
         "recommendation": "Avoid large amounts of aged cheese, fermented foods, and cured meats."},
        {"food": "Alcohol", "severity": "major",
         "description": "Both isoniazid and alcohol are hepatotoxic. Combination greatly increases liver damage risk.",
         "recommendation": "Avoid alcohol entirely during isoniazid therapy."},
    ],
    "fluconazole": [
        {"food": "Caffeine", "severity": "mild",
         "description": "Fluconazole inhibits CYP1A2, which can increase caffeine levels and cause jitteriness.",
         "recommendation": "Reduce caffeine intake if experiencing palpitations or insomnia."},
    ],
    "cyclosporine": [
        {"food": "Grapefruit / grapefruit juice", "severity": "major",
         "description": "Grapefruit inhibits CYP3A4 and P-glycoprotein, significantly increasing cyclosporine levels and nephrotoxicity.",
         "recommendation": "Avoid grapefruit entirely. Use consistent diet to maintain stable drug levels."},
        {"food": "St. John's Wort", "severity": "major",
         "description": "St. John's Wort induces CYP3A4, dramatically reducing cyclosporine levels and risking organ rejection.",
         "recommendation": "Absolutely avoid St. John's Wort."},
    ],
    "felodipine": [
        {"food": "Grapefruit / grapefruit juice", "severity": "major",
         "description": "Grapefruit can increase felodipine levels by up to 300%, causing severe hypotension.",
         "recommendation": "Avoid grapefruit entirely."},
    ],
    "sildenafil": [
        {"food": "Grapefruit / grapefruit juice", "severity": "moderate",
         "description": "Grapefruit may increase sildenafil levels via CYP3A4 inhibition.",
         "recommendation": "Avoid grapefruit. High-fat meals also delay absorption."},
    ],
    "clopidogrel": [
        {"food": "Grapefruit / grapefruit juice", "severity": "moderate",
         "description": "Grapefruit may inhibit CYP2C19 activation of clopidogrel, reducing its antiplatelet effect.",
         "recommendation": "Avoid grapefruit to ensure full drug activation."},
    ],
    "sertraline": [
        {"food": "Alcohol", "severity": "moderate",
         "description": "Alcohol enhances CNS depressant effects of SSRIs, worsening drowsiness and impairing judgment.",
         "recommendation": "Avoid or strictly limit alcohol while taking sertraline."},
        {"food": "St. John's Wort", "severity": "major",
         "description": "Combined serotonergic activity can precipitate serotonin syndrome.",
         "recommendation": "Do NOT combine SSRIs with St. John's Wort."},
    ],
    "fluoxetine": [
        {"food": "Alcohol", "severity": "moderate",
         "description": "Alcohol worsens CNS depression and may impair antidepressant efficacy.",
         "recommendation": "Avoid alcohol."},
        {"food": "St. John's Wort", "severity": "major",
         "description": "Risk of serotonin syndrome from combined serotonergic activity.",
         "recommendation": "Do NOT take St. John's Wort with fluoxetine."},
    ],
    "prednisone": [
        {"food": "Alcohol", "severity": "moderate",
         "description": "Both prednisone and alcohol irritate the stomach lining, increasing ulcer and GI bleeding risk.",
         "recommendation": "Avoid or limit alcohol. Take prednisone with food."},
    ],
    "potassium_chloride": [
        {"food": "Salt substitutes", "severity": "major",
         "description": "Salt substitutes contain potassium; combined with supplements may cause hyperkalemia.",
         "recommendation": "Avoid potassium-based salt substitutes while taking potassium supplements."},
    ],
    "iron_supplements": [
        {"food": "Coffee / tea", "severity": "moderate",
         "description": "Tannins and polyphenols in coffee and tea reduce iron absorption by up to 60%.",
         "recommendation": "Separate iron supplements from coffee/tea by at least 1-2 hours. Take with vitamin C to enhance absorption."},
        {"food": "Dairy products", "severity": "moderate",
         "description": "Calcium in dairy competes with iron for absorption.",
         "recommendation": "Take iron supplements separately from dairy, ideally on an empty stomach."},
    ],
}


# ══════════════════════════════════════════════════════════════════════
# Common Medication Name Database (for autocomplete/search)
# ══════════════════════════════════════════════════════════════════════

MEDICATION_NAMES = [
    "Acetaminophen", "Adderall", "Alendronate", "Allopurinol", "Alprazolam",
    "Amitriptyline", "Amlodipine", "Amoxicillin", "Aspirin", "Atenolol",
    "Atorvastatin", "Azithromycin", "Benazepril", "Bupropion", "Buspirone",
    "Carvedilol", "Cefdinir", "Cephalexin", "Cetirizine", "Ciprofloxacin",
    "Citalopram", "Clindamycin", "Clobetasol", "Clonazepam", "Clopidogrel",
    "Cyclobenzaprine", "Cyclosporine", "Diazepam", "Diclofenac", "Digoxin",
    "Diltiazem", "Donepezil", "Doxycycline", "Duloxetine", "Enalapril",
    "Escitalopram", "Esomeprazole", "Famotidine", "Felodipine", "Fenofibrate",
    "Ferrous Sulfate", "Finasteride", "Fluconazole", "Fluoxetine", "Fluticasone",
    "Furosemide", "Gabapentin", "Glimepiride", "Glipizide", "Hydrochlorothiazide",
    "Hydrocodone", "Hydroxychloroquine", "Ibuprofen", "Indomethacin", "Insulin",
    "Irbesartan", "Iron Supplements", "Isoniazid", "Ketoconazole", "Ketorolac",
    "Lamotrigine", "Lansoprazole", "Levofloxacin", "Levothyroxine", "Lisinopril",
    "Lithium", "Loratadine", "Lorazepam", "Losartan", "Lovastatin",
    "Meloxicam", "Memantine", "Metformin", "Methotrexate", "Methylphenidate",
    "Metoprolol", "Metronidazole", "Montelukast", "Naproxen", "Nifedipine",
    "Nitrofurantoin", "Omeprazole", "Ondansetron", "Oxycodone", "Pantoprazole",
    "Paroxetine", "Penicillin", "Phenelzine", "Pioglitazone", "Potassium Chloride",
    "Pravastatin", "Prednisone", "Pregabalin", "Propranolol", "Quetiapine",
    "Ramipril", "Ranitidine", "Risperidone", "Rosuvastatin", "Sertraline",
    "Sildenafil", "Simvastatin", "Sitagliptin", "Spironolactone", "Sumatriptan",
    "Tamsulosin", "Telmisartan", "Tetracycline", "Theophylline", "Topiramate",
    "Tramadol", "Tranylcypromine", "Trazodone", "Trimethoprim", "Valacyclovir",
    "Valsartan", "Venlafaxine", "Verapamil", "Warfarin", "Zolpidem",
]


# ══════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════

# ── CRUD: Medications ─────────────────────────────────────────────────

@medication_router.get("/")
async def list_medications(request: Request):
    """List all medications for the current user."""
    user_id = _get_user_id(request)
    meds = _medications.get(user_id, {})
    return {"medications": list(meds.values()), "count": len(meds)}


@medication_router.post("/", status_code=201)
async def add_medication(request: Request, med: MedicationCreate):
    """Add a new medication."""
    user_id = _get_user_id(request)
    if user_id not in _medications:
        _medications[user_id] = {}

    med_id = str(uuid.uuid4())
    record = {
        "id": med_id,
        **med.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _medications[user_id][med_id] = record
    return record


@medication_router.put("/{med_id}")
async def update_medication(request: Request, med_id: str, med: MedicationUpdate):
    """Update an existing medication."""
    user_id = _get_user_id(request)
    user_meds = _medications.get(user_id, {})
    if med_id not in user_meds:
        raise HTTPException(status_code=404, detail="Medication not found")

    updates = med.model_dump(exclude_unset=True)
    user_meds[med_id].update(updates)
    user_meds[med_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    return user_meds[med_id]


@medication_router.delete("/{med_id}")
async def delete_medication(request: Request, med_id: str):
    """Delete a medication."""
    user_id = _get_user_id(request)
    user_meds = _medications.get(user_id, {})
    if med_id not in user_meds:
        raise HTTPException(status_code=404, detail="Medication not found")

    deleted = user_meds.pop(med_id)
    return {"deleted": True, "medication": deleted}


# ── Drug-Drug Interaction Check ───────────────────────────────────────

@medication_router.post("/interactions/check")
async def check_interactions(request: Request, body: InteractionCheckRequest):
    """Check drug-drug interactions using the local DrugInteractionAgent database,
    plus allergy and contraindication checks if provided."""
    agent = get_drug_interaction_agent()

    result = agent.check_interactions(body.medications)

    # Allergy check
    if body.allergies:
        allergy_result = agent.check_allergies(body.medications, body.allergies)
        result["allergy_check"] = allergy_result

    # Contraindication check (check each med against all conditions)
    if body.conditions:
        contra_results = []
        for med in body.medications:
            contra = agent.get_contraindications(med, body.conditions)
            if contra["total_contraindications"] > 0:
                contra_results.append(contra)
        result["contraindication_check"] = {
            "total_contraindicated": len(contra_results),
            "details": contra_results,
        }

    # If no interactions found locally and Claude is available, try Claude fallback
    api_key = _get_anthropic_key(request)
    if result["total_interactions"] == 0 and len(body.medications) >= 2 and api_key:
        med_list = ", ".join(body.medications)
        claude_text = await _call_claude(
            api_key,
            system=(
                "You are a clinical pharmacist. Check the following medications for drug-drug interactions. "
                "Return a JSON object with: interactions (array of {drug_a, drug_b, severity, description, recommendation}), "
                "total_interactions (int), safe (bool). Only include clinically significant interactions."
            ),
            user_content=f"Check interactions between: {med_list}",
            max_tokens=2048,
        )
        if claude_text:
            try:
                # Try to parse the JSON from Claude's response
                text = claude_text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                claude_data = json.loads(text)
                result["claude_analysis"] = claude_data
            except (json.JSONDecodeError, Exception):
                result["claude_analysis"] = {"raw": claude_text}

    return result


# ── Food/Lifestyle Interactions ───────────────────────────────────────

@medication_router.post("/food-interactions")
async def get_food_interactions(request: Request, body: FoodInteractionRequest):
    """Get food and lifestyle interactions for medications.
    Uses local FOOD_INTERACTION_DB first, with Claude enrichment if available."""
    results: dict[str, list[dict]] = {}
    missing: list[str] = []

    for med_name in body.medications:
        key = med_name.strip().lower().replace("-", " ").replace("_", " ")
        # Try direct lookup and normalized variants
        found = FOOD_INTERACTION_DB.get(key)
        if not found:
            # Try matching with underscores
            key_underscore = key.replace(" ", "_")
            found = FOOD_INTERACTION_DB.get(key_underscore)
        if found:
            results[med_name] = found
        else:
            missing.append(med_name)

    # Use Claude for medications not in local DB
    api_key = _get_anthropic_key(request)
    if missing and api_key:
        med_list = ", ".join(missing)
        claude_text = await _call_claude(
            api_key,
            system=(
                "You are a clinical pharmacist specializing in food-drug interactions. "
                "For each medication, list known food and lifestyle interactions. "
                "Return a JSON object where keys are medication names and values are arrays of "
                "{food, severity (major/moderate/mild), description, recommendation}. "
                "Only include clinically relevant interactions."
            ),
            user_content=f"List food and lifestyle interactions for: {med_list}",
            max_tokens=3000,
        )
        if claude_text:
            try:
                text = claude_text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                claude_data = json.loads(text)
                for med_name in missing:
                    if med_name in claude_data:
                        results[med_name] = claude_data[med_name]
                    elif med_name.lower() in claude_data:
                        results[med_name] = claude_data[med_name.lower()]
            except (json.JSONDecodeError, Exception) as e:
                logger.warning("Failed to parse Claude food interaction response: %s", e)
    elif missing and not api_key:
        # Return fallback for missing meds
        for med_name in missing:
            results[med_name] = [
                {"food": "General advice", "severity": "info",
                 "description": f"No specific food interactions found for {med_name} in local database.",
                 "recommendation": "Take as directed by your prescriber. Ask your pharmacist about food interactions."}
            ]

    return {
        "food_interactions": results,
        "medications_checked": body.medications,
        "source": "local_db" if not missing else ("local_db+claude" if api_key else "local_db+fallback"),
    }


# ── Medication Guide ──────────────────────────────────────────────────

@medication_router.get("/{med_id}/guide")
async def get_medication_guide(request: Request, med_id: str):
    """Get a patient-friendly medication guide. Uses drug_interaction_agent's local guide DB."""
    user_id = _get_user_id(request)
    user_meds = _medications.get(user_id, {})

    # If med_id matches a stored medication, use its name; otherwise treat med_id as a name
    if med_id in user_meds:
        med_name = user_meds[med_id]["name"]
    else:
        med_name = med_id

    agent = get_drug_interaction_agent()
    guide = agent.generate_medication_guide(med_name)

    # If not found locally and Claude is available, generate one
    if not guide.get("found"):
        api_key = _get_anthropic_key(request)
        if api_key:
            claude_text = await _call_claude(
                api_key,
                system=(
                    "You are a patient education pharmacist. Generate a comprehensive, patient-friendly "
                    "medication guide. Return a JSON object with: generic_name, brand_names (array), drug_class, "
                    "purpose, how_it_works, common_dosage, side_effects ({common: [], serious: []}), "
                    "warnings (array), food_interactions (array). Use simple language."
                ),
                user_content=f"Generate a medication guide for: {med_name}",
                max_tokens=2048,
            )
            if claude_text:
                try:
                    text = claude_text.strip()
                    if text.startswith("```"):
                        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                    guide = json.loads(text)
                    guide["found"] = True
                    guide["source"] = "claude"
                    guide["generated_at"] = datetime.now(timezone.utc).isoformat()
                except (json.JSONDecodeError, Exception):
                    guide["claude_raw"] = claude_text

    return guide


# ── Prescription Scan (Claude Vision) ─────────────────────────────────

@medication_router.post("/prescription/scan")
async def scan_prescription(request: Request, body: PrescriptionScanRequest):
    """Parse a prescription image using Claude Vision."""
    api_key = _get_anthropic_key(request)
    if not api_key:
        return {
            "parsed": False,
            "error": "No API key available for prescription scanning.",
            "fallback": {
                "message": "Prescription scanning requires an Anthropic API key. Please add your medications manually.",
            },
        }

    user_content = [
        {"type": "text", "text": (
            "Analyze this prescription image. Extract all medication information. "
            "Return a JSON object with: medications (array of {name, dosage, frequency, quantity, refills, prescriber, notes}), "
            "patient_name (if visible), date (if visible), pharmacy (if visible). "
            "If the image is not a valid prescription, set is_prescription: false and explain why."
        )},
        {"type": "image", "source": {
            "type": "base64",
            "media_type": body.media_type,
            "data": body.image_base64,
        }},
    ]

    claude_text = await _call_claude(
        api_key,
        system="You are an expert at reading and parsing medical prescriptions. Return structured JSON only.",
        user_content=user_content,
        max_tokens=2048,
    )

    if not claude_text:
        return {"parsed": False, "error": "Failed to analyze prescription image."}

    try:
        text = claude_text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        parsed = json.loads(text)
        parsed["parsed"] = True
        return parsed
    except (json.JSONDecodeError, Exception):
        return {"parsed": False, "raw_analysis": claude_text}


# ── Adherence Logging ─────────────────────────────────────────────────

@medication_router.post("/adherence/log")
async def log_adherence(request: Request, log: AdherenceLog):
    """Log a medication taken/skipped/late event."""
    user_id = _get_user_id(request)
    if user_id not in _adherence:
        _adherence[user_id] = []

    entry = {
        "id": str(uuid.uuid4()),
        **log.model_dump(),
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }
    _adherence[user_id].append(entry)
    return entry


@medication_router.get("/adherence/history")
async def get_adherence_history(
    request: Request,
    medication_id: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=365),
):
    """Get adherence history, optionally filtered by medication and time range."""
    user_id = _get_user_id(request)
    logs = _adherence.get(user_id, [])

    # Filter by medication_id if provided
    if medication_id:
        logs = [l for l in logs if l.get("medication_id") == medication_id]

    # Filter by date range
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    logs = [l for l in logs if l.get("logged_at", "") >= cutoff]

    # Compute stats
    total = len(logs)
    taken = sum(1 for l in logs if l.get("status") == "taken")
    skipped = sum(1 for l in logs if l.get("status") == "skipped")
    late = sum(1 for l in logs if l.get("status") == "late")
    adherence_rate = (taken / total * 100) if total > 0 else 0.0

    return {
        "logs": logs,
        "stats": {
            "total": total,
            "taken": taken,
            "skipped": skipped,
            "late": late,
            "adherence_rate": round(adherence_rate, 1),
        },
        "period_days": days,
    }


# ── Side Effects ──────────────────────────────────────────────────────

@medication_router.post("/side-effects", status_code=201)
async def report_side_effect(request: Request, report: SideEffectReport):
    """Report a side effect."""
    user_id = _get_user_id(request)
    if user_id not in _side_effects:
        _side_effects[user_id] = []

    entry = {
        "id": str(uuid.uuid4()),
        **report.model_dump(),
        "reported_at": datetime.now(timezone.utc).isoformat(),
    }
    _side_effects[user_id].append(entry)
    return entry


@medication_router.get("/side-effects")
async def list_side_effects(
    request: Request,
    medication_id: Optional[str] = Query(None),
):
    """List reported side effects, optionally filtered by medication."""
    user_id = _get_user_id(request)
    effects = _side_effects.get(user_id, [])

    if medication_id:
        effects = [e for e in effects if e.get("medication_id") == medication_id]

    return {"side_effects": effects, "count": len(effects)}


@medication_router.post("/side-effects/analyze")
async def analyze_side_effects(request: Request, body: SideEffectAnalysisRequest):
    """Use Claude to analyze reported side effects for patterns and recommendations."""
    user_id = _get_user_id(request)
    effects = _side_effects.get(user_id, [])

    if not effects:
        return {
            "analysis": "No side effects have been reported yet.",
            "recommendations": [],
            "patterns": [],
        }

    # Filter by medication names if provided
    if body.medication_names:
        names_lower = {n.lower() for n in body.medication_names}
        effects = [e for e in effects if e.get("medication_name", "").lower() in names_lower]

    api_key = _get_anthropic_key(request)
    if not api_key:
        # Provide basic local analysis
        severity_counts = {}
        symptom_counts = {}
        for e in effects:
            sev = e.get("severity", "unknown")
            sym = e.get("symptom", "unknown")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            symptom_counts[sym] = symptom_counts.get(sym, 0) + 1

        most_common = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        return {
            "analysis": "Basic analysis (no API key for AI-powered analysis).",
            "total_reports": len(effects),
            "severity_breakdown": severity_counts,
            "most_common_symptoms": [{"symptom": s, "count": c} for s, c in most_common],
            "recommendations": [
                "Discuss reported side effects with your healthcare provider.",
                "Severe side effects should be reported immediately.",
            ],
            "patterns": [],
        }

    effects_summary = json.dumps(effects, indent=2)
    claude_text = await _call_claude(
        api_key,
        system=(
            "You are a clinical pharmacist analyzing a patient's reported medication side effects. "
            "Identify patterns, potential causes, and provide actionable recommendations. "
            "Return a JSON object with: analysis (string summary), patterns (array of {pattern, medications_involved, concern_level}), "
            "recommendations (array of strings), requires_medical_attention (bool), "
            "possible_alternatives (array of {current_medication, suggestion, reason})."
        ),
        user_content=f"Analyze these reported side effects:\n{effects_summary}",
        max_tokens=3000,
    )

    if claude_text:
        try:
            text = claude_text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)
        except (json.JSONDecodeError, Exception):
            return {"analysis": claude_text, "patterns": [], "recommendations": []}

    return {"analysis": "Analysis unavailable.", "patterns": [], "recommendations": []}


# ── Schedule Generation ───────────────────────────────────────────────

@medication_router.get("/schedule")
async def get_schedule(request: Request):
    """Generate a daily medication schedule from the user's active medications."""
    user_id = _get_user_id(request)
    meds = _medications.get(user_id, {})

    active_meds = [m for m in meds.values() if m.get("active", True)]
    if not active_meds:
        return {"schedule": {}, "medications": [], "message": "No active medications found."}

    # Group medications by time of day
    schedule: dict[str, list[dict]] = {}
    unscheduled: list[dict] = []

    for med in active_meds:
        times = med.get("time_of_day", [])
        if not times:
            unscheduled.append({
                "medication_id": med["id"],
                "name": med["name"],
                "dosage": med.get("dosage", ""),
                "frequency": med.get("frequency", ""),
            })
            continue

        for t in times:
            time_key = t.strip().lower()
            # Normalize common time labels
            if time_key in ("am", "morning"):
                time_key = "morning"
            elif time_key in ("noon", "midday", "afternoon"):
                time_key = "afternoon"
            elif time_key in ("pm", "evening"):
                time_key = "evening"
            elif time_key in ("night", "bedtime"):
                time_key = "bedtime"

            if time_key not in schedule:
                schedule[time_key] = []
            schedule[time_key].append({
                "medication_id": med["id"],
                "name": med["name"],
                "dosage": med.get("dosage", ""),
                "frequency": med.get("frequency", ""),
                "notes": med.get("notes", ""),
            })

    # Sort schedule by typical time ordering
    time_order = ["morning", "afternoon", "evening", "bedtime"]
    sorted_schedule = {}
    for t in time_order:
        if t in schedule:
            sorted_schedule[t] = schedule[t]
    # Add any custom times not in the standard list
    for t, meds_list in schedule.items():
        if t not in sorted_schedule:
            sorted_schedule[t] = meds_list

    return {
        "schedule": sorted_schedule,
        "unscheduled": unscheduled,
        "total_active": len(active_meds),
    }


# ── Reminders ─────────────────────────────────────────────────────────

@medication_router.post("/reminders", status_code=201)
async def create_reminder(request: Request, reminder: ReminderCreate):
    """Create a medication reminder."""
    user_id = _get_user_id(request)
    if user_id not in _reminders:
        _reminders[user_id] = {}

    reminder_id = str(uuid.uuid4())
    record = {
        "id": reminder_id,
        **reminder.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _reminders[user_id][reminder_id] = record
    return record


@medication_router.get("/reminders")
async def list_reminders(request: Request):
    """List all reminders for the current user."""
    user_id = _get_user_id(request)
    reminders = _reminders.get(user_id, {})
    return {"reminders": list(reminders.values()), "count": len(reminders)}


@medication_router.delete("/reminders/{reminder_id}")
async def delete_reminder(request: Request, reminder_id: str):
    """Delete a reminder."""
    user_id = _get_user_id(request)
    user_reminders = _reminders.get(user_id, {})
    if reminder_id not in user_reminders:
        raise HTTPException(status_code=404, detail="Reminder not found")

    deleted = user_reminders.pop(reminder_id)
    return {"deleted": True, "reminder": deleted}


# ── Pill Identification (Claude Vision) ───────────────────────────────

@medication_router.post("/identify")
async def identify_pill(request: Request, body: PillIdentifyRequest):
    """Identify a pill from an image using Claude Vision."""
    api_key = _get_anthropic_key(request)
    if not api_key:
        return {
            "identified": False,
            "error": "No API key available for pill identification.",
            "fallback": {
                "message": "Pill identification requires an Anthropic API key. You can use the FDA Pill Identifier at https://www.drugs.com/pill_identification.html",
                "suggestion": "Describe the pill's color, shape, and imprint to search manually.",
            },
        }

    desc = f"\nAdditional description: {body.description}" if body.description else ""
    user_content = [
        {"type": "text", "text": (
            f"Identify this pill/medication from the image.{desc} "
            "Return a JSON object with: identified (bool), confidence (high/medium/low), "
            "possible_matches (array of {name, generic_name, strength, manufacturer, description}), "
            "pill_characteristics ({color, shape, imprint, size, scoring}), "
            "warnings (array of strings). If you cannot identify it, explain why."
        )},
        {"type": "image", "source": {
            "type": "base64",
            "media_type": body.media_type,
            "data": body.image_base64,
        }},
    ]

    claude_text = await _call_claude(
        api_key,
        system="You are a pharmaceutical expert skilled at pill identification. Return structured JSON only.",
        user_content=user_content,
        max_tokens=2048,
    )

    if not claude_text:
        return {"identified": False, "error": "Failed to analyze pill image."}

    try:
        text = claude_text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, Exception):
        return {"identified": False, "raw_analysis": claude_text}


# ── Medication Search / Autocomplete ──────────────────────────────────

@medication_router.get("/search")
async def search_medications(q: str = Query("", min_length=1)):
    """Search medication names for autocomplete."""
    query = q.strip().lower()
    matches = [name for name in MEDICATION_NAMES if query in name.lower()]
    # Sort: exact prefix matches first, then contains matches
    prefix_matches = [m for m in matches if m.lower().startswith(query)]
    other_matches = [m for m in matches if not m.lower().startswith(query)]
    return {
        "results": (prefix_matches + other_matches)[:20],
        "query": q,
        "total": len(matches),
    }


# ── Refill Tracking ──────────────────────────────────────────────────

@medication_router.get("/refills/upcoming")
async def get_upcoming_refills(
    request: Request,
    days_ahead: int = Query(30, ge=1, le=180),
):
    """Get medications that need refills within the specified timeframe."""
    user_id = _get_user_id(request)
    meds = _medications.get(user_id, {})

    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=days_ahead)
    upcoming: list[dict] = []

    for med in meds.values():
        if not med.get("active", True):
            continue

        refill_date_str = med.get("refill_date", "")
        pills_remaining = med.get("pills_remaining")

        needs_refill = False
        reason = ""

        # Check refill date
        if refill_date_str:
            try:
                refill_date = datetime.fromisoformat(refill_date_str.replace("Z", "+00:00"))
                if refill_date <= cutoff:
                    needs_refill = True
                    days_until = (refill_date - now).days
                    reason = f"Refill date is in {max(days_until, 0)} days"
                    if days_until < 0:
                        reason = f"Refill was due {abs(days_until)} days ago"
            except (ValueError, TypeError):
                pass

        # Check pills remaining
        if pills_remaining is not None and pills_remaining <= 7:
            needs_refill = True
            reason = f"Only {pills_remaining} pills remaining"
            if pills_remaining == 0:
                reason = "No pills remaining"

        if needs_refill:
            upcoming.append({
                "medication_id": med["id"],
                "name": med["name"],
                "dosage": med.get("dosage", ""),
                "refill_date": refill_date_str,
                "pills_remaining": pills_remaining,
                "reason": reason,
                "urgency": "high" if (pills_remaining is not None and pills_remaining <= 3) else "normal",
            })

    # Sort by urgency (high first) then by pills remaining
    upcoming.sort(key=lambda x: (0 if x["urgency"] == "high" else 1, x.get("pills_remaining") or 999))

    return {
        "upcoming_refills": upcoming,
        "count": len(upcoming),
        "days_ahead": days_ahead,
    }
