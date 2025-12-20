"""Core orchestration logic for the Prompt Refiner CLI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence

from .providers.base import BaseProvider, ProviderError
from .utils import default_variant_order


@dataclass
class RefinementResult:
    """Structured response for refined prompts."""

    prompt: str
    variants: Dict[str, str]

    def ordered_pairs(self, order: Sequence[str] | None = None) -> list[tuple[str, str]]:
        """Return ordered variant pairs respecting the requested order."""

        order = list(order or default_variant_order())
        pairs = []
        for key in order:
            value = self.variants.get(key)
            if not value:
                continue
            pairs.append((key, value))
        return pairs


class PromptRefiner:
    """High-level interface for refining prompts through a provider."""

    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def refine(
        self, prompt: str, modes: Iterable[str] | None = None
    ) -> RefinementResult:
        """Refine a prompt and return the requested variants."""

        normalized = (prompt or "").strip()
        if not normalized:
            raise ValueError("Prompt cannot be empty.")

        raw = self.provider.generate(normalized)
        if not isinstance(raw, Mapping):
            raise ProviderError("Provider returned an invalid response payload.")

        requested = list(modes or default_variant_order())
        variants = {}
        for key in requested:
            value = raw.get(key)
            if not value:
                continue
            variants[key] = value.strip()

        return RefinementResult(prompt=normalized, variants=variants)
