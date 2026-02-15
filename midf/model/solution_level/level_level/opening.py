from dataclasses import dataclass
from typing import Any, List, Optional

import shapely

from midf.enums import (
    IMDFAccessControlCategory,
    IMDFAccessibilityCategory,
    IMDFOpeningCategory,
)
from midf.midf_typing import Labels, MIDFFeature

__all__ = ["MIDFOpening"]


@dataclass
class MIDFOpening(MIDFFeature):
    geometry: shapely.LineString

    category: IMDFOpeningCategory
    accessibility: Optional[List[IMDFAccessibilityCategory]] = None

    access_control: Optional[List[IMDFAccessControlCategory]] = None

    door: Optional[Any] = None

    name: Optional[Labels] = None
    alt_name: Optional[Labels] = None

    display_point: Optional[shapely.Point] = None
