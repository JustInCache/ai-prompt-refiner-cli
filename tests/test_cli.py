"""Tests for CLI argument parsing and flow."""

from __future__ import annotations

from click.testing import CliRunner

from promptrefiner import cli as cli_module


class StubProvider:
    """Deterministic provider used during CLI tests."""

    def generate(self, prompt: str):
        return {
            "improved": f"Improved::{prompt}",
            "power": "Power version",
            "short": "Short version",
            "long": "Long version",
            "creative": "Creative twist",
        }


def patch_provider(monkeypatch):
    """Replace the provider factory with the stub."""

    monkeypatch.setattr(
        cli_module, "get_provider", lambda name="openai": StubProvider()
    )


def test_cli_refine_with_argument(monkeypatch):
    patch_provider(monkeypatch)
    runner = CliRunner()

    result = runner.invoke(
        cli_module.cli, ["refine", "launch a rocket", "--short"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert "Short Prompt" in result.output
    assert "Improved Prompt" not in result.output


def test_cli_refine_with_default_modes(monkeypatch):
    patch_provider(monkeypatch)
    runner = CliRunner()

    result = runner.invoke(cli_module.cli, ["refine", "compose music"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "Improved Prompt" in result.output
    assert "Creative Twist" in result.output


def test_cli_fails_for_unknown_provider(monkeypatch):
    runner = CliRunner()

    result = runner.invoke(
        cli_module.cli, ["refine", "test", "--provider", "nope"], catch_exceptions=False
    )

    assert result.exit_code != 0
    assert "Unknown provider" in result.output
