# API Reference

Base URL: `http://127.0.0.1:8000` (interactive Swagger UI at `/docs`).
If `VIRALMIND_API_TOKEN` is set, include header `Authorization: Bearer <token>`.

## Endpoints
- `GET /health` — Server health & active provider.
- `POST /api/v1/onboarding` — Guided "What are you trying to grow?" intake & project persistence.
- `GET /api/v1/projects` — List saved growth projects.
- `POST /api/v1/virality/score` — 11-dimension Viral Potential Score (0–100).
- `GET /api/v1/platforms` — List supported platforms.
- `GET /api/v1/platforms/{platform}` — Verified ranking signals, observed patterns, and hypotheses.
- `POST /api/v1/trends/research` — 9-field trend & competitor gap analysis.
- `POST /api/v1/content/generate` — Generate 1–100 content concepts + 7-day calendar.
- `POST /api/v1/brand/build` — Brand positioning, naming, color psychology & typography.
- `POST /api/v1/design/brief` — Creative brief with dimensions & image-gen prompt.
- `POST /api/v1/psychology/analyze` — Ethical consumer psychology & generational fusion.
- `POST /api/v1/growth/roadmap` — 7-day sprint, 30-day plan, 90-day roadmap.
- `POST /api/v1/analytics/outcomes` — Log actual campaign metrics for calibration.
- `GET /api/v1/analytics/insights` — Query experiment knowledge base & MAE calibration.
- `GET /api/v1/providers/status` — Provider configuration & session cost tracker.
- `POST /api/v1/providers/configure` — Switch default or fallback providers.
