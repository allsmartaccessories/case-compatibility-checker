import json
import pathlib

_DATA = pathlib.Path(__file__).resolve().parent / "data" / "phones.json"


def load_phones():
    """Return the list of phone dicts from phones.json."""
    with _DATA.open(encoding="utf-8") as fh:
        return json.load(fh)["phones"]
