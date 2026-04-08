"""EHR/FHIR Integration Agent — converts diagnosis data to FHIR R4 resources and manages EHR syncs."""

import random
import uuid
from datetime import datetime, timezone, timedelta


class EHRIntegrationAgent:
    """Converts diagnosis output to FHIR resources and manages EHR system connections."""

    # FHIR R4 resource templates
    FHIR_CONDITION_TEMPLATE = {
        "resourceType": "Condition",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Condition"]},
        "clinicalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}],
        },
        "verificationStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "provisional"}],
        },
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "encounter-diagnosis", "display": "Encounter Diagnosis"}],
        }],
    }

    FHIR_PATIENT_TEMPLATE = {
        "resourceType": "Patient",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Patient"]},
        "active": True,
    }

    FHIR_OBSERVATION_TEMPLATE = {
        "resourceType": "Observation",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Observation"]},
        "status": "final",
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs", "display": "Vital Signs"}],
        }],
    }

    # Common SNOMED CT codes for demo
    SNOMED_CODES = {
        "hypertension": {"code": "38341003", "display": "Hypertensive disorder"},
        "diabetes": {"code": "73211009", "display": "Diabetes mellitus"},
        "migraine": {"code": "37796009", "display": "Migraine"},
        "asthma": {"code": "195967001", "display": "Asthma"},
        "anxiety": {"code": "197480006", "display": "Anxiety disorder"},
        "pneumonia": {"code": "233604007", "display": "Pneumonia"},
        "uti": {"code": "68566005", "display": "Urinary tract infection"},
        "gerd": {"code": "235595009", "display": "Gastroesophageal reflux disease"},
    }

    # LOINC codes for observations
    LOINC_CODES = {
        "heart_rate": {"code": "8867-4", "display": "Heart rate", "unit": "beats/min"},
        "blood_pressure_systolic": {"code": "8480-6", "display": "Systolic blood pressure", "unit": "mmHg"},
        "blood_pressure_diastolic": {"code": "8462-4", "display": "Diastolic blood pressure", "unit": "mmHg"},
        "temperature": {"code": "8310-5", "display": "Body temperature", "unit": "degC"},
        "respiratory_rate": {"code": "9279-1", "display": "Respiratory rate", "unit": "breaths/min"},
        "oxygen_saturation": {"code": "2708-6", "display": "Oxygen saturation", "unit": "%"},
        "bmi": {"code": "39156-5", "display": "Body mass index", "unit": "kg/m2"},
    }

    def __init__(self):
        self._connected_systems: list[dict] = []
        self._sync_history: list[dict] = []
        self._fhir_resources_created: int = 0
        self._sync_errors: int = 0
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 3 connected EHR systems, 200 FHIR resources, 5 sync errors."""
        now = datetime.now(timezone.utc)

        self._connected_systems = [
            {
                "id": "ehr-001",
                "name": "Epic",
                "vendor": "Epic Systems",
                "fhir_version": "R4",
                "base_url": "https://epic.example.com/fhir/r4",
                "status": "connected",
                "last_sync": (now - timedelta(minutes=15)).isoformat(),
                "patients_synced": 1245,
                "resources_exchanged": 8430,
                "error_count": 2,
                "avg_latency_ms": 180,
                "connected_since": (now - timedelta(days=300)).isoformat(),
                "capabilities": ["Patient", "Condition", "Observation", "MedicationRequest", "AllergyIntolerance"],
            },
            {
                "id": "ehr-002",
                "name": "Cerner",
                "vendor": "Oracle Health",
                "fhir_version": "R4",
                "base_url": "https://cerner.example.com/fhir/r4",
                "status": "connected",
                "last_sync": (now - timedelta(hours=2)).isoformat(),
                "patients_synced": 872,
                "resources_exchanged": 5210,
                "error_count": 1,
                "avg_latency_ms": 240,
                "connected_since": (now - timedelta(days=180)).isoformat(),
                "capabilities": ["Patient", "Condition", "Observation", "Encounter", "DiagnosticReport"],
            },
            {
                "id": "ehr-003",
                "name": "Athenahealth",
                "vendor": "Athenahealth",
                "fhir_version": "R4",
                "base_url": "https://athena.example.com/fhir/r4",
                "status": "disconnected",
                "last_sync": (now - timedelta(days=3)).isoformat(),
                "patients_synced": 340,
                "resources_exchanged": 1890,
                "error_count": 2,
                "avg_latency_ms": 310,
                "connected_since": (now - timedelta(days=90)).isoformat(),
                "capabilities": ["Patient", "Condition", "Observation"],
            },
        ]

        self._fhir_resources_created = 200
        self._sync_errors = 5

        # Seed sync history
        statuses = ["success", "success", "success", "success", "success",
                     "success", "success", "success", "partial", "failed"]
        ehr_names = ["Epic", "Cerner", "Athenahealth"]
        for i in range(25):
            ts = now - timedelta(hours=random.randint(0, 168))
            status = random.choice(statuses)
            ehr = random.choice(ehr_names)
            self._sync_history.append({
                "id": f"sync-{uuid.uuid4().hex[:8]}",
                "patient_id": f"patient-{random.randint(1000, 9999)}",
                "ehr_system": ehr,
                "direction": random.choice(["push", "pull"]),
                "status": status,
                "resources_synced": random.randint(1, 15) if status != "failed" else 0,
                "errors": [] if status == "success" else [
                    {"code": "TIMEOUT", "message": "Connection timed out"} if status == "failed"
                    else {"code": "PARTIAL", "message": "Some resources skipped due to validation errors"}
                ],
                "duration_ms": random.randint(200, 5000),
                "started_at": ts.isoformat(),
                "completed_at": (ts + timedelta(seconds=random.randint(1, 10))).isoformat(),
            })

        self._sync_history.sort(key=lambda x: x["started_at"], reverse=True)

    def diagnosis_to_fhir(self, diagnosis_result: dict) -> dict:
        """Convert diagnosis output to a FHIR Condition resource."""
        resource_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        condition_name = diagnosis_result.get("primary_condition", "Unknown condition")
        condition_lower = condition_name.lower()

        # Try to find a SNOMED code
        snomed = None
        for key, code_data in self.SNOMED_CODES.items():
            if key in condition_lower:
                snomed = code_data
                break

        code_block = {
            "coding": [],
            "text": condition_name,
        }
        if snomed:
            code_block["coding"].append({
                "system": "http://snomed.info/sct",
                "code": snomed["code"],
                "display": snomed["display"],
            })
        else:
            code_block["coding"].append({
                "system": "http://snomed.info/sct",
                "code": "unknown",
                "display": condition_name,
            })

        severity_map = {
            "low": {"code": "255604002", "display": "Mild"},
            "medium": {"code": "6736007", "display": "Moderate"},
            "high": {"code": "24484000", "display": "Severe"},
            "critical": {"code": "442452003", "display": "Life threatening severity"},
        }
        urgency = diagnosis_result.get("urgency", "medium")
        severity = severity_map.get(urgency, severity_map["medium"])

        resource = {
            **self.FHIR_CONDITION_TEMPLATE,
            "id": resource_id,
            "code": code_block,
            "severity": {
                "coding": [{"system": "http://snomed.info/sct", **severity}],
            },
            "subject": {
                "reference": f"Patient/{diagnosis_result.get('patient_id', 'unknown')}",
            },
            "onsetDateTime": now,
            "recordedDate": now,
            "note": [{"text": diagnosis_result.get("summary", "")}],
            "evidence": [
                {"detail": [{"display": cause}]}
                for cause in diagnosis_result.get("causes", [])[:5]
            ],
        }

        self._fhir_resources_created += 1
        return {"fhir_resource": resource, "resource_type": "Condition", "id": resource_id}

    def patient_to_fhir(self, patient_data: dict) -> dict:
        """Convert patient data to a FHIR Patient resource."""
        resource_id = str(uuid.uuid4())

        gender_map = {"male": "male", "female": "female", "m": "male", "f": "female"}
        gender = gender_map.get(patient_data.get("gender", "").lower(), "unknown")

        resource = {
            **self.FHIR_PATIENT_TEMPLATE,
            "id": resource_id,
            "name": [{
                "use": "official",
                "family": patient_data.get("last_name", "Unknown"),
                "given": [patient_data.get("first_name", "Unknown")],
            }],
            "gender": gender,
            "birthDate": patient_data.get("birth_date", None),
            "telecom": [],
            "address": [],
        }

        if patient_data.get("email"):
            resource["telecom"].append({"system": "email", "value": patient_data["email"]})
        if patient_data.get("phone"):
            resource["telecom"].append({"system": "phone", "value": patient_data["phone"]})

        self._fhir_resources_created += 1
        return {"fhir_resource": resource, "resource_type": "Patient", "id": resource_id}

    def observation_to_fhir(self, observation_data: dict) -> dict:
        """Convert lab/vital data to a FHIR Observation resource."""
        resource_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        obs_type = observation_data.get("type", "heart_rate")
        loinc = self.LOINC_CODES.get(obs_type, self.LOINC_CODES["heart_rate"])

        resource = {
            **self.FHIR_OBSERVATION_TEMPLATE,
            "id": resource_id,
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": loinc["code"],
                    "display": loinc["display"],
                }],
                "text": loinc["display"],
            },
            "subject": {
                "reference": f"Patient/{observation_data.get('patient_id', 'unknown')}",
            },
            "effectiveDateTime": now,
            "valueQuantity": {
                "value": observation_data.get("value", 0),
                "unit": loinc["unit"],
                "system": "http://unitsofmeasure.org",
                "code": loinc["unit"],
            },
        }

        self._fhir_resources_created += 1
        return {"fhir_resource": resource, "resource_type": "Observation", "id": resource_id}

    def get_connected_systems(self) -> list:
        """Return list of connected EHR systems with status."""
        return self._connected_systems

    def sync_patient_record(self, patient_id: str, ehr_system: str) -> dict:
        """Mock sync operation for a patient record."""
        now = datetime.now(timezone.utc)
        success = random.random() < 0.92

        sync_record = {
            "id": f"sync-{uuid.uuid4().hex[:8]}",
            "patient_id": patient_id,
            "ehr_system": ehr_system,
            "direction": "push",
            "status": "success" if success else "failed",
            "resources_synced": random.randint(3, 12) if success else 0,
            "errors": [] if success else [{"code": "SYNC_ERROR", "message": f"Failed to sync with {ehr_system}"}],
            "duration_ms": random.randint(200, 3000),
            "started_at": now.isoformat(),
            "completed_at": (now + timedelta(seconds=random.randint(1, 5))).isoformat(),
        }

        self._sync_history.insert(0, sync_record)
        if not success:
            self._sync_errors += 1

        return sync_record

    def get_sync_history(self, limit: int = 20) -> list:
        """Return recent sync operations with status."""
        return self._sync_history[:limit]

    def get_fhir_metrics(self) -> dict:
        """Resources created, syncs performed, errors, latency."""
        total_syncs = len(self._sync_history)
        successful_syncs = sum(1 for s in self._sync_history if s["status"] == "success")
        failed_syncs = sum(1 for s in self._sync_history if s["status"] == "failed")
        avg_latency = (
            round(sum(s["duration_ms"] for s in self._sync_history) / total_syncs)
            if total_syncs else 0
        )

        connected = sum(1 for s in self._connected_systems if s["status"] == "connected")

        return {
            "fhir_resources_created": self._fhir_resources_created,
            "total_syncs": total_syncs,
            "successful_syncs": successful_syncs,
            "failed_syncs": failed_syncs,
            "sync_success_rate": round((successful_syncs / total_syncs) * 100, 1) if total_syncs else 0,
            "sync_errors_total": self._sync_errors,
            "avg_sync_latency_ms": avg_latency,
            "connected_systems": connected,
            "total_systems": len(self._connected_systems),
            "total_patients_synced": sum(s.get("patients_synced", 0) for s in self._connected_systems),
            "total_resources_exchanged": sum(s.get("resources_exchanged", 0) for s in self._connected_systems),
        }

    def validate_fhir_resource(self, resource: dict) -> dict:
        """Validate a FHIR JSON resource (basic structural validation)."""
        errors = []
        warnings = []

        resource_type = resource.get("resourceType")
        if not resource_type:
            errors.append({"field": "resourceType", "message": "Missing required field 'resourceType'"})
        elif resource_type not in ["Patient", "Condition", "Observation", "Encounter",
                                    "MedicationRequest", "AllergyIntolerance", "DiagnosticReport"]:
            warnings.append({"field": "resourceType", "message": f"Uncommon resource type: {resource_type}"})

        if not resource.get("id"):
            warnings.append({"field": "id", "message": "Resource has no 'id' field"})

        if resource_type == "Condition":
            if not resource.get("code"):
                errors.append({"field": "code", "message": "Condition resource must have a 'code' field"})
            if not resource.get("subject"):
                errors.append({"field": "subject", "message": "Condition resource must have a 'subject' field"})
            if not resource.get("clinicalStatus"):
                warnings.append({"field": "clinicalStatus", "message": "Condition should have 'clinicalStatus'"})

        if resource_type == "Patient":
            if not resource.get("name"):
                warnings.append({"field": "name", "message": "Patient should have at least one 'name'"})
            if not resource.get("gender"):
                warnings.append({"field": "gender", "message": "Patient should have 'gender'"})

        if resource_type == "Observation":
            if not resource.get("code"):
                errors.append({"field": "code", "message": "Observation resource must have a 'code' field"})
            if not resource.get("status"):
                errors.append({"field": "status", "message": "Observation resource must have a 'status' field"})

        valid = len(errors) == 0
        return {
            "valid": valid,
            "resource_type": resource_type,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
        }


# Singleton
_ehr_agent = None


def get_ehr_agent() -> EHRIntegrationAgent:
    global _ehr_agent
    if _ehr_agent is None:
        _ehr_agent = EHRIntegrationAgent()
    return _ehr_agent
