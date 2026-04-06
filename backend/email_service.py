"""
Email Notification Service

Sends transactional emails for:
- Welcome (after signup)
- Diagnosis complete
- Subscription upgrade confirmation
- Usage limit warning (80% used)
"""
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@meddiagnose.ai")
        self.enabled = bool(self.smtp_host and self.smtp_user)

    def send(self, to_email, subject, html_body):
        if not self.enabled:
            logger.info("[EMAIL-DEMO] To: %s | Subject: %s", to_email, subject)
            # Store for demo/testing
            self._log_email(to_email, subject, html_body)
            return True
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.from_email, to_email, msg.as_string())
            return True
        except Exception as e:
            logger.error("Email send failed: %s", e)
            return False

    def _log_email(self, to, subject, body):
        """Log emails for demo mode."""
        from pathlib import Path
        import json
        log_path = Path(__file__).parent / "email_log.json"
        logs = []
        if log_path.exists():
            try: logs = json.loads(log_path.read_text())
            except Exception: pass
        logs.append({"to": to, "subject": subject, "timestamp": datetime.now().isoformat(), "body_preview": body[:200]})
        log_path.write_text(json.dumps(logs[-50:], indent=2))

    def send_welcome(self, email, name):
        self.send(email, "Welcome to MedDiagnose AI!", f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
            <h1 style="color:#3b82f6;">Welcome, {name}!</h1>
            <p>Your AI medical assistant is ready. 7 specialized agents are standing by to help.</p>
            <a href="{FRONTEND_URL}/consult" style="display:inline-block;padding:12px 24px;background:#3b82f6;color:white;text-decoration:none;border-radius:8px;">Start Your First Consultation</a>
            <p style="color:#64748b;font-size:12px;margin-top:20px;">MedDiagnose AI — For informational purposes only.</p>
        </div>""")

    def send_diagnosis_complete(self, email, name, diagnosis, confidence):
        self.send(email, f"Your Diagnosis Report is Ready — {diagnosis}", f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
            <h1 style="color:#3b82f6;">Your Report is Ready</h1>
            <p>Hi {name}, your AI clinical assessment is complete.</p>
            <div style="background:#f0f9ff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6;">
                <strong>{diagnosis}</strong><br/>
                Confidence: {confidence}%
            </div>
            <a href="{FRONTEND_URL}/dashboard" style="display:inline-block;padding:12px 24px;background:#3b82f6;color:white;text-decoration:none;border-radius:8px;margin-top:16px;">View Full Report</a>
        </div>""")

    def send_upgrade_confirmation(self, email, name, tier, price):
        self.send(email, f"Welcome to {tier.title()}! — MedDiagnose AI", f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
            <h1 style="color:#10b981;">You're Upgraded!</h1>
            <p>Hi {name}, your plan is now <strong>{tier.title()}</strong> (${price}/mo).</p>
            <p>You now have access to all premium features.</p>
        </div>""")

    def send_usage_warning(self, email, name, used, limit):
        self.send(email, "You're Running Low on Diagnoses — MedDiagnose AI", f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
            <h1 style="color:#f59e0b;">Usage Alert</h1>
            <p>Hi {name}, you've used {used} of {limit} diagnoses this month.</p>
            <a href="{FRONTEND_URL}/pricing" style="display:inline-block;padding:12px 24px;background:#f59e0b;color:white;text-decoration:none;border-radius:8px;">Upgrade for More</a>
        </div>""")
