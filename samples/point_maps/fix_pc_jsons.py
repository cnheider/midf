import json
import logging
import shutil
from pathlib import Path
from typing import Any, Optional

import pandas
import shapely

from model.enums import PointConsultingFeatureStem
from warg import ensure_existence

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class MultipleMatchException(Exception): ...


def drop_invalid_features(p: Path) -> Optional[dict[str, Any]]:
    with open(p) as f:
        json_dict = json.loads(f.read())

    a = pandas.DataFrame.from_records(json_dict["features"])

    invalid_features = []

    if "geometry" in a:
        for i in a["geometry"].values:
            fail = False
            gj = None
            try:
                gj = json.dumps(i)

                g = shapely.from_geojson(gj)

                if False:
                    if not g.is_valid:
                        fail = True

                if g.is_empty:
                    fail = True
            except Exception as e:
                _logger.error(f"{p}:{e}")
                if gj:
                    _logger.error(f"{p}:{gj}")
                fail = True

            if fail:
                invalid_features.append(True)
            else:
                invalid_features.append(False)

        a.drop(a.index[invalid_features], inplace=True)
    else:
        return None

    json_dict["features"] = a.to_dict(orient="records")

    return json_dict


def fix_venue_jsons(pc_venue, target_path):
    target_venue_dir = ensure_existence(target_path / pc_venue.stem)

    for a in pc_venue.iterdir():
        if a.is_file() and a.suffix == ".json":
            s = a.stem
            g = None
            for c in PointConsultingFeatureStem:
                if c.value in s:
                    if g is None:
                        g = c
                    else:
                        raise MultipleMatchException

            assert g is not None, f"{a} did not match any feature type"

            target_file = target_venue_dir / a.name

            if g == PointConsultingFeatureStem.venue and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.fixture and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.unit and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.building and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.level and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.occupant and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.opening and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.section and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.basemap and True:
                l = drop_invalid_features(a)
                if l:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(l))

            elif g == PointConsultingFeatureStem.route and True:
                shutil.copy(a, target_file)

            elif g == PointConsultingFeatureStem.point and True:
                shutil.copy(a, target_file)

            elif g == PointConsultingFeatureStem.category and True:
                shutil.copy(a, target_file)

            elif g == PointConsultingFeatureStem.dictionary and True:
                shutil.copy(a, target_file)

            elif g == PointConsultingFeatureStem.setting and True:
                shutil.copy(a, target_file)

            elif g == PointConsultingFeatureStem.style and True:
                shutil.copy(a, target_file)

            else:
                raise NotImplementedError("This should never happen")

        else:
            _logger.info(f"{a} was skipped")


def fix_pc_venue_jsons():
    source_path = Path(__file__).parent / "exclude2"
    target_path = Path(__file__).parent / "fixed_json2"

    assert source_path.exists(), f"{source_path} does not exist"

    for pc_venue in source_path.iterdir():
        if pc_venue.is_file():
            continue

        if False:
            if pc_venue.stem not in (
                # "national_gallery_1",
                # "suss_wayfinding",
                # "sit_visitor",
                # "suss_spatial",
                # "sit_campus",
                # "btrts",
                # "berlin_brandenburg_airport",
                "zurich_airport"
            ):
                _logger.error(f"skipped {pc_venue.stem}")
                continue

        _logger.info(f"Processing {pc_venue}")

        try:
            fix_venue_jsons(pc_venue, target_path)
        except Exception as e:
            _logger.error(f"{pc_venue}: {e}")


if __name__ == "__main__":

    fix_pc_venue_jsons()
