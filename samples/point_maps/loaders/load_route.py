import json
import logging
from itertools import count
from pathlib import Path

import osmnx
import pyproj
import shapely
from networkx import MultiDiGraph


from jord.networkx_utilities import assertive_add_shapely_node, assertive_add_edge
from warg import recursive_flatten

_logger = logging.getLogger(__name__)


def save_graph(new_graph: MultiDiGraph, save_path: Path) -> None:
    new_graph.graph["crs"] = pyproj.CRS.from_user_input("EPSG:4326")

    edge_tags = set(
        recursive_flatten([edge.keys() for edge in new_graph.edges.values()])
    )
    node_tags = set(
        recursive_flatten([node.keys() for node in new_graph.nodes.values()])
    )

    osmnx.settings.useful_tags_way = edge_tags
    osmnx.settings.useful_tags_node = node_tags

    osmnx.save_graph_xml(
        new_graph,
        filepath=save_path,
    )


def parse_route(route_file_path: Path, target_file_path: Path) -> MultiDiGraph:
    assert route_file_path.exists()
    assert route_file_path.is_file()
    assert route_file_path.suffix == ".json"

    osmnx.settings.all_oneway = True

    with open(route_file_path) as route_file:
        route_dict = json.load(route_file)

        coordinates = route_dict["coordinates"]
        links = route_dict["links"]
        level_coords = route_dict["level_coords"]

        coordinate_levels = {i: None for i in range(len(coordinates))}
        for level_index, (from_idx, num) in level_coords.items():
            for i in range(from_idx, from_idx + num):
                assert coordinate_levels[i] is None
                coordinate_levels[i] = level_index

        assert all(coordinate_levels.values())

        graph = MultiDiGraph()

        node_id_offset = 1

        for i, coords in enumerate(coordinates):
            assertive_add_shapely_node(
                graph=graph,
                u=i + node_id_offset,
                point=shapely.Point(coords),
                level=coordinate_levels[i],
            )

        edge_id_counter = iter(count())
        if node_id_offset:  # OSM does not like 0 as id
            next(edge_id_counter)
        for i, edges in enumerate(links):
            for edge in edges:
                to_distance = edge["d"]
                to_link = edge["i"]

                # assert isinstance(to_distance, float), f'{to_distance} was not a float'
                assert isinstance(to_link, int), f"{to_link} was not an int"

                if i != to_link:
                    edge_id = next(edge_id_counter)
                    assertive_add_edge(
                        graph=graph,
                        u=int(i + node_id_offset),
                        v=int(to_link + node_id_offset),
                        key=edge_id,
                        attributes=dict(
                            # distance=to_distance,
                            level=coordinate_levels[i],
                            id=edge_id,
                        ),
                        allow_loops=False,
                        allow_duplicates=False,
                    )
                else:
                    _logger.error(f"Loop detected {i, to_link}")
        if True:
            save_graph(graph, target_file_path)

        return graph


if __name__ == "__main__":
    parse_route(Path(__file__).parent / "data" / "Routes.json")
