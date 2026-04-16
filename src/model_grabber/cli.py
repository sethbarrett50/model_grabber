"""CLI orchestration."""

from __future__ import annotations

import sys

from pydantic import ValidationError

from model_grabber.config import build_download_requests, parse_cli_args
from model_grabber.downloader import download_model, safe_output_dir
from model_grabber.exceptions import ModelDownloadError, ModelGrabberError
from model_grabber.parser import build_parser


def run() -> int:
    """Run the CLI application and return an exit code."""
    parser = build_parser()
    namespace = parser.parse_args()

    try:
        config = parse_cli_args(namespace)
        config.root.mkdir(parents=True, exist_ok=True)
        requests = build_download_requests(config)
    except ValidationError as exc:
        print(f'Configuration validation failed:\n{exc}', file=sys.stderr)
        return 2
    except ModelGrabberError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    exit_code = 0

    for request in requests:
        destination_dir = safe_output_dir(request.root, request.repo_id)
        print(f'Downloading {request.repo_id} into {destination_dir}')

        try:
            destination = download_model(request)
        except ModelDownloadError as exc:
            print(str(exc), file=sys.stderr)
            exit_code = 1
            continue

        print(f'Finished: {request.repo_id} -> {destination}')

    return exit_code
