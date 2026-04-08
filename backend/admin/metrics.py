"""Metrics collector for agent health and system stats with file-based persistence."""

import json
import math
import os
import time
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from collections import deque, OrderedDict, Counter

from .store import CaseStore

# Persistence settings
_DATA_DIR = Path(__file__).parent / "data"
_STATE_FILE = _DATA_DIR / "metrics_state.json"
_SAVE_INTERVAL = 30  # seconds between auto-saves


class MetricsCollector:
    """Thread-safe metrics collector for agents and system health."""

    def __init__(self):
        self._lock = threading.Lock()
        self._start_time = time.time()
        self.case_store = CaseStore()

        # Agent registry: name -> health data
        self._agents: dict[str, dict] = {}
        self._alerts: deque[dict] = deque(maxlen=200)
        self._alert_counter = 0

        # Structured logs
        self._logs: deque[dict] = deque(maxlen=5000)
        self._log_counter = 0

        # Runtime config
        self._config: dict = {}

        # Reports and reviews
        self._reports: OrderedDict = OrderedDict()
        self._report_counter = 0
        self._reviews: OrderedDict = OrderedDict()
        self._review_counter = 0

        # Per-agent execution records
        self._agent_executions: dict[str, deque] = {}

        # Model comparisons
        self._comparisons: OrderedDict = OrderedDict()
        self._comparison_counter = 0

        # Initialize all 7 agents
        self._init_agents()
        # Initialize default config
        self._init_default_config()
        # Load persisted state (overrides defaults with saved data)
        self._load_state()
        # Start background save thread
        self._save_thread = threading.Thread(target=self._auto_save_loop, daemon=True)
        self._save_thread.start()

    # ── Agent Setup ──────────────────────────────────────────────────

    def _init_agents(self):
        agent_defs = [
            ("triage", "Triage Agent", "Urgency assessment, red flag detection, domain classification"),
            ("diagnostician", "Diagnostician Agent", "Differential diagnosis, Bayesian clinical reasoning"),
            ("research", "Research Agent", "Evidence-based literature, clinical guidelines, drug interactions"),
            ("specialist", "Specialist Agent", "Domain-specific deep analysis, diagnostic criteria scoring"),
            ("treatment", "Treatment Agent", "Treatment plans, medication safety, lifestyle recommendations"),
            ("safety", "Safety Agent", "Contraindication checks, dosage safety, allergy risk detection"),
            ("empathy", "Empathy Agent", "Patient-friendly language, plain-language summaries"),
        ]
        for name, display_name, description in agent_defs:
            self._agents[name] = {
                "name": name,
                "display_name": display_name,
                "description": description,
                "status": "healthy",
                "avg_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "error_count": 0,
                "cases_processed": 0,
                "success_rate": 100.0,
                "last_active": None,
                "uptime_pct": 100.0,
                "recent_errors": [],
                "latency_history": [],
                "config": {},
            }

    # ── Default Config ───────────────────────────────────────────────

    def _init_default_config(self):
        configs = [
            {"key": "confidence_threshold", "value": 60, "description": "Minimum confidence score to include a diagnosis", "category": "diagnostics", "type": "number", "validation": {"min": 0, "max": 100}},
            {"key": "urgency_escalation_threshold", "value": "ESI-2", "description": "ESI level that triggers urgent review", "category": "safety", "type": "select", "options": ["ESI-1", "ESI-2", "ESI-3", "ESI-4", "ESI-5"]},
            {"key": "max_diagnoses", "value": 5, "description": "Maximum differential diagnoses to return", "category": "diagnostics", "type": "number", "validation": {"min": 1, "max": 15}},
            {"key": "agent_timeout_cloud", "value": 60, "description": "Timeout in seconds for cloud LLM calls", "category": "system", "type": "number", "validation": {"min": 10, "max": 300}},
            {"key": "agent_timeout_ollama", "value": 120, "description": "Timeout in seconds for Ollama calls", "category": "system", "type": "number", "validation": {"min": 30, "max": 600}},
            {"key": "safety_review_enabled", "value": True, "description": "Enable automatic safety agent review", "category": "safety", "type": "boolean"},
            {"key": "auto_review_low_confidence", "value": True, "description": "Auto-create review items for low confidence cases", "category": "safety", "type": "boolean"},
            {"key": "low_confidence_threshold", "value": 40, "description": "Confidence below this triggers review", "category": "safety", "type": "number", "validation": {"min": 0, "max": 100}},
            {"key": "max_retry_attempts", "value": 2, "description": "Max retries for failed agent calls", "category": "system", "type": "number", "validation": {"min": 0, "max": 5}},
            {"key": "pdf_export_enabled", "value": True, "description": "Enable PDF report generation", "category": "export", "type": "boolean"},
            {"key": "default_model", "value": "claude-sonnet-4-6", "description": "Default LLM model for agents", "category": "routing", "type": "select", "options": ["claude-sonnet-4-6", "claude-opus-4-6", "gpt-4o", "gpt-4o-mini", "gemini-2.5-pro"]},
            {"key": "parallel_agents_enabled", "value": True, "description": "Run Diagnostician and Research agents in parallel", "category": "system", "type": "boolean"},
            {"key": "empathy_agent_enabled", "value": True, "description": "Include patient-friendly summary", "category": "diagnostics", "type": "boolean"},
            {"key": "image_analysis_enabled", "value": True, "description": "Allow image uploads for visual diagnosis", "category": "diagnostics", "type": "boolean"},
            {"key": "max_interview_questions", "value": 15, "description": "Maximum PA agent interview questions", "category": "diagnostics", "type": "number", "validation": {"min": 5, "max": 30}},
            {"key": "review_auto_escalate_hours", "value": 24, "description": "Hours before unresolved reviews auto-escalate", "category": "safety", "type": "number", "validation": {"min": 1, "max": 168}},
            {"key": "fallback_model", "value": "gpt-4o-mini", "description": "Fallback model when primary fails", "category": "routing", "type": "select", "options": ["gpt-4o-mini", "gpt-4o", "gemini-2.5-flash"]},
        ]
        now = datetime.now(timezone.utc).isoformat()
        for c in configs:
            c["updated_at"] = now
            c["updated_by"] = "system"
            c["readonly"] = False
            if "options" not in c:
                c["options"] = None
            if "validation" not in c:
                c["validation"] = None
            self._config[c["key"]] = c

    # ── Agent Metrics ────────────────────────────────────────────────

    def record_agent_call(
        self,
        agent_name: str,
        latency_ms: float,
        success: bool = True,
        error_msg: Optional[str] = None,
    ):
        with self._lock:
            agent = self._agents.get(agent_name)
            if not agent:
                return
            agent["cases_processed"] += 1
            agent["last_active"] = datetime.now(timezone.utc).isoformat()

            # Update latency history (keep last 100)
            history = agent["latency_history"]
            history.append(latency_ms)
            if len(history) > 100:
                agent["latency_history"] = history[-100:]
                history = agent["latency_history"]

            # Recalculate averages
            agent["avg_latency_ms"] = round(sum(history) / len(history), 1)
            sorted_h = sorted(history)
            p95_idx = max(0, int(len(sorted_h) * 0.95) - 1)
            agent["p95_latency_ms"] = round(sorted_h[p95_idx], 1)

            if not success:
                agent["error_count"] += 1
                if error_msg:
                    agent["recent_errors"].append(error_msg)
                    if len(agent["recent_errors"]) > 20:
                        agent["recent_errors"] = agent["recent_errors"][-20:]

            total = agent["cases_processed"]
            errors = agent["error_count"]
            agent["success_rate"] = round(((total - errors) / total) * 100, 1) if total > 0 else 100.0

    def record_agent_execution(
        self,
        agent_name: str,
        case_id: str,
        latency_ms: float,
        success: bool,
        error: Optional[str] = None,
        token_usage: Optional[dict] = None,
        model_used: Optional[str] = None,
    ):
        """Store a per-agent execution record and update agent health stats."""
        with self._lock:
            if agent_name not in self._agent_executions:
                self._agent_executions[agent_name] = deque(maxlen=200)
            record = {
                "case_id": case_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "latency_ms": latency_ms,
                "success": success,
                "error": error,
                "token_usage": token_usage,
                "model_used": model_used,
            }
            self._agent_executions[agent_name].appendleft(record)
        # Also update the main agent health stats (outside inner lock since record_agent_call acquires it)
        self.record_agent_call(agent_name, latency_ms, success, error_msg=error)

    def get_agent_executions(self, agent_name: str, limit: int = 50) -> list[dict]:
        """Return recent execution records for an agent."""
        with self._lock:
            execs = self._agent_executions.get(agent_name, deque())
            return list(execs)[:limit]

    def get_agent_health(self, name: str) -> Optional[dict]:
        with self._lock:
            return self._agents.get(name)

    def get_all_agents(self) -> list[dict]:
        with self._lock:
            return list(self._agents.values())

    def set_agent_status(self, name: str, status: str) -> Optional[dict]:
        with self._lock:
            agent = self._agents.get(name)
            if not agent:
                return None
            old_status = agent["status"]
            agent["status"] = status
            return {"previous_status": old_status, "new_status": status}

    # ── Structured Logs ─────────────────────────────────────────────

    def add_log(
        self,
        level: str,
        source: str,
        message: str,
        case_id: Optional[str] = None,
        agent: Optional[str] = None,
        details: Optional[dict] = None,
        trace_id: Optional[str] = None,
    ) -> dict:
        with self._lock:
            entry = {
                "id": f"log-{self._log_counter:06d}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level,
                "source": source,
                "message": message,
                "case_id": case_id,
                "agent": agent,
                "details": details,
                "trace_id": trace_id,
            }
            self._log_counter += 1
            self._logs.appendleft(entry)
            return entry

    def get_logs(
        self,
        level: Optional[str] = None,
        source: Optional[str] = None,
        agent: Optional[str] = None,
        case_id: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[dict], int]:
        """Filter logs by criteria, return paginated results."""
        with self._lock:
            logs = list(self._logs)

        # Apply filters
        if level:
            logs = [l for l in logs if l["level"] == level]
        if source:
            logs = [l for l in logs if l["source"] == source]
        if agent:
            logs = [l for l in logs if l.get("agent") == agent]
        if case_id:
            logs = [l for l in logs if l.get("case_id") == case_id]
        if search:
            search_lower = search.lower()
            logs = [l for l in logs if search_lower in l["message"].lower()
                    or search_lower in l["source"].lower()]

        total = len(logs)
        return logs[offset:offset + limit], total

    # ── Alerts ───────────────────────────────────────────────────────

    def add_alert(
        self,
        severity: str,
        source: str,
        message: str,
    ):
        with self._lock:
            self._alert_counter += 1
            self._alerts.append({
                "id": f"alert-{self._alert_counter:04d}",
                "severity": severity,
                "source": source,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "resolved": False,
            })

    def get_alerts(self, limit: int = 50) -> list[dict]:
        with self._lock:
            alerts = list(self._alerts)
        alerts.sort(key=lambda a: a["timestamp"], reverse=True)
        return alerts[:limit]

    # ── Config ───────────────────────────────────────────────────────

    def get_config(self) -> list[dict]:
        with self._lock:
            return list(self._config.values())

    def get_config_entry(self, key: str) -> Optional[dict]:
        with self._lock:
            return self._config.get(key)

    def update_config(self, key: str, value, updated_by: str = "admin") -> Optional[dict]:
        """Update a config entry, return dict with old and new values."""
        with self._lock:
            entry = self._config.get(key)
            if not entry:
                return None
            if entry.get("readonly"):
                return None

            previous_value = entry["value"]
            entry["value"] = value
            entry["updated_at"] = datetime.now(timezone.utc).isoformat()
            entry["updated_by"] = updated_by

        # Log the change (outside lock to avoid deadlock)
        self.add_log(
            level="info",
            source="config",
            message=f"Config '{key}' changed from {previous_value!r} to {value!r} by {updated_by}",
        )

        return {
            "key": key,
            "value": value,
            "previous_value": previous_value,
            "updated_at": entry["updated_at"],
            "updated_by": updated_by,
        }

    # ── Reports ──────────────────────────────────────────────────────

    def create_report(
        self,
        case_id: str,
        report_type: str = "diagnosis",
        status: str = "generated",
        file_size: Optional[int] = None,
        error: Optional[str] = None,
    ) -> dict:
        with self._lock:
            self._report_counter += 1
            now = datetime.now(timezone.utc).isoformat()
            report_id = f"rpt-{self._report_counter:05d}"

            # Try to get patient info from case store
            case = self.case_store.get_case(case_id)
            report = {
                "id": report_id,
                "case_id": case_id,
                "type": report_type,
                "status": status,
                "created_at": now,
                "updated_at": now,
                "file_size": file_size,
                "error": error,
                "patient_age": case.get("age") if case else None,
                "patient_gender": case.get("gender") if case else None,
                "symptoms_preview": (case.get("symptoms", "")[:80] + "...") if case and len(case.get("symptoms", "")) > 80 else (case.get("symptoms") if case else None),
            }
            self._reports[report_id] = report
            # Evict oldest if over 500
            while len(self._reports) > 500:
                self._reports.popitem(last=False)
            return report

    def get_report(self, report_id: str) -> Optional[dict]:
        with self._lock:
            return self._reports.get(report_id)

    def update_report_status(self, report_id: str, status: str, error: Optional[str] = None) -> Optional[dict]:
        with self._lock:
            report = self._reports.get(report_id)
            if not report:
                return None
            report["status"] = status
            report["updated_at"] = datetime.now(timezone.utc).isoformat()
            if error is not None:
                report["error"] = error
            return report

    def get_reports(
        self,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        with self._lock:
            reports = list(self._reports.values())
        if status:
            reports = [r for r in reports if r["status"] == status]
        reports.sort(key=lambda r: r["created_at"], reverse=True)
        total = len(reports)
        start = (page - 1) * limit
        return reports[start:start + limit], total

    # ── Reviews ──────────────────────────────────────────────────────

    def create_review(
        self,
        case_id: str,
        review_type: str,
        priority: str,
        summary: str,
    ) -> dict:
        with self._lock:
            self._review_counter += 1
            now = datetime.now(timezone.utc).isoformat()
            review_id = f"rev-{self._review_counter:05d}"
            review = {
                "id": review_id,
                "case_id": case_id,
                "type": review_type,
                "status": "pending",
                "priority": priority,
                "summary": summary,
                "created_at": now,
                "claimed_by": None,
                "resolution_notes": None,
                "resolved_at": None,
            }
            self._reviews[review_id] = review
            # Evict oldest if over 500
            while len(self._reviews) > 500:
                self._reviews.popitem(last=False)
            return review

    def get_reviews(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> tuple[list[dict], dict]:
        """Return reviews and status counts."""
        with self._lock:
            all_reviews = list(self._reviews.values())

        # Compute counts by status
        counts: dict[str, int] = {}
        for r in all_reviews:
            counts[r["status"]] = counts.get(r["status"], 0) + 1

        # Filter
        filtered = all_reviews
        if status:
            filtered = [r for r in filtered if r["status"] == status]
        filtered.sort(key=lambda r: r["created_at"], reverse=True)

        return filtered[:limit], counts

    def get_review(self, review_id: str) -> Optional[dict]:
        with self._lock:
            return self._reviews.get(review_id)

    def update_review(
        self,
        review_id: str,
        action: str,
        notes: Optional[str] = None,
    ) -> Optional[dict]:
        """Apply an action to a review item."""
        with self._lock:
            review = self._reviews.get(review_id)
            if not review:
                return None

            now = datetime.now(timezone.utc).isoformat()

            if action == "claim":
                review["status"] = "claimed"
                review["claimed_by"] = "admin"
            elif action == "resolve":
                review["status"] = "resolved"
                review["resolved_at"] = now
                if notes:
                    review["resolution_notes"] = notes
            elif action == "escalate":
                review["status"] = "escalated"
                review["priority"] = "critical"
            elif action == "add_note":
                existing = review.get("resolution_notes") or ""
                separator = "\n---\n" if existing else ""
                review["resolution_notes"] = existing + separator + (notes or "")
            else:
                return None

            return review

    # ── Model Comparisons ───────────────────────────────────────────

    def create_comparison(self, symptoms, age, gender, models):
        self._comparison_counter += 1
        comp_id = f"cmp-{self._comparison_counter:04d}"
        comp = {
            "id": comp_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "status": "running",
            "prompt": symptoms,
            "age": age,
            "gender": gender,
            "models_requested": models,
            "results": [],
        }
        with self._lock:
            self._comparisons[comp_id] = comp
            if len(self._comparisons) > 50:
                self._comparisons.popitem(last=False)
        return comp

    def add_comparison_result(self, comp_id, result):
        with self._lock:
            comp = self._comparisons.get(comp_id)
            if comp:
                comp["results"].append(result)

    def complete_comparison(self, comp_id):
        with self._lock:
            comp = self._comparisons.get(comp_id)
            if comp:
                comp["completed_at"] = datetime.now(timezone.utc).isoformat()
                all_done = all(r["status"] in ("completed", "failed", "skipped") for r in comp["results"])
                comp["status"] = "completed" if all_done else "partial"

    def get_comparison(self, comp_id):
        with self._lock:
            return self._comparisons.get(comp_id)

    def get_comparisons(self, limit=20):
        with self._lock:
            items = list(reversed(self._comparisons.values()))
            return items[:limit], len(self._comparisons)

    # ── Analytics ────────────────────────────────────────────────────

    def get_analytics(self, period: str = "24h") -> dict:
        """Compute analytics from stored case data. Falls back to demo data when few cases exist."""
        import random

        # Determine time cutoff
        period_hours = {"24h": 24, "7d": 168, "30d": 720}.get(period, 24)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=period_hours)
        cutoff_iso = cutoff.isoformat()

        # Get all cases
        all_cases, _ = self.case_store.list_cases(limit=MAX_RECENT)
        period_cases = [c for c in all_cases if c["created_at"] >= cutoff_iso]

        # If fewer than 20 real cases, return demo data for better visualization
        if len(period_cases) < 20:
            return self._demo_analytics(period, period_hours)

        # 1. Throughput: cases per hour
        throughput = self._compute_throughput(period_cases, period_hours)

        # 2. Turnaround trend: avg pipeline duration over time
        turnaround_trend = self._compute_turnaround_trend(period_cases, period_hours)

        # 3. Agent latency: per-agent latency arrays
        agent_latency = {}
        with self._lock:
            for agent_name, execs in self._agent_executions.items():
                recent = [e for e in execs if e["timestamp"] >= cutoff_iso]
                agent_latency[agent_name] = [e["latency_ms"] for e in recent]

        # 4. Error rates: per-agent error percentages
        error_rates = {}
        with self._lock:
            for agent_name, agent_data in self._agents.items():
                total = agent_data["cases_processed"]
                errors = agent_data["error_count"]
                error_rates[agent_name] = round((errors / total) * 100, 2) if total > 0 else 0.0

        # 5. Urgency distribution
        urgency_distribution: dict[str, int] = {}
        for c in period_cases:
            urg = c.get("urgency") or "unknown"
            urgency_distribution[urg] = urgency_distribution.get(urg, 0) + 1

        # 6. Confidence distribution
        confidence_distribution = self._compute_confidence_distribution(period_cases)

        # 7. Review rate
        with self._lock:
            total_reviews = len(self._reviews)
        total_cases_count = len(period_cases)
        review_rate = round((total_reviews / total_cases_count) * 100, 2) if total_cases_count > 0 else 0.0

        # 8. Completion funnel
        completion_funnel = self._compute_completion_funnel(period_cases)

        # 9. Top failure categories
        top_failure_categories = self._compute_failure_categories()

        return {
            "throughput": throughput,
            "turnaround_trend": turnaround_trend,
            "agent_latency": agent_latency,
            "error_rates": error_rates,
            "urgency_distribution": urgency_distribution,
            "confidence_distribution": confidence_distribution,
            "review_rate": review_rate,
            "completion_funnel": completion_funnel,
            "top_failure_categories": top_failure_categories,
            "period": period,
        }

    def _demo_analytics(self, period: str, period_hours: int) -> dict:
        """Generate realistic demo analytics data for visualization."""
        import random
        now = datetime.now(timezone.utc)

        # Throughput: realistic hourly distribution
        num_buckets = min(period_hours, 24)
        throughput = []
        for i in range(num_buckets):
            t = now - timedelta(hours=num_buckets - i)
            # More cases during business hours
            hour = t.hour
            base = 8 if 8 <= hour <= 18 else 2
            count = max(0, base + random.randint(-3, 5))
            throughput.append({"time": t.strftime("%Y-%m-%dT%H:00:00"), "count": count})

        # Agent latency
        agents = ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"]
        agent_latency = {}
        base_latencies = {"triage": 800, "diagnostician": 3200, "research": 2800, "specialist": 2500, "treatment": 2200, "safety": 1500, "empathy": 1200}
        for a in agents:
            base = base_latencies.get(a, 2000)
            agent_latency[a] = [base + random.randint(-400, 600) for _ in range(20)]

        # Error rates
        error_rates = {a: round(random.uniform(0, 3.5), 2) for a in agents}
        error_rates["safety"] = round(random.uniform(0, 0.5), 2)  # Safety agent rarely errors

        # Urgency distribution
        urgency_distribution = {"routine": 42, "soon": 18, "urgent": 7, "emergency": 2}

        # Confidence distribution
        confidence_distribution = {"0-20": 1, "20-40": 4, "40-60": 12, "60-80": 28, "80-100": 22}

        # Completion funnel
        completion_funnel = {s: max(5, 67 - i * 3 - random.randint(0, 5)) for i, s in enumerate(
            ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy", "completed"]
        )}

        # Top failure categories
        top_failure_categories = [
            {"category": "LLM timeout", "count": 3, "pct": 33.3},
            {"category": "JSON parse error", "count": 2, "pct": 22.2},
            {"category": "Context too long", "count": 2, "pct": 22.2},
            {"category": "Rate limited", "count": 1, "pct": 11.1},
            {"category": "Network error", "count": 1, "pct": 11.1},
        ]

        return {
            "throughput": throughput,
            "turnaround_trend": [{"time": (now - timedelta(hours=i)).strftime("%H:00"), "avg_ms": 8000 + random.randint(-2000, 3000)} for i in range(12, 0, -1)],
            "agent_latency": agent_latency,
            "error_rates": error_rates,
            "urgency_distribution": urgency_distribution,
            "confidence_distribution": confidence_distribution,
            "review_rate": 14.5,
            "completion_funnel": completion_funnel,
            "top_failure_categories": top_failure_categories,
            "period": period,
        }

    def _compute_throughput(self, cases: list[dict], period_hours: int) -> list[dict]:
        """Compute cases per hour over the period."""
        if not cases:
            return []

        # Determine bucket size
        if period_hours <= 24:
            bucket_hours = 1
        elif period_hours <= 168:
            bucket_hours = 6
        else:
            bucket_hours = 24

        now = datetime.now(timezone.utc)
        buckets: dict[str, int] = {}
        num_buckets = max(1, period_hours // bucket_hours)

        for i in range(num_buckets):
            bucket_start = now - timedelta(hours=(i + 1) * bucket_hours)
            bucket_key = bucket_start.strftime("%Y-%m-%dT%H:00:00")
            buckets[bucket_key] = 0

        for c in cases:
            try:
                created = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
                diff_hours = (now - created).total_seconds() / 3600
                bucket_idx = int(diff_hours / bucket_hours)
                bucket_start = now - timedelta(hours=(bucket_idx + 1) * bucket_hours)
                bucket_key = bucket_start.strftime("%Y-%m-%dT%H:00:00")
                if bucket_key in buckets:
                    buckets[bucket_key] += 1
            except Exception:
                continue

        result = [{"timestamp": k, "count": v} for k, v in sorted(buckets.items())]
        return result

    def _compute_turnaround_trend(self, cases: list[dict], period_hours: int) -> list[dict]:
        """Compute average pipeline duration trend."""
        completed = [c for c in cases if c.get("total_duration_ms") and c["status"] == "completed"]
        if not completed:
            return []

        # Group by hour buckets
        now = datetime.now(timezone.utc)
        bucket_hours = 1 if period_hours <= 24 else (6 if period_hours <= 168 else 24)
        buckets: dict[str, list[float]] = {}

        for c in completed:
            try:
                created = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
                diff_hours = (now - created).total_seconds() / 3600
                bucket_idx = int(diff_hours / bucket_hours)
                bucket_start = now - timedelta(hours=(bucket_idx + 1) * bucket_hours)
                bucket_key = bucket_start.strftime("%Y-%m-%dT%H:00:00")
                if bucket_key not in buckets:
                    buckets[bucket_key] = []
                buckets[bucket_key].append(c["total_duration_ms"])
            except Exception:
                continue

        result = [
            {"timestamp": k, "avg_ms": round(sum(v) / len(v), 1)}
            for k, v in sorted(buckets.items())
            if v
        ]
        return result

    def _compute_confidence_distribution(self, cases: list[dict]) -> list[dict]:
        """Compute confidence score distribution from diagnostician results."""
        ranges = [
            ("0-20", 0, 20),
            ("21-40", 21, 40),
            ("41-60", 41, 60),
            ("61-80", 61, 80),
            ("81-100", 81, 100),
        ]
        counts = {r[0]: 0 for r in ranges}

        for c in cases:
            diag = c.get("agent_outputs", {}).get("diagnostician", {})
            if isinstance(diag, dict):
                diff = diag.get("differential_diagnosis", [])
                if isinstance(diff, list):
                    for d in diff:
                        if isinstance(d, dict):
                            conf = d.get("confidence", d.get("probability", 0))
                            try:
                                conf = float(conf)
                            except (TypeError, ValueError):
                                continue
                            for label, lo, hi in ranges:
                                if lo <= conf <= hi:
                                    counts[label] += 1
                                    break

        return [{"range": k, "count": v} for k, v in counts.items()]

    def _compute_completion_funnel(self, cases: list[dict]) -> dict:
        """Compute how many cases reach each pipeline stage."""
        stages = ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"]
        funnel = {s: 0 for s in stages}
        funnel["started"] = len(cases)

        for c in cases:
            completed_stages = {s.get("stage") for s in c.get("stages", []) if s.get("status") == "completed"}
            for s in stages:
                if s in completed_stages:
                    funnel[s] += 1

        return funnel

    def _compute_failure_categories(self) -> list[dict]:
        """Compute most common error types from agent executions."""
        error_counter: Counter = Counter()
        with self._lock:
            for agent_name, execs in self._agent_executions.items():
                for e in execs:
                    if not e["success"] and e.get("error"):
                        # Categorize errors
                        err = e["error"]
                        if "timeout" in err.lower() or "timed out" in err.lower():
                            error_counter["Timeout"] += 1
                        elif "rate limit" in err.lower() or "429" in err:
                            error_counter["Rate Limit"] += 1
                        elif "json" in err.lower() or "parse" in err.lower():
                            error_counter["Parse Error"] += 1
                        elif "connection" in err.lower() or "network" in err.lower():
                            error_counter["Connection Error"] += 1
                        elif "auth" in err.lower() or "401" in err or "403" in err:
                            error_counter["Auth Error"] += 1
                        else:
                            error_counter["Other"] += 1

        return [{"category": k, "count": v} for k, v in error_counter.most_common(10)]

    # ── Agent Detail ─────────────────────────────────────────────────

    def get_agent_detail(self, name: str) -> Optional[dict]:
        """Get comprehensive agent detail for the admin detail page."""
        with self._lock:
            agent = self._agents.get(name)
            if not agent:
                return None
            agent_copy = dict(agent)
            execs = list(self._agent_executions.get(name, deque()))[:50]

        # Build health dict
        health = {
            "name": agent_copy["name"],
            "display_name": agent_copy["display_name"],
            "status": agent_copy["status"],
            "avg_latency_ms": agent_copy["avg_latency_ms"],
            "p95_latency_ms": agent_copy["p95_latency_ms"],
            "error_count": agent_copy["error_count"],
            "cases_processed": agent_copy["cases_processed"],
            "success_rate": agent_copy["success_rate"],
            "last_active": agent_copy.get("last_active"),
            "uptime_pct": agent_copy.get("uptime_pct", 100.0),
        }

        # Failure clusters from execution records
        failure_clusters = []
        error_groups: dict[str, int] = {}
        for e in execs:
            if not e["success"] and e.get("error"):
                key = e["error"][:100]
                error_groups[key] = error_groups.get(key, 0) + 1
        for err_msg, count in sorted(error_groups.items(), key=lambda x: -x[1])[:5]:
            failure_clusters.append({"error": err_msg, "count": count})

        # Performance trend from execution records
        performance_trend = []
        if execs:
            # Group by 1-hour buckets
            now = datetime.now(timezone.utc)
            buckets: dict[str, dict] = {}
            for e in execs:
                try:
                    ts = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
                    bucket_key = ts.strftime("%Y-%m-%dT%H:00:00")
                    if bucket_key not in buckets:
                        buckets[bucket_key] = {"latencies": [], "errors": 0, "total": 0}
                    buckets[bucket_key]["latencies"].append(e["latency_ms"])
                    buckets[bucket_key]["total"] += 1
                    if not e["success"]:
                        buckets[bucket_key]["errors"] += 1
                except Exception:
                    continue
            for ts_key, data in sorted(buckets.items()):
                avg_lat = round(sum(data["latencies"]) / len(data["latencies"]), 1) if data["latencies"] else 0
                err_rate = round((data["errors"] / data["total"]) * 100, 1) if data["total"] > 0 else 0
                performance_trend.append({
                    "timestamp": ts_key,
                    "avg_latency": avg_lat,
                    "error_rate": err_rate,
                })

        # Learning insights (derived from patterns)
        learning_insights = self._derive_learning_insights(name, execs)

        # Agent dependencies
        pipeline_order = ["triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"]
        idx = pipeline_order.index(name) if name in pipeline_order else -1
        dependencies = pipeline_order[:idx] if idx > 0 else []
        downstream = pipeline_order[idx + 1:] if idx >= 0 and idx < len(pipeline_order) - 1 else []
        # Diagnostician and research are parallel, so adjust
        if name == "diagnostician":
            dependencies = ["triage"]
            downstream = ["specialist", "treatment", "safety", "empathy"]
        elif name == "research":
            dependencies = ["triage"]
            downstream = ["specialist", "treatment", "safety", "empathy"]

        return {
            "health": health,
            "description": agent_copy["description"],
            "recent_executions": execs,
            "failure_clusters": failure_clusters,
            "performance_trend": performance_trend,
            "learning_insights": learning_insights,
            "config": agent_copy.get("config", {}),
            "dependencies": dependencies,
            "downstream": downstream,
        }

    def _derive_learning_insights(self, agent_name: str, execs: list[dict]) -> list[dict]:
        """Derive learning insights from execution patterns."""
        insights = []
        if not execs:
            return insights

        now = datetime.now(timezone.utc).isoformat()

        # Check for timeout patterns
        timeouts = [e for e in execs if e.get("error") and "timeout" in str(e.get("error", "")).lower()]
        if len(timeouts) >= 2:
            insights.append({
                "category": "timeout_pattern",
                "description": f"Agent has experienced {len(timeouts)} timeouts in recent executions",
                "frequency": len(timeouts),
                "last_seen": timeouts[0]["timestamp"] if timeouts else now,
                "suggestion": "Consider increasing the agent timeout or reducing prompt complexity",
            })

        # Check for high latency trend
        latencies = [e["latency_ms"] for e in execs if e.get("latency_ms")]
        if len(latencies) >= 5:
            recent_avg = sum(latencies[:5]) / 5
            overall_avg = sum(latencies) / len(latencies)
            if recent_avg > overall_avg * 1.5:
                insights.append({
                    "category": "latency_increase",
                    "description": f"Recent average latency ({recent_avg:.0f}ms) is {(recent_avg/overall_avg - 1)*100:.0f}% higher than overall average ({overall_avg:.0f}ms)",
                    "frequency": 1,
                    "last_seen": now,
                    "suggestion": "Monitor for degraded model performance or increased prompt sizes",
                })

        # Check error rate
        errors = [e for e in execs if not e["success"]]
        if len(errors) >= 3 and len(execs) >= 10:
            error_rate = len(errors) / len(execs) * 100
            if error_rate > 10:
                insights.append({
                    "category": "high_error_rate",
                    "description": f"Error rate of {error_rate:.1f}% ({len(errors)} errors in {len(execs)} executions)",
                    "frequency": len(errors),
                    "last_seen": errors[0]["timestamp"] if errors else now,
                    "suggestion": "Review error patterns and consider adding retry logic or fallback models",
                })

        return insights

    # ── System Metrics ───────────────────────────────────────────────

    def get_system_metrics(self) -> dict:
        uptime = time.time() - self._start_time
        active = self.case_store.get_active_cases()

        # Calculate avg pipeline duration from completed cases
        completed_cases, _ = self.case_store.list_cases(status="completed", limit=100)
        durations = [c["total_duration_ms"] for c in completed_cases if c.get("total_duration_ms")]
        avg_duration = round(sum(durations) / len(durations), 1) if durations else 0.0

        return {
            "uptime_seconds": round(uptime, 1),
            "total_cases": self.case_store.total_count,
            "active_cases": len(active),
            "completed_cases": self.case_store.completed_count,
            "error_cases": self.case_store.error_count,
            "avg_pipeline_duration_ms": avg_duration,
            "cases_last_hour": self._count_recent_cases(hours=1),
            "cases_last_24h": self._count_recent_cases(hours=24),
        }

    def _count_recent_cases(self, hours: int) -> int:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        cases, _ = self.case_store.list_cases(limit=MAX_RECENT)
        return sum(1 for c in cases if c["created_at"] >= cutoff)

    # ── Persistence ─────────────────────────────────────────────────────

    def _save_state(self):
        """Save current state to JSON file for persistence across restarts."""
        try:
            _DATA_DIR.mkdir(parents=True, exist_ok=True)
            with self._lock:
                state = {
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "agents": dict(self._agents),
                    "alerts": list(self._alerts),
                    "alert_counter": self._alert_counter,
                    "logs": list(self._logs),
                    "log_counter": self._log_counter,
                    "config": dict(self._config),
                    "reports": dict(self._reports),
                    "report_counter": self._report_counter,
                    "reviews": dict(self._reviews),
                    "review_counter": self._review_counter,
                    "agent_executions": {
                        name: list(execs) for name, execs in self._agent_executions.items()
                    },
                    "comparisons": dict(self._comparisons),
                    "comparison_counter": self._comparison_counter,
                    "cases": dict(self.case_store._cases),
                }
            # Write atomically via temp file
            tmp = _STATE_FILE.with_suffix(".tmp")
            with open(tmp, "w") as f:
                json.dump(state, f, default=str)
            tmp.replace(_STATE_FILE)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Failed to save metrics state: %s", e)

    def _load_state(self):
        """Load persisted state from JSON file if it exists."""
        if not _STATE_FILE.exists():
            return
        try:
            with open(_STATE_FILE, "r") as f:
                state = json.load(f)

            with self._lock:
                # Restore agents (merge with defaults to pick up any new agents)
                saved_agents = state.get("agents", {})
                for name, data in saved_agents.items():
                    if name in self._agents:
                        self._agents[name].update(data)

                # Restore alerts
                saved_alerts = state.get("alerts", [])
                self._alerts = deque(saved_alerts, maxlen=200)
                self._alert_counter = state.get("alert_counter", len(saved_alerts))

                # Restore logs
                saved_logs = state.get("logs", [])
                self._logs = deque(saved_logs, maxlen=5000)
                self._log_counter = state.get("log_counter", len(saved_logs))

                # Restore config (merge: saved values override defaults, new defaults kept)
                saved_config = state.get("config", {})
                for key, entry in saved_config.items():
                    if key in self._config:
                        self._config[key].update(entry)
                    else:
                        self._config[key] = entry

                # Restore reports
                saved_reports = state.get("reports", {})
                self._reports = OrderedDict(saved_reports)
                self._report_counter = state.get("report_counter", len(saved_reports))

                # Restore reviews
                saved_reviews = state.get("reviews", {})
                self._reviews = OrderedDict(saved_reviews)
                self._review_counter = state.get("review_counter", len(saved_reviews))

                # Restore agent executions
                saved_execs = state.get("agent_executions", {})
                for name, execs in saved_execs.items():
                    self._agent_executions[name] = deque(execs, maxlen=200)

                # Restore comparisons
                saved_comparisons = state.get("comparisons", {})
                self._comparisons = OrderedDict(saved_comparisons)
                self._comparison_counter = state.get("comparison_counter", len(saved_comparisons))

                # Restore cases
                saved_cases = state.get("cases", {})
                self.case_store._cases = OrderedDict(saved_cases)

            import logging
            logging.getLogger(__name__).info(
                "Loaded persisted admin state: %d cases, %d logs, %d alerts",
                len(saved_cases), len(saved_logs), len(saved_alerts),
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning("Failed to load metrics state: %s", e)

    def _auto_save_loop(self):
        """Background thread that saves state periodically."""
        while True:
            time.sleep(_SAVE_INTERVAL)
            self._save_state()

    def save_now(self):
        """Manually trigger a state save (called after important mutations)."""
        threading.Thread(target=self._save_state, daemon=True).start()


MAX_RECENT = 1000


# ── Singleton ────────────────────────────────────────────────────────

_collector: Optional[MetricsCollector] = None


def get_metrics() -> MetricsCollector:
    """Return the global MetricsCollector singleton."""
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector
