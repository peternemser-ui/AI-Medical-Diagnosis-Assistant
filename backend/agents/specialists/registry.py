"""
Specialist Agent Registry

Maps specialty names to their agent classes. Falls back to the generic
SpecialistAgent when a requested specialty isn't available.
"""

import logging
from ..base import BaseAgent
from ..message_bus import MessageBus
from ..llm_client import LLMClient

logger = logging.getLogger(__name__)


def _lazy_imports():
    """Lazy import all specialist agents to avoid circular imports."""
    from .cardiology import CardiologyAgent
    from .dermatology import DermatologyAgent
    from .neurology import NeurologyAgent
    from .gastroenterology import GastroenterologyAgent
    from .psychiatry import PsychiatryAgent
    return {
        "cardiology": CardiologyAgent,
        "dermatology": DermatologyAgent,
        "neurology": NeurologyAgent,
        "gastroenterology": GastroenterologyAgent,
        "psychiatry": PsychiatryAgent,
    }


# Aliases that map to the same specialist
_ALIASES = {
    "cardiac": "cardiology",
    "heart": "cardiology",
    "skin": "dermatology",
    "neuro": "neurology",
    "brain": "neurology",
    "gastro": "gastroenterology",
    "gi": "gastroenterology",
    "digestive": "gastroenterology",
    "mental_health": "psychiatry",
    "psychology": "psychiatry",
    "urology": "general_medicine",
    "pulmonology": "general_medicine",
    "endocrinology": "general_medicine",
    "rheumatology": "general_medicine",
    "infectious_disease": "general_medicine",
    "orthopedics": "general_medicine",
}

SPECIALIST_REGISTRY = {}


def _ensure_registry():
    global SPECIALIST_REGISTRY
    if not SPECIALIST_REGISTRY:
        SPECIALIST_REGISTRY.update(_lazy_imports())


def get_specialist_agent(
    specialty: str,
    api_key: str,
    bus: MessageBus,
    llm_client: LLMClient | None = None,
) -> BaseAgent:
    """
    Factory: return the appropriate specialist agent for the given specialty.

    Falls back to the generic SpecialistAgent if the specialty isn't registered.
    """
    _ensure_registry()

    # Normalize the specialty name
    specialty_lower = specialty.lower().strip().replace(" ", "_")

    # Check aliases
    if specialty_lower in _ALIASES:
        specialty_lower = _ALIASES[specialty_lower]

    # Look up in registry
    agent_class = SPECIALIST_REGISTRY.get(specialty_lower)

    if agent_class:
        logger.info("Using specialist agent: %s for specialty: %s", agent_class.name, specialty)
        return agent_class(api_key=api_key, bus=bus, llm_client=llm_client)
    else:
        # Fallback to generic specialist
        logger.info("No specialist agent for '%s', using generic SpecialistAgent", specialty)
        from ..specialist import SpecialistAgent
        return SpecialistAgent(api_key=api_key, bus=bus, llm_client=llm_client)


def list_available_specialties() -> list[str]:
    """Return list of available specialist names."""
    _ensure_registry()
    return sorted(SPECIALIST_REGISTRY.keys())
