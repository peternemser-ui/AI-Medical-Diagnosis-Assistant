"""
Orchestrator Agent – Coordinates the entire multi-agent diagnostic pipeline.

Flow:
  1. Receive patient case from API
  2. Run Triage Agent (urgency + red flags)
  3. Run Diagnostician Agent + Research Agent IN PARALLEL (both get triage context)
  4. Run Specialist Agent (deep analysis) with diagnosis + research context
  5. Run Treatment Agent (treatment plan) with all prior context
  6. Run Safety Agent (reviews everything for patient safety)
  7. Run Empathy Agent (produces final patient-friendly summary)
  8. Synthesize all agent outputs into a unified response

Agents run in a pipeline but can also communicate laterally via the MessageBus.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from .message_bus import MessageBus
from .triage import TriageAgent
from .diagnostician import DiagnosticianAgent
from .specialist import SpecialistAgent
from .treatment import TreatmentAgent
from .research import ResearchAgent
from .safety import SafetyAgent
from .empathy import EmpathyAgent
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Top-level coordinator.  Not a Claude-powered agent itself — it's
    deterministic Python that launches the specialist agents in sequence,
    passes context between them, and assembles the final response.
    """

    def __init__(
        self,
        api_key: str,
        openai_key: str | None = None,
        google_key: str | None = None,
    ):
        self.api_key = api_key
        self.bus = MessageBus()

        # Create multi-vendor LLM client
        self.llm_client = LLMClient(
            anthropic_key=api_key,
            openai_key=openai_key,
            google_key=google_key,
        )

        # Instantiate all agents with shared bus and LLM client
        self.triage = TriageAgent(api_key, self.bus, llm_client=self.llm_client)
        self.diagnostician = DiagnosticianAgent(api_key, self.bus, llm_client=self.llm_client)
        self.specialist = SpecialistAgent(api_key, self.bus, llm_client=self.llm_client)
        self.treatment = TreatmentAgent(api_key, self.bus, llm_client=self.llm_client)
        self.research = ResearchAgent(api_key, self.bus, llm_client=self.llm_client)
        self.safety = SafetyAgent(api_key, self.bus, llm_client=self.llm_client)
        self.empathy = EmpathyAgent(api_key, self.bus, llm_client=self.llm_client)

    async def run_diagnosis(
        self,
        symptoms: str,
        age: int = 30,
        gender: str = "unknown",
        duration: str = "recent",
        severity: int = 5,
        image_base64: str | None = None,
        medical_history: str | None = None,
        current_medications: str | None = None,
        allergies: str | None = None,
        family_history: str | None = None,
        social_history: str | None = None,
        model_preference: str = "auto",
    ) -> dict[str, Any]:
        """
        Execute the full multi-agent diagnostic pipeline.

        Returns a unified response combining all agent outputs.
        """
        start = time.time()
        agent_results: dict[str, Any] = {}
        agent_timings: dict[str, float] = {}

        # Apply model preference to all agents
        if model_preference and model_preference != "auto":
            model_map = {
                # Anthropic shortcuts
                "opus": "claude-opus-4-6",
                "sonnet": "claude-sonnet-4-6",
                "haiku": "claude-haiku-4-5",
                # Full model names pass through directly
            }
            target_model = model_map.get(model_preference, model_preference)
            for agent in [self.triage, self.diagnostician, self.research,
                          self.specialist, self.treatment, self.safety, self.empathy]:
                agent.model = target_model

        # Prepare image list for visual agents (triage, diagnostician, specialist)
        images = [image_base64] if image_base64 else None

        # Build comprehensive clinical summary from all available data
        patient_summary = f"Patient: {age}-year-old {gender}\n"
        patient_summary += f"Severity: {severity}/10\n"
        patient_summary += f"Duration: {duration}\n\n"

        # Check if symptoms already contains structured clinical data (from the questionnaire)
        if any(marker in symptoms for marker in [
            "Chief Complaint:", "Onset:", "Character/Quality:", "Location/Radiation:",
            "Past Medical History:", "Current Medications:", "Allergies:"
        ]):
            # Symptoms field contains rich structured data — use it directly
            patient_summary += f"=== CLINICAL HISTORY ===\n{symptoms}\n"
        else:
            # Simple symptoms string — add it as chief complaint
            patient_summary += f"Chief complaint: {symptoms}\n"

        # Append any additional structured fields from the request
        extra_sections = []
        if medical_history:
            extra_sections.append(f"Past Medical History: {medical_history}")
        if current_medications:
            extra_sections.append(f"Current Medications: {current_medications}")
        if allergies:
            extra_sections.append(f"Allergies: {allergies}")
        if family_history:
            extra_sections.append(f"Family History: {family_history}")
        if social_history:
            extra_sections.append(f"Social/Lifestyle History: {social_history}")

        if extra_sections:
            patient_summary += "\n=== ADDITIONAL HISTORY ===\n" + "\n".join(extra_sections) + "\n"

        if image_base64:
            patient_summary += "\nNote: The patient has attached a clinical image for visual analysis."

        logger.info(f"Patient summary length: {len(patient_summary)} chars (model: {model_preference})")

        # ── Step 1: Triage ──────────────────────────────────────────
        logger.info("Step 1/7: Running Triage Agent")
        t0 = time.time()
        try:
            triage_result = await self.triage.run(
                f"Triage this patient case. You MUST respond with a JSON object containing: urgency_level (string), red_flags (array of strings), symptom_domains (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
                images=images,
            )
            agent_results["triage"] = self._extract_agent_data(triage_result)
            agent_results["triage_raw"] = triage_result["text"]
            agent_results["triage_tool_calls"] = triage_result["tool_calls"]
        except Exception as e:
            logger.error("Triage agent failed: %s", e)
            agent_results["triage"] = {"urgency_level": "routine", "red_flags": [], "error": str(e)}
        agent_timings["triage"] = round(time.time() - t0, 2)

        # ── Steps 2+3: Diagnostician + Research IN PARALLEL ─────────
        logger.info("Steps 2+3/7: Running Diagnostician + Research Agents in parallel")
        t0 = time.time()

        triage_context = {"triage_assessment": agent_results.get("triage", {})}

        diag_task = asyncio.create_task(self.diagnostician.run(
            f"Perform differential diagnosis for this patient. You MUST respond with a JSON object containing: differential_diagnosis (array of objects with condition, confidence 0-100, reasoning, urgency, specialty), recommended_tests (array of strings), follow_up_questions (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
            context=triage_context,
            images=images,
        ))
        research_task = asyncio.create_task(self.research.run(
            (
                f"Provide evidence-based medical research context for this patient case.\n"
                f"Search for relevant clinical guidelines, drug interactions, and disease prevalence.\n\n"
                f"{patient_summary}"
            ),
            context=triage_context,
        ))

        diag_result, research_result = await asyncio.gather(
            diag_task, research_task, return_exceptions=True
        )

        # Process diagnostician result
        if isinstance(diag_result, Exception):
            logger.error("Diagnostician agent failed: %s", diag_result)
            agent_results["diagnosis"] = {"differential_diagnosis": [], "error": str(diag_result)}
        else:
            agent_results["diagnosis"] = self._extract_agent_data(diag_result)
            agent_results["diagnosis_raw"] = diag_result["text"]
            agent_results["diagnosis_tool_calls"] = diag_result["tool_calls"]

        # Process research result
        if isinstance(research_result, Exception):
            logger.error("Research agent failed: %s", research_result)
            agent_results["research"] = {"evidence_summary": "Not available", "error": str(research_result)}
        else:
            agent_results["research"] = self._extract_agent_data(research_result)
            agent_results["research_raw"] = research_result["text"]
            agent_results["research_tool_calls"] = research_result["tool_calls"]

        agent_timings["diagnostician_and_research"] = round(time.time() - t0, 2)

        # ── Step 4: Specialist (with diagnosis + research context) ──
        logger.info("Step 4/7: Running Specialist Agent")
        t0 = time.time()

        # Determine which specialty to consult based on triage
        triage_data = agent_results.get("triage", {})
        domains = triage_data.get("symptom_domains", ["general medicine"])
        if isinstance(domains, list) and domains:
            specialty_focus = domains[0]
        else:
            specialty_focus = "general medicine"

        try:
            spec_result = await self.specialist.run(
                (
                    f"Provide specialist consultation for this case.\n"
                    f"Focus specialty: {specialty_focus}\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                },
                images=images,
            )
            agent_results["specialist"] = self._extract_agent_data(spec_result)
            agent_results["specialist_raw"] = spec_result["text"]
            agent_results["specialist_tool_calls"] = spec_result["tool_calls"]
        except Exception as e:
            logger.error("Specialist agent failed: %s", e)
            agent_results["specialist"] = {"specialist_assessment": "Not available", "error": str(e)}
        agent_timings["specialist"] = round(time.time() - t0, 2)

        # ── Step 5: Treatment (with all context) ────────────────────
        logger.info("Step 5/7: Running Treatment Agent")
        t0 = time.time()
        try:
            treat_result = await self.treatment.run(
                (
                    f"Create a comprehensive treatment plan for this patient.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                },
            )
            agent_results["treatment"] = self._extract_agent_data(treat_result)
            agent_results["treatment_raw"] = treat_result["text"]
            agent_results["treatment_tool_calls"] = treat_result["tool_calls"]
        except Exception as e:
            logger.error("Treatment agent failed: %s", e)
            agent_results["treatment"] = {"treatment_plans": [], "error": str(e)}
        agent_timings["treatment"] = round(time.time() - t0, 2)

        # ── Step 6: Safety (reviews everything) ─────────────────────
        logger.info("Step 6/7: Running Safety Agent")
        t0 = time.time()
        try:
            safety_result = await self.safety.run(
                (
                    f"Review ALL recommendations from the medical team for patient safety concerns.\n"
                    f"Check for contraindications, dosage safety, allergy risks, and dangerous combinations.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                },
            )
            agent_results["safety"] = self._extract_agent_data(safety_result)
            agent_results["safety_raw"] = safety_result["text"]
            agent_results["safety_tool_calls"] = safety_result["tool_calls"]
        except Exception as e:
            logger.error("Safety agent failed: %s", e)
            agent_results["safety"] = {"safety_status": "UNKNOWN", "error": str(e)}
        agent_timings["safety"] = round(time.time() - t0, 2)

        # ── Step 7: Empathy (patient-friendly summary) ──────────────
        logger.info("Step 7/7: Running Empathy Agent")
        t0 = time.time()
        try:
            empathy_result = await self.empathy.run(
                (
                    f"Create a patient-friendly summary of this medical assessment.\n"
                    f"Translate all clinical jargon into plain language.\n"
                    f"Include a clear action checklist and when to seek help.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                    "safety_review": agent_results.get("safety", {}),
                },
            )
            agent_results["empathy"] = self._extract_agent_data(empathy_result)
            agent_results["empathy_raw"] = empathy_result["text"]
            agent_results["empathy_tool_calls"] = empathy_result["tool_calls"]
        except Exception as e:
            logger.error("Empathy agent failed: %s", e)
            agent_results["empathy"] = {"patient_summary": "Summary not available.", "error": str(e)}
        agent_timings["empathy"] = round(time.time() - t0, 2)

        total_time = round(time.time() - start, 2)

        # ── Synthesize final response ───────────────────────────────
        return self._synthesize(agent_results, agent_timings, total_time, symptoms, age, gender)

    # ------------------------------------------------------------------
    # Streaming diagnosis (SSE support)
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_key_findings(agent_name: str, data: dict) -> str:
        """Extract a 1-line summary of key findings from an agent result."""
        try:
            if agent_name == "triage":
                urgency = data.get("urgency_level", "unknown")
                flags = data.get("red_flags", [])
                flag_count = len(flags) if isinstance(flags, list) else 0
                return f"{urgency.upper()}, {flag_count} red flag(s) detected"

            elif agent_name == "diagnostician":
                diff = data.get("differential_diagnosis", [])
                if diff and isinstance(diff, list) and isinstance(diff[0], dict):
                    top = diff[0].get("condition", diff[0].get("name", "Unknown"))
                    conf = diff[0].get("confidence", diff[0].get("probability", "?"))
                    return f"Top diagnosis: {top} ({conf}% confidence)"
                return "Differential diagnosis generated"

            elif agent_name == "research":
                guidelines = data.get("clinical_guidelines", [])
                gl_count = len(guidelines) if isinstance(guidelines, list) else 0
                return f"{gl_count} clinical guideline(s) referenced"

            elif agent_name == "specialist":
                specialty = data.get("specialty_consulted", data.get("focus_specialty", "General"))
                return f"Specialty consulted: {specialty}"

            elif agent_name == "treatment":
                meds = data.get("medications", [])
                med_count = len(meds) if isinstance(meds, list) else 0
                return f"{med_count} medication(s) recommended"

            elif agent_name == "safety":
                status = data.get("safety_status", "UNKNOWN")
                return f"Safety review: {status}"

            elif agent_name == "empathy":
                summary = data.get("patient_summary", "")
                length = len(summary) if isinstance(summary, str) else 0
                return f"Patient summary: {length} chars"

            return "Complete"
        except Exception:
            return "Complete"

    async def run_diagnosis_streaming(
        self,
        event_queue: "asyncio.Queue",
        symptoms: str,
        age: int = 30,
        gender: str = "unknown",
        duration: str = "recent",
        severity: int = 5,
        image_base64: str | None = None,
        medical_history: str | None = None,
        current_medications: str | None = None,
        allergies: str | None = None,
        family_history: str | None = None,
        social_history: str | None = None,
        model_preference: str = "auto",
    ) -> None:
        """
        Execute the full multi-agent diagnostic pipeline with SSE streaming.

        After each agent completes, puts an event dict onto event_queue.
        At the end, puts a 'complete' event with the full synthesized result.
        """
        start = time.time()
        agent_results: dict[str, Any] = {}
        agent_timings: dict[str, float] = {}

        # Apply model preference
        if model_preference and model_preference != "auto":
            model_map = {
                "opus": "claude-opus-4-6",
                "sonnet": "claude-sonnet-4-6",
                "haiku": "claude-haiku-4-5",
            }
            target_model = model_map.get(model_preference, model_preference)
            for agent in [self.triage, self.diagnostician, self.research,
                          self.specialist, self.treatment, self.safety, self.empathy]:
                agent.model = target_model

        images = [image_base64] if image_base64 else None

        # Build comprehensive clinical summary (same logic as run_diagnosis)
        patient_summary = f"Patient: {age}-year-old {gender}\n"
        patient_summary += f"Severity: {severity}/10\n"
        patient_summary += f"Duration: {duration}\n\n"

        if any(marker in symptoms for marker in [
            "Chief Complaint:", "Onset:", "Character/Quality:", "Location/Radiation:",
            "Past Medical History:", "Current Medications:", "Allergies:"
        ]):
            patient_summary += f"=== CLINICAL HISTORY ===\n{symptoms}\n"
        else:
            patient_summary += f"Chief complaint: {symptoms}\n"

        extra_sections = []
        if medical_history:
            extra_sections.append(f"Past Medical History: {medical_history}")
        if current_medications:
            extra_sections.append(f"Current Medications: {current_medications}")
        if allergies:
            extra_sections.append(f"Allergies: {allergies}")
        if family_history:
            extra_sections.append(f"Family History: {family_history}")
        if social_history:
            extra_sections.append(f"Social/Lifestyle History: {social_history}")

        if extra_sections:
            patient_summary += "\n=== ADDITIONAL HISTORY ===\n" + "\n".join(extra_sections) + "\n"

        if image_base64:
            patient_summary += "\nNote: The patient has attached a clinical image for visual analysis."

        logger.info(f"[stream] Patient summary length: {len(patient_summary)} chars (model: {model_preference})")

        # ── Step 1: Triage ──────────────────────────────────────────
        logger.info("[stream] Step 1/7: Running Triage Agent")
        t0 = time.time()
        try:
            triage_result = await self.triage.run(
                f"Triage this patient case. You MUST respond with a JSON object containing: urgency_level (string), red_flags (array of strings), symptom_domains (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
                images=images,
            )
            agent_results["triage"] = self._extract_agent_data(triage_result)
            agent_results["triage_raw"] = triage_result["text"]
            agent_results["triage_tool_calls"] = triage_result["tool_calls"]
        except Exception as e:
            logger.error("Triage agent failed: %s", e)
            agent_results["triage"] = {"urgency_level": "routine", "red_flags": [], "error": str(e)}
        elapsed_triage = round(time.time() - t0, 2)
        agent_timings["triage"] = elapsed_triage

        await event_queue.put({
            "event": "agent_complete",
            "agent": "triage",
            "elapsed": elapsed_triage,
            "key_findings": self._extract_key_findings("triage", agent_results["triage"]),
            "data": agent_results["triage"],
        })

        # ── Steps 2+3: Diagnostician + Research IN PARALLEL ─────────
        logger.info("[stream] Steps 2+3/7: Running Diagnostician + Research in parallel")
        t0 = time.time()

        triage_context = {"triage_assessment": agent_results.get("triage", {})}

        diag_task = asyncio.create_task(self.diagnostician.run(
            f"Perform differential diagnosis for this patient. You MUST respond with a JSON object containing: differential_diagnosis (array of objects with condition, confidence 0-100, reasoning, urgency, specialty), recommended_tests (array of strings), follow_up_questions (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
            context=triage_context,
        ))
        research_task = asyncio.create_task(self.research.run(
            (
                f"Provide evidence-based medical research context for this patient case.\n"
                f"Search for relevant clinical guidelines, drug interactions, and disease prevalence.\n\n"
                f"{patient_summary}"
            ),
            context=triage_context,
        ))

        diag_result, research_result = await asyncio.gather(
            diag_task, research_task, return_exceptions=True
        )

        parallel_elapsed = round(time.time() - t0, 2)
        agent_timings["diagnostician_and_research"] = parallel_elapsed

        # Process diagnostician result
        if isinstance(diag_result, Exception):
            logger.error("Diagnostician agent failed: %s", diag_result)
            agent_results["diagnosis"] = {"differential_diagnosis": [], "error": str(diag_result)}
        else:
            agent_results["diagnosis"] = self._extract_agent_data(diag_result)
            agent_results["diagnosis_raw"] = diag_result["text"]
            agent_results["diagnosis_tool_calls"] = diag_result["tool_calls"]

        # Process research result
        if isinstance(research_result, Exception):
            logger.error("Research agent failed: %s", research_result)
            agent_results["research"] = {"evidence_summary": "Not available", "error": str(research_result)}
        else:
            agent_results["research"] = self._extract_agent_data(research_result)
            agent_results["research_raw"] = research_result["text"]
            agent_results["research_tool_calls"] = research_result["tool_calls"]

        agent_timings["diagnostician"] = parallel_elapsed
        agent_timings["research"] = parallel_elapsed

        # Emit both parallel agents
        await event_queue.put({
            "event": "agent_complete",
            "agent": "diagnostician",
            "elapsed": parallel_elapsed,
            "key_findings": self._extract_key_findings("diagnostician", agent_results["diagnosis"]),
            "data": agent_results["diagnosis"],
        })
        await event_queue.put({
            "event": "agent_complete",
            "agent": "research",
            "elapsed": parallel_elapsed,
            "key_findings": self._extract_key_findings("research", agent_results["research"]),
            "data": agent_results["research"],
        })

        # ── Step 4: Specialist ──────────────────────────────────────
        logger.info("[stream] Step 4/7: Running Specialist Agent")
        t0 = time.time()

        triage_data = agent_results.get("triage", {})
        domains = triage_data.get("symptom_domains", ["general medicine"])
        if isinstance(domains, list) and domains:
            specialty_focus = domains[0]
        else:
            specialty_focus = "general medicine"

        try:
            spec_result = await self.specialist.run(
                (
                    f"Provide specialist consultation for this case.\n"
                    f"Focus specialty: {specialty_focus}\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                },
            )
            agent_results["specialist"] = self._extract_agent_data(spec_result)
            agent_results["specialist_raw"] = spec_result["text"]
            agent_results["specialist_tool_calls"] = spec_result["tool_calls"]
        except Exception as e:
            logger.error("Specialist agent failed: %s", e)
            agent_results["specialist"] = {"specialist_assessment": "Not available", "error": str(e)}
        elapsed_spec = round(time.time() - t0, 2)
        agent_timings["specialist"] = elapsed_spec

        await event_queue.put({
            "event": "agent_complete",
            "agent": "specialist",
            "elapsed": elapsed_spec,
            "key_findings": self._extract_key_findings("specialist", agent_results["specialist"]),
            "data": agent_results["specialist"],
        })

        # ── Step 5: Treatment ───────────────────────────────────────
        logger.info("[stream] Step 5/7: Running Treatment Agent")
        t0 = time.time()
        try:
            treat_result = await self.treatment.run(
                (
                    f"Create a comprehensive treatment plan for this patient.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                },
            )
            agent_results["treatment"] = self._extract_agent_data(treat_result)
            agent_results["treatment_raw"] = treat_result["text"]
            agent_results["treatment_tool_calls"] = treat_result["tool_calls"]
        except Exception as e:
            logger.error("Treatment agent failed: %s", e)
            agent_results["treatment"] = {"treatment_plans": [], "error": str(e)}
        elapsed_treat = round(time.time() - t0, 2)
        agent_timings["treatment"] = elapsed_treat

        await event_queue.put({
            "event": "agent_complete",
            "agent": "treatment",
            "elapsed": elapsed_treat,
            "key_findings": self._extract_key_findings("treatment", agent_results["treatment"]),
            "data": agent_results["treatment"],
        })

        # ── Step 6: Safety ──────────────────────────────────────────
        logger.info("[stream] Step 6/7: Running Safety Agent")
        t0 = time.time()
        try:
            safety_result = await self.safety.run(
                (
                    f"Review ALL recommendations from the medical team for patient safety concerns.\n"
                    f"Check for contraindications, dosage safety, allergy risks, and dangerous combinations.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                },
            )
            agent_results["safety"] = self._extract_agent_data(safety_result)
            agent_results["safety_raw"] = safety_result["text"]
            agent_results["safety_tool_calls"] = safety_result["tool_calls"]
        except Exception as e:
            logger.error("Safety agent failed: %s", e)
            agent_results["safety"] = {"safety_status": "UNKNOWN", "error": str(e)}
        elapsed_safety = round(time.time() - t0, 2)
        agent_timings["safety"] = elapsed_safety

        await event_queue.put({
            "event": "agent_complete",
            "agent": "safety",
            "elapsed": elapsed_safety,
            "key_findings": self._extract_key_findings("safety", agent_results["safety"]),
            "data": agent_results["safety"],
        })

        # ── Step 7: Empathy ─────────────────────────────────────────
        logger.info("[stream] Step 7/7: Running Empathy Agent")
        t0 = time.time()
        try:
            empathy_result = await self.empathy.run(
                (
                    f"Create a patient-friendly summary of this medical assessment.\n"
                    f"Translate all clinical jargon into plain language.\n"
                    f"Include a clear action checklist and when to seek help.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                    "safety_review": agent_results.get("safety", {}),
                },
            )
            agent_results["empathy"] = self._extract_agent_data(empathy_result)
            agent_results["empathy_raw"] = empathy_result["text"]
            agent_results["empathy_tool_calls"] = empathy_result["tool_calls"]
        except Exception as e:
            logger.error("Empathy agent failed: %s", e)
            agent_results["empathy"] = {"patient_summary": "Summary not available.", "error": str(e)}
        elapsed_empathy = round(time.time() - t0, 2)
        agent_timings["empathy"] = elapsed_empathy

        await event_queue.put({
            "event": "agent_complete",
            "agent": "empathy",
            "elapsed": elapsed_empathy,
            "key_findings": self._extract_key_findings("empathy", agent_results["empathy"]),
            "data": agent_results["empathy"],
        })

        total_time = round(time.time() - start, 2)

        # ── Synthesize final response ───────────────────────────────
        try:
            final_result = self._synthesize(agent_results, agent_timings, total_time, symptoms, age, gender)
        except Exception as e:
            logger.error("[stream] Synthesis failed: %s", e, exc_info=True)
            final_result = {
                "answer": f"Diagnosis completed but synthesis failed: {e}\n\nRaw agent outputs are available.",
                "causes": [],
                "red_flags": [],
                "recommended_tests": [],
                "agent_timings": agent_timings,
                "total_time": total_time,
                "multi_agent": True,
                "agents_used": list(agent_results.keys()),
                "error": str(e),
            }

        await event_queue.put({
            "event": "complete",
            "result": final_result,
        })

    # ------------------------------------------------------------------
    # Follow-up question handler
    # ------------------------------------------------------------------

    async def run_followup(
        self,
        question: str,
        previous_diagnosis: dict[str, Any] | None = None,
        original_symptoms: str = "",
    ) -> dict[str, Any]:
        """Handle follow-up questions using the treatment agent with full context."""
        context = {}
        if previous_diagnosis:
            context["previous_diagnosis"] = previous_diagnosis
        if original_symptoms:
            context["original_symptoms"] = original_symptoms

        result = await self.treatment.run(
            f"Patient follow-up question: {question}",
            context=context,
        )
        return {
            "answer": result["text"],
            "agent": "treatment",
            "tool_calls": result["tool_calls"],
        }

    # ------------------------------------------------------------------
    # Question generation handler
    # ------------------------------------------------------------------

    async def generate_question(
        self,
        symptoms: str,
        age: int,
        gender: str,
        conversation_history: list[str],
        previous_questions: list[str],
        questions_asked: int,
        total_ai_questions: int,
    ) -> str:
        """Generate a follow-up question using the diagnostician agent."""
        history_block = "\n".join(f"- {h}" for h in conversation_history[-5:]) if conversation_history else "None yet"
        prev_q_block = "\n".join(f"- {q}" for q in previous_questions) if previous_questions else "None yet"

        prompt = (
            f"Generate ONE specific follow-up question for this patient.\n\n"
            f"Patient: {age}-year-old {gender}\n"
            f"Chief complaint: {symptoms}\n\n"
            f"This is question {questions_asked + 1} of {total_ai_questions}.\n\n"
            f"Conversation so far:\n{history_block}\n\n"
            f"Questions already asked (DO NOT repeat):\n{prev_q_block}\n\n"
            f"Return ONLY the question text, nothing else."
        )

        result = await self.diagnostician.run(prompt)
        return result["text"].strip().strip('"')

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_agent_data(self, result: dict) -> dict:
        """Extract structured data from an agent's output.

        Tries multiple sources in priority order:
        1. publish_result tool calls (most structured)
        2. JSON in the text output
        3. Raw text fallback
        """
        # First: check tool calls for publish_result data
        tool_calls = result.get("tool_calls", [])
        published_data = {}
        for tc in tool_calls:
            if tc.get("tool") == "publish_result":
                inp = tc.get("input", {})
                data = inp.get("data", {})
                if isinstance(data, dict) and len(data) > 0:
                    published_data.update(data)

        if published_data and len(published_data) > 1:
            logger.info("Extracted %d fields from publish_result tool calls", len(published_data))
            return published_data

        # Second: try parsing JSON from text
        text = result.get("text", "")
        parsed = self._safe_parse(text)
        if "raw_text" not in parsed:
            return parsed

        # Third: merge published data with text-parsed data
        if published_data:
            return published_data

        return parsed

    def _safe_parse(self, text: str) -> dict:
        """Try to extract JSON from agent text output. Very aggressive parsing."""
        if not text or not isinstance(text, str):
            return {"raw_text": str(text) if text else ""}

        import re

        # Strategy 1: Direct JSON parse
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, TypeError):
            pass

        # Strategy 2: ```json code blocks
        match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group(1).strip())
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass

        # Strategy 3: Find the largest JSON object in the text
        # Use bracket matching to find complete JSON objects
        candidates = []
        depth = 0
        start = -1
        for i, ch in enumerate(text):
            if ch == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0 and start >= 0:
                    candidates.append(text[start:i + 1])
                    start = -1

        # Try candidates from largest to smallest
        candidates.sort(key=len, reverse=True)
        for candidate in candidates:
            try:
                result = json.loads(candidate)
                if isinstance(result, dict) and len(result) > 1:
                    return result
            except json.JSONDecodeError:
                # Try fixing common issues: trailing commas, single quotes
                fixed = candidate
                fixed = re.sub(r',\s*}', '}', fixed)
                fixed = re.sub(r',\s*]', ']', fixed)
                try:
                    result = json.loads(fixed)
                    if isinstance(result, dict):
                        return result
                except json.JSONDecodeError:
                    continue

        logger.warning("_safe_parse failed to extract JSON from %d chars of text", len(text))
        return {"raw_text": text}

    def _synthesize(
        self,
        results: dict[str, Any],
        timings: dict[str, float],
        total_time: float,
        symptoms: str,
        age: int,
        gender: str,
    ) -> dict[str, Any]:
        """Combine all agent outputs into the unified API response."""

        triage = results.get("triage", {})
        diagnosis = results.get("diagnosis", {})
        specialist = results.get("specialist", {})
        treatment = results.get("treatment", {})
        research = results.get("research", {})
        safety = results.get("safety", {})
        empathy = results.get("empathy", {})

        # Extract diagnoses in the format the frontend expects
        # Try multiple key names since agents may use different schemas
        differential = (
            diagnosis.get("differential_diagnosis")
            or diagnosis.get("diagnoses")
            or diagnosis.get("differential")
            or diagnosis.get("conditions")
            or []
        )
        causes = []
        for d in differential[:5]:
            if isinstance(d, dict):
                causes.append({
                    "cause": d.get("condition") or d.get("name") or d.get("diagnosis") or "Unknown",
                    "value": d.get("confidence") or d.get("probability") or d.get("likelihood") or 50,
                    "explanation": d.get("reasoning") or d.get("clinical_reasoning") or d.get("explanation") or d.get("rationale") or "",
                    "urgency": d.get("urgency") or d.get("priority") or "routine",
                    "specialty": d.get("specialty") or d.get("recommended_specialty") or "Primary Care",
                })
            elif isinstance(d, str):
                # Agent returned list of strings instead of dicts
                causes.append({"cause": d, "value": 50, "explanation": "", "urgency": "routine", "specialty": "Primary Care"})

        # Fallback: if causes empty but raw text exists, try to extract from text
        if not causes and diagnosis.get("raw_text"):
            logger.warning("No structured diagnoses found — extracting from raw text")
            raw = diagnosis["raw_text"]
            # Look for numbered diagnoses like "1. Condition Name" or "- Condition"
            import re
            pattern = re.findall(r'(?:^|\n)\s*(?:\d+[\.\)]\s*|[-•]\s*)([A-Z][A-Za-z\s\(\)/]+?)(?:\s*[-–:]\s*|\n)', raw)
            for i, name in enumerate(pattern[:5]):
                name = name.strip().rstrip('.-:')
                if len(name) > 3 and len(name) < 80:
                    causes.append({
                        "cause": name,
                        "value": max(20, 80 - i * 15),
                        "explanation": "Extracted from agent analysis. See full text for details.",
                        "urgency": "routine",
                        "specialty": "Primary Care",
                    })

        # Extract red flags — handle both flat strings and structured dicts
        raw_flags = triage.get("red_flags", [])
        red_flags = []
        for f in raw_flags:
            if isinstance(f, dict):
                red_flags.append(f.get("finding", f.get("description", str(f))))
            elif isinstance(f, str):
                red_flags.append(f)

        # Extract follow-up questions (try multiple key names)
        additional_questions = (
            diagnosis.get("follow_up_questions")
            or diagnosis.get("additional_questions")
            or diagnosis.get("questions")
            or []
        )

        # Extract recommended tests (try multiple key names)
        recommended_tests = (
            diagnosis.get("recommended_tests")
            or diagnosis.get("tests")
            or diagnosis.get("diagnostic_tests")
            or []
        )
        specialist_tests = (
            specialist.get("specialty_specific_tests")
            or specialist.get("recommended_tests")
            or specialist.get("tests")
            or []
        )
        if isinstance(specialist_tests, list):
            recommended_tests = list(dict.fromkeys(recommended_tests + specialist_tests))  # dedupe preserving order

        # Build the comprehensive text answer
        answer = self._build_text_answer(
            triage, diagnosis, specialist, treatment,
            research, safety, empathy,
            symptoms, age, gender, causes, red_flags,
        )

        # Confidence scores
        confidence_scores = self._calculate_confidence(causes)

        # Agent communication log
        bus_log = self.bus.get_full_log()

        # Extract structured data for frontend cards (try multiple key names)
        patient_summary = (
            empathy.get("patient_summary")
            or empathy.get("summary")
            or empathy.get("plain_language_summary")
            or ""
        )
        action_checklist = (
            empathy.get("action_checklist")
            or empathy.get("actions")
            or empathy.get("next_steps")
            or empathy.get("recommendations")
            or []
        )
        safety_status = (
            safety.get("safety_status")
            or safety.get("status")
            or safety.get("overall_status")
            or "PASS"
        )
        safety_warnings = (
            (safety.get("critical_issues") or [])
            + (safety.get("high_issues") or [])
            + (safety.get("warnings") or [])
            + (safety.get("concerns") or [])
        )
        # Flatten safety warnings
        flat_safety = []
        for w in safety_warnings:
            if isinstance(w, dict):
                flat_safety.append(w.get("issue", str(w)))
            elif isinstance(w, str):
                flat_safety.append(w)

        medications = treatment.get("medications", [])
        lifestyle = treatment.get("lifestyle_recommendations", [])
        warning_signs = treatment.get("warning_signs", [])
        follow_up = treatment.get("follow_up_timeline", "")

        return {
            "answer": answer,
            "confidence_scores": confidence_scores,
            "causes": causes,
            "red_flags": red_flags,
            "additional_questions": additional_questions,
            "recommended_tests": recommended_tests,
            # Structured treatment data
            "patient_summary": patient_summary,
            "action_checklist": action_checklist if isinstance(action_checklist, list) else [],
            "safety_status": safety_status,
            "safety_warnings": flat_safety,
            "medications": medications,
            "lifestyle_recommendations": lifestyle,
            "warning_signs": warning_signs,
            "follow_up_timeline": follow_up,
            # Agent details
            "agent_details": {
                "triage": triage,
                "diagnosis": diagnosis,
                "specialist": specialist,
                "treatment": treatment,
                "research": research,
                "safety": safety,
                "empathy": empathy,
            },
            "agent_timings": timings,
            "total_time": total_time,
            "agent_communication_log": bus_log[:20],
            "multi_agent": True,
            "agents_used": [
                "triage", "diagnostician", "research",
                "specialist", "treatment", "safety", "empathy",
            ],
            "estimated_cost": round(total_time * 0.002, 4),
        }

    def _build_text_answer(
        self,
        triage: dict,
        diagnosis: dict,
        specialist: dict,
        treatment: dict,
        research: dict,
        safety: dict,
        empathy: dict,
        symptoms: str,
        age: int,
        gender: str,
        causes: list[dict],
        red_flags: list,
    ) -> str:
        lines = []
        lines.append("AI Medical Assessment (Multi-Agent Analysis)")
        lines.append("=" * 46)
        lines.append(f"Age: {age} years | Gender: {gender}")
        preview = (symptoms[:600] + "...") if len(symptoms) > 600 else symptoms
        lines.append(f"Chief complaint: {preview}")

        # ── Patient Summary (from Empathy Agent) ── at the TOP
        patient_summary = empathy.get("patient_summary", "")
        if patient_summary:
            lines.append("")
            lines.append("PATIENT SUMMARY")
            lines.append("-" * 40)
            lines.append(patient_summary)

        what_this_means = empathy.get("what_this_means", "")
        if what_this_means:
            lines.append("")
            lines.append(f"What this means: {what_this_means}")

        action_checklist = empathy.get("action_checklist", [])
        if action_checklist:
            lines.append("")
            lines.append("YOUR ACTION CHECKLIST:")
            if isinstance(action_checklist, list):
                for i, item in enumerate(action_checklist, 1):
                    lines.append(f"  {i}. {item}")
            elif isinstance(action_checklist, str):
                lines.append(f"  {action_checklist}")

        # ── Safety Review ──
        safety_status = safety.get("safety_status", "")
        if safety_status:
            lines.append("")
            lines.append("SAFETY REVIEW")
            lines.append("-" * 40)
            lines.append(f"Status: {safety_status}")

        safety_summary = safety.get("safety_summary", "")
        if safety_summary:
            lines.append(f"  {safety_summary}")

        critical_issues = safety.get("critical_issues", [])
        if critical_issues:
            lines.append("")
            lines.append("  CRITICAL SAFETY ISSUES:")
            for issue in critical_issues:
                if isinstance(issue, dict):
                    lines.append(f"    - {issue.get('issue', issue)}")
                else:
                    lines.append(f"    - {issue}")

        high_issues = safety.get("high_issues", [])
        if high_issues:
            lines.append("")
            lines.append("  IMPORTANT SAFETY WARNINGS:")
            for issue in high_issues:
                if isinstance(issue, dict):
                    lines.append(f"    - {issue.get('issue', issue)}")
                else:
                    lines.append(f"    - {issue}")

        safety_recommendations = safety.get("recommendations", [])
        if safety_recommendations and isinstance(safety_recommendations, list):
            lines.append("")
            lines.append("  SAFETY RECOMMENDATIONS:")
            for rec in safety_recommendations[:5]:
                lines.append(f"    - {rec}")

        # ── Clinical Details ──
        lines.append("")
        lines.append("CLINICAL DETAILS")
        lines.append("=" * 46)

        # Triage
        urgency = triage.get("urgency_level", "routine")
        lines.append("")
        lines.append(f"TRIAGE: {urgency.upper()}")
        if triage.get("triage_summary"):
            lines.append(f"Summary: {triage['triage_summary']}")

        # Red flags
        if red_flags:
            lines.append("")
            lines.append("WARNING SIGNS:")
            for flag in red_flags:
                lines.append(f"  - {flag}")

        # Differential diagnosis
        if causes:
            lines.append("")
            lines.append("DIFFERENTIAL DIAGNOSIS:")
            for i, c in enumerate(causes, 1):
                lines.append(f"  {i}. {c['cause']} — Confidence: {c['value']}% — Urgency: {c['urgency']}")
                if c.get("explanation"):
                    expl = c["explanation"][:400]
                    lines.append(f"     Reasoning: {expl}")

        # Research evidence
        evidence_summary = research.get("evidence_summary", "")
        if evidence_summary:
            lines.append("")
            lines.append("RESEARCH EVIDENCE:")
            if isinstance(evidence_summary, str):
                lines.append(f"  {evidence_summary[:500]}")
            elif isinstance(evidence_summary, dict):
                for k, v in evidence_summary.items():
                    lines.append(f"  {k}: {v}")
            elif isinstance(evidence_summary, list):
                for item in evidence_summary[:5]:
                    if isinstance(item, dict):
                        lines.append(f"  - {item.get('finding', item)}")
                    else:
                        lines.append(f"  - {item}")

        clinical_guidelines = research.get("clinical_guidelines", [])
        if clinical_guidelines:
            lines.append("")
            lines.append("CLINICAL GUIDELINES:")
            if isinstance(clinical_guidelines, list):
                for gl in clinical_guidelines[:3]:
                    if isinstance(gl, dict):
                        source = gl.get("source", gl.get("guideline", ""))
                        rec = gl.get("recommendation", gl.get("summary", ""))
                        lines.append(f"  - [{source}] {rec}")
                    else:
                        lines.append(f"  - {gl}")
            elif isinstance(clinical_guidelines, str):
                lines.append(f"  {clinical_guidelines}")

        # Specialist notes
        if specialist.get("specialist_assessment"):
            lines.append("")
            lines.append("SPECIALIST CONSULTATION:")
            assessment = specialist["specialist_assessment"]
            if isinstance(assessment, str):
                lines.append(f"  {assessment[:500]}")
            elif isinstance(assessment, dict):
                for k, v in assessment.items():
                    lines.append(f"  {k}: {v}")

        if specialist.get("clinical_pearls"):
            pearls = specialist["clinical_pearls"]
            if isinstance(pearls, list):
                lines.append("")
                lines.append("CLINICAL PEARLS:")
                for pearl in pearls[:3]:
                    lines.append(f"  - {pearl}")

        # Treatment plan
        if treatment.get("immediate_actions"):
            lines.append("")
            lines.append("IMMEDIATE ACTIONS:")
            actions = treatment["immediate_actions"]
            if isinstance(actions, list):
                for a in actions:
                    lines.append(f"  - {a}")
            elif isinstance(actions, str):
                lines.append(f"  {actions}")

        if treatment.get("medications"):
            lines.append("")
            lines.append("MEDICATION GUIDANCE:")
            meds = treatment["medications"]
            if isinstance(meds, list):
                for med in meds[:5]:
                    if isinstance(med, dict):
                        name = med.get("name", med.get("medication", ""))
                        dose = med.get("dose", med.get("dosage", ""))
                        lines.append(f"  - {name}: {dose}")
                    else:
                        lines.append(f"  - {med}")

        # Medications explained (from empathy agent)
        meds_explained = empathy.get("medications_explained", "")
        if meds_explained:
            lines.append("")
            lines.append("MEDICATIONS IN PLAIN LANGUAGE:")
            if isinstance(meds_explained, str):
                lines.append(f"  {meds_explained}")
            elif isinstance(meds_explained, list):
                for me in meds_explained:
                    if isinstance(me, dict):
                        lines.append(f"  - {me.get('medication', '')}: {me.get('explanation', '')}")
                    else:
                        lines.append(f"  - {me}")

        if treatment.get("lifestyle_recommendations"):
            lines.append("")
            lines.append("LIFESTYLE RECOMMENDATIONS:")
            recs = treatment["lifestyle_recommendations"]
            if isinstance(recs, list):
                for r in recs[:4]:
                    lines.append(f"  - {r}")
            elif isinstance(recs, str):
                lines.append(f"  {recs}")

        if treatment.get("warning_signs"):
            lines.append("")
            lines.append("WHEN TO SEEK IMMEDIATE CARE:")
            signs = treatment["warning_signs"]
            if isinstance(signs, list):
                for s in signs[:5]:
                    lines.append(f"  - {s}")

        # When to get help (from empathy agent, in plain language)
        when_to_help = empathy.get("when_to_get_help", "")
        if when_to_help:
            lines.append("")
            lines.append("WHEN TO GET HELP (IN PLAIN LANGUAGE):")
            if isinstance(when_to_help, str):
                lines.append(f"  {when_to_help}")
            elif isinstance(when_to_help, list):
                for item in when_to_help:
                    lines.append(f"  - {item}")

        if treatment.get("follow_up_timeline"):
            lines.append("")
            timeline = treatment["follow_up_timeline"]
            if isinstance(timeline, str):
                lines.append(f"FOLLOW-UP: {timeline}")
            elif isinstance(timeline, dict):
                for k, v in timeline.items():
                    lines.append(f"FOLLOW-UP ({k}): {v}")

        # Recommended tests
        recommended_tests = diagnosis.get("recommended_tests", [])
        if recommended_tests:
            lines.append("")
            lines.append("RECOMMENDED TESTS:")
            for t in recommended_tests[:6]:
                lines.append(f"  - {t}")

        # Follow-up questions
        follow_up = diagnosis.get("follow_up_questions", [])
        if follow_up:
            lines.append("")
            lines.append("ADDITIONAL QUESTIONS:")
            for q in follow_up[:5]:
                lines.append(f"  - {q}")

        # Questions for doctor (from empathy agent)
        doc_questions = empathy.get("questions_for_doctor", [])
        if doc_questions and isinstance(doc_questions, list):
            lines.append("")
            lines.append("QUESTIONS TO ASK YOUR DOCTOR:")
            for q in doc_questions[:5]:
                lines.append(f"  - {q}")

        # Reassurance (from empathy agent)
        reassurance = empathy.get("reassurance", "")
        if reassurance:
            lines.append("")
            lines.append(reassurance)

        # Disclaimer
        lines.append("")
        lines.append("---")
        lines.append("DISCLAIMER: This multi-agent AI assessment is for informational purposes only.")
        lines.append("It is NOT a substitute for professional medical care.")
        lines.append("In emergencies, call local emergency services immediately.")
        lines.append("")
        lines.append("Powered by Multi-Agent Medical AI (Triage + Diagnostician + Research + Specialist + Treatment + Safety + Empathy)")

        return "\n".join(lines)

    def _calculate_confidence(self, causes: list[dict]) -> dict[str, float]:
        if not causes:
            return {"high": 0.6, "medium": 0.3, "low": 0.1}

        total = sum(c.get("value", 0) for c in causes)
        if total == 0:
            return {"high": 0.6, "medium": 0.3, "low": 0.1}

        high = medium = low = 0.0
        for c in causes:
            v = c.get("value", 0)
            w = v / total
            if v >= 70:
                high += w
            elif v >= 40:
                medium += w
            else:
                low += w

        s = high + medium + low
        if s > 0:
            high, medium, low = high / s, medium / s, low / s
        else:
            high, medium, low = 0.6, 0.3, 0.1

        return {
            "high": round(high, 2),
            "medium": round(medium, 2),
            "low": round(low, 2),
        }
