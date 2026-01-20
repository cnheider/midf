from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAnchor

__all__ = ["load_imdf_anchors"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_anchors(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFAnchor]],
) -> None:
    if IMDFFeatureType.anchor.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.anchor} features")
        for ith_row, anchor_row in dataframes[IMDFFeatureType.anchor.value].iterrows():
            anchor_dict = anchor_row.to_dict()

            anchor = IMDFAnchor(**anchor_dict)
            out[IMDFFeatureType.anchor].append(anchor)
