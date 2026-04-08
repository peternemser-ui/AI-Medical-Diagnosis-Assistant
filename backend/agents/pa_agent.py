"""
PA (Physician's Assistant) Interview Agent

Conducts a contextual clinical intake interview, then routes the patient
to the appropriate specialist doctor agent(s) for diagnosis.
"""

import json
import logging
from .base import BaseAgent

logger = logging.getLogger(__name__)

# Short prompt optimized for Ollama JSON reliability
_PA_SYSTEM_PROMPT = """You are a medical PA interviewing a patient. Ask ONE question at a time about their symptoms.

RULES:
- Ask relevant follow-up questions about their specific condition
- Gather: onset, severity, duration, triggers, medical history, medications, allergies
- After 6+ questions with enough info, route to a specialist
- Do NOT ask generic pain questions for non-pain conditions

RESPOND WITH JSON ONLY:
To ask: {"action":"ask","question":"your question here"}
To route: {"action":"route","routing":{"specialties":["dermatology"],"urgency":"routine","patient_summary":"summary","chief_complaint":"complaint"}}

Specialties: cardiology, dermatology, neurology, gastroenterology, psychiatry, pulmonology, endocrinology, orthopedics, general_medicine
"""


class PAInterviewAgent(BaseAgent):
    """Physician's Assistant that conducts clinical interviews and routes to specialists."""

    name = "pa_interview"
    description = "Physician's Assistant — conducts clinical intake interviews and routes to specialist doctors"
    model = "claude-sonnet-4-20250514"
    max_tokens = 800
    temperature = 0.4

    def _build_system_prompt(self):
        return _PA_SYSTEM_PROMPT

    def _get_tools(self):
        return []  # No tools — JSON-only for Ollama compatibility

    async def interview(self, conversation: list[dict], age: int = 0, gender: str = "unknown",
                        model_preference: str | None = None, language_instruction: str = "") -> dict:
        """
        Run one round of the PA interview.

        Args:
            conversation: List of {role: "user"|"assistant", content: "..."} messages
            age: Patient age
            gender: Patient gender
            model_preference: Optional model override

        Returns:
            dict with 'action' ("ask" or "route"), plus 'question' or 'routing'
        """
        if model_preference:
            self.model = model_preference

        # Count user exchanges
        exchange_count = len([m for m in conversation if m.get("role") == "user"])

        # Build conversation transcript as a single user message for the LLM
        lines = [f"Patient: {age}-year-old {gender}. This is exchange {exchange_count}/15.{language_instruction}"]
        if exchange_count >= 14:
            lines.append("YOU MUST route to a specialist now — maximum exchanges reached.")
        elif exchange_count >= 6:
            lines.append("You may route to a specialist if you have collected sufficient clinical data.")

        lines.append("\n--- CONVERSATION SO FAR ---")
        for msg in conversation:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if content:
                speaker = "PATIENT" if role == "user" else "PA"
                lines.append(f"{speaker}: {content}")
        lines.append("--- END CONVERSATION ---")
        lines.append("\nBased on the conversation above, respond with your next action as JSON.")

        user_message = "\n".join(lines)

        # Run through the LLM (uses BaseAgent.run with use_tools=False)
        try:
            result = await self.run(
                user_message=user_message,
                context=None,
                use_tools=False,
            )

            # Parse the response
            return self._parse_response(result.get("text", ""), exchange_count)

        except Exception as e:
            logger.error("PA interview failed: %s", e, exc_info=True)
            # On failure, return a safe fallback question
            if exchange_count < 3:
                return {
                    "action": "ask",
                    "question": "What brings you in today? Please describe your main concern.",
                    "exchange_count": exchange_count
                }
            else:
                # If we've had enough exchanges, route to general medicine
                return {
                    "action": "route",
                    "routing": {
                        "specialties": ["general_medicine"],
                        "urgency": "routine",
                        "patient_summary": "Interview incomplete due to error. Manual review needed.",
                        "chief_complaint": "See conversation history"
                    }
                }

    def _parse_response(self, text: str, exchange_count: int) -> dict:
        """Parse the PA's JSON response with aggressive fallback handling for Ollama."""
        import re

        # Strip markdown code blocks
        clean = re.sub(r'```(?:json)?\s*|\s*```', '', text).strip()

        # Strategy 1: Direct JSON parse
        try:
            parsed = json.loads(clean)
            if isinstance(parsed, dict):
                parsed["exchange_count"] = exchange_count
                # Normalize action field
                if "action" not in parsed:
                    if "question" in parsed or "response" in parsed:
                        parsed["action"] = "ask"
                        parsed["question"] = parsed.get("question") or parsed.get("response", "")
                    elif "routing" in parsed or "specialties" in parsed:
                        parsed["action"] = "route"
                return parsed
        except json.JSONDecodeError:
            pass

        # Strategy 2: Find JSON object in text
        for match in re.finditer(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', clean):
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, dict):
                    parsed["exchange_count"] = exchange_count
                    if "action" not in parsed:
                        if "question" in parsed or "response" in parsed:
                            parsed["action"] = "ask"
                            parsed["question"] = parsed.get("question") or parsed.get("response", "")
                    return parsed
            except json.JSONDecodeError:
                continue

        # Strategy 3: Extract a question from plain text (Ollama sometimes just writes a question)
        logger.warning("PA response not JSON, extracting question from text: %s", clean[:200])

        # Remove any JSON-like fragments
        plain = re.sub(r'\{[^}]*\}', '', clean).strip()
        # Look for a sentence ending with ?
        q_match = re.search(r'([A-Z][^.!?]*\?)', plain)
        if q_match:
            return {"action": "ask", "question": q_match.group(1).strip(), "exchange_count": exchange_count}

        # Take the first substantial sentence
        sentences = [s.strip() for s in re.split(r'[.!?\n]', plain) if len(s.strip()) > 15]
        if sentences:
            return {"action": "ask", "question": sentences[0] + "?", "exchange_count": exchange_count}

        # Last resort
        return {"action": "ask", "question": "", "exchange_count": exchange_count}
