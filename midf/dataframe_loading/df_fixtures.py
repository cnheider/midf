import json
import logging
import shapely
import uuid
from pandas import DataFrame
from typing import List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFixture

__all__ = ["load_imdf_fixtures"]

_logger = logging.getLogger(__name__)


def load_imdf_fixtures(
    dataframes: Mapping[str, DataFrame],
    out: Mapping[IMDFFeatureType, List[IMDFFixture]],
) -> None:
    if IMDFFeatureType.fixture.value in dataframes:
        _logger.error(f"Loading {IMDFFeatureType.fixture} features")

        for ith_row, fixture_row in dataframes[
            IMDFFeatureType.fixture.value
        ].iterrows():
            fixture_dict = fixture_row.to_dict()

            name = fixture_dict.pop("name")
            if False:
                if name is not None:
                    name = json.loads(name)

            alt_name = fixture_dict.pop("alt_name")
            if False:
                if alt_name is not None:
                    alt_name = json.loads(alt_name)

            fixture_id = fixture_dict.pop("id")
            if True:
                if fixture_id is not None:
                    ...
                    # fixture_id = str(fixture_id)
                else:
                    _logger.error(
                        f"fixture_id is None, generating a new one"
                        # f"{fixture_row}"
                    )
                    fixture_id = uuid.uuid4().hex

            display_point = fixture_dict.pop("display_point")
            if display_point is not None:
                if isinstance(display_point, dict):
                    display_point = shapely.from_geojson(json.dumps(display_point))
                else:
                    display_point = shapely.from_geojson(display_point)

            fixture = IMDFFixture(
                **fixture_dict,
                id=fixture_id,
                name=name,
                alt_name=alt_name,
                display_point=display_point,
            )

            out[IMDFFeatureType.fixture].append(fixture)
