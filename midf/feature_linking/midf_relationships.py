from typing import Collection, Mapping, Optional

from midf.enums import IMDFFeatureType
from midf.imdf_model import (
    IMDFAddress,
    IMDFAmenity,
    IMDFAnchor,
    IMDFBuilding,
    IMDFDetail,
    IMDFFeature,
    IMDFFixture,
    IMDFFootprint,
    IMDFGeofence,
    IMDFKiosk,
    IMDFLevel,
    IMDFOccupant,
    IMDFOpening,
    IMDFRelationship,
    IMDFSection,
    IMDFUnit,
)
from midf.midf_typing import MIDFFeature
from midf.model import MIDFRelationship

__all__ = ["link_relationships"]

import logging

_logger = logging.getLogger(__name__)


def resolve_feature_reference(
    relationship,  #:Dict[str, Any],
    *,
    levels: Mapping[str, IMDFLevel],
    geofences: Mapping[str, IMDFGeofence],
    amenities: Mapping[str, IMDFAmenity],
    buildings: Mapping[str, IMDFBuilding],
    footprints: Mapping[str, IMDFFootprint],
    addresses: Mapping[str, IMDFAddress],
    kiosks: Mapping[str, IMDFKiosk],
    openings: Mapping[str, IMDFOpening],
    sections: Mapping[str, IMDFSection],
    units: Mapping[str, IMDFUnit],
    anchors: Mapping[str, IMDFAnchor],
    occupants: Mapping[str, IMDFOccupant],
    fixtures: Mapping[str, IMDFFixture],
    details: Mapping[str, IMDFDetail],
) -> Optional[MIDFFeature]:
    """
    If the relationship is not None, return the feature that the relationship points to.
    else, return None.

    :param relationship:
    :param levels:
    :param geofences:
    :param amenities:
    :param buildings:
    :param footprints:
    :param addresses:
    :param kiosks:
    :param openings:
    :param sections:
    :param units:
    :param anchors:
    :param occupants:
    :param fixtures:
    :return:
    """
    if relationship:
        result = None
        if relationship.feature_type == IMDFFeatureType.level:
            result = levels.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.geofence:
            result = geofences.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.amenity:
            result = amenities.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.building:
            result = buildings.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.footprint:
            result = footprints.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.address:
            result = addresses.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.kiosk:
            result = kiosks.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.opening:
            result = openings.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.section:
            result = sections.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.unit:
            result = units.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.anchor:
            result = anchors.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.occupant:
            result = occupants.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.fixture:
            result = fixtures.get(relationship.id)
        elif relationship.feature_type == IMDFFeatureType.detail:
            result = details.get(relationship.id)
        else:
            _logger.error(f"Unknown feature type {relationship.feature_type}")

        if result is None:
            _logger.error(f"Could not resolve feature reference {relationship}")

        return result
    return None


def link_relationships(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    *,
    levels: Mapping[str, IMDFLevel],
    geofences: Mapping[str, IMDFGeofence],
    amenities: Mapping[str, IMDFAmenity],
    buildings: Mapping[str, IMDFBuilding],
    footprints: Mapping[str, IMDFFootprint],
    addresses: Mapping[str, IMDFAddress],
    kiosks: Mapping[str, Collection[IMDFKiosk]],
    openings: Mapping[str, Collection[IMDFOpening]],
    sections: Mapping[str, Collection[IMDFSection]],
    units: Mapping[str, Collection[IMDFUnit]],
    anchors: Mapping[str, Collection[IMDFAnchor]],
    occupants: Mapping[str, Collection[IMDFOccupant]],
    fixtures: Mapping[str, Collection[IMDFFixture]],
    details: Mapping[str, Collection[IMDFDetail]],
) -> Mapping[str, MIDFRelationship]:
    relationships = {}
    _logger.error(
        f"Linking relationships from {len(imdf_dict[IMDFFeatureType.relationship])} relationships"
    )

    flattened_units = {unit.id: unit for level in units.values() for unit in level}
    flattened_anchors = {anchor.id: anchor for a in anchors.values() for anchor in a}
    flattened_occupants = {
        occupant.id: occupant for o in occupants.values() for occupant in o
    }
    flattened_fixtures = {
        fixture.id: fixture for level in fixtures.values() for fixture in level
    }
    flattened_sections = {
        section.id: section for level in sections.values() for section in level
    }
    flattened_openings = {
        opening.id: opening for level in openings.values() for opening in level
    }
    flattened_kiosks = {kiosk.id: kiosk for level in kiosks.values() for kiosk in level}
    flattened_details = {
        detail.id: detail for level in details.values() for detail in level
    }

    for relationship in imdf_dict[IMDFFeatureType.relationship]:
        relationship: IMDFRelationship

        relationships[relationship.id] = MIDFRelationship(
            id=relationship.id,
            category=relationship.category,
            direction=relationship.direction,
            geometry=relationship.geometry,
            origin=(
                resolve_feature_reference(
                    relationship.origin,
                    levels=levels,
                    geofences=geofences,
                    amenities=amenities,
                    buildings=buildings,
                    footprints=footprints,
                    addresses=addresses,
                    kiosks=flattened_kiosks,
                    openings=flattened_openings,
                    sections=flattened_sections,
                    units=flattened_units,
                    anchors=flattened_anchors,
                    occupants=flattened_occupants,
                    fixtures=flattened_fixtures,
                    details=flattened_details,
                )
                if relationship.origin
                else None
            ),
            intermediary=(
                [
                    (
                        resolve_feature_reference(
                            r,
                            levels=levels,
                            geofences=geofences,
                            amenities=amenities,
                            buildings=buildings,
                            footprints=footprints,
                            addresses=addresses,
                            kiosks=flattened_kiosks,
                            openings=flattened_openings,
                            sections=flattened_sections,
                            units=flattened_units,
                            anchors=flattened_anchors,
                            occupants=flattened_occupants,
                            fixtures=flattened_fixtures,
                            details=flattened_details,
                        )
                        if r
                        else None
                    )
                    for r in relationship.intermediary
                ]
                if relationship.intermediary
                else None
            ),
            destination=(
                resolve_feature_reference(
                    relationship.destination,
                    levels=levels,
                    geofences=geofences,
                    amenities=amenities,
                    buildings=buildings,
                    footprints=footprints,
                    addresses=addresses,
                    kiosks=flattened_kiosks,
                    openings=flattened_openings,
                    sections=flattened_sections,
                    units=flattened_units,
                    anchors=flattened_anchors,
                    occupants=flattened_occupants,
                    fixtures=flattened_fixtures,
                    details=flattened_details,
                )
                if relationship.destination
                else None
            ),
            hours=relationship.hours,  # TODO: PARSE
        )

    return relationships
