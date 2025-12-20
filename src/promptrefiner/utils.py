"""Utility helpers for the Prompt Refiner CLI."""

from __future__ import annotations

import logging
import sys
from typing import Dict, Iterable, List, Sequence

from rich.prompt import Prompt

VARIANT_LABELS: Dict[str, str] = {
    "improved": "Improved Prompt",
    "power": "Power Prompt",
    "short": "Short Prompt",
    "long": "Long Form Prompt",
    "creative": "Creative Twist",
}


def default_variant_order() -> List[str]:
    """Return the default order of prompt variants."""

    return list(VARIANT_LABELS.keys())


def select_variants(flags: Sequence[str] | None) -> List[str]:
    """Resolve which variants should be displayed based on user flags."""

    if not flags:
        return default_variant_order()

    seen = []
    for flag in flags:
        if flag not in VARIANT_LABELS:
            raise KeyError(f"Unknown variant flag '{flag}'")
        if flag not in seen:
            seen.append(flag)
    return seen


def gather_prompt(prompt_arg: str | None) -> str:
    """Gather the prompt from CLI argument, stdin, or interactive input."""

    if prompt_arg and prompt_arg.strip():
        return prompt_arg.strip()

    if not sys.stdin.isatty():
        streamed = sys.stdin.read().strip()
        if streamed:
            return streamed

    return Prompt.ask("Enter a prompt to refine").strip()


def format_variants_for_display(
    variants: Dict[str, str], order: Iterable[str] | None = None
) -> List[tuple[str, str]]:
    """Return ordered (label, text) tuples for rendering."""

    order = list(order or default_variant_order())
    formatted = []
    for key in order:
        value = variants.get(key)
        if not value:
            continue
        formatted.append((VARIANT_LABELS.get(key, key.title()), value.strip()))
    return formatted


def setup_logging(debug: bool) -> None:
    """Configure logging level for the CLI runtime."""

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
