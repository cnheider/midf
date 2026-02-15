import json
from typing import List, Mapping

from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFOccupant
from midf.midf_typing import Temporality

__all__ = ["load_imdf_occupants"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_occupants(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFOccupant]],
) -> None:
    if IMDFFeatureType.occupant.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.occupant} features")

        for ith_row, occupant_row in dataframes[
            IMDFFeatureType.occupant.value
        ].iterrows():
            occupant_dict = occupant_row.to_dict()

            name = occupant_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            if "validity" in occupant_dict:
                validity = occupant_dict.pop("validity")
                if validity is not None:
                    validity = Temporality(**json.loads(validity))
            else:
                validity = None

            occupant = IMDFOccupant(**occupant_dict, name=name, validity=validity)
            out[IMDFFeatureType.occupant].append(occupant)
