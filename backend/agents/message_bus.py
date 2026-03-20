"""
Async message bus for inter-agent communication.

Agents post structured messages to the bus and subscribe to messages
from other agents. This enables fully autonomous agent-to-agent dialogue
without the orchestrator having to manually shuttle every payload.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any


class Message:
    """A single message on the bus."""

    __slots__ = ("id", "sender", "recipient", "kind", "payload", "timestamp", "correlation_id")

    def __init__(
        self,
        sender: str,
        recipient: str,
        kind: str,
        payload: dict[str, Any],
        correlation_id: str | None = None,
    ):
        self.id = uuid.uuid4().hex[:12]
        self.sender = sender
        self.recipient = recipient
        self.kind = kind  # e.g. "triage_result", "consult_request", "diagnosis_result"
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.correlation_id = correlation_id or uuid.uuid4().hex[:12]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "kind": self.kind,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }


class MessageBus:
    """
    In-process async message bus.

    Agents register mailboxes.  Any agent can ``send`` a message to another
    agent's mailbox, and the recipient ``receives`` it when ready.  The bus
    also keeps a full audit log so the orchestrator can review the entire
    conversation between agents.
    """

    def __init__(self):
        self._queues: dict[str, asyncio.Queue[Message]] = {}
        self._log: list[Message] = []

    def register(self, agent_name: str) -> None:
        if agent_name not in self._queues:
            self._queues[agent_name] = asyncio.Queue()

    async def send(self, message: Message) -> None:
        self._log.append(message)
        recipient = message.recipient
        if recipient not in self._queues:
            self._queues[recipient] = asyncio.Queue()
        await self._queues[recipient].put(message)

    async def receive(self, agent_name: str, timeout: float = 30.0) -> Message | None:
        if agent_name not in self._queues:
            self._queues[agent_name] = asyncio.Queue()
        try:
            return await asyncio.wait_for(self._queues[agent_name].get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def get_messages_for(self, agent_name: str) -> list[dict]:
        return [m.to_dict() for m in self._log if m.recipient == agent_name]

    def get_messages_from(self, agent_name: str) -> list[dict]:
        return [m.to_dict() for m in self._log if m.sender == agent_name]

    def get_full_log(self) -> list[dict]:
        return [m.to_dict() for m in self._log]

    def get_conversation(self, correlation_id: str) -> list[dict]:
        return [m.to_dict() for m in self._log if m.correlation_id == correlation_id]

    def clear(self) -> None:
        self._queues.clear()
        self._log.clear()
