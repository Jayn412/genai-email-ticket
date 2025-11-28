# GCP Deployment Guide (Cloud Run) - quick steps

1. `gcloud builds submit --tag gcr.io/$PROJECT_ID/genai-email-ticket`
2. `gcloud run deploy genai-email-ticket --image gcr.io/$PROJECT_ID/genai-email-ticket --platform managed --region us-central1 --allow-unauthenticated --set-env-vars "OPENAI_API_KEY=...,DATABASE_URL=..."`
3. Use Cloud SQL (Postgres) with Private IP and configure `DATABASE_URL`.
4. Use Cloud Tasks or Cloud Run jobs for background work instead of Celery.
5. Use Cloud Monitoring for metrics and alerts.
