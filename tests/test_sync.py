import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_package_data_matches_root_data():
    root = (ROOT / "data" / "phones.json").read_bytes()
    packaged = (ROOT / "casefinder" / "data" / "phones.json").read_bytes()
    assert hashlib.sha256(root).hexdigest() == hashlib.sha256(packaged).hexdigest(), (
        "casefinder/data/phones.json is stale — run: "
        "cp data/phones.json casefinder/data/phones.json"
    )
