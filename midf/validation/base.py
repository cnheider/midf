from abc import ABC, abstractmethod

import shapely

from midf.imdf_model import (
    IMDFAddress,
    IMDFAmenity,
    IMDFAnchor,
    IMDFDetail,
    IMDFFeature,
    IMDFFixture,
    IMDFFootprint,
    IMDFGeofence,
    IMDFKiosk,
    IMDFLevel,
    IMDFOpening,
    IMDFSection,
    IMDFUnit,
    IMDFVenue,
)
from .exceptions import (
    FeatureGeometryTypeInvalidError,
    GeometryMustBeValidError,
)


class ValidationError(Exception): ...


def get_expected_geometry_types(feature: IMDFFeature) -> tuple:
    geometry_map = {
        IMDFAddress: (shapely.geometry.Point,),
        IMDFAmenity: (shapely.geometry.Point, shapely.geometry.Polygon),
        IMDFAnchor: (shapely.geometry.Point,),
        # IMDFBuilding: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFDetail: (shapely.geometry.LineString, shapely.geometry.Polygon),
        IMDFFixture: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFFootprint: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFGeofence: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFKiosk: (shapely.geometry.Polygon,),
        IMDFLevel: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFOpening: (shapely.geometry.LineString, shapely.geometry.Point),
        IMDFSection: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFUnit: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
        IMDFVenue: (shapely.geometry.Polygon, shapely.geometry.MultiPolygon),
    }
    return geometry_map.get(
        type(feature),
        (
            shapely.geometry.Polygon,
            shapely.geometry.MultiPolygon,
            shapely.geometry.LineString,
            shapely.geometry.Point,
        ),
    )


def validate_geometry(feature: IMDFFeature) -> None:
    expected_geometry_types = get_expected_geometry_types(feature)

    if hasattr(feature, "geometry"):
        if feature.geometry:
            if not isinstance(feature.geometry, expected_geometry_types):
                raise FeatureGeometryTypeInvalidError(
                    f"Invalid geometry type for {feature.id, type(feature)}. Expected {expected_geometry_types}, got "
                    f"{type(feature.geometry)}",
                    feature.id,
                )

            if not feature.geometry.is_valid:
                raise GeometryMustBeValidError(
                    f"Invalid geometry for {feature.id}", feature.id
                )


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, feature: IMDFFeature) -> None:
        pass
