from pathlib import Path

import geopandas
import logging

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFLevel
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_level"]


def load_level(file_path: Path, intermediate_rep) -> None:
    """Load level features"""
    _logger.info(f"Loading level FeatureCollection: {file_path}")

    try:
        pc_levels = geopandas.read_file(file_path, engine="fiona")
    except Exception as e:
        _logger.error(f"Failed to load {file_path}: {e}")
        return

    if IMDFFeatureType.level not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.level] = []
    for ith, v in pc_levels.iterrows():
        outdoor = None
        if "OUTDOOR" in v:
            outdoor = v["OUTDOOR"]
            if not isinstance(outdoor, bool):
                _logger.warning(f"{outdoor=}, casting to bool {not bool(outdoor)}")
                outdoor = not bool(outdoor)

        restriction = None
        if "RESTRICTION" in v:
            restriction = v["RESTRICTION"]

        address_id = None
        if "ADDRESS_ID" in v:
            address_id = v["ADDRESS_ID"]

        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        short_name = None
        if "SHORT_NAME_MULTILANG" in v:
            short_name = v["SHORT_NAME_MULTILANG"]

        building_ids = []
        if "BLDG_IDS" in v:
            if v["BLDG_IDS"]:
                building_ids.extend(v["BLDG_IDS"])

        if PATCH_DATA:
            if name is None:
                name = {"en": "ERROR!"}

            if short_name is None:
                short_name = {"en": "ERROR!"}

            if outdoor is None:
                outdoor = False

        intermediate_rep[IMDFFeatureType.level].append(
            IMDFLevel(
                id=v["LEVEL_ID"],
                category=v["CATEGORY"],
                name=name,
                short_name=short_name,
                restriction=restriction,
                outdoor=outdoor,
                ordinal=v["ORDINAL"],
                display_point=convert_display_point(v),
                address_id=address_id,
                building_ids=building_ids,
                geometry=v.geometry,
                # v['OPENING_IDS']  List # TODO: WAT?
            )
        )
