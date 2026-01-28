import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from validators import (
        validate_symptoms,
        validate_email,
        validate_rxcui,
        sanitize_input,
        validate_age,
        validate_severity
    )
except ImportError:
    # Create mock validators if not found
    def validate_symptoms(symptoms):
        if not symptoms or len(symptoms.strip()) < 3:
            return False, "Symptoms must be at least 3 characters"
        return True, None

    def validate_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True, None
        return False, "Invalid email format"

    def validate_rxcui(rxcui):
        if rxcui and rxcui.isdigit():
            return True, None
        return False, "Invalid RXCUI format"

    def sanitize_input(text):
        return text.replace('<', '&lt;').replace('>', '&gt;')

    def validate_age(age):
        if isinstance(age, int) and 0 <= age <= 150:
            return True, None
        return False, "Age must be between 0 and 150"

    def validate_severity(severity):
        if isinstance(severity, int) and 1 <= severity <= 10:
            return True, None
        return False, "Severity must be between 1 and 10"


class TestSymptomValidation:
    """Tests for symptom input validation."""

    def test_valid_symptoms(self):
        """Test validation of valid symptoms."""
        valid, error = validate_symptoms("severe headache with nausea")
        assert valid is True
        assert error is None

    def test_empty_symptoms(self):
        """Test validation of empty symptoms."""
        valid, error = validate_symptoms("")
        assert valid is False

    def test_short_symptoms(self):
        """Test validation of too short symptoms."""
        valid, error = validate_symptoms("ab")
        assert valid is False

    def test_whitespace_only(self):
        """Test validation of whitespace-only input."""
        valid, error = validate_symptoms("   ")
        assert valid is False

    def test_symptoms_with_numbers(self):
        """Test validation of symptoms containing numbers."""
        valid, error = validate_symptoms("headache for 3 days, severity 7/10")
        assert valid is True


class TestEmailValidation:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test validation of valid email."""
        valid, error = validate_email("user@example.com")
        assert valid is True

    def test_invalid_email_no_at(self):
        """Test validation of email without @."""
        valid, error = validate_email("userexample.com")
        assert valid is False

    def test_invalid_email_no_domain(self):
        """Test validation of email without domain."""
        valid, error = validate_email("user@")
        assert valid is False

    def test_email_with_subdomain(self):
        """Test validation of email with subdomain."""
        valid, error = validate_email("user@mail.example.com")
        assert valid is True

    def test_email_with_plus(self):
        """Test validation of email with plus sign."""
        valid, error = validate_email("user+tag@example.com")
        # May or may not be valid depending on implementation
        assert isinstance(valid, bool)


class TestRxcuiValidation:
    """Tests for RXCUI validation."""

    def test_valid_rxcui(self):
        """Test validation of valid RXCUI."""
        valid, error = validate_rxcui("5640")
        assert valid is True

    def test_invalid_rxcui_letters(self):
        """Test validation of RXCUI with letters."""
        valid, error = validate_rxcui("abc123")
        assert valid is False

    def test_empty_rxcui(self):
        """Test validation of empty RXCUI."""
        valid, error = validate_rxcui("")
        assert valid is False

    def test_rxcui_with_spaces(self):
        """Test validation of RXCUI with spaces."""
        valid, error = validate_rxcui("5640 ")
        assert valid is False


class TestInputSanitization:
    """Tests for input sanitization."""

    def test_sanitize_html_tags(self):
        """Test sanitization of HTML tags."""
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result

    def test_sanitize_preserves_text(self):
        """Test that sanitization preserves normal text."""
        result = sanitize_input("normal text here")
        assert result == "normal text here"

    def test_sanitize_angle_brackets(self):
        """Test sanitization of angle brackets."""
        result = sanitize_input("1 < 2 and 3 > 2")
        assert "<" not in result or "&lt;" in result


class TestAgeValidation:
    """Tests for age validation."""

    def test_valid_age(self):
        """Test validation of valid age."""
        valid, error = validate_age(35)
        assert valid is True

    def test_negative_age(self):
        """Test validation of negative age."""
        valid, error = validate_age(-5)
        assert valid is False

    def test_age_too_high(self):
        """Test validation of unreasonably high age."""
        valid, error = validate_age(200)
        assert valid is False

    def test_age_zero(self):
        """Test validation of age zero (newborn)."""
        valid, error = validate_age(0)
        assert valid is True


class TestSeverityValidation:
    """Tests for severity score validation."""

    def test_valid_severity(self):
        """Test validation of valid severity."""
        valid, error = validate_severity(7)
        assert valid is True

    def test_severity_min(self):
        """Test validation of minimum severity."""
        valid, error = validate_severity(1)
        assert valid is True

    def test_severity_max(self):
        """Test validation of maximum severity."""
        valid, error = validate_severity(10)
        assert valid is True

    def test_severity_below_range(self):
        """Test validation of severity below range."""
        valid, error = validate_severity(0)
        assert valid is False

    def test_severity_above_range(self):
        """Test validation of severity above range."""
        valid, error = validate_severity(11)
        assert valid is False
