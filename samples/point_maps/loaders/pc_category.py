from pathlib import Path

import json
import logging
from typing import Any, Dict

_logger = logging.getLogger(__name__)

__all__ = ["load_category"]


def load_category(file_path: Path) -> Dict[str, Any]:
    """Load category features"""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)
