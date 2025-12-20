"""Command-line interface for the Prompt Refiner CLI."""

from __future__ import annotations

import logging
from typing import Iterable, List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

from .core import PromptRefiner
from .providers.base import ProviderConfigurationError, ProviderError
from .providers.openai_provider import OpenAIProvider
from .utils import (
    default_variant_order,
    format_variants_for_display,
    gather_prompt,
    select_variants,
    setup_logging,
)

LOGGER = logging.getLogger(__name__)
CONSOLE = Console(
    theme=Theme(
        {
            "primary": "bold cyan",
            "accent": "magenta",
            "error": "bold red",
            "success": "bold green",
        }
    )
)


def get_provider(name: str):
    """Return the provider implementation for the given alias."""

    if name == "openai":
        return OpenAIProvider()
    raise click.ClickException(
        f"Unknown provider '{name}'. Available providers: openai."
    )


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose debug logging.")
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    """Prompt refiner command group."""

    setup_logging(debug)
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug


@cli.command()
@click.argument("prompt", required=False)
@click.option("--short", "short_flag", is_flag=True, help="Only show the short version.")
@click.option("--long", "long_flag", is_flag=True, help="Only show the long version.")
@click.option("--power", is_flag=True, help="Only show the power prompt.")
@click.option(
    "--creative", is_flag=True, help="Only show the creative twist version."
)
@click.option("--all", "show_all", is_flag=True, help="Show all versions (default).")
@click.option(
    "--provider",
    default="openai",
    show_default=True,
    help="Provider backend for generating refinements.",
)
@click.pass_context
def refine(
    ctx: click.Context,
    prompt: Optional[str],
    short_flag: bool,
    long_flag: bool,
    power: bool,
    creative: bool,
    show_all: bool,
    provider: str,
):
    """Refine prompts into multiple high-quality variants."""

    prompt_text = gather_prompt(prompt)

    flags: List[str] | None = _resolve_flag_selection(
        show_all=show_all,
        short_flag=short_flag,
        long_flag=long_flag,
        power=power,
        creative=creative,
    )

    try:
        modes = select_variants(flags) if flags is not None else default_variant_order()
    except KeyError as exc:  # pragma: no cover - defensive
        raise click.ClickException(str(exc)) from exc

    try:
        provider_instance = get_provider(provider)
        engine = PromptRefiner(provider=provider_instance)
        result = engine.refine(prompt_text, modes=modes)
    except ProviderConfigurationError as exc:
        raise click.ClickException(
            f"{exc} Set OPENAI_API_KEY and try again."
        ) from exc
    except ProviderError as exc:
        raise click.ClickException(str(exc)) from exc
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    _render_output(result.variants, prompt_text, modes)


def _resolve_flag_selection(
    show_all: bool,
    short_flag: bool,
    long_flag: bool,
    power: bool,
    creative: bool,
) -> List[str] | None:
    """Turn CLI flag combinations into a list of variant keys."""

    if show_all:
        return None

    requested: List[str] = []
    if short_flag:
        requested.append("short")
    if long_flag:
        requested.append("long")
    if power:
        requested.append("power")
    if creative:
        requested.append("creative")

    if not requested:
        return None
    return requested


def _render_output(variants: dict, original_prompt: str, order: Iterable[str]):
    """Render the refined prompts using a rich table."""

    CONSOLE.print(f"[success]Original:[/] {original_prompt}\n")

    table = Table(show_header=True, header_style="primary")
    table.add_column("Variant", style="accent", no_wrap=True)
    table.add_column("Prompt", style="white")

    for label, value in format_variants_for_display(variants, order):
        table.add_row(label, value)

    CONSOLE.print(table)


def main():
    """CLI entrypoint for packaging."""

    cli()
