import json
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFLevel

__all__ = ["load_imdf_levels"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_levels(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFLevel]],
) -> None:
    if IMDFFeatureType.level.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.level} features")
        for ith_row, level_row in dataframes[IMDFFeatureType.level.value].iterrows():
            level_dict = level_row.to_dict()

            name = level_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            short_name = level_dict.pop("short_name")
            if False:
                if short_name is not None:
                    short_name = json.loads(short_name)

            outdoor = level_dict.pop("outdoor")
            if True:
                if not isinstance(outdoor, bool):
                    outdoor = bool(outdoor)

            display_point = level_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            building_ids = level_dict.pop("building_ids")
            if True:
                if building_ids is not None:
                    if isinstance(building_ids, List):
                        ...
                    else:
                        building_ids = [building_ids]

            level = IMDFLevel(
                **level_dict,
                name=name,
                short_name=short_name,
                outdoor=outdoor,
                display_point=display_point,
                building_ids=building_ids,
            )
            out[IMDFFeatureType.level].append(level)
