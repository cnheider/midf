import json
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFOpening
from midf.imdf_model.opening import IMDFDoor

__all__ = ["load_imdf_openings"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_openings(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFOpening]],
) -> None:
    if IMDFFeatureType.opening.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.opening} features")
        for ith_row, opening_row in dataframes[
            IMDFFeatureType.opening.value
        ].iterrows():
            opening_dict = opening_row.to_dict()

            name = opening_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = opening_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            display_point = opening_dict.pop("display_point")
            if display_point is not None:
                a = json.dumps(display_point)

                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(a)
                else:
                    display_point = shapely.from_geojson(display_point)

            door = opening_dict.pop("door")
            if door is not None:
                if isinstance(door, str):
                    door = json.loads(door)
                else:
                    ...
                door = IMDFDoor(**door)

            opening = IMDFOpening(
                **opening_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
                door=door,
            )
            out[IMDFFeatureType.opening].append(opening)
