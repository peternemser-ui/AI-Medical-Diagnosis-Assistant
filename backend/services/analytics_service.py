from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


class AnalyticsService:
    """Service for tracking and analyzing system metrics."""

    def __init__(self):
        self._events: List[Dict] = []
        self._metrics: Dict[str, List[Dict]] = defaultdict(list)
        self._aggregations: Dict[str, Any] = {}

    async def track_event(
        self,
        event_name: str,
        user_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track an analytics event."""
        event = {
            'name': event_name,
            'user_id': user_id,
            'properties': properties or {},
            'timestamp': datetime.utcnow()
        }
        self._events.append(event)

    async def track_diagnosis(
        self,
        user_id: str,
        diagnosis_id: str,
        conditions: List[str],
        urgency: str,
        confidence: float,
        processing_time_ms: int
    ) -> None:
        """Track diagnosis event with detailed metrics."""
        await self.track_event('diagnosis_created', user_id, {
            'diagnosis_id': diagnosis_id,
            'condition_count': len(conditions),
            'primary_condition': conditions[0] if conditions else None,
            'urgency': urgency,
            'confidence': confidence,
            'processing_time_ms': processing_time_ms
        })

        # Update aggregations
        self._update_diagnosis_stats(urgency, confidence)

    async def track_user_action(
        self,
        user_id: str,
        action: str,
        target: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """Track user interaction."""
        await self.track_event('user_action', user_id, {
            'action': action,
            'target': target,
            **(metadata or {})
        })

    async def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a numeric metric."""
        metric = {
            'value': value,
            'type': metric_type.value,
            'tags': tags or {},
            'timestamp': datetime.utcnow()
        }
        self._metrics[name].append(metric)

    async def get_dashboard_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get statistics for admin dashboard."""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        if not end_date:
            end_date = datetime.utcnow()

        filtered_events = [
            e for e in self._events
            if start_date <= e['timestamp'] <= end_date
        ]

        diagnoses = [e for e in filtered_events if e['name'] == 'diagnosis_created']
        logins = [e for e in filtered_events if e['name'] == 'user_login']

        urgency_counts = defaultdict(int)
        condition_counts = defaultdict(int)
        total_confidence = 0

        for d in diagnoses:
            props = d.get('properties', {})
            urgency_counts[props.get('urgency', 'unknown')] += 1
            if props.get('primary_condition'):
                condition_counts[props['primary_condition']] += 1
            total_confidence += props.get('confidence', 0)

        return {
            'total_diagnoses': len(diagnoses),
            'total_logins': len(logins),
            'unique_users': len(set(e.get('user_id') for e in filtered_events if e.get('user_id'))),
            'urgency_distribution': dict(urgency_counts),
            'top_conditions': dict(sorted(condition_counts.items(), key=lambda x: -x[1])[:10]),
            'average_confidence': total_confidence / len(diagnoses) if diagnoses else 0,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }

    async def get_diagnosis_trends(
        self,
        days: int = 30,
        granularity: str = 'day'
    ) -> List[Dict]:
        """Get diagnosis count trends over time."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        diagnoses = [
            e for e in self._events
            if e['name'] == 'diagnosis_created' and start_date <= e['timestamp'] <= end_date
        ]

        # Group by date
        date_counts = defaultdict(int)
        for d in diagnoses:
            if granularity == 'day':
                key = d['timestamp'].strftime('%Y-%m-%d')
            elif granularity == 'hour':
                key = d['timestamp'].strftime('%Y-%m-%d %H:00')
            else:
                key = d['timestamp'].strftime('%Y-%m-%d')
            date_counts[key] += 1

        return [
            {'date': date, 'count': count}
            for date, count in sorted(date_counts.items())
        ]

    async def get_user_activity(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get activity history for a specific user."""
        user_events = [
            e for e in self._events
            if e.get('user_id') == user_id
        ]

        return sorted(user_events, key=lambda x: x['timestamp'], reverse=True)[:limit]

    async def get_system_health_metrics(self) -> Dict[str, Any]:
        """Get system health metrics."""
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)

        recent_diagnoses = [
            e for e in self._events
            if e['name'] == 'diagnosis_created' and e['timestamp'] >= last_hour
        ]

        processing_times = [
            e['properties'].get('processing_time_ms', 0)
            for e in recent_diagnoses
        ]

        return {
            'diagnoses_last_hour': len(recent_diagnoses),
            'avg_processing_time_ms': sum(processing_times) / len(processing_times) if processing_times else 0,
            'max_processing_time_ms': max(processing_times) if processing_times else 0,
            'min_processing_time_ms': min(processing_times) if processing_times else 0,
            'timestamp': now.isoformat()
        }

    async def get_condition_statistics(self) -> Dict[str, Any]:
        """Get statistics about diagnosed conditions."""
        diagnoses = [e for e in self._events if e['name'] == 'diagnosis_created']

        condition_data = defaultdict(lambda: {'count': 0, 'avg_confidence': 0, 'urgency_counts': defaultdict(int)})

        for d in diagnoses:
            props = d.get('properties', {})
            condition = props.get('primary_condition')
            if condition:
                condition_data[condition]['count'] += 1
                condition_data[condition]['avg_confidence'] += props.get('confidence', 0)
                condition_data[condition]['urgency_counts'][props.get('urgency', 'unknown')] += 1

        # Calculate averages
        for condition in condition_data:
            count = condition_data[condition]['count']
            condition_data[condition]['avg_confidence'] /= count
            condition_data[condition]['urgency_counts'] = dict(condition_data[condition]['urgency_counts'])

        return dict(condition_data)

    def _update_diagnosis_stats(self, urgency: str, confidence: float) -> None:
        """Update running diagnosis statistics."""
        if 'diagnosis_stats' not in self._aggregations:
            self._aggregations['diagnosis_stats'] = {
                'total': 0,
                'by_urgency': defaultdict(int),
                'confidence_sum': 0
            }

        stats = self._aggregations['diagnosis_stats']
        stats['total'] += 1
        stats['by_urgency'][urgency] += 1
        stats['confidence_sum'] += confidence

    async def export_data(
        self,
        start_date: datetime,
        end_date: datetime,
        event_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """Export analytics data for a date range."""
        filtered = [
            e for e in self._events
            if start_date <= e['timestamp'] <= end_date
        ]

        if event_types:
            filtered = [e for e in filtered if e['name'] in event_types]

        return [
            {
                **e,
                'timestamp': e['timestamp'].isoformat()
            }
            for e in filtered
        ]
