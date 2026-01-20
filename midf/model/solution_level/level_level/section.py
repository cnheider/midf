import shapely
from dataclasses import dataclass
from typing import List, Optional

from midf.enums import IMDFSectionCategory
from midf.midf_typing import Labels, MIDFFeature, Polygonal
from ..address import MIDFAddress

__all__ = ["MIDFSection"]


@dataclass
class MIDFSection(MIDFFeature):
    geometry: Polygonal
    category: IMDFSectionCategory

    restriction: Optional[str] = None
    accessibility: Optional[List[str]] = None
    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None
    display_point: Optional[shapely.Point] = None
    correlation_id: Optional[str] = None

    address: Optional[MIDFAddress] = None
    parents: Optional[List["MIDFSection"]] = None
