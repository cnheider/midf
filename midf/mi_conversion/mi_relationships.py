import logging
import uuid
from itertools import count

from midf.enums import IMDFRelationshipCategory
from midf.imdf_model.opening import IMDFDirection
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFRelationship, MIDFSolution, MIDFUnit
from sync_module.model import Area, Connector, Room, Solution
from sync_module.shared import MIConnectionType

_logger = logging.getLogger(__name__)

__all__ = ["convert_relationships"]


def convert_relationships(
    mi_solution: Solution, midf_solution: MIDFSolution, venue_graph_key: str
) -> None:
    """

    :param mi_solution:
    :type mi_solution:
    :param midf_solution:
    :type midf_solution:
    :param venue_graph_key:
    :type venue_graph_key:
    :return:
    :rtype:
    """
    if midf_solution.relationships:
        id_counter = iter(count())
        for relationship in midf_solution.relationships:
            relationship: MIDFRelationship

            category_ = relationship.category
            connection_type = MIConnectionType.elevator
            if category_ == IMDFRelationshipCategory.elevator:
                connection_type = MIConnectionType.elevator
            elif category_ == IMDFRelationshipCategory.escalator:
                connection_type = MIConnectionType.escalator
            elif category_ == IMDFRelationshipCategory.stairs:
                connection_type = MIConnectionType.steps
            elif category_ == IMDFRelationshipCategory.ramp:
                connection_type = MIConnectionType.ramp
            elif category_ == IMDFRelationshipCategory.moving_walkway:
                continue
                connection_type = MIConnectionType.escalator  # skip?
            elif category_ == IMDFRelationshipCategory.traversal:
                continue
                connection_type = MIConnectionType.wheel_chair_ramp
            elif category_ == IMDFRelationshipCategory.traversal_path:
                continue
                connection_type = MIConnectionType.wheel_chair_lift
            else:
                _logger.warning(f"Unknown relationship category {category_}")

            if (
                relationship.direction == IMDFDirection.directed
            ):  # TODO: Directed relationships are not supported,
                # so we skip them for now.
                _logger.error(
                    f"Directed relationships are not supported {relationship}"
                )
                ...

            origin_room = mi_solution.rooms.get(
                key=Room.compute_key(admin_id=clean_admin_id(relationship.origin.id))
            )
            if not origin_room:
                _logger.error(f"Origin room not found for relationship {relationship}")
                if mi_solution.areas.get(
                    key=Area.compute_key(
                        admin_id=clean_admin_id(relationship.origin.id)
                    )
                ):
                    _logger.error(f"Origin area found for relationship {relationship}")
                continue

            connectors = [
                Connector(
                    uuid.uuid4().hex,
                    floor_index=origin_room.floor.floor_index,
                    point=relationship.origin.geometry.representative_point(),
                ),
            ]

            if relationship.intermediary:
                for unit in relationship.intermediary:
                    if not isinstance(unit, MIDFUnit):
                        _logger.error(f"Intermediary is not a unit {unit}")
                        continue

                    in_room = mi_solution.rooms.get(
                        key=Room.compute_key(admin_id=clean_admin_id(unit.id))
                    )

                    if not in_room:
                        _logger.error(
                            f"Intermediary room not found for relationship {relationship}"
                        )
                        if mi_solution.areas.get(
                            key=Area.compute_key(admin_id=clean_admin_id(unit.id))
                        ):
                            _logger.error(
                                f"Intermediary area found for relationship {relationship}"
                            )
                        continue

                    connectors.append(
                        Connector(
                            uuid.uuid4().hex,
                            floor_index=in_room.floor.floor_index,
                            point=unit.geometry.representative_point(),
                        )
                    )

            if relationship.destination is None:
                if True:
                    continue

            destination_room = mi_solution.rooms.get(
                key=Room.compute_key(
                    admin_id=clean_admin_id(relationship.destination.id)
                )
            )

            if not destination_room:
                _logger.error(
                    f"Destination room not found for relationship {relationship}"
                )
                if mi_solution.areas.get(
                    key=Area.compute_key(
                        admin_id=clean_admin_id(relationship.destination.id)
                    )
                ):
                    _logger.error(
                        f"Destination area found for relationship {relationship}"
                    )
                continue

            connectors.append(
                Connector(
                    uuid.uuid4().hex,
                    floor_index=destination_room.floor.floor_index,
                    point=relationship.origin.geometry.representative_point(),
                )
            )

            mi_solution.add_connection(
                next(id_counter),
                graph_key=venue_graph_key,
                connection_type=connection_type,
                connectors=connectors,
            )
