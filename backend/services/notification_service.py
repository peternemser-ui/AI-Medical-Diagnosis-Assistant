from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import json


class NotificationType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    URGENT = "urgent"


class NotificationChannel(str, Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Notification:
    """Represents a notification."""

    def __init__(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        channels: List[NotificationChannel] = None,
        data: Optional[Dict[str, Any]] = None,
        action_url: Optional[str] = None
    ):
        self.id = f"notif_{datetime.utcnow().timestamp()}"
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.channels = channels or [NotificationChannel.IN_APP]
        self.data = data or {}
        self.action_url = action_url
        self.created_at = datetime.utcnow()
        self.read_at: Optional[datetime] = None
        self.sent_via: List[str] = []


class NotificationService:
    """Service for managing and sending notifications."""

    def __init__(self):
        self._notifications: Dict[str, List[Notification]] = {}
        self._user_preferences: Dict[str, Dict] = {}

    async def send(self, notification: Notification) -> bool:
        """Send a notification through configured channels."""
        user_prefs = self._get_user_preferences(notification.user_id)

        for channel in notification.channels:
            if self._is_channel_enabled(user_prefs, channel):
                success = await self._send_via_channel(notification, channel)
                if success:
                    notification.sent_via.append(channel.value)

        # Store notification for in-app display
        self._store_notification(notification)

        return len(notification.sent_via) > 0

    async def send_to_users(
        self,
        user_ids: List[str],
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        **kwargs
    ) -> int:
        """Send notification to multiple users."""
        sent_count = 0

        for user_id in user_ids:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                **kwargs
            )

            if await self.send(notification):
                sent_count += 1

        return sent_count

    async def notify_diagnosis_complete(
        self,
        user_id: str,
        diagnosis_id: str,
        primary_condition: str,
        urgency: str
    ) -> bool:
        """Notify user that diagnosis is complete."""
        notification = Notification(
            user_id=user_id,
            title="Diagnosis Complete",
            message=f"Your symptom analysis is ready. Primary finding: {primary_condition}",
            notification_type=NotificationType.SUCCESS if urgency == "routine" else NotificationType.WARNING,
            data={
                "diagnosis_id": diagnosis_id,
                "primary_condition": primary_condition,
                "urgency": urgency
            },
            action_url=f"/diagnosis/{diagnosis_id}"
        )

        return await self.send(notification)

    async def notify_urgent_case(
        self,
        admin_user_ids: List[str],
        patient_name: str,
        diagnosis_id: str,
        urgency: str
    ) -> int:
        """Notify admins of urgent case."""
        return await self.send_to_users(
            user_ids=admin_user_ids,
            title=f"[{urgency.upper()}] New urgent case",
            message=f"Patient {patient_name} has submitted symptoms requiring urgent review.",
            notification_type=NotificationType.URGENT,
            channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL],
            data={"diagnosis_id": diagnosis_id},
            action_url=f"/admin/diagnoses/{diagnosis_id}"
        )

    async def notify_medication_reminder(
        self,
        user_id: str,
        medication_name: str,
        dosage: str
    ) -> bool:
        """Send medication reminder."""
        notification = Notification(
            user_id=user_id,
            title="Medication Reminder",
            message=f"Time to take {medication_name} ({dosage})",
            notification_type=NotificationType.INFO,
            channels=[NotificationChannel.IN_APP, NotificationChannel.PUSH]
        )

        return await self.send(notification)

    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user."""
        notifications = self._notifications.get(user_id, [])

        if unread_only:
            notifications = [n for n in notifications if n.read_at is None]

        return sorted(notifications, key=lambda n: n.created_at, reverse=True)[:limit]

    def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications."""
        notifications = self._notifications.get(user_id, [])
        return len([n for n in notifications if n.read_at is None])

    async def mark_as_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read."""
        notifications = self._notifications.get(user_id, [])

        for notification in notifications:
            if notification.id == notification_id:
                notification.read_at = datetime.utcnow()
                return True

        return False

    async def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read."""
        notifications = self._notifications.get(user_id, [])
        count = 0

        for notification in notifications:
            if notification.read_at is None:
                notification.read_at = datetime.utcnow()
                count += 1

        return count

    def set_user_preferences(self, user_id: str, preferences: Dict) -> None:
        """Set notification preferences for a user."""
        self._user_preferences[user_id] = preferences

    def _get_user_preferences(self, user_id: str) -> Dict:
        """Get notification preferences for a user."""
        return self._user_preferences.get(user_id, {
            'in_app': True,
            'email': True,
            'sms': False,
            'push': True
        })

    def _is_channel_enabled(self, preferences: Dict, channel: NotificationChannel) -> bool:
        """Check if channel is enabled in preferences."""
        return preferences.get(channel.value, False)

    def _store_notification(self, notification: Notification) -> None:
        """Store notification for in-app display."""
        if notification.user_id not in self._notifications:
            self._notifications[notification.user_id] = []

        self._notifications[notification.user_id].append(notification)

        # Keep only last 100 notifications per user
        if len(self._notifications[notification.user_id]) > 100:
            self._notifications[notification.user_id] = \
                self._notifications[notification.user_id][-100:]

    async def _send_via_channel(
        self,
        notification: Notification,
        channel: NotificationChannel
    ) -> bool:
        """Send notification via specific channel."""
        if channel == NotificationChannel.IN_APP:
            return True  # Already stored

        elif channel == NotificationChannel.EMAIL:
            # Integrate with EmailService
            print(f"Sending email notification to user {notification.user_id}")
            return True

        elif channel == NotificationChannel.SMS:
            # Integrate with SMS provider
            print(f"Sending SMS notification to user {notification.user_id}")
            return True

        elif channel == NotificationChannel.PUSH:
            # Integrate with push notification service
            print(f"Sending push notification to user {notification.user_id}")
            return True

        return False
