import json
import shapely
from typing import Any

from .base import IMDFFeature

__all__ = ["IMDFDetail"]

from ..enums import IMDFFeatureType

from ..midf_typing import Lineal


class IMDFDetail(IMDFFeature):
    level_id: str
    geometry: Lineal

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.detail.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))

        return out
