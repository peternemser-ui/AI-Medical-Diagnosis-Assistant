"""
Multi-Agent Medical Diagnosis System

Architecture:
  Orchestrator -> Triage -> Diagnostician + Research (parallel) -> Specialist -> Treatment -> Safety -> Empathy

Each agent is autonomous, uses Claude via tool use, and communicates
through the shared MessageBus.
"""

from .orchestrator import OrchestratorAgent
from .message_bus import MessageBus
from .research import ResearchAgent
from .safety import SafetyAgent
from .empathy import EmpathyAgent

__all__ = [
    "OrchestratorAgent",
    "MessageBus",
    "ResearchAgent",
    "SafetyAgent",
    "EmpathyAgent",
]
