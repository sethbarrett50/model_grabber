"""Smoke tests for model_grabber."""

from __future__ import annotations

from pathlib import Path

from model_grabber.main import (
    PRESET_MODELS,
    build_parser,
    load_token,
    resolve_model_name,
    safe_output_dir,
)


def test_build_parser() -> None:
    """Ensure the parser can be constructed."""
    parser = build_parser()
    assert parser.prog == 'model-grabber'


def test_resolve_model_name_known_preset() -> None:
    """Ensure known preset aliases resolve correctly."""
    assert resolve_model_name('kimi-k2.5') == PRESET_MODELS['kimi-k2.5']
    assert resolve_model_name('glm-5.1') == PRESET_MODELS['glm-5.1']


def test_resolve_model_name_unknown_preset() -> None:
    """Ensure unknown names pass through unchanged."""
    repo_id = 'Qwen/Qwen3-8B'
    assert resolve_model_name(repo_id) == repo_id


def test_safe_output_dir() -> None:
    """Ensure repo IDs map to predictable local directories."""
    root = Path('/tmp/models')
    output_dir = safe_output_dir(root=root, repo_id='org/model-name')
    assert output_dir == Path('/tmp/models/org--model-name')


def test_load_token_from_env_file(tmp_path: Path) -> None:
    """Ensure HF_TOKEN can be loaded from a .env file."""
    env_file = tmp_path / '.env'
    env_file.write_text('HF_TOKEN=test-token\n', encoding='utf-8')

    token = load_token(env_file=env_file, cli_token=None)
    assert token == 'test-token'


def test_load_token_cli_overrides_env_file(tmp_path: Path) -> None:
    """Ensure explicit CLI token takes precedence."""
    env_file = tmp_path / '.env'
    env_file.write_text('HF_TOKEN=env-token\n', encoding='utf-8')

    token = load_token(env_file=env_file, cli_token='cli-token')
    assert token == 'cli-token'
