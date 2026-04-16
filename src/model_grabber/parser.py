"""Argument parser construction."""

from __future__ import annotations

import argparse

from pathlib import Path

from model_grabber.constants import DEFAULT_DOTENV_PATH, DEFAULT_ROOT


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog='model-grabber',
        description=('Download one or more Hugging Face model repositories into a local folder.'),
    )
    parser.add_argument(
        'models',
        nargs='+',
        help=('Model repo IDs or preset names. Examples: kimi-k2.5 glm-5.1 Qwen/Qwen3-8B'),
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=DEFAULT_ROOT,
        help=f'Base directory for downloads. Default: {DEFAULT_ROOT}',
    )
    parser.add_argument(
        '--token',
        type=str,
        default=None,
        help=('Optional Hugging Face token. Overrides HF_TOKEN from the environment or .env.'),
    )
    parser.add_argument(
        '--env-file',
        type=Path,
        default=DEFAULT_DOTENV_PATH,
        help='Path to .env file. Default: .env',
    )
    parser.add_argument(
        '--revision',
        type=str,
        default=None,
        help='Optional branch, tag, or commit hash to download.',
    )
    parser.add_argument(
        '--allow-pattern',
        action='append',
        default=None,
        help='Optional glob pattern to include. May be passed multiple times.',
    )
    parser.add_argument(
        '--ignore-pattern',
        action='append',
        default=None,
        help='Optional glob pattern to exclude. May be passed multiple times.',
    )
    return parser
