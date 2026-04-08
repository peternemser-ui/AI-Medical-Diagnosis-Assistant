"""
Stripe Webhook Handler

POST /api/webhooks/stripe — Verifies Stripe signature and dispatches events:
  - checkout.session.completed   → Activate subscription
  - customer.subscription.updated → Update tier
  - customer.subscription.deleted → Downgrade to free
  - invoice.payment_failed        → Flag account, send notification

Uses STRIPE_WEBHOOK_SECRET env var for signature verification.
Returns 503 when Stripe is not configured.
"""

import os
import logging
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

stripe_webhook_router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
_STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")


def _stripe_configured() -> bool:
    return bool(
        _STRIPE_KEY and _STRIPE_KEY.startswith("sk_")
        and _WEBHOOK_SECRET and _WEBHOOK_SECRET.startswith("whsec_")
    )


@stripe_webhook_router.post("/stripe")
async def stripe_webhook(request: Request):
    """
    Receive and verify Stripe webhook events.

    Stripe delivers signed POST requests; we verify the signature using
    stripe.Webhook.construct_event() before processing any payload.

    Returns 503 when Stripe is not configured so that Stripe's dashboard
    shows a clear failure state rather than a silent 200.
    """
    # Reload at request time so env changes (e.g., .env reload) take effect
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "")

    if not (stripe_key and stripe_key.startswith("sk_") and webhook_secret):
        return JSONResponse(
            status_code=503,
            content={"error": "Stripe is not configured on this server"},
        )

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        import stripe as _stripe
        _stripe.api_key = stripe_key
        event = _stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ImportError:
        logger.error("stripe package is not installed")
        return JSONResponse(status_code=503, content={"error": "stripe package not installed"})
    except Exception as exc:
        # Covers stripe.error.SignatureVerificationError and malformed payload
        logger.warning("Stripe webhook signature verification failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})

    event_type = event["type"]
    logger.info("Stripe webhook received: %s", event_type)

    try:
        if event_type == "checkout.session.completed":
            _handle_checkout_completed(event["data"]["object"])

        elif event_type == "customer.subscription.updated":
            _handle_subscription_updated(event["data"]["object"])

        elif event_type == "customer.subscription.deleted":
            _handle_subscription_deleted(event["data"]["object"])

        elif event_type == "invoice.payment_failed":
            _handle_payment_failed(event["data"]["object"])

        else:
            logger.debug("Stripe webhook: unhandled event type %s (ignored)", event_type)

    except Exception as exc:
        # Log but still return 200 — Stripe will otherwise retry endlessly
        logger.error("Error processing Stripe event %s: %s", event_type, exc, exc_info=True)

    return {"status": "ok", "type": event_type}


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------

def _handle_checkout_completed(session: dict) -> None:
    """checkout.session.completed — activate the subscription for the user."""
    user_id = session.get("metadata", {}).get("user_id")
    tier = session.get("metadata", {}).get("tier")
    customer_id = session.get("customer")

    if not user_id or not tier:
        logger.warning("checkout.session.completed missing user_id/tier in metadata: %s", session.get("id"))
        return

    from agents.subscription_agent import SubscriptionManager
    sub = SubscriptionManager()
    sub.set_user_tier(user_id, tier)

    # Persist the Stripe customer_id so we can open billing portal later
    if customer_id:
        try:
            from database import Database
            db = Database.get()
            db.update_user(user_id, {"stripe_customer_id": customer_id})
        except Exception as exc:
            logger.warning("Could not store stripe_customer_id: %s", exc)

    logger.info("Stripe: activated %s subscription for user %s", tier, user_id)

    # Send confirmation email if user record and email service are available
    try:
        from database import Database
        from email_service import EmailService
        db = Database.get()
        user = db.get_user(user_id)
        if user:
            tier_prices = {"plus": 9.99, "pro": 29.99, "family": 49.99}
            EmailService().send_upgrade_confirmation(
                email=user.get("email", ""),
                name=user.get("name", ""),
                tier=tier,
                price=tier_prices.get(tier, 0),
            )
    except Exception as exc:
        logger.warning("Could not send upgrade confirmation email: %s", exc)


def _handle_subscription_updated(subscription: dict) -> None:
    """customer.subscription.updated — sync the tier when plan changes."""
    user_id = subscription.get("metadata", {}).get("user_id")
    status = subscription.get("status")

    if not user_id:
        logger.debug("subscription.updated without user_id in metadata — skipping")
        return

    # Derive tier from subscription items
    tier = _tier_from_subscription(subscription)

    if status in ("active", "trialing") and tier:
        from agents.subscription_agent import SubscriptionManager
        SubscriptionManager().set_user_tier(user_id, tier)
        logger.info("Stripe: updated user %s to tier %s (status=%s)", user_id, tier, status)
    elif status in ("canceled", "unpaid", "past_due"):
        from agents.subscription_agent import SubscriptionManager
        SubscriptionManager().set_user_tier(user_id, "free")
        logger.info("Stripe: downgraded user %s to free (status=%s)", user_id, status)


def _handle_subscription_deleted(subscription: dict) -> None:
    """customer.subscription.deleted — downgrade the user to the free tier."""
    user_id = subscription.get("metadata", {}).get("user_id")

    if not user_id:
        logger.debug("subscription.deleted without user_id in metadata — skipping")
        return

    from agents.subscription_agent import SubscriptionManager
    SubscriptionManager().set_user_tier(user_id, "free")
    logger.info("Stripe: subscription deleted — downgraded user %s to free", user_id)


def _handle_payment_failed(invoice: dict) -> None:
    """invoice.payment_failed — flag the account and notify the user."""
    customer_id = invoice.get("customer")
    user_email = invoice.get("customer_email", "")
    attempt_count = invoice.get("attempt_count", 1)

    logger.warning(
        "Stripe: payment failed for customer %s (email=%s, attempt=%s)",
        customer_id, user_email, attempt_count,
    )

    # Try to find the user and send a payment-failed notification
    try:
        from database import Database
        from email_service import EmailService

        db = Database.get()
        user = None

        # Look up by stripe_customer_id if the DB supports it
        if customer_id:
            try:
                user = db.get_user_by_stripe_customer_id(customer_id)
            except AttributeError:
                pass  # Method may not exist; fall through to email lookup

        if user is None and user_email:
            user = db.get_user_by_email(user_email)

        if user:
            _send_payment_failed_email(EmailService(), user, attempt_count)
    except Exception as exc:
        logger.error("Failed to process payment_failed event: %s", exc)


def _send_payment_failed_email(email_svc, user: dict, attempt_count: int) -> None:
    """Send a payment failure notification email."""
    from email_service import FRONTEND_URL

    name = user.get("name") or "Valued Customer"
    email = user.get("email", "")
    if not email:
        return

    subject = "Action Required: Payment Failed — MedDiagnose AI"
    body = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
        <h1 style="color:#ef4444;">Payment Failed</h1>
        <p>Hi {name},</p>
        <p>We were unable to process your subscription payment (attempt {attempt_count}).</p>
        <p>Please update your payment method to avoid losing access to premium features.</p>
        <a href="{FRONTEND_URL}/settings?billing=true"
           style="display:inline-block;padding:12px 24px;background:#ef4444;color:white;
                  text-decoration:none;border-radius:8px;margin-top:16px;">
            Update Payment Method
        </a>
        <p style="color:#64748b;font-size:12px;margin-top:20px;">
            If you believe this is an error, please contact support.
        </p>
    </div>"""

    email_svc.send(email, subject, body)
    logger.info("Sent payment_failed email to %s", email)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tier_from_subscription(subscription: dict) -> Optional[str]:
    """Derive our tier key from a Stripe subscription's price metadata or nickname."""
    import os
    try:
        items = subscription.get("items", {}).get("data", [])
        if not items:
            return None
        price_id = items[0].get("price", {}).get("id", "")
        # Match against known price IDs
        for key, pid in {
            "plus_monthly": os.getenv("STRIPE_PRICE_PLUS_MONTHLY", ""),
            "plus_annual": os.getenv("STRIPE_PRICE_PLUS_ANNUAL", ""),
            "pro_monthly": os.getenv("STRIPE_PRICE_PRO_MONTHLY", ""),
            "pro_annual": os.getenv("STRIPE_PRICE_PRO_ANNUAL", ""),
            "family_monthly": os.getenv("STRIPE_PRICE_FAMILY_MONTHLY", ""),
            "family_annual": os.getenv("STRIPE_PRICE_FAMILY_ANNUAL", ""),
        }.items():
            if pid and price_id == pid:
                return key.split("_")[0]  # "plus", "pro", or "family"
        # Fall back to nickname
        nickname = items[0].get("price", {}).get("nickname", "").lower()
        for t in ("plus", "pro", "family"):
            if t in nickname:
                return t
        return None
    except Exception:
        return None
