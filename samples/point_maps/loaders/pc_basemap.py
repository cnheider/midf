import logging
from pathlib import Path

import geopandas
import shapely

from midf.enums import IMDFFeatureType, IMDFLevelCategory
from midf.imdf_model import IMDFFixture, IMDFLevel

_logger = logging.getLogger(__name__)

__all__ = ["load_basemap"]

BASEMAP_LEVEL_NAME = "BASEMAP_LEVEL"
BASEMAP_ID_PREFIX = "BASEMAP_FIXTURE"


def load_basemap(file_path: Path, intermediate_rep) -> None:
    """Load basemap features"""
    pc_basemap_elements = geopandas.read_file(file_path, engine="fiona")
    if pc_basemap_elements is None:
        return

    if IMDFFeatureType.level not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.level] = []

    level_geometry = shapely.convex_hull(pc_basemap_elements.make_valid().unary_union)

    if level_geometry is None or level_geometry.is_empty:
        return

    basemap_level = IMDFLevel(
        id=BASEMAP_LEVEL_NAME,
        geometry=level_geometry,
        category=IMDFLevelCategory.unspecified,
        outdoor=True,
        name={"en": BASEMAP_LEVEL_NAME},
        short_name={"en": BASEMAP_LEVEL_NAME},
    )
    intermediate_rep[IMDFFeatureType.level].append(basemap_level)

    if IMDFFeatureType.fixture not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.fixture] = []

    for ith, v in pc_basemap_elements.iterrows():
        intermediate_rep[IMDFFeatureType.fixture].append(
            IMDFFixture(
                id=f"{BASEMAP_ID_PREFIX}{ith}",
                geometry=v.geometry,
                category=v["CATEGORY"],
                level_id=basemap_level.id,
            )
        )
