import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def _strip_comments(js):
    """Remove block and line comments so the XSS gate can't trip on prose."""
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"(^|\s)//[^\n]*", r"\1", js)


def test_index_exists_and_is_static():
    html = _read("index.html")
    assert "<!DOCTYPE html>" in html
    assert '<script src="app.js"' in html
    assert '<link rel="stylesheet" href="styles.css"' in html


def test_no_external_scripts_or_styles():
    """CSP script-src 'self' is unenforceable if we load third-party assets."""
    html = _read("index.html")
    assert not re.search(r'src="https?://', html), "external script found"
    assert not re.search(r'href="https?://[^"]*\.css', html), "external stylesheet found"


def test_appjs_never_uses_innerhtml():
    """XSS boundary: all rendering must use textContent/createElement."""
    js = _strip_comments(_read("app.js"))
    for bad in (
        "innerHTML",
        "outerHTML",
        "document.write",
        "insertAdjacentHTML",
        "eval(",
    ):
        assert bad not in js, f"app.js must not use {bad}"


def test_appjs_reads_phones_json():
    assert "data/phones.json" in _read("app.js")


def test_headers_file_locks_down_csp():
    h = _read("_headers")
    assert "Content-Security-Policy" in h
    assert "script-src 'self'" in h
    assert "form-action 'none'" in h


def test_index_has_canonical_and_description():
    html = _read("index.html")
    assert 'rel="canonical"' in html
    assert 'name="description"' in html
