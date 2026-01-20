import logging
from pathlib import Path

import geopandas

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFBuilding
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_building"]


def load_building(file_path: Path, intermediate_rep) -> None:
    """Load building features"""
    jgf = geopandas.read_file(file_path, engine="fiona")

    if IMDFFeatureType.building not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.building] = []
    for ith, v in jgf.iterrows():
        alt_name = None
        if "ALT_NAME_MULTILANG" in v:
            alt_name = v["ALT_NAME_MULTILANG"]

        restriction = None
        if "RESTRICTION" in v:
            restriction = v["RESTRICTION"]

        address_id = None
        if "ADDRESS" in v:
            address_id = v["ADDRESS"]

        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        building_id = v["BLDG_ID"]
        category = v["CATEGORY"]

        if PATCH_DATA:
            if address_id is None:
                address_id = "ERROR!!"

            if building_id is None:
                building_id = "ERROR!!"

            if category is None:
                category = "ERROR!!"

        intermediate_rep[IMDFFeatureType.building].append(
            IMDFBuilding(
                id=building_id,
                name=name,
                alt_name=alt_name,
                category=category,
                restriction=restriction,
                display_point=convert_display_point(v),
                address_id=address_id,
                # geometry=v.geometry, # TODO: WAT? MAKE FOOT PRINTS!?!
                # v['FOOTPRINT_CATEGORY'] str # TODO: WAT?
                # v['FOOTPRINT_NAME']  str # TODO: WAT?
            )
        )
