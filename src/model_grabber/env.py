"""Environment and token loading helpers."""

from __future__ import annotations

import os

from typing import TYPE_CHECKING

from dotenv import load_dotenv

from model_grabber.exceptions import TokenError

if TYPE_CHECKING:
    from pathlib import Path


def load_token(env_file: Path, cli_token: str | None) -> str | None:
    """Load the Hugging Face token from CLI or environment."""
    try:
        if env_file.is_file():
            load_dotenv(dotenv_path=env_file, override=False)
    except OSError as exc:
        raise TokenError(f"Failed to read env file '{env_file}': {exc}") from exc

    if cli_token:
        return cli_token

    return os.getenv('HF_TOKEN')
