"""Appointment Booking Agent — suggests appointment types, finds slots, books appointments, and manages providers."""

import random
import uuid
from datetime import datetime, timezone, timedelta


# Mock provider database: specialty -> list of providers
PROVIDER_DB = {
    "cardiology": [
        {"provider_id": "CARD-001", "name": "Dr. Sarah Chen", "npi": "1234567001", "facility": "HeartCare Specialists", "location": "New York, NY", "accepting_new": True, "rating": 4.9, "telehealth": True},
        {"provider_id": "CARD-002", "name": "Dr. James Okafor", "npi": "1234567002", "facility": "Metro Cardiology Group", "location": "New York, NY", "accepting_new": True, "rating": 4.7, "telehealth": True},
        {"provider_id": "CARD-003", "name": "Dr. Maria Rodriguez", "npi": "1234567003", "facility": "University Heart Center", "location": "Chicago, IL", "accepting_new": False, "rating": 4.8, "telehealth": False},
        {"provider_id": "CARD-004", "name": "Dr. David Kim", "npi": "1234567004", "facility": "Pacific Cardiology", "location": "Los Angeles, CA", "accepting_new": True, "rating": 4.6, "telehealth": True},
    ],
    "dermatology": [
        {"provider_id": "DERM-001", "name": "Dr. Emily Nguyen", "npi": "1234567011", "facility": "ClearSkin Dermatology", "location": "New York, NY", "accepting_new": True, "rating": 4.8, "telehealth": True},
        {"provider_id": "DERM-002", "name": "Dr. Robert Walsh", "npi": "1234567012", "facility": "Metro Derm Associates", "location": "Boston, MA", "accepting_new": True, "rating": 4.5, "telehealth": True},
        {"provider_id": "DERM-003", "name": "Dr. Aisha Patel", "npi": "1234567013", "facility": "SkinHealth Clinic", "location": "Chicago, IL", "accepting_new": True, "rating": 4.9, "telehealth": False},
    ],
    "neurology": [
        {"provider_id": "NEUR-001", "name": "Dr. Michael Torres", "npi": "1234567021", "facility": "BrainHealth Neurology", "location": "Houston, TX", "accepting_new": True, "rating": 4.7, "telehealth": True},
        {"provider_id": "NEUR-002", "name": "Dr. Lisa Yamamoto", "npi": "1234567022", "facility": "NeuroScience Institute", "location": "San Francisco, CA", "accepting_new": True, "rating": 4.9, "telehealth": True},
        {"provider_id": "NEUR-003", "name": "Dr. Ahmed Hassan", "npi": "1234567023", "facility": "Central Neurology Group", "location": "New York, NY", "accepting_new": False, "rating": 4.6, "telehealth": False},
    ],
    "orthopedics": [
        {"provider_id": "ORTH-001", "name": "Dr. Jennifer Martinez", "npi": "1234567031", "facility": "BoneJoint Orthopedics", "location": "Denver, CO", "accepting_new": True, "rating": 4.8, "telehealth": False},
        {"provider_id": "ORTH-002", "name": "Dr. William Chang", "npi": "1234567032", "facility": "SportsMed Orthopedic Center", "location": "Los Angeles, CA", "accepting_new": True, "rating": 4.7, "telehealth": True},
        {"provider_id": "ORTH-003", "name": "Dr. Rachel Green", "npi": "1234567033", "facility": "Metro Orthopedic Surgeons", "location": "New York, NY", "accepting_new": True, "rating": 4.5, "telehealth": False},
    ],
    "psychiatry": [
        {"provider_id": "PSYC-001", "name": "Dr. Laura Bennett", "npi": "1234567041", "facility": "MindWell Psychiatry", "location": "New York, NY", "accepting_new": True, "rating": 4.9, "telehealth": True},
        {"provider_id": "PSYC-002", "name": "Dr. Kevin Osei", "npi": "1234567042", "facility": "Serenity Mental Health", "location": "Atlanta, GA", "accepting_new": True, "rating": 4.8, "telehealth": True},
        {"provider_id": "PSYC-003", "name": "Dr. Hannah Zhou", "npi": "1234567043", "facility": "BehavioralHealth Associates", "location": "Seattle, WA", "accepting_new": True, "rating": 4.7, "telehealth": True},
        {"provider_id": "PSYC-004", "name": "Dr. Carlos Mendez", "npi": "1234567044", "facility": "University Psychiatry Clinic", "location": "Chicago, IL", "accepting_new": False, "rating": 4.6, "telehealth": True},
    ],
}

# Appointment type mapping
APPOINTMENT_TYPES = {
    "emergency": {"label": "Emergency Room", "response_time": "Immediate", "setting": "Hospital ER", "icon": "alert-triangle"},
    "urgent_care": {"label": "Urgent Care Visit", "response_time": "Same day", "setting": "Urgent care clinic", "icon": "clock"},
    "specialist": {"label": "Specialist Consultation", "response_time": "1-4 weeks", "setting": "Specialist office", "icon": "user-md"},
    "primary_care": {"label": "Primary Care Visit", "response_time": "1-7 days", "setting": "Primary care office", "icon": "stethoscope"},
    "telehealth": {"label": "Telehealth Visit", "response_time": "1-3 days", "setting": "Video/phone call", "icon": "video"},
    "follow_up": {"label": "Follow-Up Appointment", "response_time": "2-4 weeks", "setting": "Provider office", "icon": "calendar-check"},
}

# Diagnosis -> recommended specialty mapping
DIAGNOSIS_SPECIALTY_MAP = {
    "chest pain": "cardiology",
    "heart palpitations": "cardiology",
    "hypertension": "cardiology",
    "atrial fibrillation": "cardiology",
    "heart failure": "cardiology",
    "skin rash": "dermatology",
    "acne": "dermatology",
    "eczema": "dermatology",
    "psoriasis": "dermatology",
    "headache": "neurology",
    "migraine": "neurology",
    "seizure": "neurology",
    "neuropathy": "neurology",
    "stroke": "neurology",
    "back pain": "orthopedics",
    "joint pain": "orthopedics",
    "fracture": "orthopedics",
    "arthritis": "orthopedics",
    "depression": "psychiatry",
    "anxiety": "psychiatry",
    "bipolar disorder": "psychiatry",
    "ptsd": "psychiatry",
    "insomnia": "psychiatry",
}

# Telehealth suitability
TELEHEALTH_SUITABLE = {
    "depression", "anxiety", "insomnia", "follow-up", "medication review",
    "hypertension", "type 2 diabetes", "allergic rhinitis", "eczema",
    "migraine", "gerd", "hypothyroidism", "asthma",
}

INPERSON_REQUIRED = {
    "chest pain", "fracture", "severe abdominal pain", "stroke",
    "seizure", "heart attack", "deep vein thrombosis", "pulmonary embolism",
    "skin biopsy", "joint injection",
}


class AppointmentBookingAgent:
    """Suggests appointment types, finds available slots, books appointments, and manages providers."""

    def __init__(self):
        self._bookings: list[dict] = []
        self._seed_bookings()

    def _seed_bookings(self):
        """Seed some mock booking history."""
        now = datetime.now(timezone.utc)
        specialties = list(PROVIDER_DB.keys())
        statuses = ["completed", "completed", "completed", "no_show", "cancelled", "upcoming"]

        for i in range(30):
            spec = random.choice(specialties)
            providers = PROVIDER_DB[spec]
            provider = random.choice(providers)
            days_offset = random.randint(-30, 14)
            appt_time = now + timedelta(days=days_offset, hours=random.randint(8, 17))
            status = "upcoming" if days_offset > 0 else random.choice(statuses)

            self._bookings.append({
                "booking_id": f"BK-{uuid.uuid4().hex[:8].upper()}",
                "patient_id": f"PAT-{random.randint(100, 999)}",
                "provider_id": provider["provider_id"],
                "provider_name": provider["name"],
                "specialty": spec,
                "appointment_type": random.choice(["specialist", "telehealth", "follow_up"]),
                "scheduled_at": appt_time.isoformat(),
                "status": status,
                "location": provider["location"],
            })

    def suggest_appointment_type(self, diagnosis: str, urgency: str) -> dict:
        """Recommend an appointment type based on diagnosis and urgency."""
        diag_key = diagnosis.strip().lower()
        urgency_key = urgency.strip().lower()

        # Determine appointment type based on urgency
        if urgency_key == "critical" or urgency_key == "emergency":
            appt_type = "emergency"
        elif urgency_key == "high":
            appt_type = "urgent_care"
        elif diag_key in TELEHEALTH_SUITABLE:
            appt_type = "telehealth"
        elif diag_key in DIAGNOSIS_SPECIALTY_MAP:
            appt_type = "specialist"
        else:
            appt_type = "primary_care"

        type_info = APPOINTMENT_TYPES[appt_type]

        # Determine specialty
        specialty = DIAGNOSIS_SPECIALTY_MAP.get(diag_key, "internal medicine")

        return {
            "diagnosis": diagnosis,
            "urgency": urgency,
            "recommended_type": appt_type,
            "type_info": type_info,
            "recommended_specialty": specialty,
            "reasoning": self._get_reasoning(diagnosis, urgency_key, appt_type),
            "alternative_types": self._get_alternatives(appt_type),
        }

    def find_available_slots(self, specialty: str, location: str | None = None, date_range: str | None = None) -> dict:
        """Return mock available time slots for a specialty."""
        spec_key = specialty.strip().lower()
        providers = PROVIDER_DB.get(spec_key, [])

        if not providers:
            available_specs = list(PROVIDER_DB.keys())
            return {
                "specialty": specialty,
                "found": False,
                "message": f"No providers found for '{specialty}'. Available specialties: {', '.join(available_specs)}",
                "slots": [],
            }

        # Filter by location if provided
        if location:
            loc_lower = location.strip().lower()
            filtered = [p for p in providers if loc_lower in p["location"].lower()]
            if filtered:
                providers = filtered

        # Generate available slots for the next 14 days
        now = datetime.now(timezone.utc)
        slots = []
        slot_id = 1

        for provider in providers:
            if not provider["accepting_new"]:
                continue
            for day_offset in range(1, 15):
                day = now + timedelta(days=day_offset)
                if day.weekday() >= 5:  # Skip weekends
                    continue
                # Generate 2-4 slots per day per provider
                num_slots = random.randint(2, 4)
                hours = sorted(random.sample([9, 10, 11, 13, 14, 15, 16], min(num_slots, 7)))
                for hour in hours[:num_slots]:
                    slot_time = day.replace(hour=hour, minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)
                    slots.append({
                        "slot_id": f"SLOT-{slot_id:04d}",
                        "provider_id": provider["provider_id"],
                        "provider_name": provider["name"],
                        "facility": provider["facility"],
                        "location": provider["location"],
                        "datetime": slot_time.isoformat(),
                        "duration_minutes": 30,
                        "telehealth_available": provider["telehealth"],
                        "date_display": slot_time.strftime("%A, %B %d, %Y"),
                        "time_display": slot_time.strftime("%I:%M %p"),
                    })
                    slot_id += 1

        # Limit to reasonable number
        slots = slots[:30]

        return {
            "specialty": specialty,
            "location": location,
            "found": True,
            "total_slots": len(slots),
            "providers_available": len([p for p in providers if p["accepting_new"]]),
            "slots": slots,
        }

    def book_appointment(self, patient_id: str, provider_id: str, slot_id: str) -> dict:
        """Create a mock appointment booking."""
        # Find provider
        provider = None
        specialty = None
        for spec, providers in PROVIDER_DB.items():
            for p in providers:
                if p["provider_id"] == provider_id:
                    provider = p
                    specialty = spec
                    break
            if provider:
                break

        if not provider:
            return {"error": f"Provider '{provider_id}' not found.", "booked": False}

        booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)
        scheduled = now + timedelta(days=random.randint(1, 14), hours=random.randint(9, 16))

        booking = {
            "booking_id": booking_id,
            "patient_id": patient_id,
            "provider_id": provider_id,
            "provider_name": provider["name"],
            "specialty": specialty,
            "facility": provider["facility"],
            "location": provider["location"],
            "slot_id": slot_id,
            "scheduled_at": scheduled.isoformat(),
            "status": "confirmed",
            "telehealth_available": provider["telehealth"],
            "created_at": now.isoformat(),
            "confirmation_number": f"CONF-{uuid.uuid4().hex[:6].upper()}",
        }

        self._bookings.append(booking)

        return {
            "booked": True,
            "booking": booking,
            "message": f"Appointment confirmed with {provider['name']} at {provider['facility']}.",
            "instructions": [
                "Arrive 15 minutes early for paperwork",
                "Bring photo ID and insurance card",
                "Bring a list of current medications",
                "Bring any relevant medical records or test results",
            ],
        }

    def get_booking_metrics(self) -> dict:
        """Return booking performance metrics."""
        total = len(self._bookings)
        if total == 0:
            return {"total_bookings": 0, "message": "No booking data available."}

        completed = sum(1 for b in self._bookings if b["status"] == "completed")
        no_shows = sum(1 for b in self._bookings if b["status"] == "no_show")
        cancelled = sum(1 for b in self._bookings if b["status"] == "cancelled")
        upcoming = sum(1 for b in self._bookings if b["status"] == "upcoming")
        confirmed = sum(1 for b in self._bookings if b["status"] == "confirmed")

        # Specialty breakdown
        by_specialty = {}
        for b in self._bookings:
            spec = b.get("specialty", "unknown")
            if spec not in by_specialty:
                by_specialty[spec] = 0
            by_specialty[spec] += 1

        # Sort by popularity
        popular = sorted(by_specialty.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_bookings": total,
            "status_breakdown": {
                "completed": completed,
                "upcoming": upcoming,
                "confirmed": confirmed,
                "no_show": no_shows,
                "cancelled": cancelled,
            },
            "no_show_rate": round((no_shows / total) * 100, 1) if total > 0 else 0,
            "cancellation_rate": round((cancelled / total) * 100, 1) if total > 0 else 0,
            "completion_rate": round((completed / max(1, completed + no_shows + cancelled)) * 100, 1),
            "popular_specialties": [{"specialty": s, "count": c} for s, c in popular],
            "avg_bookings_per_day": round(total / 30, 1),
            "telehealth_percentage": round(
                sum(1 for b in self._bookings if b.get("appointment_type") == "telehealth") / total * 100, 1
            ),
        }

    def recommend_telehealth_vs_inperson(self, diagnosis: str) -> dict:
        """Recommend telehealth or in-person visit with reasoning."""
        diag_key = diagnosis.strip().lower()

        if diag_key in INPERSON_REQUIRED:
            recommendation = "in_person"
            confidence = "high"
            reasoning = f"{diagnosis.title()} requires hands-on physical examination, diagnostic tests, or urgent intervention that cannot be performed remotely."
            factors = [
                "Physical examination required",
                "Diagnostic imaging or lab work likely needed",
                "Condition may require urgent intervention",
                "In-person monitoring essential for safety",
            ]
        elif diag_key in TELEHEALTH_SUITABLE:
            recommendation = "telehealth"
            confidence = "high"
            reasoning = f"{diagnosis.title()} can typically be effectively managed via telehealth. The provider can assess symptoms, adjust medications, and provide guidance remotely."
            factors = [
                "Condition can be assessed through patient history",
                "Visual examination via video may be sufficient",
                "Medication management can be done remotely",
                "Follow-up monitoring does not require in-person visit",
            ]
        else:
            recommendation = "either"
            confidence = "moderate"
            reasoning = f"For {diagnosis.title()}, either telehealth or in-person visit may be appropriate depending on symptom severity and the need for physical examination."
            factors = [
                "Initial assessment possible via telehealth",
                "In-person visit may be needed if physical exam is required",
                "Consider patient preference and travel distance",
                "Follow-ups are good candidates for telehealth",
            ]

        return {
            "diagnosis": diagnosis,
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": reasoning,
            "factors": factors,
            "telehealth_benefits": [
                "No travel time or transportation costs",
                "Reduced exposure to other illnesses in waiting rooms",
                "Shorter wait times on average",
                "More flexible scheduling options",
                "Access to specialists regardless of location",
            ],
            "inperson_benefits": [
                "Complete physical examination possible",
                "Diagnostic tests and imaging on-site",
                "Procedures can be performed immediately",
                "Better for complex or severe conditions",
            ],
        }

    def get_provider_directory(self, specialty: str, location: str | None = None) -> dict:
        """Return a list of providers for a specialty, optionally filtered by location."""
        spec_key = specialty.strip().lower()
        providers = PROVIDER_DB.get(spec_key, [])

        if not providers:
            return {
                "specialty": specialty,
                "found": False,
                "available_specialties": list(PROVIDER_DB.keys()),
                "providers": [],
                "total": 0,
            }

        if location:
            loc_lower = location.strip().lower()
            filtered = [p for p in providers if loc_lower in p["location"].lower()]
            if filtered:
                providers = filtered

        return {
            "specialty": specialty,
            "location": location,
            "found": True,
            "total": len(providers),
            "providers": providers,
        }

    # ── Internal helpers ────────────────────────────────────────────

    def _get_reasoning(self, diagnosis: str, urgency: str, appt_type: str) -> str:
        if appt_type == "emergency":
            return f"Based on the urgency level ({urgency}) of {diagnosis}, an emergency room visit is recommended for immediate evaluation and treatment."
        if appt_type == "urgent_care":
            return f"{diagnosis} with {urgency} urgency warrants same-day evaluation at an urgent care facility."
        if appt_type == "telehealth":
            return f"{diagnosis} can typically be effectively assessed and managed via telehealth, offering convenience and faster access."
        if appt_type == "specialist":
            return f"{diagnosis} would benefit from specialist evaluation for targeted diagnostic workup and treatment planning."
        return f"A primary care visit is appropriate for initial evaluation of {diagnosis}."

    def _get_alternatives(self, primary_type: str) -> list[dict]:
        alternatives = []
        for type_id, info in APPOINTMENT_TYPES.items():
            if type_id != primary_type:
                alternatives.append({"type": type_id, **info})
        return alternatives[:3]


# Singleton
_booking_agent = None


def get_booking_agent() -> AppointmentBookingAgent:
    global _booking_agent
    if _booking_agent is None:
        _booking_agent = AppointmentBookingAgent()
    return _booking_agent
