"""Google Gemini REST API provider adapter using httpx."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional
import httpx

from backend.config import settings
from server.providers.base import LLMProvider, ProviderError, ProviderResponse


class GeminiProvider(LLMProvider):
    name = "gemini"

    def is_configured(self) -> bool:
        return bool(settings.gemini_api_key.strip())

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.4,
        max_tokens: int = 1800,
    ) -> ProviderResponse:
        if not self.is_configured():
            raise ProviderError(self.name, "GEMINI_API_KEY is not configured.", retryable=False)

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
        )
        gen_cfg: Dict[str, Any] = {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        }
        if json_schema is not None:
            gen_cfg["responseMimeType"] = "application/json"

        payload: Dict[str, Any] = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": gen_cfg,
        }

        t0 = time.perf_counter()
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(url, json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(self.name, f"Network error: {exc}", retryable=True) from exc

        latency_ms = (time.perf_counter() - t0) * 1000.0
        if resp.status_code == 429:
            raise ProviderError(self.name, "Rate limit exceeded (429).", retryable=True)
        if resp.status_code >= 400:
            raise ProviderError(self.name, f"HTTP {resp.status_code}: {resp.text[:300]}", retryable=resp.status_code >= 500)

        data = resp.json()
        candidates = data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        content = "".join(p.get("text", "") for p in parts)
        usage = data.get("usageMetadata", {})
        in_tok = int(usage.get("promptTokenCount", 0))
        out_tok = int(usage.get("candidatesTokenCount", 0))
        cost = (in_tok * 0.15 + out_tok * 0.60) / 1_000_000.0

        structured = None
        if json_schema is not None:
            try:
                structured = json.loads(content)
            except json.JSONDecodeError:
                structured = None

        return ProviderResponse(
            provider=self.name,
            model=settings.gemini_model,
            content=content,
            structured_data=structured,
            input_tokens=in_tok,
            output_tokens=out_tok,
            estimated_cost_usd=cost,
            latency_ms=latency_ms,
        )
