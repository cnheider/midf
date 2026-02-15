import logging
import uuid
from pathlib import Path

import geopandas
import shapely

from midf.constants import PATCH_DATA
from midf.enums import IMDFFeatureType, IMDFVenueCategory
from midf.imdf_model import IMDFAddress, IMDFVenue
from .geojson_utilities import convert_display_point

_logger = logging.getLogger(__name__)

__all__ = ["load_venue"]


class MissingAtLeastOneVenue(Exception):
    pass


def load_venue(file_path: Path, intermediate_rep) -> None:
    """Load venue features"""

    _logger.info(f"Loading venue FeatureCollection: {file_path}")

    try:
        jgf = geopandas.read_file(file_path, engine="fiona")
    except Exception as e:
        _logger.error(f"Failed to load {file_path}: {e}")
        raise MissingAtLeastOneVenue(f"Could not load {file_path}, error: {e}")

    if len(jgf) == 0:
        if not PATCH_DATA:
            raise MissingAtLeastOneVenue(f"{file_path} venue featurecollection {jgf}")
        else:
            jgf = geopandas.GeoDataFrame(
                [
                    {
                        "geometry": shapely.Point(0.0, 0.0).buffer(1),
                    }
                ]
            )

    if IMDFFeatureType.venue not in intermediate_rep:
        intermediate_rep[IMDFFeatureType.venue] = []

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

        address_id = None
        if "ADDRESS_ID" in v:
            address_id = v["ADDRESS_ID"]

        venue_id = None
        if "VENUE_ID" in v:
            venue_id = v["VENUE_ID"]

        category = None
        if "CATEGORY" in v:
            category = v["CATEGORY"]

        hours = None
        if "HOURS" in v:
            hours = v["HOURS"]

        phone = None
        if "PHONE" in v:
            phone = v["PHONE"]

        website = None
        if "WEBSITE" in v:
            website = v["WEBSITE"]

        if PATCH_DATA:
            if name is None:
                if False:
                    name = {"en": "ERROR!"}
                else:
                    name = {"en": file_path.parent.stem}

            if address_id is None:
                if False:
                    address_id = "ERROR!"
                else:
                    address_id = file_path.parent.stem

                if IMDFFeatureType.address not in intermediate_rep:
                    intermediate_rep[IMDFFeatureType.address] = []

                intermediate_rep[IMDFFeatureType.address].append(
                    IMDFAddress(id=address_id, address=file_path.parent.stem)
                )

            if venue_id is None:
                if False:
                    venue_id = uuid.uuid4().hex
                else:
                    venue_id = file_path.parent.stem

            if category is None:
                category = IMDFVenueCategory.airport

        intermediate_rep[IMDFFeatureType.venue].append(
            IMDFVenue(
                id=venue_id,
                category=category,
                name=name,
                hours=hours,
                alt_name=alt_name,
                phone=phone,
                restriction=restriction,
                display_point=convert_display_point(v),
                website=website,
                geometry=v.geometry,
                address_id=address_id,
            )
        )
