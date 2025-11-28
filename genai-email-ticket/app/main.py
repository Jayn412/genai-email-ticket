from fastapi import FastAPI, Request, HTTPException, Depends
from .email_parser import parse_webhook
from .tasks import process_email_sync
from .db import init_db, SessionLocal, Ticket
from .config import settings
from pydantic import BaseModel
from .models import TicketRecordOut

app = FastAPI(title="GenAI Email → Ticket")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/webhook/email")
async def email_webhook(request: Request):
    # Support both form and JSON payloads
    content_type = request.headers.get("content-type","")
    payload = {}
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        payload = dict(form)
    else:
        payload = await request.json()
    try:
        email = parse_webhook(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse email: {e}")
    try:
        res = process_email_sync(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status":"ok", **res}

@app.get("/tickets/{id}", response_model=TicketRecordOut)
def get_ticket(id: int):
    db = SessionLocal()
    t = db.query(Ticket).filter(Ticket.id==id).first()
    db.close()
    if not t:
        raise HTTPException(status_code=404, detail="not found")
    return {
        "id": t.id,
        "ticket_id": t.ticket_id,
        "email_from": t.email_from,
        "subject": t.subject,
        "llm_summary": t.llm_summary,
        "created_at": t.created_at
    }

@app.get("/health")
def health():
    return {"status":"ok"}
