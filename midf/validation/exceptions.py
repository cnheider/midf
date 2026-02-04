class IMDFValidationError(Exception):
    """Base exception class for all IMDF validation errors.

    This exception includes both a message and an optional feature_id
    to help identify which feature caused the validation error.
    """

    def __init__(self, message: str, feature_id: str = None):
        self.message = message
        self.feature_id = feature_id
        super().__init__(self.message)


class ViolationError(IMDFValidationError):
    """Base class for IMDF validation violations.

    Violations are critical errors that must be fixed for the IMDF data to be valid.
    """

    pass


class InfoError(IMDFValidationError):
    """Base class for IMDF validation informational messages.

    Info errors are recommendations that don't affect validity but may improve data quality.
    """

    pass


class WarningError(IMDFValidationError):
    """Base class for IMDF validation warnings.

    Warnings indicate potential issues that should be reviewed but don't invalidate the data.
    """

    pass


# Info errors
class ZeroCountOfUnitQualifiedAddressesError(InfoError):
    """Raised when no unit-qualified addresses are found in the IMDF data."""

    pass


# Violation errors
class FeatureIdMustBeStringError(ViolationError):
    """Raised when a feature ID is not a string type."""

    pass


class FeatureIdMustBeUniqueError(ViolationError):
    """Raised when duplicate feature IDs are found in the IMDF data."""

    pass


class FeatureIdMustNotBeEmptyError(ViolationError):
    """Raised when a feature has an empty ID."""

    pass


class FeatureMustHaveFeatureTypeError(ViolationError):
    """Raised when a feature is missing the feature_type property."""

    pass


class FeatureMustHaveIdError(ViolationError):
    """Raised when a feature is missing an ID."""

    pass


class FeatureTypeMustBeStringError(ViolationError):
    """Raised when a feature type is not a string."""

    pass


class FeatureTypeMustNotBeEmptyError(ViolationError):
    """Raised when a feature has an empty feature type."""

    pass


class FileMustBeValidGeoJSONError(ViolationError):
    """Raised when a file is not valid GeoJSON format."""

    pass


class FileMustContainFeatureCollectionError(ViolationError):
    """Raised when a GeoJSON file does not contain a FeatureCollection."""

    pass


class ManifestFileMustBePresentError(ViolationError):
    """Raised when the required manifest file is missing."""

    pass


class NameMustBeStringError(ViolationError):
    """Raised when a name property is not a string."""

    pass


class ReferencedFeatureIDMustBeResolvableError(ViolationError):
    """Raised when a referenced feature ID cannot be found in the dataset."""

    pass


class VenueCountMustBeExactlyOneError(ViolationError):
    """Raised when the dataset does not contain exactly one venue feature."""

    pass


class AddressMustHaveAddressError(ViolationError):
    """Raised when an address feature is missing the required address property."""

    pass


class AddressMustHaveCountryError(ViolationError):
    """Raised when an address feature is missing the required country property."""

    pass


class AddressMustHaveLocalityError(ViolationError):
    """Raised when an address feature is missing the required locality property."""

    pass


class AmenityMustHaveCategoryError(ViolationError):
    """Raised when an amenity feature is missing the required category property."""

    pass


class AmenityMustHaveUnitIdsError(ViolationError):
    """Raised when an amenity feature is missing the required unit_ids property."""

    pass


class AnchorMustHaveGeoreferenceError(ViolationError):  # TODO: NOT a rule!
    """Raised when an anchor feature is missing georeference information."""

    pass


class FootprintMustHaveBuildingIdsError(Exception):
    """Raised when a footprint feature is missing building IDs."""

    pass


class RelationshipMustHaveDirectionError(Exception):
    """Raised when a relationship feature is missing the required direction property."""

    pass


class SectionMustHaveNameError(Exception):  # TODO: NOT a rule!
    """Raised when a section feature is missing a name."""

    pass


class ManifestMustHaveGeneratedByError(Exception):
    """Raised when the manifest is missing the required generated_by property."""

    pass


class ManifestMustHaveVersionError(Exception):
    """Raised when the manifest is missing the required version property."""

    pass


class ManifestMustHaveCreatedDateError(Exception):
    """Raised when the manifest is missing the required created date."""

    pass


class ManifestMustHaveLanguageError(Exception):
    """Raised when the manifest is missing the required language property."""

    pass


class BuildingMustHaveNameError(ViolationError):
    """Raised when a building feature is missing the required name property."""

    pass


class DetailMustHaveCategoryError(ViolationError):
    """Raised when a detail feature is missing the required category property."""

    pass


class FixtureMustHaveCategoryError(ViolationError):
    """Raised when a fixture feature is missing the required category property."""

    pass


class FixtureMustHaveLevelIdError(ViolationError):
    """Raised when a fixture feature is missing the required level_id property."""

    pass


class FeatureGeometryTypeInvalidError(Exception):
    """Raised when a feature has an invalid geometry type."""

    ...


class FootprintMustHaveBuildingIdError(ViolationError):
    """Raised when a footprint feature is missing the required building_id property."""

    pass


class GeofenceMustHaveCategoryError(ViolationError):
    """Raised when a geofence feature is missing the required category property."""

    pass


class KioskMustHaveCategoryError(ViolationError):
    """Raised when a kiosk feature is missing the required category property."""

    pass


class KioskMustHaveLevelIdError(ViolationError):
    """Raised when a kiosk feature is missing the required level_id property."""

    pass


class LevelMustHaveOrdinalError(ViolationError):
    """Raised when a level feature is missing the required ordinal property."""

    pass


class LevelMustHaveShortNameError(ViolationError):
    """Raised when a level feature is missing the required short_name property."""

    pass


class OccupantMustHaveCategoryError(ViolationError):
    """Raised when an occupant feature is missing the required category property."""

    pass


class OccupantMustHaveNameError(ViolationError):
    """Raised when an occupant feature is missing the required name property."""

    pass


class OpeningMustHaveCategoryError(ViolationError):
    """Raised when an opening feature is missing the required category property."""

    pass


class RelationshipMustHaveCategoryError(ViolationError):
    """Raised when a relationship feature is missing the required category property."""

    pass


class RelationshipMustHaveDestinationError(ViolationError):
    """Raised when a relationship feature is missing the required destination property."""

    pass


class RelationshipMustHaveOriginError(ViolationError):
    """Raised when a relationship feature is missing the required origin property."""

    pass


class SectionMustHaveCategoryError(ViolationError):
    """Raised when a section feature is missing the required category property."""

    pass


class SectionMustHaveLevelIdError(ViolationError):
    """Raised when a section feature is missing the required level_id property."""

    pass


class UnitMustHaveCategoryError(ViolationError):
    """Raised when a unit feature is missing the required category property."""

    pass


class UnitMustHaveLevelIdError(ViolationError):
    """Raised when a unit feature is missing the required level_id property."""

    pass


class VenueMustHaveAddressIdError(ViolationError):
    """Raised when a venue feature is missing the required address_id property."""

    pass


class VenueMustHaveCategoryError(ViolationError):
    """Raised when a venue feature is missing the required category property."""

    pass


class VenueMustHaveNameError(ViolationError):
    """Raised when a venue feature is missing the required name property."""

    pass


# Warning errors
class AddressHasDissimilarProvinceCodeError(WarningError):
    """Raised when address province codes are inconsistent across the dataset."""

    pass


class AddressMustBeDistinctError(WarningError):
    """Raised when duplicate addresses are found in the IMDF data."""

    pass


class AddressShouldHavePostalCodeError(WarningError):
    """Raised when an address is missing a postal code."""

    pass


class AmenityNameShouldBeProvidedError(WarningError):
    """Raised when an amenity feature is missing a name property."""

    pass


class AnchorShouldHaveAddressIdError(WarningError):
    """Raised when an anchor feature is missing an address_id reference."""

    pass


class AnchorShouldHaveUnitIdError(WarningError):
    """Raised when an anchor feature is missing a unit_id reference."""

    pass


class BuildingAddressIdShouldBeProvidedError(WarningError):
    """Raised when a building feature is missing an address_id reference."""

    pass


class BuildingShouldHaveDisplayPointError(WarningError):
    """Raised when a building feature is missing a display_point property."""

    pass


class DetailShouldHaveLevelIdError(WarningError):
    """Raised when a detail feature is missing a level_id reference."""

    pass


class FixtureShouldHaveAnchorIdError(WarningError):
    """Raised when a fixture feature is missing an anchor_id reference."""

    pass


class GeofenceShouldHaveDisplayPointError(WarningError):
    """Raised when a geofence feature is missing a display_point property."""

    pass


class KioskShouldHaveDisplayPointError(WarningError):
    """Raised when a kiosk feature is missing a display_point property."""

    pass


class LevelShouldHaveAddressIdError(WarningError):
    """Raised when a level feature is missing an address_id reference."""

    pass


class LevelShouldHaveBuildingIdsError(WarningError):
    """Raised when a level feature is missing building_ids references."""

    pass


class LevelShouldHaveDisplayPointError(WarningError):
    """Raised when a level feature is missing a display_point property."""

    pass


class OccupantShouldHaveAddressIdError(WarningError):
    """Raised when an occupant feature is missing an address_id reference."""

    pass


class OccupantShouldHaveDisplayPointError(WarningError):
    """Raised when an occupant feature is missing a display_point property."""

    pass


class OccupantShouldHaveUnitIdsError(WarningError):
    """Raised when an occupant feature is missing unit_ids references."""

    pass


class OpeningShouldHaveDisplayPointError(WarningError):
    """Raised when an opening feature is missing a display_point property."""

    pass


class OpeningShouldHaveLevelIdError(WarningError):
    """Raised when an opening feature is missing a level_id reference."""

    pass


class RelationshipShouldHaveDisplayPointError(WarningError):
    """Raised when a relationship feature is missing a display_point property."""

    pass


class SectionShouldHaveDisplayPointError(WarningError):
    """Raised when a section feature is missing a display_point property."""

    pass


class UnitShouldHaveDisplayPointError(WarningError):
    """Raised when a unit feature is missing a display_point property."""

    pass


class VenueShouldHaveDisplayPointError(WarningError):
    """Raised when a venue feature is missing a display_point property."""

    pass


# Additional Violation errors
class GeometryMustBeValidError(ViolationError):
    """Raised when a feature has invalid geometry."""

    pass


class GeometryTypeMustBeValidError(ViolationError):
    """Raised when a feature has an invalid geometry type."""

    pass


class PropertiesMustBeValidJSONError(ViolationError):
    """Raised when feature properties are not valid JSON."""

    pass


class RequiredPropertiesMustBePresentError(ViolationError):
    """Raised when a feature is missing required properties."""

    pass


class PropertyValuesMustBeValidError(ViolationError):
    """Raised when property values do not meet validation requirements."""

    pass


class CoordinateReferenceSystemMustBeWGS84Error(ViolationError):
    """Raised when the coordinate reference system is not WGS84."""

    pass


class FeatureCollectionMustContainFeaturesError(ViolationError):
    """Raised when a FeatureCollection does not contain any features."""

    pass


class FeatureMustHaveGeometryError(ViolationError):
    """Raised when a feature is missing geometry."""

    pass


class FeatureMustHavePropertiesError(ViolationError):
    """Raised when a feature is missing properties."""

    pass


class AltitudeMustBeValidNumberError(ViolationError):
    """Raised when an altitude value is not a valid number."""

    pass


class CategoryMustBeValidError(ViolationError):
    """Raised when a category value is not valid for the feature type."""

    pass


class DisplayPointMustBeValidPointError(ViolationError):
    """Raised when a display_point is not a valid Point geometry."""

    pass


class RestrictionMustBeValidError(ViolationError):
    """Raised when a restriction value is not valid."""

    pass


class AccessibilityMustBeValidError(ViolationError):
    """Raised when an accessibility value is not valid."""

    pass


class HoursMustBeValidError(ViolationError):
    """Raised when hours information is not in valid format."""

    pass


class PhoneMustBeValidError(ViolationError):
    """Raised when a phone number is not in valid format."""

    pass


class WebsiteMustBeValidURLError(ViolationError):
    """Raised when a website URL is not valid."""

    pass


class CorrelationIdMustBeValidError(ViolationError):
    """Raised when a correlation_id is not valid."""

    pass


class AddressUnitMustBeValidError(ViolationError):
    """Raised when an address unit value is not valid."""

    pass


class PostalCodeMustBeValidError(ViolationError):
    """Raised when a postal code format is not valid."""

    pass


class ProvinceMustBeValidError(ViolationError):
    """Raised when a province value is not valid."""

    pass


class RegionMustBeValidError(ViolationError):
    """Raised when a region value is not valid."""

    pass


class SubregionMustBeValidError(ViolationError):
    """Raised when a subregion value is not valid."""

    pass


class TimeZoneMustBeValidError(ViolationError):
    """Raised when a timezone value is not valid."""

    pass


class AnchorLatitudeMustBeValidError(ViolationError):
    """Raised when an anchor latitude value is not valid."""

    pass


class AnchorLongitudeMustBeValidError(ViolationError):
    """Raised when an anchor longitude value is not valid."""

    pass


class BuildingHeightMustBeValidError(ViolationError):
    """Raised when a building height value is not valid."""

    pass


class LevelOrdinalMustBeUniqueError(ViolationError):
    """Raised when duplicate level ordinal values are found."""

    pass


class OutdoorMustBeBooleanError(ViolationError):
    """Raised when an outdoor property is not a boolean value."""

    pass


class RelationshipFromMustBeValidError(ViolationError):
    """Raised when a relationship 'from' reference is not valid."""

    pass


class RelationshipToMustBeValidError(ViolationError):
    """Raised when a relationship 'to' reference is not valid."""

    pass


class LevelOrdinalMustBeIntegerError(ViolationError):
    """Raised when a level ordinal is not an integer value."""

    pass


class LevelShortNameMustNotBeEmptyError(ViolationError):
    """Raised when a level short_name is empty."""

    pass


class RelationshipDirectionMustBeValidError(ViolationError):
    """Raised when a relationship direction value is not valid."""

    pass


class ManifestVersionMustBeValidError(ViolationError):
    """Raised when the manifest version is not valid."""

    pass


class ManifestCreatedDateMustBeValidError(ViolationError):
    """Raised when the manifest created date is not valid."""

    pass


class ManifestGeneratedByMustNotBeEmptyError(ViolationError):
    """Raised when the manifest generated_by field is empty."""

    pass


class ManifestLanguageMustBeValidError(ViolationError):
    """Raised when the manifest language code is not valid."""

    pass


# Additional Warning errors
class AltitudeReferenceMustBeValidError(WarningError):
    """Raised when an altitude reference value is not valid."""

    pass


class AnchorPositionMustBeWithinVenueError(WarningError):
    """Raised when an anchor position is not within the venue boundaries."""

    pass


class BuildingHeightShouldBeProvidedError(WarningError):
    """Raised when a building feature is missing height information."""

    pass


class DisplayPointShouldBeProvidedError(WarningError):
    """Raised when a feature is missing a recommended display_point property."""

    pass


class FeatureShouldHaveNameError(WarningError):
    """Raised when a feature is missing a recommended name property."""

    pass


class LevelOrdinalShouldBeSequentialError(WarningError):
    """Raised when level ordinals are not sequential."""

    pass


class OpeningHeightShouldBeProvidedError(WarningError):
    """Raised when an opening feature is missing height information."""

    pass


class OpeningWidthShouldBeProvidedError(WarningError):
    """Raised when an opening feature is missing width information."""

    pass


class RelationshipShouldHaveOrderError(WarningError):
    """Raised when a relationship feature is missing an order property."""

    pass


class UnitShouldHaveAddressIdError(WarningError):
    """Raised when a unit feature is missing an address_id reference."""

    pass


class FeatureShouldHaveCorrelationIdError(WarningError):
    """Raised when a feature is missing a recommended correlation_id property."""

    pass


class FeatureShouldHaveExternalReferenceError(WarningError):
    """Raised when a feature is missing a recommended external reference."""

    pass


# Additional Info errors
class DuplicateFeatureIdWarningError(InfoError):
    """Raised when duplicate feature IDs are detected (informational)."""

    pass


class FeatureIdFormatRecommendationError(InfoError):
    """Raised when a feature ID format does not follow recommendations."""

    pass


class GeometryPrecisionRecommendationError(InfoError):
    """Raised when geometry precision could be improved."""

    pass


class LanguageCodeRecommendationError(InfoError):
    """Raised when a language code could be more specific or follow recommendations."""

    pass


class NameTranslationRecommendationError(InfoError):
    """Raised when name translations are recommended but missing."""

    pass


class PropertyNameRecommendationError(InfoError):
    """Raised when property names could follow better conventions."""

    pass


class ReferencedFeatureTypeMismatchWarningError(InfoError):
    """Raised when a referenced feature type does not match the expected type."""

    pass


class UnusedAddressWarningError(InfoError):
    """Raised when an address feature is not referenced by any other features."""

    pass


class UnusedAnchorWarningError(InfoError):
    """Raised when an anchor feature is not referenced by any other features."""

    pass


class UnusedBuildingWarningError(InfoError):
    """Raised when a building feature is not referenced by any other features."""

    pass


class UnusedLevelWarningError(InfoError):
    """Raised when a level feature is not referenced by any other features."""

    pass


class UnusedUnitWarningError(InfoError):
    """Raised when a unit feature is not referenced by any other features."""

    pass


class FeatureNameShouldBeTranslatedError(InfoError):
    """Raised when feature names should be translated for better localization."""

    pass


class FeaturePropertiesShouldUseRecommendedNamesError(InfoError):
    """Raised when feature properties should use recommended naming conventions."""

    pass


# Add any additional rules that might be in the CSV but not listed here


class BuildingMustHaveCategoryError(ViolationError):
    """Raised when a building feature is missing the required category property."""

    pass


# ... (add any other new exception classes here)
