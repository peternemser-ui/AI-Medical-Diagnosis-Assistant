"""Multi-Tenant Agent — manages clinics/organizations, roles, and cross-tenant analytics."""

import random
import uuid
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from enum import Enum


class TenantRole(str, Enum):
    ADMIN = "admin"
    PHYSICIAN = "physician"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    PATIENT = "patient"
    BILLING = "billing"


TENANT_TYPES = ["hospital", "clinic", "telehealth", "rural_health", "academic"]


class MultiTenantAgent:
    """Manages clinics/organizations, user roles, and cross-tenant analytics."""

    def __init__(self):
        self._tenants: dict[str, dict] = {}
        self._users: dict[str, list[dict]] = {}  # tenant_id -> list of users
        self._usage: dict[str, dict] = {}  # tenant_id -> usage stats
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 5 clinics with user counts, usage data, and revenue."""
        now = datetime.now(timezone.utc)

        clinics = [
            {
                "id": "tenant-001",
                "name": "City General Hospital",
                "type": "hospital",
                "admin_email": "admin@citygeneral.example.com",
                "status": "active",
                "plan": "enterprise",
                "user_count": 85,
                "monthly_revenue": 4990,
                "created_at": (now - timedelta(days=365)).isoformat(),
            },
            {
                "id": "tenant-002",
                "name": "Westside Family Practice",
                "type": "clinic",
                "admin_email": "dr.chen@westsidepractice.example.com",
                "status": "active",
                "plan": "pro",
                "user_count": 12,
                "monthly_revenue": 990,
                "created_at": (now - timedelta(days=210)).isoformat(),
            },
            {
                "id": "tenant-003",
                "name": "MedCenter Telehealth",
                "type": "telehealth",
                "admin_email": "ops@medcentertele.example.com",
                "status": "active",
                "plan": "enterprise",
                "user_count": 45,
                "monthly_revenue": 4990,
                "created_at": (now - timedelta(days=180)).isoformat(),
            },
            {
                "id": "tenant-004",
                "name": "Rural Health Clinic",
                "type": "rural_health",
                "admin_email": "nurse.johnson@ruralhealth.example.com",
                "status": "active",
                "plan": "starter",
                "user_count": 6,
                "monthly_revenue": 290,
                "created_at": (now - timedelta(days=120)).isoformat(),
            },
            {
                "id": "tenant-005",
                "name": "University Medical Center",
                "type": "academic",
                "admin_email": "it@universitymed.example.com",
                "status": "trial",
                "plan": "enterprise",
                "user_count": 120,
                "monthly_revenue": 0,
                "created_at": (now - timedelta(days=14)).isoformat(),
            },
        ]

        role_distribution = {
            "hospital": {"admin": 2, "physician": 20, "nurse": 35, "receptionist": 5, "patient": 20, "billing": 3},
            "clinic": {"admin": 1, "physician": 3, "nurse": 4, "receptionist": 1, "patient": 2, "billing": 1},
            "telehealth": {"admin": 2, "physician": 15, "nurse": 10, "receptionist": 3, "patient": 12, "billing": 3},
            "rural_health": {"admin": 1, "physician": 1, "nurse": 2, "receptionist": 1, "patient": 1, "billing": 0},
            "academic": {"admin": 3, "physician": 30, "nurse": 40, "receptionist": 7, "patient": 35, "billing": 5},
        }

        for clinic in clinics:
            tenant_id = clinic["id"]
            self._tenants[tenant_id] = {
                "id": tenant_id,
                "name": clinic["name"],
                "type": clinic["type"],
                "admin_email": clinic["admin_email"],
                "status": clinic["status"],
                "plan": clinic["plan"],
                "created_at": clinic["created_at"],
                "settings": {
                    "branding": {
                        "primary_color": random.choice(["#2563EB", "#059669", "#7C3AED", "#DC2626", "#0891B2"]),
                        "logo_url": f"/logos/{tenant_id}.png",
                        "display_name": clinic["name"],
                    },
                    "features": {
                        "voice_input": True,
                        "pdf_reports": clinic["plan"] != "starter",
                        "api_access": clinic["plan"] == "enterprise",
                        "custom_agents": clinic["plan"] == "enterprise",
                    },
                    "security": {
                        "mfa_required": clinic["plan"] == "enterprise",
                        "session_timeout_minutes": 30,
                        "ip_whitelist": [],
                    },
                },
            }

            # Seed users for this tenant
            roles = role_distribution.get(clinic["type"], role_distribution["clinic"])
            users = []
            user_counter = 0
            for role, count in roles.items():
                for j in range(count):
                    user_counter += 1
                    users.append({
                        "id": f"{tenant_id}-user-{user_counter:03d}",
                        "tenant_id": tenant_id,
                        "role": role,
                        "email": f"{role}{j+1}@{clinic['name'].lower().replace(' ', '')}.example.com",
                        "status": "active" if random.random() > 0.1 else "inactive",
                        "last_active": (now - timedelta(hours=random.randint(0, 168))).isoformat(),
                        "created_at": clinic["created_at"],
                    })
            self._users[tenant_id] = users

            # Seed usage data
            diagnoses_30d = random.randint(20, 500) if clinic["status"] == "active" else random.randint(5, 30)
            self._usage[tenant_id] = {
                "tenant_id": tenant_id,
                "diagnoses_total": diagnoses_30d * random.randint(3, 12),
                "diagnoses_30d": diagnoses_30d,
                "diagnoses_7d": diagnoses_30d // 4,
                "diagnoses_today": random.randint(0, diagnoses_30d // 10),
                "api_calls_30d": diagnoses_30d * random.randint(3, 7),
                "avg_response_time_ms": random.randint(800, 3500),
                "storage_used_mb": random.randint(50, 2000),
                "monthly_revenue": clinic["monthly_revenue"],
                "active_users": sum(1 for u in users if u["status"] == "active"),
            }

    def create_tenant(self, name: str, type: str, admin_email: str) -> dict:
        """Create a new clinic/organization."""
        tenant_id = f"tenant-{uuid.uuid4().hex[:6]}"
        now = datetime.now(timezone.utc)
        tenant = {
            "id": tenant_id,
            "name": name,
            "type": type if type in TENANT_TYPES else "clinic",
            "admin_email": admin_email,
            "status": "active",
            "plan": "starter",
            "created_at": now.isoformat(),
            "settings": {
                "branding": {
                    "primary_color": "#2563EB",
                    "logo_url": f"/logos/{tenant_id}.png",
                    "display_name": name,
                },
                "features": {
                    "voice_input": True,
                    "pdf_reports": False,
                    "api_access": False,
                    "custom_agents": False,
                },
                "security": {
                    "mfa_required": False,
                    "session_timeout_minutes": 30,
                    "ip_whitelist": [],
                },
            },
        }
        self._tenants[tenant_id] = tenant
        self._users[tenant_id] = [{
            "id": f"{tenant_id}-user-001",
            "tenant_id": tenant_id,
            "role": "admin",
            "email": admin_email,
            "status": "active",
            "last_active": now.isoformat(),
            "created_at": now.isoformat(),
        }]
        self._usage[tenant_id] = {
            "tenant_id": tenant_id,
            "diagnoses_total": 0,
            "diagnoses_30d": 0,
            "diagnoses_7d": 0,
            "diagnoses_today": 0,
            "api_calls_30d": 0,
            "avg_response_time_ms": 0,
            "storage_used_mb": 0,
            "monthly_revenue": 0,
            "active_users": 1,
        }
        return {"status": "created", "tenant": tenant}

    def get_tenant(self, tenant_id: str) -> dict | None:
        """Return tenant details with user and usage summaries."""
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return None
        users = self._users.get(tenant_id, [])
        usage = self._usage.get(tenant_id, {})

        # Role breakdown
        role_counts = defaultdict(int)
        for u in users:
            role_counts[u["role"]] += 1

        return {
            **tenant,
            "user_count": len(users),
            "role_breakdown": dict(role_counts),
            "usage": usage,
        }

    def list_tenants(self, status: str | None = None) -> list:
        """Return all tenants, optionally filtered by status."""
        tenants = []
        for tid, t in self._tenants.items():
            if status and t.get("status") != status:
                continue
            usage = self._usage.get(tid, {})
            tenants.append({
                **t,
                "user_count": len(self._users.get(tid, [])),
                "diagnoses_30d": usage.get("diagnoses_30d", 0),
                "monthly_revenue": usage.get("monthly_revenue", 0),
            })
        return tenants

    def update_tenant_settings(self, tenant_id: str, settings: dict) -> dict | None:
        """Update branding, config, or feature flags for a tenant."""
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return None
        # Deep merge settings
        for key, value in settings.items():
            if key in tenant["settings"] and isinstance(value, dict):
                tenant["settings"][key].update(value)
            else:
                tenant["settings"][key] = value
        return {"status": "updated", "tenant": tenant}

    def get_tenant_usage(self, tenant_id: str) -> dict | None:
        """Usage stats for a specific tenant."""
        if tenant_id not in self._tenants:
            return None
        return self._usage.get(tenant_id)

    def get_cross_tenant_analytics(self) -> dict:
        """Aggregated metrics across all tenants."""
        total_diagnoses = 0
        total_revenue = 0
        total_users = 0
        tenants_by_plan = defaultdict(int)
        tenants_by_type = defaultdict(int)
        tenants_by_status = defaultdict(int)

        for tid, tenant in self._tenants.items():
            usage = self._usage.get(tid, {})
            total_diagnoses += usage.get("diagnoses_30d", 0)
            total_revenue += usage.get("monthly_revenue", 0)
            total_users += len(self._users.get(tid, []))
            tenants_by_plan[tenant.get("plan", "unknown")] += 1
            tenants_by_type[tenant.get("type", "unknown")] += 1
            tenants_by_status[tenant.get("status", "unknown")] += 1

        # Top tenants by usage
        tenant_usage_list = []
        for tid, tenant in self._tenants.items():
            usage = self._usage.get(tid, {})
            tenant_usage_list.append({
                "tenant_id": tid,
                "name": tenant["name"],
                "diagnoses_30d": usage.get("diagnoses_30d", 0),
                "monthly_revenue": usage.get("monthly_revenue", 0),
            })
        tenant_usage_list.sort(key=lambda x: x["diagnoses_30d"], reverse=True)

        return {
            "total_tenants": len(self._tenants),
            "total_users": total_users,
            "total_diagnoses_30d": total_diagnoses,
            "total_monthly_revenue": total_revenue,
            "tenants_by_plan": dict(tenants_by_plan),
            "tenants_by_type": dict(tenants_by_type),
            "tenants_by_status": dict(tenants_by_status),
            "top_tenants_by_usage": tenant_usage_list[:5],
            "avg_users_per_tenant": round(total_users / max(len(self._tenants), 1), 1),
            "avg_revenue_per_tenant": round(total_revenue / max(len(self._tenants), 1), 2),
        }

    def manage_roles(self, tenant_id: str, user_id: str, role: str) -> dict | None:
        """Assign a role to a user within a tenant."""
        if role not in [r.value for r in TenantRole]:
            return {"error": f"Invalid role '{role}'. Valid roles: {[r.value for r in TenantRole]}"}
        users = self._users.get(tenant_id)
        if users is None:
            return None
        for user in users:
            if user["id"] == user_id:
                old_role = user["role"]
                user["role"] = role
                return {"status": "updated", "user_id": user_id, "old_role": old_role, "new_role": role}
        return {"error": f"User '{user_id}' not found in tenant '{tenant_id}'"}

    def get_tenant_metrics(self) -> dict:
        """Total tenants, active tenants, users per tenant, revenue per tenant."""
        active = sum(1 for t in self._tenants.values() if t.get("status") == "active")
        trial = sum(1 for t in self._tenants.values() if t.get("status") == "trial")
        total_users = sum(len(u) for u in self._users.values())
        total_revenue = sum(u.get("monthly_revenue", 0) for u in self._usage.values())

        per_tenant = []
        for tid, tenant in self._tenants.items():
            usage = self._usage.get(tid, {})
            per_tenant.append({
                "tenant_id": tid,
                "name": tenant["name"],
                "plan": tenant.get("plan"),
                "status": tenant.get("status"),
                "user_count": len(self._users.get(tid, [])),
                "diagnoses_30d": usage.get("diagnoses_30d", 0),
                "monthly_revenue": usage.get("monthly_revenue", 0),
                "avg_response_time_ms": usage.get("avg_response_time_ms", 0),
            })

        return {
            "total_tenants": len(self._tenants),
            "active_tenants": active,
            "trial_tenants": trial,
            "total_users": total_users,
            "total_monthly_revenue": total_revenue,
            "avg_users_per_tenant": round(total_users / max(len(self._tenants), 1), 1),
            "avg_revenue_per_tenant": round(total_revenue / max(len(self._tenants), 1), 2),
            "tenants": per_tenant,
        }


# Singleton
_tenant_agent = None


def get_tenant_agent() -> MultiTenantAgent:
    global _tenant_agent
    if _tenant_agent is None:
        _tenant_agent = MultiTenantAgent()
    return _tenant_agent
