import logging
from pathlib import Path

from .load_route import parse_route

_logger = logging.getLogger(__name__)

__all__ = ["load_route"]


def load_route(file_path: Path, destination_file: Path) -> None:
    """Load route features"""

    parse_route(file_path, destination_file)
