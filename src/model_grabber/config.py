"""Configuration assembly helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from model_grabber.env import load_token
from model_grabber.models import CliArgsModel, DownloadRequest, resolve_model_name

if TYPE_CHECKING:
    import argparse


def parse_cli_args(namespace: argparse.Namespace) -> CliArgsModel:
    """Convert argparse namespace into a validated CLI config model."""
    return CliArgsModel.model_validate(vars(namespace))


def build_download_requests(config: CliArgsModel) -> list[DownloadRequest]:
    """Build validated download requests from CLI config."""
    token = load_token(env_file=config.env_file, cli_token=config.token)

    return [
        DownloadRequest(
            repo_id=resolve_model_name(model_name),
            root=config.root,
            token=token,
            revision=config.revision,
            allow_patterns=config.allow_pattern,
            ignore_patterns=config.ignore_pattern,
        )
        for model_name in config.models
    ]
