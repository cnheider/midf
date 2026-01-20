import json
import shapely
from typing import Any

from .base import IMDFFeature

__all__ = ["IMDFAnchor"]

from ..enums import IMDFFeatureType


class IMDFAnchor(IMDFFeature):
    geometry: shapely.Point
    address_id: Any = None
    unit_id: str = ""

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.anchor.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        return out
