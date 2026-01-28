import json
import csv
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    HTML = "html"


class ExportService:
    """Service for exporting data in various formats."""

    async def export_diagnosis(
        self,
        diagnosis: Dict[str, Any],
        format: ExportFormat = ExportFormat.JSON
    ) -> bytes:
        """Export a single diagnosis."""
        if format == ExportFormat.JSON:
            return self._to_json(diagnosis)
        elif format == ExportFormat.CSV:
            return self._diagnosis_to_csv([diagnosis])
        elif format == ExportFormat.HTML:
            return self._diagnosis_to_html(diagnosis)
        else:
            raise ValueError(f"Unsupported format: {format}")

    async def export_diagnoses(
        self,
        diagnoses: List[Dict[str, Any]],
        format: ExportFormat = ExportFormat.JSON
    ) -> bytes:
        """Export multiple diagnoses."""
        if format == ExportFormat.JSON:
            return self._to_json(diagnoses)
        elif format == ExportFormat.CSV:
            return self._diagnosis_to_csv(diagnoses)
        else:
            raise ValueError(f"Unsupported format for batch export: {format}")

    async def export_user_data(
        self,
        user_id: str,
        include_diagnoses: bool = True,
        include_history: bool = True,
        include_conversations: bool = False
    ) -> bytes:
        """Export all user data (GDPR compliance)."""
        data = {
            'export_date': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'data': {}
        }

        if include_diagnoses:
            data['data']['diagnoses'] = []  # Would fetch from database

        if include_history:
            data['data']['medical_history'] = []  # Would fetch from database

        if include_conversations:
            data['data']['conversations'] = []  # Would fetch from database

        return self._to_json(data)

    async def export_analytics_report(
        self,
        stats: Dict[str, Any],
        format: ExportFormat = ExportFormat.JSON
    ) -> bytes:
        """Export analytics report."""
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'report_type': 'analytics',
            'data': stats
        }

        if format == ExportFormat.JSON:
            return self._to_json(report)
        elif format == ExportFormat.CSV:
            return self._stats_to_csv(stats)
        elif format == ExportFormat.HTML:
            return self._stats_to_html(stats)
        else:
            raise ValueError(f"Unsupported format: {format}")

    async def export_audit_logs(
        self,
        logs: List[Dict[str, Any]],
        format: ExportFormat = ExportFormat.CSV
    ) -> bytes:
        """Export audit logs."""
        if format == ExportFormat.CSV:
            return self._logs_to_csv(logs)
        elif format == ExportFormat.JSON:
            return self._to_json(logs)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _to_json(self, data: Any) -> bytes:
        """Convert data to JSON bytes."""
        return json.dumps(data, indent=2, default=str).encode('utf-8')

    def _diagnosis_to_csv(self, diagnoses: List[Dict]) -> bytes:
        """Convert diagnoses to CSV."""
        if not diagnoses:
            return b''

        output = io.StringIO()
        fieldnames = [
            'id', 'created_at', 'symptoms', 'primary_condition',
            'confidence', 'urgency', 'recommendations', 'red_flags'
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for d in diagnoses:
            conditions = d.get('conditions', [])
            row = {
                'id': d.get('id', ''),
                'created_at': d.get('created_at', ''),
                'symptoms': '; '.join(d.get('symptoms', [])),
                'primary_condition': conditions[0].get('name', '') if conditions else '',
                'confidence': conditions[0].get('confidence', '') if conditions else '',
                'urgency': d.get('urgency', ''),
                'recommendations': '; '.join(d.get('recommendations', [])),
                'red_flags': '; '.join(d.get('red_flags', []))
            }
            writer.writerow(row)

        return output.getvalue().encode('utf-8')

    def _diagnosis_to_html(self, diagnosis: Dict) -> bytes:
        """Convert diagnosis to HTML report."""
        conditions = diagnosis.get('conditions', [])
        primary = conditions[0] if conditions else {}

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Medical Diagnosis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .header {{ border-bottom: 2px solid #3B82F6; padding-bottom: 20px; margin-bottom: 20px; }}
        .section {{ margin-bottom: 30px; }}
        .section-title {{ font-size: 18px; font-weight: bold; color: #1F2937; margin-bottom: 10px; }}
        .urgency {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 14px; }}
        .urgency-routine {{ background: #D1FAE5; color: #065F46; }}
        .urgency-soon {{ background: #FEF3C7; color: #92400E; }}
        .urgency-urgent {{ background: #FED7AA; color: #9A3412; }}
        .urgency-emergency {{ background: #FEE2E2; color: #991B1B; }}
        .condition {{ background: #F3F4F6; padding: 15px; border-radius: 8px; margin-bottom: 10px; }}
        .condition-name {{ font-weight: bold; font-size: 16px; }}
        .confidence {{ color: #6B7280; }}
        .red-flag {{ background: #FEE2E2; border-left: 4px solid #EF4444; padding: 10px 15px; margin-bottom: 10px; }}
        .recommendation {{ background: #DBEAFE; border-left: 4px solid #3B82F6; padding: 10px 15px; margin-bottom: 10px; }}
        .disclaimer {{ font-size: 12px; color: #6B7280; border-top: 1px solid #E5E7EB; padding-top: 20px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Medical Diagnosis Report</h1>
        <p>Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    </div>

    <div class="section">
        <div class="section-title">Assessment Summary</div>
        <p><strong>Primary Finding:</strong> {primary.get('name', 'N/A')}</p>
        <p><strong>Confidence:</strong> {primary.get('confidence', 'N/A')}%</p>
        <p><strong>Urgency:</strong> <span class="urgency urgency-{diagnosis.get('urgency', 'routine')}">{diagnosis.get('urgency', 'N/A').upper()}</span></p>
    </div>

    <div class="section">
        <div class="section-title">Reported Symptoms</div>
        <p>{diagnosis.get('symptom_description', 'N/A')}</p>
    </div>

    <div class="section">
        <div class="section-title">Possible Conditions</div>
        {''.join(f'<div class="condition"><div class="condition-name">{c.get("name", "")}</div><div class="confidence">{c.get("confidence", "")}% confidence</div><p>{c.get("description", "")}</p></div>' for c in conditions)}
    </div>

    {'<div class="section"><div class="section-title">Red Flags</div>' + ''.join(f'<div class="red-flag">{flag}</div>' for flag in diagnosis.get('red_flags', [])) + '</div>' if diagnosis.get('red_flags') else ''}

    <div class="section">
        <div class="section-title">Recommendations</div>
        {''.join(f'<div class="recommendation">{rec}</div>' for rec in diagnosis.get('recommendations', []))}
    </div>

    <div class="disclaimer">
        <p><strong>Disclaimer:</strong> This report is generated by an AI-assisted medical diagnosis system and is intended for informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
    </div>
</body>
</html>
"""
        return html.encode('utf-8')

    def _stats_to_csv(self, stats: Dict) -> bytes:
        """Convert statistics to CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['Metric', 'Value'])

        for key, value in stats.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    writer.writerow([f"{key}.{sub_key}", sub_value])
            else:
                writer.writerow([key, value])

        return output.getvalue().encode('utf-8')

    def _stats_to_html(self, stats: Dict) -> bytes:
        """Convert statistics to HTML report."""
        rows = []
        for key, value in stats.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    rows.append(f"<tr><td>{key}.{sub_key}</td><td>{sub_value}</td></tr>")
            else:
                rows.append(f"<tr><td>{key}</td><td>{value}</td></tr>")

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Analytics Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #E5E7EB; }}
        th {{ background: #F3F4F6; }}
    </style>
</head>
<body>
    <h1>Analytics Report</h1>
    <p>Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    <table>
        <thead>
            <tr><th>Metric</th><th>Value</th></tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
</body>
</html>
"""
        return html.encode('utf-8')

    def _logs_to_csv(self, logs: List[Dict]) -> bytes:
        """Convert audit logs to CSV."""
        if not logs:
            return b''

        output = io.StringIO()
        fieldnames = ['timestamp', 'user', 'action', 'level', 'details', 'ip_address']

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for log in logs:
            row = {
                'timestamp': log.get('timestamp', ''),
                'user': log.get('userName', ''),
                'action': log.get('action', ''),
                'level': log.get('level', ''),
                'details': log.get('details', ''),
                'ip_address': log.get('ipAddress', '')
            }
            writer.writerow(row)

        return output.getvalue().encode('utf-8')
