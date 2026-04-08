"""In-memory case store for tracking diagnosis pipeline cases."""

import threading
from datetime import datetime, timezone
from typing import Optional
from collections import OrderedDict


MAX_CASES = 1000


class CaseStore:
    """Thread-safe in-memory store for pipeline cases."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cases: OrderedDict[str, dict] = OrderedDict()

    # ── Mutations ────────────────────────────────────────────────────

    def create_case(
        self,
        case_id: str,
        symptoms: str,
        age: int = 30,
        gender: str = "unknown",
    ) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        case = {
            "case_id": case_id,
            "symptoms": symptoms,
            "age": age,
            "gender": gender,
            "status": "in_progress",
            "urgency": None,
            "created_at": now,
            "completed_at": None,
            "total_duration_ms": None,
            "current_stage": "triage",
            "agents_completed": 0,
            "agents_total": 7,
            "stages": [],
            "agent_outputs": {},
            "final_result": None,
        }
        with self._lock:
            self._cases[case_id] = case
            # Evict oldest if over limit
            while len(self._cases) > MAX_CASES:
                self._cases.popitem(last=False)
        return case

    def update_stage(
        self,
        case_id: str,
        stage: str,
        agent_name: str,
        result: Optional[dict] = None,
        timing_ms: Optional[float] = None,
    ) -> Optional[dict]:
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            case = self._cases.get(case_id)
            if not case:
                return None
            stage_entry = {
                "stage": stage,
                "agent_name": agent_name,
                "status": "completed",
                "started_at": now,
                "completed_at": now,
                "duration_ms": timing_ms,
                "result_summary": _summarize(result) if result else None,
            }
            case["stages"].append(stage_entry)
            case["current_stage"] = stage
            case["agents_completed"] = len(case["stages"])
            if result:
                case["agent_outputs"][agent_name] = result
            if result and agent_name == "triage" and isinstance(result, dict):
                case["urgency"] = result.get("urgency")
            return case

    def complete_case(
        self,
        case_id: str,
        final_result: Optional[dict] = None,
    ) -> Optional[dict]:
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            case = self._cases.get(case_id)
            if not case:
                return None
            case["status"] = "completed"
            case["completed_at"] = now
            case["final_result"] = final_result
            case["current_stage"] = None
            # Calculate total duration
            try:
                created = datetime.fromisoformat(case["created_at"])
                completed = datetime.fromisoformat(now)
                case["total_duration_ms"] = (completed - created).total_seconds() * 1000
            except Exception:
                pass
            return case

    def fail_case(self, case_id: str, error: str) -> Optional[dict]:
        with self._lock:
            case = self._cases.get(case_id)
            if not case:
                return None
            case["status"] = "error"
            case["completed_at"] = datetime.now(timezone.utc).isoformat()
            case["agent_outputs"]["error"] = error
            return case

    # ── Queries ──────────────────────────────────────────────────────

    def get_case(self, case_id: str) -> Optional[dict]:
        with self._lock:
            return self._cases.get(case_id)

    def list_cases(
        self,
        status: Optional[str] = None,
        urgency: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        with self._lock:
            cases = list(self._cases.values())

        # Filter
        if status:
            cases = [c for c in cases if c["status"] == status]
        if urgency:
            cases = [c for c in cases if c.get("urgency") == urgency]

        # Sort newest first
        cases.sort(key=lambda c: c["created_at"], reverse=True)

        total = len(cases)
        start = (page - 1) * limit
        end = start + limit
        return cases[start:end], total

    def get_active_cases(self) -> list[dict]:
        with self._lock:
            return [c for c in self._cases.values() if c["status"] == "in_progress"]

    @property
    def total_count(self) -> int:
        with self._lock:
            return len(self._cases)

    @property
    def completed_count(self) -> int:
        with self._lock:
            return sum(1 for c in self._cases.values() if c["status"] == "completed")

    @property
    def error_count(self) -> int:
        with self._lock:
            return sum(1 for c in self._cases.values() if c["status"] == "error")

    def status_counts(self) -> dict[str, int]:
        """Return a dict of case counts grouped by status."""
        with self._lock:
            counts: dict[str, int] = {}
            for c in self._cases.values():
                status = c["status"]
                counts[status] = counts.get(status, 0) + 1
            return counts

    def get_case_timeline(self, case_id: str) -> Optional[list[dict]]:
        """Return an ordered list of events for a case (stages + lifecycle)."""
        with self._lock:
            case = self._cases.get(case_id)
            if not case:
                return None

        events: list[dict] = []

        # Case creation event
        events.append({
            "event": "case_created",
            "timestamp": case["created_at"],
            "details": {
                "symptoms": case["symptoms"],
                "age": case["age"],
                "gender": case["gender"],
            },
        })

        # Stage events
        for stage in case.get("stages", []):
            if stage.get("started_at"):
                events.append({
                    "event": "stage_started",
                    "timestamp": stage["started_at"],
                    "details": {
                        "stage": stage["stage"],
                        "agent": stage["agent_name"],
                    },
                })
            if stage.get("completed_at"):
                events.append({
                    "event": "stage_completed",
                    "timestamp": stage["completed_at"],
                    "details": {
                        "stage": stage["stage"],
                        "agent": stage["agent_name"],
                        "duration_ms": stage.get("duration_ms"),
                        "status": stage["status"],
                        "result_summary": stage.get("result_summary"),
                    },
                })

        # Case completion / failure event
        if case.get("completed_at"):
            events.append({
                "event": "case_completed" if case["status"] == "completed" else "case_failed",
                "timestamp": case["completed_at"],
                "details": {
                    "status": case["status"],
                    "total_duration_ms": case.get("total_duration_ms"),
                },
            })

        # Sort by timestamp
        events.sort(key=lambda e: e["timestamp"])
        return events


def _summarize(result: Optional[dict]) -> Optional[str]:
    """Extract a short summary from an agent result dict."""
    if not result:
        return None
    if isinstance(result, dict):
        for key in ("summary", "assessment", "diagnosis", "message"):
            if key in result:
                text = str(result[key])
                return text[:200] if len(text) > 200 else text
    return str(result)[:200]
