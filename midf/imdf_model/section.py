import json
from typing import Any, Mapping, Optional, Union

import shapely

from .base import IMDFFeature
from ..enums import IMDFFeatureType, IMDFSectionCategory

__all__ = ["IMDFSection"]

from ..midf_typing import Polygonal


class IMDFSection(IMDFFeature):
    geometry: Polygonal

    category: Union[
        IMDFSectionCategory, str
    ]  # TODO: Some sections have a category that is not in the enum, so we allow a
    # string here, but we should validate it, it is not valid, we should raise an error. # TODO: REMOVE FOR
    #  STRICT
    restriction: Any = None
    accessibility: Any = None
    address_id: Any = None
    correlation_id: Any = None
    parents: Any = None
    level_id: str = None
    display_point: Optional[shapely.Point] = None
    alt_name: Optional[Mapping[str, str]] = None
    name: Optional[Mapping[str, str]] = None

    def to_imdf_spec_feature(self) -> dict[str, Any]:
        out = self.model_dump()

        out["feature_type"] = IMDFFeatureType.section.value
        if False:
            out["geometry"] = json.loads(shapely.to_geojson(out.pop("geometry")))
        if True:
            if out["display_point"] is not None:
                out["display_point"] = json.loads(
                    shapely.to_geojson(out.pop("display_point"))
                )

        return out
