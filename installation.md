# Installation & Setup

## Requirements
- Python 3.11+
- `fastapi`, `uvicorn`, `pydantic`, `httpx`

## Steps
1. Clone or enter `viralmind-ai/`:
   ```bash
   cd viralmind-ai
   ```
2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Optional: add `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` and set `VIRALMIND_DEFAULT_PROVIDER`.
   By default, `VIRALMIND_DEFAULT_PROVIDER=local` runs 100% locally with zero external API keys.
3. Start the API & Dashboard:
   ```bash
   uvicorn server.api.app:app --host 127.0.0.1 --port 8000
   ```
4. Verify health:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
