import json
from typing import Any, List, Mapping, Optional, Union

import shapely

from .base import IMDFFeature

__all__ = ["IMDFAmenity"]

from ..enums import IMDFAccessibilityCategory, IMDFAmenityCategory, IMDFFeatureType


class IMDFAmenity(IMDFFeature):
    geometry: shapely.Point
    unit_ids: Optional[List[str]] = None  # TODO: SHOULD NOT BE NULLABLE!
    category: Union[
        IMDFAmenityCategory, str
    ]  # TODO: Some amenity have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    accessibility: Optional[Union[IMDFAccessibilityCategory, str]] = (
        None  # TODO: Some amenity have a category that is not in the enum,
    )
    # so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    hours: Any = None
    phone: Any = None
    website: Any = None

    address_id: Optional[str] = None
    correlation_id: Optional[str] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.amenity.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        return out
