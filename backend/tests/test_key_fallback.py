"""Tests for API key resolution and fallback logic.

Covers:
  1. _resolve_key_with_fallback — priority ordering
  2. _resolve_key_with_fallback — excluding failed providers
  3. _is_auth_or_key_error — detecting auth-related errors
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import _resolve_key_with_fallback, _is_auth_or_key_error


def _mock_httpx_ok():
    """Create a mock httpx module where get() returns 200."""
    mock = MagicMock()
    mock.get.return_value = MagicMock(status_code=200)
    return mock


def _mock_httpx_fail():
    """Create a mock httpx module where get() raises an error."""
    mock = MagicMock()
    mock.get.side_effect = ConnectionError("Ollama not running")
    return mock


class TestResolveKeyAnthropicFirst:

    def test_auto_mode_prefers_anthropic(self):
        """Auto mode should prefer anthropic when all keys are available."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("auto", keys)
        assert provider == "anthropic"
        assert key == "sk-ant-123"

    def test_auto_mode_falls_back_to_openai(self):
        """When anthropic is missing, auto should fall back to openai."""
        keys = {"anthropic": None, "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("auto", keys)
        assert provider == "openai"
        assert key == "sk-456"

    def test_auto_mode_falls_back_to_google(self):
        """When anthropic and openai are missing, auto should fall back to google."""
        keys = {"anthropic": None, "openai": None, "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("auto", keys)
        assert provider == "google"
        assert key == "AIza-789"

    def test_auto_mode_no_keys_tries_ollama(self):
        """When no cloud keys are available, should try Ollama."""
        mock_httpx = _mock_httpx_ok()
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            keys = {"anthropic": None, "openai": None, "google": None}
            key, provider = _resolve_key_with_fallback("auto", keys)
            assert provider == "ollama"
            assert key == "ollama"

    def test_auto_mode_no_keys_no_ollama(self):
        """When no keys and no Ollama, should return none."""
        mock_httpx = _mock_httpx_fail()
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            keys = {"anthropic": None, "openai": None, "google": None}
            key, provider = _resolve_key_with_fallback("auto", keys)
            assert provider == "none"
            assert key is None

    def test_gpt_model_prefers_openai(self):
        """GPT model preference should prefer openai."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("gpt-4o", keys)
        assert provider == "openai"
        assert key == "sk-456"

    def test_gemini_model_prefers_google(self):
        """Gemini model preference should prefer google."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("gemini-2.0", keys)
        assert provider == "google"
        assert key == "AIza-789"

    def test_sonnet_model_prefers_anthropic(self):
        """Sonnet model preference should prefer anthropic."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("sonnet", keys)
        assert provider == "anthropic"
        assert key == "sk-ant-123"

    def test_haiku_model_prefers_anthropic(self):
        """Haiku model preference should prefer anthropic."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": None}
        key, provider = _resolve_key_with_fallback("haiku", keys)
        assert provider == "anthropic"

    def test_gpt_falls_back_to_anthropic(self):
        """GPT model preference should fall back to anthropic if openai is missing."""
        keys = {"anthropic": "sk-ant-123", "openai": None, "google": None}
        key, provider = _resolve_key_with_fallback("gpt-4o", keys)
        assert provider == "anthropic"


class TestResolveKeyExcludesFailed:

    def test_excludes_single_provider(self):
        """Should skip excluded providers and use next in order."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("auto", keys, exclude_providers=["anthropic"])
        assert provider == "openai"
        assert key == "sk-456"

    def test_excludes_multiple_providers(self):
        """Should skip multiple excluded providers."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
        key, provider = _resolve_key_with_fallback("auto", keys, exclude_providers=["anthropic", "openai"])
        assert provider == "google"
        assert key == "AIza-789"

    def test_excludes_all_cloud_tries_ollama(self):
        """When all cloud providers are excluded, should try Ollama."""
        mock_httpx = _mock_httpx_ok()
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
            key, provider = _resolve_key_with_fallback(
                "auto", keys, exclude_providers=["anthropic", "openai", "google"]
            )
            assert provider == "ollama"

    def test_excludes_all_including_ollama(self):
        """When everything is excluded, should return none."""
        mock_httpx = _mock_httpx_fail()
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": "AIza-789"}
            key, provider = _resolve_key_with_fallback(
                "auto", keys, exclude_providers=["anthropic", "openai", "google", "ollama"]
            )
            assert provider == "none"
            assert key is None

    def test_exclude_does_not_affect_unexcluded(self):
        """Excluding openai should not affect anthropic priority in auto mode."""
        keys = {"anthropic": "sk-ant-123", "openai": "sk-456", "google": None}
        key, provider = _resolve_key_with_fallback("auto", keys, exclude_providers=["openai"])
        assert provider == "anthropic"


class TestIsAuthError:

    def test_detects_401_unauthorized(self):
        """Should detect 401 unauthorized errors."""
        err = Exception("Request failed with status 401 Unauthorized")
        assert _is_auth_or_key_error(err) is True

    def test_detects_403_forbidden(self):
        """Should detect 403 forbidden errors."""
        err = Exception("403 Forbidden: access denied")
        assert _is_auth_or_key_error(err) is True

    def test_detects_invalid_api_key(self):
        """Should detect invalid API key errors."""
        err = Exception("Error: invalid_api_key - The API key provided is invalid")
        assert _is_auth_or_key_error(err) is True

    def test_detects_authentication_error(self):
        """Should detect authentication failure messages."""
        err = Exception("Authentication failed: bad credentials")
        assert _is_auth_or_key_error(err) is True

    def test_detects_rate_limit(self):
        """Should detect rate limit / 429 errors."""
        err = Exception("Rate limit exceeded (429)")
        assert _is_auth_or_key_error(err) is True

    def test_detects_quota_error(self):
        """Should detect quota exceeded errors."""
        err = Exception("You have exceeded your quota")
        assert _is_auth_or_key_error(err) is True

    def test_detects_billing_error(self):
        """Should detect billing-related errors."""
        err = Exception("Billing issue: payment required")
        assert _is_auth_or_key_error(err) is True

    def test_detects_overloaded_529(self):
        """Should detect overloaded/529 errors."""
        err = Exception("API overloaded (529)")
        assert _is_auth_or_key_error(err) is True

    def test_does_not_flag_timeout(self):
        """Should NOT flag timeout errors as auth errors."""
        err = Exception("Request timed out after 30 seconds")
        assert _is_auth_or_key_error(err) is False

    def test_does_not_flag_network_error(self):
        """Should NOT flag network connectivity errors."""
        err = Exception("Connection refused: server unreachable")
        assert _is_auth_or_key_error(err) is False

    def test_does_not_flag_json_parse_error(self):
        """Should NOT flag JSON parse errors."""
        err = Exception("JSONDecodeError: Expecting value at line 1")
        assert _is_auth_or_key_error(err) is False

    def test_case_insensitive(self):
        """Should match case-insensitively."""
        err = Exception("AUTHENTICATION FAILED")
        assert _is_auth_or_key_error(err) is True
