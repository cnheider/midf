import shapely
from dataclasses import dataclass
from typing import Optional

from midf.enums import IMDFVenueCategory
from midf.midf_typing import Labels, MIDFFeature, Polygonal

__all__ = ["MIDFVenue"]


@dataclass
class MIDFVenue(MIDFFeature):
    geometry: Polygonal
    category: IMDFVenueCategory

    name: Labels

    display_point: shapely.Point

    restriction: Optional[str] = None
    alt_name: Optional[Labels] = None
    hours: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
