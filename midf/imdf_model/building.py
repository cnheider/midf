import json
import shapely
from typing import Any, Mapping, Optional, Union

from midf.imdf_model.base import IMDFFeature

__all__ = ["IMDFBuilding"]

from ..enums import IMDFBuildingCategory, IMDFFeatureType


class IMDFBuilding(IMDFFeature):
    # geometry: None # Nonsense

    category: Union[
        IMDFBuildingCategory, str
    ]  # May have invalid categories, hence the union with str # TODO: REMOVE FOR STRICT
    restriction: Optional[str] = None
    name: Optional[Mapping[str, str]] = None
    alt_name: Optional[Mapping[str, str]] = None
    display_point: Optional[shapely.Point] = None
    address_id: Optional[str] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.building.value
        out["geometry"] = None
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
