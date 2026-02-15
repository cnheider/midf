import json
from typing import Any, Optional, Union

import shapely

from .base import IMDFFeature

__all__ = ["IMDFVenue"]

from ..enums import IMDFFeatureType, IMDFVenueCategory
from ..midf_typing import Labels, Polygonal


class IMDFVenue(IMDFFeature):
    geometry: Polygonal
    name: Labels  # Language:Value # { ""en"": ""Kansas City International Airport"" }"
    address_id: str  # 984eb70b-da05-4ed7-809b-4d0e169f5d29
    display_point: shapely.Point
    category: Union[
        IMDFVenueCategory, str
    ]  # TODO: Some venue have a category that is not in the enum, so we allow a # TODO: REMOVE FOR STRICT
    hours: Optional[str] = None  # 24/7
    website: Optional[str] = None  # https://www.flykci.com/
    phone: Optional[str] = None  # +1-816-243-5237
    restriction: Optional[Any] = None
    alt_name: Optional[Labels] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.venue.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
