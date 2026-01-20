from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAmenity

__all__ = ["load_imdf_amenities"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_amenities(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFAmenity]],
) -> None:
    if IMDFFeatureType.amenity.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.amenity} features")
        for ith_row, amenity_row in dataframes[
            IMDFFeatureType.amenity.value
        ].iterrows():
            amenity_dict = amenity_row.to_dict()

            amenity = IMDFAmenity(**amenity_dict)
            out[IMDFFeatureType.amenity].append(amenity)
