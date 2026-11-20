# Security Policy

## Secret Management
- All LLM provider keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`) and `VIRALMIND_API_TOKEN` must reside strictly on the server in `.env` or environment variables.
- The frontend (`frontend/`) never receives or stores provider API keys.
- Set `VIRALMIND_API_TOKEN` in `.env` before exposing the REST API beyond `127.0.0.1` to require `Authorization: Bearer <token>` on all `/api/v1/*` endpoints.

## Reporting a Vulnerability
Please report security issues privately to the repository maintainers rather than opening a public issue.
