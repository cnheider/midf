import json
import logging
from pathlib import Path
from typing import Any, Dict

_logger = logging.getLogger(__name__)

__all__ = ["load_setting"]


def load_setting(file_path: Path) -> Dict[str, Any]:
    """Load setting features"""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)
