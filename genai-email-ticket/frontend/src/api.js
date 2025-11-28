export async function fetchTickets() {
  const resp = await fetch('/api/tickets'); // proxy or full URL
  return resp.json();
}

export async function fetchTicket(id) {
  const resp = await fetch(`/tickets/${id}`);
  return resp.json();
}
