from dataclasses import dataclass
from typing import Collection, Optional

import shapely

from midf.midf_typing import Labels, MIDFFeature
from .address import MIDFAddress
from .level_level import MIDFUnit

__all__ = ["MIDFAmenity"]

from ...enums import IMDFAmenityCategory


@dataclass
class MIDFAmenity(MIDFFeature):
    geometry: shapely.Point
    category: IMDFAmenityCategory
    units: Collection[MIDFUnit]

    accessibility: Optional[str] = None
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
    hours: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    correlation_id: Optional[str] = None

    address: Optional[MIDFAddress] = None
