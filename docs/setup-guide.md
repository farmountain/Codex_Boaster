# Setup Guide

This guide explains how to configure and run setup commands via the Terminal Runner.

## Configuration
Available runtime versions are defined by the backend. Typical options include Python 3.11+, Node 18+ and Rust 1.72. Environment variables follow KEY=value format. Saving the form also generates `.env.template.json` with empty values for easy sharing.

1. Navigate to the **Configure Environment** page in the frontend.
2. Adjust the runtime versions for Python, Node or Rust.
3. Add any required environment variables.
4. Enter your setup commands, one per line.

### Environment Variables

Configure secrets for each integration before running the agents. Common keys
include:

- `HIPCORTEX_URL` – base URL for the HipCortex memory service.
- `OPENAI_API_KEY` and optional `OPENAI_MODEL`.
- `OLLAMA_URL` and optional `OLLAMA_MODEL` for local inference.
- `STRIPE_SECRET_KEY`, `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_PRO`,
  `STRIPE_PRICE_ENTERPRISE` for billing.
- `VERCEL_TOKEN` or `FLY_API_TOKEN` for deployments.
- `SUPABASE_URL` and `SUPABASE_KEY` when storing config remotely.
- `FRONTEND_URL` and `NEXT_PUBLIC_API_BASE_URL` for the UI.
- `API_KEY` and `JWT_SECRET` for API authentication.
- `RATE_LIMIT` and `RATE_WINDOW` to throttle requests.
- `ENABLE_OTEL` set to `0` to disable OpenTelemetry exporters.
- `OTLP_TRACES_ENDPOINT`, `OTLP_METRICS_ENDPOINT` and `OTLP_LOGS_ENDPOINT`
  for sending traces/metrics to Tempo/Jaeger and logs to Loki.
- `OBJECT_STORAGE_BUCKET` and optional `OBJECT_STORAGE_ENDPOINT` for
  uploading run artifacts to external object storage.

Saving the form writes `.env` and a shareable `.env.template.json` with empty
values. A typical template looks like:

```json
{
  "API_KEY": "",
  "HIPCORTEX_URL": "",
  "OPENAI_API_KEY": "",
  "OPENAI_MODEL": "",
  "STRIPE_SECRET_KEY": "",
  "STRIPE_PRICE_STARTER": "",
  "STRIPE_PRICE_PRO": "",
  "STRIPE_PRICE_ENTERPRISE": "",
  "VERCEL_TOKEN": "",
  "FLY_API_TOKEN": "",
  "SUPABASE_URL": "",
  "SUPABASE_KEY": "",
  "FRONTEND_URL": "",
  "NEXT_PUBLIC_API_BASE_URL": "",
  "JWT_SECRET": "",
  "RATE_LIMIT": "",
  "RATE_WINDOW": "",
  "OLLAMA_URL": "",
  "OLLAMA_MODEL": ""
}
```

## Example Commands

```
npm install
pip install -r requirements.txt
pytest
```

Click **Run Setup** to execute these commands. Output is streamed to the browser and stored under `logs/runtime/` with a timestamped log file.


## Security

All Terminal Runner endpoints require a valid JWT sent in the `Authorization` header. The token payload must include a `role` field and only users with the `admin` role can execute setup commands. In addition, commands are validated against an allow list of common build tools such as `npm`, `pip`, `pytest`, `python` and `node`. Any command outside this list is rejected.
