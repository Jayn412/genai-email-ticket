# GenAI Email → Ticket

## Local dev
1. Copy `.env.example` to `.env` and fill secrets.
2. docker-compose up --build
3. POST emails to http://localhost:8000/webhook/email (use Postman or ngrok)
4. Open frontend dev server (if implemented) or call /tickets/{id}

## Tests
pytest
