import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_pyproject_declares_metadata():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for needle in (
        'name = "casefinder"',
        "requires-python",
        "MIT",
        "Homepage",
        "casefinder = ",
    ):
        assert needle in text, f"pyproject.toml missing {needle!r}"


def test_license_present():
    assert (ROOT / "LICENSE").exists()


def test_readme_links_the_tool():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "https://allsmartaccessories.com/tools/case-checker/" in text
    assert "pip install casefinder" in text
