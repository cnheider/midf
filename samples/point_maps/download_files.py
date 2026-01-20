import base64
import json
import logging
import zlib
from json import JSONDecodeError
from pathlib import Path

import requests
import tqdm

from warg import clean_string, ensure_existence

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

map_id_edit_urls = {
    "DUB Airport_OLD": "https://cms.point-maps.com/map/cknqfsbg1004w0cmd6hsz9t34",
    "Vitra Campus": "https://cms.point-maps.com/map/ckp7a6ra200h608l8164n36ew",
    "SUSS_SPATIAL": "https://cms.point-maps.com/map/cku890j8o007o08lddkrw9135",
    "AIFA Map": "https://cms.point-maps.com/map/ckusuz2q6005s09jq9a1fbbdq",
    "Dymocks Sydney": "https://cms.point-maps.com/map/ckuy590t8002n08l58qlv4tz2",
    "National Gallery_1": "https://cms.point-maps.com/map/ckv3g8kql014n08mg6p7f6ppo",  #
    "Kansas International Airport - New": "https://cms.point-maps.com/map/ckyzmt9cd00hk09lbggco2pqy",  #
    "IMDA": "https://cms.point-maps.com/map/cl4ewqmrv01v309l3ab4th0af",  #
    "SJII": "https://cms.point-maps.com/map/clakmo5yc006008lc3fcn633o",  #
    "Coomalie": "https://cms.point-maps.com/map/cle3xo6xy003108kygmntakyf",  #
    "Temasek": "https://cms.point-maps.com/map/clnssorc7000608mu40r3gviz",  #
    "SUSS Wayfinding": "https://cms.point-maps.com/map/clprxosy8000x0bie7hfrao47",
    "HNL": "https://cms.point-maps.com/map/clr75fdn306sz08jp4awo2qo6",  #
    "ITO": "https://cms.point-maps.com/map/clsu7i9qd00230al3hv6b1du0",  #
    "KOA": "https://cms.point-maps.com/map/clsucr647002f0aicgf2m5y5i",  #
    "LIH": "https://cms.point-maps.com/map/clt6jynwb003f0al49bbo9a9k",  #
    "OGG": "https://cms.point-maps.com/map/cluulpt5500aj08js5jea057g",  #
    "HNM": "https://cms.point-maps.com/map/clven5uf7002a0al0h6n28k9j",  #
    "JHM": "https://cms.point-maps.com/map/clven6ndq000t0ajxatp77b61",  #
    "MKK": "https://cms.point-maps.com/map/clven7e6i006n0ajx5tlhhpdp",  #
    "LNY": "https://cms.point-maps.com/map/clven86xb005f09jyesprfcp9",  #
    "LUP": "https://cms.point-maps.com/map/clvgg6sdd001u09kz0hxm9rcn",  #
    "SIT Campus": "https://cms.point-maps.com/map/clvqbidp9005f07l68g0vgk6q",
    "SIT Visitor": "https://cms.point-maps.com/map/clvqg9249004h0ajjhvg4a5j5",
    "BTRTS": "https://cms.point-maps.com/map/clzklq2ox01h40akwcbugedsa",  #
    "Berlin Brandenburg Airport": "https://cms.point-maps.com/map/cm1z1rucy01hr0amlh7nb5zuu",  #
    "Zurich Airport": "https://cms.point-maps.com/map/cm2xdja47008709mn4ccb0ch1",  #
    "MP Demo": "https://cms.point-maps.com/map/cm6aimazu009p09la1d6439cp",  #
}

map_ids = {
    n: m.split("https://cms.point-maps.com/map/")[-1]
    for n, m in map_id_edit_urls.items()
}

a = "https://cms.point-maps.com/api/v1/map/{0}/files/latest"
if False:
    a += "?decompress=true"

download_destination = Path(__file__).parent / "exclude2"

# shutil.rmtree(download_destination, ignore_errors=True)

exclude_path = ensure_existence(download_destination)


def download_files():

    for map_name, map_id in tqdm.tqdm(map_ids.items()):
        _logger.info(f"Downloading {map_name}")
        h = a.format(map_id)
        req = requests.get(h)
        folder = ensure_existence(exclude_path / map_name.lower().replace(" ", "_"))

        try:
            json_rep = req.json()
            out = {}
            for k, v in tqdm.tqdm(json_rep.items()):
                if "compressed" in v:
                    dec = base64.b64decode(v["compressed"])
                    dec = zlib.decompress(dec).decode()
                    out[k] = dec
                else:
                    out[k] = json.dumps(v)

            for f_name, f_content in out.items():
                try:
                    with open(
                        (folder / clean_string(f_name)).with_suffix(".json"),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(f_content)
                except Exception as e:
                    _logger.error(f"Error writing {f_name} in {map_name}: {e}")

        except JSONDecodeError as e:
            _logger.error(e)
            logging.error(f"Error downloading {map_name} : {map_id}")


if __name__ == "__main__":
    download_files()
