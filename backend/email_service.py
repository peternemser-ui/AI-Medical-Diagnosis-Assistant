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

    def send_verification_email(self, email: str, name: str, token: str) -> bool:
        """Send an email address verification link to a newly registered user."""
        verify_url = f"{FRONTEND_URL}/login?verified=pending&token={token}"
        # The backend verify endpoint does the actual verification and redirects;
        # the link points there via the API.
        api_verify_url = f"/api/auth/verify-email?token={token}"
        # Build an absolute URL using FRONTEND_URL as origin base for the API call
        import os
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        verify_link = f"{backend_url}/api/auth/verify-email?token={token}"

        subject = "Verify your email address — MedDiagnose AI"
        body = f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
            <div style="text-align:center;padding:32px 0 24px;">
                <div style="display:inline-flex;padding:16px;border-radius:16px;
                            background:linear-gradient(135deg,#10b981,#0d9488);
                            margin-bottom:20px;">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
                        <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z"/>
                    </svg>
                </div>
                <h1 style="color:#0f172a;font-size:24px;margin:0;">Verify your email</h1>
            </div>
            <p style="color:#334155;">Hi {name or 'there'},</p>
            <p style="color:#334155;">
                Thanks for signing up for MedDiagnose AI. Click the button below to
                verify your email address and activate your account.
            </p>
            <div style="text-align:center;margin:32px 0;">
                <a href="{verify_link}"
                   style="display:inline-block;padding:14px 32px;
                          background:linear-gradient(135deg,#10b981,#0d9488);
                          color:white;font-weight:600;text-decoration:none;
                          border-radius:10px;font-size:16px;">
                    Verify Email Address
                </a>
            </div>
            <p style="color:#64748b;font-size:13px;">
                This link expires in 24 hours. If you did not create an account,
                you can safely ignore this email.
            </p>
            <p style="color:#94a3b8;font-size:12px;">
                Or copy and paste this URL: {verify_link}
            </p>
            <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;"/>
            <p style="color:#94a3b8;font-size:11px;text-align:center;">
                MedDiagnose AI — For informational purposes only. Not a substitute
                for professional medical advice.
            </p>
        </div>"""

        return self.send(email, subject, body)
