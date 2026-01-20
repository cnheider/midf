import json
import logging
import shapely
from typing import Any, Mapping, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFFixture"]

from ..enums import IMDFFeatureType, IMDFFixtureCategory
from ..midf_typing import Polygonal

_logger = logging.getLogger(__name__)


class IMDFFixture(IMDFFeature):
    geometry: Polygonal
    level_id: str

    category: Union[
        IMDFFixtureCategory, str
    ]  # TODO: Some fixtures have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    anchor_id: Any = None

    display_point: Optional[shapely.Point] = None

    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.fixture.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        if True:
            if out["display_point"] is not None:
                display_point = out.pop("display_point")
                if not display_point.is_empty:
                    out["display_point"] = json.loads(shapely.to_geojson(display_point))
                else:
                    _logger.error(f"{display_point} was empty, remains None in out")

        return out
