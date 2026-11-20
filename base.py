"""Provider abstraction layer base classes and cost/rate-limit tracking."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ProviderResponse:
    provider: str
    model: str
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    latency_ms: float = 0.0
    used_fallback: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProviderError(Exception):
    """Raised when an AI provider fails or is rate-limited."""

    def __init__(self, provider: str, message: str, retryable: bool = True):
        super().__init__(f"[{provider}] {message}")
        self.provider = provider
        self.retryable = retryable


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if credentials/runtime are available for this provider."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.4,
        max_tokens: int = 1800,
    ) -> ProviderResponse:
        """Generate text or structured JSON from the provider."""


class CostTracker:
    """In-memory session cost and usage ledger."""

    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def record(self, resp: ProviderResponse) -> None:
        self.records.append(
            {
                "timestamp": resp.timestamp,
                "provider": resp.provider,
                "model": resp.model,
                "input_tokens": resp.input_tokens,
                "output_tokens": resp.output_tokens,
                "estimated_cost_usd": round(resp.estimated_cost_usd, 6),
                "latency_ms": round(resp.latency_ms, 2),
                "used_fallback": resp.used_fallback,
            }
        )

    def summary(self) -> Dict[str, Any]:
        total_cost = sum(r["estimated_cost_usd"] for r in self.records)
        total_in = sum(r["input_tokens"] for r in self.records)
        total_out = sum(r["output_tokens"] for r in self.records)
        return {
            "total_calls": len(self.records),
            "total_input_tokens": total_in,
            "total_output_tokens": total_out,
            "total_estimated_cost_usd": round(total_cost, 6),
            "recent_calls": self.records[-20:],
        }
