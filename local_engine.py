"""Deterministic local intelligence provider (zero-dependency fallback)."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from server.providers.base import LLMProvider, ProviderResponse


class LocalProvider(LLMProvider):
    name = "local"

    def is_configured(self) -> bool:
        return True

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.4,
        max_tokens: int = 1800,
    ) -> ProviderResponse:
        t0 = time.perf_counter()
        summary = (
            "Local deterministic engine active. External LLM synthesis is optional; "
            "configure OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY in .env to enable "
            "cloud LLM enrichment."
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return ProviderResponse(
            provider=self.name,
            model="viralmind-deterministic-v1",
            content=summary,
            structured_data={"mode": "local_deterministic", "note": summary},
            input_tokens=max(1, len(user_prompt) // 4),
            output_tokens=max(1, len(summary) // 4),
            estimated_cost_usd=0.0,
            latency_ms=latency_ms,
        )
