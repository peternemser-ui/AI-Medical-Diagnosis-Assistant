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

from config import AGENT_TIMEOUT_CLOUD, AGENT_TIMEOUT_OLLAMA

from anthropic import AsyncAnthropic

from .message_bus import Message, MessageBus
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class BaseAgent:
    """Abstract base for all medical agents."""

    name: str = "base_agent"
    description: str = "Base agent"
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 5000
    temperature: float = 0.3
    reflection_enabled: bool = False

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
    # Output validation
    # ------------------------------------------------------------------

    def _validate_and_parse_output(self, raw_data: dict, schema_class=None) -> dict:
        """Validate agent output against a Pydantic schema, filling defaults for missing fields."""
        if not schema_class:
            return raw_data
        try:
            validated = schema_class.model_validate(raw_data)
            return validated.model_dump(by_alias=False)
        except Exception:
            # Schema validation failed -- return raw with best-effort defaults
            try:
                defaults = schema_class().model_dump()
                for key, val in defaults.items():
                    if key not in raw_data:
                        raw_data[key] = val
            except Exception:
                pass
            return raw_data

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
    # Reflection / Self-Critique
    # ------------------------------------------------------------------

    async def reflect(self, initial_output: str, context: str = "") -> str:
        """Self-critique loop — asks the LLM to review and improve its own output."""
        if not self.reflection_enabled:
            return initial_output

        reflection_prompt = (
            f"You are reviewing your own previous analysis as a {self.description}.\n\n"
            f"=== YOUR INITIAL OUTPUT ===\n{initial_output[:3000]}\n\n"
            f"=== CONTEXT ===\n{context[:1000]}\n\n"
            f"Critically review your analysis:\n"
            f"1. Did you miss any important diagnoses or conditions?\n"
            f"2. Are there cognitive biases (anchoring, availability, premature closure)?\n"
            f"3. Did you adequately consider dangerous 'must-not-miss' conditions?\n"
            f"4. Are your confidence percentages well-calibrated?\n"
            f"5. Would a senior attending physician find any gaps?\n\n"
            f"Provide a REVISED and IMPROVED version of your analysis in the same JSON format. "
            f"If your analysis was already correct, return it unchanged with a note explaining why."
        )

        try:
            reflected = await self.run(reflection_prompt, use_tools=False)
            reflected_text = reflected.get("text", "") if isinstance(reflected, dict) else str(reflected)
            return reflected_text if reflected_text and len(reflected_text) > 50 else initial_output
        except Exception as e:
            logger.warning("Reflection failed for %s: %s", self.name, e)
            return initial_output

    # ------------------------------------------------------------------
    # Core agent loop
    # ------------------------------------------------------------------

    async def run(self, user_message: str, context: dict[str, Any] | None = None, images: list[str] | None = None, timeout: float = None, use_tools: bool = True, max_iterations: int = 8) -> dict[str, Any]:
        """
        Run the autonomous agent loop with a timeout.

        Sends *user_message* to Claude along with the agent's tools.
        Loops over tool_use blocks until Claude produces a final text answer.
        Returns a dict with ``text`` (final answer) and ``tool_calls`` (log).

        If *use_tools* is False, the agent produces a single response without
        any tool use — much faster for structured JSON output.

        If *images* is provided (list of base64-encoded image strings),
        the user message is sent as a multi-part content block so Claude
        can perform visual analysis.
        """
        import asyncio
        from .llm_client import get_vendor
        # Local models (Ollama) need more time per agent
        if timeout is None:
            timeout = AGENT_TIMEOUT_OLLAMA if get_vendor(self.model) == "ollama" else AGENT_TIMEOUT_CLOUD
        try:
            return await asyncio.wait_for(
                self._run_loop(user_message, context, images, use_tools=use_tools, max_iterations=max_iterations),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.error("[%s] Agent timed out after %.0fs", self.name, timeout)
            return {
                "text": f"Agent {self.name} timed out after {timeout:.0f}s. The analysis may be incomplete.",
                "tool_calls": [],
                "timed_out": True,
            }

    async def _run_loop(self, user_message: str, context: dict[str, Any] | None = None, images: list[str] | None = None, use_tools: bool = True, max_iterations: int = 8) -> dict[str, Any]:
        """Internal agent loop — called by run() with timeout wrapper."""
        messages: list[dict] = []

        # Inject context from other agents if available
        if context:
            from .llm_client import get_vendor
            is_local = get_vendor(self.model) in ("ollama",)

            if is_local:
                # Compact context for local models — strip raw_text, limit size
                compact = {}
                for k, v in context.items():
                    if isinstance(v, dict):
                        compact[k] = {ck: cv for ck, cv in v.items()
                                      if ck != "raw_text" and not ck.startswith("_")}
                    else:
                        compact[k] = v
                context_str = json.dumps(compact, indent=1)
                if len(context_str) > 3000:
                    context_str = context_str[:2800] + "\n..."
            else:
                context_str = json.dumps(context, indent=2)

            context_block = "Here is context from other agents on the team:\n" + context_str
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

        tools = self._get_tools() if use_tools else []

        # Fast path: no tools → single API call, return text directly
        if not tools:
            from .llm_client import get_vendor
            use_llm_client = self.llm_client and (get_vendor(self.model) != "anthropic" or self.client is None)
            if use_llm_client:
                resp = await self.llm_client.create_message(
                    model=self.model,
                    system=self._system_prompt,
                    messages=messages,
                    tools=None,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                assistant_content = resp["content"]
                usage = resp.get("usage", {})
            else:
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=self._system_prompt,
                    messages=messages,
                )
                assistant_content = response.content
                usage = {}
                if hasattr(response, "usage"):
                    usage = {"input_tokens": getattr(response.usage, "input_tokens", 0),
                             "output_tokens": getattr(response.usage, "output_tokens", 0)}

            text_parts = [b.text for b in assistant_content if hasattr(b, "text") and b.type == "text"]
            return {
                "text": "\n".join(text_parts),
                "tool_calls": [],
                "token_usage": usage,
            }
        tool_call_log: list[dict] = []
        total_input_tokens = 0
        total_output_tokens = 0
        # max_iterations is now a parameter (default 8), can be overridden per call

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

        # Max iterations reached — ask for a final JSON answer without tools
        logger.warning("[%s] Hit max iterations (%d) — requesting final answer", self.name, max_iterations)
        messages.append({
            "role": "user",
            "content": (
                "You have used all available tool rounds. Please provide your FINAL answer now "
                "as a single JSON object. Do NOT call any more tools. Respond ONLY with valid JSON."
            ),
        })
        try:
            if use_llm_client:
                resp = await self.llm_client.create_message(
                    model=self.model,
                    system=self._system_prompt,
                    messages=messages,
                    tools=None,  # No tools — force text response
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
                    messages=messages,
                )
                assistant_content = response.content

            text_parts = [b.text for b in assistant_content if hasattr(b, "text") and b.type == "text"]
            final_text = "\n".join(text_parts)
            if final_text.strip():
                return {
                    "text": final_text,
                    "tool_calls": tool_call_log,
                    "token_usage": {"input_tokens": total_input_tokens, "output_tokens": total_output_tokens},
                }
        except Exception as e:
            logger.error("[%s] Last-chance answer failed: %s", self.name, e)

        # True fallback — collect any text from the last assistant message
        last_text_parts = []
        if messages:
            last_assistant = [m for m in messages if m.get("role") == "assistant"]
            if last_assistant:
                content = last_assistant[-1].get("content", [])
                if isinstance(content, list):
                    for b in content:
                        if hasattr(b, "text") and hasattr(b, "type") and b.type == "text":
                            last_text_parts.append(b.text)

        return {
            "text": "\n".join(last_text_parts) if last_text_parts else "Agent reached maximum iterations without a final answer.",
            "tool_calls": tool_call_log,
            "token_usage": {"input_tokens": total_input_tokens, "output_tokens": total_output_tokens},
        }
