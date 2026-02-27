import logging
import math
import pickle
from pathlib import Path

from midf.conversion import to_mi_solution
from midf.linking import link_imdf
from midf.loading import MANIFEST_KEY, load_imdf
from sync_module.mi import SyncLevel, synchronize
from sync_module.model import OccupantCategory, OccupantTemplate
from sync_module.shared import MIMediaType

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def upload_to_mi():
    data_base = Path(__file__).parent / "imdfication2"

    for pc_venue_dir in data_base.iterdir():
        if False:
            if pc_venue_dir.stem not in (
                # "national_gallery_1",
                # "ogg",
                # "sit_campus",
                # "sit_visitor",
                # "sjii",
                # "suss_wayfinding",
                # "suss_spatial" "temasek",
                "vitra_campus",
                "zurich_airport",
            ):
                continue

        _logger.error(f"Processing {pc_venue_dir}")

        try:
            imdf_dict = load_imdf(pc_venue_dir / "imdf.zip")

            midf_solution = link_imdf(imdf_dict)

            imdf_manifest = imdf_dict.pop(MANIFEST_KEY)[0]

            mi_solution = to_mi_solution(midf_solution)

            occupant_package_file_path = pc_venue_dir / "occupant_package.pkl"
            if occupant_package_file_path.exists():
                with open(occupant_package_file_path, "rb") as f:
                    imdf_pickle = pickle.load(f)
                    for occupant_id, occupant_data in imdf_pickle.items():
                        occupant_template_admin_id = OccupantTemplate.compute_key(
                            name=next(iter(occupant_data["name"].values())),
                            occupant_category_key=OccupantCategory.compute_key(
                                name=occupant_data["category"]
                            ),
                        )
                        occupant_template = mi_solution.occupant_templates.get(
                            occupant_template_admin_id
                        )
                        if occupant_template is None:
                            occupant_template_admin_id = OccupantTemplate.compute_key(
                                name=occupant_id,
                                occupant_category_key=OccupantCategory.compute_key(
                                    name=occupant_data["category"]
                                ),
                            )
                            occupant_template = mi_solution.occupant_templates.get(
                                occupant_template_admin_id
                            )
                        if occupant_template is None:
                            _logger.error(f"No template found for {occupant_id}")
                            continue
                        assert occupant_template is not None, (
                            f"{occupant_template_admin_id} not found in "
                            f"{list(mi_solution.occupant_templates.keys)}"
                        )

                        media_key = ...
                        if occupant_data["images"]:
                            for ith, image_data in enumerate(occupant_data["images"]):
                                image_id = occupant_id + str(ith)
                                media_key = mi_solution.add_media(
                                    image_id, image_data, MIMediaType.jpg
                                )

                        mi_solution.update_occupant_template(
                            occupant_template.key,
                            media_key=media_key,
                            description=occupant_data["description"],
                        )

            osm_file_path = pc_venue_dir / "route.osm"
            if osm_file_path.exists():
                venue_ = next(iter(mi_solution.venues))

                with open(osm_file_path) as f:
                    new_graph_key = mi_solution.update_graph(
                        venue_.graph.key,
                        osm_xml=f.read(),
                        boundary=venue_.polygon.buffer(
                            math.sqrt(venue_.polygon.area) / 2.0
                        ),
                    )

            if True:
                synchronize(
                    mi_solution, sync_level=SyncLevel.venue, include_occupants=True
                )
            else:
                from sync_module.tools.serialisation import to_json

                with open(data_base / "go.json", "w") as f:
                    f.write(to_json(mi_solution))
        except Exception as e:
            _logger.error(f"Failed to process {pc_venue_dir}: {e}")
            if True:
                raise e


if __name__ == "__main__":
    upload_to_mi()
