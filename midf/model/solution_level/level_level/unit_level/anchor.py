from dataclasses import dataclass
from typing import Collection, Optional

import shapely

from midf.midf_typing import MIDFFeature
from .anchor_level import MIDFOccupant
from ...address import MIDFAddress

__all__ = ["MIDFAnchor"]


@dataclass
class MIDFAnchor(MIDFFeature):
    geometry: shapely.Point
    address: Optional[MIDFAddress] = None
    occupants: Optional[Collection[MIDFOccupant]] = None
