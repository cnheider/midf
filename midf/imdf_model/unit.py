import json
from typing import Any, Mapping, Optional, Union

import shapely

from .base import IMDFFeature
from ..enums import (
    IMDFAccessibilityCategory,
    IMDFFeatureType,
    IMDFRestrictionCategory,
    IMDFUnitCategory,
)

__all__ = ["IMDFUnit"]

from ..midf_typing import Polygonal


class IMDFUnit(IMDFFeature):
    geometry: Polygonal
    level_id: str

    category: Union[
        IMDFUnitCategory, str
    ]  # TODO: Some sections have a category that is not in the enum, so we allow a #
    # TODO: REMOVE FOR STRICT
    restriction: Optional[Union[IMDFRestrictionCategory, str]] = (
        None  # TODO: Some sections have a category that is not in the enum,
    )
    # so we allow a #
    # TODO: REMOVE FOR STRICT
    accessibility: Optional[Union[IMDFAccessibilityCategory, str]] = (
        None  # TODO: Some sections have a category that is not in the enum,
    )
    # so we allow a #
    # TODO: REMOVE FOR STRICT

    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.unit.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
