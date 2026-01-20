import json
import shapely
from typing import Any, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFKiosk"]

from ..enums import IMDFFeatureType
from ..midf_typing import Polygonal


class IMDFKiosk(IMDFFeature):
    geometry: Polygonal

    alt_name: Optional[Mapping[str, str]] = None
    name: Optional[Mapping[str, str]] = None
    anchor_id: Optional[str] = None
    level_id: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.kiosk.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
