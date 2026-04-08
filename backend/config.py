"""
Centralized configuration for the AI Medical Diagnosis Assistant backend.
All hardcoded values (URLs, timeouts, model names) belong here.
"""

import os

# Ollama (local LLM)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_URL = f"{OLLAMA_BASE_URL}/v1"
OLLAMA_VERSION_URL = f"{OLLAMA_BASE_URL}/api/version"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "180.0"))
OLLAMA_CONNECT_TIMEOUT = 10.0
OLLAMA_HEALTH_CHECK_TIMEOUT = 5.0

# Agent timeouts (seconds)
AGENT_TIMEOUT_CLOUD = float(os.getenv("AGENT_TIMEOUT", "180.0"))
AGENT_TIMEOUT_OLLAMA = float(os.getenv("AGENT_TIMEOUT_OLLAMA", "180.0"))
# Specialist/Treatment get more time (larger context, tool use)
AGENT_TIMEOUT_HEAVY = float(os.getenv("AGENT_TIMEOUT_HEAVY", "240.0"))
