import logging

import geopandas

from sync_module.mi import get_remote_solution, synchronize

logging.basicConfig(level=logging.DEBUG)

solution_name = "Temasek Polytechnic"
chen_customer_id = "953f7a89334a4013927857ab"
venue_name = "Temasek Polytechnic"
file = "data/zips9/thomas_temasek/occupant.geojson"

df = geopandas.read_file(file, engine="fiona")
venue_poly = df.unary_union.convex_hull
solution = get_remote_solution(external_id=solution_name)
# solution = Solution(solution_name, solution_name, customer_id=chen_customer_id)

# venue_key = solution.add_venue(venue_name, venue_name, venue_poly)
# building_key = solution.add_building(venue_name, venue_name, venue_poly, venue_key)
# floor_key = solution.add_floor(0, building_key, venue_key, venue_poly)
for ir, r in df.iterrows():
    # an = 'https://api.8base.com/file/download/ckcnbfq4v000207jo0qx99gu1_Master/{0}?download=true'

    media_key = None
    if len(r["IMAGES"]) > 0:
        # a = "https://cms.point-maps.com/images/{0}"
        image_id = r["IMAGES"][0]
        # b = requests.get(a.format(image_id)).content

        # media_key = solution.add_media(image_id, b, MediaType.jpg)

    solution.update_point_of_interest(
        r["OCCU_ID"],
        description="\n\n".join(
            [
                r["DESCRIPTION"],
                r["EMAIL"],
                r["PHONE"],
                r["HOURS"],
            ]
        ),
        media_key=media_key,
    )

    # break

synchronize(solution)
