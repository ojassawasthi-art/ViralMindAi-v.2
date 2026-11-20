"""SQLite persistence for projects, campaign outcomes, and self-improving calibration."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.config import settings


class LearningStore:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = Path(db_path or settings.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    niche TEXT NOT NULL,
                    target_audience TEXT NOT NULL,
                    platforms_json TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    brief_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS campaign_outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    campaign_name TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    content_format TEXT NOT NULL,
                    hook_used TEXT NOT NULL,
                    predicted_score REAL NOT NULL,
                    actual_normalized_score REAL NOT NULL,
                    views INTEGER NOT NULL,
                    likes INTEGER NOT NULL,
                    comments INTEGER NOT NULL,
                    shares INTEGER NOT NULL,
                    saves INTEGER NOT NULL,
                    avg_watch_pct REAL NOT NULL,
                    conversions INTEGER NOT NULL,
                    audience_feedback TEXT NOT NULL,
                    what_worked TEXT NOT NULL,
                    what_failed TEXT NOT NULL
                );
                """
            )

    def save_project(
        self,
        goal: str,
        niche: str,
        target_audience: str,
        platforms: List[str],
        stage: str,
        brief: Dict[str, Any],
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO projects (created_at, goal, niche, target_audience, platforms_json, stage, brief_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (now, goal, niche, target_audience, json.dumps(platforms), stage, json.dumps(brief)),
            )
            return int(cur.lastrowid)

    def list_projects(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [
            {
                "id": r["id"],
                "created_at": r["created_at"],
                "goal": r["goal"],
                "niche": r["niche"],
                "target_audience": r["target_audience"],
                "platforms": json.loads(r["platforms_json"]),
                "stage": r["stage"],
                "brief": json.loads(r["brief_json"]),
            }
            for r in rows
        ]

    @staticmethod
    def compute_actual_score(
        views: int,
        likes: int,
        comments: int,
        shares: int,
        saves: int,
        avg_watch_pct: float,
        conversions: int,
    ) -> float:
        """Normalize real campaign metrics to a 0-100 empirical performance index."""
        if views <= 0:
            return 0.0
        eng_rate = (likes + comments * 2 + shares * 4 + saves * 3) / views
        eng_component = min(40.0, eng_rate * 400.0)  # 10% weighted engagement -> 40 pts
        watch_component = min(35.0, (avg_watch_pct / 100.0) * 35.0)
        share_rate = (shares + saves) / views
        virality_component = min(15.0, share_rate * 500.0)
        conv_component = min(10.0, (conversions / views) * 500.0)
        return round(min(100.0, eng_component + watch_component + virality_component + conv_component), 2)

    def log_outcome(self, data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        actual_score = self.compute_actual_score(
            views=data["views"],
            likes=data["likes"],
            comments=data["comments"],
            shares=data["shares"],
            saves=data["saves"],
            avg_watch_pct=data["avg_watch_pct"],
            conversions=data["conversions"],
        )
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO campaign_outcomes (
                    created_at, campaign_name, platform, content_format, hook_used,
                    predicted_score, actual_normalized_score, views, likes, comments,
                    shares, saves, avg_watch_pct, conversions, audience_feedback,
                    what_worked, what_failed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    data["campaign_name"],
                    data["platform"],
                    data["content_format"],
                    data["hook_used"],
                    data["predicted_score"],
                    actual_score,
                    data["views"],
                    data["likes"],
                    data["comments"],
                    data["shares"],
                    data["saves"],
                    data["avg_watch_pct"],
                    data["conversions"],
                    data.get("audience_feedback", ""),
                    data.get("what_worked", ""),
                    data.get("what_failed", ""),
                ),
            )
            row_id = int(cur.lastrowid)
        return {
            "id": row_id,
            "campaign_name": data["campaign_name"],
            "predicted_score": data["predicted_score"],
            "actual_normalized_score": actual_score,
            "prediction_error": round(actual_score - data["predicted_score"], 2),
        }

    def get_calibration_offset(self, platform: Optional[str] = None) -> Dict[str, Any]:
        with self._connect() as conn:
            if platform:
                rows = conn.execute(
                    "SELECT predicted_score, actual_normalized_score FROM campaign_outcomes WHERE platform = ?",
                    (platform,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT predicted_score, actual_normalized_score FROM campaign_outcomes"
                ).fetchall()
        if not rows:
            return {"sample_count": 0, "mean_bias": 0.0, "mae": None}
        diffs = [r["actual_normalized_score"] - r["predicted_score"] for r in rows]
        mae = sum(abs(d) for d in diffs) / len(diffs)
        mean_bias = sum(diffs) / len(diffs)
        return {
            "sample_count": len(rows),
            "mean_bias": round(mean_bias, 2),
            "mae": round(mae, 2),
        }

    def search_experiments(self, query: str = "", platform: str = "") -> Dict[str, Any]:
        with self._connect() as conn:
            sql = "SELECT * FROM campaign_outcomes WHERE 1=1"
            params: List[Any] = []
            if platform:
                sql += " AND platform = ?"
                params.append(platform)
            if query:
                like = f"%{query}%"
                sql += " AND (campaign_name LIKE ? OR hook_used LIKE ? OR what_worked LIKE ? OR what_failed LIKE ?)"
                params.extend([like, like, like, like])
            sql += " ORDER BY actual_normalized_score DESC, id DESC LIMIT 50"
            rows = conn.execute(sql, params).fetchall()

        records = [dict(r) for r in rows]
        top_formats: Dict[str, List[float]] = {}
        for r in records:
            top_formats.setdefault(r["content_format"], []).append(r["actual_normalized_score"])
        format_benchmarks = [
            {
                "content_format": fmt,
                "campaigns": len(scores),
                "avg_actual_score": round(sum(scores) / len(scores), 2),
            }
            for fmt, scores in sorted(top_formats.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
        ]

        return {
            "total_experiments": len(records),
            "calibration": self.get_calibration_offset(platform or None),
            "format_benchmarks": format_benchmarks,
            "experiments": records,
        }


learning_store = LearningStore()
