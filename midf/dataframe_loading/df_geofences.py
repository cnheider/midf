import json

import shapely
from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFGeofence

__all__ = ["load_imdf_geofences"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_geofences(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFGeofence]],
) -> None:
    if IMDFFeatureType.geofence.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.geofence} features")
        for ith_row, geofence_row in dataframes[
            IMDFFeatureType.geofence.value
        ].iterrows():
            geofence_dict = geofence_row.to_dict()

            display_point = geofence_dict.pop("display_point")
            if display_point is not None:
                a = json.dumps(display_point)

                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(a)
                else:
                    display_point = shapely.from_geojson(display_point)

            geofence = IMDFGeofence(**geofence_dict, display_point=display_point)
            out[IMDFFeatureType.geofence].append(geofence)
