import json
import shapely
from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFBuilding

__all__ = ["load_imdf_buildings"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_buildings(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFBuilding]],
) -> None:
    if IMDFFeatureType.building.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.building} features")
        for ith_row, building_row in dataframes[
            IMDFFeatureType.building.value
        ].iterrows():
            building_dict = building_row.to_dict()

            name = building_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = building_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            display_point = building_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            building = IMDFBuilding(
                **building_dict,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )

            out[IMDFFeatureType.building].append(building)
