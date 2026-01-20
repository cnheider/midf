import logging
import pickle
from datetime import datetime
from pathlib import Path

from loaders import (
    load_basemap,
    load_building,
    load_category,
    load_dictionary,
    load_fixture,
    load_level,
    load_occupant,
    load_opening,
    load_point,
    load_route,
    load_section,
    load_setting,
    load_style,
    load_unit,
    load_venue,
)
from midf.packaging import package_imdf
from model.enums import PointConsultingFeatureStem
from warg import ensure_existence

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

logging.getLogger("fiona").setLevel(logging.INFO)


class MultipleMatchException(Exception): ...


def imdifify_venue(pc_venue, z):
    target_venue_dir = ensure_existence(z / pc_venue.stem)
    target_imdf_file = target_venue_dir / f"imdf.zip"
    osm_file = target_venue_dir / f"route.osm"
    occupant_package_file = target_venue_dir / "occupant_package.pkl"
    intermediate_rep = {}

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

            if g == PointConsultingFeatureStem.venue and True:
                load_venue(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.fixture and True:
                load_fixture(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.unit and True:
                load_unit(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.building and True:
                load_building(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.level and True:
                load_level(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.occupant and True:
                skip_media = False
                occupant_package = load_occupant(a, intermediate_rep, skip_media)
                if (not skip_media) and (occupant_package is not None):
                    with open(occupant_package_file, "wb") as f:
                        pickle.dump(
                            occupant_package, f, protocol=pickle.HIGHEST_PROTOCOL
                        )

            elif g == PointConsultingFeatureStem.opening and True:
                load_opening(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.section and True:
                load_section(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.point and False:
                load_point(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.basemap and True:
                load_basemap(a, intermediate_rep)

            elif g == PointConsultingFeatureStem.route and True:
                try:
                    load_route(a, osm_file)  # has size effects
                except ValueError as e:
                    _logger.error(f"Failed to load route {a}: {e}")

            elif g == PointConsultingFeatureStem.category and False:
                jgf = load_category(a)

                for ith, v in jgf.items():
                    ...
            elif g == PointConsultingFeatureStem.dictionary and False:
                jgf = load_dictionary(a)

                for ith, v in jgf.items():
                    ...
            elif g == PointConsultingFeatureStem.setting and False:
                jgf = load_setting(a)

                for ith, v in jgf.items():
                    ...
            elif g == PointConsultingFeatureStem.style and False:
                jgf = load_style(a)

                for ith, v in jgf.items():
                    ...
            else:
                if False:
                    raise NotImplementedError("This should never happen")

        else:
            _logger.info(f"{a} was skipped")

    manifest = {
        "version": "0.0.1",
        "created": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
        "generated_by": "Point-Maps By Chen - Reloaded",
        "language": "en-US",
    }
    package_imdf(
        target_imdf_file,
        manifest,
        intermediate_rep,
    )


def to_imdf_venue():
    a = Path(__file__).parent / "fixed_json2"
    z = ensure_existence(a.parent / "imdfication2")

    assert a.exists(), f"{a} does not exist"

    for pc_venue in a.iterdir():
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
                continue

        _logger.info(f"Processing {pc_venue}")

        try:
            imdifify_venue(pc_venue, z)
        except Exception as e:
            _logger.error(f"{pc_venue}: {e}")
            if True:
                raise e


if __name__ == "__main__":

    to_imdf_venue()
