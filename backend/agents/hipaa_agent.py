"""HIPAA Compliance Agent — PII redaction, audit trails, and compliance monitoring."""

import re
import random
import uuid
from datetime import datetime, timezone, timedelta


class HIPAAComplianceAgent:
    """Manages HIPAA compliance: PII redaction, audit logging, and compliance checks."""

    # Regex patterns for PII detection
    PII_PATTERNS = {
        "SSN": (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
        "PHONE": (r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]"),
        "EMAIL": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]"),
        "DOB": (r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}\b", "[REDACTED_DOB]"),
        "DOB_ISO": (r"\b(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b", "[REDACTED_DOB]"),
        "MRN": (r"\bMRN[:\s]?\d{6,10}\b", "[REDACTED_MRN]"),
        "NAME_PREFIX": (r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b", "[REDACTED_NAME]"),
    }

    def __init__(self):
        self._audit_log: list[dict] = []
        self._compliance_issues: list[dict] = []
        self._retention_records: list[dict] = []
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 50 audit log entries and compliance issues."""
        now = datetime.now(timezone.utc)

        actions = [
            "VIEW_RECORD", "EXPORT_DATA", "MODIFY_RECORD", "DELETE_RECORD",
            "LOGIN", "LOGOUT", "API_ACCESS", "DOWNLOAD_REPORT",
            "CREATE_PATIENT", "UPDATE_DIAGNOSIS", "VIEW_PHI", "SHARE_RECORD",
        ]
        resources = [
            "patient/P-1001", "patient/P-1042", "patient/P-1087",
            "diagnosis/D-2001", "diagnosis/D-2034", "diagnosis/D-2099",
            "report/R-3001", "report/R-3015", "settings/encryption",
            "audit/export", "user/admin-01", "user/dr-smith",
        ]
        users = [
            "admin-01", "dr-smith", "dr-jones", "nurse-patel",
            "tech-wong", "dr-garcia", "receptionist-lee", "admin-02",
        ]

        for i in range(50):
            days_ago = random.randint(0, 30)
            ts = now - timedelta(
                days=days_ago,
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
            action = random.choice(actions)
            self._audit_log.append({
                "id": f"audit-{uuid.uuid4().hex[:8]}",
                "timestamp": ts.isoformat(),
                "user_id": random.choice(users),
                "action": action,
                "resource": random.choice(resources),
                "ip_address": f"192.168.1.{random.randint(10, 200)}",
                "success": random.random() > 0.05,
                "details": f"User performed {action.lower().replace('_', ' ')} operation",
            })

        # Sort audit log newest first
        self._audit_log.sort(key=lambda x: x["timestamp"], reverse=True)

        # 3 medium-risk compliance issues
        self._compliance_issues = [
            {
                "id": "issue-001",
                "category": "access_control",
                "severity": "medium",
                "title": "Shared login credentials detected",
                "description": "Two concurrent sessions detected for user 'dr-smith' from different IP addresses within a 5-minute window.",
                "detected_at": (now - timedelta(days=2)).isoformat(),
                "status": "open",
                "recommendation": "Enforce single-session policy and enable MFA for all clinical users.",
            },
            {
                "id": "issue-002",
                "category": "encryption",
                "severity": "medium",
                "title": "Unencrypted backup storage detected",
                "description": "Database backup files on secondary storage volume are not encrypted at rest.",
                "detected_at": (now - timedelta(days=5)).isoformat(),
                "status": "in_progress",
                "recommendation": "Enable AES-256 encryption on all backup storage volumes.",
            },
            {
                "id": "issue-003",
                "category": "training",
                "severity": "medium",
                "title": "Staff HIPAA training overdue",
                "description": "3 staff members have not completed annual HIPAA training. Training was due 15 days ago.",
                "detected_at": (now - timedelta(days=15)).isoformat(),
                "status": "open",
                "recommendation": "Send training reminders and schedule makeup sessions within 7 days.",
            },
        ]

        # Seed retention records
        self._retention_records = [
            {"age_bracket": "0-1 years", "record_count": 342, "category": "active"},
            {"age_bracket": "1-3 years", "record_count": 891, "category": "active"},
            {"age_bracket": "3-5 years", "record_count": 567, "category": "active"},
            {"age_bracket": "5-7 years", "record_count": 234, "category": "review"},
            {"age_bracket": "7+ years", "record_count": 89, "category": "due_for_deletion"},
        ]

    def redact_pii(self, text: str) -> dict:
        """Replace PII in text with redaction markers."""
        redacted = text
        redactions_found = []

        for pii_type, (pattern, replacement) in self.PII_PATTERNS.items():
            matches = re.findall(pattern, redacted)
            if matches:
                redactions_found.extend(
                    {"type": pii_type, "count": len(matches)}
                    for _ in []  # don't expose matched values
                )
                if matches:
                    redactions_found.append({"type": pii_type, "count": len(matches)})
                redacted = re.sub(pattern, replacement, redacted)

        return {
            "original_length": len(text),
            "redacted_text": redacted,
            "redactions_applied": redactions_found,
            "total_redactions": sum(r["count"] for r in redactions_found),
            "is_clean": len(redactions_found) == 0,
        }

    def log_access(self, user_id: str, resource: str, action: str) -> dict:
        """Record an audit trail entry."""
        entry = {
            "id": f"audit-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "ip_address": "0.0.0.0",
            "success": True,
            "details": f"User {user_id} performed {action} on {resource}",
        }
        self._audit_log.insert(0, entry)
        return {"status": "logged", "entry": entry}

    def get_audit_trail(self, filters: dict | None = None) -> dict:
        """Return paginated audit logs with optional filters."""
        filters = filters or {}
        logs = list(self._audit_log)

        if filters.get("user_id"):
            logs = [l for l in logs if l["user_id"] == filters["user_id"]]
        if filters.get("action"):
            logs = [l for l in logs if l["action"] == filters["action"]]
        if filters.get("resource"):
            logs = [l for l in logs if filters["resource"] in l["resource"]]

        page = filters.get("page", 1)
        limit = filters.get("limit", 20)
        total = len(logs)
        start = (page - 1) * limit
        end = start + limit

        return {
            "entries": logs[start:end],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": max(1, (total + limit - 1) // limit),
        }

    def check_compliance_status(self) -> dict:
        """Return compliance score and checklist."""
        checklist = [
            {"requirement": "Data Encryption at Rest", "status": "compliant", "category": "encryption", "last_checked": "2026-03-30T10:00:00Z"},
            {"requirement": "Data Encryption in Transit (TLS 1.3)", "status": "compliant", "category": "encryption", "last_checked": "2026-03-30T10:00:00Z"},
            {"requirement": "Role-Based Access Control (RBAC)", "status": "compliant", "category": "access_control", "last_checked": "2026-03-29T14:00:00Z"},
            {"requirement": "Multi-Factor Authentication", "status": "partial", "category": "access_control", "last_checked": "2026-03-28T09:00:00Z"},
            {"requirement": "Business Associate Agreement (BAA)", "status": "compliant", "category": "legal", "last_checked": "2026-03-15T12:00:00Z"},
            {"requirement": "Annual Staff Training", "status": "non_compliant", "category": "training", "last_checked": "2026-03-25T08:00:00Z"},
            {"requirement": "Audit Logging Enabled", "status": "compliant", "category": "audit", "last_checked": "2026-03-30T10:00:00Z"},
            {"requirement": "Data Backup & Recovery Plan", "status": "compliant", "category": "backup", "last_checked": "2026-03-27T16:00:00Z"},
            {"requirement": "Incident Response Plan", "status": "compliant", "category": "incident", "last_checked": "2026-03-20T11:00:00Z"},
            {"requirement": "Minimum Necessary Access Policy", "status": "partial", "category": "access_control", "last_checked": "2026-03-29T14:00:00Z"},
            {"requirement": "PHI De-identification Procedures", "status": "compliant", "category": "privacy", "last_checked": "2026-03-28T10:00:00Z"},
            {"requirement": "Patient Rights (Access/Amendment)", "status": "compliant", "category": "privacy", "last_checked": "2026-03-26T09:00:00Z"},
        ]

        compliant_count = sum(1 for c in checklist if c["status"] == "compliant")
        partial_count = sum(1 for c in checklist if c["status"] == "partial")
        total = len(checklist)

        return {
            "compliance_score": 87,
            "grade": "B+",
            "total_requirements": total,
            "compliant": compliant_count,
            "partial": partial_count,
            "non_compliant": total - compliant_count - partial_count,
            "checklist": checklist,
            "issues": self._compliance_issues,
            "last_assessment": "2026-03-30T10:00:00Z",
            "next_assessment": "2026-04-30T10:00:00Z",
        }

    def generate_compliance_report(self) -> dict:
        """Generate a structured compliance report."""
        now = datetime.now(timezone.utc)
        status = self.check_compliance_status()

        return {
            "report_id": f"hipaa-rpt-{uuid.uuid4().hex[:8]}",
            "generated_at": now.isoformat(),
            "period": {
                "start": (now - timedelta(days=30)).isoformat(),
                "end": now.isoformat(),
            },
            "summary": {
                "overall_score": status["compliance_score"],
                "grade": status["grade"],
                "risk_level": "medium",
                "total_requirements_assessed": status["total_requirements"],
                "compliant": status["compliant"],
                "non_compliant": status["non_compliant"],
                "partial": status["partial"],
            },
            "findings": [
                {
                    "id": "F-001",
                    "category": "Access Control",
                    "severity": "medium",
                    "finding": "Multi-Factor Authentication not enforced for all users",
                    "impact": "Increased risk of unauthorized access to PHI",
                    "recommendation": "Enable mandatory MFA for all users with PHI access",
                    "remediation_deadline": (now + timedelta(days=30)).isoformat(),
                },
                {
                    "id": "F-002",
                    "category": "Training",
                    "severity": "medium",
                    "finding": "3 staff members overdue for annual HIPAA training",
                    "impact": "Non-compliance with HIPAA training requirements",
                    "recommendation": "Schedule and complete training within 7 days",
                    "remediation_deadline": (now + timedelta(days=7)).isoformat(),
                },
                {
                    "id": "F-003",
                    "category": "Encryption",
                    "severity": "medium",
                    "finding": "Backup storage encryption gap identified",
                    "impact": "Potential PHI exposure in backup files",
                    "recommendation": "Enable AES-256 encryption on all backup volumes",
                    "remediation_deadline": (now + timedelta(days=14)).isoformat(),
                },
            ],
            "audit_summary": {
                "total_events": len(self._audit_log),
                "failed_access_attempts": sum(1 for l in self._audit_log if not l["success"]),
                "unique_users": len(set(l["user_id"] for l in self._audit_log)),
                "phi_access_events": sum(1 for l in self._audit_log if "VIEW_PHI" in l["action"]),
            },
            "recommendations": [
                {"priority": "high", "action": "Enforce MFA for all clinical users", "effort": "low"},
                {"priority": "high", "action": "Complete overdue HIPAA training", "effort": "low"},
                {"priority": "medium", "action": "Encrypt backup storage volumes", "effort": "medium"},
                {"priority": "low", "action": "Review and tighten minimum necessary access policies", "effort": "medium"},
                {"priority": "low", "action": "Conduct tabletop incident response exercise", "effort": "high"},
            ],
        }

    def get_data_retention_status(self) -> dict:
        """Return records count by age and retention policy."""
        total_records = sum(r["record_count"] for r in self._retention_records)
        due_for_deletion = sum(
            r["record_count"] for r in self._retention_records if r["category"] == "due_for_deletion"
        )

        return {
            "total_records": total_records,
            "records_by_age": self._retention_records,
            "due_for_deletion": due_for_deletion,
            "retention_policy": {
                "medical_records": "7 years from last encounter",
                "audit_logs": "6 years",
                "billing_records": "7 years",
                "consent_forms": "10 years",
            },
            "last_purge": "2026-01-15T03:00:00Z",
            "next_scheduled_purge": "2026-04-15T03:00:00Z",
            "auto_purge_enabled": True,
        }

    def enforce_retention(self) -> dict:
        """Mark expired records for deletion."""
        now = datetime.now(timezone.utc)
        expired_count = sum(
            r["record_count"] for r in self._retention_records if r["category"] == "due_for_deletion"
        )

        return {
            "status": "retention_enforced",
            "records_marked_for_deletion": expired_count,
            "enforcement_timestamp": now.isoformat(),
            "next_auto_purge": "2026-04-15T03:00:00Z",
            "details": f"{expired_count} records past the 7-year retention period have been marked for secure deletion.",
        }


# Singleton
_hipaa_agent = None


def get_hipaa_agent() -> HIPAAComplianceAgent:
    global _hipaa_agent
    if _hipaa_agent is None:
        _hipaa_agent = HIPAAComplianceAgent()
    return _hipaa_agent
