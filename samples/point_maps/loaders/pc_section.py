from pathlib import Path

import geopandas
import logging
import uuid

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFSection
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_section"]


def load_section(file_path: Path, intermediate_rep) -> None:
    """Load section features"""
    _logger.info(f"Loading section FeatureCollection from {file_path}")

    try:
        pc_sections = geopandas.read_file(file_path, engine="fiona")
    except Exception as e:
        _logger.error(f"Failed to load {file_path}: {e}")
        return

    if IMDFFeatureType.section not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.section] = []
    for ith, v in pc_sections.iterrows():
        restriction = None
        if "RESTRICTION" in v:
            restriction = v["RESTRICTION"]

        accessibility = None
        if "ACCESSIBILITY" in v:
            accessibility = v["ACCESSIBILITY"]

        address_id = None
        if "ADDRESS_ID" in v:
            address_id = v["ADDRESS_ID"]

        correlation_id = None
        if "CORRELATION_ID" in v:
            correlation_id = v["CORRELATION_ID"]

        parents = None
        if "PARENTS" in v:
            parents = v["PARENTS"]

        alt_name = None
        if "ALT_NAME" in v:
            alt_name = v["ALT_NAME_MULTILANG"]

        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        section_id = v["SECTION_ID"]
        if PATCH_DATA:
            if section_id is None:
                section_id = uuid.uuid4().hex

        intermediate_rep[IMDFFeatureType.section].append(
            IMDFSection(
                id=section_id,
                geometry=v.geometry,
                category=v["CATEGORY"],
                restriction=restriction,
                accessibility=accessibility,
                address_id=address_id,
                correlation_id=correlation_id,
                parents=parents,
                level_id=v["LEVEL_ID"],
                display_point=convert_display_point(v),
                alt_name=alt_name,
                name=name,
            )
        )
