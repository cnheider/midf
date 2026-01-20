__all__ = ["convert_footprints"]

import logging
from typing import List, Mapping

from midf.model import MIDFBuilding, MIDFFootprint, MIDFSolution

_logger = logging.getLogger(__name__)


def convert_footprints(
    building_footprint_mapping: Mapping[str, List[MIDFFootprint]],
    midf_solution: MIDFSolution,
) -> None:
    for footprint in midf_solution.footprints:
        footprint: MIDFFootprint
        for building in footprint.buildings:
            building: MIDFBuilding
            building_footprint_mapping[building.id].append(footprint)
