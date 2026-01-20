import json
import shapely
from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFVenue

__all__ = ["load_imdf_venues"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_venues(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFVenue]],
) -> None:
    if IMDFFeatureType.venue.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.venue} features")
        for ith_row, venue_row in dataframes[IMDFFeatureType.venue.value].iterrows():
            venue_dict = venue_row.to_dict()

            name = venue_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            display_point = venue_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)
            else:
                display_point = venue_dict["geometry"].representative_point()

            if "id" in venue_dict:
                venue_id = venue_dict.pop("id")
                if venue_id is None:
                    venue_id = next(iter(name.values()))
            else:
                venue_id = next(iter(name.values()))

            venue = IMDFVenue(
                **venue_dict, id=venue_id, name=name, display_point=display_point
            )
            out[IMDFFeatureType.venue].append(venue)
