import copy
import logging
from typing import List

import shapely.geometry

from . import fixes

_logger = logging.getLogger(__name__)


def apply_fix(criterium: str, shapely_geom):
    """Applies the correct check for the criteria"""

    return getattr(fixes, f"fix_{criterium}")(shapely_geom)


def process_fix(fc, geometry_validation_results: dict, criteria: List[str]) -> dict:
    fc_copy = copy.deepcopy(fc)
    for criterium in criteria:
        if criterium in geometry_validation_results["invalid"]:
            indices = geometry_validation_results["invalid"][criterium]
        elif criterium in geometry_validation_results["problematic"]:
            indices = geometry_validation_results["problematic"][criterium]
        else:
            continue

        for idx in indices:
            if isinstance(idx, int):
                geometry = fc_copy["features"][idx]["geometry"]
                if geometry["type"] != "Polygon":
                    _logger.info("Currently only fixing polygons, skipping")
                    continue
                geom = shapely.geometry.shape(geometry)
                geom_fixed = apply_fix(criterium, geom)
                fc_copy["features"][idx]["geometry"] = geom_fixed.__geo_interface__

            elif isinstance(idx, dict):  # multitype geometry e.g. idx is {0: [1, 2]}
                if len(idx) == 0:
                    continue

                idx, indices_subgeoms = list(idx.items())[0]

                for idx_subgeom in indices_subgeoms:
                    if not isinstance(idx_subgeom, int):
                        raise TypeError(
                            "Fixing Multigeometries within Multigeometries not supported."
                        )
                    subgeom = shapely.geometry.shape(
                        fc_copy["features"][idx]["geometry"]
                    ).geoms[idx_subgeom]

                    subgeom_fixed = apply_fix(criterium, subgeom)

                    fc_copy["features"][idx]["geometry"][
                        idx_subgeom
                    ] = subgeom_fixed.__geo_interface__

    return fc_copy
