import logging
import uuid
from pathlib import Path

import geopandas

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFixture
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_fixture"]


def load_fixture(file_path: Path, intermediate_rep) -> None:
    """Load fixture features"""
    _logger.info(f"Loading fixture FeatureCollection from {file_path}")

    try:
        jgf = geopandas.read_file(file_path, engine="fiona")
    except Exception as e:
        _logger.error(f"Failed to load fixture: {file_path} {e}")
        return

    if IMDFFeatureType.fixture not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.fixture] = []

    for ith, v in jgf.iterrows():
        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        alt_name = None
        if "ALT_NAME_MULTILANG" in v:
            alt_name = v["ALT_NAME_MULTILANG"]

        anchor_id = None
        if "ANCHOR_ID" in v:
            anchor_id = v["ANCHOR_ID"]

        fixture_id = None
        if "FIXTURE_ID" in v:
            fixture_id = v["FIXTURE_ID"]

        if PATCH_DATA:
            if fixture_id is None:
                fixture_id = uuid.uuid4().hex

        intermediate_rep[IMDFFeatureType.fixture].append(
            IMDFFixture(
                id=fixture_id,
                geometry=v.geometry,
                name=name,
                anchor_id=anchor_id,
                alt_name=alt_name,
                display_point=convert_display_point(v),
                category=v["CATEGORY"],
                level_id=v["LEVEL_ID"],
            )
        )
