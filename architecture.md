# Architecture Overview

VIRALMIND AI is structured into five decoupled layers:

1. **Intelligence Engines (`backend/engines/`)**:
   - `viral_scoring.py`: 11-dimension weighted rubric + SQLite calibration offset.
   - `platform_intelligence.py`: Verified official platform signals vs. observed patterns & hypotheses.
   - `trend_research.py`: 9-field opportunity briefs with optional live public API enrichment.
   - `content_studio.py`: 1–100 concept generator with 12 required fields per idea.
   - `branding_agency.py`: Brand positioning, naming, color psychology, typography, and design briefs.
   - `psychology_growth.py`: Ethical behavioral economics, generational fusion, 7/30/90-day roadmaps, and guided onboarding.
2. **Self-Improving Store (`database/store.py`)**:
   - SQLite database (`viralmind.db`) tracking projects, predicted vs. normalized actual campaign scores, MAE, and format benchmarks.
3. **Provider Abstraction (`server/providers/`)**:
   - `ProviderRouter` supporting `local` (zero-dependency deterministic fallback), `openai`, `anthropic`, and `gemini` with automatic fallback and session cost tracking.
4. **Interfaces (`server/api/` & `server/mcp/`)**:
   - FastAPI REST API + static Agency Dashboard (`frontend/`).
   - JSON-RPC 2.0 stdio MCP server exposing 10 tools.
5. **Cross-Platform Skills & Adapters (`skills/`, `integrations/`)**:
   - Portable `SKILL.md` skills and schemas for Claude, ChatGPT Custom GPTs, and Google Gemini.
