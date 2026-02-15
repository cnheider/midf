from dataclasses import dataclass
from typing import List, Optional

import shapely

from midf.enums import IMDFRelationshipCategory
from midf.imdf_model.opening import IMDFDirection
from midf.midf_typing import MIDFFeature

__all__ = ["MIDFRelationship"]


@dataclass
class MIDFRelationship(MIDFFeature):
    """
      A relationship feature is a feature that describes a relationship between two or more other features.

      Example of a relationship feature:

      {
    "id": "11111111-1111-1111-1111-111111111111",
    "type": "Feature",
    "feature_type": "relationship",
    "geometry": null,
    "properties": {
      "category": "traversal",
      "direction": "directed",
      "hours": null,
      "origin": {
        "id": "22222222-2222-2222-2222-222222222222",
        "feature_type": "unit"
      },
      "intermediary": [{
        "id": "33333333-3333-3333-3333-333333333333",
        "feature_type": "opening"
      }],
      "destination": {
        "id": "44444444-4444-4444-4444-444444444444",
        "feature_type": "unit"
      }
    }
    }

    """

    category: IMDFRelationshipCategory
    direction: IMDFDirection

    geometry: Optional[shapely.geometry.base.BaseGeometry] = None
    origin: Optional[MIDFFeature] = None
    intermediary: Optional[List[MIDFFeature]] = None
    destination: Optional[MIDFFeature] = None

    hours: Optional[str] = None
