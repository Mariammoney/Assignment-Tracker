import logging

import requests
from flask import current_app

logger = logging.getLogger(__name__)


def send_email(to, subject, html):
    api_key = current_app.config.get("RESEND_API_KEY")
    from_email = current_app.config.get("RESEND_FROM_EMAIL")
    if not api_key or not from_email:
        logger.warning("Resend is not configured; skipped email to %s", to)
        return False

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": from_email,
                "to": [to],
                "subject": subject,
                "html": html,
            },
            timeout=15,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Resend email delivery failed for %s", to)
        return False
