# AWS Deployment Guide (ECS / Fargate) - quick steps

1. Build container image and push to ECR:
   - `aws ecr create-repository --repository-name genai-email-ticket`
   - `docker build -t genai-email-ticket .`
   - Tag & push to ECR.

2. Create ECS cluster (Fargate), define TaskDefinition using the image, set environment variables (OPENAI_API_KEY, etc.) in TaskDefinition secrets (use AWS Secrets Manager / Parameter Store).

3. Configure Service with desired count, attach to Application Load Balancer (ALB) with health check `/health`.

4. Use RDS (Postgres) for production DB; set DATABASE_URL accordingly.

5. For background processing use AWS SQS + Lambda or ECS Service with Celery workers (Redis on Elasticache).

6. Use CloudWatch for logs and metrics; set alarms for LLM latency and ticket failure rates.

(Refer to project README for local dev steps.)
