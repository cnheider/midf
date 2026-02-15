from collections import defaultdict
from typing import Dict, List

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFManifest
from midf.validation.exceptions import (
    IMDFValidationError,
    InfoError,
    ViolationError,
    WarningError,
)
from midf.validation.features import (
    AddressValidator,
    AmenityValidator,
    AnchorValidator,
    BuildingValidator,
    DetailValidator,
    FixtureValidator,
    FootprintValidator,
    GeofenceValidator,
    KioskValidator,
    LevelValidator,
    ManifestValidator,
    OccupantValidator,
    OpeningValidator,
    RelationshipValidator,
    SectionValidator,
    UnitValidator,
    VenueValidator,
)


class IMDFValidator:

    def __init__(self):
        self.validators = {
            IMDFFeatureType.address: AddressValidator(),
            IMDFFeatureType.amenity: AmenityValidator(),
            IMDFFeatureType.anchor: AnchorValidator(),
            IMDFFeatureType.building: BuildingValidator(),
            IMDFFeatureType.detail: DetailValidator(),
            IMDFFeatureType.fixture: FixtureValidator(),
            IMDFFeatureType.footprint: FootprintValidator(),
            IMDFFeatureType.geofence: GeofenceValidator(),
            IMDFFeatureType.kiosk: KioskValidator(),
            IMDFFeatureType.level: LevelValidator(),
            IMDFFeatureType.occupant: OccupantValidator(),
            IMDFFeatureType.opening: OpeningValidator(),
            IMDFFeatureType.relationship: RelationshipValidator(),
            IMDFFeatureType.section: SectionValidator(),
            IMDFFeatureType.unit: UnitValidator(),
            IMDFFeatureType.venue: VenueValidator(),
        }
        self.manifest_validator = ManifestValidator()

    def validate_dataset(
        self, imdf_dict: Dict[str, List[IMDFFeature]], manifest: IMDFManifest
    ) -> Dict[str, List[IMDFValidationError]]:
        errors = defaultdict(list)

        # Validate manifest
        try:
            manifest_errors = self.manifest_validator.validate(manifest)
            errors["manifest"].extend(manifest_errors)
        except IMDFValidationError as e:
            errors["manifest"].append(e)

        # Validate features
        for feature_type, features in imdf_dict.items():
            validator = self.validators.get(feature_type)
            if validator:
                for feature in features:
                    try:
                        validator.validate(feature)
                    except IMDFValidationError as e:
                        errors[feature_type].append(e)

        # Validate relationships
        relationship_validator = self.validators.get(IMDFFeatureType.relationship)
        if relationship_validator:
            try:
                relationship_errors = relationship_validator.validate_relationships(
                    imdf_dict
                )
                errors[IMDFFeatureType.relationship].extend(relationship_errors)
            except IMDFValidationError as e:
                errors[IMDFFeatureType.relationship].append(e)

        return self._categorize_errors(errors)

    def _categorize_errors(
        self, errors: Dict[str, List[IMDFValidationError]]
    ) -> Dict[str, List[IMDFValidationError]]:
        categorized_errors = {"violations": [], "warnings": [], "info": []}

        for feature_type, error_list in errors.items():
            for error in error_list:
                if isinstance(error, ViolationError):
                    categorized_errors["violations"].append(error)
                elif isinstance(error, WarningError):
                    categorized_errors["warnings"].append(error)
                elif isinstance(error, InfoError):
                    categorized_errors["info"].append(error)

        return categorized_errors
