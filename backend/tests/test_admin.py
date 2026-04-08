"""Comprehensive tests for the backend admin system.

Covers:
  1. MetricsCollector unit tests
  2. CaseStore unit tests
  3. Admin API endpoint integration tests (FastAPI TestClient)
"""

import sys
import os
import time
import math

import pytest

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from admin.metrics import MetricsCollector, get_metrics, _collector
import admin.metrics as metrics_module
from admin.store import CaseStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def collector(tmp_path, monkeypatch):
    """Return a fresh MetricsCollector with no shared state (uses temp dir for persistence)."""
    import admin.metrics as m_mod
    monkeypatch.setattr(m_mod, "_STATE_FILE", tmp_path / "test_state.json")
    monkeypatch.setattr(m_mod, "_DATA_DIR", tmp_path)
    mc = MetricsCollector.__new__(MetricsCollector)
    mc.__init__()
    return mc


@pytest.fixture()
def store():
    """Return a fresh CaseStore."""
    return CaseStore()


@pytest.fixture()
def app_client(collector):
    """Create a FastAPI TestClient that uses the given collector as the singleton."""
    original = metrics_module._collector
    metrics_module._collector = collector

    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    yield client

    # Restore
    metrics_module._collector = original


# ===================================================================
# 1. MetricsCollector unit tests
# ===================================================================

class TestMetricsCollectorInit:

    def test_singleton_pattern(self):
        """get_metrics() returns the same instance on repeated calls."""
        original = metrics_module._collector
        metrics_module._collector = None
        try:
            a = get_metrics()
            b = get_metrics()
            assert a is b
        finally:
            metrics_module._collector = original

    def test_init_agents(self, collector):
        """All 7 pipeline agents are initialised."""
        agents = collector.get_all_agents()
        assert len(agents) == 7
        expected_names = {
            "triage", "diagnostician", "research",
            "specialist", "treatment", "safety", "empathy",
        }
        assert {a["name"] for a in agents} == expected_names

    def test_init_default_config(self, collector):
        """17 config entries are created at init."""
        config = collector.get_config()
        assert len(config) == 17


class TestMetricsCollectorAgents:

    def test_record_agent_call(self, collector):
        """record_agent_call updates latency, success rate, and error count."""
        collector.record_agent_call("triage", 100.0, success=True)
        collector.record_agent_call("triage", 200.0, success=True)
        collector.record_agent_call("triage", 300.0, success=False, error_msg="test error")

        agent = collector.get_agent_health("triage")
        assert agent["cases_processed"] == 3
        assert agent["error_count"] == 1
        assert agent["avg_latency_ms"] == 200.0
        assert agent["success_rate"] == pytest.approx(66.7, abs=0.1)
        assert "test error" in agent["recent_errors"]

    def test_record_agent_execution(self, collector):
        """record_agent_execution stores records retrievable per agent."""
        collector.record_agent_execution(
            "diagnostician", "case-001", 150.0, True,
            model_used="claude-sonnet-4-6",
        )
        collector.record_agent_execution(
            "diagnostician", "case-002", 250.0, False,
            error="timeout", model_used="claude-sonnet-4-6",
        )

        execs = collector.get_agent_executions("diagnostician")
        assert len(execs) == 2
        # Most recent first (appendleft)
        assert execs[0]["case_id"] == "case-002"
        assert execs[0]["success"] is False
        assert execs[1]["case_id"] == "case-001"

        # Also updates agent health
        agent = collector.get_agent_health("diagnostician")
        assert agent["cases_processed"] == 2

    def test_get_agent_detail(self, collector):
        """get_agent_detail returns health, executions, config, dependencies."""
        collector.record_agent_execution("specialist", "c1", 100.0, True)
        detail = collector.get_agent_detail("specialist")

        assert detail is not None
        assert "health" in detail
        assert "recent_executions" in detail
        assert "config" in detail
        assert "dependencies" in detail
        assert "downstream" in detail
        assert detail["health"]["name"] == "specialist"
        assert isinstance(detail["dependencies"], list)
        assert isinstance(detail["downstream"], list)

    def test_get_all_agents(self, collector):
        """get_all_agents returns a list of 7 agent dicts."""
        agents = collector.get_all_agents()
        assert len(agents) == 7
        for a in agents:
            assert "name" in a
            assert "status" in a

    def test_set_agent_status(self, collector):
        """set_agent_status changes agent status and returns old/new."""
        result = collector.set_agent_status("triage", "paused")
        assert result is not None
        assert result["previous_status"] == "healthy"
        assert result["new_status"] == "paused"

        agent = collector.get_agent_health("triage")
        assert agent["status"] == "paused"

        # Resume
        result2 = collector.set_agent_status("triage", "healthy")
        assert result2["previous_status"] == "paused"
        assert result2["new_status"] == "healthy"


class TestMetricsCollectorLogs:

    def test_add_log(self, collector):
        """add_log creates a structured log entry."""
        entry = collector.add_log(
            level="error",
            source="triage",
            message="Something went wrong",
            case_id="case-42",
            agent="triage",
        )
        assert entry["id"].startswith("log-")
        assert entry["level"] == "error"
        assert entry["source"] == "triage"
        assert entry["case_id"] == "case-42"

    def test_get_logs_filtering(self, collector):
        """Logs can be filtered by level, source, agent, case_id, and search text."""
        collector.add_log("info", "system", "Boot complete")
        collector.add_log("error", "triage", "Agent failed", case_id="c1", agent="triage")
        collector.add_log("warning", "safety", "Contraindication found", agent="safety")
        collector.add_log("info", "triage", "Triage done", case_id="c2", agent="triage")

        # Filter by level
        logs, total = collector.get_logs(level="error")
        assert total == 1
        assert logs[0]["level"] == "error"

        # Filter by source
        logs, total = collector.get_logs(source="triage")
        assert total == 2

        # Filter by agent
        logs, total = collector.get_logs(agent="safety")
        assert total == 1

        # Filter by case_id
        logs, total = collector.get_logs(case_id="c1")
        assert total == 1

        # Search text
        logs, total = collector.get_logs(search="contraindication")
        assert total == 1

    def test_get_logs_pagination(self, collector):
        """Logs support offset and limit."""
        for i in range(10):
            collector.add_log("info", "system", f"Message {i}")

        logs, total = collector.get_logs(limit=3, offset=0)
        assert len(logs) == 3
        assert total == 10

        logs2, _ = collector.get_logs(limit=3, offset=3)
        assert len(logs2) == 3
        # Should be different entries
        assert logs[0]["id"] != logs2[0]["id"]


class TestMetricsCollectorConfig:

    def test_get_config(self, collector):
        """get_config returns all config entries."""
        config = collector.get_config()
        assert isinstance(config, list)
        assert len(config) == 17

    def test_get_config_entry(self, collector):
        """get_config_entry returns a single entry by key."""
        entry = collector.get_config_entry("confidence_threshold")
        assert entry is not None
        assert entry["key"] == "confidence_threshold"
        assert entry["value"] == 60

    def test_update_config(self, collector):
        """update_config changes the value and returns previous."""
        result = collector.update_config("confidence_threshold", 80)
        assert result is not None
        assert result["previous_value"] == 60
        assert result["value"] == 80
        assert result["updated_by"] == "admin"

        # Verify persisted
        entry = collector.get_config_entry("confidence_threshold")
        assert entry["value"] == 80

        # Verify audit log created
        logs, _ = collector.get_logs(source="config")
        assert len(logs) >= 1
        assert "confidence_threshold" in logs[0]["message"]

    def test_update_config_nonexistent(self, collector):
        """update_config returns None for a non-existent key."""
        result = collector.update_config("does_not_exist", 42)
        assert result is None


class TestMetricsCollectorReviews:

    def test_create_review(self, collector):
        """create_review creates a review item with pending status."""
        review = collector.create_review(
            case_id="case-1",
            review_type="low_confidence",
            priority="high",
            summary="Low confidence diagnosis",
        )
        assert review["id"].startswith("rev-")
        assert review["status"] == "pending"
        assert review["priority"] == "high"
        assert review["case_id"] == "case-1"

    def test_get_reviews_filtering(self, collector):
        """Reviews can be filtered by status."""
        collector.create_review("c1", "low_confidence", "high", "Review 1")
        collector.create_review("c2", "safety_flag", "medium", "Review 2")
        r3 = collector.create_review("c3", "error", "low", "Review 3")
        collector.update_review(r3["id"], "resolve", notes="Fixed")

        items, counts = collector.get_reviews(status="pending")
        assert len(items) == 2
        assert counts["pending"] == 2
        assert counts["resolved"] == 1

    def test_update_review_claim(self, collector):
        """Claiming a review sets status to claimed."""
        review = collector.create_review("c1", "error", "high", "Test")
        updated = collector.update_review(review["id"], "claim")
        assert updated["status"] == "claimed"
        assert updated["claimed_by"] == "admin"

    def test_update_review_resolve(self, collector):
        """Resolving a review sets status and adds notes."""
        review = collector.create_review("c1", "error", "high", "Test")
        updated = collector.update_review(review["id"], "resolve", notes="All good")
        assert updated["status"] == "resolved"
        assert updated["resolved_at"] is not None
        assert updated["resolution_notes"] == "All good"

    def test_update_review_escalate(self, collector):
        """Escalating a review sets status to escalated and priority to critical."""
        review = collector.create_review("c1", "error", "medium", "Test")
        updated = collector.update_review(review["id"], "escalate")
        assert updated["status"] == "escalated"
        assert updated["priority"] == "critical"


class TestMetricsCollectorReports:

    def test_create_report(self, collector):
        """create_report creates a report record."""
        report = collector.create_report("case-1", report_type="diagnosis", file_size=1024)
        assert report["id"].startswith("rpt-")
        assert report["case_id"] == "case-1"
        assert report["status"] == "generated"
        assert report["file_size"] == 1024

    def test_get_reports_filtering(self, collector):
        """Reports can be filtered by status."""
        collector.create_report("c1", status="generated")
        collector.create_report("c2", status="failed", error="Render error")
        collector.create_report("c3", status="generated")

        reports, total = collector.get_reports(status="generated")
        assert total == 2
        assert all(r["status"] == "generated" for r in reports)

    def test_get_reports_pagination(self, collector):
        """Reports support page and limit."""
        for i in range(10):
            collector.create_report(f"c{i}")

        reports_p1, total = collector.get_reports(page=1, limit=3)
        assert len(reports_p1) == 3
        assert total == 10

        reports_p2, _ = collector.get_reports(page=2, limit=3)
        assert len(reports_p2) == 3

    def test_update_report_status(self, collector):
        """update_report_status changes the report status."""
        report = collector.create_report("c1", status="generated")
        updated = collector.update_report_status(report["id"], "regenerating")
        assert updated["status"] == "regenerating"


class TestMetricsCollectorAlerts:

    def test_add_alert(self, collector):
        """add_alert adds an alert to the queue."""
        collector.add_alert("warning", "triage", "High latency detected")
        alerts = collector.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["severity"] == "warning"
        assert alerts[0]["message"] == "High latency detected"

    def test_get_alerts(self, collector):
        """get_alerts returns alerts sorted by timestamp (newest first)."""
        collector.add_alert("info", "system", "First")
        collector.add_alert("error", "safety", "Second")
        collector.add_alert("warning", "triage", "Third")

        alerts = collector.get_alerts()
        assert len(alerts) == 3
        # Newest first
        assert alerts[0]["message"] == "Third"
        assert alerts[-1]["message"] == "First"


class TestMetricsCollectorAnalytics:

    def test_get_analytics(self, collector):
        """get_analytics returns all expected keys."""
        # Add some data to make it meaningful
        collector.case_store.create_case("c1", "headache", 30, "male")
        collector.case_store.complete_case("c1", {"diagnosis": "migraine"})

        analytics = collector.get_analytics(period="24h")

        expected_keys = {
            "throughput", "turnaround_trend", "agent_latency",
            "error_rates", "urgency_distribution",
            "confidence_distribution", "review_rate",
            "completion_funnel", "top_failure_categories", "period",
        }
        assert set(analytics.keys()) == expected_keys
        assert analytics["period"] == "24h"


# ===================================================================
# 2. CaseStore unit tests
# ===================================================================

class TestCaseStore:

    def test_create_case(self, store):
        """create_case creates a case with the expected fields."""
        case = store.create_case("c1", "headache and fever", age=35, gender="female")
        assert case["case_id"] == "c1"
        assert case["symptoms"] == "headache and fever"
        assert case["age"] == 35
        assert case["gender"] == "female"
        assert case["status"] == "in_progress"
        assert case["current_stage"] == "triage"
        assert case["agents_total"] == 7

    def test_update_stage(self, store):
        """update_stage adds a stage entry and updates current_stage."""
        store.create_case("c1", "cough")
        result = store.update_stage(
            "c1", "triage", "triage",
            result={"urgency": "medium"}, timing_ms=120.5,
        )
        assert result is not None
        assert result["current_stage"] == "triage"
        assert result["agents_completed"] == 1
        assert len(result["stages"]) == 1
        assert result["stages"][0]["duration_ms"] == 120.5
        # Triage result sets urgency
        assert result["urgency"] == "medium"

    def test_complete_case(self, store):
        """complete_case marks the case completed with a result."""
        store.create_case("c1", "pain")
        case = store.complete_case("c1", {"diagnosis": "strain"})
        assert case["status"] == "completed"
        assert case["completed_at"] is not None
        assert case["final_result"] == {"diagnosis": "strain"}
        assert case["total_duration_ms"] is not None
        assert case["current_stage"] is None

    def test_fail_case(self, store):
        """fail_case marks the case as error with a message."""
        store.create_case("c1", "pain")
        case = store.fail_case("c1", "LLM timeout")
        assert case["status"] == "error"
        assert case["completed_at"] is not None
        assert case["agent_outputs"]["error"] == "LLM timeout"

    def test_get_case(self, store):
        """get_case retrieves by ID."""
        store.create_case("c1", "symptoms")
        case = store.get_case("c1")
        assert case is not None
        assert case["case_id"] == "c1"

    def test_get_case_not_found(self, store):
        """get_case returns None for missing ID."""
        assert store.get_case("nonexistent") is None

    def test_list_cases(self, store):
        """list_cases returns paginated results."""
        for i in range(5):
            store.create_case(f"c{i}", f"symptom {i}")

        cases, total = store.list_cases(page=1, limit=2)
        assert len(cases) == 2
        assert total == 5

        cases2, _ = store.list_cases(page=2, limit=2)
        assert len(cases2) == 2

    def test_list_cases_filter_status(self, store):
        """list_cases filters by status."""
        store.create_case("c1", "s1")
        store.create_case("c2", "s2")
        store.complete_case("c2")

        cases, total = store.list_cases(status="completed")
        assert total == 1
        assert cases[0]["case_id"] == "c2"

    def test_list_cases_filter_urgency(self, store):
        """list_cases filters by urgency."""
        store.create_case("c1", "s1")
        store.update_stage("c1", "triage", "triage", result={"urgency": "high"})
        store.create_case("c2", "s2")
        store.update_stage("c2", "triage", "triage", result={"urgency": "low"})

        cases, total = store.list_cases(urgency="high")
        assert total == 1
        assert cases[0]["case_id"] == "c1"

    def test_status_counts(self, store):
        """status_counts returns count by status."""
        store.create_case("c1", "s1")
        store.create_case("c2", "s2")
        store.create_case("c3", "s3")
        store.complete_case("c2")
        store.fail_case("c3", "err")

        counts = store.status_counts()
        assert counts["in_progress"] == 1
        assert counts["completed"] == 1
        assert counts["error"] == 1

    def test_get_case_timeline(self, store):
        """get_case_timeline returns ordered events."""
        store.create_case("c1", "headache")
        store.update_stage("c1", "triage", "triage", result={"urgency": "medium"}, timing_ms=100)
        store.complete_case("c1", {"diagnosis": "migraine"})

        timeline = store.get_case_timeline("c1")
        assert timeline is not None
        assert len(timeline) >= 3  # created + stage_started + stage_completed + case_completed
        assert timeline[0]["event"] == "case_created"
        assert timeline[-1]["event"] == "case_completed"

    def test_get_case_timeline_not_found(self, store):
        """get_case_timeline returns None for missing case."""
        assert store.get_case_timeline("nonexistent") is None

    def test_max_cases_eviction(self):
        """Old cases are evicted when exceeding MAX_CASES."""
        from admin.store import MAX_CASES

        small_store = CaseStore()
        # Create MAX_CASES + 5 cases
        for i in range(MAX_CASES + 5):
            small_store.create_case(f"c{i}", f"symptom {i}")

        assert small_store.total_count == MAX_CASES
        # Earliest cases should be evicted
        assert small_store.get_case("c0") is None
        assert small_store.get_case("c4") is None
        # Latest should exist
        assert small_store.get_case(f"c{MAX_CASES + 4}") is not None


# ===================================================================
# 3. API endpoint integration tests
# ===================================================================

class TestOverviewEndpoint:

    def test_get_overview(self, app_client, collector):
        """GET /api/admin/overview returns system, agents, cases, alerts."""
        collector.case_store.create_case("c1", "headache", 30, "male")
        collector.add_alert("info", "system", "Test alert")

        resp = app_client.get("/api/admin/overview")
        assert resp.status_code == 200
        data = resp.json()
        assert "system" in data
        assert "agents" in data
        assert "recent_cases" in data
        assert "recent_alerts" in data
        assert len(data["agents"]) == 7


class TestAgentsEndpoints:

    def test_get_agents(self, app_client):
        """GET /api/admin/agents returns list of agents."""
        resp = app_client.get("/api/admin/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 7

    def test_get_agent_by_name(self, app_client):
        """GET /api/admin/agents/{name} returns agent detail."""
        resp = app_client.get("/api/admin/agents/triage")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "triage"

    def test_get_agent_not_found(self, app_client):
        """GET /api/admin/agents/{name} returns 404 for unknown agent."""
        resp = app_client.get("/api/admin/agents/nonexistent")
        assert resp.status_code == 404

    def test_control_agent_pause(self, app_client):
        """POST control with action=pause pauses the agent."""
        resp = app_client.post(
            "/api/admin/agents/triage/control",
            json={"action": "pause"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["new_status"] == "paused"
        assert data["previous_status"] == "healthy"

    def test_control_agent_resume(self, app_client, collector):
        """POST control with action=resume resumes the agent."""
        collector.set_agent_status("triage", "paused")
        resp = app_client.post(
            "/api/admin/agents/triage/control",
            json={"action": "resume"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["new_status"] == "healthy"
        assert data["previous_status"] == "paused"

    def test_control_agent_restart(self, app_client):
        """POST control with action=restart sets agent to healthy."""
        resp = app_client.post(
            "/api/admin/agents/triage/control",
            json={"action": "restart"},
        )
        assert resp.status_code == 200
        assert resp.json()["new_status"] == "healthy"

    def test_control_agent_invalid_action(self, app_client):
        """POST control with invalid action returns 400."""
        resp = app_client.post(
            "/api/admin/agents/triage/control",
            json={"action": "destroy"},
        )
        assert resp.status_code == 400

    def test_control_agent_not_found(self, app_client):
        """POST control for unknown agent returns 404."""
        resp = app_client.post(
            "/api/admin/agents/nonexistent/control",
            json={"action": "pause"},
        )
        assert resp.status_code == 404

    def test_get_agent_detail_endpoint(self, app_client, collector):
        """GET /api/admin/agents/{name}/detail returns comprehensive info."""
        collector.record_agent_execution("triage", "c1", 100.0, True)
        resp = app_client.get("/api/admin/agents/triage/detail")
        assert resp.status_code == 200
        data = resp.json()
        assert "health" in data
        assert "recent_executions" in data
        assert "dependencies" in data

    def test_get_agent_detail_not_found(self, app_client):
        """GET /api/admin/agents/{name}/detail returns 404 for unknown."""
        resp = app_client.get("/api/admin/agents/nonexistent/detail")
        assert resp.status_code == 404

    def test_get_agent_executions(self, app_client, collector):
        """GET /api/admin/agents/{name}/executions returns records."""
        collector.record_agent_execution("triage", "c1", 100.0, True)
        collector.record_agent_execution("triage", "c2", 200.0, False, error="timeout")

        resp = app_client.get("/api/admin/agents/triage/executions")
        assert resp.status_code == 200
        data = resp.json()
        assert "executions" in data
        assert len(data["executions"]) == 2

    def test_get_agent_executions_not_found(self, app_client):
        """GET /api/admin/agents/{name}/executions returns 404 for unknown."""
        resp = app_client.get("/api/admin/agents/nonexistent/executions")
        assert resp.status_code == 404


class TestCasesEndpoints:

    def test_get_cases(self, app_client, collector):
        """GET /api/admin/cases returns paginated cases."""
        collector.case_store.create_case("c1", "headache", 30, "male")
        collector.case_store.create_case("c2", "fever", 25, "female")

        resp = app_client.get("/api/admin/cases")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["cases"]) == 2
        assert "total_pages" in data

    def test_get_cases_filter(self, app_client, collector):
        """GET /api/admin/cases?status=completed filters results."""
        collector.case_store.create_case("c1", "headache")
        collector.case_store.create_case("c2", "fever")
        collector.case_store.complete_case("c2")

        resp = app_client.get("/api/admin/cases?status=completed")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["cases"][0]["case_id"] == "c2"

    def test_get_case_counts(self, app_client, collector):
        """GET /api/admin/cases/counts returns status counts."""
        collector.case_store.create_case("c1", "headache")
        collector.case_store.create_case("c2", "fever")
        collector.case_store.complete_case("c2")

        resp = app_client.get("/api/admin/cases/counts")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert data.get("in_progress", 0) == 1
        assert data.get("completed", 0) == 1

    def test_get_case_detail(self, app_client, collector):
        """GET /api/admin/cases/{id} returns full case with stages."""
        collector.case_store.create_case("c1", "headache", 30, "male")
        collector.case_store.update_stage("c1", "triage", "triage", {"urgency": "medium"}, 100)

        resp = app_client.get("/api/admin/cases/c1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["case_id"] == "c1"
        assert len(data["stages"]) == 1

    def test_get_case_not_found(self, app_client):
        """GET /api/admin/cases/{id} returns 404 for missing case."""
        resp = app_client.get("/api/admin/cases/nonexistent")
        assert resp.status_code == 404

    def test_get_case_timeline(self, app_client, collector):
        """GET /api/admin/cases/{id}/timeline returns events."""
        collector.case_store.create_case("c1", "headache")
        collector.case_store.update_stage("c1", "triage", "triage", {"urgency": "low"}, 50)

        resp = app_client.get("/api/admin/cases/c1/timeline")
        assert resp.status_code == 200
        data = resp.json()
        assert data["case_id"] == "c1"
        assert len(data["events"]) >= 2

    def test_get_case_timeline_not_found(self, app_client):
        """GET /api/admin/cases/{id}/timeline returns 404 for missing case."""
        resp = app_client.get("/api/admin/cases/nonexistent/timeline")
        assert resp.status_code == 404


class TestAlertsEndpoints:

    def test_get_alerts(self, app_client, collector):
        """GET /api/admin/alerts returns alert list."""
        collector.add_alert("warning", "triage", "Slow response")
        collector.add_alert("error", "safety", "Critical flag")

        resp = app_client.get("/api/admin/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["alerts"]) == 2


class TestLogsEndpoints:

    def test_get_logs(self, app_client, collector):
        """GET /api/admin/logs returns filtered logs."""
        collector.add_log("info", "system", "Boot")
        collector.add_log("error", "triage", "Failed", agent="triage")

        resp = app_client.get("/api/admin/logs")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2

        # Filter by level
        resp2 = app_client.get("/api/admin/logs?level=error")
        assert resp2.status_code == 200
        assert resp2.json()["total"] == 1


class TestConfigEndpoints:

    def test_get_config(self, app_client):
        """GET /api/admin/config returns config entries."""
        resp = app_client.get("/api/admin/config")
        assert resp.status_code == 200
        data = resp.json()
        assert "config" in data
        assert len(data["config"]) == 17

    def test_update_config(self, app_client):
        """PUT /api/admin/config/{key} updates and returns result."""
        resp = app_client.put(
            "/api/admin/config/confidence_threshold",
            json={"value": 75},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["previous_value"] == 60
        assert data["value"] == 75

    def test_update_config_not_found(self, app_client):
        """PUT /api/admin/config/{key} returns 404 for unknown key."""
        resp = app_client.put(
            "/api/admin/config/nonexistent_key",
            json={"value": 42},
        )
        assert resp.status_code == 404


class TestReviewsEndpoints:

    def test_get_reviews(self, app_client, collector):
        """GET /api/admin/reviews returns items and counts."""
        collector.create_review("c1", "low_confidence", "high", "Test review")

        resp = app_client.get("/api/admin/reviews")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert "counts" in data
        assert "items" in data

    def test_review_action_claim(self, app_client, collector):
        """POST /api/admin/reviews/{id}/action claim sets claimed."""
        review = collector.create_review("c1", "error", "high", "Test")

        resp = app_client.post(
            f"/api/admin/reviews/{review['id']}/action",
            json={"action": "claim"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["review"]["status"] == "claimed"

    def test_review_action_resolve(self, app_client, collector):
        """POST /api/admin/reviews/{id}/action resolve with notes."""
        review = collector.create_review("c1", "error", "high", "Test")

        resp = app_client.post(
            f"/api/admin/reviews/{review['id']}/action",
            json={"action": "resolve", "notes": "Fixed the issue"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["review"]["status"] == "resolved"
        assert data["review"]["resolution_notes"] == "Fixed the issue"

    def test_review_not_found(self, app_client):
        """POST /api/admin/reviews/{id}/action returns 404 for unknown."""
        resp = app_client.post(
            "/api/admin/reviews/rev-99999/action",
            json={"action": "claim"},
        )
        assert resp.status_code == 404


class TestAnalyticsEndpoints:

    def test_get_analytics(self, app_client, collector):
        """GET /api/admin/analytics returns analytics data."""
        collector.case_store.create_case("c1", "headache")
        collector.case_store.complete_case("c1")

        resp = app_client.get("/api/admin/analytics?period=24h")
        assert resp.status_code == 200
        data = resp.json()
        assert data["period"] == "24h"
        assert "throughput" in data
        assert "error_rates" in data

    def test_get_analytics_invalid_period(self, app_client):
        """GET /api/admin/analytics with invalid period returns 400."""
        resp = app_client.get("/api/admin/analytics?period=1y")
        assert resp.status_code == 400


class TestReportsEndpoints:

    def test_get_reports(self, app_client, collector):
        """GET /api/admin/reports returns paginated reports."""
        collector.create_report("c1", status="generated")
        collector.create_report("c2", status="failed", error="Render error")

        resp = app_client.get("/api/admin/reports")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert "reports" in data
        assert "total_pages" in data

    def test_get_reports_filter(self, app_client, collector):
        """GET /api/admin/reports?status=failed filters results."""
        collector.create_report("c1", status="generated")
        collector.create_report("c2", status="failed", error="err")

        resp = app_client.get("/api/admin/reports?status=failed")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["reports"][0]["status"] == "failed"

    def test_regenerate_report(self, app_client, collector):
        """POST /api/admin/reports/{id}/regenerate marks for regeneration."""
        report = collector.create_report("c1", status="generated")

        resp = app_client.post(f"/api/admin/reports/{report['id']}/regenerate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "regenerating"

    def test_regenerate_report_not_found(self, app_client):
        """POST /api/admin/reports/{id}/regenerate returns 404 for unknown."""
        resp = app_client.post("/api/admin/reports/rpt-99999/regenerate")
        assert resp.status_code == 404
