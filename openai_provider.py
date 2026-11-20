"""OpenAI REST API provider adapter using httpx."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional
import httpx

from backend.config import settings
from server.providers.base import LLMProvider, ProviderError, ProviderResponse


class OpenAIProvider(LLMProvider):
    name = "openai"
    ENDPOINT = "https://api.openai.com/v1/chat/completions"

    def is_configured(self) -> bool:
        return bool(settings.openai_api_key.strip())

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.4,
        max_tokens: int = 1800,
    ) -> ProviderResponse:
        if not self.is_configured():
            raise ProviderError(self.name, "OPENAI_API_KEY is not configured.", retryable=False)

        payload: Dict[str, Any] = {
            "model": settings.openai_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if json_schema is not None:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
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
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        in_tok = int(usage.get("prompt_tokens", 0))
        out_tok = int(usage.get("completion_tokens", 0))
        # Approximate pricing for gpt-4o-mini ($0.15/1M in, $0.60/1M out)
        cost = (in_tok * 0.15 + out_tok * 0.60) / 1_000_000.0

        structured = None
        if json_schema is not None:
            try:
                structured = json.loads(content)
            except json.JSONDecodeError:
                structured = None

        return ProviderResponse(
            provider=self.name,
            model=settings.openai_model,
            content=content,
            structured_data=structured,
            input_tokens=in_tok,
            output_tokens=out_tok,
            estimated_cost_usd=cost,
            latency_ms=latency_ms,
        )
