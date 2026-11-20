# VIRALMIND AI

**AI-Powered Marketing, Branding, Creative Direction & Viral Growth Intelligence Platform**

VIRALMIND AI is an open-source, modular marketing intelligence system that combines:
- **11-Dimension Viral Potential Scoring (0–100)** with empirical SQLite calibration (no fake virality guarantees)
- **Platform Algorithm Intelligence** strictly separating verified official documentation from observed patterns and testable hypotheses
- **Trend & Competitor Radar** with structured 9-field opportunity briefs
- **AI Content Generation Studio** turning one seed idea into up to 100 multi-platform concepts, scripts, and calendars
- **Brand Builder & Creative Design Studio** with color psychology, typography, and platform-exact dimensions
- **Ethical Consumer Psychology & 7/30/90-Day Growth Roadmaps**
- **Universal AI Connectors**: FastAPI REST API, JSON-RPC 2.0 stdio MCP Server (Claude), Custom GPT Actions (ChatGPT), Gemini Function Declarations, and portable `SKILL.md` skills.

## Quick Start

```bash
cd viralmind-ai
cp .env.example .env
uvicorn server.api.app:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000` for the Agency Dashboard or `http://127.0.0.1:8000/docs` for interactive OpenAPI docs.

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

## Run MCP Server (Claude Desktop / MCP Clients)

```bash
python3 -m server.mcp.mcp_server
```
