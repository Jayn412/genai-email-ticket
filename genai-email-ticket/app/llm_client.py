import os, json, re
from .config import settings
import requests

def build_prompt(subject: str, body: str) -> str:
    return f"""
You are a support triage assistant. Parse the email and return a JSON with keys:
- summary: one-sentence summary
- actions: list of up to 5 action items
- category: one of [bug, billing, feature, account, other]
- priority: one of [P0,P1,P2,P3]
- assignee_role: one of [SRE, Billing, Product, Support]

Email Subject: {subject}
Email Body:
{body}
Return only a JSON object.
"""

def call_llm_for_summary(email_subject: str, email_body: str) -> dict:
    prompt = build_prompt(email_subject, email_body)
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role":"system","content":"You are a helpful support summarizer."},
            {"role":"user","content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 500
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
    resp.raise_for_status()
    out = resp.json()
    text = out["choices"][0]["message"]["content"]
    # Try to extract JSON object
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    # fallback: best-effort
    return {"summary": text.strip(), "actions": [], "category":"other", "priority":"P3", "assignee_role":"Support"}
