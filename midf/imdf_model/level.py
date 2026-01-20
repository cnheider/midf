import json
import shapely
from typing import Any, Dict, List, Optional, Union

from .base import IMDFFeature

__all__ = ["IMDFLevel"]

from ..enums import IMDFFeatureType, IMDFLevelCategory
from ..midf_typing import Polygonal


class IMDFLevel(IMDFFeature):
    geometry: Polygonal

    name: dict[str, str]
    short_name: Dict[str, str]
    category: Union[
        IMDFLevelCategory, str
    ]  # TODO: Some levels have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT

    outdoor: bool = False  # SOME SANE DEFAULT IN CASE OF SHIT DATA
    ordinal: int = 0  # SOME SANE DEFAULT IN CASE OF SHIT DATA

    restriction: Optional[str] = None
    display_point: Optional[shapely.Point] = None
    address_id: Optional[str] = None
    building_ids: Optional[List[str]] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.level.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
