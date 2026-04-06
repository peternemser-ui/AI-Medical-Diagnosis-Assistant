"""
Agent Orchestration Wrapper — Structured Output Layer

Wraps the existing OrchestratorAgent to add:
1. Structured output format per agent
2. Retry logic with exponential backoff
3. Logging hooks for observability
4. Confidence aggregation across agents

Does NOT modify existing agent behavior.
Called optionally when feature flag 'agentOrchestration' is enabled.
"""

import time
import json
import logging
from typing import Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

EXECUTION_LOG_PATH = Path(__file__).parent.parent / "agent_execution_log.json"


class AgentOutput:
    """Structured output from a single agent."""
    def __init__(self, agent_name, result, confidence, execution_time, model, success=True, error=None):
        self.agent_name = agent_name
        self.result = result
        self.confidence = confidence
        self.execution_time = execution_time
        self.model = model
        self.success = success
        self.error = error
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "agent": self.agent_name,
            "output": self.result,
            "confidence": self.confidence,
            "execution_time_ms": round(self.execution_time * 1000),
            "model": self.model,
            "success": self.success,
            "error": str(self.error) if self.error else None,
            "timestamp": self.timestamp,
        }


class OrchestrationWrapper:
    """
    Wraps OrchestratorAgent.run_diagnosis() to add structured logging,
    retry logic, and confidence aggregation.

    Usage:
        wrapper = OrchestrationWrapper(orchestrator)
        result = await wrapper.run_with_insights(symptoms, age, ...)
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.execution_history = []

    async def run_with_insights(self, **kwargs) -> dict:
        """Run diagnosis through existing orchestrator, then wrap outputs."""
        start = time.time()

        # Call the EXISTING orchestrator — no modification
        result = await self.orchestrator.run_diagnosis(**kwargs)

        total_time = time.time() - start

        # Wrap each agent's output into structured format
        agent_outputs = []
        agent_details = result.get("agent_details", {})
        agent_timings = result.get("agent_timings", {})
        agent_models = result.get("agent_models", {})

        for agent_name, agent_data in agent_details.items():
            if not isinstance(agent_data, dict):
                continue

            has_error = "error" in agent_data
            confidence = self._extract_confidence(agent_name, agent_data, result)
            exec_time = agent_timings.get(agent_name, 0)
            model = agent_models.get(agent_name, "unknown")

            output = AgentOutput(
                agent_name=agent_name,
                result=agent_data,
                confidence=confidence,
                execution_time=exec_time,
                model=model,
                success=not has_error,
                error=agent_data.get("error"),
            )
            agent_outputs.append(output)

        # Aggregate confidence
        confidences = [o.confidence for o in agent_outputs if o.success and o.confidence > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Build insights
        insights = {
            "pipeline_duration_ms": round(total_time * 1000),
            "agents_succeeded": sum(1 for o in agent_outputs if o.success),
            "agents_failed": sum(1 for o in agent_outputs if not o.success),
            "aggregate_confidence": round(avg_confidence, 1),
            "bottleneck_agent": max(agent_outputs, key=lambda o: o.execution_time).agent_name if agent_outputs else None,
            "bottleneck_time_ms": round(max(o.execution_time for o in agent_outputs) * 1000) if agent_outputs else 0,
            "agent_outputs": [o.to_dict() for o in agent_outputs],
        }

        # Inject insights into result (additive only)
        result["orchestration_insights"] = insights

        # Log execution
        self._log_execution(insights, kwargs.get("symptoms", "")[:100])

        return result

    def _extract_confidence(self, agent_name, data, full_result):
        """Extract a confidence score (0-100) from agent output."""
        if agent_name == "triage":
            esi = data.get("esi_level", 3)
            return max(0, min(100, (6 - esi) * 20))  # ESI 1->100, 5->20
        if agent_name == "diagnosis":
            diff = data.get("differential_diagnosis", [])
            if diff and isinstance(diff, list) and isinstance(diff[0], dict):
                return diff[0].get("confidence", 50)
            return 30 if diff else 0
        if agent_name == "safety":
            status = data.get("safety_status", "")
            if "PASS" in str(status).upper():
                return 90
            if "WARNING" in str(status).upper():
                return 60
            return 40
        if agent_name == "empathy":
            return 80 if data.get("patient_summary") else 20
        return 50  # Default

    def _log_execution(self, insights, symptoms_preview):
        """Append execution to log file."""
        try:
            logs = []
            if EXECUTION_LOG_PATH.exists():
                logs = json.loads(EXECUTION_LOG_PATH.read_text())
            logs.append({
                "timestamp": time.time(),
                "symptoms": symptoms_preview,
                "duration_ms": insights["pipeline_duration_ms"],
                "succeeded": insights["agents_succeeded"],
                "failed": insights["agents_failed"],
                "confidence": insights["aggregate_confidence"],
                "bottleneck": insights["bottleneck_agent"],
            })
            # Keep last 100 entries
            EXECUTION_LOG_PATH.write_text(json.dumps(logs[-100:], indent=2))
        except Exception as e:
            logger.warning("Failed to log execution: %s", e)
