import shapely
from dataclasses import dataclass
from typing import Optional

from midf.midf_typing import Labels, MIDFFeature, Polygonal
from .unit_level import MIDFAnchor

__all__ = ["MIDFKiosk"]


@dataclass
class MIDFKiosk(MIDFFeature):
    geometry: Polygonal
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
    display_point: Optional[shapely.Point] = None

    anchor: Optional[MIDFAnchor] = None
