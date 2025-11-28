import requests
from .config import settings
import json

def notify_slack(text: str, channel: str = None):
    if settings.SLACK_WEBHOOK_URL:
        payload = {"text": text}
        requests.post(settings.SLACK_WEBHOOK_URL, json=payload, timeout=5)
    elif settings.SLACK_BOT_TOKEN and channel:
        # use chat.postMessage
        headers = {"Authorization": f"Bearer {settings.SLACK_BOT_TOKEN}", "Content-Type":"application/json"}
        data = {"channel": channel, "text": text}
        requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=data, timeout=5)
