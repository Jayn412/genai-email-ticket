from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EmailIn(BaseModel):
    from_address: str
    to_address: str
    subject: str
    body_text: str
    html: Optional[str] = None
    attachments: Optional[List[str]] = []

class LLMResult(BaseModel):
    summary: str
    actions: List[str] = []
    category: str = "other"
    priority: str = "P3"
    assignee_role: str = "Support"

class TicketRecordOut(BaseModel):
    id: int
    ticket_id: Optional[str]
    email_from: str
    subject: str
    llm_summary: LLMResult
    created_at: datetime
