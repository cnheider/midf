import json
from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFootprint

__all__ = ["load_imdf_footprints"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_footprints(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFFootprint]],
) -> None:
    if IMDFFeatureType.footprint.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.footprint} features")
        for ith_row, footprint_row in dataframes[
            IMDFFeatureType.footprint.value
        ].iterrows():
            footprint_dict = footprint_row.to_dict()

            name = footprint_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            footprint = IMDFFootprint(**footprint_dict, name=name)
            out[IMDFFeatureType.footprint].append(footprint)
