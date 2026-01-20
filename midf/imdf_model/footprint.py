import json
import shapely
from typing import Any, List, Mapping, Optional

from .base import IMDFFeature

__all__ = ["IMDFFootprint"]

from ..enums import IMDFFeatureType, IMDFFootprintCategory
from ..midf_typing import Polygonal


class IMDFFootprint(IMDFFeature):
    geometry: Polygonal
    category: IMDFFootprintCategory
    name: Optional[Mapping[str, str]] = None
    building_ids: Optional[List[str]] = (
        None  # TODO: SHOULD NOT BE NULLABLE! # TODO: REMOVE FOR STRICT
    )

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.footprint.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        return out
