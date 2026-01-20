from pathlib import Path

import geopandas
import logging
import uuid

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType, IMDFUnitCategory
from midf.imdf_model import IMDFUnit
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_unit"]


def load_unit(file_path: Path, intermediate_rep) -> None:
    """Load unit features"""

    _logger.info(f"Loading unit FeatureCollection: {file_path}")

    try:
        jgf = geopandas.read_file(file_path, engine="fiona")
    except Exception as e:
        _logger.error(f"Failed to load {file_path}: {e}")
        return

    if IMDFFeatureType.unit not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.unit] = []
    for ith, v in jgf.iterrows():
        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        alt_name = None
        if "ALT_NAME_MULTILANG" in v:
            alt_name = v["ALT_NAME_MULTILANG"]

        restriction = None
        if "RESTRICTION" in v:
            restriction = v["RESTRICTION"]

        accessibility = None
        if "ACCESSIBILITY" in v:
            accessibility = v["ACCESSIBILITY"]

        unit_id = v["UNIT_ID"]

        category = v["CATEGORY"]
        if PATCH_DATA:
            if category is None:
                category = IMDFUnitCategory.room

            if unit_id is None:
                unit_id = uuid.uuid4().hex

        intermediate_rep[IMDFFeatureType.unit].append(
            IMDFUnit(
                id=unit_id,
                name=name,
                alt_name=alt_name,
                display_point=convert_display_point(v),
                geometry=v.geometry,
                category=category,
                restriction=restriction,
                accessibility=accessibility,
                level_id=v["LEVEL_ID"],
            )
        )
