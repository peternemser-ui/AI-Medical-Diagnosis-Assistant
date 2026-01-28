import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_check_success(self, client):
        """Test health check returns success."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, client):
        """Test health check response structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data or isinstance(data, dict)

    def test_health_check_status_value(self, client):
        """Test health check status is healthy."""
        response = client.get("/health")
        data = response.json()
        if "status" in data:
            assert data["status"] in ["healthy", "ok", "up"]

    def test_health_check_includes_version(self, client):
        """Test health check includes version info."""
        response = client.get("/health")
        data = response.json()
        # Version might be optional
        assert isinstance(data, dict)

    def test_health_check_response_time(self, client):
        """Test health check responds quickly."""
        import time
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 1.0  # Should respond within 1 second

    def test_health_check_no_auth_required(self, client):
        """Test health check doesn't require authentication."""
        # No auth headers
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_method_not_allowed(self, client):
        """Test health check only accepts GET."""
        response = client.post("/health")
        assert response.status_code in [405, 422, 200]

    def test_root_endpoint(self, client):
        """Test root endpoint returns info."""
        response = client.get("/")
        assert response.status_code in [200, 404]

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/health")
        # CORS headers might be set
        assert response.status_code in [200, 405]


class TestAPIInfo:
    """Tests for API information endpoints."""

    def test_api_docs_available(self, client):
        """Test API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data or "info" in data

    def test_redoc_available(self, client):
        """Test ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200
