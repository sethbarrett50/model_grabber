"""Custom exception types for model_grabber."""

from __future__ import annotations


class ModelGrabberError(Exception):
    """Base exception for all application-specific errors."""


class ConfigurationError(ModelGrabberError):
    """Raised when CLI or configuration values are invalid."""


class TokenError(ModelGrabberError):
    """Raised when token loading fails."""


class ModelDownloadError(ModelGrabberError):
    """Raised when a model download fails."""
