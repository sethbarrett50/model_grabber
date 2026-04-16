"""Package constants."""

from __future__ import annotations

from pathlib import Path
from typing import Final

DEFAULT_ROOT: Final[Path] = Path('/data/seth/models')
DEFAULT_DOTENV_PATH: Final[Path] = Path('.env')

PRESET_MODELS: Final[dict[str, str]] = {
    'kimi-k2.5': 'moonshotai/Kimi-K2.5',
    'glm-5.1': 'zai-org/GLM-5.1',
}
