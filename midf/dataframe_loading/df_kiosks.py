from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFKiosk

__all__ = ["load_imdf_kiosks"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_kiosks(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFKiosk]],
) -> None:
    if IMDFFeatureType.kiosk.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.kiosk} features")
        for ith_row, kiosk_row in dataframes[IMDFFeatureType.kiosk.value].iterrows():
            kiosk_dict = kiosk_row.to_dict()

            kiosk = IMDFKiosk(**kiosk_dict)
            out[IMDFFeatureType.kiosk].append(kiosk)
