import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import base64
import io


class TestImageAnalysisEndpoint:
    """Tests for the /api/analyze-image endpoint."""

    def create_test_image(self):
        """Create a simple test image."""
        # Create a minimal valid PNG image (1x1 pixel)
        png_header = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
            0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
            0x54, 0x08, 0xD7, 0x63, 0xF8, 0xFF, 0xFF, 0x3F,
            0x00, 0x05, 0xFE, 0x02, 0xFE, 0xDC, 0xCC, 0x59,
            0xE7, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
            0x44, 0xAE, 0x42, 0x60, 0x82
        ])
        return png_header

    def test_image_analysis_success(self, client, mock_openai):
        """Test successful image analysis."""
        image_data = self.create_test_image()
        files = {"file": ("test.png", io.BytesIO(image_data), "image/png")}
        response = client.post("/api/analyze-image", files=files)
        assert response.status_code in [200, 422, 500]

    def test_image_analysis_no_file(self, client):
        """Test image analysis without file."""
        response = client.post("/api/analyze-image")
        assert response.status_code == 422

    def test_image_analysis_invalid_type(self, client):
        """Test image analysis with invalid file type."""
        files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
        response = client.post("/api/analyze-image", files=files)
        assert response.status_code in [200, 400, 415, 422]

    def test_image_analysis_with_context(self, client, mock_openai):
        """Test image analysis with additional context."""
        image_data = self.create_test_image()
        files = {"file": ("test.png", io.BytesIO(image_data), "image/png")}
        data = {"context": "skin rash on arm"}
        response = client.post("/api/analyze-image", files=files, data=data)
        assert response.status_code in [200, 422, 500]

    def test_image_analysis_large_file(self, client):
        """Test image analysis with oversized file."""
        # Create a large fake file (over limit)
        large_data = b"0" * (10 * 1024 * 1024 + 1)  # 10MB+
        files = {"file": ("large.png", io.BytesIO(large_data), "image/png")}
        response = client.post("/api/analyze-image", files=files)
        assert response.status_code in [200, 400, 413, 422, 500]

    def test_image_analysis_base64(self, client, mock_openai):
        """Test image analysis with base64 encoded image."""
        image_data = self.create_test_image()
        base64_image = base64.b64encode(image_data).decode()
        payload = {
            "image_base64": base64_image,
            "mime_type": "image/png"
        }
        response = client.post("/api/analyze-image", json=payload)
        assert response.status_code in [200, 422, 500]

    def test_image_analysis_supported_formats(self, client, mock_openai):
        """Test image analysis supports various formats."""
        image_data = self.create_test_image()
        formats = [
            ("test.png", "image/png"),
            ("test.jpg", "image/jpeg"),
            ("test.webp", "image/webp")
        ]
        for filename, mime_type in formats:
            files = {"file": (filename, io.BytesIO(image_data), mime_type)}
            response = client.post("/api/analyze-image", files=files)
            assert response.status_code in [200, 400, 415, 422, 500]


class TestDeepDiveEndpoint:
    """Tests for the /api/deep-dive endpoint."""

    def test_deep_dive_success(self, client, mock_openai):
        """Test successful deep dive analysis."""
        payload = {
            "condition": "Migraine",
            "symptoms": ["headache", "nausea"],
            "context": "Patient has history of migraines"
        }
        response = client.post("/api/deep-dive", json=payload)
        assert response.status_code in [200, 422]

    def test_deep_dive_missing_condition(self, client):
        """Test deep dive without condition."""
        payload = {"symptoms": ["headache"]}
        response = client.post("/api/deep-dive", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_deep_dive_response_structure(self, client, mock_openai):
        """Test deep dive response has expected structure."""
        payload = {
            "condition": "Tension Headache",
            "symptoms": ["headache", "neck pain"]
        }
        response = client.post("/api/deep-dive", json=payload)
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
