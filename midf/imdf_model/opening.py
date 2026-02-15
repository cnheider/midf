import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Union

import shapely

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from .base import IMDFFeature
from ..enums import (
    IMDFAccessControlCategory,
    IMDFAccessibilityCategory,
    IMDFDoorCategory,
    IMDFDoorMaterial,
    IMDFFeatureType,
    IMDFOpeningCategory,
)

__all__ = ["IMDFOpening", "IMDFDirection", "IMDFDoor"]


class IMDFDirection(StrEnum):
    directed = "directed"
    undirected = "undirected"


@dataclass
class IMDFDoor:
    type: Optional[IMDFDoorCategory] = None
    automatic: Optional[bool] = None
    material: Optional[IMDFDoorMaterial] = None


class IMDFOpening(IMDFFeature):
    geometry: shapely.LineString
    category: Union[
        IMDFOpeningCategory, str
    ]  # TODO: Some openings have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    level_id: str

    accessibility: Optional[IMDFAccessibilityCategory] = None
    access_control: Optional[IMDFAccessControlCategory] = None
    door: Optional[IMDFDoor] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.opening.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
