from .models import EmailIn
from typing import Dict

def parse_webhook(payload: Dict) -> EmailIn:
    # Support multiple providers; simple fallbacks
    from_address = payload.get("from") or payload.get("sender") or payload.get("mail",{}).get("source")
    to_address = payload.get("recipient") or payload.get("to")
    subject = payload.get("subject","")
    body_text = payload.get("body-plain") or payload.get("text") or payload.get("content","")
    html = payload.get("body-html") or payload.get("html")
    attachments = payload.get("attachments",[])  # may be URLs or names depending on webhook
    return EmailIn(
        from_address=str(from_address),
        to_address=str(to_address),
        subject=subject,
        body_text=body_text,
        html=html,
        attachments=attachments
    )
