"""Download service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError

from model_grabber.exceptions import ModelDownloadError

if TYPE_CHECKING:
    from pathlib import Path

    from model_grabber.models import DownloadRequest


def safe_output_dir(root: Path, repo_id: str) -> Path:
    """Create a predictable local directory for a repo ID."""
    return root / repo_id.replace('/', '--')


def download_model(request: DownloadRequest) -> Path:
    """Download a model snapshot and return its local directory."""
    output_dir = safe_output_dir(root=request.root, repo_id=request.repo_id)
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        snapshot_download(
            repo_id=request.repo_id,
            repo_type='model',
            local_dir=output_dir,
            token=request.token,
            revision=request.revision,
            allow_patterns=request.allow_patterns,
            ignore_patterns=request.ignore_patterns,
        )
    except HfHubHTTPError as exc:
        raise ModelDownloadError(f'Failed to download {request.repo_id}: {exc}') from exc
    except OSError as exc:
        raise ModelDownloadError(f'Filesystem error while downloading {request.repo_id}: {exc}') from exc

    return output_dir
