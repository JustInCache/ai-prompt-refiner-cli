"""Tests for core refinement logic."""

from __future__ import annotations

import pytest

from promptrefiner.core import PromptRefiner
from promptrefiner.providers.base import BaseProvider, ProviderError


class FakeProvider(BaseProvider):
    """Simple provider returning canned responses for testing."""

    def generate(self, prompt: str):
        return {
            "improved": f"Improved::{prompt}",
            "power": f"Power::{prompt}",
            "short": "Short version",
            "long": "Long version",
            "creative": "Creative twist",
        }


class BadProvider(BaseProvider):
    """Provider that returns an invalid payload."""

    def generate(self, prompt: str):
        return "not-a-mapping"  # type: ignore[return-value]


def test_refiner_filters_requested_modes():
    provider = FakeProvider()
    refiner = PromptRefiner(provider)

    result = refiner.refine("Build a spaceship", modes=["short", "creative"])

    assert list(result.variants.keys()) == ["short", "creative"]
    assert result.variants["short"] == "Short version"


def test_refiner_rejects_blank_prompts():
    provider = FakeProvider()
    refiner = PromptRefiner(provider)

    with pytest.raises(ValueError):
        refiner.refine("   ")


def test_refiner_validates_provider_payload():
    provider = BadProvider()
    refiner = PromptRefiner(provider)

    with pytest.raises(ProviderError):
        refiner.refine("hello world")
