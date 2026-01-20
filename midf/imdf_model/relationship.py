import json
import shapely
from typing import Any, List, Optional

from .base import IMDFFeature, IMDFFeatureReference
from ..enums import IMDFFeatureType, IMDFRelationshipCategory

__all__ = ["IMDFRelationship"]

from .opening import IMDFDirection


class IMDFRelationship(IMDFFeature):
    category: IMDFRelationshipCategory
    direction: IMDFDirection
    origin: Optional[IMDFFeatureReference] = None
    intermediary: Optional[List[IMDFFeatureReference]] = None
    destination: Optional[IMDFFeatureReference] = None
    hours: Any = None  # Actual type HOURS
    geometry: Optional[shapely.geometry.base.BaseGeometry] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.relationship.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        return out
