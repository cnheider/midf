import json
import logging
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Collection, List, Union

from midf.imdf_model import (
    IMDFFeature,
    IMDFManifest,
)
from .dataframe_loading import (
    load_imdf_addresses,
    load_imdf_amenities,
    load_imdf_anchors,
    load_imdf_buildings,
    load_imdf_details,
    load_imdf_fixtures,
    load_imdf_footprints,
    load_imdf_geofences,
    load_imdf_kiosks,
    load_imdf_levels,
    load_imdf_occupants,
    load_imdf_openings,
    load_imdf_relationships,
    load_imdf_sections,
    load_imdf_units,
    load_imdf_venues,
)

_logger = logging.getLogger(__name__)

__all__ = ["load_imdf", "MANIFEST_KEY"]

MANIFEST_KEY = "manifest"


def load_imdf(
    imdf_file_path: Path,
) -> dict[str, Union[IMDFManifest, Collection[IMDFFeature]]]:
    from zipfile import ZipFile
    import geopandas

    assert imdf_file_path.exists()
    assert imdf_file_path.is_file()
    assert imdf_file_path.suffix == ".zip"

    dataframes = {}
    manifest = None

    with ZipFile(imdf_file_path) as zf:
        for file in zf.namelist():
            z_file_path = Path(file)
            if z_file_path.suffix == ".geojson":  # optional filtering by filetype
                with zf.open(file) as f:
                    try:
                        feature_name = z_file_path.stem
                        if False:
                            with tempfile.TemporaryDirectory() as tmp_dir:
                                tmp_file = Path(tmp_dir) / f"{feature_name}.geojson"
                                with open(tmp_file, "wb") as ft:
                                    a = f.read()
                                    ft.write(a)

                                df = geopandas.read_file(tmp_file, engine="fiona")

                                dataframes[feature_name] = df
                        else:
                            df = geopandas.read_file(f, engine="fiona")

                            dataframes[feature_name] = df
                    except Exception as e:
                        _logger.error(f"Failed to load {file}: {e}")
                        if False:
                            raise e

            elif z_file_path.suffix == ".json":
                with zf.open(file) as f:
                    assert manifest is None
                    manifest_file_content = json.loads(f.read())
                    if isinstance(manifest_file_content, List):
                        _logger.error(f"{file} is a list, expected a dict")
                        if len(manifest_file_content) == 1:
                            manifest_file_content = manifest_file_content[0]
                            _logger.error(
                                f"Using first and only element: {manifest_file_content}"
                            )
                    manifest = IMDFManifest(**manifest_file_content)
                    _logger.error(f"Successfully loaded manifest from {file}")

            else:
                _logger.error(f"{file} was skipped")

    out = defaultdict(list)
    if manifest is not None:
        out[MANIFEST_KEY].append(manifest)

    load_imdf_venues(dataframes, out)

    load_imdf_buildings(dataframes, out)

    load_imdf_footprints(dataframes, out)

    load_imdf_fixtures(dataframes, out)

    load_imdf_units(dataframes, out)

    load_imdf_levels(dataframes, out)

    load_imdf_sections(dataframes, out)

    load_imdf_occupants(dataframes, out)

    load_imdf_openings(dataframes, out)

    load_imdf_relationships(dataframes, out)

    load_imdf_kiosks(dataframes, out)

    load_imdf_details(dataframes, out)

    load_imdf_anchors(dataframes, out)

    load_imdf_geofences(dataframes, out)

    load_imdf_addresses(dataframes, out)

    load_imdf_amenities(dataframes, out)

    return out
