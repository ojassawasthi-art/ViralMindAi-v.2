"""Anthropic Messages REST API provider adapter using httpx."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional
import httpx

from backend.config import settings
from server.providers.base import LLMProvider, ProviderError, ProviderResponse


class AnthropicProvider(LLMProvider):
    name = "anthropic"
    ENDPOINT = "https://api.anthropic.com/v1/messages"

    def is_configured(self) -> bool:
        return bool(settings.anthropic_api_key.strip())

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.4,
        max_tokens: int = 1800,
    ) -> ProviderResponse:
        if not self.is_configured():
            raise ProviderError(self.name, "ANTHROPIC_API_KEY is not configured.", retryable=False)

        prompt = user_prompt
        if json_schema is not None:
            prompt += "\n\nReturn valid JSON only matching the requested structure."

        payload: Dict[str, Any] = {
            "model": settings.anthropic_model,
            "system": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": settings.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        t0 = time.perf_counter()
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(self.ENDPOINT, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(self.name, f"Network error: {exc}", retryable=True) from exc

        latency_ms = (time.perf_counter() - t0) * 1000.0
        if resp.status_code == 429:
            raise ProviderError(self.name, "Rate limit exceeded (429).", retryable=True)
        if resp.status_code >= 400:
            raise ProviderError(self.name, f"HTTP {resp.status_code}: {resp.text[:300]}", retryable=resp.status_code >= 500)

        data = resp.json()
        blocks = data.get("content", [])
        content = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        usage = data.get("usage", {})
        in_tok = int(usage.get("input_tokens", 0))
        out_tok = int(usage.get("output_tokens", 0))
        # Approximate pricing ($3/1M in, $15/1M out)
        cost = (in_tok * 3.0 + out_tok * 15.0) / 1_000_000.0

        structured = None
        if json_schema is not None:
            try:
                structured = json.loads(content)
            except json.JSONDecodeError:
                structured = None

        return ProviderResponse(
            provider=self.name,
            model=settings.anthropic_model,
            content=content,
            structured_data=structured,
            input_tokens=in_tok,
            output_tokens=out_tok,
            estimated_cost_usd=cost,
            latency_ms=latency_ms,
        )
