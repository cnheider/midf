import json
import logging
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

_logger = logging.getLogger(__name__)

IGNORE_THIS = """
  "clickable": true,
  "color": "#8595bd",
  "dotMaxZoom": 25,
  "dotMinZoom": 18,
  "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 145 145\"><path
  fill=\"currentColor\" d=\"M72.5 145C112.541 145 145 112.541 145 72.5C145 32.4594 112.541 0 72.5 0C32.4594
  0 0 32.4594 0 72.5C0 112.541 32.4594 145 72.5 145Z\"/><path fill=\"white\" d=\"M59.0081 57.38L56.5292
  71.8338C56.3685 72.7672 56.996 73.6544 57.9294 73.8138C58.3009 73.8781 58.6841 73.8177 59.0171
  73.6415L71.9987 66.8183L84.9804 73.6428C85.8187 74.0838 86.855 73.7611 87.296 72.9228C87.4721 72.5885
  87.5326 72.2067 87.4683 71.8338L84.9894 57.38L95.4897 47.1433C96.1686 46.4824 96.1827 45.396 95.5206
  44.7172C95.257 44.4472 94.9124 44.271 94.5396 44.217L80.0266 42.1072L73.5364 28.9571C73.1173 28.1072 72.09
  27.7588 71.2402 28.1767C70.9008 28.3438 70.6269 28.6177 70.4598 28.9571L63.9696 42.1072L49.4566
  44.217C48.5194 44.3533 47.8701 45.2237 48.0064 46.161C48.0604 46.5339 48.2365 46.8797 48.5065
  47.1433L59.0081 57.38Z\"/><path fill=\"white\" d=\"M102.144 73.7238C101.69 73.4024 101.108 73.3214 100.583
  73.5065L71.9985 83.5954L43.4136 73.5065C42.52 73.1915 41.5416 73.6595 41.2266 74.5531C41.1623 74.7369
  41.1289 74.9298 41.1289 75.1239V85.4133C41.1289 86.141 41.5879 86.789 42.2732 87.0307L71.4289
  97.3215C71.7979 97.4526 72.2016 97.4526 72.5706 97.3215L101.726 87.0307C102.412 86.789 102.871 86.141
  102.871 85.4133V75.1239C102.869 74.5672 102.599 74.0452 102.144 73.7238Z\"/><path fill=\"white\"
  d=\"M102.144 94.3053C101.69 93.9838 101.108 93.9028 100.583 94.088L71.9985 104.176L43.4136 94.0867C42.52
  93.7717 41.5416 94.2397 41.2266 95.1333C41.1623 95.3171 41.1289 95.51 41.1289 95.7041V105.994C41.1289
  106.721 41.5879 107.369 42.2732 107.611L71.4289 117.902C71.7979 118.033 72.2016 118.033 72.5706
  117.902L101.724 107.611C102.409 107.369 102.868 106.721 102.868 105.994V95.7041C102.869 95.1474 102.599
  94.6267 102.144 94.3053Z\"/></svg>",
  "iconMaxZoom": 25,
  "iconMinZoom": 19,
  "iconScale": 0.7,
  "id": "376737be-02f0-47cc-ae5a-dde87fdc382f",
  "keywords": [],
  "name": "USO",
  "poiType": "occupants",
  "priority": 0,
  "showInCategoriesList": false,
  "showInSearchResult": true,
  "subCategories": [],
  "titleMaxZoom": 25,
  "titleMinZoom": 19
  """


class PointMapCategory(BaseModel):
    clickable: bool
    color: str
    dotMaxZoom: int
    dotMinZoom: int
    icon: str
    iconMaxZoom: int
    iconMinZoom: int
    iconScale: float
    id: str
    keywords: Optional[List[str]] = None
    name: str
    poiType: str
    priority: int
    showInCategoriesList: bool
    showInSearchResult: bool
    subCategories: Optional[List["PointMapCategory"]] = None
    titleMaxZoom: int
    titleMinZoom: int


def parse_categories(categories_file_path: Path):
    assert categories_file_path.exists()
    assert categories_file_path.is_file()
    assert categories_file_path.suffix == ".json"
    categories = {}
    with open(categories_file_path) as category_file:
        category_dicts = json.load(category_file)

        for cat_dict in category_dicts:
            cat = PointMapCategory(**cat_dict)

            categories[cat.id] = cat

    print(categories)


if __name__ == "__main__":
    parse_categories(Path(__file__).parent / "data" / "Categories.json")
