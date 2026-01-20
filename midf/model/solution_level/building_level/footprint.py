from dataclasses import dataclass
from typing import Collection

from midf.enums import IMDFFootprintCategory
from midf.midf_typing import Labels, MIDFFeature, Polygonal
from ..building import MIDFBuilding

__all__ = ["MIDFFootprint"]


@dataclass
class MIDFFootprint(MIDFFeature):
    geometry: Polygonal
    category: IMDFFootprintCategory
    name: Labels
    buildings: Collection[MIDFBuilding]
