import shapely
from typing import Optional

__all__ = ["convert_display_point"]

import geopandas


def convert_display_point(v: geopandas.GeoSeries) -> Optional[shapely.geometry.Point]:
    """
    DISPLAY_PO
    DISPLAY__1
    DISPLAY__2

    :param v:
    :return:
    """

    if "DISPLAY_POINT" in v:
        if v["DISPLAY_POINT"] is not None:
            return shapely.from_geojson(str(v["DISPLAY_POINT"]).replace("'", '"'))

    else:
        if v.geometry:
            return v.geometry.representative_point()

    return None
