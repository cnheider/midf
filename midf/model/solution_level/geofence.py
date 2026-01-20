import shapely
from dataclasses import dataclass
from typing import List, Optional

from midf.midf_typing import Labels, MIDFFeature, Polygonal
from .building import MIDFBuilding
from .level import MIDFLevel

__all__ = ["MIDFGeofence"]

from ...enums import IMDFGeofenceCategory


@dataclass
class MIDFGeofence(MIDFFeature):
    geometry: Polygonal

    category: IMDFGeofenceCategory
    restriction: Optional[str] = None
    accessibility: Optional[List[str]] = None

    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None

    correlation_id: Optional[str] = None
    display_point: Optional[shapely.Point] = None

    buildings: Optional[List[MIDFBuilding]] = None
    levels: Optional[List[MIDFLevel]] = None
    parents: Optional[List["MIDFGeofence"]] = None
