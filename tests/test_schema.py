import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "phones.json"

REQUIRED_TOP = {"version", "generatedFrom", "phones"}
REQUIRED_PHONE = {
    "id",
    "brand",
    "model",
    "releaseYear",
    "dimensionsMm",
    "magsafe",
    "caseTypes",
    "screenProtector",
    "postUrl",
}
VALID_CASE_TYPES = {
    "rugged",
    "clear",
    "slim",
    "wallet",
    "battery",
    "magsafe",
    "kickstand",
    "waterproof",
    "stylish",
    "bumper",
}


@pytest.fixture(scope="module")
def db():
    assert DATA.exists(), f"missing {DATA}"
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_top_level_keys(db):
    assert REQUIRED_TOP <= set(db), REQUIRED_TOP - set(db)


def test_phone_entries_complete(db):
    phones = db["phones"]
    assert len(phones) >= 60, f"expected >=60 models, got {len(phones)}"
    for p in phones:
        missing = REQUIRED_PHONE - set(p)
        assert not missing, f"{p.get('id')}: missing {missing}"


def test_ids_unique(db):
    ids = [p["id"] for p in db["phones"]]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate ids: {dupes}"


def test_case_types_valid(db):
    for p in db["phones"]:
        assert p["caseTypes"], f"{p['id']} has no caseTypes"
        bad = set(p["caseTypes"]) - VALID_CASE_TYPES
        assert not bad, f"{p['id']}: unknown caseTypes {bad}"


def test_dimensions_shape(db):
    for p in db["phones"]:
        d = p["dimensionsMm"]
        if d is None:
            continue
        assert set(d) == {"h", "w", "t"}, f"{p['id']} dimensionsMm keys {set(d)}"
        assert all(isinstance(v, (int, float)) and v > 0 for v in d.values()), p["id"]


def test_post_urls_are_real_site_urls(db):
    for p in db["phones"]:
        u = p["postUrl"]
        assert u.startswith("https://allsmartaccessories.com/"), u
        assert " " not in u and u.endswith("/"), u


def test_no_ocr_artifacts_in_ids(db):
    for p in db["phones"]:
        assert "One Plus" not in p["id"], p["id"]
        assert not p["id"].endswith("+"), p["id"]
