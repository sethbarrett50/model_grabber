"""Smoke tests for model_grabber."""

from __future__ import annotations

from pathlib import Path

from model_grabber.config import build_download_requests
from model_grabber.downloader import safe_output_dir
from model_grabber.models import CliArgsModel, resolve_model_name
from model_grabber.parser import build_parser


def test_build_parser() -> None:
    """Ensure the parser can be constructed."""
    parser = build_parser()
    assert parser.prog == 'model-grabber'


def test_resolve_model_name_known_preset() -> None:
    """Ensure known preset aliases resolve correctly."""
    assert resolve_model_name('kimi-k2.5') == 'moonshotai/Kimi-K2.5'
    assert resolve_model_name('glm-5.1') == 'zai-org/GLM-5.1'


def test_resolve_model_name_unknown_preset() -> None:
    """Ensure unknown names pass through unchanged."""
    repo_id = 'Qwen/Qwen3-8B'
    assert resolve_model_name(repo_id) == repo_id


def test_safe_output_dir() -> None:
    """Ensure repo IDs map to predictable local directories."""
    root = Path('/tmp/models')
    output_dir = safe_output_dir(root=root, repo_id='org/model-name')
    assert output_dir == Path('/tmp/models/org--model-name')


def test_cli_model_normalizes_values(tmp_path: Path) -> None:
    """Ensure CLI args are normalized by validators."""
    config = CliArgsModel(
        models=[' kimi-k2.5 ', 'glm-5.1'],
        root=tmp_path,
        token=None,
        env_file=tmp_path / '.env',
        revision=' main ',
        allow_pattern=[' *.json ', ''],
        ignore_pattern=[' *.bin ', ''],
    )
    assert config.models == ['kimi-k2.5', 'glm-5.1']
    assert config.revision == 'main'
    assert config.allow_pattern == ['*.json']
    assert config.ignore_pattern == ['*.bin']


def test_build_download_requests(tmp_path: Path) -> None:
    """Ensure download requests are built from CLI config."""
    config = CliArgsModel(
        models=['kimi-k2.5'],
        root=tmp_path,
        token='abc123',
        env_file=tmp_path / '.env',
        revision=None,
        allow_pattern=None,
        ignore_pattern=None,
    )

    requests = build_download_requests(config)

    assert len(requests) == 1
    assert requests[0].repo_id == 'moonshotai/Kimi-K2.5'
    assert requests[0].root == tmp_path.resolve()
    assert requests[0].token == 'abc123'
