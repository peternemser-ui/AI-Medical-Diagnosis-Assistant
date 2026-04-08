"""Insurance Pre-Auth Agent — ICD-10 mapping, pre-authorization, cost estimation, and coverage analysis."""

import random
import uuid
from datetime import datetime, timezone, timedelta


# ICD-10 mapping database: condition name -> list of (code, description)
ICD10_DB = {
    "hypertension": [("I10", "Essential (primary) hypertension")],
    "type 2 diabetes": [("E11.9", "Type 2 diabetes mellitus without complications"), ("E11.65", "Type 2 diabetes mellitus with hyperglycemia")],
    "type 1 diabetes": [("E10.9", "Type 1 diabetes mellitus without complications")],
    "asthma": [("J45.909", "Unspecified asthma, uncomplicated"), ("J45.20", "Mild intermittent asthma, uncomplicated")],
    "migraine": [("G43.909", "Migraine, unspecified, not intractable, without status migrainosus")],
    "depression": [("F32.9", "Major depressive disorder, single episode, unspecified"), ("F33.0", "Major depressive disorder, recurrent, mild")],
    "anxiety": [("F41.1", "Generalized anxiety disorder"), ("F41.9", "Anxiety disorder, unspecified")],
    "pneumonia": [("J18.9", "Pneumonia, unspecified organism"), ("J15.9", "Unspecified bacterial pneumonia")],
    "urinary tract infection": [("N39.0", "Urinary tract infection, site not specified")],
    "chest pain": [("R07.9", "Chest pain, unspecified"), ("I20.9", "Angina pectoris, unspecified")],
    "back pain": [("M54.5", "Low back pain"), ("M54.9", "Dorsalgia, unspecified")],
    "copd": [("J44.1", "Chronic obstructive pulmonary disease with acute exacerbation"), ("J44.9", "Chronic obstructive pulmonary disease, unspecified")],
    "heart failure": [("I50.9", "Heart failure, unspecified"), ("I50.22", "Chronic systolic (congestive) heart failure")],
    "atrial fibrillation": [("I48.91", "Unspecified atrial fibrillation"), ("I48.0", "Paroxysmal atrial fibrillation")],
    "hypothyroidism": [("E03.9", "Hypothyroidism, unspecified")],
    "hyperthyroidism": [("E05.90", "Thyrotoxicosis, unspecified without thyrotoxic crisis")],
    "iron deficiency anemia": [("D50.9", "Iron deficiency anemia, unspecified")],
    "gerd": [("K21.0", "Gastro-esophageal reflux disease with esophagitis"), ("K21.9", "Gastro-esophageal reflux disease without esophagitis")],
    "osteoarthritis": [("M19.90", "Unspecified osteoarthritis, unspecified site")],
    "rheumatoid arthritis": [("M06.9", "Rheumatoid arthritis, unspecified")],
    "stroke": [("I63.9", "Cerebral infarction, unspecified"), ("I61.9", "Nontraumatic intracerebral hemorrhage, unspecified")],
    "deep vein thrombosis": [("I82.409", "Acute embolism and thrombosis of unspecified deep veins of lower extremity")],
    "pulmonary embolism": [("I26.99", "Other pulmonary embolism without acute cor pulmonale")],
    "skin infection": [("L08.9", "Local infection of the skin and subcutaneous tissue, unspecified")],
    "allergic rhinitis": [("J30.9", "Allergic rhinitis, unspecified")],
    "sinusitis": [("J32.9", "Chronic sinusitis, unspecified")],
    "bronchitis": [("J20.9", "Acute bronchitis, unspecified"), ("J42", "Unspecified chronic bronchitis")],
    "kidney disease": [("N18.9", "Chronic kidney disease, unspecified"), ("N18.3", "Chronic kidney disease, stage 3")],
    "epilepsy": [("G40.909", "Epilepsy, unspecified, not intractable, without status epilepticus")],
    "celiac disease": [("K90.0", "Celiac disease")],
    "crohn disease": [("K50.90", "Crohn's disease, unspecified, without complications")],
    "ulcerative colitis": [("K51.90", "Ulcerative colitis, unspecified, without complications")],
    "obesity": [("E66.9", "Obesity, unspecified"), ("E66.01", "Morbid (severe) obesity due to excess calories")],
}

# Insurance tier definitions
INSURANCE_TIERS = {
    "medicare": {
        "name": "Medicare",
        "copay_primary": 20,
        "copay_specialist": 40,
        "deductible": 226,
        "coinsurance_pct": 20,
        "out_of_pocket_max": 7550,
        "preauth_threshold": "moderate",
        "covered_services": ["primary care", "specialist", "lab work", "imaging", "emergency", "hospitalization", "preventive"],
    },
    "medicaid": {
        "name": "Medicaid",
        "copay_primary": 0,
        "copay_specialist": 0,
        "deductible": 0,
        "coinsurance_pct": 0,
        "out_of_pocket_max": 0,
        "preauth_threshold": "low",
        "covered_services": ["primary care", "specialist", "lab work", "imaging", "emergency", "hospitalization", "preventive", "behavioral health"],
    },
    "ppo": {
        "name": "PPO (Preferred Provider Organization)",
        "copay_primary": 30,
        "copay_specialist": 50,
        "deductible": 500,
        "coinsurance_pct": 20,
        "out_of_pocket_max": 8000,
        "preauth_threshold": "moderate",
        "covered_services": ["primary care", "specialist", "lab work", "imaging", "emergency", "hospitalization", "preventive"],
    },
    "hmo": {
        "name": "HMO (Health Maintenance Organization)",
        "copay_primary": 20,
        "copay_specialist": 40,
        "deductible": 250,
        "coinsurance_pct": 15,
        "out_of_pocket_max": 6500,
        "preauth_threshold": "high",
        "covered_services": ["primary care", "specialist", "lab work", "imaging", "emergency", "hospitalization", "preventive"],
    },
    "high_deductible": {
        "name": "High-Deductible Health Plan (HDHP)",
        "copay_primary": 0,
        "copay_specialist": 0,
        "deductible": 3000,
        "coinsurance_pct": 20,
        "out_of_pocket_max": 7050,
        "preauth_threshold": "moderate",
        "covered_services": ["primary care", "specialist", "lab work", "imaging", "emergency", "hospitalization", "preventive"],
    },
}

# Procedure cost estimates
PROCEDURE_COSTS = {
    "office visit - primary": {"base_cost": 150, "category": "primary care"},
    "office visit - specialist": {"base_cost": 300, "category": "specialist"},
    "complete blood count": {"base_cost": 40, "category": "lab work"},
    "comprehensive metabolic panel": {"base_cost": 55, "category": "lab work"},
    "lipid panel": {"base_cost": 45, "category": "lab work"},
    "thyroid panel": {"base_cost": 75, "category": "lab work"},
    "urinalysis": {"base_cost": 30, "category": "lab work"},
    "chest x-ray": {"base_cost": 250, "category": "imaging"},
    "ct scan": {"base_cost": 1200, "category": "imaging"},
    "mri": {"base_cost": 2000, "category": "imaging"},
    "ultrasound": {"base_cost": 400, "category": "imaging"},
    "echocardiogram": {"base_cost": 800, "category": "imaging"},
    "ekg": {"base_cost": 150, "category": "lab work"},
    "colonoscopy": {"base_cost": 3000, "category": "specialist"},
    "endoscopy": {"base_cost": 2500, "category": "specialist"},
    "physical therapy session": {"base_cost": 150, "category": "specialist"},
    "emergency room visit": {"base_cost": 2000, "category": "emergency"},
    "hospitalization per day": {"base_cost": 3500, "category": "hospitalization"},
}

# Procedures that commonly require pre-authorization
PREAUTH_REQUIRED = {
    "mri", "ct scan", "colonoscopy", "endoscopy", "hospitalization per day",
    "physical therapy session", "echocardiogram",
}


class InsurancePreAuthAgent:
    """Manages ICD-10 mapping, pre-authorization, cost estimation, and coverage analysis."""

    def __init__(self):
        self._preauth_requests: list[dict] = []
        self._seed_metrics()

    def _seed_metrics(self):
        """Seed mock pre-auth metrics."""
        now = datetime.now(timezone.utc)
        statuses = ["approved", "approved", "approved", "denied", "pending"]
        for i in range(25):
            days_ago = random.randint(0, 60)
            self._preauth_requests.append({
                "request_id": f"PA-{uuid.uuid4().hex[:8].upper()}",
                "status": random.choice(statuses),
                "submitted_at": (now - timedelta(days=days_ago)).isoformat(),
                "processing_days": random.randint(1, 14),
                "insurance_type": random.choice(list(INSURANCE_TIERS.keys())),
                "procedure": random.choice(list(PREAUTH_REQUIRED)),
            })

    def map_to_icd10(self, diagnosis: str) -> dict:
        """Map a diagnosis name to ICD-10 code(s)."""
        key = diagnosis.strip().lower()
        # Try exact match first
        if key in ICD10_DB:
            codes = ICD10_DB[key]
            return {
                "diagnosis": diagnosis,
                "found": True,
                "codes": [{"code": c[0], "description": c[1]} for c in codes],
                "primary_code": codes[0][0],
            }

        # Try partial match
        matches = []
        for db_key, codes in ICD10_DB.items():
            if key in db_key or db_key in key:
                matches.append({
                    "diagnosis_match": db_key,
                    "codes": [{"code": c[0], "description": c[1]} for c in codes],
                })

        if matches:
            primary = matches[0]["codes"][0]
            return {
                "diagnosis": diagnosis,
                "found": True,
                "partial_match": True,
                "matches": matches,
                "primary_code": primary["code"],
                "codes": matches[0]["codes"],
            }

        return {
            "diagnosis": diagnosis,
            "found": False,
            "codes": [],
            "message": f"No ICD-10 mapping found for '{diagnosis}'. Manual coding may be required.",
        }

    def check_preauth_required(self, icd10_code: str, procedure: str, insurance_type: str) -> dict:
        """Determine whether pre-authorization is required."""
        proc_key = procedure.strip().lower()
        ins_key = insurance_type.strip().lower().replace("-", "_").replace(" ", "_")

        tier = INSURANCE_TIERS.get(ins_key)
        if not tier:
            return {"error": f"Unknown insurance type: {insurance_type}. Valid types: {', '.join(INSURANCE_TIERS.keys())}"}

        requires_preauth = proc_key in PREAUTH_REQUIRED

        # HMO requires preauth for more procedures
        if ins_key == "hmo" and proc_key in {"office visit - specialist", "echocardiogram", "ekg"}:
            requires_preauth = True

        return {
            "icd10_code": icd10_code,
            "procedure": procedure,
            "insurance_type": ins_key,
            "insurance_name": tier["name"],
            "requires_preauth": requires_preauth,
            "estimated_processing_days": random.randint(3, 10) if requires_preauth else 0,
            "notes": "Pre-authorization required. Submit clinical documentation." if requires_preauth else "No pre-authorization needed for this procedure.",
        }

    def generate_preauth_letter(self, patient_info: dict, diagnosis: str, procedures: list[str]) -> dict:
        """Generate a pre-authorization request letter."""
        icd_result = self.map_to_icd10(diagnosis)
        icd_code = icd_result.get("primary_code", "UNSPECIFIED")
        request_id = f"PA-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        letter = f"""PRE-AUTHORIZATION REQUEST
{'='*50}

Request ID: {request_id}
Date: {now.strftime('%B %d, %Y')}

PATIENT INFORMATION
{'─'*30}
Name: {patient_info.get('name', 'N/A')}
Date of Birth: {patient_info.get('dob', 'N/A')}
Member ID: {patient_info.get('member_id', 'N/A')}
Insurance: {patient_info.get('insurance_type', 'N/A')}

CLINICAL INFORMATION
{'─'*30}
Primary Diagnosis: {diagnosis}
ICD-10 Code: {icd_code}

Requested Procedures:
{chr(10).join(f"  {i+1}. {p}" for i, p in enumerate(procedures))}

CLINICAL JUSTIFICATION
{'─'*30}
The above procedures are medically necessary for the evaluation and
management of the patient's {diagnosis}. Clinical examination and
preliminary workup support the need for the requested services.

Standard treatment protocols indicate that the requested procedures
are the appropriate next step in the diagnostic and therapeutic pathway
for this condition.

REQUESTING PROVIDER
{'─'*30}
Provider: {patient_info.get('provider_name', 'AI Medical Diagnosis System')}
NPI: {patient_info.get('provider_npi', '1234567890')}
Facility: {patient_info.get('facility', 'AI Medical Diagnosis Clinic')}

{'='*50}
This is an automatically generated pre-authorization request.
"""

        self._preauth_requests.append({
            "request_id": request_id,
            "status": "pending",
            "submitted_at": now.isoformat(),
            "processing_days": 0,
            "insurance_type": patient_info.get("insurance_type", "ppo"),
            "procedure": procedures[0] if procedures else "unspecified",
        })

        return {
            "request_id": request_id,
            "letter": letter,
            "diagnosis": diagnosis,
            "icd10_code": icd_code,
            "procedures": procedures,
            "status": "submitted",
            "submitted_at": now.isoformat(),
            "estimated_response_days": random.randint(3, 10),
        }

    def estimate_costs(self, procedures: list[str], insurance_type: str) -> dict:
        """Estimate patient out-of-pocket costs for a list of procedures."""
        ins_key = insurance_type.strip().lower().replace("-", "_").replace(" ", "_")
        tier = INSURANCE_TIERS.get(ins_key)
        if not tier:
            return {"error": f"Unknown insurance type: {insurance_type}. Valid types: {', '.join(INSURANCE_TIERS.keys())}"}

        line_items = []
        total_billed = 0
        total_patient = 0

        for proc in procedures:
            proc_key = proc.strip().lower()
            cost_info = PROCEDURE_COSTS.get(proc_key)

            if cost_info:
                base = cost_info["base_cost"]
                category = cost_info["category"]
            else:
                base = 200  # default estimate
                category = "other"

            # Calculate patient responsibility
            if tier["deductible"] > 0 and total_billed < tier["deductible"]:
                # Patient pays full cost up to deductible
                remaining_deductible = tier["deductible"] - total_billed
                deductible_portion = min(base, remaining_deductible)
                coinsurance_portion = (base - deductible_portion) * (tier["coinsurance_pct"] / 100)
                patient_cost = deductible_portion + coinsurance_portion
            else:
                patient_cost = base * (tier["coinsurance_pct"] / 100)

            # Apply copay for office visits
            if "office visit" in proc_key:
                if "specialist" in proc_key:
                    patient_cost = tier["copay_specialist"]
                else:
                    patient_cost = tier["copay_primary"]

            patient_cost = round(min(patient_cost, base), 2)
            insurance_pays = round(base - patient_cost, 2)

            line_items.append({
                "procedure": proc,
                "category": category,
                "billed_amount": base,
                "insurance_pays": insurance_pays,
                "patient_responsibility": patient_cost,
            })

            total_billed += base
            total_patient += patient_cost

        # Cap at out-of-pocket max
        if tier["out_of_pocket_max"] > 0:
            total_patient = min(total_patient, tier["out_of_pocket_max"])

        return {
            "insurance_type": ins_key,
            "insurance_name": tier["name"],
            "deductible": tier["deductible"],
            "coinsurance_pct": tier["coinsurance_pct"],
            "out_of_pocket_max": tier["out_of_pocket_max"],
            "line_items": line_items,
            "total_billed": round(total_billed, 2),
            "total_insurance_pays": round(total_billed - total_patient, 2),
            "total_patient_responsibility": round(total_patient, 2),
            "disclaimer": "These are estimates only. Actual costs may vary based on your specific plan and provider network.",
        }

    def get_coverage_summary(self, insurance_type: str, icd10_codes: list[str]) -> dict:
        """Get coverage details for an insurance type and set of diagnosis codes."""
        ins_key = insurance_type.strip().lower().replace("-", "_").replace(" ", "_")
        tier = INSURANCE_TIERS.get(ins_key)
        if not tier:
            return {"error": f"Unknown insurance type: {insurance_type}. Valid types: {', '.join(INSURANCE_TIERS.keys())}"}

        covered_codes = []
        for code in icd10_codes:
            covered_codes.append({
                "code": code,
                "covered": True,
                "notes": "Standard coverage applies under medical necessity.",
            })

        return {
            "insurance_type": ins_key,
            "insurance_name": tier["name"],
            "plan_details": {
                "copay_primary_care": tier["copay_primary"],
                "copay_specialist": tier["copay_specialist"],
                "annual_deductible": tier["deductible"],
                "coinsurance": f"{tier['coinsurance_pct']}%",
                "out_of_pocket_maximum": tier["out_of_pocket_max"],
            },
            "covered_services": tier["covered_services"],
            "diagnosis_coverage": covered_codes,
            "preauth_policy": f"Pre-authorization threshold: {tier['preauth_threshold']}",
        }

    def get_preauth_metrics(self) -> dict:
        """Return pre-authorization performance metrics."""
        total = len(self._preauth_requests)
        if total == 0:
            return {"total_requests": 0, "message": "No pre-authorization data available."}

        approved = sum(1 for r in self._preauth_requests if r["status"] == "approved")
        denied = sum(1 for r in self._preauth_requests if r["status"] == "denied")
        pending = sum(1 for r in self._preauth_requests if r["status"] == "pending")
        avg_processing = sum(r["processing_days"] for r in self._preauth_requests) / total

        # Common denial reasons (mock)
        denial_reasons = [
            {"reason": "Insufficient clinical documentation", "count": max(1, denied // 2)},
            {"reason": "Alternative treatment not attempted", "count": max(1, denied // 3)},
            {"reason": "Service not covered under plan", "count": max(1, denied // 4)},
        ]

        # By insurance type
        by_insurance = {}
        for r in self._preauth_requests:
            ins = r["insurance_type"]
            if ins not in by_insurance:
                by_insurance[ins] = {"total": 0, "approved": 0, "denied": 0, "pending": 0}
            by_insurance[ins]["total"] += 1
            by_insurance[ins][r["status"]] = by_insurance[ins].get(r["status"], 0) + 1

        return {
            "total_requests": total,
            "approval_rate": round((approved / total) * 100, 1) if total > 0 else 0,
            "denial_rate": round((denied / total) * 100, 1) if total > 0 else 0,
            "pending_count": pending,
            "avg_processing_days": round(avg_processing, 1),
            "status_breakdown": {
                "approved": approved,
                "denied": denied,
                "pending": pending,
            },
            "common_denial_reasons": denial_reasons,
            "by_insurance_type": by_insurance,
            "recent_requests": sorted(self._preauth_requests, key=lambda x: x["submitted_at"], reverse=True)[:10],
        }


# Singleton
_insurance_agent = None


def get_insurance_agent() -> InsurancePreAuthAgent:
    global _insurance_agent
    if _insurance_agent is None:
        _insurance_agent = InsurancePreAuthAgent()
    return _insurance_agent
