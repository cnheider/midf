from dataclasses import dataclass
from typing import Collection, Optional

from midf.midf_typing import Labels, MIDFFeature, Polygonal
from .address import MIDFAddress
from .building import MIDFBuilding
from .level_level import (
    MIDFDetail,
    MIDFFixture,
    MIDFKiosk,
    MIDFOpening,
    MIDFSection,
    MIDFUnit,
)

__all__ = ["MIDFLevel"]

from ...enums import IMDFLevelCategory


@dataclass
class MIDFLevel(MIDFFeature):
    geometry: Polygonal
    category: IMDFLevelCategory
    outdoor: bool
    ordinal: int

    name: Labels
    short_name: Labels

    restriction: Optional[str] = None
    address: Optional[MIDFAddress] = None

    buildings: Optional[Collection[MIDFBuilding]] = None

    sections: Optional[Collection[MIDFSection]] = None
    kiosks: Optional[Collection[MIDFKiosk]] = None
    fixtures: Optional[Collection[MIDFFixture]] = None
    openings: Optional[Collection[MIDFOpening]] = None
    units: Optional[Collection[MIDFUnit]] = None
    details: Optional[Collection[MIDFDetail]] = None
