"""
Unit tests for the agent infrastructure:

  - OrchestratorAgent initialises all 7 pipeline agents
  - MessageBus registers, sends, and delivers messages
  - BaseAgent subclass instantiation, model attribute, tool-use loop helpers
"""

from __future__ import annotations

import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Async helper — runs a coroutine inside a single dedicated event loop so
# that asyncio.Queue objects created within the same call share the loop.
# Using asyncio.run() each time would create a fresh loop, breaking Queue
# objects that were created on a previous loop.
# ---------------------------------------------------------------------------

def _run(coro):
    """Run an async coroutine synchronously, creating a new event loop."""
    return asyncio.run(coro)


async def _send_and_receive(bus_class, message_class, sender_name, recipient_name, msg_kwargs):
    """Helper coroutine: create bus, send message, receive it."""
    from agents.message_bus import MessageBus, Message
    bus = MessageBus()
    bus.register(sender_name)
    bus.register(recipient_name)
    msg = Message(**msg_kwargs)
    await bus.send(msg)
    received = await bus.receive(recipient_name, timeout=1.0)
    return bus, msg, received

# ---------------------------------------------------------------------------
# Make the backend package importable
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Helpers / shared fixtures
# ---------------------------------------------------------------------------

FAKE_KEY = "sk-ant-fake-key-for-unit-tests"


# ---------------------------------------------------------------------------
# MessageBus tests
# ---------------------------------------------------------------------------

class TestMessageBus:
    """Unit tests for the async inter-agent message bus."""

    def test_register_creates_mailbox(self):
        from agents.message_bus import MessageBus
        bus = MessageBus()
        bus.register("triage")
        assert "triage" in bus._queues

    def test_register_is_idempotent(self):
        from agents.message_bus import MessageBus
        bus = MessageBus()
        bus.register("diagnostician")
        bus.register("diagnostician")
        # Still only one queue for the agent
        assert len(bus._queues) == 1

    def test_send_appends_to_log(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("triage")
            msg = Message(sender="orchestrator", recipient="triage", kind="start", payload={"task": "triage"})
            await bus.send(msg)
            return bus, msg

        bus, msg = asyncio.run(_run_test())
        assert len(bus._log) == 1
        assert bus._log[0] is msg

    def test_receive_delivers_message(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("diagnostician")
            msg = Message(sender="triage", recipient="diagnostician", kind="triage_result", payload={"urgency": "medium"})
            await bus.send(msg)
            received = await bus.receive("diagnostician", timeout=1.0)
            return received

        received = asyncio.run(_run_test())
        assert received is not None
        assert received.sender == "triage"
        assert received.kind == "triage_result"
        assert received.payload["urgency"] == "medium"

    def test_receive_times_out_when_no_message(self):
        from agents.message_bus import MessageBus

        async def _run_test():
            bus = MessageBus()
            bus.register("safety")
            return await bus.receive("safety", timeout=0.1)

        result = asyncio.run(_run_test())
        assert result is None

    def test_get_messages_for_filters_by_recipient(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("treatment")
            bus.register("empathy")
            m1 = Message("o", "treatment", "plan", {})
            m2 = Message("o", "empathy", "translate", {})
            await bus.send(m1)
            await bus.send(m2)
            return bus

        bus = asyncio.run(_run_test())
        treatment_msgs = bus.get_messages_for("treatment")
        assert len(treatment_msgs) == 1
        assert treatment_msgs[0]["recipient"] == "treatment"

    def test_get_messages_from_filters_by_sender(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("specialist")
            bus.register("treatment")
            m1 = Message("specialist", "treatment", "result", {"diagnosis": "migraine"})
            m2 = Message("triage", "specialist", "start", {})
            await bus.send(m1)
            await bus.send(m2)
            return bus

        bus = asyncio.run(_run_test())
        from_specialist = bus.get_messages_from("specialist")
        assert len(from_specialist) == 1
        assert from_specialist[0]["sender"] == "specialist"

    def test_get_full_log_returns_all_messages(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("a")
            bus.register("b")
            for i in range(5):
                await bus.send(Message("a", "b", f"kind_{i}", {}))
            return bus

        bus = asyncio.run(_run_test())
        log = bus.get_full_log()
        assert len(log) == 5

    def test_clear_empties_queues_and_log(self):
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("x")
            await bus.send(Message("a", "x", "k", {}))
            bus.clear()
            return bus

        bus = asyncio.run(_run_test())
        assert len(bus._log) == 0
        assert len(bus._queues) == 0

    def test_message_to_dict_has_expected_keys(self):
        from agents.message_bus import Message
        msg = Message(sender="triage", recipient="diagnostician", kind="triage_result", payload={"urgency": "high"})
        d = msg.to_dict()
        for key in ("id", "sender", "recipient", "kind", "payload", "timestamp", "correlation_id"):
            assert key in d, f"Missing key in Message.to_dict(): {key}"

    def test_message_id_is_unique(self):
        from agents.message_bus import Message
        ids = {Message("a", "b", "k", {}).id for _ in range(100)}
        assert len(ids) == 100

    def test_get_conversation_filters_by_correlation_id(self):
        from agents.message_bus import MessageBus, Message

        corr_id = "test-correlation-123"

        async def _run_test():
            bus = MessageBus()
            bus.register("b")
            m1 = Message("a", "b", "k", {}, correlation_id=corr_id)
            m2 = Message("a", "b", "k", {})  # different correlation_id
            await bus.send(m1)
            await bus.send(m2)
            return bus

        bus = asyncio.run(_run_test())
        conversation = bus.get_conversation(corr_id)
        assert len(conversation) == 1
        assert conversation[0]["correlation_id"] == corr_id


# ---------------------------------------------------------------------------
# OrchestratorAgent initialisation
# ---------------------------------------------------------------------------

class TestOrchestratorInit:
    """Test that the Orchestrator correctly instantiates all pipeline agents."""

    @pytest.fixture(autouse=True)
    def mock_anthropic(self):
        """Prevent real Anthropic client creation."""
        with patch("anthropic.AsyncAnthropic") as mock_cls:
            mock_cls.return_value = MagicMock()
            yield mock_cls

    def test_orchestrator_creates_bus(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.message_bus import MessageBus
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.bus, MessageBus)

    def test_orchestrator_has_triage_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.triage import TriageAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.triage, TriageAgent)

    def test_orchestrator_has_diagnostician_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.diagnostician import DiagnosticianAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.diagnostician, DiagnosticianAgent)

    def test_orchestrator_has_research_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.research import ResearchAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.research, ResearchAgent)

    def test_orchestrator_has_specialist_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.specialist import SpecialistAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.specialist, SpecialistAgent)

    def test_orchestrator_has_treatment_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.treatment import TreatmentAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.treatment, TreatmentAgent)

    def test_orchestrator_has_safety_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.safety import SafetyAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.safety, SafetyAgent)

    def test_orchestrator_has_empathy_agent(self):
        from agents.orchestrator import OrchestratorAgent
        from agents.empathy import EmpathyAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert isinstance(orch.empathy, EmpathyAgent)

    def test_orchestrator_all_seven_agents_registered_on_bus(self):
        """All 7 agents must register a mailbox on the shared MessageBus."""
        from agents.orchestrator import OrchestratorAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        expected_agents = {"triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"}
        registered = set(orch.bus._queues.keys())
        assert expected_agents.issubset(registered), (
            f"Missing agents: {expected_agents - registered}"
        )

    def test_orchestrator_model_tiers_applied(self):
        """Triage, research, empathy use cheaper haiku model by default."""
        from agents.orchestrator import OrchestratorAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY)
        assert "haiku" in orch.triage.model.lower()
        assert "haiku" in orch.research.model.lower()
        assert "haiku" in orch.empathy.model.lower()

    def test_orchestrator_accepts_openai_key(self):
        """OrchestratorAgent can be constructed with an openai_key argument."""
        from agents.orchestrator import OrchestratorAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY, openai_key="sk-openai-fake")
        assert orch is not None  # No exception raised

    def test_orchestrator_accepts_google_key(self):
        """OrchestratorAgent can be constructed with a google_key argument."""
        from agents.orchestrator import OrchestratorAgent
        orch = OrchestratorAgent(api_key=FAKE_KEY, google_key="AIzafakekey")
        assert orch is not None


# ---------------------------------------------------------------------------
# BaseAgent class-level unit tests
# ---------------------------------------------------------------------------

class TestBaseAgentClass:
    """
    Tests for BaseAgent behaviour accessible without running the full pipeline.
    We use a concrete subclass since BaseAgent is abstract (_build_system_prompt
    raises NotImplementedError).
    """

    @pytest.fixture(autouse=True)
    def mock_anthropic(self):
        with patch("anthropic.AsyncAnthropic") as mock_cls:
            mock_cls.return_value = MagicMock()
            yield mock_cls

    @pytest.fixture()
    def concrete_agent(self):
        """Return a minimal concrete agent (TriageAgent) for testing base behaviour."""
        from agents.triage import TriageAgent
        from agents.message_bus import MessageBus
        bus = MessageBus()
        return TriageAgent(api_key=FAKE_KEY, bus=bus)

    def test_agent_has_name_attribute(self, concrete_agent):
        assert hasattr(concrete_agent, "name")
        assert concrete_agent.name  # not empty

    def test_agent_has_model_attribute(self, concrete_agent):
        assert hasattr(concrete_agent, "model")
        assert isinstance(concrete_agent.model, str)
        assert len(concrete_agent.model) > 0

    def test_agent_has_bus_attribute(self, concrete_agent):
        from agents.message_bus import MessageBus
        assert isinstance(concrete_agent.bus, MessageBus)

    def test_agent_registered_on_bus(self, concrete_agent):
        assert concrete_agent.name in concrete_agent.bus._queues

    def test_agent_has_system_prompt(self, concrete_agent):
        assert hasattr(concrete_agent, "_system_prompt")
        assert isinstance(concrete_agent._system_prompt, str)
        assert len(concrete_agent._system_prompt) > 10

    def test_agent_has_get_tools_method(self, concrete_agent):
        assert hasattr(concrete_agent, "_get_tools")
        tools = concrete_agent._get_tools()
        assert isinstance(tools, list)

    def test_agent_ollama_mode_does_not_create_anthropic_client(self):
        """When api_key='ollama', the Anthropic client must not be created."""
        from agents.triage import TriageAgent
        from agents.message_bus import MessageBus

        # Use a fresh bus so we don't clash with other tests
        bus = MessageBus()
        agent = TriageAgent(api_key="ollama", bus=bus)
        # client should be None in Ollama mode
        assert agent.client is None

    def test_agent_with_real_key_creates_anthropic_client(self, concrete_agent):
        """When a real (fake) key is provided, client should be set."""
        assert concrete_agent.client is not None

    def test_diagnostician_has_higher_tier_model(self):
        """DiagnosticianAgent uses sonnet (not haiku) by default."""
        from agents.diagnostician import DiagnosticianAgent
        from agents.message_bus import MessageBus
        bus = MessageBus()
        agent = DiagnosticianAgent(api_key=FAKE_KEY, bus=bus)
        # Diagnostician should not use haiku
        assert "haiku" not in agent.model.lower()

    def test_specialist_uses_sonnet_model(self):
        from agents.specialist import SpecialistAgent
        from agents.message_bus import MessageBus
        bus = MessageBus()
        agent = SpecialistAgent(api_key=FAKE_KEY, bus=bus)
        assert "haiku" not in agent.model.lower()

    def test_safety_uses_sonnet_model(self):
        from agents.safety import SafetyAgent
        from agents.message_bus import MessageBus
        bus = MessageBus()
        agent = SafetyAgent(api_key=FAKE_KEY, bus=bus)
        assert "haiku" not in agent.model.lower()

    def test_treatment_uses_sonnet_model(self):
        from agents.treatment import TreatmentAgent
        from agents.message_bus import MessageBus
        bus = MessageBus()
        agent = TreatmentAgent(api_key=FAKE_KEY, bus=bus)
        assert "haiku" not in agent.model.lower()


# ---------------------------------------------------------------------------
# LLMClient unit tests
# ---------------------------------------------------------------------------

class TestLLMClient:

    def test_llm_client_instantiates_with_anthropic_key(self):
        from agents.llm_client import LLMClient
        with patch("anthropic.AsyncAnthropic"):
            client = LLMClient(anthropic_key=FAKE_KEY)
        assert client is not None

    def test_llm_client_instantiates_with_no_keys(self):
        """LLMClient must not raise when all keys are None."""
        from agents.llm_client import LLMClient
        client = LLMClient()
        assert client is not None

    def test_llm_client_instantiates_with_openai_key(self):
        from agents.llm_client import LLMClient
        client = LLMClient(openai_key="sk-openai-fake-key")
        assert client is not None


# ---------------------------------------------------------------------------
# Inter-agent message delivery (integration-level)
# ---------------------------------------------------------------------------

class TestMessageBusIntegration:
    """Tests that confirm multiple agents can communicate through the bus."""

    def test_triage_can_send_to_diagnostician(self):
        """A message sent from triage arrives in diagnostician's queue."""
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("triage")
            bus.register("diagnostician")
            msg = Message(
                sender="triage",
                recipient="diagnostician",
                kind="triage_result",
                payload={"urgency": "high", "red_flags": ["chest pain"]},
            )
            await bus.send(msg)
            received = await bus.receive("diagnostician", timeout=1.0)
            return received

        received = asyncio.run(_run_test())
        assert received is not None
        assert received.payload["urgency"] == "high"

    def test_multiple_messages_delivered_in_order(self):
        """Messages are delivered FIFO to their recipient."""
        from agents.message_bus import MessageBus, Message

        async def _run_test():
            bus = MessageBus()
            bus.register("treatment")
            kinds = ["start", "context", "result"]
            for kind in kinds:
                await bus.send(Message("orch", "treatment", kind, {}))
            received_kinds = []
            for _ in range(3):
                msg = await bus.receive("treatment", timeout=1.0)
                assert msg is not None
                received_kinds.append(msg.kind)
            return received_kinds

        received_kinds = asyncio.run(_run_test())
        assert received_kinds == ["start", "context", "result"]
