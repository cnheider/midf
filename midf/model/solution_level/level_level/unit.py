from dataclasses import dataclass
from typing import Collection, List, Optional

from midf.enums import IMDFUnitCategory
from midf.midf_typing import Labels, MIDFFeature, Polygonal
from .unit_level import MIDFAnchor

__all__ = ["MIDFUnit"]


@dataclass
class MIDFUnit(MIDFFeature):
    geometry: Polygonal
    category: IMDFUnitCategory
    anchors: Optional[Collection[MIDFAnchor]] = None
    restriction: Optional[str] = None
    accessibility: Optional[List[str]] = None
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
