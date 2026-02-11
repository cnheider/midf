from typing import Collection, Mapping, Union

from midf.enums import IMDFFeatureType
from midf.feature_linking import (
    link_addresses,
    link_anchors,
    link_buildings,
    link_details,
    link_fixtures,
    link_footprints,
    link_geofences,
    link_kiosks,
    link_levels,
    link_occupants,
    link_openings,
    link_relationships,
    link_sections,
    link_units,
    link_venues,
)
from midf.feature_linking.midf_amenities import link_amenities
from midf.imdf_model import (
    IMDFFeature,
    IMDFManifest,
)
from midf.loading import MANIFEST_KEY
from midf.model import (
    MIDFManifest,
    MIDFSolution,
)
from sync_module.mi import from_manager_api_datetime_format


def parse_datetime(created):
    return from_manager_api_datetime_format(created) if created is not None else None


def link_imdf(
    imdf_dict: Mapping[
        Union[str, IMDFFeatureType], Collection[Union[IMDFManifest, IMDFFeature]]
    ],
) -> MIDFSolution:
    """

    :param imdf_dict:
    :type imdf_dict:
    :return:
    :rtype:
    """
    imdf_manifest: IMDFManifest = next(iter(imdf_dict[MANIFEST_KEY]))

    solution = MIDFSolution(
        manifest=MIDFManifest(
            version=imdf_manifest.version,
            created=parse_datetime(imdf_manifest.created),
            generated_by=imdf_manifest.generated_by,
            language=imdf_manifest.language,
            extensions=imdf_manifest.extensions,
        )
    )

    venue_mapping = link_venues(imdf_dict)

    addresses = link_addresses(imdf_dict, venue_mapping)

    buildings = link_buildings(imdf_dict)

    footprints = link_footprints(buildings, imdf_dict)

    sections = link_sections(imdf_dict)

    occupants = link_occupants(imdf_dict)
    found_occupant_anchors = occupants.keys()

    anchors = link_anchors(found_occupant_anchors, imdf_dict, occupants)

    units = link_units(anchors, imdf_dict)

    amenities = link_amenities(imdf_dict, units)
    details = link_details(imdf_dict)

    anchor_id_mapping = {anchor_.id: anchor_ for a in anchors.values() for anchor_ in a}
    kiosks = link_kiosks(anchor_id_mapping, imdf_dict)

    fixtures = link_fixtures(anchor_id_mapping, imdf_dict)

    openings = link_openings(imdf_dict)

    found_section_levels = sections.keys()
    found_unit_levels = units.keys()
    found_detail_levels = details.keys()
    found_kiosk_levels = kiosks.keys()
    found_fixture_levels = fixtures.keys()
    found_opening_levels = openings.keys()

    levels = link_levels(
        buildings=buildings,
        details=details,
        fixtures=fixtures,
        found_detail_levels=found_detail_levels,
        found_fixture_levels=found_fixture_levels,
        found_kiosk_levels=found_kiosk_levels,
        found_opening_levels=found_opening_levels,
        found_section_levels=found_section_levels,
        found_unit_levels=found_unit_levels,
        imdf_dict=imdf_dict,
        kiosks=kiosks,
        openings=openings,
        sections=sections,
        units=units,
    )

    geofences = link_geofences(imdf_dict)

    relationships = link_relationships(
        imdf_dict,
        levels=levels,
        geofences=geofences,
        amenities=amenities,
        buildings=buildings,
        footprints=footprints,
        addresses=addresses,
        kiosks=kiosks,
        openings=openings,
        sections=sections,
        units=units,
        anchors=anchors,
        occupants=occupants,
        fixtures=fixtures,
        details=details,
    )

    solution.relationships = list(relationships.values())
    solution.amenities = list(amenities.values())
    solution.addresses = list(addresses.values())
    solution.buildings = list(buildings.values())
    solution.footprints = list(footprints.values())
    solution.levels = list(levels.values())
    solution.geofences = list(geofences.values())

    return solution
