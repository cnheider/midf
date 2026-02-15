import logging
from pathlib import Path

import geopandas

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType, IMDFOpeningCategory
from midf.imdf_model import IMDFOpening
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_opening"]


def load_opening(file_path: Path, intermediate_rep) -> None:
    """Load opening features"""
    pc_openings = geopandas.read_file(file_path, engine="fiona")

    if IMDFFeatureType.opening not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.opening] = []

    for ith, v in pc_openings.iterrows():
        accessibility = None
        if "ACCESSIBILITY" in v:
            accessibility = v["ACCESSIBILITY"]

        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        alt_name = None
        if "ALT_NAME_MULTILANG" in v:
            alt_name = v["ALT_NAME_MULTILANG"]

        access_control = None
        if "ACCESS_CONTROL" in v:
            access_control = v["ACCESS_CONTROL"]

        category = None
        if "CATEGORY" in v:
            category = v["CATEGORY"]

        door = None
        if "DOOR" in v:
            door = v["DOOR"]

        level_id = None
        if "LEVEL_ID" in v:
            level_id = v["LEVEL_ID"]

        opening_id = None
        if "OPENING_ID" in v:
            opening_id = v["OPENING_ID"]

        if PATCH_DATA:
            if category is None:
                category = IMDFOpeningCategory.pedestrian

        intermediate_rep[IMDFFeatureType.opening].append(
            IMDFOpening(
                id=opening_id,
                geometry=v.geometry,
                category=category,
                level_id=level_id,
                accessibility=accessibility,
                access_control=access_control,
                door=door,
                name=name,
                alt_name=alt_name,
                display_point=convert_display_point(v),
            )
        )
