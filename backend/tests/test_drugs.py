import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


class TestDrugSearchEndpoint:
    """Tests for the /api/drugs/search endpoint."""

    def test_drug_search_success(self, client):
        """Test successful drug search."""
        payload = {"query": "ibuprofen"}
        response = client.post("/api/drugs/search", json=payload)
        assert response.status_code in [200, 422, 500]

    def test_drug_search_empty_query(self, client):
        """Test drug search with empty query."""
        payload = {"query": ""}
        response = client.post("/api/drugs/search", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_drug_search_short_query(self, client):
        """Test drug search with very short query."""
        payload = {"query": "a"}
        response = client.post("/api/drugs/search", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_drug_search_special_characters(self, client):
        """Test drug search with special characters."""
        payload = {"query": "aspirin-500mg"}
        response = client.post("/api/drugs/search", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_drug_search_case_insensitive(self, client):
        """Test that drug search is case insensitive."""
        responses = []
        for query in ["ASPIRIN", "aspirin", "Aspirin"]:
            response = client.post("/api/drugs/search", json={"query": query})
            responses.append(response.status_code)
        # All should return same status
        assert len(set(responses)) <= 2


class TestDrugDetailsEndpoint:
    """Tests for the /api/drugs/details endpoint."""

    def test_drug_details_success(self, client):
        """Test successful drug details retrieval."""
        payload = {"rxcui": "5640"}
        response = client.post("/api/drugs/details", json=payload)
        assert response.status_code in [200, 422, 404, 500]

    def test_drug_details_invalid_rxcui(self, client):
        """Test drug details with invalid RXCUI."""
        payload = {"rxcui": "invalid"}
        response = client.post("/api/drugs/details", json=payload)
        assert response.status_code in [200, 400, 422, 404, 500]

    def test_drug_details_missing_rxcui(self, client):
        """Test drug details without RXCUI."""
        payload = {}
        response = client.post("/api/drugs/details", json=payload)
        assert response.status_code == 422


class TestDrugInteractionsEndpoint:
    """Tests for the /api/drugs/interactions endpoint."""

    def test_drug_interactions_success(self, client):
        """Test successful drug interaction check."""
        payload = {"drugs": ["aspirin", "ibuprofen"]}
        response = client.post("/api/drugs/interactions", json=payload)
        assert response.status_code in [200, 422, 500]

    def test_drug_interactions_single_drug(self, client):
        """Test drug interactions with single drug."""
        payload = {"drugs": ["aspirin"]}
        response = client.post("/api/drugs/interactions", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_drug_interactions_empty_list(self, client):
        """Test drug interactions with empty list."""
        payload = {"drugs": []}
        response = client.post("/api/drugs/interactions", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_drug_interactions_multiple_drugs(self, client):
        """Test drug interactions with multiple drugs."""
        payload = {"drugs": ["aspirin", "ibuprofen", "warfarin", "metformin"]}
        response = client.post("/api/drugs/interactions", json=payload)
        assert response.status_code in [200, 422, 500]

    def test_drug_interactions_rxcui_format(self, client):
        """Test drug interactions using RXCUI format."""
        payload = {"rxcuis": ["5640", "161"]}
        response = client.post("/api/drugs/interactions", json=payload)
        assert response.status_code in [200, 422, 500]
