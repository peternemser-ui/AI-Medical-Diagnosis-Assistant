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
from .schemas import (
    TriageOutput, DiagnosticianOutput, ResearchOutput,
    SpecialistOutput, TreatmentOutput, SafetyOutput, EmpathyOutput,
)

logger = logging.getLogger(__name__)

# Admin metrics integration — import safely so it never breaks the pipeline
try:
    from admin.metrics import MetricsCollector, get_metrics
    _metrics = get_metrics()
except Exception:
    _metrics = None


def _safe_metrics(fn, *args, **kwargs):
    """Call a metrics function safely, swallowing all errors."""
    try:
        if _metrics is not None:
            return fn(*args, **kwargs)
    except Exception as e:
        logger.debug("Metrics call failed (non-fatal): %s", e)
    return None


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

        # Cache for routed specialist agents (avoid recreating per request)
        self._specialist_cache: dict[str, "BaseAgent"] = {}

        # Optimize model tiers -- use cheaper models where full reasoning isn't needed
        # These defaults are overridden when model_preference != "auto" in run_diagnosis
        self.triage.model = "claude-haiku-4-5"       # Classification only
        self.research.model = "claude-haiku-4-5"      # Lookup-based
        self.empathy.model = "claude-haiku-4-5"       # Text simplification
        # Keep Sonnet for reasoning-heavy agents (diagnostician, specialist, treatment, safety)

    async def run_diagnosis(
        self,
        symptoms: str,
        age: int = 30,
        gender: str = "unknown",
        duration: str = "recent",
        severity: int = 5,
        language: str = "en",
        image_base64: str | None = None,
        medical_history: str | None = None,
        current_medications: str | None = None,
        allergies: str | None = None,
        family_history: str | None = None,
        social_history: str | None = None,
        model_preference: str = "auto",
        specialist_routing: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Execute the full multi-agent diagnostic pipeline.

        Returns a unified response combining all agent outputs.
        """
        start = time.time()
        agent_results: dict[str, Any] = {}
        agent_timings: dict[str, float] = {}

        # Create case in admin metrics
        import uuid
        case_id = f"case-{uuid.uuid4().hex[:8]}"
        _safe_metrics(lambda: _metrics.case_store.create_case(case_id, symptoms, age, gender))
        _safe_metrics(lambda: _metrics.add_log("info", "orchestrator", f"Pipeline started for case {case_id}", case_id=case_id))

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

        # Add language instruction if not English
        LANG_NAMES = {
            "en": "English", "zh": "Chinese (Simplified)", "es": "Spanish", "fr": "French",
            "hi": "Hindi", "de": "German", "pt": "Portuguese", "ja": "Japanese",
            "ko": "Korean", "ar": "Arabic", "ru": "Russian", "it": "Italian",
        }
        if language and language != "en" and language in LANG_NAMES:
            lang_name = LANG_NAMES[language]
            patient_summary += (
                f"\n\n=== LANGUAGE INSTRUCTION ===\n"
                f"IMPORTANT: The patient speaks {lang_name}. You MUST write ALL your output "
                f"(condition names, reasoning, recommendations, warnings, summaries) in {lang_name}. "
                f"Use medical terminology appropriate for {lang_name}-speaking patients. "
                f"Keep JSON keys in English but all values/text in {lang_name}."
            )

        logger.info(f"Patient summary length: {len(patient_summary)} chars (model: {model_preference})")

        # ── Step 1: Triage ──────────────────────────────────────────
        logger.info("Step 1/7: Running Triage Agent")
        t0 = time.time()
        try:
            triage_result = await self.triage.run(
                f"Triage this patient case. You MUST respond with a JSON object containing: urgency_level (string), red_flags (array of strings), symptom_domains (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
                images=images,
                use_tools=False,
            )
            agent_results["triage"] = self._validate_agent_output(
                self._extract_agent_data(triage_result), TriageOutput
            )
            agent_results["triage_raw"] = triage_result["text"]
            agent_results["triage_tool_calls"] = triage_result["tool_calls"]
            agent_results["_token_triage"] = triage_result.get("token_usage", {})
        except Exception as e:
            logger.error("Triage agent failed: %s", e)
            agent_results["triage"] = {"urgency_level": "routine", "red_flags": [], "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("triage", case_id, round((time.time() - t0) * 1000), False, error=str(e)))
            _safe_metrics(lambda: _metrics.add_alert("warning", "triage", f"Triage agent failed: {e}"))
        agent_timings["triage"] = round(time.time() - t0, 2)
        triage_latency_ms = round(agent_timings["triage"] * 1000, 1)
        triage_success = "error" not in agent_results.get("triage", {})
        if triage_success:
            _safe_metrics(lambda: _metrics.record_agent_execution("triage", case_id, triage_latency_ms, True, token_usage=agent_results.get("_token_triage")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "triage", "triage", result=agent_results.get("triage"), timing_ms=triage_latency_ms))

        # ── Emergency fast path — ESI-1/ESI-2 with life threat ──────
        triage = agent_results.get("triage", {})
        esi_level = 5
        if isinstance(triage, dict):
            esi_level = triage.get("esi_level", 5)
            if isinstance(esi_level, str):
                try: esi_level = int(esi_level)
                except Exception: esi_level = 5

        if esi_level <= 1 or (esi_level == 2 and triage.get("requires_life_saving_intervention")):
            logger.warning("ESI-%d EMERGENCY detected — fast path activated", esi_level)

            # Run only Empathy for a clear emergency message
            emergency_prompt = (
                f"{patient_summary}\n\n"
                f"=== EMERGENCY: ESI-{esi_level} ===\n"
                f"Triage assessment: {str(triage)[:1000]}\n\n"
                f"This is a MEDICAL EMERGENCY. Generate:\n"
                f"1. Clear, calm instructions for the patient to CALL 911 / emergency services immediately\n"
                f"2. What to do while waiting (position, don't eat/drink, stay calm)\n"
                f"3. What to tell the 911 dispatcher\n"
                f"4. Red flags that mean the situation is getting worse"
            )

            t_emp = time.time()
            emergency_response = await self.empathy.run(emergency_prompt, use_tools=False)
            agent_timings["empathy"] = round(time.time() - t_emp, 2)
            emergency_data = self._extract_agent_data(emergency_response)

            total_time = round(time.time() - start, 2)

            red_flags = triage.get("red_flags", [])

            return {
                "answer": emergency_data.get("patient_summary", "") or emergency_data.get("plain_language_explanation", "Please call emergency services (911) immediately."),
                "confidence_scores": [{"cause": "Medical Emergency", "value": 99}],
                "causes": [{"cause": triage.get("domain", "Emergency"), "value": 99, "reasoning": f"ESI-{esi_level} emergency requiring immediate medical attention"}],
                "red_flags": red_flags if isinstance(red_flags, list) else [str(red_flags)],
                "additional_questions": [],
                "recommended_tests": ["Emergency department evaluation"],
                "patient_summary": emergency_data.get("patient_summary", ""),
                "action_checklist": emergency_data.get("action_checklist", ["Call 911 immediately", "Do not drive yourself", "Stay calm and in a safe position"]),
                "safety_status": "EMERGENCY",
                "safety_warnings": [f"ESI-{esi_level}: Requires immediate emergency care"],
                "medications": [],
                "lifestyle_recommendations": [],
                "warning_signs": red_flags if isinstance(red_flags, list) else [],
                "follow_up_timeline": "Emergency department NOW",
                "agent_details": {"triage": triage, "empathy": emergency_data},
                "agent_timings": agent_timings,
                "total_time": total_time,
                "multi_agent": True,
                "emergency_fast_path": True,
                "agents_used": ["triage", "empathy"],
            }

        # ── Steps 2+3: Diagnostician + Research IN PARALLEL ─────────
        logger.info("Steps 2+3/7: Running Diagnostician + Research Agents in parallel")
        t0 = time.time()

        triage_context = {"triage_assessment": agent_results.get("triage", {})}

        diag_task = asyncio.create_task(self.diagnostician.run(
            f"Perform differential diagnosis for this patient. You MUST respond with a JSON object containing: differential_diagnosis (array of objects with condition, confidence 0-100, reasoning, urgency, specialty), recommended_tests (array of strings), follow_up_questions (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
            context=triage_context,
            images=images,
            use_tools=True,
            max_iterations=4,
        ))
        research_task = asyncio.create_task(self.research.run(
            (
                f"Provide evidence-based medical research context for this patient case.\n"
                f"Search for relevant clinical guidelines, drug interactions, and disease prevalence.\n\n"
                f"{patient_summary}"
            ),
            context=triage_context,
            use_tools=True,
            max_iterations=4,
        ))

        diag_result, research_result = await asyncio.gather(
            diag_task, research_task, return_exceptions=True
        )

        # Process diagnostician result
        if isinstance(diag_result, Exception):
            logger.error("Diagnostician agent failed: %s", diag_result)
            agent_results["diagnosis"] = {"differential_diagnosis": [], "error": str(diag_result)}
        else:
            agent_results["diagnosis"] = self._validate_agent_output(
                self._extract_agent_data(diag_result), DiagnosticianOutput
            )
            logger.debug("[agent] Diagnostician raw text (first 500): %s", (diag_result.get("text") or "")[:500])
            logger.debug("[agent] Diagnostician extracted keys: %s", list(agent_results["diagnosis"].keys()))
            logger.debug("[agent] Diagnostician tool_calls count: %d", len(diag_result.get("tool_calls", [])))
            if diag_result.get("timed_out"):
                logger.warning("[agent] Diagnostician TIMED OUT")
            agent_results["diagnosis_raw"] = diag_result["text"]
            agent_results["diagnosis_tool_calls"] = diag_result["tool_calls"]
            agent_results["_token_diagnostician"] = diag_result.get("token_usage", {})

        # Process research result
        if isinstance(research_result, Exception):
            logger.error("Research agent failed: %s", research_result)
            agent_results["research"] = {"evidence_summary": "Not available", "error": str(research_result)}
        else:
            agent_results["research"] = self._validate_agent_output(
                self._extract_agent_data(research_result), ResearchOutput
            )
            logger.debug("[agent] Research extracted keys: %s", list(agent_results["research"].keys()))
            if research_result.get("timed_out"):
                logger.warning("[agent] Research TIMED OUT")
            agent_results["research_raw"] = research_result["text"]
            agent_results["research_tool_calls"] = research_result["tool_calls"]
            agent_results["_token_research"] = research_result.get("token_usage", {})

        agent_timings["diagnostician_and_research"] = round(time.time() - t0, 2)
        parallel_latency_ms = round(agent_timings["diagnostician_and_research"] * 1000, 1)

        # Record diagnostician metrics
        diag_success = not isinstance(diag_result, Exception) and "error" not in agent_results.get("diagnosis", {})
        diag_error = str(diag_result) if isinstance(diag_result, Exception) else (agent_results.get("diagnosis", {}).get("error") if not diag_success else None)
        _safe_metrics(lambda: _metrics.record_agent_execution("diagnostician", case_id, parallel_latency_ms, diag_success, error=diag_error, token_usage=agent_results.get("_token_diagnostician")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "diagnostician", "diagnostician", result=agent_results.get("diagnosis"), timing_ms=parallel_latency_ms))
        if not diag_success:
            _safe_metrics(lambda: _metrics.add_alert("warning", "diagnostician", f"Diagnostician failed: {diag_error}"))

        # Record research metrics
        research_success = not isinstance(research_result, Exception) and "error" not in agent_results.get("research", {})
        research_error = str(research_result) if isinstance(research_result, Exception) else (agent_results.get("research", {}).get("error") if not research_success else None)
        _safe_metrics(lambda: _metrics.record_agent_execution("research", case_id, parallel_latency_ms, research_success, error=research_error, token_usage=agent_results.get("_token_research")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "research", "research", result=agent_results.get("research"), timing_ms=parallel_latency_ms))
        if not research_success:
            _safe_metrics(lambda: _metrics.add_alert("warning", "research", f"Research failed: {research_error}"))

        # ── Confidence check — re-invoke Diagnostician if low confidence ──
        diagnosis = agent_results.get("diagnosis", {})
        research = agent_results.get("research", {})
        top_confidence = 0
        if isinstance(diagnosis, dict):
            diff_dx = diagnosis.get("differential_diagnosis", [])
            if isinstance(diff_dx, list) and len(diff_dx) > 0:
                first = diff_dx[0]
                if isinstance(first, dict):
                    top_confidence = first.get("confidence", 0) or first.get("confidence_pct", 0) or first.get("value", 0)
                    if isinstance(top_confidence, str):
                        try: top_confidence = int(top_confidence)
                        except Exception: top_confidence = 0

        if top_confidence > 0 and top_confidence < 50 and isinstance(research, dict):
            logger.info("Low confidence (%d%%) — re-invoking Diagnostician with research evidence", top_confidence)
            reinvoke_prompt = (
                f"{patient_summary}\n\n"
                f"=== YOUR INITIAL ASSESSMENT (confidence was only {top_confidence}%) ===\n"
                f"{str(diagnosis)[:2000]}\n\n"
                f"=== NEW EVIDENCE FROM RESEARCH AGENT ===\n"
                f"{str(research)[:2000]}\n\n"
                f"Your initial confidence was low ({top_confidence}%). With this new research evidence, "
                f"please REVISE your differential diagnosis. Be more decisive — use the evidence to "
                f"either confirm or rule out conditions. Recalculate confidence percentages."
            )
            t_re = time.time()
            revised_diagnosis = await self.diagnostician.run(reinvoke_prompt, use_tools=False)
            agent_timings["diagnostician_revision"] = round(time.time() - t_re, 2)
            revised_data = self._extract_agent_data(revised_diagnosis)

            # Check if revision improved confidence
            rev_diff = revised_data.get("differential_diagnosis", [])
            if isinstance(rev_diff, list) and len(rev_diff) > 0:
                rev_first = rev_diff[0]
                rev_conf = rev_first.get("confidence", 0) or rev_first.get("confidence_pct", 0) or 0
                if isinstance(rev_conf, str):
                    try: rev_conf = int(rev_conf)
                    except Exception: rev_conf = 0
                if rev_conf > top_confidence:
                    logger.info("Revision improved confidence: %d%% -> %d%%", top_confidence, rev_conf)
                    diagnosis = revised_data
                    agent_results["diagnosis"] = diagnosis

        # Reflection loop for Diagnostician — self-critique for bias and completeness
        if self.diagnostician.reflection_enabled:
            logger.info("Running Diagnostician reflection loop")
            t_ref = time.time()
            reflected_raw = await self.diagnostician.reflect(
                str(diagnosis)[:3000],
                context=patient_summary[:1000]
            )
            reflected_data = self._extract_agent_data({"text": reflected_raw, "tool_calls": []})
            if reflected_data and reflected_data.get("differential_diagnosis"):
                diagnosis = reflected_data
                agent_results["diagnosis"] = diagnosis
            agent_timings["diagnostician_reflection"] = round(time.time() - t_ref, 2)

        # ── Step 4: Specialist (with diagnosis + research context) ──
        # Use routed specialist(s) from PA agent, or fall back to generic specialist
        t0 = time.time()

        specialist_agent = self.specialist  # default: generic specialist
        specialist_name = "specialist"
        specialists_consulted = []

        if specialist_routing and len(specialist_routing) > 0:
            # PA agent routed to specific specialist(s) — use cache
            from .specialists.registry import get_specialist_agent
            primary_specialty = specialist_routing[0]
            if primary_specialty in self._specialist_cache:
                specialist_agent = self._specialist_cache[primary_specialty]
            else:
                specialist_agent = get_specialist_agent(
                    primary_specialty, self.api_key, self.bus, self.llm_client
                )
                self._specialist_cache[primary_specialty] = specialist_agent
            specialist_name = specialist_agent.name
            specialists_consulted = specialist_routing
            logger.info("Step 4/7: Running Routed Specialist: %s (from PA routing: %s)",
                        specialist_name, specialist_routing)

            # Apply model preference to the new specialist agent
            if model_preference and model_preference != "auto":
                model_map = {"opus": "claude-opus-4-6", "sonnet": "claude-sonnet-4-6",
                             "haiku": "claude-haiku-4-5-20251001"}
                specialist_agent.model = model_map.get(model_preference, model_preference)
        else:
            logger.info("Step 4/7: Running Generic Specialist Agent")
            # Determine specialty from triage as before
            triage_data = agent_results.get("triage", {})
            domains = triage_data.get("symptom_domains", ["general medicine"])
            specialty_focus = domains[0] if isinstance(domains, list) and domains else "general medicine"

        try:
            specialty_focus_str = specialists_consulted[0] if specialists_consulted else (
                specialty_focus if 'specialty_focus' in dir() else "general medicine")
            spec_result = await specialist_agent.run(
                (
                    f"Provide specialist consultation for this case. You MUST respond with a JSON object containing: specialist_assessment (string), specialty_specific_tests (array of strings), diagnostic_criteria (array of strings), severity_assessment (string). Respond ONLY with valid JSON.\n"
                    f"Focus specialty: {specialty_focus_str}\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                },
                images=images,
                use_tools=True,
                max_iterations=4,
            )
            agent_results["specialist"] = self._validate_agent_output(
                self._extract_agent_data(spec_result), SpecialistOutput
            )
            agent_results["specialist"]["specialist_name"] = specialist_name
            agent_results["specialist"]["specialists_consulted"] = specialists_consulted
            logger.debug("[agent] Specialist (%s) extracted keys: %s, timed_out: %s",
                        specialist_name, list(agent_results["specialist"].keys()), spec_result.get("timed_out", False))
            agent_results["specialist_raw"] = spec_result["text"]
            agent_results["specialist_tool_calls"] = spec_result["tool_calls"]
            agent_results["_token_specialist"] = spec_result.get("token_usage", {})
        except Exception as e:
            logger.error("Specialist agent (%s) failed: %s", specialist_name, e)
            agent_results["specialist"] = {"specialist_assessment": "Not available", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("specialist", case_id, round((time.time() - t0) * 1000), False, error=str(e)))
            _safe_metrics(lambda: _metrics.add_alert("warning", "specialist", f"Specialist ({specialist_name}) failed: {e}"))
        agent_timings["specialist"] = round(time.time() - t0, 2)
        spec_latency_ms = round(agent_timings["specialist"] * 1000, 1)
        spec_success = "error" not in agent_results.get("specialist", {})
        if spec_success:
            _safe_metrics(lambda: _metrics.record_agent_execution("specialist", case_id, spec_latency_ms, True, token_usage=agent_results.get("_token_specialist")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "specialist", "specialist", result=agent_results.get("specialist"), timing_ms=spec_latency_ms))

        # Consensus check — resolve Diagnostician vs Specialist disagreements
        specialist = agent_results.get("specialist", {})
        diagnosis = await self._check_consensus(diagnosis, specialist, patient_summary)
        agent_results["diagnosis"] = diagnosis

        # ── Step 5: Treatment (with all context) ────────────────────
        logger.info("Step 5/7: Running Treatment Agent")
        t0 = time.time()
        try:
            treat_result = await self.treatment.run(
                (
                    f"Create a comprehensive treatment plan for this patient. You MUST respond with a JSON object containing: treatment_plans (array of objects with condition, first_line, medications), lifestyle_recommendations (array of strings), warning_signs (array of strings), follow_up_timeline (string), immediate_actions (array of strings). Respond ONLY with valid JSON.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                },
                use_tools=True,
                max_iterations=4,
            )
            agent_results["treatment"] = self._validate_agent_output(
                self._extract_agent_data(treat_result), TreatmentOutput
            )
            logger.debug("[agent] Treatment extracted keys: %s, timed_out: %s", list(agent_results["treatment"].keys()), treat_result.get("timed_out", False))
            agent_results["treatment_raw"] = treat_result["text"]
            agent_results["treatment_tool_calls"] = treat_result["tool_calls"]
            agent_results["_token_treatment"] = treat_result.get("token_usage", {})
        except Exception as e:
            logger.error("Treatment agent failed: %s", e)
            agent_results["treatment"] = {"treatment_plans": [], "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("treatment", case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        agent_timings["treatment"] = round(time.time() - t0, 2)
        treat_latency_ms = round(agent_timings["treatment"] * 1000, 1)
        treat_success = "error" not in agent_results.get("treatment", {})
        if treat_success:
            _safe_metrics(lambda: _metrics.record_agent_execution("treatment", case_id, treat_latency_ms, True, token_usage=agent_results.get("_token_treatment")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "treatment", "treatment", result=agent_results.get("treatment"), timing_ms=treat_latency_ms))

        # ── Step 6: Safety (reviews everything) ─────────────────────
        logger.info("Step 6/7: Running Safety Agent")
        t0 = time.time()
        try:
            safety_result = await self.safety.run(
                (
                    f"Review ALL recommendations from the medical team for patient safety concerns.\n"
                    f"Check for contraindications, dosage safety, allergy risks, and dangerous combinations.\n"
                    f"You MUST respond with a JSON object containing: safety_status (string: PASS/WARNING/ALERT), warnings (array of strings), contraindications (array of strings), recommendations (array of strings). Respond ONLY with valid JSON.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                },
                use_tools=False,
            )
            agent_results["safety"] = self._validate_agent_output(
                self._extract_agent_data(safety_result), SafetyOutput
            )
            logger.debug("[agent] Safety extracted keys: %s, timed_out: %s", list(agent_results["safety"].keys()), safety_result.get("timed_out", False))
            agent_results["safety_raw"] = safety_result["text"]
            agent_results["safety_tool_calls"] = safety_result["tool_calls"]
            agent_results["_token_safety"] = safety_result.get("token_usage", {})
        except Exception as e:
            logger.error("Safety agent failed: %s", e)
            agent_results["safety"] = {"safety_status": "UNKNOWN", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("safety", case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        agent_timings["safety"] = round(time.time() - t0, 2)
        safety_latency_ms = round(agent_timings["safety"] * 1000, 1)
        safety_success = "error" not in agent_results.get("safety", {})
        if safety_success:
            _safe_metrics(lambda: _metrics.record_agent_execution("safety", case_id, safety_latency_ms, True, token_usage=agent_results.get("_token_safety")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "safety", "safety", result=agent_results.get("safety"), timing_ms=safety_latency_ms))

        # Reflection loop for Safety — double-check for missed risks
        safety = agent_results.get("safety", {})
        treatment = agent_results.get("treatment", {})
        if self.safety.reflection_enabled:
            logger.info("Running Safety reflection loop")
            t_sref = time.time()
            reflected_safety_raw = await self.safety.reflect(
                str(safety)[:3000],
                context=f"Treatment plan: {str(treatment)[:1000]}"
            )
            reflected_safety_data = self._extract_agent_data({"text": reflected_safety_raw, "tool_calls": []})
            if reflected_safety_data and reflected_safety_data.get("safety_status"):
                safety = reflected_safety_data
                agent_results["safety"] = safety
            agent_timings["safety_reflection"] = round(time.time() - t_sref, 2)

        # ── Safety veto loop — revise treatment if critical issues found ──
        treatment, safety, was_vetoed = await self._safety_veto_loop(
            treatment, safety, patient_summary,
            {"diagnosis": agent_results.get("diagnosis", {}), "specialist": agent_results.get("specialist", {})},
        )
        if was_vetoed:
            agent_results["treatment"] = treatment
            agent_results["safety"] = safety

        # ── Step 7: Empathy (patient-friendly summary) ──────────────
        logger.info("Step 7/7: Running Empathy Agent")
        t0 = time.time()
        try:
            empathy_result = await self.empathy.run(
                (
                    f"Create a patient-friendly summary of this medical assessment.\n"
                    f"Translate all clinical jargon into plain language.\n"
                    f"You MUST respond with a JSON object containing: patient_summary (string - plain language overview), action_checklist (array of strings - clear steps for the patient), when_to_seek_help (array of strings), emotional_support (string). Respond ONLY with valid JSON.\n\n"
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
                use_tools=False,
            )
            agent_results["empathy"] = self._validate_agent_output(
                self._extract_agent_data(empathy_result), EmpathyOutput
            )
            logger.debug("[agent] Empathy extracted keys: %s, timed_out: %s", list(agent_results["empathy"].keys()), empathy_result.get("timed_out", False))
            agent_results["empathy_raw"] = empathy_result["text"]
            agent_results["empathy_tool_calls"] = empathy_result["tool_calls"]
            agent_results["_token_empathy"] = empathy_result.get("token_usage", {})
        except Exception as e:
            logger.error("Empathy agent failed: %s", e)
            agent_results["empathy"] = {"patient_summary": "Summary not available.", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("empathy", case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        agent_timings["empathy"] = round(time.time() - t0, 2)
        empathy_latency_ms = round(agent_timings["empathy"] * 1000, 1)
        empathy_success = "error" not in agent_results.get("empathy", {})
        if empathy_success:
            _safe_metrics(lambda: _metrics.record_agent_execution("empathy", case_id, empathy_latency_ms, True, token_usage=agent_results.get("_token_empathy")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(case_id, "empathy", "empathy", result=agent_results.get("empathy"), timing_ms=empathy_latency_ms))

        total_time = round(time.time() - start, 2)

        # ── Synthesize final response ───────────────────────────────
        try:
            result = self._synthesize(agent_results, agent_timings, total_time, symptoms, age, gender)
        except Exception as e:
            logger.error("Synthesis failed: %s", e, exc_info=True)
            result = {
                "answer": f"Diagnosis completed but synthesis failed: {e}\n\nRaw agent outputs are available.",
                "causes": [],
                "red_flags": [],
                "recommended_tests": [],
                "agent_timings": agent_timings,
                "total_time": total_time,
                "multi_agent": True,
                "agents_used": list(agent_timings.keys()),
                "error": str(e),
            }

        # ── Collect token usage from all raw results ──────────────
        token_usage = self._collect_token_usage(agent_results)
        result["token_usage"] = token_usage
        result["estimated_cost"] = self._calculate_cost(token_usage)

        # Complete case in admin metrics and persist
        _safe_metrics(lambda: _metrics.case_store.complete_case(case_id, result))
        _safe_metrics(lambda: _metrics.add_log("info", "orchestrator", f"Pipeline completed for case {case_id} in {total_time}s", case_id=case_id))
        _safe_metrics(lambda: _metrics.create_report(case_id, "diagnosis", "generated"))
        _safe_metrics(lambda: _metrics.save_now())

        # Auto-create review for low confidence or safety issues
        try:
            if _metrics is not None:
                diag_data = agent_results.get("diagnosis", {})
                diff = diag_data.get("differential_diagnosis", [])
                if isinstance(diff, list) and diff:
                    top_conf = diff[0].get("confidence", 100) if isinstance(diff[0], dict) else 100
                    try:
                        top_conf = float(top_conf)
                    except (TypeError, ValueError):
                        top_conf = 100
                    low_threshold = _metrics.get_config_entry("low_confidence_threshold")
                    threshold_val = low_threshold["value"] if low_threshold else 40
                    if top_conf < threshold_val:
                        _metrics.create_review(case_id, "low_confidence", "medium", f"Top diagnosis confidence {top_conf}% below threshold {threshold_val}%")

                safety_data = agent_results.get("safety", {})
                safety_status = safety_data.get("safety_status", "")
                if safety_status in ("WARNING", "ALERT"):
                    _metrics.create_review(case_id, "safety_flag", "high", f"Safety review status: {safety_status}")
        except Exception:
            pass

        return result


    # ------------------------------------------------------------------
    # Consensus mechanism — Diagnostician vs Specialist
    # ------------------------------------------------------------------

    async def _check_consensus(self, diagnostician_result, specialist_result, patient_summary):
        """Check if Diagnostician and Specialist agree on top diagnosis. Reconcile if they disagree."""
        diag_dx = []
        spec_dx = []

        if isinstance(diagnostician_result, dict):
            diag_dx = diagnostician_result.get('differential_diagnosis', [])
        if isinstance(specialist_result, dict):
            spec_dx = (specialist_result.get('additional_diagnoses', [])
                       or specialist_result.get('differential_diagnosis', [])
                       or specialist_result.get('diagnostic_criteria_applied', []))

        if not diag_dx or not spec_dx:
            return diagnostician_result  # Can't compare

        # Extract top diagnosis from each
        diag_top = ''
        spec_top = ''
        if isinstance(diag_dx[0], dict):
            diag_top = (diag_dx[0].get('condition', '') or diag_dx[0].get('cause', '')).lower().strip()
        if isinstance(spec_dx[0], dict):
            spec_top = (spec_dx[0].get('condition', '') or spec_dx[0].get('cause', '') or spec_dx[0].get('criteria', '')).lower().strip()

        if not diag_top or not spec_top:
            return diagnostician_result

        # Check agreement — allow partial matches (e.g., 'migraine' matches 'migraine without aura')
        if diag_top in spec_top or spec_top in diag_top:
            logger.info("Consensus: Diagnostician and Specialist AGREE on '%s'", diag_top)
            return diagnostician_result  # Agreement — no changes needed

        # Disagreement — invoke consensus resolution
        logger.warning("DISAGREEMENT: Diagnostician says '%s', Specialist says '%s'", diag_top, spec_top)

        consensus_prompt = (
            f"{patient_summary}\n\n"
            f"=== DIAGNOSTIC DISAGREEMENT ===\n"
            f"Two medical experts have analyzed this case and DISAGREE on the primary diagnosis.\n\n"
            f"DIAGNOSTICIAN's differential:\n{str(diag_dx[:5])[:1500]}\n\n"
            f"SPECIALIST's assessment:\n{str(spec_dx[:5])[:1500]}\n\n"
            f"As a senior attending physician, reconcile these two assessments:\n"
            f"1. Where do they agree? Where do they disagree?\n"
            f"2. Which assessment is better supported by the clinical evidence?\n"
            f"3. Are there diagnoses one expert considered that the other missed?\n"
            f"4. Produce a FINAL reconciled differential diagnosis list.\n\n"
            f"Output JSON with 'differential_diagnosis' (list), 'consensus_notes' (string explaining resolution), "
            f"and 'disagreement_resolved' (boolean)."
        )

        try:
            consensus_raw = await self.diagnostician.run(consensus_prompt, use_tools=False)
            consensus_data = self._extract_agent_data(consensus_raw)

            if consensus_data and consensus_data.get('differential_diagnosis'):
                logger.info('Consensus resolved: %s', str(consensus_data.get('consensus_notes', ''))[:100])
                # Merge consensus back into diagnostician result
                diagnostician_result['differential_diagnosis'] = consensus_data['differential_diagnosis']
                diagnostician_result['consensus_notes'] = consensus_data.get('consensus_notes', '')
                diagnostician_result['disagreement_resolved'] = consensus_data.get('disagreement_resolved', True)
                return diagnostician_result
        except Exception as e:
            logger.warning('Consensus resolution failed: %s', e)

        return diagnostician_result

    # ------------------------------------------------------------------
    # Safety veto loop
    # ------------------------------------------------------------------

    async def _safety_veto_loop(self, treatment_result, safety_result, patient_summary, context, max_retries=2):
        """If Safety agent flags ALERT, re-invoke Treatment with safety constraints."""
        safety_status = ""
        if isinstance(safety_result, dict):
            safety_status = (safety_result.get("safety_status") or "").upper()

        if safety_status != "ALERT":
            return treatment_result, safety_result, False  # No veto needed

        logger.warning("Safety ALERT detected — initiating veto loop")

        for retry in range(max_retries):
            # Extract what was flagged
            warnings = safety_result.get("warnings", [])
            contraindications = safety_result.get("contraindications", [])
            vetoed_items = []
            for w in warnings:
                if isinstance(w, str):
                    vetoed_items.append(w)
                elif isinstance(w, dict):
                    vetoed_items.append(w.get("warning", "") or w.get("description", "") or str(w))
            for c in contraindications:
                if isinstance(c, str):
                    vetoed_items.append(c)
                elif isinstance(c, dict):
                    vetoed_items.append(c.get("contraindication", "") or c.get("description", "") or str(c))

            veto_context = "\n".join(vetoed_items[:10])  # Cap at 10 items

            # Re-invoke Treatment with safety constraints
            revision_prompt = (
                f"{patient_summary}\n\n"
                f"=== SAFETY VETO — REVISION REQUIRED ===\n"
                f"The Safety Agent has VETOED parts of the previous treatment plan.\n"
                f"Critical safety issues found:\n{veto_context}\n\n"
                f"You MUST revise the treatment plan to:\n"
                f"1. REMOVE any medications or treatments flagged above\n"
                f"2. SUBSTITUTE safer alternatives\n"
                f"3. Add appropriate warnings\n"
                f"4. Explain why the original recommendation was changed\n\n"
                f"Previous context: {str(context)[:2000]}"
            )

            revised_treatment = await self.treatment.run(revision_prompt, use_tools=False)
            revised_treatment = self._extract_agent_data(revised_treatment)

            # Re-run Safety on revised plan
            safety_check_prompt = (
                f"{patient_summary}\n\n"
                f"=== REVISED TREATMENT PLAN (after safety veto round {retry+1}) ===\n"
                f"{str(revised_treatment)[:3000]}\n\n"
                f"Review this REVISED plan. Has the safety issue been resolved?"
            )
            revised_safety = await self.safety.run(safety_check_prompt, use_tools=False)
            revised_safety = self._extract_agent_data(revised_safety)

            new_status = (revised_safety.get("safety_status") or "").upper()
            if new_status != "ALERT":
                logger.info("Safety veto resolved after %d revision(s)", retry + 1)
                return revised_treatment, revised_safety, True

        # Still ALERT after max retries — flag for human review
        logger.warning("Safety veto NOT resolved after %d retries — flagging for human review", max_retries)
        if isinstance(treatment_result, dict):
            treatment_result["requires_human_review"] = True
        if isinstance(safety_result, dict):
            safety_result["requires_human_review"] = True
        return treatment_result, safety_result, True

    # ------------------------------------------------------------------
    # Token usage & cost calculation
    # ------------------------------------------------------------------

    @staticmethod
    def _collect_token_usage(agent_results: dict) -> dict:
        """Collect token usage from all agents into a summary."""
        agents = ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"]
        per_agent = {}
        total_input = 0
        total_output = 0

        for agent_name in agents:
            usage = agent_results.get(f"_token_{agent_name}", {})
            inp = usage.get("input_tokens", 0)
            out = usage.get("output_tokens", 0)
            per_agent[agent_name] = {"input_tokens": inp, "output_tokens": out}
            total_input += inp
            total_output += out

        return {
            "per_agent": per_agent,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
        }

    @staticmethod
    def _calculate_cost(token_usage: dict) -> float:
        """Calculate estimated cost based on Claude Sonnet pricing.

        Claude Sonnet 4 pricing (as of 2025):
          Input:  $3.00 per 1M tokens
          Output: $15.00 per 1M tokens
        """
        input_tokens = token_usage.get("total_input_tokens", 0)
        output_tokens = token_usage.get("total_output_tokens", 0)

        input_cost = (input_tokens / 1_000_000) * 3.00
        output_cost = (output_tokens / 1_000_000) * 15.00

        return round(input_cost + output_cost, 4)

    # ------------------------------------------------------------------
    # Deep extraction helpers for treatment data
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_medications(treatment: dict) -> list:
        """Extract medications from treatment agent output, handling nested structures."""
        # Direct top-level
        meds = treatment.get("medications", [])
        if isinstance(meds, list) and len(meds) > 0:
            return meds

        # Nested under treatment_plans
        for key in ("treatment_plans", "treatment_algorithm", "stepped_care"):
            plans = treatment.get(key, {})
            if isinstance(plans, list):
                for plan in plans:
                    if isinstance(plan, dict):
                        m = plan.get("medications", [])
                        if isinstance(m, list) and len(m) > 0:
                            return m
                        # Check pharmacological sub-key
                        m = plan.get("pharmacological", plan.get("first_line", []))
                        if isinstance(m, list) and len(m) > 0:
                            return m
            elif isinstance(plans, dict):
                # stepped_care -> first_line -> medications
                for step_key in ("first_line", "second_line", "pharmacological"):
                    step = plans.get(step_key, {})
                    if isinstance(step, dict):
                        m = step.get("medications", [])
                        if isinstance(m, list) and len(m) > 0:
                            return m
                    elif isinstance(step, list) and len(step) > 0:
                        return step

        # Nested under immediate_actions
        immediate = treatment.get("immediate_actions", [])
        if isinstance(immediate, list):
            med_items = [a for a in immediate if isinstance(a, dict) and a.get("name")]
            if med_items:
                return med_items

        return []

    @staticmethod
    def _extract_lifestyle(treatment: dict) -> list:
        """Extract lifestyle recommendations from treatment agent output."""
        for key in ("lifestyle_recommendations", "lifestyle", "conservative_measures"):
            recs = treatment.get(key, [])
            if isinstance(recs, list) and len(recs) > 0:
                return recs

        # Nested under treatment_plans
        for key in ("treatment_plans", "treatment_algorithm"):
            plans = treatment.get(key, {})
            if isinstance(plans, list):
                for plan in plans:
                    if isinstance(plan, dict):
                        for rkey in ("lifestyle_recommendations", "lifestyle", "conservative", "conservative_measures"):
                            r = plan.get(rkey, [])
                            if isinstance(r, list) and len(r) > 0:
                                return r
            elif isinstance(plans, dict):
                conservative = plans.get("conservative", plans.get("conservative_measures", []))
                if isinstance(conservative, list) and len(conservative) > 0:
                    return conservative

        # Fallback: care_plan lifestyle section
        care = treatment.get("care_plan", {})
        if isinstance(care, dict):
            for rkey in ("lifestyle", "lifestyle_modifications", "recommendations"):
                r = care.get(rkey, [])
                if isinstance(r, list) and len(r) > 0:
                    return r

        return []

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
        except Exception as e:
            logger.debug("Agent summary extraction failed for %s: %s", agent_name, e)
            return "Complete"

    @staticmethod
    def _extract_highlights(agent_name: str, data: dict) -> dict:
        """Extract agent-specific structured highlights for live frontend cards."""
        try:
            if agent_name == "triage":
                red_flags = data.get("red_flags", [])
                if not isinstance(red_flags, list):
                    red_flags = []
                domains = data.get("symptom_domains", [])
                if not isinstance(domains, list):
                    domains = []
                return {
                    "urgency": data.get("urgency_level", "unknown"),
                    "red_flags_count": len(red_flags),
                    "red_flags": red_flags[:10],  # cap to avoid huge payloads
                    "domains": domains,
                }

            elif agent_name == "diagnostician":
                diff = data.get("differential_diagnosis", [])
                top_diagnoses = []
                if isinstance(diff, list):
                    for d in diff[:5]:
                        if isinstance(d, dict):
                            top_diagnoses.append({
                                "name": d.get("condition", d.get("name", "Unknown")),
                                "confidence": d.get("confidence", d.get("probability", 0)),
                                "urgency": d.get("urgency", "unknown"),
                            })
                tests = data.get("recommended_tests", [])
                tests_count = len(tests) if isinstance(tests, list) else 0
                return {
                    "top_diagnoses": top_diagnoses,
                    "tests_count": tests_count,
                }

            elif agent_name == "research":
                guidelines = data.get("clinical_guidelines", [])
                gl_count = len(guidelines) if isinstance(guidelines, list) else 0
                evidence = data.get("evidence_summary", "")
                preview = evidence[:200] if isinstance(evidence, str) else ""
                return {
                    "guidelines_count": gl_count,
                    "evidence_summary_preview": preview,
                }

            elif agent_name == "specialist":
                return {
                    "specialty_consulted": data.get("specialty_consulted", data.get("focus_specialty", "General")),
                    "risk_level": data.get("risk_level", data.get("risk_assessment", "unknown")),
                    "criteria_applied": data.get("criteria_applied", data.get("scoring_criteria", "none")),
                }

            elif agent_name == "treatment":
                meds = data.get("medications", data.get("treatment_plans", []))
                med_count = len(meds) if isinstance(meds, list) else 0
                lifestyle = data.get("lifestyle_recommendations", [])
                lifestyle_count = len(lifestyle) if isinstance(lifestyle, list) else 0
                immediate = data.get("immediate_actions", [])
                has_immediate = bool(immediate and isinstance(immediate, list) and len(immediate) > 0)
                return {
                    "medications_count": med_count,
                    "lifestyle_recs_count": lifestyle_count,
                    "has_immediate_actions": has_immediate,
                }

            elif agent_name == "safety":
                warnings = data.get("warnings", [])
                warnings_count = len(warnings) if isinstance(warnings, list) else 0
                contras = data.get("contraindications", [])
                critical = []
                if isinstance(contras, list):
                    critical = contras[:5]
                status = data.get("safety_status", "UNKNOWN")
                # Normalize to PASS / CAUTION / ALERT
                status_upper = status.upper() if isinstance(status, str) else "UNKNOWN"
                if status_upper in ("PASS", "CAUTION", "ALERT"):
                    normalized = status_upper
                elif status_upper in ("WARNING",):
                    normalized = "CAUTION"
                else:
                    normalized = status_upper
                return {
                    "status": normalized,
                    "warnings_count": warnings_count,
                    "critical_issues": critical,
                }

            elif agent_name == "empathy":
                summary = data.get("patient_summary", "")
                preview = summary[:200] if isinstance(summary, str) else ""
                actions = data.get("action_checklist", [])
                action_count = len(actions) if isinstance(actions, list) else 0
                return {
                    "summary_preview": preview,
                    "action_items_count": action_count,
                }

            return {}
        except Exception as e:
            logger.debug("Highlights extraction failed for %s: %s", agent_name, e)
            return {}

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

        # Create case in admin metrics
        import uuid
        stream_case_id = f"case-{uuid.uuid4().hex[:8]}"
        _safe_metrics(lambda: _metrics.case_store.create_case(stream_case_id, symptoms, age, gender))
        _safe_metrics(lambda: _metrics.add_log("info", "orchestrator", f"Streaming pipeline started for case {stream_case_id}", case_id=stream_case_id))

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
        await event_queue.put({"event": "agent_start", "agent": "triage"})
        t0 = time.time()
        try:
            triage_result = await self.triage.run(
                f"Triage this patient case. You MUST respond with a JSON object containing: urgency_level (string), red_flags (array of strings), symptom_domains (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
                images=images,
                use_tools=False,
            )
            agent_results["triage"] = self._validate_agent_output(
                self._extract_agent_data(triage_result), TriageOutput
            )
            agent_results["triage_raw"] = triage_result["text"]
            agent_results["triage_tool_calls"] = triage_result["tool_calls"]
            agent_results["_token_triage"] = triage_result.get("token_usage", {})
        except Exception as e:
            logger.error("Triage agent failed: %s", e)
            agent_results["triage"] = {"urgency_level": "routine", "red_flags": [], "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("triage", stream_case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        elapsed_triage = round(time.time() - t0, 2)
        agent_timings["triage"] = elapsed_triage
        _triage_latency = round(elapsed_triage * 1000, 1)
        if "error" not in agent_results.get("triage", {}):
            _safe_metrics(lambda: _metrics.record_agent_execution("triage", stream_case_id, _triage_latency, True, token_usage=agent_results.get("_token_triage")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "triage", "triage", result=agent_results.get("triage"), timing_ms=_triage_latency))

        await event_queue.put({
            "event": "agent_complete",
            "agent": "triage",
            "elapsed": elapsed_triage,
            "key_findings": self._extract_key_findings("triage", agent_results["triage"]),
            "data": agent_results["triage"],
            "highlights": self._extract_highlights("triage", agent_results["triage"]),
        })

        # ── Steps 2+3: Diagnostician + Research IN PARALLEL ─────────
        logger.info("[stream] Steps 2+3/7: Running Diagnostician + Research in parallel")
        await event_queue.put({"event": "agent_start", "agent": "diagnostician"})
        await event_queue.put({"event": "agent_start", "agent": "research"})
        t0 = time.time()

        triage_context = {"triage_assessment": agent_results.get("triage", {})}

        diag_task = asyncio.create_task(self.diagnostician.run(
            f"Perform differential diagnosis for this patient. You MUST respond with a JSON object containing: differential_diagnosis (array of objects with condition, confidence 0-100, reasoning, urgency, specialty), recommended_tests (array of strings), follow_up_questions (array of strings). Respond ONLY with valid JSON.\n\n{patient_summary}",
            context=triage_context,
            use_tools=True,
            max_iterations=4,
        ))
        research_task = asyncio.create_task(self.research.run(
            (
                f"Provide evidence-based medical research context for this patient case.\n"
                f"Search for relevant clinical guidelines, drug interactions, and disease prevalence.\n"
                f"You MUST respond ONLY with valid JSON.\n\n"
                f"{patient_summary}"
            ),
            context=triage_context,
            use_tools=True,
            max_iterations=4,
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
            agent_results["diagnosis"] = self._validate_agent_output(
                self._extract_agent_data(diag_result), DiagnosticianOutput
            )
            agent_results["diagnosis_raw"] = diag_result["text"]
            agent_results["diagnosis_tool_calls"] = diag_result["tool_calls"]
            agent_results["_token_diagnostician"] = diag_result.get("token_usage", {})

        # Process research result
        if isinstance(research_result, Exception):
            logger.error("Research agent failed: %s", research_result)
            agent_results["research"] = {"evidence_summary": "Not available", "error": str(research_result)}
        else:
            agent_results["research"] = self._validate_agent_output(
                self._extract_agent_data(research_result), ResearchOutput
            )
            agent_results["research_raw"] = research_result["text"]
            agent_results["research_tool_calls"] = research_result["tool_calls"]
            agent_results["_token_research"] = research_result.get("token_usage", {})

        agent_timings["diagnostician"] = parallel_elapsed
        agent_timings["research"] = parallel_elapsed
        _par_latency = round(parallel_elapsed * 1000, 1)

        # Record diagnostician metrics (streaming)
        _s_diag_success = not isinstance(diag_result, Exception) and "error" not in agent_results.get("diagnosis", {})
        _s_diag_err = str(diag_result) if isinstance(diag_result, Exception) else (agent_results.get("diagnosis", {}).get("error") if not _s_diag_success else None)
        _safe_metrics(lambda: _metrics.record_agent_execution("diagnostician", stream_case_id, _par_latency, _s_diag_success, error=_s_diag_err, token_usage=agent_results.get("_token_diagnostician")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "diagnostician", "diagnostician", result=agent_results.get("diagnosis"), timing_ms=_par_latency))

        # Record research metrics (streaming)
        _s_res_success = not isinstance(research_result, Exception) and "error" not in agent_results.get("research", {})
        _s_res_err = str(research_result) if isinstance(research_result, Exception) else (agent_results.get("research", {}).get("error") if not _s_res_success else None)
        _safe_metrics(lambda: _metrics.record_agent_execution("research", stream_case_id, _par_latency, _s_res_success, error=_s_res_err, token_usage=agent_results.get("_token_research")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "research", "research", result=agent_results.get("research"), timing_ms=_par_latency))

        # Emit both parallel agents
        await event_queue.put({
            "event": "agent_complete",
            "agent": "diagnostician",
            "elapsed": parallel_elapsed,
            "key_findings": self._extract_key_findings("diagnostician", agent_results["diagnosis"]),
            "data": agent_results["diagnosis"],
            "highlights": self._extract_highlights("diagnostician", agent_results["diagnosis"]),
        })
        await event_queue.put({
            "event": "agent_complete",
            "agent": "research",
            "elapsed": parallel_elapsed,
            "key_findings": self._extract_key_findings("research", agent_results["research"]),
            "data": agent_results["research"],
            "highlights": self._extract_highlights("research", agent_results["research"]),
        })

        # ── Step 4: Specialist ──────────────────────────────────────
        logger.info("[stream] Step 4/7: Running Specialist Agent")
        await event_queue.put({"event": "agent_start", "agent": "specialist"})
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
                    f"Provide specialist consultation for this case. You MUST respond with a JSON object containing: specialist_assessment (string), specialty_specific_tests (array of strings), diagnostic_criteria (array of strings), severity_assessment (string). Respond ONLY with valid JSON.\n"
                    f"Focus specialty: {specialty_focus}\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                },
                use_tools=True,
                max_iterations=4,
            )
            agent_results["specialist"] = self._validate_agent_output(
                self._extract_agent_data(spec_result), SpecialistOutput
            )
            logger.debug("[agent] Specialist extracted keys: %s, timed_out: %s", list(agent_results["specialist"].keys()), spec_result.get("timed_out", False))
            agent_results["specialist_raw"] = spec_result["text"]
            agent_results["specialist_tool_calls"] = spec_result["tool_calls"]
            agent_results["_token_specialist"] = spec_result.get("token_usage", {})
        except Exception as e:
            logger.error("Specialist agent failed: %s", e)
            agent_results["specialist"] = {"specialist_assessment": "Not available", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("specialist", stream_case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        elapsed_spec = round(time.time() - t0, 2)
        agent_timings["specialist"] = elapsed_spec
        _spec_lat = round(elapsed_spec * 1000, 1)
        if "error" not in agent_results.get("specialist", {}):
            _safe_metrics(lambda: _metrics.record_agent_execution("specialist", stream_case_id, _spec_lat, True, token_usage=agent_results.get("_token_specialist")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "specialist", "specialist", result=agent_results.get("specialist"), timing_ms=_spec_lat))

        await event_queue.put({
            "event": "agent_complete",
            "agent": "specialist",
            "elapsed": elapsed_spec,
            "key_findings": self._extract_key_findings("specialist", agent_results["specialist"]),
            "data": agent_results["specialist"],
            "highlights": self._extract_highlights("specialist", agent_results["specialist"]),
        })

        # ── Step 5: Treatment ───────────────────────────────────────
        logger.info("[stream] Step 5/7: Running Treatment Agent")
        await event_queue.put({"event": "agent_start", "agent": "treatment"})
        t0 = time.time()
        try:
            treat_result = await self.treatment.run(
                (
                    f"Create a comprehensive treatment plan for this patient. You MUST respond with a JSON object containing: treatment_plans (array of objects with condition, first_line, medications), lifestyle_recommendations (array of strings), warning_signs (array of strings), follow_up_timeline (string), immediate_actions (array of strings). Respond ONLY with valid JSON.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                },
                use_tools=True,
                max_iterations=4,
            )
            agent_results["treatment"] = self._validate_agent_output(
                self._extract_agent_data(treat_result), TreatmentOutput
            )
            logger.debug("[agent] Treatment extracted keys: %s, timed_out: %s", list(agent_results["treatment"].keys()), treat_result.get("timed_out", False))
            agent_results["treatment_raw"] = treat_result["text"]
            agent_results["treatment_tool_calls"] = treat_result["tool_calls"]
            agent_results["_token_treatment"] = treat_result.get("token_usage", {})
        except Exception as e:
            logger.error("Treatment agent failed: %s", e)
            agent_results["treatment"] = {"treatment_plans": [], "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("treatment", stream_case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        elapsed_treat = round(time.time() - t0, 2)
        agent_timings["treatment"] = elapsed_treat
        _treat_lat = round(elapsed_treat * 1000, 1)
        if "error" not in agent_results.get("treatment", {}):
            _safe_metrics(lambda: _metrics.record_agent_execution("treatment", stream_case_id, _treat_lat, True, token_usage=agent_results.get("_token_treatment")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "treatment", "treatment", result=agent_results.get("treatment"), timing_ms=_treat_lat))

        await event_queue.put({
            "event": "agent_complete",
            "agent": "treatment",
            "elapsed": elapsed_treat,
            "key_findings": self._extract_key_findings("treatment", agent_results["treatment"]),
            "data": agent_results["treatment"],
            "highlights": self._extract_highlights("treatment", agent_results["treatment"]),
        })

        # ── Step 6: Safety ──────────────────────────────────────────
        logger.info("[stream] Step 6/7: Running Safety Agent")
        await event_queue.put({"event": "agent_start", "agent": "safety"})
        t0 = time.time()
        try:
            safety_result = await self.safety.run(
                (
                    f"Review ALL recommendations from the medical team for patient safety concerns.\n"
                    f"Check for contraindications, dosage safety, allergy risks, and dangerous combinations.\n"
                    f"You MUST respond with a JSON object containing: safety_status (string: PASS/WARNING/ALERT), warnings (array of strings), contraindications (array of strings), recommendations (array of strings). Respond ONLY with valid JSON.\n\n"
                    f"Patient:\n{patient_summary}"
                ),
                context={
                    "triage_assessment": agent_results.get("triage", {}),
                    "differential_diagnosis": agent_results.get("diagnosis", {}),
                    "research_evidence": agent_results.get("research", {}),
                    "specialist_consultation": agent_results.get("specialist", {}),
                    "treatment_plan": agent_results.get("treatment", {}),
                },
                use_tools=False,
            )
            agent_results["safety"] = self._validate_agent_output(
                self._extract_agent_data(safety_result), SafetyOutput
            )
            logger.debug("[agent] Safety extracted keys: %s, timed_out: %s", list(agent_results["safety"].keys()), safety_result.get("timed_out", False))
            agent_results["safety_raw"] = safety_result["text"]
            agent_results["safety_tool_calls"] = safety_result["tool_calls"]
            agent_results["_token_safety"] = safety_result.get("token_usage", {})
        except Exception as e:
            logger.error("Safety agent failed: %s", e)
            agent_results["safety"] = {"safety_status": "UNKNOWN", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("safety", stream_case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        elapsed_safety = round(time.time() - t0, 2)
        agent_timings["safety"] = elapsed_safety
        _safety_lat = round(elapsed_safety * 1000, 1)
        if "error" not in agent_results.get("safety", {}):
            _safe_metrics(lambda: _metrics.record_agent_execution("safety", stream_case_id, _safety_lat, True, token_usage=agent_results.get("_token_safety")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "safety", "safety", result=agent_results.get("safety"), timing_ms=_safety_lat))

        await event_queue.put({
            "event": "agent_complete",
            "agent": "safety",
            "elapsed": elapsed_safety,
            "key_findings": self._extract_key_findings("safety", agent_results["safety"]),
            "data": agent_results["safety"],
            "highlights": self._extract_highlights("safety", agent_results["safety"]),
        })

        # ── Step 7: Empathy ─────────────────────────────────────────
        logger.info("[stream] Step 7/7: Running Empathy Agent")
        await event_queue.put({"event": "agent_start", "agent": "empathy"})
        t0 = time.time()
        try:
            empathy_result = await self.empathy.run(
                (
                    f"Create a patient-friendly summary of this medical assessment.\n"
                    f"Translate all clinical jargon into plain language.\n"
                    f"You MUST respond with a JSON object containing: patient_summary (string - plain language overview), action_checklist (array of strings - clear steps for the patient), when_to_seek_help (array of strings), emotional_support (string). Respond ONLY with valid JSON.\n\n"
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
                use_tools=False,
            )
            agent_results["empathy"] = self._validate_agent_output(
                self._extract_agent_data(empathy_result), EmpathyOutput
            )
            logger.debug("[agent] Empathy extracted keys: %s, timed_out: %s", list(agent_results["empathy"].keys()), empathy_result.get("timed_out", False))
            agent_results["empathy_raw"] = empathy_result["text"]
            agent_results["empathy_tool_calls"] = empathy_result["tool_calls"]
            agent_results["_token_empathy"] = empathy_result.get("token_usage", {})
        except Exception as e:
            logger.error("Empathy agent failed: %s", e)
            agent_results["empathy"] = {"patient_summary": "Summary not available.", "error": str(e)}
            _safe_metrics(lambda: _metrics.record_agent_execution("empathy", stream_case_id, round((time.time() - t0) * 1000), False, error=str(e)))
        elapsed_empathy = round(time.time() - t0, 2)
        agent_timings["empathy"] = elapsed_empathy
        _empathy_lat = round(elapsed_empathy * 1000, 1)
        if "error" not in agent_results.get("empathy", {}):
            _safe_metrics(lambda: _metrics.record_agent_execution("empathy", stream_case_id, _empathy_lat, True, token_usage=agent_results.get("_token_empathy")))
        _safe_metrics(lambda: _metrics.case_store.update_stage(stream_case_id, "empathy", "empathy", result=agent_results.get("empathy"), timing_ms=_empathy_lat))

        await event_queue.put({
            "event": "agent_complete",
            "agent": "empathy",
            "elapsed": elapsed_empathy,
            "key_findings": self._extract_key_findings("empathy", agent_results["empathy"]),
            "data": agent_results["empathy"],
            "highlights": self._extract_highlights("empathy", agent_results["empathy"]),
        })

        total_time = round(time.time() - start, 2)

        # ── Synthesize final response ───────────────────────────────
        try:
            final_result = self._synthesize(agent_results, agent_timings, total_time, symptoms, age, gender)
            token_usage = self._collect_token_usage(agent_results)
            final_result["token_usage"] = token_usage
            final_result["estimated_cost"] = self._calculate_cost(token_usage)
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

        # Debug: dump result for inspection
        try:
            import pathlib
            debug_path = pathlib.Path(__file__).parent.parent / "_debug_last_result.json"
            debug_path.write_text(json.dumps(final_result, indent=2, default=str), encoding="utf-8")
            # Also dump raw agent results for deeper inspection
            debug_raw_path = pathlib.Path(__file__).parent.parent / "_debug_agent_results.json"
            debug_raw_path.write_text(json.dumps(agent_results, indent=2, default=str), encoding="utf-8")
            logger.info("Debug: result has %d causes, written to %s", len(final_result.get("causes", [])), debug_path)
        except Exception as dbg_err:
            logger.warning("Debug dump failed: %s", dbg_err)

        # Complete case in admin metrics (streaming) and persist
        _safe_metrics(lambda: _metrics.case_store.complete_case(stream_case_id, final_result))
        _safe_metrics(lambda: _metrics.add_log("info", "orchestrator", f"Streaming pipeline completed for case {stream_case_id} in {total_time}s", case_id=stream_case_id))
        _safe_metrics(lambda: _metrics.create_report(stream_case_id, "diagnosis", "generated"))
        _safe_metrics(lambda: _metrics.save_now())

        # Auto-create review for low confidence or safety issues (streaming)
        try:
            if _metrics is not None:
                diag_data = agent_results.get("diagnosis", {})
                diff = diag_data.get("differential_diagnosis", [])
                if isinstance(diff, list) and diff:
                    top_conf = diff[0].get("confidence", 100) if isinstance(diff[0], dict) else 100
                    try:
                        top_conf = float(top_conf)
                    except (TypeError, ValueError):
                        top_conf = 100
                    low_threshold = _metrics.get_config_entry("low_confidence_threshold")
                    threshold_val = low_threshold["value"] if low_threshold else 40
                    if top_conf < threshold_val:
                        _metrics.create_review(stream_case_id, "low_confidence", "medium", f"Top diagnosis confidence {top_conf}% below threshold {threshold_val}%")

                safety_data = agent_results.get("safety", {})
                safety_status = safety_data.get("safety_status", "")
                if safety_status in ("WARNING", "ALERT"):
                    _metrics.create_review(stream_case_id, "safety_flag", "high", f"Safety review status: {safety_status}")
        except Exception:
            pass

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
        language: str = "en",
    ) -> dict[str, Any]:
        """Handle follow-up questions using the treatment agent with full context."""
        context = {}
        if previous_diagnosis:
            context["previous_diagnosis"] = previous_diagnosis
        if original_symptoms:
            context["original_symptoms"] = original_symptoms

        LANG_NAMES = {
            "en": "English", "zh": "Chinese (Simplified)", "es": "Spanish", "fr": "French",
            "hi": "Hindi", "de": "German", "pt": "Portuguese", "ja": "Japanese",
            "ko": "Korean", "ar": "Arabic", "ru": "Russian", "it": "Italian",
        }
        lang_suffix = ""
        if language and language != "en" and language in LANG_NAMES:
            lang_suffix = f"\n\nIMPORTANT: Respond entirely in {LANG_NAMES[language]}."

        result = await self.treatment.run(
            f"Patient follow-up question: {question}{lang_suffix}",
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
        language: str = "en",
    ) -> str:
        """Generate a follow-up question using the diagnostician agent."""
        history_block = "\n".join(f"- {h}" for h in conversation_history[-5:]) if conversation_history else "None yet"
        prev_q_block = "\n".join(f"- {q}" for q in previous_questions) if previous_questions else "None yet"

        LANG_NAMES = {
            "en": "English", "zh": "Chinese (Simplified)", "es": "Spanish", "fr": "French",
            "hi": "Hindi", "de": "German", "pt": "Portuguese", "ja": "Japanese",
            "ko": "Korean", "ar": "Arabic", "ru": "Russian", "it": "Italian",
        }
        lang_suffix = ""
        if language and language != "en" and language in LANG_NAMES:
            lang_suffix = f"\nIMPORTANT: Write the question in {LANG_NAMES[language]}."

        prompt = (
            f"Generate ONE specific follow-up question for this patient.\n\n"
            f"Patient: {age}-year-old {gender}\n"
            f"Chief complaint: {symptoms}\n\n"
            f"This is question {questions_asked + 1} of {total_ai_questions}.\n\n"
            f"Conversation so far:\n{history_block}\n\n"
            f"Questions already asked (DO NOT repeat):\n{prev_q_block}\n\n"
            f"Return ONLY the question text, nothing else.{lang_suffix}"
        )

        result = await self.diagnostician.run(prompt)
        return result["text"].strip().strip('"')

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_agent_output(self, data: dict, schema_class) -> dict:
        """Validate agent output against a Pydantic schema, filling defaults for missing fields."""
        try:
            validated = schema_class.model_validate(data)
            return validated.model_dump(by_alias=False)
        except Exception:
            # Best effort: fill missing keys with defaults
            try:
                defaults = schema_class().model_dump()
                for key, val in defaults.items():
                    if key not in data:
                        data[key] = val
            except Exception:
                pass
            return data

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

        # Strategy 2: ```json code blocks (with or without closing ```)
        match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if not match:
            # Handle truncated response: opening ``` but no closing ```
            match = re.search(r'```(?:json)?\s*\n(.*)', text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            try:
                result = json.loads(content)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                # Try to repair truncated JSON
                repaired = self._repair_truncated_json(content)
                if repaired:
                    return repaired

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
                if isinstance(result, dict) and len(result) >= 1:
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

        # Strategy 4: If text starts with { but is truncated (no matching }),
        # try to repair the truncated JSON
        stripped = text.strip().lstrip('`').lstrip('json').strip()
        if stripped.startswith('{'):
            repaired = self._repair_truncated_json(stripped)
            if repaired:
                return repaired

        logger.warning("_safe_parse failed to extract JSON from %d chars of text", len(text))
        return {"raw_text": text}

    @staticmethod
    def _repair_truncated_json(text: str) -> dict | None:
        """Attempt to repair truncated JSON by closing open brackets/braces."""
        import re
        if not text or not text.strip().startswith('{'):
            return None

        # Remove trailing incomplete string/value
        # Trim back to the last complete key-value pair or array element
        trimmed = text.rstrip()

        # Remove any trailing partial string (unclosed quote)
        # Count quotes — if odd, we're inside a string; trim back to last complete line
        if trimmed.count('"') % 2 != 0:
            # Find last complete line (ending before the incomplete string)
            lines = trimmed.split('\n')
            while lines:
                last = lines[-1]
                if last.count('"') % 2 != 0:
                    lines.pop()
                else:
                    break
            trimmed = '\n'.join(lines)

        # Remove trailing commas
        trimmed = re.sub(r',\s*$', '', trimmed)

        # Count open vs close brackets/braces
        open_braces = trimmed.count('{') - trimmed.count('}')
        open_brackets = trimmed.count('[') - trimmed.count(']')

        # Close them in reverse order based on what was opened
        # Build closing sequence by scanning what's still open
        stack = []
        in_string = False
        escape = False
        for ch in trimmed:
            if escape:
                escape = False
                continue
            if ch == '\\' and in_string:
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                stack.append('}')
            elif ch == '[':
                stack.append(']')
            elif ch in ('}', ']') and stack and stack[-1] == ch:
                stack.pop()

        # Close everything that's still open
        closing = ''.join(reversed(stack))
        attempt = trimmed + closing

        try:
            result = json.loads(attempt)
            if isinstance(result, dict) and len(result) >= 1:
                logger.info("_repair_truncated_json succeeded: recovered %d keys", len(result))
                return result
        except json.JSONDecodeError:
            pass

        # More aggressive: trim back further, try again
        # Remove last incomplete array element or object
        for trim_pattern in [
            r',\s*\{[^{}]*$',    # trailing incomplete object in array
            r',\s*"[^"]*":\s*$', # trailing incomplete key
            r',\s*"[^"]*$',      # trailing incomplete string
        ]:
            aggressive = re.sub(trim_pattern, '', trimmed)
            if aggressive != trimmed:
                stack2 = []
                in_str = False
                esc = False
                for ch in aggressive:
                    if esc: esc = False; continue
                    if ch == '\\' and in_str: esc = True; continue
                    if ch == '"': in_str = not in_str; continue
                    if in_str: continue
                    if ch == '{': stack2.append('}')
                    elif ch == '[': stack2.append(']')
                    elif ch in ('}', ']') and stack2 and stack2[-1] == ch: stack2.pop()
                closing2 = ''.join(reversed(stack2))
                try:
                    result = json.loads(aggressive + closing2)
                    if isinstance(result, dict) and len(result) >= 1:
                        logger.info("_repair_truncated_json (aggressive) succeeded: recovered %d keys", len(result))
                        return result
                except json.JSONDecodeError:
                    continue

        return None

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
        logger.info("[SYNTH] diagnosis keys = %s", list(diagnosis.keys()) if isinstance(diagnosis, dict) else type(diagnosis))
        logger.info("[SYNTH] diagnosis content (first 500): %s", json.dumps(diagnosis, default=str)[:500])
        logger.info("[SYNTH] treatment keys = %s", list(treatment.keys()) if isinstance(treatment, dict) else type(treatment))
        logger.info("[SYNTH] safety keys = %s", list(safety.keys()) if isinstance(safety, dict) else type(safety))
        differential = (
            diagnosis.get("differential_diagnosis")
            or diagnosis.get("diagnoses")
            or diagnosis.get("differential")
            or diagnosis.get("conditions")
            or []
        )
        logger.info("[SYNTH] differential count = %d, type = %s", len(differential) if isinstance(differential, list) else -1, type(differential))
        if isinstance(differential, list) and differential:
            logger.info("[SYNTH] first differential item = %s", str(differential[0])[:200])
        else:
            logger.warning("[SYNTH] NO differential found! Will try raw_text fallback. Has raw_text: %s", bool(diagnosis.get("raw_text")))
        causes = []
        for d in differential[:5]:
            if isinstance(d, dict):
                # Handle multiple possible confidence key names
                confidence = (
                    d.get("confidence") or d.get("confidence_pct")
                    or d.get("probability") or d.get("likelihood")
                    or d.get("post_test_probability") or 50
                )
                # Ensure confidence is a number 0-100
                if isinstance(confidence, str):
                    try:
                        confidence = float(confidence.strip('%'))
                    except (ValueError, AttributeError):
                        confidence = 50
                causes.append({
                    "cause": d.get("condition") or d.get("name") or d.get("diagnosis") or "Unknown",
                    "value": min(100, max(0, int(confidence))),
                    "explanation": (
                        d.get("reasoning") or d.get("clinical_reasoning")
                        or d.get("bayesian_reasoning") or d.get("explanation")
                        or d.get("rationale") or d.get("illness_script_fit") or ""
                    ),
                    "urgency": d.get("urgency") or d.get("priority") or "routine",
                    "specialty": d.get("specialty") or d.get("recommended_specialty") or "Primary Care",
                    "supporting_features": d.get("supporting_features", []),
                    "opposing_features": d.get("opposing_features", []),
                    "must_not_miss": d.get("must_not_miss", False),
                })
            elif isinstance(d, str):
                # Agent returned list of strings instead of dicts
                causes.append({"cause": d, "value": 50, "explanation": "", "urgency": "routine", "specialty": "Primary Care"})

        # Fallback: if causes empty but raw text exists, try to extract from text
        if not causes and diagnosis.get("raw_text"):
            logger.warning("No structured diagnoses found — extracting from raw text")
            raw = diagnosis["raw_text"]
            import re

            # Strategy 1: Find all JSON objects in the text via bracket matching, then
            # look for differential/diagnoses arrays in any of them
            candidates = []
            depth = 0
            start = -1
            for i, ch in enumerate(raw):
                if ch == '{':
                    if depth == 0:
                        start = i
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0 and start >= 0:
                        candidates.append(raw[start:i + 1])
                        start = -1
            # Try largest candidates first (most likely the full response object)
            candidates.sort(key=len, reverse=True)

            diff_keys = ["differential_diagnosis", "diagnoses", "differential", "conditions"]
            for candidate in candidates:
                if causes:
                    break
                try:
                    parsed = json.loads(candidate)
                except json.JSONDecodeError:
                    # Try fixing trailing commas
                    fixed = re.sub(r',\s*}', '}', candidate)
                    fixed = re.sub(r',\s*]', ']', fixed)
                    try:
                        parsed = json.loads(fixed)
                    except json.JSONDecodeError:
                        continue
                if not isinstance(parsed, dict):
                    continue
                # Look for differential diagnosis under any known key
                diff = None
                for dk in diff_keys:
                    diff = parsed.get(dk)
                    if isinstance(diff, list) and diff:
                        break
                if not isinstance(diff, list) or not diff:
                    continue
                for d in diff[:5]:
                    if isinstance(d, dict):
                        confidence = (
                            d.get("confidence") or d.get("confidence_pct")
                            or d.get("probability") or d.get("likelihood")
                            or d.get("post_test_probability") or 50
                        )
                        if isinstance(confidence, str):
                            try:
                                confidence = float(confidence.strip('%'))
                            except (ValueError, AttributeError):
                                confidence = 50
                        causes.append({
                            "cause": d.get("condition") or d.get("name") or d.get("diagnosis") or "Unknown",
                            "value": min(100, max(0, int(confidence))),
                            "explanation": (
                                d.get("reasoning") or d.get("clinical_reasoning")
                                or d.get("bayesian_reasoning") or d.get("explanation")
                                or d.get("rationale") or ""
                            ),
                            "urgency": d.get("urgency") or d.get("priority") or "routine",
                            "specialty": d.get("specialty") or d.get("recommended_specialty") or "Primary Care",
                            "supporting_features": d.get("supporting_features", []),
                            "opposing_features": d.get("opposing_features", []),
                            "must_not_miss": d.get("must_not_miss", False),
                        })

            # Strategy 2: Look for numbered diagnoses like "1. Condition Name" or "- Condition"
            if not causes:
                pattern = re.findall(r'(?:^|\n)\s*(?:\d+[\.\)]\s*|[-•]\s*\*{0,2})([A-Z][A-Za-z\s\(\)/\-\']+?)(?:\s*[-–:]\s*|\s*\(|\s*\n)', raw)
                for i, name in enumerate(pattern[:5]):
                    name = name.strip().rstrip('.-:*')
                    if len(name) > 3 and len(name) < 80:
                        # Try to extract confidence percentage near the name
                        conf_match = re.search(re.escape(name) + r'.*?(\d{1,3})\s*%', raw)
                        confidence = int(conf_match.group(1)) if conf_match else max(20, 80 - i * 15)
                        causes.append({
                            "cause": name,
                            "value": min(100, confidence),
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
            or diagnosis.get("discriminating_features")
            or []
        )
        # Also check must_not_miss for recommended tests
        must_not_miss = diagnosis.get("must_not_miss", [])
        if isinstance(must_not_miss, list):
            for mnm in must_not_miss:
                if isinstance(mnm, dict):
                    mnm_tests = mnm.get("recommended_tests", [])
                    if isinstance(mnm_tests, list):
                        recommended_tests = recommended_tests + mnm_tests

        specialist_tests = (
            specialist.get("specialty_specific_tests")
            or specialist.get("recommended_tests")
            or specialist.get("tests")
            or specialist.get("diagnostic_criteria")
            or []
        )
        if isinstance(specialist_tests, list):
            # Flatten to strings before deduplicating (agents may return dicts or strings)
            combined = []
            for item in recommended_tests + specialist_tests:
                if isinstance(item, dict):
                    combined.append(item.get("test") or item.get("name") or item.get("description") or str(item))
                elif isinstance(item, str) and item.strip():
                    combined.append(item)
            recommended_tests = list(dict.fromkeys(combined))  # dedupe preserving order

        # Fallback: extract tests from raw text
        if not recommended_tests:
            import re
            for raw_key in ["diagnosis_raw", "specialist_raw"]:
                raw_text = results.get(raw_key, "")
                if raw_text and isinstance(raw_text, str):
                    # Look for test names in lists
                    test_patterns = re.findall(
                        r'(?:^|\n)\s*[-•\d.]+\s*\*{0,2}((?:Complete|CBC|CT|MRI|X-ray|Biopsy|Blood|Urine|ECG|EKG|Ultrasound|PET|Mammogram|Colonoscopy|Endoscopy|Dermatoscopy|Patch test|Skin|Liver|Kidney|Thyroid|Lipid|Metabolic|Hemoglobin|Urinalysis|Culture|Swab)[A-Za-z\s\(\)/\-,]*)',
                        raw_text, re.IGNORECASE
                    )
                    for t in test_patterns[:8]:
                        t = t.strip().rstrip('.-:*')
                        if t and len(t) > 3 and t not in recommended_tests:
                            recommended_tests.append(t)

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
            or empathy.get("patient_friendly_summary")
            or ""
        )
        # Fallback: use first paragraph of empathy raw text as summary
        if not patient_summary and results.get("empathy_raw"):
            raw_empathy = results["empathy_raw"]
            # Skip any JSON and get the first substantial text paragraph
            paragraphs = [p.strip() for p in raw_empathy.split('\n\n') if p.strip() and not p.strip().startswith('{')]
            if paragraphs:
                patient_summary = paragraphs[0][:500]
        action_checklist = (
            empathy.get("action_checklist")
            or empathy.get("actions")
            or empathy.get("next_steps")
            or empathy.get("recommendations")
            or empathy.get("action_items")
            or empathy.get("checklist")
            or treatment.get("action_checklist")
            or treatment.get("next_steps")
            or treatment.get("immediate_actions")
            or []
        )
        # Fallback: extract action items from empathy raw text
        if not action_checklist and results.get("empathy_raw"):
            import re
            raw_empathy = results["empathy_raw"]
            # Look for checklist items: "☐ ...", "✅ ...", "- [ ] ...", "1. ...", "• ..."
            items = re.findall(
                r'(?:^|\n)\s*(?:[☐✅□■▪●◆✓]|[-•]\s*\[.\]|\d+[\.\)])\s*(.+?)(?:\n|$)',
                raw_empathy
            )
            if not items:
                # Simpler pattern: bulleted items in action/next steps sections
                action_section = re.search(
                    r'(?:action|next step|what.*do|checklist|recommendation)s?\s*[:]*\s*\n((?:\s*[-•\d].+\n?)+)',
                    raw_empathy, re.IGNORECASE
                )
                if action_section:
                    items = re.findall(r'[-•\d.]+\s*(.+)', action_section.group(1))
            action_checklist = [i.strip() for i in items[:10] if i.strip()]
        # Flatten action_checklist items to strings (agents may return dicts)
        if isinstance(action_checklist, list):
            flat_actions = []
            for item in action_checklist:
                if isinstance(item, dict):
                    flat_actions.append(item.get("action") or item.get("step") or item.get("description") or item.get("text") or str(item))
                elif isinstance(item, str) and item.strip():
                    flat_actions.append(item.strip())
            action_checklist = flat_actions
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
        # Flatten safety warnings to plain strings
        flat_safety = []
        for w in safety_warnings:
            if isinstance(w, dict):
                text = w.get("issue") or w.get("title") or w.get("message") or w.get("description") or w.get("text")
                if not text:
                    title = w.get("title", "")
                    detail = w.get("detail", "")
                    text = f"{title}: {detail}" if title and detail else title or detail or str(w)
                flat_safety.append(text)
            elif isinstance(w, str):
                flat_safety.append(w)

        medications = self._extract_medications(treatment)
        lifestyle = self._extract_lifestyle(treatment)
        warning_signs_raw = treatment.get("warning_signs", [])
        warning_signs = []
        for ws in (warning_signs_raw if isinstance(warning_signs_raw, list) else []):
            if isinstance(ws, dict):
                warning_signs.append(ws.get("sign") or ws.get("warning") or ws.get("description") or str(ws))
            elif isinstance(ws, str) and ws.strip():
                warning_signs.append(ws)
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
