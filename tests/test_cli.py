import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "casefinder", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_list_brands():
    r = run("brands")
    assert r.returncode == 0, r.stderr
    assert "Apple" in r.stdout
    assert "Samsung" in r.stdout


def test_models_for_brand():
    r = run("models", "--brand", "Samsung")
    assert r.returncode == 0, r.stderr
    assert "Galaxy S24 Ultra" in r.stdout


def test_check_known_phone():
    r = run("check", "iPhone 17")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "Compatible case types" in out
    assert "rugged" in out
    assert "allsmartaccessories.com" in out, "must link back to the site"


def test_check_unknown_phone_fails_cleanly():
    r = run("check", "Nokia 3310")
    assert r.returncode != 0
    assert "not found" in (r.stdout + r.stderr).lower()


def test_check_json_output():
    r = run("check", "iPhone 17", "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["model"] == "iPhone 17"
    assert data["postUrl"].startswith("https://allsmartaccessories.com/")
