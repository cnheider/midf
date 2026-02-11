from pathlib import Path
from zipfile import ZipFile

import geopandas
import json
import logging
from typing import Collection, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature

_logger = logging.getLogger(__name__)


def prepare_feature_collection(feature_collection: Collection[IMDFFeature]) -> str:
    """

    :param feature_collection:
    :type feature_collection:
    :return:
    :rtype:
    """
    out = []
    for feature in feature_collection:
        out.append(feature.to_imdf_spec_feature())

    df = geopandas.GeoDataFrame(out)

    try:
        return df.to_json()
    except Exception as e:
        _logger.error(f"{feature_collection}: {e}")
        _logger.info("RETURNING empty FeatureCollection")
        return '{"type": "FeatureCollection", "features": []}'


def package_imdf(
    target_imdf_file: Path,
    manifest: Mapping[str, str],
    feature_collections: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> None:
    """

    :param target_imdf_file:
    :type target_imdf_file:
    :param manifest:
    :type manifest:
    :param feature_collections:
    :type feature_collections:
    :return:
    :rtype:
    """
    with ZipFile(target_imdf_file, "w") as zf:
        zf.writestr("manifest.json", json.dumps(manifest))

        for feature_type, feature_collection in feature_collections.items():
            feature_collection_json = prepare_feature_collection(feature_collection)
            zf.writestr(f"{feature_type.value}.geojson", feature_collection_json)
