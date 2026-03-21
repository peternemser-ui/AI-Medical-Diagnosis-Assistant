"""
Multi-vendor LLM client abstraction.

Provides a unified interface for calling different AI providers (Anthropic, OpenAI, Google)
while maintaining tool-use support for the agent pipeline.
"""

from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Vendor → model catalog
MODEL_CATALOG = {
    # Anthropic
    "claude-opus-4-6": {"vendor": "anthropic", "model_id": "claude-opus-4-6"},
    "claude-sonnet-4-6": {"vendor": "anthropic", "model_id": "claude-sonnet-4-6"},
    "claude-haiku-4-5": {"vendor": "anthropic", "model_id": "claude-haiku-4-5-20251001"},
    # OpenAI
    "gpt-4o": {"vendor": "openai", "model_id": "gpt-4o"},
    "gpt-4o-mini": {"vendor": "openai", "model_id": "gpt-4o-mini"},
    "o3": {"vendor": "openai", "model_id": "o3"},
    "o4-mini": {"vendor": "openai", "model_id": "o4-mini"},
    # Google
    "gemini-2.5-pro": {"vendor": "google", "model_id": "gemini-2.5-pro-preview-06-05"},
    "gemini-2.5-flash": {"vendor": "google", "model_id": "gemini-2.5-flash-preview-05-20"},
    "gemini-2.0-flash": {"vendor": "google", "model_id": "gemini-2.0-flash"},
    # Ollama (local)
    "llama3.1:8b": {"vendor": "ollama", "model_id": "llama3.1:8b"},
    "llama3.1": {"vendor": "ollama", "model_id": "llama3.1:8b"},
    "mistral": {"vendor": "ollama", "model_id": "mistral"},
    "gemma2": {"vendor": "ollama", "model_id": "gemma2:9b"},
}


def get_vendor(model_name: str) -> str:
    """Get the vendor for a model name."""
    entry = MODEL_CATALOG.get(model_name)
    if entry:
        return entry["vendor"]
    # Infer from name prefix
    if model_name.startswith("claude"):
        return "anthropic"
    if model_name.startswith(("gpt-", "o1", "o3", "o4")):
        return "openai"
    if model_name.startswith("gemini"):
        return "google"
    if model_name.startswith(("llama", "mistral", "gemma", "phi", "qwen", "deepseek", "codellama")):
        return "ollama"
    return "anthropic"  # default


def resolve_model_id(model_name: str) -> str:
    """Resolve a friendly model name to its API model ID."""
    entry = MODEL_CATALOG.get(model_name)
    return entry["model_id"] if entry else model_name


class LLMClient:
    """
    Unified LLM client that dispatches to the appropriate vendor SDK.

    Usage:
        client = LLMClient(
            anthropic_key="sk-ant-...",
            openai_key="sk-...",
            google_key="AIza...",
        )
        response = await client.create_message(
            model="gpt-4o",
            system="You are a doctor.",
            messages=[{"role": "user", "content": "Diagnose this..."}],
            tools=[...],
            max_tokens=4096,
            temperature=0.3,
        )
        # response = {"content": [...], "stop_reason": "end_turn"|"tool_use"}
    """

    def __init__(
        self,
        anthropic_key: str | None = None,
        openai_key: str | None = None,
        google_key: str | None = None,
    ):
        self._anthropic_key = anthropic_key
        self._openai_key = openai_key
        self._google_key = google_key
        self._clients: dict[str, Any] = {}

    def _get_anthropic(self):
        if "anthropic" not in self._clients:
            from anthropic import AsyncAnthropic
            self._clients["anthropic"] = AsyncAnthropic(api_key=self._anthropic_key)
        return self._clients["anthropic"]

    def _get_openai(self):
        if "openai" not in self._clients:
            from openai import AsyncOpenAI
            self._clients["openai"] = AsyncOpenAI(api_key=self._openai_key)
        return self._clients["openai"]

    def _get_google(self):
        if "google" not in self._clients:
            from google import genai
            self._clients["google"] = genai.Client(api_key=self._google_key)
        return self._clients["google"]

    def _get_ollama(self):
        if "ollama" not in self._clients:
            import httpx
            from openai import AsyncOpenAI
            self._clients["ollama"] = AsyncOpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",  # Ollama doesn't need a real key
                http_client=httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)),
            )
        return self._clients["ollama"]

    async def create_message(
        self,
        model: str,
        system: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """
        Create a message using the appropriate vendor.

        Returns a normalized response:
        {
            "content": [{"type": "text", "text": "..."} | {"type": "tool_use", ...}],
            "stop_reason": "end_turn" | "tool_use"
        }
        """
        vendor = get_vendor(model)
        model_id = resolve_model_id(model)

        if vendor == "anthropic":
            return await self._call_anthropic(model_id, system, messages, tools, max_tokens, temperature)
        elif vendor == "openai":
            return await self._call_openai(model_id, system, messages, tools, max_tokens, temperature)
        elif vendor == "google":
            return await self._call_google(model_id, system, messages, tools, max_tokens, temperature)
        elif vendor == "ollama":
            return await self._call_ollama(model_id, system, messages, tools, max_tokens, temperature)
        else:
            raise ValueError(f"Unknown vendor for model: {model}")

    # ── Anthropic ──────────────────────────────────────────────────

    async def _call_anthropic(self, model_id, system, messages, tools, max_tokens, temperature):
        client = self._get_anthropic()
        kwargs = dict(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
        )
        if tools:
            kwargs["tools"] = tools

        response = await client.messages.create(**kwargs)

        # Already in the right format — Anthropic response.content is a list of blocks
        return {
            "content": response.content,
            "stop_reason": response.stop_reason,
        }

    # ── OpenAI ─────────────────────────────────────────────────────

    async def _call_openai(self, model_id, system, messages, tools, max_tokens, temperature):
        client = self._get_openai()

        # Convert Anthropic-style messages to OpenAI format
        oai_messages = [{"role": "system", "content": system}]
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if isinstance(content, str):
                oai_messages.append({"role": role, "content": content})
            elif isinstance(content, list):
                # Handle tool_result blocks (from agent loop)
                if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_result":
                            oai_messages.append({
                                "role": "tool",
                                "tool_call_id": block.get("tool_use_id", ""),
                                "content": block.get("content", ""),
                            })
                else:
                    # Multi-part content (text + images) or assistant content blocks
                    parts = []
                    tool_calls = []
                    for block in content:
                        if hasattr(block, "type"):
                            # Anthropic SDK content block objects
                            if block.type == "text":
                                parts.append({"type": "text", "text": block.text})
                            elif block.type == "tool_use":
                                tool_calls.append({
                                    "id": block.id,
                                    "type": "function",
                                    "function": {
                                        "name": block.name,
                                        "arguments": json.dumps(block.input),
                                    },
                                })
                        elif isinstance(block, dict):
                            if block.get("type") == "text":
                                parts.append(block)
                            elif block.get("type") == "image":
                                # Convert base64 image to OpenAI format
                                src = block.get("source", {})
                                parts.append({
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{src.get('media_type', 'image/jpeg')};base64,{src.get('data', '')}",
                                    },
                                })

                    if tool_calls:
                        oai_messages.append({
                            "role": "assistant",
                            "content": parts[0]["text"] if parts else None,
                            "tool_calls": tool_calls,
                        })
                    elif parts:
                        oai_messages.append({"role": role, "content": parts})

        # Convert Anthropic tools to OpenAI function format
        oai_tools = None
        if tools:
            oai_tools = []
            for tool in tools:
                oai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("input_schema", {"type": "object", "properties": {}}),
                    },
                })

        kwargs = dict(
            model=model_id,
            messages=oai_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        if oai_tools:
            kwargs["tools"] = oai_tools

        response = await client.chat.completions.create(**kwargs)
        choice = response.choices[0]

        # Normalize to Anthropic-like format
        content = []
        if choice.message.content:
            content.append(type("TextBlock", (), {"type": "text", "text": choice.message.content})())

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                content.append(type("ToolUseBlock", (), {
                    "type": "tool_use",
                    "id": tc.id,
                    "name": tc.function.name,
                    "input": json.loads(tc.function.arguments),
                })())

        stop_reason = "tool_use" if choice.message.tool_calls else "end_turn"
        return {"content": content, "stop_reason": stop_reason}

    # ── Ollama (local, OpenAI-compatible) ────────────────────────

    async def _call_ollama(self, model_id, system, messages, tools, max_tokens, temperature):
        """Call Ollama using the OpenAI-compatible API (no tool support)."""
        client = self._get_ollama()

        # Cap max_tokens for local models to prevent very slow generation
        max_tokens = min(max_tokens, 1500)

        # Trim system prompt for Ollama — keep it under 2000 chars for speed
        if len(system) > 2000:
            system = system[:1900] + "\n\n[System prompt trimmed for local model. Provide a concise clinical analysis.]"

        # Build simple message list — Ollama doesn't support tool use well,
        # so we skip tools and just use text messages
        oai_messages = [{"role": "system", "content": system}]
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if isinstance(content, str):
                oai_messages.append({"role": role, "content": content})
            elif isinstance(content, list):
                # Flatten multi-part content to text
                text_parts = []
                for block in content:
                    if hasattr(block, "text"):
                        text_parts.append(block.text)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif isinstance(block, dict) and block.get("type") == "tool_result":
                        text_parts.append(str(block.get("content", "")))
                if text_parts:
                    oai_messages.append({"role": role, "content": "\n".join(text_parts)})

        try:
            response = await client.chat.completions.create(
                model=model_id,
                messages=oai_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            text = response.choices[0].message.content or ""
            return {
                "content": [type("TextBlock", (), {"type": "text", "text": text})()],
                "stop_reason": "end_turn",
            }
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            raise

    # ── Google Gemini ──────────────────────────────────────────────

    async def _call_google(self, model_id, system, messages, tools, max_tokens, temperature):
        client = self._get_google()
        from google.genai import types

        # Build contents from messages
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            content = msg["content"]

            if isinstance(content, str):
                contents.append(types.Content(role=role, parts=[types.Part.from_text(content)]))
            elif isinstance(content, list):
                parts = []
                for block in content:
                    if hasattr(block, "type") and block.type == "text":
                        parts.append(types.Part.from_text(block.text))
                    elif isinstance(block, dict) and block.get("type") == "text":
                        parts.append(types.Part.from_text(block["text"]))
                    elif isinstance(block, dict) and block.get("type") == "tool_result":
                        parts.append(types.Part.from_text(block.get("content", "")))
                if parts:
                    contents.append(types.Content(role=role, parts=parts))

        # Convert tools to Gemini function declarations
        gemini_tools = None
        if tools:
            func_decls = []
            for tool in tools:
                schema = tool.get("input_schema", {})
                func_decls.append(types.FunctionDeclaration(
                    name=tool["name"],
                    description=tool.get("description", ""),
                    parameters=schema if schema.get("properties") else None,
                ))
            gemini_tools = [types.Tool(function_declarations=func_decls)]

        config = types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
            temperature=temperature,
            tools=gemini_tools,
        )

        response = await client.aio.models.generate_content(
            model=model_id,
            contents=contents,
            config=config,
        )

        # Normalize response
        content = []
        for part in response.candidates[0].content.parts:
            if part.text:
                content.append(type("TextBlock", (), {"type": "text", "text": part.text})())
            elif part.function_call:
                content.append(type("ToolUseBlock", (), {
                    "type": "tool_use",
                    "id": f"gemini_{id(part)}",
                    "name": part.function_call.name,
                    "input": dict(part.function_call.args) if part.function_call.args else {},
                })())

        has_tool_calls = any(hasattr(b, "type") and b.type == "tool_use" for b in content)
        return {"content": content, "stop_reason": "tool_use" if has_tool_calls else "end_turn"}
