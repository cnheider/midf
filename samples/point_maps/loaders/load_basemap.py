from pathlib import Path

import geopandas
import logging
import shapely

# from jord.qlive_utilities import AutoQliveClient
from jord.shapely_utilities import clean_shape
from sync_module.mi import synchronize
from sync_module.model import Solution

# file_path = (    Path(__file__).parent / "data" / "auxiliary_data" / "SIT" / "basemap.geojson")
file_path = Path(__file__).parent / "data" / "VitraCampus" / "basemap.geojson"

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

df = geopandas.read_file(file_path, engine="fiona")

# with AutoQliveClient(address="tcp://localhost:5555") as qlive:

solution_name = "Vitra Basemap"
chen_customer_id = "953f7a89334a4013927857ab"

BASEMAP_ID_PREFIX = "Basemap"

solution = Solution(solution_name, solution_name, _customer_id=chen_customer_id)

venue_poly = df.unary_union.convex_hull

venue_key = solution.add_venue(BASEMAP_ID_PREFIX, BASEMAP_ID_PREFIX, venue_poly)
building_key = solution.add_building(
    BASEMAP_ID_PREFIX, BASEMAP_ID_PREFIX, polygon=venue_poly, venue_key=venue_key
)
floor_key = solution.add_floor(
    0, building_key=building_key, name=BASEMAP_ID_PREFIX, polygon=venue_poly
)

for ith, row in df.iterrows():
    category = row["CATEGORY"]
    g = row["geometry"]
    bid = f"{BASEMAP_ID_PREFIX}_{ith}"

    if isinstance(g, shapely.Polygon):
        solution.add_area(bid, category, polygon=clean_shape(g), floor_key=floor_key)
    elif isinstance(g, shapely.MultiPolygon):
        for jth, g_ in enumerate(g.geoms):
            solution.add_area(
                f"{bid}_{jth}", category, polygon=clean_shape(g_), floor_key=floor_key
            )
    else:
        _logger.error(f"Unexpected geometry type: {type(g)}")
        # raise ValueError(f'Unexpected geometry type: {type(g)}')

    # qlive.add_shapely_geometry(g)

synchronize(solution)
