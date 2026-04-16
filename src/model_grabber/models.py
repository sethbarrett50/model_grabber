"""Validated application models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from model_grabber.constants import PRESET_MODELS
from model_grabber.exceptions import ConfigurationError


class CliArgsModel(BaseModel):
    """Validated representation of parsed CLI arguments."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    models: list[str]
    root: Path
    token: str | None = None
    env_file: Path
    revision: str | None = None
    allow_pattern: list[str] | None = None
    ignore_pattern: list[str] | None = None

    @field_validator('models')
    @classmethod
    def validate_models(cls, value: list[str]) -> list[str]:
        """Ensure at least one non-empty model string is present."""
        cleaned = [item.strip() for item in value if item.strip()]
        if not cleaned:
            raise ConfigurationError('At least one model must be provided.')
        return cleaned

    @field_validator('root', 'env_file', mode='before')
    @classmethod
    def expand_paths(cls, value: Path | str) -> Path:
        """Normalize incoming path values."""
        return Path(value).expanduser()

    @field_validator('revision')
    @classmethod
    def normalize_revision(cls, value: str | None) -> str | None:
        """Normalize optional revision."""
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator('allow_pattern', 'ignore_pattern')
    @classmethod
    def normalize_patterns(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        """Drop empty patterns and return None when empty."""
        if value is None:
            return None

        cleaned = [item.strip() for item in value if item.strip()]
        return cleaned or None


class DownloadRequest(BaseModel):
    """Validated request for a single model download."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    repo_id: str = Field(min_length=1)
    root: Path
    token: str | None = None
    revision: str | None = None
    allow_patterns: list[str] | None = None
    ignore_patterns: list[str] | None = None

    @field_validator('repo_id')
    @classmethod
    def validate_repo_id(cls, value: str) -> str:
        """Validate repository identifier."""
        stripped = value.strip()
        if not stripped:
            raise ConfigurationError('Repository ID cannot be empty.')
        return stripped

    @field_validator('root', mode='before')
    @classmethod
    def normalize_root(cls, value: Path | str) -> Path:
        """Normalize the root path."""
        return Path(value).expanduser().resolve()

    @field_validator('allow_patterns', 'ignore_patterns')
    @classmethod
    def normalize_download_patterns(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        """Normalize optional pattern lists."""
        if value is None:
            return None

        cleaned = [item.strip() for item in value if item.strip()]
        return cleaned or None


def resolve_model_name(model_name: str) -> str:
    """Resolve a preset alias to a Hugging Face repository ID."""
    return PRESET_MODELS.get(model_name.lower(), model_name)
