"""CLI for downloading Hugging Face model repositories."""

from __future__ import annotations

import argparse
import sys

from pathlib import Path
from typing import Final

from huggingface_hub import snapshot_download
from huggingface_hub.utils import HfHubHTTPError

DEFAULT_ROOT: Final[Path] = Path('/data/seth/models')

PRESET_MODELS: Final[dict[str, str]] = {
    'kimi-k2.5': 'moonshotai/Kimi-K2.5',
    'glm-5.1': 'zai-org/GLM-5.1',
}


def build_parser() -> argparse.ArgumentParser:
    """Build the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog='model-grabber',
        description=('Download one or more Hugging Face model repos into a local folder.'),
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
        help=('Optional Hugging Face token. If omitted, huggingface_hub will use your cached login/token.'),
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
        help=('Optional glob pattern to include. May be passed multiple times.'),
    )
    parser.add_argument(
        '--ignore-pattern',
        action='append',
        default=None,
        help=('Optional glob pattern to exclude. May be passed multiple times.'),
    )
    parser.add_argument(
        '--local-dir-use-symlinks',
        action='store_true',
        help=('Use symlinks when supported by huggingface_hub/local filesystem.'),
    )
    return parser


def resolve_model_name(model_name: str) -> str:
    """Resolve a preset alias to a Hugging Face repo ID."""
    return PRESET_MODELS.get(model_name.lower(), model_name)


def safe_output_dir(root: Path, repo_id: str) -> Path:
    """Create a predictable local directory for a repo ID."""
    return root / repo_id.replace('/', '--')


def download_model(
    repo_id: str,
    root: Path,
    token: str | None,
    revision: str | None,
    allow_patterns: list[str] | None,
    ignore_patterns: list[str] | None,
    use_symlinks: bool,
) -> Path:
    """Download a model snapshot and return its local directory."""
    output_dir = safe_output_dir(root=root, repo_id=repo_id)
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    snapshot_download(
        repo_id=repo_id,
        repo_type='model',
        local_dir=output_dir,
        local_dir_use_symlinks=use_symlinks,
        token=token,
        revision=revision,
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
        resume_download=True,
    )

    return output_dir


def main() -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()

    root: Path = args.root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    exit_code = 0

    for raw_model in args.models:
        repo_id = resolve_model_name(raw_model)

        print(f'Downloading {repo_id} into {safe_output_dir(root, repo_id)}')

        try:
            destination = download_model(
                repo_id=repo_id,
                root=root,
                token=args.token,
                revision=args.revision,
                allow_patterns=args.allow_pattern,
                ignore_patterns=args.ignore_pattern,
                use_symlinks=args.local_dir_use_symlinks,
            )
        except HfHubHTTPError as exc:
            print(f'Failed to download {repo_id}: {exc}', file=sys.stderr)
            exit_code = 1
            continue
        except Exception as exc:
            print(
                f'Unexpected error while downloading {repo_id}: {exc}',
                file=sys.stderr,
            )
            exit_code = 1
            continue

        print(f'Finished: {repo_id} -> {destination}')

    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
