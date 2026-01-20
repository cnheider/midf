import logging
import uuid
from pathlib import Path
from typing import Any, Mapping

import geopandas
import requests
import shapely

from midf.constants import (
    PATCH_DATA,
    UNIT_LESS_OCCUPANT_LEVEL_NAME,
    UNIT_LESS_POINT_SIZE,
)
from midf.enums import (
    IMDFFeatureType,
    IMDFLevelCategory,
    IMDFOccupantCategory,
    IMDFUnitCategory,
)
from midf.imdf_model import IMDFAnchor, IMDFLevel, IMDFOccupant, IMDFUnit

_logger = logging.getLogger(__name__)

__all__ = ["load_occupant"]

POINT_MAPS_IMAGE_PATH = "https://cms.point-maps.com/images/{0}"


def load_occupant(file_path: Path, intermediate_rep, skip_media) -> Mapping[str, Any]:
    """Load occupant features"""
    jgf = geopandas.read_file(file_path, engine="fiona")

    occupant_package = {}

    if IMDFFeatureType.occupant not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.occupant] = []

    had_unit_less_occupant = False
    for ith, v in jgf.iterrows():
        name = None
        if "NAME_MULTILANG" in v:
            name = v["NAME_MULTILANG"]

        if PATCH_DATA:
            _name = None

            if _name is None:
                if "NAME" in v:
                    _name = v["NAME"]

            if _name is None:
                if "AREA" in v:
                    _name = v["AREA"]

            if _name is None:
                if "ZONE" in v:
                    _name = v["ZONE"]

            if _name is None:
                _name = "ERROR!"

            if name is None:
                name = {"en": _name}

        validity = None
        if "VALIDITY" in v:
            validity = v["VALIDITY"]

        correlation_id = None
        if "CORRELATION_ID" in v:
            correlation_id = v["CORRELATION_ID"]

        website = None
        if "WEBSITE" in v:
            website = v["WEBSITE"]

        phone = None
        if "PHONE" in v:
            phone = v["PHONE"]

        hours = None
        if "HOURS" in v:
            hours = v["HOURS"]

        category = None
        if "CATEGORY" in v:
            category = v["CATEGORY"]

        anchor_id = v["ANCHOR_ID"]

        if PATCH_DATA:
            if category is None:
                category = IMDFOccupantCategory.utilities

            if anchor_id is None:
                anchor_id = uuid.uuid4().hex

        unit_id = None
        if "UNIT_ID" in v:
            unit_id = v["UNIT_ID"]

        if unit_id is None:
            if "UNIT_IDS" in v:
                if v["UNIT_IDS"]:
                    if len(v["UNIT_IDS"]) > 0:
                        assert len(v["UNIT_IDS"]) == 1
                        unit_id = v["UNIT_IDS"][0]

        if unit_id is None:
            unit_id = uuid.uuid4().hex

            if IMDFFeatureType.unit not in intermediate_rep:
                intermediate_rep[IMDFFeatureType.unit] = []

            level_id = None
            if "LEVEL_ID" in v:
                level_id = v["LEVEL_ID"]

            accessibility = None
            if "ACCESSIBILITY" in v:
                accessibility = v["ACCESSIBILITY"]

            alt_name = None
            if "ALT_NAME_MULTILANG" in v:
                alt_name = v["ALT_NAME_MULTILANG"]

            if PATCH_DATA:
                if level_id is None:
                    level_id = UNIT_LESS_OCCUPANT_LEVEL_NAME

            intermediate_rep[IMDFFeatureType.unit].append(
                IMDFUnit(
                    id=unit_id,
                    name={"en": "UnitLessOccupantUnit"},
                    alt_name=alt_name,
                    geometry=v.geometry.buffer(UNIT_LESS_POINT_SIZE),
                    level_id=level_id,
                    category=IMDFUnitCategory.unspecified,
                    accessibility=accessibility,
                )
            )

            had_unit_less_occupant = True

        assert unit_id is not None and unit_id, f"{unit_id=}"

        if IMDFFeatureType.anchor not in intermediate_rep:
            intermediate_rep[IMDFFeatureType.anchor] = []

        address_id = None
        if "ADDRESS_ID" in v:
            address_id = v["ADDRESS_ID"]

        intermediate_rep[IMDFFeatureType.anchor].append(
            IMDFAnchor(
                id=anchor_id,
                geometry=v.geometry,
                unit_id=unit_id,
                address_id=address_id,
            )
        )

        occupant_id = v["OCCU_ID"]

        intermediate_rep[IMDFFeatureType.occupant].append(
            IMDFOccupant(
                id=occupant_id,
                category=category,
                name=name,
                anchor_id=anchor_id,
                hours=hours,
                phone=phone,
                website=website,
                validity=validity,
                correlation_id=correlation_id,
            )
        )

        if not skip_media:
            occupant_p = {
                k: v.get(k)
                for k in [
                    "CATEGORY_ID",  # str hash              # PC SPECIFIC
                    "DESCRIPTION",  # None                  # PC SPECIFIC
                    "EMAIL",  # None                        # PC SPECIFIC
                    "EXTRA_CATEGORY_IDS",  # Empty List            # PC SPECIFIC
                    "KEYWORDS",  # None                      # PC SPECIFIC
                    "OMNI_ORDINAL",  # None                  # PC SPECIFIC
                    "ROUTABLE",  # None                     # PC SPECIFIC
                    "RoutePoints",  # List[int]             # PC SPECIFIC
                    "SHOW",  # bool                        # PC SPECIFIC
                    "Waypoints",  # List[str]   some id     # PC SPECIFIC
                ]
            }

            images = []
            if "IMAGES" in v and v["IMAGES"]:
                if len(v["IMAGES"]) > 0:
                    for image_id in v["IMAGES"]:
                        if "http://" in image_id or "https://" in image_id:
                            image_url = image_id
                        else:
                            image_url = POINT_MAPS_IMAGE_PATH.format(image_id)
                        _logger.info(f"Loading image {image_url}")
                        try:
                            images.append(requests.get(image_url).content)
                        except Exception as e:
                            _logger.error(f"Failed to load image {image_url}: {e}")

            description = (
                f"Description: {str(occupant_p['DESCRIPTION'])}"
                f"\n\n"
                f"Email: {str(occupant_p['EMAIL'])}"
            )

            occupant_p["images"] = images
            occupant_p["anchor_id"] = anchor_id
            occupant_p["category"] = category
            occupant_p["name"] = name
            occupant_p["description"] = description

            occupant_package[occupant_id] = occupant_p

    if had_unit_less_occupant:
        if IMDFFeatureType.level not in intermediate_rep:
            intermediate_rep[IMDFFeatureType.level] = []

        intermediate_rep[IMDFFeatureType.level].append(
            IMDFLevel(
                id=UNIT_LESS_OCCUPANT_LEVEL_NAME,
                geometry=shapely.convex_hull(jgf.unary_union),
                category=IMDFLevelCategory.unspecified,
                outdoor=True,
                name={"en": UNIT_LESS_OCCUPANT_LEVEL_NAME},
                short_name={"en": UNIT_LESS_OCCUPANT_LEVEL_NAME},
            )
        )

    return occupant_package
