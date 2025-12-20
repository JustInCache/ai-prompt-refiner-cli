"""OpenAI provider implementation for prompt refinement."""

from __future__ import annotations

import json
import logging
import os
from typing import Dict

try:  # pragma: no cover - optional dependency guard
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled in provider init
    OpenAI = None  # type: ignore[assignment]

from .base import BaseProvider, ProviderConfigurationError, ProviderError
from ..utils import default_variant_order

LOGGER = logging.getLogger(__name__)

SYSTEM_MESSAGE = (
    "You are an elite prompt engineer. Transform raw user prompts into five "
    "enhanced variants: improved (polished), power (detailed), short (<20 words), "
    "long (story-like), and creative twist. Respond ONLY with JSON following the "
    "provided schema."
)


class OpenAIProvider(BaseProvider):
    """Generate refinements using OpenAI's Responses API."""

    name = "openai"

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        if OpenAI is None:
            raise ProviderConfigurationError(
                "The 'openai' package is not installed. Install promptrefiner with the full dependencies."
            )

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderConfigurationError(
                "OpenAI provider requires the OPENAI_API_KEY environment variable."
            )

        self.model = model
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as exc:  # pragma: no cover - defensive
            raise ProviderConfigurationError(
                "Failed to initialize OpenAI client."
            ) from exc

    def generate(self, prompt: str) -> Dict[str, str]:
        """Send the prompt to OpenAI and parse the refined variants."""

        schema = {
            "type": "object",
            "properties": {
                "improved": {"type": "string"},
                "power": {"type": "string"},
                "short": {"type": "string"},
                "long": {"type": "string"},
                "creative": {"type": "string"},
            },
            "required": default_variant_order(),
            "additionalProperties": False,
        }

        schema_instruction = json.dumps(schema, indent=2)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {
                        "role": "user",
                        "content": (
                            "Refine this prompt:\n"
                            f"'''{prompt.strip()}'''\n\n"
                            "Respond ONLY with JSON that matches this schema:\n"
                            f"{schema_instruction}"
                        ),
                    },
                ],
            )
        except Exception as exc:  # pragma: no cover - network dependent
            raise ProviderError(f"OpenAI request failed: {exc}") from exc

        payload = self._extract_payload(response)
        return {key: payload.get(key, "").strip() for key in default_variant_order()}

    @staticmethod
    def _extract_payload(response: object) -> Dict[str, str]:
        """Extract and decode the JSON payload from an OpenAI response."""

        try:
            content = response.output[0].content[0].text  # type: ignore[attr-defined]
        except (AttributeError, IndexError) as exc:  # pragma: no cover - defensive
            raise ProviderError("Unexpected response shape from OpenAI.") from exc

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            LOGGER.debug("Raw provider payload: %s", content)
            raise ProviderError("Failed to parse OpenAI response JSON.") from exc
