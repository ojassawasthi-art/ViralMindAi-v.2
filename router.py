"""Provider router with fallback chain, retry, and cost tracking."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.config import settings
from server.providers.anthropic_provider import AnthropicProvider
from server.providers.base import CostTracker, LLMProvider, ProviderError, ProviderResponse
from server.providers.gemini_provider import GeminiProvider
from server.providers.local_engine import LocalProvider
from server.providers.openai_provider import OpenAIProvider


class ProviderRouter:
    def __init__(self) -> None:
        self.providers: Dict[str, LLMProvider] = {
            "local": LocalProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "gemini": GeminiProvider(),
        }
        self.default_provider = settings.default_provider
        self.fallback_providers = list(settings.fallback_providers)
        self.cost_tracker = CostTracker()

    def status(self) -> Dict[str, Any]:
        return {
            "default_provider": self.default_provider,
            "fallback_providers": self.fallback_providers,
            "available": {
                name: {"configured": prov.is_configured()}
                for name, prov in self.providers.items()
            },
            "usage": self.cost_tracker.summary(),
        }

    def configure(
        self,
        default_provider: Optional[str] = None,
        fallback_providers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        if default_provider and default_provider in self.providers:
            self.default_provider = default_provider
        if fallback_providers is not None:
            self.fallback_providers = [p for p in fallback_providers if p in self.providers]
        return self.status()

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        preferred_provider: Optional[str] = None,
    ) -> ProviderResponse:
        order: List[str] = []
        primary = preferred_provider or self.default_provider
        for candidate in [primary, *self.fallback_providers, "local"]:
            if candidate in self.providers and candidate not in order:
                order.append(candidate)

        last_err: Optional[Exception] = None
        for idx, name in enumerate(order):
            prov = self.providers[name]
            if not prov.is_configured():
                continue
            try:
                resp = prov.generate(system_prompt, user_prompt, json_schema=json_schema)
                resp.used_fallback = idx > 0
                self.cost_tracker.record(resp)
                return resp
            except ProviderError as exc:
                last_err = exc
                continue

        # Guaranteed local fallback
        resp = self.providers["local"].generate(system_prompt, user_prompt, json_schema=json_schema)
        resp.used_fallback = True
        self.cost_tracker.record(resp)
        return resp


router = ProviderRouter()
