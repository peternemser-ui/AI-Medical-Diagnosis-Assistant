import os
from typing import Optional, List
from datetime import datetime


class EmailTemplate:
    """Email template with placeholders."""

    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body

    def render(self, **kwargs) -> tuple[str, str]:
        """Render template with provided values."""
        subject = self.subject.format(**kwargs)
        body = self.body.format(**kwargs)
        return subject, body


# Pre-defined email templates
TEMPLATES = {
    'welcome': EmailTemplate(
        subject="Welcome to AI Medical Diagnosis Assistant",
        body="""
        Hello {name},

        Welcome to AI Medical Diagnosis Assistant! We're glad you've joined us.

        Your account has been created successfully. You can now:
        - Get AI-powered symptom analysis
        - Check drug interactions
        - Track your health history

        If you have any questions, please don't hesitate to reach out.

        Best regards,
        The Medical Diagnosis Team
        """
    ),
    'verification': EmailTemplate(
        subject="Verify your email address",
        body="""
        Hello {name},

        Please verify your email address by clicking the link below:

        {verification_url}

        This link will expire in 24 hours.

        If you didn't create an account, please ignore this email.

        Best regards,
        The Medical Diagnosis Team
        """
    ),
    'password_reset': EmailTemplate(
        subject="Reset your password",
        body="""
        Hello {name},

        We received a request to reset your password. Click the link below to set a new password:

        {reset_url}

        This link will expire in 1 hour.

        If you didn't request a password reset, please ignore this email.

        Best regards,
        The Medical Diagnosis Team
        """
    ),
    'urgent_diagnosis': EmailTemplate(
        subject="[URGENT] New urgent diagnosis requires review",
        body="""
        Attention Medical Staff,

        A new urgent diagnosis has been submitted that requires immediate review:

        Patient: {patient_name}
        Symptoms: {symptoms}
        AI Assessment: {assessment}
        Urgency Level: {urgency}
        Submitted: {timestamp}

        Red Flags Detected:
        {red_flags}

        Please review this case as soon as possible.

        View in dashboard: {dashboard_url}
        """
    ),
    'diagnosis_complete': EmailTemplate(
        subject="Your diagnosis results are ready",
        body="""
        Hello {name},

        Your symptom analysis is complete. Here's a summary:

        Primary Assessment: {primary_condition}
        Confidence: {confidence}%
        Urgency: {urgency}

        Recommendations:
        {recommendations}

        Please note that this is an AI-assisted assessment and should not replace professional medical advice.
        If you're experiencing severe symptoms, please seek immediate medical attention.

        View full results: {results_url}

        Best regards,
        The Medical Diagnosis Team
        """
    )
}


class EmailService:
    """Service for sending emails."""

    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@medicaldiagnosis.ai')
        self.from_name = os.getenv('FROM_NAME', 'Medical Diagnosis AI')

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[dict]] = None
    ) -> bool:
        """Send an email."""
        try:
            # In production, use aiosmtplib or similar
            print(f"Sending email to {to_email}: {subject}")
            print(f"Body: {body[:200]}...")

            # Log email for development
            self._log_email(to_email, subject, body)

            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    async def send_template(
        self,
        to_email: str,
        template_name: str,
        **kwargs
    ) -> bool:
        """Send email using a template."""
        template = TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"Unknown email template: {template_name}")

        subject, body = template.render(**kwargs)
        return await self.send_email(to_email, subject, body)

    async def send_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email to new user."""
        return await self.send_template(email, 'welcome', name=name)

    async def send_verification_email(
        self,
        email: str,
        name: str,
        verification_url: str
    ) -> bool:
        """Send email verification link."""
        return await self.send_template(
            email, 'verification',
            name=name,
            verification_url=verification_url
        )

    async def send_password_reset(
        self,
        email: str,
        name: str,
        reset_url: str
    ) -> bool:
        """Send password reset link."""
        return await self.send_template(
            email, 'password_reset',
            name=name,
            reset_url=reset_url
        )

    async def send_urgent_diagnosis_alert(
        self,
        admin_emails: List[str],
        patient_name: str,
        symptoms: str,
        assessment: str,
        urgency: str,
        red_flags: List[str],
        dashboard_url: str
    ) -> int:
        """Send alert to admins for urgent diagnosis."""
        sent_count = 0
        red_flags_text = '\n'.join(f"- {flag}" for flag in red_flags)

        for email in admin_emails:
            success = await self.send_template(
                email, 'urgent_diagnosis',
                patient_name=patient_name,
                symptoms=symptoms,
                assessment=assessment,
                urgency=urgency,
                red_flags=red_flags_text,
                timestamp=datetime.utcnow().isoformat(),
                dashboard_url=dashboard_url
            )
            if success:
                sent_count += 1

        return sent_count

    async def send_diagnosis_complete(
        self,
        email: str,
        name: str,
        primary_condition: str,
        confidence: int,
        urgency: str,
        recommendations: List[str],
        results_url: str
    ) -> bool:
        """Send diagnosis results to patient."""
        recommendations_text = '\n'.join(f"- {rec}" for rec in recommendations)

        return await self.send_template(
            email, 'diagnosis_complete',
            name=name,
            primary_condition=primary_condition,
            confidence=confidence,
            urgency=urgency,
            recommendations=recommendations_text,
            results_url=results_url
        )

    def _log_email(self, to: str, subject: str, body: str):
        """Log email for development/debugging."""
        log_dir = 'email_logs'
        os.makedirs(log_dir, exist_ok=True)

        filename = f"{log_dir}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{to.replace('@', '_at_')}.txt"

        with open(filename, 'w') as f:
            f.write(f"To: {to}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}\n")
            f.write("-" * 50 + "\n")
            f.write(body)
