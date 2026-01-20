from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFGeofence
from midf.model import MIDFGeofence

__all__ = ["link_geofences"]

import logging

_logger = logging.getLogger(__name__)


def link_geofences(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, MIDFGeofence]:
    geofences = {}
    _logger.error(f"Linking {len(imdf_dict[IMDFFeatureType.geofence])} geofences")
    for geofence in imdf_dict[IMDFFeatureType.geofence]:
        geofence: IMDFGeofence
        geofences[geofence.id] = MIDFGeofence(
            id=geofence.id,
            geometry=geofence.geometry,
            category=geofence.category,
            restriction=geofence.restriction,
            accessibility=geofence.accessibility,
            name=geofence.name,
            alt_name=geofence.alt_name,
            correlation_id=geofence.correlation_id,
            display_point=geofence.display_point,
            # buildings=geofence.buildings, # TODO: PARSE
            # levels=geofence.levels, # TODO: PARSE
            # parents=geofence.parents, # TODO: PARSE
        )
    return geofences
