"""JSON-RPC 2.0 over stdio Model Context Protocol (MCP) server for VIRALMIND AI.

Implements the MCP stdio transport specification:
- Reads newline-delimited JSON-RPC 2.0 messages from stdin
- Writes newline-delimited JSON-RPC 2.0 responses to stdout
- Logs diagnostics strictly to stderr
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict, List

from backend.engines.branding_agency import build_brand_identity, generate_design_brief
from backend.engines.content_studio import generate_content_campaign
from backend.engines.platform_intelligence import analyze_platform
from backend.engines.psychology_growth import analyze_consumer_psychology, build_growth_roadmap
from backend.engines.trend_research import research_trends
from backend.engines.viral_scoring import score_virality
from backend.schemas import (
    BrandBuildRequest,
    CampaignOutcomeRequest,
    ContentCampaignRequest,
    DesignBriefRequest,
    GrowthRoadmapRequest,
    PsychologyRequest,
    TrendResearchRequest,
    ViralityScoreRequest,
)
from database.store import learning_store


SERVER_INFO = {"name": "viralmind-ai", "version": "1.0.0"}
PROTOCOL_VERSION = "2025-03-26"


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "score_virality",
        "description": "Evaluate a content hook and concept across 11 viral potential dimensions (0-100) with strengths, weaknesses, and 3 alternative hooks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title_or_hook": {"type": "string"},
                "concept": {"type": "string"},
                "platform": {"type": "string", "default": "instagram_reels"},
                "target_audience": {"type": "string", "default": "general"},
                "niche": {"type": "string", "default": "general"},
            },
            "required": ["title_or_hook", "concept"],
        },
    },
    {
        "name": "research_trends",
        "description": "Discover emerging trends, audience complaints, and competitor gaps for a niche or keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "niche": {"type": "string", "default": "general"},
                "audience": {"type": "string", "default": "general"},
                "include_live_web": {"type": "boolean", "default": False},
            },
            "required": ["query"],
        },
    },
    {
        "name": "analyze_platform_algorithm",
        "description": "Retrieve verified official platform ranking signals, observed patterns, and testable hypotheses.",
        "inputSchema": {
            "type": "object",
            "properties": {"platform": {"type": "string"}},
            "required": ["platform"],
        },
    },
    {
        "name": "generate_content_campaign",
        "description": "Turn one idea into 1-100 multi-platform content concepts with scripts, visual direction, captions, CTAs, and KPIs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "idea": {"type": "string"},
                "niche": {"type": "string"},
                "target_audience": {"type": "string"},
                "idea_count": {"type": "integer", "default": 5},
            },
            "required": ["idea", "niche", "target_audience"],
        },
    },
    {
        "name": "build_brand_identity",
        "description": "Build brand positioning, naming, USP, personality, color psychology palette, and typography.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "business_or_idea": {"type": "string"},
                "niche": {"type": "string"},
                "target_audience": {"type": "string"},
                "price_positioning": {"type": "string", "default": "mid_premium"},
            },
            "required": ["business_or_idea", "niche", "target_audience"],
        },
    },
    {
        "name": "generate_design_brief",
        "description": "Produce a creative design brief with layout, hierarchy, platform dimensions, and image-gen prompt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_type": {"type": "string"},
                "brand_name": {"type": "string"},
                "topic": {"type": "string"},
                "platform": {"type": "string", "default": "instagram_reels"},
            },
            "required": ["asset_type", "brand_name", "topic"],
        },
    },
    {
        "name": "analyze_consumer_psychology",
        "description": "Apply ethical behavioral economics and generational fusion strategy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_or_offer": {"type": "string"},
                "target_audience": {"type": "string"},
                "main_objection": {"type": "string", "default": "trust_and_roi"},
            },
            "required": ["product_or_offer", "target_audience"],
        },
    },
    {
        "name": "build_growth_roadmap",
        "description": "Generate a 7-day sprint, 30-day plan, and 90-day growth roadmap.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "business_name": {"type": "string"},
                "niche": {"type": "string"},
                "target_audience": {"type": "string"},
            },
            "required": ["business_name", "niche", "target_audience"],
        },
    },
    {
        "name": "log_campaign_outcome",
        "description": "Log real campaign metrics to calibrate future Viral Potential Scores.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "campaign_name": {"type": "string"},
                "platform": {"type": "string"},
                "content_format": {"type": "string"},
                "hook_used": {"type": "string"},
                "predicted_score": {"type": "number"},
                "views": {"type": "integer"},
                "likes": {"type": "integer", "default": 0},
                "comments": {"type": "integer", "default": 0},
                "shares": {"type": "integer", "default": 0},
                "saves": {"type": "integer", "default": 0},
                "avg_watch_pct": {"type": "number", "default": 0},
                "conversions": {"type": "integer", "default": 0},
            },
            "required": ["campaign_name", "platform", "content_format", "hook_used", "predicted_score", "views"],
        },
    },
    {
        "name": "get_learning_insights",
        "description": "Query past logged campaign experiments and calibration accuracy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "default": ""},
                "platform": {"type": "string", "default": ""},
            },
        },
    },
]


DISPATCH: Dict[str, Callable[[Dict[str, Any]], Any]] = {
    "score_virality": lambda a: score_virality(ViralityScoreRequest(**a)).model_dump(),
    "research_trends": lambda a: research_trends(TrendResearchRequest(**a)),
    "analyze_platform_algorithm": lambda a: analyze_platform(a["platform"]),
    "generate_content_campaign": lambda a: generate_content_campaign(ContentCampaignRequest(**a)),
    "build_brand_identity": lambda a: build_brand_identity(BrandBuildRequest(**a)),
    "generate_design_brief": lambda a: generate_design_brief(DesignBriefRequest(**a)),
    "analyze_consumer_psychology": lambda a: analyze_consumer_psychology(PsychologyRequest(**a)),
    "build_growth_roadmap": lambda a: build_growth_roadmap(GrowthRoadmapRequest(**a)),
    "log_campaign_outcome": lambda a: learning_store.log_outcome(CampaignOutcomeRequest(**a).model_dump()),
    "get_learning_insights": lambda a: learning_store.search_experiments(
        query=a.get("query", ""), platform=a.get("platform", "")
    ),
}


def handle_message(msg: Dict[str, Any]) -> Dict[str, Any] | None:
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "notifications/initialized" or msg_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        }

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments") or {}
        if tool_name not in DISPATCH:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        try:
            output = DISPATCH[tool_name](args)
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(output, indent=2)}],
                    "isError": False,
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": f"Tool error: {exc}"}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    print("VIRALMIND AI MCP Server started (stdio)", file=sys.stderr, flush=True)
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()
            continue

        resp = handle_message(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
