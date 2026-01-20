import json
import shapely
from typing import Any, List, Mapping, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFGeofence"]

from ..enums import (
    IMDFAccessibilityCategory,
    IMDFFeatureType,
    IMDFGeofenceCategory,
    IMDFRestrictionCategory,
)
from ..midf_typing import Polygonal


class IMDFGeofence(IMDFFeature):
    geometry: Polygonal
    category: Union[
        IMDFGeofenceCategory, str
    ]  # TODO: Some geofences have a category that is not in the enum, so we allow a # TODO: REMOVE FOR STRICT
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    restriction: Optional[IMDFRestrictionCategory] = None
    accessibility: Optional[IMDFAccessibilityCategory] = None
    correlation_id: Optional[str] = None
    display_point: Optional[shapely.Point] = None
    building_ids: Optional[List[str]] = None
    level_ids: Optional[List[str]] = None
    parents: Optional[List[str]] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.geofence.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
