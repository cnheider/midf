from dataclasses import dataclass
from typing import Collection, Optional

from .solution_level import (
    MIDFAddress,
    MIDFAmenity,
    MIDFBuilding,
    MIDFFootprint,
    MIDFGeofence,
    MIDFLevel,
    MIDFManifest,
    MIDFRelationship,
)

__all__ = ["MIDFSolution"]


@dataclass
class MIDFSolution:
    manifest: MIDFManifest

    addresses: Optional[Collection[MIDFAddress]] = None
    levels: Optional[Collection[MIDFLevel]] = None
    buildings: Optional[Collection[MIDFBuilding]] = None
    relationships: Optional[Collection[MIDFRelationship]] = None
    geofences: Optional[Collection[MIDFGeofence]] = None
    footprints: Optional[Collection[MIDFFootprint]] = None
    amenities: Optional[Collection[MIDFAmenity]] = None
