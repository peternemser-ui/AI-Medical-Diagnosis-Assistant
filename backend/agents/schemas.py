"""
Pydantic output schemas for each agent in the diagnostic pipeline.

These schemas define the expected structured output from each agent.
Used by the orchestrator to validate and fill defaults for agent outputs.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Optional


class FlexibleModel(BaseModel):
    """Base model that tolerates extra fields from LLM outputs."""
    model_config = ConfigDict(extra="ignore", coerce_numbers_to_str=False)


class TriageOutput(FlexibleModel):
    esi_level: int = Field(ge=1, le=5, default=3, description="Emergency Severity Index 1-5")
    urgency: str = "routine"  # emergency, urgent, semi_urgent, routine
    urgency_level: str = "routine"  # alias used by existing pipeline
    domain: str = "general_medicine"
    red_flags: Any = []  # list of str or dicts with body_system/finding
    symptom_domains: list[str] = []
    requires_life_saving_intervention: bool = False
    reasoning: str = ""


class DiagnosisEntry(FlexibleModel):
    condition: str = "Unknown"
    confidence: float = Field(ge=0, le=100, default=50)
    reasoning: str = ""
    urgency: str = "routine"
    specialty: str = "general"
    recommended_specialty: str = ""
    supporting_features: list[str] = []
    opposing_features: list[str] = []
    must_not_miss: Any = False
    illness_script_fit: str = ""


class DiagnosticianOutput(FlexibleModel):
    problem_representation: str = ""
    differential_diagnosis: list[DiagnosisEntry] = []
    must_not_miss: Any = []
    recommended_tests: Any = []
    follow_up_questions: Any = []
    anchoring_bias_check: Any = ""


class ResearchOutput(FlexibleModel):
    evidence_summary: str = ""
    clinical_guidelines: list[dict] = []
    drug_interactions: list[str] = []
    prevalence_data: dict = {}
    key_references: list[str] = []


class SpecialistOutput(FlexibleModel):
    specialist_assessment: str = ""
    diagnostic_criteria_applied: list[dict] = []
    risk_scores: dict = {}
    additional_diagnoses: list[DiagnosisEntry] = []
    specialist_recommendations: list[str] = []
    specialty_specific_tests: list[str] = []
    diagnostic_criteria: list[str] = []
    severity_assessment: str = ""


class TreatmentPlan(FlexibleModel):
    condition: str = ""
    approach: str = ""
    medications: list[dict] = []
    lifestyle: list[str] = []
    follow_up: str = ""


class TreatmentOutput(FlexibleModel):
    treatment_plans: list[TreatmentPlan] = []
    immediate_actions: list[str] = []
    medication_schedule: list[dict] = []
    warning_signs: list[str] = []
    follow_up_timeline: str = ""
    lifestyle_recommendations: list[str] = []
    medications: list[dict] = []


class SafetyOutput(FlexibleModel):
    safety_status: str = "SAFE"  # SAFE, CAUTION, ALERT
    warnings: list[str] = []
    contraindications: list[dict] = []
    dosage_concerns: list[str] = []
    interaction_risks: list[str] = []
    recommendations: list[str] = []
    safety_summary: str = ""


class EmpathyOutput(FlexibleModel):
    patient_summary: str = ""
    action_checklist: list[str] = []
    when_to_seek_care: list[str] = []
    reassurance: str = ""
    plain_language_explanation: str = ""
    emotional_support: str = ""
    when_to_seek_help: list[str] = []
