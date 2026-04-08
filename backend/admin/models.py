"""Pydantic response models for the admin API."""

from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


# ── Agent Models ─────────────────────────────────────────────────────

class AgentHealth(BaseModel):
    name: str
    display_name: str
    status: str  # "healthy", "degraded", "down", "paused"
    avg_latency_ms: float
    p95_latency_ms: float
    error_count: int
    cases_processed: int
    success_rate: float
    last_active: Optional[str] = None
    uptime_pct: float = 100.0


class AgentDetail(AgentHealth):
    description: str
    recent_errors: list[str] = []
    latency_history: list[float] = []  # last N latency values
    config: dict = {}


class AgentControlRequest(BaseModel):
    action: str  # "pause", "resume", "restart"


class AgentControlResponse(BaseModel):
    agent: str
    action: str
    previous_status: str
    new_status: str
    message: str


# ── Case Models ──────────────────────────────────────────────────────

class CaseStage(BaseModel):
    stage: str
    agent_name: str
    status: str  # "pending", "running", "completed", "error"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    result_summary: Optional[str] = None


class CaseSummary(BaseModel):
    case_id: str
    symptoms: str
    age: int
    gender: str
    status: str  # "in_progress", "completed", "error"
    urgency: Optional[str] = None  # "low", "medium", "high", "critical"
    created_at: str
    completed_at: Optional[str] = None
    total_duration_ms: Optional[float] = None
    current_stage: Optional[str] = None
    agents_completed: int = 0
    agents_total: int = 7


class CaseDetail(CaseSummary):
    stages: list[CaseStage] = []
    final_result: Optional[dict] = None
    agent_outputs: dict = {}


class CaseListResponse(BaseModel):
    cases: list[CaseSummary]
    total: int
    page: int
    limit: int
    total_pages: int


# ── Alert Models ─────────────────────────────────────────────────────

class Alert(BaseModel):
    id: str
    severity: str  # "info", "warning", "error", "critical"
    source: str  # agent name or "system"
    message: str
    timestamp: str
    resolved: bool = False


class AlertListResponse(BaseModel):
    alerts: list[Alert]
    total: int


# ── Overview / Dashboard ────────────────────────────────────────────

class SystemMetrics(BaseModel):
    uptime_seconds: float
    total_cases: int
    active_cases: int
    completed_cases: int
    error_cases: int
    avg_pipeline_duration_ms: float
    cases_last_hour: int
    cases_last_24h: int


class OverviewResponse(BaseModel):
    system: SystemMetrics
    agents: list[AgentHealth]
    recent_cases: list[CaseSummary]
    recent_alerts: list[Alert]


# ── Log Models ──────────────────────────────────────────────────────

class LogEntry(BaseModel):
    id: str
    timestamp: str
    level: str  # info, warning, error, debug
    source: str  # agent name, system, etc.
    message: str
    case_id: Optional[str] = None
    agent: Optional[str] = None
    details: Optional[dict] = None
    trace_id: Optional[str] = None


class LogListResponse(BaseModel):
    logs: list[LogEntry]
    total: int


# ── Config Models ───────────────────────────────────────────────────

class ConfigEntry(BaseModel):
    key: str
    value: Any
    description: str
    category: str  # diagnostics, safety, routing, export, system
    type: str  # number, string, boolean, select
    options: Optional[list] = None  # for select type
    validation: Optional[dict] = None  # min, max, pattern
    updated_at: str
    updated_by: str = "system"
    readonly: bool = False


class ConfigUpdateRequest(BaseModel):
    value: Any


class ConfigUpdateResponse(BaseModel):
    key: str
    value: Any
    previous_value: Any
    updated_at: str
    updated_by: str


# ── Report Models ───────────────────────────────────────────────────

class ReportSummary(BaseModel):
    id: str
    case_id: str
    type: str  # diagnosis, pdf, followup
    status: str  # generated, failed, pending, regenerating
    created_at: str
    updated_at: str
    file_size: Optional[int] = None
    error: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    symptoms_preview: Optional[str] = None


class ReportListResponse(BaseModel):
    reports: list[ReportSummary]
    total: int
    page: int
    total_pages: int


# ── Review Models ───────────────────────────────────────────────────

class ReviewItem(BaseModel):
    id: str
    case_id: str
    type: str  # low_confidence, safety_flag, error, conflicting_outputs
    status: str  # pending, claimed, resolved, escalated
    priority: str  # critical, high, medium, low
    summary: str
    created_at: str
    claimed_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[str] = None


class ReviewListResponse(BaseModel):
    items: list[ReviewItem]
    total: int
    counts: dict  # by status


class ReviewActionRequest(BaseModel):
    action: str  # claim, resolve, escalate, add_note
    notes: Optional[str] = None


# ── Analytics Models ────────────────────────────────────────────────

class AnalyticsResponse(BaseModel):
    throughput: list[dict]  # [{timestamp, count}]
    turnaround_trend: list[dict]  # [{timestamp, avg_ms}]
    agent_latency: dict  # {agent_name: [latency values]}
    error_rates: dict  # {agent_name: float}
    urgency_distribution: dict  # {level: count}
    confidence_distribution: list[dict]  # [{range, count}]
    review_rate: float
    completion_funnel: dict  # {stage: count}
    top_failure_categories: list[dict]  # [{category, count}]
    period: str  # 24h, 7d, 30d


# ── Agent Detail Models ────────────────────────────────────────────

class AgentExecutionRecord(BaseModel):
    case_id: str
    timestamp: str
    latency_ms: float
    success: bool
    error: Optional[str] = None
    token_usage: Optional[dict] = None
    model_used: Optional[str] = None


class AgentLearningInsight(BaseModel):
    category: str
    description: str
    frequency: int
    last_seen: str
    suggestion: Optional[str] = None


class AgentDetailResponse(BaseModel):
    health: AgentHealth  # reuse existing
    description: str
    recent_executions: list[AgentExecutionRecord]
    failure_clusters: list[dict]
    performance_trend: list[dict]  # [{timestamp, avg_latency, error_rate}]
    learning_insights: list[AgentLearningInsight]
    config: dict
    dependencies: list[str]
    downstream: list[str]


# ── Model Comparison ──────────────────────────────────────────────────

class ModelComparisonRequest(BaseModel):
    """Request to run a sample diagnosis across multiple models for comparison."""
    symptoms: str = "I have been experiencing persistent headaches for the past 2 weeks, mostly on the right side. The pain is throbbing, rated 6/10. I also have some light sensitivity and occasional nausea."
    age: int = 35
    gender: str = "female"
    models: list[str] = []  # Empty means use all available

class ModelRunResult(BaseModel):
    model: str
    vendor: str
    status: str  # "completed", "failed", "skipped"
    total_time: float = 0
    agent_timings: dict = {}
    token_usage: dict = {}
    estimated_cost: float = 0
    causes_count: int = 0
    top_diagnosis: Optional[str] = None
    top_confidence: Optional[int] = None
    red_flags_count: int = 0
    tests_count: int = 0
    error: Optional[str] = None

class ModelComparisonResult(BaseModel):
    id: str
    started_at: str
    completed_at: Optional[str] = None
    status: str  # "running", "completed", "partial"
    prompt: str
    age: int
    gender: str
    models_requested: list[str]
    results: list[ModelRunResult] = []

class ModelComparisonListResponse(BaseModel):
    comparisons: list[ModelComparisonResult]
    total: int
