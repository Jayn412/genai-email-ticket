# Simple background runner wrapper (sync for demo).
# In prod switch to Celery/RQ and push call_llm/create_ticket to background.
from .llm_client import call_llm_for_summary
from .ticketing import create_ticket
from .db import SessionLocal, Ticket

def process_email_sync(email):
    llm_res = call_llm_for_summary(email.subject, email.body_text)
    ticket_payload = {
        "category": llm_res.get("category"),
        "priority": llm_res.get("priority"),
        "assignee_role": llm_res.get("assignee_role"),
        "actions": llm_res.get("actions")
    }
    try:
        ticket_resp = create_ticket(title=email.subject, description=llm_res.get("summary"), metadata=ticket_payload)
        ticket_id = ticket_resp.get("id") or ticket_resp.get("ticket_id") or str(ticket_resp)
    except Exception as e:
        ticket_id = None
    # persist
    db = SessionLocal()
    t = Ticket(email_from=email.from_address, subject=email.subject, body=email.body_text, llm_summary=llm_res, ticket_id=str(ticket_id))
    db.add(t); db.commit(); db.refresh(t); db.close()
    return {"ticket_id": ticket_id, "id": t.id, "summary": llm_res}
