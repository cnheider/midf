from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFRelationship

__all__ = ["load_imdf_relationships"]

import logging

_logger = logging.getLogger(__name__)


def load_imdf_relationships(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFRelationship]],
) -> None:
    if IMDFFeatureType.relationship.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.relationship} features")
        for ith_row, relationship_row in dataframes[
            IMDFFeatureType.relationship.value
        ].iterrows():
            relationship_dict = relationship_row.to_dict()

            destination = relationship_dict.pop("destination")
            origin = relationship_dict.pop("origin")
            intermediary = relationship_dict.pop("intermediary")

            try:
                relationship = IMDFRelationship(
                    **relationship_dict,
                    destination=destination,
                    origin=origin,
                    intermediary=intermediary,
                )
                out[IMDFFeatureType.relationship].append(relationship)
            except Exception as e:
                _logger.error(
                    f"Error loading {IMDFFeatureType.relationship} features: {e}"
                )
