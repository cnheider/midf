from pathlib import Path

import json
import logging
from pydantic import BaseModel
from typing import Optional

_logger = logging.getLogger(__name__)
IGNORE_THIS = """
    },
    "ede9cbd5-681d-42f5-b8b1-7d0a205c8ab2": {
        "roof": false,
        "floor": true,
        "solid": false,
        "walls": true,
        "priority": 0,
        "roofColor": "#202020",
        "floorColor": "#ffe5cc",
        "roofHeight": 2.5,
        "wallsColor": "#dcdddc",
        "wallsWidth": 0.1,
        "wallsHeight": 2.5
    },
    "f3fde1bb-4615-4b44-a9fc-f3995e6056aa": {
        "roof": false,
        "floor": true,
        "solid": false,
        "walls": true,
        "priority": 0,
        "roofColor": "#202020",
        "floorColor": "#00A499",
        "roofHeight": 2.5,
        "wallsColor": "#dcdddc",
        "wallsWidth": 0.1,
        "wallsHeight": 2.5
    }
}
"""


class PointMapStyle(BaseModel):
    floor: bool
    walls: bool

    priority: int

    floorColor: str
    wallsColor: str

    wallsHeight: float

    solid: Optional[bool] = None
    roof: Optional[bool] = None
    roofColor: Optional[str] = None
    roofHeight: Optional[float] = None
    wallsWidth: Optional[float] = None


def parse_styles(style_file_path: Path):
    assert style_file_path.exists()
    assert style_file_path.is_file()
    assert style_file_path.suffix == ".json"
    styles = {}
    with open(style_file_path) as style_file:
        style_dict = json.load(style_file)

        for k, v in style_dict.items():
            style = PointMapStyle(**v)

            styles[k] = style

    print(styles)


if __name__ == "__main__":
    parse_styles(Path(__file__).parent / "data" / "Styles.json")
