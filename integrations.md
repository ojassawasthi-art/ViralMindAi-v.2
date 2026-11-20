# Cross-Platform AI Integrations

## 1. Claude Desktop & MCP Clients
Copy `integrations/claude/claude_desktop_config.json` into your Claude Desktop configuration, replacing `/ABSOLUTE/PATH/TO/viralmind-ai` with your local path. The stdio MCP server exposes all 10 ViralMind tools via JSON-RPC 2.0.

## 2. ChatGPT Custom GPT Actions
Deploy the FastAPI server behind HTTPS and import `integrations/chatgpt/openapi_actions.json` into your Custom GPT Actions configuration.

## 3. Google Gemini Function Calling
Use `integrations/gemini/gemini_tools.json` as your `function_declarations` payload when integrating with the Gemini API, routing tool calls to `server/api/app.py` or `backend/engines/*`.

## 4. Portable Skills (`skills/`)
Each directory in `skills/` contains a standalone `SKILL.md` with YAML frontmatter (`viralmind-core`, `viral-research`, `content-strategy`, `brand-strategy`, `creative-director`, `growth-marketing`).
