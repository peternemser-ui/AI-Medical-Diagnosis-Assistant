"""Admin API router for the medical AI dashboard."""

import math
import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request

from .metrics import get_metrics
from .models import (
    AgentControlRequest,
    AgentControlResponse,
    AgentDetail,
    AgentDetailResponse,
    AgentExecutionRecord,
    AgentHealth,
    AgentLearningInsight,
    Alert,
    AlertListResponse,
    AnalyticsResponse,
    CaseDetail,
    CaseListResponse,
    CaseStage,
    CaseSummary,
    ConfigEntry,
    ConfigUpdateRequest,
    ConfigUpdateResponse,
    LogEntry,
    LogListResponse,
    ModelComparisonRequest,
    OverviewResponse,
    ReportListResponse,
    ReportSummary,
    ReviewActionRequest,
    ReviewItem,
    ReviewListResponse,
    SystemMetrics,
)

admin_router = APIRouter(prefix="/api/admin", tags=["admin"])


# ── Overview ─────────────────────────────────────────────────────────

@admin_router.get("/overview", response_model=OverviewResponse)
async def get_overview():
    """Dashboard metrics summary with agents, recent cases, and alerts."""
    m = get_metrics()
    system = SystemMetrics(**m.get_system_metrics())
    agents = [AgentHealth(**_agent_health_dict(a)) for a in m.get_all_agents()]
    recent_cases_raw, _ = m.case_store.list_cases(limit=5)
    recent_cases = [CaseSummary(**_case_summary_dict(c)) for c in recent_cases_raw]
    recent_alerts = [Alert(**a) for a in m.get_alerts(limit=10)]
    return OverviewResponse(
        system=system,
        agents=agents,
        recent_cases=recent_cases,
        recent_alerts=recent_alerts,
    )


# ── Agents ───────────────────────────────────────────────────────────

@admin_router.get("/agents", response_model=list[AgentHealth])
async def list_agents():
    """List all agents with health data."""
    m = get_metrics()
    return [AgentHealth(**_agent_health_dict(a)) for a in m.get_all_agents()]


@admin_router.get("/agents/{name}", response_model=AgentDetail)
async def get_agent(name: str):
    """Get detailed info for a single agent."""
    m = get_metrics()
    agent = m.get_agent_health(name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return AgentDetail(**agent)


@admin_router.get("/agents/{name}/detail")
async def get_agent_detail(name: str):
    """Get comprehensive agent detail including executions, trends, and insights."""
    try:
        m = get_metrics()
        detail = m.get_agent_detail(name)
        if not detail:
            raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
        return detail
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent detail: {str(e)}")


@admin_router.get("/agents/{name}/executions")
async def get_agent_executions(name: str, limit: int = Query(50, ge=1, le=200)):
    """Get recent execution records for an agent."""
    try:
        m = get_metrics()
        agent = m.get_agent_health(name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
        execs = m.get_agent_executions(name, limit=limit)
        return {"executions": execs, "total": len(execs)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent executions: {str(e)}")


@admin_router.post("/agents/{name}/control", response_model=AgentControlResponse)
async def control_agent(name: str, body: AgentControlRequest):
    """Pause, resume, or restart an agent."""
    m = get_metrics()
    agent = m.get_agent_health(name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")

    action = body.action.lower()
    if action not in ("pause", "resume", "restart"):
        raise HTTPException(status_code=400, detail=f"Invalid action '{action}'. Use: pause, resume, restart")

    status_map = {
        "pause": "paused",
        "resume": "healthy",
        "restart": "healthy",
    }
    new_status = status_map[action]
    result = m.set_agent_status(name, new_status)

    # Log an alert for the action
    m.add_alert(
        severity="info",
        source=name,
        message=f"Agent '{name}' {action}d by admin",
    )
    m.save_now()

    return AgentControlResponse(
        agent=name,
        action=action,
        previous_status=result["previous_status"],
        new_status=result["new_status"],
        message=f"Agent '{name}' successfully {action}d",
    )


# ── Cases ────────────────────────────────────────────────────────────

@admin_router.get("/cases", response_model=CaseListResponse)
async def list_cases(
    status: Optional[str] = Query(None, description="Filter by status: in_progress, completed, error"),
    urgency: Optional[str] = Query(None, description="Filter by urgency: low, medium, high, critical"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """Paginated case list with optional filters."""
    m = get_metrics()
    cases_raw, total = m.case_store.list_cases(
        status=status, urgency=urgency, page=page, limit=limit
    )
    cases = [CaseSummary(**_case_summary_dict(c)) for c in cases_raw]
    total_pages = max(1, math.ceil(total / limit))
    return CaseListResponse(
        cases=cases,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )


@admin_router.get("/cases/counts")
async def get_case_counts():
    """Get case counts by status for tab badges."""
    try:
        m = get_metrics()
        counts = m.case_store.status_counts()
        counts["total"] = m.case_store.total_count
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case counts: {str(e)}")


@admin_router.get("/cases/{case_id}", response_model=CaseDetail)
async def get_case(case_id: str):
    """Full case detail including all pipeline stages."""
    m = get_metrics()
    case = m.case_store.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    return CaseDetail(
        **_case_summary_dict(case),
        stages=[CaseStage(**s) for s in case.get("stages", [])],
        final_result=case.get("final_result"),
        agent_outputs=case.get("agent_outputs", {}),
    )


@admin_router.get("/cases/{case_id}/timeline")
async def get_case_timeline(case_id: str):
    """Get an ordered timeline of events for a case."""
    try:
        m = get_metrics()
        timeline = m.case_store.get_case_timeline(case_id)
        if timeline is None:
            raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
        return {"case_id": case_id, "events": timeline}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case timeline: {str(e)}")


# ── Alerts ───────────────────────────────────────────────────────────

@admin_router.get("/alerts", response_model=AlertListResponse)
async def list_alerts(
    limit: int = Query(50, ge=1, le=200, description="Max alerts to return"),
):
    """Recent alerts sorted newest first."""
    m = get_metrics()
    alerts = [Alert(**a) for a in m.get_alerts(limit=limit)]
    return AlertListResponse(alerts=alerts, total=len(alerts))


# ── Logs ─────────────────────────────────────────────────────────────

@admin_router.get("/logs")
async def get_logs(
    level: Optional[str] = Query(None, description="Filter by level: info, warning, error, debug"),
    source: Optional[str] = Query(None, description="Filter by source"),
    agent: Optional[str] = Query(None, description="Filter by agent name"),
    case_id: Optional[str] = Query(None, description="Filter by case ID"),
    search: Optional[str] = Query(None, description="Search in message text"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """Get filtered and paginated logs."""
    try:
        m = get_metrics()
        logs, total = m.get_logs(
            level=level, source=source, agent=agent,
            case_id=case_id, search=search,
            limit=limit, offset=offset,
        )
        return {"logs": logs, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")


# ── Config ───────────────────────────────────────────────────────────

@admin_router.get("/config")
async def get_config():
    """Get all configuration entries."""
    try:
        m = get_metrics()
        return {"config": m.get_config()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")


@admin_router.put("/config/{key}")
async def update_config(key: str, req: ConfigUpdateRequest):
    """Update a configuration value."""
    try:
        m = get_metrics()
        entry = m.get_config_entry(key)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Config key '{key}' not found")
        if entry.get("readonly"):
            raise HTTPException(status_code=400, detail=f"Config key '{key}' is read-only")

        result = m.update_config(key, req.value, updated_by="admin")
        if not result:
            raise HTTPException(status_code=400, detail=f"Failed to update config key '{key}'")

        m.save_now()
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config: {str(e)}")


# ── Reports ──────────────────────────────────────────────────────────

@admin_router.get("/reports")
async def get_reports(
    status: Optional[str] = Query(None, description="Filter by status: generated, failed, pending, regenerating"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Get paginated list of reports."""
    try:
        m = get_metrics()
        reports, total = m.get_reports(status=status, page=page, limit=limit)
        total_pages = max(1, math.ceil(total / limit))
        return {
            "reports": reports,
            "total": total,
            "page": page,
            "total_pages": total_pages,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get reports: {str(e)}")


@admin_router.post("/reports/{report_id}/regenerate")
async def regenerate_report(report_id: str):
    """Mark a report for regeneration."""
    try:
        m = get_metrics()
        report = m.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found")

        updated = m.update_report_status(report_id, "regenerating")
        m.add_log(
            level="info",
            source="reports",
            message=f"Report {report_id} marked for regeneration",
            case_id=report.get("case_id"),
        )
        return {"status": "regenerating", "report": updated}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate report: {str(e)}")


# ── Reviews ──────────────────────────────────────────────────────────

@admin_router.get("/reviews")
async def get_reviews(
    status: Optional[str] = Query(None, description="Filter by status: pending, claimed, resolved, escalated"),
    limit: int = Query(50, ge=1, le=200),
):
    """Get review items with status counts."""
    try:
        m = get_metrics()
        items, counts = m.get_reviews(status=status, limit=limit)
        return {
            "items": items,
            "total": len(items),
            "counts": counts,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get reviews: {str(e)}")


@admin_router.post("/reviews/{review_id}/action")
async def review_action(review_id: str, req: ReviewActionRequest):
    """Apply an action to a review item."""
    try:
        m = get_metrics()
        review = m.get_review(review_id)
        if not review:
            raise HTTPException(status_code=404, detail=f"Review '{review_id}' not found")

        valid_actions = ("claim", "resolve", "escalate", "add_note")
        if req.action not in valid_actions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action '{req.action}'. Use: {', '.join(valid_actions)}"
            )

        updated = m.update_review(review_id, req.action, notes=req.notes)
        if not updated:
            raise HTTPException(status_code=400, detail="Failed to apply action")

        m.add_log(
            level="info",
            source="reviews",
            message=f"Review {review_id} action: {req.action}",
            case_id=review.get("case_id"),
        )
        m.save_now()
        return {"status": "ok", "review": updated}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process review action: {str(e)}")


# ── Analytics ────────────────────────────────────────────────────────

@admin_router.get("/analytics")
async def get_analytics(
    period: str = Query("24h", description="Time period: 24h, 7d, 30d"),
):
    """Get analytics data for the specified period."""
    try:
        valid_periods = ("24h", "7d", "30d")
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period '{period}'. Use: {', '.join(valid_periods)}"
            )
        m = get_metrics()
        return m.get_analytics(period=period)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


# ── Helpers ──────────────────────────────────────────────────────────

def _agent_health_dict(agent: dict) -> dict:
    """Extract only AgentHealth fields from internal agent dict."""
    return {
        "name": agent["name"],
        "display_name": agent["display_name"],
        "status": agent["status"],
        "avg_latency_ms": agent["avg_latency_ms"],
        "p95_latency_ms": agent["p95_latency_ms"],
        "error_count": agent["error_count"],
        "cases_processed": agent["cases_processed"],
        "success_rate": agent["success_rate"],
        "last_active": agent.get("last_active"),
        "uptime_pct": agent.get("uptime_pct", 100.0),
    }


def _case_summary_dict(case: dict) -> dict:
    """Extract CaseSummary fields from internal case dict."""
    return {
        "case_id": case["case_id"],
        "symptoms": case["symptoms"],
        "age": case["age"],
        "gender": case["gender"],
        "status": case["status"],
        "urgency": case.get("urgency"),
        "created_at": case["created_at"],
        "completed_at": case.get("completed_at"),
        "total_duration_ms": case.get("total_duration_ms"),
        "current_stage": case.get("current_stage"),
        "agents_completed": case.get("agents_completed", 0),
        "agents_total": case.get("agents_total", 7),
    }


# ── SEO & Marketing ─────────────────────────────────────────────────

from agents.seo_agent import get_seo_agent


@admin_router.get("/seo/audit")
async def seo_audit():
    """SEO health check — scores, issues, and recommendations."""
    try:
        agent = get_seo_agent()
        return agent.get_seo_audit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SEO audit failed: {str(e)}")


@admin_router.get("/seo/meta/{page}")
async def seo_meta(page: str):
    """Get SEO meta tags for a specific page."""
    try:
        agent = get_seo_agent()
        return agent.generate_meta_tags(page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate meta tags: {str(e)}")


@admin_router.post("/seo/blog-ideas")
async def seo_blog_ideas():
    """Generate blog content suggestions from recent diagnosis patterns."""
    try:
        agent = get_seo_agent()
        suggestions = agent.generate_blog_suggestions()
        return {"suggestions": suggestions, "total": len(suggestions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate blog ideas: {str(e)}")


@admin_router.post("/seo/social-share")
async def seo_social_share(request: Request):
    """Generate social share card content from a diagnosis result."""
    try:
        body = await request.json()
        agent = get_seo_agent()
        return agent.generate_social_share(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate social share: {str(e)}")


@admin_router.get("/seo/landing/{specialty}")
async def seo_landing_page(specialty: str):
    """Generate landing page copy for a medical specialty."""
    try:
        agent = get_seo_agent()
        return agent.generate_landing_page_copy(specialty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate landing page: {str(e)}")


# ── Billing (Admin) ─────────────────────────────────────────────────

from agents.billing_agent import get_billing_agent


@admin_router.get("/billing/summary")
async def billing_summary():
    """Revenue metrics for the admin dashboard."""
    try:
        agent = get_billing_agent()
        return agent.get_revenue_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get billing summary: {str(e)}")


@admin_router.get("/billing/usage")
async def billing_usage_admin():
    """Platform-wide usage statistics."""
    try:
        agent = get_billing_agent()
        return agent.get_platform_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get billing usage: {str(e)}")


# ── Billing (Public) ────────────────────────────────────────────────

billing_router = APIRouter(prefix="/api/billing", tags=["billing"])


@billing_router.get("/usage")
async def billing_usage_user(user_id: str = Query("user-001", description="User ID")):
    """Current user's usage and quota."""
    try:
        agent = get_billing_agent()
        return agent.check_usage(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get usage: {str(e)}")


@billing_router.post("/checkout")
async def billing_checkout(request: Request):
    """Create a Stripe checkout session (mock)."""
    try:
        body = await request.json()
        agent = get_billing_agent()
        result = agent.create_checkout_session(
            user_id=body.get("user_id", "user-001"),
            tier=body.get("tier", "starter"),
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout: {str(e)}")


@billing_router.post("/webhook")
async def billing_webhook(request: Request):
    """Handle Stripe webhook events (mock)."""
    try:
        body = await request.json()
        agent = get_billing_agent()
        return agent.handle_webhook(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


@billing_router.get("/plans")
async def billing_plans():
    """Available subscription plans."""
    try:
        agent = get_billing_agent()
        return {"plans": agent.get_plans()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get plans: {str(e)}")


# ── Notifications ──────────────────────────────────────────────────

from agents.notification_agent import get_notification_agent


@admin_router.get("/notifications/history")
async def notification_history(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    type: Optional[str] = Query(None, description="Filter by channel: email, sms, push"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Paginated notification log."""
    try:
        agent = get_notification_agent()
        return agent.get_notification_history(user_id=user_id, type=type, page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notification history: {str(e)}")


@admin_router.get("/notifications/metrics")
async def notification_metrics():
    """Delivery metrics by channel."""
    try:
        agent = get_notification_agent()
        return agent.get_notification_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notification metrics: {str(e)}")


@admin_router.get("/notifications/webhooks")
async def notification_webhooks():
    """List configured webhooks."""
    try:
        agent = get_notification_agent()
        return {"webhooks": agent.get_webhook_configs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get webhooks: {str(e)}")


# ── Multi-Tenant ───────────────────────────────────────────────────

from agents.tenant_agent import get_tenant_agent


@admin_router.get("/tenants")
async def list_tenants(
    status: Optional[str] = Query(None, description="Filter by status: active, trial, suspended"),
):
    """List all tenants."""
    try:
        agent = get_tenant_agent()
        return {"tenants": agent.list_tenants(status=status)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tenants: {str(e)}")


@admin_router.get("/tenants/analytics")
async def tenant_analytics():
    """Cross-tenant aggregated analytics."""
    try:
        agent = get_tenant_agent()
        return agent.get_cross_tenant_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tenant analytics: {str(e)}")


@admin_router.get("/tenants/metrics")
async def tenant_metrics():
    """Tenant-level metrics summary."""
    try:
        agent = get_tenant_agent()
        return agent.get_tenant_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tenant metrics: {str(e)}")


@admin_router.get("/tenants/{tenant_id}")
async def get_tenant(tenant_id: str):
    """Get tenant detail."""
    try:
        agent = get_tenant_agent()
        tenant = agent.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail=f"Tenant '{tenant_id}' not found")
        return tenant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tenant: {str(e)}")


# ── EHR / FHIR ────────────────────────────────────────────────────

from agents.ehr_agent import get_ehr_agent


@admin_router.get("/ehr/systems")
async def ehr_systems():
    """List connected EHR systems."""
    try:
        agent = get_ehr_agent()
        return {"systems": agent.get_connected_systems()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get EHR systems: {str(e)}")


@admin_router.get("/ehr/sync-history")
async def ehr_sync_history(
    limit: int = Query(20, ge=1, le=100),
):
    """Recent sync operations."""
    try:
        agent = get_ehr_agent()
        history = agent.get_sync_history(limit=limit)
        return {"syncs": history, "total": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sync history: {str(e)}")


@admin_router.get("/ehr/metrics")
async def ehr_metrics():
    """FHIR resource and sync metrics."""
    try:
        agent = get_ehr_agent()
        return agent.get_fhir_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get EHR metrics: {str(e)}")


@admin_router.post("/ehr/convert")
async def ehr_convert(request: Request):
    """Convert a diagnosis result to a FHIR Condition resource."""
    try:
        body = await request.json()
        agent = get_ehr_agent()
        return agent.diagnosis_to_fhir(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert to FHIR: {str(e)}")


# ── Analytics & Insights ──────────────────────────────────────────

from agents.analytics_agent import get_analytics_agent


@admin_router.get("/insights/trends")
async def insights_trends():
    """Population health trends."""
    try:
        agent = get_analytics_agent()
        return agent.get_population_health_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get health trends: {str(e)}")


@admin_router.get("/insights/clusters")
async def insights_clusters():
    """Detected symptom clusters."""
    try:
        agent = get_analytics_agent()
        return agent.detect_symptom_clusters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect clusters: {str(e)}")


@admin_router.get("/insights/report")
async def insights_report(
    month: int = Query(None, ge=1, le=12, description="Month (1-12)"),
    year: int = Query(None, ge=2024, le=2030, description="Year"),
):
    """Monthly intelligence report."""
    try:
        now = datetime.now(timezone.utc)
        m = month or now.month
        y = year or now.year
        agent = get_analytics_agent()
        return agent.generate_monthly_report(m, y)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@admin_router.get("/insights/benchmarks")
async def insights_benchmarks():
    """Diagnostic benchmarks vs published literature."""
    try:
        agent = get_analytics_agent()
        return agent.get_diagnostic_benchmarks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get benchmarks: {str(e)}")


@admin_router.get("/insights/intelligence")
async def insights_intelligence():
    """Platform intelligence — growth, seasonality, drift."""
    try:
        agent = get_analytics_agent()
        return agent.get_platform_intelligence()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get intelligence: {str(e)}")


# ── HIPAA Compliance ─────────────────────────────────────────────

from agents.hipaa_agent import get_hipaa_agent


@admin_router.get("/hipaa/status")
async def hipaa_compliance_status():
    """HIPAA compliance score, checklist, and issues."""
    try:
        agent = get_hipaa_agent()
        return agent.check_compliance_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get compliance status: {str(e)}")


@admin_router.get("/hipaa/audit-trail")
async def hipaa_audit_trail(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type"),
    resource: Optional[str] = Query(None, description="Filter by resource (partial match)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Paginated HIPAA audit logs."""
    try:
        agent = get_hipaa_agent()
        filters = {"page": page, "limit": limit}
        if user_id:
            filters["user_id"] = user_id
        if action:
            filters["action"] = action
        if resource:
            filters["resource"] = resource
        return agent.get_audit_trail(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get audit trail: {str(e)}")


@admin_router.get("/hipaa/retention")
async def hipaa_retention_status():
    """Data retention status and policy."""
    try:
        agent = get_hipaa_agent()
        return agent.get_data_retention_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get retention status: {str(e)}")


@admin_router.post("/hipaa/report")
async def hipaa_compliance_report():
    """Generate a structured HIPAA compliance report."""
    try:
        agent = get_hipaa_agent()
        return agent.generate_compliance_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate compliance report: {str(e)}")


# ── Quality Assurance ────────────────────────────────────────────

from agents.qa_agent import get_qa_agent


@admin_router.get("/qa/scorecard")
async def qa_accuracy_scorecard():
    """Accuracy scorecard with per-agent metrics."""
    try:
        agent = get_qa_agent()
        return agent.get_accuracy_scorecard()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get accuracy scorecard: {str(e)}")


@admin_router.get("/qa/metrics")
async def qa_quality_metrics():
    """Quality dashboard data: accuracy trends, error categories, agent reliability."""
    try:
        agent = get_qa_agent()
        return agent.get_quality_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get quality metrics: {str(e)}")


@admin_router.post("/qa/benchmark")
async def qa_run_benchmark():
    """Run diagnosis benchmark against known test cases."""
    try:
        agent = get_qa_agent()
        return agent.run_benchmark()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run benchmark: {str(e)}")


@admin_router.get("/qa/regressions")
async def qa_regression_results():
    """Results of the last regression test run."""
    try:
        agent = get_qa_agent()
        return agent.get_regression_results()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get regression results: {str(e)}")


# ── Patient Follow-Up ───────────────────────────────────────────

from agents.followup_agent import get_followup_agent


@admin_router.get("/followup/pending")
async def followup_pending():
    """All overdue and upcoming follow-ups."""
    try:
        agent = get_followup_agent()
        return agent.get_pending_followups()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pending follow-ups: {str(e)}")


@admin_router.get("/followup/metrics")
async def followup_metrics():
    """Follow-up compliance rate, overdue count, and visit frequency."""
    try:
        agent = get_followup_agent()
        return agent.get_followup_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get follow-up metrics: {str(e)}")


@admin_router.get("/followup/trends")
async def followup_worsening_trends():
    """Detect patients with worsening symptom trends."""
    try:
        agent = get_followup_agent()
        return agent.detect_worsening_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect worsening trends: {str(e)}")


# ── Medical Image Analysis ──────────────────────────────────────

from agents.image_agent import get_image_agent


@admin_router.get("/imaging/metrics")
async def imaging_metrics():
    """Image analysis metrics: volume, accuracy, processing time, findings distribution."""
    try:
        agent = get_image_agent()
        return agent.get_analysis_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get imaging metrics: {str(e)}")


# ── Drug Interactions ──────────────────────────────────────────────

from agents.drug_interaction_agent import get_drug_interaction_agent


@admin_router.post("/drugs/check")
async def drugs_check(request: Request):
    """Check a list of medications for interactions."""
    try:
        body = await request.json()
        agent = get_drug_interaction_agent()
        medications = body.get("medications", [])
        if not medications:
            raise HTTPException(status_code=400, detail="'medications' list is required")
        result = agent.check_interactions(medications)
        # Optionally check allergies if provided
        allergies = body.get("known_allergies")
        if allergies:
            result["allergy_check"] = agent.check_allergies(medications, allergies)
        # Optionally check contraindications if conditions provided
        conditions = body.get("conditions")
        if conditions:
            contra_results = []
            for med in medications:
                contra_results.append(agent.get_contraindications(med, conditions))
            result["contraindication_checks"] = contra_results
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drug interaction check failed: {str(e)}")


@admin_router.post("/drugs/guide")
async def drugs_guide(request: Request):
    """Generate a patient-friendly medication guide."""
    try:
        body = await request.json()
        medication = body.get("medication", "")
        if not medication:
            raise HTTPException(status_code=400, detail="'medication' is required")
        agent = get_drug_interaction_agent()
        return agent.generate_medication_guide(medication)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate medication guide: {str(e)}")


@admin_router.get("/drugs/stats")
async def drugs_stats():
    """Drug interaction database statistics."""
    try:
        agent = get_drug_interaction_agent()
        return agent.get_interaction_database_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drug stats: {str(e)}")


@admin_router.post("/drugs/dosage")
async def drugs_dosage(request: Request):
    """Validate dosage for a patient profile."""
    try:
        body = await request.json()
        medication = body.get("medication", "")
        dose = body.get("dose")
        patient_age = body.get("patient_age")
        if not medication or dose is None or patient_age is None:
            raise HTTPException(status_code=400, detail="'medication', 'dose', and 'patient_age' are required")
        agent = get_drug_interaction_agent()
        return agent.check_dosage_safety(
            medication=medication,
            dose=float(dose),
            patient_age=int(patient_age),
            patient_weight=body.get("patient_weight"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosage check failed: {str(e)}")


# ── Insurance Pre-Auth ─────────────────────────────────────────────

from agents.insurance_agent import get_insurance_agent


@admin_router.post("/insurance/icd10")
async def insurance_icd10(request: Request):
    """Map a diagnosis name to ICD-10 code(s)."""
    try:
        body = await request.json()
        diagnosis = body.get("diagnosis", "")
        if not diagnosis:
            raise HTTPException(status_code=400, detail="'diagnosis' is required")
        agent = get_insurance_agent()
        return agent.map_to_icd10(diagnosis)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ICD-10 mapping failed: {str(e)}")


@admin_router.post("/insurance/preauth")
async def insurance_preauth(request: Request):
    """Generate a pre-authorization request letter."""
    try:
        body = await request.json()
        patient_info = body.get("patient_info", {})
        diagnosis = body.get("diagnosis", "")
        procedures = body.get("procedures", [])
        if not diagnosis or not procedures:
            raise HTTPException(status_code=400, detail="'diagnosis' and 'procedures' are required")
        agent = get_insurance_agent()
        return agent.generate_preauth_letter(patient_info, diagnosis, procedures)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pre-auth generation failed: {str(e)}")


@admin_router.post("/insurance/estimate")
async def insurance_estimate(request: Request):
    """Estimate patient out-of-pocket costs."""
    try:
        body = await request.json()
        procedures = body.get("procedures", [])
        insurance_type = body.get("insurance_type", "ppo")
        if not procedures:
            raise HTTPException(status_code=400, detail="'procedures' list is required")
        agent = get_insurance_agent()
        result = agent.estimate_costs(procedures, insurance_type)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cost estimation failed: {str(e)}")


@admin_router.get("/insurance/metrics")
async def insurance_metrics():
    """Pre-authorization performance metrics."""
    try:
        agent = get_insurance_agent()
        return agent.get_preauth_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insurance metrics: {str(e)}")


@admin_router.post("/insurance/coverage")
async def insurance_coverage(request: Request):
    """Get coverage summary for an insurance type and diagnosis codes."""
    try:
        body = await request.json()
        insurance_type = body.get("insurance_type", "ppo")
        icd10_codes = body.get("icd10_codes", [])
        agent = get_insurance_agent()
        result = agent.get_coverage_summary(insurance_type, icd10_codes)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coverage check failed: {str(e)}")


# ── Health Literacy ────────────────────────────────────────────────

from agents.literacy_agent import get_literacy_agent


@admin_router.post("/literacy/simplify")
async def literacy_simplify(request: Request):
    """Simplify medical text to a target reading level."""
    try:
        body = await request.json()
        text = body.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="'text' is required")
        grade_level = body.get("target_grade_level", 5)
        agent = get_literacy_agent()
        return agent.simplify_text(text, target_grade_level=grade_level)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text simplification failed: {str(e)}")


@admin_router.post("/literacy/explain")
async def literacy_explain(request: Request):
    """Explain a medical term in plain English."""
    try:
        body = await request.json()
        term = body.get("term", "")
        if not term:
            raise HTTPException(status_code=400, detail="'term' is required")
        agent = get_literacy_agent()
        return agent.explain_term(term)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Term explanation failed: {str(e)}")


@admin_router.post("/literacy/educate")
async def literacy_educate(request: Request):
    """Generate a patient education packet for a condition."""
    try:
        body = await request.json()
        condition = body.get("condition", "")
        if not condition:
            raise HTTPException(status_code=400, detail="'condition' is required")
        agent = get_literacy_agent()
        return agent.generate_patient_education(condition)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Patient education generation failed: {str(e)}")


@admin_router.get("/literacy/terms")
async def literacy_terms():
    """Get the full medical terminology database."""
    try:
        agent = get_literacy_agent()
        return agent.get_terminology_database()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get terminology database: {str(e)}")


@admin_router.post("/literacy/readability")
async def literacy_readability(request: Request):
    """Assess readability of a text passage."""
    try:
        body = await request.json()
        text = body.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="'text' is required")
        agent = get_literacy_agent()
        return agent.assess_readability(text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Readability assessment failed: {str(e)}")


# ── Appointment Booking ───────────────────────────────────────────

from agents.booking_agent import get_booking_agent


@admin_router.post("/booking/suggest")
async def booking_suggest(request: Request):
    """Suggest an appointment type based on diagnosis and urgency."""
    try:
        body = await request.json()
        diagnosis = body.get("diagnosis", "")
        urgency = body.get("urgency", "medium")
        if not diagnosis:
            raise HTTPException(status_code=400, detail="'diagnosis' is required")
        agent = get_booking_agent()
        return agent.suggest_appointment_type(diagnosis, urgency)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Appointment suggestion failed: {str(e)}")


@admin_router.get("/booking/metrics")
async def booking_metrics():
    """Booking performance metrics."""
    try:
        agent = get_booking_agent()
        return agent.get_booking_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get booking metrics: {str(e)}")


@admin_router.get("/booking/providers")
async def booking_providers(
    specialty: str = Query(..., description="Medical specialty"),
    location: Optional[str] = Query(None, description="Location filter"),
):
    """Get provider directory for a specialty."""
    try:
        agent = get_booking_agent()
        return agent.get_provider_directory(specialty, location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get provider directory: {str(e)}")


@admin_router.post("/booking/slots")
async def booking_slots(request: Request):
    """Find available appointment slots."""
    try:
        body = await request.json()
        specialty = body.get("specialty", "")
        if not specialty:
            raise HTTPException(status_code=400, detail="'specialty' is required")
        agent = get_booking_agent()
        return agent.find_available_slots(
            specialty=specialty,
            location=body.get("location"),
            date_range=body.get("date_range"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Slot search failed: {str(e)}")


@admin_router.post("/booking/book")
async def booking_book(request: Request):
    """Book an appointment."""
    try:
        body = await request.json()
        patient_id = body.get("patient_id", "")
        provider_id = body.get("provider_id", "")
        slot_id = body.get("slot_id", "")
        if not patient_id or not provider_id or not slot_id:
            raise HTTPException(status_code=400, detail="'patient_id', 'provider_id', and 'slot_id' are required")
        agent = get_booking_agent()
        result = agent.book_appointment(patient_id, provider_id, slot_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")


@admin_router.post("/booking/telehealth-recommend")
async def booking_telehealth_recommend(request: Request):
    """Recommend telehealth vs in-person visit."""
    try:
        body = await request.json()
        diagnosis = body.get("diagnosis", "")
        if not diagnosis:
            raise HTTPException(status_code=400, detail="'diagnosis' is required")
        agent = get_booking_agent()
        return agent.recommend_telehealth_vs_inperson(diagnosis)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Telehealth recommendation failed: {str(e)}")


# ── Model Comparison ──────────────────────────────────────────────────

# Pricing per 1M tokens (approximate)
_MODEL_PRICING = {
    "claude-opus-4-6": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.0},
    "gpt-4o": {"input": 2.50, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "o3": {"input": 10.0, "output": 40.0},
    "o4-mini": {"input": 1.10, "output": 4.40},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.0},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "llama3.1:8b": {"input": 0, "output": 0},
    "llama3.1": {"input": 0, "output": 0},
    "mistral": {"input": 0, "output": 0},
    "gemma2": {"input": 0, "output": 0},
}


@admin_router.get("/models")
async def get_available_models(request: Request):
    """Return available models based on configured API keys."""
    from agents.llm_client import MODEL_CATALOG

    # Check which API keys are available
    all_keys = {
        "anthropic": request.headers.get("x-anthropic-api-key") or os.getenv("ANTHROPIC_API_KEY"),
        "openai": request.headers.get("x-openai-api-key") or os.getenv("OPENAI_API_KEY"),
        "google": request.headers.get("x-google-api-key") or os.getenv("GOOGLE_API_KEY"),
    }

    # Check Ollama
    ollama_available = False
    try:
        import httpx
        resp = httpx.get("http://localhost:11434/api/version", timeout=2)
        ollama_available = resp.status_code == 200
    except Exception:
        pass

    models = []
    for model_key, info in MODEL_CATALOG.items():
        vendor = info.get("vendor", "unknown")
        available = False
        if vendor == "anthropic" and all_keys.get("anthropic"):
            available = True
        elif vendor == "openai" and all_keys.get("openai"):
            available = True
        elif vendor == "google" and all_keys.get("google"):
            available = True
        elif vendor == "ollama" and ollama_available:
            available = True

        # Pricing info (per 1M tokens)
        pricing = _MODEL_PRICING.get(model_key, {"input": 0, "output": 0})

        models.append({
            "model": model_key,
            "model_id": info.get("model_id", model_key),
            "vendor": vendor,
            "available": available,
            "input_price": pricing["input"],
            "output_price": pricing["output"],
        })

    return {"models": models, "keys_configured": {k: bool(v) for k, v in all_keys.items()}, "ollama_available": ollama_available}


@admin_router.post("/compare")
async def run_model_comparison(req: ModelComparisonRequest, request: Request):
    """Start a model comparison in the background, returns immediately with comparison ID."""
    import asyncio
    from agents.llm_client import MODEL_CATALOG

    m = get_metrics()

    # Determine which models to test
    all_keys = {
        "anthropic": request.headers.get("x-anthropic-api-key") or os.getenv("ANTHROPIC_API_KEY"),
        "openai": request.headers.get("x-openai-api-key") or os.getenv("OPENAI_API_KEY"),
        "google": request.headers.get("x-google-api-key") or os.getenv("GOOGLE_API_KEY"),
    }

    if req.models:
        models_to_test = req.models
    else:
        models_to_test = []
        if all_keys.get("anthropic"):
            models_to_test.append("claude-sonnet-4-6")
        if all_keys.get("openai"):
            models_to_test.append("gpt-4o-mini")
        if all_keys.get("google"):
            models_to_test.append("gemini-2.5-flash")
        try:
            import httpx
            resp = httpx.get("http://localhost:11434/api/version", timeout=2)
            if resp.status_code == 200:
                models_to_test.append("llama3.1:8b")
        except Exception:
            pass

    if not models_to_test:
        raise HTTPException(status_code=400, detail="No models available. Configure at least one API key.")

    comp = m.create_comparison(req.symptoms, req.age, req.gender, models_to_test)
    comp_id = comp["id"]

    # Fire-and-forget background task
    asyncio.create_task(_run_comparison_models(comp_id, models_to_test, req, all_keys))

    return {"id": comp_id, "status": "running", "models": models_to_test}


async def _run_comparison_models(comp_id, models_to_test, req, all_keys):
    """Background worker that runs each model through the diagnostic pipeline."""
    import asyncio
    from agents.orchestrator import OrchestratorAgent
    from agents.llm_client import MODEL_CATALOG

    m = get_metrics()

    for model_name in models_to_test:
        catalog_entry = MODEL_CATALOG.get(model_name, {})
        vendor = catalog_entry.get("vendor", "unknown")

        # Determine API key for this vendor
        api_key = all_keys.get(vendor)
        if vendor == "ollama":
            api_key = "ollama"

        if not api_key:
            m.add_comparison_result(comp_id, {
                "model": model_name,
                "vendor": vendor,
                "status": "skipped",
                "total_time": 0,
                "agent_timings": {},
                "token_usage": {},
                "estimated_cost": 0,
                "causes_count": 0,
                "top_diagnosis": None,
                "top_confidence": None,
                "red_flags_count": 0,
                "tests_count": 0,
                "error": f"No API key for {vendor}",
            })
            continue

        try:
            orchestrator = OrchestratorAgent(
                api_key=api_key if vendor != "ollama" else "ollama",
                openai_key=all_keys.get("openai"),
                google_key=all_keys.get("google"),
            )

            result = await orchestrator.run_diagnosis(
                symptoms=req.symptoms,
                age=req.age,
                gender=req.gender,
                model_preference=model_name,
            )

            causes = result.get("causes", [])
            top = causes[0] if causes else {}
            token_usage = result.get("token_usage", {})

            m.add_comparison_result(comp_id, {
                "model": model_name,
                "vendor": vendor,
                "status": "completed",
                "total_time": result.get("total_time", 0),
                "agent_timings": result.get("agent_timings", {}),
                "token_usage": token_usage,
                "estimated_cost": result.get("estimated_cost", 0),
                "causes_count": len(causes),
                "top_diagnosis": top.get("cause", None),
                "top_confidence": top.get("value", None),
                "red_flags_count": len(result.get("red_flags", [])),
                "tests_count": len(result.get("recommended_tests", [])),
                "error": None,
                # Full diagnostic output for side-by-side comparison
                "diagnosis_output": {
                    "causes": causes,
                    "red_flags": result.get("red_flags", []),
                    "recommended_tests": result.get("recommended_tests", []),
                    "treatment_plan": (
                        result.get("agent_details", {}).get("treatment", {}).get("treatment_plans")
                        or result.get("treatment_plans", [])
                    ),
                    "safety": result.get("agent_details", {}).get("safety", {}),
                    "safety_warnings": result.get("safety_warnings", []),
                    "safety_status": result.get("safety_status", ""),
                    "summary": result.get("patient_summary", "") or result.get("answer", ""),
                    "medications": result.get("medications", []),
                    "lifestyle": result.get("lifestyle_recommendations", []),
                    "action_checklist": result.get("action_checklist", []),
                    "warning_signs": result.get("warning_signs", []),
                },
            })
        except Exception as e:
            m.add_comparison_result(comp_id, {
                "model": model_name,
                "vendor": vendor,
                "status": "failed",
                "total_time": 0,
                "agent_timings": {},
                "token_usage": {},
                "estimated_cost": 0,
                "causes_count": 0,
                "top_diagnosis": None,
                "top_confidence": None,
                "red_flags_count": 0,
                "tests_count": 0,
                "error": str(e),
            })

    m.complete_comparison(comp_id)
    m.save_now()


@admin_router.get("/comparisons")
async def get_comparisons(limit: int = Query(20, ge=1, le=100)):
    """Get recent model comparison results."""
    m = get_metrics()
    items, total = m.get_comparisons(limit=limit)
    return {"comparisons": items, "total": total}


@admin_router.get("/comparisons/{comp_id}")
async def get_comparison(comp_id: str):
    """Get a specific model comparison result."""
    m = get_metrics()
    comp = m.get_comparison(comp_id)
    if not comp:
        raise HTTPException(status_code=404, detail=f"Comparison '{comp_id}' not found")
    return comp


# ── Quality Audit ──────────────────────────────────────────────────────

@admin_router.post("/audit")
async def run_quality_audit(request: Request):
    """Run quality audit on all stored diagnosis results."""
    import json
    from pathlib import Path
    from agents.quality_auditor import QualityAuditor

    # Load stored cases from debug files and admin metrics
    cases = []

    # Try to load from debug file
    debug_path = Path(__file__).parent.parent / "_debug_last_result.json"
    if debug_path.exists():
        try:
            cases.append(json.loads(debug_path.read_text()))
        except Exception:
            pass

    # Try to load from admin metrics case store
    try:
        m = get_metrics()
        if hasattr(m, 'case_store') and hasattr(m.case_store, 'cases'):
            for case_id, case_data in m.case_store.cases.items():
                if case_data.get('result'):
                    cases.append(case_data['result'])
    except Exception:
        pass

    if not cases:
        return {"error": "No cases found to audit", "total_cases": 0}

    auditor = QualityAuditor()
    result = auditor.run_full_audit(cases)
    return result


@admin_router.get("/audit/latest")
async def get_latest_audit():
    """Get the most recent audit results."""
    from agents.quality_auditor import QualityAuditor
    auditor = QualityAuditor()
    return auditor.get_latest_audit()


# ── Stripe Configuration ────────────────────────────────────────────

@admin_router.post("/stripe/config")
async def save_stripe_config(request: Request):
    """Save Stripe API keys to environment and .env file."""
    body = await request.json()
    secret_key = body.get("secret_key", "")
    webhook_secret = body.get("webhook_secret", "")

    os.environ["STRIPE_SECRET_KEY"] = secret_key
    os.environ["STRIPE_WEBHOOK_SECRET"] = webhook_secret

    # Also save to .env for persistence
    from pathlib import Path
    env_path = Path(__file__).parent.parent / ".env"
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    new_lines = [l for l in lines if not l.startswith("STRIPE_SECRET_KEY=") and not l.startswith("STRIPE_WEBHOOK_SECRET=")]
    if secret_key:
        new_lines.append(f"STRIPE_SECRET_KEY={secret_key}")
    if webhook_secret:
        new_lines.append(f"STRIPE_WEBHOOK_SECRET={webhook_secret}")
    env_path.write_text("\n".join(new_lines) + "\n")

    return {"status": "saved", "stripe_configured": bool(secret_key)}


@admin_router.get("/stripe/status")
async def get_stripe_status():
    """Check if Stripe is configured and return mode."""
    key = os.getenv("STRIPE_SECRET_KEY", "")
    return {
        "configured": bool(key and key.startswith("sk_")),
        "mode": "live" if key.startswith("sk_live") else "test" if key.startswith("sk_test") else "demo",
    }
