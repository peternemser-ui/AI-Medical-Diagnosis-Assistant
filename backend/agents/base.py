"""
Base agent class – every specialist agent inherits from this.

Each agent:
  * Has a name, role description, and system prompt
  * Calls an LLM via the multi-vendor LLMClient with tool use
  * Can send/receive messages on the MessageBus
  * Runs an autonomous tool-use loop until it produces a final answer
"""

from __future__ import annotations

import json
import logging
from typing import Any

from anthropic import AsyncAnthropic

from .message_bus import Message, MessageBus
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class BaseAgent:
    """Abstract base for all medical agents."""

    name: str = "base_agent"
    description: str = "Base agent"
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 4096
    temperature: float = 0.3

    def __init__(self, api_key: str, bus: MessageBus, llm_client: LLMClient | None = None):
        # Keep legacy Anthropic client for backward compatibility
        # Skip Anthropic init if using Ollama (key="ollama")
        if api_key and api_key != "ollama":
            self.client = AsyncAnthropic(api_key=api_key)
        else:
            self.client = None
        # Multi-vendor LLM client (used when model is non-Anthropic)
        self.llm_client = llm_client
        self.bus = bus
        self.bus.register(self.name)
        self._system_prompt = self._build_system_prompt()

    # ------------------------------------------------------------------
    # Subclass hooks
    # ------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        raise NotImplementedError

    def _get_tools(self) -> list[dict]:
        """Return tool definitions available to this agent."""
        return self._default_tools()

    async def _handle_tool_call(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool call and return the result string."""
        if tool_name == "send_message_to_agent":
            return await self._tool_send_message(tool_input)
        if tool_name == "request_consultation":
            return await self._tool_request_consultation(tool_input)
        if tool_name == "publish_result":
            return json.dumps({"status": "published", "data": tool_input})
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    # ------------------------------------------------------------------
    # Default tools every agent gets
    # ------------------------------------------------------------------

    def _default_tools(self) -> list[dict]:
        return [
            {
                "name": "send_message_to_agent",
                "description": (
                    "Send a structured message to another agent on the team. "
                    "Use this to request analysis, share findings, or ask for a second opinion."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "recipient": {
                            "type": "string",
                            "description": "Name of the agent to send to (triage, diagnostician, specialist, treatment, orchestrator)",
                        },
                        "kind": {
                            "type": "string",
                            "description": "Message type (e.g. consult_request, findings, second_opinion)",
                        },
                        "content": {
                            "type": "object",
                            "description": "Structured payload for the recipient agent",
                        },
                    },
                    "required": ["recipient", "kind", "content"],
                },
            },
            {
                "name": "request_consultation",
                "description": (
                    "Request a focused consultation from a specialist agent. "
                    "Describe what you need and which agent should handle it."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "target_agent": {
                            "type": "string",
                            "description": "The agent to consult (specialist, diagnostician, treatment)",
                        },
                        "question": {
                            "type": "string",
                            "description": "The specific clinical question to answer",
                        },
                        "context": {
                            "type": "object",
                            "description": "Relevant patient data and findings so far",
                        },
                    },
                    "required": ["target_agent", "question", "context"],
                },
            },
            {
                "name": "publish_result",
                "description": "Publish your final structured result so other agents and the orchestrator can use it.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "result_type": {
                            "type": "string",
                            "description": "Type of result (triage, diagnosis, specialist_review, treatment_plan)",
                        },
                        "data": {
                            "type": "object",
                            "description": "The structured result data",
                        },
                    },
                    "required": ["result_type", "data"],
                },
            },
        ]

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    async def _tool_send_message(self, tool_input: dict) -> str:
        msg = Message(
            sender=self.name,
            recipient=tool_input["recipient"],
            kind=tool_input["kind"],
            payload=tool_input.get("content", {}),
        )
        await self.bus.send(msg)
        logger.info("[%s] -> [%s] kind=%s", self.name, msg.recipient, msg.kind)
        return json.dumps({"status": "sent", "message_id": msg.id, "recipient": msg.recipient})

    async def _tool_request_consultation(self, tool_input: dict) -> str:
        msg = Message(
            sender=self.name,
            recipient=tool_input["target_agent"],
            kind="consult_request",
            payload={
                "question": tool_input["question"],
                "context": tool_input.get("context", {}),
            },
        )
        await self.bus.send(msg)
        logger.info("[%s] consultation request -> [%s]", self.name, msg.recipient)
        return json.dumps({
            "status": "consultation_requested",
            "target": tool_input["target_agent"],
            "message_id": msg.id,
        })

    # ------------------------------------------------------------------
    # Core agent loop
    # ------------------------------------------------------------------

    async def run(self, user_message: str, context: dict[str, Any] | None = None, images: list[str] | None = None, timeout: float = None) -> dict[str, Any]:
        """
        Run the autonomous agent loop with a timeout.

        Sends *user_message* to Claude along with the agent's tools.
        Loops over tool_use blocks until Claude produces a final text answer.
        Returns a dict with ``text`` (final answer) and ``tool_calls`` (log).

        If *images* is provided (list of base64-encoded image strings),
        the user message is sent as a multi-part content block so Claude
        can perform visual analysis.
        """
        import asyncio
        from .llm_client import get_vendor
        # Local models (Ollama) need more time per agent
        if timeout is None:
            timeout = 90.0 if get_vendor(self.model) == "ollama" else 45.0
        try:
            return await asyncio.wait_for(
                self._run_loop(user_message, context, images),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.error("[%s] Agent timed out after %.0fs", self.name, timeout)
            return {
                "text": f"Agent {self.name} timed out after {timeout:.0f}s. The analysis may be incomplete.",
                "tool_calls": [],
                "timed_out": True,
            }

    async def _run_loop(self, user_message: str, context: dict[str, Any] | None = None, images: list[str] | None = None) -> dict[str, Any]:
        """Internal agent loop — called by run() with timeout wrapper."""
        messages: list[dict] = []

        # Inject context from other agents if available
        if context:
            context_block = (
                "Here is context from other agents on the team:\n"
                + json.dumps(context, indent=2)
            )
            messages.append({"role": "user", "content": context_block})
            messages.append({"role": "assistant", "content": "Thank you. I have reviewed the context from my colleagues. I will now proceed with my analysis."})

        # Build user content — plain string or multimodal with images
        if images:
            content: list[dict] = [{"type": "text", "text": user_message}]
            for img in images:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img,
                    },
                })
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": user_message})

        tools = self._get_tools()
        tool_call_log: list[dict] = []
        total_input_tokens = 0
        total_output_tokens = 0
        max_iterations = 4  # Limit tool-use rounds to prevent agents from looping too long

        # Determine whether to use multi-vendor LLMClient or direct Anthropic
        from .llm_client import get_vendor
        use_llm_client = self.llm_client and (get_vendor(self.model) != "anthropic" or self.client is None)

        for _ in range(max_iterations):
            if use_llm_client:
                resp = await self.llm_client.create_message(
                    model=self.model,
                    system=self._system_prompt,
                    messages=messages,
                    tools=tools,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                assistant_content = resp["content"]
            else:
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=self._system_prompt,
                    tools=tools,
                    messages=messages,
                )
                assistant_content = response.content

            # Track token usage
            if not use_llm_client and hasattr(response, "usage"):
                u = response.usage
                total_input_tokens += getattr(u, "input_tokens", 0)
                total_output_tokens += getattr(u, "output_tokens", 0)
            elif use_llm_client and isinstance(resp, dict) and "usage" in resp:
                u = resp["usage"]
                total_input_tokens += u.get("input_tokens", 0)
                total_output_tokens += u.get("output_tokens", 0)

            messages.append({"role": "assistant", "content": assistant_content})

            # Check for tool use
            tool_blocks = [b for b in assistant_content if hasattr(b, "type") and b.type == "tool_use"]
            if not tool_blocks:
                # No tool use → final answer
                text_parts = [b.text for b in assistant_content if hasattr(b, "text") and b.type == "text"]
                return {
                    "text": "\n".join(text_parts),
                    "tool_calls": tool_call_log,
                    "token_usage": {"input_tokens": total_input_tokens, "output_tokens": total_output_tokens},
                }

            # Process each tool call
            tool_results = []
            for tb in tool_blocks:
                logger.info("[%s] tool_use: %s", self.name, tb.name)
                result_str = await self._handle_tool_call(tb.name, tb.input)
                tool_call_log.append({
                    "tool": tb.name,
                    "input": tb.input,
                    "result": result_str,
                })
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": result_str,
                })

            messages.append({"role": "user", "content": tool_results})

        # Fallback if max iterations reached
        return {
            "text": "Agent reached maximum iterations without a final answer.",
            "tool_calls": tool_call_log,
            "token_usage": {"input_tokens": total_input_tokens, "output_tokens": total_output_tokens},
        }
