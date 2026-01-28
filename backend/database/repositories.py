from typing import Optional, List
from datetime import datetime
import uuid

from .models import (
    UserModel, DiagnosisModel, SessionModel,
    MedicalHistoryModel, ConversationModel,
    DrugInteractionModel, AppointmentModel
)


class BaseRepository:
    """Base repository with common CRUD operations."""

    def __init__(self):
        # In-memory storage for development
        self._storage: dict = {}

    async def create(self, item: dict) -> dict:
        item_id = item.get('id', str(uuid.uuid4()))
        item['id'] = item_id
        self._storage[item_id] = item
        return item

    async def get_by_id(self, item_id: str) -> Optional[dict]:
        return self._storage.get(item_id)

    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        if item_id in self._storage:
            self._storage[item_id].update(data)
            self._storage[item_id]['updated_at'] = datetime.utcnow()
            return self._storage[item_id]
        return None

    async def delete(self, item_id: str) -> bool:
        if item_id in self._storage:
            del self._storage[item_id]
            return True
        return False

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[dict]:
        items = list(self._storage.values())
        return items[offset:offset + limit]


class UserRepository(BaseRepository):
    """Repository for user operations."""

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        for user in self._storage.values():
            if user.get('email') == email:
                return UserModel(**user)
        return None

    async def create_user(self, user_data: dict) -> UserModel:
        user = await self.create(user_data)
        return UserModel(**user)

    async def update_user(self, user_id: str, data: dict) -> Optional[UserModel]:
        user = await self.update(user_id, data)
        if user:
            return UserModel(**user)
        return None

    async def search_users(
        self,
        query: str,
        role: Optional[str] = None,
        limit: int = 20
    ) -> List[UserModel]:
        results = []
        for user in self._storage.values():
            if query.lower() in user.get('name', '').lower() or \
               query.lower() in user.get('email', '').lower():
                if role is None or user.get('role') == role:
                    results.append(UserModel(**user))
                    if len(results) >= limit:
                        break
        return results


class DiagnosisRepository(BaseRepository):
    """Repository for diagnosis operations."""

    async def create_diagnosis(self, diagnosis_data: dict) -> DiagnosisModel:
        diagnosis = await self.create(diagnosis_data)
        return DiagnosisModel(**diagnosis)

    async def get_user_diagnoses(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[DiagnosisModel]:
        results = []
        for diagnosis in self._storage.values():
            if diagnosis.get('user_id') == user_id:
                if status is None or diagnosis.get('status') == status:
                    results.append(DiagnosisModel(**diagnosis))
                    if len(results) >= limit:
                        break
        return sorted(results, key=lambda x: x.created_at, reverse=True)

    async def get_recent_diagnoses(self, limit: int = 10) -> List[DiagnosisModel]:
        diagnoses = [DiagnosisModel(**d) for d in self._storage.values()]
        return sorted(diagnoses, key=lambda x: x.created_at, reverse=True)[:limit]

    async def get_diagnoses_by_urgency(
        self,
        urgency: str,
        limit: int = 50
    ) -> List[DiagnosisModel]:
        results = []
        for diagnosis in self._storage.values():
            if diagnosis.get('urgency') == urgency:
                results.append(DiagnosisModel(**diagnosis))
                if len(results) >= limit:
                    break
        return results


class SessionRepository(BaseRepository):
    """Repository for session operations."""

    async def create_session(self, session_data: dict) -> SessionModel:
        session = await self.create(session_data)
        return SessionModel(**session)

    async def get_user_sessions(self, user_id: str) -> List[SessionModel]:
        return [
            SessionModel(**s) for s in self._storage.values()
            if s.get('user_id') == user_id and s.get('is_active')
        ]

    async def invalidate_session(self, session_id: str) -> bool:
        if session_id in self._storage:
            self._storage[session_id]['is_active'] = False
            return True
        return False

    async def invalidate_user_sessions(self, user_id: str) -> int:
        count = 0
        for session_id, session in self._storage.items():
            if session.get('user_id') == user_id and session.get('is_active'):
                session['is_active'] = False
                count += 1
        return count


class MedicalHistoryRepository(BaseRepository):
    """Repository for medical history operations."""

    async def create_entry(self, entry_data: dict) -> MedicalHistoryModel:
        entry = await self.create(entry_data)
        return MedicalHistoryModel(**entry)

    async def get_user_history(
        self,
        user_id: str,
        entry_type: Optional[str] = None,
        limit: int = 100
    ) -> List[MedicalHistoryModel]:
        results = []
        for entry in self._storage.values():
            if entry.get('user_id') == user_id:
                if entry_type is None or entry.get('entry_type') == entry_type:
                    results.append(MedicalHistoryModel(**entry))
                    if len(results) >= limit:
                        break
        return sorted(results, key=lambda x: x.date, reverse=True)

    async def get_timeline(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[MedicalHistoryModel]:
        results = []
        for entry in self._storage.values():
            if entry.get('user_id') == user_id:
                entry_date = entry.get('date')
                if start_date and entry_date < start_date:
                    continue
                if end_date and entry_date > end_date:
                    continue
                results.append(MedicalHistoryModel(**entry))
        return sorted(results, key=lambda x: x.date, reverse=True)


class ConversationRepository(BaseRepository):
    """Repository for conversation history."""

    async def create_conversation(self, data: dict) -> ConversationModel:
        conversation = await self.create(data)
        return ConversationModel(**conversation)

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> Optional[ConversationModel]:
        if conversation_id in self._storage:
            message = {
                'role': role,
                'content': content,
                'timestamp': datetime.utcnow().isoformat()
            }
            self._storage[conversation_id]['messages'].append(message)
            return ConversationModel(**self._storage[conversation_id])
        return None

    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[ConversationModel]:
        results = [
            ConversationModel(**c) for c in self._storage.values()
            if c.get('user_id') == user_id
        ]
        return sorted(results, key=lambda x: x.updated_at, reverse=True)[:limit]


class AppointmentRepository(BaseRepository):
    """Repository for appointments."""

    async def create_appointment(self, data: dict) -> AppointmentModel:
        appointment = await self.create(data)
        return AppointmentModel(**appointment)

    async def get_user_appointments(
        self,
        user_id: str,
        status: Optional[str] = None,
        upcoming_only: bool = False
    ) -> List[AppointmentModel]:
        results = []
        now = datetime.utcnow()

        for appt in self._storage.values():
            if appt.get('user_id') == user_id:
                if status and appt.get('status') != status:
                    continue
                if upcoming_only and appt.get('scheduled_at') < now:
                    continue
                results.append(AppointmentModel(**appt))

        return sorted(results, key=lambda x: x.scheduled_at)

    async def get_provider_appointments(
        self,
        provider_id: str,
        date: Optional[datetime] = None
    ) -> List[AppointmentModel]:
        results = []
        for appt in self._storage.values():
            if appt.get('provider_id') == provider_id:
                if date:
                    appt_date = appt.get('scheduled_at')
                    if appt_date.date() != date.date():
                        continue
                results.append(AppointmentModel(**appt))
        return sorted(results, key=lambda x: x.scheduled_at)
