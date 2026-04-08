"""Patient Follow-Up Agent — scheduling, symptom tracking, and trend detection."""

import random
import uuid
from datetime import datetime, timezone, timedelta


class PatientFollowUpAgent:
    """Manages patient follow-ups, symptom progression, and visit comparisons."""

    def __init__(self):
        self._patients: dict[str, dict] = {}
        self._followups: list[dict] = []
        self._visits: list[dict] = []
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed 12 patients with follow-ups, visits, and trends."""
        now = datetime.now(timezone.utc)

        patient_data = [
            ("P-1001", "John D.", 58, "M", "Hypertension, Chest Pain"),
            ("P-1002", "Sarah M.", 34, "F", "Migraine with Aura"),
            ("P-1003", "Robert K.", 72, "M", "Type 2 Diabetes, Neuropathy"),
            ("P-1004", "Emily R.", 45, "F", "Rheumatoid Arthritis"),
            ("P-1005", "Michael T.", 29, "M", "Anxiety Disorder"),
            ("P-1006", "Linda W.", 61, "F", "COPD, Chronic Cough"),
            ("P-1007", "James H.", 55, "M", "Lower Back Pain"),
            ("P-1008", "Maria G.", 40, "F", "Hypothyroidism"),
            ("P-1009", "David L.", 67, "M", "Atrial Fibrillation"),
            ("P-1010", "Susan B.", 38, "F", "Iron Deficiency Anemia"),
            ("P-1011", "Thomas P.", 50, "M", "GERD, Abdominal Pain"),
            ("P-1012", "Jennifer C.", 43, "F", "Asthma, Allergic Rhinitis"),
        ]

        symptom_sets = {
            "P-1001": [
                {"date_offset": -60, "symptoms": ["chest tightness", "shortness of breath", "elevated BP 155/95"], "severity": 7},
                {"date_offset": -30, "symptoms": ["occasional chest discomfort", "BP 145/90"], "severity": 5},
                {"date_offset": -5, "symptoms": ["rare chest discomfort", "BP 138/85", "improved exercise tolerance"], "severity": 3},
            ],
            "P-1003": [
                {"date_offset": -90, "symptoms": ["numbness in feet", "HbA1c 8.2", "fatigue"], "severity": 6},
                {"date_offset": -45, "symptoms": ["worsening numbness", "HbA1c 8.5", "blurred vision"], "severity": 8},
                {"date_offset": -10, "symptoms": ["numbness spreading to calves", "HbA1c 8.9", "persistent blurred vision"], "severity": 9},
            ],
            "P-1006": [
                {"date_offset": -45, "symptoms": ["productive cough", "wheezing", "FEV1 62%"], "severity": 6},
                {"date_offset": -15, "symptoms": ["worsening cough", "increased sputum", "FEV1 55%", "nocturnal dyspnea"], "severity": 8},
            ],
        }

        for pid, name, age, gender, conditions in patient_data:
            self._patients[pid] = {
                "patient_id": pid,
                "name": name,
                "age": age,
                "gender": gender,
                "conditions": conditions,
                "first_visit": (now - timedelta(days=random.randint(60, 365))).isoformat(),
                "last_visit": (now - timedelta(days=random.randint(1, 30))).isoformat(),
                "total_visits": random.randint(2, 8),
            }

            # Create visits
            num_visits = random.randint(2, 5)
            patient_symptoms = symptom_sets.get(pid, [])

            if patient_symptoms:
                for vs in patient_symptoms:
                    visit_date = now + timedelta(days=vs["date_offset"])
                    visit_id = f"V-{uuid.uuid4().hex[:6]}"
                    self._visits.append({
                        "visit_id": visit_id,
                        "patient_id": pid,
                        "date": visit_date.isoformat(),
                        "symptoms": vs["symptoms"],
                        "severity": vs["severity"],
                        "diagnosis": conditions.split(",")[0].strip(),
                        "notes": f"Follow-up visit for {conditions}",
                    })
            else:
                for j in range(num_visits):
                    visit_date = now - timedelta(days=random.randint(5, 120))
                    visit_id = f"V-{uuid.uuid4().hex[:6]}"
                    severity = random.randint(2, 8)
                    self._visits.append({
                        "visit_id": visit_id,
                        "patient_id": pid,
                        "date": visit_date.isoformat(),
                        "symptoms": [f"symptom_{k}" for k in range(random.randint(1, 4))],
                        "severity": severity,
                        "diagnosis": conditions.split(",")[0].strip(),
                        "notes": f"Routine follow-up for {conditions}",
                    })

        # Create follow-ups: 3 overdue, rest upcoming or completed
        statuses = ["overdue"] * 3 + ["upcoming"] * 5 + ["completed"] * 4
        random.shuffle(statuses)

        for i, (pid, name, age, gender, conditions) in enumerate(patient_data):
            status = statuses[i]
            if status == "overdue":
                due_date = now - timedelta(days=random.randint(3, 21))
            elif status == "upcoming":
                due_date = now + timedelta(days=random.randint(1, 30))
            else:
                due_date = now - timedelta(days=random.randint(1, 14))

            self._followups.append({
                "id": f"fu-{uuid.uuid4().hex[:8]}",
                "patient_id": pid,
                "patient_name": name,
                "diagnosis": conditions.split(",")[0].strip(),
                "reason": f"Follow-up assessment for {conditions}",
                "scheduled_date": due_date.isoformat(),
                "status": status,
                "priority": "high" if status == "overdue" else "normal",
                "created_at": (due_date - timedelta(days=14)).isoformat(),
                "notes": f"{'OVERDUE - Contact patient immediately' if status == 'overdue' else 'Regular follow-up'}",
            })

    def schedule_followup(self, patient_id: str, diagnosis: str, timeframe: str = "2 weeks") -> dict:
        """Create a follow-up reminder."""
        now = datetime.now(timezone.utc)
        days_map = {
            "1 week": 7, "2 weeks": 14, "1 month": 30,
            "3 months": 90, "6 months": 180,
        }
        days = days_map.get(timeframe, 14)
        due_date = now + timedelta(days=days)

        patient = self._patients.get(patient_id, {"patient_id": patient_id, "name": "Unknown"})

        followup = {
            "id": f"fu-{uuid.uuid4().hex[:8]}",
            "patient_id": patient_id,
            "patient_name": patient.get("name", "Unknown"),
            "diagnosis": diagnosis,
            "reason": f"Scheduled follow-up for {diagnosis}",
            "scheduled_date": due_date.isoformat(),
            "status": "upcoming",
            "priority": "normal",
            "created_at": now.isoformat(),
            "notes": f"Follow-up in {timeframe}",
        }
        self._followups.append(followup)

        return {"status": "scheduled", "followup": followup}

    def get_patient_timeline(self, patient_id: str) -> dict:
        """Return chronological list of visits, diagnoses, and follow-ups."""
        patient = self._patients.get(patient_id)
        if not patient:
            return {"error": f"Patient {patient_id} not found", "events": []}

        events = []

        # Add visits
        patient_visits = sorted(
            [v for v in self._visits if v["patient_id"] == patient_id],
            key=lambda x: x["date"],
        )
        for v in patient_visits:
            events.append({
                "type": "visit",
                "date": v["date"],
                "visit_id": v["visit_id"],
                "summary": f"Visit: {v['diagnosis']} (severity {v['severity']}/10)",
                "details": v,
            })

        # Add follow-ups
        patient_fus = [f for f in self._followups if f["patient_id"] == patient_id]
        for fu in patient_fus:
            events.append({
                "type": "followup",
                "date": fu["scheduled_date"],
                "followup_id": fu["id"],
                "summary": f"Follow-up: {fu['diagnosis']} ({fu['status']})",
                "details": fu,
            })

        events.sort(key=lambda x: x["date"])

        return {
            "patient": patient,
            "events": events,
            "total_events": len(events),
        }

    def check_symptom_progression(self, patient_id: str) -> dict:
        """Compare current vs previous symptoms and detect trends."""
        patient_visits = sorted(
            [v for v in self._visits if v["patient_id"] == patient_id],
            key=lambda x: x["date"],
        )

        if len(patient_visits) < 2:
            return {
                "patient_id": patient_id,
                "trend": "insufficient_data",
                "message": "Need at least 2 visits to detect trends",
                "visits_analyzed": len(patient_visits),
            }

        latest = patient_visits[-1]
        previous = patient_visits[-2]

        severity_change = latest["severity"] - previous["severity"]
        if severity_change > 2:
            trend = "worsening"
        elif severity_change < -2:
            trend = "improving"
        else:
            trend = "stable"

        new_symptoms = [s for s in latest["symptoms"] if s not in previous["symptoms"]]
        resolved_symptoms = [s for s in previous["symptoms"] if s not in latest["symptoms"]]

        return {
            "patient_id": patient_id,
            "trend": trend,
            "severity_change": severity_change,
            "current_severity": latest["severity"],
            "previous_severity": previous["severity"],
            "current_visit": latest,
            "previous_visit": previous,
            "new_symptoms": new_symptoms,
            "resolved_symptoms": resolved_symptoms,
            "visits_analyzed": len(patient_visits),
            "recommendation": {
                "worsening": "Consider escalation. Schedule urgent follow-up within 48 hours.",
                "stable": "Continue current treatment plan. Follow up as scheduled.",
                "improving": "Treatment appears effective. Consider extending follow-up interval.",
            }.get(trend, "Continue monitoring."),
        }

    def get_pending_followups(self) -> dict:
        """Return all overdue and upcoming follow-ups."""
        overdue = [f for f in self._followups if f["status"] == "overdue"]
        upcoming = [f for f in self._followups if f["status"] == "upcoming"]

        overdue.sort(key=lambda x: x["scheduled_date"])
        upcoming.sort(key=lambda x: x["scheduled_date"])

        return {
            "overdue": overdue,
            "upcoming": upcoming,
            "overdue_count": len(overdue),
            "upcoming_count": len(upcoming),
            "total_pending": len(overdue) + len(upcoming),
        }

    def generate_comparison_report(self, patient_id: str, visit1_id: str, visit2_id: str) -> dict:
        """Generate a side-by-side comparison between two visits."""
        visit1 = next((v for v in self._visits if v["visit_id"] == visit1_id and v["patient_id"] == patient_id), None)
        visit2 = next((v for v in self._visits if v["visit_id"] == visit2_id and v["patient_id"] == patient_id), None)

        if not visit1 or not visit2:
            return {"error": "One or both visits not found"}

        severity_change = visit2["severity"] - visit1["severity"]
        return {
            "patient_id": patient_id,
            "visit_1": visit1,
            "visit_2": visit2,
            "comparison": {
                "severity_change": severity_change,
                "trend": "worsening" if severity_change > 0 else "improving" if severity_change < 0 else "stable",
                "new_symptoms": [s for s in visit2["symptoms"] if s not in visit1["symptoms"]],
                "resolved_symptoms": [s for s in visit1["symptoms"] if s not in visit2["symptoms"]],
                "persistent_symptoms": [s for s in visit1["symptoms"] if s in visit2["symptoms"]],
                "days_between": abs((
                    datetime.fromisoformat(visit2["date"].replace("Z", "+00:00")) -
                    datetime.fromisoformat(visit1["date"].replace("Z", "+00:00"))
                ).days),
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def detect_worsening_trends(self) -> dict:
        """Scan all patients for concerning progressions."""
        worsening = []
        for pid in self._patients:
            progression = self.check_symptom_progression(pid)
            if progression.get("trend") == "worsening":
                worsening.append({
                    "patient_id": pid,
                    "patient_name": self._patients[pid].get("name", "Unknown"),
                    "conditions": self._patients[pid].get("conditions", ""),
                    "severity_change": progression["severity_change"],
                    "current_severity": progression["current_severity"],
                    "recommendation": progression["recommendation"],
                })

        return {
            "total_patients_scanned": len(self._patients),
            "worsening_detected": len(worsening),
            "patients": worsening,
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "alert_level": "critical" if len(worsening) > 3 else "warning" if len(worsening) > 0 else "normal",
        }

    def get_followup_metrics(self) -> dict:
        """Return compliance rate, overdue count, and avg time between visits."""
        total = len(self._followups)
        completed = sum(1 for f in self._followups if f["status"] == "completed")
        overdue = sum(1 for f in self._followups if f["status"] == "overdue")

        compliance_rate = round((completed / max(total, 1)) * 100, 1)

        # Calculate average time between visits per patient
        visit_gaps = []
        for pid in self._patients:
            patient_visits = sorted(
                [v for v in self._visits if v["patient_id"] == pid],
                key=lambda x: x["date"],
            )
            for i in range(1, len(patient_visits)):
                d1 = datetime.fromisoformat(patient_visits[i - 1]["date"].replace("Z", "+00:00"))
                d2 = datetime.fromisoformat(patient_visits[i]["date"].replace("Z", "+00:00"))
                visit_gaps.append(abs((d2 - d1).days))

        avg_gap = round(sum(visit_gaps) / max(len(visit_gaps), 1), 1)

        return {
            "total_followups": total,
            "completed": completed,
            "overdue": overdue,
            "upcoming": total - completed - overdue,
            "compliance_rate": compliance_rate,
            "avg_days_between_visits": avg_gap,
            "total_patients_tracked": len(self._patients),
            "patients_with_worsening_trends": self.detect_worsening_trends()["worsening_detected"],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }


# Singleton
_followup_agent = None


def get_followup_agent() -> PatientFollowUpAgent:
    global _followup_agent
    if _followup_agent is None:
        _followup_agent = PatientFollowUpAgent()
    return _followup_agent
