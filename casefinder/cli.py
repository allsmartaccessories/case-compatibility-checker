import argparse
import json
import sys

from . import __version__
from .data import load_phones


def _find(model, phones):
    """Case-insensitive exact match on brand+model, then substring fallback."""
    needle = model.strip().lower()
    for p in phones:
        if f"{p['brand']} {p['model']}".lower() == needle:
            return p
    for p in phones:
        if needle in f"{p['brand']} {p['model']}".lower():
            return p
    return None


def _cmd_brands(phones, _args):
    for brand in sorted({p["brand"] for p in phones}):
        print(brand)
    return 0


def _cmd_models(phones, args):
    rows = [p for p in phones if p["brand"].lower() == args.brand.lower()]
    if not rows:
        print(f"No models found for brand '{args.brand}'", file=sys.stderr)
        return 1
    for p in sorted(rows, key=lambda x: x["model"]):
        print(p["model"])
    return 0


def _cmd_check(phones, args):
    phone = _find(args.model, phones)
    if phone is None:
        print(
            f"'{args.model}' not found. Run `casefinder brands` to see supported brands.",
            file=sys.stderr,
        )
        return 1

    if args.json:
        print(json.dumps(phone, indent=2))
        return 0

    d = phone.get("dimensionsMm") or {}
    print(f"{phone['brand']} {phone['model']} ({phone['releaseYear']})")
    if d:
        print(f"Dimensions: {d['h']} x {d['w']} x {d['t']} mm")
    print(f"MagSafe: {'yes' if phone.get('magsafe') else 'no'}")
    print("Compatible case types:")
    for case_type in phone.get("caseTypes", []):
        print(f"  - {case_type}")

    sp = phone.get("screenProtector") or {}
    if sp.get("type"):
        curved = " (curved)" if sp.get("curved") else ""
        print(f"Screen protector: {sp['type']}{curved}")

    print(f"Recommended cases: {phone['postUrl']}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="casefinder",
        description="Phone case & screen protector compatibility lookup.",
    )
    parser.add_argument(
        "--version", action="version", version=f"casefinder {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("brands", help="list supported brands")

    p_models = sub.add_parser("models", help="list models for a brand")
    p_models.add_argument("--brand", required=True)

    p_check = sub.add_parser("check", help="show compatibility for a phone")
    p_check.add_argument("model")
    p_check.add_argument("--json", action="store_true", help="emit raw JSON")

    args = parser.parse_args(argv)
    phones = load_phones()

    handlers = {
        "brands": _cmd_brands,
        "models": _cmd_models,
        "check": _cmd_check,
    }
    return handlers[args.command](phones, args)
