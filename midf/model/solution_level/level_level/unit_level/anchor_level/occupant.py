from dataclasses import dataclass
from typing import Optional

from midf.enums import IMDFOccupantCategory
from midf.midf_typing import Labels, MIDFFeature, Temporality

__all__ = ["MIDFOccupant"]


@dataclass
class MIDFOccupant(MIDFFeature):
    name: Labels
    category: IMDFOccupantCategory

    hours: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    validity: Optional[Temporality] = None
    correlation_id: Optional[str] = None
