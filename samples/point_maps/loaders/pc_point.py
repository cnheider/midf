import logging
from pathlib import Path

import geopandas

_logger = logging.getLogger(__name__)

__all__ = ["load_point"]


def load_point(file_path: Path, intermediate_rep) -> None:
    """Load point features"""
    jgf = geopandas.read_file(file_path, engine="fiona")

    for ith, v in jgf.iterrows():
        ...
