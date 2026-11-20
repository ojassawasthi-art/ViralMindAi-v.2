"""Comprehensive unit, API, SQLite calibration, and MCP stdio integration tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from database.store import LearningStore
from server.api.app import app
from server.providers.router import ProviderRouter


class TestViralMindPlatform(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_and_dashboard(self) -> None:
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")

        dash = self.client.get("/")
        self.assertEqual(dash.status_code, 200)
        self.assertIn("What are you trying to grow?", dash.text)

    def test_onboarding_and_project_persistence(self) -> None:
        resp = self.client.post(
            "/api/v1/onboarding",
            json={
                "goal": "Grow B2B SaaS organic signups",
                "niche": "Workflow Automation",
                "target_audience": "Operations managers at 20-person agencies",
                "platforms": ["instagram_reels", "linkedin"],
                "stage": "early",
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("project_id", data)
        self.assertEqual(len(data["recommended_sequence"]), 4)

    def test_virality_scoring_11_dimensions(self) -> None:
        resp = self.client.post(
            "/api/v1/virality/score",
            json={
                "title_or_hook": "Stop wasting 6 hours a week on manual onboarding — 3 steps",
                "concept": "Case study teardown showing before and after automation framework for agencies.",
                "platform": "instagram_reels",
                "target_audience": "Agency founders",
                "niche": "Automation",
                "visual_plan": "Split-screen workflow demo with bold 3-word captions",
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["dimension_scores"]), 11)
        self.assertGreaterEqual(data["viral_potential_score"], 0)
        self.assertLessEqual(data["viral_potential_score"], 100)
        self.assertEqual(len(data["alternative_versions"]), 3)
        self.assertIn("NOT a guarantee", data["methodology_disclaimer"])

    def test_platform_intelligence_epistemic_separation(self) -> None:
        for plat in ["youtube", "instagram", "tiktok", "linkedin", "x"]:
            resp = self.client.get(f"/api/v1/platforms/{plat}")
            self.assertEqual(resp.status_code, 200)
            body = resp.json()
            self.assertTrue(len(body["verified_official_signals"]) >= 1)
            self.assertTrue(len(body["official_sources"]) >= 1)
            self.assertIn("observed_patterns", body)
            self.assertIn("testable_hypotheses", body)

    def test_trend_content_brand_design_psychology_growth(self) -> None:
        t_resp = self.client.post("/api/v1/trends/research", json={"query": "AI workflow", "niche": "SaaS"})
        self.assertEqual(t_resp.status_code, 200)
        self.assertTrue(len(t_resp.json()["opportunities"]) >= 2)

        c_resp = self.client.post(
            "/api/v1/content/generate",
            json={"idea": "Client onboarding", "niche": "Agencies", "target_audience": "Founders", "idea_count": 12},
        )
        self.assertEqual(c_resp.status_code, 200)
        self.assertEqual(c_resp.json()["total_ideas_generated"], 12)

        b_resp = self.client.post(
            "/api/v1/brand/build",
            json={"business_or_idea": "LumaFlow", "niche": "Analytics", "target_audience": "DTC brands"},
        )
        self.assertEqual(b_resp.status_code, 200)
        self.assertIn("color_palette", b_resp.json()["visual_system"])

        d_resp = self.client.post(
            "/api/v1/design/brief",
            json={"asset_type": "thumbnail", "brand_name": "LumaFlow", "topic": "Q4 ROAS Teardown"},
        )
        self.assertEqual(d_resp.status_code, 200)
        self.assertIn("image_generation_prompt", d_resp.json())

        p_resp = self.client.post(
            "/api/v1/psychology/analyze",
            json={"product_or_offer": "LumaFlow Pro", "target_audience": "DTC founders"},
        )
        self.assertEqual(p_resp.status_code, 200)
        self.assertIn("dark patterns", p_resp.json()["ethical_guardrail"].lower())

        g_resp = self.client.post(
            "/api/v1/growth/roadmap",
            json={"business_name": "LumaFlow", "niche": "Analytics", "target_audience": "DTC founders"},
        )
        self.assertEqual(g_resp.status_code, 200)
        self.assertEqual(len(g_resp.json()["sprint_7_day"]), 4)

    def test_sqlite_learning_calibration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = LearningStore(db_path=Path(tmp) / "test.db")
            for i in range(3):
                out = store.log_outcome(
                    {
                        "campaign_name": f"Test {i}",
                        "platform": "instagram_reels",
                        "content_format": "short_video",
                        "hook_used": "Stop doing X",
                        "predicted_score": 60.0,
                        "views": 10000,
                        "likes": 500,
                        "comments": 40,
                        "shares": 200,
                        "saves": 300,
                        "avg_watch_pct": 75.0,
                        "conversions": 25,
                    }
                )
                self.assertGreater(out["actual_normalized_score"], 0)
            cal = store.get_calibration_offset("instagram_reels")
            self.assertEqual(cal["sample_count"], 3)
            self.assertIsNotNone(cal["mae"])

    def test_provider_router_fallback(self) -> None:
        r = ProviderRouter()
        resp = r.generate("sys", "user", preferred_provider="openai")
        self.assertEqual(resp.provider, "local")
        self.assertEqual(r.status()["usage"]["total_calls"], 1)

    def test_mcp_stdio_server(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        requests = "\n".join(
            [
                json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
                json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "tools/call",
                        "params": {
                            "name": "score_virality",
                            "arguments": {"title_or_hook": "3 AI mistakes", "concept": "Detailed breakdown"},
                        },
                    }
                ),
            ]
        ) + "\n"

        proc = subprocess.run(
            [sys.executable, "-m", "server.mcp.mcp_server"],
            cwd=str(repo_root),
            input=requests,
            text=True,
            capture_output=True,
            timeout=15,
            check=True,
        )
        lines = [json.loads(line) for line in proc.stdout.strip().splitlines() if line.strip()]
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0]["result"]["serverInfo"]["name"], "viralmind-ai")
        self.assertEqual(len(lines[1]["result"]["tools"]), 10)
        tool_payload = json.loads(lines[2]["result"]["content"][0]["text"])
        self.assertIn("viral_potential_score", tool_payload)


if __name__ == "__main__":
    unittest.main()
