"""Tests for the QualityAuditor agent.

Covers:
  1. Scoring a perfect/complete case
  2. Scoring a case with empty diagnosis
  3. Scoring a case with agent timeouts
  4. Running a full audit with recommendations
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.quality_auditor import QualityAuditor


@pytest.fixture()
def auditor(tmp_path, monkeypatch):
    """Return a QualityAuditor that uses a temp file for persistence."""
    import agents.quality_auditor as qa_mod
    monkeypatch.setattr(qa_mod, "AUDIT_DB_PATH", tmp_path / "test_audits.json")
    return QualityAuditor()


def _make_case(**overrides):
    """Build a complete diagnosis result dict with sensible defaults."""
    base = {
        "causes": [
            {"cause": "Migraine", "value": 75},
            {"cause": "Tension headache", "value": 60},
            {"cause": "Cluster headache", "value": 40},
        ],
        "recommended_tests": ["CT scan", "Blood panel"],
        "safety_status": "OK",
        "patient_summary": "You may be experiencing a migraine.",
        "medications": [{"name": "Ibuprofen", "dosage": "400mg"}],
        "lifestyle_recommendations": ["Stay hydrated", "Rest in dark room"],
        "agent_timings": {
            "triage": 1.2,
            "diagnostician": 5.4,
            "research": 4.8,
            "specialist": 3.1,
            "treatment": 2.5,
            "safety": 1.0,
            "empathy": 1.5,
        },
        "agent_details": {},
        "missing_sections": [],
        "total_time": 20.0,
        "provider": "anthropic",
        "agents_used": ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"],
    }
    base.update(overrides)
    return base


class TestAuditCasePerfect:

    def test_perfect_case_scores_90_plus(self, auditor):
        """A complete case with all sections should score 90+."""
        case = _make_case()
        audit = auditor.audit_case(case)
        assert audit["score"] >= 90
        assert audit["grade"] in ("A",)
        assert len(audit["issues"]) == 0

    def test_perfect_case_has_correct_metadata(self, auditor):
        """Audit result should contain expected metadata fields."""
        case = _make_case()
        audit = auditor.audit_case(case)
        assert audit["diagnosis"] == "Migraine"
        assert audit["provider"] == "anthropic"
        assert "timestamp" in audit
        assert audit["total_time"] == 20.0
        assert len(audit["agents_used"]) == 7


class TestAuditCaseEmptyDiagnosis:

    def test_no_causes_scores_low(self, auditor):
        """Missing causes should reduce score significantly."""
        case = _make_case(causes=[])
        audit = auditor.audit_case(case)
        assert audit["score"] < 70
        assert any("No differential" in i["issue"] for i in audit["issues"])
        assert audit["diagnosis"] == "None"

    def test_few_causes_has_warning(self, auditor):
        """Only 1-2 causes should produce a warning."""
        case = _make_case(causes=[{"cause": "Migraine", "value": 75}])
        audit = auditor.audit_case(case)
        assert any("Only 1 differential" in i["issue"] for i in audit["issues"])

    def test_no_tests_reduces_score(self, auditor):
        """Missing recommended tests should reduce score."""
        case = _make_case(recommended_tests=[])
        audit = auditor.audit_case(case)
        assert audit["score"] < 100
        assert any("No recommended tests" in i["issue"] for i in audit["issues"])

    def test_no_patient_summary_reduces_score(self, auditor):
        """Missing patient summary should reduce score."""
        case = _make_case(patient_summary="")
        audit = auditor.audit_case(case)
        assert audit["score"] < 100
        assert any("No patient-friendly summary" in i["issue"] for i in audit["issues"])

    def test_no_treatment_reduces_score(self, auditor):
        """Missing medications AND lifestyle recs should reduce score."""
        case = _make_case(medications=[], lifestyle_recommendations=[])
        audit = auditor.audit_case(case)
        assert any("No treatment" in i["issue"] for i in audit["issues"])


class TestAuditCaseTimeout:

    def test_agent_timeout_reduces_score(self, auditor):
        """Agent timeouts (>=175s) should reduce the score."""
        timings = {
            "triage": 1.0,
            "diagnostician": 180.0,  # timeout
            "research": 4.0,
            "specialist": 3.0,
            "treatment": 2.0,
            "safety": 1.0,
            "empathy": 1.0,
        }
        case = _make_case(agent_timings=timings)
        audit = auditor.audit_case(case)
        assert audit["score"] < 90
        assert any("timed out" in i["issue"] for i in audit["issues"])

    def test_multiple_timeouts_reduce_more(self, auditor):
        """Multiple agent timeouts should reduce score further."""
        timings = {
            "triage": 1.0,
            "diagnostician": 200.0,
            "research": 190.0,
            "specialist": 3.0,
            "treatment": 2.0,
            "safety": 175.0,
            "empathy": 1.0,
        }
        case = _make_case(agent_timings=timings)
        audit = auditor.audit_case(case)
        # 3 timeouts at -15 each = -45, so max 55
        assert audit["score"] <= 60

    def test_slow_total_time_adds_issue(self, auditor):
        """Total pipeline time > 300s should add a warning."""
        case = _make_case(total_time=350.0)
        audit = auditor.audit_case(case)
        assert any("Pipeline took" in i["issue"] for i in audit["issues"])


class TestAuditCaseAgentErrors:

    def test_agent_error_reduces_score(self, auditor):
        """An error in agent_details should reduce score."""
        case = _make_case(agent_details={
            "diagnostician": {"error": "LLM timeout after 30s"}
        })
        audit = auditor.audit_case(case)
        assert audit["score"] < 90
        assert any("diagnostician error" in i["issue"] for i in audit["issues"])

    def test_missing_sections_reduce_score(self, auditor):
        """Missing sections should each reduce the score."""
        case = _make_case(missing_sections=["research", "specialist"])
        audit = auditor.audit_case(case)
        assert audit["score"] < 90
        assert sum(1 for i in audit["issues"] if "Missing section" in i["issue"]) == 2


class TestRunFullAudit:

    def test_full_audit_produces_summary(self, auditor):
        """Full audit should produce a summary with all expected keys."""
        cases = [_make_case(), _make_case(causes=[])]
        summary = auditor.run_full_audit(cases)

        assert summary["total_cases"] == 2
        assert "average_score" in summary
        assert "grade_distribution" in summary
        assert "recommendations" in summary
        assert "case_audits" in summary
        assert len(summary["case_audits"]) == 2

    def test_full_audit_recommendations_for_bad_cases(self, auditor):
        """Full audit of poor cases should generate recommendations."""
        bad_timings = {k: 200.0 for k in ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"]}
        cases = [
            _make_case(causes=[], agent_timings=bad_timings),
            _make_case(causes=[], agent_timings=bad_timings),
        ]
        summary = auditor.run_full_audit(cases)

        assert len(summary["recommendations"]) > 0
        rec_titles = [r["title"] for r in summary["recommendations"]]
        # Should have timeout and empty diagnosis recommendations
        assert any("Timeout" in t for t in rec_titles)
        assert any("Differential" in t or "Empty" in t for t in rec_titles)

    def test_full_audit_perfect_cases_high_average(self, auditor):
        """Full audit of perfect cases should have high average score."""
        cases = [_make_case() for _ in range(5)]
        summary = auditor.run_full_audit(cases)
        assert summary["average_score"] >= 90

    def test_full_audit_persists_results(self, auditor):
        """Audit results should be persisted and retrievable."""
        cases = [_make_case()]
        auditor.run_full_audit(cases)

        latest = auditor.get_latest_audit()
        assert "stats" in latest
        assert "recommendations" in latest
        assert "recent_cases" in latest
        assert latest["stats"]["total_cases_audited"] >= 1

    def test_full_audit_grade_distribution(self, auditor):
        """Grade distribution should add up to total cases."""
        cases = [_make_case(), _make_case(causes=[]), _make_case(causes=[], recommended_tests=[], patient_summary="", medications=[], lifestyle_recommendations=[])]
        summary = auditor.run_full_audit(cases)

        dist = summary["grade_distribution"]
        total = sum(dist.values())
        assert total == 3
