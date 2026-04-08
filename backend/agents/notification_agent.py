"""Notification & Alert Agent — manages email, SMS, push notifications, and webhooks."""

import random
import uuid
from datetime import datetime, timezone, timedelta
from collections import defaultdict


class NotificationAgent:
    """Manages email, SMS, push notifications, system alerts, and webhooks."""

    CHANNELS = ["email", "sms", "push"]

    TEMPLATES = {
        "diagnosis_complete": {
            "subject": "Your Diagnosis Report is Ready",
            "body": "Your AI-powered diagnostic assessment has been completed. Log in to view your results.",
        },
        "appointment_reminder": {
            "subject": "Upcoming Appointment Reminder",
            "body": "You have an upcoming appointment. Please review your diagnosis report beforehand.",
        },
        "critical_alert": {
            "subject": "Urgent: Critical Findings Detected",
            "body": "Critical findings have been detected in a recent diagnostic assessment. Immediate review required.",
        },
        "welcome": {
            "subject": "Welcome to AI Medical Diagnosis Assistant",
            "body": "Welcome! Your account has been set up successfully. Start your first consultation now.",
        },
        "weekly_summary": {
            "subject": "Your Weekly Health Summary",
            "body": "Here is your weekly summary of diagnostic activity and health insights.",
        },
    }

    SEVERITY_LEVELS = ["info", "warning", "critical", "error"]

    def __init__(self):
        self._notifications: list[dict] = []
        self._alerts: list[dict] = []
        self._preferences: dict[str, dict] = {}
        self._webhook_configs: list[dict] = []
        self._webhook_deliveries: list[dict] = []
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 100 notification records across email/SMS/push with 95% delivery rate."""
        now = datetime.now(timezone.utc)

        # Seed webhook configs
        self._webhook_configs = [
            {
                "id": "wh-001",
                "name": "EHR Sync Webhook",
                "url": "https://ehr.example.com/api/webhook",
                "events": ["diagnosis.completed", "patient.updated"],
                "active": True,
                "created_at": (now - timedelta(days=60)).isoformat(),
                "last_triggered": (now - timedelta(hours=3)).isoformat(),
                "success_rate": 98.5,
            },
            {
                "id": "wh-002",
                "name": "Billing Webhook",
                "url": "https://billing.example.com/hooks/medical-ai",
                "events": ["diagnosis.completed", "subscription.changed"],
                "active": True,
                "created_at": (now - timedelta(days=45)).isoformat(),
                "last_triggered": (now - timedelta(hours=1)).isoformat(),
                "success_rate": 99.2,
            },
            {
                "id": "wh-003",
                "name": "Analytics Pipeline",
                "url": "https://analytics.example.com/ingest",
                "events": ["diagnosis.completed", "agent.error"],
                "active": False,
                "created_at": (now - timedelta(days=30)).isoformat(),
                "last_triggered": (now - timedelta(days=5)).isoformat(),
                "success_rate": 95.0,
            },
        ]

        # Seed user preferences
        for i in range(1, 11):
            user_id = f"user-{i:03d}"
            self._preferences[user_id] = {
                "user_id": user_id,
                "email": random.choice([True, True, True, False]),
                "sms": random.choice([True, False]),
                "push": random.choice([True, True, False]),
                "quiet_hours": {"start": "22:00", "end": "07:00"},
                "frequency": random.choice(["immediate", "hourly_digest", "daily_digest"]),
            }

        # Seed 100 notification records — 95% delivered
        template_keys = list(self.TEMPLATES.keys())
        for i in range(100):
            days_ago = random.randint(0, 29)
            ts = now - timedelta(
                days=days_ago,
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
            channel = random.choice(self.CHANNELS)
            template_key = random.choice(template_keys)
            template = self.TEMPLATES[template_key]
            user_id = f"user-{random.randint(1, 20):03d}"

            # 95% delivery rate
            roll = random.random()
            if roll < 0.95:
                status = "delivered"
            elif roll < 0.98:
                status = "bounced"
            else:
                status = "failed"

            self._notifications.append({
                "id": f"notif-{uuid.uuid4().hex[:8]}",
                "user_id": user_id,
                "channel": channel,
                "template": template_key,
                "subject": template["subject"],
                "body": template["body"],
                "status": status,
                "sent_at": ts.isoformat(),
                "delivered_at": ts.isoformat() if status == "delivered" else None,
                "read_at": (ts + timedelta(minutes=random.randint(5, 120))).isoformat()
                if status == "delivered" and random.random() > 0.3
                else None,
            })

        # Seed system alerts
        alert_messages = [
            ("critical", "Agent pipeline timeout exceeded 30s threshold", "orchestrator"),
            ("warning", "SMS delivery rate dropped below 90%", "notification_agent"),
            ("info", "Daily backup completed successfully", "system"),
            ("error", "FHIR sync failed for patient record P-1042", "ehr_agent"),
            ("warning", "High memory usage detected on worker node 2", "system"),
            ("info", "Monthly report generated for October 2025", "analytics_agent"),
            ("critical", "Database connection pool exhausted", "system"),
            ("warning", "API rate limit approaching for Anthropic key", "orchestrator"),
        ]
        for i, (severity, message, source) in enumerate(alert_messages):
            ts = now - timedelta(hours=random.randint(1, 72))
            self._alerts.append({
                "id": f"alert-{uuid.uuid4().hex[:8]}",
                "severity": severity,
                "message": message,
                "source": source,
                "case_id": f"case-{random.randint(100, 999)}" if random.random() > 0.5 else None,
                "acknowledged": random.choice([True, False]),
                "created_at": ts.isoformat(),
            })

    def send_email(self, to: str, subject: str, body: str, template: str | None = None) -> dict:
        """Mock email send — returns delivery status."""
        notif_id = f"notif-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        status = "delivered" if random.random() < 0.95 else "failed"
        record = {
            "id": notif_id,
            "channel": "email",
            "to": to,
            "subject": subject,
            "body": body,
            "template": template,
            "status": status,
            "sent_at": now.isoformat(),
            "delivered_at": now.isoformat() if status == "delivered" else None,
        }
        self._notifications.append(record)
        return record

    def send_sms(self, to: str, message: str) -> dict:
        """Mock SMS send."""
        notif_id = f"notif-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        status = "delivered" if random.random() < 0.93 else "failed"
        record = {
            "id": notif_id,
            "channel": "sms",
            "to": to,
            "body": message,
            "status": status,
            "sent_at": now.isoformat(),
            "delivered_at": now.isoformat() if status == "delivered" else None,
        }
        self._notifications.append(record)
        return record

    def send_push(self, user_id: str, title: str, body: str, data: dict | None = None) -> dict:
        """Mock push notification."""
        notif_id = f"notif-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        status = "delivered" if random.random() < 0.97 else "failed"
        record = {
            "id": notif_id,
            "channel": "push",
            "user_id": user_id,
            "subject": title,
            "body": body,
            "data": data,
            "status": status,
            "sent_at": now.isoformat(),
            "delivered_at": now.isoformat() if status == "delivered" else None,
        }
        self._notifications.append(record)
        return record

    def create_alert(self, severity: str, message: str, source: str, case_id: str | None = None) -> dict:
        """Create a system alert."""
        alert = {
            "id": f"alert-{uuid.uuid4().hex[:8]}",
            "severity": severity if severity in self.SEVERITY_LEVELS else "info",
            "message": message,
            "source": source,
            "case_id": case_id,
            "acknowledged": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._alerts.append(alert)
        return alert

    def get_notification_history(
        self, user_id: str | None = None, type: str | None = None,
        page: int = 1, limit: int = 20,
    ) -> dict:
        """Paginated notification log with optional filters."""
        results = list(self._notifications)

        if user_id:
            results = [n for n in results if n.get("user_id") == user_id]
        if type:
            results = [n for n in results if n.get("channel") == type]

        results.sort(key=lambda x: x.get("sent_at", ""), reverse=True)
        total = len(results)
        start = (page - 1) * limit
        page_results = results[start : start + limit]

        return {
            "notifications": page_results,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": max(1, -(-total // limit)),
        }

    def get_notification_metrics(self) -> dict:
        """Sent/delivered/failed counts by channel, response rates."""
        by_channel: dict[str, dict] = {}
        for ch in self.CHANNELS:
            channel_notifs = [n for n in self._notifications if n.get("channel") == ch]
            total = len(channel_notifs)
            delivered = sum(1 for n in channel_notifs if n.get("status") == "delivered")
            failed = sum(1 for n in channel_notifs if n.get("status") == "failed")
            bounced = sum(1 for n in channel_notifs if n.get("status") == "bounced")
            read = sum(1 for n in channel_notifs if n.get("read_at"))
            by_channel[ch] = {
                "total": total,
                "delivered": delivered,
                "failed": failed,
                "bounced": bounced,
                "delivery_rate": round((delivered / total) * 100, 1) if total else 0,
                "read_rate": round((read / delivered) * 100, 1) if delivered else 0,
            }

        total_all = len(self._notifications)
        delivered_all = sum(1 for n in self._notifications if n.get("status") == "delivered")

        return {
            "total_sent": total_all,
            "total_delivered": delivered_all,
            "total_failed": total_all - delivered_all,
            "overall_delivery_rate": round((delivered_all / total_all) * 100, 1) if total_all else 0,
            "by_channel": by_channel,
            "active_alerts": len([a for a in self._alerts if not a.get("acknowledged")]),
            "templates_available": len(self.TEMPLATES),
        }

    def configure_preferences(self, user_id: str, preferences: dict) -> dict:
        """Set notification preferences per user."""
        existing = self._preferences.get(user_id, {"user_id": user_id})
        existing.update(preferences)
        existing["user_id"] = user_id
        self._preferences[user_id] = existing
        return {"status": "updated", "preferences": existing}

    def trigger_webhook(self, url: str, payload: dict) -> dict:
        """Mock webhook delivery."""
        delivery_id = f"whd-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        success = random.random() < 0.97
        record = {
            "id": delivery_id,
            "url": url,
            "payload": payload,
            "status": "delivered" if success else "failed",
            "status_code": 200 if success else random.choice([500, 502, 503]),
            "response_time_ms": random.randint(50, 500),
            "triggered_at": now.isoformat(),
        }
        self._webhook_deliveries.append(record)
        return record

    def get_webhook_configs(self) -> list:
        """List configured webhooks."""
        return self._webhook_configs


# Singleton
_notification_agent = None


def get_notification_agent() -> NotificationAgent:
    global _notification_agent
    if _notification_agent is None:
        _notification_agent = NotificationAgent()
    return _notification_agent
