"""Provider abstractions for prompt refinement."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class ProviderError(RuntimeError):
    """Generic error for provider failures."""


class ProviderConfigurationError(ProviderError):
    """Raised when the provider cannot be initialized."""


class BaseProvider(ABC):
    """Abstract provider interface for generating refined prompts."""

    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str) -> Dict[str, str]:
        """Return a mapping of prompt variants keyed by variant name."""
