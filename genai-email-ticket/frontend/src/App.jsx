import React, {useEffect, useState} from "react";
import { fetchTicket } from "./api";

export default function App(){
  const [id, setId] = useState("");
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);

  async function load(){
    setLoading(true);
    try {
      const t = await fetch(`/tickets/${id}`);
      const data = await t.json();
      setTicket(data);
    } catch(e){
      alert("Error fetching ticket");
    } finally { setLoading(false) }
  }

  return (
    <div style={{padding:24,fontFamily:"sans-serif"}}>
      <h2>GenAI Email → Ticket — Admin</h2>
      <div style={{marginBottom:12}}>
        <input placeholder="Ticket DB id" value={id} onChange={e=>setId(e.target.value)} />
        <button onClick={load} disabled={!id || loading}>Fetch</button>
      </div>
      {ticket && (
        <div>
          <h3>{ticket.subject}</h3>
          <p><b>From:</b> {ticket.email_from}</p>
          <p><b>Summary:</b> {ticket.llm_summary.summary}</p>
          <div>
            <b>Actions:</b>
            <ul>{ticket.llm_summary.actions.map((a,i)=><li key={i}>{a}</li>)}</ul>
          </div>
          <p><b>Category:</b> {ticket.llm_summary.category}</p>
          <p><b>Priority:</b> {ticket.llm_summary.priority}</p>
        </div>
      )}
    </div>
  );
}
