import logging
from pathlib import Path

from .main import fix_geometries, validate_geometries, validate_structure

if __name__ == "__main__":

    def ayusghdyug():
        logging.basicConfig(level=logging.WARNING)

        a = Path(__file__).parent.parent / "exclude2" / "national_gallery_1"
        assert a.exists(), f"{a} does not exist"
        for i in a.iterdir():
            if i.is_file() and i.suffix == ".json":
                try:
                    fix_geometries(i)
                except Exception as e:
                    logging.error(f"invalid gjson: {i} {e}")
                    pass

    ayusghdyug()
