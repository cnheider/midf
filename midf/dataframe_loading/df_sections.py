import json
import logging
import uuid
from typing import List, Mapping

import shapely
from pandas import DataFrame

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFSection

_logger = logging.getLogger(__name__)

__all__ = ["load_imdf_sections"]


def load_imdf_sections(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFSection]],
) -> None:
    if IMDFFeatureType.section.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.section} features")

        for ith_row, section_row in dataframes[
            IMDFFeatureType.section.value
        ].iterrows():
            section_dict = section_row.to_dict()

            name = section_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = section_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            section_id = section_dict.pop("id")
            if True:
                if section_id is not None:
                    ...
                    # section_id = str(section_id)
                else:
                    _logger.error(
                        f"section_id is None, generating a new one"
                        # f"{section_row}"
                    )
                    section_id = uuid.uuid4().hex

            display_point = section_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            section = IMDFSection(
                **section_dict,
                id=section_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )
            out[IMDFFeatureType.section].append(section)
