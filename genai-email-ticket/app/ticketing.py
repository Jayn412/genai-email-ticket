import requests
from .config import settings

def create_ticket(title: str, description: str, metadata: dict) -> dict:
    # Placeholder integration. If using Zendesk/Jira adapt payload & auth.
    url = settings.TICKET_API_URL
    token = settings.TICKET_API_TOKEN
    if not url:
        return {"id": f"local-{title[:8]}", "note":"no-ticket-api-configured"}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"title": title, "description": description, "metadata": metadata}
    r = requests.post(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()
